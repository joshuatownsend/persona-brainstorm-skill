# Phase 3 discovery — printed CLIs

Concrete mechanics for the supply-side inventory when the target is a CLI Printing Press output
(`bamcli`, `micetrocli`, and their siblings). Recognise one by a `cmd/<name>-pp-cli` directory, a
`tools-manifest.json`, and an `AGENTS.md` that names the Printing Press.

**This is one fully worked instance of the discovery contract in `../discovery.md`** — a
Read-surface subject taken all the way down to specific commands, files, and greps. Nothing here
generalizes, and nothing needs to: read it when your subject is a printed CLI, or read it as a
template for how much specificity a good recipe carries when you are writing one for an archetype
that has no section yet. The rest of the skill assumes nothing about the subject being a CLI, being
software, or existing at all.

## Ask the binary first

The generated CLI describes itself more accurately than any doc in the tree. Prefer runtime truth
over reading source when both are available.

```bash
<name>-pp-cli doctor --json          # health, auth posture, mirror state
<name>-pp-cli agent-context --pretty # the machine-readable self-description
<name>-pp-cli which "<capability>" --json
<name>-pp-cli <command> --help
```

If the binary isn't on PATH, look for it in the repo root or `build/`, and check
`~/.claude/plugins/cache/<name>/` — these ship as Claude Code plugins.

Read-only by construction: `doctor`, `agent-context`, `which`, and any `--help`. Never run a
command that mutates remote state during discovery.

## Files worth reading, in order

| File | What it gives you |
|---|---|
| `tools-manifest.json` | The MCP tool surface: `mcp_ready`, orchestration mode, whether endpoint tools are hidden. Start here. |
| `spec.json` | The upstream API spec. Count GET vs. non-GET endpoints — that ratio frames the whole read-only conversation. |
| `AGENTS.md` / `CLAUDE.md` | The local operating contract, and any repo-specific loop worth knowing about. |
| `SKILL.md`, `README.md` | Product framing and worked examples. Large; grep rather than read whole. |
| `manifest.json`, `.printing-press.json` | Provenance and version stamps. |
| the repo's issue-docs directory | Known defects — check before writing up a "new" caveat. Commonly `docs/issues/`, but not every tree has one; if it's absent, that's where a new writeup goes. |
| `.printing-press-patches/` | Hand-fixes that survive a reprint. Tells you what's deliberately divergent from a fresh print, and is where a new root-level doc must be registered. |

## The three lanes these CLIs have

Printed CLIs with an MCP server tend to expose the same three shapes. Naming them makes the
coverage column far more legible than an endpoint-by-endpoint map.

- **Raw API passthrough** — a search tool plus a generic executor. Broadest reach, no semantics.
  Look for the read-only env gate (`<NAME>_MCP_READ_ONLY`) and check *what it actually gates* —
  in `internal/mcp/code_orch.go`. This is a rich source of caveats.
- **Local mirror queries** — SQL over a synced SQLite copy. The only lane that does cross-estate
  joins and aggregates, and the one with no web-UI equivalent. Note its row cap
  (`internal/mcp/safety.go`) and that every answer inherits mirror staleness.
- **Curated composites** — hand-written tools with real semantics. Registration differs by
  vintage, so discover it rather than assuming a path: `grep -rn "AddTool(" internal/mcp/*.go`
  gives you every registered tool and the files that own them. Some trees wrap read-only ones in a
  `readOnlyTool(` helper (`internal/mcp/composite_tools.go`); others register them directly from
  per-feature files (`intents.go`, `tools.go`, `estate_report_tool.go`). Also grep
  `mcp:read-only=true` and `mcp:local-write=true` for the annotations on mirrored CLI commands.

## Caveats these repos reliably have

Check each; they map straight onto coverage marks and onto the provenance/freshness primitive.

- **Staleness.** Every mirror answer is only as fresh as the last `sync`. A capacity or hygiene
  answer from a stale mirror is worse than no answer. Look for a freshness-reporting command
  (`<name>-pp-cli which "mirror freshness" --json`, or grep the command tree for `sync`/`mirror`)
  and note whether anything *enforces* freshness or merely reports it. A tree with no such command
  at all is itself the finding.
- **Incomplete read-only enforcement.** Verify the kill switch covers the *mirrored command* tools
  too, not just the generic executor — walk `internal/mcp/cobratree/walker.go` and the blocked-flag
  list in `shellout.go`. A root `--yes` published as an ordinary tool parameter defeats the switch.
- **Row caps that silently truncate.** A capped aggregate that doesn't say it was capped is a
  wrong answer, not a partial one.
- **Provenance fields that misreport** which lane an answer came from.

## For any other subject

`../discovery.md` carries the contract these mechanics satisfy — named lanes, each lane's real
limits — plus recipes for the other archetypes: library/SDK, application, data platform,
infrastructure, and process. Go there rather than adapting this file.
