# Skill: psalm-whole-then-stanza-v1 (candidate)

**PROPRIETARY - All Rights Reserved.** Part of the Covered Work under
`pipelines/chunking/LICENSE`. Copyright (c) 2026 Lowell Wong.

## What it is

A behavior-preserving extraction seam for literal Book of Psalms (`book == "Ps"`)
chunking. Increment 3a routes Psalms through this candidate skill while the skill
delegates to the current monolith Pass-2 Psalm behavior, so chunks and context
packets remain byte-identical to `monolith-pass2-v1`.

This skill is **candidate** only. It is not active, preferred, or a quality
improvement. It exists to prove the orchestrator can route one target form
without changing output.

T333 adds a reviewed-gold guardrail around the delegated output. The guardrail
fails closed if the current Psalm route violates already reviewed Psalm gold:
Psalm 23, Psalm 3, short Psalm holdouts, Psalm 119, Psalm 78, Psalm 105, and
Psalm 106. This does not authorize new Psalm boundaries and does not claim score
or chunking improvement.

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
monolith would receive. No new boundary choices, budget changes, score tuning, or
Psalm optimization are made in Increment 3a.

After delegation, the algorithm validates exact reviewed Psalm postconditions
when those chapters are present in the returned chunks. Reviewed whole-psalm
cases must remain whole-psalm chunks. Reviewed parent/child cases must retain
their exact reviewed child spans. Partial Psalm inputs that do not include a
reviewed chapter are not forced through unrelated reviewed cases.

## Output contract

`RetrievalChunk[]` produced byte-for-byte identically to the monolith path for
literal Psalms. Route facts live only in the route ledger.

## Forbidden

- Do not consume `detect_form` output.
- Do not route all `genre == "psalms"` material.
- Do not route `Song` or `Lam`.
- Do not reintroduce `PrMan`, `Ps151`, or other non-66 material as canonical
  controls.
- Do not add route metadata to chunk/context records.
- Do not claim quality improvement.
- Do not use the reviewed-gold guardrail as permission to split Ps.105/Ps.106,
  merge Ps.78, change Psalm 119, or infer new speaker/marker-based boundaries.
