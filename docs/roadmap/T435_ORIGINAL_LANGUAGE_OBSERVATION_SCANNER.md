# T435 SBLGNT Original-Language Observation Scanner

Status: implementation.
Mode: Rust no-text observation scanner, non-authorizing.

## Purpose

T435-A moves the original-language program from a tiny Python pilot to a deterministic Rust observation substrate for the SBLGNT canonical source view.

The scanner observes file, verse, token-shape, and editorial-shape counts across the 27 SBLGNT New Testament XML files. It does not emit source wording, populate production candidate roots, create alignment truth, choose preferred readings, judge translation faithfulness, or make theology claims.

## Scope

Input:

```text
data/candidate/original_language_evidence/canonical_source_views/sblgnt/
```

Generated output:

```text
build/original_language_observation/T435-A/sblgnt/
```

Output files:

- `scan_manifest.json`
- `source_view_file_observations.jsonl`
- `verse_token_observations.jsonl`
- `source_token_shape_index.jsonl`
- `editorial_layer_shape_index.jsonl`
- `t433_shadow_parity.json`

## No-Text Contract

Rows store counts, refs, source-view paths, checksums, token/editorial hashes, and lineage. They do not store Greek source wording, manuscript transcription, manuscript image data, preferred readings, or normalized source text.

The scanner requires `--no-authority` and `--no-text`.

## T433 Shadow Parity

T435-A compares the Rust-observed Phlm.1.1-Phlm.1.3 shape counts with the T433 candidate pilot:

- 41 source-token shapes
- 7 editorial-layer shapes

This is a same-scope parity check only. It does not replace T433 rows and does not authorize alignment truth.

## Why Rust Here

This slice is a stable deterministic leaf workload: parse XML, count observed shapes, hash content without storing it, and emit ordered JSON/JSONL. That fits the Rust-first direction without moving governance meaning into Rust.

Python still validates source-view lineage, row shape, authority flags, production-root blocks, and parity.

## Not Yet

T435-A is not a Hebrew scanner. Hebrew Jonah should get a separate pilot before UXLC/OSHB assumptions are hardened in Rust.

T435-A does not populate:

- `data/candidate/original_language_evidence/source_tokens/`
- `data/candidate/original_language_evidence/strong_alignment/`
- `data/candidate/original_language_evidence/lemma_morphology/`
- `data/candidate/original_language_evidence/textual_variants/`
- `data/candidate/original_language_evidence/witness_support/`
- `data/candidate/original_language_evidence/editorial_layers/`

## Non-Authorizations

T435-A authorizes no source-language truth, lexical truth, word-level alignment truth, Strong's-as-source-text claim, lemma/morphology population, preferred reading, source-tradition preference, textual-critical decision, manuscript witness support, translation judgment, chunk boundary, reviewed gold, chunk output, route/evaluator behavior, graph/retrieval truth, embeddings/indexes, or theology authority.

## Validation

Focused gates:

```bash
cargo fmt --manifest-path tools/original_language_observation_scanner/Cargo.toml --check
cargo test --manifest-path tools/original_language_observation_scanner/Cargo.toml
cargo run --manifest-path tools/original_language_observation_scanner/Cargo.toml -- scan-sblgnt --source-view data/candidate/original_language_evidence/canonical_source_views/sblgnt --manifest data/candidate/original_language_evidence/canonical_source_views/sblgnt/canonical_source_view_manifest.yaml --included data/candidate/original_language_evidence/canonical_source_views/sblgnt/included_files.jsonl --out build/original_language_observation/T435-A/sblgnt --no-authority --no-text --shadow-t433 data/candidate/original_language_evidence/pilots/T433_phlm_alignment_bridge
python scripts/validate_t435_original_language_observation_scanner.py --input build/original_language_observation/T435-A/sblgnt
python -m pytest tests/test_t435_original_language_observation_scanner.py -q
```

Merge gates remain `validate_all.py`, full pytest, data-map check, and `git diff --check`.
