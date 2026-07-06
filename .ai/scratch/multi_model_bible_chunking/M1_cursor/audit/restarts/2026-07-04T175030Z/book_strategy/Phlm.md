# Phlm — book strategy (literary_marker_aware_v2)

## selected_strategy
Independent scratch chunking for Phlm using Rust observation substrate verse markers.
Produced 8 chunks. Strategy profile: {"base_lit": "epistle", "split_p": true, "epistle_sections": true}.

## literature_type_or_mixed_genre
Base genre: epistle. Per-chunk literature_type_guess assigned from markers and epistle/psalm heuristics.

## substrate_markers_considered
Verse-level marker_counts: p (paragraph), q1/q2 (poetry stanzas), d (superscription/doxology evidence), f/fr/ft (footnotes evidence-only).
Chapter rollups used for coverage checks only, not as silent boundary authority.

## strongs_metadata_considered_evidence_only
strong_ids and wh/wg marker counts inform strong_or_hebrew_tags_used only; never boundary authority.

## independent_boundary_rationale
Boundaries chosen from paragraph and pericope signals visible in substrate without copying other models or template example spans.

## chapter_only_fallback_reason_if_used
No silent chapter-only fallback; paragraph (p) and chapter boundaries drive splits where substrate shows them.

## expected_low_confidence_regions
Marker-rich poetry, embedded hymn (Jonah 2), epistle transitions (Phlm), apocalyptic scenes (Rev), mixed narrative-law (Gen).

## frontier_or_atlas_candidate_expectations
Rev: every chunk frontier_flag_considered; low/medium_low chunks feed all three sidecars.

## non_authorizing
Scratch compare input only. Not canon, gold, atlas promotion, or theology authority.
