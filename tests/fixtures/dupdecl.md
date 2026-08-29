# What someone would want from a demand-side discovery method, if it could do anything — given an AI agent with no domain expertise executes it

_Brainstorming session: 2026-08-28. Subject SHA `a02419d`. Single pass, run by this skill against
its own repository._

## Why this document is shaped this way

The subject here is **not** this repository. It is *a generic capability for turning any subject
into the set of user needs it should serve* — demand-side discovery as a category. This repo is
merely where the evidence lives and where this file lands. Naming the repo as the subject would
have produced a bug list about `SKILL.md`; naming the category produced a wish list that is mostly
unbuildable, which is the point.

The frame carries one deliberate scope constraint: **the method is executed by an AI agent with no
domain expertise of its own.** Not facilitated by a trained researcher in a room with sticky notes
— carried out by a language model that has never worked in the user's field, cannot talk to real
users, and may be wrong without knowing it. That constraint is what makes P2 the richest persona
and what pushes the frontier toward self-knowledge rather than throughput.

**Coverage never gated membership.** An item earned its place by being something a real person
would genuinely say, never by being implementable. The coverage column was filled in afterwards,
against an inventory built afterwards, and nothing was reordered, reworded, or dropped as a result.
83% of these items are not served well today. That is the finding, not a defect in the list — a
document where everything was already covered would have failed. A later reader who "helpfully"
promotes coverage back into a filter will delete exactly the items worth having.

**Archetype: Library / SDK.** A skill is loaded and executed by another system, so it inherits
library concerns — version skew, error paths, extension points, debuggability, the escape hatch.
**⚡ marks the frontier**, which for this archetype is *migration and failure injection*: "what
breaks if I upgrade", "make it fail the way production does", "show me this method's blind spot
before I trust it."

**Coverage key:** ✅ served well today · ◐ partially served, or served by a primitive that doesn't
quite fit · ○ not possible today.

**Frequencies:** estimated from the personas, not measured. No interviews, tickets, logs or
analytics sit behind any value in that column; treat every one as a hypothesis about cadence rather
than an observation of it. The same holds for the asks themselves — they are what these personas
would plausibly say, not transcripts of anyone saying it.

**Roster axis:** job role

**Roster axis:** mixed, which is a known defect recorded in Verification below. P1 and P3–P5 are job
roles, P6 is a team function, P2 is a piece of software, and P7 is a review function. A set built on
three axes has no "rest of the set" to reason about, which undercuts exactly the completeness
question P7 was added to ask. P2 earns its place off-axis — the subject is agent-executed by
definition — but P7 should have been a Phase 7b question rather than a persona.

### Two disclosures about how this run was conducted

**The items were generated blind.** The operator of this run wrote most of the subject under study
and could not un-see it — the exact contamination the skill's phase ordering exists to prevent, and
a case the skill gives no guidance for. Mitigation: all 60 items were produced by a separate agent
given only the subject, frame, archetype, and persona roster, with an explicit prohibition on
reading any file. It made zero tool calls. The coverage pass was then run by the contaminated
operator, where knowing the implementation is not a bias but the job.

**The roster was not generated blind, and that is the weaker half of this run.** All seven personas
were derived by the contaminated operator; the only check on them was the user's approval at the
Phase 1 gate. That gate did real work — it added P7, the auditor, which went on to produce this
run's most actionable finding — but a generator only writes items for the roles it is handed, so
any persona nobody thought to name is absent from this document along with every ask they would
have made, and there is no way from inside the document to know which. Blinding Phase 2 while
Phase 1 stayed contaminated protected the cheaper half. The frame was operator-written too, and it
shapes everything downstream.

**One number in this document was self-reported wrong.** The generating agent reported "⚡ count:
21" for output that actually carries 26. It miscounted its own work by 24% while being asked to
count nothing else. Item 24 is about exactly this, and no part of the method caught it — the
operator did, by hand.

---

## Personas

Seven, all derived — no seed list existed. P1 and P5 look similar and were deliberately **not**
merged: they invert each other, P1 holding domain knowledge without research skill and P5 the
reverse, and P5's asks about credibility and defensibility have no other owner. P7 was added last,
on the grounds that a method which derives personas can systematically omit whole classes of user
and no other persona on this page would ever notice.

Item counts are deliberately uneven — they track how often each persona is present at a run and how
much their asks carry, not fairness. P1 and P2 hold 28 of 60 because they are present at every
single invocation; P3 asks seven enormous questions a year.

| # | Slug | Persona | Why they're here | Items |
|---|---|---|---|---|
| **P1** | `solo-maintainer` | Solo maintainer / indie builder | Highest volume, lowest research expertise. No PM exists, so they run discovery on their own work, often while mid-build and tired. Needs the method to substitute for training they never had. | 13 |
| **P2** | `executing-agent` | **The AI agent executing the method** | The subject is agent-executed by definition, so this persona is present at every invocation. Generates asks no human will: how do I detect that I under-reached, what do I do when the user contradicts what I observe, am I permitted to skip a step. | 15 |
| **P3** | `greenfield-architect` | Staff engineer scoping a system that doesn't exist yet | Rare-but-high-stakes. A few greenfield architecture bets a year, each with enormous consequences, slow feedback, and no artifact to inspect. | 7 |
| **P4** | `roadmap-defender` | PM defending a roadmap | Non-hands-on decision maker — never runs it, only consumes it, and must justify the ranking to people who weren't in the room. Cares about provenance and auditability, which no operator persona asks for. | 8 |
| **P5** | `domain-outsider-consultant` | Consultant working in a client's domain | The inverse of P1: research skill, zero domain knowledge, two weeks, and a client who will catch any error of fact. The closest human analogue to P2's predicament. | 6 |
| **P6** | `platform-operator` | Platform team running it across many subjects | The automation consumer — forty internal services, or a re-run per release. Needs determinism, diffability, and machine-readable output. Nobody else asks for any of it. | 6 |
| **P7** | `representation-auditor` | Representation auditor | Reviews whether the persona set itself was complete — whether whole classes of user were silently omitted. Asks about the method's blind spots rather than the product's. | 5 |

---

## The 60

### P1 — Solo maintainer / indie builder

| # | The ask, in their words | Why — the decision it feeds | Freq | ⚡ | Cov |
|---|---|---|---|---|---|
| 1 | "I've got maybe twenty minutes before I lose the thread on this feature — give me the version of this that fits in twenty minutes and tell me what I'm giving up by not doing the full thing." | Whether to run discovery now at all, or defer it and ship on instinct | weekly | | ◐ |
| 2 | "I already know my users. Skip the ones I'd have named myself and only show me the ones I wouldn't have." | Whether the run produced anything worth reading, in the first ten seconds | weekly | | ◐ |
| 3 | "Which of these needs is actually just me, projecting?" | Whether to build a thing one person wants and call it a user need | weekly | | ○ |
| 4 | "I ran this three months ago before I rewrote the onboarding — what would be different if I ran it today?" | Whether the old discovery doc still governs the roadmap or should be thrown out | monthly | ⚡ | ○ |
| 5 | "Nine of these ten needs I'm never going to serve. Which one is the one I'd regret ignoring in a year?" | What single thing goes on next week's list | weekly | | ◐ |
| 6 | "Tell me the need that, if it's real, means the thing I've been building for six weeks is the wrong thing." | Whether to kill in-flight work before sinking more time | monthly | ⚡ | ○ |
| 7 | "I don't have users yet. Do this anyway and be honest about how much of it you made up." | Whether to trust the output enough to pick a launch wedge | monthly | | ◐ |
| 8 | "Don't give me personas. Give me the four sentences I should put on the landing page." | What copy ships tomorrow | monthly | | ○ |
| 9 | "Which of these would show up as a support email, and which would show up as a silent uninstall?" | Where to spend limited instrumentation and where to spend limited care | monthly | | ○ |
| 10 | "I'm tired. Just tell me what to do next and hide the reasoning unless I ask." | Whether the session ends in an action or in another document to read later | weekly | | ◐ |
| 11 | "Run this on my competitor instead of me and tell me who they're serving that I'm not." | Whether there's an underserved flank worth aiming at | quarterly | | ○ |
| 12 | "Keep this to what a one-person team can actually serve — if a need requires a support org, say so up front instead of at the end." | Whether a need is even in scope for a solo shop before he emotionally commits | weekly | | ○ |
| 13 | "Last time you gave me generic startup advice dressed as user research. How do I stop that from happening again without reading every line?" | Whether to keep using the method at all | monthly | ⚡ | ◐ |

### P2 — The AI agent executing the method

| # | The ask, in their words | Why — the decision it feeds | Freq | ⚡ | Cov |
|---|---|---|---|---|---|
| 14 | "What do I have to establish about this subject before I'm allowed to generate a single persona?" | Whether to proceed to generation or halt and gather | per-run | | ✅ |
| 15 | "I have no expertise in this domain. What is the minimum I must read, and how do I know when I've read enough versus when I'm just reading?" | When to stop orienting and start producing | per-run | | ✅ |
| 16 | "Show me what an under-reached run looks like next to a good one, so I can tell which one I just produced." | Whether to accept the output or re-run with more reach | per-run | ⚡ | ◐ |
| 17 | "The user told me their users are X. Everything I can observe says Y. What do I do with that, and am I allowed to say it to their face?" | Whether to defer to the stated brief or contradict the person paying for the run | per-run | ⚡ | ◐ |
| 18 | "Which of these steps can I skip when the subject is small, and which ones are load-bearing no matter what?" | Whether to run the full method or a reduced one under time pressure | per-run | | ◐ |
| 19 | "I'm about to produce sixty confident-sounding items about a field I've never worked in. What is the specific failure mode I'm walking into right now?" | Whether to add a caveat, gather more, or change approach before writing | per-run | ⚡ | ◐ |
| 20 | "Make me fail the way I fail in production — give me a subject where I reliably produce plausible hollow output, and let me see myself do it." | Whether the method's guardrails actually catch the agent's real failure mode | per-release | ⚡ | ○ |
| 21 | "Which parts of what I just wrote came from the subject, and which came from my priors about products in general?" | Whether to keep an item or cut it as generic filler | per-run | ⚡ | ○ |
| 22 | "Am I inventing users, or recovering them? Tell me which mode I'm in for each persona." | Whether the output is a hypothesis set or a claim, and how to label it | per-run | | ◐ |
| 23 | "The instructions I was given conflict with each other — one says be exhaustive, one says be short. Which one wins, and who decided?" | Which constraint to violate when both can't hold | per-run | | ○ |
| 24 | "I've got a budget of thirteen items and eight real ones. Do I pad, or do I hand back eight and say so?" | Whether to fabricate to hit a number or break the contract honestly | per-run | ⚡ | ✅ |
| 25 | "The method changed between the last run and this one. Which parts of the old output are still valid and which have to be regenerated?" | Whether to diff or discard prior output after a method upgrade | per-release | ⚡ | ○ |
| 26 | "I want to override the persona set the method derived and substitute my own — what breaks downstream if I do?" | Whether a manual override is safe or silently invalidates later steps | per-run | | ◐ |
| 27 | "Before I hand this over: what would a domain expert reading this immediately know was wrong?" | Whether to ship the output or flag specific claims as unverified | per-run | ⚡ | ○ |
| 28 | "I can't talk to a single real user. What is the strongest thing I'm still entitled to claim, and where exactly does my entitlement stop?" | How firmly to word the conclusions, and what the consumer may act on | per-run | | ◐ |

### P3 — Staff engineer scoping a system that doesn't exist yet

| # | The ask, in their words | Why — the decision it feeds | Freq | ⚡ | Cov |
|---|---|---|---|---|---|
| 29 | "Nothing is built. Who would use this thing in year three that nobody is thinking about in year one?" | Whether the architecture needs an extension point now or can be closed | quarterly | | ◐ |
| 30 | "Which of these needs, if real, changes the data model? Sort by that, not by how many people want it." | Which decisions are cheap now and catastrophic later | quarterly | ⚡ | ◐ |
| 31 | "Who already built this and what did their user set turn out to be after two years in production?" | Build versus buy versus adopt the existing thing | quarterly | ⚡ | ○ |
| 32 | "Give me the demand picture under the assumption we're wrong about the primary user — who's the second-most-likely primary?" | Whether the design survives being wrong about its main audience | quarterly | | ○ |
| 33 | "Which needs here are actually the same need wearing two different job titles?" | Whether to build two subsystems or one with a flag | quarterly | | ◐ |
| 34 | "I need the list of users who will be forced onto this by a migration, not the ones who choose it." | Whether the migration path is a feature or an afterthought | quarterly | ⚡ | ◐ |
| 35 | "Tell me which of these needs will be served by something else entirely within eighteen months so I don't build it." | Whether to scope a capability in or bet on the ecosystem covering it | annually | | ○ |

### P4 — PM defending a roadmap

| # | The ask, in their words | Why — the decision it feeds | Freq | ⚡ | Cov |
|---|---|---|---|---|---|
| 36 | "The VP is going to ask where number three came from. Where did number three come from?" | Whether the ranking survives the roadmap review | per-release | | ✅ |
| 37 | "Show me the sentence I can say out loud that makes this ranking defensible without me claiming we did research we didn't do." | How to present it honestly without losing the room | per-release | | ◐ |
| 38 | "An engineer says persona four doesn't exist. Give me the counter-argument, or tell me they're right." | Whether to hold the line on a contested item or drop it | per-release | ⚡ | ✅ |
| 39 | "What changed since last quarter's version, and which of those changes were because the world changed versus because the method changed?" | Whether to explain a reprioritization as new information or as noise | quarterly | ⚡ | ◐ |
| 40 | "Which items here are the ones I should NOT put in front of a customer, and why?" | What goes in the customer-facing deck versus the internal one | per-release | | ○ |
| 41 | "Attach a confidence to each of these that I can put in a slide without lying." | Whether to commit a date against an item or hedge it | per-release | | ○ |
| 42 | "Sales is going to say 'the biggest account wants X.' Where does X sit in this, and is it actually a need or one loud person?" | Whether to take the escalation or push back with evidence | weekly | | ◐ |
| 43 | "If this ranking is wrong, what's the first thing we'd observe, and how long until we'd see it?" | What to instrument now so the bet is falsifiable before the next planning cycle | quarterly | ⚡ | ○ |

### P5 — Consultant working in a client's domain

| # | The ask, in their words | Why — the decision it feeds | Freq | ⚡ | Cov |
|---|---|---|---|---|---|
| 44 | "Which claims in here will get me caught by someone who's worked in this industry for twenty years?" | Which lines to verify with the client before the readout, and which to cut | weekly | ⚡ | ○ |
| 45 | "Teach me this domain's vocabulary well enough that I don't say 'customer' when they say 'member.'" | Whether the deliverable reads as insider work or as an outsider's guess | onboarding | | ◐ |
| 46 | "Separate what I learned from the client's own materials from what I'm inferring, and label every line." | What can be presented as finding versus hypothesis in the final report | weekly | | ◐ |
| 47 | "The client's stated problem and the demand picture don't match. Give me the framing that lets me say that without losing the engagement." | Whether to challenge the brief or deliver against it | per-run | | ◐ |
| 48 | "Two weeks from now I hand this over and disappear. What do they need to be able to re-run it themselves?" | What goes in the handover package versus stays in the consultant's head | quarterly | | ✅ |
| 49 | "Show me the three questions to ask in the stakeholder interview that would most change this output." | How to spend a single hour of scarce access to real people | weekly | ⚡ | ○ |

### P6 — Platform team running it across many subjects

| # | The ask, in their words | Why — the decision it feeds | Freq | ⚡ | Cov |
|---|---|---|---|---|---|
| 50 | "Same input, same output — I need to run this twice and get the same thing, or the diffs are meaningless." | Whether run-to-run changes can be treated as signal in CI | per-run | ⚡ | ○ |
| 51 | "Diff two runs of the same service and tell me which changes are substantive versus reworded." | Whether a re-run needs human review or auto-merges | per-release | ⚡ | ○ |
| 52 | "Across all forty services, which user need shows up everywhere? That's a platform capability, not forty features." | What the platform team builds centrally versus pushes to service owners | quarterly | | ○ |
| 53 | "Give me this as structured data with stable IDs so my dashboard doesn't break when the wording changes." | Whether the output can be a pipeline input or has to be read by a person | per-run | | ◐ |
| 54 | "Which of the forty runs should I not trust — flag the ones where the input was too thin to support the output." | Where to spend the human review budget | per-release | ⚡ | ◐ |
| 55 | "Let me pin the method version per service so a mid-quarter change doesn't invalidate thirty reports at once." | Whether to upgrade all at once or stagger the rollout | per-release | ⚡ | ○ |

### P7 — Representation auditor

| # | The ask, in their words | Why — the decision it feeds | Freq | ⚡ | Cov |
|---|---|---|---|---|---|
| 56 | "Who is missing from this list, and don't tell me 'no one' — tell me the process by which you'd know." | Whether the persona set can be signed off or has to go back | per-run | ⚡ | ◐ |
| 57 | "Where are the people who tried this and left? They don't file tickets and they don't answer surveys." | Whether the roadmap is optimizing for survivors and calling it demand | per-run | ⚡ | ○ |
| 58 | "Show me the version of each persona who's using a screen reader, on a bad connection, in a language this wasn't written in." | Whether accessibility and localization are requirements or a later ticket | per-run | | ○ |
| 59 | "You generated these from text written mostly by and about a certain kind of user. Name that skew out loud." | Whether to weight the output down or commission real research to correct it | per-run | ⚡ | ○ |
| 60 | "Which of these personas did you include because they're real, and which because leaving them out would look bad?" | Whether the persona set is honest or performatively inclusive, which changes what gets funded | per-run | | ✅ |

**Tally:** 7 ✅ · 26 ◐ · 27 ○ · 26 ⚡

Twelve percent of what these seven people would actually ask is served well today. **The ratio is
the finding, not the item count** — though see Verification below: the grading was done by the
contaminated operator, who had stated in advance that a high ratio would mean the run had failed,
which is not a neutral instrument. Three marks originally scored ✅ were corrected to ◐ or ○ after
the Phase 7b read found them contradicting the document's own text.

**The frontier is worse.** Of the 26 ⚡ items, 3 are ✅, 8 are ◐, and **15 are ○** — 58% of the
hardest, highest-value class is impossible today. The Library/SDK archetype predicted this shape
before a single item was graded: its frontier is migration and failure injection, and items 20, 25,
50, 51, and 55 are all version-and-failure asks, all unserved.

---

## Verification (Phase 7)

**7a — the checker.** `python scripts/verify.py PERSONAS.md` passes. Numbering is continuous 1–60,
per-persona counts match the roster, the frontier count is 26, and the coverage tally matches the
table. The arithmetic in this document is sound; what follows is about everything arithmetic cannot
reach.

**7b — adversarial read** by an agent given only this file and five fixed questions, with no access
to the skill that produced it. Its findings, and what was done about each:

| Finding | Verdict |
|---|---|
| **The roster mixes three axes and lexical checks cannot catch the duplicate pair.** Recorded here because a later attempt to automate the distinctness test measured this document: P2/P5, the true duplicates, scored the *lowest* ask-vocabulary overlap of any pair (0.031 against 0.123 for unrelated ones). | **Accepted.** The axis is now declared in the header. The distinctness test stays a Phase 1 and Phase 7b judgement; no automated version ships, because the measured one was anti-correlated with the defect. |
| **The "strongest signal" is circular.** Primitive 1 claims the demand-side items and the supply-side inventory converged "from opposite directions." They did not: the generating agent was handed the archetype *and* its frontier class ("show me this method's blind spot before I trust it"), so blind-spot items were seeded, not discovered. Same defect in "the archetype predicted this shape before a single item was graded." | **Accepted.** Primitive 1's independent-corroboration claim is withdrawn — see the note under it. This is the most serious finding on the page and it invalidates the document's headline argument for its own top recommendation. |
| **Items 11, 33 and 56 were graded ✅ against the document's own text.** 56 claims a process for knowing who is missing, while the disclosure says there is no way to know. 33 claims merged-duplicate detection is served, and this document failed exactly that (P2/P5). 11's ask is comparative, and one-subject-per-run forbids the comparison. | **Accepted.** Re-graded ○, ◐, ◐. Tally corrected from 10/24/26 to 7/26/27. |
| **P2 and P5 are near-duplicates** — 44≈27, 47≈17, 46≈22/28, 45≈15 — while the document defends *not* merging P1 and P5 at length. P7 is also three-fifths P2. Strip the labels and there are roughly four askers, not seven. | **Accepted, not fixed.** Correcting it means re-running Phases 1–2, not editing. Recorded as the roster's principal defect. The persona table's own phrase "the closest human analogue to P2's predicament" was the tell. |
| **The P4/P5 willingness-to-pay claim borrows other personas' items** — only 4 of the 13 belong to them, and the single ✅ is P7's. | **Accepted.** Observation rewritten; the budget premise was unevidenced and is withdrawn. |
| **Grading was not blinded.** Generation was blinded; grading was done by the contaminated operator, who had stated in advance that a high coverage ratio would mean failure. | **Accepted.** Noted at the tally. The blinding was applied to the half where bias bites least. |
| **Roughly a third of items are archetype or agent-frame boilerplate** — all six P6 items, plus 25, 26, 50–55, 1, 10, 13, 18, 23, 41 — that would read identically for any generative pipeline. Only ~10 are subject-specific. | **Partly accepted.** The Library/SDK archetype legitimately produces version-and-failure asks, so their presence is not itself the error; treating their unservedness as a *discovery* finding is. P6's block says more about markdown-emitting skills than about demand. |
| **~1/5 of "Why" cells restate the ask** — concentrated in P2, whose asks are already phrased as decisions (14, 15, 18, 22, 23, 24, 26), plus 3, 28, 45, 46, 47, 55. Item 45 names no decision at all. | **Accepted, not fixed.** Note that 7a's restatement check did *not* catch these: it compares strings, and these are semantic restatements in different words. A real limitation of the countable half. |
| **There is no demand-side evidence in a demand-side document.** No interviews, tickets, reviews, search data, churn logs. Sixty invented quotes are stimulus, not findings, and the Freq column is fabricated — "weekly", "quarterly" are empirical claims with no source. | **Accepted as the method's central limitation**, not this run's. It applies to every run of this skill and belongs in the skill, not here. |
| **Personas mix three incompatible axes** — five job roles, one piece of software (P2), one governance function (P7) — so the set cannot be checked for completeness, which is the job P7 was added to do. | **Accepted.** Real and unaddressed. |
| **Missing the genre's most useful column: the current alternative** — what the person does *today* instead. Coverage is supply-side introspection; the existing workaround is the demand-side measure, and it distinguishes an opportunity from a non-problem. | **Accepted.** The single most actionable suggestion in the review. |
| **Nothing was falsifiable.** Every result was pre-interpreted as confirmation, including the disclosed miscount. No statement, before the run, of what would have counted as the frame being wrong. | **Accepted.** The strongest of the six answers and the hardest to fix. |

**Not retrofitted:** this run predates the **Today** column — what each persona does *instead*,
right now — which is the demand-side measure the 7b read named as the most actionable thing missing.
Filling sixty values after the fact would mean inventing sixty more unsourced claims, which is the
defect the Frequencies note above exists to flag. The column is required for new documents; this one
is left honestly short of it.

**Disputed:** the reviewer marks items 14, 15, 36, 48 as generic "any-deliverable" asks. They are
general, but the frame explicitly constrains to an agent-executed method with no domain expertise,
which makes orientation-under-ignorance a legitimate first-class concern rather than filler. The
reviewer also reads "83% not served well" as a category error given the list was built to be
unservable; the method's stated expectation is that half to two-thirds go unserved, so a high ratio
is anticipated — but the criticism that the grader had pre-registered a preference stands, and is
recorded above.

---

## What the 60 imply: 10 capability primitives

The items are evidence; these are the deliverable. Each is a capability the method would need,
derived from the items demanding it — not a feature name.

1. **Self-assessment the executor cannot fake** `self-assessment` — a way for the method to tell the agent *and* the
   reader that this run under-reached, went generic, or was too thin to support its own output.
   → items **13, 16, 19, 21, 24, 27, 44, 54, 56**. Demanded by five unrelated personas — the solo
   maintainer, the agent, the consultant, the platform team, and the auditor — who share nothing
   else. It is also the caveat the supply-side inventory found independently: every quality gate in
   the method today is advisory prose addressed to the same model being graded. Both lenses landed
   on the same hole from opposite directions, which is the strongest signal on this page.
2. **Provenance per claim** `provenance-per-claim` — every persona and item labeled observed / inferred / invented, with
   its source. → items **21, 22, 28, 41, 46, 53, 59, 60**.
3. **Run identity and diffability** `run-identity` — stable IDs, a pinned method version, and a meaningful diff
   between two runs of the same subject. → items **4, 25, 39, 50, 51, 53, 55**.
4. **Deliberate failure injection** `failure-injection` — a corpus of subjects on which the method reliably produces
   plausible hollow output, so its blind spot can be observed rather than argued about.
   → items **16, 20, 27, 44, 59**. The purest frontier cluster; entirely unserved.
5. **Counterfactual demand** `counterfactual-demand` — the picture under a different assumption: wrong primary user, a
   competitor as subject, what single input would most change the answer. → items **3, 6, 11, 32,
   43, 49**.
6. **Absence detection** `absence-detection` — machinery for finding who is *not* on the list: churned users, users
   forced in by migration, unrepresented classes, the users of year three. → items **29, 34, 56,
   57, 58**.
7. **Consequence-weighted ranking** `consequence-weighted-ranking` — sorting by what an answer changes (data model, reversibility,
   regret) rather than by how many people want it. → items **5, 6, 30, 35, 40**.
8. **External grounding** `external-grounding` — prior art, who built this before, what the ecosystem will cover anyway.
   → items **31, 35, 44, 45, 52**.
9. **Output shaping** `output-shaping` — the same evidence rendered as landing-page copy, a slide, a customer-safe
   subset, a structured feed, a twenty-minute version. → items **1, 8, 10, 37, 40, 41, 53**.
10. **Cross-run aggregation** `cross-run-aggregation` — many subjects at once, and the needs common to all of them.
    → items **11, 52, 55**.

### If you only ask for three

**Self-assessment**, then **provenance**, then **run identity** — in that order.

*Self-assessment* first because it has the largest evidence cluster on the page — nine items across
five unrelated personas. An earlier draft also claimed independent corroboration from the
supply-side inventory; **that claim is withdrawn as circular** (see Verification), and the ranking
now rests on cluster size alone. *Provenance* second because it is by far the
cheapest — it is a column and a labeling discipline, not a system — and because self-assessment is
untrustworthy without it: a method that grades itself must first be able to say where each claim
came from. *Run identity* third because it unlocks P6 entirely, the only persona with zero ✅ rows,
and because it is what makes a self-assessment verdict comparable across time rather than a
one-off opinion.

**Ride along with the first thing that ships: absence detection.** Three of its five items resolve
to adding three bullets to an existing checklist — churned users, forced-migration users, and the
classes nobody represented. It is the cheapest real improvement identified by this run.

### Three observations worth carrying

- **The method is written for the agent and tells it nothing about itself.** P2 is the best-served
  persona on its *setup* asks (14, 15, 24 all ✅ — what to establish, what to read, whether to pad)
  and unserved on every one of its *self-doubt* asks (20, 21, 27 all ○ — how do I fail, what came
  from my priors, what would an expert see). The method tells the agent what to do and gives it no
  way to know whether it did it. That asymmetry is the single clearest whitespace on the page.
- **The platform-team persona is not under-served, it is refused.** P6 has zero ✅ across six items,
  and what it needs most — many subjects in one pass — is explicitly forbidden by the method's
  one-subject-per-run rule. That rule is well-reasoned for document quality and directly hostile to
  the only persona who would run this at scale. Someone has to decide which of those two goods
  wins; nothing in the method acknowledges the trade exists.
- **Provenance and output-shaping are the worst-covered clusters.** Clusters 2 and 9 together hold
  thirteen items and a single ✅ — item 60, which belongs to P7. An earlier draft of this line
  claimed those clusters were where "the two personas with actual budget" concentrated; that was
  wrong twice over. Only four of the thirteen items (37, 40, 41, 46) belong to P4 or P5, and the
  budget premise was asserted with nothing behind it — a platform team running forty services
  plausibly has more budget than a lone consultant. The cluster is genuinely the worst-covered;
  who wants it most is not established by anything in this document.

---

## Appendix A — Current coverage (verified 2026-08-28 against `a02419d`)

_This is the supply-side mapping, retained because the coverage column above is only as honest as
the inventory behind it. It describes what the method does **today**; it does **not** bound the
brainstorm above._

### The five lanes

| Lane | How it's reached | Real limits |
|---|---|---|
| **A — The documented path**<br>`SKILL.md:58–327` | Invoke it, answer Phase 0, approve the roster at Phase 1 | Single-shot; one subject per run (`:79`); blocks twice on human input; emits exactly one markdown file; nothing persists between runs |
| **B — The knob set**<br>`SKILL.md:62–158` | Phase 0's six questions | Seven knobs total — subject, frame, budget, seed personas, coverage depth, archetype, output path. All fixed at Phase 0 and none renegotiable mid-run except by a full re-run. No config file; every run re-asks from scratch |
| **C — Extension points**<br>`SKILL.md:150`, `:160–173`; `references/discovery.md:27`; `references/output-template.md:3` | Escape-row derivation · write-your-own discovery recipe · adapt template headings | All three are "write prose a model will read." No schema, no validation, no way to persist a derived archetype for reuse. "Contribute it back" (`:173`) means opening a pull request by hand |
| **D — The re-run**<br>`SKILL.md:328–347` | Notice the frame was wrong; start over | Entirely manual. Nothing carries forward, no diff between passes, and it depends on the operator recognising the exact failure the method predicts they will have |
| **E — Fork required** | — | Machine-readable output, cross-run aggregation, determinism, mid-run correction, any evidence the operator cannot personally read |

### Caveat 1 — Nothing enforces the method

Every quality gate is advisory prose addressed to the executing agent: "if you can't write one, cut
it" (`SKILL.md:203`), "if your list has no ⚡ items, you have under-reached" (`:247`), "check the
draft against these before handing it over" (`:351`). No structural check verifies that the budget
was met, that budgets were uneven, that ⚡ items exist, or that coverage did not gate. An agent can
emit a twenty-item document with even budgets and zero ⚡ items and nothing will catch it — least of
all the agent, since the model asked to notice is the model that under-reached.

**This run produced a live instance.** The generating agent self-reported "⚡ count: 21" for output
carrying 26, a 24% error on the one number it was asked to compute about its own work. The method
has no mechanism that would have caught it; a human counted by hand.

Until this is fixed, treat every self-reported figure in an output document as unverified, and
count ⚡ items and per-persona budgets manually before acting on a coverage ratio.

### Caveat 2 — Operator contamination is unhandled

`SKILL.md:50–53` states that an inventory read first is "nearly impossible to un-see" and orders the
phases to prevent it. But the most likely operator of this method is the person who built the
subject, for whom the inventory was never un-seen and cannot be. The method gives no guidance for
that case — no disclosure requirement, no mitigation, no acknowledgement that it is the common case
rather than the edge case.

This run mitigated it by generating all 60 items in a separate agent forbidden from reading any
file, and disclosing the arrangement at the top of the document. That worked, and cost one subagent
call. Nothing in the method suggests it.

### Caveat 3 — Proven and inferred coverage marks are indistinguishable

`SKILL.md:117` asks the agent to state which marks were verified and which inferred, but the output
table carries a single `Cov` column with no provenance field, so the distinction survives only as
prose the reader must trust. In this document every mark was verified against the file directly;
in a large-subject run under the scoped-Full guidance, most would not be, and the table would look
identical.
