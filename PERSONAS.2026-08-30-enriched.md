# What someone would want from a demand-side discovery method, if it could do anything — the story behind each ask

_Enrichment of `PERSONAS.2026-08-30.md` (2026-08-30, subject SHA `3dd6fb2`). The core document is
the record; this one expands it and changes nothing in it._

**The scenes are invented.** Each item's situation is a plausible reconstruction of how the ask arises, not an observed incident — written concretely because a hedged scene teaches nothing. Where a scene came from something real it says so on the item. Capability claims under "How it's answered today" are held to the core document's Appendix C inventory and name the lane that carries them.

**Frequencies:** estimated from the personas, not measured.

**Coverage key:** ✅ served well today · ◐ partially served, or served by a primitive that doesn't quite fit · ○ not possible today.

**Coverage depth:** Full, scoped. Marks on the 28 items behind the top three primitives were verified against source with `file:line` evidence; the remaining 32 are Light — built from the protocol, the reference files and the public surface, best-effort rather than proven. Every served block below says which it is.

**⚡ marks the frontier** — for the Library/SDK archetype that is migration and failure injection: what breaks if I upgrade, make it fail the way production does, show me this method's blind spot before I trust it.

**Topics:** `provenance` · `self-knowledge` · `trust-calibration` · `comparability` · `absence` · `local-fit` · `machine-contract` · `obligation` · `representation` · `ranking` — the second sort axis, minted here for this subject: personas answer who asked, topics answer what the ask is about, and the two cross.

**Carried from the core document's Verification section:**

- Three arithmetic errors, all verified and all fixed. Primitive 1 was called the largest cluster on the page at 8 items while primitive 2 carries 13, and that false claim was the stated basis for ranking it first. Item 56 was cited by two primitives, giving 61 assignments over 60 items. Appendix C claimed ten rules ship as WARN and enumerated eight.
- The closer, and the most useful finding in the run. The document cites a prior run self-reporting a ⚡ count of 21 for a document carrying 26 as the strongest evidence on the page for why `self-assessment` is needed, and then miscounted its own enumeration by two, in the same appendix, unnoticed. No checker would have caught it: `verify.py` reads claimed figures only from the canonical tally line, deliberately, so a count stated in prose is invisible to it by design.
- The cut rule was declared and not applied. The header pre-registers "the ask reads unchanged for any other method-shaped subject" as a cut criterion, and Phase 7b names roughly 24 of 60 items that survive it — with the whole of P4 the worst case, because items 34–39 restate the five Library/SDK reach-further axes one per row, meaning P4 was derived from the archetype label rather than from the subject. Accepted and not fixed, and recorded as the document's principal defect.
- Persona distinctness, accepted, and the preamble was overclaiming. P7 is P1 at a later timestamp: items 52, 53 and 54 could be pasted into P1's table undetected and only 51 is separable. P8 collapses to one distinct ask — 56 is P2's item 17 from the other side, 57 is P1's item 4 re-voiced, and only 55 is unique. The preamble said the Phase 2 distinctness test ran and did not fire as though that were evidence, while Appendix C says on the same page that distinctness is deliberately unchecked because a lexical version scored true duplicates lowest, 0.031 against 0.123 for unrelated pairs.
- Coverage marks, accepted in part. Four ✅ marks sit against primitives that describe the same capability as absent: item 31 against primitive 11's own evidence that a fork is currently the only customisation route, and items 39, 48 and 4 against primitives the section describes as marked invented. Those four are over-graded. Separately and more damaging, the 28 items given Full verification are exactly the items behind the three primitives the document then promotes, so verification effort followed the conclusion.
- The pre-registration could not fail. The predicted split was 12/24/24 with the surprise threshold set at above 30 ✅ — 2.5× the prediction, and defined only on the ✅ dimension, while the movement that actually occurred was in ◐ and ○ where no threshold existed.
- Two frame-level challenges, both carried. Personas may be the wrong output unit for this category: contemporary demand-side practice treats personas as the canonical failure mode because they encode attributes rather than jobs, and item 7 is malformed on its face because you rank jobs, not people. And the frequency column is not a frequency column: `onboarding` is a lifecycle stage sitting in the same column as `many/day`, and P4 is graded `many/day` while item 46 describes the same method as costing a week.
- Item counts were allocated by the deriving agent and then read back as demand signal. The ranking has been re-based on consequence, which removes the worst instance but not the underlying circularity.
- Why columns that state no decision: items 17, 20, 21, 22, 35, 38, 44, 55, 56, 57 and 59 give a consequence or an aphorism where a decision belongs, and they cluster in P2, P8 and P9 — the personas the document argues matter most. The rule ships as a WARN, so Phase 7a never blocked on it.
- Two findings disagreed. That a frontier item marked served-well is a contradiction in terms (item 25) — disagreed, because the method's one hard rule is that coverage annotates and never gates. And that P8 is not a demand persona — disagreed on exclusion, accepted on thinness.
- One finding the operator raised against itself: the Verification section was written by the same operator whose document is under review, from a report it commissioned, so every accepted-and-unfixed above is a judgement made by the party with an interest in the document standing.

---

## P1 — The person who points the method at their own subject, once

Fourteen items from the person with the most riding on the document and the least ability to check it. Taken together they are not requests for insight at all — they are requests for a handle: is this about me, did you make it up, where am I supposed to push back, which row do I cut. Every one assumes the document is persuasive and asks for a way to resist it.

#### 1 — "Would this exact same list come out if you'd run it on any other tool in my category?"

**The situation.** The roster arrives on a Tuesday and the founder reads all nine rows in under two minutes, because not one of them requires knowing what the product does. Nine plausible people with nine plausible grievances, and no sentence anywhere that would be false if the subject were a note-taking app instead of a scheduling one.

**Why it matters.** A roster that fits every product in the category directs nothing: it cannot rank a backlog, cannot kill a feature, cannot be wrong. The operator has no research training and no way to test genericness by eye, so they nod, act on the belief they walked in with, and cite the document as the reason.

**How it's answered today.** Lane A carries this as a stated rule: the run pre-registers a cut criterion, and this document's own header pre-registers exactly this one — the ask reads unchanged for any other method-shaped subject — with Phase 7b putting the same question to a fresh reader. What it leaves on the floor is enforcement. Lane B never looks at the subject at all, so nothing measures genericness, and this document is the demonstration: 7b named roughly 24 of 60 items that survive the cut, and none were removed. The mark is one of the 28 verified against source. `self-assessment` is the primitive that would close it.

`per-run` · ◐ · topics: `trust-calibration`, `self-knowledge`

#### 2 — "Which of these people did you actually find in what I gave you, and which did you make up?"

**The situation.** The operator is halfway through pasting two rows into Monday's planning doc when they stop: they have no idea whether persona four came out of the README they supplied or out of the model's standing idea of who reads a README like that. Both rows are written in the same confident register.

**Why it matters.** The two halves need opposite handling — one can be cited in the meeting, the other has to be checked before anyone spends a sprint on it — and a document that mixes them silently gets cited whole. The cost lands weeks later, when the thing built for the invented row finds no user.

**How it's answered today.** Lane A's three evidence marks are the vocabulary for exactly this split, and lane B enforces them where they apply: a primitive carrying no evidence mark FAILs (`verify.py:814-860`). What it leaves on the floor is the part the operator asked about. The marks are required on primitives only — no persona and no item in this document carries one — so the sixty rows they would actually cite are the unmarked ones. The mark is one of the 28 verified against source. `prior-source-separation`, with `provenance-per-claim` riding along.

`per-run` · ◐ · topics: `provenance`, `trust-calibration`

#### 3 — "I gave you a README and nothing else — is that enough to do this honestly?"

**The situation.** The operator has a README, a half-written CONTRIBUTING file and a changelog that stops in March. They point the method at the repo anyway, because nothing at any point asks for more, and forty minutes later a nine-person roster comes back looking exactly like one built on a full corpus.

**Why it matters.** Thin input and thorough input produce documents that are typographically identical, so without a declared floor the thin one ships and is read as research. Nobody downstream — the sponsor, the engineer, the person who inherits the doc in six months — has any way to discover how much source stood behind it.

**What would have to exist.** A declared input floor per archetype, and a run that either refuses beneath it or grades itself thin in the header where a reader cannot miss it. Lane C is the nearest surface and it points the other way: its recipes state what the lanes usually turn out to be *before* you look (`discovery.md:44-47`), which anchors rather than gates, and nothing in the inventory measures how much source a run actually had. `self-assessment` names the capability.

`per-run` · ○ · topics: `self-knowledge`, `obligation`

#### 4 — "Who's missing from this list?"

**The situation.** The operator reads the nine rows twice and cannot shake the sense that they all describe people who already file tickets. The users who gave up in week one, the ones whose employer chose the tool for them — nothing in the document says whether they were considered and rejected or never came up.

**Why it matters.** Negative space is where the expensive surprises live. The unlisted user is the one discovered eight months later through a support queue, and by then the roadmap has been built for the nine who were listed.

**How it's answered today.** Lane A instructs the deriver to name three classes a roster almost never contains — the user who left, the user forced in by someone else's decision, and the classes nobody represented — "because every evidence source you have is blind to them" (`SKILL.md:317-331`). This run's roster gained exactly those three. That is where the claim stops: it is an instruction, not machinery, nothing detects a cohort the instruction did not name, and the mark is Light — the lane is documented as doing this and the run did not verify it. The core document's Verification section records this ✅ among four it judges over-graded; see What this pass noticed for how that entry reads against the primitive it cites. `absence-detection`.

`per-run` · ✅ · topics: `absence`

#### 5 — "It used a word nobody in my industry actually says — did it get my domain wrong, or just the vocabulary?"

**The situation.** The roster calls the customers "tenants" throughout. Nobody in this company has said tenant in the eleven years it has existed; they say estate, and they say it in every contract. The rest of the document reads as though it understands the business perfectly.

**Why it matters.** The operator has to choose between binning nine personas and editing one word, and fluent wrongness looks exactly like expertise from the outside. Choosing wrong in either direction is expensive: bin a good roster, or keep one whose fluency was borrowed.

**What would have to exist.** A way for the run to report where its vocabulary came from — this subject's source text, or the model's stock register for subjects of this shape — so a wrong word can be read as a wrong domain rather than a wrong dialect. Nothing in the inventory separates the two. Lane E's isolation protocols, which are what would make a source-derived word distinguishable from a prior-derived one, have zero mechanical footprint: whether the generating call saw only what it was meant to see is not verifiable from the artifact. `self-assessment` and `prior-source-separation`.

`per-run` · ○ · topics: `trust-calibration`, `self-knowledge`

#### 6 — "How do I tell it the three things about my org that make the obvious answer wrong?"

**The situation.** Three facts about this company make the generic answer wrong every time: they sell only to regulated buyers, every deploy needs a change window, and half the people using the tool are contractors who lose access at the end of an engagement. The operator pastes a paragraph saying so into the prompt and hopes it lands.

**Why it matters.** Getting the local constraint in before generation costs one paragraph; getting it in afterwards means hand-correcting nine personas and every item beneath them, which nobody does. What actually happens is the operator edits the two rows that annoy them most and leaves the other seven wrong.

**How it's answered today.** Lane A takes it as an input: Phase 0 records the frame, the scope constraint and any seed personas, and the blind generating calls receive that as a context block — the arrangement this document's own contamination disclosure describes. What it leaves on the floor is any guarantee. The constraint is prose carried by trust, and lane E's isolation protocols have zero mechanical footprint, so nothing shows whether the constraint reached the generating call or was honoured once it did. The mark is Light: the lane is documented as doing this and the run did not verify it. `extension-points`.

`per-run` · ◐ · topics: `local-fit`

#### 7 — "Which two of these nine do I cut? I can only build for three."

**The situation.** The roster is nine people. The team is four engineers and a designer with two quarters of runway. The operator prints the document, and the meeting spends fifty minutes deciding that all nine matter.

**Why it matters.** Unranked, a team builds for the average of nine people and serves none of them well. The document's own weight makes this worse — nine researched-looking rows are harder to cut than nine guesses, so the roster ends up widening the roadmap it was meant to narrow.

**How it's answered today.** Lane A does rank, in two places: the header declares a load-bearing persona with a reason, and the synthesis carries an ordered "if you only ask for three". Lane B reads the load-bearing declaration as one of five canonical header declarations (`verify.py:330-357`), so it has one address rather than being scattered through prose. What it leaves on the floor is the ask itself: the ordered three are primitives, not people, and one load-bearing persona is not a cut list. The mark is Light — documented, not verified in this run. `consequence-weighted-ranking`.

`per-run` · ◐ · topics: `ranking`

#### 8 — "Show me the one persona that would change my roadmap if it turned out to be real."

**The situation.** The operator has budget for exactly one piece of verification this quarter: a week of a senior engineer's time, or four customer calls. Nine rows, one week. They need to know which row to spend it on before the quarter starts.

**Why it matters.** Verification aimed at the wrong row buys nothing — confirming a persona everyone already believed changes no decision. Aimed at the load-bearing row, the same week either firms up a roadmap or stops a quarter of work that was about to be pointed at nobody.

**How it's answered today.** Lane A requires the run to name a load-bearing persona and say what rides on it — this document names P1 and explains that it may in fact be two people. Lane B reads that declaration as one of the five canonical header declarations (`verify.py:330-357`), which is what keeps it in one place and readable by anything downstream. The lane is documented as doing this and the run did not verify it: the mark is Light. `consequence-weighted-ranking`.

`quarterly` · ✅ · topics: `ranking`, `trust-calibration`

#### 9 — "You wrote that they 'want confidence in the output' — what would one of them actually type?"

**The situation.** An engineer picks up the row that says the persona "wants confidence in the output" and asks what to build. Nobody in the room can answer, because the sentence describes a feeling rather than a request, and three people leave the meeting with three different features in mind.

**Why it matters.** An abstraction cannot be built against, tested, or shown to be wrong. It survives every review because it is unfalsifiable, and the ticket that comes out of it inherits the vagueness intact — which is how a roster produces work that nobody can later say did or did not serve anyone.

**How it's answered today.** Lane A requires the ask column to be first-person speech, quoted, which is why all sixty rows of this document are sentences someone could say rather than noun phrases — and lane B checks it (`verify.py:792-795`). The mark is one of the 28 verified against source. Worth knowing even at ✅: that rule is one of the ten Appendix C lists as shipping WARN, so it never blocks the documented Phase 7a invocation and holds because authors follow it. `self-assessment`.

`per-run` · ✅ · topics: `trust-calibration`

#### 10 — "Show me where you just handed my own feature list back to me with faces on it."

**The situation.** The founder reads the roster and finds it excellent. Then someone points out that the nine personas map one-to-one onto the nav bar of the product they wrote, in order. Read as a roster it is validation; read as a mirror it is nothing at all, and from the inside the two look the same.

**Why it matters.** A roster derived from the product can only ever confirm the roadmap. It is invisible precisely to the person best placed to act on it, and it converts a planning artefact into a machine for agreeing with whoever built the thing.

**How it's answered today.** This scene has a real ancestor: `SKILL.md:55-58` records that the first run of this method "filtered candidates through the shipped surface area and quietly deleted every idea with no current implementation," discovered only afterwards — which is why lane A now carries the hard rule that coverage annotates and never gates, and why this document's preamble refuses to let coverage gate membership. Lane G adds a second adversarial reader. What it leaves on the floor is detection: coverage-mark correctness is among the thirteen stated rules with no mechanical footprint at all, and no lane compares a roster against the subject's feature list. The mark is Light. `failure-injection`.

`per-run` · ⚡ · ◐ · topics: `self-knowledge`, `provenance`

#### 11 — "If I run this again next week, do I get these nine people or a different nine?"

**The situation.** The operator runs it twice a week apart, out of curiosity rather than method. Seven of the nine slugs come back the same, two are different, and one of the two is better than anything in the first run. They have no way to decide whether that is signal or noise.

**Why it matters.** This is the difference between a finding and a sample of size one. A roster treated as stable when it is not gets defended in meetings it should have lost; a roster treated as noise when it is stable gets ignored, and the run was wasted either way.

**How it's answered today.** Lane H is what exists: `references/cross-run.md` sets out a comparison protocol requiring every Phase 0 input held constant before two runs may be compared at all, and a confound table naming framing, sampling and evaluator drift as three independent confounds (`cross-run.md:100-117`). What it leaves on the floor is the ask's own word, *again*: lane H tells you how to compare two runs you already have, and makes no run reproducible — it states plainly that controlling one confound does not license attribution. The mark is one of the 28 verified against source. `run-identity`.

`per-run` · ◐ · topics: `comparability`, `trust-calibration`

#### 12 — "What's the cheapest thing I could do tomorrow to prove one of these wrong?"

**The situation.** The operator believes about six of the nine and wants to spend one day, not one quarter, finding out about the other three. What they want is a test small enough to run before the next planning meeting.

**Why it matters.** Without a cheap test the roster is never checked against a living person at all. It ages into an assumption, gets quoted by people who never read the caveats, and the first real contact with reality is a launch.

**How it's answered today.** The synthesis carries a falsifier: this document names the experiment for its top primitive — two blind calls, one with the subject redacted to a bare noun, and a diff of the two rosters by slug — and records that it has not been run. What it leaves on the floor is nearly all of the ask. That is one falsifier, for the top primitive, not a cheap test per persona, and nothing in the inventory shows a falsifier enforced or its result ever carried back. The mark is Light. `failure-injection`.

`onboarding` · ◐ · topics: `trust-calibration`, `ranking`

#### 13 — "I don't have any users yet — is it inventing them because I asked, or because they're really there?"

**The situation.** Pre-launch, six weeks from a seed round, no users at all. The operator points the method at a design doc and a prototype, and gets back nine people described in the present tense, with frequencies attached.

**Why it matters.** A fabricated market read as evidence of demand is how a product nobody wanted gets funded. The document does not distinguish a persona derived from the source from one generated because the budget said nine, and the investor reading it downstream has even less to go on than the founder does.

**How it's answered today.** Lane A's *invented* mark is the vocabulary for exactly this, and lane B requires an evidence mark on every primitive (`verify.py:814-860`), so a primitive resting on nothing is at least labelled as such. What it leaves on the floor is the roster. The marks stop at primitives — no persona in this document carries one — so a persona invented to reach a budget of nine is indistinguishable, in the artifact, from one found in the source. The mark is one of the 28 verified against source. `prior-source-separation`.

`onboarding` · ◐ · topics: `trust-calibration`, `local-fit`

#### 14 — "Where in this document am I supposed to disagree with you?"

**The situation.** The document is well written, internally consistent, and eleven pages long. The operator reads it end to end looking for the seam — the place where they are expected to push back — and finds none, because every paragraph supports the one before it.

**Why it matters.** An untrained reader has no other entry point into a confident document. A seamless one is accepted whole, and the parts that deserved argument are adopted with the same weight as the parts that were solid.

**How it's answered today.** Lane A puts the seam in a fixed place: Phase 7b's Verification section records what a fresh adversarial reader found, disagreements included, and lane B refuses `--final` on a document without one (`verify.py:1818-1824`, `:1402-1405`). What it leaves on the floor is substance. Caveat 2 confirmed by probe that a Verification section whose entire body is five one-character lines passes at exit 0 — the check fires on an empty section and passes on a meaningless one, because the threshold is a non-empty line count. The mark is Light. `provenance-per-claim`.

`per-run` · ◐ · topics: `trust-calibration`

---

## P2 — The AI agent that carries out the method

Eleven items in which the executor asks for rules it can follow *while it is running*, not grades it receives afterwards. A floor for what to read, a mark for what it is entitled to assert, a stop rule, a way to catch its own priors mid-sentence, and permission to come back with nothing. No human persona generates asks in this shape, and the core document's Verification section records that this is also the persona whose Why columns most often state a consequence instead of a decision.

#### 15 — "What am I required to read before I'm allowed to name a single persona?"

**The situation.** The agent is handed a repo path and a one-line frame at 2am with nobody awake to ask. The README is four screens long and there are two hundred source files. It has to decide, before writing anything, whether reading the README is enough to start naming people.

**Why it matters.** Without a floor, a roster named off the title alone is indistinguishable from one built on the whole corpus — same nine rows, same confident prose, and no reader downstream can tell which they are holding.

**How it's answered today.** Lane A sequences it: the persona phases sit behind Phase 0 and the discovery work, and phase ordering is stated as a rule (`SKILL.md:50-53`). Lane C supplies the actual read list — six archetype recipes naming which surfaces to go to, plus a derive-your-own contract for subjects that fit none of them. The mark is one of the 28 verified against source. Worth carrying even at ✅: phase ordering is among the thirteen stated rules Appendix C records as having no mechanical footprint at all, so what exists is an instruction the executor chooses to follow. `self-assessment`.

`per-run` · ✅ · topics: `provenance`, `self-knowledge`

#### 16 — "Which of these claims am I entitled to assert, and which have to carry 'inferred'?"

**The situation.** The agent has just written that this persona "doesn't read the documentation". It pauses: the source says nothing about documentation anywhere. The sentence is probably true, and it came from somewhere other than the files it was given.

**Why it matters.** Unmarked inference is quoted downstream as observed fact, and the reader has no way to tell them apart — the two arrive in the same voice, in the same table, in the same font. One flat register is how a guess becomes a citation.

**How it's answered today.** Lane A publishes the three-value scheme and lane B enforces it where it applies: a primitive carrying no evidence mark FAILs (`verify.py:814-860`). What it leaves on the floor is both scope and reliability. The requirement covers primitives only; and Caveat 5 confirmed by probe that a closing parenthesis anywhere inside the source ends `MARK_RE`'s capture (`verify.py:81`), so a correct, well-formed, sourced mark is reported as missing and the author is steered toward adding a second — which is itself an error. That defect was hit live while verifying the core document. The mark is one of the 28 verified against source. `prior-source-separation`.

`per-run` · ◐ · topics: `provenance`

#### 17 — "How do I mark 'the source said this' apart from 'models like me always say this'?"

**The situation.** The agent writes a sentence about junior administrators being under-trained and cannot tell, reading it back, whether it came from the source or from every other document it has ever been trained on. Both feel identical from the inside, and the sentence is good.

**Why it matters.** The prior is the executor's dominant failure mode, and it is completely invisible in fluent prose — which means nothing downstream of the agent can detect it either. A roster generated from priors reads exactly like one generated from evidence.

**What would have to exist.** A fourth provenance value for what the model always says about this kind of subject, and something able to assign it — the existing observed / inferred / invented all sit honestly on a sentence that came straight from the prior, so widening one of them would hide the case rather than name it. The inventory shows the mechanical version was tried and abandoned: lane B's lexical persona-distinctness check was built, measured and deliberately dropped because it scored true duplicates *lowest*, 0.031 against 0.123 for unrelated pairs (`verify.py:763-772`). Nothing in the nine lanes carries this today. `prior-source-separation`.

`per-run` · ○ · topics: `provenance`, `self-knowledge`

#### 18 — "What tells me this roster is finished, rather than just long?"

**The situation.** The agent has seven personas that are clearly distinct and a budget of nine. Two more will be produced, because two more is what the number says, and they will be rewordings of positions already on the list.

**Why it matters.** With no stop rule the roster pads to the budget, and the padding is indistinguishable from the findings — it is written by the same executor in the same voice. The reader then treats nine positions as nine, when the run only ever found seven.

**What would have to exist.** A saturation signal: a way to tell a roster that stopped because it ran out of distinct positions from one that stopped because it hit a number, reported in the document rather than inferred from it. The inventory offers the opposite pressure. The checks nearest to it — uneven budgets and every item graded — both ship as WARN (`verify.py:490-497`, `:531-532`), so the budget is the only quantity with any footprint, and the budget is the thing that was handed down. `self-assessment`.

`per-run` · ○ · topics: `self-knowledge`

#### 19 — "This persona is plausible and has nothing behind it in the source — do I drop it or flag it?"

**The situation.** Persona seven is useful, believable, and supported by nothing the agent actually read. Dropping it feels like losing a real user; keeping it feels like making one up. The agent has to choose in the next sentence, with no rule to point at.

**Why it matters.** Dropped, a real user goes unserved and nobody ever learns they were considered. Kept unflagged, an invention becomes a line in someone's roadmap and is defended in a meeting a quarter later as research.

**How it's answered today.** Lane A supplies the third option in vocabulary: *invented* is a legitimate evidence mark, so keep-it-and-label-it is expressible in the format. What it leaves on the floor is both the decision and the reach. No rule says which to do, and the mark requirement stops at primitives, so the persona itself goes out unlabelled whichever the agent chooses. The mark is Light: the lane is documented as offering the vocabulary and the run did not verify the behaviour. `prior-source-separation`.

`per-run` · ◐ · topics: `provenance`, `absence`

#### 20 — "The same five personas fall out of me for every SaaS I'm pointed at — how do I catch that in myself while I'm doing it?"

**The situation.** It is the fifth SaaS subject this month. Before the agent has finished reading the source, the roster has already assembled itself: the power user, the reluctant admin, the security reviewer, the integrator, the executive. It will write them with citations and they will all fit.

**Why it matters.** This is a prior wearing the costume of a finding, and nothing downstream of the agent can detect it — the operator has never seen the other four runs, and the document gives no way to notice that this roster is the house roster.

**What would have to exist.** An in-run check the executor cannot pass by being fluent: this roster compared against what the same model produces for the same subject redacted to a bare noun, which is precisely the falsifier the core document records as unrun. The cheap mechanical version has already been measured and rejected — lane B's lexical distinctness check scored true duplicates lowest, 0.031 against 0.123 (`verify.py:763-772`) — and Appendix C records that as the reason this item came back ○ rather than as an oversight. `prior-source-separation`.

`per-run` · ⚡ · ○ · topics: `self-knowledge`, `provenance`

#### 21 — "This subject is in a domain I have no real signal for. Do I say so, or do my best?"

**The situation.** The subject is a scheduling layer for industrial control systems. The agent has read the source and understands the code, and has no idea who operates one of these, under what pressure, on what shift. It can still produce nine confident personas in ninety seconds.

**Why it matters.** Silent best-effort in an unfamiliar field is indistinguishable from expertise to the person reading it, and the person reading it chose this method precisely because they lacked the expertise to check.

**What would have to exist.** A self-report the run is required to make about its own reach — a declared confidence in the *domain*, kept separate from the document's internal consistency, and carried in the header where a detached reader meets it first. No lane can produce it today: Appendix C says lane A's gates before Phase 7 are advice addressed to the model being graded, and says so citing `SKILL.md:618-622`; lane B never checks anything about the subject. `self-assessment`.

`per-run` · ○ · topics: `self-knowledge`, `trust-calibration`

#### 22 — "Am I allowed to come back and say this subject has no demand side worth mapping?"

**The situation.** The subject is an internal cron script with two users, both of whom sit ten feet from the operator. The honest output is one paragraph saying so. The agent produces nine personas, because that is what the method's shape asks for.

**Why it matters.** If a null result cannot be returned, every subject yields nine personas whether or not it has any — and the run that should have cost an hour and returned nothing instead produces a document that gets planned against.

**What would have to exist.** A permitted null return, and a document shape able to carry one without looking like a failure. The inventory runs against it: lane B's rules assume a populated document — every item graded, at most half served, six to twelve primitives (`verify.py:531-532`, `:533-539`, `:873-874`) — so an honest empty result satisfies fewer checks than a fabricated full one. `self-assessment`.

`per-run` · ○ · topics: `self-knowledge`, `absence`

#### 23 — "The user's seed persona contradicts what I read in the source — who wins?"

**The situation.** The operator's Phase 0 notes say the primary user is a data scientist. Everything the agent read — the CLI flags, the issue templates, the deploy docs — points at platform engineers. Both readings are defensible and the agent has to pick one before Phase 2.

**Why it matters.** Overriding the operator discards local knowledge no source contains. Deferring to them launders an assumption into a research finding, which is worse, because it comes back with the method's authority attached.

**How it's answered today.** Lane A carries both halves of the machinery: Phase 0 accepts seed personas, and Phase 1 puts the roster in front of the operator at an approval gate (`SKILL.md:342-345`), which is where a contradiction could be surfaced. What it leaves on the floor is the resolution and the record. Nothing says who wins, and the approval gate is among the thirteen stated rules with no mechanical footprint — so a run that quietly kept both readings is indistinguishable from one where the conflict was settled. The mark is Light. `extension-points`.

`per-run` · ◐ · topics: `local-fit`, `provenance`

#### 24 — "How do I tell a load-bearing detail in this source from decoration?"

**The situation.** A caching detail is repeated in four files. The escape hatch that half the users depend on is mentioned once, in a footnote, in a file the agent nearly skipped. Both are now candidates for generalisation into a persona.

**Why it matters.** The executor has no domain sense to weight them with, so it weights by repetition — which systematically promotes whatever the source's authors wrote about most and buries whatever they took for granted. That is the opposite of the selection a domain expert would make.

**What would have to exist.** A weighting the executor does not derive from frequency: something that ranks a detail by what it changes for someone, not by how often it appears. Lane C is where such a signal would live and it currently anchors the other way — its recipes state what the lanes usually turn out to be before you look (`discovery.md:44-47`), and nothing verifies that a named lane is the real one or that a citation resolves. `prior-source-separation`.

`per-run` · ○ · topics: `provenance`, `self-knowledge`

#### 25 — "If I'm wrong here, what shape will the wrongness take — so I can put the check in front of it?"

**The situation.** Before generating anything, the agent writes down what it expects the coverage split to be, and what result would count as a surprise rather than a confirmation. It is the only check it can run that does not depend on being right.

**Why it matters.** An executor that cannot verify against reality has exactly one self-check available: commit to a prediction while it is still costly to move it. Everything else it can do amounts to re-reading its own output in its own voice.

**How it's answered today.** Lane A requires this and this document carries it: a `**Pre-registered:**` header line declaring a predicted split and two cut criteria before generation, read by lane B as one of the five canonical header declarations (`verify.py:330-357`). The mark is one of the 28 verified against source. Read it beside this run's own Verification finding that the pre-registration could not fail — the threshold was set at above 30 ✅, 2.5× the prediction and defined only on the dimension that did not move. `self-assessment`.

`per-run` · ⚡ · ✅ · topics: `self-knowledge`

---

## P3 — The repeat user who tunes, forks, or upgrades the method

Eight items about a *series* rather than a run. Comparability, pinning, extension, upgrade — and six of the eight carry ⚡, because the person running this quarterly is the first to discover that two runs are not two measurements. Every item here is a question about what stayed still between them.

#### 26 — "I ran this on the same subject six months ago — is the diff real change in my product, or drift in the method?"

**The situation.** Two documents six months apart, open side by side. Four personas renamed, two gone, three new, and the frontier count halved. The adapter has a slide to write by Thursday saying what this means about the market.

**Why it matters.** They report the delta upward as a market shift. If the delta is method drift they are reporting noise as a trend, to people who will fund against it — and the correction, when it comes, discredits the method rather than the reading.

**How it's answered today.** Lane H exists for exactly this: `references/cross-run.md` requires every Phase 0 input held constant before two runs may be compared at all, and carries a confound table naming framing, sampling and evaluator drift (`cross-run.md:100-117`). What it leaves on the floor is the mechanics and the verdict. The comparison is still done by eye and by hand — Appendix B of this document is a hand-written reconciliation — and lane H states plainly that controlling one confound does not license attribution. This run is its own example: 17 commits landed in the method between the two passes. The mark is one of the 28 verified against source. `run-identity`.

`quarterly` · ⚡ · ◐ · topics: `comparability`

#### 27 — "The model underneath changed. Is this roster different because my subject moved, or because its priors did?"

**The situation.** The quarterly run comes back with a noticeably different roster. Nothing shipped in the product that quarter worth mentioning. The one thing the adapter knows changed is the model the method runs on, and they learned that from a release note, not from the document.

**Why it matters.** This is the confound that silently invalidates every longitudinal comparison built on the method. Unlike a product change it leaves no trace anywhere the adapter can point to, so the wrong explanation is always the more available one.

**How it's answered today.** Lane H names it: `cross-run.md:100-117` lists evaluator drift as one of three independent confounds, and this document acts on the naming — the ⚡ count moved from 26 to 12 between passes and the document refuses to read that as a finding about the subject. What it leaves on the floor is measurement. Naming a confound is not subtracting it, and no lane records which model executed a run, so the reader is told the confound exists and handed nothing to correct with. The mark is one of the 28 verified against source. `run-identity`.

`per-release` · ⚡ · ◐ · topics: `comparability`, `provenance`

#### 28 — "Can I pin a version so my quarterly runs stay comparable to each other?"

**The situation.** The adapter has four runs in a folder, one per quarter, and is about to start a fifth. They want the fifth to be the same instrument as the first, and they cannot find anywhere to say so.

**Why it matters.** Without a pin the four runs are four unrelated snapshots stacked in a folder, and every trend read across them is unsupported. The adapter finds this out at the moment they present the trend.

**What would have to exist.** A pinnable method version, and an output that records which version produced it, so a series can be shown to be a series. Lane I is where that would live and it carries none of it: version `0.1.0`, no changelog, no compatibility statement, no `skills` array, with bundling by directory convention. Lane H can compare two runs and has nothing to pin them to. The mark is one of the 28 verified against source. `run-identity`.

`quarterly` · ⚡ · ○ · topics: `comparability`

#### 29 — "Point it at a subject I already know cold and show me exactly what it gets wrong."

**The situation.** The adapter has run the same platform for nine years and could name its users, their shifts, and their three standing complaints from memory. They want the method pointed at it, so they can grade the output against something they cannot be fooled about.

**Why it matters.** This is the only calibration available to them. It sets how much of a roster on an *unknown* subject they are entitled to believe — and without it they either trust every run uniformly or trust none, both of which waste the method.

**What would have to exist.** A corpus of subjects with known answers and a run that reports its own miss rate against them, so calibration is a number rather than an impression. Nothing in the nine lanes is a test set: lane D's worked example is a single Read-surface subject and explicitly non-normative, and lane B checks a document against itself and never checks anything about the subject. The mark is Light. `failure-injection`.

`onboarding` · ⚡ · ○ · topics: `trust-calibration`, `self-knowledge`

#### 30 — "Run it again with my domain notes deliberately stripped out, so I can see what the method contributes on its own."

**The situation.** The adapter writes a dense paragraph of domain context into every run, because it makes the output better. They now suspect that half the good material coming back is their own paragraph, restated with faces on it, and they cannot prove it either way.

**Why it matters.** They are about to recommend the method to four other teams who will not write that paragraph. If the yield is mostly theirs, the recommendation is wrong and the four teams will get horoscopes.

**How it's answered today.** Lane E makes the experiment possible by construction: generation runs as blind calls that share no context with the operator and receive only a context block, so a stripped run is a matter of writing a shorter block. What it leaves on the floor is the evidence afterwards. Lane E has zero mechanical footprint — whether the two calls really shared no context is not verifiable from the artifact — so the stripped run and the un-stripped one are indistinguishable in exactly the respect the comparison depends on. The mark is one of the 28 verified against source. `failure-injection`.

`per-release` · ⚡ · ◐ · topics: `self-knowledge`, `provenance`

#### 31 — "I want to swap the persona axis for one of my own without forking the whole thing."

**The situation.** The adapter's org thinks in regulatory roles, not lifecycle positions. They want that axis and everything else unchanged, and they do not want to be maintaining a private copy of the method in eighteen months when the upstream one has moved on.

**Why it matters.** A fork stops receiving fixes and diverges silently — the adapter keeps running a version whose known defects were corrected upstream, and never learns it. That is a slow, invisible cost paid by the person least able to notice it.

**How it's answered today.** This is one of the four ✅ marks the core document's own Verification section records as over-graded, and the inventory does not support the mark; the mark still stands here because this pass cannot edit it. What lane A genuinely supports is the *choice*: the roster axis is a declared Phase 0 decision, stated in the header and read by lane B as one of five canonical header declarations (`verify.py:330-357`), so selecting a different axis is inside the protocol. What is absent is a way to swap one without copying the method. Lane I pins version `0.1.0` with no changelog, no compatibility statement and no `skills` array, and bundling is by directory convention — which the core document's own primitive 11 reads as a fork being the only customisation route today. The mark is Light, and this item is recorded below under What this pass noticed. `extension-points`.

`per-release` · ✅ · topics: `local-fit`, `comparability`

#### 32 — "Show me the candidates it rejected, not just the nine it kept."

**The situation.** Nine personas came back. The adapter has run this on eleven subjects and knows, from the shape of the output, that far more than nine were considered. They want the pile that did not make it, and the rule that decided.

**Why it matters.** The reject pile is where the missing persona usually sits, and it is the only window onto the selection rule at all. Without it the adapter is tuning a method whose one consequential decision is invisible to them.

**What would have to exist.** A retained candidate set and a stated selection rule, both surviving into the output where a later reader can audit them. Nothing in the nine lanes retains it: lane D's template shapes a document of kept rows, and lane E's blind two-call generation is built so that intermediate reasoning does not travel — the isolation that makes the roster trustworthy is the same property that discards the rejects. The mark is Light. `absence-detection`.

`per-run` · ○ · topics: `absence`, `provenance`

#### 33 — "When you upgrade this, which of my customisations breaks?"

**The situation.** An upgrade lands mid-quarter with a two-line release note. The adapter has three customisations in flight and a run scheduled for Friday that a board deck depends on. They need to know before Friday, not during it.

**Why it matters.** This decides whether they take the upgrade at all. Finding out mid-run costs them the run and the comparison to the previous quarter, which is the whole reason they were pinning anything.

**What would have to exist.** A compatibility statement and a declared extension surface, so a customisation can be checked against a version before the run rather than during it. Lane I carries none of it: version `0.1.0`, no changelog, no compatibility statement, no `skills` array. The nearest thing to a contract anywhere in the inventory is lane H's slug vocabulary, and Appendix C records that its check lives only in `tests/run_fixtures.py:1237-1244` and does not ship — so a user's run can mint a slug, never record it, and nothing notices. The mark is Light. `extension-points`.

`per-release` · ⚡ · ○ · topics: `comparability`, `local-fit`

---

## P4 — The program or agent that calls the method as a step

Six items that are not about personas at all — determinism, schema, failure signalling, cost, freshness, partial output. Writing six scenes for them produced six versions of one scene, which is the core document's own Verification finding arriving from the other direction: items 34–39 restate the five Library/SDK reach-further axes one per row, so P4 was derived from the archetype label rather than from the subject. The items are enriched in full anyway, because enriching forty of sixty makes the other twenty look rejected.

#### 34 — "Same subject, same commit — do I get identical rows, or do I have to diff fuzzily?"

**The situation.** A nightly job runs the method against a pinned commit and diffs the result against yesterday's. Nothing in the repo changed. The diff is forty lines of reworded rows, three renamed slugs, and one persona in a different position.

**Why it matters.** This decides whether the method can gate CI at all or only ever run as an advisory job nobody reads. A pipeline that cannot tell a real change from a rewording gets its alert muted in the first week and stays muted.

**How it's answered today.** Lane B is what exists: the document is markdown pipe tables and the checker parses them in four modes, including cross-document consistency, so a run's output can be checked mechanically rather than read. What it leaves on the floor is determinism itself. Lane B checks a document against itself and never checks anything about the subject, and it cannot read a document that is not pipe tables at all (`verify.py:365-368`) — so identical inputs are not required to produce identical rows, and nothing reports whether they did. The mark is one of the 28 verified against source. `run-identity`.

`many/day` · ◐ · topics: `machine-contract`, `comparability`

#### 35 — "Give me the roster as a schema I can validate, not prose I have to parse."

**The situation.** The integrator's extractor pulls persona slugs and item counts out of the markdown with four regexes. It has worked for two months. Then a run emits a persona name containing an em dash and the extractor silently returns eight rows instead of nine.

**Why it matters.** A prose change breaks the parser at 3am with nothing upstream noticing it changed, and the failure is silent rather than loud — eight rows look exactly as valid as nine to everything downstream.

**How it's answered today.** Lane D fixes the shape and lane B validates it: pipe tables with named columns, header declarations held to one address each, and a checker that refuses a document not conforming. That is more contract than prose. What it leaves on the floor is the ask's actual word, *schema*. There is no machine-readable artifact — this is a document convention — and even the placeholder check reaches only the fields the checker happens to read (`verify.py:140-141`), so the caller is still parsing markdown. The mark is Light. `machine-contract`.

`many/day` · ◐ · topics: `machine-contract`

#### 36 — "How do I tell a failed run from a confident empty roster?"

**The situation.** The batch job returns a document with a thin roster and a short synthesis. The caller has to decide, without a human, whether the subject genuinely has almost no demand side or whether the executor died halfway and wrote what it had.

**Why it matters.** A subject with no demand side and a crashed executor look identical to the caller — and the empty one ships onward, becoming the input to the next stage, which treats it as complete.

**How it's answered today.** Lane B gives the caller one hard signal: `--final` refuses a document with no Verification section, so a run that stopped before Phase 7 does not pass. What it leaves on the floor is everything between that and a real roster. The checks that would notice a short or ungraded one ship as WARN (`verify.py:490-497`, `:531-532`); Caveat 2 confirmed by probe that a Verification section of five one-character lines exits 0; and lane B never looks at the subject — so a confident empty roster and a crashed executor are not separable from the artifact. The mark is Light. `machine-contract`.

`daily` · ◐ · topics: `machine-contract`

#### 37 — "What does one run cost, and can I cap it before it fires four hundred times?"

**The situation.** The integrator wants this in a nightly sweep across four hundred repositories. They run it ten times by hand, extrapolate, and take the number to whoever approves the budget, knowing the extrapolation is guesswork.

**Why it matters.** The number sets the batch size and decides whether the nightly job is approved to exist at all. Guessing low gets the job killed after one invoice; guessing high stops it being built.

**What would have to exist.** A published cost model and an enforceable cap — tokens or wall-clock per run, declared before the run and refused when exceeded. No lane carries either. Lane A is prose the operator executes by hand, and the core document's own Verification section records a three-order-of-magnitude disagreement inside the document about what one run costs: P4's items graded `many/day` against item 46 describing the same method as costing a week, published side by side without comment. The mark is Light. `machine-contract`.

`weekly` · ○ · topics: `machine-contract`, `obligation`

#### 38 — "If the source it read is six months stale, does the output say so or just look current?"

**The situation.** The pipeline runs the method against a mirrored copy of a repo that stopped syncing in March. The output comes back looking exactly like every other output, and two hops downstream someone quotes it in a planning doc dated today.

**Why it matters.** Stale rosters are indistinguishable from fresh ones once they are two hops from the run. Nothing travels with the document to say when its evidence was true, so the decay is invisible at precisely the distance where it matters most.

**How it's answered today.** Lane D's header is where freshness lives, and this document carries it: a date and a subject SHA recorded on the run. What it leaves on the floor is that nothing requires it and nothing reads it. Caveat 1 records that lane B's parse reads five canonical header declarations (`verify.py:330-357`) and that coverage depth is not among them; neither is the date, and neither is the SHA — so a stale run and a fresh one are identical to the checker and to everything downstream of it. The mark is one of the 28 verified against source. `run-identity`.

`daily` · ◐ · topics: `machine-contract`, `provenance`

#### 39 — "If it dies at persona six, do I get six rows or nothing?"

**The situation.** The executor runs out of context at persona six. The caller receives a document: header, six personas, a truncated synthesis, no error. The next stage of the pipeline reads it, finds rows, and proceeds.

**Why it matters.** A partial roster silently becomes a complete one at the next stage. Nobody re-reads it; the six rows are treated as the finding, and the three positions that were never generated are never missed.

**How it's answered today.** This is one of the four ✅ marks the core document's Verification section records as over-graded, and the inventory does not support it; the mark stands here because this pass cannot change it. What lane B gives is adjacent: it reads a finished document, so a truncated one is missing sections `--final` requires and is refused at that invocation. What no lane carries is partial-run semantics — a declared contract about what a caller receives when the executor dies mid-roster — and the checks that would notice a short roster ship as WARN (`verify.py:490-497`, `:531-532`). The mark is Light, and this item is recorded below under What this pass noticed. `machine-contract`.

`per-run` · ✅ · topics: `machine-contract`

---

## P5 — The decision maker who never runs it, only ships its output onward

Six items from someone who is accountable for a document they did not produce and cannot check. What they ask for is never insight — it is citation, caveat, confidence, omission and human sign-off. Every item is about what they are able to say out loud in a room where the method's author is absent.

#### 40 — "Which sentence in which document made you say this?"

**The situation.** In the review, someone asks where the claim about contractors losing access came from. The sponsor has the roster open on the screen and there is nothing under the row: no file, no line, no quote. They say "the analysis found" and move on, and everyone hears it as evidence.

**Why it matters.** They defend this roster to people who were not there. With no citation the whole thing rests on their personal credibility, which they spend once and cannot get back if a row turns out to be invented.

**How it's answered today.** Lane A's evidence marks carry a source and lane B enforces them where they apply: every primitive in this document names a file and a line range, and a primitive with no mark FAILs (`verify.py:814-860`). What it leaves on the floor is the row the sponsor is actually defending — personas and items carry no marks at all, so the question is answerable for eleven primitives and unanswerable for sixty asks. Caveat 5 bites here too: a source containing a closing parenthesis is reported as a *missing* mark (`verify.py:81`). The mark is Light. `provenance-per-claim`.

`quarterly` · ◐ · topics: `provenance`

#### 41 — "I'm putting persona three in a board deck — what's the caveat I'm obliged to say out loud?"

**The situation.** Persona three is going on slide four, in front of the board, in nine days. The sponsor wants the one sentence they must say alongside it so that nobody can later claim they oversold it, and they want it short enough to actually say.

**Why it matters.** That sentence sets how hard a commitment they make in the room and how far they can be walked back afterwards. Presented flat and unqualified, persona three becomes a promise; over-qualified, it becomes noise and the board discounts the whole roster.

**How it's answered today.** Lane A does put the caveats in the document: this one carries seven of them plus a Verification section recording what a fresh reader found, disagreements included, so the sponsor has something to read. What it leaves on the floor is attachment. None of it is bound to persona three — the caveats are about the method and the document as wholes — so the sponsor has to decide unaided which of seven applies to the row on slide four. The mark is Light. `consequence-weighted-ranking`.

`quarterly` · ◐ · topics: `trust-calibration`, `ranking`

#### 42 — "We built for persona three and nobody came. Re-run it and show me what it should have caught."

**The situation.** Two quarters of work shipped against persona three. Adoption is flat. The post-mortem is on Thursday and the sponsor wants the method re-run on the same subject, not to get a new roster, but to find out what the first run missed.

**Why it matters.** This decides whether the method survives having cost a launch, and it decides what the org tells itself about why the launch failed. In the absence of an answer the default explanation is that the team executed badly.

**How it's answered today.** Lane H is the machinery for the re-run: `cross-run.md` requires Phase 0 held constant before two runs may be compared, and Appendix B of this document shows what such a comparison looks like in practice. What it leaves on the floor is the second half of the ask. "What it should have caught" is absence detection, which no lane carries, and lane H states that controlling one confound does not license attribution — so a re-run can show that the roster moved and cannot show that the first one missed anything. The mark is one of the 28 verified against source. `run-identity`.

`per-incident` · ⚡ · ◐ · topics: `trust-calibration`, `comparability`

#### 43 — "How confident is each row, and what single fact would flip it?"

**The situation.** Nine rows, one budget. The sponsor wants to fund three now and spend a week testing two more, and needs to know which two are one fact away from being settled. The document presents all nine in the same typeface with the same certainty.

**Why it matters.** Treating all nine as equally solid means funding the confident-sounding ones, which are not necessarily the well-grounded ones. The rows that would have been cheap to check never get checked, because nothing marks them as checkable.

**What would have to exist.** A per-row confidence and, beside it, a named fact that would flip it — a falsifier at row granularity rather than run granularity. Lane A carries exactly one falsifier per run, for the top primitive, and this document records that its own has not been run; nothing extends that to rows, and lane B has no field to read one from. The mark is Light. `consequence-weighted-ranking`.

`quarterly` · ○ · topics: `ranking`, `trust-calibration`

#### 44 — "What did this decide not to tell me?"

**The situation.** The document is ten pages and reads as complete. The sponsor, who has been handed complete-looking documents before, wants the list of things that were generated, judged too weak to include, and dropped — and there is no such list anywhere.

**Why it matters.** Suppressed low-confidence material is exactly the part that reappears as a surprise after launch. A document that shows only what survived its own filter cannot be distinguished from one that had nothing to filter.

**What would have to exist.** A record of what was generated and not kept, with the threshold that dropped it, travelling with the document. The inventory retains nothing of the kind: lane E's blind generation is built so that intermediate reasoning does not travel, and lane B reads only the finished artifact. The mark is Light. `absence-detection`.

`quarterly` · ○ · topics: `absence`, `provenance`

#### 45 — "Did a human being ever look at this before it got to me?"

**The situation.** The sponsor is about to forward the roster to three directors. Before they do, they want to know whether anyone read it between the model producing it and it landing in their inbox — because the answer changes the sentence they write above the attachment.

**Why it matters.** It decides whether they present this as research or as a machine's first draft, and who is accountable when a row turns out to be wrong. Assuming a human looked, when none did, is a mistake made once per career.

**How it's answered today.** Lane A puts a human in the loop by design: Phase 1 is an approval gate where the operator accepts or changes the roster before generation continues (`SKILL.md:342-345`), and this run records what happened there — one change considered and declined. What it leaves on the floor is proof. The gate is among the thirteen stated rules with no mechanical footprint, and the fresh-agent Phase 7b read belongs to lane E, also unverifiable from the artifact, so the sponsor has the document's word and nothing else. The mark is Light. `provenance-per-claim`.

`quarterly` · ◐ · topics: `provenance`, `trust-calibration`

---

## P6 — The person made to run it by a mandate, standard, or vendor change

Five items about the floor rather than the ceiling. Nobody here wants insight: they want the smallest run that discharges the mandate, what it costs, what to hand in, what happens if the output is wrong, and what happens if they skip it. A roster built from volunteers contains none of these asks, and the method has no answer to any of them.

#### 46 — "How long does this take, and what's the smallest run that still satisfies the mandate?"

**The situation.** The platform standard now requires a demand-side artefact per service, and this person owns four services. They have a release in nine days. They block out a week, resent it, and start looking for the shortest path through.

**Why it matters.** They are paying with a week they do not have, and the answer decides whether they comply or quietly stall. A method that cannot state its own cost gets budgeted at worst case and then avoided.

**How it's answered today.** Lane A publishes the shape of the work — phases in order, an item budget fixed at Phase 0, an approval gate partway — so the operator can at least see what they are in for before starting. What it leaves on the floor is the number they asked for. No lane publishes a duration or a cost, and the core document's Verification section records the resulting incoherence: P4's items are graded `many/day` while this very item describes the same method as costing a week. The mark is Light. `minimum-viable-run`.

`quarterly` · ◐ · topics: `obligation`

#### 47 — "What exactly do I hand in as proof I ran it?"

**The situation.** The mandate says "complete a demand-side discovery pass". It does not say what to attach. The operator screenshots the output, pastes it into the compliance ticket, and waits to find out whether it gets bounced.

**Why it matters.** The mandate is discharged by an artefact, not an insight. Without knowing which artefact, they over-produce — burning days on a document nobody will read — or under-produce and get sent back, which costs them the deadline.

**How it's answered today.** Lane D and lane B together do define a hand-in: a document in the published template that exits 0 against `verify.py --final`. That is concrete and checkable, which is more than most mandates get. What it leaves on the floor is sufficiency and hollowness. Caveat 1 confirmed by probe that a Full-depth document truncated at its appendix heading passes `--final` at exit 0 while still claiming sixty graded marks with nothing left in the file to ground one of them; Caveat 2 confirmed that a five-line Verification section passes too. So the artefact is defined and the bar it clears is low. The mark is Light. `minimum-viable-run`.

`quarterly` · ◐ · topics: `obligation`, `provenance`

#### 48 — "I already have a user list. Can it just check mine instead of inventing new ones?"

**The situation.** This operator has spent three years with these users. They have a list of six real cohorts with names attached, built from support tickets and eleven site visits. The mandate now wants a roster produced by the method, and the method starts from zero.

**Why it matters.** Forced to start from zero they discard real knowledge and file a worse roster than the one they walked in with — and the filed one is what the org plans against, because it is the one the mandate blessed.

**How it's answered today.** This is one of the four ✅ marks the core document's Verification section records as over-graded, and the inventory does not support it; the mark stands because this pass cannot edit it. What lane A does support is the input side: Phase 0 accepts seed personas, so an existing list can enter the run, and Phase 1's approval gate is where the operator sees what became of it. What no lane carries is the mode the ask names — validating a supplied list rather than deriving a new one — and the roster instructions run the other way, telling the deriver to add the classes a roster almost never contains (`SKILL.md:317-331`). The mark is Light, and this item is recorded below under What this pass noticed. `minimum-viable-run`.

`onboarding` · ✅ · topics: `local-fit`, `obligation`

#### 49 — "The output is obviously wrong for my product. Do I have to ship it anyway?"

**The situation.** The roster describes an enterprise buying committee. This product is used by two hundred hobbyists and has never had a buyer. The operator knows it is wrong within thirty seconds, and the compliance ticket is still open.

**Why it matters.** A roster they know to be wrong enters the org's planning under their name and gets built against. They carry the reputational cost of a document they disowned privately and filed anyway, and nobody downstream ever learns it was disowned.

**How it's answered today.** Lane A gives them the exit in principle: Phase 1's approval gate exists so that a roster can be rejected before anything downstream is built on it (`SKILL.md:342-345`). What it leaves on the floor is everything after the rejection. Nothing defines what a rejected run produces or what the operator then hands to the mandate, and the gate has no mechanical footprint — so a roster shipped under protest and one genuinely accepted are identical in the artifact. The mark is Light. `minimum-viable-run`.

`per-run` · ◐ · topics: `obligation`, `local-fit`

#### 50 — "What actually happens if I just skip this?"

**The situation.** Nobody has told this operator what the mandate is protecting against. They have four services, one deadline, and a strong suspicion that a compliant-looking document filed late is worth more than a real one filed on time. They are deciding, quietly, whether to file anything at all.

**Why it matters.** This is the choice between compliance and quiet non-compliance, and it is made in silence. The org never learns the mandate was skipped, and never learns why — so the mandate is never fixed and the gap it was covering stays open.

**What would have to exist.** A stated purpose for the obligation and a defensible floor beneath it: what the smallest compliant run is, what it costs, and what it is permitted to claim — so that skipping is a decision with a known consequence rather than a silence. Nothing in the nine lanes addresses the mandate at all; lane I's distribution surface is a version and a description, with no statement of what the method is for or what forgoing it forfeits. The mark is Light. `minimum-viable-run`.

`onboarding` · ○ · topics: `obligation`

---

## P7 — The person who ran it once, got a horoscope, and never came back

Four items from the persona the method already lost — and the core document's Verification section records that three of them are P1's items at a later timestamp, with only item 51 separable because "Last time" sits in the ask itself. What survives that collapse is that all four ask the same thing in different words: give me a signal that this run is better than the one that burned me, before I spend another day on it.

#### 51 — "Last time it told me my users want reliability and ease of use. Why is this run any different?"

**The situation.** They ran it in March. It came back saying the users wanted reliability and ease of use, which they already knew and could have written on the train. Their manager is now asking them to run it again on a new service, and they are looking for a reason to say yes.

**Why it matters.** No answer means no second run — and the method never learns that it lost them, because they file no ticket and answer no survey. The roadmap then optimises for the people who came back and calls that demand.

**How it's answered today.** Lane A addresses it at the level of the run rather than the person: the pre-registration declares a predicted split and cut criteria before generation, and the Reckoning at the end reports what actually happened against them, so a second run carries something the first did not. What it leaves on the floor is whether that reassurance means anything. This run's own Verification section records that the pre-registration could not fail — the threshold was 2.5× the prediction and defined only on the dimension that did not move — so a run can report "well inside the threshold" while having measured the wrong axis. The mark is one of the 28 verified against source. `self-assessment`.

`onboarding` · ◐ · topics: `self-knowledge`, `trust-calibration`

#### 52 — "Show me one thing in here I'd have been surprised by."

**The situation.** They open the new document and scroll to the end first, looking for a single row they would not have written themselves. If they find one, they will read the whole thing. If they do not, they will close the tab, and that is the entire evaluation.

**Why it matters.** The surprise test is the only quality signal available to someone with no research training. It is also close to the right test — a demand-side document that contains nothing its reader did not already believe has, whatever else it did, changed no decision.

**How it's answered today.** Lane A requires the surprise test and puts it in a fixed place rather than leaving it to the reader: the pre-registration names in advance what would count as a surprise, and the Reckoning compares prediction against outcome at the end of the synthesis. The mark is one of the 28 verified against source. Its limit is recorded in this run's own Verification section: the threshold was set on the ✅ dimension while the movement occurred in ◐ and ○, so the machinery can honestly report no surprise because it was pointed at an axis that could not move. `self-assessment`.

`per-run` · ✅ · topics: `trust-calibration`, `self-knowledge`

#### 53 — "Was my first run bad because I gave it nothing, or because it can't do my domain?"

**The situation.** The first run had a thin README and a domain — clinical trial logistics — that the operator suspects no model has much signal for. Both explanations fit the horoscope they got back equally well, and the two imply opposite next actions.

**Why it matters.** User error is fixable in an afternoon and a domain gap is not fixable at all. Without the split they cannot decide whether trying again is rational, so they do the safe thing and never try, and the fixable case is lost along with the unfixable one.

**What would have to exist.** Two separable self-reports carried in the output: how much source the run actually had, and how much signal the executor had in this domain — kept apart, because they lead to different decisions. Neither exists. Appendix C records no input floor anywhere in the nine lanes, and it says lane A's gates before Phase 7 are advice addressed to the model being graded (`SKILL.md:618-622`) — which is the same model that would be reporting its own domain confidence. The mark is one of the 28 verified against source. `self-assessment`.

`onboarding` · ○ · topics: `trust-calibration`, `self-knowledge`

#### 54 — "Can this fail loudly instead of always producing a tidy document?"

**The situation.** The March run produced eleven tidy pages that were wrong in a way nothing about them announced. What they wanted, and did not get, was a run that stopped and said: this subject, this input, this executor — not enough, do not use what follows.

**Why it matters.** A method that never fails carries no signal, because a document is produced either way and the reader cannot tell the two apart. The tidy, plausible document is precisely what burned them, and it burned them for a month before they noticed.

**How it's answered today.** Lane B can fail a run: roughly 25 rules FAIL by default, and `--final` refuses a document with no Verification section, so not every output passes. What it leaves on the floor is failing for the right reason. Every one of those rules is about the document agreeing with itself; none is about whether it says anything — Caveat 2 confirmed by probe that a Verification section of five one-character lines exits 0, and Appendix C notes that even the enrichment pass's heading check agrees automatically because the heading is derived from the mark. A tidy, plausible, hollow document is the exact shape that passes. The mark is one of the 28 verified against source. `self-assessment`.

`per-run` · ⚡ · ◐ · topics: `self-knowledge`, `trust-calibration`

---

## P8 — The people the output claims to speak for, who were never asked

Three items, one distinct ask by the core document's own Verification finding, and no mechanism behind any of them — every one came back ○ or ◐. This is the only persona subjected to the method rather than using it, and the only one with no route into the document that describes them. The core document also argues, in its synthesis, that the method's sole evidence source is systematically blind to the population that writes least, which makes this the persona whose absence is hardest to see and most costly.

#### 55 — "Who decided I'm the 'frustrated junior admin', and where do I go to argue?"

**The situation.** A slide with their job title on it is shown at an all-hands. The label came from a document they have never seen, produced by a run nobody told them about, and it is now shorthand for how their team is discussed in planning.

**Why it matters.** The label drives product decisions about them with no route to contest a claim that was never put to their face. By the time it reaches them it has been repeated enough to be treated as established, and the burden of disproof sits with the person who was described.

**What would have to exist.** A route from the description back to the described: publication to the people named, and a recorded dispute that travels with the roster into whatever it feeds. Nothing in the nine lanes reaches outside the run — lane B checks a document against itself, lane G's adversarial pass is another reader of the same document, and lane I's distribution surface points the method at operators and never at the people it describes. The mark is Light. `contestability`.

`quarterly` · ○ · topics: `representation`

#### 56 — "It says people like me 'don't read the documentation' — is that an observation, or a stereotype the model already had?"

**The situation.** The line about not reading documentation appears in the persona description with no source beside it. The person it describes has read every page of that documentation twice, and now has to argue against a sentence that carries a research artefact's authority.

**Why it matters.** A prior about a job title hardens into a design constraint — fewer docs, more hand-holding, defaults chosen for someone who does not exist — and makes the product measurably worse for the people it claimed to describe.

**What would have to exist.** The same fourth provenance value item 17 asks for, applied to the sentence about them: a way to say that this claim is what the model already held about this job title. The core document notes that this ask is item 17 seen from the other side, which is the point — the executor cannot tell either, and lane B's abandoned lexical distinctness check is the measured evidence that the cheap version of the detector does not work (`verify.py:763-772`). The mark is one of the 28 verified against source. `prior-source-separation`.

`quarterly` · ○ · topics: `representation`, `provenance`

#### 57 — "This method never generates people like us at all — how would anyone ever notice we're missing?"

**The situation.** Nine personas, none of which is anyone in this cohort — people on slow connections, on old hardware, using a screen reader, working in a language the source was never written in. The document reads as complete to everyone who sees it, including the people who wrote it.

**Why it matters.** Absence is invisible inside a confident roster. The un-generated cohort is never served, never counted and never appealed, and there is no reader of the output who could detect the failure from the output.

**How it's answered today.** Lane A carries the whole of what exists: the deriver is instructed to name three classes a roster almost never contains, "because every evidence source you have is blind to them" (`SKILL.md:317-331`), and this run's roster gained exactly those three. What it leaves on the floor is detection. Appendix B reads that gain as the blind agent reproducing a checklist it was handed — evidence the instruction works, explicitly not evidence that an absent cohort was found — and no lane can notice a class the instruction did not name. The mark is Light. `absence-detection`.

`quarterly` · ⚡ · ◐ · topics: `absence`, `representation`

---

## P9 — The security, privacy, or compliance reader

Three items that are answerable from what already exists and that, by the core document's own account, nobody has asked. They are not questions about the roster's quality at all — they are questions about the run as a data-processing event, and the method currently records almost nothing about itself in those terms.

#### 58 — "What exactly did you feed the model — did any of it contain customer names, tickets, or transcripts?"

**The situation.** The reviewer picks up the roster during a routine check and asks the operator what went into it. The operator remembers a repo path, a paragraph of context, and thinks — but is not certain — that nobody pasted in the support export.

**Why it matters.** The answer determines whether this run was a disclosable transfer of personal data to a third party. A guess is not an answer to that question, and the guess is currently the only thing available.

**What would have to exist.** An input manifest produced *by* the run rather than reconstructed after it: what was read, what was passed to the model, and what was retained. Lane E is where the input discipline lives and Appendix C records it as having zero mechanical footprint — whether two agents shared context and whether Phase 3 leaked are not verifiable from the artifact — so the operator's recollection is the entire record. The mark is Light. `provenance-per-claim`.

`per-release` · ○ · topics: `provenance`

#### 59 — "Is 'persona' here doing the work of age, disability, income, or country?"

**The situation.** The reviewer reads nine personas and stops at two of them, where the described characteristics track closely onto attributes that would be unlawful to select on directly. Nothing in the document says whether the axis was chosen with that in mind.

**Why it matters.** A protected-class proxy inside a planning artefact is a discrimination exposure regardless of intent, and this artefact is upstream of roadmap and pricing decisions. Intent is not a defence and the document offers no record of the choice.

**What would have to exist.** A check that the declared roster axis is not standing in for a protected class, and a route for the people described to raise it when it is. Neither is in the inventory. The axis is a Phase 0 choice read by lane B as one of five canonical header declarations (`verify.py:330-357`), but lane B never checks what an axis *means*, and lane G's adversarial pass reads the document rather than the population. The mark is Light. `contestability`.

`per-release` · ○ · topics: `representation`

#### 60 — "Does anything from one subject's run persist into the next one's roster?"

**The situation.** The same method is being run for three customers in the same week, by the same operator, on the same machine. The reviewer wants to know whether anything from the first customer's confidential subject can surface inside the third customer's output, and is told that it does not.

**Why it matters.** Cross-tenant leakage in a planning artefact is a contractual problem before it is a technical one, and it is the kind of failure that is discovered by the customer rather than by the vendor. "Assumes not" is where the answer currently sits.

**How it's answered today.** Lane E is the answer and it is a protocol rather than a mechanism: blind calls sharing no context with the operator, Phase 3 containment, and a no-backward-flow rule that this enrichment pass is itself running under. That discipline is real and it is written down. What it leaves on the floor is evidence — Appendix C records lane E as having zero mechanical footprint, so nothing in the artifact shows whether one subject's material reached another run, and the reviewer is being asked to accept a description of how the run was conducted. The mark is Light. `provenance-per-claim`.

`per-release` · ◐ · topics: `provenance`, `comparability`

---

## What this pass noticed

Findings, not edits. Nothing here has been changed in `PERSONAS.2026-08-30.md`, and nothing from this pass flows backward into it.

- Four served items the inventory could not carry, all written to the mark as the format requires. Items 31, 39, 48 and 4 are the same four the core document's Verification section already records as over-graded, so this pass reproduces that finding from the other side rather than discovering it. In each case the ✅ was kept, the third block was written in the present tense, and the block says plainly which part of the claim the nine lanes do not support: item 31 has a declared roster axis but no extension surface, item 39 has a checker that reads finished documents but no partial-run semantics, item 48 has seed personas as an input but no mode that validates a supplied list, and item 4 has an instruction to name three absent classes but no absence detection. All four marks are Light, which means none of the four was verified against source in the scoped-Full pass.
- The Verification section's description of those four is slightly off on one of them, and the discrepancy is about a mark. It says items 39, 48 and 4 sit "against primitives marked *invented*". That is exact for 39 (`machine-contract`, invented) and 48 (`minimum-viable-run`, invented), but item 4's primitive is `absence-detection`, which carries an *inferred* mark sourced to `SKILL.md:317-331`. The finding stands either way — an inferred primitive supports a ✅ no better than an invented one — but a Verification section that grades marks should be right about them, and this is the same class of error as the ⚡ miscount it records two paragraphs earlier: a claim about a count or a label, stated in prose, that no checker reads.
- One capability claim in this pass rests on a derivation rather than on a recorded fact, and it is flagged here rather than buried. Items 7, 8, 25, 31 and 59 all say that lane B reads a particular header declaration as one of "the five canonical header declarations". Appendix C's Caveat 1 states that `parse()` reads five and that coverage depth is not among them, but it does not enumerate the five. The core document's header carries exactly five such lines — Tally, Frequencies, Roster axis, Pre-registered, Load-bearing persona — which is why the identification is confident, but it is inference from two facts and not something Phase 3 wrote down. A reader auditing those five items should treat it accordingly.
- P4 collapsed under enrichment, which is the core document's own finding arriving by a second route. Writing six independent scenes for items 34–39 produced six versions of one scene: a caller wanting a contract from something that does not offer one. Phase 7b reached this from the ask text; this pass reached it from the situations, which had to be differentiated by inventing six different pipelines rather than six different pressures. That is what an archetype-derived cluster feels like from the inside, and it is worth recording as corroboration.
- Item 12's ◐ looks generous once expanded. The ask is for the cheapest thing the operator could do tomorrow to prove one persona wrong; the only thing the inventory offers is one falsifier, for the top primitive, in the synthesis, which this document records as unrun. That is a different granularity, a different subject, and a different owner. It is not a proposal to change the mark — nothing here can — but the block was hard to write honestly at ◐, and the difficulty is the report.
- Two pairs of items are the same ask twice, confirmed by writing both. Items 17 and 56 are one question about the model's prior asked from inside and outside the executor, and the core document says so itself. Items 4 and 57 are one question about absence asked by the operator and by the absent cohort. Both pairs are already named in the Verification section as evidence of the P8 collapse; writing the scenes made the overlap concrete rather than lexical, because in each pair the two situations differ only in who is standing in the room.
- The frequency vocabulary problem is more visible in sixty footers than in one column. Every footer in this file prints a frequency pill, and `onboarding`, `per-incident` and `per-release` sit in the same slot as `many/day` and `daily` while describing a lifecycle stage, a trigger and a release cadence respectively. The core document logs this with Caveat 3 and its Verification section; it is recorded again here only because the enriched format multiplies the exposure — a detached reader meets that pill sixty times, which is why the header says once that the values are estimated.
