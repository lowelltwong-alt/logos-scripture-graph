# T461 Scripture Front-Door Decomposition Audit

## Verdict

T461 is a control-plane findability hardening PR. It keeps `AI_FRONT_DOOR.md` as the stable operating-rules entry point, moves volatile T3xx/T4xx task-history narrative into `docs/roadmap/TASK_LEDGER.md`, and adds deterministic validation so the split cannot hide task history, non-authorizations, or no-context audit routes.

## Scope Reviewed

- Compact front door: `AI_FRONT_DOOR.md`
- Moved task ledger: `docs/roadmap/TASK_LEDGER.md`
- AI TOC routing: `AI_TABLE_OF_CONTENTS.md`
- Roadmap TOC routing: `docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md`
- Lesson memory: `.ai/control/chunking_lesson_index.yaml` (`LSN-047`)
- Decision register: `.ai/control/chunking_theological_decision_register.yaml` (`CD-091`)
- Validator: `scripts/validate_task_ledger.py`
- Tests: `tests/test_task_ledger.py`
- Task/handoff: `.ai/tasks/T461.task.yaml`, `.ai/handoffs/T461/handoff.md`

## Audit Checks

- Front door remains under the T461 maximum of 250 lines.
- Mandatory read order is sequential and points to task ledger, AI TOCs, lesson index, test-runtime preflight, and coding-runtime preflight.
- Moved task-history narrative remains discoverable in `docs/roadmap/TASK_LEDGER.md`.
- Standing non-authorizations remain visible: no chunk output, reviewed gold, child spans, route/evaluator behavior, graph/retrieval/vector truth, source rows, canon changes, preferred readings, or theology authority.
- Legacy validator anchors remain visible so older gates can still discover protected surfaces after the split.
- No canonical/raw Scripture data, generated chunk output, graph output, retrieval output, vector output, source rows, boundary import, route/evaluator behavior, preferred readings, source-tradition preference, canon scope, or theology authority changed.

## No-Context Reviewer Instructions

Read `AI_FRONT_DOOR.md`, `docs/roadmap/TASK_LEDGER.md`, `AI_TABLE_OF_CONTENTS.md`, `docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md`, `.ai/control/chunking_lesson_index.yaml`, and `scripts/validate_task_ledger.py`.

Review whether the front door is now easier to use without losing:

- required startup routing,
- Fable PR-7 task-history preservation,
- audit/no-context routing,
- protected decision-register discoverability,
- chunking non-authorizations,
- runtime-preflight lessons for long validation commands.

## Known Residual Risk

The compatibility anchor bank is intentionally dense because many historical validators use exact substring discovery. Future work may replace that with structured metadata, but this PR does not broaden that validator architecture.

## Validation

- `python scripts\validate_task_ledger.py`: passed
- `python scripts\validate_chunking_lesson_index.py`: passed
- `python scripts\validate_chunking_theological_decision_register.py`: passed after adding `CD-091`
- `python scripts\validate_repository_link_contract.py`: passed
- `python scripts\validate_coding_runtime_language_preflight.py`: passed
- `python scripts\validate_governance_memory_durability.py`: passed
- `python scripts\validate_source_metadata_authority.py`: passed
- `python scripts\validate_all.py`: passed
- `python -m pytest tests\test_task_ledger.py tests\test_chunking_lesson_index.py tests\test_chunking_agent_preflight.py tests\test_governance_memory_durability.py tests\test_source_metadata_authority.py tests\test_control_plane.py tests\test_t424_rust_fast_validators.py -q`: passed, 49 passed
- `python -m pytest -q`: failed because generated canonical sidecars such as `data/canonical/translations/eng-web/word_tokens.jsonl` are absent in this clean control-plane worktree
- `python scripts\generate_data_map.py --check`: failed because the generated-data sidecars are absent and T461 does not authorize rewriting `DATA_MAP.md` for a sparse worktree
- `git diff --check`: passed with line-ending warnings only

The generated-data failures are not fixed in this PR because T461 forbids touching `data/canonical/`, `data/processed/`, and generated Scripture surfaces.
