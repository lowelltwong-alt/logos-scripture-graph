# Task Handoff

## Task

- task_id: T397
- title: Eph.1.3-Eph.1.14 Route-Isolated Harness Prep
- phase: phase_4
- status: complete_non_output_changing_route_isolation_harness_prep

## Agent

- agent_name: codex
- mode: build
- stage: final
- updated_at: 2026-06-24T12:45:00+00:00
- handoff_id: t397-eph1-route-isolation-harness

## Files read

- AI_FRONT_DOOR.md
- .ai/control/chunking_agent_preflight.yaml
- .ai/control/chunking_theological_decision_register.yaml
- .ai/control/chunking_lesson_index.yaml
- .ai/control/bible_chunking_readiness_map.yaml
- .ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml
- eval/chunking_gold/per_form/epistle_argument_gold_manifest.json
- eval/chunking_gold/review_packets/eph1_3_14_argument_review.md
- ROADMAP_STATE.yaml

## Files changed

- .ai/control/t397_eph1_route_isolation_harness.yaml
- scripts/chunking/route_isolation_harness.py
- tests/test_route_isolation_harness.py
- scripts/validate_t397_eph1_route_isolation_harness.py
- tests/test_t397_eph1_route_isolation_harness.py
- docs/roadmap/T397_EPH1_ROUTE_ISOLATION_HARNESS.md
- .ai/tasks/T397.task.yaml
- .ai/audits/reports/20260624-T397-eph1-route-isolation-harness.md
- .ai/control/chunking_theological_decision_register.yaml
- .ai/control/chunking_lesson_index.yaml
- .ai/control/chunking_agent_preflight.yaml
- .ai/control/bible_chunking_readiness_map.yaml
- .ai/control/current_focus.yaml
- .ai/control/PROJECT_STATUS.md
- .ai/control/roadmap_events.jsonl
- .ai/control/test_runtime_preflight.yaml
- .ai/audits/reports/README.md
- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- ROADMAP_STATE.yaml
- docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md
- scripts/validate_all.py
- scripts/validate_bible_chunking_readiness_map.py
- scripts/validate_chunking_agent_preflight.py
- scripts/validate_chunking_lesson_index.py
- scripts/validate_owner_decision_projection_policy.py
- scripts/validate_owner_selection_implementation_gate.py
- scripts/validate_t372_route_isolation_harness_plan.py
- scripts/validate_t373_owner_implementation_authorization.py
- scripts/validate_t374_baseline_overlap_owner_decision_packet.py
- scripts/validate_1cor8_10_owner_review_docket.py
- scripts/validate_1cor8_10_parent_evidence_packet.py
- tests/test_bible_chunking_readiness_map.py
- tests/test_chunking_agent_preflight.py
- tests/test_chunking_lesson_index.py
- tests/test_ai_roadmap_table_of_contents.py
- tests/test_t342_revelation_candidate_selection.py
- tests/test_t343_revelation_review_packet.py
- tests/test_t344_revelation_owner_selection.py
- tests/test_test_runtime_preflight.py

## Decisions made

- Recorded CD-074: route-isolation harnesses prove output shape and non-target identity, but do not authorize output.
- Recorded LSN-028: harness readiness must be discoverable in preflight/TOCs/audit surfaces and still blocked behind owner output-pilot authorization.
- Preserved T394 reviewed-gold promotion as parent-only reviewed gold for Eph.1.3-Eph.1.14 while denying parent-span-as-chunk-boundary use until a future owner output-pilot gate.
- Kept T397 strictly non-output-changing: no chunks, child spans, route/evaluator behavior, graph/retrieval/vector truth, source/manuscript rows, boundary import, preferred readings/source traditions, canon-scope changes, or theology authority.
- Recorded that local full pytest with generated canonical data took about 13 minutes 51 seconds on T397 and should use a 1200000 ms timeout in future local desktop runs.

## Validation run

- command: python -m pytest -q tests/test_route_isolation_harness.py
- result: passed
- failures: none from the focused harness test
- command: python scripts/validate_all.py
- result: passed after regenerating ignored local canonical/processed outputs with python pipelines/ingest/usfm_importer.py --canonical-66-filter
- failures: none
- command: python -m pytest -q
- result: passed; 608 tests in 820.06 seconds
- failures: none

## Known risks

- Future output work must not treat T397 harness readiness as implementation permission.
- Future output work must run the harness against real baseline/candidate outputs and record same-baseline/no-context audit proof.
- A fresh owner output-pilot authorization is required before any parent-span-as-chunk-boundary use for Eph.1.3-Eph.1.14.

## Open questions

- None for T397 harness prep.

## Next agent instruction

Stop before output. If the owner explicitly authorizes a future Eph.1.3-Eph.1.14 output pilot, first create a new task scope that permits only the exact output paths, run the T397 route-isolation harness on real baseline/candidate outputs, require same-baseline evaluation, update the decision register and audit surfaces, and preserve all non-target output byte-identical.
