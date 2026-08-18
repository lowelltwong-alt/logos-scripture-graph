# 1Chr book strategy (M8_fable, fable-orchestrator-authored) — 2026-08-04

Non-authorizing planning artifact. Binding inputs: m8-mesh-r2 contract (Writings:
pe AND samekh tier-3 weak, never driver, "(single-witness)" on every cite, absence
never evidence, chapter/verse/modern ¶ tier-4 metadata only), owner scribal-weights
addendum, campaign lessons (SP/1Chr/freeze/CYCLE_STATE.md).

## 1. What kind of book this is

1 Chronicles is REGISTER-DOMINANT LITERATURE with an embedded narrative spine:
chs 1-9 are a genealogical prologue (Adam → the tribes → Jerusalem's restored
community), ch 10 a hinge (Saul's death), chs 11-29 a David narrative whose center
of gravity is cultic (ark, dynastic oracle, temple site, temple personnel,
succession), not military-political. Two literary consequences drive everything:

(a) The dominant boundary devices are LIST devices — register heads, summary
closures, settlement notices, muster totals, lot-casting sequences, course
rotations — not the regnal frames of Kings.
(b) Registers contain NARRATIVE INSETS (Jabez 4:9-10; Hagrite war 5:18-22;
Ephraim's bereavement 7:21b-23) and the narrative contains REGISTER INSETS
(mighty-men catalogue 11:10-47; Ziklag/Hebron musters ch 12; personnel rosters
23-27). The unit question is almost always "does the inset stay inside the host
unit?" — default: an inset framed by and syntactically resumed within its host
register/narrative stays inside (larger-unit preservation); split only at a
genuine tier-1 seam.

## 2. Device matrix (tier-1 text signals expected to drive boundaries)

- Register-head formula: "The sons of X" / "Of the sons of X" (בְּנֵי X, וּבְנֵי X,
  לִבְנֵי X) opening a new lineage block (2:1; 4:1; 4:24; 6:16; 7:1...).
- Summary/closure formula: "These are the..." (אֵלֶּה) closing or opening a register
  (1:54 chiefs of Edom; 6:31 "these are they whom David set"; 11:10; 12:23 "these
  are the numbers"), incl. toledot-type closures.
- Scene/participant/location change with wayyiqtol gathering verbs: 11:1 ויקבצו;
  13:1 David consults; 15:1 houses/tent; 28:1 ויקהל assembly.
- Speech and prayer frames: Nathan-oracle frame ch 17 (17:1 setting; 17:3 word of
  God comes; 17:16 "David the king went in and sat"); David's charges (22:6-16;
  28:2 "Then David the king stood up and said"); the great blessing 29:10-19;
  liturgical medley frame 16:7 (ordination of thanks) / 16:36b (people's amen).
- Campaign-report openers: "After this" (ויהי אחרי כן) 18:1; 19:1; 20:4; annual-
  campaign frame 20:1 "at the time of the return of the year".
- Census/muster formulas: "their number" (מספרם), "able to bear buckler and sword"
  5:18; 21:5 census totals; 23:3-5 Levite count.
- Lot-casting and division formulas: 24:1 "these were the divisions"; 24:5/25:8/26:13
  ויפילו גורלות; 26:1 "For the divisions of the doorkeepers".
- Course-rotation formula ch 27: "of the first course for the first month ...
  in his course were 24,000" — a 12-fold refrain (inclusio-type cycle).
- Settlement formulas: "lived in" (וישבו) + place registers (6:54 "these are their
  dwelling places"; 9:2-3).
- Exile/return notices as register closures: 5:25-26; 6:15 (MT 5:41); 9:1b.
- Source-citation colophon + regnal summary: 29:26-30 (history of Samuel/Nathan/Gad).
- IN-BOOK resumption (Wiederaufnahme): 9:35-44 re-runs 8:29-38 (Jeiel of Gibeon →
  Saul) to relaunch the Saul narrative of ch 10 — internal evidence, arguable.

## 3. Marker policy (m8-mesh-r2, Writings)

72 PE + 188 SAMEKH (WLC single-witness, MT numbering; pmarks_1Chr.json). In the
Writings BOTH are parashah-class tier-3 WEAK corroboration — never a driver, never
counterevidence by absence. TEN verses carry DOUBLE SAMEKH (1.34, 1.41, 5.29,
11.32, 11.44, 23.6, 27.16, 27.21, 27.25, 27.28) — WLC intra-list division practice
inside registers; any cite of a doubled verse must disclose the doubling. Every mark
cite carries "(single-witness)". The dense samekh field in chs 1-9 and 23-27 mostly
tracks LIST-ITEM granularity finer than our rows — do not let samekh density pull
row granularity down; the register unit is the row.

## 4. Witness/citation policy

WEB 942 vv / MT 943 vv, three offset chapters (crosswalk + seam content verified,
Phase 0):
- WEB 6:1-15 = MT 5:27-41; WEB 6:16-81 = MT 6:1-66. Anchor: WEB 6:1/MT 5:27 spells
  GershoN (גרשון), WEB 6:16/MT 6:1 GershoM (גרשם).
- WEB 12:4 = MT 12:4+12:5; WEB 12:5-40 = MT 12:6-41.
- DUAL-CITE every original-language ref inside WEB ch 6 ("web:1Chr.6.16 =
  oshb:1Chr.6.1 (MT)" style) and WEB 12:4-40. Comparanda refs into these zones
  dual-cite too (2Kgs r3 lesson), in EVERY round including micro-rounds.
- Hebrew is sliced programmatically from 1Chr_oshb.txt (never hand-typed);
  orchestrator runs normalize_hebrew_in_json.py over every agent JSON.
- Translator glosses marked as glosses, never presented as WEB text; argued
  comparanda mirrored into boundary_evidence_refs (2Kgs postcheck lesson).
- Chronicles-specific hygiene: name-form variants between witnesses are COMMON
  (Diphath/Riphath 1:6, Jozacar-class variants, Gershon/Gershom). Quote the witness
  actually cited; never harmonize names across witnesses in a quote.

## 5. Synoptic discipline (binding)

Sam-Kgs parallels (10 = 1Sam 31; 11:1-9 = 2Sam 5:1-10; 13 = 2Sam 6:1-11;
15:25-16:3 = 2Sam 6:12-19a; 17 = 2Sam 7; 18 = 2Sam 8; 19 = 2Sam 10; 20:1-3 =
2Sam 11:1+12:26-31; 20:4-8 = 2Sam 21:18-22; 21 = 2Sam 24; 11:10-41a = 2Sam
23:8-39) and Psalter parallels (16:8-22 ≈ Ps 105:1-15; 16:23-33 ≈ Ps 96;
16:34-36 ≈ Ps 106:1,47-48) are CROSS-BOOK METADATA ONLY: record as typed
decision_relations (non_authorizing), never as boundary evidence in either
direction. 1Chr's seams are argued from 1Chr's own text. The Chronicler's
OMISSIONS (no Bathsheba, no Absalom) are background, never a boundary argument.
The ONLY arguable parallel is the IN-BOOK resumption 8:29-38 ≈ 9:35-44.

## 6. Block map with larger-unit tests

Genealogical prologue (1-9):
- 1:1-54 universal register: linear Adam-Noah (1-4), table of nations (5-23),
  linear Shem-Abram (24-27), Abraham's sons (28-34a), Esau/Seir (34b-42),
  Edomite kings (43-51a), Edomite chiefs (51b-54). Test: do linear-chain vs
  segmented-table transitions rise to row seams? (1:24 asyndetic linear restart —
  yes; smaller sub-lists — argue case by case.)
- 2:1-2 all-Israel head; 2:3-4:23 JUDAH complex (2:3-55 Hezron/Caleb/Jerahmeel
  cycles; 3:1-24 David's house: Hebron sons, Jerusalem sons, kings, post-exilic
  line; 4:1-23 supplementary Judahite registers + Jabez inset 4:9-10 STAYS INSIDE
  its register run unless a primary shows a tier-1 frame). Test: 2:42/2:50b
  Caleb re-heads; 3:10 linear king-chain start.
- 4:24-43 Simeon (with settlement + Hezekiah-era raid notice 39-43 as register
  coda). 5:1-26 Transjordan: Reuben (1-10), Gad (11-17), Hagrite war inset
  (18-22), half-Manasseh + exile closure (23-26).
- WEB ch 6 LEVI: high-priestly line (6:1-15 = MT 5:27-41, closing at the exile),
  Levite lines (16-30), temple singers (31-48), Aaronic priests (49-53),
  settlements (54-81). All rows dual-cite.
- 7:1-40 six-tribe roster (Issachar, Benjamin-military, Naphtali one-verse,
  Manasseh, Ephraim + bereavement inset 21b-23 + Beth-horon building notice,
  Asher). Test: keep 7:12 (Ir/Aher fragment) and 7:13 Naphtali inside adjacent
  register rows or argue the fragment separately — expect low confidence.
- 8:1-40 Benjamin→Saul's house (Gibeon segment 29-38, archers coda 39-40).
- 9:1 summary hinge + exile notice; 9:2-34 restored Jerusalem (laity, priests,
  Levites, GATEKEEPERS 17-27 with duties 28-34); 9:35-44 Saul-line resumption
  (Wiederaufnahme toward ch 10).

Narrative spine (10-29):
- 10:1-14 Saul's death + Chronicler's verdict (13-14 evaluative close).
- 11:1-9 anointing + Jerusalem; 11:10-47 mighty-men register (the Three 11-19
  with water-libation narrative inset STAYING INSIDE; Abishai/Benaiah 20-25;
  the roster 26-47). 12:1-22 Ziklag/stronghold accessions (Benjaminite archers,
  Gadites, Judah-Benjamin band, Manassites); 12:23-40 Hebron muster + feast
  (38-40 celebratory close). Dual-cite zone from WEB 12:4.
- 13:1-14 first ark move (Uzza; ark to Obed-Edom); 14:1-17 Hiram, family,
  two Philistine victories (interlude proving blessing).
- 15:1-16:43 ark success complex: preparations 15:1-24 (Levite/singer rosters
  INSIDE the narrative), procession 15:25-29 (Michal notice 29 stays inside),
  installation + distribution 16:1-3, ministry appointment 16:4-6(7), MEDLEY
  16:8-36 (internal movements at 16:23 "Sing to Yahweh, all the earth" and the
  16:34-36 thanksgiving/doxology join argued from the 1Chr text; 16:36b people's
  response closes the frame), standing arrangements 16:37-42, dismissal 16:43.
- 17:1-27 dynastic oracle (setting 1-2, oracle 3-15, prayer 16-27).
- 18-20 wars: 18:1-13 campaign catalogue + 18:14-17 cabinet list; 19:1-19 Ammon/
  Aram war (two-front battle); 20:1-3 Rabbah, 20:4-8 giant-slayer notices.
- 21:1-30 census/plague/threshing floor + 22:1 site declaration ("This is the
  house") — 22:1 is the arc's punchline; test whether it closes the ch-21 unit
  (likely) vs opens temple-prep (the 21:28-22:1 join is an expected dispute).
- 22:2-19 preparations + charge to Solomon + charge to princes.
- 23:1-2 succession/assembly head; 23:3-32 Levites (count 3-5, three-clan
  courses 6-23, duties reprise 24-32); 24:1-19 priestly lots; 24:20-31 remaining
  Levites' lots; 25:1-7 singer families, 25:8-31 the 24 singer lots (the lot
  sequence is ONE formulaic unit — resist verse-level splitting); 26:1-11
  gatekeeper families, 26:12-19 gate assignments by lot, 26:20-28 treasuries,
  26:29-32 outward duties; 27:1-15 twelve military courses (12-fold refrain =
  one register unit), 27:16-24 tribal officers (+ census aside 23-24 stays
  inside), 27:25-31 royal stewards, 27:32-34 counselors.
- 28:1-21 assembly + charge + temple pattern (תבנית) handover; 29:1-9 freewill
  offerings; 29:10-19 David's blessing-prayer; 29:20-25 worship + Solomon
  enthroned; 29:26-30 Davidic conclusion + source colophon.

## 7. Expected low-confidence regions (disclose to primaries)

1. ch 1 sub-register joins (esp. 1:34b Esau head after double-samekh 1.34;
   1:43 kings head; 1:51b chiefs transition mid-verse — mid-verse = hold-style
   care, do not split mid-verse).
2. 2:42-55 Caleb cycles + 2:55 Kenite scribes coda.
3. 4:9-10 Jabez inset (inset-vs-row).
4. 5:18-22 war inset boundaries.
5. WEB 6:31/6:49/6:54 internal Levi seams (inside dual-cite zone).
6. 7:12-13 register fragments (Ir/Aher; Naphtali single verse).
7. 9:1-3 hinge; 9:28-34 duties tail vs 9:35 resumption.
8. 11:20-25 (between the Three and the roster); 12:1-22 group joins.
9. 15:16-24 roster inside narrative (row-vs-inset).
10. 16:8-36 medley internal movements (argue strictly from 1Chr wording).
11. 21:28-22:1 join (site declaration attachment).
12. 23:24-32 duties reprise (its relation to 23:6-23 courses).
13. 24:20-31 second Levite list (relation to ch 23 list).
14. 27:23-24 census aside.
15. 29:21-25 enthronement notice (close of assembly vs its own unit).

## 8. Granularity disclosure (to writers AND primaries)

Register-dominant books chunk COARSER than narrative: a whole register/lot
sequence/course rotation is one decision when internally formulaic (e.g., 25:8-31
lots; 27:1-15 courses; 6:54-81 settlements). Narrative chapters run ~5-8 vv/dec
(Samuel-like). Expected total ≈ 115-140 decisions (~7-8 vv/dec overall). Form
drives, not quota: primaries should challenge any span hiding an unargued internal
tier-1 seam, and equally challenge over-splits of formulaic sequences. No
chapter-shaped spans except where the register genuinely IS the chapter — and then
the row caps at medium_low per T423 chapter_only_fallback UNLESS an internal seam
set is argued instead (prefer arguing the internal seams; ch 1 and ch 8 both have
usable internal heads; ch 17 splits at 17:1/3/16; ch 10 at 10:1/8/13 if needed —
target ZERO chapter-shaped rows this book).

## 9. writer_part_plan — 14 parts tiling 942 vv exactly (all seams tier-1 verified)

p01 1:1-1:54    (54) universal register
p02 2:1-3:24    (79) all-Israel head; Judah; David's house      [seam: 2:1 sons-of-Israel head]
p03 4:1-5:26    (69) Judah supplement; Simeon; Transjordan      [seam: 4:1 register head]
p04 6:1-6:81    (81) LEVI — ENTIRE offset zone A, dual-cite     [seam: 6:1 register head = MT 5:27]
p05 7:1-8:40    (80) six tribes; Benjamin→Saul                  [seam: 7:1 register head]
p06 9:1-10:14   (58) Jerusalem community; Saul resumption+death [seam: 9:1 summary hinge]
p07 11:1-12:40  (87) kingship; mighty men — offset zone B whole [seam: 11:1 gathering]
p08 13:1-14:17  (31) first ark move; Hiram/Philistines          [seam: 13:1 consult scene]
p09 15:1-16:43  (72) ark success + medley + arrangements        [seam: 15:1 scene/prep]
p10 17:1-20:8   (71) oracle; prayer; wars                       [seam: 17:1 scene shift]
p11 21:1-22:19  (49) census arc + site + preparations/charges   [seam: 21:1 Satan/census]
p12 23:1-25:31  (94) succession head; Levites; priests; singers [seam: 23:1 old-age/king]
p13 26:1-27:34  (66) gatekeepers; treasuries; courses; officers [seam: 26:1 divisions head]
p14 28:1-29:30  (51) final assembly; prayer; succession; close  [seam: 28:1 assembly]

Provisional ids M8-1Chr-pNN-K; orchestrator renumbers to M8-1Chr-NNN at combine
(combine_parts.py pattern). Writer = sonnet high per part
(attempt ids sonnet_book_writer_1Chr_pNN_r1), routing recorded per part.

## 10. Writer-prompt guards (campaign lessons, enforced)

Vary all disclosure/verification prose (7-gram gate); slice Hebrew from
1Chr_oshb.txt programmatically; dual-cite zones (WEB ch 6; WEB 12:4-40);
"(single-witness)" on all mark cites + disclose double-samekh verses; book-wide
grep any exclusivity/universal claim before asserting it; mirror argued comparanda
into boundary_evidence_refs; mark translator glosses; one-sentence
rejected_alternative; no fabricated ancient context (absent corpus ⇒ gap +
insufficient_evidence); insets stay inside host units absent a tier-1 frame;
never harmonize name variants across witnesses.

## post_adjudication_outcome (2026-08-04)

146 decisions, 942/942 exact coverage, ~6.5 vv/decision (register-dominant book
chunked finer than the regnal books, as the matrix predicted). Full mesh cycle:
38 blind primaries (253 challenges on 118 rows, 8 highs incl. one unrendered
template placeholder caught convergently), 19 peers (253/253 ruled, 7
cross-cutting rulings), six-part author round, boss adjudication (17 ratified
confidence deltas total incl. one rise and one finalize-stage 076 calibration),
30 blind rev reviews (498/506 cures verified; 179-item second-generation docket),
3-part rev peer + micro round, postcheck 146/146 pass 0 holds. ZERO span changes,
ZERO retirements, ZERO appeals end-to-end: every drafted boundary survived; all
amendment was evidential/prose. Confidence final: 76 high / 53 medium /
16 medium_low / 1 low; 17 rows to the sidecar/frontier/atlas registers (largest
of the campaign — the ch.1 sub-registers, offset-zone Levi rows, ch.9 hinge,
fragment rows 046/013, and the 23:6-11 granularity dispute dominate). Verified
book-fact addition: WEB/MT divide 27:30/31 at CLAUSE level despite equal verse
counts. The 8:29-38≈9:35-44 Wiederaufnahme is the book's one sanctioned in-book
parallel (REL-008). Non-authorizing; candidate-only.

# T467 compliance sections (content mirrors §§1-10 above; headings per protocol)

## literary_form_decision_matrix
See §2 (device matrix) and §6 (block map): register-head בני-X formulas, אלה
summaries/toledot, speech/prayer/charge frames, campaign-report openers,
census/muster/lot/course formulas, settlement notices, exile/return closures,
source-citation colophon, in-book Wiederaufnahme — tier-1 drivers per
m8-mesh-r2; applied row-by-row in the 146 final decisions.

## source_metadata_evidence_only_check
Chapter/verse numbers, WEB headings/footnotes/¶ marks: tier-4 metadata only —
never cited as evidence (§3-4). Pe/samekh: tier-3 weak, single-witness-tagged,
double-samekh disclosed (ten verses), never driver, absence never
counterevidence. Verified by citation sweep + postcheck 146/146.

## larger_unit_preservation_check (planned tests)
§6's larger-unit tests executed: Jabez/Hagrite-war/bereavement insets, water-
libation inset (11:11-19), roster-inside-narrative (15:16-24), census aside
(27:23-24), lot cycles kept whole (24:7-19, 25:8-31, 27:1-15). Inset rule (§1)
held except where a tier-1 frame was argued (4:9-10) and survived the mesh.

## list_register_function_check
Registers chunked at register grain (§8): whole lot-sequences and course
rotations as single rows; sub-clan heads rank-subordinated to clan heads
(23:6-11 dispute preserved at medium_low in the frontier queue); samekh density
never pulled granularity down.

## epistle_unit_check_if_applicable
Not applicable: 1 Chronicles contains no epistolary material. The nearest
formulaic analogues (charge speeches 22/28, blessing-prayer 29:10-19) were
handled under speech-frame devices.

## over_split_risk_check
§8's dual guard applied: primaries challenged over-splits of formulaic
sequences (none survived: the 24-lot and 12-course cycles stayed single rows)
and under-splits hiding tier-1 seams (the mesh's 253-item docket tested every
flagged span; zero span changes were needed — amendments were evidential).

## sidecar_specificity_plan
17 low-confidence rows carry full 8-field register entries (see
post_adjudication_outcome): bespoke why_low_confidence, concrete substrate
signals, typed concern (register_granularity_judgment 7 / hinge_ambiguity 5 /
fragment 2 / inset 2 / witness_divergence 1), named reviewer per row
(cross_model_convergence 10 / human_owner 7), downstream risk stated.
