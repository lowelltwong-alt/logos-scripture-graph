# Chunking Gold

Status: executable Psalm gold exists for settled T310 3b-gold cases; Ps.78 remains
characterization-only and pending human review.

This directory is the landing zone for per-form chunking gold evidence. Output-changing chunking
skill work must cite a per-form gold file or manifest before claiming improvement.

## Current Baseline

- Corrected evaluator baseline: `D_claude_pass2` = 93.0.
- Old evaluator baseline: 88.5.
- Provenance: the same D / Claude pass2 chunk output was scored under both evaluators.
- Interpretation: T311 corrected the evaluator surface; it did not improve chunk output.

## Current Executable Gold

- Psalm manifest: `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- Executable tests: `tests/test_chunker_gold.py`
- Reviewed/settled Psalm cases:
  - Ps.23 as one whole-psalm chunk.
  - Ps.119 as 22 intentional sections, reported but not penalized as literal fragmentation.
  - Short Psalm holdouts: Ps.1, Ps.8, Ps.100, Ps.117.
  - Real superscription source evidence for Ps.3 with no orphan title chunk.
  - Non-target poetry controls route-stable on monolith fallback: Song, Lam, PrMan, Ps151.
- Characterization-only case:
  - Ps.78 current split, token counts, and structural evidence. Its merge-vs-preserve-`\b`
    decision remains unresolved and human-gated.

## Manifest Convention

No formal repository-wide gold manifest schema is committed yet. Until one exists, each per-form
manifest or plan must state:

- target form and route/skill under test;
- passages or controls;
- expected chunk-boundary behavior;
- forbidden diffs;
- evaluator metric used and known risks;
- baseline run or scorecard provenance;
- reviewer or promotion status;
- whether each case is reviewed gold, characterization-only, or pending human review.

Do not treat characterization-only records as promoted expected boundaries. Promotion requires
explicit review and committed tests or manifests that name the accepted boundaries.
