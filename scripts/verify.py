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
# A declaration has to declare something. Length is not evidence of substance:
# "TBD" clears a three-character bar while asserting nothing at all.
PLACEHOLDERS = {
    "tbd", "tba", "tbc", "todo", "fixme", "na", "n/a", "none", "null", "nil",
    "unknown", "unspecified", "pending", "xxx", "placeholder", "?", "???", "-", "--",
}
# An ask is speech, so it opens and closes with matching delimiters. Testing for a
# quote character anywhere lets "I've got twenty minutes" pass on its apostrophe.
OPENERS = "\"'“‘«„"
CLOSERS = "\"'”’»“"
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
    today: str
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


def is_substantive(value: str) -> bool:
    """True when a field actually declares something.

    Length is not evidence of substance — "TBD" clears a three-character bar
    while asserting nothing — and an unedited template placeholder is worse
    than a blank, because a blank is visibly missing. Every required field is
    held to this, not just the ones a reviewer happened to name.
    """
    v = value.strip().strip("*").strip()
    if len(v) < 2 or v.startswith("<"):
        return False
    if re.sub(r"[^a-z0-9/?-]+", "", v.lower()) in PLACEHOLDERS:
        return False
    # Alphabetic, not ASCII: a Today value of "何もしない" declares as much as
    # "does nothing by hand", and this skill is meant to run on any subject.
    return sum(1 for ch in v if ch.isalpha()) >= 2


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
    dupes_seen: list[str] = []
    dupe_pids: list[str] = []

    current_persona = None
    citing = None
    in_primitives = False
    in_header = True   # until the first roster or item row
    item_has_today = None   # set from the item-table header, not guessed
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
        if re.match(r"#{1,3}\s", raw):
            current_persona = None
        # Primitives are parsed only inside the synthesis section. Phase 7 asks the
        # adversarial reader to answer five numbered questions, which produces
        # "1. **Something** — ..." entries that are not primitives at all.
        if re.match(r"##\s", raw):
            in_primitives = bool(
                re.search(r"capability primitives|what the .+ imply", raw, re.I)
            )

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
            m = re.match(r"\s*\d+\.\s+\*\*(.+?)\*\*\s*(?:`([^`]+)`)?", raw) if in_primitives else None
            if m:
                name = m.group(1)
                if name in primitives:
                    # Overwriting would hide both the duplicate and its citations.
                    dupes_seen.append(name)
                    name = f"{name} (duplicate #{dupes_seen.count(name) + 1})"
                primitives[name] = []
                slugs["primitive"][name] = m.group(2)
                continue
            # Claims are read ONLY from the canonical tally line, never from free
            # prose. A document legitimately discusses numbers — quoting a figure
            # that turned out wrong, citing a prior run — and scanning everywhere
            # lets that prose masquerade as the document's own claim. One home.
            #
            #   **Tally:** 10 ✅ · 24 ◐ · 26 ○ · 26 ⚡
            # Frequencies and Roster axis are canonical header claims, held to the
            # same rule as the tally: one address, read nowhere else. Parsed only
            # before the first data table, so a passing mention in later prose —
            # a Verification section discussing the roster axis, say — cannot
            # satisfy a requirement it was never making.
            for label, key in (("Frequencies", "freq_basis"), ("Roster axis", "axis")):
                m = re.match(rf"\*{{0,2}}{label}\*{{0,2}}:\*{{0,2}}(.*)", raw.strip())
                if m and in_header:
                    value = m.group(1).strip().strip("*").strip()
                    claims[key + "_count"] = claims.get(key + "_count", 0) + 1
                    if is_substantive(value):
                        claims[key] = value
            if re.match(r"\*{0,2}Tally\*{0,2}:", raw.strip()):
                claims["tally_count"] = claims.get("tally_count", 0) + 1
                claims["tally_seen"] = True
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

        # Item-table header row: records the column layout for the rows beneath it.
        if cells[0] == "#" and any("ask" in c.lower() for c in cells):
            item_has_today = any(c.strip().lower() == "today" for c in cells)
            continue

        # Roster row: | **P1** | `slug` | Role | Why | 13 |
        m = re.match(r"\*{0,2}(P\d+)\*{0,2}$", cells[0])
        if m and len(cells) >= 4 and cells[-1].isdigit():
            in_header = False
            pid = m.group(1)
            if pid in roster:
                dupe_pids.append(pid)
            roster[pid] = int(cells[-1])
            sm = re.match(r"`([^`]+)`$", cells[1]) if len(cells) >= 5 else None
            slugs["persona"][pid] = sm.group(1) if sm else None
            continue

        # Item row: | 12 | "ask" | why | freq | ⚡ | cov |
        if cells[0].isdigit() and len(cells) >= 5 and current_persona:
            in_header = False
            n = int(cells[0])
            ask, why = cells[1], cells[2]
            # The Today column sits between Why and Freq, and documents written
            # before it existed have Freq there instead. Read the layout from the
            # table header: sniffing the cell's content misreads any frequency
            # outside the vocabulary as a Today value and shifts every column
            # after it, so an unrecognised word silently deletes the frontier
            # mark instead of warning about the word.
            if item_has_today is None:
                has_today = cells[3].lower().lstrip("~") not in FREQ_VOCAB
            else:
                has_today = item_has_today
            if has_today:
                today, freq, rest = cells[3], cells[4], cells[5:]
            else:
                today, freq, rest = "", cells[3], cells[4:]
            frontier = any("⚡" in c for c in rest)
            cov = next((c for c in rest if c.strip() in COVERAGE_MARKS), "")
            items.append(Item(n, current_persona, ask, why, today, freq, frontier, cov, i))

    claims["has_today_column"] = (
        item_has_today if item_has_today is not None else any(it.today for it in items)
    )
    claims["duplicate_primitives"] = sorted(set(dupes_seen))
    claims["duplicate_personas"] = sorted(set(dupe_pids))
    return roster, items, primitives, claims, slugs


def check(roster, items, primitives, claims, slugs, rep: Report) -> None:
    # Structural preconditions. Every check below is a guard of the shape
    # "if <thing> parsed: compare it" — which silently reports PASS when the
    # thing is missing entirely. Absence of a required part is a failure here,
    # once, so the individual checks can assume presence.
    if not items:
        rep.fail("no item rows parsed — is this a persona-brainstorm document?")
        return
    if not roster:
        rep.fail("no persona roster table parsed — item budgets cannot be checked against anything")
    if claims.get("tally_count", 0) > 1:
        rep.fail(
            f"{claims['tally_count']} canonical tally lines. Only the last is validated, so an "
            "obsolete one left above a corrected one leaves the document asserting two different "
            "counts while this check reports consistency."
        )
    if not claims.get("tally_seen"):
        rep.fail(
            "no canonical tally line found. It is the only place a claimed figure may live, so "
            "without it there is nothing to check a self-reported count against — which is the "
            "gate this whole script exists to hold."
        )
    if any(it.coverage for it in items) and "tally" not in claims:
        rep.fail(
            "items carry coverage marks but the tally line states no coverage figures. The "
            "frontier-only form is for runs that skipped coverage; using it here skips the "
            "comparison entirely."
        )
    if claims.get("duplicate_personas"):
        rep.fail(
            f"roster rows sharing a persona id: {claims['duplicate_personas']}. The later row "
            "overwrites the earlier budget and slug, making two personas indistinguishable."
        )

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

    # 5b. The demand-side measure, the frequency basis, and the roster axis.
    missing_today = [it.n for it in items if not is_substantive(it.today)]
    if not claims.get("has_today_column"):
        # No column at all: a document written before the field existed. Warn, so
        # old runs stay readable, and say plainly that new ones must carry it.
        rep.warn(
            "no Today column — what each persona does instead, right now. Coverage says whether "
            "you serve an ask; Today says whether anyone needs it served, and without it an "
            "unserved item cannot be told apart from a non-problem. Required for new documents."
        )
    elif missing_today:
        # The column is declared, so the field is required here and a warning would
        # pass the standard Phase 7 invocation, which does not use --strict.
        rep.fail(
            f"{len(missing_today)} item(s) in a declared Today column have no value: "
            f"{missing_today[:8]}. A declared column that is empty is not back-compatibility, "
            "it is the demand-side measure missing from a document that claims to carry it."
        )

    for key, label in (("freq_basis", "Frequencies"), ("axis", "Roster axis")):
        if claims.get(key + "_count", 0) > 1:
            rep.fail(
                f"{claims[key + '_count']} **{label}:** declarations in the header. Only the last "
                "is read, so a contradictory earlier one leaves the document asserting two "
                "different things while this check reports one."
            )
    if not claims.get("freq_basis"):
        rep.fail(
            "no **Frequencies:** line with a stated basis, in the header before the persona "
            "table. Values like 'weekly' read as measurement and are usually estimates; the "
            "document has to say which, and a bare label declares nothing."
        )
    if not claims.get("axis"):
        rep.fail(
            "no **Roster axis:** line with a stated axis, in the header before the persona "
            "table. A roster mixing job roles, software and review functions cannot be checked "
            "for completeness, which is the whole point of asking who is missing."
        )

    # 5c. Persona distinctness is deliberately NOT checked here, and should not be
    #     added. A lexical version was written and measured against a document with a
    #     known duplicate pair: the true duplicates scored 0.031 ask-vocabulary overlap,
    #     the LOWEST of any pair, while unrelated personas reached 0.123. Real duplicates
    #     ask the same question in different words — "what would a domain expert know is
    #     wrong" and "which claims get me caught by a twenty-year veteran" share almost no
    #     vocabulary — so the score is anti-correlated with the thing it would claim to
    #     detect, and a passing run would be false reassurance. The distinctness test lives
    #     in Phase 1 (cover the names, read only the asks) and in the Phase 7b question
    #     list, where a reader who understands the questions can answer it.

    # 6. Frequency vocabulary.
    for it in items:
        if not it.freq:
            rep.fail(f"item {it.n} (line {it.line}) has no frequency")
        elif it.freq.lstrip("~") not in FREQ_VOCAB:
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
        a = it.ask.strip().rstrip(".,;")
        if not (len(a) >= 2 and a[0] in OPENERS and a[-1] in CLOSERS):
            rep.warn(f"item {it.n}: ask is not quoted — is it written as a Jira title?")

    # 9. Primitives must cite real items.
    if claims.get("duplicate_primitives"):
        rep.fail(
            f"capability primitives sharing a display name: {claims['duplicate_primitives']}. "
            "Each primitive is cited by item number and addressed by slug; two with one name "
            "cannot be told apart by either."
        )
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
    ap.add_argument(
        "--final",
        action="store_true",
        help="also require the Phase 7b Verification section (run after the adversarial read)",
    )
    args = ap.parse_args()

    text = open(args.path, encoding="utf-8").read()
    rep = Report()
    check(*parse(text), rep)
    if args.final:
        m = re.search(r"^#{2,3}\s*Verification\b(.*?)(?=^#{2}\s|\Z)", text, re.M | re.S)
        if not m:
            rep.fail(
                "no Verification section — Phase 7b was skipped or its findings were not "
                "recorded. An absent verification section reads as a passed one, which is why "
                "this is checked rather than trusted."
            )
        else:
            # A bare heading satisfies a heading check while recording nothing. The
            # adversarial read answers five questions; require enough substance to
            # have carried them.
            body = [ln for ln in m.group(1).splitlines() if ln.strip()]
            if len(body) < 5:
                rep.fail(
                    f"Verification section has {len(body)} non-empty line(s). Phase 7b asks five "
                    "questions and requires the answers recorded, disagreements included; a "
                    "heading on its own passes the gate without carrying any of them."
                )

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
