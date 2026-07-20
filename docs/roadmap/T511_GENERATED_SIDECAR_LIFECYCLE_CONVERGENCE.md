---
object_type: implementation_roadmap
trust_zone: governance_control
lifecycle_status: complete_pending_merge
task_id: T511
---

# T511 Generated Sidecar Lifecycle Convergence

## Outcome

Generated canonical sidecars remain ignored, rebuildable products. They are not copied into Git,
removed from validation, or linked across worktrees. A single governed lifecycle registry now
declares each generated-data gate, its command and arguments, and the canonical inputs it requires.

`python scripts/validate_all.py` is the clean-checkout developer mode. It runs every static gate and
every generated-data gate whose complete declared input set is present, while reporting explicit
skips for unavailable generated-data gates. `python scripts/validate_all.py
--require-generated-data` is the release/full-data mode and fails before validation if any declared
generated canonical input is absent.

Pytest modules that directly consume generated canonical rows use the repository-wide
`generated_data(...)` marker. Missing files cause an explicit clean-checkout skip; present files are
never excused, so stale or malformed generated data remains red.

## Contract and parity separation

T433 and T439 committed no-text fixtures retain static contract validation in a clean checkout.
Their builders' `--check` modes are separately registered generated-data parity gates. This keeps
schema, provenance, and non-authorization coverage active without pretending that fixture copies
are independent evidence of current generated-token parity.

## Failure prevention rules

- Add a generated-data consumer to `.ai/control/validation_gate_lifecycle.yaml`; do not add another
  hardcoded presence list to `validate_all.py`.
- Mark direct pytest consumers with every `data/canonical/...` dependency.
- Keep static fixture contract checks separate from currentness/parity checks.
- Treat generated fixture copies as lineage evidence, not as proof that the absent upstream sidecar
  is current.
- Use release mode only after the canonical importer has hydrated the checkout.
- Never junction or symlink mutable generated data between worktrees; independent worktrees need
  independent hydration when full-data verification is required.

## Non-authorizations

T511 does not regenerate or mutate canonical data, retire validators, change Scripture or chunk
output, select doctrine or readings, change canon scope, or create graph, retrieval, vector, index,
or theology authority.

## Validation

- Lifecycle registry and scheduler unit tests, including path-escape rejection.
- Static T433/T439 validation in the clean checkout.
- Explicit release-mode missing-data failure.
- Full clean-checkout `validate_all` and pytest.
- Deterministic writer/checker replay and forced handoff validation.
