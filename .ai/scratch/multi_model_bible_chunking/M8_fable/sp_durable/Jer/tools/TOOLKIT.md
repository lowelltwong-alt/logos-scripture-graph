# Jer shared verification toolkit (m8-mesh-r3, built Phase 0 by the orchestrator)

**USE these tools. Do NOT rebuild, copy, or re-derive any of them.** Every brief
points here. Work in a UNIQUELY-NAMED private subdirectory of YOUR OWN session
scratchpad — never write scratch into SP/Jer or at any scratchpad root, and no
debug files anywhere under SP, including in SP output directories during
self-check.

Run everything with `PYTHONIOENCODING=utf-8 python <tool> ...` from this directory.

## Book facts (Phase 0 verified — trust these; do not re-derive)

### Numbering: NOT IDENTITY — ONE offset zone, pure renumbering, NO split (byte-PROVEN)
WEB 1,364 verses / MT 1,364, 52 chapters — EQUAL totals:

- **ZONE (chs 8-9):** **MT 8:23 = WEB 9:1** ("Oh that my head were waters …
  spring of tears" — the weeping-prophet line); **MT 9:1-25 = WEB 9:2-26**.
  WEB ch 8 = 22 vv / MT 23; WEB ch 9 = 26 / MT 25.

Every other chapter is identity. The crosswalk is **INJECTIVE** — every WEB
verse has exactly ONE MT counterpart and vice versa (no Isa-style split
anywhere; equal totals exclude it arithmetically). Proof layers
(../web_mt_offset_map.json): per-chapter count equality UNDER THE RULE SET
from both witnesses' bytes; 1,829 automatic content anchors agreeing at the
CROSSWALK-mapped refs (32 in-zone; all 21 misses byte-reviewed as
spelling/lexeme/inflection divergences at identity refs — zero unexplained,
zero in-zone); FALSIFICATION probes showing identity fails 27 anchor checks
inside the zone (under identity WEB 9:26 has NO MT 9:26 at all); and seam
byte-review assertions incl. identity at both zone edges (MT 8:22
balm-in-Gilead; MT 10:1 hear-the-word). **The OSHB KJV-variance note layer
is EMPTY for Jer despite a real zone (the FOURTH book running: Eccl, Song,
Isa, Jer) — absence of notes proves NOTHING.** There are NO title
pseudo-verses — **Jer.N.0 is always invalid**; Jer 1:1 (the divrei-Yirmeyahu
superscription) is an ordinary counted verse in BOTH witnesses.

Convention: bare/web: refs and row spans = WEB; oshb:/pmarks = MT.
**OFFSET-ZONE RULE (Tier-0 ENFORCED): any structured ref touching WEB ch 9
(web: side) or MT 8:23 / MT ch 9 (oshb: side) MUST carry an explicit dual
or numeric qualifier (`web:Jer.9.1 = oshb:Jer.8.23`, or `(MT 9:3)` after a
web: ref) — bare coordinates are ambiguous across witnesses exactly there.**
Elsewhere duals stay optional, but any WRITTEN dual/qualifier must be
arithmetically right — machine-checked by `citation_sweep.py`. Single-verse
spans use the full X-X form (`Jer.5.24-Jer.5.24`) — machine-checked. Use
`jer_lib.web_to_mt()/mt_to_web()` ALWAYS — never hand-assume, in either
direction. (Tool-prose note: `PSALM_RULES` keeps its historical Ps-lineage
name, and older shared-tool docstrings say "psalm" where they mean
"chapter" — read them so.)

### Cross-tradition note — JEREMIAH IS THE CAMPAIGN'S FLAGSHIP CASE
LXX Jeremiah is FAMOUSLY divergent: roughly **one-eighth shorter**, with the
oracles-against-nations block placed **after 25:13** and internally
re-ordered; 4QJer-b/d attest a short Hebrew text type; blocks like
33:14-26, 39:4-13, and the 52:28-30 exile counts are absent from the LXX.
**NONE of that touches this campaign's two witnesses**: WEB and MT both
follow the MT arrangement, and their ONLY numbering divergence is the chs
8-9 seam above. ALL LXX/Old Greek/Septuagint/Vulgate/Peshitta/Targum/DSS/
Qumran material — **including 4QJer-b/d** — is cross-tradition METADATA in
prose, never boundary evidence, never counterevidence, never a
boundary_evidence_refs entry (`citation_sweep.py` guards). **The 2 Kgs
24:18-25:30 parallel to ch 52 (and the 2 Kgs 18-20 ‖ Isa 36-39 precedent's
law) is intra-canon synoptic metadata: typed-relation territory, NEVER
boundary evidence for Jeremiah's seams.** Numbering-tradition comparisons
in prose need an explicit crosswalk statement.

### LANGUAGE — ONE ARAMAIC VERSE (a first for the campaign's Prophets)
**MT 10:11 = WEB 10:11 (identity numbering) is Aramaic** — a self-contained
island inside the ch-10 idol polemic (byte-proven: 15 A-prefixed OSHB morph
codes, all in that verse; the other 21,961 codes are H-prefixed; 10:10 and
10:12 are Hebrew). `check_language_zones.py` enforces three arms: an
Aramaic label on any OTHER verse flags; a Hebrew label on 10:11 flags; and
**any ROW whose span covers WEB 10:11 must disclose the island** (Tier-0
symmetry arm). `collate.py` reports `language: Aramaic` for that window.

### PARASHAH LAYER — the campaign's LARGEST (MT-keyed)
WLC Jer carries **58 petuchah (PE) + 246 setumah (SAMEKH) segs over 303
marked verses** (../pmarks_Jer.json, byte-extracted) — surpassing Isa's
209-verse layer. In the PROPHETS this is **TIER-3 WEAK corroboration**
(owner addendum: parashah_in_prophets_or_writings): never a boundary
driver, single-witness disclosure required on every citation, PE never
conflated with SAMEKH. Absence is NEVER counterevidence. The span-relevant
mark-disclosure SYMMETRY sweep (check_marks rule 2) is the heaviest of the
campaign — stage the pmarks read in every writer/author workflow.

### Fabrication classes for Jer (hard errors)
- **selah** — Psalter device; zero occurrences in Jer (byte-swept).
- **reversed/inverted nun, suspended letter** — no such segs in WLC Jer.
- **LARGE letters — NONE in WLC Jer**: any large-letter/majuscule claim is
  a fabrication.
- **SMALL letters — exactly ONE: the small NUN (x-small) at MT 39:13** (in
  the Nebuzaradan officer list; the seg content carries its accent mark in
  the source bytes). A small-letter claim anywhere else is a fabrication;
  at 39:13 it needs single-witness disclosure.

### Disclosure inventories (../pmarks_Jer.json, MT-keyed)
- **Paseq**: 157 segs over 146 verses — seg layer, NOT quotable verse
  bytes; citable from the inventory only; "(single-witness)" required;
  COUNT-ONLY — intra-verse position claims are unsourceable (WARN arm).
- **Ketiv/qere: 141 notes over 124 verses — the campaign's LARGEST K/Q
  inventory by a wide margin** (Isa's 53/49 was the previous record).
  **ONE sits INSIDE the offset zone: MT 9:7 (= WEB 9:8).** Twelve
  doubled-note verses: MT 3:19, 4:19, 6:25, 13:20, 14:14, 22:23, 48:7,
  48:20, 49:39, 50:6, 50:11, 51:34. Check pmarks kq before counting or
  slicing in ANY K/Q verse. **The 49:28 K/Q rides on the KING'S NAME**
  (see the hazard catalog).
- **OSHB exegesis notes** at MT 29:23 and MT 48:44 — single-witness
  apparatus, not text bytes.
- **Morph tally**: 21,961 H + 15 A codes; the A codes are all in 10:11.

### PROPHETIC FRAME SPINE (../jer_device_inventory.json — the tier-1 seam skeleton)
Byte-swept (every count NAMES its object; verse counts, MT keys):
- **WORD-EVENT FORMULAS — the book's primary macro-seam device, THREE
  shapes, never blended**: `vayehi debar-YHWH` 21 verses (20 verse-initial;
  the ONE non-initial is 42:7, after the ten-days wait), `ha-davar asher
  hayah el-Yirmeyahu` 11 verses (the prose-sermon superscription shape:
  7:1, 11:1, 18:1, 21:1, 30:1, 32:1, 34:1, 34:8, 35:1, 40:1, 44:1 — 25:1 is
  NOT a member: its bytes read `asher hayah AL-Yirmeyahu` (ayin-lamed,
  "concerning"), a one-site AL-variant davar header, its own count object;
  E-03-instance correction 2026-08-28, byte-verified),
  `asher hayah debar-YHWH el-Yirmeyahu` 4 verses (the OAN/topical header
  shape: 14:1 drought, 46:1 nations rubric, 47:1 Philistines, 49:34 Elam).
- **koh-amar census: 153 verses** — 152 `koh amar YHWH` (50 with tsevaot)
  + ONE `koh amar ADONAI YHWH` stack (7:20). **FRAME-OWNERSHIP HAZARD,
  harder than Isa's chs 36-37: HANANIAH speaks the full divine formula
  (koh amar YHWH tsevaot) as a false prophet (28:2, 28:11), and chs 27-29
  letters/confrontations embed formulas inside quoted speech. A koh-amar
  digit that does not name WHOSE MOUTH carries the formula is
  meaningless.**
- **neum-YHWH: 162 verses — the OT's densest concentration** (169 verses
  carry the neum token). Stack shapes: `neum adonai YHWH (tsevaot)` (2:19,
  2:22, 49:5, 50:31); **`neum ha-melekh YHWH tsevaot shemo` — "says the
  King, whose name is YHWH of Armies" — an OAN-zone signature (46:18,
  48:15, 51:57)**. **VERB TRAP: 23:31 carries BOTH the divine formula AND
  the book's only occurrence of the VERB na'am (vayin'amu ne'um, of the
  false prophets)** — a bare neum sweep blends noun and verb there. At 162
  verses the formula is too dense to drive boundaries verse-by-verse:
  closure corroboration, and role-split before any digit.
- **Date/reign headers**: 19 candidate sites — the bishnat/bashanah token
  sweep PLUS the bet+cardinal shape (E-03-instance correction 2026-08-28:
  the year word follows a bet-prefixed cardinal, needle-invisible before) —
  classified in the inventory (verse-initial date frames 28:1, 36:1, 36:9,
  39:1, **39:2 (bet+cardinal: "in the eleventh year")**, 52:4, 52:29,
  52:30, 52:31; header-internal dates **1:2 (bet+cardinal, inside the
  superscription)**, 25:1, 32:1, 45:1, 46:2, 51:59, 52:28; narrative date
  28:17; NOT dates: 17:8 year-of-drought simile, 51:46 year-by-year rumor;
  adjacent shapes OUTSIDE this object, per-site reads: 52:1 regnal-age
  formula, 52:5 mid-narrative duration, 52:12 month-first notice with
  mid-verse year; שְׁנַת at 51:39/51:57 is the SLEEP noun homograph and
  שנים at 52:20 is "twelve" — never year digits) + `bereshit mamlekhet` at THREE byte-verified sites in two
  spellings (E-03-instance correction 2026-08-28): 26:1 mamlekhut (vav
  plene) verse-initial, 27:1 mamlekhet verse-initial, 28:1 mamlekhet
  MID-VERSE after vayehi-bashanah-hahi. NOT a member: 49:34's `bereshit
  malkhut Tsidqiyahu` — malkhut (מלכות) is a DIFFERENT noun form from
  mamlekhet/mamlekhut (byte-checked 2026-08-28); a per-site read, its own
  object.
  The dated-prose spine of chs 21-45 + 52.
- **OAN headers**: SIX lamed-initial nation headers (46:2 Egypt, 48:1
  Moab, 49:1 Ammon, 49:7 Edom, 49:23 Damascus, 49:28 Kedar/Hazor) + four
  non-lamed shapes (46:1 rubric, 47:1 Philistines, 49:34 Elam, 50:1
  Babylon `hadavar asher dibber`). 51:16 `le-qol` is a FALSE lamed
  candidate (at-the-sound phrase).
- **hoy: 7 bare verses + the VAV-PREFIXED shape** — role split BEFORE any
  digit: woe-oracle onsets 22:13, 23:1 (+ 48:1 inside the Moab header
  verse, 50:27 after the battle call); day-alas 30:7; funeral cries 22:18
  (fourfold — bare AND vav-prefixed in one verse) and 34:5 (ve-hoy ONLY —
  invisible to a bare-token sweep); the 47:6 sword apostrophe. אוי is a
  different lexeme (10 verses).
- **Divine names**: YHWH in 604 verses; YHWH-tsevaot 71; **the FULL stack
  `YHWH tsevaot Elohei Yisrael` in 32 verses — a Jer signature, its OWN
  count object**; adonai-skeleton token in 13 verses, POINT-AWARE
  split (E-03-instance correction 2026-08-28): **11 divine-title sites
  (qamats) + 2 courtly adoni sites (hiriq): 37:20 and 38:9, the human "my
  lord the king" addressed to Zedekiah — the courtly role-split IS live in
  Jer's narrative zone**, exactly the Isa pattern; name the form before
  any adonai digit. **PREFIXED la-adonai is its OWN token object (second
  E-03-instance correction 2026-08-28, writer-caught): 46:10 (twice in
  the verse) + 50:25, both divine-title stacks, both OAN-block — a
  bare-token adonai sweep never sees them.**
- **The 51:64 COLOPHON**: "Thus far are the words of Jeremiah" closes ch
  51 — **the book's own colophon stands BEFORE the ch-52 appendix** (= 2
  Kgs 24:18-25:30 parallel). A first-order macro-structure byte fact.
- **Named figures** (spelling variants are the hazard — see catalog):
  Jeremiah 109 long + 8 short-spelling verses; Zedekiah 44 + 4; Jehoiakim
  22 + 1 defective (27:1!); Jehoiachin = THREE name forms (Jehoiachin
  52:31; Jeconiah 24:1, 27:20, 28:4, 29:2; Coniah 22:24, 22:28, 37:1);
  Gedaliah 19 + 4; Baruch 23 (chs 32, 36, 43, 45 — and the token also
  reads "blessed": 17:7, 20:14 are the participle, NOT the scribe);
  Hananiah, Pashhur, Rachel (31:15) per inventory.
- **Chapter texture table** (chapter_texture rows): per-chapter poetry
  share + koh-amar/neum/word-event/YHWH densities — staging profile for
  the at-scale part plan; writers re-derive, never row evidence. 517 of
  1,364 WEB verses open poetry lines (prose-heavier than Isa); 21
  paragraph-continuation folds are LIVE, clustered in the narrative
  chapters (1:11/13, 24:3, 32:8, 36:14-15, 37:14/17, 38:12, 40:5/14,
  41:8, 44:25, 52:3/27-30 among them).

## SWEEP HAZARD CATALOG (E-11 discipline — every class byte-verified in Jer)
- **ירמיהו contains רמיה (THE Jer trap)**: the deceit/slackness noun
  remiyyah (48:10 "does the work of YHWH with slackness") is a consonantal
  SUBSTRING of the prophet's name (yod+resh-mem-yod-he+vav) — a bare
  substring sweep for the noun matches inside every one of the 109+
  name occurrences. AND the short spelling ירמיה (8 verses) is itself a
  substring of the long form — **token-bound sweeps only, per attested
  spelling**.
- **Nebuchadnezzar has FOUR live spellings**: nun-resh family נבוכדראצר
  (29 vv, dominant) + its PLENE byform נבוכדראצור at 49:28 — **standing
  beside the usual spelling in the SAME verse as a K/Q doubled token
  (check pmarks kq before slicing 49:28)**; nun-nun family נבוכדנאצר
  (6 vv, clustered chs 27-29) + its vav-less defective נבכדנאצר (28:11,
  28:14). Name-form claims name their spelling.
- **Jehoiachin/Jeconiah/Coniah**: ONE king, THREE name forms + spelling
  variants — name the form before any digit. 27:1 carries DEFECTIVE
  Jehoiakim in the famous setting crux (the chapter's events are under
  Zedekiah; the MT name stands — a held question, never silently
  "corrected").
- **Shiloh spelling varies BY SITE**: בשילו 7:12 / לשלו 7:14 / כשלה 26:6 /
  כשלו 26:9 / משלו 41:5 — THREE spellings across five sites, and the
  bases collide with kashal (stumble: 6:21, 46:6, 46:12 lookalikes),
  shalu (prosper: 12:1), and mashal forms (30:21). Per-site byte reading
  before any Shiloh digit.
- **koh-amar frame ownership**: divine vs QUOTED-PROPHET (Hananiah!) vs
  letter-embedded — name the mouth (the Isa i2 lesson, harder here).
- **neum noun-vs-verb**: 23:31 (above); and the melekh-signature stack is
  its own object.
- **שקר (falsehood, 34 vv) vs שקד (almond) / שקד (watching)**: the 1:11-12
  call-vision PUN pair (shaqed/shoqed — byte-verified in both verses); a
  2-letter-overlap sweep blends the keyword and the pun.
- **שוב return/turn family**: Jer's signature wordplay (3:1-4:4 cluster;
  meshuvah "faithlessness" 5 vv) — the root inflects far beyond any
  needle and the staged tools carry NO morphology layer: every root-level
  claim needs its own per-form sweep with the form named (bare/prefixed
  token = only 8 vv — that digit is NOT "the shuv motif").
- **hoy shapes**: bare vs vav-prefixed (34:5 invisible to bare sweeps);
  woe vs funeral cry vs day-alas vs sword apostrophe.
- **OFFSET-ZONE COUNTING**: any per-chapter digit touching chs 8-9 must
  NAME its numbering space (e.g. the weeping verse is MT 8:23 = WEB 9:1;
  the zone K/Q verse is MT 9:7 = WEB 9:8).
- **K/Q before slicing**: 124 K/Q verses (largest inventory of the
  campaign) — check pmarks kq before counting or slicing in ANY of them;
  twelve doubled-note verses; the 49:28 royal-name K/Q.
- **Mater-lectionis / plene-defective pairs are LIVE**: Jerusalem PLENE
  ירושלים at 26:18 (vs the usual defective); Jacob PLENE יעקוב at 30:18 +
  51:19; Jehoiakim defective at 27:1; Anathothite gentilic הענתתי 29:27 —
  sweep per attested spelling (the anchor review's live classes).
- **tirosh vs yayin**: 31:12 "new wine" renders tirosh — lexeme-distinct
  from yayin; name the object in any wine digit.
- **בבל density**: Babylon saturates chs 20-52 (plus מבבלה directional and
  כשדים Chaldeans as separate objects) — Babylon digits name their token.

## Data files (consume directly)
- `verse_map_web.json` — WEB ref → {text, clean, para_before,
  continuation_paragraphs, poetry_lines, language, mt}; **language is
  "Aramaic" exactly at Jer.10.11**; 517 of 1,364 verses open poetry lines;
  21 continuation-paragraph folds LIVE (token audit 1364/1364 PASS
  against raw USFM).
- `verse_map_oshb.json` — MT ref → {text (full pointed), language, web}.
- `consonantal_index.json` — MT ref → {skeleton, accent_stripped, nfd,
  language}.
- `../pmarks_Jer.json`, `../jer_device_inventory.json`,
  `../web_mt_offset_map.json`, `../verse_inventory.json`.
- WEB Jer carries ZERO editorial apparatus lines (no [HEADING]/[SPEAKER]/
  [SUPERSCRIPTION]/[MAJOR-SECTION]); 11 [fn …] footnote sites inline
  (norm_english strips them).

## Tools
| Tool | Purpose |
|---|---|
| `collate.py --ref oshb:Jer.C.V --quote "…"` | Hebrew/Aramaic quote tier: byte / nfd / accent_stripped / skeleton / none. Only **byte** is quotation-grade for pointed text. Bare/web: refs are crosswalk-mapped to MT internally. Reports the window's language (Aramaic at 10:11). |
| `check_web_quotes.py FILE...` | Verbatim check of curly-quoted English near web: refs. CURLY QUOTES + an inline web: ref in the SAME field are MANDATORY at every layer. **E-15 ARMS (new): unbalanced/broken curly pairing; Hebrew inside curly quotes; WEB text in straight quotes.** The neighbor-only WARN arm is LIVE in WEB chs 8-9. |
| `check_refs_mirror.py ROWS...` | Every verse argued in prose OUTSIDE the row's own span must appear in boundary_evidence_refs — INCLUDING bare "verse N"/"vv. N-M" mentions resolved against the row's span chapter. Witness-prefix-aware; injective crosswalk. |
| `check_marks.py ROWS...` | Jer pivot: selah/reversed-nun/suspended/LARGE-letter claims = fabrication; SMALL-letter claims validated against the ONE x-small site (MT 39:13); petuchah/setumah claims validated under the claimed TYPE (PE≠SAMEKH) at MT keys (dual-reading in the zone); UNCONDITIONAL span-relevant mark-disclosure symmetry (DENSEST layer of the campaign); K/Q claim validation; paseq-position WARN. |
| `citation_sweep.py ROWS` | Ref validity incl. RANGE ENDS and X-X span form, CROSSWALK dual-cite arithmetic, **offset-zone disclosure enforcement**, mark/paseq/K-Q/special-letter claims vs inventories at MT keys, witness disclosure, LXX/DSS/4QJer guard, selah + large-letter bans, Hebrew-quote-to-cited-ref byte binding (nfd_degraded is HARD at the suite level — E-01). |
| `sweep.py --heb/--skel/--web Q [--tokens]` | Book-wide occurrence sweep. **Counts are VERSE counts** unless --tokens; every citation NAMES its unit and carries A DIGIT. --skel is contiguous consonantal SUBSTRING search — see the hazard catalog before trusting any short-token digit. |
| `jer_devices.py` | Rebuilds ../jer_device_inventory.json (orchestrator-run; agents consume the JSON). |
| `ngram7.py ROWS` | Cross-row authorial 7-gram templating gate (≥10 rows = RED), WEB-quotation-aware; unit_type/parent_collection/writer_*/wj_or_red_letter_considered/review_status/book/model_id excluded (p1/p2/p4/i4 lineage). |
| `check_universals.py FILE...` | Flags universal claims lacking an adjacent DIGIT-BEARING sweep count in-sentence. **E-16 (new): exclusivity claims (only/sole/unique/never/exclusively/nowhere/no other) are NEVER tier-dampened — a tier label proves the quote, not the exclusivity.** |
| `check_language_zones.py FILE...` | THREE arms: Aramaic label outside 10:11; Hebrew label on 10:11; **island-disclosure symmetry (a row spanning WEB 10:11 must say Aramaic)**. |
| `cap_sweep.py ROWS` | **Tier-0 HARD (E-02, new)**: whole-chapter rows must sit at medium_low/low + frontier flag + cap disclosure (count + phrase). |
| `check_register.py ROWS` | **FLAGS member (E-06 + E-18 residual arms, new)**: workflow/administrative language in row prose — positional-row ("that row") and cross-part arms, decision-ids, tool filenames, review actors, erratum/repair narration, session/wave talk, strategy citations, staged-file stems. Flags are triage candidates (E-12 law). |
| `normalize_hebrew_in_json.py [--write] FILE...` | Byte-splices NFD-equivalent Hebrew runs to source bytes (MIN_LEN=2). NEVER hand-type Hebrew — slice from verse_map_oshb.json. **A dry-run fixed count > 0 is a HARD failure at the suite level (E-01).** |
| `check_tiling.py FILE --range Jer.a.b-Jer.c.d` | Exact tiling of a WEB range: gaps/overlaps/order. |
| `check_atomic_isolation.py ROWS` | **STAGED, NOT ARMED** (p3-guarded output path): atomic-row neighbor-isolation validator + scoped-mesh cluster builder. ATOMIC_TYPES is pinned AFTER the owner gate; unarmed = every row model-reviewed. Crosswalk-aware (WEB 9:1 fetches MT 8:23 bytes — smoke-proven DISCRIMINATING via the ammi share). |
| `run_validator_suite.py ROWS [--reviews F...]` | Full Tier-0 suite (10 members) + consolidated report. HARD: citation_sweep, ngram7, **nfd (E-01)**, **cap_sweep (E-02)**. FLAGS: web_quotes, refs_mirror, mark_symmetry, universals, language_zones, **register**. |

### NO MORPHOLOGY LAYER in the staged extract
verse_map_oshb.json carries text/language/web only. Form claims (gender of
a suffix or verb, jussive, participle) CANNOT be machine-verified with the
staged tools — argue them from the pointed bytes plus both witnesses'
renderings; form-class labels are byte-checkable claims and get the same
discipline as digits.

## Encoding + skeleton notes (READ before quoting Hebrew)
- **The staged extract is MAQAF-FREE at every tier** (byte-verified: 0 ×
  U+05BE across all 1,364 MT verses — the extractor serialized maqaf as
  SPACE; the OSHB XML's 3,471 x-maqqef segs all became spaces). Never
  assert maqaf in quoted spans; quote spans from the source bytes, never
  retype.
- **accent_stripped RETAINS meteg (U+05BD)**: it strips cantillation
  U+0591-05AF only. Disclose the tier you matched at.
- **Final-letter allography (ך ם ן ף ץ) is preserved exactly** — sweep per
  attested spelling; build every hand-written needle FINALS-NORMALIZED
  (E-11: this discipline caught the orchestrator's own fixtures again at
  Jer Phase 0 — the 28:11 Nebuchadnezzar hypothesis and the vav-prefixed
  hoy at 22:18/34:5 were both corrected by the bytes).
- **SHELL-TRANSIT HAZARD** (scope: ANY pointed Hebrew through a shell):
  shells can silently LOSE accent codepoints. Pass pointed queries via
  subprocess argv from a JSON-held source splice, or write the quote to a
  file; trust only accent_stripped/skeleton tiers for anything typed
  through a shell.
- QUOTE CONVENTION book-wide: curly double quotes are for WEB text ONLY
  (E-15b enforces); quote row/tool wording in straight quotes; Hebrew is
  spliced bare, never inside curly doubles.
- COPY-DEGRADATION HAZARD: even a model-authored copy of pointed Hebrew
  inside your own draft can degrade byte→nfd. Never re-key AND never
  copy-through-your-own-text: splice programmatically from
  verse_map_oshb.json every time, then re-collate your own output. ASCII
  punctuation INSIDE spliced Hebrew runs is invisible to the suite —
  read the normalize dry-run alongside collate on every splice. **nfd
  degradation is HARD at the Jer writer gate (E-01).**
- K/Q: 124 verses — check pmarks kq before counting or slicing in any of
  them (list in ../pmarks_Jer.json; MT 9:7 is IN the zone; 49:28 rides on
  the king's name).

## Standing rules (campaign governance; Esth a-g + Job a-j + Ps a-k + Prov a-k + Eccl a-k + Song a-k + Isa lessons applied)
- Tier-4 metadata (chapter/verse numbers, WEB headings/footnotes, modern ¶
  and poetry-line breaks, WEB strong= attrs) is NEVER boundary evidence and
  NEVER counterevidence by absence.
- Quote the original language for every boundary-relevant original-language
  claim; cite the tier when you cite a non-textual signal. TIER-LABEL every
  recurrence claim at write time; "verbatim/byte-identical" only per
  collate truth WITH the tier named (Eccl B-4 campaign law). **E-16: a tier
  label NEVER substitutes for an exclusivity sweep.**
- SEAM-PAIR CURES ARE ONE EDIT; REPLACEMENT WARRANTS MUST PASS THE TEST THAT
  KILLED THE ORIGINAL; QUOTE/GLOSS PARITY REPAIRS RE-CUT THE GLOSS.
- observed_substrate_signals IS A DEPENDENT FIELD of every driver swap;
  driver swaps also re-open rejected_alternative, unit_type, confidence.
  **oss FIELD CONTRACT: entries use the dotted signal-key taxonomy
  (word_event.*, speech_formula.*, oan_header.*, date_frame.*,
  narrative_frame.*, superscription.*, refrain.*, lament_frame.*,
  divine_title.*, symbolic_act.*-style keys); parashah.* keys are BARRED
  from oss (the Isa p09 window-collision law); staged-file names/stems are
  BARRED in EVERY field.**
- CROSS-SEAM COHESION: a byte-true device straddling the row's own seam
  argues continuity against the row unless disclosed.
- SYMMETRY completion is a SWEEP, not a spot fix — for parashah marks (303
  marked verses!), the Aramaic island, and every other disclosure object;
  sweep BEFORE postcheck.
- SEMANTIC-CLASS COUNT DISCIPLINE: name the swept object FIRST (spelling vs
  term vs formula vs construction vs speech-role vs frame-owner vs name
  form), then count; blended sweeps forbidden.
- unit_type uses the CONTROLLED VOCABULARY declared in the writer brief —
  no free-text unit types (vocabulary set at the Jer owner gate).
- ENGAGEMENT CLASS: pointed splices + tier labels are MANDATORY for every
  boundary-relevant Hebrew claim.
- REGISTER PURGE (Tier-0-swept by check_register.py): NO decision-ids,
  strategy-file/§ citations, erratum narration, positional row references
  (incl. "that row"), cross-part references, file-order talk, review-actor
  names, TOOL FILENAMES, session/wave talk, or staged-file names/stems in
  ANY field in row prose EVER; the "(sweep: N verses)" convention is the
  one sanctioned citation shorthand. Cross-row references are
  verse-anchored. Self-reference ("this unit") is exempt.
- rejected_alternative: one sentence, PLUS an optional second sentence ONLY
  when it carries the mandated rival disclosure. No third sentence.
- Mandated recurring sentences ship with VARIATION ORDERS: 4+ distinct
  formulations, pooled pre-check.
- HAIKU BATCH CEILING: single-agent generative work degrades at ~50+ items —
  slice at <=50 with distinctness + no-generic rules.
- DISK-DERIVED LAUNCH SETS; MUTATE-THEN-LAUNCH IN SEPARATE TURNS; FIX-AGENTS
  RUN THE FULL SUITE; collision/comparison cites get CONTENT-match
  verification; peers verify OBJECTS and tiers, not digits; boundary-
  proposal triage is CONTENT-READ on every remedy, never keyword-matched;
  author-refusal discipline is ratified law (a remedy's embedded boundary
  change is never author work); **consolidation MUST emit an explicit
  corpus_wide_orders list beside the per-row docket, each carried to
  execution as its own sweep (E-18)**; **the B-8 LF-SUPPORT AUDIT LANE runs
  BY DEFAULT in the rev/spot round**.
- BRIEF HYGIENE: briefs carry FULL absolute paths for worktree reads + the
  explicit forbidden-lane list (M1..M7); existence-check of your own output
  file is permitted; "your ONLY SP write is your one deliverable — no debug
  files anywhere under SP, including during self-check."
- INFRASTRUCTURE (E-13/E-14): on connection-lost / host-process exit /
  stream-watchdog kills, verify the deliverable path is EMPTY, then
  resume-in-place with the SAME attempt id; orphaned deliverables get
  VALIDATED, never re-run. On an api-filter-misfire kill ([bio]-class
  false positive), NEVER resume-in-place — FRESH relaunch with the
  research-context preamble (carried in EVERY launch message; it mitigates
  but does not immunize). On any cold notification, trust DISK STATE only.
- If you find yourself building a tool, STOP — it exists here or you don't
  need it.
