# T424 Rust-Accelerated Validation Layer

## Summary

T424 keeps Python and pytest as the governance orchestrator, while adding Rust for deterministic, data-heavy validation passes. The first enabled fast paths are JSONL invariant scanning and canonical 66-book scope checks. Policy, theology, task-scope, handoff, route, evaluator, and control-plane validation remain Python-owned.

## Implemented Slice

- `tools/logos_fast_validators/` is an isolated Rust CLI for deterministic leaf validators.
- `jsonl-scan` mirrors the existing generated JSONL invariants and can emit a JSON summary.
- `canonical-scope` mirrors the canonical 66-book config and record-scope checks.
- `canonical-qa` exists only as a scaffold; `scripts/qa_canonical_corpus.py` remains authoritative.
- `chunk-map` is enabled as a T424-D shadow fast path for deterministic scratch chunk-map structure/span checks only.
- `span-parse` exposes a small span-shape check for fixture/module troubleshooting.
- `bundle` provides a single command entry point for agents that need one run/one summary while
  preserving per-check `CheckReport` names, timings, and failure messages.

## Modular Rust Shape

Rust fast validators must stay modular, even when agents call one combined command:

```text
main.rs
  -> parse command line and dispatch only
reports.rs
  -> CheckReport, status, elapsed time, JSON summary, aggregate failure handling
jsonl_scan.rs
canonical_scope.rs
canonical_qa.rs
span_parse.rs
chunk_map.rs
word_tokens.rs
bundle.rs
  -> each exposes run_check(input) -> CheckReport
legacy.rs
  -> temporary compatibility module for pre-split validator internals
```

The goal is Rust speed without a black-box mega-test. Each deterministic validator must have a named
module, a small input type, and a `run_check(input) -> CheckReport` boundary. The combined command
is allowed only when it preserves those per-check reports in machine-readable JSON. Python wrappers
remain the stable repo ergonomics, but Rust internals should be easy to unit test and troubleshoot
one module at a time.

Future work should migrate logic out of `legacy.rs` into the named modules incrementally. Do not
move theology policy, owner gates, route/evaluator decisions, reviewed-gold promotion, graph truth,
or other governance semantics into Rust while doing that mechanical cleanup.

## Python Boundary

The wrappers preserve existing repo ergonomics:

```bash
python scripts/validate_fast_jsonl.py --python-fallback --require-canon <jsonl...>
python scripts/validate_fast_canonical_scope.py --python-fallback <jsonl...>
python scripts/validate_fast_chunk_map.py --python-fallback --compare-python <model-folder-or-whole_bible_chunk_map.jsonl>
```

`--python-fallback` is availability fallback only. If Rust runs and reports a validation failure, the wrapper fails closed instead of hiding the failure behind Python.

## validate_all Integration

`scripts/validate_all.py` uses the fast wrappers only for generated canonical data scans:

- canonical 66 record scope
- generated JSONL invariants

It does not use Rust for governance YAML, task scopes, handoffs, theology-policy language, route isolation, evaluator policy, or corpus QA.

The T424-D chunk-map fast path is not wired into routine `validate_all.py`. It is intended for explicit T423/multi-model scratch validation and parity checks. Rust validates required fields, `non_authorizing`, model id, allowed book scope, span shape, duplicate decision ids, contiguous per-book indices, overlap/order, and optional full-Bible book coverage. Python remains authoritative for model comparison, agreement/delta policy, stress-book handling, frontier escalation, owner gates, and promotion decisions.

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

The modular validator follow-up is also reported to DAD as
`msg-20260706-t462-modular-rust-validator-bundle`. That DAD message is a candidate reusable asset
for repos that want Rust speed while keeping failures pinpointable and non-authorizing.

## Non-Authorizations

T424 does not authorize chunk output, reviewed gold, child spans, route/evaluator behavior, graph/retrieval/vector truth, embeddings, indexes, source rows, canon changes, source-tradition preference, target selection, or theology authority.

## Next Steps

- T424-B/C can add benchmark summaries and parity runs on larger generated ledgers.
- Future T424 work may benchmark the `chunk-map` path on completed multi-model marathons and decide whether any focused CI gate is worthwhile. Do not add full scratch scans to routine `validate_all.py` without a separate policy decision.
