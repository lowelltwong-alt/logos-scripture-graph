# T451 Handoff - Bible Edge Candidate Type Catalog

## Task

- Task id: T451
- Agent: Codex
- Mode: planning/control-plane, non-authorizing
- Branch: `codex/t451-bible-edge-taxonomy-deepening`

## Files Read

- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `config/governance/predicate_registry.yaml`
- `schemas/graph_edge_record.schema.json`
- `schemas/relationship_object.schema.json`
- `.ai/control/bible_edge_taxonomy_research_program.yaml`
- `.ai/control/orthodox_hermeneutic_firewall_docket.yaml`
- `.ai/control/contextual_reading_policy.yaml`
- `.ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml`
- `.ai/control/narrative_legal_covenant_dossier_queue.yaml`
- `.ai/control/gospel_wj_discourse_dossier_queue.yaml`
- `.ai/control/epistle_argument_theological_issue_dossier_queue.yaml`
- `.ai/control/wisdom_dialogue_poetry_dossier_queue.yaml`
- `.ai/control/prophetic_oracle_vision_dossier_queue.yaml`

## Files Changed

- `.ai/tasks/T451.task.yaml`
- `.ai/control/bible_edge_candidate_type_catalog.yaml`
- `.ai/context/agent_work/T451/edge_taxonomy_research_notes.md`
- `.ai/prompts/bible_edge_taxonomy_model_review_prompt.md`
- `.ai/prompts/bible_edge_taxonomy_frontier_audit_prompt.md`
- `docs/roadmap/T451_BIBLE_EDGE_CANDIDATE_TYPE_CATALOG.md`
- `scripts/validate_t451_bible_edge_candidate_type_catalog.py`
- `tests/test_t451_bible_edge_candidate_type_catalog.py`
- `.digital-asset/context-map.json`
- `.digital-asset/lessons/t451_bible_edge_candidate_type_catalog.yaml`
- `.digital-asset/mail/outbox.jsonl`
- `scripts/validate_all.py`
- `.ai/control/PROJECT_STATUS.md`

## Decisions Made

- T451 deepens T450 into a candidate edge-type catalog, not a predicate registry change.
- All candidate types remain `candidate_type_only`.
- High-risk families require frontier review before any owner gate or future predicate proposal.
- Post-review P2 hardening requires the catalog's registered-predicate snapshot to match `config/governance/predicate_registry.yaml`.
- Post-review P2 hardening requires every candidate edge type to preserve at least one explicit authority/output/truth-denial in `never_auto_create`.
- Domain-review P2 hardening splits observed place-name occurrence from site/route identification candidates.
- Domain-review P2 hardening adds explicit person, kinship, people-group, and office-role evidence coverage.
- Rust is deferred to a future deterministic edge-candidate JSONL hygiene validator; this task's small semantic policy validator remains Python.

## Validation Performed

- `python scripts/validate_t451_bible_edge_candidate_type_catalog.py` - passed, 56 candidate edge types
- `python -m pytest tests/test_t451_bible_edge_candidate_type_catalog.py -q` - 8 passed
- `python scripts/validate_dad_outbox.py` - passed
- `python scripts/validate_task_scope.py --task-id T451` - passed
- `python scripts/agent/validate_handoffs.py` - passed
- `python scripts/validate_chunking_theological_decision_register.py` - passed
- `python scripts/validate_chunking_lesson_index.py` - passed
- First `python scripts/validate_all.py` run failed because this fresh worktree lacked ignored generated canonical files.
- `python pipelines/ingest/usfm_importer.py --canonical-66-filter` generated ignored local canonical files.
- Rerun `python scripts/validate_all.py` - all validation gates passed
- Post-review sandboxed `python scripts/validate_all.py` attempt failed on temp/Cargo access-denied environment noise.
- Unsandboxed post-review rerun `python scripts/validate_all.py` - all validation gates passed
- Two sandboxed `python -m pytest -q` attempts failed on `WinError 5` pytest temp-directory access/cleanup; treated as environment noise.
- One unsandboxed `python -m pytest -q` attempt timed out at the 30-minute ceiling while `validate_all.py` was running in parallel; rerun with a longer ceiling.
- Unsandboxed rerun `python -m pytest -q` - 762 passed in 1856.90s
- `python scripts/generate_data_map.py --check` - current
- `git diff --check` - passed

## Risks Introduced

- The taxonomy is broad and useful enough that a future agent could mistake it for graph authority. The validator and docs explicitly deny predicate expansion, edge generation, retrieval/vector truth, theology authority, and apologetic conclusions.

## Unresolved Questions

- Which proposed future predicate names should be registered, renamed, or rejected in a later T452 owner-gated proposal?
- Which edge families should never become graph predicates and remain only review tags?
- Which first low-risk structural/editorial sandbox should be chosen after owner review?

## Exact Next Action

Route the catalog through model review and Claude/frontier audit before any T452 predicate proposal. Do not expand the predicate registry, generate graph edges, populate candidate edge rows, or use this catalog as theology authority without a later exact owner gate.
