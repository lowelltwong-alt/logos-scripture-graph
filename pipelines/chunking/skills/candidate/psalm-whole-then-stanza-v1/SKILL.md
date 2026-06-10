# Skill: psalm-whole-then-stanza-v1 (candidate)

**PROPRIETARY - All Rights Reserved.** Part of the Covered Work under
`pipelines/chunking/LICENSE`. Copyright (c) 2026 Lowell Wong.

## What it is

A route-isolated candidate skill for literal Book of Psalms (`book == "Ps"`)
chunking. It delegates to the current monolith Pass-2 Psalm behavior, then applies
only the owner-reviewed Psalm 89 Option C split authorized by T337B/T338. Chunks
outside Psalm 89 must remain identical to the monolith baseline.

This skill is **candidate** only. It is not active, preferred, or a whole-Bible
quality improvement claim. It exists to keep one reviewed Psalm target isolated
behind the Psalm route.

T333 adds a reviewed-gold guardrail around the delegated output. The guardrail
fails closed if the current Psalm route violates already reviewed Psalm gold:
Psalm 23, Psalm 3, short Psalm holdouts, Psalm 119, Psalm 78, Psalm 105, and
Psalm 106. T338 adds the reviewed Psalm 89 Option C output change only. This does
not authorize new non-Psalm-89 boundaries and does not claim whole-Bible
improvement.

## Handles

- Form: `psalm_whole`
- Source book: literal `Ps` only
- Canonical non-target poetry books (`Song`, `Lam`) remain on
  `monolith-pass2-v1` during Increment 3a. T327D/T327E removed `PrMan` and
  `Ps151` from canonical controls because they are outside the owner-approved
  66-book corpus.

## Method

The algorithm validates that every input unit belongs to literal `Ps`, then calls
the existing `chunker.chunk_book(...)` implementation with the same arguments the
monolith would receive. It applies the exact Psalm 89 child spans only when the
full `Ps.89.1-Ps.89.52` input is present.

After the Psalm 89 split, the algorithm validates exact reviewed Psalm
postconditions when those chapters are present in the returned chunks. Reviewed
whole-psalm cases must remain whole-psalm chunks. Reviewed parent/child cases
must retain their exact reviewed child spans. Partial Psalm inputs that do not
include a reviewed chapter are not forced through unrelated reviewed cases.

## Output contract

`RetrievalChunk[]` from the routed path must differ from the monolith path only
for the approved Psalm 89 parent/child target. Route facts live only in the route
ledger.

## Forbidden

- Do not consume `detect_form` output.
- Do not route all `genre == "psalms"` material.
- Do not route `Song` or `Lam`.
- Do not reintroduce `PrMan`, `Ps151`, or other non-66 material as canonical
  controls.
- Do not add route metadata to chunk/context records.
- Do not claim quality improvement.
- Do not split `Ps.89.52` into a one-verse orphan child.
- Do not treat `Ps.89.52` as an ordinary continuation of the lament appeal.
- Do not generalize Psalm 89 Option C into global Selah, blank-line, doxology,
  poetry, or long-Psalm rules.
- Do not use the reviewed-gold guardrail as permission to split Ps.105/Ps.106,
  merge Ps.78, change Psalm 119, or infer new speaker/marker-based boundaries.
