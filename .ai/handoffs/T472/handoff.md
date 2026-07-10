# Task Handoff

## Task

- task_id: T472
- title: Multi-Model Panel Calibration And Provenance Correction
- phase: phase_4
- status: complete

## Agent

- agent_name: Codex
- mode: model_panel_calibration_and_provenance_correction_non_authorizing
- stage: final
- updated_at: 2026-07-10T00:00:00+00:00
- handoff_id: pending_force_handoff_final

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- T464 comparison artifacts and six frozen model manifests/maps
- T465 owner docket
- T471 refinement and owner-support docket
- T414/T415 2 John reviewed-gold/output surfaces
- T467/T468/T470 harness, faithful-route, and evidence policies
- DAD outbox, context-map, lesson-slot contract, and validator

## Files changed

- .ai/tasks/T472.task.yaml
- .ai/control/t472_model_panel_calibration_gate.yaml
- .ai/control/t472_2john_owner_packet.yaml
- .ai/context/agent_work/T472/
- docs/roadmap/T472_MODEL_PANEL_CALIBRATION_AND_PROVENANCE_CORRECTION.md
- docs/roadmap/T472_2JOHN_OWNER_PACKET.md
- scripts/build_t472_model_panel_calibration_gate.py
- scripts/validate_t472_model_panel_calibration_gate.py
- scripts/validate_t472_2john_owner_packet.py
- scripts/compare_multi_model_bible_chunk_maps.py
- scripts/t423_chunk_map_utils.py
- focused tests and validate_all wiring
- PROJECT_STATUS, current focus, CD-110, LSN-055, handoff ledger
- .digital-asset/mail/outbox.jsonl
- .digital-asset/context-map.json
- .digital-asset/lessons/t472_model_panel_calibration_lessons.yaml

## Findings

- The old 2 John whole-letter route was invalid. `2John.1.1-2John.1.13` is the disagreement region; the actual M4/M6 span is `2John.1.12-2John.1.13`.
- A whole-letter route overlaps existing reviewed gold/output at `2John.1.1-2John.1.3`.
- All 1,048 deltas were mechanically classified; 130 have region/model-span mismatch, 76 have chapter-coincident pair spans, 33 contain strict-larger calibrated dissent, and 951 retain frontier pressure.
- The legacy 19-row docket has zero owner-ready rows after correction.
- M1 and M5 are preserved as negative controls and audit evidence, not deleted. They cannot influence confidence or majority routing until a fixed-harness pilot passes.
- The M4/M6 preferred lens is retired. Pair equality is an observation only.
- A correction system is safer than relying on perfect first-pass chunking: typed provenance, semantic checks, overlap admission, calibrated roles, proposer plus independent critic, frontier review, owner gate, and route isolation.

## Decisions made

- Freeze T464-T471 evidence byte-for-byte and supersede routing only.
- Withdraw the former T472-A recommendation and block T473.
- Make future comparison rows distinguish disagreement regions from all model span observations.
- Fail closed on manifest/progress inconsistency.
- Give complete chapter envelopes no confidence credit without literary identity evidence.
- Send DAD a candidate-only corrective lesson with root causes, prevention assets, and explicit correction of the T465 preferred-pair lesson.

## Validation performed

- T472 builder check and corrective validator passed.
- T464/T465/T471 compatibility validators passed.
- Focused T464-T472 tests passed: 28 total; final regression subset 19 passed.
- DAD outbox, task scope, handoff, decision-register, lesson-index, DATA_MAP, and diff checks passed.
- Full pytest passed: 926 tests in 603.97 seconds.
- `validate_all.py` reached and passed every T472/control/data gate twice, then failed only three legacy output-pilot subprocesses (`T374`, `T401`, `T415`) because this sandbox denies child writes in newly created temp directories. Re-pinning `TEMP`/`TMP` reproduced the host ACL failure. GitHub CI remains the unsandboxed merge verdict.

## Risks introduced

- Historical T465/T471 artifacts still contain legacy routing. T472 freezes them for audit and marks the T472 correction overlay as effective.
- The future fixed-harness pilot may change model calibration, but cannot silently rehabilitate a run.
- No reviewed gold, chunk output, child spans, route/evaluator behavior, graph/retrieval/vector truth, preferred reading, source-tradition choice, canon change, or theology authority is authorized.

## Unresolved questions

- Which exact literary candidates should return after the four-scope calibration pilot?
- Should the general reviewed-gold/output overlap admission validator land in the pilot task or the next owner-docket task?

## Exact next action

Run focused and full gates, commit/push/merge the corrective T472 PR, then design the fixed-harness four-scope proposer/independent-critic pilot. Do not start T473 promotion.

---

## Handoff refresh: final

- agent_name: Codex
- mode: model_panel_calibration_and_provenance_correction_non_authorizing
- updated_at: 2026-07-10T05:05:46+00:00
- handoff_id: 230edea27ccf91c1
