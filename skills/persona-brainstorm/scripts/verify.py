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
    # Whether the table this row came from declared a Today column. Per row, not
    # per document: a document can mix schemas, and one legacy section at the end
    # must not excuse an earlier section that declared the column and left it empty.
    in_today_table: bool = False


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


# Evidence marks are a closed set. An open one lets "probably", "strong" and
# "high-confidence" accumulate until the column sorts nothing, which is the
# failure the frequency vocabulary already exists to prevent.
EVIDENCE = ("observed", "inferred", "invented")

# The source runs to the mark's own closing delimiter, not to the first closing
# parenthesis. A plain [^)]* ended the capture at any ')' inside the source, the
# trailing \)\* then failed, and the mark vanished -- reported as *absent* by
# every caller. The text most likely to trip it was this checker's own output,
# because those messages contain "primitive(s)", so quoting what the checker
# reported -- the most auditable source an observed mark can name -- was the
# thing the rule punished. Accept a ')' that is not the delimiter.
MARK_SOURCE = r"(?:[^)]|\)(?!\*))*"

# The annotation, anchored: leading space, then *(kind)* or *(kind: source)*.
MARK_RE = r"\s*\*\(\s*([A-Za-z-]+)\s*(?::\s*(" + MARK_SOURCE + r"))?\)\*"

# An attempt at a mark, however malformed. Used only to tell "you wrote no mark"
# apart from "your mark did not parse": the first sends the author to write one,
# and telling them that when a correct mark is present sends them to add a
# second, which the two-marks rule then refuses. A diagnostic that names the
# wrong cause is worse than a silent failure, because it steers the fix.
MARK_ATTEMPT_RE = r"\*\(\s*[A-Za-z-]+\s*[:)]"


def parse_prediction(text: str, mode: str = "prereg") -> dict:
    """Pull the checkable figures out of a Pre-registered or Reckoning line.

    The two lines have different shapes and are parsed differently on purpose.
    A pre-registration carries one prediction plus required prose — a surprise
    threshold and a cut rule, either of which may legitimately contain a comma.
    A reckoning carries two figures separated by the word "actual". One regex
    guessing between them let a comma in "cut: vague, unsupported, or duplicate"
    reclassify a prediction and fail a valid document.
    """
    SPLIT = r"(\d+)\s*/\s*(\d+)\s*/\s*(\d+)"
    FRONT = r"(\d+)\s*⚡"

    def figures(chunk):
        got = {}
        m = re.search(SPLIT, chunk)
        if m:
            got["split"] = tuple(int(x) for x in m.groups())
        m = re.search(FRONT, chunk)
        if m:
            got["frontier"] = int(m.group(1))
        return got

    if mode == "prereg":
        # The figure has to be marked as a prediction. A header that merely
        # mentions a number — "historical baseline 7/26/27" — is not an advance
        # guess, and a reckoning that later calls it one is precisely the
        # retrofit pre-registration exists to prevent.
        head = re.split(r"\bpredicted\b", text, maxsplit=1, flags=re.I)
        return figures(head[1]) if len(head) > 1 else {}

    # Reckoning: everything before "actual" is the prediction, everything after
    # is the result. Splitting on the word rather than on punctuation means
    # prose commas on either side are harmless.
    parts = re.split(r"\bactual\b", text, maxsplit=1, flags=re.I)
    out = {}
    head = re.split(r"\bpredicted\b", parts[0], maxsplit=1, flags=re.I)
    if len(head) > 1:
        for k, v in figures(head[1]).items():
            out["predicted_" + k] = v
    if len(parts) > 1:
        for k, v in figures(parts[1]).items():
            out["actual_" + k] = v
    return out


def is_substantive(value: str) -> bool:
    """True when a field actually declares something.

    Length is not evidence of substance — "TBD" clears a three-character bar
    while asserting nothing — and an unedited template placeholder is worse
    than a blank, because a blank is visibly missing. Every required field is
    held to this, not just the ones a reviewer happened to name.
    """
    v = value.strip().strip("*").strip()
    if not v or v.startswith("<"):
        return False
    if re.sub(r"[^a-z0-9/?-]+", "", v.lower()) in PLACEHOLDERS:
        return False
    # Alphabetic, not ASCII: a Today value of "何もしない" declares as much as
    # "does nothing by hand", and this skill is meant to run on any subject.
    alpha = [ch for ch in v if ch.isalpha()]
    if not alpha:
        return False
    # A lone ideograph is a whole word — 等 is "wait", 问 is "ask" — while a lone
    # Latin letter is a stray keystroke. Length minimums are an English habit and
    # must not be applied to scripts that do not share it.
    #
    # Count alphanumerics, not letters: "P2" is how a load-bearing persona is
    # actually named, and a rule that rejects it is rejecting the answer people
    # will write.
    alnum = [ch for ch in v if ch.isalnum()]
    if len(alnum) < 2 and all(ch.isascii() for ch in alpha):
        return False
    return True


def is_source(value: str) -> bool:
    """True when an evidence source identifies something lookup-able.

    Deliberately not `is_substantive`, which is tuned for prose fields and
    rejects two of the most ordinary references there are: "#12" carries no
    letters, and "<https://example.test/issues/12>" opens with the angle
    bracket that marks an unedited template slot. Both name a real artifact.

    The angle-bracket rule is the only subtle part. A Markdown autolink is a
    source; "<where it was seen>" is the template asking to be filled in, and
    the difference is whether the brackets hold a URI rather than a phrase.
    """
    v = value.strip().strip("*").strip()
    if not v:
        return False
    if re.sub(r"[^a-z0-9/?-]+", "", v.lower()) in PLACEHOLDERS:
        return False
    if v.startswith("<"):
        return bool(re.fullmatch(r"<[A-Za-z][A-Za-z0-9+.-]*:[^>\s]+>", v)
                    or re.fullmatch(r"<[^>\s@]+@[^>\s]+>", v))
    # An identifier is enough: a bare "#5" is a reference someone can follow.
    return len([ch for ch in v if ch.isalnum()]) >= 2 or any(ch.isdigit() for ch in v)


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
    evidence: dict[str, tuple] = {}
    claims: dict = {}
    slugs: dict[str, dict] = {"persona": {}, "primitive": {}}
    dupes_seen: list[str] = []
    multi_marked: list[str] = []
    malformed_marks: list[str] = []
    dupe_pids: list[str] = []
    malformed: list[tuple] = []

    current_persona = None
    citing = None
    in_primitives = False
    in_header = True   # until the first roster or item row
    item_has_today = None   # set from the item-table header, not guessed
    item_width = None       # and its column count, to catch short rows
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
        #
        # Every depth, not just the three the persona heading itself uses: a
        # #### subsection under a persona left the section open, so the rows
        # beneath it were charged to that persona -- the miscount this line
        # exists to prevent, at the one depth it did not reach. Markdown has no
        # level 7, so 1-6 is exhaustive.
        if re.match(r"#{1,6}\s", raw):
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
                # "*(observed: issue #12)*" or "*(invented)*", after the slug.
                # Read the whole entry, not the first physical line: an
                # annotation naming its source is long, and the template's own
                # layout wraps it. Reading one line would reject an ordinary
                # document for having no mark, and Phase 7 gates on this.
                entry = raw
                for nxt in lines[i:]:
                    if not nxt.strip():
                        break
                    # The citation ends the declaration -- but only a real
                    # citation. Stopping at any arrow truncated annotations
                    # whose source contained one, such as a "Login → Checkout"
                    # trace, and the primitive then read as unmarked.
                    if re.match(r"\s*→\s*items?\b", nxt):
                        break
                    if re.match(r"\s*\d+\.\s+\*\*", nxt):
                        break
                    entry += " " + nxt.strip()
                # Only the annotation in its prescribed position counts: the
                # template puts it immediately after the slug, so anchor there
                # rather than searching. Searching the entry let a literal
                # example in the prose -- `*(invented)*` quoted while
                # explaining the notation -- stand in for a mark that was never
                # written; bounding the search at the description dash then
                # broke sources that legitimately contain one, such as
                # "RFC 9110 - HTTP Semantics". Anchoring needs neither.
                region = entry[m.end():]
                first = re.match(MARK_RE, region)
                # Any further mark in the declaration contradicts the first --
                # adjacent to it or beyond the description, both count.
                # Inline code is stripped so a quoted example is not counted --
                # the same distinction anchoring makes for the first mark.
                rest = re.sub(r"`[^`]*`", "", region[first.end():]) if first else ""
                marks = ([(first.group(1), first.group(2) or "")] if first else [])
                if first and re.search(MARK_RE, rest):
                    marks.append(("", ""))
                if len(marks) > 1:
                    # Keeping only the first would let a stale mark sit beside
                    # its replacement and report the document as consistent.
                    multi_marked.append(name)
                elif marks:
                    evidence[name] = (marks[0][0].lower(), marks[0][1].strip())
                elif re.match(r"\s*" + MARK_ATTEMPT_RE, region):
                    # A mark was written and did not parse. Reporting that as
                    # "no mark" sends the author to add one, and the two-marks
                    # rule then refuses the result -- so the diagnostic has to
                    # name the real cause or it steers the fix into a second
                    # error.
                    malformed_marks.append(name)
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
            for label, key in (
                ("Frequencies", "freq_basis"),
                ("Roster axis", "axis"),
                ("Pre-registered", "prereg"),
                ("Load-bearing persona", "loadbearing"),
            ):
                m = re.match(rf"\*{{0,2}}{label}\*{{0,2}}:\*{{0,2}}(.*)", raw.strip())
                if m and in_header:
                    value = m.group(1).strip().strip("*").strip()
                    claims[key + "_count"] = claims.get(key + "_count", 0) + 1
                    if is_substantive(value):
                        claims[key] = value
            m = re.match(r"\*{0,2}Reckoning\*{0,2}:\*{0,2}(.*)", raw.strip())
            if m and in_primitives:
                claims["reckoning_count"] = claims.get("reckoning_count", 0) + 1
                if is_substantive(m.group(1)):
                    claims["reckoning"] = m.group(1).strip()
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
            item_width = len(cells)
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
            # Positional decoding is only safe against a row of the declared width.
            # A row one cell short slides every field left — Today takes the
            # frequency, the frequency takes the frontier mark — so a required
            # field looks filled and a displaced one only warns.
            if item_width is not None and len(cells) != item_width:
                malformed.append((n, len(cells), item_width))
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
            items.append(Item(n, current_persona, ask, why, today, freq, frontier, cov, i, has_today))

    claims["malformed_rows"] = malformed
    claims["duplicate_primitives"] = sorted(set(dupes_seen))
    claims["evidence"] = evidence
    claims["multi_marked"] = multi_marked
    claims["malformed_marks"] = malformed_marks
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
    if claims.get("malformed_rows"):
        detail = ", ".join(f"item {n} has {got} cells, header declares {want}"
                           for n, got, want in claims["malformed_rows"][:4])
        rep.fail(
            f"{len(claims['malformed_rows'])} row(s) do not match their table header: {detail}. "
            "Fields are read by position, so a short row slides every value left and a required "
            "one reads as filled from its neighbour."
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
    declared = [it for it in items if it.in_today_table]
    legacy = [it for it in items if not it.in_today_table]
    missing_today = [it.n for it in declared if not is_substantive(it.today)]
    if declared and legacy:
        rep.warn(
            f"mixed table schemas: {len(declared)} item(s) come from a table declaring a Today "
            f"column and {len(legacy)} from one without. The declared rows are still required to "
            "carry values; a legacy section later in the document does not excuse them."
        )
    if not declared:
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

    for key, label, where in (
        ("freq_basis", "Frequencies", "header"), ("axis", "Roster axis", "header"),
        ("prereg", "Pre-registered", "header"), ("loadbearing", "Load-bearing persona", "header"),
        ("reckoning", "Reckoning", "synthesis"),
    ):
        if claims.get(key + "_count", 0) > 1:
            rep.fail(
                f"{claims[key + '_count']} **{label}:** lines in the {where}. Only the last is "
                "read, so a contradictory earlier one leaves the document asserting two different "
                "things while this check reports one."
            )
        # A line that is present but says nothing is a different fault from an
        # absent one, and telling someone to add a line they already wrote is a
        # bad error message.
        if claims.get(key + "_count") and not claims.get(key):
            rep.fail(
                f"**{label}:** is present but declares nothing — a placeholder or an empty value. "
                "Fill it or remove the line; a label on its own reads as a declaration and is not."
            )
    if not claims.get("prereg_count"):
        rep.warn(
            "no **Pre-registered:** line. Without a prediction recorded before generation, no "
            "result from this run can come out surprising, and the coverage ratio reports your "
            "priors rather than the subject. Required for new documents."
        )
    elif not claims.get("reckoning"):
        rep.fail(
            "pre-registered but no **Reckoning:** line in the synthesis. A prediction nobody "
            "returns to is decoration; the reckoning is the half that costs something, including "
            "when the news is that the prediction held and the run taught you nothing."
        )
    if not claims.get("prereg_count") and claims.get("reckoning"):
        rep.fail(
            "a **Reckoning:** line with no **Pre-registered:** line to reckon against. A "
            "prediction recovered after the result is not a prediction."
        )
    # A modern document is one using the current table schema. Legacy documents
    # keep warnings so old runs stay readable; anything written to today's
    # template is held to today's requirements, because the standard Phase 7
    # invocation does not pass --strict and a warning it ignores is not a rule.
    modern = any(it.in_today_table for it in items)
    if modern:
        for key, label in (("prereg", "Pre-registered"), ("loadbearing", "Load-bearing persona")):
            if not claims.get(key + "_count"):
                rep.fail(
                    f"no **{label}:** line in a document using the current table schema. "
                    "Legacy documents only warn; this one is written to today's template."
                )

    # Naming a persona the roster does not contain leaves the assumption
    # unrevisitable, which is the only thing this declaration is for. Ids are
    # checked when present; a declaration naming nobody the roster knows fails
    # too, because "the on-call responder" resolves only if the roster says so.
    lb = claims.get("loadbearing", "")
    if lb and roster:
        unknown = sorted(set(re.findall(r"\bP\d+\b", lb)) - set(roster))
        known_slugs = [v for v in slugs["persona"].values() if v]
        if unknown:
            rep.fail(
                f"the load-bearing persona names {', '.join(unknown)}, which the roster does "
                f"not contain (it has {', '.join(sorted(roster))})."
            )
        elif not re.search(r"\bP\d+\b", lb) and not any(g in lb for g in known_slugs):
            rep.fail(
                "the load-bearing persona names nobody on the roster. Identify them by id "
                "(P2) or by slug, so synthesis can revisit the assumption."
            )

    # The reckoning is the one place a number is claimed *about* this document,
    # which makes it the last place to accept one on trust.
    if claims.get("reckoning"):
        pre = parse_prediction(claims.get("prereg", ""), "prereg")
        rec = parse_prediction(claims["reckoning"], "reckoning")
        graded_now = [it for it in items if it.coverage]
        actual_tally = tuple(
            sum(1 for it in items if it.coverage == mk) for mk in ("✅", "◐", "○")
        )
        actual_front = sum(1 for it in items if it.frontier)

        # Which figure this run owes depends on whether it graded coverage.
        kind = "split" if graded_now else "frontier"
        want_pred, want_act = f"predicted_{kind}", f"actual_{kind}"
        missing = [k for k in (want_pred, want_act) if k not in rec]
        if missing:
            other = "frontier" if kind == "split" else "split"
            if rec.get(f"predicted_{other}") or rec.get(f"actual_{other}") or rec.get(other):
                rep.fail(
                    f"the reckoning reports a {other} figure, but this run "
                    f"{'graded coverage' if kind == 'split' else 'graded no coverage'}, so the "
                    f"figure to reckon is the {kind}."
                )
            elif rec.get(kind):
                rep.fail(
                    "the **Reckoning:** line carries figures but not in the form "
                    "'predicted X, actual Y', so the two cannot be told apart. Both halves are "
                    "required and both are compared."
                )
            else:
                rep.fail(
                    f"the **Reckoning:** line is missing "
                    f"{' and '.join(m.replace('_', ' ') for m in missing)}. Both halves are "
                    "required: a line that states a prediction and then characterises the outcome "
                    "in words is the half that costs nothing."
                )
        # A pre-registration with no figure in it cannot be reckoned against, and
        # leaves the reckoning free to report a prediction nobody made.
        if not (pre.keys() & {"split", "frontier"}):
            rep.fail(
                "the **Pre-registered:** line states no prediction — substantive prose is not a "
                "figure. Without one, the reckoning below can report any prediction it likes, "
                "which is precisely the failure pre-registering was meant to prevent."
            )
        elif kind == "split" and "split" not in pre:
            rep.fail(
                "this run graded coverage but pre-registered only a frontier figure. Predict the "
                "kind of result the run produces."
            )
        elif not all(w in claims.get("prereg", "").lower() for w in ("surprise", "cut")):
            rep.fail(
                "the **Pre-registered:** line carries a prediction but not the surprise threshold "
                "or the cut rule. All three are required: without a threshold no result can come "
                "out surprising, and without a cut rule every item generated survives."
            )
        elif kind == "frontier" and "frontier" not in pre:
            rep.fail(
                "this run graded no coverage but pre-registered a coverage split, which can never "
                "be reckoned against. Predict the kind of result the run produces."
            )
        # (2) The prediction is made against a budget set in Phase 0, so a predicted
        #     split that does not add up to it was never a plan for this run.
        budget = sum(roster.values()) if roster else None
        declared = re.search(r"\bof\s+(\d+)", claims.get("prereg", ""))
        if declared and budget and int(declared.group(1)) != budget:
            rep.fail(
                f"the pre-registration is written against {declared.group(1)} items but the "
                f"roster budgets {budget}. A denominator that disagrees with the roster describes "
                "a different run."
            )
        target = budget or (int(declared.group(1)) if declared else None)
        if "split" in pre and target and sum(pre["split"]) != target:
            rep.fail(
                f"the pre-registered split {pre['split']} sums to {sum(pre['split'])}, but the "
                f"run is budgeted for {target} items. These are counts against a total you set "
                "in Phase 0."
            )
        # Frontier items are a subset of the roster's items, so a prediction
        # larger than the whole run is not a bold guess, it is unreadable.
        if "frontier" in pre and target and pre["frontier"] > target:
            rep.fail(
                f"the pre-registration predicts {pre['frontier']} frontier items in a run "
                f"budgeted for {target}. Frontier items are a subset of the roster's items."
            )
        # Counts, so the actual split must account for every graded item.
        if "actual_split" in rec and graded_now and sum(rec["actual_split"]) != len(graded_now):
            rep.fail(
                f"the reckoning's actual split sums to {sum(rec['actual_split'])} across "
                f"{len(graded_now)} graded items. These are counts, not percentages."
            )
        pre_val = pre["split"] if "split" in pre else pre.get("frontier")
        rec_pred = (rec["predicted_split"] if "predicted_split" in rec
                    else rec.get("predicted_frontier"))
        if pre_val is not None and rec_pred is not None and pre_val != rec_pred:
            rep.fail(
                f"the reckoning says it predicted {rec_pred}, but the pre-registration says "
                f"{pre_val}. A prediction restated differently after the result is not the "
                "prediction that was made."
            )
        if "actual_split" in rec and graded_now and rec["actual_split"] != actual_tally:
            rep.fail(
                f"the reckoning reports an actual split of {rec['actual_split']}; the table gives "
                f"{actual_tally}."
            )
        if "actual_frontier" in rec and rec["actual_frontier"] != actual_front:
            rep.fail(
                f"the reckoning reports {rec['actual_frontier']} frontier items; the table has "
                f"{actual_front}."
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
    # Evidence annotation. The rule that makes this safe to add: it gates
    # well-formedness, never kind. An `invented` primitive is never penalised --
    # the frontier is invented by construction and holds the best findings on
    # most pages -- but a claim of `observed` with no source is worse than an
    # honest `invented`, because it cannot be audited and reads as stronger.
    for name in claims.get("multi_marked") or []:
        rep.fail(
            f"primitive {name!r} carries more than one evidence mark. Two provenance claims on "
            "one primitive contradict each other, and reading only the first would let a stale "
            "mark sit beside its replacement and pass."
        )
    if primitives:
        marks = claims.get("evidence") or {}
        # One message for the whole section, not one per primitive: a document
        # written before evidence marks existed is missing all of them, and ten
        # copies of the same sentence bury every other finding on the page.
        # A primitive carrying two marks is invalid, not unmarked; naming it
        # here too would report the wrong defect and inflate the count.
        contradicted = set(claims.get("multi_marked") or [])
        # A mark that was written and did not parse is a third state, and it is
        # the one an author cannot act on from a "no mark" message.
        malformed = claims.get("malformed_marks") or []
        for name in malformed:
            rep.fail(
                f"primitive {name!r} carries an evidence mark that could not be read. The mark "
                "is present -- do not add another, which the two-marks rule refuses -- but its "
                "source runs past the closing delimiter. The usual cause is a ')' inside the "
                "source text; the mark ends at the first ')*', so quote carefully or reword."
            )
        contradicted |= set(malformed)
        unmarked = [n for n in primitives if n not in marks and n not in contradicted]
        if unmarked:
            msg = (f"{len(unmarked)} primitive(s) carry no evidence mark: "
                   f"{', '.join(repr(n) for n in unmarked[:3])}"
                   f"{', ...' if len(unmarked) > 3 else ''}. One of "
                   f"{', '.join(EVIDENCE)} after the slug says whether the demand behind it was "
                   "seen, reasoned to, or imagined; without it the reader cannot tell an "
                   "issue-tracker finding from a plausible guess.")
            rep.fail(msg) if modern else rep.warn(msg)
        for name in primitives:
            got = marks.get(name)
            if not got:
                continue
            mark, source = got
            if mark not in EVIDENCE:
                rep.fail(
                    f"primitive {name!r} is marked {mark!r}, which is not one of "
                    f"{', '.join(EVIDENCE)}. An open vocabulary of confidence words sorts "
                    "nothing once it has grown."
                )
            elif mark in ("observed", "inferred") and not is_source(source):
                rep.fail(
                    f"primitive {name!r} is marked {mark!r} but names no source. Evidence that "
                    "cannot be looked up is a stronger claim than 'invented' with none of the "
                    "backing; write the issue, transcript or document it came from."
                )
            elif mark == "invented" and source:
                rep.fail(
                    f"primitive {name!r} is marked 'invented' but names a source "
                    f"({source!r}). The mark says there is no artifact behind it, so a source "
                    "contradicts it: choose 'observed' or 'inferred' if the artifact is real, "
                    "and drop the suffix if it is not."
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


# The three forms an enriched item's third block may take, keyed by the coverage
# mark that selects it. The mapping is the whole point of the enrichment format:
# a heading derived from a mark cannot drift the way a judgement call does, and
# it is checkable precisely because it is derived. See references/enrichment.md.
#
# "" is the no-coverage case -- not a stylistic variant of ○ but a different
# claim. ○ means assessed and absent; a run that assessed nothing has not earned
# it, and writing "what would have to exist" there asserts it anyway.
ENRICHED_HEADINGS = {
    "✅": "How it's answered today",
    "◐": "How it's answered today",
    "○": "What would have to exist",
    "": "What answering this would take",
}
# Apostrophes are the one character an author is most likely to smarten, and a
# heading rule that rejects a curly one would fail the documents most carefully
# written. Normalise rather than demand.
APOSTROPHES = str.maketrans({"’": "'", "ʼ": "'", "´": "'"})


def normalise(s: str) -> str:
    return s.translate(APOSTROPHES).lower()


def carried_block(header: str, pos: int) -> str:
    """The carried findings: the rest of the line plus the block beneath it.

    The reference calls this a block and allows the findings verbatim or
    summarised, which in Markdown is most naturally a bullet list under the
    label. Reading only the declaration's own line rejected the shape the
    format actually invites.
    """
    rest = [header[pos:].split("\n", 1)[0]]
    for line in header[pos:].split("\n")[1:]:
        # Stops at the next canonical declaration or a rule, not at a blank:
        # a list separated from its label by one blank line is still its block.
        if re.match(r"\s*(\*\*[^*]+:\*\*|---|##)", line):
            break
        rest.append(line)
    return " ".join(rest).strip().strip("*").strip()


def blank_fences(text: str) -> str:
    """Replace fenced-block lines with blanks, keeping line and offset counts.

    Blanked rather than removed so every position computed against the result
    still lines up with the original — the alternative silently shifts every
    reported offset once a document contains one example.
    """
    out = []
    fence = None
    for line in text.split("\n"):
        m = re.match(r"\s*(`{3,}|~{3,})", line)
        # Tilde fences are as valid as backtick ones and are what a document
        # containing a backtick fence has to use to quote it. Closing requires
        # the same character, so a ``` inside a ~~~ block does not end it.
        if m and (fence is None or m.group(1)[0] == fence):
            fence = m.group(1)[0] if fence is None else None
            out.append(" " * len(line))
            continue
        out.append(" " * len(line) if fence else line)
    return "\n".join(out)


def check_enriched(items: list[Item], claims: dict, core_text: str,
                   text: str, rep: Report) -> None:
    """Check an enriched document against the core document it expands.

    Only the things a checker can settle: that every item is present exactly
    once, that each one's third-block heading is the one its coverage mark
    selects, and that the header carries the declarations a detached reader
    needs. Whether the prose is any good is Phase 7b's job, not this one's.
    """
    # Fenced blocks are examples, not entries. The core parser has skipped them
    # since it was written; this one scanned raw text, so a document with every
    # entry inside one fence -- which renders as a code sample and contains no
    # headings at all -- was read as a conforming enrichment.
    text = blank_fences(text)

    entries: dict[int, tuple[int, int]] = {}
    dupes: list[int] = []
    heads: dict[int, str] = {}
    starts = []
    for m in re.finditer(r"^####\s+(\d+)\s*[—\-–]\s*(.*)$", text, re.M):
        starts.append((int(m.group(1)), m.start()))
        heads.setdefault(int(m.group(1)), m.group(2).strip())
    if not starts:
        rep.fail(
            "no enriched entries found. Each item gets a '#### <n> — \"<the ask>\"' heading; "
            "without them there is nothing to check against the core document."
        )
        return
    # The header is everything before the first entry. Bounding it matters for
    # the same reason the core reads its claims only before the first table: a
    # declaration quoted inside an entry is discussion, not the document's own.
    header = text[: starts[0][1]]
    for idx, (n, pos) in enumerate(starts):
        end = starts[idx + 1][1] if idx + 1 < len(starts) else len(text)
        if n in entries:
            dupes.append(n)
        else:
            entries[n] = (pos, end)

    if dupes:
        rep.fail(
            f"item(s) {sorted(set(dupes))} have more than one enriched entry. Two entries for "
            "one ask means a reader gets whichever they scroll to first."
        )

    core = {it.n: it.coverage.strip() for it in items}
    missing = sorted(set(core) - set(entries))
    extra = sorted(set(entries) - set(core))
    if missing:
        shown = ", ".join(str(n) for n in missing[:12])
        more = f" (+{len(missing) - 12} more)" if len(missing) > 12 else ""
        rep.fail(
            f"{len(missing)} item(s) have no enriched entry: {shown}{more}. Enrichment covers "
            "every item — enriching forty of sixty makes the other twenty look rejected."
        )
    if extra:
        rep.fail(
            f"enriched entries for item(s) {extra}, which the core document does not contain. "
            "An entry with no item behind it cites nothing a reader can check."
        )

    graded = any(core.values())
    known = {normalise(v) for v in ENRICHED_HEADINGS.values()}
    item_ask = {it.n: it.ask.strip().strip("\"“”'‘’«»") for it in items}
    item_freq = {it.n: it.freq.strip() for it in items}
    item_frontier = {it.n: it.frontier for it in items}
    askless: list[int] = []
    mismatched_ask: list[int] = []
    two_footers: list[int] = []
    freq_off: list[str] = []
    frontier_off: list[str] = []
    wrong: list[str] = []
    unheaded: list[int] = []
    two: list[int] = []
    misplaced: list[str] = []
    cov_mismatch: list[str] = []
    no_mark: list[int] = []
    no_footer: list[int] = []
    for n in sorted(set(core) & set(entries)):
        start, end = entries[n]
        body = text[start:end]
        want = ENRICHED_HEADINGS[core[n]]
        labels = [m.group(1) for m in re.finditer(r"^\*\*([^*]+?)\.?\*\*", body, re.M)]
        found = [h for h in labels if normalise(h) in known]
        if not found:
            unheaded.append(n)
        elif len(found) > 1:
            # By count, not by distinct value. The same heading twice is as
            # malformed as two different ones, and a set comparison passes it.
            two.append(n)
        elif labels.index(found[0]) != 2:
            # It is the *third* block, and checking only that the heading exists
            # somewhere leaves the position unchecked -- an entry can put
            # anything third and the derived heading fourth, and still satisfy a
            # rule this checker advertises as positional.
            at = labels.index(found[0]) + 1
            misplaced.append(
                f"{n} has '{found[0]}' as block {at} of {len(labels)}, not the third"
            )
        elif normalise(found[0]) != normalise(want):
            mark = core[n] or "no coverage pass"
            wrong.append(f"{n} is {mark} and needs '{want}', not '{found[0]}'")
        # The footer copies the coverage mark from the core document. A mark that
        # disagrees with the heading beside it is the contradiction the derived
        # heading exists to prevent, arriving through the other column.
        # The heading carries the ask, so a reader knows what the scene expands
        # without holding the core document open beside it. Compared loosely —
        # an enriched heading may shorten a long ask — but a heading carrying
        # someone else's ask, or none, is not a shortening.
        head = heads.get(n, "")
        # Double quotes only, and non-greedy. An apostrophe is not a delimiter:
        # treating one as an opener let "don't" match from the apostrophe to
        # whatever quote-like character came next, so an unquoted ask containing
        # a contraction read as quoted.
        quoted = re.search(r"[\"“](.+?)[\"”]", head, re.S)
        if not quoted:
            askless.append(n)
        elif SequenceMatcher(
                None, normalise(quoted.group(1)), normalise(item_ask.get(n, ""))
        ).ratio() < 0.5:
            mismatched_ask.append(n)

        # The prescribed footer, not any line mentioning topics: a prose
        # sentence containing the word satisfied the loose form while the
        # frequency and frontier mark it is supposed to copy were gone.
        foots = list(re.finditer(r"^`([^`]+)`\s*·.*\btopics:.*$", body, re.M))
        if len(foots) > 1:
            two_footers.append(n)
        foot = foots[0] if foots else None
        # Ordered, not the COVERAGE_MARKS set: set iteration order varies with
        # the interpreter's hash seed, so a footer carrying two marks would
        # report a different one run to run -- and pass or fail by luck.
        seen = [c for c in ("✅", "◐", "○") if foot and c in foot.group(0)]
        if not foot:
            # The footer is the fourth required part, and on a run with no
            # coverage pass nothing else proves it exists: every branch below is
            # reached through a mark, and an entry with no mark to carry would
            # otherwise be free to drop the frequency and topics with it.
            no_footer.append(n)
        elif len(seen) > 1:
            cov_mismatch.append(
                f"{n} carries {' and '.join(seen)} in one footer"
            )
        elif core[n] and not seen:
            # An absent mark agrees with anything, so "the marks agree" is not a
            # check until the mark is required to be there.
            no_mark.append(n)
        elif core[n] and seen and seen[0] != core[n]:
            cov_mismatch.append(f"{n} is {core[n]} in the core document, {seen[0]} here")
        elif not core[n] and seen:
            # Either the run graded nothing, or this item was left unmarked in a
            # run that graded others. Both mean the footer has nothing to copy,
            # and a mark appearing anyway was invented here.
            where = "on a run with no coverage pass" if not graded else \
                    "while the core document leaves it unmarked"
            cov_mismatch.append(f"{n} carries {seen[0]} {where}")

        if foot:
            # Frequency and the frontier mark are copied like the coverage mark,
            # and go wrong the same way. A frequency rewritten here is a claim
            # about how often someone does something, made in the file that gets
            # forwarded.
            if normalise(foot.group(1)) != normalise(item_freq.get(n, "")):
                freq_off.append(
                    f"{n} is {item_freq.get(n, '')!r} in the core document, "
                    f"{foot.group(1)!r} here"
                )
            if ("⚡" in foot.group(0)) != item_frontier.get(n, False):
                frontier_off.append(
                    f"{n} {'carries' if '⚡' in foot.group(0) else 'omits'} ⚡, "
                    f"{'unlike' if '⚡' in foot.group(0) else 'unlike'} the core document"
                )

    if askless:
        shown = ", ".join(str(n) for n in askless[:12])
        more = f" (+{len(askless) - 12} more)" if len(askless) > 12 else ""
        rep.fail(
            f"{len(askless)} entry heading(s) carry no quoted ask: {shown}{more}. The heading "
            "is '#### <n> — \"<the ask>\"' so a reader knows what the scene expands without "
            "holding the core document open beside it."
        )
    if mismatched_ask:
        shown = ", ".join(str(n) for n in mismatched_ask[:12])
        more = f" (+{len(mismatched_ask) - 12} more)" if len(mismatched_ask) > 12 else ""
        rep.fail(
            f"{len(mismatched_ask)} entry heading(s) quote an ask unlike the core document's: "
            f"{shown}{more}. Shortening a long ask is fine; carrying a different one means the "
            "scene beneath it expands something the reader cannot find."
        )
    for f in freq_off:
        rep.fail(
            f"frequency disagrees with the core document: {f}. It is copied rather than "
            "restated — a frequency rewritten here is a claim about how often someone does "
            "something, made in the copy that gets forwarded."
        )
    for f in frontier_off:
        rep.fail(
            f"frontier mark disagrees with the core document: {f}. ⚡ is the class of ask this "
            "subject makes hard and valuable; adding or dropping one here re-grades the item."
        )
    if two_footers:
        rep.fail(
            f"entr(y/ies) {two_footers} carry more than one footer. Two versions of the fourth "
            "part leave a reader with two frequencies and two coverage marks for one ask, and "
            "neither line says which is stale."
        )
    if no_footer:
        shown =", ".join(str(n) for n in no_footer[:12])
        more = f" (+{len(no_footer) - 12} more)" if len(no_footer) > 12 else ""
        rep.fail(
            f"{len(no_footer)} entr(y/ies) have no footer line: {shown}{more}. The footer is the "
            "fourth required part — frequency, the frontier mark, the coverage mark and the "
            "topics — and it is the only place an entry says what it is about."
        )
    if no_mark:
        shown = ", ".join(str(n) for n in no_mark[:12])
        more = f" (+{len(no_mark) - 12} more)" if len(no_mark) > 12 else ""
        rep.fail(
            f"{len(no_mark)} entr(y/ies) carry no coverage mark in their footer: {shown}{more}. "
            "The mark is what tells a reader which of the three third-block forms they are "
            "reading; without it the entry is a scene with no stated relation to what exists."
        )
    for m in misplaced:
        rep.fail(
            f"third-block heading is not the third block: {m}. The order is the situation, then "
            "why it matters, then what answering it takes — a reader who finds the capability "
            "before the stakes has been given the answer to a question not yet asked."
        )
    if unheaded:
        shown = ", ".join(str(n) for n in unheaded[:12])
        more = f" (+{len(unheaded) - 12} more)" if len(unheaded) > 12 else ""
        rep.fail(
            f"{len(unheaded)} entr(y/ies) carry none of the three third-block headings: "
            f"{shown}{more}. Expected one of "
            + " / ".join(f"'{v}'" for v in dict.fromkeys(ENRICHED_HEADINGS.values()))
            + "."
        )
    if two:
        rep.fail(
            f"entr(y/ies) {two} carry more than one third-block heading. The heading is derived "
            "from the coverage mark, so exactly one of the three can be right."
        )
    for w in wrong:
        rep.fail(
            f"third-block heading does not match the coverage mark: {w}. The mark selects the "
            "heading; a served item described in the conditional understates it, and an unserved "
            "one described in the present tense claims a capability that does not exist."
        )
    for c in cov_mismatch:
        rep.fail(
            f"coverage mark disagrees with the core document: {c}. The enriched footer copies "
            "the mark rather than restating it — ○ is a finding, and a run that assessed nothing "
            "has not earned one."
        )

    # Header declarations. These are what a detached reader has instead of the
    # core document, and every one of them was added because it was found
    # missing: a frequency pill reads as measurement, a coverage mark is
    # unreadable without its key, and the Phase 7b findings name the very items
    # this pass rewrites into their most persuasive form.
    values: dict[str, str] = {}
    for label, key in (("Frequencies", "frequency basis"), ("Topics", "topic axis")):
        all_of = re.findall(rf"^\*{{0,2}}{label}\*{{0,2}}:\*{{0,2}}(.*)$", header, re.M)
        if len(all_of) > 1:
            # One address, as everywhere else in this method. Two declarations
            # give a detached reader both bases for the same pills, and neither
            # line says which of them is stale.
            rep.fail(
                f"{len(all_of)} **{label}:** lines in the enriched header. A declaration read "
                "from two places is read from neither."
            )
        m = re.search(rf"^\*{{0,2}}{label}\*{{0,2}}:\*{{0,2}}(.*)$", header, re.M)
        if not m:
            rep.fail(
                f"no **{label}:** line in the enriched header. It is copied from the core "
                f"document so the {key} survives the file being read on its own."
            )
        elif not is_substantive(m.group(1).strip().strip("*").strip()):
            rep.fail(f"**{label}:** is present but declares nothing.")
        else:
            values[label] = m.group(1).strip().strip("*").strip()

    # Copied, not restated. A core document declaring its frequencies estimated
    # and an enrichment declaring them measured is the single most consequential
    # disagreement the two can have: it changes how a reader takes every pill on
    # every card, and the enriched file is the one that gets forwarded.
    core_freq = claims.get("freq_basis")
    if core_freq and "Frequencies" in values:
        flat = lambda v: re.sub(r"\s+", " ", v).strip().rstrip(".").lower()
        if flat(values["Frequencies"]) != flat(core_freq):
            rep.fail(
                "the enriched **Frequencies:** line does not match the core document's. It is "
                f"copied rather than rewritten — the core says {core_freq!r}, this says "
                f"{values['Frequencies']!r}."
            )

    # Anchored to the start of a line, like every other canonical declaration in
    # this method: unanchored, a sentence merely *mentioning* the Verification
    # section satisfies the requirement to carry it.
    carried = re.search(
        r"^\*{0,2}Carried from the core document'?s Verification section:?\*{0,2}(.*)",
        header, re.I | re.M)
    if not carried:
        rep.fail(
            "the core document's Verification section is not carried into the enriched header. "
            "Phase 7b records what is wrong with these items; this pass rewrites those same "
            "items into their most persuasive form, and a file carrying the scenes without the "
            "warnings inverts the point of the phase that produced them."
        )
    elif not is_substantive(carried_block(header, carried.start(1))):
        # The label alone satisfies a label check while carrying nothing, which
        # is the same defect --final catches in the core document: an absent
        # verification reads as a passed one.
        rep.fail(
            "the carried Verification line is present but records no findings. A label with "
            "nothing after it reads as though the adversarial pass found nothing, which is a "
            "stronger claim than the document is making."
        )
    elif verification_problem(core_text):
        rep.fail(
            f"the core document {verification_problem(core_text)}, so it has not passed --final "
            "and there is nothing for this pass to carry. Run Phase 7b on the core document "
            "first: these passes amplify what is already there."
        )
    elif not shares_vocabulary(carried_block(header, carried.start(1)),
                               core_verification(core_text)):
        rep.fail(
            "the carried Verification findings have no vocabulary in common with the core "
            "document's Verification section. A tight summary is allowed; replacing the "
            "findings with something reassuring is the failure this line exists to prevent."
        )

    # Sentence by sentence, and negation-free. Matching a window between two
    # phrases keeps admitting the opposite claim by a route the window does not
    # cover: "are not invented" was rejected, then "no scenes are invented"
    # walked straight through it.
    def affirms(sentence: str) -> bool:
        m = re.search(r"\bare invented\b", sentence, re.I)
        if not m or not re.search(r"\bscenes\b", sentence[: m.start()], re.I):
            return False
        # Only the clause making the claim. What follows it is free to say what
        # the scenes are *not* — "not an observed incident" is the template's
        # own next words, and a whole-sentence negation test rejects it.
        return not re.search(r"\b(no|not|never|nothing|none)\b",
                             sentence[: m.end()], re.I)

    # Trailing markdown and quote characters do not end a sentence, but they do
    # sit between the full stop and the whitespace -- and a bare (?<=[.!?])\s+
    # then never splits there. The templates all open with an italic provenance
    # line, "_... changes nothing in it._", so the sentence after it joined the
    # same chunk and the negation guard below found that line's "nothing". The
    # declaration was present, correct, and reported as absent.
    affirmed = any(affirms(s) for s in re.split(r"(?<=[.!?])[_*\"'”’)\]]*\s+", header))
    if not affirmed:
        rep.fail(
            "the enriched header carries no affirmative statement that the scenes are invented "
            "— expected a sentence of the form 'The scenes are invented.' The word appearing "
            "somewhere is not the same declaration: 'the scenes are not invented' contains it "
            "and says the opposite. Each situation is a reconstruction of how the ask arises, "
            "and prose is read as reporting unless it says otherwise once."
        )

    # The frontier legend travels at every coverage depth, because the frontier
    # is a property of the items rather than of the coverage pass: a depth-None
    # run's footers still carry ⚡ and still need it explained.
    # The legend, not the character. A ⚡ appearing in a quoted footer or an
    # aside satisfies a containment test while explaining nothing, and the
    # diagnostic promises an explanation.
    if any(it.frontier for it in items) and not re.search(
            r"⚡[^\n]{0,30}\bfrontier\b|\bfrontier\b[^\n]{0,30}⚡", header, re.I):
        rep.fail(
            "the enriched header does not explain ⚡, which the entries carry — expected the "
            "core document's '**⚡ marks the frontier** — …' legend. The frontier class is "
            "specific to this subject, and a reader who does not know it reads every frontier "
            "entry as wishful thinking."
        )

    keys = re.findall(r"^\*{0,2}Coverage key\*{0,2}:\*{0,2}(.*)", header, re.M)
    if len(keys) > 1:
        rep.fail(
            f"{len(keys)} **Coverage key:** lines in the enriched header. Two keys give a "
            "standalone reader two incompatible readings of the same marks."
        )
    key = re.search(r"^\*{0,2}Coverage key\*{0,2}:\*{0,2}(.*)", header, re.M)
    unassessed = re.search(r"^\*{0,2}Coverage\*{0,2}:\*{0,2}\s*not assessed", header, re.M | re.I)
    if graded and not key:
        rep.fail(
            "no **Coverage key:** line in the enriched header, but the entries carry coverage "
            "marks. A reader who cannot tell ◐ from ○ cannot read them."
        )
    elif graded:
        # A label is not a key. What can be checked is that every mark the
        # entries use is explained; whether the explanations are the right way
        # round is not mechanical, and the reference says so.
        absent = [c for c in ("✅", "◐", "○") if c not in key.group(1)]
        if absent:
            rep.fail(
                f"**Coverage key:** does not explain {' '.join(absent)}, which the entries use. "
                "A key that omits a mark is worse than none: it reads as complete."
            )
    if not graded and not unassessed:
        rep.fail(
            "no '**Coverage:** not assessed' line in the enriched header. On a run with no "
            "coverage pass the key is replaced rather than deleted: a deleted line and an "
            "unassessed run look identical to a detached reader, and an unlabelled absence "
            "is read as a finding."
        )
    if key and unassessed:
        rep.fail(
            "the enriched header carries both a **Coverage key:** and a '**Coverage:** not "
            "assessed' line. One replaces the other — together they tell a detached reader "
            "that coverage was both assessed and not, and neither line says which is stale."
        )


# The five kinds a grievance may be. Closed, like the frequency vocabulary and
# the evidence marks, and for the same reason: an open one accumulates synonyms
# until the field sorts nothing.
ADVERSARIAL_KINDS = ("it's wrong", "it's expensive", "it refuses", "it surprises",
                     "the expectation gap")
# The blocks an entry carries, in the order the reference sets out.
ADVERSARIAL_BLOCKS = ("About", "Kind", "What they expected", "What it costs",
                      "What would fix it")


STOPWORDS = {
    "the", "and", "that", "this", "with", "from", "which", "were", "was", "are",
    "for", "not", "its", "it's", "their", "them", "they", "have", "has", "had",
    "than", "then", "into", "onto", "over", "under", "each", "every", "some",
    "any", "all", "one", "two", "three", "found", "read", "does", "did", "but",
    "section", "document", "core", "verification", "findings", "finding",
}


def core_verification(core_text: str) -> str:
    m = re.search(r"^#{2,3}\s*Verification\b[^\n]*\n(.*?)(?=^#{2}\s|\Z)", core_text, re.M | re.S)
    return m.group(1) if m else ""


def verification_problem(core_text: str) -> str:
    """Why the core document's Verification section fails --final, or "".

    One definition, used by --final and by both optional passes. Each had its
    own approximation of "the core passed --final" and they disagreed: a
    one-line Verification section was refused by --final and accepted by the
    passes whose precondition is that --final passed.
    """
    body = core_verification(core_text)
    if not body:
        return ("has no Verification section — Phase 7b was skipped or its findings were not "
                "recorded")
    # Substantive, not merely non-empty. A line count let five one-character
    # lines satisfy a gate whose whole job is recording five answers -- the
    # check fired on an empty section and passed a meaningless one, which is
    # the shape this suite calls a claim satisfied by a non-claim.
    # Blocks, not lines. Phase 7b asks five questions and this is standing in
    # for "five answers are recorded" -- so a single answer hard-wrapped across
    # five physical lines used to satisfy it while four questions went
    # unanswered. A blank-line-separated block is the closest structural proxy
    # for one answer that does not also dictate the section's format; requiring
    # five bullets would reject a section written as prose, which the method
    # nowhere forbids.
    lines = verification_answers(body)
    if len(lines) < 5:
        filled = len([b for b in re.split(r"\n\s*\n", body) if b.strip()])
        # "0 substantive of 5 present" and "0 substantive of 0 present" are
        # different defects -- placeholders standing in for answers, versus a
        # section nobody wrote -- and the author fixes them differently.
        detail = (f" ({filled} non-empty block(s) present, none substantive)"
                  if filled > len(lines) else "")
        return (f"has a Verification section of {len(lines)} substantive block(s){detail}. "
                "Phase 7b asks five questions and requires the answers recorded, "
                "disagreements included")
    return ""


def distinctive(s: str) -> set[str]:
    # Apostrophes normalised first: a curly one in the source and a straight one
    # in the summary are the same word, and tokenising them apart makes a
    # faithful summary look like an unrelated sentence.
    return {w for w in re.findall(r"[a-z][a-z'-]{3,}", normalise(s)) if w not in STOPWORDS}


def shares_vocabulary(carried: str, source: str) -> bool:
    """True when the carried text plausibly derives from the source.

    A floor scaled to the source, not a match. The reference allows the findings
    verbatim *or* tightly summarised, so the verbatim comparison the frequency
    basis gets would be wrong — but a summary of a long section shares more with
    it than a two-word phrase does, and the floor grows with the section.

    What this detects is wholesale replacement. It cannot prove every finding
    survived, and neither the message nor the reference claims it does.
    """
    src = distinctive(source)
    if not src:
        return True
    return len(distinctive(carried) & src) >= max(3, min(6, len(src) // 8))


def appendix_section(core_text: str) -> str:
    """The appendix that carries the inventory, or "" when there is none.

    Scoped rather than whole-document, because both callers use the result as
    proof that an inventory *exists*. Searching everywhere accepted any
    lane-shaped text as that proof: a fenced example, or the Verification
    section quoting the expected row syntax, satisfied the guard while the
    appendix itself was gone. Fences are blanked first for the same reason --
    an example of a lane row is not a lane.

    The appendix is identified by what its heading says it is, not by whether it
    happens to contain lane-shaped rows. Selecting on shape accepted the wrong
    appendix entirely: a document may carry several, and one of them holding a
    row that looks like a lane is not evidence that the inventory survived. A
    movement or comparison appendix tabulating lanes will do it, which is not
    hypothetical -- the run that found this has exactly that pair.

    The letter is deliberately not fixed. The template writes "Appendix A" but a
    document letters its appendices in the order it uses them, and this run's
    own inventory is Appendix C. What the template does fix is the subject:
    "Current coverage".
    """
    body = blank_fences(core_text)
    for m in re.finditer(r"^(#{2,3})\s*Appendix\s+[A-Z]\b([^\n]*)$", body, re.M):
        # Exactly the two words output-template.md documents. "lanes" was in
        # this list and is not in that rule, and the gap was reachable: an
        # appendix headed "Lanes moved" -- a movement table, not an inventory --
        # satisfied the guard while the inventory itself was deleted. Both
        # reviewers found it independently, which is what a whitelist wider than
        # its own documentation earns.
        if not re.search(r"\b(coverage|inventory)\b", m.group(2), re.I):
            continue
        # Stop at the next heading of the same level or higher. The search above
        # accepts an H3 appendix, so terminating only at the next H2 let an H3
        # inventory swallow its sibling appendices -- an empty
        # "### Appendix B - Current coverage" absorbed a later
        # "### Appendix C - Run comparison", whose lane row then proved the
        # missing inventory existed. Matching two heading depths and stopping at
        # one is the same rule read two ways.
        level = len(m.group(1))
        stop = re.search(r"^#{2,%d}\s" % level, body[m.end():], re.M)
        section = body[m.end():m.end() + stop.start()] if stop else body[m.end():]
        if re.search(r"\|\s*\*\*[A-Z]\s*[—\-–]", section):
            return section
    return ""


def verification_answers(body: str) -> list[str]:
    """The distinct answers recorded in a Verification section.

    Phase 7b asks five questions, so the count standing in for "five answers
    were recorded" has to track answers rather than typography. Two shapes both
    have to work, and counting either unit alone breaks the other:

    - counting physical lines let ONE answer hard-wrapped over five lines pass
      while four questions went unanswered;
    - counting blank-line-separated blocks then rejected five answers written
      as an ordinary Markdown list, because adjacent list items share a block.

    So: split on blank lines, then split each block again at list markers and
    table rows, joining soft-wrapped continuation lines into the entry above.
    Nothing here dictates the section's format, which is the point -- the method
    nowhere requires bullets, or prose, or a table.

    Table rulers carry no letters and fall out at is_substantive, so a table
    contributes its header and its data rows and not its underline.
    """
    entry_start = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+|^\s*\|")
    out: list[str] = []
    for block in re.split(r"\n\s*\n", body):
        entries: list[str] = []
        for line in block.splitlines():
            if entry_start.match(line) or not entries:
                entries.append(line)
            else:
                entries[-1] += " " + line.strip()
        out.extend(e for e in entries if is_substantive(e))
    return out


def core_lanes(core_text: str) -> set[str]:
    """Lane identifiers from the inventory appendix: the letter, and its name."""
    out: set[str] = set()
    for m in re.finditer(r"\|\s*\*\*([A-Z])\s*[—\-–]\s*([^*|]+?)\*\*",
                         appendix_section(core_text)):
        out.add(m.group(1))
        out.add(normalise(m.group(2).strip()))
    return out


def check_adversarial(roster: dict, items: list[Item], core_text: str,
                      text: str, rep: Report) -> None:
    """Check an adversarial pass output against the core document it reads.

    The gate this exists for: a grievance is about something that exists, so it
    names the Appendix A lane it is about. Without that the pass regenerates the
    unserved list in an irritated tone, and a well-written duplicate reads fine.
    """
    if not any(it.coverage.strip() for it in items):
        rep.fail(
            "the core document has no coverage marks, so this pass has nothing to run against. "
            "A persona cannot resent a hypothetical — only the thing that exists — which is why "
            "adversarial mode requires coverage depth Full or Light."
        )
        return

    text = blank_fences(text)
    lanes = core_lanes(core_text)
    if not lanes:
        # Not permission to skip the rule. An unreadable appendix means the one
        # gate this pass exists for cannot run, and a checker that quietly
        # stops checking is worse than one that refuses: the document passes and
        # nobody learns that nothing was verified.
        rep.fail(
            "no inventory lanes could be read from the core document, so the rule this pass "
            "turns on — every grievance names the lane it is about — cannot be checked at all. "
            "Lanes are read from rows of the form '| **A — The documented path** | …' in the "
            "appendix that carries them; any appendix letter will do."
        )
        return

    starts = []
    heads: dict[str, str] = {}
    for m in re.finditer(r"^####\s+(P\d+)-(\d+)\s*[—\-–]\s*(.*)$", text, re.M):
        key = f"{m.group(1)}-{m.group(2)}"
        starts.append((key, m.group(1), m.start()))
        # The heading wraps in the reference's own example, so the complaint is
        # read from the heading plus its continuation, not from one line.
        # Stops at the first block as well as at a blank line: without the
        # blank line the continuation swallowed the About block, and a quoted
        # phrase there stood in for the complaint the heading was missing.
        tail = re.split(r"\n\s*\n|\n\s*\*\*", text[m.end():], maxsplit=1)[0]
        heads.setdefault(key, m.group(3) + " " + tail.replace("\n", " "))
    if not starts:
        rep.fail(
            "no grievance entries found. Each one gets a '#### P<n>-<k> — \"<the complaint>\"' "
            "heading, numbered per persona; without them there is nothing to check."
        )
        return

    header = text[: starts[0][2]]
    seen: dict[str, tuple[int, int]] = {}
    dupes: list[str] = []
    for idx, (key, pid, pos) in enumerate(starts):
        end = starts[idx + 1][2] if idx + 1 < len(starts) else len(text)
        if key in seen:
            dupes.append(key)
        else:
            seen[key] = (pos, end)
    if dupes:
        rep.fail(
            f"duplicate grievance id(s): {sorted(set(dupes))}. Numbering is per persona and has "
            "to identify one entry, or a reader following a reference gets whichever comes first."
        )

    off_roster = sorted({pid for _, pid, _ in starts if pid not in roster})
    if off_roster:
        rep.fail(
            f"grievances for {off_roster}, who are not on the approved roster. This pass reuses "
            "the roster the user approved at Phase 1; a roster that grows during an optional "
            "pass has skipped that gate."
        )

    unquoted: list[str] = []
    missing_blocks: list[str] = []
    duplicated_blocks: list[str] = []
    empty_blocks: list[str] = []
    statusless: list[str] = []
    bad_kind: list[str] = []
    no_mark: list[str] = []
    malformed_mark: list[str] = []
    multi_mark: list[str] = []
    off_vocab: list[str] = []
    unsourced: list[str] = []
    sourced_invention: list[str] = []
    laneless: list[str] = []
    promiseless: list[str] = []
    observed_count = 0

    for key in sorted(seen):
        start, end = seen[key]
        body = text[start:end]
        if not re.search(r"[\"“](.+?)[\"”]", heads.get(key, ""), re.S):
            unquoted.append(key)

        # The label's trailing period lives inside the bold — "**What it
        # costs.**" — so it has to come off the key or no block ever matches.
        labels = {}
        blocks = {}
        spans = {}
        counts: dict[str, int] = {}
        # Only the five known block labels open a block. Any bold run at the
        # start of a line used to, which meant a continuation line beginning
        # with emphasis -- "**verified**. *(observed: ..." after a soft wrap --
        # was read as a new label and silently truncated the block above it.
        # The labels are a closed set, so matching against it is exact, and a
        # mistyped label now reports as an absent block rather than corrupting
        # its neighbour.
        _known = {normalise(b).strip(" .:") for b in ADVERSARIAL_BLOCKS}
        found_labels = [m for m in re.finditer(r"^\*\*([^*]+?):?\*\*:?(.*)$", body, re.M)
                        if normalise(m.group(1)).strip(" .:") in _known]
        for i, m in enumerate(found_labels):
            k = normalise(m.group(1)).strip(" .:")
            counts[k] = counts.get(k, 0) + 1
            labels.setdefault(k, m.group(2).strip())
            # Two extents, deliberately. `labels` is the label's own line, which
            # is what a one-line field like Kind means. `blocks` is the whole
            # block, which is what a field whose content gets *searched* means:
            # About carries a lane, a status word and a mark on one long line,
            # and reading only line one failed a correct document the moment it
            # soft-wrapped. The reference's own worked example wraps its heading
            # because these lines are long, and every other continuation in this
            # checker is handled -- heading, primitive entry, carried finding.
            _stop = (found_labels[i + 1].start()
                     if i + 1 < len(found_labels) else len(body))
            blocks.setdefault(k, re.sub(r"\s+", " ",
                                        (m.group(2) + " " + body[m.end():_stop]).strip()))
            spans.setdefault(k, m.end(1))
            # The block's content runs to the next label, so a label with an
            # empty body is visible. Presence alone let an entry carry all five
            # headings and no expectation, no cost and no remedy.
            stop = found_labels[i + 1].start() if i + 1 < len(found_labels) else len(body)
            if k in {normalise(b).strip(" .:") for b in ADVERSARIAL_BLOCKS[2:]}:
                # The rest of the label's own line plus everything up to the
                # next label: the template puts the block's first sentence on
                # the label line, so reading only what follows the match finds
                # nothing and fails every conforming document.
                if not is_substantive(m.group(2) + " " + body[m.end():stop]):
                    empty_blocks.append(f"{key}'s {m.group(1).strip(' .:')} is empty")
        # setdefault kept the first and ignored the rest, so a stale block sat
        # beside its replacement and the entry read as consistent -- the same
        # failure the two-marks rule already refuses one level down.
        repeated = sorted(b for b in ADVERSARIAL_BLOCKS
                          if counts.get(normalise(b).strip(" .:"), 0) > 1)
        if repeated:
            duplicated_blocks.append(f"{key} repeats {', '.join(repeated)}")
        absent = [b for b in ADVERSARIAL_BLOCKS if normalise(b).strip(" .:") not in labels]
        if absent:
            missing_blocks.append(f"{key} is missing {', '.join(absent)}")

        kind = normalise(labels.get("kind", "")).strip(" .")
        if "kind" in labels and kind not in {normalise(k) for k in ADVERSARIAL_KINDS}:
            bad_kind.append(f"{key} says {labels['kind'].strip() or '(nothing)'!r}")

        about = blocks.get("about", "")
        # The mark is read from the About block, anchored at the label's own
        # position rather than found by searching for its text: the About text
        # can occur earlier in the entry — quoted in the complaint, say — and a
        # find() then slices from the wrong place and reports a missing mark.
        about_block = blocks.get("about", "")
        # One definition, one home: this was a second copy of the mark pattern
        # and it drifted from MARK_RE the moment MARK_RE was fixed, so a mark
        # that parsed for a primitive still vanished for a grievance.
        marks = re.findall(MARK_RE, about_block)
        if not marks:
            if re.search(MARK_ATTEMPT_RE, about_block):
                malformed_mark.append(key)
            else:
                no_mark.append(key)
        elif len(marks) > 1:
            multi_mark.append(key)
        else:
            kindname, source = marks[0][0].lower(), (marks[0][1] or "").strip()
            if kindname not in EVIDENCE:
                off_vocab.append(f"{key} is marked {kindname!r}")
            elif kindname in ("observed", "inferred") and not is_source(source):
                unsourced.append(f"{key} is {kindname} and names no source")
            elif kindname == "invented" and source:
                sourced_invention.append(f"{key} is invented and names a source")
            if kindname == "observed":
                observed_count += 1

        if kind == normalise("the expectation gap"):
            # The one laneless kind, and it is not exempt from citing anything:
            # it names the promise and where it is made. An expectation traced
            # to nothing is a preference, and belongs in the core document.
            stripped = re.sub(r"\*\([^)]*\)\*", "", about)
            # Both halves, not either: the promise *and* where it is made. An
            # alternation accepted a quotation with no location and a filename
            # with no promise, and each of those is half a citation.
            promise = re.search(r"[\"“][^\"”]+[\"”]", stripped)
            where = re.search(r"`[^`]+`|\[[^\]]+\]\([^)]+\)|https?://"
                              r"|\b[\w./-]+\.(?:md|html|txt|json|ya?ml)\b|:\d+", stripped)
            if not (promise and where):
                promiseless.append(key)
        elif kind:
            # Case-insensitive: "lane B" names the same lane as "Lane B", and a
            # rule that fails on the capital is failing valid documents.
            if not any(re.search(rf"\blane {re.escape(l)}\b", about, re.I) if len(l) == 1
                       else l in normalise(about) for l in lanes):
                laneless.append(key)
            elif not re.search(r"\b(verified|proven|light|unverified|documented)\b",
                               about, re.I):
                # Shape, not truth: this cannot tell whether the status named is
                # the one Appendix A records, only that the entry states one. A
                # scoped Full run leaves some lanes Light, so an entry silent
                # about its lane's status reads as resting on verified inventory.
                statusless.append(key)

    for label, entries, message in (
        ("carry no quoted complaint", unquoted,
         "The complaint is a sentence the persona would say out loud, held to the same standard "
         "as an ask. A bug title is not one."),
        ("carry no evidence mark", no_mark,
         "An unmarked grievance is an accusation: it asserts in someone's voice that real people "
         "are unhappy with a real thing, to the person who owns that thing."),
        ("carry an evidence mark that could not be read", malformed_mark,
         "The mark is present -- do not add another, which the two-marks rule refuses -- but its "
         "source runs past the closing delimiter. The usual cause is a ')' inside the source "
         "text; the mark ends at the first ')*', so quote carefully or reword."),
        ("carry more than one evidence mark", multi_mark,
         "Keeping the first would let a stale mark sit beside its replacement and read as "
         "consistent."),
        ("cite no promise", promiseless,
         "An expectation gap is the one kind that may skip the lane, because the capability it "
         "implies has none — but it names the promise that created the belief and where that "
         "promise is made: a quotation, a backticked reference, a link, or a file. An "
         "expectation traced to nothing is a preference, and preferences are asks."),
        ("name no verification status for the lane they cite", statusless,
         "A scoped Full run leaves some lanes Light, so the run's depth says nothing about "
         "the lane a given grievance rests on. Name it: verified, proven, Light, unverified, "
         "or documented. This checks that a status is stated, not that it is the right one."),
        ("name no inventory lane", laneless,
         "A grievance is about something that exists. If nothing in the appendix carries it, the "
         "complaint is an unserved ask and is already in the core document. Only the expectation "
         "gap is exempt, and it names the promise instead."),
    ):
        if entries:
            shown = ", ".join(entries[:12])
            more = f" (+{len(entries) - 12} more)" if len(entries) > 12 else ""
            rep.fail(f"{len(entries)} grievance(s) {label}: {shown}{more}. {message}")

    for group, message in (
        (empty_blocks, "A heading with nothing under it satisfies a shape check while "
                       "carrying none of what the block is for."),
        (duplicated_blocks, "One block, once. A stale one beside its replacement leaves a "
                            "reader two answers and no line saying which is current."),
        (missing_blocks, "Every entry carries all five blocks; the gap between expectation and "
                         "behaviour is the actionable part and it lives in two of them."),
        (bad_kind, "One of: " + ", ".join(repr(k) for k in ADVERSARIAL_KINDS) +
                   ". An open vocabulary accumulates synonyms until the field sorts nothing."),
        (off_vocab, "One of: " + ", ".join(EVIDENCE) + "."),
        (unsourced, "observed and inferred name what they rest on; invented needs nothing and is "
                    "not a lesser mark."),
        (sourced_invention, "invented means there is no artifact behind it. A source beside it "
                            "says the mark is wrong, not that the claim is stronger."),
    ):
        for entry in group:
            rep.fail(f"{entry}. {message}")

    # Header declarations, held to the rules --enriched arrived at one round at
    # a time: anchored, counted, and required to say something.
    depth = re.findall(r"^\*{0,2}Coverage depth\*{0,2}:\*{0,2}(.*)", header, re.M)
    if not depth:
        rep.fail(
            "no **Coverage depth:** line in the adversarial header. A grievance resting on a "
            "Light lane rests on a reading of documentation nobody checked, and this file is "
            "read detached from the core document that recorded the depth."
        )
    elif len(depth) > 1:
        rep.fail(f"{len(depth)} **Coverage depth:** lines in the adversarial header.")
    elif not re.match(r"\s*\*{0,2}(full|light)\b", depth[0], re.I):
        # The value, not a mention of it. Searching anywhere accepted
        # "None, not Full or Light" — a line declaring the one depth this pass
        # refuses, passing on the word it used to refuse it.
        rep.fail(
            f"**Coverage depth:** says {depth[0].strip()!r}, which does not open with Full or "
            "Light. Those are the two depths this pass can run at, and the line states one of "
            "them rather than discussing them."
        )

    carried = re.search(
        r"^\*{0,2}Carried from the core document'?s Verification section:?\*{0,2}(.*)",
        header, re.I | re.M)
    if not carried:
        rep.fail(
            "the core document's Verification section is not carried into the adversarial "
            "header. Phase 7b may have questioned the very personas this pass writes complaints "
            "for, and a file carrying the grievances without those findings inverts it."
        )
    elif verification_problem(core_text):
        # The precondition is that the core passed --final. Checking only that
        # the section is non-empty was a weaker rule than --final's own, so a
        # document --final refuses was accepted by the pass whose precondition
        # is that --final accepted it.
        rep.fail(
            f"the core document {verification_problem(core_text)}, so it has not passed --final "
            "and there is nothing for this pass to carry. Run Phase 7b on the core document "
            "first: these passes amplify what is already there."
        )
    else:
        block = carried_block(header, carried.start(1))
        if not is_substantive(block):
            rep.fail("the carried Verification line is present but records no findings.")
        elif not shares_vocabulary(block, core_verification(core_text)):
            # A floor, not a match. The reference allows the findings verbatim
            # *or* tightly summarised, so an exact comparison would be wrong —
            # but a summary of a document shares words with it, and "everything
            # passed" written over three recorded findings shares none.
            rep.fail(
                "the carried Verification findings have no vocabulary in common with the core "
                "document's Verification section. A tight summary is allowed; replacing the "
                "findings with something reassuring is the failure this line exists to prevent."
            )

    # Negation-checked, like the enriched disclosure: a bold sentence saying the
    # observed entries are *not* reported complaints contains the word and
    # asserts the opposite of the rule it is standing in for.
    # And what it asserts, not only its polarity. A bold sentence saying the
    # observed entries are "fictional reconstructions" is affirmative, mentions
    # the word, and states the opposite relationship.
    disclosed = any(
        not re.search(r"\b(no|not|never|nothing|none)\b", m.group(0), re.I)
        and re.search(r"\breport|complaint", m.group(0), re.I)
        for m in re.finditer(r"^\*\*[^*]*\bobserved\b[^*]*\*\*", header, re.M)
    )
    if not disclosed:
        rep.fail(
            "the adversarial header does not say which entries are reported complaints — "
            "expected a declaration of the form '**Only the `observed` entries are reported "
            "complaints.**'. inferred and invented are both reconstructions, and a source named "
            "beside inferred reads as established unless the header says otherwise."
        )
    # A declaration, not advice. "Do not label invented entries observed" is a
    # negation near the word and instructs the author rather than telling the
    # reader what this run contains, so the assertion has to be a bold
    # declaration and must not be an imperative.
    said_none_observed = any(
        re.search(r"\b(no|none|nothing)\b", m.group(0), re.I)
        and not re.match(r"\*\*\s*(do|don't|do not|never|avoid|always)\b", m.group(0), re.I)
        for m in re.finditer(r"^\*\*[^*]*\bobserved\b[^*]*\*\*", header, re.M)
    )
    if not observed_count and not said_none_observed:
        rep.fail(
            "no grievance is marked observed, and the header does not say so. A run where every "
            "entry is a reconstruction is a list of ways the subject would plausibly frustrate "
            "these personas, not a report of complaints anyone made — and that belongs in the "
            "header rather than inferred from the marks."
        )


def main() -> int:
    # This method's vocabulary is not ASCII -- the frontier mark is in almost
    # every message -- and a console that cannot encode it must still get the
    # findings. Without this the checker raises UnicodeEncodeError instead of
    # reporting, which reads as a crash rather than as a verdict.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    ap.add_argument(
        "--final",
        action="store_true",
        help="also require the Phase 7b Verification section (run after the adversarial read)",
    )
    ap.add_argument(
        "--enriched",
        metavar="PATH",
        help="also check an enrichment pass output against this core document",
    )
    ap.add_argument(
        "--adversarial",
        metavar="PATH",
        help="also check an adversarial pass output against this core document",
    )
    args = ap.parse_args()

    text = open(args.path, encoding="utf-8").read()
    rep = Report()
    parsed = parse(text)
    check(*parsed, rep)
    if args.enriched:
        # Checked against the core document rather than alone, because every
        # rule worth checking is a relation between the two: the heading a mark
        # selects, the items that must all be present, the declarations copied
        # across. An enriched file has no meaning apart from what it expands.
        check_enriched(parsed[1], parsed[3], text,
                       open(args.enriched, encoding="utf-8").read(), rep)
    if args.adversarial:
        # The core text as well as its parse: the lane identifiers a grievance
        # has to cite live in Appendix A, which the item tables do not carry.
        check_adversarial(parsed[0], parsed[1], text,
                          open(args.adversarial, encoding="utf-8").read(), rep)
    # A graded document whose inventory is gone. Coverage marks are claims about
    # what the subject serves, and Appendix A is the only thing in the document
    # that grounds them -- so a Full or Light run with no readable lanes states
    # sixty findings and carries the evidence for none. This was reachable:
    # truncating a document at its appendix heading left --final passing at
    # exit 0 with a full tally still on the page.
    #
    # Marks are the trigger rather than a declared depth, deliberately. A
    # depth-None run has no marks and no appendix and is correct; a graded run
    # has both. The two are told apart by what the document already carries,
    # which costs no new required field and cannot go stale.
    if any(it.coverage.strip() for it in parsed[1]) and not core_lanes(text):
        msg = ("this document grades coverage but no inventory lanes can be read from it. "
               "Every coverage mark is a claim about what the subject serves today, and the "
               "inventory is what grounds them — without it the tally is sixty findings with no "
               "evidence behind any of them. Lanes are read from rows of the form "
               "'| **A — The documented path** | …', in an appendix whose heading names coverage or the inventory — the letter is free, the subject is not, because a movement or comparison appendix carrying a lane-shaped row is not an inventory. A run at coverage depth None has no marks "
               "and needs no appendix; this one has marks.")
        rep.fail(msg) if args.final else rep.warn(msg)

    if args.final:
        m = re.search(r"^#{2,3}\s*Verification\b[^\n]*\n(.*?)(?=^#{2}\s|\Z)", text, re.M | re.S)
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
            # Substantive, not merely non-empty: a body of "x/y/z/a/b" cleared a
            # bare line count while recording nothing at all. is_substantive is
            # the same bar every required field is already held to.
            # Blocks, not lines -- one answer wrapped over five lines is one
            # answer. See core_verification_problem for why blocks rather than
            # bullets.
            body = verification_answers(m.group(1))
            filled = len([b for b in re.split(r"\n\s*\n", m.group(1)) if b.strip()])
            if len(body) < 5:
                # Say which of the two it is. A section of placeholder lines and
                # a section nobody wrote both count zero, and the author fixes
                # them differently -- one is a stub to fill in, the other is a
                # phase that was skipped.
                detail = (f", from {filled} non-empty placeholder block(s)"
                          if filled > len(body) else "")
                rep.fail(
                    f"Verification section has {len(body)} substantive block(s){detail}. Phase 7b "
                    "asks five questions and requires the answers recorded, disagreements "
                    "included; a heading on its own, or placeholder lines, passes a bare line "
                    "count without carrying any of them."
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
