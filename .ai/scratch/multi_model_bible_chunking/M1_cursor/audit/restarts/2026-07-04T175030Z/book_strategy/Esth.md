# Esth — book strategy (literary_marker_aware_v2)

## selected_strategy
Independent scratch chunking for Esth using Rust observation substrate verse markers.
Produced 73 chunks. Wave processing with paragraph (`p`) and chapter discourse signals.

## literature_type_or_mixed_genre
Book genre from config: narrative. Per-chunk `literature_type_guess` from marker heuristics (narrative, poetry, oracle, etc.).

## substrate_markers_considered
Verse-level `marker_counts`: p (paragraph), q1/q2 (poetry), s/s1 (section), f/fr/ft (footnotes evidence-only).
Chapter rollups used for coverage checks only, not silent boundary authority.

## strongs_metadata_considered_evidence_only
`strong_ids` and wh/wg counts inform `strong_or_hebrew_tags_used` only; never boundary authority.

## independent_boundary_rationale
Boundaries from substrate paragraph/chapter signals without copying other models or template example spans.

## chapter_only_fallback_reason_if_used
No silent chapter-only fallback; paragraph and chapter boundaries drive splits where substrate shows them.

## expected_low_confidence_regions
Genealogy/list spans, embedded poetry, footnote-dense transitions, chronicle parallel passages.

## frontier_or_atlas_candidate_expectations
Low/medium_low and marker-rich chunks append to all three sidecars for Codex/Claude review.

## non_authorizing
Scratch compare input only. Not canon, gold, atlas promotion, or theology authority.
