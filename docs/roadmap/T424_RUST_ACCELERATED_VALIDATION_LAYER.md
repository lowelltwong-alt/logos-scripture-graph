# T424 Rust-Accelerated Validation Layer

## Summary

T424 adds a narrow Rust fast path for deterministic data-validation scans while keeping Python as
the governance orchestrator. The first implemented slice covers large JSONL streaming checks and
canonical-66 scope checks. Semantic canonical corpus QA, task scope, handoffs, theology-policy
language, and route/evaluator authority remain in Python.

## Implemented Slice

- `tools/logos_fast_validators/` is an isolated Rust CLI.
- `jsonl-scan` mirrors the generated JSONL invariants from `scripts/validate_jsonl.py`.
- `canonical-scope` mirrors the streamable canonical-66 record checks from
  `scripts/validate_canonical_66_scope.py`.
- `canonical-qa` is present only as a non-authorizing scaffold. Full canonical QA remains
  `scripts/qa_canonical_corpus.py`.
- `chunk-map` is intentionally deferred until T424-D, after multi-model artifacts are large enough
  to justify a Rust checker.

## Python Boundary

The wrappers `scripts/validate_fast_jsonl.py` and
`scripts/validate_fast_canonical_scope.py` call Rust when available. They expose:

- `--require-rust` for focused proof and CI slices that must exercise the Rust path.
- `--python-fallback` for rollout environments where Cargo is unavailable.
- `--compare-python` for parity proof against the original validators.

Fallback is used only when Rust cannot be invoked. A Rust validation failure remains a failure.

## validate_all Integration

`scripts/validate_all.py` now uses the fast wrappers for generated canonical JSONL and canonical
scope scans. It still runs the original Python validators for policy/control-plane surfaces and
keeps canonical corpus QA in Python.

## Non-Authorizations

T424 authorizes no reviewed gold, chunk output, child spans, route behavior, evaluator behavior,
graph truth, retrieval truth, vector/index work, boundary import, backend choice, retrieval profile
promotion, source/manuscript row creation, canon-scope change, preferred reading/source-tradition
selection, or theology authority.

## Next Steps

- T424-D may add a Rust chunk-map checker only after multi-model chunk artifacts become large.
- A later CI task may add path-triggered/manual Rust workflows, following DAD's instruction-mail
  guidance that Logos repos own their own Rust files.
