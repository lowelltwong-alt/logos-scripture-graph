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
- [`docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md`](docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md) - local AI roadmap/review artifact map
- [`HANDOFF_PROTOCOL.md`](HANDOFF_PROTOCOL.md) - deterministic agent handoff rules

## Architecture And Governance

- [`docs/architecture/ARCHITECTURE.md`](docs/architecture/ARCHITECTURE.md)
- [`docs/architecture/SCRIPTURE_VECTORIZATION_AND_EDGE_DURABILITY_CONTRACT.md`](docs/architecture/SCRIPTURE_VECTORIZATION_AND_EDGE_DURABILITY_CONTRACT.md) - planning-only; embedding runs not authorized
- [`.ai/control/scripture_vectorization_plan.yaml`](.ai/control/scripture_vectorization_plan.yaml) - machine-readable fail-closed vectorization flags
- [`.ai/control/chunking_agent_preflight.yaml`](.ai/control/chunking_agent_preflight.yaml) - mandatory chunking-agent preflight and lesson-capture contract
- [`.ai/control/chunking_theological_decision_register.yaml`](.ai/control/chunking_theological_decision_register.yaml) - first-class chunking/theological decision register
- [`.ai/control/bible_chunking_readiness_map.yaml`](.ai/control/bible_chunking_readiness_map.yaml) - non-authorizing Bible-wide lane and algorithm readiness map
- [`docs/chunking/CHUNKING_DESIGN.md`](docs/chunking/CHUNKING_DESIGN.md)
- [`docs/methodology/WORKFLOW_LESSONS.md`](docs/methodology/WORKFLOW_LESSONS.md)
- [`docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md`](docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md)
- [`docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`](docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md)
- [`docs/methodology/UNINTENDED_CONSEQUENCE_REVIEW.md`](docs/methodology/UNINTENDED_CONSEQUENCE_REVIEW.md)
- [`docs/roadmap/T336_OPTIMIZED_WHOLE_BIBLE_CHUNKING_ROADMAP.md`](docs/roadmap/T336_OPTIMIZED_WHOLE_BIBLE_CHUNKING_ROADMAP.md)
- [`docs/roadmap/T337_SELECT_ONE_PSALM_BEHAVIOR_CHANGE.md`](docs/roadmap/T337_SELECT_ONE_PSALM_BEHAVIOR_CHANGE.md)
- [`docs/roadmap/T337B_PS89_OWNER_DECISION_OPTION_C.md`](docs/roadmap/T337B_PS89_OWNER_DECISION_OPTION_C.md)
- [`docs/roadmap/T338_PS89_ROUTE_ISOLATED_IMPLEMENTATION.md`](docs/roadmap/T338_PS89_ROUTE_ISOLATED_IMPLEMENTATION.md)
- [`docs/roadmap/T339_PS89_SAME_BASELINE_RISK_EVALUATION.md`](docs/roadmap/T339_PS89_SAME_BASELINE_RISK_EVALUATION.md)
- [`docs/roadmap/T340_PSALM_CANDIDATE_PROMOTION_DECISION.md`](docs/roadmap/T340_PSALM_CANDIDATE_PROMOTION_DECISION.md)
- [`docs/roadmap/T341_REVELATION_HARD_BOOK_ATLAS.md`](docs/roadmap/T341_REVELATION_HARD_BOOK_ATLAS.md)
- [`docs/roadmap/T341_REVELATION_OBSERVED_BEHAVIOR_AUDIT.md`](docs/roadmap/T341_REVELATION_OBSERVED_BEHAVIOR_AUDIT.md)
- [`docs/roadmap/T342_REVELATION_REVIEW_PACKET_CANDIDATE_SELECTION.md`](docs/roadmap/T342_REVELATION_REVIEW_PACKET_CANDIDATE_SELECTION.md)
- [`docs/roadmap/T343_REVELATION_REVIEW_PACKETS_AND_GOLD_CANDIDATES.md`](docs/roadmap/T343_REVELATION_REVIEW_PACKETS_AND_GOLD_CANDIDATES.md)
- [`docs/roadmap/T344_REVELATION_OWNER_SELECTION_DOCKET.md`](docs/roadmap/T344_REVELATION_OWNER_SELECTION_DOCKET.md)
- [`docs/roadmap/T350_BIBLE_WIDE_CHUNKING_READINESS_PLAN.md`](docs/roadmap/T350_BIBLE_WIDE_CHUNKING_READINESS_PLAN.md)
- [`.ai/control/t340_psalm_candidate_promotion_decision.yaml`](.ai/control/t340_psalm_candidate_promotion_decision.yaml)
- [`config/governance/repository_link_contract.yaml`](config/governance/repository_link_contract.yaml)
- [`.ai/control/boundary_material_routing.yaml`](.ai/control/boundary_material_routing.yaml)
- [`config/governance/predicate_registry.yaml`](config/governance/predicate_registry.yaml)
- [`config/agents/agent_roles.yaml`](config/agents/agent_roles.yaml)
- [`config/agents/model_routing.yaml`](config/agents/model_routing.yaml)
- [`config/agents/agent_hostile_policy.yaml`](config/agents/agent_hostile_policy.yaml)

## Workflows And Templates

- [`.ai/audits/README.md`](.ai/audits/README.md) - no-context review and red-team audit entry point
- [`.ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md`](.ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md) - independent reviewer instructions
- [`.ai/audits/templates/REVIEW_REPORT_TEMPLATE.md`](.ai/audits/templates/REVIEW_REPORT_TEMPLATE.md) - durable review report template
- [`.ai/control/audit_surface_map.yaml`](.ai/control/audit_surface_map.yaml) - machine-readable audit surface map
- [`.ai/control/harness_upgrade_roadmap.yaml`](.ai/control/harness_upgrade_roadmap.yaml) - future harness upgrade watchlist and roadmap
- [`scripts/agent/no_context_audit_harness.py`](scripts/agent/no_context_audit_harness.py) - generates no-context audit briefs
- [`scripts/validate_owner_selection_implementation_gate.py`](scripts/validate_owner_selection_implementation_gate.py) - HARN-012 gate blocking T345/output-changing work until owner selection and governed evidence agree
- [`scripts/validate_source_metadata_authority.py`](scripts/validate_source_metadata_authority.py) - HARN-006 scanner keeping source metadata evidence from becoming boundary, lexical, intertext, graph-edge, or truth authority
- [`docs/workflows/AGENT_COORDINATION_WORKFLOW.md`](docs/workflows/AGENT_COORDINATION_WORKFLOW.md)
- [`docs/workflows/ROADMAP_CHANGE_WORKFLOW.md`](docs/workflows/ROADMAP_CHANGE_WORKFLOW.md)

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
