# Song shared verification toolkit (m8-mesh-r3, built Phase 0 by the orchestrator)

**USE these tools. Do NOT rebuild, copy, or re-derive any of them.** Every brief
points here. Work in a UNIQUELY-NAMED private subdirectory of YOUR OWN session
scratchpad — never write scratch into SP/Song or at any scratchpad root, and no
debug files anywhere under SP, including in SP output directories during
self-check iteration.

Run everything with `PYTHONIOENCODING=utf-8 python <tool> ...` from this directory.

## Book facts (Phase 0 verified — trust these; do not re-derive)

### Numbering: NOT IDENTITY (byte-PROVEN — the expected non-identity was CONFIRMED)
WEB 117 verses / MT 117, 8 chapters — the classic 6:13|7:1 seam is real:
**MT 7:1 = WEB 6:13** ("Return, return, Shulammite!") and
**MT 7:2-14 = WEB 7:1-13**; every other chapter is identity. Proof layers
(../web_mt_offset_map.json): per-chapter count equality UNDER THE RULE SET
from both witnesses' bytes (WEB ch 6 = 13 / MT 12; WEB ch 7 = 13 / MT 14);
104 automatic content anchors agreeing at the CROSSWALK-mapped refs (18 in
the offset zone), the single miss byte-reviewed (WEB 7:2 "mixed wine"
renders המזג, the mixed-drink hapax — rendering divergence, not an offset);
a FALSIFICATION probe showing the identity mapping fails 18 anchor checks
in the zone (WEB 6:13 has NO MT 6:13 at all); and six seam byte-review
assertions. **The OSHB KJV-variance note layer is EMPTY for Song despite
the real offset (exactly as in Eccl) — absence of notes proves NOTHING
here.** There are NO title pseudo-verses — **Song.N.0 is always invalid**;
Song 1:1 (shir ha-shirim, the superscription) is an ordinary counted verse
in BOTH witnesses.

Convention: bare/web: refs and row spans = WEB; oshb:/pmarks = MT.
**OFFSET-ZONE RULE (Tier-0 ENFORCED): any structured ref touching WEB 6:13
or WEB ch 7 (web: side) or MT ch 7 (oshb: side) MUST carry an explicit dual
or numeric qualifier (`web:Song.6.13 = oshb:Song.7.1`, or `(MT 7:3)` after
a web: ref) — bare coordinates are ambiguous across witnesses exactly
there.** Elsewhere duals stay optional, but any WRITTEN dual/qualifier must
be arithmetically right — machine-checked by `citation_sweep.py`.
Single-verse spans use the full X-X form (`Song.2.7-Song.2.7`) —
machine-checked. Use `song_lib.web_to_mt()/mt_to_web()` ALWAYS — never
hand-assume, in either direction. (Tool-prose note: `PSALM_RULES` keeps its
historical Ps-lineage name, and older shared-tool docstrings say "psalm"
where they mean "chapter" — read them so.)

### Cross-tradition note
LXX/Greek numbering FOLLOWS MT at the 6:13/7:1 seam; the English chapter
division follows the Vulgate-family tradition; Greek order matches MT
book-wide. ALL LXX/Septuagint/Old Greek/Vulgate/Peshitta/Targum/DSS/Qumran
material is cross-tradition METADATA in prose — never boundary evidence,
never counterevidence, never a boundary_evidence_refs entry
(`citation_sweep.py` guards). Numbering-tradition comparisons in prose need
an explicit crosswalk statement.

### PARASHAH LAYER RICH — and it shadows the refrain skeleton (MT-keyed)
WLC Song carries exactly **1 petuchah (PE) + 19 setumah (SAMEKH) segs**
(../pmarks_Song.json, byte-extracted): **PE at MT 8:10 only**; SAMEKH at MT
1:4, 1:8, 1:14, 2:7, 2:13, 2:14, 2:17, 3:5, 3:8, 3:11, 4:7, 4:11, 5:1,
6:3, 6:9, 6:10, 7:11, 8:4, 8:7. Note **MT 7:11 = WEB 7:10** (offset zone).
The layer visibly tracks the refrains (SAMEKH at all three adjuration sites
2:7/3:5/8:4 and at the mutual-belonging sites 6:3/7:11) — **the tier does
NOT rise for that**: in the Writings this is **TIER-3 WEAK corroboration**,
never a boundary driver, single-witness disclosure required on every
citation, PE never conflated with SAMEKH; the refrains themselves are the
tier-1 evidence. Absence is NEVER counterevidence. Claims are validated
against the inventory by `citation_sweep.py` (refs) and `check_marks.py`
(prose + span symmetry: every span-relevant mark must be disclosed).

### Fabrication classes for Song (hard errors)
- **selah** — Psalter device; zero occurrences in Song.
- **reversed/inverted nun, suspended letter** — no such segs in WLC Song.
- **small/large letters — NONE AT ALL in WLC Song** (like Eccl): ANY
  special-letter claim at ANY Song verse is a fabrication.
- **YHWH / Elohim citations — BOTH ZERO (byte-swept)**: Song carries no
  plain divine name. The sole Yah-form surface is the MT 8:6 crux (below).

### Disclosure inventories (../pmarks_Song.json, MT-keyed)
- **Paseq**: 12 segs over 12 verses (MT 1:13, 1:14, 2:7, 2:13, 3:5, 3:11,
  4:8, 4:12, 4:14, 5:2, 8:4, 8:14) — seg layer, NOT quotable verse bytes;
  citable from the inventory only; "(single-witness)" required; COUNT-ONLY —
  intra-verse position claims are unsourceable (WARN arm). None in the
  offset zone.
- **Ketiv/qere**: 4 notes over 4 verses (MT 1:17, 2:11, 2:13, 4:9) — the
  SMALLEST K/Q inventory of the campaign so far; **NONE in the offset zone;
  the seam verse MT 7:1 = WEB 6:13 is NOT K/Q-bearing (unlike Eccl's
  seam)**. Check pmarks kq before counting or slicing in ANY K/Q verse.
- **Morph tally**: all 1,255 morph codes H-prefixed — NO Aramaic zones.
  Aramaism/LBH-influence DISCUSSION (the pervasive she- relative — אשר
  appears ONLY in the 1:1 superscription, byte-swept; the Persian loan
  פרדס 4:13) is legitimate; labeling a VERSE as Aramaic is flagged
  (check_language_zones).
- **OSHB exegesis notes** sit at MT 6:12 (the merkavot-ammi-nadiv crux) and
  MT 8:6 (shalhevet-yah) — single-witness apparatus, not text bytes.

### WEB SPEAKER HEADINGS — the Song-specific TIER-4 TRAP
The WEB extract carries **31 [SPEAKER: Lover/Beloved/Friends/...]
apparatus sites** (cataloged in ../speaker_headings_web.json). They are
MODERN EDITORIAL metadata — **owner-addendum TIER 4: NEVER boundary
evidence, NEVER voice-attribution evidence, NEVER counterevidence by
absence.** Voice attribution is argued from the text's own signals per the
owner-gated VOICE-ATTRIBUTION policy: vocatives and address vocabulary
(דודי her-word / רעיתי his-word / כלה / אחתי), grammatical gender of
suffixes and verb forms, the daughters-addresses, and refrain brackets.
The catalog exists ONLY so reviewers can audit a claim AGAINST having
leaned on the headings.

### Voice / frame spine (../song_device_inventory.json — the tier-1 seam skeleton)
Byte-swept (every count NAMES its object; verse counts unless noted):
- **Superscription**: MT 1:1 שיר השירים אשר לשלמה — the book's only header;
  the book's only אשר.
- **dodi exact** (דודי/ודודי/לדודי — her word for him): 24 verses;
  **dod-family** (prefix-tolerant): 28 verses; **דדיך/דדי 'your loves'
  DEFECTIVE spelling: 4 verses (MT 1:2, 1:4, 4:10, 7:13 = WEB 7:12)** —
  escapes every dod-sweep (no vav); **דודאים mandrakes (MT 7:14 = WEB
  7:13)** — dod-adjacent homograph. Three different objects; never blend.
- **rayati** (רעיתי — his word for her): 9 verses (1:9, 1:15, 2:2, 2:10,
  2:13, 4:1, 4:7, 5:2, 6:4). **kallah**: 6 verses (4:8-12 + 5:1).
  **achoti**: 6 verses — but 8:8 אחות is the brothers' little sister, NOT
  the bride epithet; role-split before counting.
- **Adjuration refrain** (השבעתי): exactly 4 sites — MT 2:7, 3:5, 5:8, 8:4
  in THREE attested shapes: 2:7 = 3:5 FULL (daughters + gazelles/does +
  אם תעירו ואם תעוררו); 5:8 = אם תמצאו / מה תגידו variant WITHOUT gazelles;
  8:4 = מה תעירו variant WITHOUT gazelles. **MT 5:9 שהשבעתנו is the
  daughters QUOTING the oath back — same root, different speech role; the
  site count rightly excludes it.**
- **Mutual-belonging refrain**: 3 sites, 3 DIFFERENT shapes — MT 2:16
  דודי לי ואני לו (his-mine), MT 6:3 אני לדודי ודודי לי (mine-his, order
  FLIPPED), **MT 7:11 = WEB 7:10 אני לדודי ועלי תשוקתו (desire variant,
  OFFSET ZONE)**. Quote the attested shape, never a harmonized one.
- **Daughters addresses**: בנות ירושלם adjacent-pair 6 verses (MT 1:5, 2:7,
  3:5, 5:8, 5:16, 8:4); בנות ציון 1 verse (3:11); prefixed מבנות ירושלם at
  3:10 is a FROM-phrase, not an address.
- **she-ahavah nafshi** relative formula: 5 verses (1:7, 3:1, 3:2, 3:3,
  3:4); **ahavah NOUN** (ש-prefix verb form excluded): 10 verses (2:4, 2:5,
  2:7, 3:5, 3:10, 5:8, 7:7 = WEB 7:6, 8:4, 8:6, 8:7).
- **Refrain small-set**: qol dodi 2:8, 5:2; ad-she-yafuach 2:17, 4:6;
  mi-zot ascents 3:6, 6:10, 8:5; semadar 2:13, 2:15, 7:13 (= WEB 7:12);
  henetsu ha-rimmonim 6:11 + 7:13 (TWO spellings: הרמנים defective 6:11,
  הרמונים plene 7:13); foxes 2:15 only (שועלים twice in the verse);
  tsvi-family 7 verses.
- **Shelomo**: 8 verses; **melek-lexeme**: 5 verses (המלך 1:4, 3:9;
  שהמלך 1:12; במלך 3:11; bare מלך MT 7:6 = WEB 7:5) — distinguish from
  מלכות 'queens' (6:8, 6:9) before any king-digit.
- **Wasf zones (derived, runs of >=3 consecutive suffixed-body-part
  verses)**: MT 4:1-5, MT 5:11-14, MT 6:5-7, **MT 7:2-6 (= WEB 7:1-5)**,
  **MT 7:8-7:10 (= WEB 7:7-7:9)** — staging signal ONLY; exact wasf BOUNDS
  are writer territory argued from bytes (openers כלך יפה 4:7-class,
  closures, addressee shifts). The lesson-j guesses 6:4-9 and 7:2-10
  resolved to these byte-derived runs.
- **First-person texture**: אני/ואני 11 verses (incl. the mutual-belonging
  sites and 8:10 אני חומה); נפשי 7 verses (5 of them in the she-ahavah
  formula).

### Structural texture (staging signals for the granularity gate — writers
re-derive; heuristic, never row evidence)
- **Catchword adjacency** (skeleton-tier shared-content-token pairs):
  ch 1 = 4/16, ch 2 = 5/16, ch 3 = 4/10, ch 4 = 5/15, ch 5 = 2/15,
  ch 6 = 3/11, **ch 7 = 1/13 (MT)**, ch 8 = 3/13 — LOW EVERYWHERE:
  continuous lyric coheres by refrain/frame, not catchword chains. This is
  a DIFFERENT shape from Prov/Eccl sentence zones — the granularity gate
  question (voice-shift seams vs refrain brackets) exists because of it.
- **Continuation-paragraph folds: ZERO in this book** (poetry-dominant;
  115/117 WEB verses open poetry lines) — the folding hazard class
  (M8-LOG-0002) is INERT here but the machinery stays armed.

## SWEEP HAZARD CATALOG (lesson e — every class byte-verified in Song)
- **dod digit-blending (THE Song trap)**: dodi-exact 24 verses vs
  dod-family 28 verses vs family TOKENS (more) vs the DEFECTIVE דדיך/דדי
  4 verses vs דודאים mandrakes 1 verse — five different true objects on one
  skeleton family. Name the object, then count. דודאים and דדיך both sit
  in/near the OFFSET ZONE (MT 7:13-14 = WEB 7:12-13).
- **שבע oath-only homograph**: every Song hit is the SWEAR root — השבעתי
  ×4 + the quoted-back שהשבעתנו at 5:9; 'seven' and 'sated' NEVER occur: a
  blended שבע digit is meaningless; name root AND speech role.
- **resh-ayin family**: רעיתי 'my love' (9) / רעה graze-family (הרעה,
  לרעות...) / רע 'evil' (ZERO in Song) — same skeleton neighborhood, three
  objects; the graze verses (2:16, 6:2-3...) sit INSIDE mutual-belonging
  verses.
- **כרם-in-כרמל contained substring**: vineyard kerem-family 6 verses
  (MT 1:6, 1:14, 2:15, 7:13 = WEB 7:12, 8:11, 8:12) vs Carmel exactly 1
  (MT 7:6 = WEB 7:5, IN THE OFFSET ZONE) — word-bind or byte-check every
  vineyard sweep; bare כרם (final mem, 8:11) and suffixed כרמי/בכרמי
  (medial mem) split across allography, and this very split hid 8:11 from
  the Phase-0 first-pass sweep.
- **מור/מר myrrh spellings**: plene מור vs DEFECTIVE מר (MT 1:13, 4:14) —
  the defective form collides with mar 'bitter' (absent in Song) and
  escapes plene sweeps.
- **עין eye-vs-spring**: the En-Gedi phrase עין גדי (1:14) is a SPRING;
  role-split any eye-count (עיניך/עיניו wasf tokens are the eye family).
- **Final-letter allography**: יין wine vs suffixed ייני (5:1) — medial vs
  final nun; sweep per attested spelling (this class refuted 8 of the
  Phase-0 anchor first-run misses).
- **בנות address-vs-phrase**: the vocative בנות ירושלם (6 sites) vs
  prefixed מבנות ירושלם 3:10 (from-phrase) vs bare בנות 6:9 (the daughters
  praising) — three roles; the ADDRESS count is the refrain object.
- **אחות epithet-vs-sister**: אחתי bride-epithet (4:9-5:2 zone) vs 8:8
  little-sister — role-split.
- **מלך king-vs-queens**: melek-lexeme 5 verses vs מלכות queens 6:8-9;
  prefix forms שהמלך/במלך escape exact sweeps.
- **שלהבת יה (MT 8:6)**: the staged extract carries TWO tokens (OSHB
  divided the single WLC word for exegesis and tags יה as lemma 3050 Yah) —
  a naive standalone-יה sweep hits here. The construal (intensive 'mighty
  flame' vs divine element 'flame of Yah') is a CLASSIC CRUX: hold, never
  decide, never cite as a divine-name occurrence without the crux AND the
  one-word/divided-token disclosure. The OSHB exegesis note at 8:6 is
  single-witness apparatus.
- **OFFSET-ZONE COUNTING (book-specific)**: any per-chapter digit touching
  chs 6-7 must NAME its numbering space — WEB ch 7 and MT ch 7 have
  different membership (e.g. the third mutual-belonging site MT 7:11 =
  WEB 7:10; the SAMEKH at MT 7:11; Carmel MT 7:6 = WEB 7:5; the mandrakes
  MT 7:14 = WEB 7:13).
- **el/al/et short-token trap** — unchanged from Ps/Prov/Eccl: never sweep
  2-letter function words without word-binding + pointed checks.
- **Mater-lectionis / defective-plene pairs**: unchanged — sweep per
  attested spelling (הרמנים 6:11 vs הרמונים 7:13 is the live in-book pair).

## Data files (consume directly)
- `verse_map_web.json` — WEB ref → {text, clean, para_before,
  continuation_paragraphs, poetry_lines, language, mt}; 115 of 117 verses
  open poetry lines (poetry-dominant book); ZERO continuation-paragraph
  folds (token audit 117/117 PASS against raw USFM).
- `verse_map_oshb.json` — MT ref → {text (full pointed), language, web}.
- `consonantal_index.json` — MT ref → {skeleton, accent_stripped, nfd}.
- `../pmarks_Song.json`, `../song_device_inventory.json`,
  `../web_mt_offset_map.json`, `../verse_inventory.json`,
  `../speaker_headings_web.json` (TIER-4 audit catalog — see above).

## Tools
| Tool | Purpose |
|---|---|
| `collate.py --ref oshb:Song.C.V --quote "…"` | Hebrew quote tier: byte / nfd / accent_stripped / skeleton / none. Only **byte** is quotation-grade for pointed text. Bare/web: refs are crosswalk-mapped to MT internally. |
| `check_web_quotes.py FILE...` | Verbatim check of curly-quoted English near web: refs. CURLY QUOTES + an inline web: ref in the SAME field are MANDATORY at every layer. The neighbor-only WARN arm is LIVE in WEB chs 6-7 (MT-number-under-web-prefix hazard). |
| `check_refs_mirror.py ROWS...` | Every verse argued in prose OUTSIDE the row's own span must appear in boundary_evidence_refs — INCLUDING bare "verse N"/"vv. N-M" mentions resolved against the row's span chapter. Witness-prefix-aware: an oshb: token never mirrors a WEB verse of the same numerals in the offset zone. |
| `check_marks.py ROWS...` | Song pivot: selah/reversed-nun/suspended AND all small/large-letter claims = fabrication; petuchah/setumah claims validated against the 20-seg inventory under the claimed TYPE (PE≠SAMEKH) at MT keys (dual-reading in the offset zone); UNCONDITIONAL span-relevant mark-disclosure symmetry; K/Q claim validation; paseq-position WARN. |
| `citation_sweep.py ROWS` | Ref validity incl. RANGE ENDS and X-X span form, CROSSWALK dual-cite arithmetic, **offset-zone disclosure enforcement**, mark/paseq/K-Q claims vs inventories at MT keys, witness disclosure, LXX/Greek guard, selah + special-letter bans, Hebrew-quote-to-cited-ref byte binding. |
| `sweep.py --heb/--skel/--web Q [--tokens]` | Book-wide occurrence sweep. **Counts are VERSE counts** unless --tokens; every citation NAMES its unit and carries A DIGIT. --skel is contiguous consonantal SUBSTRING search — see the hazard catalog above before trusting any short-token digit. |
| `song_devices.py` | Rebuilds ../song_device_inventory.json (orchestrator-run; agents consume the JSON). |
| `ngram7.py ROWS` | Cross-row authorial 7-gram templating gate (≥10 rows = RED), WEB-quotation-aware; unit_type/parent_collection/writer_*/wj_or_red_letter_considered/review_status excluded (p1/p2/p4 lineage). |
| `check_universals.py FILE...` | Flags universal claims lacking an adjacent DIGIT-BEARING sweep count. |
| `check_language_zones.py FILE...` | Flags Aramaic VERSE labels (all-Hebrew book; influence discussion is fine). |
| `normalize_hebrew_in_json.py [--write] FILE...` | Byte-splices NFD-equivalent Hebrew runs to source bytes (MIN_LEN=2). NEVER hand-type Hebrew — slice from verse_map_oshb.json. |
| `check_tiling.py FILE --range Song.a.b-Song.c.d` | Exact tiling of a WEB range: gaps/overlaps/order. |
| `check_atomic_isolation.py ROWS` | **STAGED, NOT ARMED** (Prov lesson-a lineage, p3-guarded output path): atomic-row neighbor-isolation validator + scoped-mesh cluster builder. ATOMIC_TYPES is pinned AFTER the owner gate; unarmed = every row model-reviewed. Crosswalk-aware (WEB 6:13 fetches MT 7:1 bytes). |
| `run_validator_suite.py ROWS [--reviews F...]` | Orchestrator-only: full Tier-0 suite + consolidated report. |

### NO MORPHOLOGY LAYER in the staged extract
verse_map_oshb.json carries text/language/web only. Form claims (gender of
a suffix or verb, jussive, participle) CANNOT be machine-verified with the
staged tools — argue them from the pointed bytes plus both witnesses'
renderings, and remember the VOICE-ATTRIBUTION policy tier set at the owner
gate governs how far grammatical-gender arguments may carry a seam.

## Encoding + skeleton notes (READ before quoting Hebrew)
- **The staged extract is MAQAF-FREE at every tier** (byte-verified: 0 ×
  U+05BE across all 117 MT verses — the extractor serialized maqaf as
  SPACE). Never assert maqaf in quoted spans; quote spans from the source
  bytes, never retype. (The 8:6 שלהבת יה pair is OSHB's exegetical
  division, not a maqaf artifact — see the hazard catalog.)
- **accent_stripped RETAINS meteg (U+05BD)**: it strips cantillation
  U+0591-05AF only. Disclose the tier you matched at.
- **Final-letter allography (ך ם ן ף ץ) is preserved exactly** — sweep per
  attested spelling.
- **SHELL-TRANSIT HAZARD** (scope: ANY pointed Hebrew through a shell):
  shells can silently LOSE accent codepoints. Pass pointed queries via
  subprocess argv from a JSON-held source splice, or write the quote to a
  file; trust only accent_stripped/skeleton tiers for anything typed
  through a shell.
- QUOTE CONVENTION book-wide: curly double quotes are for WEB text ONLY;
  quote row/tool wording in straight quotes.
- COPY-DEGRADATION HAZARD (OL-c26 class, extends to RENDERED-DISPLAY
  copies): even a model-authored copy of pointed Hebrew inside your own
  draft can degrade byte→nfd. Never re-key AND never
  copy-through-your-own-text: splice programmatically from
  verse_map_oshb.json every time, then re-collate your own output.
- K/Q: only 4 verses (MT 1:17, 2:11, 2:13, 4:9) — check pmarks kq before
  counting or slicing in any of them.

## Standing rules (campaign governance; Esth a-g + Job a-j + Ps a-k + Prov a-k + Eccl a-k applied)
- Tier-4 metadata (chapter/verse numbers, WEB headings/footnotes, **WEB
  [SPEAKER] voice headings**, modern ¶ and poetry-line breaks, WEB strong=
  attrs) is NEVER boundary evidence and NEVER counterevidence by absence.
- Quote the original language for every boundary-relevant original-language
  claim; cite the tier when you cite a non-textual signal. TIER-LABEL every
  recurrence claim at write time (Eccl lesson e: tier re-labeling was the
  mesh's largest cure class); "verbatim/byte-identical" only per collate
  truth WITH the tier named (TIER-DISCLOSURE STANDARD, boss B-4 campaign
  law: a skeleton-tier cohesion driver satisfies the byte-grounded bar ONLY
  with the tier honestly named).
- SEAM-PAIR CURES ARE ONE EDIT; REPLACEMENT WARRANTS MUST PASS THE TEST THAT
  KILLED THE ORIGINAL; QUOTE/GLOSS PARITY REPAIRS RE-CUT THE GLOSS.
- observed_substrate_signals IS A DEPENDENT FIELD of every driver swap;
  driver swaps also re-open rejected_alternative, unit_type, confidence.
  **oss FIELD CONTRACT (Eccl lesson c, MANDATED): entries use the dotted
  signal-key taxonomy (voice_shift.*, adjuration_refrain.*,
  mutual_belonging.*, wasf.*, daughters_address.*, parashah.*-style keys);
  staged-file names/stems are BARRED in EVERY field.**
- CROSS-SEAM COHESION: a byte-true device straddling the row's own seam
  argues continuity against the row unless disclosed (the refrain brackets
  and the wasf chains make this LIVE book-wide).
- SYMMETRY completion is a SWEEP, not a spot fix — for parashah marks
  (20 marked verses!) and every other disclosure object.
- SEMANTIC-CLASS COUNT DISCIPLINE: name the swept object FIRST (spelling vs
  term vs formula vs construction vs speech-role), then count; blended
  sweeps forbidden.
- unit_type uses the CONTROLLED VOCABULARY declared in the writer brief —
  no free-text unit types (vocabulary set at the Song owner gate).
- ENGAGEMENT CLASS (Prov lesson g, reinforced by Eccl lesson e): pointed
  splices + tier labels are MANDATORY for every boundary-relevant Hebrew
  claim.
- REGISTER PURGE: NO decision-ids, strategy-file/§ citations, erratum
  narration, positional row references, file-order talk, review-actor
  names, TOOL FILENAMES, **or staged-file names/stems in ANY field** (Eccl
  lesson k) in row prose EVER; the "(sweep: N verses)" convention is the
  one sanctioned citation shorthand. Cross-row references are
  verse-anchored.
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
  ledger consequence text (Eccl lesson d).
- BRIEF HYGIENE (Prov lesson c): briefs carry FULL absolute paths for
  worktree reads + the explicit forbidden-lane list (M1..M7); existence-
  check of your own output file is permitted; "your ONLY SP write is your
  one deliverable — no debug files anywhere under SP, no cleanup heuristics
  in shared dirs."
- If you find yourself building a tool, STOP — it exists here or you don't
  need it.
