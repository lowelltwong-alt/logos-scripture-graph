# AI Table of Contents

This file maps the repository for AI agents, coding assistants, maintainers, and reviewers.

## Agent Routing Contract

AI-facing tables of contents in this repo are routing surfaces, not just file lists. Each AI TOC
should give future agents:

- `tags:` searchable keywords for audit, engineering, governance, chunking, theology risk, data,
  validation, and user-facing workflows.
- `use when:` a short trigger that tells a no-context agent when the file matters.
- `start here:` one or more entry points for that tag or task type.

If a future task creates or updates an AI TOC, apply this pattern there too. This is recorded as
`WORKFLOW-LESSON-004` in `docs/methodology/WORKFLOW_LESSONS.md`.

## Functional Tag Index

| Tags | Use when | Start here |
| --- | --- | --- |
| `audit`, `no-context-review`, `red-team`, `a-b-check`, `review-report` | An independent AI or reviewer needs to verify a branch/PR without chat context. | [`.ai/audits/README.md`](.ai/audits/README.md); [`.ai/control/audit_surface_map.yaml`](.ai/control/audit_surface_map.yaml); [`scripts/agent/no_context_audit_harness.py`](scripts/agent/no_context_audit_harness.py) |
| `front-door`, `agent-startup`, `required-reading`, `mode-selection` | Any AI starts work in this repo or needs the mandatory entry protocol. | [`AI_FRONT_DOOR.md`](AI_FRONT_DOOR.md); [`HANDOFF_PROTOCOL.md`](HANDOFF_PROTOCOL.md) |
| `current-state`, `status`, `handoff`, `roadmap`, `next-route` | An agent needs to know what is active, complete, blocked, or next. | [`.ai/control/PROJECT_STATUS.md`](.ai/control/PROJECT_STATUS.md); [`.ai/control/current_focus.yaml`](.ai/control/current_focus.yaml); [`ROADMAP_STATE.yaml`](ROADMAP_STATE.yaml); [`docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md`](docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md) |
| `chunking`, `theology-risk`, `decision-register`, `owner-decision`, `non-authorizing` | A change could affect chunking, evaluator behavior, gold, routes, defaults, speaker attribution, intertexts, or theology-facing output. | [`.ai/control/chunking_agent_preflight.yaml`](.ai/control/chunking_agent_preflight.yaml); [`.ai/control/chunking_theological_decision_register.yaml`](.ai/control/chunking_theological_decision_register.yaml); [`.ai/control/bible_chunking_readiness_map.yaml`](.ai/control/bible_chunking_readiness_map.yaml) |
| `whole-bible-research`, `canonical-66`, `book-watchpoints`, `research-registry`, `review-packet-candidates` | An agent needs to prepare Bible-wide research before choosing exact review packets or algorithms. | [`.ai/control/bible_wide_chunking_research_registry.yaml`](.ai/control/bible_wide_chunking_research_registry.yaml); [`docs/roadmap/T358_BIBLE_WIDE_CHUNKING_RESEARCH_REGISTRY.md`](docs/roadmap/T358_BIBLE_WIDE_CHUNKING_RESEARCH_REGISTRY.md) |
| `source-metadata`, `cross-references`, `strongs`, `lexical-rarity`, `footnotes`, `headings`, `wj`, `red-letter`, `capitalization` | Source formatting or metadata may look theologically meaningful and must remain evidence-only unless authorized. | [`.ai/control/source_metadata_research_atlas.yaml`](.ai/control/source_metadata_research_atlas.yaml); [`.ai/control/RAW_SOURCE_INVENTORY.md`](.ai/control/RAW_SOURCE_INVENTORY.md); [`docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md`](docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md); [`.ai/control/divine_capitalization_inventory.yaml`](.ai/control/divine_capitalization_inventory.yaml); [`.ai/control/wj_marker_inventory.yaml`](.ai/control/wj_marker_inventory.yaml) |
| `apocalyptic`, `prophetic`, `revelation`, `daniel`, `intertext`, `hermeneutic-neutrality`, `eschatology` | Revelation, Daniel, prophetic, Olivet discourse, or symbolic intertext work must preserve orthodox options without authorizing graph/chunk/output behavior. | [`.ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml`](.ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml); [`docs/roadmap/T360_APOCALYPTIC_PROPHETIC_INTERTEXT_DOSSIERS.md`](docs/roadmap/T360_APOCALYPTIC_PROPHETIC_INTERTEXT_DOSSIERS.md) |
| `epistle`, `argument-boundary`, `election`, `law-gospel`, `faith-works`, `assurance`, `sacramental`, `theology-risk` | Epistle argument work might smuggle doctrinal systems or reviewed-gold assumptions through labels, packet state, or boundaries. | [`.ai/control/epistle_argument_theological_issue_dossier_queue.yaml`](.ai/control/epistle_argument_theological_issue_dossier_queue.yaml); [`docs/roadmap/T361_EPISTLE_ARGUMENT_THEOLOGICAL_ISSUE_DOSSIERS.md`](docs/roadmap/T361_EPISTLE_ARGUMENT_THEOLOGICAL_ISSUE_DOSSIERS.md); [`docs/roadmap/T352_EPISTLE_ARGUMENT_REVIEW_PACKETS.md`](docs/roadmap/T352_EPISTLE_ARGUMENT_REVIEW_PACKETS.md) |
| `john3`, `wj-speaker`, `speaker-boundary`, `owner-review`, `gospel-discourse` | Work touches John 3, WJ/red-letter evidence, Jesus/narrator boundaries, or Gospel discourse chunking. | [`.ai/control/wj_speaker_discourse_policy.yaml`](.ai/control/wj_speaker_discourse_policy.yaml); [`.ai/control/john3_wj_owner_review_docket.yaml`](.ai/control/john3_wj_owner_review_docket.yaml); [`docs/roadmap/T356_JOHN3_WJ_OWNER_REVIEW_DOCKET.md`](docs/roadmap/T356_JOHN3_WJ_OWNER_REVIEW_DOCKET.md) |
| `validation`, `ci`, `harness`, `task-scope`, `protected-paths`, `regression` | A developer or agent needs to know what must pass or why a change is blocked. | [`scripts/validate_all.py`](scripts/validate_all.py); [`scripts/validate_task_scope.py`](scripts/validate_task_scope.py); [`.ai/control/harness_upgrade_roadmap.yaml`](.ai/control/harness_upgrade_roadmap.yaml) |
| `data-plane`, `raw`, `canonical`, `importer`, `qa`, `schemas`, `pipelines` | Work touches source artifacts, generated canonical records, ingest, schemas, or deterministic rebuilds. | [`.ai/control/DATA_MAP.md`](.ai/control/DATA_MAP.md); [`.ai/control/RAW_SOURCE_INVENTORY.md`](.ai/control/RAW_SOURCE_INVENTORY.md); [`pipelines/`](pipelines/); [`schemas/`](schemas/) |
| `graph`, `vector`, `retrieval`, `embedding`, `planning-only` | Work might create graph edges, retrieval truth, vectorization, or embeddings. | [`docs/architecture/SCRIPTURE_VECTORIZATION_AND_EDGE_DURABILITY_CONTRACT.md`](docs/architecture/SCRIPTURE_VECTORIZATION_AND_EDGE_DURABILITY_CONTRACT.md); [`.ai/control/scripture_vectorization_plan.yaml`](.ai/control/scripture_vectorization_plan.yaml) |
| `cross-repo`, `governance`, `boundary`, `repository-contract`, `authority` | Work depends on governance architecture, boundary material, repo relationships, or authority order. | [`config/governance/repository_link_contract.yaml`](config/governance/repository_link_contract.yaml); [`.ai/control/boundary_material_routing.yaml`](.ai/control/boundary_material_routing.yaml) |
| `developer-engineering`, `architecture`, `workflow`, `tests`, `scripts` | A software engineer needs implementation context, local workflows, or repo structure. | [`docs/architecture/ARCHITECTURE.md`](docs/architecture/ARCHITECTURE.md); [`docs/workflows/AGENT_COORDINATION_WORKFLOW.md`](docs/workflows/AGENT_COORDINATION_WORKFLOW.md); [`docs/workflows/ROADMAP_CHANGE_WORKFLOW.md`](docs/workflows/ROADMAP_CHANGE_WORKFLOW.md) |

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

- [`README.md`](README.md) - human-facing landing page and project overview; tags: `overview`, `human-start`
- [`AI_FRONT_DOOR.md`](AI_FRONT_DOOR.md) - mandatory agent entry point, modes, validation gates; tags: `front-door`, `agent-startup`, `required-reading`
- [`.ai/control/MASTER_CONTEXT.md`](.ai/control/MASTER_CONTEXT.md) - human-gated architecture authority; tags: `architecture-authority`, `human-gated`
- [`.ai/control/PROJECT_STATUS.md`](.ai/control/PROJECT_STATUS.md) - current operational state; tags: `current-state`, `status`
- [`.ai/control/DATA_MAP.md`](.ai/control/DATA_MAP.md) - generated data/pipeline map; tags: `data-plane`, `pipelines`, `generated`
- [`.ai/control/RAW_SOURCE_INVENTORY.md`](.ai/control/RAW_SOURCE_INVENTORY.md) - actual raw-source marker inventory; tags: `raw`, `source-metadata`, `markers`
- [`ROADMAP.md`](ROADMAP.md) - phase plan; tags: `roadmap`, `phase-plan`
- [`ROADMAP_STATE.yaml`](ROADMAP_STATE.yaml) - machine-readable task state; tags: `roadmap`, `task-state`, `next-route`
- [`docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md`](docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md) - local AI roadmap/review artifact map; tags: `roadmap`, `review-packets`, `owner-decisions`
- [`HANDOFF_PROTOCOL.md`](HANDOFF_PROTOCOL.md) - deterministic agent handoff rules; tags: `handoff`, `agent-continuity`

## Architecture And Governance

- [`docs/architecture/ARCHITECTURE.md`](docs/architecture/ARCHITECTURE.md)
- [`docs/architecture/SCRIPTURE_VECTORIZATION_AND_EDGE_DURABILITY_CONTRACT.md`](docs/architecture/SCRIPTURE_VECTORIZATION_AND_EDGE_DURABILITY_CONTRACT.md) - planning-only; embedding runs not authorized
- [`.ai/control/scripture_vectorization_plan.yaml`](.ai/control/scripture_vectorization_plan.yaml) - machine-readable fail-closed vectorization flags
- [`.ai/control/chunking_agent_preflight.yaml`](.ai/control/chunking_agent_preflight.yaml) - mandatory chunking-agent preflight and lesson-capture contract
- [`.ai/control/chunking_theological_decision_register.yaml`](.ai/control/chunking_theological_decision_register.yaml) - first-class chunking/theological decision register
- [`.ai/control/bible_chunking_readiness_map.yaml`](.ai/control/bible_chunking_readiness_map.yaml) - non-authorizing Bible-wide lane and algorithm readiness map
- [`.ai/control/bible_chunking_research_triage_map.yaml`](.ai/control/bible_chunking_research_triage_map.yaml) - non-authorizing Bible-wide research triage before more chunking work
- [`.ai/control/bible_wide_chunking_research_registry.yaml`](.ai/control/bible_wide_chunking_research_registry.yaml) - canonical 66-book research queue; tags: `whole-bible-research`, `canonical-66`, `review-packet-candidates`; evidence only, not chunk/gold/graph authority
- [`.ai/control/source_metadata_research_atlas.yaml`](.ai/control/source_metadata_research_atlas.yaml) - source-metadata research atlas; tags: `source-metadata`, `cross-references`, `strongs`, `lexical-rarity`, `footnotes`, `headings`, `wj`, `capitalization`; evidence only, not Scripture/lexical/intertext/speaker/graph/chunk/retrieval/output authority
- [`.ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml`](.ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml) - Revelation/Daniel/prophetic intertext dossier queue; tags: `apocalyptic`, `prophetic`, `revelation`, `daniel`, `intertext`, `hermeneutic-neutrality`; evidence only, not intertext/graph/chunk/retrieval/output authority
- [`.ai/control/epistle_argument_theological_issue_dossier_queue.yaml`](.ai/control/epistle_argument_theological_issue_dossier_queue.yaml) - epistle argument theological issue dossier queue; tags: `epistle`, `argument-boundary`, `election`, `law-gospel`, `faith-works`, `assurance`, `sacramental`; evidence only, not doctrine/reviewed-gold/graph/chunk/retrieval/output authority
- [`.ai/control/divine_capitalization_inventory.yaml`](.ai/control/divine_capitalization_inventory.yaml) - observed divine-name/title/pronoun capitalization inventory; evidence only, not graph/chunk/retrieval authority
- [`.ai/control/wj_marker_inventory.yaml`](.ai/control/wj_marker_inventory.yaml) - observed words-of-Jesus/red-letter marker token runs; evidence only, not speaker/chunk/graph/retrieval authority
- [`.ai/control/wj_speaker_discourse_policy.yaml`](.ai/control/wj_speaker_discourse_policy.yaml) - WJ speaker/discourse policy and John 3 owner-review target selection; review-only, not chunk/speaker/graph/retrieval authority
- [`.ai/control/john3_wj_owner_review_docket.yaml`](.ai/control/john3_wj_owner_review_docket.yaml) - pending John 3 WJ owner-review options; no parent/child/speaker/chunk approval
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
- [`docs/roadmap/T351_BIBLE_WIDE_CHUNKING_RESEARCH_TRIAGE_ATLAS.md`](docs/roadmap/T351_BIBLE_WIDE_CHUNKING_RESEARCH_TRIAGE_ATLAS.md)
- [`docs/roadmap/T352_EPISTLE_ARGUMENT_REVIEW_PACKETS.md`](docs/roadmap/T352_EPISTLE_ARGUMENT_REVIEW_PACKETS.md)
- [`docs/roadmap/T353_DIVINE_CAPITALIZATION_INVENTORY_HARNESS.md`](docs/roadmap/T353_DIVINE_CAPITALIZATION_INVENTORY_HARNESS.md)
- [`docs/roadmap/T354_WJ_MARKER_INVENTORY_HARNESS.md`](docs/roadmap/T354_WJ_MARKER_INVENTORY_HARNESS.md)
- [`docs/roadmap/T355_WJ_SPEAKER_POLICY_AND_TARGET_SELECTION.md`](docs/roadmap/T355_WJ_SPEAKER_POLICY_AND_TARGET_SELECTION.md)
- [`docs/roadmap/T356_JOHN3_WJ_OWNER_REVIEW_DOCKET.md`](docs/roadmap/T356_JOHN3_WJ_OWNER_REVIEW_DOCKET.md)
- [`docs/roadmap/T358_BIBLE_WIDE_CHUNKING_RESEARCH_REGISTRY.md`](docs/roadmap/T358_BIBLE_WIDE_CHUNKING_RESEARCH_REGISTRY.md)
- [`docs/roadmap/T359_SOURCE_METADATA_RESEARCH_ATLAS.md`](docs/roadmap/T359_SOURCE_METADATA_RESEARCH_ATLAS.md)
- [`docs/roadmap/T360_APOCALYPTIC_PROPHETIC_INTERTEXT_DOSSIERS.md`](docs/roadmap/T360_APOCALYPTIC_PROPHETIC_INTERTEXT_DOSSIERS.md)
- [`docs/roadmap/T361_EPISTLE_ARGUMENT_THEOLOGICAL_ISSUE_DOSSIERS.md`](docs/roadmap/T361_EPISTLE_ARGUMENT_THEOLOGICAL_ISSUE_DOSSIERS.md)
- [`.ai/tasks/T351.task.yaml`](.ai/tasks/T351.task.yaml) - completed Bible-wide research triage before more chunking work
- [`.ai/tasks/T352.task.yaml`](.ai/tasks/T352.task.yaml) - completed epistle argument review-packet prep
- [`.ai/tasks/T353.task.yaml`](.ai/tasks/T353.task.yaml) - completed divine capitalization inventory harness
- [`.ai/tasks/T354.task.yaml`](.ai/tasks/T354.task.yaml) - completed WJ/red-letter marker inventory harness
- [`.ai/tasks/T355.task.yaml`](.ai/tasks/T355.task.yaml) - completed WJ speaker/discourse policy and target selection
- [`.ai/tasks/T356.task.yaml`](.ai/tasks/T356.task.yaml) - active John 3 WJ owner-review docket
- [`.ai/tasks/T358.task.yaml`](.ai/tasks/T358.task.yaml) - completed Bible-wide chunking research registry
- [`.ai/tasks/T359.task.yaml`](.ai/tasks/T359.task.yaml) - completed source metadata research atlas
- [`.ai/tasks/T360.task.yaml`](.ai/tasks/T360.task.yaml) - completed apocalyptic prophetic intertext dossier queue
- [`.ai/tasks/T361.task.yaml`](.ai/tasks/T361.task.yaml) - completed epistle argument theological issue dossier queue
- [`.ai/handoffs/T352/handoff.md`](.ai/handoffs/T352/handoff.md) - handoff for epistle argument review-packet prep
- [`.ai/handoffs/T353/handoff.md`](.ai/handoffs/T353/handoff.md) - handoff for divine capitalization inventory harness
- [`.ai/handoffs/T354/handoff.md`](.ai/handoffs/T354/handoff.md) - handoff for WJ/red-letter marker inventory harness
- [`.ai/handoffs/T355/handoff.md`](.ai/handoffs/T355/handoff.md) - handoff for WJ speaker/discourse policy and John 3 target selection
- [`.ai/handoffs/T356/handoff.md`](.ai/handoffs/T356/handoff.md) - handoff for John 3 WJ owner-review docket
- [`.ai/handoffs/T358/handoff.md`](.ai/handoffs/T358/handoff.md) - handoff for Bible-wide chunking research registry
- [`.ai/handoffs/T359/handoff.md`](.ai/handoffs/T359/handoff.md) - handoff for source metadata research atlas
- [`.ai/handoffs/T360/handoff.md`](.ai/handoffs/T360/handoff.md) - handoff for apocalyptic prophetic intertext dossier queue
- [`.ai/handoffs/T361/handoff.md`](.ai/handoffs/T361/handoff.md) - handoff for epistle argument theological issue dossier queue
- [`docs/roadmap/T350_BIBLE_WIDE_CHUNKING_READINESS_PLAN.md`](docs/roadmap/T350_BIBLE_WIDE_CHUNKING_READINESS_PLAN.md)
- [`.ai/control/t340_psalm_candidate_promotion_decision.yaml`](.ai/control/t340_psalm_candidate_promotion_decision.yaml)
- [`config/governance/repository_link_contract.yaml`](config/governance/repository_link_contract.yaml)
- [`.ai/control/boundary_material_routing.yaml`](.ai/control/boundary_material_routing.yaml)
- [`config/governance/predicate_registry.yaml`](config/governance/predicate_registry.yaml)
- [`config/agents/agent_roles.yaml`](config/agents/agent_roles.yaml)
- [`config/agents/model_routing.yaml`](config/agents/model_routing.yaml)
- [`config/agents/agent_hostile_policy.yaml`](config/agents/agent_hostile_policy.yaml)

## Workflows And Templates

- [`.ai/audits/README.md`](.ai/audits/README.md) - no-context review and red-team audit entry point; tags: `audit`, `no-context-review`, `red-team`
- [`.ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md`](.ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md) - independent reviewer instructions; tags: `audit`, `review-protocol`
- [`.ai/audits/templates/REVIEW_REPORT_TEMPLATE.md`](.ai/audits/templates/REVIEW_REPORT_TEMPLATE.md) - durable review report template; tags: `audit`, `review-report`
- [`.ai/control/audit_surface_map.yaml`](.ai/control/audit_surface_map.yaml) - machine-readable audit surface map; tags: `audit`, `surface-map`, `machine-readable`
- [`.ai/control/harness_upgrade_roadmap.yaml`](.ai/control/harness_upgrade_roadmap.yaml) - future harness upgrade watchlist and roadmap; tags: `harness`, `validation`, `watchlist`
- [`scripts/agent/no_context_audit_harness.py`](scripts/agent/no_context_audit_harness.py) - generates no-context audit briefs; tags: `audit`, `automation`, `brief-generator`
- [`scripts/validate_task_scope.py`](scripts/validate_task_scope.py) - HARN-001 protected-path and task-scope diff validator; tags: `task-scope`, `protected-paths`, `validation`
- [`scripts/validate_owner_selection_implementation_gate.py`](scripts/validate_owner_selection_implementation_gate.py) - HARN-012 gate blocking T345/output-changing work until owner selection and governed evidence agree; tags: `owner-decision`, `implementation-gate`, `validation`
- [`scripts/validate_source_metadata_authority.py`](scripts/validate_source_metadata_authority.py) - HARN-006 scanner keeping source metadata evidence from becoming boundary, lexical, intertext, graph-edge, or truth authority; tags: `source-metadata`, `authority`, `validation`
- [`scripts/validate_source_metadata_research_atlas.py`](scripts/validate_source_metadata_research_atlas.py) - checks the source-metadata research atlas, observed sidecar counts, metadata families, priority cases, and non-authorization flags; tags: `source-metadata`, `research-atlas`, `validation`
- [`scripts/validate_apocalyptic_prophetic_intertext_dossier_queue.py`](scripts/validate_apocalyptic_prophetic_intertext_dossier_queue.py) - checks the apocalyptic/prophetic intertext dossier queue, hermeneutic preservation policy, source cross-reference limits, required dossiers, and non-authorization flags; tags: `apocalyptic`, `prophetic`, `intertext`, `validation`
- [`scripts/validate_epistle_argument_theological_issue_dossier_queue.py`](scripts/validate_epistle_argument_theological_issue_dossier_queue.py) - checks the epistle argument theological issue dossier queue, preserved orthodox options, T352 packet dependencies, and non-authorization flags; tags: `epistle`, `argument-boundary`, `theology-risk`, `validation`
- [`scripts/validate_divine_capitalization_inventory.py`](scripts/validate_divine_capitalization_inventory.py) - rebuilds/checks the divine capitalization inventory and fails if it is stale or authorizing
- [`scripts/build_divine_capitalization_inventory.py`](scripts/build_divine_capitalization_inventory.py) - regenerates the evidence-only capitalization inventory from canonical word tokens
- [`scripts/validate_wj_marker_inventory.py`](scripts/validate_wj_marker_inventory.py) - rebuilds/checks the WJ/red-letter marker inventory and fails if it is stale or authorizing
- [`scripts/build_wj_marker_inventory.py`](scripts/build_wj_marker_inventory.py) - regenerates the evidence-only WJ marker inventory from canonical word tokens
- [`scripts/validate_wj_speaker_discourse_policy.py`](scripts/validate_wj_speaker_discourse_policy.py) - checks the WJ speaker/discourse policy, John 3 target selection, and non-authorization flags
- [`scripts/validate_john3_owner_review_docket.py`](scripts/validate_john3_owner_review_docket.py) - checks the pending John 3 owner-review docket and non-authorization flags
- [`scripts/validate_bible_wide_chunking_research_registry.py`](scripts/validate_bible_wide_chunking_research_registry.py) - checks canonical 66 research registry coverage, sensitive watchpoints, and non-authorization flags
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
