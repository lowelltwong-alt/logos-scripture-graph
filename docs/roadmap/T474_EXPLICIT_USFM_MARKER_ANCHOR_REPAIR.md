# T474 Explicit USFM Marker-Anchor Repair

## Purpose

T474 repairs the importer defect established by T473 without regenerating committed
Scripture data. Marker ownership is resolved before an event, boundary claim,
section heading, witness, or token can be emitted.

## Owner Gate

The owner instructed Codex to continue after T473-ANCHOR-A was presented as the
exact recommended gate. T474 records that instruction as approval for importer
code and synthetic fixtures only.

It does not authorize canonical or processed regeneration, reviewed-gold changes,
chunk output, route/evaluator changes, graph/retrieval/vector truth, source
tradition, canon scope, or theology authority.

## Resolution Model

Every line marker is represented by:

- anchor_kind
- anchor_osis_ref
- prior_osis_ref
- next_osis_ref
- body_disposition
- anchor_resolved

The six anchor kinds are current_content, next_content_start,
between_units, chapter_context, book_context, and unresolved.

Body disposition is separate because a paragraph or poetry marker may either
carry current-verse text or introduce the following verse. Heading and speaker
label bodies are editorial metadata and never Scripture text.

## Deterministic Rules

- Empty paragraph, poetry, and list markers bind to the following verse.
- Body-bearing paragraph, poetry, and list lines append only when an active
  current verse exists.
- d, section headings, and sp describe following content and are editorial-only.
- b and nb preserve both neighboring refs. A terminal b keeps a null next ref
  rather than guessing.
- c, cl, and cp are chapter context.
- qs is an inline character marker and never a line-level boundary claim.
- Unknown or malformed ownership is unresolved, receives no anchor, and cannot
  mutate witness text or canonical tokens.

The importer precomputes the next verse at or after each source line in O(n)
time per file, avoiding repeated scans and keeping the rule deterministic.

## Fixture Proof

Synthetic fixtures cover:

1. Psalm 119 headings before verses 1 and 9.
2. Song of Songs speaker labels.
3. Current-verse body-bearing margin and poetry lines.
4. Empty next-start paragraph/poetry lines.
5. Interior and terminal blank lines.
6. Cross-chapter no-break relations.
7. Inline qs.
8. Unknown and malformed marker bodies.

The fixtures prove that heading/speaker Strong tags do not create WordTokens and
that labels do not enter TranslationWitness text.

## Next Route

T475 may run the repaired importer only into ignored shadow roots and produce
exact hashes and row-level deltas. It may not replace committed canonical or
processed outputs. T476 then presents those exact deltas for owner decision.
