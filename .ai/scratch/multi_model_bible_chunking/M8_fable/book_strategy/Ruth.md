# Ruth — Book Strategy (M8_fable, candidate-only, non-authorizing)

## selected_strategy

Ruth was chunked on text signals alone, per the freeze file's instruction that this book is "nearly marker-silent" (one pe, zero samekh, both witnesses agreeing) — marks are weak corroboration only and were never used as a driver or a lifter. The resulting map has 19 decisions tiling Ruth.1.1-Ruth.4.22 exactly (85/85 verses, verified by script), averaging 4.5 verses per span, ranging from single-verse asides (2:1, 4:7) to a 10-verse continuous night scene (3:6-15). Boundaries were driven by five recurring, checkable device-types that this short book uses repeatedly and consistently: (1) scene/location/participant-entrance shifts (וַתָּקָם at 1:6, הִנֵּה-fronted entrances at 2:4 and 4:1, movement verbs at 1:19, 2:18, 3:16); (2) addressee-narrowing within a single ongoing conversation (plural-to-singular at 1:14/15, "about her" to "to her" at 2:7/8); (3) inclusio/refrain repetition (the חן bracket at 2:10/13, the doubled weeping-plus-עוד at 1:9/14, the מי את echo at 3:9/16); (4) disjunctive/circumstantial-clause narrator asides (2:1, 4:1, 4:7); and (5) formal genre-heading shifts (the תולדות heading at 4:18). Where a tempting split lacked an independent marker on both edges (the road dialogue's individual speech-turns, the night scene's "until morning" echo, the birth-scene's three speech-beats), the larger unit was preserved and the rejected finer split was documented with reasons.

## literature_type_or_mixed_genre

Predominantly narrative prose carrying direct discourse — most spans are tagged "narrative" or "narrative with embedded dialogue" rather than pure narration, since well over half the book's verses are quoted speech. Three spans break out of this pattern: 1:15-18 embeds one poetic/oath set-piece (Ruth's pledge) without being lifted out as standalone poetry, since it carries no independent scene-marker; 4:7 is a narrator's etiological aside explaining a legal custom, syntactically and temporally distinct from character speech; and 4:18-22 is a formal genealogical register (toledot list), the one span with no narrative or dialogue content whatsoever. So: single dominant genre (narrative-with-dialogue) at the macro scale, with two genuine micro-genre departures (aside, list) both clearly text-marked rather than merely thematically distinct.

## literary_form_decision_matrix

| Device type | Where it surfaced | Effect on chunking |
|---|---|---|
| Scene/location movement verb | 1:6, 1:19, 2:4, 2:18, 3:16, 4:1 | Opens a new unit |
| Disjunctive/circumstantial clause (off-storyline) | 2:1, 4:1 (subject-fronted qatal), 4:7 | Marks narrator-background as its own unit |
| Addressee-scope narrowing (plural→singular) | 1:14/15 | Splits a single conversation into two units |
| "About X" → "to X" addressee shift | 2:7/8 | Splits identification from direct address |
| Inclusio/repeated-phrase bracket | 2:10/13 (חן), 1:9/14 (עוד+weeping), 3:9/16 (מי את) | Confirms/binds unit edges |
| Catchword linkage (concatenatio) | 4:10/11 (עדים) | Weak split signal, priced medium_low |
| Wish (jussive) → fulfillment (wayyiqtol) shift | 4:12/13 | Opens a new unit |
| Formal genre-heading | 4:18 (תולדות) | Hard genre-register boundary |
| Temporal-echo without scene change | 3:13/14 ("until morning") | Treated as continuity (Wiederaufnahme), NOT a boundary |

## substrate_markers_considered

chapter_profile.json and span_features.jsonl were reviewed for the four chapter-level rollups (marker counts for c/f/fr/ft/p/v/w/wh). risk_signals.jsonl flags six WEB translational footnotes (1:6, 1:15, 1:16, 1:20, 2:17, 4:12). These footnotes annotate translation choices (the divine name, "Elohim," the ephah measure, "offspring") and were checked against this map's boundaries: no consistent correlation was found — e.g. the 1:15 and 1:16 footnotes fall on either side of decision boundary M8-Ruth-002/003, which is coincidental (the footnotes annotate the words "Behold" and "God," not a literary seam), while the 1:6, 1:20, 2:17, and 4:12 footnotes all fall mid-unit. Footnote placement was treated as non-authorizing WEB-editorial metadata and never used as boundary evidence.

## strongs_metadata_considered_evidence_only

book_observation.jsonl reports strong_h_count: 2223 and a wh (Strong's-linked word) count of 4 in chapter 1's rollup. These are lexical-tagging density figures describing how much of the translated text carries a Strong's-number link, not a distribution that varies meaningfully across the book's sub-units (Ruth's prose is evenly glossed throughout; there is no untagged or sparsely-tagged stretch that would suggest a source-layer seam). No decision in this map cites Strong's density as evidence; it was consulted only to confirm the absence of any anomaly worth flagging.

## source_metadata_evidence_only_check

web_mt_crosswalk.json and web_mt_verse_check.json both report Ruth as fully verse-identical between WEB and MT (85=85, "status": "identical", chapter_mismatches: []). Every oshb: citation in this map's decisions therefore maps 1:1 to the same verse number in the corresponding web: citation with no realignment, split-verse, or MT/WEB numbering adjustment required anywhere in the book.

## larger_unit_preservation_check

Three places where a finer split was seriously considered and rejected in favor of a larger unit, each documented in the relevant decision's strongest_rejected_alternative:
- 1:6-14 kept as one appeal-and-refusal cycle rather than three per-speech-turn decisions, because the doubled weeping-plus-עוד refrain binds the two speech-rounds together.
- 3:6-15 kept as one unbroken night-and-dawn scene rather than splitting at the "until morning" echo (v13/14), because that repetition is a fulfillment-of-instruction device (continuity), not a scene break.
- 4:13-17 kept as one birth-and-naming scene rather than three per-speech-beat decisions, because none of its internal turns (women's blessing, Naomi's nursing gesture, women's naming) carries an independent location, time, or participant-set change.
- 4:1-6 kept merged rather than split at the elders-convened/negotiation-begins seam (v2/v3), because that internal transition carries no text marker at all — it is a pure topic shift within one continuous wayyiqtol chain.

## list_register_function_check

The toledot genealogy (4:18-22) is the book's only list-like structure and was treated as a single register-unit rather than ten separate "X begat Y" decisions. This follows the principle that a formulaic, internally uniform list functions cumulatively by genre convention — its payoff (reaching דוד, "David") only lands when the whole chain is read as one unit, and each individual link carries no independent narrative content that would justify its own decision. No other genealogies, censuses, or catalogue-lists appear anywhere else in Ruth.

## epistle_unit_check_if_applicable

n/a — Ruth is Hebrew narrative, not epistolary literature; no epistolary conventions (salutation, thanksgiving, body, closing) apply.

## over_split_risk_check

The single biggest over-split risk in this book is the road dialogue of ch.1, where Naomi's three speech-turns (each introduced by an explicit-subject וַתֹּאמֶר) could mechanically be read as three separate decisions per this campaign's general explicit-subject-reset precedent. This map resists that reading: the precedent was applied in combination with (not instead of) a search for an independent, checkable co-occurring signal, and only the plural-to-singular addressee shift at v14/15 supplied one — the earlier explicit-subject reset at v11 (Naomi's second speech) does NOT correspond to any scene, location, or addressee change and was therefore treated as continuation, not a new unit. The same discipline was applied at 4:8-10 (kept as one span despite containing both narrated action and formal speech) and at 3:6-15 (kept as one span despite an internal night/dawn temporal marker). The two-verse spans that WERE split off as their own decisions (4:11-12; and the single-verse 2:1, 4:7) were each anchored to an independent grammatical marker — an explicit-subject speaker change plus catchword-link for 4:11-12, a disjunctive circumstantial clause for 2:1 and 4:7 — rather than to topical intuition alone.

## sidecar_specificity_plan

Each decision's literature_type_guess was written to be specific to its own span rather than a single genre tag applied uniformly: "narrator aside / character introduction," "narrator aside / etiological gloss," "narrative dialogue (favor/blessing exchange)," "narrative dialogue (instruction speech)," "narrative dialogue (report scene)," "genealogical register (toledot list)," etc. This is intended to give any downstream sidecar or atlas consumer real differentiation between spans that are superficially all "Ruth narrative" but function differently (background exposition vs. direct dialogue vs. legal-procedure formula vs. formal list).

## chapter_only_fallback_reason_if_used

Not used anywhere in this map. No decision equals a full chapter; the largest single span (3:6-15, ten verses) still covers only 10 of chapter 3's 18 verses. Ruth's text carries strong enough sub-chapter signals throughout (scene shifts, inclusios, an aside, a genre-heading) that the chapter-only fallback was never needed.

## expected_low_confidence_regions

Two decisions are priced medium_low: 2:1 (the Boaz character-introduction, a single disjunctive-clause verse) and 4:11-12 (the people's blessing-response, linked to what precedes mainly by catchword repetition rather than a harder scene marker). Both carry a real, identifiable text signal but are thin spans (one or two verses) where "both edges independently strong" is a harder bar to clear honestly. More broadly, because this book has essentially no parashah-marker safety net (one pe in 85 verses, zero samekh), every seam in this map — including the five rated high — rests entirely on text-internal literary-critical judgment; the confidence ratings reflect that honestly rather than borrowing false certainty from marker corroboration that does not exist for all but one seam (4:17/18).

## frontier_or_atlas_candidate_expectations

The two disjunctive-clause narrator asides (2:1, 4:7) and the toledot genre-heading (4:18-22) are the strongest candidates for cross-book atlas comparison: these are recognizable, portable Biblical Hebrew narrative-prose conventions (off-storyline circumstantial clauses; tôlědôt-formula headings) that should recur, and be independently checkable, in other narrative books of the corpus. The חן inclusio (2:8-13) and the מי את echo (3:9/3:16) are more book-internal Leitwort patterns specific to Ruth's own compact, symmetrical design and are flagged as candidates for a Ruth-specific literary-device index rather than a general cross-book frontier signal.

## post_adjudication_outcome

Final map: 19 decisions, exact 85/85 coverage, zero chapter-shaped rows, zero retirements, zero
splits or merges - the only book so far whose drafted layout survived adjudication span-intact.
Confidence 4 high / 13 medium / 2 medium_low (one demotion: 008 high->medium after the chen-figure
misdescription); all 19 accepted_candidate, zero held, zero appeals, zero ultra requests. The
frontier queue stayed empty.

Mesh: one OL (opus) + one LF (sonnet) blind primary over all 19 (LF 18/1, OL 12/7; one blind
convergence - the reversed witnesses-formula citation at 4:9, whose correction strengthened the
row into a true speech-initial/speech-final inclusio); one peer supported all 8 challenges; author
round accepted all with no span moves; 11 rows revised at rationale/citation level. Total ruled: 8.

Signature outcomes: the TURN-MARKER principle (named-speaker formulas mark turns, not unit resets,
in dialogue-dense narrative - 2:20 doubles the formula inside one exchange; REL-001); the
DISJUNCTIVE-CLAUSE differentiator (seams only with a new participant ahead of its scene and/or a
narrator-time deictic - one principle now governs 1:2, 2:1, 4:7; REL-002); the toledot coda held
as one register row under the content-vs-tag criterion (REL-003). Ruth is near-marker-silent (one
pe, zero samekh, both witnesses agreeing) - every seam in the book rests on text signals alone,
making it the campaign's cleanest test of the no-marker discipline.
