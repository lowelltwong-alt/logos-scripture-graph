# Ps book strategy (M8_fable, m8-mesh-r3) — fable-authored, Phase 1

Status: DRAFT for the writer wave; candidate-only, non-authorizing. Every count
below is byte-swept from SP/Ps staging artifacts (pmarks_Ps.json,
psalm_device_inventory.json, web_mt_offset_map.json — re-runnable via
sweep.py / psalm_devices.py; skeleton tier, maqaf = word separator).
COUNT-OBJECT DISCIPLINE: every count names WHAT it counts; writers re-derive
independently and report errata with bytes (Job's mesh corrected the
orchestrator six times; the pipeline expects and credits errata).

## §1 Objective and shape
2461 WEB verses / 150 psalms; MT 2527 (66 counted-title verses — §3). The
LARGEST book of the marathon and its purest poetry: 2418 of 2461 WEB verses
open poetry lines. There is NO narrative frame — 150 independent liturgical
compositions in a five-book editorial architecture (§5). Chunk at
literary_marker_aware_v2 + T467 overlay quality. OWNER GATE RULINGS
(2026-08-12, all binding): strophe-level rows inside longer psalms;
whole-psalm rows for short indivisible psalms; MANDATORY per-psalm parent
grouping (150 parents) in decision_relations; Ps 119 rows follow its 22
letter-stanzas; titled psalms' OPENING rows carry web:Ps.N.0 =
oshb:Ps.N.1(-2) in refs; two-sentence rejected_alternative allowed ONLY when
the second sentence carries the mandated rival. Expect ~420-520 decisions
(~5-6 vv/row poetry norm; whole-psalm rows for the many short psalms), 34
writer parts (§9), ~48 review clusters of <=8, ~24 scoped peers. ALL waves
slice <=8 rows per attempt id from the start.

## §2 Device matrix (byte-swept; MT refs; WEB aliases via the offset map)

### §2a Superscriptions (the tier-1 opener spine; psalm_device_inventory.json — consume, don't re-derive)
116 WEB titles (Ps 119 has NONE — its 22 [SUPERSCRIPTION] markers are
acrostic stanza headers, WEB spelling KAPF and "SIN AND SHIN"). MT counts 66
of them as verses (58 psalms as v1; 51/52/54/60 as vv1-2); in the other 53
titled psalms the title is the PREFIX of MT v1. Genre labels byte-swept
(membership lists in the inventory) [SEE §11 p22 ERRATUM: shir 30, le-David 73 post-fix]: mizmor 57 psalms, shir 31, maskil 13,
miktam 6 (16, 56-60), tefillah 5, shiggaion 1 (7), lamnatseach 55, le-David
74, le-Asaph 12 (50, 73-83), bene-Qorach 11 (42, 44-49, 84-85, 87-88),
li-Shlomo 2 (72, 127), le-Moshe 1 (90), Heman 1 (88), Ethan 1 (89),
Yeduthun 2 (39, 62; +77 עַל-ידיתון spelling — VERIFY before citing a third),
shir hamma'alot 14 + shir lammaalot 1 (121) = the 15 ascents 120-134.
Superscription = tier-1 opener evidence (owner addendum), and the opening
row of every titled psalm MUST list web:Ps.N.0 = oshb:Ps.N.1 (or .1-.2 for
the four +2 psalms) in boundary_evidence_refs. Historical-note titles
(3, 7, 18, 34, 51, 52, 54, 56, 57, 59, 60, 63, 142) are title material, not
narrative rows.

### §2b Doxology seams + the five-book architecture (§5 details)
Book-boundary doxologies byte-verified: MT 41.14 (= WEB 41.13; baruch +
amen x2), 72.18-19 (baruch x2 + amen x2) with 72.20 the "prayers of David
son of Jesse are ended" COLOPHON (tier-1 colophon class), 89.53 (= WEB
89.52; baruch + amen x2), 106.48 (baruch + amen x1 + hallelu-Yah). These
four seams are the highest-tier macro boundaries in the book. Rows covering
them: unit_type coda (§8).

### §2c Hallelu-Yah / hodu frames
hallelu-Yah (הללו־יה, skeleton הללו יה): verse-initial 11, verse-final 13,
interior 1 — 25 occurrences total; frames psalms 104-106, 111-113, 115-117,
135, 146-150 (open and/or close; membership in the inventory). hodu-le-YHWH
verse-initial: MT 33.2, 105.1, 107.1, 118.1, 118.29, 136.1 — NOTE 107.1 is
spelled DEFECTIVELY (הדו, no waw): sweep BOTH spellings for any hodu claim.
Frame presence/absence at psalm edges is tier-1 opener/closer evidence;
mid-psalm occurrences are interior refrain texture.

### §2d Selah (the disclosure object of this book)
71 verses, EXACTLY one selah each (no multi-selah verses); WEB renders
"Selah." and the WEB<->MT bijection through the offset map verified 71=71.
Selah IS quotable verse text in both witnesses (unlike paseq). POLICY
(binding): selah is at MOST tier-3-like corroboration of a strophe/section
close — NEVER a boundary driver alone (its placement logic is debated);
every row whose span-relevant set (front seam + interior + end) contains
selah DISCLOSES every instance (check_marks enforces symmetry, span-scoped
absence, nearest-ref binding). Psalm-level counts live in pmarks_Ps.json —
cite the inventory, never lore (3 in Ps 3; 71 book-wide).

### §2e Acrostics (surface data byte-swept; letter tables in the inventory)
119: fully regular 22 stanzas x 8 verses, every verse of a stanza opening
with its letter — the row spine for P29 (letter_stanza rows + parent).
145: complete EXCEPT nun (its ONLY missing letter) — and WEB 145:13 carries
the restored nun couplet from DSS/LXX/Syriac with MT lacking it: chunk
WITHOUT selecting a reading; disclose on any row touching 145:13; the seam
is a natural low-confidence register entry. 34: missing waw (+ a closing
extra-alphabetic pe verse 34.23 MT). 25: irregular (bet buried mid-verse in
25.2, waw absent, doubled resh zone, closing pe verse) — surface letters in
the inventory; do NOT assert regularity. 37: every-OTHER-verse acrostic
(letter per 2 vv, surface gaps at ayin/tav from prefixed forms — first
letters are surface data, the scheme claim needs the buried-letter caveat).
9-10: ONE broken acrostic spanning BOTH psalms (the strongest textual
argument that 9-10 cohere; LXX merges them — cross-tradition METADATA only,
§4) — record as a typed cross-psalm relation, not a merged row. 111-112:
COLON-level acrostics (22 cola over 10 verses each) — verse-granularity
letters are NOT the scheme; claims stay at colon level with that caveat.
Acrostic structure where regular is tier-1 (inclusio/acrostic class) for
INTERNAL stanza seams (esp. 119); surface irregularities are disclosed, not
harmonized.

### §2f Divine-name texture (macro-device; token counts at skeleton tier)
Elohistic Psalter: Book II (42-72) runs YHWH 32 / Elohim 165; contrast
Book I (1-41) 278/15, III (73-89) 44/46, IV (90-106) 105/6, V (107-150)
236/10. Per-psalm counts in the inventory. TEXTURE ONLY — never a boundary
driver by itself; legitimate as corroborating discussion at the 41|42 and
83|84 texture edges. The doublets (14=53, 40:14-18=70, 57+60=108) are
typed cross-psalm relations (decision_relations), never merge candidates.

## §3 Numbering discipline (THE book hazard; ../web_mt_offset_map.json is
the arithmetic authority — content-verified three ways at Phase 0)
Two numbering spaces: bare/web: refs + row spans = WEB; oshb:/pmarks = MT.
Per-psalm rules: 87 identity; 58 shift+1; 4 shift+2 (51, 52, 54, 60);
Ps 13 SPLIT (WEB 13:1-4 = MT 13:2-5; WEB 13:5 AND 13:6 BOTH = MT 13:6 —
both halves dual-cite oshb:Ps.13.6). EVERY original-language citation in a
non-identity psalm dual-cites (web:Ps.N.V = oshb:Ps.N.MTv) — machine-checked
(citation_sweep), including range ENDS and the X-X single-verse span form.
Use ps_lib.web_to_mt()/mt_to_web(); NEVER hand-compute; "verse N" prose
mentions resolve against the row's psalm and must be mirrored. WEB Strong's
attrs are MISALIGNED in offset psalms (index-aligned to MT) — never cite.

## §4 Marker policy + cross-tradition scope
WLC Psalms carries NO petuchah/setumah segs AT ALL (byte-verified): the
paragraph-mark layer is ABSENT; absence is never counterevidence, and any
positive pe/samekh claim is a fabrication (hard validator error). Seg-layer
objects that DO exist (single-witness disclosure required, inventory-cited,
never quotable as verse bytes): paseq 522/481 verses; inverted nuns
(x-reversednun) 7 at MT 107.20-25 + 107.39 AS THE BYTES HAVE THEM
(traditions differ on placement — cite the inventory); suspended ayin at
MT 80.14. K/Q: 68 notes / 65 verses — disclose when a quoted span crosses
one (validator arm reads the inventory). Cross-tradition (ALL metadata-only,
never in refs): LXX/Vulgate psalm NUMBERING runs one behind MT through most
of the book (LXX 9 = MT 9-10; LXX 113 = 114-115; MT 116, 147 split in LXX);
11QPsa's divergent order + Ps 151; the Syriac Pss 152-155. Greek-numbering
comparisons in prose need an explicit crosswalk sentence.

## §5 Five-book architecture (working hypothesis for writers; verify, don't inherit)
I 1-41 (Davidic core; YHWH), II 42-72 (Elohistic: Korah 42-49, Asaph 50,
David 51-65+68-70, Solomon 72 + colophon 72.20), III 73-89 (Asaph 73-83,
Korah 84-85+87-88, Ethan 89), IV 90-106 (Moses 90; YHWH-malak cluster
93-99; hallelu-Yah close 104-106), V 107-150 (hodu 107; Davidic 108-110,
138-145; hallel blocks 111-118 + 135-136; ascents 120-134; final hallel
146-150). Genre clusters (lament/praise/thanksgiving/royal/wisdom) are
DISCUSSION texture; the tier-1 seam evidence stays superscriptions,
hallelu-Yah/hodu frames, doxologies, acrostic structure, and explicit
speaker/addressee shifts INSIDE psalms.

## §6 Row-granularity policy (owner-ruled)
- Psalm = parent, ALWAYS: every row carries its psalm's parent grouping in
  decision_relations (150 parents; the convergence layer compares across
  granularities through them).
- Short psalms (roughly <=8 vv, indivisible movement): ONE whole_psalm row
  (e.g. 117 at 2 vv, 100, 131, 133, 134). Never pad.
- Longer psalms: strophe rows ~4-8 vv at tier-1-supported internal seams
  (speaker/addressee shifts, refrain returns, vocative openings, imperative
  clusters, selah-corroborated closes only WITH an independent driver).
- Ps 119: 22 letter_stanza rows (8 vv each) + parent.
- Refrained psalms [SEE §11 ERRATUM: add 56 to this roster] (42-43 עם one refrain spine; 46; 57; 59; 62; 67; 80; 99;
  107 with its double refrain pair; 116? verify): strophe rows follow the
  refrain returns; the 42-43 pair records a typed cross-psalm relation
  (shared refrain 42.6, 42.12, 43.5 MT) — two parents, never a merged row.
- unit_type CONTROLLED VOCABULARY (lesson f; writers choose EXACTLY one):
  whole_psalm | strophe | letter_stanza | refrain_unit | coda.
  coda = doxology/colophon closes (41.13 WEB, 72.18-20 WEB, 89.52 WEB,
  106.48, 150 as the Psalter's closing doxology-psalm if argued). No
  free-text unit types; combine normalizes nothing.

## §7 Expected low-confidence regions (register early, hold honestly)
9-10 broken acrostic pair (row seams inside both psalms + the cross-psalm
relation); 145:13 nun-line variant zone; 25/34 irregular acrostic closes;
111/112 colon-level schemes; the 42-43 refrain pair; 107's double refrain
lattice; 118's antiphonal structure; 132's oath dialogue; 68 (the Psalter's
hardest text — fragment-catalog texture, many hapaxes: expect medium_low
confidence rows and say so); 87's terse oracle (locus of the Zion register);
110's two oracles (byte-settle כדברתי מלכי־צדק before any ordinal claim);
the ascents' step-parallelism (texture, not driver). Confidence follows the
byte-verified warrant, not genre familiarity (Job boss rubric BOSS-JOB-5
carries forward).

## §8 Numbering-adjacent register rules (verbatim into every brief)
- The MT title verses are TEXT, not paratext: quote them like any verse
  (they are the tier-1 opener evidence), always via dual-cite.
- NEVER write "superscription" for Ps 119's letter headers (they are WEB
  typography for the acrostic; MT has no headers — the letters are the
  verses' own initials).
- "Psalm N" in prose = the composition; "Ps.N.V" = WEB verse; "MT N:V" =
  MT verse. LXX numbers never appear without the word "LXX" and a crosswalk
  sentence.
- Selah/paseq/inverted-nun/suspended claims cite their inventory with
  "(single-witness)" for seg-layer objects; selah needs no witness tag (it
  is verse text in both witnesses) but respects span-scoped symmetry.

## §9 Granularity + writer part plan (tiling 2461 EXACTLY, 34 parts,
psalm-aligned — no part splits a psalm; owner-ratified scale)
P01 1-8 (82) · P02 9-16 (82) · P03 17-19 (79) · P04 20-24 (69) ·
P05 25-30 (80) · P06 31-34 (79) · P07 35-37 (80) · P08 38-43 (81; Book I|II
seam + 42-43 pair) · P09 44-48 (77) · P10 49-53 (77) · P11 54-59 (82) ·
P12 60-65 (66) · P13 66-68 (62; incl. Ps 68 — the hard one) · P14 69-71
(65) · P15 72-75 (81; Book II|III seam + colophon) · P16 76-77 (32) ·
P17 78 (72) · P18 79-83 (74) · P19 84-88 (67) · P20 89-90 (69; Book III|IV
seam) · P21 91-95 (70) · P22 96-101 (56) · P23 102-103 (50) · P24 104-105
(80) · P25 106 (48; Book IV|V seam) · P26 107-108 (56) · P27 109-114 (75) ·
P28 115-118 (68) · P29 119 (176; letter_stanza spine) · P30 120-131 (77;
ascents) · P31 132-137 (80) · P32 138-143 (74) · P33 144-148 (80) ·
P34 149-150 (15). Writers: sonnet, one part each, briefs point at
SP/Ps/tools/TOOLKIT.md; every part's rows tile its psalms exactly
(check_tiling per psalm); <=8 rows per attempt id; seam-pair rows at part
edges are authored by the EARLIER part (the later part consumes and may
challenge via errata, never re-authors).

## §10 Register + hygiene (verbatim into every brief)
NO decision-ids, strategy-§ citations, erratum narration ("is now
dual-cited", "correcting a prior"), positional row references, file-order
talk, or review-actor names in row prose EVER; cross-row references are
verse-anchored ("the seam at 41:13|42:1"). Curly quotes + inline web: ref
for every English quotation; byte-spliced Hebrew (never hand-typed) bound
to its cited oshb: ref in the same field; tier named for every non-textual
signal; every universal claim carries an adjacent DIGIT-bearing sweep count
NAMING ITS UNIT (verses vs occurrences); driver swaps re-open
observed_substrate_signals, rejected_alternative, unit_type, confidence;
seam-pair cures are ONE edit installed on BOTH rows; replacement warrants
pass the test that killed the original; quote/gloss parity repairs re-cut
the gloss. rejected_alternative: one sentence, + an optional second ONLY for
the mandated rival. Mandated recurring sentences (the parent-grouping
standard sentence) ship with 4+ pooled variation orders. Work in uniquely-
named private subdirectories of your OWN session scratchpad — never in
SP/Ps; if you find yourself building a tool, STOP (it exists in the
toolkit or you don't need it).

## §11 Writer-wave errata + supplements (installed 2026-08-12; append-only)
- ERRATUM (p11, byte-verified by orchestrator): Ps 56 belongs in the §6
  refrain roster — MT 56:5 (באלהים אהלל דברו באלהים בטחתי לא אירא מה יעשה
  בשר לי) returns SPLIT across MT 56:11 (doubled hallel-clause, ביהוה added)
  + 56:12 (identical trust-clause with בשר -> אדם). Cite per-member with
  collate tiers; never claim verbatim across the swap.
- ERRATUM (p02, byte-verified): the inventory's al_alamot label wrongly
  included Ps 9 — MT 9:1 reads pointed עַלְמוּת לַבֵּן (almut labben, now its
  own label), skeleton-identical to but distinct from Ps 46's עֲלָמוֹת.
  Inventory rebuilt with pointed disambiguation; al_alamot = {46} only.
- ERRATUM (p08, byte-verified): al_yeduthun membership was {62, 77} —
  Ps 39:1's לידותון (lamed prefix; ketiv לידיתון) was missed by the
  no-prefix label regex. Builder now allows prefixes + both spellings;
  membership {39, 62, 77}. §2a's "VERIFY before citing a third" resolves:
  THREE yeduthun titles, two spelling classes, K/Q pairs at 39:1 and 77:1.
- ERRATUM (p22, byte-verified): Ps 98 IS titled ("A Psalm." = mizmor inside
  MT v1) — the §-note class "96-99 untitled" was wrong for 98. AND the
  inventory's shir label falsely included 98 (body shir hadash) and 18
  (ha-shirah in the historical title) — the label sweep now uses a right
  boundary + title-prefix haystack for identity psalms. Corrected counts:
  shir 30, le_david 73 (132's "remember FOR David" is content, not
  attribution), binginot 7 {4,6,54,55,61,67,76} (attested forms
  binginot/neginat).
- ERRATUM (p26, byte-verified): §2f/§6's Ps 108 composite spans were MT
  numbers mislabeled as WEB. Correct WEB numbering: Ps 108 = Ps 57:7-11 +
  Ps 60:5-12 (join at WEB 108:5|108:6 = MT 108:6|108:7; divine-name
  substitution Adonai(57:10 MT) -> YHWH(108:4 MT) in the identical slot).
- ERRATUM (p27, byte-verified) + SOURCE-VIEW FACT: the staged OSHB extract
  (Ps_oshb.txt / verse_map_oshb.json) serializes maqaf as a SPACE — 0
  maqaf codepoints book-wide, though the OSHB XML carries 2404 x-maqqef
  segs. "Byte tier" means fidelity to the staged source view, which is
  maqaf-free; typographic-maqaf claims (e.g. Melchizedek at MT 110:4) are
  claims about WLC print tradition, NOT about our quotable bytes — cite
  the XML seg layer if ever needed, never assert maqaf in quoted spans.
- ERRATUM (OL-c17, byte-verified): §2f's doublet roster "40:14-18=70" uses
  MT numbers unlabeled (WEB Ps 40 has 17 verses). Correct WEB form:
  Ps 40:13-17 = Ps 70 (whole body). Same class as the p26 erratum — when
  citing doublets, label the numbering space explicitly.
- NOTE (OL-c28): §7's "many hapaxes" phrasing for Ps 68 is an unquantified
  rarity claim that propagated into row prose. Hapax status is NOT decidable
  with the Psalms-scoped staged tools (sweep is book-internal); rows must
  either drop rarity claims or scope them explicitly ("1 verse in Psalms,
  skeleton tier") — never "hapax" bare.

## §12 T467 required-section compliance addendum (appended at book close, 2026-08-18)

Appended append-only at Ps book close: the T467 overlay validator requires these
seven section tokens verbatim in every book strategy; the Ps strategy predates
that check and covers each concern in the sections cited. No pre-existing text
above this line was altered.

- literary_form_decision_matrix: §2 device matrix (superscriptions, doxology
  seams, hallelu-Yah/hodu frames, Selah, acrostics, divine-name texture) plus
  the §6 unit_type vocabulary (whole_psalm / strophe / refrain_unit /
  letter_stanza / coda) drive form-by-form boundary decisions.
- larger_unit_preservation_check: §6 mandates per-psalm parent grouping (150
  parents in decision_relations) and whole-psalm rows for short indivisible
  psalms, preserving the larger liturgical unit over strophe convenience.
- list_register_function_check: §2c litany/refrain frames (hallelu-Yah, hodu)
  and §2e acrostic letter tables are treated as register-bearing structures
  chunked by function, never split mechanically mid-frame.
- epistle_unit_check_if_applicable: not applicable — the Psalter contains no
  epistolary units; recorded here as the explicit not-applicable finding.
- source_metadata_evidence_only_check: §4 marker policy and §2d Selah
  disclosure apply the owner tier rules — scribal/editorial layers corroborate,
  never originate, a boundary; chapter/verse numbering is metadata only (§3).
- over_split_risk_check: §6 and §9 set the ~5–6 vv/row poetry norm with
  whole-psalm rows for short psalms and letter-stanza rows only for Ps 119,
  guarding against strophe-level over-splitting.
- sidecar_specificity_plan: §7 registers expected low-confidence regions early
  with bespoke uncertainty text; the 10 medium_low rows plus the conflict-D
  owner hold (M8-Ps-433) are mirrored across all three sidecars at book close.
