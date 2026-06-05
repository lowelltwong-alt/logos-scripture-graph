# Chunking Gold Scaffold

Status: planning scaffold; no new gold assertions are promoted by this file.

This directory is the landing zone for per-form chunking gold evidence. Output-changing chunking
skill work must cite a per-form gold file or manifest before claiming improvement.

## Current Baseline

- Corrected evaluator baseline: `D_claude_pass2` = 93.0.
- Old evaluator baseline: 88.5.
- Provenance: the same D / Claude pass2 chunk output was scored under both evaluators.
- Interpretation: T311 corrected the evaluator surface; it did not improve chunk output.

## Required Before T310 3b

- Reproduce the corrected baseline scorecard and relevant output hashes.
- Cite the target per-form gold plan or manifest.
- Identify the target-form output behavior expected to change.
- Prove non-target output remains byte-identical.
- Preserve hard gates: 0 USFM leaks, 0 book crossings, 100% prose sentence integrity, Psalm 23 as
  one chunk, and Genesis 1 no mid-sentence.
- Keep raw and canonical data untouched.

## Manifest Convention

No formal gold manifest schema is committed yet. Until one exists, each per-form plan must state:

- target form and route/skill under test;
- passages or controls;
- expected chunk-boundary behavior;
- forbidden diffs;
- evaluator metric used and known risks;
- baseline run or scorecard provenance;
- reviewer or promotion status.

Do not treat a plan file as promoted gold. Promotion requires explicit review and a committed
manifest or tests that name the accepted boundaries.
