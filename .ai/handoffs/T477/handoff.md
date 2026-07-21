# Task Handoff

## Task

- task_id: T477
- title: Owner-Approved Canonical Regeneration And Baseline Reset
- phase: phase_4
- status: in_progress

## Agent

- agent_name: cursor
- mode: build
- stage: final
- updated_at: 2026-07-21T15:45:00+00:00
- handoff_id: t477c0ffee01

## Files read

- AI_FRONT_DOOR.md
- docs/roadmap/T476_CANONICAL_WEB_REPAIR_OWNER_PACKET.md
- .ai/control/t475_usfm_shadow_delta_gate.yaml
- .ai/audits/reports/20260720-T475-independent-shadow-delta-audit-post-t519.md
- pipelines/ingest/usfm_importer.py

## Files changed

- docs/roadmap/T476_CANONICAL_WEB_REPAIR_OWNER_PACKET.md (Option A recorded)
- docs/roadmap/T477_CANONICAL_REGENERATION_AND_BASELINE_RESET.md
- .ai/tasks/T476.task.yaml
- .ai/tasks/T477.task.yaml
- .ai/control/current_focus.yaml (T477)
- .ai/control/DATA_MAP.md (regenerated)
- .ai/control/t475_usfm_shadow_delta_gate.yaml (superseded_by T477)
- scripts/validate_t477_baseline_reset.py
- scripts/validate_all.py / conftest.py / validate_t475 gate updates
- tests/test_t477_baseline_reset.py
- decision register CD-126 / lesson LSN-072
- ROADMAP_STATE / PROJECT_STATUS / TASK_LEDGER / TOC

## Decisions made

- Lowell authorized T476 Option A (authorize T477).
- Regenerated eng-web with `--canonical-66-filter` to audited candidate counts.
- Gold/chunker/pilot assertions remain deferred through T478-T479.

## Validation run

- command: python pipelines/ingest/usfm_importer.py --canonical-66-filter
- result: word_tokens=677686, footnotes=1130, passages=31103
- command: python scripts/validate_t477_baseline_reset.py
- result: passed (exact semantic match to candidate_manifest_t519.json)
- command: validate_all / pytest (running)

## Known risks

- Deferred gold/pilot gates still encode pre-T474 expectations until T478-T479.
- DATA_MAP total JSONL count includes other candidate surfaces beyond eng-web sidecars.

## Open questions

- None for T477 authorization; T478 is next for Psalm 119/78 gold re-review.

## Next agent instruction

1. Finish/merge T477 PR after validate_all + pytest green.
2. Open T478 for Psalm 119 / Psalm 78 reviewed-gold re-review (no gold edits yet).
3. Do not emit chunk output or promote gold in T477.

## Non-Authorizations Preserved

No reviewed gold, chunk output, child spans, route/evaluator, graph/retrieval/vector,
preferred reading, canon, or theology authority in this task.

---

## Handoff refresh: final

- agent_name: cursor
- mode: 
- updated_at: 2026-07-21T15:40:00+00:00
- handoff_id: d28d08a17dd250d4
