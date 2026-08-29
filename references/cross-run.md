# Comparing runs

One subject per run is a rule about **generation**, not about analysis. A document that spans two
subjects produces personas for neither — that is why Phase 0 forbids it. Nothing stops you from reading
several finished documents together afterwards, and this file is how.

Two jobs live here, and they are different. **Re-running one subject** asks what changed since last
time. **Reading many subjects** asks what they have in common. Both need stable slugs, which is why
Phase 6's template requires them.

---

## What makes two runs comparable

Item numbers are positional. Insert one item at the top and all sixty renumber, so a textual diff
of two runs is noise — which is exactly the complaint behind the ask *"diff two runs and tell me
which changes are substantive versus reworded."*

**Slugs are the join key.** Personas and primitives carry a stable kebab-case slug, chosen once and
kept identical across re-runs of the same subject. Items do not: an item is a sentence someone would
say, and rephrasing it is not a change worth tracking. Items are compared through the primitives
that cite them.

So a comparison is over three things:

| | Compared by | A change means |
|---|---|---|
| **Personas** | slug | someone entered or left the picture |
| **Primitives** | slug | the underlying capability set moved |
| **Coverage** | per-primitive tally | the subject served more or less of what people want |

Coverage is the one dimension that may be unavailable. A run at coverage depth **None** carries no
marks — the template removes the column — and that depth is not an edge case: it is required when
the subject has no artifact to inspect. Compare coverage only when *both* runs were Full or Light,
and when they were not, say so in the report rather than leaving the dimension silently absent. A
missing row reads as "no movement".

---

## Re-running one subject

**Snapshot the existing document before you regenerate anything.** A re-run follows Phase 6, which
writes to the agreed output path — `PERSONAS.md` by default — so the second run overwrites the
first, and the first is what the comparison needs. Either copy it to a dated name
(`PERSONAS.2026-08-29.md`, or a `personas/` directory keyed by date) or give the new run a distinct
output path in Phase 0. Do this even in a repository: `git show` will recover a committed file, but
it will not recover one that was never committed, and the skill explicitly supports subjects with
no repository at all, where nothing recovers it.

Two different things get called a re-run, and only one of them is comparable.

**A comparison re-run holds Phase 0 constant** — same subject, same frame and scope constraint,
same item budget, same archetype, same coverage depth. Regenerate the roster and the items fresh,
and keep the previous *document* out of the generating agents' prompts, because it anchors exactly
as an inventory does. But carry the *inputs* over deliberately. Change the frame and every
difference downstream is confounded by that change: a primitive present in one pass and missing
from the other may say nothing whatever about the subject.

**A reframe is not a comparison.** If the frame itself was wrong, that is the corrected-frame
workflow in `SKILL.md`, and its output is not comparable with what came before. Say plainly that
the frames differ and compare nothing — a movement report across two frames measures your own
wording, not the world.

Compare the finished documents, not the drafts.

**Reconcile the slugs before comparing anything.** A blind agent cannot know what the previous run
called things, so the same idea will often arrive under a synonym — `provenance-per-claim` one time,
`claim-provenance` the next. Joining on slugs without reconciling first reports that one vanished
and another appeared, which is the loudest possible false finding.

Reconciliation happens **after** both documents exist, never in the prompt: put the two slug lists
side by side, map the pairs that are plainly the same idea, and record the mapping alongside the
comparison so a later reader can check your judgement. That preserves generation isolation for the
same reason aggregation does — it operates on finished output, not on the run.

Then report movement in these terms:

- **Personas gained or lost**, by reconciled slug. A persona that disappears without the subject
  changing is usually a roster error in one of the two runs, not a real departure — say which you
  think it is.
- **Primitives gained, lost, or renamed.** Decide renames from the reconciliation mapping and from
  what the cited asks actually *say* — never from the citation numbers. Those are item numbers, and
  this file has already said they are positional: two unrelated primitives can both cite items 4
  and 12, and a genuine rename can cite entirely different numbers because the fresh run sampled
  different asks. A slug reused for a different idea is a mistake and will make every future
  comparison wrong.
- **Coverage movement per primitive** — only if both runs graded coverage, and **with a caveat that
  limits what it can mean.** Two fresh runs
  sample different asks for the same primitive, so a coverage figure can move because the cohort
  changed and not because anything shipped. Movement between two independent runs tells you the
  demand picture shifted; it does **not** measure whether your work served it.

**To measure whether shipping served demand, hold the cohort fixed.** Take the *previous*
document's items unchanged and run Phases 3–4 against today's artifact — a re-grade, not a
brainstorm. Same asks, same wording, new coverage marks. Hold the discovery pass and the coverage
depth constant too, and note in the report which agent graded each pass. This is the closest thing
here to a measurement against something other than the method's own judgement, and it is worth
doing separately from a fresh run rather than conflated with one.

### What a comparison cannot tell you

Three things vary between any two runs, and each one confounds attribution on its own:

| Confound | Controlled by | Left uncontrolled |
|---|---|---|
| **Framing** — subject, frame, budget, archetype | holding Phase 0 constant | every difference downstream |
| **Sampling** — which asks got written | re-grading a fixed cohort | coverage moves when nothing ships |
| **Evaluator** — Phase 4 is a judgement | same grader, same depth, same discovery pass | marks move when nothing ships |

Controlling one does not license attribution; it only removes one alternative explanation. A
fixed-cohort re-grade rules out sampling and leaves evaluator drift entirely intact — a different
agent, or a deeper discovery pass, can move a mark from ◐ to ✅ with nothing shipped at all.

So report movement as **evidence, qualified by what was held fixed**, and never as proof that the
work served the demand. Where a mark changed and you cannot point at a corresponding change in the
artifact, say the mark changed and the cause is unestablished. That sentence is more useful than a
confident number, and it is the honest form of the only measurement this method has.
- **What the method did, versus what the world did.** If the skill itself changed between the runs,
  some movement is method drift and some is real. Say which is which, or the reader will assume all
  of it is real. When you cannot tell, say that.

**Do not average the two runs.** They are two independent judgements, and the disagreement between
them is information — a primitive that appears in one pass and not the other is a weak primitive,
and the honest report says so rather than quietly keeping it. That reading holds **only** for a
comparison re-run with Phase 0 held constant. Across changed inputs, a one-run-only primitive tells
you the inputs changed.

---

## Reading many subjects

Forty services, one document each. The question is which primitives recur.

Group by primitive slug across documents and count how many subjects demand each. Then:

- **A primitive demanded by many unrelated subjects is a platform capability**, not N copies of a
  feature. That is the whole reason to do this: it converts forty local findings into one central
  decision.
- **Weight by unrelatedness, not by count.** Ten services owned by one team that share a primitive
  is one signal repeated ten times. Two services with nothing in common demanding the same thing is
  stronger evidence than either.
- **A primitive that appears everywhere and is served everywhere is not an opportunity.** Check the
  coverage marks before treating recurrence as a gap.
- **Slug discipline is the whole game.** If two teams name the same idea `provenance` and
  `data-lineage`, they will not group, and you will conclude there is no shared need. Keep a
  written slug vocabulary for a set of subjects that will be compared, and reconcile before
  aggregating rather than after.

Aggregation reads finished documents only. It never merges two subjects into one run.

---

## What not to build

**Determinism is the wrong goal.** The ask *"same input, same output, or the diffs are
meaningless"* describes a real frustration and a remedy that will not work: a language model asked
to imagine sixty asks will not produce the same sixty twice, and a method that pretended otherwise
would be brittle theatre — a seed and a temperature setting buying reproducibility of wording while
the judgements underneath still move.

Serve the need instead of the request. The frustration is that **diffs are unreadable**, and stable
slugs fix that without needing sameness: two runs that share no sentences can still be compared
persona-by-persona and primitive-by-primitive, which is the comparison anyone actually wanted. Say
so plainly when someone asks for determinism, and show them a slug diff.

The corollary is worth stating: **a re-run that produces different wording and the same primitives
is a good sign**, not a failure. It means the finding survived being re-derived by a fresh pass.
Identical output would tell you only that the cache worked.
