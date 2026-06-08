# Task Handoff

## Task

- task_id: T327B
- title: Canonical 66-Book Ingest Filter
- phase: phase_4
- status: complete

## Agent

- agent_name: Codex
- mode: build
- stage: final
- updated_at: 2026-06-08T21:00:00+00:00
- handoff_id: t327b-codex-20260608

## Files read

- AI_FRONT_DOOR.md
- .ai/control/boundary_material_routing.yaml
- docs/roadmap/T327A_FORENSIC_CANONICAL_CORPUS_SCOPE_AUDIT.md
- docs/roadmap/CANONICAL_66_BOOK_SCOPE_POLICY.md
- pipelines/ingest/usfm_importer.py
- pipelines/util/canon.py
- pipelines/util/usfm_to_osis.py
- scripts/validate_all.py
- tests/test_t327a_canonical_scope_audit.py
- tests/test_web_usfm_feature_extraction.py

## Files changed

- config/canon/canonical_66_books.yaml
- pipelines/util/canonical_scope.py
- pipelines/ingest/usfm_importer.py
- scripts/validate_canonical_66_scope.py
- scripts/validate_all.py
- tests/test_t327b_canonical_66_ingest_filter.py
- tests/test_web_usfm_feature_extraction.py
- docs/roadmap/T327B_CANONICAL_66_INGEST_FILTER.md
- docs/roadmap/CANONICAL_66_BOOK_SCOPE_POLICY.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/roadmap_events.jsonl
- .ai/tasks/T327B.task.yaml
- .ai/handoffs/T327B/handoff.md
- ROADMAP_STATE.yaml

## Decisions made

- T327A.1 routing guardrails were already live on `main`, so T327B was allowed to start.
- Added an explicit canonical 66-book allow-list and known-excluded list.
- Added a canonical-scope filter utility and config validator.
- Added an explicit WEB USFM importer `--canonical-66-filter` flag for T327C regeneration.
- The filter writes canonical records only for allowed 66-book Scripture books while preserving raw
  USFM event observation when the flag is enabled.
- Existing generated outputs may still contain non-66 records until T327C regeneration.
- T327D handles chunk/scorecard/leaderboard re-baselining.
- T327E cleans gold/stress/review packet surfaces.

## Validation run

- command: `python scripts/validate_all.py`
- result: passed, all validation gates passed.
- command: `python -m pytest -q`
- result: passed, `128 passed`.
- command: `git diff --check`
- result: passed.

## Known risks

- Existing generated outputs remain pre-filter until T327C.
- Scorecards and leaderboard remain pre-corpus-scope-correction until T327D.

## Open questions

- Whether T327C should preserve all raw USFM events or introduce a parallel canonical-only
  processed-event output.

## Next agent instruction

Review T327B. Do not start T327C until T327B is merged. Do not start T327F boundary intake.
