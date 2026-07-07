# 2Sam — book strategy (literary_marker_aware_v2)

## selected_strategy
2Sam: historical narrative. 281 chunks from paragraph (`p`), scene/speech boundaries, and chapter discourse markers.

## literature_type_or_mixed_genre
Config genre: narrative. Scene and speech units, royal lists, land-allotment material, embedded poetry.

## substrate_markers_considered
p (paragraph/scene), q1/q2 (embedded poetry), s/s1 (section headings evidence-only), f/fr/ft (footnotes evidence-only).

## strongs_metadata_considered_evidence_only
Strong's Greek (G) and Hebrew (H) IDs from substrate `strong_ids` and wh/wg marker counts inform `strong_or_hebrew_tags_used` as evidence only. They do not set chunk boundaries.

## independent_boundary_rationale
Boundaries for 2Sam chosen from substrate paragraph, chapter, stanza, and discourse markers. No copied template spans or other-model maps.

## chapter_only_fallback_reason_if_used
No silent chapter-only fallback where paragraph, scene, or speech markers exist.

## expected_low_confidence_regions
Royal speeches, land-allotment lists, genealogy/list spans, embedded poetry, variant/footnote pressure.

## frontier_or_atlas_candidate_expectations
Low/medium_low and marker-rich chunks append to all three sidecars.

## non_authorizing
Scratch compare input only. Not canon, reviewed gold, atlas promotion, or theology authority.
