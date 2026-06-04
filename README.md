# Logos Scripture Graph Repository

This repository is the governed semantic substrate for a Bible knowledge graph, concordance, chunking system, and retrieval layer.

It is intentionally **not** the agent runtime. The future agent/orchestration harness should live in a separate runtime repo and call this repository through explicit contracts, generated artifacts, and validated releases.

## Start here (table of contents)

Every human or AI contributor must follow this read order:

| # | File | Purpose |
|---|------|---------|
| 1 | [`AI_FRONT_DOOR.md`](AI_FRONT_DOOR.md) | Entry point, modes, validation gates |
| 2 | [`.ai/control/MASTER_CONTEXT.md`](.ai/control/MASTER_CONTEXT.md) | **Human-gated** architecture theory & decisions (AI read-only) |
| 3 | [`.ai/control/PROJECT_STATUS.md`](.ai/control/PROJECT_STATUS.md) | Current phase, blockers, active handoffs |
| 4 | [`ROADMAP.md`](ROADMAP.md) | Phase plan |
| 5 | [`ROADMAP_STATE.yaml`](ROADMAP_STATE.yaml) | Machine-readable task state |
| 6 | [`HANDOFF_PROTOCOL.md`](HANDOFF_PROTOCOL.md) | Deterministic agent handoffs |
| 7 | [`docs/chunking/CHUNKING_DESIGN.md`](docs/chunking/CHUNKING_DESIGN.md) | Chunking architecture |

**Validation (CI green/red):**

```bash
python scripts/validate_all.py && python -m pytest -q
```

Gates include `validate_control_plane.py` (master context lock + routing).

## Contributing

`main` is protected: all changes land via Pull Request (passing the `validate` check
+ CODEOWNER review). See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the PR workflow,
agent-swarm/token guidance, and capability-based model routing
([`config/agents/model_routing.yaml`](config/agents/model_routing.yaml) +
[`.ai/control/MODEL_ROSTER.md`](.ai/control/MODEL_ROSTER.md)).

## Raw source drop location

Put downloaded Bible/source files only under:

```text
data/raw/
```

For the World English Bible Classic USFM archive, use:

```text
data/raw/bible/eng-web/usfm/eng-web_usfm.zip
```

Do not edit files in `data/raw/` manually after drop. Treat them as immutable source artifacts.

## Core build order

```text
raw source files
  -> source manifests
  -> canonical passage registry
  -> translation witnesses
  -> boundary witnesses
  -> retrieval chunks
  -> context packets
  -> graph edges / claims
  -> indexes / release artifacts
```

## Design doctrine

See [`.ai/control/MASTER_CONTEXT.md`](.ai/control/MASTER_CONTEXT.md) for authoritative principles. Summary:

- Source texts are canonical evidence; chunks are derived artifacts.
- Verse references are address units, not always meaning units.
- Chunking must preserve sentence, paragraph, poetic, discourse, and literary units.
- Hebrew/Greek alignment is required for mature scholarship but does not block the English WEB MVP.
- Every non-trivial claim needs provenance, confidence, source, license, and trust-zone metadata.
- Roadmap and handoff state are deterministic control files, not loose notes.
- **Master context changes require human review** — agents propose, humans promote.

## Agent context directories

```text
.ai/control/MASTER_CONTEXT.md     ← human-gated (AI read-only)
.ai/control/PROJECT_STATUS.md     ← updated each task
.ai/handoffs/T###/handoff.md      ← task state packets
.ai/context/agent_work/           ← agent session notes (non-authoritative)
.ai/context/recommendations/      ← master context change proposals
```
