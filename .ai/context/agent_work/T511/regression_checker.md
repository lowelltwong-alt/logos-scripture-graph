# T511 deterministic regression checker

- Role: `regression-checker`
- Relation: distinct read-only checker phase after writer completion
- Verdict: `PASS`

## Replayed evidence

- `python scripts/validate_validation_gate_lifecycle.py` passed.
- Focused lifecycle and T433/T439 tests passed: 18 passed, 2 explicit generated-data skips.
- `python scripts/validate_all.py --require-generated-data` returned the expected exit code 1 and
  lifecycle-declared missing-input message before running gates.
- The simulated-present scheduler test dispatched its registered dummy command and preserved a
  present-but-failing gate as red.
- Forbidden data, pipeline, chunking, governance, master-context, and CI paths had no semantic diff.
- Full clean pytest passed: 996 passed, 55 explicit generated-data skips.

## Proof obligations

- `clean-checkout-convergence`: satisfied.
- `release-fails-closed`: satisfied.
- `coverage-preserved`: satisfied for orchestration and clean-checkout contract coverage.

## Residual limit

This clean worktree intentionally was not hydrated. True corpus parity remains delegated to the
registered existing leaf validators and must run with `--require-generated-data` before release.
No generated artifact was copied or linked merely to manufacture a local parity result.
