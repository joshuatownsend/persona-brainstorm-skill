# Enrichment — the story behind each item

Read this when the user asks for an enrichment pass. `SKILL.md` § Optional passes carries the rules
that decide *whether* to run one; this file is the format.

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
| ✅ or ◐ | **How it's answered today** | present tense — describes something that runs |
| ○ | **What would have to exist** | conditional — describes something that does not |

At coverage depth **None** there are no marks, so **every** item takes the second form. A run with
no inventory cannot describe how anything is answered, and reaching for the first form there is
the failure this table exists to prevent.

This is deliberately mechanical. A heading derived from a mark cannot drift the way a judgment
call does, a reader can tell the two forms apart at a glance without trusting you, and a checker
can verify it later with a join on the item number. A disclosure paragraph at the top of the
document achieves none of those things.

### A served item may only claim what the inventory records

The heading rule stops the crudest failure — past tense on an unserved item. It does not stop the
subtler one, which is **invented specificity on a served item**: a plausible number, a named field,
a duration, a sequence of events, all reading as observation because they are too particular to be
anything else.

So: in a **How it's answered today** block, every capability claim must trace to something Phase 3
actually found, and the block names the lane from Appendix A that carries it. If you cannot name
the lane, the item does not get that heading — it drops to **What would have to exist**, which is
an honest description of a capability nobody has verified.

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

**It reads** the finished `PERSONAS.md` — the item tables, the coverage marks, and Appendix A.

**It writes** `PERSONAS-enriched.md`, beside the core document, and optionally an artifact.

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
- **One to three per item.** An item touching everything is usually an item phrased too broadly.
- **Derived from the items, never from the subject's architecture.** Topics named after the
  subject's modules re-impose the supply side on a demand-side document, and the crossing goes
  flat because each persona maps to the module they use.
- **Recorded in the document header.** A later enrichment of the same subject reuses the recorded
  set rather than minting a synonym for a topic that already exists — the light-weight version of
  what `PRIMITIVES.md` does for primitive slugs, and it works because the topics only ever have to
  be consistent within one subject.

---

## Document skeleton

```markdown
# <The core document's title> — the story behind each ask

_Enrichment of `PERSONAS.md` (<date>, subject SHA `<sha>`). The core document is the record; this
one expands it and changes nothing in it._

**The scenes are invented.** Each item's situation is a plausible reconstruction of how the ask
arises, not an observed incident — written concretely because a hedged scene teaches nothing.
Where a scene came from something real it says so on the item. Capability claims under
"How it's answered today" are held to Appendix A of the core document.

**Topics:** `<slug>` · `<slug>` · … <one line on what the axis is here>

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
2. **The honesty note from the markdown header**, in full. It is more necessary here, not less:
   the artifact is the version that gets shared onward, detached from this conversation.
3. **Topic chips** — click to filter. `n of N` visible.
4. **Topic mix by persona** — one stacked bar per persona, segmented by topic, with the item count.
   This is the crossing made visible, and it is the one view that justifies the format: it answers
   "who is this document actually about" in a glance.
5. **Persona sections** — the roster's order and the roster's uneven counts. Each item a card:
   number, ask, the one-line why, then frequency / frontier / coverage / topic pills, then the
   three blocks, collapsible and collapsed by default.
6. **The synthesis, collapsed** — the primitives and "if you only ask for three", carried over from
   the core document. Collapsed because the items are what this page is for.
7. **A dated source line** — what this is, what it was generated from, and when.

Keep the coverage mark visible on every card. It is what tells a reader which of the two third-block
forms they are reading, and a filtered view that hides it turns the whole page back into a
case study.

The page must be **self-contained**: styles and behaviour inline, no external assets. Filtering and
collapsing are the only interactions it needs, and both are a few lines of vanilla JavaScript.
