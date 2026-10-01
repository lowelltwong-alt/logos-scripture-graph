# 2Sam — Book Strategy (M8_fable, candidate-only, non-authorizing)

## selected_strategy

2Sam is chunked on tier-1 text signals alone, with the WLC parashah apparatus (46 petuchah + 96 setumah, single-witness, MT numbering — pmarks_2Sam.json) used strictly as weak corroboration per the m8-mesh-r2 addendum: in the Prophets both pe and samekh sit in the weak-corroboration tier and never drive or lift a boundary. The book divides into three literary macro-blocks that demand different chunking discipline: (1) chs 1–8, episodic royal-accession narrative (rise, civil war, consolidation) built from scene-changes, messenger formulas, and annalistic notices; (2) chs 9–20, the long-form court narrative (Mephibosheth, Ammonite war frame, Bathsheba, Amnon–Absalom, revolt and return), where the prose is continuous and the over-split risk is highest — units follow participant/location shifts and discourse frames, not speech-turns; (3) chs 21–24, the appendix (famine narrative, gibborim registers, two poems, census narrative), where genre-register boundaries are hard and list-internal splitting must be resisted. Poetry is lifted only where a formal superscription or discourse frame marks it (1:17–27 lament with Jashar citation; 22:1–51 psalm with full superscription; 23:1–7 "last words" oracle frame); embedded two-line qinah fragments (3:33–34) stay inside their narrative scene. Boundary drivers throughout: speech/messenger formulas, superscriptions, explicit scene/participant/location change, inclusio/refrain (e.g. "How the mighty have fallen" 1:19/25/27; "went in peace" 3:21–23), discourse frames, and list/register formulas (3:2–5 Hebron sons; 5:13–16; 8:16–18; 20:23–26; 21:15–22; 23:8–39; officer/son lists).

## literature_type_or_mixed_genre

Mixed. Dominant register: narrative prose dense with direct discourse (court dialogue, messenger reports, oracles). Distinct embedded genres, each requiring its own tag rather than a uniform label: qinah lament poetry (1:19–27, plus the 3:33–34 fragment kept in-scene), dynastic oracle (7:4–17) with responding prayer (7:18–29), annalistic war/administration summaries (5:17–25 compressed battle etiologies, 8:1–14 catalogue, 8:15–18 + 20:23–26 officer registers), genealogical/name lists (3:2–5, 5:13–16), thanksgiving psalm (22), prophetic testament oracle (23:1–7), heroic register with narrative vignettes (21:15–22, 23:8–39), and theophanic census narrative closing on altar etiology (24). The Succession-Narrative chapters (11–20) are the longest continuous artistic prose in the book and are treated as high-continuity narrative, not as chapter-shaped blocks.

## literary_form_decision_matrix

| Device type | Where it surfaces (samples) | Effect on chunking |
|---|---|---|
| Temporal/dynastic opening formula (ויהי אחרי...) | 1:1, 2:1, 8:1, 10:1, 13:1, 15:1, 21:18 | Opens a new unit |
| Messenger/speech formula with new addressee | 2:5, 3:12, 3:14, 11:18–25, 12:1, 14:1–3, 19:11 | Opens a new unit |
| Superscription/quotation frame for poetry | 1:17–18 (Jashar), 22:1, 23:1 | Hard genre boundary; frame stays with its poem |
| Explicit scene/participant/location change | 2:12–13, 4:5, 6:1–2, 11:1, 15:13, 17:24 | Opens a new unit |
| Disjunctive-clause participant introduction (off-storyline) | 2:8, 3:6, 4:2–3, 4:4, 9:1–3, 16:1, 20:1 | Marks narrator-background or new-thread unit |
| Inclusio/refrain | 1:19/25/27; 3:21/22/23 "went in peace"; 7:8/16 covenant frame; 22:2–3/47–51 | Confirms/binds unit edges |
| List/register formula | 3:2–5, 5:13–16, 8:16–18, 20:23–26, 21:15–22, 23:8–39, 23:24 ff. | Whole list = one register unit unless the list itself changes formula |
| Regnal/annalistic summary notice | 2:10–11, 5:4–5, 8:15 | Own small unit (annalistic register) |
| Etiological naming close | 2:16 (Helkath Hazzurim), 5:20 (Baal Perazim), 6:8 (Perez Uzzah) | Closes (never opens) its unit |
| Turn-marker inside one dialogue (named-speaker resets) | 1:3–10 Q&A; 2:1 fourfold inquiry exchange; 19:41–43 | NOT a boundary (campaign turn-marker principle) |
| Wiederaufnahme/resumptive repetition | 3:6 resumes 3:1; 21:18 resumes 21:15 frame | Continuity signal, NOT a boundary |
| Parashah marks (pe/samekh, WLC single-witness) | 141 marked verses | Weak corroboration only; never driver; disclose "(single-witness)" |

## substrate_markers_considered

chapter_profile.json (24 chapter rollups) and span_features.jsonl reviewed. Poetry/liturgy markers (q1/q2) concentrate exactly where the genre map predicts: ch 1 (11 q1 / 18 q2 — the lament), ch 22 (the psalm), ch 23 (last-words oracle). risk_signals.jsonl carries 80 signals, dominated by has_footnote; every footnote inspected so far annotates translation choices (hinneh, Yahweh, Elohim, place-name glosses) — WEB-editorial metadata, never boundary evidence. The heavy samekh run inside 23:8–39 tracks the gibborim list's internal name-entries, which is precisely the case where marker-following would shred a register that functions as one cumulative unit; the addendum's weak-corroboration tier plus the list-register rule keeps the roster whole.

## strongs_metadata_considered_evidence_only

book_observation.jsonl reports strong_h tagging density (w count 24k+ across the book, wh sparse) uniform across chapters; no sparsely-tagged stretch suggesting a seam. No decision cites Strong's density as evidence.

## source_metadata_evidence_only_check

web_mt_crosswalk.json (status: verified): WEB 1:1–18:32 and 20:1–24:25 verse-identical with MT; WEB 18:33–19:43 = MT 19:1–19:44. Canonical passages inventory (freeze tiling target) uses WEB numbering (ch18 ends 18.33, ch19 ends 19.43; 695 total). Consequence: every oshb: citation inside WEB 18:33–19:43 must dual-cite (e.g. "web:2Sam.18.33 = oshb:2Sam.19.1 (MT)"). All parashah citations are additionally tagged "(single-witness)" since only WLC witnesses them in this substrate.

## larger_unit_preservation_check (planned tests)

Known temptation points where a finer split will be considered and, absent independent tier-1 markers on both edges, rejected with documentation: the fourfold inquiry exchange at 2:1 (four speech-turns, one oracle consultation); Abner's death complex 3:26–39 (murder, curse, funeral, fast — split only at hearing-formula and scene edges); the Bathsheba unit 11:2–5 (one continuous transgression scene); Nathan's parable + verdict 12:1–15 (parable, application, and sentence form one prophetic audience); the Absalom-death battle report chain 18:19–33 (two-runner suspense structure is one narrative arc with internal turn-markers); the gibborim roster 23:8–39 (samekh after nearly every name; one register).

## list_register_function_check

Seven list/register structures identified in advance: 3:2–5 (Hebron sons), 5:13–16 (Jerusalem sons), 8:16–18 (officers), 20:23–26 (officers, second recension), 21:15–22 (four Philistine-giant vignettes — formulaic "there was again war" chain, treated as one register of vignettes), 23:8–39 (gibborim roster with narrative insets), plus the 24:5–8 census itinerary (kept inside its narrative unit as an embedded route list). Each list is one decision unless its own formula visibly changes register mid-stream (23:8–23 exploits-prose vs 23:24–39 bare name-chain is the one candidate internal seam, to be argued on the formula change, not on the samekh chain).

## epistle_unit_check_if_applicable

n/a — Hebrew narrative; the two embedded letters (11:15 Uriah letter; the exchange in 11:18–25) are discourse-framed quotations inside their scenes, not epistolary macro-structure.

## over_split_risk_check

Highest-risk material: (1) dialogue-dense scenes where named-speaker formulas repeat (turn-marker principle applies — 1:3–16, 13:24–27, 19:41–43); (2) the revolt narrative's rapid scene-relay (15:13–16:14 David's flight is a procession of short encounters, each opened by a genuine participant-arrival formula — these ARE units, but their edges must be argued from the arrival/departure formulas, not from intuition); (3) chapter seams that are not literary seams (10:1–11:1 Ammonite war frame brackets the Bathsheba story; 21:1–14 famine narrative is one arc across internal samekh marks). Conversely under-split risk: ch 8's catalogue must not absorb 8:15–18 (register change); ch 24's census/plague/altar sequence has three genuine movements.

## sidecar_specificity_plan

literature_type_guess written span-specific (e.g. "qinah_lament_with_superscription", "dynastic_oracle", "royal_thanksgiving_psalm", "heroic_register_with_narrative_insets", "annalistic_war_catalogue", "narrative_dialogue (audience scene)"), not uniform "narrative_prose". Narrator parentheses (4:4 Mephibosheth; 4:2b–3 Beerothites) tagged as narrator asides per the Ruth/1Sam disjunctive-clause standard.

## chapter_only_fallback_reason_if_used

Not planned. Ch 22 (51 vv) is a single psalm and will be one decision spanning the whole chapter WITH literary warrant (superscription 22:1 + closing doxology 22:51) — that is a genre unit that happens to be chapter-shaped, documented as such, not a fallback.

## expected_low_confidence_regions

(1) 8:1–14 war catalogue internal seams (annalistic compression, few discourse frames); (2) the 5:6–10 Jebus conquest with its crux verses (5:8 lame-and-blind saying); (3) 19:9–15 (MT 19:10–16) restoration negotiations — rapid addressee shifts with offset numbering; (4) 23:8–39 internal structure (exploits vs name-chain seam); (5) seams inside 16:15–17:23 (Ahithophel/Hushai counsel cycle — long continuous court debate; internal units rest on audience-change formulas of medium strength). These are the candidate low_confidence_register / frontier-queue entries.

## frontier_or_atlas_candidate_expectations

Portable cross-book conventions expected to feed the atlas: (a) the "ויהי אחרי־כן" episode-opening chain (shared with Judg/1Sam); (b) etiological naming closes (Helkath Hazzurim, Baal Perazim, Perez Uzzah — same device as Judg); (c) the officer-register duplicate frame (8:16–18 ‖ 20:23–26 — an inclusio bracketing the court narrative, a candidate cross-reference relation); (d) regnal summary formula (2:10–11, 5:4–5) shared with Kings; (e) the two-runner report scene (18:19–32) as a paradigm messenger-relay structure. Book-internal Leitwort candidates (shalom in ch 3; "eat bread at the king's table" in ch 9; sword-devours motif 2:26/11:25/18:8) flagged for a 2Sam-specific index rather than the cross-book frontier feed.

## post_adjudication_outcome

Final map: 147 decisions, exact 695/695 coverage, zero retirements, zero span changes -
the drafted layout survived adjudication span-intact (second book after Ruth to do so).
Confidence 78 high / 68 medium / 1 medium_low; all 147 accepted_candidate, zero held,
zero appeals, zero ultra requests. The single medium_low is M8-2Sam-137 (the ch-22
psalm): a boss protocol amendment, not an evidence deficit - the span coincides with a
marker-rich chapter rollup and the T423 chapter_only_fallback rule caps such units
outside the Psalter and routes them to the low-confidence register and frontier
escalation queue for convergence-time review. That policy question (Psalter-only
exemption vs. superscribed whole-psalm units elsewhere) is flagged for the owner before
the Psalms cycle.

Mesh: one LF (sonnet) + one OL (opus) blind primary over all 147 (LF 134 supports /
13 challenge-rows; OL 114 / 33 rows, 37 items; blind convergences on the fabricated
Pas Dammim import at 23:9, the six-not-seven territory count at 2:9, and the
wayyiqtol-mislabeled-as-disjunctive class). Peer supported 49 of 50 challenges and
rejected one (LF's "first designation as wife" objection - MT 12:15 still reads
'eshet Uriyyah after the 11:27 marriage notice, vindicating the row). Author round:
48 accept / 1 partial / 1 dispute across two halves; revision round on the 38-row
material set drew 10 further challenges (2 medium: an invented waw at 13:36, the
officer-formula mischaracterization at 20:23-26), all rev-peer-verified and adopted.
Total ruled: 60. One deterministic micro-edit round (r3) fixed an unmarked quote
elision; postcheck passed 147/147 with six low cosmetic defect classes left as
recorded per 1Sam precedent.

Signature outcomes: the WAYYIQTOL/DISJUNCTIVE standard (REL-001; the book's own
13:34-vs-13:37/38 contrast is the test - narrative-chain verbs may never be sold as
fronting); the WITNESS-FIDELITY rule (REL-002; cite what the quoted witness prints,
disclose WEB/MT divergences such as Merab/Michal at 21:8 and "Goliath's brother" at
21:19, never import from Chronicles); the OFFSET CITATION convention (REL-003; inside
WEB 18:33-19:43 = MT 19:1-19:44 every verse number is qualified and the +1 rule
declared in-row, M8-2Sam-116 the model); the INCLUSIO-SCOPE standard (REL-004; both
members in-span or relabel); the OFFICER-REGISTER bracket (REL-005; 8:15-18 and
20:23-26 as the court narrative's frame, kohen rendered uniformly); and the
CONFIDENCE EDGE TEST (REL-006; 033 down, 029 held). Anti-batch hardening: the
deterministic 7-gram gate surfaced formulaic disclosure boilerplate in row and review
prose; all of it was reworded content-preservingly (peer by its own hand; the
spend-limit-interrupted primaries via disclosed orchestrator reword-only
normalization, prose_normalized tags in-file) until the gate ran clean at 0 errors.
