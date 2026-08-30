# Enrichment — the story behind each item

Read this when the user asks for an enrichment pass. `SKILL.md` § Enrichment carries the rules that
decide *whether* to run one; this file is the format.

The core document is a table. A table is the right shape for sixty asks — scannable, sortable,
countable — and the wrong shape for persuading anyone that a single ask matters. A row says
`"Who was on 10.20.5.66 at 14:20 yesterday?" · Attribution for abuse requests · Greps four
spreadsheets · many/day · ○`. Everything true about the ask is in there, and none of it lands.

Enrichment writes the three or four sentences that make one row land, for every row.

---

## The one rule this format exists to enforce

**Enrichment is where a demand-side document turns into a case study, and a case study is a
different claim.** The core document says *someone would ask this, and we don't serve it*.
Enrichment writes a scene: a named situation, a pressure, an answer. Prose is far more convincing
than a table cell, and a reader six months out has no way to tell a narrated scenario from an
observed one.

So the format carries its honesty structurally rather than by disclaimer.

### The coverage mark chooses the heading

Every item's third block is titled by the item's own coverage mark. Not by your judgment — by the
mark already in the table:

| Coverage | Third block heading | Mood |
|---|---|---|
| ✅ | **How it's answered today** | present tense — describes something that runs |
| ◐ | **How it's answered today** | present tense, and states what it still cannot do |
| ○ | **What would have to exist** | conditional — describes something assessed and absent |
| *no coverage pass* | **What answering this would take** | conditional — describes the capability, claims nothing about whether it is there |

The third row is not a stylistic variant of the second. At coverage depth **None** nobody looked,
so coverage is **unknown** — and unknown is not the same as unserved. Writing *"what would have to
exist"* over an unassessed item asserts that it does not exist, which is precisely the claim `○`
makes and precisely the claim the footer rule below refuses to let that run make. Withholding the
mark while asserting its meaning one line up would be the same error wearing a different hat.

What a depth-None run can honestly say is what the ask *requires*. That is worth writing — it is
the same capability-shaped reasoning Phase 5 does, one item at a time — and it commits to nothing
about the subject.

This is deliberately mechanical. A heading derived from a mark cannot drift the way a judgment
call does, a reader can tell the forms apart at a glance without trusting you, and a checker can
verify it later with a join on the item number. A disclosure paragraph at the top of the
document achieves none of those things.

### A served item may only claim what the inventory records

The heading rule stops the crudest failure — past tense on an unserved item. It does not stop the
subtler one, which is **invented specificity on a served item**: a plausible number, a named field,
a duration, a sequence of events, all reading as observation because they are too particular to be
anything else.

So: in a **How it's answered today** block, every capability claim must trace to something Phase 3
actually found, and the block names the lane from Appendix A that carries it — **and says whether
that lane's mark was proven or inferred.**

That second half matters because the coverage column routinely mixes the two. A Light pass builds
its marks from docs and manifests without verifying them, and Phase 0 explicitly allows a scoped
Full run that proves the marks behind the primitives and leaves the rest Light. The core document
keeps that distinction in Appendix A — which does not travel with the enriched file. A present-tense
sentence built on an inferred mark reads to a detached reader as verified fact, which is this
section's failure mode arriving by a different route. Where the mark was not proven, say so in the
block: *"the lane is documented as doing this; the run did not verify it."*

**When no lane carries it, the mark still wins.** Do not quietly switch the heading to the
conditional form — the footer would still show ✅ and the item would contradict itself, which
breaks the one thing rule 1 buys you. A served item whose capability cannot be traced to a lane is
a finding about the *core document*: either the coverage mark is wrong or the appendix is
incomplete. Write the block to the extent the inventory supports, say plainly which part is
unverified, and record the item under **What this pass noticed**. Then let the user decide.

That is the honest handling, and it is also the only one available: enrichment cannot edit the
core document, so a mark it disagrees with is something to report, never something to route
around.

**A ◐ item must say what is missing, not only what works.** It shares a heading with ✅ because
something genuinely runs, and that is where the two stop being alike: ◐ means *part* of the quoted
ask is served, and a block describing only the served part makes the whole ask sound answered. The
legend does not rescue it — `◐ partially served` says some unspecified portion, and the item is the
only place the portion can be named. So write both halves: what the lane returns today, and which
clause of the ask it leaves on the floor, taken from that lane's limits in Appendix A. Getting this
wrong turns the most informative mark on the page into the least.

The situation and the stakes are yours to write. The capability is not.

### Say once that the scenes are invented

The scenes are hypotheses about how the ask arises, and they should read well — a hedged scene is
useless. Handle it the way the rest of this skill handles the same problem: declare it once, in a
fixed place, in the vocabulary already in use. The header line is in the template below and the
skill's `observed` / `inferred` / `invented` marks are the vocabulary. If any scene *is* drawn from
something real — a ticket, a transcript, an incident — name it on that item, and the declaration
becomes the honest default rather than a blanket.

---

## What enrichment may touch

**It reads** the finished core document — the item tables, the coverage marks, and Appendix A — and
one line of its own previous output, the `**Topics:**` header, when re-enriching a subject it has
enriched before. Nothing else.

**It writes** a sibling of it, and optionally an artifact.

Take the core document's path from the run rather than assuming one. Phase 0 defaults to
`PERSONAS.md` at the repo root but explicitly gives way to a repo's own docs convention, so a real
run may have written `docs/platform-personas.md`. The enriched file is that path with `-enriched`
before the extension, in the same directory — `docs/platform-personas-enriched.md`. Hard-coding
`PERSONAS.md` here would send the pass to read a file that does not exist, or worse, a different
project's file that does.

**It changes nothing upstream.** Not an ask, not a coverage mark, not the tally, not a primitive.
The core document passed `--final` before this pass began and it must still pass afterwards,
unchanged. If enrichment convinces you an item is wrong, that is a real finding — say so at the
end of the enriched document and let the user decide whether to re-run. Editing the verified
document from a downstream pass silently un-verifies it.

This is the same containment Phase 3 works under, for the same reason: a pass that can reach
backwards will eventually be used to make the earlier work agree with it.

---

## The item entry

Four parts, in this order, for every item in the document. Not a selection of the interesting
ones — enriching forty of sixty makes the other twenty look rejected.

```markdown
#### 7 — "Give me a plain-English summary of everything we know about this host."

**The situation.** Every ticket the analyst opens starts the same way: fifteen minutes of
assembling one host out of six different screens, then retyping the useful parts into the ticket
so the next person does not have to repeat it.

**Why it matters.** This is the highest-volume work in the building and none of it is analysis —
it is transcription. The cost is not any single lookup; it is the same lookup performed several
hundred times a day across the desk.

**What would have to exist.** A surface that assembles the host across every lane at once and
returns prose rather than records: where it sits in the address hierarchy, who owns it, its DNS
records across all views, its lease state, when it last changed and by whom. Appendix A shows the
four lanes each hold a piece of this and none of them join.

`many/day` · ⚡ · ○ · topics: `identity`, `agent-surface`
```

**The situation** — the scene that produces the ask. Concrete, one short paragraph, no more than
about four sentences. It names a moment, not a category: *"a P2 ticket lands with nothing but an IP
in the subject line"* rather than *"analysts often lack context."* This is the invented part, and
it is invented deliberately — a generic situation persuades nobody and teaches nobody.

**Why it matters** — the pressure behind it, expanded from the core document's *Why* column. Not a
restatement of the situation. Name what goes wrong, to whom, at what scale, when the answer is not
available. The core document's `Today` column is the seed: *"greps four spreadsheets and guesses"*
is a cost, and this is where you say what that cost is.

**The third block** — titled by the coverage mark, per the rule above. For a served item, what
the answer looks like and which lane produces it. For an unserved one, what would have to exist for
the answer to be possible, in capability terms rather than feature terms — this is the same
distinction Phase 5 draws between a primitive and a feature name, applied one item at a time.
Where a primitive from the synthesis covers the item, name it by slug; that is what ties the two
halves of the document together.

**The footer line** — frequency, the frontier mark if the item carries one, the coverage mark, and
the topics. Everything here is copied from the core document except the topics.

At coverage depth **None** the core document has no coverage column, so the footer has no mark to
copy and simply omits it: `many/day · ⚡ · topics: …`. Do not write `○` there. `○` is a finding —
assessed and not served — and a run that never assessed anything has not earned it. The artifact
drops the coverage pill for the same reason, rather than showing an empty one.

---

## Topics

The second sort axis. Personas answer *who asked*; topics answer *what it is about*, and the two
cross — a persona's items scatter across topics, and a topic's items scatter across personas.
The crossing is the point: it shows which subject areas are demanded by people who have nothing
else in common, which is the item-level version of the signal Phase 5 looks for in primitives.

**Mint them here, at enrichment time.** They are presentation, not schema: they do not appear in
the core document, `verify.py` does not read them, and they are specific to one subject in a way
persona and primitive slugs are not. Every subject needs a different set — `DNS`, `DHCP`,
`security` for a DDI estate; `migration`, `error-paths`, `debuggability` for a library.

- **Six to ten of them.** Fewer and they do not separate; more and every item gets a private label
  and the axis stops grouping anything.
- **One to three per item, the first of them primary.** An item touching everything is usually an
  item phrased too broadly. The first topic listed is the one the item is *most* about, and it is
  what the artifact's per-persona bars are segmented by — a bar built from every label on every
  item would sum past the persona's item count and stop meaning anything. Filtering still matches
  on all of an item's topics; only the bar uses the primary.
- **Derived from the items, never from the subject's architecture.** Topics named after the
  subject's modules re-impose the supply side on a demand-side document, and the crossing goes
  flat because each persona maps to the module they use.
- **Recorded in the document header**, and read back from there. A later enrichment of the same
  subject reuses the recorded set rather than minting a synonym for a topic that already exists —
  the light-weight version of what `PRIMITIVES.md` does for primitive slugs, and it works because
  topics only ever have to be consistent within one subject.

  This is the one thing the pass may read besides the core document: **the `**Topics:**` line of
  its own previous output**, and nothing else in that file. Reading the prior enriched document's
  header is not contamination — it is this pass's own vocabulary, the way Phase 5 reads
  `PRIMITIVES.md` — but reading its *scenes* would anchor the new ones to the old, so do not.
  Without this the reuse rule cannot be satisfied at all: the topics live nowhere else, and every
  re-run would mint a fresh set and overwrite the file that held the last one.

---

## Document skeleton

```markdown
# <The core document's title> — the story behind each ask

_Enrichment of `<core document path>` (<date><, subject SHA `<sha>` — only if the core document
recorded one>). The core document is the record; this one expands it and changes nothing in it._

**The scenes are invented.** Each item's situation is a plausible reconstruction of how the ask
arises, not an observed incident — written concretely because a hedged scene teaches nothing.
Where a scene came from something real it says so on the item. Capability claims under
"How it's answered today" are held to Appendix A of the core document.

**Frequencies:** <copied verbatim from the core document's header — estimated, or observed from
SOURCE>.

**Coverage key:** <copied from the core document: ✅ served well today · ◐ partially served ·
○ not possible today.>

...or, on a run with no coverage pass, that line is *replaced* rather than deleted:

**Coverage:** not assessed — no coverage pass ran, so no item carries a mark. An absent mark here
means nobody looked, not that the ask is unserved.

Replaced, because a deleted line and an unassessed run look identical to a reader holding only
this file: no key, no pills, and no way to tell whether coverage was checked and omitted or never
checked at all. Silence is the one thing that cannot say which.

**⚡ marks the frontier** — <the frontier class for this subject, copied from the core document.
This line stays at every coverage depth: the frontier is a property of the items, not of the
coverage pass, so a depth-None run's footers carry ⚡ and need it explained.>

**Topics:** `<slug>` · `<slug>` · … <one line on what the axis is here>

**Carried from the core document's Verification section:** <the Phase 7b findings, verbatim or
tightly summarised, including the ones the run disagreed with and why it disagreed. Never dropped.>

That last block is not optional politeness. `--final` refuses to pass a document without a
Verification section, and what it holds is the adversarial reader's list of what is wrong: items
that would apply unchanged to any subject, personas indistinguishable by their asks, coverage marks
that read inferred. Enrichment then takes those exact items and writes them into their most
persuasive form. A standalone file that carries the scenes but not the warnings has inverted the
point of the phase that produced them.

---

## P1 — <Role>

<One line: what this persona's items are about, taken as a group. The thing visible from their
seven items together that no single one shows.>

#### 1 — "<the ask>"
…

---

## What this pass noticed

<Optional, and only if it did. Items whose Why looked thin once expanded, two asks that turned out
to be the same ask, a coverage mark that looks wrong on closer reading. Findings, not edits — the
core document is not changed here. If the pass noticed nothing, delete this section rather than
padding it.>
```

The per-persona opening line is worth the effort. Writing sixty scenes surfaces things invisible
row by row, and that line is where they land.

---

## The artifact

The markdown is the deliverable and the source of truth. The artifact is an offer — ask once, and
take a decline as final for the run.

It is worth offering because this document is read by *browsing*, and markdown is bad at browsing:
sixty expanded items is a very long file, and the reason to have topics at all is to filter and
regroup, which a static file cannot do.

Structure, in order:

1. **Header** — the question as the title, one paragraph on how to read the page, and one line on
   what the frontier mark means for this subject.
2. **The honesty note, the `**Frequencies:**` line, the coverage key, and the carried Verification
   findings**, all from the markdown header and all in full. They are more necessary here, not less: the artifact is the version that
   gets shared onward, detached from this conversation and from the core document. Every card shows
   a frequency pill, and `many/day` on sixty cards reads as measurement unless the page says
   otherwise once — and a reader who cannot tell ◐ from ○ cannot read the coverage pills at all.
3. **Topic chips** — click to filter. `n of N` visible.
4. **Topic mix by persona** — one stacked bar per persona, segmented by each item's **primary**
   topic, with the item count. Primary, because items carry up to three topics and a bar counting
   all of them exceeds the persona's item total; segmenting on the primary keeps the bar summing to
   the number printed beside it. This is the crossing made visible, and it is the one view that
   justifies the format: it answers "who is this document actually about" in a glance.
5. **Persona sections** — the roster's order and the roster's uneven counts. Each item a card:
   number, ask, the one-line why, then frequency / frontier / coverage / topic pills, then the
   three blocks, collapsible and collapsed by default.
6. **The synthesis, collapsed** — the primitives and "if you only ask for three", carried over from
   the core document. Collapsed because the items are what this page is for.
7. **A dated source line** — what this is, what it was generated from, and when.

Where there are coverage marks, keep them visible on every card. The mark is what tells a reader
which third-block form they are reading, and a filtered view that hides it turns the page back into
a case study. A depth-**None** run has no marks and shows no pills — and carries the header's
**Coverage: not assessed** line to say so, for the same reason the markdown replaces that line
instead of dropping it. This is the copy most likely to reach someone who never saw the core
document, so an absence here has to be labelled or it will be read as a finding.

Write it as a single HTML file beside the markdown, named the same way — `<core>-enriched.html`
next to `<core>-enriched.md`. Naming it deterministically is what makes a re-run replace the page
rather than leave a second one beside it, and what lets someone find it later without asking which
run produced it.

The page must be **self-contained**: styles and behaviour inline, no external assets. Filtering and
collapsing are the only interactions it needs, and both are a few lines of vanilla JavaScript.
Where the environment can publish an artifact, publish that same file rather than building a
different one — one page, one source, and the local copy survives whether or not publishing does.
