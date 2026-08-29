---
name: persona-brainstorm
description: Run an unconstrained, demand-side persona and use-case brainstorm about what users would actually want from a system — imagining what could be possible rather than cataloguing what currently ships. Derives the personas, captures what each would ask for in their own words and the decision it feeds, then synthesizes the underlying capability primitives and the gaps. Use this whenever the user wants personas, user research, use cases, a wish list, a gap analysis, feature discovery, whitespace analysis, or roadmap input — and also when they describe the goal without naming any of that, e.g. "who would use this and what would they want", "what should this MCP server be able to answer", "what's possible here that we haven't built", "what are we missing", "brainstorm use cases for X", "what would a real practitioner ask this thing". Works on any subject — a product, a service, a codebase, an API, a dataset, a team's process — not only on shipped software. Prefer this skill over an ad-hoc list any time the answer would be a set of user needs rather than a set of features.
---

# Persona Brainstorm

## What this produces

A single markdown document answering one question: **what would real practitioners ask this thing
for, if it could answer anything?** — with, for every ask, the decision that answer feeds.

The output is deliberately *not* a feature list or a roadmap. Feature lists are written in the
builder's vocabulary and bounded by what exists; this document is written in the user's vocabulary
and bounded by nothing. The point is what's *possible* and what people would genuinely want, not
an inventory of what ships.

## Why this works on any subject

That unconstrained framing is not only what makes the document good — it is what makes this skill
portable. Because the demand side is derived from a **domain and its practitioners** rather than
from an implementation, nothing in Phases 0–2 or 5 needs to know what the subject is built from.
A DDI platform, a payments API, an internal data warehouse, a design system, a hiring process —
all have practitioners with jobs to do, and that is the only input the imaginative half requires.

Only Phases 3–4 touch the artifact itself, and they are optional. If the subject has no repo, no
code, or doesn't exist yet, skip them and the rest works unchanged.

## The one hard rule

**Coverage annotates. Coverage never gates.**

An item does not earn its place by being implementable. It earns its place by being something a
real person would really ask. Whether the subject serves it today is recorded in a trailing column
and nothing else — never in the decision to include it, never in the ordering, never in the
phrasing.

This rule exists because it is the lesson that made the original run valuable. The first attempt
filtered candidates through the shipped surface area and quietly deleted every idea with no
current implementation — precisely the set worth having. If you catch yourself thinking "we can't
do that, skip it," that item is probably one of the best on the page. Write it down, mark it
unserved.

**The phase order enforces this rule so you don't have to.** The imagining happens before any
discovery of what exists. That ordering is deliberate: an inventory read first is nearly
impossible to un-see, and every item afterward bends toward it. Resist the urge to "just quickly
check what it does today" before Phase 3.

The corollary: **the unserved items are the deliverable.** A document where everything is already
covered has failed. Expect half to two-thirds of items to be partly served or impossible.

## Phase 0 — Frame and scope

Establish five things. Ask the user directly; don't guess.

1. **The subject — and it is not the repo.** The subject is the *system the personas work
   against*, named generically. A repo, if there is one, is only where evidence lives and where
   the output lands. Getting this backwards is the most common way this document comes out small:
   personas who use "BlueCat Address Manager" generate a rich, product-independent wish list,
   while personas who use "bamcli's MCP server" generate a bug list about bamcli.

   State the subject as **a hypothetical generic capability over the domain**, never as the
   shipped thing: *"a generic read-only MCP server capable of reading BlueCat Address Manager"*,
   not *"the bamcli MCP server"*. That phrasing does real work — it gives every persona
   permission to want something nobody has built, which is the entire point of the exercise.

   You may need light orientation to name the domain at all (skim a README, a manifest, the
   user's own description). Keep it to *what field is this in and who works in it* — that is not
   the same as an inventory, and the inventory waits for Phase 3.

2. **The frame** — the sentence the whole document answers, built on that subject. A good frame
   carries a scope constraint that sharpens every downstream item: *"what would a DDI practitioner
   ask a **read-only** MCP server over BAM, if it could answer anything?"*, *"what would a support
   engineer ask this library **without reading its source**?"* The "if it could answer anything"
   clause is not decoration — say it out loud so the constraint that survives is the deliberate
   one rather than an accidental one. A frame like "what could this product do" is too loose to
   produce anything good. If the user hasn't given you one, propose two or three and let them pick.

3. **The item budget — a lever, not a size.** Ask for a target count and treat it as a forcing
   function. The first fifteen items are the obvious ones anyone could write; the value is
   concentrated in the back half, because reaching a bigger number is what pushes past familiar
   asks into temporal, cross-source, entitlement, and simulation territory. If a user doubles the
   number on a second pass, they are not asking for padding — they are asking you to reach
   further. 40–80 is a healthy band; 60 is a good default.

4. **The seed personas** — whoever the user already has in mind. Often incomplete, sometimes
   containing duplicates. Both get fixed in Phase 1.

5. **Whether to run the coverage pass at all**, and at what depth. Offer three:
   - **Full** — verify what's served today against the source, cite `file:line`, write up any
     defect you find as its own issue doc. Most expensive, and the pass that finds real bugs; the
     original run surfaced a security-relevant read-only-enforcement gap this way.
   - **Light** — build the coverage map from manifests, docs, and public surface. Best-effort
     rather than proven.
   - **None** — pure demand-side. Fastest, and the only option when the subject has no artifact
     to inspect. Loses the gap-list half.

Also settle the output path. Default to `PERSONAS.md` at the repo root, unless the repo has a docs
convention that fits better. If it's a **generated tree** (look for `.printing-press.json`, a
`.printing-press-patches/` directory, or an AGENTS.md warning that a reprint can overwrite the
tree), a reprint will clobber the file — register it in the patch ledger or write it somewhere the
ledger protects, and say which you did.

## Phase 1 — Derive the personas, then stop

Start from the user's seed list and do three things to it:

- **Merge duplicates.** Seed lists routinely name the same human twice under two job titles. Say
  in the document that you merged them, and why.
- **Add what's missing, each with a stated reason.** The added personas are usually where the
  document earns its keep, because they're the ones the subject's own framing doesn't see. Look
  for: the highest-volume/lowest-expertise user (they benefit most from a natural-language
  interface); the security/compliance reader (their data is usually sitting there unqueried); the
  automation or pipeline consumer; the rare-but-high-stakes user (migrations, acquisitions,
  audits); and the non-hands-on decision maker.
- **Include the agent itself as a persona** whenever the subject might be driven by an AI agent.
  This is the single most productive addition for tool-surface planning, because it generates asks
  no human persona will — what must I read before I'm allowed to act, how fresh is this answer,
  what am I entitled to see, what would this change touch. Those items are cheap relative to their
  value and have no owner in a feature list organized by subsystem.

Give each persona a one-line justification for being on the page. If you can't write one, cut it.

**Then stop and put the roster in front of the user** (AskUserQuestion, or a plain list if it's
long). Show each persona, its justification, and your rough item budget. Ask what's missing, what's
really one person, and who doesn't belong. A wrong roster silently wastes every row generated after
it, and the user usually knows their field far better than any artifact does.

Set item budgets **deliberately uneven** — they should track volume and value, not fairness. A
persona who asks three enormous questions a year and one who asks eight small ones a day should not
get the same number of rows. Even budgets are a tell that you're organizing for tidiness instead of
truth.

## Phase 2 — The items

Work to the budget from Phase 0, and treat missing it as a signal rather than an arithmetic
problem. If you're short, don't pad with variations on what you have — reach into the places the
obvious asks never go: questions with a *time* in them ("what was true last Tuesday"), questions
that need a second system joined in, questions about entitlement and provenance, questions the
rare high-stakes personas ask once a year, and the simulation class below. Those are reliably the
best items on the page.

Number items continuously across the whole document (not per persona) so the synthesis can cite
them.

Each item is a row with four things:

| Field | What good looks like |
|---|---|
| **The ask, in their words** | A quoted sentence the persona would actually say out loud. `"Who was on 10.20.5.66 at 14:20 yesterday?"` — not `Historical lease attribution query`. If it reads like a Jira title, rewrite it. |
| **Why — the decision it feeds** | The job the answer does. Not a restatement of the ask. `"Attribution for abuse, incident, and legal requests"` earns its place; `"lets them see lease history"` does not. If you can't name a decision, the item probably isn't real. |
| **Frequency** | `many/day`, `daily`, `weekly`, `quarterly`, `per-incident`, `onboarding`, `per-run`. Frequency separates the item deserving a first-class answer from the one deserving a documented workaround, and it makes the uneven budgets legible. |
| **Coverage** | Phase 4. Leave blank. |

Mark with **⚡** the items that are reads which feel like writes: simulation, blast radius, what-if,
"what breaks if I delete this." These are consistently the highest-value and hardest items, and a
read-only surface is uniquely suited to them — all the value of a change proposal with none of the
risk. If your list has no ⚡ items, you have under-reached.

## Phase 3 — Inventory what exists today

Skip entirely if the user chose no coverage pass, or if there's nothing built to inspect.

Only now go look at the artifact. Build a map of what the subject actually serves today. This is
reference material for Phase 4 and an appendix in the final document — it is not a brainstorming
input, and by this point the items are already written, which is the protection.

Group the surface into a small number of named **lanes** — the distinct ways an answer can be
obtained (e.g. raw API passthrough, local mirror queries, curated composite commands; or for a
non-software subject, the reports, the dashboards, the person you have to email). Lanes are more
useful than an exhaustive endpoint list because a persona's ask usually maps to a lane, not a call.

For each lane, note its real limits: row caps, staleness, auth scope, what it silently refuses.
Those limits become appendix caveats and are frequently more interesting than the inventory itself.

If the subject is a printed CLI (a `*-pp-cli` binary, `tools-manifest.json`, an `internal/mcp`
tree), read `references/discovery-printed-cli.md` for concrete commands and files. That file is the
only product-shaped part of this skill; its closing section states the two things Phases 4–5
actually need from discovery, so you can write an equivalent recipe for any other kind of subject.

## Phase 4 — Annotate coverage

Walk each item against the Phase 3 inventory and mark the trailing column:

- ✅ served well today
- ◐ partially served, or served only by a primitive that doesn't quite fit
- ○ not possible today

Be honest about ◐ — the interesting distinction is usually "the data is there but the shape is
wrong," and collapsing that into ✅ hides the real gap.

Do not reorder, reword, or drop anything based on what you just marked.

## Phase 5 — Synthesis

The items are evidence. This section is the deliverable, and where a merely thorough document
becomes a useful one.

**Tally the coverage.** State the ratio explicitly and say plainly that the ratio, not the item
count, is the finding.

**Cluster the items into capability primitives.** Aim for 6–12. A primitive is the underlying thing
that would need to exist, derived from the items demanding it — *not* a feature name. Every
primitive must cite the item numbers behind it; that citation is what makes the section auditable
rather than assertive. Primitives demanded by several unrelated personas are the strongest signal
on the page — say so when you spot one.

**Write "if you only ask for three."** Name three primitives in priority order with the reasoning
for the order — highest unique value, largest evidence cluster, cheapest unlock. Forcing a rank is
what turns a survey into a recommendation, and it's the part a reader will act on. Note any
primitive cheap enough to ride along with whatever ships first.

**Write two or three observations worth carrying.** The things visible only from the whole page:
which persona the current framing under-serves, where the clearest whitespace is, which cluster has
the worst coverage against the highest willingness to pay.

## Phase 6 — Assemble

Write the document to the agreed path using the structure in `references/output-template.md`.

Open with a short section explaining the frame — and, if there was an earlier pass, what changed
between them. A reader who doesn't know why coverage is demoted will "helpfully" promote it back.

Preserve any Phase 3 inventory as an appendix, clearly labelled as describing today and explicitly
*not* bounding the brainstorm. Carry its caveats there too.

If the full coverage pass turned up a real defect, write it up properly — its own file under the
repo's issue-docs convention — and offer to file it upstream. Link it from the appendix. Those
findings are a genuine byproduct of this workflow and get lost if they live only in a table cell.

## Re-running with a corrected frame

Expect the first run to come out narrower than the user wanted, and expect them to say so — often
as "that's not quite what I was after, let's do another pass." Two things matter.

**Treat a reframe as a fresh run, not an edit.** Go back to Phase 0, restate the subject and frame,
take the new item budget, and generate again. Patching the existing document keeps its original
shape and its original anchoring; the whole reason a second pass is worth doing is that the first
one's frame is what constrained it. Re-deriving the roster is cheap next to shedding the old frame.

**Keep the first pass and say what changed.** Open the new document by naming both frames and why
the second replaced the first. That costs a paragraph and protects the result: without it, the next
reader — or the next agent — has no idea why coverage is demoted, and will promote it back.
Preserve anything independently verified in the first pass (an inventory, a filed defect) as an
appendix rather than discarding it.

The most common correction, by far, is the one the phase order exists to pre-empt: the first pass
anchored on what ships today, and the user wants the version that imagines. If you hear that,
recheck the subject in Phase 0 before anything else — the fix is almost always there, not in the
items.

## Anti-patterns

Check the draft against these before handing it over.

- **A frame anchored on the shipped thing.** If the subject sentence names your binary, your repo,
  or your current API, every persona will ask for a variation on what already exists. Name the
  domain, not the implementation.
- **Items written in product vocabulary.** "Bulk export with filters" is a feature. "Which of these
  400 hosts still answer?" is an ask. The first tells you nothing you didn't know.
- **Coverage leaking forward.** Any sign that the implementable items are better-written,
  better-placed, or more numerous than the impossible ones means the filter got in.
- **Even item counts across personas.** Fairness is the enemy of signal here.
- **Padding to hit the budget.** Three rewordings of one ask is worse than being ten short. The
  number is there to make you reach, not to be satisfied.
- **Items without a decision.** An ask with no job behind it is a feature request in costume.
- **A synthesis that re-lists the categories.** If the primitives map one-to-one onto the personas
  or onto the subject's existing subsystems, no clustering happened.
- **Hedging the ⚡ items.** The hard, "we could never build that" entries are why anyone reads the
  page. Write them at full strength and let the coverage column say ○.
