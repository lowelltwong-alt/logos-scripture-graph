# Chunking Rules

## Rule 1: Preserve source identity

Every chunk must identify its source text, source artifact, and OSIS span.

## Rule 2: Do not split sentences

A chunk may not end inside an English sentence unless:

- the source sentence exceeds emergency budget, and
- the split is marked `continuation: true`, and
- the following chunk points back to the previous chunk.

## Rule 3: Treat verses as addresses

A verse boundary alone is insufficient as a chunk boundary. Verse boundaries help cite; they do not always define meaning.

## Rule 4: Preserve USFM structure

The importer must preserve:

- `\id` book id
- `\c` chapter
- `\v` verse
- headings such as `\s`, `\ms`, `\mt`
- paragraphs such as `\p`, `\m`, `\q*`
- poetry lines such as `\q1`, `\q2`
- notes and cross-reference markers where present

## Rule 5: Preserve poetry

Poetry should be chunked by whole psalm, stanza, or poetic unit. Do not flatten poetry into prose paragraphs.

## Rule 6: Preserve direct speech

Do not split a speaker's utterance unless the speech is long and internal paragraph/sentence boundaries support it.

## Rule 7: Respect genre policy

Use book/corpus genre policy before token budget.

## Rule 8: Context packets are required for fragile chunks

A chunk requires a context packet when it depends on prior/following argument, speaker, quotation source, or literary structure.

## Rule 9: Source-language witnesses can override English convenience

When Hebrew/Greek/LXX boundary evidence is available, it should become a boundary witness and may adjust chunk policy after review.

## Rule 10: All chunk boundaries are reviewable claims

Chunk boundaries must be auditable. Store boundary source, confidence, policy version, and rationale.
