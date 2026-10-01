## selected_strategy

Text-signal-only literary chunking of Judges into 174 candidate units (M8-Judg-001 through M8-Judg-174), tiling Judg.1.1-Judg.21.25 exactly against the 618-verse OSHB/WEB crosswalk. Boundaries are driven exclusively by speech/messenger formulas, the cyclical framework formulas (sin/servitude/cry/deliverance/rest), scene and participant changes, inclusio and refrain instances, discourse-frame shifts, type-scenes, list/register formulas, and etiological or naming closures. Chapter divisions, verse numbers, and WEB paragraph marks were consulted only as navigation aids, never as evidence; several units cross chapter lines where the text itself runs on (e.g. the double introduction 2:6-3:6 is segmented independent of the 2/3 chapter break, and 20:18 is isolated as its own decision despite falling mid-chapter because it echoes 1:1-2). The cyclical-framework treatment (sin-formula opens, rest/death/tenure-closing formula closes each major-judge unit) is applied identically across Othniel, Ehud, Deborah/Barak, Gideon, Jephthah, and Samson, with the paradigm case (Othniel, 3:7-11) collapsing to a single span because no separable narrative intervenes between its formula clauses.

## literature_type_or_mixed_genre

Mixed genre, deliberately so: prose narrative cycles (deliverer stories), an embedded epic victory song (ch5), an embedded fable with interpretation (9:8-20), formulaic registers (minor-judges notices, tribal-failure lists, troop-census pairings), etiological/naming notices threaded throughout, and two appendix narratives (Micah/Danite migration; Gibeah outrage/civil war) that abandon the cyclical framework entirely in favor of a refrain-based structuring device. No single literary label covers the book; the segmentation follows genre wherever the genre itself changes (e.g. 5:1's poem/prose seam, 9:8-15's parable form, the minor-judges register's discrete closure formula).

## literary_form_decision_matrix

- Cyclical-framework narrative (Othniel through Samson, 3:7-16:31): sin-formula opens; narrative content segmented by scene/speech signals; rest/death/tenure-closing formula closes, as its own decision when narrative separates it from the opening formula.
- Minor-judges register (10:1-5, 12:8-15): register-closure criterion — each entry stands alone because each carries both a content differentiator and a discrete death-and-burial closure (Josh REL-001 precedent).
- Uniform-content lists with no per-entry closure (1:27-36 tribal-failure register; 20:14-17 troop-count pairing): stay whole.
- Embedded poetry (ch5 Song; 9:8-15 fable; riddle/taunt couplets in ch14-15): bounded by the poem/prose lineation seam in the source markup, a genuine text signal distinct from paragraph metadata.
- Refrain-structured appendices (17-21): short-form refrain (17-1 clause, "no king in Israel") opens a unit when grammatically fused with a new subject's first clause (18:1, 19:1); full-form refrain (2-clause, adding "everyone did right in his own eyes") closes/comments (17:6, 21:25), forming a deliberate 17:6/21:25 inclusio.
- Diplomatic/legal speech (Jephthah's brief, 11:14-27): kept as one span per uninterrupted quotation, since forensic argument has no internal speech-formula reset.
- Type-scenes (Achsah's request, spy narratives, hospitality-then-atrocity at Gibeah, Delilah's three-round deception): bounded by explicit-subject-reset-plus-content-shift (Josh REL-003 precedent); doubled/tripled type-scenes with genuine content differentiation (Delilah's three materials) are kept separate, while type-scenes that are pure formulaic repetition with no content differentiation (19:4-9's daily hospitality delay) are kept whole, per the register-closure criterion applied to prose rather than lists.

## substrate_markers_considered

USFM paragraph (¶) and poetry-lineation (q1/q2/b) markers from the WEB source were read as navigational hints only — never cited as evidence in any boundary_rationale. Where a q1/q2 lineation shift coincides with a genuine text signal (e.g. 5:1's superscription vs. 5:2's poetic opening; 5:31's poem-to-prose shift into the rest-formula; 14:12-14's riddle couplet), the underlying form change itself (poem/prose transition, one of the campaign's licensed signal types) is cited, not the markup tag. Footnote markers (f/fr/ft) were not used as evidence anywhere.

## strongs_metadata_considered_evidence_only

No Strong's numbers, lemma data, or morphological tagging exist in the supplied substrate files (Judg_oshb.txt is plain consonantal-vocalized Hebrew text; Judg_web_clean.txt carries no Strong's tags), and none was used as evidence for any decision. All Hebrew citations in boundary_evidence_refs are verbatim quotations from Judg_oshb.txt, quoted character-for-character. Judges' OSHB text carries numerous ketiv/qere pairs printed adjacently (e.g. Judg.1.27, 4.11, 6.5, 7.13, 9.8, 13.17, 16.21, 16.25, 19.3, 19.25, 21.20); none of these specific words happened to fall within the excerpted spans quoted in this draft's boundary_evidence_refs, so no ketiv/qere annotation was required, but the convention (quote as printed, annotate if excerpted) is noted here for any downstream reviewer who pulls a fuller quotation from those verses.

## source_metadata_evidence_only_check

verse_inventory.json, chapter_profile.json, web_mt_crosswalk.json, web_mt_verse_check.json, book_observation.jsonl, risk_signals.jsonl, and span_features.jsonl were used exclusively for coverage bookkeeping (verse counts per chapter, confirming WEB/MT identity so no dual-reference citation is required) and were never cited as literary evidence. The web_mt_crosswalk confirms Judg.1.1-21.25 is identical between WEB versification and MT, so no boundary needed dual WEB+MT verse-reference handling for non-identical segments.

## larger_unit_preservation_check

Major-judge cycles (Othniel, Ehud, Deborah/Barak, Gideon, Jephthah, Samson) are preserved as coherent multi-decision complexes bounded by their own opening and closing framework formulas, not fragmented past the point the text itself marks internal scene/speech breaks. The Abimelech complex (9:1-57, sixteen decisions) is treated as one coherent narrative arc from proposal through theological verdict, with Jotham's fable-plus-interpretation kept as two decisions (not further split) because both are single uninterrupted discourse units. The appendices (17-21) are preserved as two coherent complexes (Micah/Danite migration, 17:1-18:31; Gibeah outrage/civil war/resolution, 19:1-21:25) bracketed by the refrain, not treated as an undifferentiated tail.

## list_register_function_check

Two register types were tested against the register-closure criterion and treated oppositely on principled grounds: (a) the minor-judges register (10:1-5, 12:8-15) has per-entry death-and-burial closures plus content differentiators, so each entry stands alone (5 separate decisions); (b) the tribal-dispossession-failure register (1:27-36) and the Israel/Benjamin troop-count pairing (20:14-17) share a uniform formula with no per-entry closure device, so each stays whole (1 decision each). Delilah's three-round deception (16:6-14) was treated as three separate decisions because each round supplies both an explicit-subject-reset ("Delilah said to Samson") and a content-differentiator (different binding material), matching the Josh REL-003 precedent rather than the uniform-register precedent.

## epistle_unit_check_if_applicable

n/a — Judges contains no epistolary material.

## over_split_risk_check

Two rebalancing passes were applied after an initial draft. First, several Ehud/Gideon/ch9 sub-scenes originally planned as separate decisions were merged where a genuine Wiederaufnahme or tight causal chain argued against a split (e.g. Ehud's discovery-and-escape, 3:24-27, merged on the explicit "while they waited" resumptive marker rather than split at the servant/Ehud subject change; Gideon's kingship-refusal-plus-ephod-request, 8:22-27, merged because both are one continuous address introduced twice with "Gideon said to them"). Second, a confidence audit (below) downgraded 31 of an initial 60 "high" ratings to "medium" after recognizing that scene-narrowing or narrative-flow judgments alone, without an explicit formulaic/generic marker on both edges, do not meet this campaign's HIGH bar — the same discipline the Joshua draft required after its own re-pricing pass. Final density is 174 decisions across 618 verses (~3.6 verses/decision), toward the upper-middle of the "expect roughly 120-180" guidance, reflecting Judges' unusually dialogue-dense and scene-shifting narrative texture (Ehud, Gideon, Abimelech, Samson, and the Gibeah complex all carry many short but genuinely bounded beats) rather than mechanical over-splitting.

## sidecar_specificity_plan

Each decision's literature_type_guess is scene- or form-specific (e.g. "dowry-request type-scene," "diplomatic correspondence, historical-legal brief," "embedded fable," "burial notice and cycle tenure-closure") rather than a book-level label, so downstream sidecar/atlas tooling can key genre-sensitive treatment (poetry rendering, register/list handling, formula-family tagging) directly off individual decisions without re-deriving genre from context.

## chapter_only_fallback_reason_if_used

Not used. No decision anywhere in this draft equals a full, unmodified chapter span; every span boundary is independently text-driven, including cases (e.g. 12:7, 15:20, 20:18) that are single verses precisely because the surrounding formula material required finer resolution than chapter or even paragraph boundaries would supply.

## expected_low_confidence_regions

The thinnest seams in this draft are single-verse asides with no speech-formula on either edge: Judg.4.11 (Heber the Kenite proleptic aside — the campaign's one "low"-confidence decision, M8-Judg-026), Judg.18.7 (Laish reconnaissance description) and Judg.9.22 (Abimelech's bare tenure notice, both "medium_low"), and Judg.1.16-20 (a loosely bound settlement/conquest register with no internal speech-formula seams, "medium_low"). More broadly, the ch1 tribal-conquest material (1:9-20) and the Abimelech military-tactical beats (9:34-41, 9:42-49) sit at "medium" because their boundaries rest on scene/participant judgment rather than hard formulaic markers, even though no plausible competing boundary was identified.

## frontier_or_atlas_candidate_expectations

Strong candidates for downstream frontier/atlas flagging: the Deborah prose/poem seam and 5:31's disclosed poem-to-framework graft (M8-Judg-039); the Samson doubled colophon (M8-Judg-122, M8-Judg-134); the Gideon-to-Abimelech transition's missing sin-formula (M8-Judg-065); the appendix refrain's four-site opening/closing treatment (M8-Judg-136, M8-Judg-138, M8-Judg-148, M8-Judg-174); and the two book-spanning inclusios (1:1-2 echoed at 20:18, M8-Judg-160; 17:6 echoed at 21:25, M8-Judg-174) — all are named, disclosed anomalies rather than smoothed-over judgment calls, and are the book's most contestable calls a reviewing agent should re-examine first.

## post_adjudication_outcome

Final map: 173 active decisions (174 frozen, 3 retired by merge - 144 into 143, 167 into 166, 176
into 092 - and 2 created by split: 175 ephod episode, 176 later re-absorbed), exact 618/618
coverage, zero chapter-shaped rows. Confidence 31 high / 134 medium / 7 medium_low / 1 low; 172
accepted_candidate + 1 held_lower_confidence (140, insufficient_evidence conceded with corrected
edge attribution). Zero appeals, zero ultra requests, zero human holds; the frontier queue stayed
empty (the 9:7 sub-verse tension and the 11:28 left-edge question both resolved at candidate level).

Round 1: two blind primaries per decision (4 OL opus + 4 LF sonnet), 73 challenge objects + 3
verdict flags over 61 decisions, 12 blind two-side convergences; 4 peers supported effectively all
of it with calibrated refinements (two merges recommended, one split declined, one resumption case
downgraded). Author round: 70 accept-family / 3 peer-aligned disputes; structural moves included
the Song re-cut at 5:2|3, the 8:23|24 ephod split, the 10:10|11 framework seam, and the Jephthah
restructure that the revision round then consolidated into one 11:29-31 vow unit. The two-sided
blind revision pair (46 changed rows) filed 25 more challenges - including four rows whose
conceded round-1 remedies had never landed (caught by diff against v0, now mechanically gated) -
all fixed across micro rounds r2-r4. Total ruled: 106.

Signature findings: the campaign's first FABRICATED marker citation (a pe claimed after 15:17 that
exists in neither witness) caught by the mesh and removed; the cycle-close treatment unified under
one rule (isolate only undiluted rest/tenure notices - REL-001); the no-king refrain system mapped
by form and position with the 17:6/21:25 byte-identity bracketing the appendix (REL-002); the
register criterion sharpened into the content-vs-tag distinction (ch 1 dispossession register whole
vs minor judges split - REL-003); and three resumption-cut seams healed by merges on verbatim
Wiederaufnahme brackets (18:17|18, 20:45|47) or re-cut (21:4|5, the warrant traveling with its
decision). Anti-batch fired on the writer's own ALT-field template across 25 rows (de-templated)
and the postchecker's full-precision scan caught four accent-level citation slips below the
consonantal sweep's tolerance - both nets now standard.
