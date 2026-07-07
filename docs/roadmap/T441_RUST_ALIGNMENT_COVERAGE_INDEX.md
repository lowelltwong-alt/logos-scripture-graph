# T441 Rust Alignment Coverage Index

T441 adds a Rust no-text coverage ledger over the T439 Philemon bridge and the T436/T440 Jonah parser-contract fixtures.

This is a coverage ledger, not a retrieval index, vector index, graph index, or authority surface. It records refs, IDs, counts, hashes, source-view checksums, and semantic guardrail labels so later agents can see coverage without rereading source files or inferring meaning from field names.

## Inputs

- T439 full-Philemon no-text candidate pilot.
- T436 Jonah no-text Hebrew observation parity pilot.
- T440 Jonah source-specific parser contract.

T441 consumes candidate fixtures and canonical source-view lineage only. It does not consume raw archives directly.

## Outputs

Generated, ignored outputs live under `build/original_language_observation/T441/alignment_coverage/`:

- `coverage_manifest.json`
- `source_ref_coverage.jsonl`
- `alignment_coverage_index.jsonl`
- `semantic_guardrail_index.jsonl`
- `negative_fixture_summary.json`

Committed files are only the Rust binary, Python validator/tests, task/control/handoff, and roadmap surfaces.

## Guardrails

- No visible Greek, Hebrew, or English biblical text.
- No production source-token, Strong's, lemma, morphology, variant, witness, or editorial roots.
- No source-language truth, lexical truth, word-level alignment truth, translation-faithfulness judgment, preferred reading, source-tradition preference, KG/retrieval truth, chunk boundary, reviewed gold, chunk output, or theology authority.
- T439 Philemon bridge rows remain low-confidence, many-to-many, verse-level, and unreviewed.
- Count parity is not semantic authority.
- OSHB `w@lemma` remains Strong lookup-hint metadata only.
- OSHB `w@morph` remains source morphology metadata only.

## Rust Fit

Rust is a good fit here because the slice is deterministic JSONL/YAML scanning, counting, grouping, no-text enforcement, and JSONL emission over stable fixtures. Python remains the authority validator and orchestration layer. `validate_all.py` runs the fast contract validator only; generated-mode validation is used when scanner inputs or code change.

## Validation

```bash
cargo test --manifest-path tools/original_language_observation_scanner/Cargo.toml --bins
cargo run --manifest-path tools/original_language_observation_scanner/Cargo.toml --bin t441_alignment_coverage -- --t439-root data/candidate/original_language_evidence/pilots/T439_phlm_alignment_bridge_expansion --t436-root data/candidate/original_language_evidence/pilots/T436_jonah_hebrew_observation_parity --t440-control .ai/control/t440_jonah_hebrew_parser_contract.yaml --out build/original_language_observation/T441/alignment_coverage --no-authority --no-text
python scripts/validate_t441_rust_alignment_coverage_index.py --input build/original_language_observation/T441/alignment_coverage
python -m pytest tests/test_t441_rust_alignment_coverage_index.py -q
```
