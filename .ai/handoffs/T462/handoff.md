# T462 Handoff - Modular Rust Fast Validator Bundle

## Task id

T462

## Agent name

Codex

## Mode

deterministic_validation_architecture_hardening

## Files read

- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md` (read only)
- `.ai/control/PROJECT_STATUS.md`
- `docs/roadmap/T424_RUST_ACCELERATED_VALIDATION_LAYER.md`
- `tools/logos_fast_validators/src/main.rs`
- `tools/logos_fast_validators/Cargo.toml`
- `tests/test_t424_rust_fast_validators.py`
- `.digital-asset/context-map.json`
- `.digital-asset/mail/outbox.jsonl`

## Files changed

- `.ai/tasks/T462.task.yaml`
- `.ai/handoffs/T462/handoff.md`
- `.ai/control/PROJECT_STATUS.md`
- `.digital-asset/context-map.json`
- `.digital-asset/mail/outbox.jsonl`
- `.digital-asset/lessons/t462_modular_rust_validator_bundle.yaml`
- `docs/roadmap/T424_RUST_ACCELERATED_VALIDATION_LAYER.md`
- `tools/logos_fast_validators/src/main.rs`
- `tools/logos_fast_validators/src/legacy.rs`
- `tools/logos_fast_validators/src/reports.rs`
- `tools/logos_fast_validators/src/jsonl_scan.rs`
- `tools/logos_fast_validators/src/canonical_scope.rs`
- `tools/logos_fast_validators/src/canonical_qa.rs`
- `tools/logos_fast_validators/src/span_parse.rs`
- `tools/logos_fast_validators/src/chunk_map.rs`
- `tools/logos_fast_validators/src/word_tokens.rs`
- `tools/logos_fast_validators/src/bundle.rs`
- `tests/test_t424_rust_fast_validators.py`

## Decisions made

- Kept existing Rust fast-validator CLI command names stable for Python wrappers.
- Split the monolithic Rust entry file into a short dispatcher plus named modules.
- Added `CheckReport` as the one module boundary: every Rust check can now return a named status,
  elapsed time, and message.
- Added `span-parse` as a small standalone structural module.
- Added `bundle` as the one-way-in/one-way-out command for agents that want a single Rust run while
  preserving per-check failure identity.
- Reported the pattern to DAD as candidate-only reusable guidance.

## Validation performed

- `cargo test --manifest-path tools/logos_fast_validators/Cargo.toml` -> passed, 9 tests.
- `python -m pytest tests/test_t424_rust_fast_validators.py -q` -> passed, 21 tests.
- `python scripts/validate_dad_outbox.py` -> passed.
- `python scripts/validate_task_scope.py --task-id T462` -> passed.
- `python scripts/agent/validate_handoffs.py` -> passed.
- `python scripts/validate_all.py` -> passed in generated-sidecars-absent mode, then passed again
  after regenerating ignored canonical sidecars locally.
- `python pipelines/ingest/usfm_importer.py --canonical-66-filter` -> generated ignored canonical
  and processed sidecars for full-data validation.
- `cargo run --quiet --manifest-path tools/logos_fast_validators/Cargo.toml -- bundle --canonical-root data\canonical --summary-json build\t462\bundle_summary.json` -> passed, 3 checks.
- `python scripts/generate_data_map.py --check` -> passed after ignored sidecar generation.
- `python -m pytest -q` -> passed, 793 tests.
- `git diff --check` -> passed.

## Risks introduced

- `legacy.rs` remains as a temporary compatibility module. Future cleanup should move validator
  internals into the named modules incrementally.
- The new `bundle` command is not wired into `validate_all.py`; this is intentional until runtime
  parity and lifecycle policy justify it.

## Unresolved questions

- Whether the next T424/T46x task should migrate one legacy validator fully into its module, likely
  `span_parse` first, then `chunk_map` or `word_tokens`.
- Whether `validate_all.py` should eventually call `bundle` or keep the current Python wrapper fanout.

## Exact next action for the next agent

Open a narrow PR for T462. Do not wire `bundle` into routine validation or remove Python wrappers
without a separate lifecycle decision.

## Non-authorizations preserved

- No chunk output.
- No reviewed gold.
- No child spans.
- No route/evaluator behavior changes.
- No graph/retrieval/vector truth.
- No embeddings or indexes.
- No boundary import.
- No canon-scope change.
- No preferred reading or source-tradition choice.
- No theology authority.
