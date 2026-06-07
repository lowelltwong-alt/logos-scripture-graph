# Chunking Gold

Status: executable Psalm gold exists for settled T310 3b-gold cases; Ps.78 is now approved as a
parent whole-psalm unit with reviewed child structural chunks.

This directory is the landing zone for per-form chunking gold evidence. Output-changing chunking
skill work must cite a per-form gold file or manifest before claiming improvement.

## Current Baseline

- Current T314 evaluator-policy baseline: `D_claude_pass2` = 93.5.
- T311 book/chapter evaluator baseline: 93.0.
- Old evaluator baseline: 88.5.
- Provenance: the same D / Claude pass2 chunk output was scored under all three evaluator surfaces.
- Interpretation: T311 and T314 corrected evaluator policy; neither improved chunk output.

## Current Executable Gold

- Psalm manifest: `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- Executable tests: `tests/test_chunker_gold.py`
- Reviewed/settled Psalm cases:
  - Ps.23 as one whole-psalm chunk.
  - Ps.119 as 22 intentional sections, reported but not penalized as literal fragmentation.
  - Ps.78 as parent `Ps.78.1-72` with reviewed child chunks `Ps.78.1-69`, `Ps.78.70-71`,
    and `Ps.78.72`.
  - Short Psalm holdouts: Ps.1, Ps.8, Ps.100, Ps.117.
  - Real superscription source evidence for Ps.3 with no orphan title chunk.
  - Non-target poetry controls route-stable on monolith fallback: Song, Lam, PrMan, Ps151.
- Characterization-only cases:
  - None currently in the Psalm manifest.

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
- whether each case is reviewed gold, characterization-only, pending human review, or approved
  structural split under a parent whole unit.

Do not treat characterization-only records as promoted expected boundaries. Promotion requires
explicit review and committed tests or manifests that name the accepted boundaries.
Reviewed parent/child structural split is not bad fragmentation by default.
