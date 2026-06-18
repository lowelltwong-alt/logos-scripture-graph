---
object_type: roadmap_note
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-18 during T359 as stacked, non-output-changing research work after T358."
reason_for_inclusion: "Explain the source-metadata research atlas and its non-authorizing role before future Bible chunking research resumes."
---

# T359 Source Metadata Research Atlas

## Purpose

T359 turns the maintainer's source-metadata lesson into a first-class governed surface:

```text
.ai/control/source_metadata_research_atlas.yaml
```

The atlas makes future agents read and preserve metadata evidence before chunking research, graph
work, retrieval work, or review-packet drafting. It exists because the source Bible includes
internal cross-references, Strong's-style word numbers, Hebrew/Greek metadata, footnotes,
headings, paragraph/poetry markers, WJ/red-letter markers, capitalization, and other formatting
features that can look theologically meaningful.

## Scope

The atlas covers these evidence families:

- editorial cross-references
- Strong's-style word numbers and Hebrew/Greek lexeme tags
- lexical rarity and shared lemmas
- footnotes and alternate readings
- section headings and titles
- paragraph, poetry, and boundary markers
- WJ/red-letter markers
- divine-name/title capitalization
- speaker labels and dialogue markers
- edition formatting and layout

It links those families to observed canonical surfaces:

- `data/canonical/translations/eng-web/word_tokens.jsonl`
- `data/canonical/translations/eng-web/editorial_cross_references.jsonl`
- `data/canonical/translations/eng-web/footnotes.jsonl`
- `data/canonical/translations/eng-web/section_headings.jsonl`
- `data/canonical/translations/eng-web/boundary_claims.jsonl`
- `.ai/control/wj_marker_inventory.yaml`
- `.ai/control/divine_capitalization_inventory.yaml`
- `.ai/control/RAW_SOURCE_INVENTORY.md`

## Non-Authorization

T359 does not authorize Scripture truth, lexical truth, intertext truth, speaker attribution, graph
edges, retrieval truth, reviewed gold, chunk boundaries, output changes, boundary import,
embedding/vector work, or new algorithm behavior.

The atlas is research memory and review scaffolding only. Future output-changing use of any
metadata family still requires exact passage scope, owner review, reviewed gold or equivalent
governed evidence, non-target identity proof, validators/tests, and a later
implementation-authorizing decision.

## Priority Research Cases

The atlas records five priority cases where metadata is likely to matter:

- Revelation cross-references, WJ/voice metadata, divine titles, and symbolic intertexts.
- John 3 WJ/speaker-boundary metadata.
- Romans 9-11 argument and cross-reference metadata.
- Messianic Psalms headings, crossrefs, lexemes, and governed Psalm 89 constraints.
- Jude noncanonical-reference metadata.

These are not reviewed gold, not selected implementation targets, and not chunk-output changes.

## Validation

T359 adds:

- `scripts/validate_source_metadata_research_atlas.py`
- `tests/test_source_metadata_research_atlas.py`

The validator fails closed if the atlas loses required families, loses observed surfaces, records
stale canonical sidecar counts, drops priority cases, or lets metadata become authority.
