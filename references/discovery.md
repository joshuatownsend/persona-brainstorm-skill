# Phase 3 discovery

How to inventory what a subject serves today, per archetype. Read the **Contract** first, then the
one section matching the archetype you picked in Phase 0. Skip the rest.

Discovery is reference material for Phase 4 and an appendix in the final document. It is **not** a
brainstorming input, and by the time you are reading this the items are already written — that
ordering is the protection, not a formality.

---

## Contract

Phases 4–5 need exactly two things from discovery. Everything else you collect is optional colour.

1. **Named lanes** — the distinct ways an answer can be obtained. Three to six is the useful range.
   A lane is a *route*, not an endpoint: "the local mirror", "the raw API", "the report you have to
   email someone for". Lanes beat exhaustive surface maps because a persona's ask maps to a lane,
   not to a call, so Phase 4 becomes a lookup instead of a search.

2. **Each lane's real limits** — row caps, staleness, auth scope, what it silently refuses, what it
   truncates without saying so. These become the appendix caveats and are frequently more
   interesting than the inventory itself. A limit that produces a *wrong* answer rather than a
   missing one is always worth writing up as its own defect.

If a recipe below doesn't fit your subject, you have not lost anything — write the shortest
procedure that yields those two outputs and you are done. Consider contributing it back as a new
section.

**Prefer runtime truth over source** wherever the subject can describe itself. Self-descriptions
are more accurate than docs and far cheaper than code. Run only read-only commands.

**Stop when the lanes stop changing.** Discovery has no natural end and will consume the whole
session if allowed to. Two or three passes that add no new lane means you are done.

---

## § Read surface — API, query tool, MCP server, reporting layer

**Read, in order:** the machine-readable spec first (OpenAPI/GraphQL schema/`tools-manifest.json`),
then any self-describe command, then the auth and rate-limit docs, then source only for the
enforcement questions below.

**Lanes usually turn out to be:** raw passthrough (broad reach, no semantics) · a cached or
mirrored copy (the only lane that joins and aggregates, and the only one that goes stale) · curated
composites with real semantics · and often a fourth nobody documents, like an export or a support
escalation.

**Count the read operations against the write ones.** That ratio frames the entire read-only
conversation and takes one command — but count the right thing. For REST/OpenAPI it is GET vs.
non-GET. For GraphQL it is **not**: queries and mutations travel through the same POST endpoint, so
an HTTP-verb count reads a query-only API as entirely write-heavy. Count `query` vs. `mutation`
operation types in the schema instead. For anything else, find the surface's own read/write
distinction before assuming the transport carries one.

**Caveats to check:**
- **Staleness** — is there anything that *enforces* freshness, or does it merely report it? A
  subject with no freshness command at all is itself the finding.
- **Row caps that silently truncate** — a capped aggregate that doesn't announce the cap is a wrong
  answer, not a partial one.
- **Incomplete read-only enforcement** — verify the kill switch covers every lane, not just the
  obvious executor. This is the highest-yield defect class in this archetype.
- **Provenance fields that misreport** which lane an answer came from.

Worked instance: `discovery/printed-cli.md`.

---

## § Library / SDK / framework

**Read, in order:** the exported/public type surface (`index.*`, `__all__`, `pub` items, the `.d.ts`)
— this *is* the inventory, and it's usually one file · the README's examples, which show the
intended path · the changelog or migration guide, which shows what has broken before · the issue
tracker's most-reacted issues, which is the cheapest demand signal in existence · tests, last, for
the behaviours docs don't state.

**Lanes usually turn out to be:** the documented happy path · the configuration/options surface ·
the extension points (plugins, hooks, subclassing, middleware) · the escape hatch (raw access,
`unsafe_*`, `any`-typed passthrough) · and what you must fork or monkey-patch to get.

**Caveats to check:**
- **What it refuses, and how.** A thrown error, a silent no-op, and a `null` are three different
  products. Silent no-ops are the defect worth writing up.
- **Peer/version constraints** — what does it break against, and does it say so at install or only
  at runtime?
- **Error quality** — can a consumer diagnose a failure without reading your source? If not, that
  is a lane limit, and usually a whole cluster of Phase 5 evidence.
- **Extension points that exist but are undocumented or unstable** — served-but-unusable is `◐`,
  not `✅`.

---

## § Application / UI product

**Read, in order:** the route/screen map (router config, sitemap, nav definition) — this is the
inventory · the permission or role model · the exports and integrations · the settings surface ·
the empty and error states, which are where the real limits live.

**Lanes usually turn out to be:** the primary UI flow · search/filter · exports and reports ·
notifications and alerts · the API or integration surface · and support-mediated actions (the thing
only an admin or a ticket can do).

**Caveats to check:**
- **What requires an admin, a ticket, or a human** — these are lane limits even though nothing in
  the code marks them.
- **Bulk ceilings** — the flow that works for 5 and collapses at 500.
- **Degraded states** — offline, slow network, partial data. Usually undesigned, and a rich source
  of `○`.
- **Multi-user collision** — what happens when two people act at once. Frequently unhandled and
  invisible until Phase 4 asks.

---

## § Data platform / warehouse / dataset

**Read, in order:** the schema or catalogue · the freshness/SLA metadata per table · the lineage or
dbt graph if one exists · access grants · the semantic layer or metric definitions, if any.

**Lanes usually turn out to be:** raw/landing tables · modelled or curated tables · the semantic
metric layer · BI dashboards · direct ad-hoc query access · and the export path.

**Caveats to check:**
- **Freshness per lane, not per platform.** They differ, often by a day or more, and an answer
  joining two lanes inherits the worse one.
- **Grain mismatch** — the data exists but at the wrong resolution. This is the archetypal `◐` and
  collapsing it into `✅` hides the actual gap.
- **Backfills and restatements** — does a number change after the fact, and is that detectable?
- **Access scope** — who can actually reach each lane. A capability nobody is granted is not served.
- **Definitional drift** — the same metric name meaning two things in two lanes is a defect worth
  its own writeup.

---

## § Infrastructure / service / platform

**Read, in order:** the declared resources (IaC, manifests, inventory) · the control surface (CLI,
console, API) · the observability surface — what is actually measured, which bounds every question
about the past · the change and approval path · the runbooks, which describe the real process rather
than the intended one.

**Lanes usually turn out to be:** self-service actions · approval-gated changes · read-only
telemetry and dashboards · the audit log · and the break-glass path.

**Caveats to check:**
- **Retention** — how far back telemetry and audit actually go. This silently kills every historical
  ask, and is rarely what people assume.
- **Blast radius is knowable only after the fact** — the most common `○` in this archetype, and
  usually the strongest Phase 5 primitive.
- **Cost attribution granularity** — per-account is not per-team is not per-feature.
- **Drift** — does declared state match actual state, and does anything detect the difference?

---

## § Process / non-software

There is no artifact, so there is no discovery phase in the usual sense — but there is almost
always something to inventory, and "process" does not mean "undocumented". **If the user asked for
Full or Light coverage, run this pass**; skipping it silently drops the coverage map and the gap
list they asked for. Skip Phase 3 only when the process genuinely has nothing to inspect — one
being designed from scratch, or one that exists solely in people's heads — in which case say so in
the document rather than leaving the coverage column blank without explanation.

**Lanes are:** the documents that exist · the meetings where things get decided · the reports
someone can run · the person you have to ask · and the tribal knowledge with no owner.

**Limits are:** who can invoke each lane, how long it takes, how stale it is, and what it silently
omits. "The only person who knows this is on leave" is a lane limit, and belongs in the appendix
in exactly those terms.

---

## When the subject doesn't exist yet

A capability being scoped before anyone builds it has nothing to inspect. Run Phases 0–2 and 5,
drop the coverage column entirely, and the document is still the useful half — the items and the
synthesis were never the part that needed an artifact.
