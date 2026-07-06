# Dan Strategy

- selected_strategy: literary_marker_aware_v2
- model_id: M4_codex_gpt55
- wave: Major Prophets
- primary_literature_type: prophets
- local_marker_signals: chapter_count=12, verse_count=357, feature_flags=genre_prophets, has_footnote, has_heading_marker, has_poetry_or_liturgy_marker, has_strong_h
- marker_counts_considered: p=134, m=3, q1=19, q2=24, b=1, d=0, sp=0, li1=0, ili=0, wj=0, f=20, fqa=0, x=0

## Boundary Strategy

This pass uses the Rust observation substrate first. It starts from substrate paragraph, speaker, list, poetry, WJ, footnote, cross-reference, and chapter rollup evidence, then groups adjacent marker units into 18-30 verse literary clusters for prophets material. Chapter boundaries are treated as weak navigation evidence, not as silent authority.

Paragraph markers are used as local prose/discourse evidence. Poetry markers, superscriptions, stanza breaks, Selah-style rubric signals, and acrostic/stanza risks are preserved by smaller poetry clusters. Discourse and speaker-shift markers are kept visible, especially in Job, Gospels, Acts speeches, and WJ-marked regions. Oracle and vision material is kept in smaller units and escalated when the book or marker pattern risks fulfillment, chronology, or source-tradition pressure. Lists and genealogies are grouped as list-form units without making covenant, chronology, or identity claims.

Strong's Greek/Hebrew metadata was considered only as evidence that original-language metadata is present. It never sets a boundary, lexical meaning, theology, source-language claim, or authority decision. WJ/red-letter markers were considered only as edition metadata evidence. They never decide speaker attribution or Jesus/narrator discourse boundaries.

## Low Confidence And Escalation

Low-confidence triggers for this book: full-chapter fallback in marker-rich regions, poetry/liturgy markers, speaker labels, WJ spans, footnotes or variant readings, cross-references, list/genealogy markers, law/covenant form, oracle/vision material, and any doctrinal pressure that could make a boundary look like theology. Frontier escalation is required for Daniel and Revelation and is optional-but-visible for marker-sensitive material elsewhere.

## Independent Rationale

This strategy is not a silent chapter-only map. It uses chapter boundaries only as weak constraints while choosing paragraph, stanza, speaker, list, discourse, oracle, vision, and argument clusters from the shared substrate. The result is a scratch comparison map, non-authorizing and intentionally auditable.
