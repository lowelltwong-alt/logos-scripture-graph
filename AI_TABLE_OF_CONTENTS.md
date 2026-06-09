# AI Table of Contents

This file maps the repository for AI agents, coding assistants, maintainers, and reviewers.

## Project Family

- Upstream governance authority: [logos-governance-architecture](https://github.com/lowelltwong-alt/logos-governance-architecture)
- This repository: [logos-scripture-graph](https://github.com/lowelltwong-alt/logos-scripture-graph)
- Supporting boundary literature repo: `logos-boundary-literature`
- Link contract: [`config/governance/repository_link_contract.yaml`](config/governance/repository_link_contract.yaml)
- Governance registry source of truth: `logos-governance-architecture/governance/LOGOS_REPO_REGISTRY.yaml`
- Boundary-originated higher-layer stop rules: [`.ai/control/boundary_material_routing.yaml`](.ai/control/boundary_material_routing.yaml)
- Local context: [`.ai/control/PROJECT_CONTEXT.md`](.ai/control/PROJECT_CONTEXT.md)

Role hierarchy:

```text
logos-governance-architecture
  -> upstream theological / governance architecture authority
  -> cross-repo policy, authority contracts, update rules, validation patterns
  -> logos-scripture-graph
     -> canonical 66-book Scripture truth and governed Scripture data-plane
     -> Scripture passages, chunks, gold/evaluator surfaces, graph outputs
     -> logos-boundary-literature
        -> supporting boundary / reception / comparison / refutation material
        -> never equal or superior authority to canonical Scripture
```

Coupling is by explicit contract, schemas, validated releases, and GitHub coordination
issues. It is not a submodule, hidden runtime dependency, or automatic promotion path.

## Primary Entry Points

- [`README.md`](README.md) - human-facing landing page and project overview
- [`AI_FRONT_DOOR.md`](AI_FRONT_DOOR.md) - mandatory agent entry point, modes, validation gates
- [`.ai/control/MASTER_CONTEXT.md`](.ai/control/MASTER_CONTEXT.md) - human-gated architecture authority
- [`.ai/control/PROJECT_STATUS.md`](.ai/control/PROJECT_STATUS.md) - current operational state
- [`.ai/control/DATA_MAP.md`](.ai/control/DATA_MAP.md) - generated data/pipeline map
- [`.ai/control/RAW_SOURCE_INVENTORY.md`](.ai/control/RAW_SOURCE_INVENTORY.md) - actual raw-source marker inventory
- [`ROADMAP.md`](ROADMAP.md) - phase plan
- [`ROADMAP_STATE.yaml`](ROADMAP_STATE.yaml) - machine-readable task state
- [`HANDOFF_PROTOCOL.md`](HANDOFF_PROTOCOL.md) - deterministic agent handoff rules

## Architecture And Governance

- [`docs/architecture/ARCHITECTURE.md`](docs/architecture/ARCHITECTURE.md)
- [`docs/chunking/CHUNKING_DESIGN.md`](docs/chunking/CHUNKING_DESIGN.md)
- [`docs/methodology/WORKFLOW_LESSONS.md`](docs/methodology/WORKFLOW_LESSONS.md)
- [`docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`](docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md)
- [`config/governance/repository_link_contract.yaml`](config/governance/repository_link_contract.yaml)
- [`.ai/control/boundary_material_routing.yaml`](.ai/control/boundary_material_routing.yaml)
- [`config/governance/predicate_registry.yaml`](config/governance/predicate_registry.yaml)
- [`config/agents/agent_roles.yaml`](config/agents/agent_roles.yaml)
- [`config/agents/model_routing.yaml`](config/agents/model_routing.yaml)
- [`config/agents/agent_hostile_policy.yaml`](config/agents/agent_hostile_policy.yaml)

## Data Plane

- `data/raw/` - immutable source artifacts
- `data/canonical/` - generated canonical passage and witness records
- `data/processed/` - importer sidecars and parser reports
- `data/derived/` - rebuildable chunks and indexes
- `data/candidate/` - unpromoted candidate claims and discovery output
- `schemas/` - JSON Schema contracts
- `pipelines/` - deterministic ingest, chunking, graph, and validation pipelines

## Validation

Default gates:

```bash
python scripts/validate_all.py
python -m pytest -q
```

Canonical corpus QA:

```bash
python scripts/qa_canonical_corpus.py
```

Timeout-aware local pytest runner:

```bash
python scripts/run_pytest_guarded.py
```

`run_pytest_guarded.py` records local timeout hints under `.pytest_cache/` so the
next run can isolate likely timeout tests instead of repeatedly hanging the whole suite.

## AI-Agent Rule

If a referenced file does not exist in the local checkout, do not invent its contents.
Report it as missing and recommend either creating it or removing the link.
