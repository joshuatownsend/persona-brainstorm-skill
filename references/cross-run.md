# Comparing runs

One subject per run is a rule about **generation**, not about analysis. A document that spans two
subjects produces personas for neither — that is why Phase 0 forbids it. Nothing stops you reading
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

---

## Re-running one subject

Run the whole method again — Phase 0 through 7, a genuinely fresh pass. Do **not** hand the previous
document to the generating agents; it anchors exactly as an inventory does, and the point of a
second run is to shed the first one's framing. Compare the finished documents, not the drafts.

Then report movement in these terms:

- **Personas gained or lost**, by slug. A persona that disappears without the subject changing is
  usually a roster error in one of the two runs, not a real departure — say which you think it is.
- **Primitives gained, lost, or renamed.** A rename with the same citations is not a change; a slug
  reused for a different idea is a mistake and will make every future comparison wrong.
- **Coverage movement per primitive.** This is the number worth having: it says whether shipping
  actually served the demand you found, and it is the only measurement in this whole method that
  compares against something other than its own judgement.
- **What the method did, versus what the world did.** If the skill itself changed between the runs,
  some movement is method drift and some is real. Say which is which, or the reader will assume all
  of it is real. When you cannot tell, say that.

**Do not average the two runs.** They are two independent judgements, and the disagreement between
them is information — a primitive that appears in one pass and not the other is a weak primitive,
and the honest report says so rather than quietly keeping it.

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
