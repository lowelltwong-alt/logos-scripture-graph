# Acts — book strategy (literary_marker_aware_v2)

## selected_strategy
Acts: early church narrative. 330 chunks from paragraph/chapter discourse markers and occasional WJ legacy references.

## literature_type_or_mixed_genre
Config genre: acts. Narrative scenes, speeches, and apostolic discourse units.

## substrate_markers_considered
p (paragraph/scene), wj (where present, evidence-only), f/fr/ft (variant/footnote evidence-only), speech/discourse transitions.

## strongs_metadata_considered_evidence_only
Strong's Greek (G) and Hebrew (H) IDs from substrate `strong_ids` and wh/wg marker counts inform `strong_or_hebrew_tags_used` as evidence only. They do not set chunk boundaries.

## independent_boundary_rationale
Boundaries for Acts chosen from substrate paragraph, chapter, stanza, and discourse markers. No copied template spans or other-model maps.

## chapter_only_fallback_reason_if_used
No silent chapter-only fallback where scene or speech boundaries are visible in substrate.

## expected_low_confidence_regions
Speech boundaries, council scenes, missionary journey transitions, textual-variant pressure, theology-pressure speeches.

## frontier_or_atlas_candidate_expectations
Low/medium_low and marker-rich chunks append to all three sidecars.

## non_authorizing
Scratch compare input only. Not canon, reviewed gold, atlas promotion, or theology authority.
