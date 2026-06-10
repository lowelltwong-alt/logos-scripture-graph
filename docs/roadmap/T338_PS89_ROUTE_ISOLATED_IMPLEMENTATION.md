# T338 - Psalm 89 Route-Isolated Parent/Child Implementation

## Status

- Status: complete
- Branch: `t338-ps89-route-isolated-parent-child`
- Authorized target: `ps89_owner_decision_option_c`
- Authority: PR #47 / T337B owner decision, Psalm 89 Option C

## Precondition

PR #47 / T337B was verified merged before implementation. The merged owner decision authorizes
only the Psalm 89 Option C target:

- parent: `Ps.89.1-Ps.89.52`
- children:
  - `Ps.89.1-Ps.89.4`
  - `Ps.89.5-Ps.89.18`
  - `Ps.89.19-Ps.89.37`
  - `Ps.89.38-Ps.89.45`
  - `Ps.89.46-Ps.89.48`
  - `Ps.89.49-Ps.89.52`

`Ps.89.52` is treated as the Book III doxology scope note inside final child
`Ps.89.49-Ps.89.52`. It is not treated as ordinary lament continuation and is not split into a
one-verse orphan.

## Implementation

T338 implements the change only in the literal Psalm candidate route:

- `pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/algorithm.py`
  - delegates to the monolith Psalm behavior;
  - applies the Psalm 89 Option C split only when full `Ps.89.1-Ps.89.52` input is present;
  - validates reviewed Psalm gold after the split;
  - keeps non-Psalm-89 chunks identical by preserving downstream chunk records and IDs.
- `pipelines/chunking/orchestrator.py`
  - keeps literal `Ps` routing to the candidate skill;
  - keeps all non-Psalm books on `monolith-pass2-v1`;
  - reports route-ledger validation as `same_baseline_ps89_only_pending`.

The direct monolith chunker path remains unchanged. The output-changing behavior is isolated to the
routed Psalm skill path.

## Same-Baseline Evaluation

Temporary evaluation outputs were written only under `%TEMP%/t338_eval`; no committed chunks,
scorecards, leaderboard rows, raw data, or canonical data were regenerated.

Hashes:

- before direct chunker: `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025`
- after direct chunker: `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025`
- before routed orchestrator: `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025`
- after routed orchestrator: `eda6232b2cb7f0ab4c8dacac10ed672c247a1e41ccb1f807ace05d0ca9eec619`

Result:

- direct chunker remained byte-identical;
- routed output changed from 1,131 chunks to 1,136 chunks;
- non-Psalm-89 routed records were byte-identical to the pre-change routed baseline;
- Psalm 89 became exactly the six reviewed child chunks;
- no `Ps.89.52` orphan chunk was emitted.

Evaluator comparison:

| Metric | Before routed | After routed |
| --- | ---: | ---: |
| chunks | 1,131 | 1,136 |
| tok_p50 | 728 | 728 |
| tok_p90 | 898 | 897 |
| tok_max | 1,152 | 1,152 |
| sentence_integrity_pct | 100.0 | 100.0 |
| literal_psalms_fragmented_raw | 1 | 2 |
| reviewed_structural_splits | Ps78 | Ps78, Ps89 |
| literal_psalms_fragmented | 0 | 0 |
| book_crossings | 0 | 0 |
| usfm_leaks | 0 | 0 |

This is an authorized Psalm 89 behavior change, not a whole-Bible improvement claim.

## Scope Guardrails

T338 does not authorize or perform:

- global Selah, blank-line, doxology, poetry, or long-Psalm rules;
- Psalm 136 changes;
- Psalm 78, Psalm 105, Psalm 106, Psalm 119, short-Psalm, or superscription changes;
- evaluator formula changes;
- leaderboard or scorecard changes;
- raw/canonical data mutation;
- committed output or chunk regeneration;
- boundary text import;
- T327G;
- Revelation implementation.

## Next

Send PR #48 / T338 for Claude risk review. After review and green CI, merge if approved. Keep T339
as the next formal same-baseline/risk-evaluation lane; do not start T327G, boundary import, or
Revelation implementation.
