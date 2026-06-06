# T313 Token-Size Evaluator / Policy Alignment

## Purpose

Analyze the mismatch between the leaderboard token-size target and the configured chunking policy
before any broad token-size optimization.

## Confirmed

- Current corrected baseline: D / Claude pass2 = 93.0.
- Current D metrics from `eval/chunking_runs/claude-opus-4.8__pass2__D_claude_pass2__20260605T112450Z.json`:
  - chunks: 1374.
  - `tok_p50`: 729.
  - `tok_p90`: 907.
  - `tok_max`: 1441.
  - sentence integrity: 100.0%.
  - `literal_psalms_fragmented`: 1.
  - boundary basis coverage: 100.0%.
  - metadata carry: 100.0%.
- Leaderboard formula in `pipelines/chunking/leaderboard.py`:

```python
TARGET_P50 = 600
OVERSIZE_LIMIT = 1600
score = 100.0
score -= m.get("literal_psalms_fragmented", m.get("psalms_fragmented", 0)) * 0.5
score -= abs(m.get("tok_p50", 0) - TARGET_P50) / 20.0
score -= max(0, m.get("tok_max", 0) - OVERSIZE_LIMIT) / 100.0
score -= (100.0 - m.get("boundary_basis_cov_pct", 0)) * 0.1
score -= (100.0 - m.get("metadata_carry_pct", 0)) * 0.1
```

- Chunking policy values from `config/chunking/chunking_policy.yaml`:
  - `target_tokens`: 700.
  - `soft_max_tokens`: 1100.
  - `hard_max_tokens`: 1600.
- Current size-fitness penalty is `abs(729 - 600) / 20 = 6.45`, so p50 headroom is about +6.45
  composite points if median size were moved exactly to the evaluator target with no regressions.

## Inferred

- The p50 lever is larger than the direct Psalm 78 lever (+0.5), but it is broad and riskier.
- The evaluator currently rewards a median near 600 while the policy names 700 as the target. That
  mismatch can pull implementation toward metric fit rather than policy fit.
- Because current `tok_max` is 1441, the hard-max oversize penalty is not active for D/pass2.

## Risk

- Optimizing p50 to 600 may fight the configured `target_tokens=700`.
- A broad retune could damage sentence integrity, metadata carry, whole-form boundaries, Psalm
  behavior, prose argument units, or non-target poetry controls.
- Changing output to chase size fitness before aligning evaluator/policy could repeat the T311
  lesson: score movement can reflect metric surface choices rather than real quality.

## Proposed Next Step

Before any broad token-size optimization, decide whether:

- the evaluator target should move toward the configured policy target,
- the chunking policy target should move toward the evaluator target, or
- the system should intentionally distinguish retrieval median target from chunk assembly target.

## Recommendation

- No token-size implementation yet.
- Produce analysis/gold first, including representative corpus cases where smaller chunks help
  retrieval and cases where smaller chunks damage discourse or literary boundaries.
- Keep T313 separate from output-changing Psalm work and separate from any future evaluator formula
  PR until the intended target is reviewed.

## Unknown

- Whether 600 or 700 better serves downstream retrieval once graph/entity/context packets exist.
- Whether the p50 target should vary by textual form.
- Whether p50 should remain a composite-ranking component or become a diagnostic metric with
  form-specific thresholds.
