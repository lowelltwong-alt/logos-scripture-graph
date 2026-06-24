# Task Handoff

## Task

- task_id: T399
- title: Focused Bible-wide research queue
- phase: Goal 2 focused research after T398
- status: complete_goal2_focused_research_queue

## Agent

- agent_name: codex
- mode: implementation
- stage: final
- updated_at: 2026-06-24T01:50:00+00:00
- handoff_id: t399-focused-bible-wide-research-queue

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/t398_bible_wide_phase_one_research_synthesis.yaml
- .ai/control/bible_verse_passage_coverage_summary.yaml
- .ai/control/bible_verse_passage_readiness_matrix.yaml
- .ai/control/bible_verse_passage_gap_register.yaml
- .ai/control/bible_verse_passage_human_review_docket.yaml
- .ai/control/*_dossier_queue.yaml
- .ai/control/source_metadata_research_atlas.yaml
- .ai/control/original_language_phrase_context_policy.yaml
- .ai/control/contextual_reading_policy.yaml
- .ai/control/orthodox_hermeneutic_firewall_docket.yaml

## Files changed

- .ai/control/t399_focused_bible_wide_research_queue.yaml
- docs/roadmap/T399_FOCUSED_BIBLE_WIDE_RESEARCH_QUEUE.md
- .ai/tasks/T399.task.yaml
- .ai/audits/reports/20260624-T399-focused-bible-wide-research-queue.md
- .ai/audits/reports/README.md
- .ai/control/chunking_theological_decision_register.yaml
- .ai/control/chunking_lesson_index.yaml
- .ai/control/chunking_agent_preflight.yaml
- .ai/control/bible_chunking_readiness_map.yaml
- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md
- ROADMAP_STATE.yaml
- .ai/control/PROJECT_STATUS.md
- .ai/control/current_focus.yaml
- .ai/control/roadmap_events.jsonl
- .ai/control/handoff_ledger.jsonl
- scripts/validate_t399_focused_bible_wide_research_queue.py
- scripts/validate_all.py
- tests/test_t399_focused_bible_wide_research_queue.py

## Decisions made

- CD-073 records that T399 is a scored, non-output-changing focused research queue and owner-decision map only.
- LSN-027 records the reusable lesson that focused research score, review-only safety, and authority must remain separate.
- T399 does not depend on unmerged/conflicted T396/PR #116 source rows and creates no source/manuscript rows.
- T397 remains the current Goal 6 route-isolated harness prep path for Eph.1.3-Eph.1.14.

## Validation run

- command: python scripts/validate_t399_focused_bible_wide_research_queue.py
- result: passed
- command: python scripts/validate_all.py
- result: passed after local canonical sidecar regeneration with `python pipelines/ingest/usfm_importer.py --canonical-66-filter`
- command: python -m pytest -q
- result: passed, 598 tests in 444.20s
- failures: none

## Known risks

- A high T399 score is research priority, not authority.
- T399-HDM recommendations are not owner selections.
- Variant/source-tradition-heavy candidates remain blocked before promotion or implementation.
- No target selection, reviewed gold, child spans, output, route/evaluator behavior, graph/retrieval/vector truth, boundary import, preferred reading/source tradition, canon change, source/manuscript row work, whole-Bible output, or theology authority is authorized by T399.

## Open questions

- Owner must choose one T399-HDM option before any new review-packet strengthening that follows Goal 2.
- T397 harness prep remains separately available and does not require the T399 owner-decision selection.

## Next agent instruction

Run the T399 validator and full validation stack. If green, open the T399 PR. After merge, keep T397 as the current Eph.1.3-Eph.1.14 harness route and ask the owner to choose one T399-HDM option before any new review-packet strengthening.
