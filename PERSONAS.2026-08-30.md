# What someone would want from a demand-side discovery method, if it could do anything — given an AI agent with no domain expertise executes it

_Brainstorming session. Pass 1: 2026-08-28, subject SHA `a02419d` — preserved unchanged at
`PERSONAS.md`.
Pass 2: 2026-08-30, subject SHA `3dd6fb2` (comparison re-run — this document)._

## Why this document is shaped this way, and what changed since pass 1

The subject is **not** this repository. It is *a generic capability for turning any subject into
the set of user needs it should serve* — demand-side discovery as a category. This repo is merely
where the evidence lives and where the file lands. Naming the repo as the subject would have
produced a bug list about `SKILL.md`; naming the category produced a wish list that is mostly
unbuildable, which is the point.

The frame carries one deliberate scope constraint: **the method is executed by an AI agent with no
domain expertise of its own.** Not facilitated by a trained researcher in a room with sticky notes
— carried out by a language model that has never worked in the user's field, cannot talk to real
users, and may be wrong without knowing it.

**This is a comparison re-run, not a reframe.** Every Phase 0 input is identical to pass 1 —
subject, frame, scope constraint, item budget of 60, Library/SDK archetype, coverage depth. That is
what `references/cross-run.md` requires before two runs may be compared at all; change the frame and
every difference downstream is confounded by that change. The roster and all 60 items were
regenerated from scratch by agents that had never seen pass 1's document, because a previous
document anchors exactly as an inventory does.

**Coverage never gated membership.** An item earned its place by being something a real person
would genuinely say, never by being implementable. The coverage column was filled in afterwards,
against an inventory built afterwards, and nothing was reordered, reworded or dropped as a result.
Twenty-one of the sixty cannot be served at all today and thirty more only partly — two different
claims that this document keeps apart, because Appendix C shows many partial marks mean *the rule
exists but ships as a warning nobody runs*, which is an enforcement gap rather than a missing
capability. That split is the finding, not a defect in the list — a document where everything was
already covered would have failed. A later reader who "helpfully"
promotes coverage back into a filter will delete exactly the items worth having.

**Contamination disclosure.** The operator of this run had read the whole of `SKILL.md` before
Phase 0 — unavoidable here, because when the subject *is* the method, "don't read the
implementation" and "read the protocol" point at the same file. So Phases 1 and 2 were run as two
separate blind calls that shared no context with the operator and were forbidden to read any file,
receiving only a context block of Phase 0 decisions plus the protocol restated inline. Phase 3 ran
concurrently and **nothing from it reached either generating prompt.** This pushes the contamination
back; it does not remove it. The frame is still the operator's, and the frame shapes everything
downstream.

**Method drift is a live confound in this comparison.** Between the two passes the subject's
implementation gained the enrichment pass, the adversarial pass, three reference files and a
1,845-line checker — 17 commits. So some movement below is the world changing and some is the method
changing, and where the two cannot be separated this document says so rather than letting the reader
assume it is all real.

**Archetype: Library / SDK.** A method is loaded and executed by another system, so it inherits
library concerns — version skew, error paths, extension points, debuggability, the escape hatch.
**⚡ marks the frontier**, which for this archetype is *migration and failure injection*: "what
breaks if I upgrade", "make it fail the way production does", "show me this method's blind spot
before I trust it."

**Coverage key:** ✅ served well today · ◐ partially served, or served by a primitive that doesn't
quite fit · ○ not possible today.

**Frequencies:** estimated from the personas, not measured.
**Roster axis:** relationship to the method — each persona is a distinct position around the method's lifecycle, and the executing agent is a native position on that axis rather than an off-axis exception.
**Pre-registered:** predicted 12/24/24 of 60 · surprise above 30 ✅ · cut: the Why restates the Ask, or the ask reads unchanged for any other method-shaped subject.
**Load-bearing persona:** P1 — one-shot-operator.

No interviews, tickets, logs or analytics sit behind any value in the frequency column; treat every
one as a hypothesis about cadence rather than an observation of it. The same holds for the asks
themselves — they are what these personas would plausibly say, not transcripts of anyone saying it.

---

## Personas

Nine, derived blind from the frame alone and approved at the Phase 1 gate with one change considered
and declined: P1 was flagged by the deriving agent as possibly two people — the subject owner who
has domain knowledge but cannot judge the method, and the operator who knows the method but not the
domain — and held as one so the Phase 2 distinctness test could decide rather than a hunch. That
test did not fire, which the Verification section below establishes is **not** evidence of
distinctness: Appendix C records that distinctness is deliberately unchecked because a lexical
version scored true duplicates lowest, and Phase 7b went on to find that P7 is P1 at a later
timestamp and that P8 carries one distinct ask across three rows. The roster below is the approved
one and it has a known duplication defect. Item counts are deliberately uneven — they track how much contact each
position has with the method and how much rides on the answer, not fairness.

| # | Slug | Persona | Why they're here | Items |
|---|---|---|---|---|
| **P1** | `one-shot-operator` | The person who points the method at their own subject, once | Highest volume, lowest expertise: owns the subject but has no research training, so cannot tell a roster that is true from one that is merely plausible — and has no way to work around a bad fit. | 14 |
| **P2** | `executing-agent` | The AI agent that carries out the method | The method's only executor and its only evidence source. Generates asks no human persona will: what must I read before I act, what am I entitled to assert, when do I stop. | 11 |
| **P3** | `method-adapter` | The repeat user who tunes, forks, or upgrades the method | Runs it across many subjects, so hits version skew and comparability first. Carries most of the ⚡ migration asks, the extension points, and the escape hatch. | 8 |
| **P4** | `pipeline-integrator` | The program or agent that calls the method as a step | Asks in a different shape entirely — determinism, stable schema, freshness, budget caps, failure signalling — and none of it appears if you only imagine a human reading the result. | 6 |
| **P5** | `accountable-sponsor` | The decision maker who never runs it, only ships its output onward | Must defend the roster to people who weren't there, so needs provenance and confidence rather than prose. Also carries the rare-but-high-stakes contact: the bet-the-year run, the post-mortem after a launch failed. | 6 |
| **P6** | `conscripted-operator` | The person made to run it by a mandate, standard, or vendor change | Never chose the method; asks about cost, exit and proof-of-worth rather than insight. A roster built from volunteers contains none of them. | 5 |
| **P7** | `lapsed-operator` | The person who ran it once, got a horoscope, and never came back | Files no ticket and answers no survey. Without them the roadmap optimises for survivors and calls it demand. | 4 |
| **P8** | `described-cohort` | The people the output claims to speak for, who were never asked | The only persona *subjected to* the method rather than using it. Carries the asks about being asserted into existence, caricatured, or never generated at all. | 3 |
| **P9** | `assurance-reviewer` | The security, privacy, or compliance reader | What evidence went in, what is retained, whether the output makes claims about identifiable people or encodes a protected-class proxy. Answerable from what exists; nobody has asked. | 3 |

---

## The 60

### P1 — The person who points the method at their own subject, once

| # | The ask, in their words | Why — the decision it feeds | Today | Freq | ⚡ | Cov |
|---|---|---|---|---|---|---|
| 1 | "Would this exact same list come out if you'd run it on any other tool in my category?" | Whether the roster is worth acting on at all — one that fits everything directs nothing | Reads it, nods, can't tell | per-run |  | ◐ |
| 2 | "Which of these people did you actually find in what I gave you, and which did you make up?" | Splits what can be cited in Monday's planning meeting from what has to be verified first | Assumes all of it is grounded | per-run |  | ◐ |
| 3 | "I gave you a README and nothing else — is that enough to do this honestly?" | A roster built on one thin doc reads identically to one built on ten; without a floor they ship the thin one | Runs it anyway | per-run |  | ○ |
| 4 | "Who's missing from this list?" | Sizes the negative space — the unlisted user is the one discovered later through support tickets | Nothing — doesn't know it's answerable | per-run |  | ✅ |
| 5 | "It used a word nobody in my industry actually says — did it get my domain wrong, or just the vocabulary?" | Decides whether to bin the whole roster or fix a label; fluent wrongness looks exactly like expertise | Shrugs and edits the word | per-run |  | ○ |
| 6 | "How do I tell it the three things about my org that make the obvious answer wrong?" | Gets the local constraint in before generation instead of hand-correcting nine personas after | Pastes a paragraph and hopes | per-run |  | ◐ |
| 7 | "Which two of these nine do I cut? I can only build for three." | Forces a ranking — unranked, the team builds for the average of nine people and serves none | Picks the ones they already believed | per-run |  | ◐ |
| 8 | "Show me the one persona that would change my roadmap if it turned out to be real." | Aims the single verification they have budget for at the row that actually moves money | Verifies none of them | quarterly |  | ✅ |
| 9 | "You wrote that they 'want confidence in the output' — what would one of them actually type?" | Abstractions can't be built against or tested; the sentence can | Writes a ticket with the abstraction still in it | per-run |  | ✅ |
| 10 | "Show me where you just handed my own feature list back to me with faces on it." | A roster derived from the product can only ever confirm the roadmap — and it's invisible to someone who wrote that product | Doesn't notice it happened | per-run | ⚡ | ◐ |
| 11 | "If I run this again next week, do I get these nine people or a different nine?" | Whether one run is a finding or a sample of size one | Never runs it twice | per-run |  | ◐ |
| 12 | "What's the cheapest thing I could do tomorrow to prove one of these wrong?" | Turns a document into an experiment; with no cheap test the roster is never checked against a living person | Gives up | onboarding |  | ◐ |
| 13 | "I don't have any users yet — is it inventing them because I asked, or because they're really there?" | Pre-launch, a fabricated market read as evidence of demand funds a product nobody wanted | Takes the output as validation | onboarding |  | ◐ |
| 14 | "Where in this document am I supposed to disagree with you?" | Untrained readers have no other entry point into a confident document; a seamless one gets accepted whole | Accepts all of it | per-run |  | ◐ |

### P2 — The AI agent that carries out the method

| # | The ask, in their words | Why — the decision it feeds | Today | Freq | ⚡ | Cov |
|---|---|---|---|---|---|---|
| 15 | "What am I required to read before I'm allowed to name a single persona?" | Without a floor, a roster named off the title alone is indistinguishable from one built on the whole corpus | Reads whatever happens to be in context | per-run |  | ✅ |
| 16 | "Which of these claims am I entitled to assert, and which have to carry 'inferred'?" | Unmarked inference is quoted downstream as observed fact — the reader has no way to tell them apart | Writes everything in one flat voice | per-run |  | ◐ |
| 17 | "How do I mark 'the source said this' apart from 'models like me always say this'?" | The prior is the executor's dominant failure mode and it is completely invisible in fluent prose | No such distinction exists in the output | per-run |  | ○ |
| 18 | "What tells me this roster is finished, rather than just long?" | With no stop rule the agent pads to the budget and the last four personas are rewordings of the first | Stops at whatever number it was handed | per-run |  | ○ |
| 19 | "This persona is plausible and has nothing behind it in the source — do I drop it or flag it?" | Dropped, a real user goes unserved; kept unflagged, an invention becomes a line in someone's roadmap | Keeps it, silently | per-run |  | ◐ |
| 20 | "The same five personas fall out of me for every SaaS I'm pointed at — how do I catch that in myself while I'm doing it?" | A prior wearing the costume of a finding; nothing downstream of the agent can detect it | Nothing — it reads as a competent roster | per-run | ⚡ | ○ |
| 21 | "This subject is in a domain I have no real signal for. Do I say so, or do my best?" | Silent best-effort in an unfamiliar field is indistinguishable from expertise to the person reading it | Does its best, confidently | per-run |  | ○ |
| 22 | "Am I allowed to come back and say this subject has no demand side worth mapping?" | If a null result can't be returned, every subject yields nine personas whether or not it has any | Always produces a roster | per-run |  | ○ |
| 23 | "The user's seed persona contradicts what I read in the source — who wins?" | Overriding loses their local knowledge; deferring launders their assumption into a research finding | Quietly keeps both and hopes | per-run |  | ◐ |
| 24 | "How do I tell a load-bearing detail in this source from decoration?" | Decides what gets generalized into a persona, by an executor with no domain sense to weight it | Weights by how often a thing is repeated | per-run |  | ○ |
| 25 | "If I'm wrong here, what shape will the wrongness take — so I can put the check in front of it?" | Pre-registering the failure mode is the only self-check available to an executor that cannot verify against reality | Nothing — errors surface with the reader, or never | per-run | ⚡ | ✅ |

### P3 — The repeat user who tunes, forks, or upgrades the method

| # | The ask, in their words | Why — the decision it feeds | Today | Freq | ⚡ | Cov |
|---|---|---|---|---|---|---|
| 26 | "I ran this on the same subject six months ago — is the diff real change in my product, or drift in the method?" | They report the delta upward as a market shift; if it's drift they're reporting noise as a trend | Compares the two documents by eye | quarterly | ⚡ | ◐ |
| 27 | "The model underneath changed. Is this roster different because my subject moved, or because its priors did?" | The confound that silently invalidates every longitudinal comparison built on this | Nothing — doesn't know the model changed | per-release | ⚡ | ◐ |
| 28 | "Can I pin a version so my quarterly runs stay comparable to each other?" | Whether their series is a series at all, or four unrelated snapshots stacked in a folder | Runs whatever's latest and hopes | quarterly | ⚡ | ○ |
| 29 | "Point it at a subject I already know cold and show me exactly what it gets wrong." | The only calibration available — it sets how much of a roster on an unknown subject they're entitled to believe | Trusts it uniformly, or not at all | onboarding | ⚡ | ○ |
| 30 | "Run it again with my domain notes deliberately stripped out, so I can see what the method contributes on its own." | Separates the method's actual yield from their own expertise leaking in through the prompt | Nothing — can't tell the two apart | per-release | ⚡ | ◐ |
| 31 | "I want to swap the persona axis for one of my own without forking the whole thing." | A fork stops receiving fixes and diverges silently; they'd rather extend than inherit a dead copy | Copies it and edits in place | per-release |  | ✅ |
| 32 | "Show me the candidates it rejected, not just the nine it kept." | The reject pile is where the missing persona usually sits, and the only window onto the selection rule | Nothing — rejects are never surfaced | per-run |  | ○ |
| 33 | "When you upgrade this, which of my customisations breaks?" | Decides whether they take the upgrade at all — finding out mid-run costs them the run and the comparison | Upgrades and finds out the hard way | per-release | ⚡ | ○ |

### P4 — The program or agent that calls the method as a step

| # | The ask, in their words | Why — the decision it feeds | Today | Freq | ⚡ | Cov |
|---|---|---|---|---|---|---|
| 34 | "Same subject, same commit — do I get identical rows, or do I have to diff fuzzily?" | Whether this can gate CI at all, or only ever run as an advisory job nobody reads | Diffs it and drowns in noise | many/day |  | ◐ |
| 35 | "Give me the roster as a schema I can validate, not prose I have to parse." | A prose change breaks the parser at 3am with nothing upstream noticing it changed | Regexes the markdown | many/day |  | ◐ |
| 36 | "How do I tell a failed run from a confident empty roster?" | A subject with no demand side and a crashed executor look identical to the caller — and the empty one ships | Checks the row count and hopes | daily |  | ◐ |
| 37 | "What does one run cost, and can I cap it before it fires four hundred times?" | Sets the batch size, and whether the nightly job is approved to exist | Runs ten and extrapolates | weekly |  | ○ |
| 38 | "If the source it read is six months stale, does the output say so or just look current?" | Stale rosters are indistinguishable from fresh ones once they're two hops downstream | Nothing — no timestamp travels with the output | daily |  | ◐ |
| 39 | "If it dies at persona six, do I get six rows or nothing?" | A partial roster silently becomes a complete one at the next stage of the pipeline | Gets partial output and treats it as final | per-run |  | ✅ |

### P5 — The decision maker who never runs it, only ships its output onward

| # | The ask, in their words | Why — the decision it feeds | Today | Freq | ⚡ | Cov |
|---|---|---|---|---|---|---|
| 40 | "Which sentence in which document made you say this?" | They defend the roster to people who weren't there; with no citation the whole thing rests on their word | Says "the analysis found" and moves on | quarterly |  | ◐ |
| 41 | "I'm putting persona three in a board deck — what's the caveat I'm obliged to say out loud?" | Sets how hard a commitment they make in the room, and how far they can be walked back later | Presents it flat and unqualified | quarterly |  | ◐ |
| 42 | "We built for persona three and nobody came. Re-run it and show me what it should have caught." | Decides whether the method survives having cost a launch — and what the org tells itself about why the launch failed | Blames the team | per-incident | ⚡ | ◐ |
| 43 | "How confident is each row, and what single fact would flip it?" | Tells them which rows to fund now and which to spend a week testing first | Treats all nine rows as equally solid | quarterly |  | ○ |
| 44 | "What did this decide not to tell me?" | Suppressed low-confidence material is exactly the part that reappears as a surprise after launch | Nothing — assumes the document is the whole finding | quarterly |  | ○ |
| 45 | "Did a human being ever look at this before it got to me?" | Whether they present it as research or as a machine's first draft — and who is accountable when it's wrong | Assumes someone did | quarterly |  | ◐ |

### P6 — The person made to run it by a mandate, standard, or vendor change

| # | The ask, in their words | Why — the decision it feeds | Today | Freq | ⚡ | Cov |
|---|---|---|---|---|---|---|
| 46 | "How long does this take, and what's the smallest run that still satisfies the mandate?" | They're paying with a week they don't have; the answer decides whether they comply or quietly stall | Blocks out a week and resents it | quarterly |  | ◐ |
| 47 | "What exactly do I hand in as proof I ran it?" | The mandate is discharged by an artefact, not an insight — without knowing which, they over-produce or get bounced | Screenshots the output | quarterly |  | ◐ |
| 48 | "I already have a user list. Can it just check mine instead of inventing new ones?" | Forced to start from zero, they discard real knowledge and file a worse roster than the one they walked in with | Ignores their own list | onboarding |  | ✅ |
| 49 | "The output is obviously wrong for my product. Do I have to ship it anyway?" | A roster they know to be wrong enters the org's planning under their name and gets built against | Ships it with a shrug | per-run |  | ◐ |
| 50 | "What actually happens if I just skip this?" | Decides between compliance and quiet non-compliance; nobody has told them what the mandate is protecting against | Complies, badly | onboarding |  | ○ |

### P7 — The person who ran it once, got a horoscope, and never came back

| # | The ask, in their words | Why — the decision it feeds | Today | Freq | ⚡ | Cov |
|---|---|---|---|---|---|---|
| 51 | "Last time it told me my users want reliability and ease of use. Why is this run any different?" | No answer means no second run — and the method never learns it lost them, because they file nothing | Never came back | onboarding |  | ◐ |
| 52 | "Show me one thing in here I'd have been surprised by." | The surprise test is the only quality signal available to someone with no research training | Skims it and closes the tab | per-run |  | ✅ |
| 53 | "Was my first run bad because I gave it nothing, or because it can't do my domain?" | User error is fixable and a domain gap isn't; without the split they can't decide whether trying again is rational | Assumed the method was useless | onboarding |  | ○ |
| 54 | "Can this fail loudly instead of always producing a tidy document?" | A method that never fails carries no signal — and the tidy, plausible document is precisely what burned them | Got a horoscope and believed it for a month | per-run | ⚡ | ◐ |

### P8 — The people the output claims to speak for, who were never asked

| # | The ask, in their words | Why — the decision it feeds | Today | Freq | ⚡ | Cov |
|---|---|---|---|---|---|---|
| 55 | "Who decided I'm the 'frustrated junior admin', and where do I go to argue?" | The label now drives product decisions about them, with no route to contest a claim never put to their face | Never sees the document | quarterly |  | ○ |
| 56 | "It says people like me 'don't read the documentation' — is that an observation, or a stereotype the model already had?" | A prior about a job title hardens into a design constraint and makes the product measurably worse for them | Nothing — they aren't asked | quarterly |  | ○ |
| 57 | "This method never generates people like us at all — how would anyone ever notice we're missing?" | Absence is invisible inside a confident roster; the un-generated cohort is never served, never counted, never appealed | Nothing — no one knows to look | quarterly | ⚡ | ◐ |

### P9 — The security, privacy, or compliance reader

| # | The ask, in their words | Why — the decision it feeds | Today | Freq | ⚡ | Cov |
|---|---|---|---|---|---|---|
| 58 | "What exactly did you feed the model — did any of it contain customer names, tickets, or transcripts?" | Determines whether this run was a disclosable transfer of personal data to a third party | Asks the operator and gets a guess | per-release |  | ○ |
| 59 | "Is 'persona' here doing the work of age, disability, income, or country?" | A protected-class proxy inside a planning artefact is a discrimination exposure regardless of intent | Reads the prose and hopes | per-release |  | ○ |
| 60 | "Does anything from one subject's run persist into the next one's roster?" | Cross-tenant leakage — one customer's confidential subject surfacing inside another customer's output | Assumes not | per-release |  | ◐ |

**Tally:** 9 ✅ · 30 ◐ · 21 ○ · 12 ⚡

Twenty-one of sixty asks cannot be served at all today and thirty more are only partly served —
and those two are not the same claim. Appendix C shows that many ◐ marks mean *the rule exists but
ships as a warning nobody is required to run*, which is an enforcement gap, not an absent
capability. Eleven of the twelve frontier items are unserved or partial. **The ratio is the
finding, not the item count.**

---

## Verification (Phase 7)

Recorded from a fresh agent that had not seen this run, given only this document and the five Phase
7b questions verbatim, and forbidden to read any other file in the repository. Findings are recorded
including the ones the operator disagrees with, marked **disagreed** and why. The read was hard on
the document and mostly right.

**Three arithmetic errors, all verified and all fixed.** Recorded rather than quietly corrected,
because what they demonstrate matters more than the corrections.

| Finding | Status |
|---|---|
| Primitive 1 was called *"the largest cluster on the page"* at 8 items while primitive 2 carries 13 — and that false claim was the stated basis for ranking it first | **Accepted, fixed.** Re-ranked on consequence, which is the criterion primitive 7 says to use. |
| Item 56 was cited by two primitives — 61 assignments over 60 items | **Accepted, fixed.** Now cited by `prior-source-separation` only; `contestability` drops to two items. |
| Appendix C claimed *"ten rules ship as WARN"* and enumerated eight | **Accepted, fixed** — see Caveat 7. |

**The closer, which is the most useful finding in this run.** This document cites a prior run
self-reporting "⚡ count: 21" for a document carrying 26 as the strongest evidence on the page for
why `self-assessment` is needed — and then miscounted its own enumeration by two, in the same
appendix, unnoticed. The failure reproduced itself inside the document arguing for its fix. No
checker would have caught it: `verify.py` reads figures only from the canonical tally line,
deliberately, so a count stated in prose is invisible to it by design. Phase 7b earned its place
here on this finding alone.

**The cut rule was declared and not applied.** The header pre-registers *"the ask reads unchanged
for any other method-shaped subject"* as a cut criterion. Phase 7b names roughly 24 of 60 items that
survive it — with the whole of P4 the worst case, because items 34–39 restate the five Library/SDK
reach-further axes one per row, meaning P4 was derived from the archetype label rather than from the
subject. **Accepted and not fixed:** cutting 24 items would require regenerating the roster budgets
and re-running Phase 2, which is a fresh run rather than an edit. Recorded as this document's
principal defect, in the same way pass 1 recorded its roster's.

**Persona distinctness — accepted, and the preamble was overclaiming.** P7 (`lapsed-operator`) is
P1 at a later timestamp: items 52, 53 and 54 could be pasted into P1's table undetected, and only 51
is separable because "Last time" sits in the ask itself. P8 (`described-cohort`) collapses to one
distinct ask — 56 is P2's item 17 from the other side, 57 is P1's item 4 re-voiced, and only 55 is
unique. Worse, the Personas preamble said the Phase 2 distinctness test "ran and did not fire" as
though that were evidence; Appendix C says on the same page that distinctness is **deliberately
unchecked** because a lexical version scored true duplicates lowest. A test that cannot detect
duplicates failing to fire is the absence of evidence reported as a result. The preamble is wrong
and the roster needs regenerating, not editing.

**Coverage marks — accepted in part.** Four ✅ marks sit against primitives that describe the same
capability as absent: item 31 against primitive 11's own evidence that a fork is currently the only
customisation route, and items 39 and 48 against primitives marked *invented*. Item 4 was named in
this list too, against a primitive this section called *invented* — `absence-detection` is in fact
marked *inferred*, an error found later by the enrichment pass and corrected here. That is the third
prose-figure error in this run, all the same shape as the ⚡ miscount the document cites as its
strongest evidence, and the second found by someone other than the author. Item 4 remains
over-graded on the substance: no lane detects absence. All four are over-graded. Separately, and more damaging: the 28 items given Full verification are **exactly** the
items behind the three primitives the document then promotes — so verification effort followed the
conclusion, and the evidence for the ranking is the part of the table looked at hardest. Accepted,
unfixed, and a genuine methodological flaw in how the scoped-Full option was applied.

**The pre-registration could not fail — accepted.** The predicted split was 12/24/24 with the
surprise threshold set at "above 30 ✅": 2.5× the prediction, and defined only on the ✅ dimension.
The movement that actually occurred was in ◐ and ○, where no threshold existed. The Reckoning's
appeal to staying "well inside the threshold" is therefore close to unfalsifiable. This cannot be
retrofitted without dishonesty, so it stands as recorded — and the lesson is that a threshold must
be set on the dimension that can actually move, which nothing in the method currently says.

**Two frame-level challenges, both worth carrying.**

- *Personas are the wrong output unit for this category.* Contemporary demand-side practice
  (jobs-to-be-done, outcome-driven innovation) treats personas as the canonical failure mode
  precisely because they encode attributes rather than jobs — one person carries different demands
  in different situations. This document never uses the words job, outcome, switching, force or
  context, and item 7 ("which two of these nine do I cut?") is malformed on its face, because you
  rank jobs, not people. **Not disagreed, and not fixable inside this run:** it is a challenge to
  the frame, which was fixed in Phase 0 and held constant deliberately so the comparison would mean
  anything. It belongs on the record as the strongest external critique of the method itself.
- *The frequency column is not a frequency column.* `onboarding` is a lifecycle stage, not a
  cadence, and it sits in the same column as `many/day`. Sharper: P4 is graded `many/day` while
  P6's item 46 describes the same method as costing a week — a three-order-of-magnitude
  disagreement about one method, presented without comment, in a method that runs a human approval
  gate that makes `many/day` impossible. **Accepted**, and this is a defect in the published
  vocabulary rather than in this document. Logged with Caveat 3.

**Item counts used as evidence after being set by the author — accepted.** The roster budgets were
allocated by the deriving agent, and cluster sizes are then read back as demand signal. The ranking
has been re-based on consequence rather than size, which removes the worst instance but not the
underlying circularity.

**Why columns that state no decision — accepted.** Items 17, 20, 21, 22, 35, 38, 44, 55, 56, 57 and
59 give a consequence or an aphorism where a decision belongs, and they cluster in P2, P8 and P9 —
the personas this document argues matter most. The rule ships as a WARN (`verify.py:786-789`), so
7a never blocked on it.

**Disagreed — two.**

- *"A frontier item marked served-well is a contradiction in terms"* (on item 25, which carries ⚡
  and ✅). **Disagreed.** The method's one hard rule is that coverage annotates and never gates; a
  frontier ask that turns out to be served is exactly the outcome the rule is written to permit, and
  treating ⚡+✅ as contradictory would reintroduce coverage as a filter on the frontier.
- *"Four of twelve ⚡ marks — 10, 25, 30 and 57 — do not match the frontier class."* **Disagreed, and
  the disagreement is about a dropped clause.** The frontier class declared in this document's header
  has three forms, not two: *"what breaks if I upgrade", "make it fail the way production does"*,
  **and** *"show me this method's blind spot before I trust it."* All four contested items are the
  third form — 10 asks to be shown where the operator's own knowledge leaked into the roster, 30
  asks for the method's yield with the operator's expertise stripped out, 57 asks how anyone would
  notice a cohort the priors never generate, and 25 asks what shape the executor's wrongness will
  take so a check can be put in front of it. That is failure injection pointed inward at the
  executor, which for a method whose executor has no domain expertise is where it actually breaks.
  Recorded as disagreed rather than silently kept, because if the third clause is doing too much
  work then the frontier was named too widely, and that would be a Phase 0 error rather than a
  marking one.
- *"P8 is not a demand persona; including them inflates the roster and mixes a demand map with an
  ethics review."* **Disagreed on exclusion, accepted on thinness.** The method explicitly requires
  naming the classes nobody represented and says to state why if you conclude none belong; a roster
  that drops the people a document speaks for because they are not customers is the omission the
  instruction exists to prevent. But the finding that P8 carries one distinct ask across three rows
  is correct and is recorded above.

**One finding the operator raised against itself, which 7b did not:** this Verification section is
being written by the same operator whose document is under review, from a report it commissioned.
That is the arrangement the method prescribes, and it is still the weakest link in the chain — every
"accepted, unfixed" above is a judgement made by the party with an interest in the document
standing.

---

## What the 60 imply: 11 capability primitives

The items are evidence; these are the deliverable. Primitives were clustered with the shared
vocabulary unopened, and only then named against `references/primitives.md` — six slugs reused,
five minted. Where a minted slug was arguably close to an existing entry, the reason it was not
taken is stated, because a name bent to fit reports agreement the run did not find.

1. **Separating the model's prior from the source** `prior-source-separation` *(inferred: `skills/persona-brainstorm/scripts/verify.py:763-772`, where a lexical persona-distinctness check was built, measured and deliberately abandoned because it scored true duplicates lowest — 0.031 against 0.123 for unrelated pairs. The method has already tried to detect its own repetition mechanically and could not.)* — a third provenance value the current scheme has no slot for: not observed, not inferred, not invented, but *generated by what a model always says about this kind of subject.*
   → items 2, 13, 16, 17, 19, 20, 24, 56. Eight items — not the largest cluster on the page, `self-assessment` is — but the only one demanded by the executor, the operator and the described cohort alike — P2 asks how to catch it in itself, P1 asks to be shown where it happened, P8 asks whether the sentence about them was ever an observation at all. **Not `provenance-per-claim`:** that entry means labelling a claim observed/inferred/invented with its source, and all three of those marks can sit honestly on a sentence that came straight from the prior. Taking the slug would widen it to cover a case it was never about.

2. **Self-assessment the executor cannot fake** `self-assessment` *(observed: `skills/persona-brainstorm/SKILL.md:618-622` records a run of this method self-reporting "⚡ count: 21" for a document carrying 26 — a 24% error on the single number it was asked to compute about its own output, which nothing in the method caught.)* — a way for the method to tell its operator *and* its reader that this run under-reached, went generic, or was too thin to support its own output.
   → items 1, 3, 5, 9, 15, 18, 21, 22, 25, 51, 52, 53, 54. Thirteen items across five personas who share nothing else: the executor wants a stop rule, the lapsed operator wants one surprise, the one-shot operator wants to know a thin run from a thorough one. The recorded ⚡-miscount is the strongest evidence on this page for anything.

3. **Absence detection** `absence-detection` *(inferred: `SKILL.md:317-331` names three classes — the user who left, the user forced in by someone else's decision, and the classes nobody represented — as ones "a roster almost never contains, because every evidence source you have is blind to them." That is a statement about rosters built without them.)* — machinery for finding who is *not* on the list, and for making the absence visible rather than merely asked about.
   → items 4, 32, 44, 57. Small cluster, disproportionate stakes: item 57 is the one failure no reader of the output can ever detect from the output.

4. **Run identity and diffability** `run-identity` *(inferred: `references/cross-run.md:100-117`, the confound table, which names framing, sampling and evaluator drift as three independent confounds and states plainly that controlling one does not license attribution.)* — stable ids, a pinned method version, and a diff between two runs that separates real movement from method drift.
   → items 11, 26, 27, 28, 34, 38, 42. This run is itself the evidence: 17 commits landed between the two passes, so part of the movement reported below is the method changing and cannot be attributed to the subject.

5. **Deliberate failure injection** `failure-injection` *(inferred: `SKILL.md:55-58` — the hard rule exists because the first run of this method "filtered candidates through the shipped surface area and quietly deleted every idea with no current implementation," a failure discovered only after the fact.)* — a corpus of subjects on which the method reliably produces plausible but hollow output, so the blind spot can be observed rather than argued about.
   → items 10, 12, 29, 30. Every item here is ⚡ or adjacent to one, which is what the frontier class predicts.

6. **Provenance per claim** `provenance-per-claim` *(observed: running the shipped checker against pass 1's own document reports "10 primitive(s) carry no evidence mark" — the previous run of this method shipped every primitive unsourced.)* — every claim labelled with its kind and carrying its source, extended from primitives to personas and items.
   → items 14, 40, 45, 58, 60. The sponsor and the compliance reader want the same thing for opposite reasons.

7. **Consequence-weighted ranking** `consequence-weighted-ranking` *(invented)* — sorting rows by what the answer changes — reversibility, blast radius, regret — rather than by how many people want it.
   → items 7, 8, 41, 43.

8. **A machine contract** `machine-contract` *(invented)* — a validated schema, an explicit failure signal distinguishable from an empty result, a cost bound, and defined partial-run semantics.
   → items 35, 36, 37, 39. **Not `output-shaping`:** that entry is about rendering the same evidence for a different audience, and three of these four asks are not about rendering at all — a crash that looks like a null result is a correctness problem, not a formatting one.

9. **Contestability by the described** `contestability` *(invented)* — a route for the people a persona claims to describe to see the claim and dispute it.
   → items 55, 59. The only primitive on this page demanded by a persona who is not a user of the method, and the only one with a legal edge: item 59's protected-class proxy is an exposure regardless of intent.

10. **The minimum viable run** `minimum-viable-run` *(invented)* — a defensible floor: the smallest run that still discharges the obligation, what it costs, and what it is permitted to claim.
    → items 46, 47, 48, 49, 50. Entirely P6's, and it is the only primitive whose absence produces *quiet non-compliance* rather than a bad document.

11. **Extension points** `extension-points` *(inferred: `.claude-plugin/plugin.json` pins version `0.1.0` with no changelog, no compatibility statement and no `skills` array — bundling is by directory convention, so a fork is currently the only route to a customisation.)* — swapping a part without inheriting a dead copy, and knowing at upgrade time which customisations break.
    → items 6, 23, 31, 33.

### If you only ask for three

**`prior-source-separation`**, **`self-assessment`**, and **`run-identity`** — in that order.

`prior-source-separation` first on consequence, which is the criterion primitive 7 on this very page
says to rank by — what the answer changes, not how many people want it. An earlier draft ranked it
first on cluster size and called it "the largest cluster on the page"; both were wrong, and ranking
by cluster size would have broken this document's own rule in the one place it applies one. On
consequence it still leads: eight items across three unrelated personas, and **zero mechanical
footprint today**. It is also the one primitive whose absence is
invisible in the output by construction — a roster generated from the model's priors reads exactly
like a roster generated from the source, which is why no reader has ever caught one.

`self-assessment` second on evidence: thirteen items, and the only primitive on this page resting on
a recorded incident rather than reasoning.

`run-identity` third on cheapness of unlock. A version stamp and a coverage-depth declaration are a
schema change, not new machinery — and the same coverage-depth declaration closes Caveat 1 below,
which is a defect rather than a wish.

**Riding along:** `provenance-per-claim` is cheap enough to ship with whichever goes first. The
evidence-mark machinery already exists and is enforced for primitives
(`verify.py:814-860`); extending it to personas and items is a schema addition, not a new mechanism.

**Reckoning:** predicted 12/24/24, actual 9/30/21 — the prediction moved but stayed well inside the surprise threshold of 30 ✅, so this is the ordinary case and the direction is all that should be claimed. It moved toward *partial*: fewer asks are cleanly served than predicted and more are half-served. One candidate explanation is that the method gained a large checker between passes, attached to document self-consistency rather than to the asks people actually have — but that is a hypothesis, not an attribution, and this document cannot license it. The two passes were graded by different agents against a column with no mechanical footprint at all, which is the same evaluator drift that makes the ⚡ movement below unusable; the honest position is to apply that caveat to both figures rather than only the inconvenient one. A gap this size is as likely to be sampling as signal, and the cohort was regenerated from scratch, so the two runs share no item.

**Falsifier for the top primitive.** `prior-source-separation` is wrong if a roster generated with
the source withheld entirely — nothing but the domain name — turns out to differ substantially from
one generated with the full source. That would show the source is doing the work and the prior is
not dominant, and the primitive would be solving a problem that isn't there. The experiment is
cheap: two blind calls, one context block with the subject redacted to a bare noun, and a diff of
the two rosters by slug. It has not been run.

**The load-bearing persona is P1, `one-shot-operator`**, carrying 14 items. It is not fictional —
it is the modal user of any skill distributed through a marketplace — but the deriving agent flagged
unprompted that it may be *two* people, and if that split is real then roughly half of P1's items
belong to a subject owner who can judge the domain but not the method, and half to an operator who
can judge the method but not the domain. Primitives 1, 2 and 7 all draw heavily on P1; a split would
not remove them but would redistribute which of the two halves demands each, and
`consequence-weighted-ranking` in particular is entirely a subject-owner concern.

### Two observations worth carrying

- **The framing under-serves P8, `described-cohort`, and it does so structurally.** They have three
  items and no mechanism at all — every one of their asks came back ○ or ◐. The method's sole
  evidence source is a language model's priors, formed from text written disproportionately by
  people with fast connections, current hardware, no assistive technology, and a handful of
  well-resourced languages. A method whose one input is systematically blind to the population that
  writes least does not have a marginal coverage gap; that is a central failure mode, and the only
  persona who could report it is the one with no route into the document.

- **The clearest whitespace is the executor's own self-knowledge, and it is where the method is
  uniquely placed to act.** Primitives 1, 2 and 5 — 25 of 60 items between them — are all the same
  shape: the method inspecting its own output for hollowness before a human has to. Nobody else can
  build this, because nobody else is inside the run. Everything currently in the checker verifies
  that a document agrees *with itself*; nothing verifies that it says anything.

---

## Appendix B — Movement since pass 1

_Reported as evidence qualified by what was held fixed, never as proof that anything shipped served
demand. Phase 0 was held constant; sampling and evaluator drift were not controlled, and the method
itself changed by 17 commits between the passes._

### Slug reconciliation

Reconciliation was done after both documents existed, never in a prompt. Mapping recorded so a later
reader can check the judgement.

| Pass 1 persona | Pass 2 persona | Reading |
|---|---|---|
| `solo-maintainer` | `one-shot-operator` | Same position, renamed. Not a departure. |
| `executing-agent` | `executing-agent` | Unchanged — the only slug identical across both passes. |
| `roadmap-defender` | `accountable-sponsor` | Same position, renamed and widened to carry the rare-high-stakes contact. |
| `platform-operator` | `pipeline-integrator` | Same position: the automation consumer. |
| `representation-auditor` | `assurance-reviewer` + `described-cohort` | **Split.** Pass 1 had one persona reviewing whether the roster was complete; pass 2 separates the reviewer from the people being described. |
| `greenfield-architect` | — | Lost. |
| `domain-outsider-consultant` | — | Lost. Pass 1's own Verification section had already recorded this persona as a near-duplicate of `executing-agent`. |
| — | `method-adapter` | Gained. |
| — | `conscripted-operator` | Gained. |
| — | `lapsed-operator` | Gained. |

**Read the roster movement as a method-drift result, not a world result.** Pass 1 declared its axis
as *"mixed, which is a known defect"*; pass 2 declared a single axis and derived the roster from it.
Three of the four gains (`conscripted-operator`, `lapsed-operator`, `described-cohort`) are exactly
the three classes `SKILL.md:317-331` instructs the deriver to name explicitly — text that the
deriving agent received restated in its prompt. The blind agent reproduced the checklist it was
given, which is evidence the instruction works and **not** evidence that the demand picture moved.

### Primitive movement

| Pass 1 primitive | Pass 2 | Reading |
|---|---|---|
| `self-assessment` | re-derived | Survived independent re-derivation — the strongest form of confirmation available here. |
| `provenance-per-claim` | re-derived | Survived. |
| `run-identity` | re-derived | Survived. |
| `absence-detection` | re-derived | Survived. |
| `failure-injection` | re-derived | Survived. |
| `counterfactual-demand` | — | Not re-derived. |
| `consequence-weighted-ranking` | re-derived | Survived. |
| `external-grounding` | — | Not re-derived. |
| `output-shaping` | — | Not re-derived. |
| `cross-run-aggregation` | — | Not re-derived. |
| — | `prior-source-separation` | Minted. |
| — | `machine-contract` | Minted. |
| — | `contestability` | Minted. |
| — | `minimum-viable-run` | Minted. |
| — | `extension-points` | Minted. |

Six of pass 1's ten primitives re-derived from a fresh cohort that shares no item with the first —
but that phrase has to be read carefully, and Phase 7b was right to press on it. The *clusters* were
derived with the shared vocabulary unopened, which is the isolation the method requires; the
*names* were then reconciled against a seed file that is itself pass 1's output. So the clustering
was independent and the naming was not, and a reader should treat the six as "an independently
derived cluster that a supplied name fitted" rather than as six blind rediscoveries. This document
applies that same skepticism to the roster gains two paragraphs above; it did not originally apply
it here, which is the asymmetry Phase 7b identified.
`cross-run.md` is explicit that a primitive appearing in one pass and not the other is a **weak**
primitive, and the honest report says so rather than quietly keeping it: `counterfactual-demand`,
`external-grounding`, `output-shaping` and `cross-run-aggregation` are weak on this evidence. Note
the confound in the other direction too — `cross-run-aggregation` may have failed to re-derive
because the machinery for it *shipped* between the passes as `references/cross-run.md`, which is
movement in the subject rather than weakness in the primitive. The two cannot be separated from
these two documents alone.

### Frontier movement — and the one figure worth distrusting

Pass 1 carried **26 ⚡ of 60**; pass 2 carries **12**. This is the largest single movement between
the runs and it is almost certainly **not** a finding about the subject. Both passes used the same
archetype and the same frontier class, so the definition did not change; what changed is which
agent applied it. Frontier marking is a judgement made by the generating agent, and evaluator drift
is the one confound `cross-run.md:100-117` says a fixed Phase 0 does not control. Treat the drop as
a measurement of two different graders, and take from it only that **the ⚡ count is not comparable
across runs** — which is itself worth recording, since nothing in the method currently says so.

---

## Appendix C — Current coverage (inventory built 2026-08-30 against `3dd6fb2`)

_This is the supply-side mapping, retained because the coverage column above is meaningless without
it. It describes what the subject's one implementation does today; it does **not** bound the
brainstorm above._

**Coverage depth: Full, scoped.** Marks on the items behind the top three primitives —
`prior-source-separation`, `self-assessment` and `run-identity`, 28 items in total — were verified
against source with `file:line` evidence. The remaining 32 items are marked **Light**: built from
the protocol, the reference files and the public surface, and best-effort rather than proven. A
coverage column that silently mixed the two would be worse than one that admits the split.

### The nine lanes today

| Lane | Surface | Real limits |
|---|---|---|
| **A — The protocol** | `SKILL.md` Phases 0–6, prose the operator executes by hand | Every gate before Phase 7 is advice addressed to the model being graded, and `SKILL.md:618-622` says so outright. The frame, archetype, frontier class, budget and the honesty of the pre-registration are all taken on trust. |
| **B — The checker** | `scripts/verify.py`, four modes | Checks document *self-consistency* and *cross-document* consistency. It never checks anything about the subject. Cannot run on a document that isn't markdown pipe tables (`:365-368`). |
| **C — Discovery recipes** | `references/discovery.md`, six archetypes + a derive-your-own contract | Each recipe states what the lanes "usually turn out to be" *before* you look (`discovery.md:44-47`), which anchors. Nothing verifies that named lanes are the real ones or that a citation resolves. |
| **D — Template and worked example** | `output-template.md`, `worked-example-ddi.md`, `discovery/printed-cli.md` | `<>` placeholders are only caught on fields the checker reads (`verify.py:140-141`). The worked example is one Read-surface subject and explicitly non-normative. |
| **E — Isolation protocols** | Blind two-call generation, Phase 3 containment, fresh-agent 7b, no-backward-flow | **Zero mechanical footprint.** Whether two agents shared context, whether Phase 3 leaked, whether the 7b reader was fresh — none of it is verifiable from the artifact. |
| **F — Enrichment pass** | `references/enrichment.md`, checked by `verify.py:957-1363` | The heading is derived from the coverage mark, so the check agrees automatically. Whether a scene is invented or observed is unchecked by the reference's own admission (`enrichment.md:309-312`). |
| **G — Adversarial pass** | `references/adversarial.md`, checked by `verify.py:1442-1757` | The lane-status check is shape, not truth (`:1614-1620`). The "say where the mark stops" rule — its main safeguard against one real citation laundering four paragraphs of invention — is advice. |
| **H — Cross-run machinery** | `references/cross-run.md`, `references/primitives.md` | The slug-vocabulary check exists **only in `tests/run_fixtures.py:1237-1244`** and does not ship. A user's run can mint a slug, never record it, and nothing notices. |
| **I — Distribution** | `.claude-plugin/*.json`, the frontmatter `description` | Version `0.1.0`, no changelog, no compatibility statement, no `skills` array. Discovery depends wholly on the description matching the user's phrasing; nothing tests trigger coverage. |

### The enforced-versus-advice split

This is the single most decision-relevant fact in the appendix, and it is why so many marks above
came out ◐ rather than ✅. Roughly 25 rules FAIL by default. **Ten rules the method states as rules
ship as WARN**, and therefore never block the documented Phase 7a invocation: uneven budgets
(`verify.py:490-497`), ⚡ placement (`:500-506`), the tally stating a ⚡ count (`:516-517`), every
item graded (`:531-532`), at most half served (`:533-539`), frequency vocabulary (`:778-779`),
*Why* restating *Ask* (`:786-789`), asks quoted as speech (`:792-795`), 6–12 primitives
(`:873-874`), and slug presence (`:879-883`). That is ten, enumerated — an earlier draft of this
sentence claimed ten and listed eight, which Phase 7b caught and Caveat 7 records. `--strict`
promotes them all and no documented invocation uses it.

**Thirteen stated rules have no mechanical footprint at all**, including the entire blind-generation
isolation protocol (`SKILL.md:60-106`), the Phase 1 approval gate (`:342-345`), phase ordering
(`:50-53`), coverage-mark correctness (`:455-466`), and "never invent a citation to satisfy the
format" (`:182-185`).

Persona distinctness is **deliberately** unchecked, with a measured rationale rather than an
oversight: a lexical version scored true duplicates *lowest*, 0.031 against 0.123 for unrelated
pairs (`verify.py:763-772`). That is the correct call, and it is also why item 20 came back ○.

### Caveat 1 — Appendix A can be deleted from a Full-depth document and `--final` still exits 0

**Confirmed by probe.** `PERSONAS.md` truncated at its appendix heading passes `verify.py --final`
at exit 0 while still claiming `7 ✅ · 26 ◐ · 27 ○` — sixty graded marks with nothing left in the
file to ground one of them.

The root cause is structural rather than a missed branch: `parse()` reads five canonical header
declarations (`verify.py:330-357`) and **coverage depth is not among them**, so the checker cannot
distinguish a legitimate depth-None run from a Full run whose inventory was dropped. The adversarial
pass handles this (`:1460-1470`) because it *needs* the lanes; the core check never did.

Every claim the appendix grounds — the marks, the caveats, the `file:line` evidence, the
proven-versus-inferred split — is unanchored under both the default and `--final` invocations.
A `**Coverage depth:**` header declaration on the same one-address rule as `**Frequencies:**` would
close it, and would hand the enrichment pass the depth signal it currently infers from the presence
of marks.

### Caveat 2 — a Verification section of five one-character lines passes `--final`

**Confirmed by probe.** A section whose entire body is `x` / `y` / `z` / `a` / `b` passes at exit 0.
The threshold is a pure non-empty line count and it is exactly five: the same document with a
one-line body fails with *"Verification section has 1 non-empty line(s)"* (`verify.py:1818-1824`,
`:1402-1405`).

So the check fires on an *empty* section and passes on a *meaningless* one. The comment at
`:1815-1817` states the intent — "require enough substance to have carried them" — and a line count
does not deliver it. `is_substantive()` already exists at `:129-150` and would reject `x`.

### Caveat 3 — the frequency vocabulary has two homes and they disagree

`verify.py:23` accepts `monthly` and `annually`. `SKILL.md:391` publishes eight values and neither
is among them; `grep -rn 'monthly\|annually' skills/ README.md` returns exactly one hit, the checker
itself. Low impact — an out-of-vocabulary frequency is a WARN either way — but it is the drift shape
this repository's commit history keeps closing.

### Caveat 4 — unverified, pending the adversarial pass

The adversarial `About` block stores its value as the remainder of the label's own physical line
(`verify.py:1540-1545`), while two other checks in the same loop read the full block (`:1555`) and
everything up to the next blank line (`:1577`) — one entry, three parsing extents. Reported effect
is that soft-wrapping a valid `About` sentence produces a spurious FAIL, which would be the most
severe of the four because it fails a *correct* document. Not independently reproduced here; it
needs a conforming adversarial document, which the queued adversarial pass will produce.

### Caveat 5 — a closing parenthesis in an evidence source is reported as a missing mark

**Confirmed by probe, and hit live while verifying this document.** `MARK_RE` at `verify.py:81`
captures the source with `[^)]*`, so a `)` anywhere inside it ends the capture early and the
surrounding `\)\*` no longer matches. The mark becomes invisible.

The failure is not that it rejects the mark — it is what it says next: *"1 primitive(s) carry no
evidence mark"* (`verify.py:814-860`). An author who wrote a correct, well-formed, sourced mark is
told they omitted one, and the natural response is to add a second mark, which is itself an error
(*"two marks on one primitive is an error, not a choice"*, `output-template.md:94-95`). The check
diagnoses the wrong cause and steers the fix in the wrong direction.

This bit a source quoting a checker message, because those messages contain `primitive(s)` — so the
most likely text to trip it is this tool's own output. Sourcing an `observed` mark to what the
checker reported is exactly the auditable provenance the method asks for.

### Caveat 6 — a count stated in prose is invisible to the checker, by design, and that is where this document broke

Found by Phase 7b, in this document, in the appendix immediately above. An earlier draft of the
enforced-versus-advice section claimed *"ten rules ship as WARN"* and then enumerated eight, each
with a `file:line`. Phase 7a passed it with zero warnings, correctly: `verify.py` reads claimed
figures **only** from the canonical tally line (`:319-329`), and `SKILL.md:653-656` explains why —
a good document discusses numbers in prose, and a checker scanning everywhere would read that
discussion as a claim.

That reasoning is right, and this is its cost. The rule protects legitimate prose about numbers and
in exchange makes every prose figure unauditable. The document that reproduced the exact ⚡-miscount
it cites as its own strongest evidence is the demonstration.

**This is not straightforwardly fixable and should not be "fixed" carelessly.** Widening the checker
to scan prose would break the one-address discipline that keeps it honest. The realistic mitigations
are narrower: flag a prose cardinal immediately followed by an enumeration whose length disagrees
with it, or accept that this class of error belongs to Phase 7b and say so in `SKILL.md` — which
would at least tell an operator what the checker is *not* covering. Recorded here because the
alternative is a caveat that reads as though the tooling has it handled.

### Caveat 7 — the re-run path for this repository's own document is undefined

`tests/run_fixtures.py:1237-1244` asserts **bidirectional equality** between the primitive slugs in
`PERSONAS.md` and the seed table in `references/primitives.md` — `used but not recorded` and
`recorded but not used` are both failures. The pin is deliberate and correct: the seed is read-only
and describes exactly one run, and the check keeps it honest against that run.

What is undefined is what happens when that run is superseded. This document reuses six of the seed's
slugs and mints five, which is the outcome `cross-run.md` describes as healthy — and adopting it as
`PERSONAS.md` would fail both assertions until the seed is regenerated from it. Nothing documents
that regeneration as a step. **This document was therefore written to a dated path**, which
`cross-run.md:42-48` sanctions, leaving pass 1, the seed and the suite untouched.
