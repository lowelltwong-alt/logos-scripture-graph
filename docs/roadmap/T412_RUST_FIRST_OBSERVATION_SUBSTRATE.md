# T412 Rust-First Whole-Bible Observation Substrate

T412 changes the work pattern before Cursor runs long Bible research batches. Cursor should not reread all raw Bible layers as open-ended AI work. A deterministic Rust scanner must first produce compact, no-text, non-authorizing ledgers from the raw WEB USFM zip; Python validates those ledgers; Cursor consumes compressed packets; Codex reviews; Claude/frontier audits hard cases; the owner gates any reviewed-gold or output work.

## Pipeline

```text
Rust scan -> Python validate -> Cursor compressed packet -> Codex review -> Claude hard-case audit -> Owner gate -> output task
```

## Runtime Proof

Claude's final plan audit found no authority leakage, but blocked merge until the Rust scanner compiled and ran on real data. T412 now closes that blocker: Rust stable GNU compiled the scanner, `cargo test` passed, the scanner read the WEB USFM zip and wrote ignored no-text ledgers for 83 source files, 66 canonical books, 38,058 verses, and 1,402 chapter spans, generated-mode validation passed, and the T411 Cursor pack `--check` passed. Strong's IDs remain observable evidence in feature flags and `strong_occurrence_index.jsonl`, but Strong's presence alone does not create `risk_signal_index.jsonl` rows.

The Rust scanner lives at `tools/usfm_observation_scanner/` and writes ignored generated outputs to `build/observation_substrate/current/`:

- `scan_manifest.json`
- `book_observations.jsonl`
- `verse_observations.jsonl`
- `span_observation_features.jsonl`
- `risk_signal_index.jsonl`
- `strong_occurrence_index.jsonl`
- `marker_anomalies.jsonl`

The ledgers record hashes, source entries, canonical/excluded classification, marker counts, line spans, Strong's IDs, WJ/speaker/footnote/crossref/variant/poetry signals, and risk flags. They must not store full Bible text. Strong's IDs and `has_strong_h` / `has_strong_g` are evidence feature flags and Strong occurrence rows only; Strong's presence alone is not a risk signal because it is ubiquitous metadata. No-text enforcement is key-name based plus scanner-contract based: rows declare `no_text: true`, known Bible-text-bearing keys are forbidden, and free-text audit/anomaly reason fields are not length-scanned.

## Cursor Gate

T411 remains frozen until the Rust substrate validates. Cursor's default work product becomes a ledger-first packet, not a raw whole-Bible reread. Cursor may inspect raw USFM only for an exact owner/Codex-supplied span exception or an escalation packet, and that exception must log bytes, chars, lines, hashes, limitations, and `non_authorizing: true`.

All Rust, Python, and Cursor outputs are evidence only. They cannot authorize target selection, reviewed gold, child spans, chunk output, route/evaluator behavior, graph/retrieval/vector truth, embeddings/indexes, boundary import, backend/profile choices, source rows, canon changes, preferred readings, source-tradition choices, or theology authority.

## Validation

Focused substrate validation:

```bash
cargo test --manifest-path tools/usfm_observation_scanner/Cargo.toml
cargo run --manifest-path tools/usfm_observation_scanner/Cargo.toml -- scan --source data/raw/bible/eng-web/usfm/eng-web_usfm.zip --canon config/canon/canonical_66_books.yaml --marker-coverage config/ingest/usfm_marker_coverage.yaml --book-genres config/chunking/book_genres.yaml --out build/observation_substrate/current --no-text
python scripts/validate_rust_observation_substrate.py --input build/observation_substrate/current
python scripts/build_cursor_observation_pack.py --input build/observation_substrate/current --task-id T411 --check
python -m pytest tests/test_rust_observation_substrate.py -q
```

Merge validation keeps `validate_all.py` fast. It runs the T412 contract validator only; it does not rerun the full Rust Bible scan unless a focused data-pipeline task explicitly requests it.

## Claude Audit Prompt

```text
Review the T412 Rust-first whole-Bible observation substrate plan for logos-scripture-graph.

Goal:
Do not let Cursor reread all raw Bible layers as open-ended AI work. Rust should deterministically scan the raw WEB USFM zip first, Python should validate the ledgers, Cursor should consume compressed non-authorizing evidence packs, Codex should review, Claude/frontier should audit hard cases, owner gates should control reviewed gold/output.

Check for:
1. Any P0/P1/P2 architecture or governance findings.
2. Any authority leakage from Rust/Python/Cursor outputs into chunk boundaries, reviewed gold, route/evaluator behavior, graph/retrieval/vector truth, canon scope, source-tradition preference, or theology authority.
3. Whether the proposed ledgers are sufficient for Cursor to avoid whole-Bible raw rereads.
4. Whether no-text ledgers still preserve enough auditability: source hashes, book/file counts, verse refs, marker counts, Strong's IDs, WJ/speaker/footnote/crossref/variant signals, and risk flags.
5. Whether high-risk genres still require frontier escalation.
6. Whether validation is tiered correctly so full Rust scans do not make every routine task slow.
7. Whether T411 should be frozen until this substrate exists.

Return:
- approve / approve-with-edits / reject
- P0/P1/P2 findings
- required edits before implementation
- whether Cursor may proceed after Rust substrate validation
```

## Governance Split

The reusable orchestration pattern may later be proposed upstream to `logos-governance-architecture`. This T412 task keeps raw-source facts, USFM marker handling, generated ledgers, and T411 execution gates local to `logos-scripture-graph`.
