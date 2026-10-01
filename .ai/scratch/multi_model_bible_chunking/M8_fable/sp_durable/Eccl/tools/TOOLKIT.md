# Eccl shared verification toolkit (m8-mesh-r3, built Phase 0 by the orchestrator)

**USE these tools. Do NOT rebuild, copy, or re-derive any of them.** Every brief
points here. Work in a UNIQUELY-NAMED private subdirectory of YOUR OWN session
scratchpad — never write scratch into SP/Eccl or at any scratchpad root.

Run everything with `PYTHONIOENCODING=utf-8 python <tool> ...` from this directory.

## Book facts (Phase 0 verified — trust these; do not re-derive)

### Numbering: NOT IDENTITY (byte-PROVEN — the expected-identity assumption was REFUTED)
WEB 222 verses / MT 222, 12 chapters — but the classic ch 4/5 split is real:
**MT 4:17 = WEB 5:1** ("Guard your steps … God's house") and
**MT 5:1-19 = WEB 5:2-20**; every other chapter is identity. Proof layers
(../web_mt_offset_map.json): per-chapter count equality UNDER THE RULE SET
from both witnesses' bytes; 113 automatic content anchors agreeing at the
CROSSWALK-mapped refs (11 inside the offset zone), the single miss
byte-reviewed (WEB 4:6 "two handfuls" renders the DUAL noun חפנים — rendering
divergence, not an offset); a FALSIFICATION probe showing the identity
mapping fails 7 anchor checks in ch 5; and four seam byte-review assertions.
**The OSHB KJV-variance note layer is EMPTY for Eccl despite the real
offset — absence of notes proves NOTHING here.** There are NO title
pseudo-verses — **Eccl.N.0 is always invalid**.

Convention: bare/web: refs and row spans = WEB; oshb:/pmarks = MT.
**OFFSET-ZONE RULE (Tier-0 ENFORCED, inverted from the identity books): any
structured ref touching WEB ch 5 (web: side) or MT 4:17 / MT ch 5 (oshb:
side) MUST carry an explicit dual or numeric qualifier
(`web:Eccl.5.1 = oshb:Eccl.4.17`, or `(MT 5:3)` after a web: ref) — bare
coordinates are ambiguous across witnesses exactly there.** Elsewhere duals
stay optional, but any WRITTEN dual/qualifier must be arithmetically right —
machine-checked by `citation_sweep.py`. Single-verse spans use the full X-X
form (`Eccl.3.5-Eccl.3.5`) — machine-checked.
Use `eccl_lib.web_to_mt()/mt_to_web()` ALWAYS — never hand-assume, in either
direction.

### Cross-tradition note
LXX/Greek numbering FOLLOWS MT at the 4:17/5:1 split; the English chapter
division follows the Vulgate-family tradition; Greek order matches MT
book-wide. ALL LXX/Septuagint/Old Greek/Vulgate/Peshitta/Targum/DSS/Qumran
material is cross-tradition METADATA in prose — never boundary evidence,
never counterevidence, never a boundary_evidence_refs entry
(`citation_sweep.py` guards). Numbering-tradition comparisons in prose need
an explicit crosswalk statement.

### PARASHAH LAYER NEARLY EMPTY — but structure-shaped (MT-keyed)
WLC Eccl carries exactly **1 petuchah (PE) + 3 setumah (SAMEKH) segs**
(../pmarks_Eccl.json, byte-extracted): **PE at MT 1:11** — the last verse of
the prologue poem; **SAMEKH at MT 3:1 and MT 3:8** — bracketing the time
catalogue's own seam verses; **SAMEKH at MT 9:10**. Owner tier rules: in the
Writings this is **TIER-3 WEAK corroboration** — never a boundary driver,
single-witness disclosure required on every citation, PE never conflated
with SAMEKH. Absence is NEVER counterevidence (with only 4 segs in 222
verses, absence is the overwhelming norm). Claims are validated against the
inventory by `citation_sweep.py` (refs) and `check_marks.py` (prose + span
symmetry: every span-relevant mark must be disclosed).

### Fabrication classes for Eccl (hard errors)
- **selah** — Psalter device; zero occurrences in Eccl.
- **reversed/inverted nun, suspended letter** — no such segs in WLC Eccl.
- **small/large letters — NONE AT ALL in WLC Eccl** (stricter than Prov,
  which had its 16:28 nun): ANY special-letter claim at ANY Eccl verse is a
  fabrication.

### Disclosure inventories (../pmarks_Eccl.json, MT-keyed)
- **Paseq**: 11 segs over 11 verses (MT 1:6, 1:13, 2:12, 4:1, 4:8, 5:17,
  6:2, 6:3, 7:24, 8:14, 9:3) — seg layer, NOT quotable verse bytes; citable
  from the inventory only; "(single-witness)" required; COUNT-ONLY —
  intra-verse position claims are unsourceable (WARN arm). Note MT 5:17 =
  WEB 5:18 (offset zone).
- **Ketiv/qere**: 12 notes over 12 verses (MT 4:8, 4:17, 5:8, 5:10, 5:17,
  6:10, 7:22, 9:4, 10:3, 10:10, 10:20, 12:6). **FOUR sit in the offset zone,
  including THE SEAM VERSE ITSELF: MT 4:17 (= WEB 5:1) carries an inline
  unpointed ketiv (רגליך) before its pointed qere** — check pmarks kq before
  counting or slicing in ANY K/Q verse. `citation_sweep.py` and
  `check_marks.py` validate K/Q claims against the inventory at the MT key
  (web: refs are crosswalk-mapped first).
- **Morph tally**: all 2,999 morph codes H-prefixed — NO Aramaic zones.
  Aramaism/LBH-influence DISCUSSION (the she- relative register, Persian
  loans פרדס 2:5 / פתגם 8:11 / מדינה 5:7) is legitimate; labeling a VERSE as
  Aramaic is flagged (check_language_zones).

### Frame spine (../eccl_device_inventory.json — the tier-1 seam skeleton)
Byte-swept: **דברי verse-initial at 4 verses but ONLY 1:1 is a header**
(9:17, 10:12, 12:11 are genitive phrases mid-discourse — the Prov
header-vs-genitive hazard is live here); **qohelet at exactly 7 sites in TWO
attested spellings** — קהלת (defective) at 1:1, 1:2, 1:12, 7:27, 12:9, 12:10
and **הקוהלת (plene + definite article) at 12:8 ONLY**; **the amar-qohelet
third-person frame intrusions at 1:2, 7:27, 12:8** — and 7:27 is the
FEMININE form אמרה (byte-fact; argue any significance from bytes, hold
honestly); king self-identifications at 1:1 (בן דוד מלך בירושלם) and 1:12
(אני קהלת הייתי מלך); **PE at MT 1:11 = the prologue poem's last verse**.
First-person monologue texture: אני/ואני in 25 verses (ch 2 peak: 9),
ראיתי/וראיתי 18 verses, אמרתי 9, שבתי/ושבתי 3 (4:1, 4:7, 9:11), דברתי 2;
מלך-family tokens in 9 verses (noun/verb/name discipline before counting).

### Refrain inventories (MT-keyed; name the object before citing ANY digit)
- **hevel**: 38 family TOKENS over 30 VERSES; the bare token הבל alone is
  29 tokens / 25 verses — suffixed/prefixed forms (הבלך ×2, הבלו, הבלי,
  בהבל, והבלים, הבלים ×3) escape bare-token sweeps. **havel-havalim
  superlative: 2 verses / 3 occurrences — 1:2 (twice) and 12:8 (once): the
  inclusio brackets, byte-derived.** hakol-hevel: 6 verses (1:2, 1:14, 2:11,
  2:17, 3:19, 12:8).
- **reut-ruach** (chasing wind): 7 verses (1:14, 2:11, 2:17, 2:26, 4:4, 4:6,
  6:9); **rayon-ruach**: 2 verses (1:17, 4:16) — a DIFFERENT attested form,
  never blended.
- **tachat-hashemesh** (under the sun): 27 verses (chs: 1→3, 2→6, 3→1, 4→4,
  5→2, 6→2, 8→3, 9→5, 10→1; none in 7, 11, 12); bare שמש outside the
  formula: 5 verses (1:5, 6:5, 7:11, 11:7, 12:2).
- **Time catalogue 3:1-8**: MT 3:1 carries זמן (its only book occurrence) +
  עת once; MT 3:2-8 carry exactly 4 עת/ועת tokens each = **29 עת tokens in
  the poem**; 8 verses carry word-bound עת forms outside the poem — bare עת
  at 3:17, 8:6, 8:9, 9:8, 9:11; ועת 8:5; לעת 9:12; בעת 10:17 (all
  byte-verified per attested form); suffixed בעתו at 3:11 and עתו at 9:12
  escape bare sweeps (9:12 carries BOTH עתו and לעת);
  **עתה ("now") occurs ZERO times in Eccl** — swept, citable as absence.
- **Enjoyment (carpe-diem) sites** (eat+drink co-occurrence): 5 verses —
  MT 2:24, 3:13, 5:17 (= WEB 5:18!), 8:15, 9:7. Wider "enjoyment passage"
  bounds are writer territory argued from bytes.
- **tov comparatives**: contiguous טוב-מ adjacency 6 verses (MT 3:22, 4:3,
  4:6, 6:3, 6:9, 9:4) — but non-adjacent constructions (7:1 טוב שם משמן)
  ESCAPE adjacency sweeps; WEB "better" 23 verses (ch 7 peak: 6); tov
  openers 12 verses, **7 of them in ch 7** (7:1, 7:2, 7:3, 7:5, 7:8, 7:11,
  7:18).
- **Aging allegory zone (11:7-12:8)**: the עד אשר לא before-clause anaphora
  at 12:1, 12:2, 12:6; youth terms at 11:9, 11:10, 12:1; rejoice(שמח)/
  remember(זכר) roots interleave through 11:7-12:1.
- **Elohim/YHWH**: אלהים-family in 36 verses — the definite האלהים dominates
  (28 verses) vs bare אלהים (7); **YHWH occurs ZERO times (byte-swept)** —
  every God-reference is Elohim; any YHWH citation in an Eccl row is a
  fabrication, and the absence itself is citable WITH this sweep digit.

### Structural texture (staging signals for the granularity gate — writers
re-derive; heuristic, never row evidence)
- **Catchword adjacency** (skeleton-tier shared-content-token pairs):
  ch 2 = 18/25 and ch 3 = 15/21 (sustained discourse); **ch 7 = 11/28
  (mixed); ch 10 = 3/19 (true sentence literature — LOWER cohesion than any
  Prov sentence chapter)**; ch 11 = 2/9; ch 12 = 4/13.
- **", but " texture**: near-absent (6 verses book-wide) — Eccl's
  antithesis is not WEB-rendered like Prov's; do not lean on it.
- **Continuation-paragraph folds: LIVE in this prose book** — WEB 7:8 and
  10:14 fold across paragraph marks (Prov had zero). The folding hazard
  class (M8-LOG-0002) applies to every WEB quote in those zones.

## SWEEP HAZARD CATALOG (lesson d — every class byte-verified in Eccl)
- **שבע THREE-way homograph** (shin/sin dot + object split): the contiguous
  sweep returns 7 verses spanning THREE objects — satisfied/satiety (sin:
  תשבע 1:8, 4:8, 6:3; ישבע MT 5:9; והשבע MT 5:11), swear (shin: הנשבע 9:2),
  seven (shin: לשבעה 11:2). Blended counts are meaningless; two sites are
  ALSO offset-zone (MT 5:9 = WEB 5:10; MT 5:11 = WEB 5:12).
- **כמה-in-חכמה**: a contiguous-skeleton sweep of כמה returns 22 verses —
  ALL of them inside חכמה-family tokens; genuine standalone כמה: ZERO. In
  the wisdom-vocabulary half of the book this is THE contained-substring
  trap: word-bound or byte-check every short sweep.
- **hevel digit-blending**: 25 (bare-token verses) vs 30 (family verses) vs
  38 (family tokens) are three DIFFERENT true digits — name the object.
  חבל (het) is a different consonant and a different object entirely.
- **resh-ayin family**: רעות רוח (7) / רעיון רוח (2) / evil-family רע/רעה
  (~23 verses) / the shepherd of 12:11 — four objects on near-identical
  skeletons; name the OBJECT, then count.
- **עת family**: bare/prefixed עת forms vs suffixed בעתו (3:11, 9:12) vs
  עתה (ZERO in Eccl). A bare-token sweep undercounts; an עת-substring sweep
  overcounts (לעת/כעת classes).
- **ירא prefix-extension** (the ביראת class): 8 verses; forms ליראי, שיראו,
  ייראו carry prefixes/suffixes that escape naive word-bound sweeps; and
  12:5 יראו is fear-of-HEIGHTS inside the aging allegory — same root,
  different function; role-split before counting.
- **דברי header-vs-genitive**: 4 verse-initial sites, exactly 1 header
  (1:1); 9:17, 10:12, 12:11 are genitives — verse-initial position alone
  does NOT mark a seam here.
- **קהלת two spellings**: defective קהלת (6 sites) vs plene definite
  הקוהלת (12:8 only) — sweep per attested spelling or miss the epilogue's
  own inclusio form.
- **טוב-מ phrase-extension**: contiguous adjacency finds 6 verses; the
  ch 7 better-than series (7:1 טוב שם משמן) has INTERVENING tokens and
  escapes it. PHRASE sweeps need construction checks, both directions.
- **OFFSET-ZONE COUNTING (book-specific)**: any per-chapter digit touching
  chs 4-5 must NAME its numbering space — MT ch 5 and WEB ch 5 have
  different membership (e.g. the carpe-diem site MT 5:17 = WEB 5:18; the
  K/Q at MT 5:8 = WEB 5:9).
- **Inline-ketiv slicing**: 12 K/Q verses carry the qere pointed and may
  carry the ketiv inline unpointed (the seam verse MT 4:17 does) — check
  pmarks kq BEFORE counting tokens or slicing quotes in any K/Q verse.
- **el/al/et short-token trap** — unchanged from Ps/Prov: never sweep
  2-letter function words without word-binding + pointed checks.
- **Mater-lectionis / final-letter allography**: unchanged — sweep per
  attested spelling.

## Data files (consume directly)
- `verse_map_web.json` — WEB ref → {text, clean, para_before,
  continuation_paragraphs, poetry_lines, language, mt}; 32 of 222 verses
  open poetry lines (prose-dominant book); TWO continuation-paragraph folds
  (7:8, 10:14; token audit 222/222 PASS against raw USFM).
- `verse_map_oshb.json` — MT ref → {text (full pointed), language, web}.
- `consonantal_index.json` — MT ref → {skeleton, accent_stripped, nfd}.
- `../pmarks_Eccl.json`, `../eccl_device_inventory.json`,
  `../web_mt_offset_map.json`, `../verse_inventory.json`.

## Tools
| Tool | Purpose |
|---|---|
| `collate.py --ref oshb:Eccl.C.V --quote "…"` | Hebrew quote tier: byte / nfd / accent_stripped / skeleton / none. Only **byte** is quotation-grade for pointed text. Bare/web: refs are crosswalk-mapped to MT internally. |
| `check_web_quotes.py FILE...` | Verbatim check of curly-quoted English near web: refs. CURLY QUOTES + an inline web: ref in the SAME field are MANDATORY at every layer. The neighbor-only WARN arm is LIVE in WEB ch 5 (MT-number-under-web-prefix hazard). |
| `check_refs_mirror.py ROWS...` | Every verse argued in prose OUTSIDE the row's own span must appear in boundary_evidence_refs — INCLUDING bare "verse N"/"vv. N-M" mentions resolved against the row's span chapter. Witness-prefix-aware: an oshb: token never mirrors a WEB verse of the same numerals in the offset zone. |
| `check_marks.py ROWS...` | Eccl pivot: selah/reversed-nun/suspended AND all small/large-letter claims = fabrication; petuchah/setumah claims validated against the 4-seg inventory under the claimed TYPE (PE≠SAMEKH) at MT keys (dual-reading in the offset zone); UNCONDITIONAL span-relevant mark-disclosure symmetry; K/Q claim validation; paseq-position WARN. |
| `citation_sweep.py ROWS` | Ref validity incl. RANGE ENDS and X-X span form, CROSSWALK dual-cite arithmetic, **offset-zone disclosure enforcement**, mark/paseq/K-Q claims vs inventories at MT keys, witness disclosure, LXX/Greek guard, selah + special-letter bans, Hebrew-quote-to-cited-ref byte binding. |
| `sweep.py --heb/--skel/--web Q [--tokens]` | Book-wide occurrence sweep. **Counts are VERSE counts** unless --tokens; every citation NAMES its unit and carries A DIGIT. --skel is contiguous consonantal SUBSTRING search — see the hazard catalog above before trusting any short-token digit. |
| `eccl_devices.py` | Rebuilds ../eccl_device_inventory.json (orchestrator-run; agents consume the JSON). |
| `ngram7.py ROWS` | Cross-row authorial 7-gram templating gate (≥10 rows = RED), WEB-quotation-aware; unit_type/parent_collection/writer_* excluded (p1/p2 lineage). |
| `check_universals.py FILE...` | Flags universal claims lacking an adjacent DIGIT-BEARING sweep count. |
| `check_language_zones.py FILE...` | Flags Aramaic VERSE labels (all-Hebrew book; influence discussion is fine). |
| `normalize_hebrew_in_json.py [--write] FILE...` | Byte-splices NFD-equivalent Hebrew runs to source bytes (MIN_LEN=2). NEVER hand-type Hebrew — slice from verse_map_oshb.json. |
| `check_tiling.py FILE --range Eccl.a.b-Eccl.c.d` | Exact tiling of a WEB range: gaps/overlaps/order. |
| `check_atomic_isolation.py ROWS` | **STAGED, NOT ARMED** (built day-0 per Prov lesson a, p3-guarded output path): atomic-row neighbor-isolation validator + scoped-mesh cluster builder. ATOMIC_TYPES is pinned AFTER the owner gate; unarmed = every row model-reviewed. Crosswalk-aware (WEB 5:1 fetches MT 4:17 bytes). |
| `run_validator_suite.py ROWS [--reviews F...]` | Orchestrator-only: full Tier-0 suite + consolidated report. |

### NO MORPHOLOGY LAYER in the staged extract
verse_map_oshb.json carries text/language/web only. Form claims (jussive,
cohortative, participle) CANNOT be machine-verified with the staged tools —
argue them from the pointed bytes plus both witnesses' renderings.

## Encoding + skeleton notes (READ before quoting Hebrew)
- **The staged extract is MAQAF-FREE at every tier** (byte-verified: 0 ×
  U+05BE across all 222 MT verses — the extractor serialized maqaf as
  SPACE). Never assert maqaf in quoted spans; quote spans from the source
  bytes, never retype.
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
- INLINE-KETIV HAZARD: 12 K/Q verses; the seam verse MT 4:17 itself carries
  the unpointed ketiv inline — check pmarks kq before counting or slicing
  in a K/Q verse.

## Standing rules (campaign governance; Esth a-g + Job a-j + Ps a-k + Prov a-k applied)
- Tier-4 metadata (chapter/verse numbers, WEB headings/footnotes, modern ¶
  and poetry-line breaks, WEB strong= attrs) is NEVER boundary evidence and
  NEVER counterevidence by absence.
- Quote the original language for every boundary-relevant original-language
  claim; cite the tier when you cite a non-textual signal.
- SEAM-PAIR CURES ARE ONE EDIT; REPLACEMENT WARRANTS MUST PASS THE TEST THAT
  KILLED THE ORIGINAL; QUOTE/GLOSS PARITY REPAIRS RE-CUT THE GLOSS.
- observed_substrate_signals IS A DEPENDENT FIELD of every driver swap;
  driver swaps also re-open rejected_alternative, unit_type, confidence.
- CROSS-SEAM COHESION: a byte-true device straddling the row's own seam
  argues continuity against the row unless disclosed (the hevel/tachat-
  hashemesh refrains and catchword chains in chs 2-3 make this LIVE).
- SYMMETRY completion is a SWEEP, not a spot fix — for parashah marks and
  every other disclosure object.
- SEMANTIC-CLASS COUNT DISCIPLINE: name the swept object FIRST (spelling vs
  term vs formula vs construction), then count; blended sweeps forbidden.
- TIER/ORDINAL DISCIPLINE: "byte-identical/verbatim" only per collate truth
  WITH the tier named; series ordinals byte-settle FIRST.
- unit_type uses the CONTROLLED VOCABULARY declared in the writer brief —
  no free-text unit types (vocabulary set at the Eccl owner gate).
- ENGAGEMENT CLASS (Prov lesson g): pointed splices + tier labels are
  MANDATORY for every boundary-relevant Hebrew claim.
- REGISTER PURGE: NO decision-ids, strategy-file/§ citations, erratum
  narration, positional row references, file-order talk, review-actor
  names, OR TOOL FILENAMES in row prose EVER (Prov lesson k: the
  "(sweep: N verses)" convention is the one sanctioned citation shorthand).
  Cross-row references are verse-anchored.
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
  are CANDIDATES, triaged by content not volume.
- BRIEF HYGIENE (Prov lesson c): briefs carry FULL absolute paths for
  worktree reads + the explicit forbidden-lane list (M1..M7); existence-
  check of your own output file is permitted; "your ONLY SP write is your
  one deliverable — no debug files anywhere under SP, no cleanup heuristics
  in shared dirs."
- If you find yourself building a tool, STOP — it exists here or you don't
  need it.
