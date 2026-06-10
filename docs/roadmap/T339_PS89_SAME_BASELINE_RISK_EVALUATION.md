# T339 - Psalm 89 Same-Baseline Risk Evaluation

## Status

- Status: complete
- Branch: `t339-ps89-same-baseline-risk-eval`
- Scope: evaluation, risk review, and control-plane cleanup only
- Reviewed behavior under evaluation: T338 Psalm 89 Option C

## Baseline Inputs

T339 reconstructed the pre-T338 routed baseline from commit `1db3f12`, the PR #47 / T337B merge
commit immediately before T338. It compared that temporary pre-T338 output to current `main` after
PR #48 / T338 merge commit `a495e0c78961195db8a0d6b3df95bcc58f203dd2`.

All evaluation outputs were written under `%TEMP%/t339_eval`. No committed chunks, scorecards,
leaderboard rows, raw data, canonical data, or derived data were regenerated or committed.

## Psalm 89 Behavior

Pre-T338 routed behavior:

| Output | Boundary basis |
| --- | --- |
| `Ps.89.1-Ps.89.52` | `chapter_boundary`, `whole_psalm` |

Post-T338 routed behavior:

| Output | Boundary basis |
| --- | --- |
| `Ps.89.1-Ps.89.4` | `reviewed_structural_split`, `whole_psalm_split` |
| `Ps.89.5-Ps.89.18` | `reviewed_structural_split`, `whole_psalm_split` |
| `Ps.89.19-Ps.89.37` | `reviewed_structural_split`, `whole_psalm_split` |
| `Ps.89.38-Ps.89.45` | `reviewed_structural_split`, `whole_psalm_split` |
| `Ps.89.46-Ps.89.48` | `reviewed_structural_split`, `whole_psalm_split` |
| `Ps.89.49-Ps.89.52` | `reviewed_structural_split`, `whole_psalm_split`, `book_iii_doxology_scope_note` |

The parent literary unit remains `Ps.89.1-Ps.89.52` by reviewed-gold manifest and review-packet
authority. `Ps.89.52` remains inside final child `Ps.89.49-Ps.89.52`, carries the Book III doxology
scope note in routed output, and is not emitted as a one-verse orphan child.

## Hash And Count Results

| Output | SHA-256 |
| --- | --- |
| pre-T338 direct chunker | `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025` |
| post-T338 direct chunker | `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025` |
| pre-T338 routed orchestrator | `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025` |
| post-T338 routed orchestrator | `eda6232b2cb7f0ab4c8dacac10ed672c247a1e41ccb1f807ace05d0ca9eec619` |

Count movement:

- pre-T338 routed chunks: 1,131
- post-T338 routed chunks: 1,136
- delta: +5

The +5 delta is exactly one Psalm 89 parent chunk replaced by six reviewed children.

## Non-Target Identity

T339 compared pre- and post-T338 routed records after excluding records touching `Ps.89`.

Result: non-Psalm-89 routed records were identical.

Named controls remained identical:

| Control | Post-T338 span(s) |
| --- | --- |
| Psalm 78 | `Ps.78.1-Ps.78.69`; `Ps.78.70-Ps.78.71`; `Ps.78.72-Ps.78.72` |
| Psalm 105 | `Ps.105.1-Ps.105.45` |
| Psalm 106 | `Ps.106.1-Ps.106.48` |
| Psalm 119 | 22 reviewed acrostic sections |
| Short Psalms | `Ps.1.1-Ps.1.6`; `Ps.8.1-Ps.8.9`; `Ps.100.1-Ps.100.5`; `Ps.117.1-Ps.117.2` |
| Superscription control | `Ps.3.1-Ps.3.8` |
| Song non-target poetry fallback | `Song.1.1-Song.1.17` for Song 1 control |
| Lamentations non-target poetry fallback | `Lam.1.1-Lam.1.22` for Lam 1 control |

Route ledger checks confirmed Song and Lamentations remain on `monolith-pass2-v1` fallback.

## Metric Interpretation

| Metric | Pre | Post | Interpretation |
| --- | ---: | ---: | --- |
| chunks | 1,131 | 1,136 | Psalm 89 one parent replaced by six reviewed children |
| tok_p50 | 728 | 728 | unchanged |
| tok_p90 | 898 | 897 | distribution changed only by reviewed Psalm 89 split |
| tok_max | 1,152 | 1,152 | unchanged |
| sentence_integrity_pct | 100.0 | 100.0 | unchanged |
| literal_psalms_fragmented_raw | 1 | 2 | raw diagnostic now sees Ps78 and Ps89 structural splits |
| reviewed_structural_splits | Ps78 | Ps78, Ps89 | expected reviewed-gold recognition |
| literal_psalms_fragmented | 0 | 0 | no bad/unreviewed Psalm fragmentation introduced |
| poetry_books_fragmented | 1 | 2 | raw poetry diagnostic includes reviewed Ps89 split |
| book_crossings | 0 | 0 | unchanged |
| usfm_leaks | 0 | 0 | unchanged |

T339 makes no whole-Bible improvement claim. The movement is a reviewed structural correction for
Psalm 89 only. No leaderboard or scorecard update was run or committed.

## RISK-GATE-001

### Confirmed Risks

- Psalm 89 now intentionally differs in the routed path, so direct-vs-routed output is no longer
  byte-identical for that one reviewed target.
- The raw `poetry_books_fragmented` diagnostic increases from 1 to 2 because it sees the reviewed
  Psalm 89 structural split.
- The candidate Psalm skill now contains one output-changing rule, so promotion pressure is higher
  than it was when the skill was behavior-preserving.

### Plausible Risks

- Psalm 89 Option C could be misread as a hidden global Psalm rule.
- `book_iii_doxology_scope_note` could be misread as a global doxology split rule.
- Selah, blank-line, `b`, `qs`, or poetry marker evidence could be mistaken for automatic boundary
  authority rather than reviewed-gold support for this exact span set.
- T340 could promote the candidate skill before enough non-target and post-merge evidence exists.
- A later report could overclaim broad Bible improvement from one reviewed Psalm target.

### Unlikely But High-Impact Risks

- A future master chunker could treat Psalm 89 as training pressure for global poetry behavior or
  non-Bible corpora.
- Boundary or noncanonical texts could be imported as support for Psalm 89 or future Psalm behavior.
- Revelation or another hard-book implementation could cite Psalm 89 as precedent for output change
  without reviewed gold.

### Watch-Later Conditions

- Any new split outside Psalm 89 without reviewed-gold authorization.
- Any change that splits `Ps.89.52` into an orphan child.
- Any route ledger showing Song, Lamentations, Job, Prophets, Gospel discourse, or Revelation on the
  Psalm candidate skill.
- Any leaderboard/scorecard row that frames T338/T339 as whole-Bible improvement.
- Any T340 promotion that lacks explicit owner/reviewer decision and non-target identity evidence.

### Tests Or Guards Still Needed

- T340 should rerun same-baseline checks before any promote/reject decision.
- T340 should explicitly decide whether candidate skill promotion is warranted or whether Psalm 89
  should remain an isolated candidate behavior.
- Future Psalm behavior changes need their own reviewed-gold packets and same-baseline evaluation.

### Owner Decisions Still Needed

- Whether to promote, keep candidate, or reject `psalm-whole-then-stanza-v1` in T340.
- Whether additional Psalm targets such as Psalm 136 should remain pending, become whole-psalm
  controls, or receive separate review decisions.

## Recommendation For T340

Proceed to T340 only as a promote-or-reject decision based on the T338/T339 evidence. Do not promote
the Psalm candidate skill as a broad Psalm optimizer. Any promotion must preserve:

- Psalm 89-only output change scope;
- reviewed-gold authority as the source of behavior;
- no global marker/doxology/poetry heuristic;
- non-Psalm fallback isolation;
- no whole-Bible improvement claim without a separate scorecard/leaderboard policy decision.
