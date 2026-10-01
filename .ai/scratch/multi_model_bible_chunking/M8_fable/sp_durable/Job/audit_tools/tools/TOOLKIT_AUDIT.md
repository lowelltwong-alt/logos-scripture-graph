# Job OW-2 AUDIT toolkit (rebuilt 2026-09-03 from the raw witnesses for OW-2 item 2)

**USE these tools. Do NOT rebuild, copy, or re-derive any of them.** Run everything
with `PYTHONIOENCODING=utf-8 python <tool> ...` FROM THIS DIRECTORY. Work in a
uniquely-named private subdirectory of YOUR OWN session scratchpad — never write
anything under SP. The owner-ruled strategy
`C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Job.md`
is LAW (read it in full before auditing a Job row; every count in it is sweep-verified
and names its object).

Provenance: the original Job campaign toolkit (2026-08-11/12 scratchpad) no longer
exists on disk and was never mirrored durable (there is no sp_durable/Job); this AUDIT
subset was rebuilt from the same raw witnesses with the Song r3 lineage API.

## Book facts (byte-PROVEN by build_offset_map.py / build_pmarks.py — trust these)

### Numbering: OFFSET book — one zone (../web_mt_offset_map.json)
1070 WEB verses = 1070 MT over 42 chapters. **WEB 41:1-8 = MT 40:25-32; WEB 41:9-34 =
MT 41:1-26; ALL else identity.** Proof layers in the map: per-chapter counts under the
rule set (WEB 40 = 24 / MT 40 = 32; WEB 41 = 34 / MT 41 = 26; every other chapter
equal); 154 content anchors (8 inside the zone) at the crosswalk-mapped MT refs with
ZERO misses; the identity mapping FAILS exactly the 8 zone anchors (falsification);
seam byte-review at MT 40:15 (Behemoth, identity) / 40:24 (identity edge) / 40:25
(Leviathan = WEB 41:1) / 41:1 (= WEB 41:9) / 41:26 (= WEB 41:34) / 42:1; and the shipped
corpus's own 39 explicit dual-cites all agree with the map (secondary witness).
The Behemoth poem (40:15-24) sits BEFORE the zone in both numberings; the Leviathan poem
IS the zone (WEB 41 = MT 40:25-41:26). **The WEB 40|41 chapter break is tier-4 metadata
— never argue the Behemoth|Leviathan seam FROM the chapter break**; argue it from the
creature-introduction syntax (הנה נא בהמות 40:15 / תמשך לויתן MT 40:25) with the offset
disclosed. Row spans + bare/web: refs = WEB; oshb:/pmarks = MT. Original-language cites
inside the zone MUST dual-cite (`web:Job.41.V = oshb:Job.MTc.MTv`). Use
`job_lib.web_to_mt()/mt_to_web()`; NEVER hand-compute. No title pseudo-verses (no Job.N.0).

### Marks layer (../pmarks_Job.json, MT-keyed, byte-extracted; strategy §4 re-asserted)
**26 PE + 13 SAMEKH** (Writings: at most TIER-3 weak corroboration, never a driver,
single-witness, PE never conflated with SAMEKH, absence NEVER counterevidence; the mark
FOLLOWS its verse). Seam-tracking distribution citable as corroboration WITH
disclosure: PE follows 3:1 and 3:26; 31:40 (colophon); 32:1 and 32:5; SAMEKH follows
33:33; PE follows 39:30, 40:2, 40:5; SAMEKH follows MT 41:26 (= WEB 41:34); PE follows
42:6; SAMEKH follows 42:11, 42:15. Chapters 4, 6, 9, 12, 13, 16, 23, 27, 29, 30, 36, 38
carry NO marks — the first whirlwind speech (38) OPENS UNMARKED. Prescribed cite form:
oshb:Job.C.V (petuchah, single-witness) / (setumah, single-witness).
**Paseq 98 segs / 93 verses** (seg layer, count-only, never quotable). **Suspended ayin
x2: MT 38:13 + 38:15** (inventory-guarded; tier-3 at most). **K/Q 53 notes / 49 verses**
— HIGH; the staged extract carries ketiv+qere adjacent; disclose whenever a quote crosses
one (collate.py's byte tier tells you). **NO selah, NO reversed-nun / small / large
letters** in WLC Job — fabrication classes. Morph tally: all 8,399 codes H-prefixed —
NO Aramaic zones (Aramaism DISCUSSION is legitimate; labeling a VERSE Aramaic is not).

### The dialogue spine (strategy §2a — sweep-verified; per-speaker spellings are
DISTINCT objects: sweep per attested spelling and say so)
Verse-initial vaya'an (ויען) 27 book-wide; vayosef (ויסף) 3 (27:1, 29:1, 36:1); frame
vayomer (ויאמר) 9. Eliphaz 3 (התימני 4:1, 15:1; **התמני 22:1 defective**); Bildad 3
(השוחי 8:1; **השחי 18:1, 25:1**); Zophar 2; Elihu's four speeches (32:6, 34:1, 35:1,
36:1) with the 32:1-5 prose intro; the whirlwind speeches 38:1, 40:1, 40:6; Job's
responses 40:3-5, 42:1-6. Speech = the default larger unit, bounded by that inventory;
rows = strophe-level movements seamed at tier-1 signals (vocative/address shifts,
topic-turn interrogatives, imperative clusters, explicit speaker change) — the WEB 40|41
break and modern paragraphing never cut.

### Cross-tradition scope (metadata only, never in refs, never evidence)
The Old Greek Job is markedly SHORTER than MT (ecclesiastical tradition fills from
Theodotion); the Testament of Job is a separate work. Cross-BOOK parallels (Job 3 ||
Jer 20:14-18; 7:17-18 || Ps 8; 12:9 || Isa 41:20) are typed-relation material, never
boundary authority.

### Schema note for the audit
Job's shipped rows carry the EARLIER row schema: decision_id, span, boundary_rationale,
boundary_evidence_refs, strongest_rejected_alternative, literature_type_guess (free
text — there is NO unit_type field), confidence, review_revision, final_sha256 — and
NO observed_substrate_signals / device_notes / parent fields. Audit the fields present;
later-schema conventions are not retroactive defects (see the brief's calibration law).

## SWEEP HAZARD CATALOG (book-specific; the Ps/Prov catalog classes stay live)
- **בהמות homograph**: 12:7 "beasts" vs 40:15 Behemoth — same skeleton, different object.
- **לויתן — sweep: 2** (3:8 the Leviathan-rousers curse; MT 40:25 = WEB 41:1 the poem).
- **Plene/defective name pairs** (anchor-miss class, byte-verified): Elihu אליהוא /
  אליהו; Zophar צפר / צופר; Tema תימא / תמא; "three" שלש / שלוש; Eliphaz/Bildad
  gentilics as above. Sweep per attested spelling.
- **כסיל = fool AND Orion** (9:9, 38:31) — name the object.
- **רהב**: the sea-monster noun (9:13, 26:12) vs any verbal "storm" use elsewhere.
- **Speech-formula shapes**: vaya'an (verse-initial) vs vayosef (resumption) vs frame
  vayomer — three objects, never blended; the accents differ (merkha vs munach at
  27:1/29:1 — strategy §2a).

## Data files (consume directly)
- `verse_map_web.json` — WEB ref -> {text, clean, para_before, continuation_paragraphs,
  poetry_lines, language, mt}; 990/1070 verses open poetry lines; 5 continuation-¶ folds.
- `verse_map_oshb.json` — MT ref -> {text (full pointed), language, web}.
- `consonantal_index.json` — MT ref -> {skeleton, accent_stripped, nfd}.
- `../pmarks_Job.json`, `../web_mt_offset_map.json`, `../verse_inventory.json`,
  `../editorial_headings_web.json` (empty catalog — WEB Job carries no heading lines).

## Tools
| Tool | Purpose |
|---|---|
| `collate.py --ref oshb:Job.C.V --quote "…"` / `--ref Job.C.V` (WEB, mapped internally; ranges allowed) | Hebrew quote tier: byte / nfd / accent_stripped / skeleton / none. Only **byte** is quotation-grade for pointed text. |
| `sweep.py --heb/--skel/--web Q [--tokens]` | Book-wide occurrence sweep; VERSE counts unless --tokens; --skel is a contiguous consonantal SUBSTRING search. Hit refs are MT with WEB aliases. |
| `normalize_hebrew_in_json.py FILE` | Dry-run byte check of every Hebrew run in a JSON against Job_oshb.txt — run it over YOUR packet: 0 fixed AND 0 defects. NEVER hand-type Hebrew. |
| `check_web_quotes.py FILE` | Verbatim check of curly-quoted English near web: refs (neighbor-only WARN arm inside the zone chapters). |

## Encoding notes (READ before quoting Hebrew)
- MAQAF-FREE staged extract at every tier (0 U+05BE codepoints); accent_stripped
  RETAINS meteg (U+05BD); final-letter allography preserved exactly.
- SHELL-TRANSIT HAZARD: pass pointed queries via subprocess argv from a JSON-held splice
  or a file; trust only accent_stripped/skeleton tiers for anything typed through a shell.
- Curly double quotes are for WEB text ONLY. Never re-key Hebrew; splice from
  verse_map_oshb.json every time, then re-collate your own output.
