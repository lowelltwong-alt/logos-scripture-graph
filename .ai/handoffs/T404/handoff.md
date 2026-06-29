---
object_type: agent_handoff
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-29 by Codex for T404."
reason_for_inclusion: "Record the Cursor low-risk chunking handoff contract, validations, and exact next action for future Cursor/Codex collaboration."
---

# T404 Handoff

## Task

T404 - Cursor Low-Risk Chunking Handoff.

## Agent

Codex.

## Mode

Build, control-plane only, non-output-changing.

## Files read

- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md` (read-only)
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/DATA_MAP.md`
- `.ai/control/RAW_SOURCE_INVENTORY.md`
- `HANDOFF_PROTOCOL.md`
- `docs/architecture/ARCHITECTURE.md`
- `docs/chunking/CHUNKING_DESIGN.md`
- `.ai/control/chunking_agent_preflight.yaml`
- `.ai/control/test_runtime_preflight.yaml`
- `.ai/control/whole_bible_low_complexity_chunking_candidate_queue.yaml`
- `.ai/control/chunking_lesson_index.yaml`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/bible_chunking_readiness_map.yaml`
- `docs/roadmap/T402_LOW_COMPLEXITY_CHUNKING_RUNWAY.md`
- Cursor documentation for project commands and Plan/Agent mode behavior.

## Files changed

- `.ai/control/cursor_low_risk_chunking_handoff.yaml`
- `.ai/control/low_risk_chunking_multi_pass_plan.yaml`
- `.cursor/commands/chunking-preflight.md`
- `.cursor/commands/low-risk-chunking-candidate.md`
- `.cursor/commands/codex-review-packet.md`
- `.cursor/rules/logos-scripture-low-risk-chunking.mdc`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/chunking_lesson_index.yaml`
- `.ai/control/chunking_agent_preflight.yaml`
- `.ai/control/bible_chunking_readiness_map.yaml`
- `.ai/control/current_focus.yaml`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/roadmap_events.jsonl`
- `.ai/control/handoff_ledger.jsonl`
- `AI_FRONT_DOOR.md`
- `AI_TABLE_OF_CONTENTS.md`
- `ROADMAP_STATE.yaml`
- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`
- `docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md`
- `docs/roadmap/T404_CURSOR_LOW_RISK_CHUNKING_HANDOFF.md`
- `docs/roadmap/T406_LOW_RISK_CHUNKING_MULTI_PASS_PLAN.md`
- `.ai/tasks/T404.task.yaml`
- `.ai/handoffs/T404/handoff.md`
- `scripts/validate_cursor_low_risk_chunking_handoff.py`
- `scripts/validate_chunking_agent_preflight.py`
- `scripts/validate_chunking_lesson_index.py`
- `scripts/validate_bible_chunking_readiness_map.py`
- `scripts/validate_all.py`
- `tests/test_cursor_low_risk_chunking_handoff.py`

## Decisions made

- Recorded `CD-078`: Cursor low-risk chunking delegation is compute prep only.
- Recorded `LSN-032`: Cursor low-risk chunking handoffs must be target-explicit and non-authorizing.
- Added Cursor project slash commands for preflight, candidate classification, and Codex review packet preparation.
- Defined low risk as one exact owner-or-Codex supplied T402 `ready_for_review_packet` candidate only.
- Recorded that low-risk research is complete at T402 all-66 triage depth only, not deep verse-by-verse exegesis.
- Reserved T406 as a future multi-pass low-risk review-prep phase, not implementation or output authority.
- Renumbered the future low-risk pass from T405 to T406 after `origin/main` advanced with `2675033`
  using T405 for the governance map child mirror.
- Methodology updated: yes - added the Cursor low-risk delegation rule to the Chunking Skill Supply Chain.

## Validation run

- `python scripts/validate_cursor_low_risk_chunking_handoff.py` - passed.
- `python -m pytest tests/test_cursor_low_risk_chunking_handoff.py -q` - 6 passed.
- `python scripts/validate_chunking_agent_preflight.py` - passed.
- `python scripts/validate_chunking_lesson_index.py` - passed.
- `python scripts/validate_bible_chunking_readiness_map.py` - passed.
- `python scripts/validate_chunking_theological_decision_register.py` - passed.
- `python scripts/validate_task_scope.py --task-id T404` - passed.
- `python scripts/agent/validate_handoffs.py` - passed for 110 referenced handoff paths.
- `python -m pytest tests/test_chunking_agent_preflight.py tests/test_chunking_lesson_index.py tests/test_bible_chunking_readiness_map.py tests/test_cursor_low_risk_chunking_handoff.py -q` - 31 passed.
- `python scripts/validate_all.py` - passed after the post-fetch T406 rename.
- `python -m pytest -q` - 634 passed after the post-fetch T406 rename.
- `python scripts/generate_data_map.py --check` - passed; `DATA_MAP.md` is current.
- `git diff --check` - passed.
- `rg -n "T405|t405|405_LOW" ...` - no remaining low-risk T405 references.

## Known risks

- Cursor can be useful for compute-heavy review prep, but only if it cannot select its own target or write output surfaces.
- Apparent low complexity can still hide source-metadata, WJ/speaker, variant/source-tradition, original-language, or theological risk.
- The project commands help Cursor work efficiently but are guardrails, not authority.

## Open questions

- Lowell or Codex still must supply one exact candidate before Cursor can do candidate-specific prep.
- Codex should review Cursor's output before any merge or owner-facing promotion step.
- T406 is planned for a future batch of up to three supplied low-risk candidates after Codex review of T404-era rules.

## Next agent instruction

Use `/chunking-preflight` in Cursor Plan mode, then run `/low-risk-chunking-candidate` only for an
exact owner-or-Codex supplied T402 `ready_for_review_packet` target. Stop if Cursor would need to
choose the target or if any stop condition in `.ai/control/cursor_low_risk_chunking_handoff.yaml`
applies. After Cursor finishes, run `/codex-review-packet` and ask Codex to review the diff before
merge.
