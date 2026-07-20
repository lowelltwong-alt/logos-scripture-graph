# Task Handoff

## Task

- task_id: T519
- title: Preserve typed footnotes inside editorial heading bodies
- phase: phase_4
- status: in_progress_code_and_fixture_proof

## Agent

- agent_name: cursor
- mode: build
- stage: final
- updated_at: 2026-07-20T19:15:00+00:00
- handoff_id: f15b4c42c0df2e97

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/handoffs/T475/handoff.md
- .ai/control/t475_usfm_shadow_delta_gate.yaml
- .ai/control/t474_usfm_marker_anchor_contract.yaml
- pipelines/ingest/usfm_importer.py
- pipelines/ingest/usfm_inline_parser.py
- tests/test_t474_usfm_marker_anchor_contract.py

## Files changed

- pipelines/ingest/usfm_importer.py
- tests/test_t474_usfm_marker_anchor_contract.py
- .ai/tasks/T519.task.yaml
- .ai/handoffs/T519/handoff.md
- .ai/control/t474_usfm_marker_anchor_contract.yaml
- .ai/control/t475_usfm_shadow_delta_gate.yaml
- .ai/control/PROJECT_STATUS.md
- .ai/control/chunking_lesson_index.yaml
- .ai/control/chunking_theological_decision_register.yaml
- ROADMAP_STATE.yaml
- docs/roadmap/T519_EDITORIAL_HEADING_FOOTNOTE_PRESERVATION.md
- docs/roadmap/TASK_LEDGER.md
- docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md

## Decisions made

- Owner Lowell Wong authorized the narrow T519 repair on 2026-07-20.
- Added `emit_editorial_inline_sidecars` for `editorial_only` bodies: footnotes/crossrefs only; no witness append; no WordTokens.
- Restored exact baseline footnote IDs for Ps.46/90/145 (`…:2347:0001`, `…:4961:0001`, `…:8067:0001`); full-archive footnote count 1130.
- Recorded CD-124 and LSN-070.
- T476 remains blocked until formal T475 shadow re-freeze and independent audit.

## Validation run

- command: python -m pytest tests/test_t474_usfm_marker_anchor_contract.py -q
- result: pass (6 tests)
- failures: none

- command: full-archive `usfm_importer.py --canonical-66-filter` into `build/T519_verify`
- result: pass — footnotes.jsonl count 1130; three heading footnotes present with baseline IDs
- failures: none

## Known risks

- Formal T475 alternating shadow re-freeze not yet re-run against a committed candidate_ref tip.
- Committed `data/canonical` still reflects pre-T519 importer until a later owner-gated regeneration.
- Knowledge-manifest hash refresh may be required if T500 validators run against updated lesson/decision registers.

## Open questions

- None blocking the code/fixture proof. Shadow re-freeze + Claude audit remain the next gates before T476.

## Next agent instruction

1. Commit and open PR for T519.
2. Update `.ai/control/t475_usfm_shadow_delta_gate.yaml` `candidate_ref` to the merged/repair tip and re-run `scripts/run_t475_shadow_delta.py`.
3. Require zero footnote removals; freeze evidence; run independent Claude audit via `.ai/prompts/t475_independent_audit_prompt.md`.
4. Only then open T476 owner packet. Do not regenerate committed canonical data in this task.

## Non-Authorizations Preserved

No committed regeneration, reviewed gold, chunk output, child spans, route/evaluator behavior, graph/retrieval/vector truth, preferred reading, canon change, theology authority, or T476 packet.

---

## Handoff refresh: final

- agent_name: cursor
- mode: 
- updated_at: 2026-07-20T19:06:26+00:00
- handoff_id: 02ffa8e0a0aa8657

---

## Handoff refresh: final

- agent_name: cursor
- mode: 
- updated_at: 2026-07-20T19:07:21+00:00
- handoff_id: 02ffa8e0a0aa8657
