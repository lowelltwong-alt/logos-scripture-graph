## Task

T432 Original-Language Schema Contracts

## Agent

Codex

## Mode

Schema/control-plane, non-authorizing.

## Files read

- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/original_language_evidence_substrate.yaml`
- `docs/roadmap/T430_ORIGINAL_LANGUAGE_GOAL_OPTIONS.md`
- `.ai/tasks/T431.task.yaml`
- `.ai/handoffs/T431/handoff.md`
- `schemas/word_token.schema.json`
- `schemas/lexeme.schema.json`
- `schemas/alignment_record.schema.json`
- `schemas/textual_variant.schema.json`
- `schemas/witness.schema.json`
- DAD `lessons/rust_rollout/lesson_ledger.jsonl`

## Files changed

- `.ai/tasks/T432.task.yaml`
- `.ai/handoffs/T432/handoff.md`
- `.ai/context/agent_work/T432/dad_preflight.md`
- `.ai/control/original_language_schema_contracts.yaml`
- `.ai/control/original_language_evidence_substrate.yaml`
- `.ai/control/current_focus.yaml`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/DATA_MAP.md`
- `docs/roadmap/T432_ORIGINAL_LANGUAGE_SCHEMA_CONTRACTS.md`
- `schemas/source_language_token.schema.json`
- `schemas/editorial_layer.schema.json`
- `schemas/lexeme.schema.json`
- `schemas/alignment_record.schema.json`
- `schemas/textual_variant.schema.json`
- `schemas/witness.schema.json`
- `scripts/validate_t432_original_language_schema_contracts.py`
- `scripts/validate_schemas.py`
- `scripts/validate_all.py`
- `tests/test_t432_original_language_schema_contracts.py`

## Decisions made

- T432 stays Python/control-plane because it defines semantic schema and authority contracts.
- Rust is deferred to T435 for high-volume deterministic source-token, alignment, variant, and witness ledgers after schemas stabilize.
- Future original-language evidence rows must carry provenance, confidence/rights context, explicit non-authorizations, and authority-denial fields.
- `validate_all.py` now honors `GITHUB_BASE_REF` for changed-path detection so stacked task branches can validate against their actual PR base.
- DAD preflight found no need to emit a new DAD lesson; T432 applies existing DAD guidance to define schema contracts before Rust scanner implementation.

## Validation performed

- `python scripts/validate_t432_original_language_schema_contracts.py` - passed.
- `python -m pytest tests/test_t432_original_language_schema_contracts.py -q` - 6 passed.
- `python scripts/validate_t430_original_language_evidence_substrate.py` - passed.
- `python scripts/validate_task_scope.py --task-id T432 --base-ref origin/codex/t431-original-language-intake` - passed.
- `python scripts/validate_chunking_theological_decision_register.py --base-ref origin/codex/t431-original-language-intake` - passed.
- `python scripts/agent/validate_handoffs.py` - passed.
- `python pipelines/ingest/usfm_importer.py --canonical-66-filter` - passed; generated ignored canonical/processed outputs for data-map parity only.
- `python scripts/generate_data_map.py --check` - passed after regenerating `.ai/control/DATA_MAP.md`.
- `python scripts/validate_all.py` - passed with no env override.
- `$env:GITHUB_BASE_REF='codex/t431-original-language-intake'; python scripts/validate_all.py` - passed.
- `python -m pytest -q` - 738 passed.
- `git diff --check` - passed with a CRLF normalization warning for `.ai/control/DATA_MAP.md`.

## Risks introduced

- Schema changes may affect future candidate data; no current original-language evidence rows are populated.
- T432 intentionally leaves Rust for T435 rather than adding a premature scanner before row shapes are piloted.
- T432 must not populate evidence rows or authorize source-language truth.

## Unresolved questions

- Which T433 pilot should run first remains owner-gated: Philemon for Greek or Jonah for Hebrew.

## Exact next action

Run full merge gates, then prepare a stacked PR against T431 if clean. Do not populate original-language evidence rows or promote any authority surface.
