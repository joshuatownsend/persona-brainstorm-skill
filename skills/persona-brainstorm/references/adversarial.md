# Adversarial — what they can't stand about it

Read this when the user asks for an adversarial pass. `SKILL.md` § Optional passes carries the
rules that decide *whether* to run one — including the precondition this pass has and enrichment
does not: **it requires coverage depth Full or Light.** Everything below assumes an Appendix A
exists to cite. This file is the format.

The core document asks what people would want. That framing is generative and it has one blind
spot: **nobody phrases a grievance as a wish.** An engineer who stopped trusting the lease view
after it lied to them during an incident does not turn up in Phase 2 asking for a trustworthy lease
view. They turn up asking for something else entirely, or not at all, because they have quietly
routed around the feature and no longer think of it as part of the system.

This pass collects what the wish frame cannot reach: what each persona **dislikes, distrusts, works
around, or believes they should be able to do and can't.**

---

## The distinction the whole pass rests on

The core document already records what is missing. The `Today` column says what a persona does
instead — *"greps four spreadsheets"*, *"asks Dave"*, *"gives up"* — and the coverage column marks
what is unserved. Run without care, this pass regenerates that list in an irritated tone and adds
nothing.

The line is sharp, and it is worth stating twice because everything below depends on it:

- **`Today` and `○` are about absence.** There is no answer, so the persona does something else.
- **A grievance is about presence.** There *is* something, and it is wrong, slow, misleading,
  refusing, or surprising. The persona has used it and come away worse off than if they had not.

Absence is disappointing. Presence done badly is corrosive, because it costs trust as well as time
— and trust, once spent, does not come back when the feature is fixed. That is why this pass finds
things the core document structurally cannot.

### The gate that enforces it

**Every grievance names the thing it is about, and that thing must exist in Appendix A.** Cite the
lane. If you cannot — if the complaint is that some capability simply is not there — it is not a
grievance. It is an unserved ask, it already belongs in the core document, and writing it here
duplicates the page in a worse voice.

This is mechanical on purpose, for the same reason enrichment derives its headings from coverage
marks: a distinctness rule that depends on judgment gets applied loosely by the third persona, and
the failure is invisible in the output because a well-written duplicate reads fine.

**The one exception is the expectation gap**, below, which names a promise rather than a lane.

---

## The five kinds

Reach along all five. The first two are what people volunteer; the last three are where the pass
earns its keep, and a document with none of them has stopped at grumbling.

1. **It's wrong.** The answer is stale, partial, or misleading — and the persona cannot tell from
   the answer itself which. This is the most damaging kind and the least reported, because someone
   who has been burned once stops using the feature rather than filing anything.
2. **It's expensive.** It works, and the cost of getting to it — clicks, waits, context switches,
   asking someone — exceeds what the answer is worth. Watch for the persona who has automated their
   way around a feature: that automation is a filed complaint nobody read.
3. **It refuses.** Permissions, scope limits, rate caps, an export that stops at 1,000 rows. Note
   whether the refusal is deliberate and whether the persona knows it is — a limit nobody explained
   reads as a bug and gets escalated as one.
4. **It surprises.** The behaviour is defensible and does not match what any reasonable person
   would expect. These produce the support load that never shows up as a feature request, because
   the persona concludes they are holding it wrong.
5. **The expectation gap** — *"I should be able to do this."* Not "I wish I could": a belief that
   the capability is owed. This is the richest kind and the reason the pass is worth running.

   Where the belief comes from is the finding, not the belief itself. Something *created* it — the
   marketing page, an adjacent feature that works this way, a competitor, a docs sentence written
   optimistically, the name of the button. A persona expecting something you never promised is a
   misunderstanding; a persona expecting something the product *implied* is a defect in the
   product's story about itself, and nothing else in this method detects one.

   This is the only kind that may cite a promise instead of a lane — name the promise and where it
   is made. An expectation traced to nothing is a preference, and it goes in the core document as
   an ask.

---

## Every grievance is marked for evidence

Use the same vocabulary Phase 5 uses for primitives: `observed`, `inferred`, `invented`, with a
source named for the first two.

The stakes are higher here than anywhere else in this method, and it is worth being blunt about
why. A primitive marked `invented` is an idea nobody has evidence for. **A grievance marked
nothing is an accusation** — it asserts that real people are unhappy with a real thing, in their
voice, in a document that will be read by whoever owns that thing. Invented dissatisfaction
presented as observed dissatisfaction is not a documentation flaw; it is a false report about
people who did not say it, and it is used to make decisions about their work.

So:

- `observed` — a ticket, a transcript, a support thread, a recorded complaint. Name it.
- `inferred` — reasoned from something real one step away: a workaround that exists, an
  automation someone wrote, a documented limit, a lane's own caveat. Name that too.
- `invented` — a plausible reconstruction of how this lane would frustrate this persona. Honest,
  useful, and not a lesser mark. Most grievances in a first pass are this.

**A run whose grievances are all `invented` is a hypothesis list, and the document says so in its
header rather than in a footnote.** That framing is the difference between a page that starts a
conversation with the people who own the subject and a page that ends one.

---

## The roster is the one you already approved

Reuse it. Same personas, same slugs, same order.

Do not derive a new roster and do not add a persona here. The Phase 1 gate exists because the user
is the participant with real domain knowledge, and a roster that grows during an optional pass has
skipped that gate. If the pass makes you certain a persona is missing, that is a finding about the
core document — say so, and let the user decide whether to re-run.

**There is no budget, and the counts will be lopsided.** A persona who lives in the subject daily
has many grievances; one who touches it quarterly may have none, and *none* is a real result worth
writing down. Manufacturing a complaint to fill a row is the same failure as padding items to hit
a budget, with the added cost that this one puts words in a person's mouth.

Where a persona has nothing, say what that means. Rarely-touched surfaces are not necessarily good
— sometimes nobody complains because nobody has got far enough in to be disappointed.

---

## The entry

```markdown
#### P2-3 — "I stopped trusting the lease view after it told me an address was free during an
incident."

**About:** Lane B — the DHCP lease read. *(inferred: Caveat 2 in Appendix A records the lane's
staleness window; the incident is a reconstruction of what that window costs.)*

**Kind:** it's wrong.

**What they expected.** That a lease shown as expired was expired at the moment they looked, or
that the view said how old it was.

**What it costs.** They now confirm every lease against the server directly, which takes four
minutes and requires access half the desk does not have. The feature still exists, is still
maintained, and has one user fewer. Nobody filed anything — the view was not broken enough to
report, only enough to abandon.

**What would fix it.** Not a new capability: a timestamp on the answer. The staleness is
acceptable; the silence about it is not.
```

Number them per persona (`P2-3`), not continuously. This document is read by persona and has no
tally, so a continuous sequence would only invite comparison with the core document's numbering,
which it deliberately does not share.

**The complaint, in their words** — a quoted sentence, held to the same standard as an ask. If it
reads like a bug title, rewrite it. *"The export silently stops at a thousand rows"* is a defect
report; *"I don't know whether I've got everything, so I run it twice and diff"* is a person.

**About** — the lane, and the evidence mark. Never neither: the lane is what makes it a grievance
rather than a duplicate, and the mark is what makes it a report rather than an assertion. For an
**expectation gap** the lane is replaced by the promise and where it is made — that kind exists
precisely because the implied capability has no lane, so requiring one would force a fabricated
citation or drop the most valuable entries on the page. Every other kind names a lane.

**Kind** — one of the five. If it takes two, it is probably two grievances.

**What they expected** — the mental model the behaviour violates. This is what separates a
grievance from a complaint: the gap between expectation and behaviour is the actionable part, and
sometimes the cheaper fix is on the expectation side.

**What it costs** — time, trust, escalation, or abandonment. Abandonment is the one to watch for:
a feature with a maintenance cost and no users left is worse than one that was never built.

**What would fix it** — kept deliberately small. This is not the primitives section; most
grievances are fixed by a timestamp, an error message, a documented limit, or a raised cap. Where
one genuinely needs a capability, name the primitive by its slug from the core document's
synthesis. If several grievances converge on the same primitive, that is the strongest thing this
pass can find — say so at the end.

---

## Document skeleton

```markdown
# <The core document's title> — what they can't stand about it

_Adversarial pass over `<core document path>` (<date>). Reads that document and its appendix;
changes nothing in it._

**These are hypotheses unless marked otherwise.** Each grievance carries an `observed`, `inferred`
or `invented` mark. <If all of them are invented, say so here in one sentence: this is a list of
ways the subject would plausibly frustrate these personas, not a report of complaints anyone made.>

**Coverage depth:** <Full or Light, copied from the core document — Light marks were not verified,
so a grievance resting on one rests on an unverified reading of the lane.>

**Carried from the core document's Verification section:** <the Phase 7b findings, including the
ones that the run disagreed with. Never dropped — the personas here are the ones that section may
have questioned.>

<Those two lines are what the shared provenance rule comes to for this pass. It carries no
frequency, coverage or frontier marks on its entries, so the corresponding legends stay behind:
what travels is what the output actually rests on, which here is the depth the lane marks were
assessed at.>

---

## P2 — <Role>

<One line on what this persona's grievances have in common, if anything. "All four are about not
being able to tell how old an answer is" is a finding; four unrelated complaints are four
complaints.>

#### P2-1 — "<the complaint>"
…

---

## What this pass found

**Grievances that converge.** <Where several personas complain about the same lane, or several
complaints resolve to the same primitive. This is the section a reader acts on.>

**Personas with nothing.** <Who had no grievances, and what that means — unused, or genuinely
well served.>

**What it says about the core document.** <Findings only, never edits. A coverage mark this pass
doubts, a persona that looks missing, an ask that turns out to be a grievance in disguise.>
```

---

## The artifact

Offered once, and declining changes nothing else — the markdown is the deliverable either way.
A single self-contained HTML file beside the markdown and named the same way,
`<core>-adversarial.html`: styles and behaviour inline, no external assets. Where the environment
can publish an artifact, publish that same file rather than building a different one. Naming it
deterministically is what makes a re-run replace the page instead of leaving a second one beside
it.

Two things must be visible on every card and must survive filtering: **the evidence mark** and
**what the grievance is about** — the lane, or for an expectation gap the promise it cites. A page
of grievances with the marks hidden is a page of assertions about real people's opinions, and it is
the copy most likely to be read by whoever owns the subject.

Carry the header's **coverage depth** line and the **Verification findings** onto the page too.
Those are what this pass relies on from the core document; it shows no frequency, coverage or
frontier marks per entry, so those legends would be noise rather than provenance.

Group by persona, filter by kind. The kind filter is the one worth having: reading all the
*it's wrong* complaints together, across personas, is how a trust problem becomes visible as one
thing rather than five.
