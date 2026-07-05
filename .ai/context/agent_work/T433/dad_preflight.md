# T433 DAD Preflight

Task: T433 Philemon Original-Language Alignment Bridge Pilot.
Mode: candidate evidence pilot, non-authorizing.

## DAD Surfaces Checked

- Central DAD checkout: `C:/Users/lowel/OneDrive/Desktop/Git Projects/04_Digital_Assett_Directory`
- Existing lesson themes from prior T431/T432 work:
  - raw archives may contain mixed corpus/support material and need canonical-only source views;
  - derived source views need byte-lineage proof back to immutable raw archive members;
  - Rust fast paths should wait for stable row shapes and parity fixtures;
  - source metadata must be span-locally observed before it can populate rows.

## Applied Lessons

- T433 consumes the T431 canonical source view, not raw archives directly.
- SBLGNT is used first because `Phlm.xml` exposes explicit `<w>` source-token elements without per-token Strong's or morphology metadata.
- UGNT is treated as deferred context because the selected `Phlm.SFM` view does not visibly expose per-token Strong's or morphology fields even though the source manifest records metadata availability at the broader package level.
- Rust is deferred to T435 because this slice is a three-verse semantic/schema pilot, not a high-volume scanner.

## Candidate DAD Lesson

Lesson candidate: manifest-level metadata is not enough for evidence-row population. A task must prove metadata availability at the selected canonical source-view file and span before it records Strong's, morphology, lemma, witness, or variant rows.

Example: UGNT is package-level metadata-rich, but the selected Philemon canonical source view is plain Greek USFM for this pilot. Treating the package flags as per-token row evidence would create a provenance leak.

Recorded in central DAD as:

- `dad:rust-rollout-lesson:37f4f8df-41dc-57f5-a7af-1c2b7bf1431c`

No DAD authority was imported into local Scripture Graph governance. DAD remains candidate-only.
