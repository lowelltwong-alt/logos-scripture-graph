# Task Handoff

## Task

- task_id: T363
- title: Narrative Legal Covenant Dossier Queue
- phase: phase_4
- status: complete

## Agent

- agent_name: codex
- mode: implementation
- stage: final
- updated_at: 2026-06-18T15:35:00+00:00
- handoff_id: t363-final

## Files read

- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- ROADMAP_STATE.yaml
- .ai/control/PROJECT_STATUS.md
- .ai/control/current_focus.yaml
- .ai/control/bible_wide_chunking_research_registry.yaml
- .ai/control/narrative_legal_covenant_dossier_queue.yaml

## Files changed

- .ai/control/narrative_legal_covenant_dossier_queue.yaml
- .ai/control/bible_wide_chunking_research_registry.yaml
- .ai/control/chunking_agent_preflight.yaml
- .ai/control/chunking_theological_decision_register.yaml
- .ai/control/bible_chunking_readiness_map.yaml
- .ai/control/current_focus.yaml
- .ai/control/PROJECT_STATUS.md
- .ai/control/roadmap_events.jsonl
- .ai/control/handoff_ledger.jsonl
- .ai/tasks/T363.task.yaml
- .ai/handoffs/T363/handoff.md
- ROADMAP_STATE.yaml
- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- docs/roadmap/T363_NARRATIVE_LEGAL_COVENANT_DOSSIERS.md
- docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md
- scripts/validate_narrative_legal_covenant_dossier_queue.py
- scripts/validate_bible_wide_chunking_research_registry.py
- scripts/validate_chunking_agent_preflight.py
- scripts/validate_bible_chunking_readiness_map.py
- scripts/validate_all.py
- tests/test_narrative_legal_covenant_dossier_queue.py
- tests/test_bible_wide_chunking_research_registry.py
- tests/test_chunking_agent_preflight.py
- tests/test_bible_chunking_readiness_map.py
- tests/test_task_scope_validator.py
- tests/test_ai_roadmap_table_of_contents.py

## Decisions made

- T363 is research-only dossier prep for narrative, legal, covenant, genealogy/list, royal-annal, restoration-document, and Gospel birth narrative work.
- Scene, formula, list, document, covenant, and motif evidence remains evidence only.
- Added CD-029 to record the theological downstream risk of narrative/legal covenant dossiers as non-authorizing review memory.

## Validation run

- command: python scripts/validate_narrative_legal_covenant_dossier_queue.py
  - result: passed
- command: python scripts/validate_bible_wide_chunking_research_registry.py
  - result: passed
- command: python scripts/validate_chunking_agent_preflight.py
  - result: passed
- command: python scripts/validate_bible_chunking_readiness_map.py
  - result: passed
- command: python scripts/validate_task_scope.py --task-id T363
  - result: passed
- command: python scripts/validate_chunking_theological_decision_register.py --changed-file docs/roadmap/T363_NARRATIVE_LEGAL_COVENANT_DOSSIERS.md --changed-file .ai/control/chunking_theological_decision_register.yaml --changed-file .ai/control/narrative_legal_covenant_dossier_queue.yaml
  - result: passed
- command: python scripts/agent/validate_handoffs.py
  - result: passed for 72 referenced handoff paths
- command: python -m pytest -q tests/test_narrative_legal_covenant_dossier_queue.py tests/test_bible_wide_chunking_research_registry.py tests/test_chunking_agent_preflight.py tests/test_bible_chunking_readiness_map.py tests/test_ai_roadmap_table_of_contents.py tests/test_task_scope_validator.py tests/test_t337_selection_docs.py tests/test_t337a_psalm_review_packet.py tests/test_t342_revelation_candidate_selection.py tests/test_t343_revelation_review_packet.py tests/test_t344_revelation_owner_selection.py tests/test_t351_bible_wide_research_triage.py
  - result: 77 passed
- command: python scripts/validate_all.py
  - result: passed
- command: python -m pytest -q --maxfail=1
  - result: 379 passed

## Known risks

- Narrative scene labels can become implied causality or theological argument.
- Law/covenant formulae can encode covenant theology or law/gospel assumptions.
- Genealogies, lists, royal annals, embedded documents, and parallel accounts can become graph or retrieval authority before review.

## Open questions

- Which exact narrative/legal target should the owner review first after research-only prep?

## Next agent instruction

After T363 merges, continue research-only prep with wisdom/dialogue or prophetic/oracle dossiers, or
ask the owner to choose one exact review-packet target. Do not implement chunks, promote reviewed
gold, generate graph/retrieval/vector outputs, import boundary material, change evaluator or route
behavior, or treat these dossiers as authority.
