# Prov book strategy (M8_fable, m8-mesh-r3) — fable-authored, Phase 1

Status: ACTIVE for the writer wave; candidate-only, non-authorizing. Every count
below is byte-swept from SP/Prov staging artifacts (pmarks_Prov.json,
prov_device_inventory.json, web_mt_offset_map.json — re-runnable via
sweep.py / prov_devices.py; skeleton tier). COUNT-OBJECT DISCIPLINE: every
count names WHAT it counts; writers re-derive independently and report errata
with bytes (the pipeline expects and credits errata; Ps's mesh corrected the
orchestrator repeatedly). Strong evidence tiers, the owner scribal-layer
addendum, and the campaign strategy contract (literary_marker_aware_v2 +
T467_literary_coherence_v1) govern throughout.

## §1 Objective and shape
915 WEB verses / 31 chapters; MT identical (IDENTITY book, byte-PROVEN at
Phase 0 — per-chapter counts, 123 content anchors, 0 KJV-variance notes, the
31:10-31 acrostic as a 22-point ch-31 anchor; SP/Prov/web_mt_offset_map.json).
Prov is SENTENCE LITERATURE at its core: chs 10-29 are largely independent
couplets with weak local cohesion (byte-verified: max 11/32 adjacent pairs
share a content token, ch 16). Eight editorial collections frame it (§5).
OWNER GATE RULINGS (2026-08-18, all binding): (1) HYBRID ATOMIC DEFAULT for
10:1-22:16 and 25-29 — single-proverb rows by default; a multi-verse cluster
row ONLY with byte-grounded cohesion evidence named in the rationale
(catchword chain, pair grouping, YHWH/kings cluster, shared construction
run); (2) unit_type = the 8-value structural vocabulary of §6 — parallelism
class goes in device_notes, never unit_type; (3) r3 scaled to Prov: 13
writer parts, dual blind LF+OL primaries over clusters of <=8 rows, scoped
peers, validator-suite rev round + spot wave, ~4-6M subagent token target.
Expect ~480-560 decisions (atomic default dominates); if the projection
exceeds the approved envelope the orchestrator checks in with the owner
before launching the excess wave.

## §2 Device matrix (byte-swept; identity refs; consume the inventory, don't re-derive)

### §2a Collection seams (the tier-1 header spine) — literary_form_decision_matrix
mishle VERSE-INITIAL at 1:1 and 10:1 ONLY (25:1 carries mishle interior:
גם אלה משלי שלמה); gam-elleh verse-initial at 24:23 AND 25:1; divrei
verse-initial headers at 30:1 (Agur) and 31:1 (Lemuel) — but דברי occurs in
19 verses total (12:6, 18:8, 26:22 are NOT headers); divrei-hakhamim phrase
at 1:6 and 22:17. The 22:17 "words of the wise" seam is IN-VERSE — argue it
from the text. Form decision matrix: header/seam verses open collection
parents; inside collections the form is decided per §6 vocabulary with the
granularity policy of §1.

### §2b Parashah layer (tier-3 WEAK — Writings; single witness)
51 PE + 1 SAMEKH over 52 verses. Structure-shaped: dense in 1-9 (24 segs,
lecture ends) and ch 30 (8 segs, numerical-saying seams); sparse in 10-29.
The ONE SAMEKH at 24:22 = last verse before the 24:23 header; PE at 10:1 and
31:9 (last verse before the acrostic). NEVER a driver; corroboration only,
single-witness disclosed, PE never conflated with SAMEKH. Absence is never
counterevidence.

### §2c Acrostic — eshet chayil 31:10-31
22 verses, full alef-bet IN ORDER, derived from skeleton bytes (table in
prov_device_inventory.json). ONE row, unit_type acrostic_poem (owner-ratified).
NOTE: אשת חיל occurs TWICE in the book (12:4 AND 31:10) — sweep digit 2; any
"unique" claim at 31:10 is byte-false.

### §2d Address formula + density textures
bni ("my son") 17 verses: 12 in chs 1-7 (1:8, 1:10, 1:15, 2:1, 3:1, 3:21,
4:10, 4:20, 5:1, 6:1, 6:20, 7:1 — the lecture-frame spine) + 19:27, 23:15,
23:26, 24:13, 27:11. YHWH exact-token density peaks: ch 3 (9), ch 15 (9),
ch 16 (6) — the 15:33-16:9 center cluster is byte-visible; texture, never
alone a driver. tov openers: 16 verses. Antithetic ", but" texture cliff:
chs 10-15 run 24/21/25/22/25/20, ch 16 drops to 7 — English-side heuristic,
never row evidence.

### §2e Disclosure objects (MT-keyed inventories in pmarks_Prov.json)
K/Q 69 notes / 63 verses; paseq 60 segs / 57 verses (COUNT-ONLY — intra-verse
position claims unsourceable); ONE x-small nun at 16:28. FABRICATION CLASSES:
selah, reversed-nun, suspended letter — none exist in Prov.

## §3 Numbering discipline
Identity everywhere; Prov.N.0 is ALWAYS invalid (no title pseudo-verses).
Dual-cites never required; any WRITTEN dual/qualifier must be arithmetically
right (machine-checked). Single-verse spans use full X-X form
(Prov.3.5-Prov.3.5). Use prov_lib mapping functions — they range-guard.

## §4 Marker policy + cross-tradition scope — source_metadata_evidence_only_check
Tier-4 metadata (chapter/verse numbers, WEB headings/footnotes, modern ¶ and
poetry-line breaks, strong= attrs) is NEVER boundary evidence and NEVER
counterevidence by absence. Tier-3: parashah in Writings (§2b), single
witness. Source metadata is evidence for review, not authority. LXX REORDERS
24:23-34 and chs 30-31 (30:1-14 after 24:22; 30:15-33 + 31:1-9 after 24:34;
31:10-31 at book end) — cross-tradition METADATA in prose only, never in
refs, never counterevidence; Greek-order comparisons need an explicit
crosswalk statement.

## §5 Eight-collection architecture (byte-anchored; parents)
C1 1:1-9:18 lectures+poems (1:1-7 title/motto); C2 10:1-22:16 Solomon
sentence collection; C3 22:17-24:22 words of the wise; C4 24:23-34 also-of-
the-wise appendix; C5 25:1-29:27 Hezekiah collection; C6 30:1-33 Agur +
numerical sayings; C7 31:1-9 Lemuel royal instruction; C8 31:10-31 eshet-
chayil acrostic. MANDATORY parent grouping: every row carries
parent_collection (C1..C8 spans as above) in decision_relations-equivalent
fields — larger_unit_preservation_check: the collection is the preserved
larger unit; rows never straddle a collection seam.

## §6 Row-granularity policy (owner-ruled 2026-08-18) — over_split_risk_check
unit_type CONTROLLED VOCABULARY (8 values, closed): instruction_lecture,
wisdom_poem, single_proverb, proverb_cluster, admonition_unit,
numerical_saying, royal_instruction, acrostic_poem.
- C1: instruction_lecture units at bni/vocative + parashah-corroborated
  seams (~4-8 vv); wisdom_poem for 1:20-33, 3:13-20(?), ch 8, ch 9 — the
  writer argues each poem's bounds from bytes.
- C2 + C5: SINGLE_PROVERB DEFAULT. proverb_cluster ONLY with byte-grounded
  cohesion evidence NAMED in the rationale (e.g. the 26:4-5 answer/answer-not
  pair; catchword chains; the 15:33-16:9 YHWH cluster; kings run 16:10-15;
  construction runs like consecutive tov-min sayings). A cluster whose only
  glue is a shared THEME is over-clustering — the mesh will challenge it.
- C3: admonition_unit (~2-4 vv imperative units; 22:17-21 is the prologue).
  C4: admonition_unit/single_proverb per bytes.
- C6: numerical_saying per x-of-y unit; Agur's opening 30:1-9 argued from
  bytes (30:1 massa + K/Q-adjacent cruxes -> expect low confidence).
- C7: royal_instruction (likely ONE unit 31:1-9); C8: acrostic_poem (ONE row).
- Parallelism class (antithetic/synonymous/synthetic) is recorded in
  device_notes as texture; NEVER in unit_type; NEVER alone a boundary driver.
- list_register_function_check: numerical sayings (C6) and any register-like
  runs are chunked by FUNCTION (the x-of-y unit), never split mid-list;
  epistle_unit_check_if_applicable: NOT APPLICABLE (no epistolary units in
  Prov) — recorded as the explicit finding.

## §7 Expected low-confidence regions — sidecar_specificity_plan
Register early, hold honestly, bespoke uncertainty text per row (no
boilerplate): 22:17-21 (in-verse seam + LXX-divergent text); 26:4-5
(deliberate contradiction pair — cluster candidate WITH the pair as
evidence); 30:1 (massa/oracle + Ithiel-Ucal crux); 31:1 (massa again);
17:1 (חרבה dry-morsel homograph zone); K/Q-dense verses (69 notes — disclose
when a span touches one); catchword-cluster rows whose cohesion evidence is
thinner than 2 shared content tokens. Sidecar rows mirror every medium_low/
low decision in all three sidecars with row-specific text.

## §8 Register + hygiene (verbatim into every brief)
- Work in a UNIQUELY-NAMED private subdir of YOUR OWN session scratchpad;
  never write into SP/Prov except your assigned output file; never reuse
  bare filenames at scratch root.
- USE SP/Prov/tools (TOOLKIT.md first). If you find yourself building a
  tool, STOP — it exists or you don't need it.
- NEVER hand-type or copy-through-draft Hebrew: splice from
  verse_map_oshb.json, then re-collate your own output (byte tier for
  pointed text).
- Curly quotes for WEB text ONLY + inline web: ref in the SAME field;
  straight quotes for everything else.
- NO decision-ids, §-citations, erratum narration, positional row refs,
  file-order talk, or reviewer names in row prose. Cross-row references are
  verse-anchored.
- rejected_alternative: one sentence (+ optional second ONLY for the
  mandated rival). Recurring mandated sentences ship with 4+ variations.
- Every universal claim (only/never/densest/sole/first...) carries an
  adjacent DIGIT-BEARING sweep citation that NAMES the swept object and
  unit. See the TOOLKIT hazard catalog (כמה-in-חכמה, מלך, חרב, ימינו, כלם,
  אשת-חיל-twice, דברי, טוב-מ) before trusting any short-token digit.
- Governance note: the M8 worktree is gated; writers are SCRATCHPAD-ONLY
  (read-only on the worktree), write NOTHING outside your assigned output.

## §9 Writer part plan (tiling 915 EXACTLY, 13 parts, chapter-aligned)
P01 1:1-2:22 (55) | P02 3:1-4:27 (62) | P03 5:1-6:35 (58) |
P04 7:1-8:36 (63) | P05 9:1-11:31 (81; crosses C1|C2 at 9:18|10:1 — parts
are work units, rows still respect the seam) | P06 12:1-14:35 (88) |
P07 15:1-16:33 (66) | P08 17:1-19:29 (81) | P09 20:1-22:16 (77) |
P10 22:17-24:34 (82 = C3+C4) | P11 25:1-27:27 (83) | P12 28:1-29:27 (55) |
P13 30:1-31:31 (64 = C6+C7+C8). Sum 915. Writers: sonnet, one part each,
output draft rows JSONL to SP/Prov/writer/pNN_rows.jsonl (schema in brief);
exact verse tiling within the part REQUIRED (checked by check_tiling).
Review clusters: <=8 rows per attempt id from the start; dual blind
LF(sonnet)+OL(opus) per cluster; scoped peers; boss ledger <=8/attempt;
validator suite over drafts BEFORE primaries and over revised rows in the
rev round; 6-agent spot wave per r3.

## §10 Strategy self-checks (T467 anchor summary)
literary_form_decision_matrix: §2a+§6. larger_unit_preservation_check: §5
(collection parents; rows never straddle seams). list_register_function_check:
§6 (numerical sayings by function). epistle_unit_check_if_applicable: §6
(explicitly N/A). source_metadata_evidence_only_check: §4 (+owner addendum
tiers). over_split_risk_check: §6 (atomic default is the genre's own unit;
cluster bar prevents both over-split of coherent runs and fake clusters).
sidecar_specificity_plan: §7 (bespoke text, three-sidecar mirroring).
