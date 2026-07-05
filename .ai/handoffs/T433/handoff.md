## Task

T433 Philemon Original-Language Alignment Bridge Pilot

## Agent

Codex

## Mode

Candidate evidence pilot, non-authorizing.

## Files read

- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/current_focus.yaml`
- `.ai/control/original_language_evidence_substrate.yaml`
- `.ai/control/original_language_schema_contracts.yaml`
- `.ai/tasks/T431.task.yaml`
- `.ai/handoffs/T431/handoff.md`
- `.ai/tasks/T432.task.yaml`
- `.ai/handoffs/T432/handoff.md`
- `schemas/source_language_token.schema.json`
- `schemas/alignment_record.schema.json`
- `schemas/editorial_layer.schema.json`
- `data/candidate/original_language_evidence/canonical_source_views/sblgnt/canonical_source_view_manifest.yaml`
- `data/candidate/original_language_evidence/canonical_source_views/sblgnt/included_files.jsonl`
- `data/candidate/original_language_evidence/canonical_source_views/sblgnt/files/Phlm.xml`
- `data/candidate/original_language_evidence/canonical_source_views/ugnt/canonical_source_view_manifest.yaml`
- `data/candidate/original_language_evidence/canonical_source_views/ugnt/files/Phlm.SFM`
- `data/canonical/translations/eng-web/word_tokens.jsonl`

## Files changed

- `.ai/tasks/T433.task.yaml`
- `.ai/handoffs/T433/handoff.md`
- `.ai/context/agent_work/T433/dad_preflight.md`
- `.ai/control/t433_phlm_original_language_evidence_pilot.yaml`
- `.ai/control/original_language_evidence_substrate.yaml`
- `.ai/control/current_focus.yaml`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/DATA_MAP.md`
- `data/candidate/original_language_evidence/pilots/T433_phlm_alignment_bridge/`
- `docs/roadmap/T433_PHLM_ORIGINAL_LANGUAGE_EVIDENCE_PILOT.md`
- `scripts/build_t433_phlm_alignment_pilot.py`
- `scripts/validate_t433_phlm_alignment_pilot.py`
- `scripts/validate_all.py`
- `tests/test_t433_phlm_alignment_pilot.py`

## Decisions made

- T433 uses SBLGNT first for a tiny `Phlm.1.1-Phlm.1.3` pilot because the selected source view has explicit XML `<w>` tokens and no source-provided Strong's or morphology metadata to over-trust.
- UGNT remains deferred context because the selected `Phlm.SFM` source view does not expose per-token Strong's or morphology fields.
- Pilot rows stay under `data/candidate/original_language_evidence/pilots/T433_phlm_alignment_bridge/`, not the T432 production roots.
- WEB Strong's IDs are recorded only as translation-side alignment hints, not source-token fields or lexical/theology authority.
- Editorial-layer rows record paragraphing, versification, punctuation, and source-edition sigla as editorial evidence only.
- Rust is deferred to T435 because T433 is a small semantic/schema proof rather than a high-volume scanner.
- DAD candidate lesson: manifest-level metadata must be verified at the selected canonical source-view file/span before populating evidence rows.

## Validation run

- `python scripts/build_t433_phlm_alignment_pilot.py` - passed.
- `python scripts/build_t433_phlm_alignment_pilot.py --check` - passed.
- `python scripts/validate_t433_phlm_alignment_pilot.py` - passed.
- `python -m pytest tests/test_t433_phlm_alignment_pilot.py -q` - 5 passed.
- `python scripts/validate_t432_original_language_schema_contracts.py` - passed.
- `python scripts/validate_task_scope.py --task-id T433 --base-ref origin/codex/t432-original-language-schema-contracts` - passed.
- `python scripts/validate_chunking_theological_decision_register.py --base-ref origin/codex/t432-original-language-schema-contracts` - passed.
- `python scripts/agent/validate_handoffs.py` - passed.
- `python scripts/validate_t430_original_language_evidence_substrate.py` - passed.
- `python scripts/generate_data_map.py` - regenerated `.ai/control/DATA_MAP.md`.
- `python scripts/generate_data_map.py --check` - passed.
- `python scripts/validate_all.py` - passed after adding the `pilots/` task-scope container for live dirty-tree safety.
- `python -m pytest -q` - 743 passed in 576.26s.
- `git diff --check` - passed with the existing DATA_MAP CRLF normalization warning.
- DAD lesson JSONL validation - passed for `dad:rust-rollout-lesson:37f4f8df-41dc-57f5-a7af-1c2b7bf1431c`.

## Known risks

- The pilot records verse-level many-to-many alignment only; it is not word-level alignment truth.
- SBLGNT and UGNT may differ in editorial punctuation or sigla; T433 does not compare them or select a source tradition.
- WEB Strong's sidecar metadata can be useful but must remain a translation-side hint.

## Open questions

- Whether T435 should proceed directly to a Rust scanner after T433, or whether a Jonah Hebrew pilot should run first.
- Whether UGNT metadata-rich package surfaces should get a separate parser after span-local metadata availability is proven.

## Next agent instruction

Run the T433 builder, validator, focused tests, task-scope gate, decision-register gate, handoff validation, `validate_all.py`, full pytest, data-map check, and `git diff --check`. Do not create production source-token roots, preferred readings, translation judgments, KG/retrieval truth, chunks, reviewed gold, or theology authority.
