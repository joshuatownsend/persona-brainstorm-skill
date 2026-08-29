---
name: persona-brainstorm
description: Run an unconstrained, demand-side persona and use-case brainstorm — what would real users want from a system if it could do anything, rather than a catalogue of what ships. Derives the personas, captures each ask in their own words plus the decision it feeds, then synthesizes the capability primitives and gaps. Use for personas, user research, use cases, wish lists, gap analysis, feature discovery, whitespace analysis, or roadmap input — and when the user describes that goal without naming it — "who would use this and what would they want", "who are the users of this repo", "what would a developer want from this library that it doesn't do", "what should this MCP server be able to answer", "what are we missing", "brainstorm use cases for X". Runs against any repo (the subject comes from the repo's domain, not its implementation) and against subjects with no repo — a product, service, API, dataset, or team process. Prefer it over an ad-hoc list when the answer is user needs, not features.
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
from an implementation, nothing in Phases 0–2, 5, 6 or 7 needs to know what the subject is built from.
A DDI platform, a payments API, an internal data warehouse, a design system, a hiring process —
all have practitioners with jobs to do, and that is the only input the imaginative half requires.

Only Phases 3–4 touch the artifact itself, and they are optional. If the subject has no repo, no
code, or doesn't exist yet, skip them and the rest works unchanged.

What *does* change per subject is vocabulary: how the subject is phrased, what counts as the
frontier, and where to reach when the obvious asks run out. Phase 0 pins those down once, in one
table, and every later phase reads them from there. If you want to see the whole workflow run end
to end on a real subject before starting your own, `references/worked-example-ddi.md` is the run
this skill was extracted from.

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

**When you already know the implementation, the phase order cannot protect you.** The most likely
operator of this skill is someone who built the subject, and cannot un-see what they already know.
This is the common case, not the edge case. Don't pretend otherwise and don't skip the exercise;
do one of these, and say in the document which:

- **Derive the roster and the items in separate agents — two calls, not one.** A roster you derived
  yourself carries the contamination at its most consequential point: personas that mirror the
  surface you already know, and no trace of the people it doesn't serve. Handing that roster to a
  blind generator locks the omission in, because a generator only writes for the roles it is given.
  Blinding Phase 2 while Phase 1 stays contaminated protects the cheap half.

  Both calls need the same **context block**. Assemble it once and pass it verbatim to each:

  > the subject · the frame, with its scope constraint · the archetype, its frontier class, and its
  > reach-further axes · the total item budget · any seed personas the *user* supplied

  Every line of that is Phase 0 output — things the operator and user *decided*, not things read
  off the artifact — which is why passing it costs nothing in contamination. Assemble it once
  rather than listing inputs per call: an enumerated list maintained in two places loses an entry
  eventually, and a blind agent cannot notice what it was never given.

  **Call one — the roster.** Context block, plus Phase 1's derivation checklist. Ask it to derive
  the roster, to say what the seed list was missing, and to divide the total budget unevenly across
  the personas it derived. Then run Phase 1's approval gate unchanged: put that roster in front of
  the user, who is the one participant with real domain knowledge and no stake in the
  implementation.

  **Call two — the items.** Context block, plus the approved roster with its per-persona budgets,
  plus **the whole of Phase 2 restated in the prompt** — item schema, frequency vocabulary, the ⚡
  rule, continuous numbering, the no-padding rule. Say explicitly that **the approved roster
  supersedes the seed personas** carried in the block. Phase 1 merges duplicates and the user cuts
  entries at the gate, so a seed list left standing beside the roster can resurrect a persona the
  user removed, or split items across two the roster deliberately merged into one.

  Forbid both calls from reading any file.

  **Passing the method is not contamination; passing the inventory is.** That distinction is what
  makes this work, and it matters most where the two live in one document: when the subject *is*
  the method, "don't read the implementation" and "read the protocol" point at the same file, so
  the protocol has to travel in the prompt rather than by reference. An agent handed a few inputs
  and a prohibition cannot produce a conforming roster or item set — it will hand back something
  shaped like an answer.

  Phase 3 can still run *concurrently* with Phases 1–2, because a blind generator cannot be
  contaminated by an inventory built beside it — **provided nothing from Phase 3 reaches either
  prompt**. Its findings must never enter the context block, the roster call, or the items call.
  Pasting an inventory into a blind agent restores exactly the anchoring this whole arrangement
  exists to prevent, and does it silently, because the output still looks blind.

  **This pushes the contamination back; it does not remove it.** You still wrote the frame, and the
  frame shapes everything downstream. Say that in the document rather than claiming the run was
  clean.
- **Disclose the contamination** at the top of the document, and treat every item that maps neatly
  onto an existing capability as suspect rather than as confirmation.

Prefer the first wherever you can make **two model calls that do not share your context** — a
subagent, a separate session, another person handed the prompt. Isolation is the requirement;
no particular tooling is. The second option is honest but weak — knowing to distrust your own
anchoring does not undo it.

The corollary: **the unserved items are the deliverable.** A document where everything is already
covered has failed. Expect half to two-thirds of items to be partly served or impossible.

## Phase 0 — Frame and scope

Establish six things. Ask the user directly; don't guess.

1. **The subject — and it is not the repo.** The subject is the *system the personas work
   against*, named generically. A repo, if there is one, is only where evidence lives and where
   the output lands. Getting this backwards is the most common way this document comes out small:
   personas who use "an IP address management system" generate a rich, product-independent wish
   list, while personas who use "our CLI's MCP server" generate a bug list about the CLI.

   State the subject as **a hypothetical generic capability over the domain**, never as the
   shipped thing. That phrasing does real work — it gives every persona permission to want
   something nobody has built, which is the entire point of the exercise.

   | Say this | Not this |
   |---|---|
   | "a generic read-only interface capable of answering anything about the DNS/DHCP/IPAM estate" | "the bamcli MCP server" |
   | "a library that fully serves date-and-time handling in TypeScript" | "our `parseDate` module" |
   | "a product that fully serves the incident-response workflow" | "the alerts dashboard" |
   | "an ideal way to get a new engineer productive in week one" | "our onboarding checklist" |

   **One subject per run.** If the repo holds several (a monorepo, a platform with distinct
   products), pick one. A document spanning two subjects produces personas for neither.

   That constrains **generation, not analysis.** Run the method once per subject and read the
   finished documents together afterwards — that is how a platform team gets "which need shows up
   across all forty services" with no single run weakened, and how a re-run of one subject reports
   what moved. Both are in `references/cross-run.md`, and both depend on the stable slugs Phase 6's
   template requires.

   You may need light orientation to name the domain at all. Keep it tightly bounded, because
   Phase 3's whole protection is that you have not yet seen the surface:

   - **Allowed now:** the README's first paragraph, the package/manifest name and description,
     the top-level directory names, the user's own description of the thing.
   - **Deferred to Phase 3:** command lists, API surface, feature docs, tests, changelogs,
     issue trackers, anything enumerating what it does.

   You are answering *what field is this in and who works in it* — not *what does it do*.

2. **The frame** — the sentence the whole document answers, built on that subject. A good frame
   carries a scope constraint that sharpens every downstream item: *"what would a network engineer
   ask a **read-only** interface over the IPAM estate, if it could answer anything?"*, *"what would
   a support engineer want from this library **without reading its source**?"*, *"what would a
   frontline responder want from an incident tool **during** an incident, not after?"* Those bolded
   constraints are what make the items specific. The "if it could answer anything"
   clause is not decoration — say it out loud so the constraint that survives is the deliberate
   one rather than an accidental one. A frame like "what could this product do" is too loose to
   produce anything good. If the user hasn't given you one, propose two or three and let them pick.

3. **The item budget — a lever, not a size.** Ask for a target count and treat it as a forcing
   function. The first fifteen items are the obvious ones anyone could write; the value is
   concentrated in the back half, because reaching a bigger number is what pushes past the familiar
   asks and out along the reach-further axes for your archetype. If a user doubles the number on a
   second pass, they are not asking for padding — they are asking you to reach further. 40–80 is a
   healthy band; 60 is a good default.

4. **The seed personas** — whoever the user already has in mind. Often incomplete, sometimes
   containing duplicates. Both get fixed in Phase 1.

5. **Whether to run the coverage pass at all**, and at what depth. Offer three:
   - **Full** — verify what's served today against the evidence and cite it **in whatever form
     the lane provides**: `file:line` for code, the document and section for a written process,
     the named report, dashboard, or role for a human lane. Write up any defect you find as its
     own issue doc. Never invent a citation to satisfy the format — if a lane cannot actually be
     verified, mark it Light and say so. Most expensive, and the pass that finds real bugs — in
     the run this skill came from, it surfaced a security-relevant enforcement gap that no amount
     of doc-reading would have found.
   - **Light** — build the coverage map from manifests, docs, and public surface. Best-effort
     rather than proven.
   - **None** — pure demand-side. Fastest, and the only option when the subject has no artifact
     to inspect. Loses the gap-list half.

   In a large codebase, verifying all 40–80 items against source is disproportionate. Scope Full
   verification to the items behind your Phase 5 primitives, mark the rest Light, and say in the
   appendix which marks were proven and which were inferred. A coverage column that silently mixes
   the two is worse than one that admits the split.

6. **The subject archetype** — one row of the table below. It sets the vocabulary for the whole
   run, and it is the only thing in this skill that varies by subject.

### Subject archetypes

Pick the closest row. It fixes four things every later phase reads back: how you phrase the
subject, what counts as the frontier in Phase 2, which directions to reach when the obvious asks
run out, and which discovery recipe Phase 3 uses. If two rows fit, run the one the **personas
experience**, not the one you build. State the row you picked in the document's opening section —
a reader who disagrees with the archetype will disagree with everything downstream, and that is a
useful argument to have on page one rather than at the end.

| Archetype | Phrase the subject as | Frontier class (⚡) | Reach-further axes | Discovery |
|---|---|---|---|---|
| **Read surface** — query API, MCP server, dashboard, reporting layer | "a generic read-only interface over \<domain estate\>" | reads that feel like writes: simulation, blast radius, what-if | time ("what was true last Tuesday"), cross-source joins, entitlement, provenance | `references/discovery.md` § Read surface |
| **Library / SDK / framework** | "a library that fully serves \<the job it exists for\>" | migration and failure injection — "what breaks if I upgrade", "make it fail the way prod does" | version skew, error paths, extension points, debuggability, the escape hatch | § Library |
| **Application / UI product** | "a product that fully serves \<the workflow\>" | the task done *for* you rather than *by* you | degraded and offline states, multi-user collision, recovery from a mistake, handoff between people | § Application |
| **Data platform / warehouse / dataset** | "a store that can answer anything about \<domain\>" | counterfactual and lineage-aware answers — "where did this number come from, and what if the input were different" | freshness, grain mismatch, backfill and restatement, access scope | § Data platform |
| **Infrastructure / service / platform** | "a platform that fully operates \<the estate\>" | pre-flight and rollback reasoning — "prove this is safe before I do it" | failure modes, capacity, cost attribution, audit and who-did-what | § Infrastructure |
| **Process / non-software** | "an ideal way to \<the outcome\>" | the decision made without convening anyone | escalation, exception handling, institutional memory, the case nobody wrote down | § Process — the lanes are human; skip Phase 3 only if there is genuinely nothing to inspect |
| **None of these** | derive it — see below | derive it | derive it | write the recipe; see `references/discovery.md` § Contract |

**A subject whose value includes changing something is not the Read-surface row.** That row is for
subjects whose value is *answering* — its phrasing and its frontier are both read-only, so picking
it for a payments API, a provisioning platform, or a deployment tool deletes the core asks (create,
refund, reverse, roll out) before the brainstorm starts. "API" alone does not put a subject there.
Use the **Infrastructure / service / platform** row, whose frontier — pre-flight and rollback
reasoning — is already write-shaped, or derive your own below. The read-only constraint is a
deliberate scope choice made in the frame, never a default inherited from the word "API".

**If no row fits, derive the four columns rather than forcing a fit.** The columns are not
arbitrary; each answers a fixed question, and any subject can answer them:

- **Subject phrasing** — complete "a \_\_\_ that fully serves \_\_\_" using the *domain's* noun,
  never the implementation's. If the blank wants your product's name, you have the wrong noun.
- **Frontier class** — name the kind of ask that is obviously valuable, obviously hard, and that
  a cautious reader would delete first. That deletion instinct is the detector: whatever you
  flinch at is the frontier.
- **Reach-further axes** — ask what dimension the obvious asks all hold constant. Time, other
  systems, permission, provenance, failure, and scale are the usual constants; the axis is
  whichever of those your first fifteen items never vary.
- **Discovery** — read `references/discovery.md` § Contract. Phases 4–5 need exactly two things
  from discovery: a set of named lanes and each lane's real limits. Write the shortest recipe
  that produces those two, and consider contributing it back as a new archetype row.

### Where the document lands

Default to `PERSONAS.md` at the repo root, unless the repo has a docs convention that fits better.
Check whether that path sits in a **generated or managed tree** — a
codegen config, a `*.generated` marker, a template-sync bot, or an `AGENTS.md`/`README` warning
that regeneration overwrites the tree (in a Printing Press tree the tells are `.printing-press.json`
and a `.printing-press-patches/` directory). If it does, regeneration will clobber the file: write
it where the tree's escape hatch protects it — a patch ledger, an ignore list, a directory the
generator doesn't own — and say in the document which you did.

## Phase 1 — Derive the personas, then stop

Start from the user's seed list and do three things to it:

- **Merge duplicates.** Seed lists routinely name the same human twice under two job titles. Say
  in the document that you merged them, and why.
- **Add what's missing, each with a stated reason.** The added personas are usually where the
  document earns its keep, because they're the ones the subject's own framing doesn't see. Work
  the list below; most subjects are missing at least three of them.

  - **The highest-volume, lowest-expertise user** — most contact with the subject, least ability
    to work around it when it doesn't fit.
  - **The security, compliance, or audit reader** — their questions are usually answerable from
    what already exists, and nobody has ever asked them.
  - **The automation or pipeline consumer** — asks in a different shape entirely: determinism,
    freshness guarantees, machine-readable output.
  - **The rare-but-high-stakes user** — migrations, acquisitions, audits, incidents. A handful of
    enormous questions a year, each expensive to get wrong.
  - **The non-hands-on decision maker** — never touches the subject, only its output, and has to
    defend it to people who weren't there.

  The three below are the ones a roster almost never contains, because **every evidence source you
  have is blind to them**. Name them deliberately or they will not appear at all:

  - **The user who tried it and left.** They file no tickets and answer no surveys. A roadmap
    built from the people who stayed is optimizing for survivors and calling it demand.
  - **The user forced in by someone else's decision** — a migration, a mandate, a vendor change.
    They never chose the subject, and their asks look nothing like a volunteer's.
  - **The classes nobody represented** — on a screen reader, on a bad connection, in a language
    this was not written in, on hardware two generations old. They are absent from the material
    that shaped your priors, so they will never surface on their own. Ask explicitly, and if you
    conclude none belong on the page, say why rather than leaving it silent.
- **Include the agent itself as a persona** whenever the subject might be driven by an AI agent.
  This is the single most productive addition when planning any surface an agent will drive,
  because it generates asks no human persona will — what must I read before I'm allowed to act,
  how fresh is this answer, what am I entitled to see, what would this change touch. Those items
  are cheap relative to their value and have no owner in a feature list organized by subsystem.

Give each persona a one-line justification for being on the page. If you can't write one, cut it.

**Build the roster on one axis, and name it.** Job roles, or jobs-to-be-done, or relationships to
the subject — pick one and hold it. A roster mixing axes cannot be checked for completeness, which
defeats the point of asking who is missing: a set containing four job titles, one piece of
software, and one review function has no "rest of the set" to reason about. Declare it in the
document header, beside the coverage key, on a line of exactly this form:

  `**Roster axis:** job role` — or job-to-be-done, or relationship to the subject.

Phase 7's checker reads that line and nowhere else, for the same reason it reads the tally line and
nowhere else: a claim mentioned in passing further down is not a declaration, and a checker that
accepts one cannot tell a document that declared its axis from one that merely discussed it. Where a persona genuinely belongs to a different axis and still earns its place — the
executing agent usually does — say so explicitly rather than letting it pass unremarked.

**Then apply the distinctness test, which is the one Phase 1 has always implied and never
supplied.** Cover the persona names and read only the asks each one owns. If you cannot tell two
personas apart that way, they are one persona wearing two job titles, and the merge instruction
above applies no matter how different their justifications sound. Two people with the same
questions are the same persona for this document's purposes, whatever their business cards say.

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
problem. If you're short, don't pad with variations on what you have — reach along the
**reach-further axes for your archetype**, chosen in Phase 0. Those axes exist because the obvious
asks all hold some dimension constant, and varying it is where the good items are: for a read
surface, time and joins and entitlement; for a library, version skew and error paths; for a
process, the exception nobody wrote down. Two more pay off in every archetype regardless of which
axes you picked: what the **rare high-stakes persona** asks once a year, and the frontier class
below. Those are reliably the best items on the page.

Number items continuously across the whole document (not per persona) so the synthesis can cite
them.

**Say where the frequencies came from.** `weekly` and `quarterly` are empirical claims, and a
reader takes that column at face value — it is often the first thing they read. Unless you measured
them, they are estimates, and the document has to say so in the header beside the coverage key, on
a line of exactly this form:

  `**Frequencies:** estimated from the personas, not measured` — or `observed from <source>`.

Same rule as the axis and the tally: that line is the only place the claim is read from, and a bare
`**Frequencies:**` with nothing after it declares nothing. Never let an invented number stand
where a reader will take it for a finding. The same honesty applies to the asks themselves: unless
they came from real users, they are hypotheses about what people would say, and the document is a
set of hypotheses worth testing rather than a report of what was found.

Each item is a row with four things:

| Field | What good looks like |
|---|---|
| **The ask, in their words** | A quoted sentence the persona would actually say out loud — a question (`"Who was on 10.20.5.66 at 14:20 yesterday?"`) or a want (`"I want to restyle this component without forking it."`). Not `Historical lease attribution query`; not `Themeable component API`. If it reads like a Jira title, rewrite it. |
| **Why — the decision it feeds** | The job the answer does. Not a restatement of the ask. Watch for asks already phrased *as* a decision — `"do I pad, or hand back eight and say so?"` — where the Why has nowhere left to go and becomes an inversion of the question. When that happens, name the **consequence** instead: what goes wrong, and to whom, if the answer is unavailable. `"Attribution for abuse, incident, and legal requests"` earns its place; `"lets them see lease history"` does not. If you can't name a decision, the item probably isn't real. |
| **Today** | What they do *instead*, right now. `"Greps four spreadsheets and guesses"` · `"Asks Dave"` · `"Gives up"` · `"Nothing — they don't know it's answerable"`. This is the demand-side measure and the coverage column is not: coverage says whether *you* serve the ask, while this says whether anyone needs it served. A `○` somebody already pays a person to work around is an opportunity; a `○` nobody has ever attempted is usually a non-problem. `"Gives up"` and `"Doesn't know to ask"` are the two most valuable answers here. |
| **Frequency** | `many/day`, `daily`, `weekly`, `quarterly`, `per-incident`, `per-release`, `onboarding`, `per-run`. Frequency separates the item deserving a first-class answer from the one deserving a documented workaround, and it makes the uneven budgets legible. |
| **Coverage** | Phase 4. Leave blank. |

Mark with **⚡** the items in the **frontier class you named in Phase 0** — the class of ask that is
obviously valuable, obviously hard, and that a cautious reader would delete first. For a read
surface that's reads which feel like writes (simulation, blast radius, "what breaks if I delete
this"); for a library it's migration and failure injection; for an application it's the task done
*for* the user rather than *by* them; for a process it's the decision made without convening
anyone. These are consistently the highest-value and hardest items on the page, and the frontier
class is usually where the subject is uniquely suited to something nobody has tried — a read-only
surface, for instance, gets all the value of a change proposal with none of the risk.

If your list has no ⚡ items, you have under-reached. If your ⚡ items are all comfortable, you
named the frontier too conservatively — go back to Phase 0 and find the class you flinched at.

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

Read `references/discovery.md` and follow the section for the archetype you picked in Phase 0. It
states the contract — Phases 4–5 need exactly **named lanes** and **each lane's real limits**, and
nothing else — then gives a recipe per archetype: what to read, in what order, what the lanes
usually turn out to be, and which caveats reliably exist. If your subject is a printed CLI (a
`*-pp-cli` binary, `tools-manifest.json`, an `internal/mcp` tree), `references/discovery/printed-cli.md`
is a fully worked instance of that contract and the closest thing to a template for writing your own.

**Prefer runtime truth over reading source** wherever the subject can describe itself: a `--help`
tree, an OpenAPI document, a `doctor` or self-describe command, an exported type surface, a schema
dump. Self-descriptions are usually more accurate than the docs and far cheaper than the code. Run
only read-only commands during discovery — never one that mutates remote state.

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

**If other subjects have been run, say which primitives they share.** A primitive demanded by
several *unrelated* subjects is a platform capability rather than N copies of a feature, and it is
invisible from inside any single document. `references/cross-run.md` covers it: slugs are the join
key that groups the same primitive across documents, and how *unrelated* the demanding subjects are
decides how much the recurrence counts.

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

## Phase 7 — Verify

Every quality gate before this point is advice addressed to you, and you are the one being graded.
That is not a wording problem, it is a structural one: the model that under-reached is the model
being asked to notice it under-reached. This phase exists because a run of this skill once
self-reported "⚡ count: 21" for a document carrying 26, a 24% error on the single number it was
asked to compute about its own output, and nothing in the method caught it.

**The rule that makes this phase work: you never count anything.**

### 7a — Run the checker

```bash
# <skill-dir> is the directory this SKILL.md lives in — the path you were given when the
# skill loaded. It is NOT the working directory: this skill runs against a target repo.
python "<skill-dir>/scripts/verify.py" <output-path>      # --strict fails on warnings too
```

Resolve that path against the skill's own directory every time. A bare `scripts/verify.py` is
wrong in every repo but this one: usually it does not exist, and occasionally it is some other
project's script that will run happily and tell you nothing about your document.

It parses the tables and computes what the document actually contains, then compares that against
what the document claims. It checks continuous numbering, per-persona counts against the roster's
promised budgets, budget flatness, the frontier count, the coverage tally, frequency values against
the vocabulary, whether a *Why* merely restates its *Ask*, whether asks are quoted, and whether the
primitives cite item numbers that exist.

Fix what it reports and run it again. Do not talk yourself out of a FAIL — every rule in it exists
because that failure actually happened.

**Run it a second time after 7b, with `--final`.** That pass additionally requires the Verification
section to exist. Nothing else would catch its absence: 7a runs before 7b by definition, so the
first invocation cannot check for a section that has not been written yet, and an executor who
simply skips the adversarial read leaves a document that passes and reads as though it was
reviewed.

The checker reads claimed figures **only** from the canonical tally line. That is deliberate: a
good document discusses numbers in prose — quoting a figure that turned out wrong, citing an
earlier pass — and a checker that scans everywhere will read that discussion as a claim. If your
tally line is missing, it says so rather than guessing.

### 7b — Have a fresh agent read it adversarially

The checker cannot tell you whether the document is any good, only whether it is internally
consistent. The judgments that matter are exactly the ones you cannot make about your own output,
so hand the finished document to a **separate agent that has not seen this run** and ask it, in
these words:

- Which items would apply unchanged to any other subject in this category? Name them.
- Which personas are indistinguishable from one another by their asks alone?
- Which coverage marks read as inferred rather than verified?
- Which items state no real decision, only a restatement of the ask?
- What would a practitioner in this domain immediately know is wrong?

Its answers go in the document, under the tally, as a short **Verification** section — including
the ones you disagree with, marked as disagreed and why. A finding you argued down is more useful
to the next reader than a finding you deleted.

If no second agent is available, say so in that section rather than omitting it. An absent
verification section reads as a passed one.

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
- **An archetype forced to fit.** If you picked "read surface" for a library because it was the
  first row, every item will come out as a query and the real asks — migration, failure, escape
  hatches — never get written. Deriving the four columns from scratch is cheaper than a run spent
  in the wrong vocabulary.
