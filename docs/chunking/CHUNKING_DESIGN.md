# Bible Chunking Design

## Purpose

The chunking system must produce retrieval-ready units that preserve biblical literary structure, source formatting, sentence integrity, discourse context, and future Hebrew/Greek alignment.

A chunk is not simply a token window. A chunk is a **derived interpretive retrieval object** with boundary evidence.

## Design principle

Use a boundary stack, not one chunk size.

```text
canonical address layer: book / chapter / verse / OSIS
translation formatting layer: USFM paragraphs, headings, poetry, footnotes
sentence layer: English sentence spans
literary layer: psalm, oracle, proverb, pericope, speech, argument unit
source-language layer: Hebrew accents/clauses/poetic cola; Greek clauses/discourse units
retrieval layer: token windows with overlap only after respecting higher boundaries
```

## Why this is necessary

Generic chunking fails on the Bible because:

- verses are not always sentences
- chapter divisions are later navigation aids, not always discourse units
- poetry requires line/colon preservation
- psalms often function as whole literary objects
- prophets use oracle and vision structures
- epistles use sustained argument chains
- NT quotations may align with LXX rather than Hebrew
- English punctuation may not represent ancient source-language syntax

## Core objects

### TextSpan

A source-aligned text unit: verse, sentence, paragraph, poetic line, heading, or clause.

### BoundaryClaim

A proposed or imported boundary with source and confidence.

Examples:

- USFM paragraph boundary
- USFM poetry line boundary
- English sentence boundary
- whole psalm boundary
- curated pericope boundary
- future Hebrew Masoretic section boundary
- future Greek clause boundary

### RetrievalChunk

A retrieval-ready bundle of text spans selected by boundary rules.

### ContextPacket

The required surrounding context for a chunk.

Example: Romans 8:1-4 may require prior context from Romans 7:14-25 and following context from Romans 8:5-11.

## Boundary hierarchy

### Hard boundaries

Usually never cross:

- book boundary
- source text boundary
- license boundary
- raw source artifact boundary

### Strong boundaries

Avoid crossing unless needed for sentence or literary integrity:

- chapter boundary
- USFM section heading
- USFM paragraph
- psalm boundary
- major speech boundary
- letter opening/body/closing
- prophetic oracle
- vision cycle

### Syntax/literary boundaries

Prefer:

- English sentence end
- direct speech end
- poetic colon/stanza end
- proverb unit
- parable/pericope end
- Greek clause end when available
- Hebrew accent/phrase boundary when available

### Weak boundaries

Never use alone as a final split reason:

- verse boundary
- token budget
- arbitrary character count

## Chunking algorithm v0

1. Parse USFM into ordered events.
2. Build verse-level `TextSpan` records.
3. Preserve USFM structural markers: book, chapter, verse, headings, paragraph, poetry, notes, cross-references.
4. Run English sentence boundary detection inside paragraphs.
5. Generate boundary candidates from USFM, sentence, chapter, and genre policy.
6. Score candidate boundaries using `config/chunking/chunking_policy.yaml`.
7. Assemble chunks by preferred literary unit where possible.
8. If chunk exceeds budget, split only at valid internal boundaries.
9. Generate context packets.
10. Validate: no mid-sentence splits, no orphan headings, no orphan psalm superscriptions, no raw text mutation.

## Chunking algorithm v1

Add source-language boundary witnesses:

- WLC Hebrew sections and accents
- Hebrew poetic cola
- SBLGNT or RP Greek punctuation/clause/syntax witnesses
- LXX alignment for OT quotations
- MACULA morphology/syntax if licensed/available

## Genre policies

| Genre | Preferred chunk |
|---|---|
| Narrative | scene or episode |
| Law | legal unit or covenant section |
| Poetry/Psalms | whole psalm or stanza; preserve lines |
| Wisdom | saying/proverb cluster |
| Prophets | oracle, woe, vision report |
| Gospels | pericope, parable, miracle, discourse |
| Acts | narrative episode or speech |
| Epistles | argument or exhortation unit |
| Revelation | vision cycle or oracle |

## Non-negotiable validation rules

A chunk must fail validation if it:

- ends in the middle of a sentence
- separates heading from immediate unit without metadata
- separates psalm superscription from psalm
- splits a poetic line without continuation metadata
- drops USFM markers needed for structure
- lacks OSIS start/end refs
- lacks source text id
- lacks license metadata
- lacks chunking policy version
- lacks boundary basis

## Human review loop

The chunker must generate review-ready diffs for hard books:

- Psalms
- Proverbs
- Job
- Isaiah
- Daniel
- Matthew
- John
- Romans
- Hebrews
- Revelation

Gold sets should be curated incrementally. Do not wait for full-corpus perfection.
