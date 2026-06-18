# Task Handoff

## Task

- task_id: T356
- title: John 3 WJ Owner Review Docket
- phase: phase_4
- status: complete

## Agent

- agent_name: codex
- mode: implementation
- stage: final
- updated_at: 2026-06-17T23:32:17-04:00
- handoff_id: t356-final

## Files read

- AGENTS.md
- AI_FRONT_DOOR.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/current_focus.yaml
- .ai/control/wj_speaker_discourse_policy.yaml
- .ai/control/wj_marker_inventory.yaml
- .ai/control/chunking_agent_preflight.yaml
- .ai/control/chunking_theological_decision_register.yaml
- .ai/control/bible_chunking_readiness_map.yaml
- .ai/handoffs/T355/handoff.md
- eval/chunking_gold/review_packets/john3_wj_speaker_boundary_review.md

## Files changed

- .ai/control/john3_wj_owner_review_docket.yaml
- docs/roadmap/T356_JOHN3_WJ_OWNER_REVIEW_DOCKET.md
- scripts/validate_john3_owner_review_docket.py
- tests/test_john3_owner_review_docket.py
- .ai/tasks/T356.task.yaml
- .ai/handoffs/T356/handoff.md
- .ai/control/chunking_agent_preflight.yaml
- .ai/control/chunking_theological_decision_register.yaml
- .ai/control/bible_chunking_readiness_map.yaml
- .ai/control/bible_chunking_research_triage_map.yaml
- scripts/validate_chunking_agent_preflight.py
- scripts/validate_bible_chunking_readiness_map.py
- scripts/validate_owner_selection_implementation_gate.py
- scripts/validate_wj_speaker_discourse_policy.py
- scripts/validate_all.py
- ROADMAP_STATE.yaml
- .ai/control/current_focus.yaml
- .ai/control/PROJECT_STATUS.md
- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md
- docs/methodology/WORKFLOW_LESSONS.md
- .ai/tasks/T344.task.yaml
- tests updated for the current non-authorizing route and task scope
- .ai/control/roadmap_events.jsonl
- .ai/control/handoff_ledger.jsonl

## Decisions made

- T356 records John 3 owner-review options only; owner selection remains pending.
- The docket keeps all implementation, output-change, reviewed-gold, parent-span, child-span, speaker-attribution, graph-edge, retrieval-truth, and generated-chunk flags false.
- Option B is recorded as the lowest-risk implementation-useful future option because it would approve only the parent review scope, leaving internal speaker/discourse boundaries unresolved.
- Option C records exact child-span candidates only as review candidates and preserves the John.3.9-John.3.21 disputed zone as requiring explicit owner handling.
- Claude no-context audit P2 fixes were accepted: AI_FRONT_DOOR no longer says T352 is next, and `.ai/tasks/T344.task.yaml` now matches the completed T344 owner-selection state.
- Maintainer TOC-routing lesson was accepted: AI TOCs now expose searchable tags and use-when triggers, with `WORKFLOW-LESSON-004` requiring future AI TOCs to be functional routing surfaces for audit, developer-engineering, governance, validation, chunking, and user workflows.

## Validation run

- `python scripts\validate_john3_owner_review_docket.py`: pass
- `python scripts\validate_chunking_agent_preflight.py`: pass
- `python scripts\validate_bible_chunking_readiness_map.py`: pass
- `python scripts\validate_owner_selection_implementation_gate.py`: pass
- `python scripts\validate_wj_speaker_discourse_policy.py`: pass
- `python scripts\validate_chunking_theological_decision_register.py --changed-file docs/roadmap/T356_JOHN3_WJ_OWNER_REVIEW_DOCKET.md --changed-file .ai/control/chunking_theological_decision_register.yaml`: pass
- `python scripts\validate_task_scope.py --task-id T356`: pass
- `python -m pytest -q tests\test_john3_owner_review_docket.py tests\test_chunking_agent_preflight.py tests\test_bible_chunking_readiness_map.py tests\test_task_scope_validator.py tests\test_ai_roadmap_table_of_contents.py tests\test_t351_bible_wide_research_triage.py tests\test_t344_revelation_owner_selection.py tests\test_t343_revelation_review_packet.py tests\test_t342_revelation_candidate_selection.py tests\test_t337_selection_docs.py tests\test_t337a_psalm_review_packet.py tests\test_owner_selection_implementation_gate.py`: pass, 66 passed
- `python -m pytest -q tests\test_chunking_agent_preflight.py tests\test_t344_revelation_owner_selection.py tests\test_task_scope_validator.py tests\test_john3_owner_review_docket.py`: pass, 26 passed
- `python -m pytest -q tests\test_ai_roadmap_table_of_contents.py tests\test_chunking_agent_preflight.py tests\test_task_scope_validator.py`: pass, 23 passed
- `python scripts\validate_all.py`: pass, all validation gates passed
- `python -m pytest -q`: pass, 331 passed

## Known risks

- A future agent could mistake the docket's candidate child spans for approved reviewed gold.
- John.3.9-John.3.21 remains a sensitive Jesus/narrator boundary and must not be inferred from WJ formatting.
- Any later implementation must prove non-target identity and avoid leaking John 3 speaker/discourse behavior into other Gospel or Revelation WJ cases.

## Open questions

- Which option does the owner select: `JOHN3-T356-A`, `JOHN3-T356-B`, `JOHN3-T356-C`, `JOHN3-T356-D`, or `JOHN3-T356-E`?
- If the owner selects `JOHN3-T356-C`, what is the explicit status of `John.3.9-John.3.21`: Jesus speech, narrator/commentary, or unresolved for chunking?

## Next agent instruction

Do not implement John 3 chunks from this docket. The next safe action is owner selection of one
T356 option. Any future output-changing task requires exact owner selection, reviewed
speaker/discourse gold or equivalent governed evidence, executable tests, non-target identity
proof, same-baseline evaluation, and later implementation authorization.
