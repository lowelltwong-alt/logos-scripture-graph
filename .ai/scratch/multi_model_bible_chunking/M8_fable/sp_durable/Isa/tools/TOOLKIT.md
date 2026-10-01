# Isa shared verification toolkit (m8-mesh-r3, built Phase 0 by the orchestrator)

**USE these tools. Do NOT rebuild, copy, or re-derive any of them.** Every brief
points here. Work in a UNIQUELY-NAMED private subdirectory of YOUR OWN session
scratchpad — never write scratch into SP/Isa or at any scratchpad root, and no
debug files anywhere under SP, including in SP output directories during
self-check iteration.

Run everything with `PYTHONIOENCODING=utf-8 python <tool> ...` from this directory.

## Book facts (Phase 0 verified — trust these; do not re-derive)

### Numbering: NOT IDENTITY — TWO offset zones with DIFFERENT SHAPES (byte-PROVEN)
WEB 1,292 verses / MT 1,291, 66 chapters. Both classic seams are real, and
they are NOT the same shape:

- **ZONE A (chs 8-9) — pure renumbering:** **MT 8:23 = WEB 9:1**
  (Zebulun/Naphtali/Galilee line); **MT 9:1-20 = WEB 9:2-21**. WEB ch 8 =
  22 vv / MT 23; WEB ch 9 = 21 / MT 20.
- **ZONE B (chs 63-64) — a genuine SPLIT:** **MT 63:19 spans WEB 63:19 +
  WEB 64:1** (one MT verse, TWO WEB verses: the "never ruled / not called
  by your name" half at WEB 63:19; the "tear the heavens … mountains quake"
  half at WEB 64:1); **MT 64:1-11 = WEB 64:2-12**. Ch 63 counts are EQUAL
  (19 = 19, numbering identity) — the split is a CONTENT fact; WEB ch 64 =
  12 vv / MT 11.

Every other chapter is identity. Proof layers (../web_mt_offset_map.json):
per-chapter count equality UNDER THE RULE SET from both witnesses' bytes;
959 automatic content anchors agreeing at the CROSSWALK-mapped refs (34 in
the zones; all 29 misses byte-reviewed as rendering/spelling divergences at
identity refs — zero unexplained, zero in-zone); FALSIFICATION probes
showing identity fails 23 anchor checks in zone A and 9 in zone B (under
identity WEB 64:12 has NO MT 64:12 at all); a SPLIT DISCRIMINATOR (WEB
64:1's שמים/הרים/ירדת live in MT 63:19 and are ABSENT from MT 64:1); and 17
seam byte-review assertions incl. identity at all four zone edges (MT
8:22, 10:1, 63:18, 65:1). **The OSHB KJV-variance note layer is EMPTY for
Isa despite TWO real zones (the THIRD book running: Eccl, Song, Isa) —
absence of notes proves NOTHING here.** There are NO title pseudo-verses —
**Isa.N.0 is always invalid**; Isa 1:1 (the chazon superscription) is an
ordinary counted verse in BOTH witnesses.

Convention: bare/web: refs and row spans = WEB; oshb:/pmarks = MT.
**OFFSET-ZONE RULE (Tier-0 ENFORCED, both zones): any structured ref
touching WEB ch 9, WEB ch 64, or WEB 63:19 (web: side), or MT 8:23, MT ch
9, MT 63:19, or MT ch 64 (oshb: side) MUST carry an explicit dual or
numeric qualifier (`web:Isa.9.1 = oshb:Isa.8.23`, or `(MT 9:3)` after a
web: ref) — bare coordinates are ambiguous across witnesses exactly there,
and the split verse is ambiguous EVEN AT EQUAL NUMERALS (web:Isa.63.19 is
HALF of oshb:Isa.63.19; a first/second-half wording also satisfies the
disclosure there).** The MT-side dual for the split verse accepts EITHER
WEB half (`oshb:Isa.63.19 = web:Isa.63.19` or `= web:Isa.64.1`); any
content claim about MT 63:19 must say WHICH half it lives in. Elsewhere
duals stay optional, but any WRITTEN dual/qualifier must be arithmetically
right — machine-checked by `citation_sweep.py`. Single-verse spans use the
full X-X form (`Isa.5.24-Isa.5.24`) — machine-checked. Use
`isa_lib.web_to_mt()/mt_to_web_all()` ALWAYS — never hand-assume, in
either direction; **web_to_mt is NOT injective (WEB 63:19 and WEB 64:1
both map to MT 63:19) and mt_to_web() alone is NOT enough at the split
verse** — mt_to_web_all() is the authority there. (Tool-prose note:
`PSALM_RULES` keeps its historical Ps-lineage name, and older shared-tool
docstrings say "psalm" where they mean "chapter" — read them so.)

### Cross-tradition note
MT (and LXX-order) numbering differs from the English Vulgate-family
chapter division at BOTH seams. ALL LXX/Septuagint/Old Greek/Vulgate/
Peshitta/Targum/DSS/Qumran material — **including the great Isaiah scroll
1QIsa-a, the most famous biblical DSS witness** — is cross-tradition
METADATA in prose, never boundary evidence, never counterevidence, never a
boundary_evidence_refs entry (`citation_sweep.py` guards). **The 2 Kgs
18-20 parallel to chs 36-39 (and 2 Chr 32) is intra-canon synoptic
metadata: typed-relation territory, NEVER boundary evidence for Isaiah's
seams** (lesson j). Numbering-tradition comparisons in prose need an
explicit crosswalk statement.

### PARASHAH LAYER — the campaign's LARGEST (MT-keyed)
WLC Isa carries **41 petuchah (PE) + 168 setumah (SAMEKH) segs over 209
marked verses** (../pmarks_Isa.json, byte-extracted). In the PROPHETS this
is **TIER-3 WEAK corroboration** (owner addendum:
parashah_in_prophets_or_writings): never a boundary driver, single-witness
disclosure required on every citation, PE never conflated with SAMEKH.
Absence is NEVER counterevidence. The layer is DENSE — the span-relevant
mark-disclosure SYMMETRY sweep (check_marks rule 2) is the heaviest of the
campaign: stage the pmarks read in every writer/author workflow. Claims
are validated against the inventory by `citation_sweep.py` (refs) and
`check_marks.py` (prose + span symmetry).

### Fabrication classes for Isa (hard errors)
- **selah** — Psalter device; zero occurrences in Isa (byte-swept).
- **reversed/inverted nun, suspended letter** — no such segs in WLC Isa.
- **LARGE letters — NONE in WLC Isa**: any large-letter/majuscule claim is
  a fabrication.
- **SMALL letters — exactly ONE: the small NUN (x-small ן) at MT 44:14.**
  A small-letter claim anywhere else is a fabrication; at 44:14 it needs
  single-witness disclosure. **The famous MT 9:6 medial final-mem (לםרבה)
  is NOT a seg** — it lives in the letter bytes + K/Q apparatus (below);
  framing it as a "small/large letter" is flagged.

### Disclosure inventories (../pmarks_Isa.json, MT-keyed)
- **Paseq**: 95 segs over 87 verses — seg layer, NOT quotable verse bytes;
  citable from the inventory only; "(single-witness)" required; COUNT-ONLY —
  intra-verse position claims are unsourceable (WARN arm). In-zone paseq:
  MT 9:3, 9:16 (zone A); MT 63:1, 63:3, 63:7, 63:9, 63:11 sit just before
  zone B's split verse.
- **Ketiv/qere: 53 notes over 49 verses — the campaign's LARGEST K/Q
  inventory** (as the Song close forecast). **TWO sit INSIDE zone A: MT 9:2
  (= WEB 9:3) and MT 9:6 (= WEB 9:7, the לםרבה pair). NONE in zone B — the
  split verse MT 63:19 is NOT K/Q-bearing.** Check pmarks kq before
  counting or slicing in ANY K/Q verse. Doubled-note verses: 26:20, 28:15,
  36:12, 52:5 (2 notes each).
- **OSHB exegesis note** at MT 9:5 (= WEB 9:6, the throne-names verse) —
  single-witness apparatus, not text bytes; also inside zone A.
- **Morph tally**: all 16,988 morph codes H-prefixed — NO Aramaic zones.
  (At Isa 36:11 the officials ASK for Aramaic — story content, not an
  Aramaic verse; check_language_zones knows the difference.)

### PROPHETIC FRAME SPINE (../isa_device_inventory.json — the tier-1 seam skeleton)
Byte-swept (every count NAMES its object; verse counts, MT keys):
- **Superscriptions — exactly THREE chazah/ben-Amots headers: 1:1 (chazon),
  2:1 (ha-davar), 13:1 (massa Bavel + chazah — the hinge into the massa
  series).** 38:9 מכתב לחזקיהו is a DIFFERENT header class (psalm-type
  writing-superscription heading the 38:10-20 poetry island). The
  prophet's name appears in 16 verses (three superscriptions, 7:3, 20:2-3,
  and the narrative-zone cluster).
- **Massa series**: 10 verse-initial oracle headers — 13:1 Babylon, 15:1
  Moab, 17:1 Damascus, 19:1 Egypt, 21:1 wilderness-of-the-sea, 21:11
  Dumah, 21:13 in-Arabia, 22:1 valley-of-vision, 23:1 Tyre, 30:6
  beasts-of-the-Negev. NON-initial massa tokens: 14:28 (mid-verse header
  reference in the death-year-of-Ahaz frame), 22:25 (burden common noun),
  46:1-2 (load/carry family in the idol taunt) — never blend header-massa
  with burden-massa.
- **Hoy series**: 22 verses, 20 verse-initial. Role-split before counting:
  woe-oracle onsets (ch-5 sixfold series 5:8/11/18/20/21/22; the 28-33
  series 28:1, 29:1, 29:15, 30:1, 31:1, 33:1; 10:1, 10:5, 17:12, 18:1,
  45:9, 45:10), 1:4 opening indictment, 1:24 הוי אנחם divine
  self-exclamation, **55:1 the INVITATION cry ('Ho! everyone who
  thirsts')** — and אוי (6:5, 24:16) is a DIFFERENT lexeme, never blended.
- **Divine-speech census**: כה אמר 48 verses — **44 divine-frame vs 4
  royal-messenger (patch i2, p05 writer erratum: divine frames include
  non-adjacent title forms — 21:6 intervening dative, 30:12 qadosh-Israel,
  42:5 ha-El, 51:22 suffixed adoneikh, 57:15 ram-ve-nissa; the
  royal-messenger sites are EXACTLY 36:4, 36:14, 36:16 מלך אשור and 37:3
  Hezekiah — the chs 36-37 trap: both sides use the formula; a koh-amar
  digit that does not name WHOSE frame it counts is meaningless)**; נאם
  23 verses (incl. the stacked נאם האדון יהוה צבאות at 1:24); amar/
  vayomer+YHWH adjacency 52 verses (role-split signature vs narrative
  onset; 40:1 יאמר אלהיכם is the Elohim variant).
- **Qadosh-Israel**: 25 title verses (12 in chs 1-39, 13 in 40-66 — the
  signature title spans both halves; patch i3, p14 erratum: MT 49:7 carries
  the DEFECTIVE spelling קדש ישראל, and the same verse also has the
  suffixed epithet קדושו — a different object); the 6:3 trisagion is its
  OWN object, not a title site.
- **Remnant family — FOUR objects on one root**: the NAME Shear-Jashub
  (7:3, vav-prefixed ושאר ישוב), the reactivating clauses 10:21-22, the
  שאר noun (12 vv), שארית (4 vv), the נשאר/ישאר verb family (8 vv).
- **Servant census**: עבדי 23 verses / eved-family 44 (prefix-tolerant).
  Named referents: 20:3 the prophet, 22:20 Eliakim, 37:35 David,
  Israel/Jacob named in 41:8-9, 44:1-2, 44:21, 45:4, 48:20, 49:3; the
  UNNAMED servant-figure zones 42:1, 42:19, 43:10, 49:5-6, 50:10, 52:13,
  53:11 are a classic held question — a chunking row never decides the
  referent. The four classic servant-song candidate zones (42:1-9,
  49:1-13, 50:4-11, 52:13-53:12 neighborhoods) are STAGING SIGNALS ONLY —
  bounds are writer territory argued from tier-1 seams.
- **Stretched-hand refrain**: בכל זאת לא שב אפו ועוד ידו נטויה
  byte-identical at 5:25, 9:11, 9:16, 9:20, 10:4 (MT) — **it BRIDGES the
  ch-5 woe series and the 9:7-10:4 poem, and three sites are IN ZONE A
  (= WEB 9:12, 9:17, 9:21): every citation dual-cites.** The classic
  structural crux of chs 1-12.
- **Immanuel**: עמנו אל at 7:14, 8:8, 8:10 (8:10's כי עמנו אל is the
  formula as a CLAUSE — name-vs-clause is a held classic).
- **Divine names**: YHWH in 394 verses (EVERYWHERE — contrast Song's zero;
  citations are ordinary but count-objects still get named); bare-adonai
  51 verses (**role-split in the narrative zone: courtly 'my lord' of the
  Rabshakeh's master vs the divine Adonai of 6:1**); YHWH-tsevaot 60;
  **Yah short form at exactly THREE sites: 12:2 (יה יהוה stack), 26:4
  (ביה יהוה), 38:11 (יה יה DOUBLED, in the Hezekiah psalm)**.
- **Narrative zone chs 36-39** (identity numbering): prose-dominant with
  TWO poetry islands — the taunt-song 37:22-35 and the Hezekiah psalm
  38:10-20 under the 38:9 mikhtav header. Names: Hezekiah 29 vv,
  Sennacherib 4, Rabshakeh 8 (רב שקה — TWO TOKENS in the staged extract).
- **Chapter texture table** (chapter_texture rows): per-chapter poetry
  share + hoy/koh-amar/neum/massa/YHWH densities — staging profile for
  the at-scale part plan; writers re-derive, never row evidence.

## SWEEP HAZARD CATALOG (lesson e — every class byte-verified in Isa)
- **לםרבה (THE Isa trap, MT 9:6)**: a FINAL MEM IN MEDIAL POSITION in the
  letter bytes, staged as a DOUBLED token pair לםרבה למרבה (K/Q
  apparatus). It defeats naive mem-form assumptions in both directions,
  the verse is K/Q-bearing AND in zone A (= WEB 9:7), and the same verse
  carries the throne-name pileup. Any token count, mem-sensitive sweep, or
  quote here names which form it engages. **Build every anchor list and
  sweep regex FINALS-NORMALIZED from the start** — this discipline caught
  the orchestrator's own 1:1 fixture at Phase 0 (חזונ vs חזון — the Song
  lesson-e class biting again, recorded as live proof).
- **משא header-vs-burden**: 10 verse-initial headers vs 14:28 header
  reference vs 22:25/46:1-2 burden-noun — three roles, one skeleton.
- **הוי role-split**: woe-oracle vs indictment vs self-exclamation vs the
  55:1 invitation; אוי is a different lexeme entirely.
- **כה אמר frame ownership**: divine vs royal-messenger (both LIVE in chs
  36-37); name the speaker class before any digit.
- **ישעיהו vs the ישועה salvation family**: the prophet's name contains
  the salvation root — a שוע/ישע-skeleton sweep blends the name (16 vv),
  the salvation nouns (ישועה/ישעי forms — a major book motif, 12:2-3 etc.),
  and the verb forms. Name the object; sweep by full attested form.
- **שאר name-vs-clause-vs-noun-vs-verb**: Shear-Jashub (7:3) / 10:21-22
  clauses / שאר noun / שארית / נשאר verbs.
- **צר/צור homograph triple**: Tyre (צר, ch 23 massa), rock-epithet (צור,
  17:10, 26:4, 30:29, 44:8), adversary/narrow (צר/צרה family, pervasive).
  Word-bind or byte-check every sweep; the Egypt anchor class showed the
  poetic byform hazard too (מצור for מצרים at 19:6, 37:25).
- **אל short-token trap**: El 'God' (9:5 אל גבור, 10:21, the Immanuel
  clauses) vs the preposition אל — never sweep 2-letter function words
  without word-binding + pointed checks (standing rule since Ps).
- **Divine-name count-objects**: tetragrammaton (394 vv) vs adonai
  (role-split!) vs YHWH-tsevaot vs qadosh-Israel vs Yah (3 sites, one
  DOUBLED) — name the object; watch the stacked forms (יה יהוה 12:2, נאם
  האדון יהוה צבאות 1:24).
- **עבד referent classes**: prophet/steward/David/Israel-named/unnamed
  figure — name the class before any servant digit.
- **רב שקה is TWO TOKENS** in the staged extract (maqaf serialized as
  space): a single-token רבשקה sweep finds nothing.
- **OFFSET-ZONE COUNTING (both zones)**: any per-chapter digit touching
  chs 8-9 or 63-64 must NAME its numbering space (e.g. the stretched-hand
  refrain sites are MT 9:11/9:16/9:20 = WEB 9:12/9:17/9:21; the Zebulun
  line is MT 8:23 = WEB 9:1); **and any MT-63:19 content claim names its
  WEB half**.
- **K/Q before slicing**: 49 K/Q verses (largest inventory of the
  campaign) — check pmarks kq before counting or slicing in ANY of them;
  the doubled-note verses (26:20, 28:15, 36:12, 52:5) carry TWO notes.
- **Mater-lectionis / defective-plene pairs**: sweep per attested
  spelling — the anchor review caught plene יוצר vs defective יצר (30:14,
  41:25) and singular/article har-forms as live in-book classes.
- **Hezekiah spelling**: Isa uses חזקיהו (29 vv); the יחזקיהו byform
  (2 Kgs style) is NOT attested here — a cross-book spelling assumption
  is a fabrication.

## Data files (consume directly)
- `verse_map_web.json` — WEB ref → {text, clean, para_before,
  continuation_paragraphs, poetry_lines, language, mt} (+ mt_half on the
  two split-verse halves); 749 of 1,292 verses open poetry lines; **16
  continuation-paragraph folds are LIVE (M8-LOG-0002 machinery ARMED —
  contrast Song's zero), and the fold sites cluster ON the massa headers**
  (15:1, 17:1, 19:1, 21:1, 21:11, 21:13, 22:1, 23:1, 30:6) + 6:8, 6:11,
  9:3, 24:16, 25:10, 39:3-4 (token audit 1292/1292 PASS against raw USFM).
- `verse_map_oshb.json` — MT ref → {text (full pointed), language, web}
  (+ web_split/split_note on MT 63:19).
- `consonantal_index.json` — MT ref → {skeleton, accent_stripped, nfd}.
- `../pmarks_Isa.json`, `../isa_device_inventory.json`,
  `../web_mt_offset_map.json`, `../verse_inventory.json`.
- WEB Isa carries ZERO editorial apparatus lines (no [SPEAKER]/[HEADING]/
  [SUPERSCRIPTION]/[MAJOR-SECTION]); 31 [fn …] footnote sites remain
  inline (norm_english strips them).

## Tools
| Tool | Purpose |
|---|---|
| `collate.py --ref oshb:Isa.C.V --quote "…"` | Hebrew quote tier: byte / nfd / accent_stripped / skeleton / none. Only **byte** is quotation-grade for pointed text. Bare/web: refs are crosswalk-mapped to MT internally (WEB 63:19 and 64:1 both reach MT 63:19's bytes). |
| `check_web_quotes.py FILE...` | Verbatim check of curly-quoted English near web: refs. CURLY QUOTES + an inline web: ref in the SAME field are MANDATORY at every layer. The neighbor-only WARN arm is LIVE in WEB chs 8-9 and 63-64 (MT-number-under-web-prefix hazard). |
| `check_refs_mirror.py ROWS...` | Every verse argued in prose OUTSIDE the row's own span must appear in boundary_evidence_refs — INCLUDING bare "verse N"/"vv. N-M" mentions resolved against the row's span chapter. Witness-prefix-aware; SPLIT-AWARE (MT 63:19 argues/covers BOTH WEB halves). |
| `check_marks.py ROWS...` | Isa pivot: selah/reversed-nun/suspended/LARGE-letter claims = fabrication; SMALL-letter claims validated against the ONE x-small site (MT 44:14); petuchah/setumah claims validated against the 209-verse inventory under the claimed TYPE (PE≠SAMEKH) at MT keys (dual-reading in the zones); UNCONDITIONAL span-relevant mark-disclosure symmetry (DENSE layer — heaviest sweep of the campaign); K/Q claim validation; paseq-position WARN. |
| `citation_sweep.py ROWS` | Ref validity incl. RANGE ENDS and X-X span form, CROSSWALK dual-cite arithmetic (split-aware: MT 63:19 pairs with EITHER WEB half), **two-zone disclosure enforcement**, mark/paseq/K-Q/special-letter claims vs inventories at MT keys, witness disclosure, LXX/DSS/1QIsa guard, selah + large-letter bans, Hebrew-quote-to-cited-ref byte binding. |
| `sweep.py --heb/--skel/--web Q [--tokens]` | Book-wide occurrence sweep. **Counts are VERSE counts** unless --tokens; every citation NAMES its unit and carries A DIGIT. --skel is contiguous consonantal SUBSTRING search — see the hazard catalog above before trusting any short-token digit. |
| `isa_devices.py` | Rebuilds ../isa_device_inventory.json (orchestrator-run; agents consume the JSON). |
| `ngram7.py ROWS` | Cross-row authorial 7-gram templating gate (≥10 rows = RED), WEB-quotation-aware; unit_type/parent_collection/writer_*/wj_or_red_letter_considered/review_status excluded (p1/p2/p4 lineage). |
| `check_universals.py FILE...` | Flags universal claims lacking an adjacent DIGIT-BEARING sweep count. |
| `check_language_zones.py FILE...` | Flags Aramaic VERSE labels (all-Hebrew book; the 36:11 Rabshakeh request is story content — review candidate, not auto-fail). |
| `normalize_hebrew_in_json.py [--write] FILE...` | Byte-splices NFD-equivalent Hebrew runs to source bytes (MIN_LEN=2). NEVER hand-type Hebrew — slice from verse_map_oshb.json. |
| `check_tiling.py FILE --range Isa.a.b-Isa.c.d` | Exact tiling of a WEB range: gaps/overlaps/order. |
| `check_atomic_isolation.py ROWS` | **STAGED, NOT ARMED** (Prov lesson-a lineage, p3-guarded output path): atomic-row neighbor-isolation validator + scoped-mesh cluster builder. ATOMIC_TYPES is pinned AFTER the owner gate; unarmed = every row model-reviewed. Crosswalk-aware (WEB 9:1 fetches MT 8:23 bytes) and SPLIT-aware (a WEB 63:19|64:1 share is by construction — flagged as split, never silent cohesion). |
| `run_validator_suite.py ROWS [--reviews F...]` | Orchestrator-only: full Tier-0 suite + consolidated report. |

### NO MORPHOLOGY LAYER in the staged extract
verse_map_oshb.json carries text/language/web only. Form claims (gender of
a suffix or verb, jussive, participle) CANNOT be machine-verified with the
staged tools — argue them from the pointed bytes plus both witnesses'
renderings; form-class labels are byte-checkable claims and get the same
discipline as digits (Song postcheck lesson g).

## Encoding + skeleton notes (READ before quoting Hebrew)
- **The staged extract is MAQAF-FREE at every tier** (byte-verified: 0 ×
  U+05BE across all 1,291 MT verses — the extractor serialized maqaf as
  SPACE; hence רב שקה = two tokens). Never assert maqaf in quoted spans;
  quote spans from the source bytes, never retype.
- **accent_stripped RETAINS meteg (U+05BD)**: it strips cantillation
  U+0591-05AF only. Disclose the tier you matched at.
- **Final-letter allography (ך ם ן ף ץ) is preserved exactly** — sweep per
  attested spelling — **including the MEDIAL final-mem at MT 9:6 (לםרבה)**.
- **SHELL-TRANSIT HAZARD** (scope: ANY pointed Hebrew through a shell):
  shells can silently LOSE accent codepoints. Pass pointed queries via
  subprocess argv from a JSON-held source splice, or write the quote to a
  file; trust only accent_stripped/skeleton tiers for anything typed
  through a shell.
- QUOTE CONVENTION book-wide: curly double quotes are for WEB text ONLY;
  quote row/tool wording in straight quotes.
- COPY-DEGRADATION HAZARD (OL-c26 class): even a model-authored copy of
  pointed Hebrew inside your own draft can degrade byte→nfd. Never re-key
  AND never copy-through-your-own-text: splice programmatically from
  verse_map_oshb.json every time, then re-collate your own output. ASCII
  punctuation INSIDE spliced Hebrew runs is invisible to the suite (the
  comma-splice class, Song spot s6) — read the normalize dry-run alongside
  collate on every splice.
- K/Q: 49 verses — check pmarks kq before counting or slicing in any of
  them (list in ../pmarks_Isa.json; 9:2 and 9:6 are IN ZONE A).

## Standing rules (campaign governance; Esth a-g + Job a-j + Ps a-k + Prov a-k + Eccl a-k + Song a-k applied)
- Tier-4 metadata (chapter/verse numbers, WEB headings/footnotes, modern ¶
  and poetry-line breaks, WEB strong= attrs) is NEVER boundary evidence and
  NEVER counterevidence by absence. The WEB mid-verse paragraph opens after
  massa headers are LAYOUT, not structure.
- Quote the original language for every boundary-relevant original-language
  claim; cite the tier when you cite a non-textual signal. TIER-LABEL every
  recurrence claim at write time; "verbatim/byte-identical" only per
  collate truth WITH the tier named (TIER-DISCLOSURE STANDARD, Eccl B-4
  campaign law: a skeleton-tier cohesion driver satisfies the byte-grounded
  bar ONLY with the tier honestly named).
- SEAM-PAIR CURES ARE ONE EDIT; REPLACEMENT WARRANTS MUST PASS THE TEST THAT
  KILLED THE ORIGINAL; QUOTE/GLOSS PARITY REPAIRS RE-CUT THE GLOSS.
- observed_substrate_signals IS A DEPENDENT FIELD of every driver swap;
  driver swaps also re-open rejected_alternative, unit_type, confidence.
  **oss FIELD CONTRACT (Eccl lesson c; Song-proven day-one mandate):
  entries use the dotted signal-key taxonomy (oracle_frame.*,
  speech_formula.*, massa_header.*, woe_series.*, servant_song.*,
  narrative_frame.*, superscription.*, refrain.*, remnant_family.*,
  divine_title.*, parashah.*-style keys); staged-file names/stems are
  BARRED in EVERY field.**
- CROSS-SEAM COHESION: a byte-true device straddling the row's own seam
  argues continuity against the row unless disclosed (the stretched-hand
  refrain across 5:25|9:11ff and the woe-series chains make this LIVE).
- SYMMETRY completion is a SWEEP, not a spot fix — for parashah marks (209
  marked verses!) and every other disclosure object; sweep BEFORE
  postcheck (Song lesson k: a 3-site remainder cost a BLOCKING verdict).
- SEMANTIC-CLASS COUNT DISCIPLINE: name the swept object FIRST (spelling vs
  term vs formula vs construction vs speech-role vs frame-owner), then
  count; blended sweeps forbidden.
- unit_type uses the CONTROLLED VOCABULARY declared in the writer brief —
  no free-text unit types (vocabulary set at the Isa owner gate).
- ENGAGEMENT CLASS (Prov lesson g, reinforced through Song): pointed
  splices + tier labels are MANDATORY for every boundary-relevant Hebrew
  claim.
- REGISTER PURGE: NO decision-ids, strategy-file/§ citations, erratum
  narration, positional row references, file-order talk, review-actor
  names, TOOL FILENAMES, **or staged-file names/stems in ANY field** in row
  prose EVER; the "(sweep: N verses)" convention is the one sanctioned
  citation shorthand. Cross-row references are verse-anchored.
- rejected_alternative: one sentence, PLUS an optional second sentence ONLY
  when it carries the mandated rival disclosure. No third sentence.
- Mandated recurring sentences ship with VARIATION ORDERS: 4+ distinct
  formulations, pooled pre-check.
- HAIKU BATCH CEILING: single-agent generative work degrades at ~50+ items —
  slice at <=50 with distinctness + no-generic rules.
- DISK-DERIVED LAUNCH SETS; MUTATE-THEN-LAUNCH IN SEPARATE TURNS; FIX-AGENTS
  RUN THE FULL SUITE; collision/comparison cites get CONTENT-match
  verification; peers verify OBJECTS and tiers, not digits; file-to-file
  splice + ref-scoped re-splice as packet POST-PROCESSING; heuristic flags
  are CANDIDATES, triaged by content not volume; BOSS consequence rows are
  enumerated PER-RULING in author launch messages AND authors read the full
  ledger consequence text; **boundary-proposal triage is CONTENT-READ on
  every remedy, never keyword-matched (Song B-5 law — the "extend the
  exchange" class escapes keyword nets); author-refusal discipline is
  ratified law (a remedy's embedded boundary change is never author work)**.
- BRIEF HYGIENE (Prov lesson c): briefs carry FULL absolute paths for
  worktree reads + the explicit forbidden-lane list (M1..M7); existence-
  check of your own output file is permitted; "your ONLY SP write is your
  one deliverable — no debug files anywhere under SP, including during
  self-check."
- INFRASTRUCTURE (Song lesson h): on any kill class (connection-lost,
  host-process exit, stream-watchdog), verify the deliverable path is
  EMPTY, resume-in-place with the SAME attempt id; on any cold
  notification, trust DISK STATE only.
- If you find yourself building a tool, STOP — it exists here or you don't
  need it.
