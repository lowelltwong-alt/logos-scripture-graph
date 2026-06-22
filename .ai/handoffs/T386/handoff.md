# Task Handoff

## Task

- task_id: T386
- title: Bible-Wide Verse/Passage Coverage Inventory
- phase: phase_4
- status: complete_non_output_changing_coverage

## Agent

- agent_name: Codex
- mode: governance
- stage: final
- updated_at: 2026-06-22T12:00:00+00:00

## Files read

- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `ROADMAP_STATE.yaml`
- `.ai/control/chunking_agent_preflight.yaml`
- `.ai/control/t384_bible_wide_research_readiness_synthesis.yaml`
- `.ai/control/bible_chunking_readiness_map.yaml`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/chunking_lesson_index.yaml`
- canonical passage and eng-web sidecar JSONL files under `data/canonical/`
- existing dossier queues and owner-review dockets under `.ai/control/`

## Files changed

- Added `.ai/control/bible_verse_passage_coverage_inventory.jsonl`
- Added `.ai/control/bible_verse_passage_coverage_taxonomy.yaml`
- Added `.ai/control/bible_verse_passage_coverage_summary.yaml`
- Added `.ai/control/bible_verse_passage_readiness_matrix.yaml`
- Added `.ai/control/bible_verse_passage_gap_register.yaml`
- Added `.ai/control/bible_verse_passage_human_review_docket.yaml`
- Added `scripts/build_bible_verse_passage_coverage_inventory.py`
- Added `scripts/validate_bible_verse_passage_coverage_inventory.py`
- Added `tests/test_bible_verse_passage_coverage_inventory.py`
- Added `.ai/control/test_runtime_preflight.yaml`
- Added `scripts/validate_test_runtime_preflight.py`
- Added `tests/test_test_runtime_preflight.py`
- Added `docs/roadmap/T386_BIBLE_VERSE_PASSAGE_COVERAGE_INVENTORY.md`
- Added `.ai/tasks/T386.task.yaml`
- Added `.ai/audits/reports/20260622-T386-bible-verse-passage-coverage.md`
- Updated preflight, decision register, lesson index, readiness map, roadmap/status, AI TOCs, audit README, roadmap events, `validate_all.py`, and related validators.

## Decisions made

- Recorded `CD-062`: T386 accounts every canonical passage before chunk-output work resumes.
- Recorded `LSN-014`: every canonical passage needs deterministic coverage before chunking resumes.
- Recorded `LSN-015` and `WORKFLOW-LESSON-010`: full pytest can exceed the default 5-minute tool timeout, so future agents must read `.ai/control/test_runtime_preflight.yaml`, use the longer timeout or split strategy, and never treat timeout as green.
- Preserved T385 as the exact next non-output owner decision packet, now requiring both T384 synthesis and T386 coverage inputs.
- Kept all T386 outputs non-authorizing and evidence/review-readiness only.

## Validation run

- `python scripts/validate_bible_verse_passage_coverage_inventory.py --skip-repo-wiring` - passed.
- `python scripts/validate_test_runtime_preflight.py` - passed.
- `python scripts/validate_chunking_agent_preflight.py` - passed.
- `python scripts/validate_chunking_lesson_index.py` - passed.
- `python scripts/validate_bible_chunking_readiness_map.py` - passed.
- `python scripts/validate_chunking_theological_decision_register.py` - passed.
- `python scripts/validate_t384_bible_wide_research_readiness.py` - passed.
- `python scripts/validate_bible_verse_passage_coverage_inventory.py` - passed, 31,103 canonical passage records.
- `python scripts/validate_task_scope.py --task-id T386` - passed.
- `python scripts/agent/validate_handoffs.py` - passed for 92 referenced handoff paths.
- `python scripts/validate_all.py` - passed all gates.
- `python -m pytest -q` with `600000` ms timeout - passed, 534 tests in 447.36 seconds.
- Runtime lesson: an earlier `python -m pytest -q` run timed out at the 5-minute tool timeout, then exposed one stale readiness-map assertion when rerun with longer timeout. The test was fixed, and `.ai/control/test_runtime_preflight.yaml` now records this for future agents.

## Known risks

- The coverage inventory is intentionally large because it records one JSONL row per canonical passage.
- Coverage flags are triage/readiness signals, not theological conclusions or output authorization.
- Some passages are marked blocked before chunking because textual-variant/source-tradition or authority-sensitive handling requires later exact owner review.
- Full pytest is long-running in this worktree; do not use a 5-minute timeout and do not treat timeout as green.

## Open questions

- None for T386. The next human-facing work is T385, which must present options and repercussions before any target selection, promotion, implementation, output, graph/retrieval/vector, boundary, source-tradition, canon, or theology authority decision.

## Next agent instruction

Run the full validation gates. If green, publish the T386 non-output PR. After merge, start T385 owner decision packet using:

- `.ai/control/t384_bible_wide_research_readiness_synthesis.yaml`
- `.ai/control/bible_verse_passage_coverage_summary.yaml`
- `.ai/control/bible_verse_passage_gap_register.yaml`
- `.ai/control/bible_verse_passage_human_review_docket.yaml`

Do not implement chunks, promote reviewed gold, add child spans, change routes/evaluators, generate graph/retrieval/vector truth, import boundaries, select preferred readings/source traditions, change canon scope, or authorize theology claims.
