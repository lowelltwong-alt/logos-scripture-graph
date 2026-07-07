# T440 Handoff

Task id: T440
Agent name: Codex
Mode: source-specific parser contract, non-authorizing

## Summary

T440 defines source-specific UXLC and OSHB parser semantics for Jonah before any Hebrew Rust expansion. It records expected XML shape, counts, metadata meanings, negative fixture requirements, and the boundary between T440 contract work and future T441 Rust no-text checker work.

## Files Read

- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/t436_jonah_hebrew_metadata_pilot.yaml`
- `.ai/control/t437_oshb_lemma_attribute_policy.yaml`
- `docs/roadmap/T438_ALIGNMENT_BRIDGE_GOAL.md`
- `scripts/build_t436_jonah_hebrew_metadata_pilot.py`
- `scripts/validate_t436_jonah_hebrew_metadata_pilot.py`
- `scripts/validate_t437_oshb_lemma_attribute_policy.py`
- `data/candidate/original_language_evidence/canonical_source_views/tanach_us_uxlc/canonical_source_view_manifest.yaml`
- `data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/canonical_source_view_manifest.yaml`
- `data/candidate/original_language_evidence/pilots/T436_jonah_hebrew_observation_parity/manifest.yaml`
- `data/candidate/original_language_evidence/pilots/T436_jonah_hebrew_observation_parity/parity_summary.json`

## Files Changed

- `.ai/control/t440_jonah_hebrew_parser_contract.yaml`
- `.ai/tasks/T440.task.yaml`
- `.ai/handoffs/T440/handoff.md`
- `.ai/context/agent_work/T440/dad_preflight.md`
- `.ai/control/original_language_evidence_substrate.yaml`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/current_focus.yaml`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/DATA_MAP.md`
- `docs/roadmap/T440_JONAH_HEBREW_PARSER_CONTRACT.md`
- `scripts/validate_t440_jonah_hebrew_parser_contract.py`
- `scripts/validate_all.py`
- `tests/test_t440_jonah_hebrew_parser_contract.py`

## Decisions Made

- Keep T440 as a parser-contract gate, not a data-population task.
- Treat UXLC as the clean no-lemma/no-morph/no-Strong Jonah baseline.
- Treat OSHB `w@lemma` as Strong lookup-hint metadata and OSHB `w@morph` as source morphology metadata, not local lemma, Strong, morphology, lexical, translation, or theology authority.
- Defer Rust implementation to T441, where Rust may only implement no-text deterministic scanner/checker slices against T440.

## Validation Performed

- `python scripts\validate_t440_jonah_hebrew_parser_contract.py`
- `python -m pytest tests\test_t440_jonah_hebrew_parser_contract.py -q`
- `python scripts\validate_t430_original_language_evidence_substrate.py`
- `python scripts\validate_t438_alignment_bridge_goal.py`
- `python scripts\validate_t439_phlm_alignment_bridge_expansion.py`
- `python scripts\validate_chunking_theological_decision_register.py --base-ref origin/codex/t439-phlm-alignment-bridge`

## Risks Introduced

- Future agents could overread `authorizes_t441_design` as authorization to run Rust in T440; validators require T441 to be a separate task and PR.

## Unresolved Questions

- Whether T441 should cover both T439 Greek and T440 Hebrew in one Rust scanner/index or split Hebrew and Greek parity into separate commands.

## Exact Next Action

Run the T440 validator, focused tests, task-scope validation, handoff validation, full merge gates, then commit and push if clean.

---

## Handoff refresh: final

- agent_name: codex
- mode: source_specific_parser_contract_non_authorizing
- updated_at: 2026-07-05T05:02:19+00:00
- handoff_id: dab2a732dfc32d55
