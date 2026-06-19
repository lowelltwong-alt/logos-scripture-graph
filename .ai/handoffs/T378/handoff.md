# Task Handoff

## Task

- task_id: T378
- title: Textual-Critical Policy Owner Options
- phase: phase_4
- status: complete

## Agent

- agent_name: codex
- mode: build
- stage: final
- updated_at: 2026-06-19T01:35:00+00:00
- handoff_id: t378-final

## Files read

- `AI_FRONT_DOOR.md`
- `AI_TABLE_OF_CONTENTS.md`
- `ROADMAP_STATE.yaml`
- `.ai/control/current_focus.yaml`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/textual_critical_policy_docket.yaml`
- `.ai/control/chunking_human_decision_forecast.yaml`
- `.ai/control/chunking_agent_preflight.yaml`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/bible_chunking_readiness_map.yaml`
- `eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml`
- `eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md`
- `docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md`
- `scripts/validate_textual_critical_policy_docket.py`
- `tests/test_textual_critical_policy_docket.py`

## Files changed

- `.ai/control/textual_critical_policy_owner_options.yaml`
- `.ai/control/textual_critical_policy_docket.yaml`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/chunking_agent_preflight.yaml`
- `.ai/control/bible_chunking_readiness_map.yaml`
- `.ai/control/current_focus.yaml`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/roadmap_events.jsonl`
- `.ai/control/handoff_ledger.jsonl`
- `.ai/tasks/T378.task.yaml`
- `.ai/handoffs/T378/handoff.md`
- `AI_FRONT_DOOR.md`
- `AI_TABLE_OF_CONTENTS.md`
- `ROADMAP_STATE.yaml`
- `docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md`
- `docs/roadmap/T378_TEXTUAL_CRITICAL_POLICY_OWNER_OPTIONS.md`
- `scripts/validate_textual_critical_policy_owner_options.py`
- `scripts/validate_textual_critical_policy_docket.py`
- `scripts/validate_chunking_agent_preflight.py`
- `scripts/validate_bible_chunking_readiness_map.py`
- `scripts/validate_all.py`
- `tests/test_textual_critical_policy_owner_options.py`
- `tests/test_textual_critical_policy_docket.py`
- `tests/test_chunking_agent_preflight.py`
- `tests/test_bible_chunking_readiness_map.py`
- `tests/test_ai_roadmap_table_of_contents.py`

## Decisions made

- Added `.ai/control/textual_critical_policy_owner_options.yaml` as a non-authorizing owner options docket.
- Recorded `CD-044`: textual-critical policy options block variant-sensitive reviewed-gold promotion.
- Recommended `TCP-T378-B`, case-by-case owner policy before each variant-sensitive promotion, without selecting it.
- Recorded that T371 remains blocked until owner textual-critical policy selection or explicit hold.

## Validation run

- command: `python scripts/validate_textual_critical_policy_owner_options.py`
- result: passed
- command: `python scripts/validate_all.py`
- result: passed
- command: `python -m pytest -q`
- result: local one-shot run exceeded the 10-minute tool timeout before output; rerun by filename batches and all test files passed
- batch result: `44 passed`; `58 passed`; `47 passed`; `77 passed`; `207 passed`
- command: `git diff --check`
- result: passed
- command: protected-surface diff check for raw/canonical/processed/derived/chunking/gold/runtime/vector surfaces
- result: passed with no touched protected output surfaces
- failures: none

## Known risks

- Future agents could mistake the recommended case-by-case policy for a selected policy. The docket and validator keep `textual_critical_policy_selected: false`.
- Future agents could promote T371 reviewed gold without resolving `1Cor.9.20` and `1Cor.10.9` policy. The readiness map and CD-044 record the block.
- Future agents could treat a current source, critical text, majority text, or Textus Receptus default as hidden policy. T378 explicitly denies all such defaults.

## Open questions

- Lowell must select a textual-critical policy option before T371 promotion can proceed.
- If `TCP-T378-B` is selected, Lowell must still decide whether the `1Cor.8.1-1Cor.10.33` parent-only boundary is variant-non-dependent and can be promoted as reviewed gold.

## Next agent instruction

Ask Lowell to choose a textual-critical policy option. Recommended: `TCP-T378-B`, case-by-case
owner policy before each variant-sensitive promotion.

Do not promote T371 reviewed gold, choose a preferred reading, select source-tradition preference,
generate graph/retrieval/vector output, authorize route/evaluator behavior, or change output from
T378 alone.
