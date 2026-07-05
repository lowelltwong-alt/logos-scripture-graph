# T437 Handoff

Task id: T437
Agent name: Codex
Mode: metadata policy hardening, non-authorizing

## Summary

T437 policy-covers OSHB `w@lemma` attributes as Strong lookup-hint metadata without treating them as local lemma rows, Strong's rows, lexical truth, preferred readings, or theology authority. It updates T431 canonical source-view policy fields and regenerates T436 no-text parity outputs as policy-covered.

## Files Read

- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/original_language_source_allowlist.yaml`
- `scripts/build_original_language_canonical_source_views.py`
- `scripts/validate_original_language_raw_sources.py`
- `scripts/build_t436_jonah_hebrew_metadata_pilot.py`
- `scripts/validate_t436_jonah_hebrew_metadata_pilot.py`
- `data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/files/Jonah.xml`

## Files Changed

- `.ai/control/t437_oshb_lemma_attribute_policy.yaml`
- `.ai/tasks/T437.task.yaml`
- `.ai/handoffs/T437/handoff.md`
- `.ai/context/agent_work/T437/dad_preflight.md`
- `.ai/control/original_language_source_allowlist.yaml`
- `.ai/control/original_language_evidence_substrate.yaml`
- `.ai/control/t436_jonah_hebrew_metadata_pilot.yaml`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/current_focus.yaml`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/DATA_MAP.md`
- `.ai/handoffs/T436/handoff.md`
- `data/raw/original_language/hebrew/openscriptures_oshb/source_manifest.yaml`
- `data/candidate/original_language_evidence/canonical_source_views/`
- `data/candidate/original_language_evidence/pilots/T436_jonah_hebrew_observation_parity/`
- `docs/roadmap/T436_JONAH_HEBREW_METADATA_PILOT.md`
- `docs/roadmap/T437_OSHB_LEMMA_ATTRIBUTE_POLICY.md`
- `scripts/build_original_language_canonical_source_views.py`
- `scripts/download_original_language_sources.py`
- `scripts/validate_original_language_raw_sources.py`
- `scripts/build_t436_jonah_hebrew_metadata_pilot.py`
- `scripts/validate_t436_jonah_hebrew_metadata_pilot.py`
- `scripts/validate_t437_oshb_lemma_attribute_policy.py`
- `scripts/validate_all.py`
- `tests/test_original_language_raw_sources.py`
- `tests/test_t436_jonah_hebrew_metadata_pilot.py`
- `tests/test_t437_oshb_lemma_attribute_policy.py`

## Decisions Made

- Keep `contains_source_provided_lemmas: false` for OSHB local lemma population.
- Add explicit OSHB policy fields for `w@lemma` as Strong lookup-hint metadata.
- Keep `contains_source_provided_strongs: false` because OSHB does not expose a `strong` attribute and T437 does not populate Strong's rows.
- Do not add Rust in T437; source-specific Rust parser contracts remain future work.

## Validation Performed

- `python scripts\build_original_language_canonical_source_views.py --check`
- `python scripts\validate_original_language_raw_sources.py`
- `python -m pytest tests\test_original_language_raw_sources.py -q`
- `python scripts\build_t436_jonah_hebrew_metadata_pilot.py --check`
- `python scripts\validate_t436_jonah_hebrew_metadata_pilot.py`
- `python -m pytest tests\test_t436_jonah_hebrew_metadata_pilot.py tests\test_t437_oshb_lemma_attribute_policy.py -q`
- `python scripts\validate_chunking_theological_decision_register.py --base-ref origin/codex/t436-jonah-hebrew-pilot`
- `python scripts\validate_t437_oshb_lemma_attribute_policy.py`
- `python scripts\generate_data_map.py --check`
- `python scripts\validate_task_scope.py --task-id T437 --base-ref origin/codex/t436-jonah-hebrew-pilot`
- `python scripts\agent\validate_handoffs.py`

## Risks Introduced

- Metadata semantics are now more nuanced; future agents must distinguish source attribute presence from local evidence-row authority.

## Unresolved Questions

- Whether a later T438/T435-B should add a Rust UXLC/OSHB no-text scanner or a Python-generated fixture first.

## Exact Next Action

Run full merge gates (`validate_all.py`, full pytest, `generate_data_map.py --check`, and `git diff --check`). If clean, commit and push the stacked T437 branch. After T437 review, owner should pick from the existing five-route goal menu in `docs/roadmap/T430_ORIGINAL_LANGUAGE_GOAL_OPTIONS.md`: alignment bridge, manuscript custody chain, variant/error transparency, early-creed lane, or integrated evidence workbench.

---

## Handoff refresh: final

- agent_name: codex
- mode: metadata_policy_hardening_non_authorizing
- updated_at: 2026-07-05T03:43:31+00:00
- handoff_id: 5126a17aee6f7cae
