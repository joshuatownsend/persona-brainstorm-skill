# Output template

The structure below is what the document should look like. Adapt headings to the domain; keep the
order, because it encodes the argument: *frame → who → what they want → what exists → what it
means*. Putting coverage earlier makes readers grade the ideas instead of reading them.

Replace every `<>` placeholder. If no coverage pass ran, delete the coverage column, the coverage
key, the tally, and the appendix — the document still stands on the items and the synthesis.

---

```markdown
# <The question, as a sentence — not a noun phrase>

_Brainstorming session. <Pass 1: date — one-line note. Delete this line if no supply-side pass
ran; a single-pass run is just "Session: <date>".>
Pass 2: <date> (demand-side — this document)._

## <What changed between the passes / Why this document is shaped this way>

<If there was no earlier pass, drop the "what changed" framing and keep only the frame paragraph
plus the note that coverage never gated membership.>

<Two short paragraphs. State the frame and its scope constraint. If an earlier pass filtered by
current coverage, say so and say why that was the wrong test: it deletes exactly the ideas worth
having. Say explicitly that coverage survives as a demoted annotation and never decided
membership, and that the unimplemented items are the point. Without this, a later reader will
promote coverage back to a filter.>

**Coverage key:** ✅ served well today · ◐ partially served / needs a real primitive · ○ not
possible today. **⚡ marks the frontier** — <one line on what the frontier class is here>.

---

## Personas

<Count.> <One or two sentences on what you did to the seed list: which were merged and why, which
were added and why. Then:> Item counts are deliberately uneven — they track <what drives volume and
value for this subject>, not fairness.

| # | Persona | Why they're here | Items |
|---|---|---|---|
| **P1** | <Role> | <One line. The justification for being on the page — not a job description.> | <n> |

---

## The <N>

### P1 — <Role>

| # | The ask, in their words | Why — the decision it feeds | Freq | Cov |
|---|---|---|---|---|
| 1 | "<A sentence they'd say out loud.>" | <The job the answer does.> | <many/day> | <✅> |

<Repeat per persona. Number items continuously across the whole document.>

**Tally:** <a> ✅ · <b> ◐ · <c> ○. <One sentence naming the ratio as the finding.>

---

## What the <N> imply: <M> capability primitives

The items are evidence; these are the deliverable. Each primitive is a capability <the subject>
would need, derived from the items that demand it.

1. **<Primitive name>** — <one line on what it is, in plain terms>.
   → items <n, n, n>. <Why it matters; note if several unrelated personas demand it.>

### If you only ask for three

**<A>**, **<B>**, and **<C>** — in that order. <The reasoning for the ranking: unique value,
size of evidence cluster, cheapness of unlock. Name any primitive cheap enough to ride along
with whatever ships first.>

### Two observations worth carrying

- **<Which persona the current framing under-serves>** — <why, and what it would cost to fix>.
- **<Where the clearest whitespace is>** — <coverage vs. willingness to pay>.

---

## Appendix A — Current coverage (verified <date>)

_This is the supply-side mapping, retained because <reason>. It describes what <the subject> does
today; it does **not** bound the brainstorm above._

### The <N> lanes in <the subject> today

| Lane | Surface | Notes |
|---|---|---|
| **A — <name>** | <how it's reached> | <real limits: caps, staleness, what it refuses> |

### Caveat 1 — <the defect, stated as a claim>

<What's wrong, with file:line evidence. What an operator should do until it's fixed. Link the
full writeup if you filed one.>

### Caveat 2 — <staleness or equivalent>

<Why it matters for the items above, not just in the abstract.>
```

---

## Notes on filling it in

- **The title is a question**, and the scope constraint belongs in it. "What DDI people would read
  from an IPAM estate, if a read-only interface could answer anything" does more work than "BAM
  personas"; "What a consumer would want from a date library without reading its source" does more
  work than "date-lib personas".
- **Name the archetype and its frontier class** in the opening section, matching what you picked in
  Phase 0. The `⚡ marks the frontier` line is not boilerplate — it says which class of ask this
  particular subject makes hard and valuable, and a reader who doesn't know it will misread every
  ⚡ row as wishful thinking.
- **Say which coverage marks were proven and which were inferred** if you ran a scoped Full pass.
  A column that silently mixes verified and best-effort marks is worse than one that admits it.
- **Bold the item numbers you cite** in the primitives section only if the document is long enough
  that readers will jump; otherwise plain is fine.
- **Keep the appendix genuinely demoted.** If it grows past about a quarter of the document, it's
  competing with the brainstorm — move detail into the linked issue writeups.
- **Link filed issues inline** so the caveats stay actionable after the document ages.
