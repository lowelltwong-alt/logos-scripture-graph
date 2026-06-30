# Logos Scripture Graph Repository

This repository is the governed semantic substrate for a Bible knowledge graph, concordance, chunking system, and retrieval layer.

It is intentionally **not** the agent runtime. The future agent/orchestration harness should live in a separate runtime repo and call this repository through explicit contracts, generated artifacts, and validated releases.

> **Project context:** this repo is the **data-plane substrate** of the
> [logos-governance-architecture](https://github.com/lowelltwong-alt/logos-governance-architecture)
> project — the deterministic, machine-readable implementation of its scripture /
> translation / boundary-source / graph layers. See
> [`.ai/control/PROJECT_CONTEXT.md`](.ai/control/PROJECT_CONTEXT.md). Coupling is by
> contract (validated release artifacts), not submodule.

GitHub coordination is tracked by paired issues:

- upstream governance parent: [logos-governance-architecture#54](https://github.com/lowelltwong-alt/logos-governance-architecture/issues/54)
- downstream data-plane child: [logos-scripture-graph#7](https://github.com/lowelltwong-alt/logos-scripture-graph/issues/7)

The deterministic local contract is
[`config/governance/repository_link_contract.yaml`](config/governance/repository_link_contract.yaml).
This repo consumes upstream governance meaning; it does not silently redefine it.

This repo also enforces a local mirror of the upstream governance dependency map at
[`.ai/control/governance_dependency_map_mirror.yaml`](.ai/control/governance_dependency_map_mirror.yaml).
The upstream governance dependency map remains the source of truth at
`logos-governance-architecture/governance/GOVERNANCE_DEPENDENCY_MAP.yaml`; this repo only mirrors
and validates the child-repo obligations.

## Start here (table of contents)

Every human or AI contributor must follow this read order:

| # | File | Purpose |
|---|------|---------|
| 1 | [`AI_FRONT_DOOR.md`](AI_FRONT_DOOR.md) | Entry point, modes, validation gates |
| 2 | [`AI_TABLE_OF_CONTENTS.md`](AI_TABLE_OF_CONTENTS.md) | Repo map, project-family hierarchy, and validation surfaces |
| 3 | [`.ai/control/MASTER_CONTEXT.md`](.ai/control/MASTER_CONTEXT.md) | **Human-gated** architecture theory & decisions (AI read-only) |
| 4 | [`.ai/control/PROJECT_CONTEXT.md`](.ai/control/PROJECT_CONTEXT.md) | Cross-repo role, link type, and upstream/downstream boundary |
| 5 | [`.ai/control/PROJECT_STATUS.md`](.ai/control/PROJECT_STATUS.md) | Current phase, blockers, active handoffs |
| 5b | [`.ai/control/RAW_SOURCE_INVENTORY.md`](.ai/control/RAW_SOURCE_INVENTORY.md) | **The actual raw documents to be processed** (generated). Mandatory before ingest/chunking work. |
| 6 | [`ROADMAP.md`](ROADMAP.md) | Phase plan |
| 7 | [`ROADMAP_STATE.yaml`](ROADMAP_STATE.yaml) | Machine-readable task state |
| 8 | [`HANDOFF_PROTOCOL.md`](HANDOFF_PROTOCOL.md) | Deterministic agent handoffs |
| 9 | [`docs/chunking/CHUNKING_DESIGN.md`](docs/chunking/CHUNKING_DESIGN.md) | Chunking architecture |

**Validation (CI green/red):**

```bash
python scripts/validate_all.py && python -m pytest -q
```

Gates include `validate_control_plane.py` (master context lock + routing).
They also include `validate_repository_link_contract.py`, which fails closed if
the cross-repo governance contract, docs, or agent-hostile policy drift.
They include `validate_governance_dependency_map_mirror.py`, which fails closed if
the local mirror of the upstream governance dependency map drifts.

If pytest hangs locally, use:

```bash
python scripts/run_pytest_guarded.py
```

It records timeout hints in `.pytest_cache/` so the next run can isolate likely
timeout tests first and split segments instead of hanging the whole suite again.

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
