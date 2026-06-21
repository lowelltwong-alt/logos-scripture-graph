# Task Handoff

## Task

- task_id: T383
- title: Contextual Reading Policy
- phase: phase_4
- status: complete

## Agent

- agent_name: Codex
- mode: governance
- stage: final
- updated_at: 2026-06-21T02:05:00Z
- handoff_id: t383-contextual-reading-policy

## Files read

- `AI_FRONT_DOOR.md`
- `AI_TABLE_OF_CONTENTS.md`
- `ROADMAP_STATE.yaml`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/current_focus.yaml`
- `.ai/control/chunking_agent_preflight.yaml`
- `.ai/control/chunking_lesson_index.yaml`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/bible_chunking_readiness_map.yaml`
- `.ai/control/original_language_phrase_context_policy.yaml`
- `docs/methodology/WORKFLOW_LESSONS.md`
- `docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md`
- `scripts/validate_chunking_agent_preflight.py`
- `scripts/validate_chunking_lesson_index.py`
- `scripts/validate_bible_chunking_readiness_map.py`
- `scripts/validate_chunking_theological_decision_register.py`

## Files changed

- `.ai/control/contextual_reading_policy.yaml`
- `.ai/control/chunking_agent_preflight.yaml`
- `.ai/control/chunking_lesson_index.yaml`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/bible_chunking_readiness_map.yaml`
- `.ai/control/current_focus.yaml`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/roadmap_events.jsonl`
- `.ai/control/handoff_ledger.jsonl`
- `.ai/tasks/T383.task.yaml`
- `.ai/handoffs/T383/handoff.md`
- `.ai/audits/reports/20260621-T383-contextual-reading-policy.md`
- `.ai/audits/reports/README.md`
- `AI_FRONT_DOOR.md`
- `AI_TABLE_OF_CONTENTS.md`
- `ROADMAP_STATE.yaml`
- `docs/methodology/WORKFLOW_LESSONS.md`
- `docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md`
- `docs/roadmap/T383_CONTEXTUAL_READING_POLICY.md`
- `scripts/validate_contextual_reading_policy.py`
- `scripts/validate_chunking_agent_preflight.py`
- `scripts/validate_chunking_lesson_index.py`
- `scripts/validate_bible_chunking_readiness_map.py`
- `scripts/validate_all.py`
- `tests/test_contextual_reading_policy.py`
- `tests/test_chunking_agent_preflight.py`
- `tests/test_chunking_lesson_index.py`
- `tests/test_bible_chunking_readiness_map.py`
- `tests/test_ai_roadmap_table_of_contents.py`

## Decisions made

- Added `.ai/control/contextual_reading_policy.yaml` as mandatory contextual-reading preflight.
- Added `WORKFLOW-LESSON-006`: context always matters before chunking.
- Added `LSN-011`: context always matters.
- Added `CD-059`: contextual reading discipline is mandatory non-authorizing preflight.
- Recorded that historical/cultural background is evidence only and cannot govern Scripture, chunks, graph/retrieval truth, doctrine, or output.
- Recorded that no separate history repo is created by T383; any later sidecar must be lower-trust and owner-authorized.
- Preserved T376 as the next human owner lane-selection gate.

## Validation run

- command: `python scripts\validate_contextual_reading_policy.py`
- result: passed
- command: `python scripts\validate_chunking_agent_preflight.py`
- result: passed
- command: `python scripts\validate_chunking_lesson_index.py`
- result: passed
- command: `python scripts\validate_bible_chunking_readiness_map.py`
- result: passed
- command: `python scripts\validate_chunking_theological_decision_register.py`
- result: passed
- command: `python scripts\validate_task_scope.py --task-id T383`
- result: passed
- command: `python scripts\agent\validate_handoffs.py`
- result: passed
- command: `python scripts\validate_all.py`
- result: passed
- command: `python -m pytest -q`
- result: passed, 516 tests in 393.73 seconds
- failures: none

## Known risks

- Future agents may be tempted to treat "context required" as "context authorizes output"; T383 explicitly denies that and adds validators.
- Historical/cultural background can help reading but can also smuggle anti-supernatural or liberal-critical assumptions if not kept below Scripture authority.

## Open questions

- T376 owner lane selection is still the next human decision gate.
- A separate historical-background repo is not created now; it would require a later owner decision and governance contract.

## Next agent instruction

After T383 merges, proceed to T376 owner lane selection. Present serious faithful options and repercussions before selecting the next lane. Do not implement chunks, promote reviewed gold, create a history repo, alter evaluator formulas, generate graph/retrieval/vector truth, import boundaries, or run whole-Bible output from T383.
