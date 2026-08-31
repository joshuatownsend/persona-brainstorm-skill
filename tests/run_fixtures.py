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
import collections
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
FREQ_VOCAB = {"many/day", "daily", "weekly", "monthly", "quarterly", "annually",
              "per-incident", "per-release", "per-run", "onboarding"}
Row = collections.namedtuple("Row", "n mark persona ask freq frontier")


def core_items(core_text):
    """One Row per item row in the core document, in document order.

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
            # The frequency is the first cell holding a value from the
            # vocabulary. Positional decoding would have to reimplement the
            # checker's Today-column sniffing, and reimplementing it here is how
            # a generator drifts from the thing it generates for.
            freq = next((c for c in cells[3:] if c.lstrip("~") in FREQ_VOCAB), "")
            out.append(Row(int(cells[0]), mark, persona,
                           cells[1].strip().strip('"“”'), freq,
                           any("⚡" in c for c in cells[3:])))
    require(out, "no item rows found in the core base")
    return out


def core_freq(core_text):
    """The core document's **Frequencies:** line, verbatim.

    Copied rather than composed: the enriched header restates the core's basis,
    and a generator inventing its own wording would make the base fail the very
    check that requires them to agree.
    """
    return line_starting(core_text, FREQ)


def enriched_from(core_text):
    """A conforming enrichment of a core document. Every mutation starts here."""
    rows = core_items(core_text)
    graded = any(r.mark for r in rows)
    head = ["# What someone would want — the story behind each ask", "",
            "_Enrichment of `PERSONAS.md` (2026-08-30)._", "",
            "**The scenes are invented.** Each situation is a plausible reconstruction of how "
            "the ask arises, not an observed incident.", "",
            core_freq(core_text), ""]
    head += ["**Coverage key:** ✅ served well today · ◐ partially served · ○ not possible today.",
             ""] if graded else [
            "**Coverage:** not assessed — no coverage pass ran, so no item carries a mark.", ""]
    head += ["**⚡ marks the frontier** — reads that feel like writes.", "",
             "**Topics:** `identity` · `provenance` · `agent-surface`.", "",
             "**Carried from the core document's Verification section:** "
             + carried_verification(core_text), "", "---", ""]

    body = []
    seen = set()
    for r in rows:
        if r.persona not in seen:
            seen.add(r.persona)
            body += [f"## {r.persona} — Role", ""]
        # Ask, frequency and frontier mark are copied from the core row rather
        # than composed: the checker compares all three, so a generator that
        # invented them could not produce a base that passes.
        bolt = "⚡ · " if r.frontier else ""
        body += [f'#### {r.n} — "{r.ask}"', "",
                 "**The situation.** A moment that produces the ask.", "",
                 "**Why it matters.** What goes wrong without an answer.", "",
                 f"**{ENRICHED_HEADINGS[r.mark]}.** What the capability comes to.", "",
                 f"`{r.freq}` · {bolt}{r.mark + ' · ' if r.mark else ''}topics: `identity`", ""]
    return "\n".join(head + body)


def foot_sub(block, old, new):
    """Rewrite part of an entry's footer, whatever frequency it opens with."""
    m = re.search(r"^`[^`]+` ·.*$", block, re.M)
    require(m, "no footer line in the entry")
    require(old in m.group(0), f"{old!r} not in the footer to replace")
    return block.replace(m.group(0), m.group(0).replace(old, new, 1), 1)


def _first(text, mark):
    """The first entry whose footer carries `mark`. Raises if the base has none."""
    for m in re.finditer(r'^####\s+(\d+)\s+—', text, re.M):
        end = text.find("\n#### ", m.end())
        block = text[m.start():end if end > 0 else len(text)]
        # Any backticked frequency, not a literal one: the generated footer
        # copies the core row's frequency, so pinning this to "daily" made every
        # mutation vanish the moment the generator started copying properly.
        if re.search(rf"^`[^`]+`.*{re.escape(mark)}", block, re.M):
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
    return swap(text, block, foot_sub(block, "✅", "○"))


def footer_drops_the_mark(text):
    """A graded entry whose footer carries no mark at all.

    An absent mark agrees with anything, so "the footer marks agree" was not a
    check until the mark was required to be present.
    """
    block = _first(text, "✅")
    return swap(text, block, foot_sub(block, "✅ · ", ""))


def footer_carries_two_marks(text):
    """A stale mark left beside its replacement.

    Whichever is compared first, one of them matches the core and the entry
    passes -- and with the marks held in a set, which one that is varies with
    the interpreter's hash seed.
    """
    block = _first(text, "✅")
    return swap(text, block, foot_sub(block, "✅", "✅ · ○"))


def rewrite_a_frequency(text):
    """Swap one entry's frequency for a different valid one.

    Not a fixed pair: the generated footer copies whatever the core row says, so
    naming both sides pinned the case to one base's data.
    """
    block = _first(text, "○")
    m = re.search(r"^`([^`]+)` ·", block, re.M)
    require(m, "no footer frequency to rewrite")
    other = next(f for f in sorted(FREQ_VOCAB) if f != m.group(1))
    return swap(text, block, foot_sub(block, f"`{m.group(1)}`", f"`{other}`"))


def no_bolt(text):
    """The first entry whose footer carries no frontier mark."""
    for m in re.finditer(r"^####\s+(\d+)\s+—", text, re.M):
        end = text.find("\n#### ", m.end())
        block = text[m.start():end if end > 0 else len(text)]
        foot = re.search(r"^`[^`]+` ·.*$", block, re.M)
        if foot and "⚡" not in foot.group(0):
            return block
    raise BrokenFixture("every entry in the generated base carries ⚡")


def drop_a_footer(text):
    """An entry with no footer at all.

    On a run with no coverage pass there is no mark to compare, so nothing else
    proves the fourth part exists -- and the frequency and topics would go with
    it. Applied to the graded base too, where the missing-mark check is what
    catches it; both paths lead to a fail, which is the point.
    """
    block = _first(text, "○")
    return swap(text, block, re.sub(r"^`[^`]+` ·.*$", "", block, count=1, flags=re.M))


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
     "no affirmative statement that the scenes are invented"),
    # The word appearing somewhere is not the declaration. This sentence
    # contains "invented" and says the opposite of what is required.
    ("enriched-disclosure-inverted",
     lambda t: edit_line(t, "**The scenes are invented.**",
                         "**The scenes are not invented.** Every one was observed."),
     "no affirmative statement that the scenes are invented"),
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
    # Copied from the core document, not restated. A core declaring its
    # frequencies estimated and an enrichment declaring them measured changes
    # how a reader takes every pill on every card.
    ("enriched-frequencies-contradict-core",
     lambda t: edit_line(t, FREQ, FREQ + " observed from six months of support tickets."),
     "does not match the core document's"),
    ("enriched-footer-carries-two-marks", footer_carries_two_marks,
     "in one footer"),
    ("enriched-both-coverage-lines",
     lambda t: swap(t, "**Coverage key:**",
                    "**Coverage:** not assessed — nobody looked.\n\n**Coverage key:**"),
     "both a **Coverage key:** and"),
    ("enriched-frequencies-declared-twice",
     lambda t: swap(t, line_starting(t, FREQ),
                    line_starting(t, FREQ) + "\n\n**Frequencies:** observed from tickets."),
     "**Frequencies:** lines in the enriched header"),
    ("enriched-no-frontier-legend",
     lambda t: drop(t, "**⚡ marks the frontier**"),
     "does not explain ⚡"),
    # Unanchored, a sentence merely mentioning the section satisfied the
    # requirement to carry it.
    ("enriched-verification-mentioned-not-carried",
     lambda t: edit_line(t, "**Carried from the core document's Verification section:**",
                         "The core document's Verification section is worth a read; "
                         "carried from the core document's Verification section it is not."),
     "Verification section is not carried"),
    ("enriched-entry-without-a-footer", drop_a_footer, "have no footer line"),
    # The whole document inside one fence renders as a code sample and contains
    # no headings at all. Scanned raw, it read as a conforming enrichment.
    ("enriched-everything-fenced",
     lambda t: "```markdown\n" + t + "\n```\n", "no enriched entries found"),
    ("enriched-heading-without-an-ask",
     lambda t: re.sub(r'^(####\s+\d+\s+—).*$', r"\1 an entry", t, flags=re.M),
     "carry no quoted ask"),
    ("enriched-heading-quotes-another-ask",
     lambda t: re.sub(r'^(####\s+\d+\s+—).*$',
                      r'\1 "Something else entirely, about nothing in this document."',
                      t, count=1, flags=re.M),
     "quote an ask unlike the core document's"),
    ("enriched-footer-is-prose",
     lambda t: swap(t, _first(t, "○").splitlines()[-1],
                    "A prose sentence mentioning topics: identity."),
     "have no footer line"),
    ("enriched-frequency-disagrees", rewrite_a_frequency,
     "frequency disagrees with the core document"),
    ("enriched-frontier-mark-added",
     lambda t: swap(t, no_bolt(t), foot_sub(no_bolt(t), "` · ", "` · ⚡ · ")),
     "frontier mark disagrees with the core document"),
    # A tilde fence is what a document quoting a backtick fence has to use.
    ("enriched-everything-tilde-fenced",
     lambda t: "~~~markdown\n" + t + "\n~~~\n", "no enriched entries found"),
    ("enriched-two-footers",
     lambda t: swap(t, _first(t, "○"),
                    _first(t, "○").rstrip() + "\n\n`onboarding` · ✅ · topics: `other`\n"),
     "more than one footer"),
    # Negation ahead of the noun, which the phrase-window match let through.
    ("enriched-disclosure-negated-early",
     lambda t: edit_line(t, "**The scenes are invented.**",
                         "**No scenes are invented.** Every one was witnessed."),
     "no affirmative statement that the scenes are invented"),
    ("enriched-two-coverage-keys",
     lambda t: swap(t, line_starting(t, "**Coverage key:**"),
                    line_starting(t, "**Coverage key:**")
                    + "\n\n**Coverage key:** ✅ never · ◐ sometimes · ○ always."),
     "**Coverage key:** lines in the enriched header"),
    # An apostrophe is not a quote delimiter: treating one as an opener let an
    # unquoted ask containing a contraction read as quoted.
    # The same substitution the adversarial pass is checked for: findings
    # replaced by something reassuring rather than summarised.
    ("enriched-verification-replaced",
     lambda t: edit_line(t, "**Carried from the core document's Verification section:**",
                         "**Carried from the core document's Verification section:** "
                         "everything passed."),
     "no vocabulary in common"),
    ("enriched-heading-ask-only-apostrophes",
     lambda t: re.sub(r"^(####\s+\d+\s+—).*$", r"\1 they don't know it's answerable",
                      t, count=1, flags=re.M),
     "carry no quoted ask"),
]

# A no-coverage core takes the third heading form, and must not be given ○.
ENRICHED_NOCOV_MUTATIONS = [
    ("enriched-nocov-asserts-absence",
     lambda t: t.replace("**What answering this would take.**",
                         "**What would have to exist.**", 1),
     "third-block heading does not match the coverage mark"),
    ("enriched-nocov-invents-a-mark",
     lambda t: re.sub(r"^(`[^`]+` · )topics:", r"\1○ · topics:", t, count=1, flags=re.M),
     "carries ○ on a run with no coverage pass"),
    ("enriched-nocov-deletes-the-key", lambda t: drop(t, "**Coverage:** not assessed"),
     "not assessed' line in the enriched header"),
]

# ---------------------------------------------------------------------------
# Adversarial. Generated from a core document for the same reason the enriched
# base is: the entries cite that document's personas and its Appendix A lanes,
# so a stored one goes stale the moment either changes.
# ---------------------------------------------------------------------------
ADV_KINDS = ("it's wrong", "it's expensive", "it refuses", "it surprises")


def carried_verification(core_text):
    """A summary of the core's Verification section, drawn from its own words.

    Composed from the section rather than invented, because that is what
    carrying findings forward means -- and because a generator writing its own
    reassuring sentence would produce a base that fails the check requiring the
    two to share vocabulary, which is the check working.
    """
    m = re.search(r"^#{2,3}\s*Verification\b(.*?)(?=^#{2}\s|\Z)", core_text, re.M | re.S)
    require(m, "no Verification section in the core base")
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z'-]{3,}", m.group(1))][:60]
    require(words, "the core Verification section has no words to carry")
    return " ".join(words)


def core_lane_letters(core_text):
    """The Appendix A lane letters, in document order."""
    # Every dash the checker accepts. Matching only the em dash meant a core
    # document written with a hyphen would break the generator rather than the
    # thing it generates for, which is the wrong failure.
    out = [m.group(1) for m in
           re.finditer(r"\|\s*\*\*([A-Z])\s*[—\-–][^*|]+\*\*", core_text)]
    require(out, "no Appendix A lanes found in the core base")
    return out


def adversarial_from(core_text):
    """A conforming adversarial pass over a core document."""
    rows = core_items(core_text)
    personas = list(dict.fromkeys(r.persona for r in rows))
    lanes = core_lane_letters(core_text)
    head = ["# What someone would want — what they can't stand about it", "",
            "_Adversarial pass over `PERSONAS.md` (2026-08-30)._", "",
            "**Only the `observed` entries are reported complaints.** inferred and invented are "
            "both reconstructions.", "",
            "**Coverage depth:** Full, copied from the core document.", "",
            "**Carried from the core document's Verification section:** "
            + carried_verification(core_text), "", "---", ""]
    body = []
    for i, persona in enumerate(personas):
        body += [f"## {persona} — Role", ""]
        for k in (1, 2):
            lane = lanes[(i + k) % len(lanes)]
            mark = "observed: a support thread" if (i + k) % 3 == 0 else "invented"
            body += [f'#### {persona}-{k} — "I can never tell whether this answer is current."',
                     "",
                     f"**About:** Lane {lane} — the read it serves; Appendix A marks this "
                     f"lane verified. *({mark})*", "",
                     f"**Kind:** {ADV_KINDS[(i + k) % len(ADV_KINDS)]}.", "",
                     "**What they expected.** That the answer would say how old it was.", "",
                     "**What it costs.** They confirm it elsewhere, which takes longer.", "",
                     "**What would fix it.** A timestamp on the answer.", ""]
    return "\n".join(head + body)


def _adv_first(text):
    """The first grievance entry, as a block."""
    m = re.search(r"^####\s+P\d+-\d+\s+—", text, re.M)
    require(m, "no grievance entries in the generated base")
    end = text.find("\n#### ", m.end())
    return text[m.start():end if end > 0 else len(text)]


def _as_expectation_gap(text, about):
    """Turn the first entry into an expectation gap with the given About."""
    block = _adv_first(text)
    out = re.sub(r"^\*\*About:\*\*.*$", about, block, count=1, flags=re.M)
    out = re.sub(r"^\*\*Kind:\*\*.*$", "**Kind:** the expectation gap.", out,
                 count=1, flags=re.M)
    require(out != block, "the entry was already an expectation gap")
    return swap(text, block, out)


def expectation_gap_with_promise(text):
    return _as_expectation_gap(
        text, '**About:** the promise in `README.md` that it "answers anything". *(invented)*')


def expectation_gap_without_promise(text):
    return _as_expectation_gap(text, "**About:** the thing generally. *(invented)*")


def expectation_gap_cited_only_inside_an_underscore_mark(text):
    """An expectation gap whose only citation lives inside its evidence mark.

    The About block cites nothing of its own. The quoted promise and the file
    naming where it is made both sit inside the mark, which is the checker's own
    annotation rather than the author's citation -- so the entry is exactly the
    one the "cite no promise" rule exists to refuse.

    The mark is stripped before that search, and the strip was a third
    hard-coded copy of the mark pattern that accepted asterisks only. So the
    moment underscores became a legal spelling, this document passed or failed
    on its delimiter alone: identical content, opposite verdicts.
    """
    return _as_expectation_gap(
        text,
        '**About:** the thing generally. _(observed: "answers anything" in `README.md`)_')


def expectation_gap_cited_only_inside_a_mark_with_parentheses(text):
    """The same bypass, reached through a source that contains a parenthesis.

    The parser has accepted a ')' inside a source since the day a mark quoting
    this checker's own output vanished for containing "primitive(s)". The strip
    did not: it used [^)]*, stopped at the first ')', matched nothing, and left
    the whole mark standing for the citation search to read.

    So the parser and the redactor disagreed about what a mark *is*, and the
    gap between them was a bypass. Whatever MARK_RE can read, MARK_STRIP_RE has
    to be able to remove -- that is the invariant this fixture pins.
    """
    return _as_expectation_gap(
        text,
        '**About:** the thing generally. '
        '_(observed: "answers anything" in `README.md` (line 2))_')


def expectation_gap_cited_only_inside_a_mixed_fence_mark(text):
    """The same bypass again, reached by terminating a mark on the wrong fence.

    While the opening and closing delimiters were independent, a source
    containing ")_" ended a star-delimited mark early. The parser read only
    through "result(foo", the strip removed only that much, and everything after
    it -- the quote and the filename -- was left in the prose for the citation
    rule to read as the author's own.

    This was written off once as a cosmetic laxity affecting only odd spellings
    like *(invented)_ . It was not: it stranded part of a well-formed mark.
    """
    return _as_expectation_gap(
        text,
        '**About:** the thing generally. '
        '*(observed: result(foo)_bar "answers anything" in README.md)*')


def expectation_gap_citing_inside_an_emphasised_aside(text):
    """A real citation the author wrote inside an ordinary emphasised aside.

    Not a mark -- no kind word after the paren -- so the redaction must leave it
    alone. Widening the strip to every emphasised parenthetical deleted this
    entry's promise along with its mark and failed it for citing nothing, which
    is a false failure and worse than the bypass that widening was meant to fix.
    """
    return _as_expectation_gap(
        text,
        '**About:** the docs promise _("answers anything" in `README.md`)_. '
        '*(invented)*')


def expectation_gap_citing_inside_a_word_led_aside(text):
    """The same aside, beginning with a word rather than a quote.

    Requiring a kind word after the paren was meant to separate a mark from an
    ordinary aside, and could not: asides start with words too. "see" is a word
    and not an evidence kind, so the redaction ate a citation the author wrote
    and failed the entry for citing nothing. Only the closed vocabulary tells
    the two apart.
    """
    return _as_expectation_gap(
        text,
        '**About:** the docs promise _(see "answers anything" in `README.md`)_. '
        '*(invented)*')


def intraword_underscores_are_not_a_mark(t):
    """Markdown does not render `_emphasis_` inside a word, and nor may we.

    foo_(invented)_bar is literal text to every reader of the document and was
    a valid evidence mark to this checker, so a grievance carrying no visible
    annotation anywhere passed. Introduced by accepting underscores at all --
    before that it was correctly reported as unmarked.

    It is asserted as *malformed* rather than *absent*, which is the more useful
    of the two: the author did write a mark and it is not working. Telling them
    no mark is present would send them to add a second one, and the two-marks
    rule would then refuse the result -- the precise fix-steering failure the
    malformed/absent distinction exists to prevent.
    """
    first = _adv_first(t)
    return swap(t, first,
                first.replace("*(invented)*", "foo_(invented)_bar", 1))


ADVERSARIAL_MUTATIONS = [
    ("adversarial-no-entries", lambda t: re.sub(r"^####.*$", "", t, flags=re.M),
     "no grievance entries found"),
    ("adversarial-everything-fenced",
     lambda t: "~~~markdown\n" + t + "\n~~~\n", "no grievance entries found"),
    ("adversarial-persona-not-on-roster",
     lambda t: t.replace("#### P1-1", "#### P99-1", 1), "not on the approved roster"),
    ("adversarial-duplicate-id",
     lambda t: t + "\n" + _adv_first(t), "duplicate grievance id"),
    ("adversarial-complaint-not-quoted",
     lambda t: re.sub(r'^(####\s+P\d+-\d+\s+—).*$', r"\1 the answer is stale",
                      t, count=1, flags=re.M),
     "carry no quoted complaint"),
    ("adversarial-no-lane",
     lambda t: swap(t, _adv_first(t),
                    re.sub(r"^\*\*About:\*\*.*$", "**About:** the thing generally. *(invented)*",
                           _adv_first(t), count=1, flags=re.M)),
     "name no inventory lane"),
    ("adversarial-no-evidence-mark",
     lambda t: swap(t, _adv_first(t),
                    re.sub(r"\s*\*\([^)]*\)\*", "", _adv_first(t), count=1)),
     "carry no evidence mark"),
    # A mark that was written and did not parse is a third state. Reporting it
    # as "no mark" sends the author to add one, which the two-marks rule then
    # refuses -- a diagnostic that names the wrong cause steers the fix.
    ("adversarial-unparseable-mark-is-not-a-missing-one",
     lambda t: swap(t, _adv_first(t),
                    _adv_first(t).replace("*(invented)*", "*(invented)", 1)),
     "could not be read"),
    ("adversarial-two-evidence-marks",
     lambda t: swap(t, _adv_first(t),
                    _adv_first(t).replace("*(observed: a support thread)*",
                                          "*(observed: a support thread)* *(invented)*", 1)
                    if "*(observed" in _adv_first(t)
                    else _adv_first(t).replace("*(invented)*",
                                               "*(invented)* *(observed: a note)*", 1)),
     "carry more than one evidence mark"),
    ("adversarial-mark-off-vocabulary",
     lambda t: swap(t, _adv_first(t),
                    re.sub(r"\*\(\s*[A-Za-z-]+", "*(probable", _adv_first(t), count=1)),
     "is marked 'probable'"),
    ("adversarial-observed-without-source",
     lambda t: t.replace("*(observed: a support thread)*", "*(observed)*", 1),
     "names no source"),
    ("adversarial-invented-with-source",
     lambda t: t.replace("*(invented)*", "*(invented: a support thread)*", 1),
     "invented and names a source"),
    ("adversarial-kind-off-vocabulary",
     lambda t: swap(t, _adv_first(t),
                    re.sub(r"^\*\*Kind:\*\*.*$", "**Kind:** annoying.",
                           _adv_first(t), count=1, flags=re.M)),
     "says 'annoying.'"),
    ("adversarial-block-missing",
     lambda t: swap(t, _adv_first(t),
                    re.sub(r"^\*\*What it costs\.\*\*.*$", "",
                           _adv_first(t), count=1, flags=re.M)),
     "is missing What it costs"),
    ("adversarial-no-coverage-depth",
     lambda t: drop(t, "**Coverage depth:**"), "no **Coverage depth:** line"),
    ("adversarial-coverage-depth-neither",
     lambda t: edit_line(t, "**Coverage depth:**", "**Coverage depth:** thorough."),
     "does not open with Full or Light"),
    ("adversarial-two-coverage-depths",
     lambda t: twice(t, "**Coverage depth:**"), "**Coverage depth:** lines"),
    ("adversarial-no-verification-carry",
     lambda t: drop(t, "**Carried from the core document's Verification section:**"),
     "Verification section is not carried"),
    ("adversarial-no-observed-disclosure",
     lambda t: drop(t, "**Only the `observed` entries are reported complaints.**"),
     "does not say which entries are reported complaints"),
    ("adversarial-all-invented-undisclosed",
     lambda t: t.replace("*(observed: a support thread)*", "*(invented)*"),
     "no grievance is marked observed, and the header does not say so"),
    # The word appearing is not the declaration, here as in the enriched header.
    ("adversarial-disclosure-negated",
     lambda t: edit_line(t, "**Only the `observed` entries are reported complaints.**",
                         "**The `observed` entries are not reported complaints.**"),
     "does not say which entries are reported complaints"),
    # "None, not Full or Light" declares the one depth this pass refuses, and
    # passed on the word it used to refuse it.
    ("adversarial-depth-discusses-rather-than-states",
     lambda t: edit_line(t, "**Coverage depth:**",
                         "**Coverage depth:** None, not Full or Light."),
     "does not open with Full or Light"),
    ("adversarial-verification-replaced",
     lambda t: edit_line(t, "**Carried from the core document's Verification section:**",
                         "**Carried from the core document's Verification section:** "
                         "everything passed."),
     "no vocabulary in common"),
    ("adversarial-expectation-gap-cites-nothing", expectation_gap_without_promise,
     "cite no promise"),
    ("adversarial-expectation-gap-cited-only-inside-an-underscore-mark",
     expectation_gap_cited_only_inside_an_underscore_mark, "cite no promise"),
    ("adversarial-expectation-gap-cited-only-inside-a-mark-with-parentheses",
     expectation_gap_cited_only_inside_a_mark_with_parentheses, "cite no promise"),
    ("adversarial-expectation-gap-cited-only-inside-a-mixed-fence-mark",
     expectation_gap_cited_only_inside_a_mixed_fence_mark, "cite no promise"),
    ("adversarial-intraword-underscores-are-not-a-mark",
     intraword_underscores_are_not_a_mark, "could not be read"),
    # setdefault kept the first and ignored the rest, so a stale block sat
    # beside its replacement and the entry read as consistent.
    ("adversarial-lane-without-status",
     lambda t: swap(t, _adv_first(t),
                    re.sub(r"; Appendix A marks this lane verified", "",
                           _adv_first(t), count=1)),
     "name no verification status"),
    ("adversarial-block-empty",
     lambda t: swap(t, _adv_first(t),
                    re.sub(r"^(\*\*What it costs\.\*\*).*$", r"\1", _adv_first(t),
                           count=1, flags=re.M)),
     "What it costs is empty"),
    ("adversarial-block-repeated",
     lambda t: swap(t, _adv_first(t),
                    re.sub(r"^(\*\*Kind:\*\*.*)$", r"\1\n\n**Kind:** it refuses.",
                           _adv_first(t), count=1, flags=re.M)),
     "repeats Kind"),
    # Without the blank line the heading continuation swallowed the About block,
    # and the quoted text there stood in for the missing complaint.
    ("adversarial-heading-runs-into-the-about",
     lambda t: re.sub(r'^(####\s+P\d+-\d+\s+—).*\n\n', r"\1 the answer is stale\n",
                      t, count=1, flags=re.M),
     "carry no quoted complaint"),
    # Advice to the author, not a statement about this run.
    ("adversarial-no-observed-declared-as-advice",
     lambda t: edit_line(
         t.replace("*(observed: a support thread)*", "*(invented)*"),
         "**Only the `observed` entries are reported complaints.**",
         "**Only the `observed` entries are reported complaints.**\n\n"
         "**Do not label invented entries observed.**"),
     "no grievance is marked observed, and the header does not say so"),
]

# Must still pass: the expectation gap is the one kind exempt from the lane
# rule, and an exemption nothing asserts is an exemption nobody knows is there.
def about_soft_wrapped(t):
    """Wrap the first About block so its status word falls on line two.

    Identical words, valid markdown, identical rendering -- and it used to FAIL.
    The block value was read from the label's own physical line, so a wrap hid
    the lane or the status; and a continuation line beginning with emphasis was
    itself parsed as a new label, truncating the block. These lines carry a
    lane, a status and a mark, so they are long, and the reference's own worked
    example wraps its heading for the same reason.
    """
    first = _adv_first(t)
    m = re.search(r"^\*\*About:\*\* (.*)$", first, re.M)
    require(m is not None, "no About line in the first grievance")
    line = m.group(1)
    cut = line.rfind(" ", 0, len(line) // 2)
    require(cut > 0, "About line too short to wrap")
    return swap(t, first,
                first.replace(m.group(0),
                              "**About:** " + line[:cut] + "\n" + line[cut + 1:], 1))


def mark_source_with_a_parenthesis(t):
    """An observed source that quotes this checker's own output.

    Those messages contain "primitive(s)", and the source capture used to stop
    at the first ')' -- so the mark vanished and was reported as *absent*. The
    most auditable source an observed mark can name was the one the rule broke
    on.
    """
    first = _adv_first(t)
    quoted = '*(observed: verify.py said "1 primitive(s) carry no mark")*'
    return swap(t, first, first.replace("*(invented)*", quoted, 1))


def mark_written_with_underscores(t):
    """The same mark spelled with underscores instead of asterisks.

    Markdown spells emphasis two ways and formatters rewrite one into the other:
    prettier normalises *(invented)* to _(invented)_. That is the same document
    to every human reader and an absent mark to a checker that accepts only
    asterisks -- so a repository with prettier in a pre-commit hook broke every
    evidence mark in the act of committing them, *after* the author had run the
    checker and watched it pass.

    MARK_RE has one home and two call sites -- primitives and grievances -- so
    exercising it here covers the primitive path too.
    """
    first = _adv_first(t)
    return swap(t, first, first.replace("*(invented)*", "_(invented)_", 1))


def mark_source_may_contain_an_asterisk(t):
    """A source naming a wildcard, e.g. a column prefix written remixSource*.

    Distinct from the underscore case and worth its own row: a literal '*'
    inside the span is what makes a formatter mis-read where the emphasis ends,
    and the checker should still read the mark whichever delimiter survives.
    """
    first = _adv_first(t)
    quoted = "_(observed: the remixSource* columns in schema.ts)_"
    return swap(t, first, first.replace("*(invented)*", quoted, 1))


ADVERSARIAL_POSITIVES = [
    ("adversarial-expectation-gap-needs-no-lane", expectation_gap_with_promise),
    ("adversarial-about-block-may-soft-wrap", about_soft_wrapped),
    ("adversarial-mark-source-may-contain-a-parenthesis", mark_source_with_a_parenthesis),
    ("adversarial-mark-may-be-written-with-underscores", mark_written_with_underscores),
    ("adversarial-mark-source-may-contain-an-asterisk", mark_source_may_contain_an_asterisk),
    ("adversarial-expectation-gap-may-cite-inside-an-emphasised-aside",
     expectation_gap_citing_inside_an_emphasised_aside),
    ("adversarial-expectation-gap-may-cite-inside-a-word-led-aside",
     expectation_gap_citing_inside_a_word_led_aside),
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
     "0 substantive block(s). Phase 7b"),
    # A graded document with its inventory removed. --final used to pass this at
    # exit 0 with a full tally still on the page: sixty coverage claims and no
    # evidence in the file for any of them.
    ("final-rejects-graded-document-with-no-appendix", "d_ok.md",
     lambda t: t[:t.index("## Appendix A")],
     "no inventory lanes can be read"),
    # "Lanes moved" is a movement appendix, not an inventory. The heading
    # whitelist accepted "lanes" while output-template.md documented only
    # coverage and inventory -- a whitelist wider than its own documentation.
    ("final-rejects-a-lanes-headed-analysis-appendix", "d_ok.md",
     lambda t: t[:t.index("## Appendix A")]
     + "\n## Appendix B — Lanes moved\n\n| Lane | Note |\n|---|---|\n"
     + "| **A — Added in pass two** | analysis only |\n",
     "no inventory lanes can be read"),
    # One answer hard-wrapped over five lines is one answer. Counting physical
    # lines let it stand in for five, with four Phase 7b questions unanswered.
    ("final-rejects-one-answer-wrapped-over-five-lines", "d_ok.md",
     lambda t: t[:t.index("## Verification (Phase 7)")]
     + "## Verification (Phase 7)\n\nA fresh agent read the document and found\n"
     + "the roster holds up under the distinctness test, that several coverage\n"
     + "marks read as inferred rather than verified, that two items restate\n"
     + "their asks rather than naming a decision, and that a practitioner would\n"
     + "question the frequency column before anything else on the page.\n\n"
     + t[t.index("## What the 60 imply"):],
     "1 substantive block"),
    # ...and the fix for that must not reject the other legitimate shape. Five
    # answers as an ordinary Markdown list share one blank-line-separated block,
    # so counting blocks turned a false pass into a false failure -- the same
    # class as the About-block defect this PR opened with, reintroduced while
    # fixing something else. Neither the prose fixtures nor the shipped
    # documents caught it, because both happen to use paragraphs.
    ("final-accepts-five-answers-as-adjacent-bullets", "d_ok.md",
     lambda t: t[:t.index("## Verification (Phase 7)")]
     + "## Verification (Phase 7)\n\n"
     + "- Items 4 and 11 would apply unchanged to any other subject here.\n"
     + "- P2 and P5 are indistinguishable once the persona names are covered.\n"
     + "- The coverage marks on items 7 and 19 read as inferred, not verified.\n"
     + "- Items 22 and 30 restate their asks instead of naming a decision.\n"
     + "- A practitioner would question the frequency column's basis first.\n\n"
     + t[t.index("## What the 60 imply"):],
     None),
    # A fenced example quoting the template is not a Verification section.
    # section_body() searched raw text, so a document that merely quoted
    # "## Verification" satisfied the gate the real section proves -- the same
    # blank-fences-first rule the appendix parser already applied, in the
    # sibling function that did not.
    ("final-rejects-a-fenced-verification-example", "d_ok.md",
     lambda t: t[:t.index("## Verification (Phase 7)")]
     + t[t.index("## What the 60 imply"):]
     + "\n```markdown\n## Verification\n\nFirst answer paragraph here.\n\n"
     + "Second answer paragraph here.\n\nThird answer paragraph here.\n\n"
     + "Fourth answer paragraph here.\n\nFifth answer paragraph here.\n```\n",
     "no Verification section"),
    # Outer pipes are optional in Markdown. Requiring them meant a valid table
    # of five answers was seen as one block and the document rejected -- a false
    # failure, the defect class this checker exists not to produce.
    ("final-accepts-a-table-without-outer-pipes", "d_ok.md",
     lambda t: t[:t.index("## Verification (Phase 7)")]
     + "## Verification (Phase 7)\n\nQuestion | Answer\n---|---\n"
     + "Generic items | Items 4 and 11 apply to any subject in this category.\n"
     + "Indistinct personas | P2 and P5 cannot be told apart by their asks.\n"
     + "Inferred marks | The marks on items 7 and 19 read as inferred.\n"
     + "Missing decisions | Items 22 and 30 restate their asks.\n"
     + "Practitioner check | The frequency column's basis would be questioned.\n\n"
     + t[t.index("## What the 60 imply"):],
     None),
    # The same heading-level defect as the appendix parser, in the sibling
    # function: "### Verification" matched, but the body ended only at the next
    # H2, so an empty section absorbed its sibling headings and their paragraphs
    # were counted as the answers it did not contain. Fixing one boundary and
    # not sweeping for the other is why this survived a round longer.
    ("final-rejects-an-h3-verification-absorbing-siblings", "d_ok.md",
     lambda t: t[:t.index("## Verification (Phase 7)")]
     + "## Review\n\n### Verification\n\n### Other notes\n\n"
     + "The roster was approved without changes on the first pass.\n\n"
     + "The budget was set at sixty before any item existed.\n\n"
     + "The archetype was chosen from the table in Phase 0.\n\n"
     + "The inventory was built after the items were written.\n\n"
     + t[t.index("## What the 60 imply"):],
     "substantive block"),
    # A table's header row names the columns. Counting it let a header plus four
    # data rows read as five answers with one question unanswered.
    ("final-rejects-a-table-header-counted-as-an-answer", "d_ok.md",
     lambda t: t[:t.index("## Verification (Phase 7)")]
     + "## Verification (Phase 7)\n\n| Question | Answer |\n|---|---|\n"
     + "| Generic items | Items 4 and 11 apply to any subject in this category. |\n"
     + "| Indistinct personas | P2 and P5 cannot be told apart by their asks. |\n"
     + "| Inferred marks | The marks on items 7 and 19 read as inferred. |\n"
     + "| Missing decisions | Items 22 and 30 restate their asks. |\n\n"
     + t[t.index("## What the 60 imply"):],
     "4 substantive block"),
    # Appendices written as H3 siblings under an H2. The search accepts an H3
    # appendix heading, so terminating the section only at the next H2 let an
    # empty inventory absorb the appendices after it, and their lane rows then
    # proved the missing inventory existed.
    ("final-rejects-an-h3-inventory-absorbing-later-appendices", "d_ok.md",
     lambda t: t[:t.index("## Appendix A")]
     + "## Appendices\n\n### Appendix B - Current coverage\n\n"
     + "### Appendix C - Run comparison\n\n| Lane | Note |\n|---|---|\n"
     + "| **A - Added in pass two** | analysis only |\n",
     "no inventory lanes can be read"),
    # A lane-shaped row in the wrong appendix is not an inventory either.
    # Documents carry several appendices -- this repo's own dogfood run has a
    # movement appendix beside its inventory -- so selecting the first one that
    # contains a lane row accepts an analysis table as proof the inventory
    # survived. The heading says which appendix it is.
    ("final-rejects-lanes-in-a-non-inventory-appendix", "d_ok.md",
     lambda t: t[:t.index("## Appendix A")]
     + "\n## Appendix B — Run comparison\n\n| Lane | Note |\n|---|---|\n"
     + "| **A — Added in pass two** | analysis only |\n",
     "no inventory lanes can be read"),
    # Lane-shaped text is not an inventory. The guard searched the whole
    # document, so a fenced example -- or the Verification section quoting the
    # expected row syntax -- stood in for the appendix it was meant to prove.
    ("final-rejects-lane-shaped-text-outside-the-appendix", "d_ok.md",
     lambda t: t[:t.index("## Appendix A")]
     + "\n```markdown\n| **A — Not an inventory** | example |\n```\n",
     "no inventory lanes can be read"),
    # Five lines cleared the old non-empty count while recording nothing. The
    # gate exists to require five recorded answers, so the bar is substance --
    # a claim satisfied by a non-claim is the failure this whole suite is for.
    ("final-rejects-five-placeholder-lines", "d_ok.md",
     lambda t: t[:t.index("## Verification (Phase 7)")]
     + "## Verification (Phase 7)\n\nx\n\ny\n\nz\n\na\n\nb\n\n"
     + t[t.index("## What the 60 imply"):],
     "from 5 non-empty placeholder block(s)"),
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

        print("\nadversarial (--adversarial):")
        core_path = os.path.join(FIXTURES, "d_ok.md")
        try:
            base = adversarial_from(load("d_ok.md"))
        except (BrokenFixture, ValueError) as exc:
            report(False, "adversarial base", str(exc))
            base = None
        if base is not None:
            ok_path = os.path.join(tmp, "adversarial_ok.md")
            with open(ok_path, "w", encoding="utf-8") as fh:
                fh.write(base)
            rc, out = run(core_path, "--adversarial", ok_path)
            fails = failures_in(out)
            report(rc == 0, "generated adversarial pass over d_ok.md passes",
                   "" if rc == 0 else (fails.splitlines() or [""])[0].strip()[:90])

            # The precondition, which no mutation of the document can express:
            # it is a property of the core document, not of this one.
            rc, out = run(os.path.join(FIXTURES, "nocov.md"), "--adversarial", ok_path)
            fails = failures_in(out)
            report("nothing to run against" in fails,
                   "a core with no coverage pass is refused",
                   "" if "nothing to run against" in fails
                   else (fails.splitlines() or ["(passed)"])[0].strip()[:80])

            # The other precondition, and also a property of the core: these
            # passes require it to have passed --final, and --final refuses a
            # Verification section too short to hold Phase 7b's five answers.
            # Both passes are checked, because both stated the precondition and
            # only one of them enforced it.
            thin = re.sub(r"(^#{2,3}\s*Verification\b.*?)(?=^##\s)",
                          "## Verification (Phase 7)\n\ncoverage marks passed.\n\n",
                          load("d_ok.md"), count=1, flags=re.M | re.S)
            require(thin != load("d_ok.md"), "the Verification section was not thinned")
            thin_path = os.path.join(tmp, "thin_core.md")
            with open(thin_path, "w", encoding="utf-8") as fh:
                fh.write(thin)
            for flag, other in (("--adversarial", ok_path),
                                ("--enriched",
                                 os.path.join(tmp, "enriched_ok_d_ok.md"))):
                rc, out = run(thin_path, flag, other)
                fails = failures_in(out)
                report("has not passed --final" in fails,
                       f"{flag} refuses a core whose Verification is too thin",
                       "" if "has not passed --final" in fails
                       else (fails.splitlines() or ["(passed)"])[0].strip()[:80])

            for name, mutate, needle in ADVERSARIAL_MUTATIONS:
                try:
                    text = mutate(base)
                except (BrokenFixture, ValueError) as exc:
                    report(False, name, f"mutation no longer applies: {exc}")
                    continue
                require(text != base, f"{name} changed nothing")
                path = os.path.join(tmp, name + ".md")
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(text)
                rc, out = run(core_path, "--adversarial", path)
                fails = failures_in(out)
                if rc == 0:
                    report(False, name, "document passed; the defect was not caught")
                elif needle.lower() not in fails.lower():
                    first = fails.splitlines()[0] if fails else "(no [FAIL] line)"
                    report(False, name,
                           f"wrong reason: wanted {needle!r}, got {first.strip()[:70]!r}")
                else:
                    report(True, name)

            for name, mutate in ADVERSARIAL_POSITIVES:
                try:
                    text = mutate(base)
                except (BrokenFixture, ValueError) as exc:
                    report(False, name, f"mutation no longer applies: {exc}")
                    continue
                path = os.path.join(tmp, name + ".md")
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(text)
                rc, out = run(core_path, "--adversarial", path)
                fails = failures_in(out)
                report(rc == 0, name,
                       "" if rc == 0 else (fails.splitlines() or [""])[0].strip()[:90])

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
