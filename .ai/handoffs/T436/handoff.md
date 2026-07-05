# T436 Handoff

Task id: T436
Agent name: Codex
Mode: no-text observation parity pilot, non-authorizing

## Summary

T436 adds a full-Jonah Hebrew no-text observation/parity pilot. The pilot proves Hebrew source-view shape, token-count parity, editorial/metadata flags, and OSHB lemma-attribute flag drift before any Rust scanner expansion to UXLC or OSHB.

## Files Read

- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/original_language_evidence_substrate.yaml`
- `.ai/control/original_language_observation_scanner.yaml`
- `.ai/control/t433_phlm_original_language_evidence_pilot.yaml`
- `schemas/source_language_token.schema.json`
- `schemas/editorial_layer.schema.json`
- `schemas/alignment_record.schema.json`
- `data/raw/original_language/hebrew/tanach_us_uxlc/source_manifest.yaml`
- `data/raw/original_language/hebrew/openscriptures_oshb/source_manifest.yaml`
- `data/candidate/original_language_evidence/canonical_source_views/tanach_us_uxlc/included_files.jsonl`
- `data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/included_files.jsonl`
- `data/candidate/original_language_evidence/canonical_source_views/tanach_us_uxlc/files/Jonah.xml`
- `data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/files/Jonah.xml`

## Files Changed

- `.ai/tasks/T436.task.yaml`
- `.ai/control/t436_jonah_hebrew_metadata_pilot.yaml`
- `.ai/control/original_language_evidence_substrate.yaml`
- `.ai/control/current_focus.yaml`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/context/agent_work/T436/dad_preflight.md`
- `.ai/handoffs/T436/handoff.md`
- `docs/roadmap/T436_JONAH_HEBREW_METADATA_PILOT.md`
- `scripts/build_t436_jonah_hebrew_metadata_pilot.py`
- `scripts/validate_t436_jonah_hebrew_metadata_pilot.py`
- `scripts/validate_all.py`
- `tests/test_t436_jonah_hebrew_metadata_pilot.py`
- `data/candidate/original_language_evidence/pilots/T436_jonah_hebrew_observation_parity/`

## Decisions Made

- Use UXLC Jonah XML as the clean source-token baseline.
- Use OSHB Jonah XML as metadata context and parity canary.
- Store hashes/counts/flags only; no Hebrew wording, morphology values, or lemma values in T436 ledgers.
- Record OSHB `lemma` attributes as manifest/source-view flag drift.
- Block Rust expansion until OSHB lemma-attribute drift is fixed or policy-covered.
- Do not add Rust in T436; Rust expansion should follow after the Hebrew row semantics are reviewed.

## Validation Performed

- `python scripts/build_t436_jonah_hebrew_metadata_pilot.py --check` passed.
- `python scripts/validate_t436_jonah_hebrew_metadata_pilot.py` passed.
- `python -m pytest tests/test_t436_jonah_hebrew_metadata_pilot.py -q` passed, 6 tests.
- `python scripts/validate_t430_original_language_evidence_substrate.py` passed.
- `python scripts/validate_t432_original_language_schema_contracts.py` passed.
- `python scripts/validate_t435_original_language_observation_scanner.py` passed.
- `python scripts/validate_chunking_theological_decision_register.py --base-ref origin/codex/t435-original-language-observation` passed.
- `python scripts/validate_task_scope.py --task-id T436 --base-ref origin/codex/t435-original-language-observation` passed.
- `python scripts/agent/validate_handoffs.py` passed before the final forced handoff refresh.

## Risks Introduced

- UXLC and OSHB token counts are expected to match for Jonah, but exact token hashes can differ because source formatting/token text can differ.
- OSHB lemma-attribute drift is now explicit audit debt before Rust expansion.

## Unresolved Questions

- Whether T431 canonical source-view metadata should be corrected to flag OSHB lemma attributes as source-provided metadata.
- Whether T437 should extend the Rust observation scanner to UXLC/OSHB no-text ledgers or add a separate Hebrew scanner.

## Exact Next Action

Run the T436 builder, validator, tests, task-scope validator, handoff validator, and merge gates. If all pass, commit/push the stacked T436 branch.

---

## Handoff refresh: final

- agent_name: codex
- mode: 
- updated_at: 2026-07-05T02:41:18+00:00
- handoff_id: 7f69110ae42d5b75
