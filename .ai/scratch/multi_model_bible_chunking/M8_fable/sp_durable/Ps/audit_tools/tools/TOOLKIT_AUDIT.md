# Ps OW-2 AUDIT toolkit (rebuilt 2026-09-03 from the raw witnesses for OW-2 item 2)

**USE these tools. Do NOT rebuild, copy, or re-derive any of them.** Run everything
with `PYTHONIOENCODING=utf-8 python <tool> ...` FROM THIS DIRECTORY. Work in a
uniquely-named private subdirectory of YOUR OWN session scratchpad — never write
anything under SP. The owner-ruled strategy
`C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Ps.md`
is LAW (read it in full before auditing a Ps row; its §11 errata are binding).

Provenance: the original Ps campaign toolkit (6a933340 scratchpad) no longer exists
on disk and was never mirrored durable; this AUDIT subset was rebuilt from the same
raw witnesses (WEB USFM + OSHB XML) with the same lineage API (Song r3 tools).

## Book facts (byte-PROVEN by build_offset_map.py / build_pmarks.py — trust these)

### Numbering: NOT IDENTITY — THE book hazard (../web_mt_offset_map.json)
2461 WEB verses / MT 2527 across 150 psalms (66 counted-title verses). Per-psalm rules:
**87 identity; 58 shift+1** (MT counts the title as v1: WEB N:v = MT N:v+1);
**4 shift+2 (51, 52, 54, 60)** (MT vv1-2 = the title: WEB N:v = MT N:v+2);
**Ps 13 SPLIT** (equal counts: WEB 13:1-4 = MT 13:2-5; WEB 13:5 AND 13:6 BOTH = MT 13:6 —
both halves dual-cite oshb:Ps.13.6). Proof layers in the map: per-psalm counts under
the rule set; title-presence consistency (58+4+1+53 = 116 WEB titles); 286 proper-name
content anchors + 71/71 Selah anchors at the crosswalk-mapped MT refs with ZERO
misses; the identity mapping FAILS 113 anchor + 114 Selah checks (falsification);
seam byte-review at MT 1:1 / 3:1-2 / 13:6 / 51:1-3 / 60:1-3 / 119:1; and the shipped
corpus's own 1548 explicit dual-cites all agree with the map (secondary witness).
**TITLE PSEUDO-VERSES:** 116 psalms carry a WEB title; the campaign convention is
`web:Ps.N.0` for the title = `oshb:Ps.N.1` (shift+1) / `oshb:Ps.N.1-2` (shift+2 — a
cite may name either title verse or the pair) / the PREFIX of `oshb:Ps.N.1` in the 53
titled IDENTITY psalms (verse_map_web.json marks these `title_is_prefix_of_mt_v1`).
**Ps 119's 22 [SUPERSCRIPTION] markers are ACROSTIC LETTER HEADERS** (WEB typography,
tier 4; ../ps119_letter_headers_web.json) — NOT titles; Ps.119.0 does not exist; NEVER
call them superscriptions (MT has no headers — the letters are the verses' own initials).
WEB "BOOK n" lines are modern editorial headings (tier 4; ../editorial_headings_web.json).
Convention: bare/web: refs + row spans = WEB; oshb:/pmarks = MT. EVERY original-language
citation in a non-identity psalm dual-cites (`web:Ps.N.V = oshb:Ps.N.MTv`), incl. range
ENDS. Use `ps_lib.web_to_mt()/mt_to_web()/web_to_mt_all()/mt_to_web_all()`; NEVER
hand-compute. WEB Strong's attrs are MISALIGNED in offset psalms — never cite them.
"Psalm N" in prose = the composition; "Ps.N.V" = WEB verse; "MT N:V" = MT verse.

### Marks layer (../pmarks_Ps.json, MT-keyed, byte-extracted)
**WLC Psalms carries NO petuchah/setumah segs AT ALL** — any positive PE/SAMEKH claim in
Ps is a FABRICATION (hard error); absence is never counterevidence. Seg-layer objects
that DO exist (single-witness disclosure required, inventory-cited, never quotable as
verse bytes): **paseq 522 segs / 481 verses** (COUNT-ONLY: intra-verse position claims
are unsourceable); **7 x-reversednun segs in MT 107 AS THE BYTES HAVE THEM** (MT
107:20, 107:21, 107:22, 107:23, 107:24, 107:25 and 107:39 — read from the inventory's
other_segs; traditions differ on placement; cite the inventory); **the suspended ayin at MT 80:14** (x-suspended); **K/Q 68 notes /
65 verses** (the staged extract carries ketiv+qere adjacent — check pmarks kq before
counting or slicing in a K/Q verse). **Selah is VERSE TEXT in both witnesses** (WEB
"Selah" / MT סלה; 71 verses; no witness tag needed; span-scoped symmetry applies).
Morph tally: all 19,657 codes H-prefixed — NO Aramaic zones.

### Cross-tradition scope (metadata only, never in refs, never evidence)
LXX/Vulgate psalm NUMBERING runs one behind MT through most of the book (LXX 9 = MT
9-10; LXX 113 = 114-115; MT 116, 147 split in LXX); 11QPsa's divergent order + Ps 151;
Syriac Pss 152-155. Greek-numbering comparisons in prose need an explicit crosswalk
sentence. Doublets: WEB Ps 14 = 53; Ps 40:13-17 = Ps 70; Ps 108 = Ps 57:7-11 + 60:5-12
(WEB numbering — label the numbering space explicitly when citing doublets).

### Ruled structure (owner gate 2026-08-12; strategy §5-§6, LAW not evidence)
Psalm = parent ALWAYS (150 parents). unit_type controlled vocabulary: whole_psalm |
strophe | letter_stanza | refrain_unit | coda. **whole_psalm rows for short indivisible
psalms are RULED units — no whole-chapter confidence cap applies to them.** Ps 119 =
22 letter_stanza rows. Refrained psalms (42-43 pair with two parents, 46, 56, 57, 59,
62, 67, 80, 99, 107) follow refrain returns. Tier-1 seam evidence = superscriptions,
hallelu-Yah/hodu frames, doxologies, acrostic structure, explicit speaker/addressee
shifts INSIDE psalms; genre clusters and the five-book architecture are DISCUSSION
texture. Strategy §11 errata (binding): Ps 56 in the refrain roster; al_alamot = {46}
only (Ps 9's almut labben is a distinct pointed object); yeduthun titles {39, 62, 77}
(two spelling classes, K/Q at 39:1 and 77:1); Ps 98 IS titled; shir 30 / le-David 73;
Ps 108 composite in WEB numbering; hapax claims are NOT decidable with book-scoped
tools ("1 verse in Psalms, skeleton tier" is the only honest form).

## SWEEP HAZARD CATALOG (lesson i, carried Ps -> Prov -> Eccl -> Song; live here)
- **kmh/chkmh contained-substring trap**; **mlk noun-vs-verb**; **chrb Horeb/sword/dry**;
  **yameinu/yemino**; **kalam suffixed-noun vs klm-shame**; **le-David-at-132:1-class
  object-vs-ascription** (132's "remember FOR David" is content, not attribution);
  **PHRASE-sweep prefix-extension** (right-boundary check); **same-count-different-set**
  (hodu 6); **mater-lectionis / final-letter allography** (sweep per attested spelling:
  ירושלם vs ירושלים, יוסף vs יהוסף at 81:6); **the maqaf-free extract** (0 U+05BE
  codepoints book-wide — never assert maqaf in quoted spans; typographic-maqaf claims
  such as Melchizedek at MT 110:4 are WLC print-tradition claims, not quotable bytes).
- **Title-word objects**: mizmor / shir / maskil / miktam / tefillah / lamnatseach /
  le-David / le-Asaph / bene-Qorach / shir hamma'alot are LABEL classes with byte-swept
  memberships (strategy §2a as corrected by §11) — name the object, then the digit.
- **סלה word-bound**: `sweep.py --skel סלה` is a substring search; the word-bound Selah
  count is 71 verses (build_offset_map.py); name the unit.

## Data files (consume directly)
- `verse_map_web.json` — WEB ref -> {text, clean, para_before, continuation_paragraphs,
  poetry_lines, language, mt}; PLUS the 116 `Ps.N.0` title entries ({text, title: true,
  mt, title_is_prefix_of_mt_v1, rule}). 2418/2461 body verses open poetry lines.
- `verse_map_oshb.json` — MT ref -> {text (full pointed), language, web, web_all}.
- `consonantal_index.json` — MT ref -> {skeleton, accent_stripped, nfd}.
- `../pmarks_Ps.json`, `../web_mt_offset_map.json`, `../verse_inventory.json`,
  `../ps119_letter_headers_web.json`, `../editorial_headings_web.json`.

## Tools
| Tool | Purpose |
|---|---|
| `collate.py --ref oshb:Ps.C.V --quote "…"` / `--ref Ps.C.V` (WEB, mapped internally; `Ps.N.0` = the title; ranges allowed) | Hebrew quote tier: byte / nfd / accent_stripped / skeleton / none. Only **byte** is quotation-grade for pointed text. |
| `sweep.py --heb/--skel/--web Q [--tokens]` | Book-wide occurrence sweep; counts are VERSE counts unless --tokens; --skel is a contiguous consonantal SUBSTRING search — see the hazard catalog. Hit refs are MT with WEB aliases. |
| `normalize_hebrew_in_json.py FILE` | Dry-run byte check of every Hebrew run in a JSON against Ps_oshb.txt — run it over YOUR packet: 0 fixed AND 0 defects. NEVER hand-type Hebrew — slice from verse_map_oshb.json. |
| `check_web_quotes.py FILE` | Verbatim check of curly-quoted English near web: refs (title pseudo-verse v=0 aware; neighbor-only WARN arm for the non-identity psalms). |

## Encoding notes (READ before quoting Hebrew)
- MAQAF-FREE staged extract at every tier; accent_stripped RETAINS meteg (U+05BD);
  final-letter allography preserved exactly.
- SHELL-TRANSIT HAZARD: shells can silently LOSE accent codepoints — pass pointed
  queries via subprocess argv from a JSON-held source splice, or a file; trust only
  accent_stripped/skeleton tiers for anything typed through a shell.
- Curly double quotes are for WEB text ONLY; quote row/tool wording in straight quotes.
- COPY-DEGRADATION HAZARD: never re-key and never copy Hebrew through your own draft —
  splice programmatically from verse_map_oshb.json every time, then re-collate.
- Extractor note (2026-09-03): the upstream extractor leaks raw USFM markup into 14
  Selah lines (a nested \+w tag inside \qs); this toolkit's verse_map_web.json folds
  them to the plain WEB text and asserts no markup survives.
