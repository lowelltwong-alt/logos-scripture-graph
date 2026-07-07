## Task

T431 Original-Language Raw Intake And Strong's Overlay Guardrails

## Agent

Codex

## Files read

- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/original_language_phrase_context_policy.yaml`
- `.ai/control/manuscript_source_catalog_metadata_plan.yaml`
- `.ai/control/textual_variant_source_tradition_dossier_queue.yaml`
- `scripts/scan_raw_sources.py`
- `scripts/validate_raw_coverage.py`

## Files changed

- `.ai/control/original_language_source_allowlist.yaml`
- `.ai/control/original_language_evidence_substrate.yaml`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/chunking_lesson_index.yaml`
- `.ai/control/DATA_MAP.md`
- `.ai/control/RAW_SOURCE_INVENTORY.md`
- `.ai/context/agent_work/T431/dad_preflight.md`
- `.ai/tasks/T431.task.yaml`
- `.ai/handoffs/T431/handoff.md`
- `data/raw/original_language/` source archives and manifests
- `data/candidate/original_language_evidence/canonical_source_views/`
- `docs/roadmap/T430_ORIGINAL_LANGUAGE_GOAL_OPTIONS.md`
- `docs/roadmap/T431_ORIGINAL_LANGUAGE_RAW_INTAKE.md`
- `scripts/download_original_language_sources.py`
- `scripts/build_original_language_canonical_source_views.py`
- `scripts/validate_original_language_raw_sources.py`
- `scripts/validate_t430_original_language_evidence_substrate.py`
- `scripts/validate_all.py`
- `tests/test_original_language_raw_sources.py`
- `tests/test_t430_original_language_evidence_substrate.py`

## Decisions made

- T431 downloads only allowlisted, license-approved raw source packages.
- Raw files are immutable source packages; Strong's alignment belongs in future candidate evidence overlays outside raw.
- Manuscript libraries remain catalog-only until bulk text/image reuse is explicitly cleared.
- DAD preflight is recorded as candidate-only because `.digital-asset/` is not present on `origin/main`.
- Downloaded raw source packages: Tanach.us UXLC, Open Scriptures Hebrew Bible, SBLGNT, unfoldingWord UGNT, and CNTR Statistical Restoration.
- Catalog-only manuscript libraries: Leon Levy DSS, Codex Sinaiticus, Aleppo Codex, and NT papyri/major codices.
- Built canonical-only candidate source views: UXLC 39 included / 11 excluded, OSHB 39 / 87, SBLGNT 27 / 87, UGNT 27 / 96, CNTR-SR 1 / 7.
- Future source-language processing must consume the canonical source view, not raw archives directly, because the raw packages include docs, code, PDFs, HTML/JSON app renderings, images, metadata, nested archives, duplicate text formats, and non-selected variants.
- The first read-only subagent review found no P0/P1 issues and two P2s. Both were patched in T431:
  - CNTR-SR now truthfully records source-provided morphology and lemma columns as evidence-only metadata.
  - Canonical source view check mode now validates inclusion/exclusion ledgers against the actual archive member set, rejects duplicate archive paths, enforces included row count equals expected canonical scope, and checks unique included `book_id`/`view_path`.
- A second read-only subagent review found one P1 proof gap and one P2 raw-tree hardening gap. Both were patched in T431:
  - canonical source view check mode now compares each included view file and ledger row back to the selected ZIP member bytes, sha256, and byte size;
  - the raw original-language tree is now shape-locked to `source_manifest.yaml`, `raw/<declared archive>`, and `witness_catalogs/manuscript_libraries.yaml`, so overlay-like files cannot evade by avoiding magic filenames.
- Rust was intentionally not added to this T431 slice after review, because the remaining risk was semantic source filtering rather than raw throughput. T435 remains the right lane for Rust-first large token/alignment ledgers after schemas settle.
- Added five T430 goal options: alignment bridge, manuscript witness chain, variant/copying-error ledger, early creed/tradition-formula research lane, and integrated evidence workbench. The manuscript lane now separates oldest-known witnesses from highest-confidence witnesses and preserves minute copying/editorial issues as transparent evidence rather than authority.
- Strengthened the T430 goal options into an owner-facing decision menu and added structured `goal_options` control-plane entries. `scripts/validate_t430_original_language_evidence_substrate.py` now fails unless all five options remain present with non-authorizing authority limits.
- Added `CD-088` and `LSN-043` after GitHub CI correctly caught that roadmap/source-intake docs under `docs/roadmap/` require a chunking theological decision-register update. These entries record T431 as evidence-only and non-authorizing.
- DAD candidate lesson/outbox records were sent from the central DAD checkout:
  - `dad:rust-rollout-lesson:829dc53e-1688-5290-ab33-3352634c010d`
  - `dad:mail:829dc53e-1688-5290-ab33-3352634c010d`
  - `dad:mail:019ab2a2-09ae-51e1-b77f-d55e6712b292`
  - `dad:rust-rollout-lesson:0e46712a-0c4f-5ac2-89d4-0f2f4d431f66`
  - `dad:mail:0e46712a-0c4f-5ac2-89d4-0f2f4d431f66`

## Validation run

- `python scripts/download_original_language_sources.py --check` - passed.
- `python scripts/build_original_language_canonical_source_views.py --check` - passed.
- `python scripts/validate_original_language_raw_sources.py` - passed.
- `python scripts/validate_t430_original_language_evidence_substrate.py` - passed.
- `python -m pytest tests/test_t430_original_language_evidence_substrate.py -q` - 5 passed after adding goal-option validator coverage.
- `python scripts/validate_chunking_theological_decision_register.py --base-ref origin/main` - passed after CI remediation.
- `python scripts/validate_chunking_lesson_index.py --base-ref origin/main` - passed after CI remediation.
- `python scripts/scan_raw_sources.py --check` - passed after regenerating `.ai/control/RAW_SOURCE_INVENTORY.md`.
- `python scripts/validate_raw_coverage.py` - passed.
- `python -m pytest tests/test_original_language_raw_sources.py -q` - 10 passed after archive-member and raw-tree hardening.
- `python -m pytest tests/test_original_language_raw_sources.py tests/test_t430_original_language_evidence_substrate.py -q` - 13 passed after the second hardening pass.
- `python scripts/validate_task_scope.py --task-id T431` - passed.
- `python scripts/agent/validate_handoffs.py` - passed.
- `git diff --check` - passed.
- `python pipelines/ingest/usfm_importer.py` without `--canonical-66-filter` was tried only to populate ignored generated files and failed downstream validation by importing apocrypha/deuterocanonical books into generated canonical outputs. That confirmed a real preflight lesson: canonical regeneration for merge gates must use `--canonical-66-filter`.
- `python pipelines/ingest/usfm_importer.py --canonical-66-filter` - passed.
- `python scripts/validate_all.py` - passed after the canonical-66 filtered generated-data refresh.
- `python -m pytest -q` - 728 passed.
- `python scripts/generate_data_map.py --check` - passed after data map regeneration.
- GitHub PR #134 `validate` - passed after CI remediation at `1d2750a`; rerun after second hardening push.

## Known risks

- Original-language source archives include extra docs, code, PDFs, HTML/JSON app renderings, images, metadata, nested archives, duplicate text formats, and non-selected variants; use canonical source views only for future processing.
- Some canonical source views retain source-provided metadata columns such as morphology, lemmas, or Strong's IDs. These are evidence-only and are explicitly flagged in manifests and included-file ledgers.
- GitHub CI uses `--base-ref origin/main` semantics for watched-path gates; local final validation must include the base-ref variants when T431 touches `docs/roadmap/`.
- Public-viewable manuscript libraries are not necessarily reusable as bulk raw data.
- The committed raw archives are about 56 MB total; future larger sources may need Git LFS or external storage.

## Open questions

- Which goal option becomes the next active lane remains a later owner-gated decision. Recommended default is the Greek/Hebrew-to-English alignment bridge pilot.
- Which source edition becomes the first tiny T433 pilot remains a later owner-gated decision.

## Next agent instruction

After T431 validates, choose a T430 goal option. Recommended default: start T432 schema hardening for source-language tokens, editorial layers, variants, and candidate Strong's alignment records, then T433 pilot a tiny Philemon or Jonah alignment bridge. Do not build overlays, choose preferred readings, create source-language witness rows, import manuscript transcriptions/images, or authorize KG/chunk outputs in T431.
