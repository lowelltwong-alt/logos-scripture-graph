# Skill: monolith-pass2-v1 (interim default)

**PROPRIETARY — All Rights Reserved.** Part of the Covered Work under
`pipelines/chunking/LICENSE`. Copyright (c) 2026 Lowell Wong.

## What it is

A thin metadata wrapper around the **current** `pipelines/chunking/chunker.py` Pass-2
behavior (genre-aware, boundary-driven; corrected T311 evaluator composite **93.0**). It is the
**interim fallback default** for every biblical (non-Tier-C) form until dedicated
per-form skills are extracted (ADR-0011 Increments 3+).

Score provenance: the same D / Claude pass2 chunk output scored **88.5** under the old evaluator.
T311 corrected Psalm fragmentation grouping from bare chapter to `(book, chapter)`, moving that
unchanged output to **93.0**. This is evaluator-surface correction, not chunk-output improvement.

At Increment 0 this skill changes **no** behavior — it only makes the existing
chunker addressable from the registry so the orchestrator shim (Increment 2) can
route to it and reproduce current output byte-for-byte.

## Handles

All biblical forms in `config/chunking/form_registry.yaml` (`interim_skill:
monolith-pass2-v1`): prose, poetry/psalm, wisdom, dialogue, prophetic, gospel,
epistle, narrative, apocalyptic, front-matter. Tier C (early-church) forms are NOT
handled — they are declared gaps the orchestrator alerts on.

## Method (inherited from chunker.py)

- Genre dispatch (`book_genres.yaml`) selects the chunk unit: whole psalm
  (superscription kept), `\b`/interior-`\d` stanza splits for long psalms (Ps 119
  acrostic), heading-bounded / paragraph / sentence prose, wisdom saying-cluster
  budget scaling, epistle context packets.
- Boundary evidence via `boundary_scorer.py` + `chunking_policy.yaml`.

## Output contract

`RetrievalChunk[]` + `ContextPacket[]`, candidate/derived only — never canonical.

## Forbidden (hard gates)

No mid-sentence / mid-colon / psalm-superscription splits; 0 USFM leaks; 0 book
crossings; 100% prose sentence integrity; Psalm 23 = one whole-psalm chunk. No
writes to `data/raw` or `data/canonical`; no source-text mutation.

## Replacement

As dedicated skills (e.g. `psalm-whole-then-stanza-v1`, `prose-heading-paragraph-v1`,
`wisdom-saying-cluster-v1`) are extracted and gold-anchored, they supersede this
skill per-form via `supersedes` edges; this wrapper is deprecated, not deleted.
