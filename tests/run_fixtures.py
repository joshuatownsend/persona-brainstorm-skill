#!/usr/bin/env python3
"""Fixture suite for scripts/verify.py.

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
import subprocess
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "fixtures")
VERIFY = os.path.normpath(os.path.join(HERE, os.pardir, "scripts", "verify.py"))
REPO = os.path.normpath(os.path.join(HERE, os.pardir))


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

    print("\nthe shipped document:")
    rc, out = run(os.path.join(REPO, "PERSONAS.md"))
    report(rc == 0, "PERSONAS.md", "" if rc == 0 else "should pass")

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
