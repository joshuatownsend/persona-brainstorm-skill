# The primitive slug vocabulary

A primitive is a capability the subject would need, named once and addressed by
a stable kebab-case slug. Slugs are the join key across runs: `cross-run.md`
groups by them, and a primitive named `provenance` in one run and
`data-lineage` in another will not group, so the two subjects appear to share
no need when in fact they share the strongest one.

This file is that written vocabulary. It exists so a second run reaches for an
existing name before minting a new one.

## How to use it

**Reuse before you mint.** Read this list before naming a primitive. If a
proposed primitive means what an entry here means, take the slug — even when
the phrasing you had in mind was better. Consistency across runs is worth more
than the best name for one of them.

**Mint freely when nothing fits.** A vocabulary that forces every finding into
an existing name produces false agreement, which is worse than no vocabulary:
two subjects would appear to share a primitive because the namer had nowhere
else to put it. When the fit is arguable, mint the new slug and say in the
document why it is not the existing one.

**Never reuse a slug for a different idea.** This is the one unrecoverable
mistake. A slug that means one thing in run A and another in run B makes every
future comparison silently wrong, and nothing in the document will reveal it.
Renaming a primitive is cheap; re-pointing a slug is not.

**Display names may vary; slugs may not.** The name in the heading is prose and
can be rewritten to fit its document. The slug is an address.

## The vocabulary

Every entry below was derived from one run — this repo as its own subject,
recorded in `PERSONAS.md`. That is a single subject in a single category, so
treat the list as a seed rather than a survey: the generic entries are likely
to recur, and the two marked *method-specific* may not travel.

The item numbers each primitive was derived from live in `PERSONAS.md` and are
not repeated here. A claimed figure belongs at one address.

| Slug | Means |
|---|---|
| `self-assessment` | A way for the subject to tell its operator *and* its reader that this run under-reached, went generic, or was too thin to support its own output. *Method-specific.* |
| `provenance-per-claim` | Every claim labelled observed / inferred / invented, carrying its source. |
| `run-identity` | Stable ids, a pinned version, and a meaningful diff between two runs of the same subject. |
| `failure-injection` | A corpus on which the subject reliably produces plausible but hollow output, so its blind spot can be observed rather than argued about. *Method-specific.* |
| `counterfactual-demand` | The picture under a different assumption — the wrong primary user, a competitor as subject, the single input that would most change the answer. |
| `absence-detection` | Machinery for finding who is *not* on the list: churned users, users forced in by migration, unrepresented classes, the users of year three. |
| `consequence-weighted-ranking` | Sorting by what an answer changes — data model, reversibility, regret — rather than by how many people want it. |
| `external-grounding` | Prior art: who built this before, and what the ecosystem will cover anyway. |
| `output-shaping` | The same evidence rendered for a different audience — landing-page copy, a slide, a customer-safe subset, a structured feed. |
| `cross-run-aggregation` | Many subjects at once, and the needs common to all of them. |

## Reconciling two vocabularies

When a set of subjects is to be compared and the runs already exist, reconcile
before aggregating rather than after. Two primitives reconcile when they would
be served by the same capability — not when they sound alike.

Record the reconciliation as a mapping alongside the aggregate, and keep the
original slugs in their own documents. Rewriting history so the runs appear to
have agreed all along destroys the evidence that they did not, and the
disagreement is usually the more interesting finding: a primitive that one run
names and another misses is a weak primitive, and the honest report says so.
