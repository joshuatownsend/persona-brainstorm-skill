# Fixtures for the Phase 7 checker

```
python tests/run_fixtures.py
```

Every case here exists because a reviewer found a hole in the checker. Until
now they lived in a session scratch directory and their expectations lived in
chat, which meant the suite was rebuilt by hand on each round of review.

## Two rules, both learned the hard way

**Assert the message, not the exit code.** A fixture written for one check will,
once a later requirement joins the document schema, begin failing on the *new*
requirement instead. It is still red, still "as expected", and no longer
testing anything. This is not hypothetical: fixtures for unquoted asks,
non-ASCII substance and reckoning arithmetic were all silently failing on a
missing `**Frequencies:**` line added rounds after they were written, and a
verdict-only suite reported every one of them green.

The needle is searched **only in the `[FAIL]` lines**. Searching the whole
output would accept a case whose own diagnostic had been downgraded to a
warning while some unrelated check still failed — green for the wrong reason,
which is the same bug one level up.

**Generate negatives by mutating a passing base.** Most cases are
`(base, one mutation, expected message)` rows in `run_fixtures.py`. A schema
change then costs one edit to the base rather than one edit per fixture, which
is the rot above at its source. Static files are kept only for damage a
mutation cannot express — broken numbering, a short table row, a missing
roster.

## Retired fixtures

`RETIRED` in the runner lists files kept on disk but deliberately not asserted,
each with its reason. A fixture is retired when its intent is covered by a
mutation, or when it can no longer reach the check it was written for.

Recording a rotted fixture's *current* message as its expectation is the one
thing not to do. It converts a false green into an asserted false green, which
is worse than losing the case: the suite then actively defends the rot.

Retiring is not deletion. `unquoted.md` still describes a real check — asks
that do not read as speech — which happens to emit a warning rather than a
failure, and the suite has no warning cases yet. It is waiting for one.

## The enrichment base is generated, not stored

`--enriched` cases need an enriched document *and* the core document it expands.
A stored one would need sixty hand-written entries and would rot the moment the
core base changed — the rot the mutation design exists to avoid, at sixty times
the size. So `enriched_from()` builds a conforming enrichment from any core
base, reading its items the same way the checker does but by its own code: a
fixture that parses with the code under test cannot disagree with it, and
disagreeing is the entire job.

The generated base is asserted to pass **before** any mutation of it runs. A
base that already fails makes every negative below it green for the wrong
reason — the suite's own generator introducing exactly the rot the suite exists
to catch.

Two cores are used, because the heading rule has a case that only appears
without coverage: `d_ok.md` exercises the ✅/◐/○ forms, and `nocov.md` exercises
*"What answering this would take"* and the rule that a run which assessed
nothing may not carry `○`.

## Both passes are covered

`verify.py` has a second pass behind `--final`, which adds the Phase 7b
Verification requirements. `FINAL_CASES` runs it, so those checks cannot rot
unnoticed.

## Fixture invariants are not `assert`

They raise `BrokenFixture`. `python -O` strips assertions, and a stripped
invariant here does not raise — it lets a mutation target nothing and then
reports the unchanged document as correctly caught. The suite would go green
by doing nothing.

## Adding a case

Prefer a mutation row. Give it the message its *intent* implies, not the
message it happens to produce — if those differ, the fixture is not testing
what you think. Then confirm it fails before your fix and passes after; a case
that has never been red has not been shown to test anything.

The inventory check at the end of the run asserts that every `.md` in
`fixtures/` is either asserted or explicitly retired, so a case cannot be
orphaned by a rename without the suite saying so.
