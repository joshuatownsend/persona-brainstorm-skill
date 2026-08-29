#!/usr/bin/env python3
"""Verify a persona-brainstorm output document.

Counts what the document claims and what it actually contains, and reports every
disagreement. Nothing here asks a model to assess itself: every number below is
computed from the tables, which is the entire point — the failure this exists to
catch is an agent confidently reporting a figure about its own output that is
wrong.

Usage:  python verify.py PERSONAS.md [--strict]

Exit 0 if no FAILs. --strict also fails on WARNs.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from difflib import SequenceMatcher

FREQ_VOCAB = {
    "many/day", "daily", "weekly", "monthly", "quarterly", "annually",
    "per-incident", "per-release", "per-run", "onboarding",
}
COVERAGE_MARKS = {"✅", "◐", "○"}
# Why-restates-Ask above this ratio is a feature request in costume.
RESTATEMENT_RATIO = 0.62
# Budgets flatter than this look like fairness, which the method names as a tell.
FLATNESS_RATIO = 1.5


@dataclass
class Item:
    n: int
    persona: str
    ask: str
    why: str
    freq: str
    frontier: bool
    coverage: str
    line: int


@dataclass
class Report:
    fails: list[str] = field(default_factory=list)
    warns: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def fail(self, m: str) -> None:
        self.fails.append(m)

    def warn(self, m: str) -> None:
        self.warns.append(m)

    def note(self, m: str) -> None:
        self.notes.append(m)


def split_row(line: str) -> list[str]:
    # A shell pipeline or a regex in an ask is written `foo \| bar`. Splitting on
    # every pipe shifts every field after it and invents failures.
    body = line.strip()
    body = body[1:] if body.startswith("|") else body
    body = body[:-1] if body.endswith("|") and not body.endswith(r"\|") else body
    return [c.strip().replace(r"\|", "|") for c in re.split(r"(?<!\\)\|", body)]


def is_divider(cells: list[str]) -> bool:
    return all(set(c) <= set("-: ") and c for c in cells)


def parse(text: str) -> tuple[dict[str, int], list[Item], dict[str, list[int]], dict, dict]:
    """Return (roster budgets, items, primitive->cited items, claims, slugs)."""
    lines = text.split("\n")
    roster: dict[str, int] = {}
    items: list[Item] = []
    primitives: dict[str, list[int]] = {}
    claims: dict = {}
    slugs: dict[str, dict] = {"persona": {}, "primitive": {}}

    current_persona = None
    citing = None
    in_fence = False

    for i, raw in enumerate(lines, 1):
        if raw.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        # Persona section heading: "### P1 — Role"
        m = re.match(r"###\s+(P\d+)\s*[—-]\s*(.+)", raw)
        if m:
            current_persona = m.group(1)
            continue
        # Any other heading closes the persona section. Without this, a numbered
        # table in the appendix is parsed as more items and charged to whichever
        # persona happened to be last.
        if re.match(r"#{1,3}\s", raw) :
            current_persona = None

        if not raw.lstrip().startswith("|"):
            # Primitive citation: "→ items 3, 7, 12" / "→ items **3, 7, 12**"
            m = re.search(r"→\s*items?\s+([\d,\s*]+)", raw)
            if m and primitives:
                nums = [int(x) for x in re.findall(r"\d+", m.group(1))]
                primitives[list(primitives)[-1]].extend(nums)
                # A wrapped citation continues on the next lines. Without this,
                # a dangling reference past the first line is never checked.
                citing = list(primitives)[-1]
                continue
            if citing and raw.strip() and re.fullmatch(r"[\d,\s*]+\.?", raw.strip()):
                primitives[citing].extend(int(x) for x in re.findall(r"\d+", raw))
                continue
            citing = None
            # Primitive name: "1. **Name** — ..."
            m = re.match(r"\s*\d+\.\s+\*\*(.+?)\*\*\s*(?:`([^`]+)`)?", raw)
            if m:
                primitives[m.group(1)] = []
                slugs["primitive"][m.group(1)] = m.group(2)
                continue
            # Claims are read ONLY from the canonical tally line, never from free
            # prose. A document legitimately discusses numbers — quoting a figure
            # that turned out wrong, citing a prior run — and scanning everywhere
            # lets that prose masquerade as the document's own claim. One home.
            #
            #   **Tally:** 10 ✅ · 24 ◐ · 26 ○ · 26 ⚡
            if re.match(r"\*{0,2}Tally\*{0,2}:", raw.strip()):
                m = re.search(r"(\d+)\s*✅.*?(\d+)\s*◐.*?(\d+)\s*○", raw)
                if m:
                    claims["tally"] = tuple(int(g) for g in m.groups())
                m = re.search(r"(\d+)\s*⚡", raw)
                if m:
                    claims["frontier"] = int(m.group(1))
                else:
                    claims["frontier_absent"] = True
            continue

        cells = split_row(raw)
        if is_divider(cells):
            continue

        # Roster row: | **P1** | `slug` | Role | Why | 13 |
        m = re.match(r"\*{0,2}(P\d+)\*{0,2}$", cells[0])
        if m and len(cells) >= 4 and cells[-1].isdigit():
            pid = m.group(1)
            roster[pid] = int(cells[-1])
            sm = re.match(r"`([^`]+)`$", cells[1]) if len(cells) >= 5 else None
            slugs["persona"][pid] = sm.group(1) if sm else None
            continue

        # Item row: | 12 | "ask" | why | freq | ⚡ | cov |
        if cells[0].isdigit() and len(cells) >= 5 and current_persona:
            n = int(cells[0])
            ask, why, freq = cells[1], cells[2], cells[3]
            rest = cells[4:]
            frontier = any("⚡" in c for c in rest)
            cov = next((c for c in rest if c.strip() in COVERAGE_MARKS), "")
            items.append(Item(n, current_persona, ask, why, freq, frontier, cov, i))

    return roster, items, primitives, claims, slugs


def check(roster, items, primitives, claims, slugs, rep: Report) -> None:
    if not items:
        rep.fail("no item rows parsed — is this a persona-brainstorm document?")
        return

    # 1. Continuous, unique numbering across the whole document.
    nums = [it.n for it in items]
    dupes = sorted({n for n in nums if nums.count(n) > 1})
    if dupes:
        rep.fail(f"duplicate item numbers: {dupes}")
    expected = list(range(1, len(items) + 1))
    if nums != expected:
        missing = sorted(set(expected) - set(nums))
        extra = sorted(set(nums) - set(expected))
        if missing or extra:
            rep.fail(
                f"numbering not continuous 1..{len(items)} — missing {missing}, unexpected {extra}"
            )
        else:
            first = next(i for i, (a, b) in enumerate(zip(nums, expected)) if a != b)
            rep.fail(
                f"item numbers are complete but out of document order — position {first + 1} "
                f"holds item {nums[first]}, expected {expected[first]}"
            )

    # 2. Per-persona budgets against the roster table.
    for pid, budget in sorted(roster.items()):
        actual = sum(1 for it in items if it.persona == pid)
        if actual != budget:
            rep.fail(f"{pid}: roster promises {budget} items, document has {actual}")
    orphan = sorted({it.persona for it in items} - set(roster))
    if orphan:
        rep.fail(f"items for personas absent from the roster table: {orphan}")

    # 3. Even budgets are a tell, not a virtue.
    if len(roster) > 2:
        lo, hi = min(roster.values()), max(roster.values())
        if lo and hi / lo < FLATNESS_RATIO:
            rep.warn(
                f"budgets are nearly even ({lo}–{hi} across {len(roster)} personas); "
                "the method names fairness as the enemy of signal"
            )

    # 4. Frontier count — computed, then compared to whatever the document claims.
    stray = [it.n for it in items if "⚡" in it.ask]
    if stray:
        rep.warn(
            f"items with ⚡ inside the ask rather than the column: {stray}. "
            "Only the column is counted — a mark in prose is uncountable, which is how a "
            "wrong frontier figure went unnoticed in the first place."
        )
    frontier = [it for it in items if it.frontier]
    rep.note(f"frontier (⚡) items: {len(frontier)} of {len(items)}")
    if not frontier:
        rep.fail("no ⚡ items — the method says this means you under-reached")
    if "frontier" in claims and claims["frontier"] != len(frontier):
        rep.fail(
            f"tally line claims {claims['frontier']} ⚡ items; {len(frontier)} are marked. "
            "A self-reported count disagreeing with the table is the exact failure this checks."
        )
    if claims.get("frontier_absent"):
        rep.warn("tally line states no ⚡ count — add it so the figure can be checked")

    # 5. Coverage tally — computed, then compared to the claim.
    graded = [it for it in items if it.coverage]
    if not graded and "tally" in claims:
        rep.fail(
            f"tally line claims {claims['tally']} but no coverage mark parsed on any item — "
            "either the marks are missing or they are not in the ✅ / ◐ / ○ vocabulary"
        )
    if graded:
        tally = tuple(sum(1 for it in items if it.coverage == m) for m in ("✅", "◐", "○"))
        rep.note(f"coverage: {tally[0]} ✅ · {tally[1]} ◐ · {tally[2]} ○ of {len(graded)} graded")
        if "tally" in claims and claims["tally"] != tally:
            rep.fail(f"document claims tally {claims['tally']}; table gives {tally}")
        if len(graded) != len(items):
            rep.warn(f"{len(items) - len(graded)} items have no coverage mark")
        served = tally[0] / len(graded)
        if served > 0.5:
            rep.warn(
                f"{served:.0%} of items marked served — the method expects half to two-thirds "
                "partly served or impossible; a ✅-heavy document usually means coverage leaked "
                "into the decision to include"
            )
        if frontier:
            f_unserved = sum(1 for it in frontier if it.coverage == "○")
            rep.note(f"frontier unserved: {f_unserved} of {len(frontier)}")

    # 6. Frequency vocabulary.
    for it in items:
        if not it.freq:
            rep.fail(f"item {it.n} (line {it.line}) has no frequency")
        elif it.freq not in FREQ_VOCAB:
            rep.warn(f"item {it.n}: frequency {it.freq!r} outside the vocabulary")

    # 7. A Why that restates the Ask is a feature request in costume.
    for it in items:
        if not it.why:
            rep.fail(f"item {it.n} (line {it.line}) names no decision")
            continue
        a = re.sub(r"[^a-z ]", "", it.ask.lower())
        w = re.sub(r"[^a-z ]", "", it.why.lower())
        if a and w and SequenceMatcher(None, a, w).ratio() > RESTATEMENT_RATIO:
            rep.warn(f"item {it.n}: 'why' looks like a restatement of the ask, not a decision")

    # 8. Every ask should read as speech.
    for it in items:
        if '"' not in it.ask and "'" not in it.ask:
            rep.warn(f"item {it.n}: ask is not quoted — is it written as a Jira title?")

    # 9. Primitives must cite real items.
    if not primitives:
        rep.fail(
            "no capability primitives parsed — the synthesis is the deliverable, and a document "
            "without it is a list of asks rather than a finding"
        )
    if primitives:
        uncited = [p for p, ns in primitives.items() if not ns]
        if uncited:
            rep.fail(f"primitives citing no items: {uncited}")
        known = set(nums)
        for p, ns in primitives.items():
            bad = sorted(set(ns) - known)
            if bad:
                rep.fail(f"primitive {p!r} cites items that do not exist: {bad}")
        covered = {n for ns in primitives.values() for n in ns}
        rep.note(f"{len(primitives)} primitives citing {len(covered)} of {len(items)} items")
        if not 6 <= len(primitives) <= 12:
            rep.warn(f"{len(primitives)} primitives — the method aims for 6–12")

    # 10. Stable slugs are what let two runs of one subject be compared when
    #     every sentence has been reworded. Item numbers are positional and
    #     cannot do that job.
    for kind in ("persona", "primitive"):
        table = slugs.get(kind, {})
        missing = sorted(k for k, v in table.items() if not v)
        if missing:
            rep.warn(f"{kind}s without a stable slug: {missing[:6]}")
        present = [v for v in table.values() if v]
        bad = [v for v in present if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", v)]
        if bad:
            rep.fail(f"{kind} slugs not kebab-case: {bad}")
        dupes = sorted({v for v in present if present.count(v) > 1})
        if dupes:
            rep.fail(f"duplicate {kind} slugs: {dupes}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = ap.parse_args()

    text = open(args.path, encoding="utf-8").read()
    rep = Report()
    check(*parse(text), rep)

    for m in rep.notes:
        print(f"  ..  {m}")
    for m in rep.warns:
        print(f"[WARN] {m}")
    for m in rep.fails:
        print(f"[FAIL] {m}")

    print()
    if rep.fails:
        print(f"RESULT: FAIL — {len(rep.fails)} failure(s), {len(rep.warns)} warning(s)")
        return 1
    if rep.warns and args.strict:
        print(f"RESULT: FAIL (strict) — {len(rep.warns)} warning(s)")
        return 1
    print(f"RESULT: PASS — {len(rep.warns)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
