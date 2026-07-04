# T424 Rust-Accelerated Validation Layer

## Summary

T424 keeps Python and pytest as the governance orchestrator, while adding Rust for deterministic, data-heavy validation passes. The first enabled fast paths are JSONL invariant scanning and canonical 66-book scope checks. Policy, theology, task-scope, handoff, route, evaluator, and control-plane validation remain Python-owned.

## Implemented Slice

- `tools/logos_fast_validators/` is an isolated Rust CLI for deterministic leaf validators.
- `jsonl-scan` mirrors the existing generated JSONL invariants and can emit a JSON summary.
- `canonical-scope` mirrors the canonical 66-book config and record-scope checks.
- `canonical-qa` exists only as a scaffold; `scripts/qa_canonical_corpus.py` remains authoritative.
- `chunk-map` is intentionally deferred until T424-D.

## Python Boundary

The wrappers preserve existing repo ergonomics:

```bash
python scripts/validate_fast_jsonl.py --python-fallback --require-canon <jsonl...>
python scripts/validate_fast_canonical_scope.py --python-fallback <jsonl...>
```

`--python-fallback` is availability fallback only. If Rust runs and reports a validation failure, the wrapper fails closed instead of hiding the failure behind Python.

## validate_all Integration

`scripts/validate_all.py` uses the fast wrappers only for generated canonical data scans:

- canonical 66 record scope
- generated JSONL invariants

It does not use Rust for governance YAML, task scopes, handoffs, theology-policy language, route isolation, evaluator policy, or corpus QA.

## Coding Preflight

T424 also adds `.ai/control/coding_runtime_language_preflight.yaml`, validated by `scripts/validate_coding_runtime_language_preflight.py`.

The policy is Rust-first for high-resource deterministic code: new validators, scanners, importers, chunk-map comparisons, or CI/`validate_all.py` hot paths must consider Rust when normal repo data is expected to hit one of these thresholds:

- runtime at least 60 seconds
- streamed input at least 100 MB
- parsed records at least 100,000
- resident memory pressure at least 512 MB
- recurring validation/CI path where Rust likely saves at least 30 seconds or 25% runtime

Python/pytest remain authoritative for governance orchestration, task scopes, handoffs, theology-policy language, wrappers, fixtures, and small semantic validators. The required decision record captures data size, expected runtime, Rust trigger, chosen language, wrapper/fallback plan, validation plan, and maintenance tradeoffs.

## DAD Lesson And Asset Outbox

T424 records reusable lessons and asset candidates for DAD in `.digital-asset/mail/outbox.jsonl` as `msg-20260703-t424-rust-validation-layer`.

The DAD message is candidate-only and requires local adoption. It offers three reusable asset candidates:

- Rust leaf-validator CLI pattern
- Rust-first high-resource coding-runtime preflight
- Python wrapper plus Rust fallback pattern

`scripts/validate_dad_outbox.py` checks the outbox, required T424 artifacts, asset candidates, and non-authorizations. `validate_all.py` runs that validator so future agents keep sending useful lessons/assets to DAD without granting DAD authority over this repo.

## Non-Authorizations

T424 does not authorize chunk output, reviewed gold, child spans, route/evaluator behavior, graph/retrieval/vector truth, embeddings, indexes, source rows, canon changes, source-tradition preference, target selection, or theology authority.

## Next Steps

- T424-B/C can add benchmark summaries and parity runs on larger generated ledgers.
- T424-D may add `chunk-map` validation only once multi-model chunk artifacts are large enough to justify it.
