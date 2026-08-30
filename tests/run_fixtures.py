#!/usr/bin/env python3
"""Fixture suite for skills/persona-brainstorm/scripts/verify.py.

Run: python tests/run_fixtures.py

Every case asserts a **message**, not just an exit code. That distinction is
the whole design. A fixture written to test one check will, once a later
requirement is added to the document schema, start failing on the new
requirement instead — still red, still "expected", and no longer testing
anything. Five rounds of review on PR #6 produced exactly that: fixtures for
unquoted asks, non-ASCII substance and reckoning arithmetic were all failing
on a missing **Frequencies:** line added rounds after they were written. A
verdict-only suite reported them green.

The second defence is structural. Most negatives are generated here by
mutating a known-good base document, so a schema change costs one edit to the
base rather than one edit per fixture. Static files are kept only where a
mutation cannot express the defect.
"""
import os
import re
import subprocess
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "fixtures")
REPO = os.path.normpath(os.path.join(HERE, os.pardir))
# The skill ships as a plugin, so everything it needs at runtime lives under
# skills/<name>/ and travels with it. The suite does not: it is a development
# artifact and stays at the repo root, which is why it has to reach in.
SKILL = os.path.join(REPO, "skills", "persona-brainstorm")
VERIFY = os.path.join(SKILL, "scripts", "verify.py")


class BrokenFixture(Exception):
    """A fixture invariant no longer holds.

    Not an assert: `python -O` strips those, and a stripped invariant here does
    not raise -- it lets a mutation target nothing and report the resulting
    document as correctly caught. The suite would go green by doing nothing,
    which is the exact false green this file exists to prevent.
    """


def require(condition, message):
    if not condition:
        raise BrokenFixture(message)


def load(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return fh.read()


def line_starting(text, prefix):
    """The one line beginning with prefix. Ambiguity is a broken fixture."""
    hits = [ln for ln in text.splitlines() if ln.startswith(prefix)]
    require(len(hits) == 1, f"expected exactly one {prefix!r} line, found {len(hits)}")
    return hits[0]


def drop(text, prefix):
    return text.replace(line_starting(text, prefix) + "\n", "", 1)


def swap(text, old, new):
    require(old in text, f"anchor not present: {old[:60]!r}")
    return text.replace(old, new, 1)


def edit_line(text, prefix, new_line):
    return swap(text, line_starting(text, prefix), new_line)


def twice(text, prefix):
    old = line_starting(text, prefix)
    return swap(text, old, old + "\n" + old)


# ---------------------------------------------------------------------------
# Bases. Each must pass on its own; every mutation below starts from one.
# ---------------------------------------------------------------------------
BASES = ["d_ok.md", "d_zero.md", "c_ok.md", "e_commas.md", "nocov.md",
         "legacy_yearly.md"]

FREQ = "**Frequencies:**"
AXIS = "**Roster axis:**"
PRE = "**Pre-registered:**"
LB = "**Load-bearing persona:**"
RECK = "**Reckoning:**"
TALLY = "**Tally:**"

# ---------------------------------------------------------------------------
# (name, base, mutation, expected-substring). Expected substring is the message
# the case's INTENT implies -- never merely the message it happens to emit.
# ---------------------------------------------------------------------------
def level4_subsection(text):
    """A level-4 heading and a numbered row, inside the last persona's section.

    The parse loop clears current_persona on "any other heading", but its
    pattern stopped at ###. A #### subsection therefore left the persona open,
    and the numbered row beneath it was charged to whoever was last -- the exact
    miscount that line exists to prevent, at the one depth it did not cover.

    Placed just above the tally, which is still inside P7's section: P7 promises
    five items and would be credited with six.
    """
    tally = line_starting(text, TALLY)
    row = ('| 61 | "An aside, not an ask." | Not a decision | Nothing | '
           "per-run | | ○ |")
    return swap(text, tally, "#### A note on P7's items\n\n" + row + "\n\n" + tally)


MUTATIONS = [
    # -- header declarations must be present and must say something ----------
    ("freq-missing", "d_ok.md", lambda t: drop(t, FREQ),
     "no **Frequencies:** line"),
    ("freq-placeholder", "d_ok.md", lambda t: edit_line(t, FREQ, FREQ + " TBD"),
     "**Frequencies:** is present but declares nothing"),
    ("axis-missing", "d_ok.md", lambda t: drop(t, AXIS),
     "no **Roster axis:** line"),
    ("axis-duplicated", "d_ok.md", lambda t: twice(t, AXIS),
     "2 **Roster axis:** lines"),
    ("prereg-missing", "d_ok.md", lambda t: drop(t, PRE),
     "no **Pre-registered:** line"),
    ("prereg-placeholder", "d_ok.md", lambda t: edit_line(t, PRE, PRE + " TBD"),
     "**Pre-registered:** is present but declares nothing"),
    ("loadbearing-missing", "d_ok.md", lambda t: drop(t, LB),
     "no **Load-bearing persona:** line"),

    # -- a pre-registration is a prediction, a threshold and a cut rule ------
    ("prereg-figure-not-predicted", "d_ok.md",
     lambda t: swap(t, "predicted 12/24/24 of 60", "historical baseline 12/24/24 of 60"),
     "states no prediction"),
    ("prereg-no-surprise-threshold", "d_ok.md",
     lambda t: edit_line(t, PRE, PRE + " predicted 12/24/24 of 60 · cut: no named decision"),
     "surprise threshold"),
    ("prereg-split-misses-budget", "d_ok.md",
     lambda t: swap(t, "predicted 12/24/24 of 60", "predicted 1/1/1 of 60"),
     "sums to 3"),
    ("prereg-denominator-disagrees", "d_ok.md",
     lambda t: swap(t, "predicted 12/24/24 of 60", "predicted 12/24/24 of 100"),
     "written against 100 items"),
    ("prereg-frontier-over-budget", "d_zero.md",
     lambda t: swap(swap(t, "predicted 0 ⚡ of 60", "predicted 100 ⚡ of 60"),
                    "predicted 0 ⚡, actual", "predicted 100 ⚡, actual"),
     "frontier items are a subset"),

    # -- the load-bearing persona has to be someone on the roster ------------
    ("loadbearing-unknown-id", "d_ok.md",
     lambda t: edit_line(t, LB, LB + " P99, the executing agent"),
     "does not contain"),
    ("loadbearing-names-nobody", "d_ok.md",
     lambda t: edit_line(t, LB, LB + " the person who runs it on a schedule"),
     "names nobody on the roster"),

    # -- the reckoning is checked against the pre-registration and the table -
    ("reckoning-missing", "d_ok.md", lambda t: drop(t, RECK),
     "no **Reckoning:** line in the synthesis"),
    ("reckoning-duplicated", "d_ok.md", lambda t: twice(t, RECK),
     "2 **Reckoning:** lines"),
    ("reckoning-is-prose", "d_ok.md", lambda t: edit_line(t, RECK, RECK + " done"),
     "missing predicted split and actual split"),
    ("reckoning-omits-actual", "d_ok.md",
     lambda t: edit_line(t, RECK, RECK + " predicted 12/24/24, prediction held"),
     "missing actual split"),
    ("reckoning-actual-contradicts-table", "d_ok.md",
     lambda t: swap(t, "actual 7/26/27", "actual 8/26/26"),
     "reports an actual split"),
    ("reckoning-restates-prediction", "d_ok.md",
     lambda t: edit_line(t, RECK, RECK + " predicted 11/24/25, actual 7/26/27 — moved"),
     "says it predicted"),
    ("reckoning-uses-percentages", "d_ok.md",
     lambda t: swap(t, "actual 7/26/27", "actual 12/43/45"),
     "counts, not percentages"),

    # -- one claimed figure, at one address ----------------------------------
    ("tally-missing", "d_ok.md", lambda t: drop(t, TALLY),
     "no canonical tally line"),
    ("tally-duplicated", "d_ok.md", lambda t: twice(t, TALLY),
     "2 canonical tally lines"),

    # -- evidence marks: well-formedness is gated, the kind never is ---------
    ("evidence-mark-missing", "d_ok.md",
     lambda t: swap(t, "`cross-run-aggregation` *(invented)*", "`cross-run-aggregation`"),
     "carry no evidence mark"),
    ("evidence-mark-off-vocabulary", "d_ok.md",
     lambda t: swap(t, "`cross-run-aggregation` *(invented)*",
                    "`cross-run-aggregation` *(high-confidence)*"),
     "not one of"),
    ("evidence-observed-without-source", "d_ok.md",
     lambda t: swap(t, "`self-assessment` *(observed: Caveat 1 in this document's appendix)*",
                    "`self-assessment` *(observed)*"),
     "names no source"),
    ("evidence-prose-example-is-not-a-mark", "d_ok.md",
     lambda t: swap(swap(t, "`cross-run-aggregation` *(invented)*", "`cross-run-aggregation`"),
                    "many subjects at once, and the needs common to all of them.",
                    "many subjects at once; render `*(invented)*` when explaining metadata."),
     "carry no evidence mark"),
    ("evidence-second-mark-after-the-description", "d_ok.md",
     lambda t: swap(t, "`cross-run-aggregation` *(invented)*",
                    "`cross-run-aggregation` *(invented)* — also *(observed: issue #12)*"),
     "more than one evidence mark"),
    ("evidence-invented-with-a-source", "d_ok.md",
     lambda t: swap(t, "`cross-run-aggregation` *(invented)*",
                    "`cross-run-aggregation` *(invented: issue #12)*"),
     "marked 'invented' but names a source"),
    ("evidence-two-marks-on-one-primitive", "d_ok.md",
     lambda t: swap(t, "`cross-run-aggregation` *(invented)*",
                    "`cross-run-aggregation` *(invented)* *(observed: an old note)*"),
     "more than one evidence mark"),
    ("evidence-inferred-without-source", "d_ok.md",
     lambda t: swap(t, "`run-identity` *(inferred: the frontier miscount recorded in the "
                       "disclosures)*", "`run-identity` *(inferred: TBD)*"),
     "names no source"),
]

# ---------------------------------------------------------------------------
# Mutations that must still PASS. Evidence annotation is only safe to require
# because it never penalises a finding for being imagined -- the frontier is
# invented by construction, and a gate on kind would quietly delete it. That
# property is the one most worth asserting, so it is asserted.
# ---------------------------------------------------------------------------
def all_invented(text):
    """Every mark in the document reduced to `invented`.

    Written as a sweep rather than a list of swaps: the earlier version named
    the two `observed` marks and silently left `inferred` in place, so the
    fixture passed while asserting something weaker than its name. Replacing
    every mark cannot drift as the base document changes.
    """
    out = re.sub(r"\*\(\s*(?:observed|inferred)\b[^)]*\)\*", "*(invented)*", text)
    require(out != text, "no observed/inferred marks in the base to invert")
    require(not re.search(r"\*\(\s*(?:observed|inferred)\b", out),
            "an observed/inferred mark survived the sweep")
    return out


def wrap_a_mark(text):
    """Break one annotation across a line, the way the template's own layout does."""
    old = "`self-assessment` *(observed: Caveat 1 in this document's appendix)*"
    new = "`self-assessment` *(observed: Caveat 1 in this\n   document's appendix)*"
    return swap(text, old, new)


POSITIVE_MUTATIONS = [
    ("evidence-all-invented-passes", "d_ok.md", all_invented),
    ("evidence-mark-may-wrap", "d_ok.md", wrap_a_mark),
    # Document and issue titles contain dashes. An earlier fix bounded the
    # annotation at the description dash and broke every source that had one.
    # An arrow inside a source is not the item citation that ends a
    # declaration; stopping at either truncated the annotation.
    # The arrow must land on the CONTINUATION line to exercise the stop
    # condition: an arrow on the declaration's own line was never at risk, and
    # a fixture that puts it there passes against the unfixed checker.
    ("evidence-source-may-contain-an-arrow", "d_ok.md",
     lambda t: swap(t, "*(observed: Caveat 1 in this document's appendix)*",
                    "*(observed: the Login\n   → Checkout trace)*")),
    # Ordinary lookup references. is_substantive rejects both -- "#12" has no
    # letters, and an autolink opens with the bracket that marks a template
    # slot -- yet each names an artifact a reader can go and check.
    ("evidence-source-may-be-an-issue-id", "d_ok.md",
     lambda t: swap(t, "*(observed: Caveat 1 in this document's appendix)*",
                    "*(observed: #12)*")),
    ("evidence-source-may-be-an-autolink", "d_ok.md",
     lambda t: swap(t, "*(observed: Caveat 1 in this document's appendix)*",
                    "*(observed: <https://example.test/issues/12>)*")),
    ("evidence-source-may-contain-a-dash", "d_ok.md",
     lambda t: swap(t, "*(observed: Caveat 1 in this document's appendix)*",
                    "*(observed: RFC 9110 - HTTP Semantics)*")),
    # A heading closes the persona section at every depth. This is a positive
    # case rather than a negative one because the fix is an *absence*: after it,
    # the row below the #### belongs to no persona and is never parsed, so the
    # document is simply correct. Asserting the miscount instead would have
    # pinned the bug in place -- the case would go red the moment it was fixed.
    ("level4-heading-closes-the-persona-section", "d_ok.md", level4_subsection),
]

# ---------------------------------------------------------------------------
# Enrichment. The base is generated from a core document rather than stored,
# because a stored one would need sixty hand-written entries and would rot the
# moment the core base changed -- the same rot the mutation design exists to
# avoid, at sixty times the size.
# ---------------------------------------------------------------------------
ENRICHED_HEADINGS = {"✅": "How it's answered today",
                     "◐": "How it's answered today",
                     "○": "What would have to exist",
                     "": "What answering this would take"}


def core_items(core_text):
    """(number, coverage mark, persona id) for every item row, in document order.

    Reads the same rows verify.py reads, by the same shape: a leading number and
    a coverage mark in a trailing cell. Deliberately not an import of the
    checker -- a fixture that parses with the code under test cannot disagree
    with it, and disagreeing is the entire job.
    """
    out = []
    persona = None
    for line in core_text.split("\n"):
        if re.match(r"#{1,6}\s", line):
            persona = re.match(r"###\s+(P\d+)\b", line)
            persona = persona.group(1) if persona else None
            continue
        if not persona or not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and cells[0].isdigit():
            mark = next((c for c in cells[3:] if c in ENRICHED_HEADINGS and c), "")
            out.append((int(cells[0]), mark, persona))
    require(out, "no item rows found in the core base")
    return out


def enriched_from(core_text):
    """A conforming enrichment of a core document. Every mutation starts here."""
    rows = core_items(core_text)
    graded = any(m for _, m, _ in rows)
    head = ["# What someone would want — the story behind each ask", "",
            "_Enrichment of `PERSONAS.md` (2026-08-30)._", "",
            "**The scenes are invented.** Each situation is a plausible reconstruction of how "
            "the ask arises, not an observed incident.", "",
            "**Frequencies:** estimated from the personas, not measured.", ""]
    head += ["**Coverage key:** ✅ served well today · ◐ partially served · ○ not possible today.",
             ""] if graded else [
            "**Coverage:** not assessed — no coverage pass ran, so no item carries a mark.", ""]
    head += ["**⚡ marks the frontier** — reads that feel like writes.", "",
             "**Topics:** `identity` · `provenance` · `agent-surface`.", "",
             "**Carried from the core document's Verification section:** the adversarial read "
             "found three coverage marks contradicting the document's own text.", "", "---", ""]

    body = []
    seen = set()
    for n, mark, persona in rows:
        if persona not in seen:
            seen.add(persona)
            body += [f"## {persona} — Role", ""]
        body += [f'#### {n} — "An ask."', "",
                 "**The situation.** A moment that produces the ask.", "",
                 "**Why it matters.** What goes wrong without an answer.", "",
                 f"**{ENRICHED_HEADINGS[mark]}.** What the capability comes to.", "",
                 f"`daily` · {mark + ' · ' if mark else ''}topics: `identity`", ""]
    return "\n".join(head + body)


def _first(text, mark):
    """The first entry whose footer carries `mark`. Raises if the base has none."""
    for m in re.finditer(r'^####\s+(\d+)\s+—', text, re.M):
        end = text.find("\n#### ", m.end())
        block = text[m.start():end if end > 0 else len(text)]
        if re.search(rf"^`daily`.*{re.escape(mark)}", block, re.M):
            return block
    raise BrokenFixture(f"no entry marked {mark!r} in the generated base")


def wrong_heading(text):
    """Give a served item the heading its mark does not select."""
    block = _first(text, "✅")
    return swap(text, block, block.replace("**How it's answered today.**",
                                           "**What would have to exist.**"))


def drop_an_entry(text):
    block = _first(text, "○")
    return swap(text, block, "")


def two_headings(text):
    block = _first(text, "○")
    return swap(text, block, block.replace(
        "**What would have to exist.**",
        "**How it's answered today.** Something.\n\n**What would have to exist.**"))


def footer_mark_disagrees(text):
    block = _first(text, "✅")
    return swap(text, block, re.sub(r"^(`daily` · )✅", r"\1○", block, flags=re.M))


def footer_drops_the_mark(text):
    """A graded entry whose footer carries no mark at all.

    An absent mark agrees with anything, so "the footer marks agree" was not a
    check until the mark was required to be present.
    """
    block = _first(text, "✅")
    return swap(text, block, re.sub(r"^(`daily` · )✅ · ", r"\1", block, flags=re.M))


def heading_repeated(text):
    """The same valid heading twice. A set comparison passes this; a count does not."""
    block = _first(text, "○")
    return swap(text, block, block.replace(
        "**What would have to exist.**",
        "**What would have to exist.** One thing.\n\n**What would have to exist.**"))


def heading_not_third(text):
    """The derived heading pushed to fourth by a block placed third.

    Checking only that the heading exists somewhere leaves the position
    unchecked, and the rule this checker advertises is positional.
    """
    block = _first(text, "○")
    return swap(text, block, block.replace(
        "**What would have to exist.**",
        "**An aside.** Something else entirely.\n\n**What would have to exist.**"))


# (name, mutation, expected-substring). All run against d_ok.md as the core.
ENRICHED_MUTATIONS = [
    ("enriched-heading-contradicts-mark", wrong_heading,
     "third-block heading does not match the coverage mark"),
    ("enriched-item-missing", drop_an_entry, "have no enriched entry"),
    ("enriched-two-headings", two_headings, "more than one third-block heading"),
    ("enriched-footer-mark-disagrees", footer_mark_disagrees,
     "coverage mark disagrees with the core document"),
    ("enriched-no-frequencies", lambda t: drop(t, "**Frequencies:**"),
     "no **Frequencies:** line in the enriched header"),
    ("enriched-no-topics", lambda t: drop(t, "**Topics:**"),
     "no **Topics:** line in the enriched header"),
    ("enriched-frequencies-placeholder",
     lambda t: edit_line(t, "**Frequencies:**", "**Frequencies:** TBD"),
     "**Frequencies:** is present but declares nothing"),
    ("enriched-no-verification-carry",
     lambda t: drop(t, "**Carried from the core document's Verification section:**"),
     "Verification section is not carried"),
    ("enriched-no-invented-disclosure",
     lambda t: drop(t, "**The scenes are invented.**"),
     "does not say the scenes are invented"),
    ("enriched-no-coverage-key", lambda t: drop(t, "**Coverage key:**"),
     "no **Coverage key:** line"),
    ("enriched-entry-for-unknown-item",
     lambda t: t + '\n#### 999 — "An ask."\n\n**What would have to exist.** Nothing.\n\n'
                   "`daily` · ○ · topics: `identity`\n",
     "which the core document does not contain"),
    ("enriched-duplicate-entry",
     lambda t: t + "\n" + _first(t, "○"),
     "have more than one enriched entry"),
    ("enriched-no-entries", lambda t: re.sub(r"^####.*$", "", t, flags=re.M),
     "no enriched entries found"),
    ("enriched-footer-drops-the-mark", footer_drops_the_mark,
     "carry no coverage mark in their footer"),
    ("enriched-same-heading-twice", heading_repeated,
     "more than one third-block heading"),
    ("enriched-heading-not-third", heading_not_third,
     "third-block heading is not the third block"),
    ("enriched-verification-carry-placeholder",
     lambda t: edit_line(t, "**Carried from the core document's Verification section:**",
                         "**Carried from the core document's Verification section:** TBD"),
     "records no findings"),
    ("enriched-coverage-key-omits-a-mark",
     lambda t: edit_line(t, "**Coverage key:**",
                         "**Coverage key:** ✅ served well today · ◐ partially served."),
     "does not explain"),
]

# A no-coverage core takes the third heading form, and must not be given ○.
ENRICHED_NOCOV_MUTATIONS = [
    ("enriched-nocov-asserts-absence",
     lambda t: t.replace("**What answering this would take.**",
                         "**What would have to exist.**", 1),
     "third-block heading does not match the coverage mark"),
    ("enriched-nocov-invents-a-mark",
     lambda t: re.sub(r"^(`daily` · )topics:", r"\1○ · topics:", t, count=1, flags=re.M),
     "carries ○ on a run with no coverage pass"),
    ("enriched-nocov-deletes-the-key", lambda t: drop(t, "**Coverage:** not assessed"),
     "not assessed' line in the enriched header"),
]

# ---------------------------------------------------------------------------
# Statics: defects a mutation cannot express, because they are damage to the
# body of the document rather than to one declaration.
# ---------------------------------------------------------------------------
STATICS = [
    ("corrupt.md", "numbering not continuous"),
    ("order.md", "out of document order"),
    ("shortrow.md", "do not match their table header"),
    ("noroster.md", "no persona roster table parsed"),
    ("shapemismatch.md", "states no coverage figures"),
    ("ungraded.md", "no coverage mark parsed"),
    ("duppid.md", "sharing a persona id"),
    ("today_tbd.md", "have no value"),
    ("today_tplph.md", "have no value"),
    ("reckon_noprereg.md", "to reckon against"),
    ("c_wrongkind.md", "this run graded coverage"),
    ("c_half.md", "missing actual split"),
    ("c_pct.md", "counts, not percentages"),
    ("c_vague.md", "states no prediction"),
    ("d_badsum.md", "sums to 3"),
    ("d_nosurprise.md", "surprise threshold"),
    ("d_wrongsection.md", "no **Reckoning:** line in the synthesis"),
    ("e_baddenom.md", "written against 100 items"),
    ("rk_prose.md", "missing predicted split and actual split"),
    ("rk_nolb.md", "no **Load-bearing persona:** line"),
    ("rk_noprereg.md", "no **Pre-registered:** line"),
    ("prereg_tbd.md", "is present but declares nothing"),
    ("prereg_noreckon.md", "no **Reckoning:** line in the synthesis"),
    ("dupdecl.md", "**Roster axis:** lines"),
    ("dupreckon.md", "**Reckoning:** lines"),
    ("twotally.md", "canonical tally lines"),
    ("notally.md", "no canonical tally line"),
    ("nofreq.md", "no **Frequencies:** line"),
    ("bare.md", "declares nothing"),
    ("placeholder.md", "declares nothing"),
    ("ph_TBD.md", "declares nothing"),
    ("ph_NA.md", "declares nothing"),
    ("ph_....md", "declares nothing"),
    ("mixed.md", "have no value"),
    ("late.md", "no **Roster axis:** line"),
    ("f_nopredicted.md", "states no prediction"),
    ("f_bigfrontier.md", "frontier items are a subset"),
    ("f_badlb.md", "does not contain"),
    ("f_vaguelb.md", "names nobody on the roster"),
]

# ---------------------------------------------------------------------------
# Retired: kept on disk, deliberately not asserted, each with the reason. A
# fixture is retired only when its intent is covered elsewhere or it can no
# longer reach the check it was written for. Recording a rotted fixture's
# CURRENT message as its expectation would turn a false green into an asserted
# one, which is worse than losing the case.
# ---------------------------------------------------------------------------
RETIRED = {
    "prereg_ok.md": "20/40/40 against a 60-item budget; percentages, settled as invalid in round 3",
    "rk_ok.md": "same stale percentages; superseded by d_ok.md as the passing base",
    "rk_badactual.md": "rots to the percentage failure before reaching its own check; "
                       "covered by reckoning-actual-contradicts-table",
    "rk_badpred.md": "same rot; covered by reckoning-restates-prediction",
    "unquoted.md": "tests a WARNING, not a failure, and now fails on a later header "
                   "requirement instead; needs rebuilding as a warning case",
    "wrapped.md": "fails on a later header requirement, not on citation wrapping",
    "pipe.md": "fails on a later header requirement, not on pipe escaping",
    "curly.md": "fails on a later header requirement, not on curly quotes",
    "stray.md": "fails on a later header requirement",
    "verif.md": "superseded by the --final cases, which test these checks as mutations",
    "noverif.md": "superseded by final-rejects-a-missing-section",
    "bareverif.md": "superseded by final-rejects-a-bare-section",
    "appendix.md": "fails on a later header requirement",
    "dupname.md": "fails on a later header requirement, not on duplicate primitive names",
    "nosynth.md": "fails on a later header requirement, not on the missing synthesis",
    "cjk1.md": "fails on a later header requirement, not on non-ASCII substance",
    "nonenglish.md": "same",
    "today.md": "fails on a later header requirement, not on the Today column",
}


# --final adds the Phase 7b Verification requirements. Nothing exercised it,
# so the whole second pass could rot without the suite noticing -- and three
# fixtures written for exactly these checks are in RETIRED, rotted on a header
# requirement. Expressed as mutations, they run again.
FINAL_CASES = [
    ("final-accepts-a-real-verification", "d_ok.md", None, None),
    ("final-rejects-a-missing-section", "d_ok.md",
     lambda t: t[:t.index("## Verification (Phase 7)")]
     + t[t.index("## What the 60 imply"):],
     "no Verification section"),
    ("final-rejects-a-bare-section", "d_ok.md",
     lambda t: t[:t.index("## Verification (Phase 7)")]
     + "## Verification (Phase 7)\n\n"
     + t[t.index("## What the 60 imply"):],
     "non-empty line"),
]


def run(path, *flags):
    r = subprocess.run([sys.executable, VERIFY, path, *flags], capture_output=True,
                       text=True, encoding="utf-8", errors="replace", cwd=REPO)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def failures_in(out):
    """Only the [FAIL] lines.

    Searching the whole output would accept a case whose targeted diagnostic
    had been downgraded to [WARN] while some unrelated check still failed --
    green for the wrong reason, which is the failure mode this suite exists to
    catch. Several fixtures legitimately emit more than one failure.
    """
    return "\n".join(l for l in out.splitlines() if "[FAIL]" in l)


def main():
    import tempfile
    failures = []
    checked = set()

    def report(ok, name, detail=""):
        print(("  ok   " if ok else "  FAIL ") + name + (("  -- " + detail) if detail else ""))
        if not ok:
            failures.append(name)

    print("bases (must pass):")
    for name in BASES:
        checked.add(name)
        rc, out = run(os.path.join(FIXTURES, name))
        first = next((l for l in out.splitlines() if "[FAIL]" in l), "")
        report(rc == 0, name, "" if rc == 0 else first.strip()[:90])

    print("\ngenerated negatives (base + one mutation):")
    with tempfile.TemporaryDirectory() as tmp:
        for name, base, mutate, needle in MUTATIONS:
            try:
                text = mutate(load(base))
            except (BrokenFixture, ValueError) as exc:
                report(False, name, f"mutation no longer applies to {base}: {exc}")
                continue
            path = os.path.join(tmp, name + ".md")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            rc, out = run(path)
            fails = failures_in(out)
            if rc == 0:
                report(False, name, "document passed; the defect was not caught")
            elif needle.lower() not in fails.lower():
                first = fails.splitlines()[0] if fails else "(no [FAIL] line)"
                report(False, name, f"wrong reason: wanted {needle!r}, got {first.strip()[:70]!r}")
            else:
                report(True, name)

        print("\nenrichment (--enriched):")
        for core_name, cases in (("d_ok.md", ENRICHED_MUTATIONS),
                                 ("nocov.md", ENRICHED_NOCOV_MUTATIONS)):
            core_path = os.path.join(FIXTURES, core_name)
            try:
                base = enriched_from(load(core_name))
            except (BrokenFixture, ValueError) as exc:
                report(False, f"enriched base from {core_name}", str(exc))
                continue
            # The generated base must pass before any mutation of it means
            # anything: a base that already fails makes every negative below
            # green for the wrong reason, which is the rot this suite exists
            # to prevent, introduced by its own generator.
            ok_path = os.path.join(tmp, f"enriched_ok_{core_name}")
            with open(ok_path, "w", encoding="utf-8") as fh:
                fh.write(base)
            rc, out = run(core_path, "--enriched", ok_path)
            fails = failures_in(out)
            report(rc == 0, f"generated enrichment of {core_name} passes",
                   "" if rc == 0 else (fails.splitlines() or [""])[0].strip()[:90])

            for name, mutate, needle in cases:
                try:
                    text = mutate(base)
                except (BrokenFixture, ValueError) as exc:
                    report(False, name, f"mutation no longer applies: {exc}")
                    continue
                require(text != base, f"{name} changed nothing")
                path = os.path.join(tmp, name + ".md")
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(text)
                rc, out = run(core_path, "--enriched", path)
                fails = failures_in(out)
                if rc == 0:
                    report(False, name, "document passed; the defect was not caught")
                elif needle.lower() not in fails.lower():
                    first = fails.splitlines()[0] if fails else "(no [FAIL] line)"
                    report(False, name,
                           f"wrong reason: wanted {needle!r}, got {first.strip()[:70]!r}")
                else:
                    report(True, name)

        print("\nsecond pass (--final):")
        for name, base, mutate, needle in FINAL_CASES:
            try:
                text = mutate(load(base)) if mutate else load(base)
            except (BrokenFixture, ValueError) as exc:
                report(False, name, f"mutation no longer applies to {base}: {exc}")
                continue
            path = os.path.join(tmp, name + ".md")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            rc, out = run(path, "--final")
            fails = failures_in(out)
            if needle is None:
                report(rc == 0, name,
                       "" if rc == 0 else (fails.splitlines() or [""])[0].strip()[:80])
            elif rc == 0:
                report(False, name, "document passed; the defect was not caught")
            elif needle.lower() not in fails.lower():
                first = fails.splitlines()[0] if fails else "(no [FAIL] line)"
                report(False, name, f"wrong reason: wanted {needle!r}, got {first.strip()[:70]!r}")
            else:
                report(True, name)

        print("\ngenerated positives (a mutation that must NOT be penalised):")
        for name, base, mutate in POSITIVE_MUTATIONS:
            try:
                text = mutate(load(base))
            except (BrokenFixture, ValueError) as exc:
                report(False, name, f"mutation no longer applies to {base}: {exc}")
                continue
            path = os.path.join(tmp, name + ".md")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            rc, out = run(path)
            first = next((l for l in out.splitlines() if "[FAIL]" in l), "")
            report(rc == 0, name, "" if rc == 0 else first.strip()[:90])

    print("\nstatic negatives:")
    for name, needle in STATICS:
        checked.add(name)
        if not os.path.exists(os.path.join(FIXTURES, name)):
            report(False, name, "fixture file missing")
            continue
        rc, out = run(os.path.join(FIXTURES, name))
        fails = failures_in(out)
        if rc == 0:
            report(False, name, "document passed; the defect was not caught")
        elif needle.lower() not in fails.lower():
            first = fails.splitlines()[0] if fails else "(no [FAIL] line)"
            report(False, name, f"wrong reason: wanted {needle!r}, got {first.strip()[:70]!r}")
        else:
            report(True, name)

    # --final, because that is the invocation SKILL.md requires of a finished
    # document. Checking only the default mode here would let the shipped
    # artifact lose its Verification section without the suite noticing -- the
    # second pass exists precisely to catch that, so this is where to use it.
    print("\nthe shipped document (--final):")
    rc, out = run(os.path.join(REPO, "PERSONAS.md"), "--final")
    report(rc == 0, "PERSONAS.md", "" if rc == 0
           else (failures_in(out).splitlines() or [""])[0].strip()[:90])

    # A vocabulary that has drifted from the run it describes is worse than no
    # vocabulary: it invites reuse of a slug that no longer means what it says.
    #
    # Equality, in both directions. This was briefly a one-way subset, on the
    # reasoning that the vocabulary has to be able to grow -- but growth now
    # belongs to the per-set PRIMITIVES.md, and references/primitives.md is a
    # read-only seed describing exactly one run. Each direction catches a real
    # and different mistake:
    #
    #   used but not recorded   a slug the document uses that the seed lacks;
    #                           the next run cannot reuse a name it cannot see
    #   recorded but not used   an entry appended to the seed by hand, which
    #                           travels to every unrelated subject the skill is
    #                           run against -- the contamination this file's
    #                           own read-only rule exists to prevent
    print("\nprimitive vocabulary:")
    with open(os.path.join(REPO, "PERSONAS.md"), encoding="utf-8") as fh:
        doc = fh.read()
    with open(os.path.join(SKILL, "references", "primitives.md"), encoding="utf-8") as fh:
        vocab = fh.read()
    # Anchors are asserted, not assumed. Splitting on a missing marker yields
    # the whole document rather than an error, so a renamed heading would leave
    # this scanning the wrong text -- and most likely still reporting green,
    # which is the failure this suite exists to make impossible.
    start = re.search(r"^##\s+What the \d+ imply\b.*$", doc, re.M)
    report(start is not None, "the synthesis heading is where the check expects it",
           "" if start else "no '## What the <N> imply' heading in PERSONAS.md")
    end = re.search(r"^###\s+If you only ask\b.*$", doc, re.M)
    report(end is not None, "the synthesis section has a recognised end",
           "" if end else "no '### If you only ask' heading in PERSONAS.md")
    section = doc[start.end():end.start()] if start and end else ""
    # Only the slug in a numbered primitive entry, not every backticked token:
    # the prose in that section cites other things in backticks too.
    in_doc = set(re.findall(r"^\s*\d+\.\s+\*\*.+?\*\*\s+`([a-z0-9-]+)`", section, re.M))
    # Whitespace around the cell is formatting, not meaning; a reflowed table
    # must not read as a changed vocabulary.
    in_vocab = set(re.findall(r"\|\s*`([a-z0-9-]+)`\s*\|", vocab))
    # An empty slice would satisfy the subset test vacuously, so the check has
    # to know it found something before it can claim the comparison held.
    report(bool(in_doc), "the synthesis section yields primitive slugs",
           "no numbered primitive entries matched; the check compared nothing"
           if not in_doc else "")
    unrecorded = sorted(in_doc - in_vocab)
    report(not unrecorded, "every slug PERSONAS.md uses is in references/primitives.md",
           f"used but not recorded: {unrecorded}" if unrecorded else "")
    stray = sorted(in_vocab - in_doc)
    report(not stray, "the seed records nothing PERSONAS.md does not use",
           f"recorded but not used: {stray}. The seed is read-only and travels to "
           f"every subject; per-set slugs belong in that set's PRIMITIVES.md."
           if stray else "")

    # No fixture may sit on disk unaccounted for. Without this, a case can be
    # orphaned by a rename and nobody notices it stopped running.
    print("\ninventory:")
    on_disk = {f for f in os.listdir(FIXTURES) if f.endswith(".md")}
    accounted = checked | set(RETIRED)
    orphaned = sorted(on_disk - accounted)
    report(not orphaned, "every fixture is asserted or explicitly retired",
           f"unaccounted: {orphaned}" if orphaned else "")
    stale = sorted(set(RETIRED) - on_disk)
    report(not stale, "every retired fixture still exists on disk",
           f"missing: {stale}" if stale else "")

    print(f"\n{'FAILED' if failures else 'PASSED'}: "
          f"{len(failures)} problem(s); {len(RETIRED)} fixture(s) retired")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
