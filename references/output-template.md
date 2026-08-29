# Output template

The structure below is what the document should look like. Adapt headings to the domain; keep the
order, because it encodes the argument: *frame → who → what they want → what exists → what it
means*. Putting coverage earlier makes readers grade the ideas instead of reading them.

Replace every `<>` placeholder. If no coverage pass ran, delete the coverage column, the coverage
key, and the appendix — the document still stands on the items and the synthesis. **Keep a tally
line**, reduced to the part that is always true:

```
**Tally:** <d> ⚡
```

The frontier count exists whether or not anything was graded, and the tally line is the only place
a claimed figure may live, so deleting it outright leaves the checker with nothing to compare.

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

**Frequencies:** <estimated from the personas, not measured — or: observed from SOURCE>.
**Roster axis:** <job role / job-to-be-done / relationship to the subject — plus any persona
deliberately off that axis, and why>.
**Pre-registered:** <predicted a/b/c as item counts, not percentages — or, with no coverage
pass, predicted N ⚡ · surprise
threshold · cut: the rule you set in Phase 0>.
**Load-bearing persona:** <P-number and name — the one whose non-existence would take the most items with it>.

---

## Personas

<Count.> <One or two sentences on what you did to the seed list: which were merged and why, which
were added and why. Then:> Item counts are deliberately uneven — they track <what drives volume and
value for this subject>, not fairness.

| # | Slug | Persona | Why they're here | Items |
|---|---|---|---|---|
| **P1** | `<kebab-slug>` | <Role> | <One line. The justification for being on the page — not a job description.> | <n> |

---

## The <N>

### P1 — <Role>

| # | The ask, in their words | Why — the decision it feeds | Today | Freq | ⚡ | Cov |
|---|---|---|---|---|---|---|
| 1 | "<A sentence they'd say out loud.>" | <The job the answer does.> | <What they do instead now.> | <many/day> | <⚡ or blank> | <✅> |

<Repeat per persona. Number items continuously across the whole document.>

**Tally:** <a> ✅ · <b> ◐ · <c> ○ · <d> ⚡

<One sentence naming the ratio as the finding.>

---

## What the <N> imply: <M> capability primitives

The items are evidence; these are the deliverable. Each primitive is a capability <the subject>
would need, derived from the items that demand it.

1. **<Primitive name>** `<kebab-slug>` — <one line on what it is, in plain terms>.
   → items <n, n, n>. <Why it matters; note if several unrelated personas demand it.>

### If you only ask for three

**<A>**, **<B>**, and **<C>** — in that order. <The reasoning for the ranking: unique value,
size of evidence cluster, cheapness of unlock. Name any primitive cheap enough to ride along
with whatever ships first.>

**Reckoning:** <predicted a/b/c, actual x/y/z as counts — or predicted N ⚡, actual M ⚡ — what the gap
means, and which of the three cases
this is: the prediction held and taught you nothing, the surprise threshold was crossed and the
frame is in doubt, or it moved within the threshold and the direction is all you should claim.>

<Name the falsifier for the top primitive — the one observation that would show it is wrong. Then
restate the load-bearing persona and what goes with it if that persona is fictional.>

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
- **The tally line is the only place a claimed figure may live.** `scripts/verify.py` reads counts
  from there and nowhere else, deliberately: a document legitimately discusses numbers — quoting a
  figure that turned out wrong, citing a prior run — and a checker that scans prose will read that
  discussion as the document's own claim. One home, one address.
- **Slugs are for comparing runs, not for reading.** Give each persona and each primitive a stable
  kebab-case slug and keep it identical across re-runs of the same subject. Item numbers are
  positional and change freely; slugs are what let two runs be compared when every sentence has
  been reworded.
- **The ⚡ column is structural, not decorative.** Marking the frontier inside the ask sentence
  makes it uncountable, which is exactly how a wrong frontier count once went unnoticed.
- **The Today column is the demand-side measure; the coverage column is not.** Coverage says
  whether you serve the ask. Today says whether anyone needs it served — an unserved ask somebody
  already pays a person to work around is an opportunity, and one nobody has ever attempted is
  usually a non-problem. Fill it in even when the answer is "nothing" or "doesn't know to ask",
  because those two are the most informative values it takes.
- **A pre-registration written afterwards is not one.** The predicted split has to be recorded
  before any item exists, and the Reckoning line has to sit in the synthesis whether or not the
  news is good. A run where the prediction held is a run that confirmed a prior, and saying so is
  the finding.
- **Declare the frequencies and the roster axis in the header, not in prose further down.** Both
  are claims a reader will otherwise take on trust: the frequency column reads as measurement, and
  a roster mixing axes cannot be checked for completeness.
- **Say which coverage marks were proven and which were inferred** if you ran a scoped Full pass.
  A column that silently mixes verified and best-effort marks is worse than one that admits it.
- **Bold the item numbers you cite** in the primitives section only if the document is long enough
  that readers will jump; otherwise plain is fine.
- **Keep the appendix genuinely demoted.** If it grows past about a quarter of the document, it's
  competing with the brainstorm — move detail into the linked issue writeups.
- **Link filed issues inline** so the caveats stay actionable after the document ages.
