# What someone would want from a demand-side discovery method, if it could do anything — what they can't stand about it

_Adversarial pass over `PERSONAS.2026-08-30.md` (2026-08-30). Reads that document and its appendix;
changes nothing in it._

**Only the `observed` entries are reported complaints.** Each grievance carries an `observed`,
`inferred` or `invented` mark, and the last two are both reconstructions — one reasoned from
something real, one not. Each mark says which part of its entry the source covers and which part
was reconstructed around it.

This pass is unusual in one respect worth stating up front: an unusually high share of its
grievances are `observed`, and they were observed **during the run that produced the core
document**. The subject is the method, the operator was executing the method, and so the operator
*was* several of these personas for the duration. Where an entry says `observed`, it means the thing
happened in this session and can be pointed at. That is a real advantage of dogfooding and also its
characteristic bias: the operator-shaped personas have evidence and the others do not, which is
exactly the survivorship problem P7 and P8 exist to name.

**Coverage depth:** Full, scoped — copied from the core document. A scoped Full run leaves some
lanes Light, so this is the run's depth and not any single lane's. Each grievance names the status
of the lane it cites. Lanes A, B, E, H and I were verified against source; C, D, F and G are Light,
built from the reference files rather than checked, and a grievance resting on one of those rests on
a reading of documentation that nobody probed.

**Carried from the core document's Verification section:** Phase 7b found three arithmetic errors,
all fixed — a primitive falsely called the largest cluster on the page, one item cited by two
primitives, and an appendix claiming ten WARN rules while enumerating eight. It found the cut rule
declared and not applied, with roughly 24 of 60 items surviving it and the whole of P4 derived from
the archetype label rather than the subject. It found P7 indistinguishable from P1 at a later
timestamp, and P8 carrying one distinct ask across three rows. It found four ✅ marks contradicting
their own primitives, and that the 28 Full-verified items are exactly the items behind the three
primitives the document promotes, so verification effort followed the conclusion. It found the
pre-registration's surprise threshold set only on the ✅ dimension at 2.5× the prediction, so it
could not fire for the movement that occurred. Two findings were disagreed with and recorded as
disagreed: that a ⚡ item marked ✅ is a contradiction in terms, and that P8 does not belong on a
demand roster. **The personas below are the ones that section questioned, and their grievances
should be read knowing it.**

---

## P1 — The person who points the method at their own subject, once

Both grievances are the same shape: the tool told them something confident and wrong about their own
document, and in each case the wrongness was in the direction of making them doubt work they had
actually done.

#### P1-1 — "It told me I forgot the evidence mark. I did not forget the evidence mark. It's right there."

**About:** Lane B — the mechanical checker; Appendix C marks this lane **verified**.
*(observed: this happened during the run that produced the core document. `verify.py` reported "1 primitive(s) carry no evidence mark: 'Provenance per claim'" for a primitive whose mark was present and correctly formed. The cause is Caveat 5: `MARK_RE` captured the source with `[^)]*`, so a closing parenthesis inside the source text ended the capture early. The failure, its cause and the
message text are all sourced. What is reconstructed is the operator's reaction below — nobody
recorded how a user responds to this, only that the message misdiagnoses.)*

**Kind:** it's wrong.

**What they expected.** That a checker reporting a *missing* thing means the thing is missing. The
message names an absence — "carry no evidence mark" — and gives no hint that a mark was found and
could not be parsed.

**What it costs.** *(reconstructed.)* The obvious response to "you have no mark" is to add a mark.
Doing that produces two marks on one primitive, which `output-template.md:94-95` calls "an error,
not a choice." So the tool's diagnosis steers the fix toward a second error, and the operator's
confidence in their own correct work is what pays for it. The specific text most likely to trigger
this is a quotation of the checker's own output, because those messages contain `primitive(s)` —
and citing what the checker reported is exactly the auditable provenance the method asks for.

**What would fix it.** Not a new capability: a balanced-paren capture, and a distinct message for
"a mark was found but could not be parsed." One sentence of the second kind would have made this
a non-event.

#### P1-2 — "I'd already answered seven questions about my frame before anything told me the budget I picked would wreck the comparison."

**About:** Lane A — the protocol prose; Appendix C marks this lane **verified**. *(observed:
`SKILL.md` Phase 0 asks for the item budget at step 3, and `references/cross-run.md:56-62` — which
states that subject, frame, budget, archetype and coverage depth must all be held constant for a
re-run to be comparable — is reachable from Phase 0 only through a parenthetical in step 1. The
ordering is sourced. Whether a real operator has been burned by it is not; no ticket records one.)*

**Kind:** it surprises.

**What they expected.** That the phase which tells you what to ask would also tell you what
constrains the answer. Phase 0 reads as self-contained — seven things, ask the user directly — and
nothing in it flags that a subject with an existing document has extra rules living in another file.

**What it costs.** *(reconstructed.)* An operator who asks the seven questions in order, lets the
user pick 80 because doubling sounds like reaching further, and reads `cross-run.md` afterwards has
already destroyed comparability with every prior run of that subject, and will not find out until
the synthesis. The cost is a full re-run, and the person who pays it is the one who followed the
instructions in the order they are written.

**What would fix it.** A sentence in Phase 0 step 3: if a prior document exists for this subject,
read `references/cross-run.md` before asking.

---

## P2 — The AI agent that carries out the method

Both are about the gap between what the method *says* is a rule and what any mechanism actually
holds it to — and the executor is the one persona positioned to notice, because it is the party
being graded.

#### P2-1 — "I'm told to run two agents that share no context and read no files, and nothing anywhere ever checks that I did."

**About:** Lane E — the isolation protocols; Appendix C marks this lane **verified**. *(observed:
`SKILL.md:60-106` specifies the two-call blind generation in detail, and the enforced-versus-advice
map in Appendix C records that the entire protocol has zero mechanical footprint — no check reads
whether two agents shared context, whether the file prohibition held, or whether Phase 3 findings
leaked into either prompt. Both the instruction and the absence of any check on it are sourced. The
consequence below is reconstruction.)*

**Kind:** it surprises.

**What they expected.** That the method's most elaborate and most load-bearing procedure — the one
its own README leads with — would leave some trace that it ran. Everything else the executor is
asked to do produces an artifact the checker inspects.

**What it costs.** *(reconstructed.)* An executor that skips it produces a document
indistinguishable from one that did not, including to `--final`. The honest executor and the lazy
one are rewarded identically, and the only person who can tell them apart is the operator, who is
also the one who would have skipped it. Over time the protocol becomes something documents *claim*
rather than something runs *do*, and nothing in the artifact would ever reveal the transition.

**What would fix it.** Small and partial: a required header line declaring how Phases 1 and 2 were
generated — blind two-call, single-context, or disclosed contamination — checked for presence and
substance the way `**Frequencies:**` is. It cannot verify the claim, but it makes the claim explicit
and auditable, which is the same trade `provenance-per-claim` makes everywhere else.

#### P2-2 — "Ten of the things it calls rules are warnings I'm never told to turn on."

**About:** Lane B — the mechanical checker; Appendix C marks this lane **verified**. *(observed:
Appendix C enumerates ten rules stated as rules in the method that ship as WARN, each with a
`file:line` — uneven budgets, ⚡ placement, the tally stating a ⚡ count, every item graded, at most
half served, frequency vocabulary, Why restating Ask, asks quoted as speech, 6–12 primitives, and
slug presence. `SKILL.md:631` presents `--strict` as optional and no documented invocation uses it.
Sourced. What it costs an executor is reconstruction.)*

**Kind:** it refuses.

The refusal is quiet: the checker declines to enforce rather than announcing a limit.

**What they expected.** That "the checker checks X" and "X is a rule" would be the same statement.
The method's own framing invites this: Phase 7 opens by saying every gate before it is advice
addressed to the model being graded, which implies Phase 7 is where advice becomes enforcement.

**What it costs.** *(reconstructed.)* The rules that ship as WARN are precisely the qualitative ones
— quoted asks, Why not restating Ask, uneven budgets. Those are the rules that separate a document
with 60 real asks from one with 60 Jira titles, and they are the ones an executor under pressure
drops first. Phase 7b on the core document found the Why-restates-Ask failure in eleven items; 7a
had passed the same document at zero warnings, correctly, because that rule is a WARN.

**What would fix it.** Either promote them, or say plainly in `SKILL.md` which rules the checker
does not hold you to, so the executor knows what it is on the hook for. The second is cheaper and
almost as useful.

---

## P3 — The repeat user who tunes, forks, or upgrades the method

Both are about comparability being promised at the level of philosophy and withheld at the level of
mechanism.

#### P3-1 — "The version has said 0.1.0 through every change that moved the ground under my last four runs."

**About:** Lane I — distribution and invocation; Appendix C marks this lane **verified**.
*(observed: `.claude-plugin/plugin.json` and `marketplace.json` both pin `0.1.0`, with no changelog
and no compatibility statement, while 17 commits landed between the two passes compared in the core
document — adding the enrichment pass, the adversarial pass, three reference files and a 1,845-line
checker. Version, absence of changelog and commit count are all sourced. The four runs are
illustrative reconstruction; no user's run history was inspected.)*

**Kind:** it surprises.

**What they expected.** That a method whose own `cross-run.md:120-126` says *"if the skill itself
changed between the runs, some movement is method drift and some is real — say which is which"*
would give them the means to say which. The instruction presumes a version they can name. Nothing
emits one.

**What it costs.** *(reconstructed.)* A quarterly series becomes four unrelated snapshots that look
like a series. The failure is silent and it is worse than no comparison, because the operator will
report movement upward as a market shift — item 26 in the core document is this persona saying so in
their own words, and it came back ◐.

**What would fix it.** A method version stamped into the document header at generation time. That
is the `run-identity` primitive from the core document's synthesis, and it is the cheap half of it.

#### P3-2 — "The one check that would keep my slugs comparable runs only inside the skill's own test suite. It doesn't ship."

**About:** Lane H — the cross-run machinery; Appendix C marks this lane **verified**. *(observed:
the slug-vocabulary equality check exists at `tests/run_fixtures.py:1237-1244` and compares this
repository's own `PERSONAS.md` against `references/primitives.md`. `verify.py` treats slug presence
as a WARN at `:879-883` and has no vocabulary check at all. Both are sourced by direct reading. The
downstream consequence is reconstruction.)*

**Kind:** it's wrong.

The capability appears to exist and does not, for anyone outside this repository.

**What they expected.** That `primitives.md:35-38`, which warns that minting without recording means
"the next subject reads the vocabulary, does not find it, and mints a synonym," would be backed by
something that notices. The file describes the failure precisely and then relies on the operator to
avoid it.

**What it costs.** *(reconstructed.)* Exactly the failure the file describes, and it is undetectable
from any single document. Two runs name the same capability differently, never group, and the
platform team concludes there is no shared need. The core document's own run illustrates the shape:
five slugs were minted, and under the decision recorded there, none were written anywhere a later
subject would read.

**What would fix it.** Ship the check. A `--vocabulary PATH` flag doing what
`run_fixtures.py:1237-1244` already does would move it from this repo's CI into every user's run.

---

## P4 — The program or agent that calls the method as a step

One grievance, and Phase 7b's finding about this persona should be read alongside it: P4 was derived
from the archetype label rather than from the subject, so treat its thinness here as corroboration
rather than coincidence.

#### P4-1 — "Exit 0 means the document agrees with itself. I had been reading it as 'the document is good.'"

**About:** Lane B — the mechanical checker; Appendix C marks this lane **verified**. *(inferred:
Appendix C states the trust boundary — the checker verifies document self-consistency and
cross-document consistency and never checks anything about the subject — and records thirteen stated
rules with no mechanical footprint. The boundary is sourced. That a calling program would misread
the exit code is reasoning about a consumer this method has never had, and nothing observed sits
behind it.)*

**Kind:** it surprises.

**What they expected.** That a zero exit from a validator gates on quality. Every other checker in a
build does.

**What it costs.** *(reconstructed.)* A pipeline that gates on `verify.py` is gating on internal
consistency and reporting it as validation to everything downstream. A fabricated roster with a
correct tally line passes; the core document's own Caveat 1 shows a Full-depth document passing
`--final` with its entire evidence appendix deleted.

**What would fix it.** A line in the checker's own output naming what it did not check. It already
prints four informational lines before its verdict; a fifth saying "self-consistency only — coverage
marks, citations and isolation are not verified" would cost nothing and would travel with every run.

---

## P5 — The decision maker who never runs it, only ships its output onward

#### P5-1 — "It said PASS, so I forwarded it. Then someone in the room asked where the evidence appendix was."

**About:** Lane B — the mechanical checker; Appendix C marks this lane **verified**. *(observed:
confirmed by probe during this run. The core document's pass-1 predecessor, truncated at its
appendix heading, passes `verify.py --final` at exit 0 while still claiming a tally of 7 ✅ · 26 ◐ ·
27 ○ — sixty graded marks with nothing left in the file to ground one of them. The probe and its
result are sourced; the boardroom scene is reconstruction and no such meeting is recorded.)*

**Kind:** it's wrong.

**What they expected.** That a document which passed its own validator would not be missing the
section its central claim rests on. This persona never runs the tool and has no way to check —
`PASS` is the entirety of what reaches them.

**What it costs.** *(reconstructed.)* Trust, and asymmetrically: the sponsor is the persona who
carries the output into rooms where they cannot recover if it is wrong, and they are the persona
furthest from any means of verifying it. The core document's items 40 and 45 are this person asking
for provenance and for evidence a human looked; both came back ◐.

**What would fix it.** The root cause is structural, not a missed branch: `parse()` reads five
canonical header declarations and coverage depth is not among them, so the checker cannot tell a
legitimate depth-None run from a Full run whose inventory was dropped. A `**Coverage depth:**`
header declaration on the same one-address rule as `**Frequencies:**` closes it.

---

## P6 — The person made to run it by a mandate, standard, or vendor change

#### P6-1 — "I was told to run this for rigour. Its own documentation says every gate before the last one is advice to the thing being graded."

**About:** the expectation gap cites a promise, not a lane. The promise: `README.md` sells the output as "the document that tells you which whitespace is real", and nothing beside it says a passing run establishes nothing about the subject. *(observed: `SKILL.md:618-622` states it directly — "every quality gate before this point is advice addressed to
you, and you are the one being graded" — and gives the reason, that the model which under-reached is
the model being asked to notice it under-reached. The sentence is sourced. The mandate, and this
persona's reaction to reading it, are reconstruction.)*

**Kind:** the expectation gap.

The belief that running this constitutes rigour comes from the framing that gets it mandated, not
from any sentence claiming enforcement.

**What they expected.** That being required to run something meant the requirement was buying
verification. Nobody who mandates a process expects its core to be self-assessment by the party
being assessed.

**What it costs.** *(reconstructed.)* The conscripted operator is the persona least motivated to
supply the honesty the method depends on, and the method's protections against a dishonest run are
the ones with no mechanical footprint. So the mandate produces exactly the artifact it asked for and
none of the assurance it wanted, and the operator who noticed this is now certain their week was
theatre — which is the belief that turns into quiet non-compliance on the next cycle. Core item 50,
"what actually happens if I just skip this," came back ○.

**What would fix it.** Honesty in the framing rather than a new mechanism: a short statement of what
a passing run does and does not establish, positioned where someone deciding to mandate it will read
it. The candour already exists at `SKILL.md:618-622`; it is 618 lines in.

---

## P7 — The person who ran it once, got a horoscope, and never came back

Phase 7b found this persona indistinguishable from P1 at a later timestamp. The grievance below is
nonetheless the one P1 cannot have, because it requires having already stopped trusting the output.

#### P7-1 — "It passed my document with five letters in the section that was supposed to prove somebody read it."

**About:** Lane B — the mechanical checker; Appendix C marks this lane **verified**. *(observed:
confirmed by probe during this run. A Verification section whose entire body is `x` / `y` / `z` /
`a` / `b` passes `--final` at exit 0; the same document with a one-line body fails. The threshold is
a non-empty line count and it is exactly five, at `verify.py:1818-1824` and `:1402-1405`. Probe,
threshold and code locations are sourced. This persona's history with the tool is reconstruction.)*

**Kind:** it's wrong.

**What they expected.** That `--final`, the mode whose entire added job is requiring the Verification
section, would require the section to contain verification. `SKILL.md:673-676` says an absent
verification section reads as a passed one — the check exists precisely to stop that.

**What it costs.** *(reconstructed.)* This is the persona defined by having received a plausible,
tidy, empty document and believed it. The gate that exists to catch exactly that failure is
satisfied by five characters. For someone with no research training, `--final` passing *is* the
quality signal; there is no other one available to them. The comment at `verify.py:1815-1817` states
the intent — "require enough substance to have carried them" — which makes this a gap between
intent and implementation rather than an oversight.

**What would fix it.** `is_substantive()` already exists at `verify.py:129-150` and would reject
`x`. Applying it per line raises the bar from five keystrokes to five sentences without pretending
to judge content.

---

## P8 — The people the output claims to speak for, who were never asked

One grievance. Phase 7b argued this persona does not belong on a demand roster and the core document
disagreed, on the ground that a roster which drops the people it speaks for because they are not
customers is the omission the instruction exists to prevent. The entry below is the strongest form
of the case, and it is an expectation gap because there is no lane to cite — which is itself the
finding.

#### P8-1 — "The method promises somebody will ask whether people like us were left out. Nothing anywhere checks that anyone did."

**About:** the expectation gap cites a promise, not a lane. The promise: `SKILL.md:326-331` instructs the deriver to name "the classes nobody represented" and to "ask explicitly, and if you conclude none belong on the page, say why rather than leaving it silent." *(observed: the instruction is sourced by direct reading, and Appendix C's
enforced-versus-advice map records that no check reads whether it was followed — the roster is
checked for duplicate ids, budget arithmetic and slug shape, never for whether the question was
asked. Both halves sourced. The cohort's reaction is reconstruction, necessarily: this persona files
nothing by definition.)*

**Kind:** the expectation gap.

**What they expected.** That an explicit instruction to check for their absence, written in the
method's own voice and given its own paragraph, would be worth more than an instruction to check for
duplicate persona ids. One of those is enforced.

**What it costs.** *(reconstructed.)* The asymmetry is the whole grievance. A roster that omits this
cohort is mechanically indistinguishable from one that considered and excluded them with a stated
reason, and both pass at zero warnings. The absence is invisible in the artifact, invisible to the
reader, and invisible to the cohort, who never see the document. Core item 57 — "how would anyone
ever notice we're missing?" — is this persona asking the question the method's own tooling cannot
answer, and it came back ◐ against an instruction that is real but unenforced.

**What would fix it.** A required header line, in the same family as `**Roster axis:**`, declaring
that the unrepresented-classes question was asked and stating the answer. It cannot verify the
answer is honest. It makes silence impossible, which is the specific failure here — the method
already accepts that its declarations are claims rather than proofs, and this claim is currently the
only one it does not require.

---

## P9 — The security, privacy, or compliance reader

#### P9-1 — "The isolation protocol is the control I would rely on, and it is the one thing here that leaves no evidence at all."

**About:** Lane E — the isolation protocols; Appendix C marks this lane **verified**. *(inferred:
Appendix C records that Lane E has zero mechanical footprint, and `SKILL.md:98-102` requires that
nothing from Phase 3 reach either generating prompt. Both sourced. That an assurance reviewer would
treat this as the control worth auditing is reasoning about a reader this method has not yet had,
one step from the documented absence rather than from anything observed.)*

**Kind:** it refuses.

What it refuses is evidence: there is nothing to audit.

**What they expected.** That a documented control would produce an artifact. This is the ordinary
expectation an assurance function brings to anything: not that the control is perfect, but that its
operation is evidenced.

**What it costs.** *(reconstructed.)* Nothing in the output distinguishes a run whose blind agents
were genuinely isolated from one where the operator wrote both halves. Core item 60 — "does anything
from one subject's run persist into the next one's roster?" — is this persona's cross-tenant
question, and it came back ◐ resting on an instruction rather than a boundary. The core document's
own contamination disclosure is a paragraph the operator wrote about themselves, which is the
correct thing for it to be and is not evidence.

**What would fix it.** The same declaration P2-1 asks for, which is why this converges: a header
line naming how Phases 1 and 2 were generated, present and substantive or the run fails. It records
what was claimed. It cannot record what was done.

---

## What this pass found

**Grievances that converge.** Six of the eleven cite **Lane B**, the checker, and they resolve into
one shape rather than six complaints: *the tool reports on a narrower thing than its output implies*.
P1-1 misdiagnoses a present mark as absent, P5-1 passes a document missing the evidence its claims
rest on, P7-1 passes a Verification section containing nothing, P4-1 returns an exit code that reads
as quality, P2-2 declines to enforce ten rules the method calls rules. Each is individually a small
defect. Together they are the trust problem the *it's wrong* filter exists to make visible: the
checker is excellent at what it does and silent about its boundary, and every one of these
grievances is someone discovering the boundary the hard way.

**Two grievances converge on a single fix**, which is the strongest thing this pass can find. P2-1
and P9-1 — the executor and the assurance reader, who share no other concern — both ask for a header
declaration naming how Phases 1 and 2 were generated. P8-1 asks for a structurally identical
declaration about the unrepresented-classes question. All three are the `provenance-per-claim`
primitive from the core document's synthesis, applied to the method's own procedure rather than to
its findings, and all three cost one header line each.

**Personas with nothing.** None were empty, which is itself suspicious and worth saying plainly. The
counts are lopsided in the direction the dogfooding bias predicts: P1, P2 and P3 — the operator-shaped
personas the executing operator effectively *was* during the run — carry the `observed` marks, while
P4 and P9 carry the only two `inferred` entries and no observed evidence at all. P4's thinness
corroborates Phase 7b's finding that the persona was derived from the archetype label. A pass run by
someone who was not simultaneously the operator would likely produce the opposite distribution, and
would be more useful for it.

**What it says about the core document.** Findings only, and the core document is unchanged.

- **Item 25's ✅ looks less defensible from here.** The core document marks it served because
  pre-registration exists, and disagreed with Phase 7b about it. P2-2 shows why the mark is
  generous: pre-registration is enforced, but the surrounding self-check rules that would make it
  meaningful ship as WARN. ◐ would be the honest mark. Recorded, not changed — nothing this pass
  produces flows backward.
- **Caveat 4 is confirmed.** The core document listed the adversarial `About`-block parsing bug as
  unverified pending a conforming adversarial document. This is that document, and the bug
  reproduces decisively. Probe: take P5-1's `About` block, change nothing but move one line break
  one word earlier so the status word `**verified**` falls on the second physical line. The checker
  then reports *"1 grievance
  name no verification status for the lane they cite: P5-1."* Same words, same lane, same status,
  valid markdown, identical rendering — and a FAIL. `verify.py:1543` stores each block's value as
  the remainder of its own label line, while the empty-block check on the same loop reads the full
  block and the evidence mark reads to the next blank line: one entry, three parsing extents.
  **This is the most severe defect found in this session, because it fails a correct document** —
  and `adversarial.md`'s own worked example wraps its heading across two lines, because these lines
  are long. Recorded here and deliberately **not** written back into the core document's Caveat 4:
  nothing an optional pass produces flows backward, and a pass that resolves the document it read
  is the containment rule broken at its easiest point.

- **Caveat 5 bit three times while this file was being written, twice inside the entry documenting
  it.** The `About` mark for P1-1 first quoted the checker's message, which contains `primitive` in
  parenthesised-plural form; rewording that, the mark then quoted the offending regex itself, which
  contains a closing parenthesis by construction. Both times the checker reported the grievance as
  carrying *no* evidence mark. **The bug cannot be documented inside its own evidence source**, and
  the workaround is to describe the regex in prose rather than quote it — which is precisely the
  loss of auditable citation the evidence-mark scheme exists to prevent.
- **An ask that turns out to be a grievance in disguise.** Core item 54 — "can this fail loudly
  instead of always producing a tidy document?" — reads in the core document as a wish for a
  capability. P7-1 shows it is a grievance about a lane that exists: `--final` does fail loudly, and
  it passes five characters. The ask is not that the failure mode is missing; it is that it is
  present and hollow.
