# AI Front Door

This file is the required entry point for every AI agent and human contributor.

## Mandatory read order

Read these files before making changes:

1. `AI_FRONT_DOOR.md`
2. `.ai/control/MASTER_CONTEXT.md` — **human-gated architecture authority (READ ONLY for AI)**
3. `.ai/control/PROJECT_STATUS.md` — **current operational state**
4. `.ai/control/DATA_MAP.md` — **data artifacts + pipeline endpoints (generated)**
5. `.ai/control/RAW_SOURCE_INVENTORY.md` — **the ACTUAL raw documents to be processed** (generated). **Mandatory before any ingest/chunking/graph work** — see "Raw source inspection" below.
6. `ROADMAP.md`
6. `ROADMAP_STATE.yaml`
7. `HANDOFF_PROTOCOL.md`
8. `docs/architecture/ARCHITECTURE.md`
9. `docs/chunking/CHUNKING_DESIGN.md`
10. `config/agents/agent_roles.yaml`
11. `.ai/handoffs/<active_task_id>/handoff.md` — see `PROJECT_STATUS.md` for active task
12. The specific files in the task scope.

New or lower-capability agents: read `.ai/handoffs/AGENT_ROUTING_GUIDE.md` for full step-by-step routing.

## Context layers (who may write)

| Layer | Path | AI writes? |
|-------|------|------------|
| Master context | `.ai/control/MASTER_CONTEXT.md` | **NO** — propose via `scripts/agent/propose_master_context_change.py` |
| Project status | `.ai/control/PROJECT_STATUS.md` | Yes — after each task |
| Task handoff | `.ai/handoffs/T###/handoff.md` | Yes — task agent only |
| Agent work notes | `.ai/context/agent_work/` | Yes — non-authoritative |
| Recommendations | `.ai/context/recommendations/` | Yes — proposals only |

Human promotes master context changes via `scripts/agent/approve_master_context.py`.

## Validation gates (CI green/red)

Before stopping work, run:

```bash
python scripts/validate_all.py
python -m pytest -q
```

Individual gates:

```bash
python scripts/validate_repo.py
python scripts/validate_control_plane.py   # master context lock + front-door routing
python scripts/agent/validate_handoffs.py
```

**CI fails red** if any gate fails. Agents must not mark tasks complete with failing validation.

## Raw source inspection (HARD RULE — mandatory before processing)

The whole pipeline exists to ingest, chunk, and graph the **raw source documents**
under `data/raw/`. The actual job is defined by what those files really contain
(USFM markers, Strong's lexeme tags, words-of-Jesus `\wj`, alternate readings
`\fqa`, superscriptions `\d`, poetry `\q*`, footnotes, cross-references).

**Before designing or changing any ingest, chunking, or graph-processing logic, you MUST:**

1. Read `.ai/control/RAW_SOURCE_INVENTORY.md` (the generated first-pass inventory of the real raw documents).
2. Re-scan if data/raw changed: `python scripts/scan_raw_sources.py`.
3. Confirm every marker in the raw source is classified in `config/ingest/usfm_marker_coverage.yaml`.

Enforcement (these run in `validate_all.py` and CI — fail red):

```bash
python scripts/validate_raw_coverage.py     # fails if raw has an unclassified marker
python scripts/scan_raw_sources.py --check  # fails if the inventory is stale vs data/raw
```

A chunking/processing change is **not acceptable** unless it is demonstrably designed
against the markers that actually appear in `RAW_SOURCE_INVENTORY.md`.

## Operating modes

Agents must declare one mode at task start:

| Mode | Allowed actions |
|---|---|
| `explore` | Read, inspect, summarize, propose. No file mutations except handoff notes. |
| `plan` | Create or revise roadmap, ADRs, task plans, schema proposals. |
| `build` | Implement files/scripts/configs within assigned scope. |
| `validate` | Run checks, report failures, propose fixes. |
| `review` | Evaluate architecture/chunking/schema and recommend corrections. |

## Required task state

Every non-trivial task must have:

```text
.ai/tasks/<task_id>.task.yaml
.ai/handoffs/<task_id>/handoff.md
```

Use:

```bash
python scripts/agent/force_handoff.py --task-id T000 --agent "agent-name" --stage start
```

Then update the same handoff at the end of the task.

## Required completion checklist

Before stopping work, every agent must:

1. Read `MASTER_CONTEXT.md` and `PROJECT_STATUS.md` at task start.
2. Update its handoff file.
3. Record files changed.
4. Record architectural decisions or open questions (recommend master context changes if architectural).
5. Update `PROJECT_STATUS.md` if task status or blockers changed.
6. Update `ROADMAP_STATE.yaml` if task status changed.
7. Append to `.ai/control/roadmap_events.jsonl` if roadmap scope/status changed.
8. Regenerate the data/endpoint map if data, schemas, or pipelines changed: `python scripts/generate_data_map.py`.
9. Run `python scripts/validate_all.py` and `python -m pytest -q` — or explain why they could not run.
10. Leave the repo in a state another agent can resume.

## Forbidden shortcuts

Do not:

- Edit `.ai/control/MASTER_CONTEXT.md` or `MASTER_CONTEXT.lock.yaml` (AI forbidden; human only).
- Put raw Bible files anywhere except `data/raw/`.
- **Design or change ingest/chunking/graph processing without first inspecting the real raw documents** (`RAW_SOURCE_INVENTORY.md` + a fresh `scan_raw_sources.py`). This is enforced by `validate_raw_coverage.py`.
- Treat an LLM-generated chunk boundary as canonical truth.
- Rewrite source text during chunking.
- Mix asserted and inferred relationships in the same artifact.
- Add a relationship type without schema registration.
- Change stable IDs because a label changed.
- Delete stable resources; deprecate instead.
- Mark a roadmap task complete without a handoff.
- Skip validation gates with failing CI checks.

## Architecture correction protocol

Agents may challenge this architecture, but corrections must be explicit:

1. Propose via `propose_master_context_change.py` if it affects master principles.
2. Create or update an ADR in `docs/architecture/`.
3. Explain the reason, affected files, migration path, and risks.
4. Update `ROADMAP.md` and `ROADMAP_STATE.yaml` if the correction changes sequencing.
5. Add a handoff explaining what changed and why.
6. Human approves master context updates separately from code merges.
