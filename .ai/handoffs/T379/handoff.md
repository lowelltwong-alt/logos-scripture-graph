# Task Handoff

## Task

- task_id: T379
- title: Textual-Critical Case-By-Case Policy Selection
- phase: phase_4
- status: complete

## Agent

- agent_name: codex
- mode: build
- stage: final
- updated_at: 2026-06-19T02:20:00+00:00
- handoff_id: t379-final

## Files read

- `AI_FRONT_DOOR.md`
- `AI_TABLE_OF_CONTENTS.md`
- `ROADMAP_STATE.yaml`
- `.ai/control/current_focus.yaml`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/textual_critical_policy_owner_options.yaml`
- `.ai/control/textual_critical_policy_docket.yaml`
- `.ai/control/owner_decision_projection_policy.yaml`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/chunking_agent_preflight.yaml`
- `.ai/control/bible_chunking_readiness_map.yaml`
- `.ai/control/chunking_human_decision_forecast.yaml`
- `docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md`

## Files changed

- `.ai/control/textual_critical_case_policy.yaml`
- `.ai/control/textual_critical_policy_owner_options.yaml`
- `.ai/control/textual_critical_policy_docket.yaml`
- `.ai/control/owner_decision_projection_policy.yaml`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/chunking_agent_preflight.yaml`
- `.ai/control/bible_chunking_readiness_map.yaml`
- `.ai/control/chunking_human_decision_forecast.yaml`
- `.ai/control/current_focus.yaml`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/roadmap_events.jsonl`
- `.ai/control/handoff_ledger.jsonl`
- `.ai/tasks/T379.task.yaml`
- `.ai/handoffs/T379/handoff.md`
- `AI_FRONT_DOOR.md`
- `AI_TABLE_OF_CONTENTS.md`
- `ROADMAP_STATE.yaml`
- `docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md`
- `docs/roadmap/T379_TEXTUAL_CRITICAL_CASE_POLICY_SELECTION.md`
- `scripts/validate_textual_critical_case_policy.py`
- `scripts/validate_textual_critical_policy_owner_options.py`
- `scripts/validate_textual_critical_policy_docket.py`
- `scripts/validate_owner_decision_projection_policy.py`
- `scripts/validate_chunking_agent_preflight.py`
- `scripts/validate_bible_chunking_readiness_map.py`
- `scripts/validate_chunking_human_decision_forecast.py`
- `scripts/validate_1cor8_10_owner_review_docket.py`
- `scripts/validate_1cor8_10_parent_evidence_packet.py`
- `scripts/validate_owner_selection_implementation_gate.py`
- `scripts/validate_all.py`
- `tests/test_textual_critical_case_policy.py`
- `tests/test_textual_critical_policy_owner_options.py`
- `tests/test_textual_critical_policy_docket.py`
- `tests/test_owner_decision_projection_policy.py`
- `tests/test_chunking_agent_preflight.py`
- `tests/test_bible_chunking_readiness_map.py`
- `tests/test_chunking_human_decision_forecast.py`
- `tests/test_ai_roadmap_table_of_contents.py`

## Decisions made

- Recorded owner selection of `TCP-T378-B` as the case-by-case textual-critical process policy.
- Added `CD-045` to the chunking theological decision register.
- Added `ODP-005` so future agents may project the process rule while still stopping before preferred readings, variant dependency findings, reviewed-gold promotion, implementation, or output changes.
- Updated T371 to require exact owner review of variant dependency/non-dependency for `1Cor.9.20` and `1Cor.10.9` before parent-only reviewed-gold promotion.

## Validation run

- command: `python scripts/validate_textual_critical_case_policy.py`
- result: passed
- command: `python scripts/validate_textual_critical_policy_owner_options.py`
- result: passed
- command: `python scripts/validate_textual_critical_policy_docket.py`
- result: passed
- command: `python scripts/validate_owner_decision_projection_policy.py`
- result: passed
- command: `python scripts/validate_bible_chunking_readiness_map.py`
- result: passed
- command: `python scripts/validate_chunking_agent_preflight.py`
- result: passed
- command: `python scripts/validate_chunking_human_decision_forecast.py`
- result: passed
- command: `python scripts/validate_chunking_theological_decision_register.py`
- result: passed
- command: `python scripts/validate_task_scope.py --task-id T379`
- result: passed
- command: `python scripts/validate_all.py`
- result: passed
- command: `python -m pytest -q` by filename batches
- result: passed; `45 passed`, `58 passed`, `47 passed`, `78 passed`, `213 passed`
- command: `git diff --check`
- result: passed
- command: protected-surface diff check for raw/canonical/processed/derived/chunking/gold/runtime/vector surfaces
- result: passed with no touched protected output surfaces
- failures: none

## Known risks

- Future agents could mistake `TCP-T378-B` for preferred-reading authority. The selected policy, decision register, and validators deny that.
- Future agents could skip the exact T371 dependency/non-dependency owner question. The readiness map and case-policy validator require it.
- Future agents could project a specific promotion from `ODP-005`. The projection policy forbids that.

## Open questions

- T371 still requires owner confirmation: are the `1Cor.9.20` and `1Cor.10.9` variant notes non-dependent for the `1Cor.8.1-1Cor.10.33` parent-only boundary and reviewed-gold claim, and should parent-only promotion be authorized?

## Next agent instruction

Proceed to T371 only as an owner variant-dependency and reviewed-gold promotion decision.

Do not select preferred readings, source-tradition preference, child spans, route/evaluator behavior,
graph/retrieval truth, chunk output, implementation, boundary import, vectors, or output changes
from T379.
