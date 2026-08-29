# Worked example — the run this skill came from

The skill was extracted from a real brainstorm over a **DDI estate** (DNS, DHCP, IPAM — a BlueCat
Address Manager deployment) reached through a generated CLI with an MCP server. Read this when you
want to see the phases run end to end on a concrete subject, or when your own subject is a Read
surface and you want a calibrated sense of what "good" looked like. Nothing here is normative; the
lessons in `../SKILL.md` are.

Archetype: **Read surface.** Discovery recipe: `discovery/printed-cli.md`.

---

## Phase 0 — how the subject was named

The first pass named the subject as *"the bamcli MCP server"* and produced a small document that
read like a backlog for bamcli. The second pass named it:

> *a generic read-only MCP server capable of reading BlueCat Address Manager*

Same estate, same personas, an entirely different document. The generic phrasing gave every persona
permission to want something nobody had built — which is the whole exercise. **This is the single
highest-leverage sentence in a run**, and the most common thing to get wrong.

The frame that followed:

> *what would a DDI practitioner ask a **read-only** MCP server over BAM, if it could answer
> anything?*

The bolded scope constraint (`read-only`) sharpened every item downstream: it ruled out the entire
class of "and then change it" asks, which forced the frontier class into simulation instead. Budget:
60 items. Coverage pass: **Full**.

---

## Phase 1 — what the roster gained

The seed list was network-engineer-shaped. What the derivation added, and why each mattered:

| Added persona | Why it earned a place |
|---|---|
| The service-desk tech | Highest volume, lowest expertise — benefits most from a natural-language interface, and generated the highest-frequency items on the page |
| The security/compliance reader | Their data was already sitting in the estate, entirely unqueried. Pure whitespace |
| The automation/pipeline consumer | Asks in a completely different shape: idempotence, freshness guarantees, machine-readable provenance |
| The migration/acquisition lead | Rare, enormous, once-a-year asks — and the source of several of the best items |
| **The AI agent itself** | The most productive single addition. Generated asks no human persona will: *what must I read before I'm allowed to act*, *how fresh is this answer*, *what am I entitled to see*, *what would this change touch* |

Two seed personas turned out to be the same human under two job titles and were merged.

Budgets were deliberately uneven — the service-desk tech got many small daily items, the migration
lead got a handful of enormous annual ones.

---

## Phase 2 — what the items looked like

Good, in the persona's voice, with the decision named:

| The ask, in their words | Why — the decision it feeds | Freq |
|---|---|---|
| "Who was on 10.20.5.66 at 14:20 yesterday?" | Attribution for abuse, incident, and legal requests | many/day |
| "Which of these 400 hosts still answer?" | Reclaim decision before a subnet renumber | quarterly |
| ⚡ "What breaks if I delete this zone?" | Go/no-go on a decommission with no rollback | per-incident |

Bad, for contrast — the same content in product vocabulary, which tells the reader nothing they
didn't already know:

- ~~Historical lease attribution query~~
- ~~Bulk export with filters~~
- ~~Zone dependency analysis~~

**The frontier class here was reads that feel like writes** — simulation, blast radius, what-if.
That class exists *because* of the read-only constraint in the frame: a read-only surface gets all
the value of a change proposal with none of the risk, which made those the most valuable and
least-served items on the page. A different frame would have produced a different frontier.

The reach-further axes that filled the back half of the budget, once the obvious asks ran out: a
*time* in the question ("what was true last Tuesday"), a second system joined in, entitlement, and
provenance.

---

## Phases 3–4 — the three lanes

The inventory came out as three lanes, which made Phase 4 a lookup rather than a search:

| Lane | Reach | Real limits |
|---|---|---|
| Raw API passthrough | Broadest | No semantics; read-only gate incompletely enforced |
| Local mirror (SQL) | The only lane that joins and aggregates across the estate | Row cap that truncates silently; every answer inherits sync staleness |
| Curated composites | Real semantics, narrow | Only what someone hand-wrote |

---

## Phase 5 — what the synthesis found

The tally was roughly **one-third served, one-third partial, one-third impossible** — and stating
that ratio explicitly was the finding, not the item count.

The strongest signal on the page was a primitive demanded by four unrelated personas who shared
nothing else: **provenance and freshness on every answer** — which lane produced this, and how stale
is it. No feature list organized by subsystem would ever have surfaced it, because it belongs to no
subsystem.

## The byproduct

The Full coverage pass found a real defect: the read-only kill switch covered the generic executor
but **not** the mirrored command tools, and a root `--yes` was published as an ordinary tool
parameter — which defeated the switch entirely. That was written up as its own issue doc, filed
upstream, and linked from the appendix.

Worth knowing about this workflow: **the Full pass finds bugs that no amount of doc-reading finds**,
because Phase 4 forces you to ask "is this *actually* served?" about sixty specific things, one at a
time. That question is much harder to answer wrongly than "does the read-only mode work?"
