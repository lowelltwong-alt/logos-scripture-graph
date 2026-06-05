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

## Handles

- Form: `psalm_whole`
- Source book: literal `Ps` only
- Non-target poetry books (`Song`, `Lam`, `PrMan`, `Ps151`) remain on
  `monolith-pass2-v1` during Increment 3a.

## Method

The algorithm validates that every input unit belongs to literal `Ps`, then calls
the existing `chunker.chunk_book(...)` implementation with the same arguments the
monolith would receive. No new boundary choices, budget changes, score tuning, or
Psalm optimization are made in Increment 3a.

## Output contract

`RetrievalChunk[]` produced byte-for-byte identically to the monolith path for
literal Psalms. Route facts live only in the route ledger.

## Forbidden

- Do not consume `detect_form` output.
- Do not route all `genre == "psalms"` material.
- Do not route `Song`, `Lam`, `PrMan`, or `Ps151`.
- Do not add route metadata to chunk/context records.
- Do not claim quality improvement.
