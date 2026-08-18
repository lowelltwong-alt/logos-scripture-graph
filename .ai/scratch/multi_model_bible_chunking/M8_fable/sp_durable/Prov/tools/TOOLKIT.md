# Prov shared verification toolkit (m8-mesh-r3, built Phase 0 by the orchestrator)

**USE these tools. Do NOT rebuild, copy, or re-derive any of them.** Every brief
points here. Work in a UNIQUELY-NAMED private subdirectory of YOUR OWN session
scratchpad — never write scratch into SP/Prov or at any scratchpad root.

Run everything with `PYTHONIOENCODING=utf-8 python <tool> ...` from this directory.

## Book facts (Phase 0 verified — trust these; do not re-derive)

### Numbering: IDENTITY (byte-PROVEN, not assumed)
WEB 915 verses / MT 915, all 31 chapters equal. Proof layers
(../web_mt_offset_map.json): per-chapter count equality from both witnesses'
bytes; 123 automatic content anchors (numerals + proper names) agreeing at
the same refs, the single miss byte-reviewed (Prov 5:4 "two-edged" renders
חרב פיות "sword of edges" — rendering divergence, not an offset); ZERO OSHB
KJV-variance notes; the 31:10-31 acrostic as a 22-point ch-31 alignment
anchor. There are NO title pseudo-verses — **Prov.N.0 is always invalid**;
the collection headers are ordinary counted verses in BOTH witnesses.
Convention unchanged: bare/web: refs and row spans = WEB; oshb:/pmarks = MT
(the same numbers here). Dual-cites are never REQUIRED in an identity book,
but any WRITTEN dual/qualifier must be arithmetically right — machine-checked
by `citation_sweep.py`. Single-verse spans use the full X-X form
(`Prov.3.5-Prov.3.5`) — machine-checked.
Use `prov_lib.web_to_mt()/mt_to_web()` anyway — they range-guard bad refs.

### Cross-tradition hazard: LXX REORDERS Prov
LXX places 30:1-14 after 24:22, then 30:15-33 + ch 31:1-9 after 24:34, with
31:10-31 at the end — i.e. **24:23-34 and chs 30-31 sit at different
positions in the Greek**. Both staged witnesses follow MT order. ALL
LXX/Septuagint/Old Greek/Vulgate/Peshitta/Targum/DSS/Qumran material is
cross-tradition METADATA in prose — never boundary evidence, never
counterevidence, never a boundary_evidence_refs entry (`citation_sweep.py`
guards). Greek-order comparisons in prose need an explicit crosswalk
statement.

### PARASHAH LAYER PRESENT (inverted from Ps)
WLC Prov carries **51 petuchah (PE) + 1 setumah (SAMEKH) segs over 52
verses** (../pmarks_Prov.json, byte-extracted). Owner tier rules: in the
Writings this is **TIER-3 WEAK corroboration** — never a boundary driver,
single-witness disclosure required on every citation, PE never conflated
with SAMEKH. Distribution is structure-shaped: dense in chs 1-9 (24 segs,
mostly at lecture ends) and ch 30 (8 segs, at the numerical-saying seams);
sparse in 10-29. The ONE SAMEKH sits at **Prov.24.22** — the last verse
before the 24:23 "also of the wise" header. PE at 10:1 (Solomon header) and
31:9 (last verse before the acrostic). Absence is NEVER counterevidence.
Claims are validated against the inventory by `citation_sweep.py` (refs) and
`check_marks.py` (prose + span symmetry: every span-relevant mark must be
disclosed).

### Fabrication classes for Prov (hard errors)
- **selah** — Psalter device; zero occurrences in Prov.
- **reversed/inverted nun, suspended letter** — no such segs in WLC Prov.
- The one special letter is the **SMALL NUN at Prov.16.28** (x-small seg);
  small-letter claims must cite exactly there, single-witness.

### Disclosure inventories (../pmarks_Prov.json, MT-keyed)
- **Paseq**: 60 segs over 57 verses — seg layer, NOT quotable verse bytes
  (U+05C0 absent from staged verse bytes book-wide); citable from the
  inventory only; "(single-witness)" required; the inventory is COUNT-ONLY —
  intra-verse position claims are unsourceable (WARN arm).
- **Ketiv/qere**: 69 notes over 63 verses; `citation_sweep.py`
  and `check_marks.py` validate K/Q claims against the inventory.
- **Morph tally**: all 6,984 morph codes H-prefixed — NO Aramaic zones; the
  bar (בר "son") vocatives of 31:2 are Aramaic-influence DISCUSSION material,
  never a verse-language label (guard: check_language_zones).

### Collection seams (../prov_device_inventory.json — the tier-1 header spine)
Byte-swept: **mishle verse-initial at 1:1 and 10:1 ONLY** (25:1 carries
mishle interior: גם אלה משלי שלמה); **gam-elleh verse-initial at 24:23 and
25:1**; **divrei verse-initial at 30:1 (Agur) and 31:1 (Lemuel)** — but
דברי occurs in 19 verses total (12:6, 18:8, 26:22 etc. are NOT headers);
**divrei hakhamim phrase at 1:6 and 22:17**. The 22:17 "words of the wise"
seam is IN-VERSE (mid-verse in MT; WEB renders it as the verse opening) —
argue it from the text, not from a header line. Eshet-chayil ACROSTIC
31:10-31: 22 verses, full alef-bet IN ORDER, derived from skeleton bytes
(table in the inventory; like Ps 119's derivation).

### Structural texture (staging signals for the granularity gate — writers
re-derive; heuristic, never row evidence)
- **Antithetic cliff**: WEB ", but " verses per chapter run 24/21/25/22/25/20
  across chs 10-15, then 7 at ch 16, 1-6 through 22:16 — the classic
  antithetic (10:1-15:33) vs synthetic (16:1-22:16) split is byte-visible.
- **Catchword adjacency** (skeleton-tier shared-content-token pairs): weak
  everywhere in 10-29 (max 11/32 pairs at ch 16, ~0-7 elsewhere) — the
  sentence-literature problem is real, not folklore.
- **bni ("my son")**: 12 of 17 occurrences in chs 1-7 (the lecture frame:
  1:8, 1:10, 1:15, 2:1, 3:1, 3:21, 4:10, 4:20, 5:1, 6:1, 6:20, 7:1);
  isolated at 19:27, 23:15, 23:26, 24:13, 27:11.
- **YHWH density**: peaks in chs 3 (9), 15 (9), 16 (6), 22 (5) — the
  15:33-16:9 "YHWH cluster" at the book's center is byte-visible.
- **tov openers**: 16 verses open with טוב (the better-than class spine).

## SWEEP HAZARD CATALOG (lesson i — every class byte-verified in Prov)
- **כמה-in-חכמה (kmh/chkmh)**: a contiguous-skeleton sweep of כמה returns 38
  verses — ALL 36 chokhmah verses plus 2 genuine hits. In the wisdom book
  this is THE contained-substring trap: word-bound or byte-check every short
  sweep.
- **מלך noun-vs-verb**: 24 verses carry the skeleton מלך — king (noun),
  reign (verb), counsel (נמלך class) and the 31:1 למואל מלך line; name the
  OBJECT before counting.
- **חרב sword/dry/Horeb**: 5 verses — 5:4 (sword of edges), 12:18, 25:18,
  30:14 (sword-class) vs **17:1 חֲרֵבָה "dry (morsel)"** — a live homograph
  split; pointed byte checks per verse.
- **ימינו his-right-hand vs our-days**: one live site (27:16) — never
  count across the homograph without pointing.
- **כלם all-of-them vs klm-shame**: 8:9 and 22:2 are suffixed-noun sites;
  the shame root (נכלם/הכלים) is a different object.
- **אשת חיל occurs TWICE** (12:4 AND 31:10) — any "unique/only" claim at
  31:10 is byte-false; the sweep digit is 2.
- **דברי header-vs-genitive**: 19 total verses vs 2 headers — verse-initial
  position + context, not the word, marks the seam.
- **טוב מ phrase-extension trap**: the contiguous sweep returns 4 verses but
  3:27 is "withhold good FROM its owners" — same skeleton, NOT a better-than
  comparative. PHRASE sweeps need right-boundary AND construction checks
  (the Ps prefix-extension lesson, live in Prov).
- **Same-count-different-set**: mishle-anywhere (3) vs mishle-verse-initial
  (2); gam-elleh (2) vs wise-headers (2, different verses than you may
  assume) — name the SET, then the digit.
- **Mater-lectionis / final-letter allography**: unchanged from Ps — sweep
  per attested spelling; a search for מצרים will not hit medial-mem forms.

## Data files (consume directly)
- `verse_map_web.json` — WEB ref → {text, clean, para_before,
  continuation_paragraphs, poetry_lines, language, mt}; 907 of 915 verses
  open poetry lines; ZERO continuation-paragraph folds (token audit
  915/915 PASS against raw USFM).
- `verse_map_oshb.json` — MT ref → {text (full pointed), language, web}.
- `consonantal_index.json` — MT ref → {skeleton, accent_stripped, nfd}.
- `../pmarks_Prov.json`, `../prov_device_inventory.json`,
  `../web_mt_offset_map.json`, `../verse_inventory.json`.

## Tools
| Tool | Purpose |
|---|---|
| `collate.py --ref oshb:Prov.C.V --quote "…"` | Hebrew quote tier: byte / nfd / accent_stripped / skeleton / none. Only **byte** is quotation-grade for pointed text. |
| `check_web_quotes.py FILE...` | Verbatim check of curly-quoted English near web: refs. CURLY QUOTES + an inline web: ref in the SAME field are MANDATORY at every layer. |
| `check_refs_mirror.py ROWS...` | Every verse argued in prose OUTSIDE the row's own span must appear in boundary_evidence_refs — INCLUDING bare "verse N"/"vv. N-M" mentions resolved against the row's span chapter (lesson-j arm). |
| `check_marks.py ROWS...` | Prov pivot: selah/reversed-nun/suspended claims = fabrication; petuchah/setumah claims validated against the inventory under the claimed TYPE (PE≠SAMEKH); UNCONDITIONAL span-relevant mark-disclosure symmetry; K/Q claim validation; paseq-position WARN. |
| `citation_sweep.py ROWS` | Ref validity incl. RANGE ENDS and X-X span form, identity dual-cite arithmetic, mark/paseq/K-Q/small-letter claims vs inventories, witness disclosure, LXX/Greek guard, selah ban, **Hebrew-quote-to-cited-ref byte binding (lesson-j collate arm)**. |
| `sweep.py --heb/--skel/--web Q [--tokens]` | Book-wide occurrence sweep. **Counts are VERSE counts** unless --tokens; every citation NAMES its unit and carries A DIGIT. --skel is contiguous consonantal SUBSTRING search — see the hazard catalog above before trusting any short-token digit. |
| `prov_devices.py` | Rebuilds ../prov_device_inventory.json (orchestrator-run; agents consume the JSON). |
| `ngram7.py ROWS` | Cross-row authorial 7-gram templating gate (≥10 rows = RED), WEB-quotation-aware. |
| `check_universals.py FILE...` | Flags universal claims lacking an adjacent DIGIT-BEARING sweep count — widened lexicon (lesson j). |
| `check_language_zones.py FILE...` | Flags Aramaic VERSE labels (all-Hebrew book). |
| `normalize_hebrew_in_json.py [--write] FILE...` | Byte-splices NFD-equivalent Hebrew runs to source bytes (MIN_LEN=2 per lesson f). NEVER hand-type Hebrew — slice from verse_map_oshb.json. |
| `check_tiling.py FILE --range Prov.a.b-Prov.c.d` | Exact tiling of a WEB range: gaps/overlaps/order. |
| `run_validator_suite.py ROWS [--reviews F...]` | Orchestrator-only: full Tier-0 suite + consolidated report. |

### NO MORPHOLOGY LAYER in the staged extract
verse_map_oshb.json carries text/language/web only. Form claims (imperative,
jussive, participle) CANNOT be machine-verified with the staged tools —
argue them from the pointed bytes plus both witnesses' renderings.

## Encoding + skeleton notes (READ before quoting Hebrew)
- **The staged extract is MAQAF-FREE at every tier** (byte-verified: 0 ×
  U+05BE across all 915 MT verses — the extractor serialized maqaf as
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
- COPY-DEGRADATION HAZARD (OL-c26, extends to RENDERED-DISPLAY copies):
  even a model-authored copy of pointed Hebrew inside your own draft can
  degrade byte→nfd. Never re-key AND never copy-through-your-own-text:
  splice programmatically from verse_map_oshb.json every time, then
  re-collate your own output.
- INLINE-KETIV HAZARD: some K/Q verses carry the unpointed ketiv token
  inline before the pointed qere — check pmarks kq before counting or
  slicing in a K/Q verse (69 notes across the book).

## Standing rules (campaign governance; Esth a-g + Job a-j + Ps a-k applied)
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
  argues continuity against the row unless disclosed (catchword chains in
  10-29 make this LIVE — check adjacent verses for shared content tokens).
- SYMMETRY completion is a SWEEP, not a spot fix — for parashah marks and
  every other disclosure object.
- SEMANTIC-CLASS COUNT DISCIPLINE: name the swept object FIRST (spelling vs
  term vs formula vs construction), then count; blended sweeps forbidden.
- TIER/ORDINAL DISCIPLINE: "byte-identical/verbatim" only per collate truth
  WITH the tier named; series ordinals byte-settle FIRST.
- unit_type uses the CONTROLLED VOCABULARY declared in the writer brief —
  no free-text unit types (vocabulary set at the Prov owner gate).
- REGISTER PURGE: NO decision-ids, strategy-file/§ citations, erratum
  narration, positional row references, file-order talk, or review-actor
  names in row prose EVER. Cross-row references are verse-anchored.
- rejected_alternative: one sentence, PLUS an optional second sentence ONLY
  when it carries the mandated rival disclosure. No third sentence.
- Mandated recurring sentences ship with VARIATION ORDERS: 4+ distinct
  formulations, pooled pre-check.
- HAIKU BATCH CEILING: single-agent generative work degrades at ~50+ items —
  slice at <=50 with distinctness + no-generic rules.
- DISK-DERIVED LAUNCH SETS (Ps lesson a); MUTATE-THEN-LAUNCH IN SEPARATE
  TURNS (Ps lesson b); FIX-AGENTS RUN THE FULL SUITE (Ps lesson c);
  collision/comparison cites get CONTENT-match verification (Ps lesson d);
  peers verify OBJECTS and tiers, not digits (Ps lesson e); file-to-file
  splice + ref-scoped re-splice as packet POST-PROCESSING (Ps lesson f);
  heuristic flags are CANDIDATES, triaged by content not volume (Ps
  lesson h).
- If you find yourself building a tool, STOP — it exists here or you don't
  need it.
