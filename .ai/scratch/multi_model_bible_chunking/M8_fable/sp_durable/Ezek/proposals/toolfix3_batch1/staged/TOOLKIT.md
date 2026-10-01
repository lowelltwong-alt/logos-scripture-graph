# Ezek shared verification toolkit (m8-mesh-r3, built Phase 0 by the orchestrator)

**USE these tools. Do NOT rebuild, copy, or re-derive any of them.** Every brief
points here. Work in a UNIQUELY-NAMED private subdirectory of YOUR OWN session
scratchpad — never write scratch into SP/Ezek or at any scratchpad root, and no
debug files anywhere under SP, including in SP output directories during
self-check.

Run everything with `PYTHONIOENCODING=utf-8 python <tool> ...` from this directory.

**Ezekiel is on the OW-6b HARD-BOOK TRACK.** Fable is the controlling agent, peer
and spot coverage are raised, flagged regions get no sampling shortcut, and a
second independent Fable review of the flagged regions runs before the close.

---

## Book facts (Phase 0 verified — trust these; do not re-derive)

**1,273 verses / 48 chapters, EQUAL totals in both witnesses.** Longest chapters:
16 (63 vv), then 20, 23 and 40 (49 each). Shortest: 15 (8 vv), 2 (10), 9 (11).
Poetry is a minority texture — 487 `|q` lines out of 2,272 extract lines — so
Ezekiel reads prose-dominant with poetic oracles embedded, not the reverse.

### Numbering: NOT IDENTITY — ONE offset zone, pure renumbering, NO split (byte-PROVEN)

```
MT 21:1-5    =  WEB 20:45-49
MT 21:6-37   =  WEB 21:1-32
identity in every other chapter
```

WEB ch 20 = 49 vv / MT 44. WEB ch 21 = 32 vv / MT 37. Totals equal at 1,273, so
this is a **SHIFT, not a gap**: nothing is added or missing, the chapter break
moves. The crosswalk is **INJECTIVE** — every WEB verse has exactly one MT verse
and back.

**This is NOT Jeremiah's zone.** Jeremiah's sits at `oshb:Jer.8.23` = `web:Jer.9.1` —
note the book qualifier: a bare "MT 8:23" inside an Ezekiel toolkit reads as Ezek 8:23,
which does not exist (Ezek ch 8 has 18 verses). Ezekiel's
was derived from its own bytes; do not carry Jeremiah's habit of mind here.

**How it was established, in three independent steps** — because equal totals
alone would also fit a five-verse gap plus a five-verse surplus:

1. per-chapter verse counts from the two extracts (arithmetic);
2. verse CONTENT — MT 21:1 is the word-event formula WEB prints at 20:45, MT 21:2
   the "set your face toward the south" WEB prints at 20:46;
3. **the OSHB's OWN KJV-variance layer**, which annotates all 37 verses of MT
   ch 21 with their English reference. **37/37 agree with the map**, and that
   layer was used in neither step 1 nor step 2 — genuine corroboration, not a
   restatement. See `../ezek_kjv_variance_crosscheck.json` and
   `../_kjv_variance_crosscheck.py`.

**OFFSET-ZONE RULE (Tier-0 ENFORCED): any structured ref touching WEB 20:45-49,
WEB ch 21, or MT ch 21 MUST carry an explicit dual or numeric qualifier**
(`web:Ezek.20.45 = oshb:Ezek.21.1`, or `(MT 21:1)` after a web: ref). Bare
coordinates are ambiguous across witnesses exactly there — **and only there**.

Convention: bare/`web:` refs and row spans = WEB; `oshb:`/pmarks = MT. Convert
with `../web_mt_offset_map.json` ALWAYS — never hand-assume, in either direction.

### LANGUAGE — Hebrew throughout

Morph prefixes are **H only across 18,866 tokens**. There is **no Aramaic island**
(contrast `oshb:Jer.10.11`). An Aramaic claim anywhere in Ezekiel is a fabrication.

### PARASHAH LAYER (MT-keyed)

**113 samekh (setumah) + 71 pe (petuchah) = 184 mark occurrences over 183 verses.**
The occurrence count and the verse count differ by one and are never added
together: **Ezek 43:27 carries two consecutive samekh segs.**

Masoretic paragraph marks are EVIDENCE about how the tradition read the text.
They inform a boundary and **never decide one alone**; translation punctuation and
editorial headings never drive a boundary at all (E-23). A mark is recorded on the
verse it FOLLOWS.

Inside the numbering zone: **PE at MT 21:5** (= WEB 20:49) — i.e. the tradition
closes a unit exactly at the English chapter break, which is why the zone is a
seam site as well as a numbering site.

### Fabrication classes for Ezek (hard errors)

- **selah** — Psalter device; **zero occurrences** in Ezek (byte-swept, both the
  XML and the extract).
- **large letters / majuscule (`x-large`)** — **NONE**. Any large-letter claim is
  a fabrication.
- **small letters / minuscule (`x-small`)** — **NONE**. Any small-letter claim is
  a fabrication.
- **reversed / inverted nun, suspended letter** — **NONE** as segs in WLC Ezek.
- **BUT: `puncta extraordinaria` ARE present — exactly TWO sites, MT 41:20 and
  MT 46:22.** They are the one special-mark class Ezekiel does have. A claim of
  them anywhere else is a fabrication, and a claim at those two needs
  single-witness disclosure (citation_sweep fails a true puncta ref without it, as it does
  a mark, small-letter or paseq ref (hyphenated or spaced); in prose that symmetry is model territory).
  **CORRECTED 2026-09-08:** this entry previously said they were "carried in the
  OSHB note layer, not in the verse bytes". That was **wrong** and the Fable
  strategy author refuted it from the bytes. The dots are present in the staged
  extract as combining marks — **U+05C4 (upper dot), five at MT 41:20 and seven
  at MT 46:22** — and the note layer carries them as well. Practical consequence:
  a row splicing either verse carries U+05C4 in its quoted bytes, and an NFD
  validator arm must treat it as a legitimate combining mark rather than
  degradation. U+05C5 (lower dot) does not occur.

### Disclosure inventories (`../pmarks_Ezek.json`, MT-keyed)

- **Paseq: 136 segs over 121 verses** — seg layer, NOT quotable verse bytes;
  citable from the inventory only; "(single-witness)" required; **COUNT-ONLY —
  intra-verse position claims are unsourceable from `Ezek_oshb.txt` and must be
  read from the XML by exact path** (WARN arm). One sits inside the numbering
  zone: **MT 21:3** (= WEB 20:47).
- **Ketiv/qere: 134 notes over 99 verses.** **23 doubled-note verses** — MT 9:5,
  16:13, 16:31, 16:43, 16:51, 16:53, 23:43, 36:13, 36:14, 37:16, 40:21, 40:22,
  40:24, 40:26, 40:29, 40:31, 40:33, 40:34, 40:36, 40:37, 42:9, 43:11, 44:24.
  Check pmarks `kq` before counting or slicing in ANY K/Q verse. **None sits
  inside MT 21:1-5**; the only K/Q in MT ch 21 is **MT 21:28** (= WEB 21:23).
  Note the ch-40 cluster: **TEN** of the 23 doubled-note verses sit in ch 40
  (MT 40:21, 22, 24, 26, 29, 31, 33, 34, 36, 37), with 42:9, 43:11 and 44:24
  nearby.
  **CORRECTED 2026-09-08 — TWICE WRONG HERE, both caught by writer p10
  (`ezek_writer_p10_a1#e1`) and verified from `pmarks_Ezek.json`:**
  1. this said **eleven** while naming ten; the count is **ten**;
  2. it said "the disputed forms are frequently the measurements themselves".
     **They are not, and no reviewer should go in expecting that.** Every K/Q
     form in the ch-40 cluster is a ketiv-defective / qere-plene **3ms
     possessive suffix on an architectural noun** — `תאיו` its chambers,
     `איליו` its posts, `אלמיו` its porches, `חלוניו` its windows, `תמריו` its
     palm trees, `מעליו` its steps, `עלותיו` its stairs — plus one lexical
     variant at MT 40:15. **Not one sits on a cubit or reed numeral.** The
     contested material is the pronominal suffix standing *beside* a number,
     never the number itself.
- **OSHB editorial notes: 71 verses.** These are single-witness apparatus, not
  text bytes, and they were nearly lost — an inventory bug dropped every untyped
  `<note>` until the sof-pasuq arithmetic (1,272 vs 1,273 verses) failed to close.
  Classes:
  - 13 × "BHS has been faithful to the Leningrad Codex where there might be a question of the validity of the form and we keep the same form as BHS."
  - 8 × "We have abandoned or added a ketib/qere relative to BHS. In doing this we agree with L against BHS."
  - 6 × accents read differently from BHS
  - 3 × vowels · 2 × consonants · 1 × punctuation read differently from BHS
  - 3 × "Adaptations to a Qere which L and BHS, by their design, do not indicate." — MT 14:14,
    14:20, 28:3
  - 2 × "Marks an anomalous form." — MT 43:15, 44:3
  - 2 × puncta extraordinaria — MT 41:20, 46:22
  - 37 × KJV-variance notes across MT ch 21 (the numbering layer above)
- **`sof-pasuq`: 1,272 for 1,273 verses.** The missing one is **MT 33:20**, which
  carries instead an OSHB note — *"We read punctuation in L differently from BHS."* —
  followed directly by the pe mark. A real single-witness divergence, not
  a data gap. A row spanning MT 33:20 discloses it, and **no boundary is argued
  from the absent mark**.

### PROPHETIC FRAME SPINE (`../ezek_device_inventory.json` — the tier-1 seam skeleton)

Ezekiel is the most formulaic book the campaign has met, and the formulae are the
honest boundary evidence. Verse counts (a verse containing the form, not
occurrences within it):

| form | verses | typical role |
|---|---|---|
| `ויהי דבר יהוה אלי לאמר` word-event, STRICT | 39 | **ONSET** of an oracle |
| `ויהי דבר יהוה אלי` allowing an infixed date | 41 | ONSET; adds MT 12:8, 24:1 |
| `היה דבר יהוה אלי` perfect form | 7 | ONSET; the form dated oracles use AFTER the dateline |
| `בן אדם` "son of man" | 93 | address; near-universal oracle opener |
| `כה אמר אדני יהוה` messenger formula | 122 | opens a speech within a unit |
| `נאם אדני יהוה` utterance formula | 81 | **CLOSE**, oracle-final signature |
| `וידעו כי אני יהוה` recognition formula | 28 | **CLOSE**, characteristic refrain |
| `וידעת כי אני יהוה` (2ms variant) | 5 | **CLOSE** |
| `אני יהוה דברתי` "I YHWH have spoken" | 14 | emphatic **CLOSE** |
| `יד יהוה` hand-of-YHWH (MT 8:1 יד אדני יהוה) | 7 | **ONSET** of a vision |
| `שים פניך` "set your face toward" | 9 | sign-act / oracle direction opener |

**14 ORACLE DATELINES** — the strongest onset evidence in the book:
MT 1:1, 1:2, 8:1, 20:1, **24:1**, 26:1, 29:1, 29:17, 30:20, 31:1, 32:1, 32:17,
33:21, 40:1.

**CORRECTED 2026-09-08: this list was 13.** MT 24:1 — the siege dateline — was
missing because the first rule required a CARDINAL numeral stem and 24:1 writes
ordinals (`התשיעית`, `העשירי`, `בעשור`), which share no substring with them. A
dateline is now defined **structurally**: a YEAR word together with a MONTH or DAY
term, which needs no numeral vocabulary at all. Found by the Fable strategy
author, verified from bytes, ruled by the orchestrator. **14 is the count.**

A year word alone is not a dateline. Seven verses carry one and are NOT datelines:
MT 4:6 (a day for a year — sign-act), 29:11, 29:12, 29:13 (forty years — duration),
46:13 (a lamb of its first year), 46:17 (the year of liberty), and **MT 26:10,
which is a false positive of the year regex alone** — `שנה` appears there only
inside `תרעשנה` ("they shall shake"). The structural rule excludes all seven.

**FOUR date formulae that are NOT datelines: MT 45:18, 45:20, 45:21, 45:25.** These
are festival-calendar dates inside the temple-law section. They open no oracle, and
reading one as a unit onset puts a false boundary in the middle of a law block.

**Watch MT 45:18 above all.** It carries a full month+day formula (`בראשון באחד
לחדש`) *and* the messenger formula — exactly the combination that reads like an
oracle onset. **CORRECTED 2026-09-08: this list was three and omitted 45:18**, its
strongest member, because the rule reused a cardinal-numeral vocabulary that the
ordinal slipped past — the same root cause as the 13-vs-14 dateline miss. Found by
the distinct checker.

The rule is now word-anchored on the singular date construction `לחדש` / `בחדש`,
which also correctly excludes every `חדש` homograph in the book:

| form | sense | verses |
|---|---|---|
| `ובחדשים` | at the new moons | MT 45:17, 46:3 |
| `החדש` | the (day of the) new moon | MT 46:1, 46:6 — the closest near-miss: calendrical, same law section, no day number |
| `לחדשיו` | its months | MT 47:12 |
| `חדשים` | months (duration) | MT 39:12, 39:14 |
| `לב חדש` | a new heart | MT 18:31, 36:26 |

**MT 11:19 is NOT in that last row, and an earlier draft of this file wrongly put
it there.** 11:19 reads `לֵב אֶחָד` — "**one** heart" — with `רוּחַ חֲדָשָׁה` (citation forms, not byte quotes), "a new
spirit"; only the spirit is new. Many manuscripts and versions do read `חדש`
there, which is why the English tradition prints "a new heart", but WLC/OSHB — this
campaign's declared source — does not. The claim was caught by the distinct checker
and it refused the entire repair over it, correctly: a fabricated Hebrew reading
inside a correction note about byte fidelity is the exact error class the round was
opened to fix.

**THE THREE WORD-EVENT COUNTS ARE NEVER BLENDED.** 39 is the strict adjacent form,
41 adds the two verses with an infixed temporal phrase (MT 12:8 "in the morning";
MT 24:1 the ninth-year dateline), and 7 is the perfect `היה` form the dated oracles
use *after* their dateline. Quoting one where another is meant is the error class
this split exists to prevent — and note that the strict count alone understates
onset evidence **exactly in the dated blocks**, because those verses use the
perfect form.

**How to use the spine:**
- a **refrain CLOSES a unit** — the standing campaign rule — so a recognition
  formula or an utterance formula belongs to the unit **BEFORE** it, not the one
  after;
- a **seam is assessed from BOTH sides**: an onset-only diagnosis is incomplete
  until the adjacent unit's close is weighed from bytes;
- these are **EVIDENCE, not a verdict**. No boundary is set by a formula count
  alone.

### Flagged regions (raised coverage, no sampling shortcut — OW-6b hard track)

Recorded from the structural counts as candidates. **NOT a segmentation decision**;
the writer re-derives every boundary from bytes.

- **chs 1-3** inaugural vision and commissioning — vision-cycle seams, hand-of-YHWH onsets
- **chs 8-11** the temple vision — ONE transported vision across four chapters
- **the ch 20/21 NUMBERING ZONE** — every ref dual-qualified
- **chs 25-32** oracles against the nations — formula-dense, onset and close collide
- **chs 38-39** Gog — recapitulation-versus-sequence
- **chs 40-48** temple vision and land allotment — long measured description, few
  formulae, and the ch-40 K/Q cluster sits BESIDE the measurements: 3ms suffixes on
  architectural nouns, never on a cubit or reed numeral.
  **CORRECTED 2026-09-10:** this line still said the cluster "sits on the measurements"
  after the K/Q entry above was corrected on 2026-09-08. The correction did not sweep
  its own sibling statement. Found by the orchestrator while staging the tools.

---

## Data files (consume directly)

| file | what it is |
|---|---|
| `../Ezek_oshb.txt` | MT text, `ref\ttext`, 1,273 lines. **No maqaf, no paseq, no sof-pasuq, no morpheme `/`** — segs are dropped WITH their content by convention. |
| `../Ezek_web_clean.txt` | WEB extract: `===== EZEK N =====` banners, `¶` paragraph, `[v] N` verses, ` \|qN` poetry lines, `[fn]` at 38 note sites |
| `../Ezek_web.usfm` | the WEB member verbatim (sha256 `e8e3bf3c…`, asserted at extraction) |
| `../verse_inventory.json` | per-chapter WEB counts, total 1,273 |
| `../web_mt_offset_map.json` | the crosswalk + the Tier-0 rule; bijective, GREEN |
| `../web_mt_verse_check.json` | per-chapter counts both witnesses; divergent = [20, 21] |
| `../pmarks_Ezek.json` | parashah, paseq, K/Q, editorial notes, morph tally |
| `../ezek_device_inventory.json` | the frame spine above, with verse lists |
| `../ezek_kjv_variance_crosscheck.json` | the 37/37 independent corroboration |

## Staged tools (Tier-0, m8-mesh-r3) — staged 2026-09-10, after the writer wave; installed 2026-09-11 by receipts ezek_tools_install_t4fix_batch2.json and ezek_tools_install_toolfix2_batch3.json

Run with `PYTHONIOENCODING=utf-8 python <tool> ...` from this directory. **The variable is
not optional:** the tools print Hebrew, and without it the Windows console codec crashes a
tool, which the suite then reports as ERROR instead of as a finding.

| tool | contract |
|---|---|
| `run_validator_suite.py rows.jsonl` | runs every member; writes `<rows>.validator_report.json` beside its input. HARD members: citation_sweep, the normalizer (E-01), ngram7, cap_sweep (E-02) |
| `citation_sweep.py` | ref grammar and ranges, zone duals, mark / paseq / K/Q / puncta claims on refs, calendar-date onsets and dateline claims, Hebrew-quote binding in prose, and Hebrew inside a ref entry bound to that entry's own ref (S1-06) |
| `normalize_hebrew_in_json.py` | every Hebrew run byte-true to the verse text or to a Qere, standing on word boundaries (S1-07; collate_hebrew applies the same rule); an NFD-only match at the verse tier is REPLACED by the verse's bytes and counted fixed, and the suite treats fixed>0 as HARD (E-01); an NFD-only Qere match is a defect and is never replaced |
| `check_marks.py` | mark, K/Q and puncta claims in prose, each bound to the verse numbers of its own clause (C:V, C.V, `MT C:V` or dotted); absence phrases scoped to the verse, range or chapter they name; a negated K/Q is an absence claim (S1-22); a mark claim is also met by a mark of its type after the verse before (W1); a K/Q is negated only by a negator at most one word before it or heading a short comma list, and `no other K/Q` is checked against the span's K/Q verses the row names nowhere (W2, W5); `no pe or samekh` is an absence phrase (W6), read only in mark talk: a MARKISH_CTX word within 60 characters; besides that negator before it, a K/Q token is denied by a closed-set denial later in its clause, the same set as citation_sweep's DENIAL_COORD and DENIAL_COPULAR (T4-03); mark-disclosure symmetry (FLAGS) |
| `check_language_zones.py` | Aramaic labels — Ezekiel is Hebrew throughout |
| `cap_sweep.py` | a whole-chapter row is capped at medium_low, frontier-flagged and disclosed |
| `build_verse_maps.py` | built `verse_map_web.json`, `verse_map_oshb.json`, `consonantal_index.json` once at staging (1,273 / 1,273, token audit PASS) |
| `ezek_lib.py` | the shared library; `python ezek_lib.py` runs its selftest |

The other members — `check_web_quotes.py`, `check_refs_mirror.py`, `check_universals.py`,
`check_register.py`, `ngram7.py`, `check_tiling.py`, `collate.py`, `sweep.py`,
`check_atomic_isolation.py`, `_punct_boundary_sweep.py` — state their contracts in their
own docstrings. `check_register.py` carries the S1-05 arms, widened by REG-TF2-1 (repair history, positional row references, strategy
citations, governance posture), and `check_web_quotes.py` flags a prose field whose curly double
quote counts differ (S1-10).

**Where Ezekiel's tools differ from Jeremiah's** (each case tested in `_test_zone_tools_ezek.py`):
the numbering zone is WEB 20:45-21:32 / MT ch 21; there is no special-letter seg of any
class; a PUNCTA arm allows U+05C4 claims only at MT 41:20 and 46:22. A puncta claim binds
to the verse numbers written in its own clause (ended by a sentence stop, `;` or a
parenthesis) - in a ref annotation (citation_sweep) every such number at any distance, in
prose (check_marks) those within 60 characters of the word - and, in both, to every number
in a parenthetical that opens directly after that clause (`puncta extraordinaria (41:5)`
names 41:5), all in the same field, a named single verse must be a site; a written range must hold at least one site; among several named items
every one a site = a true claim, none = a false claim, a mix = ambiguous (a HARD
problem in citation_sweep, a flag in check_marks). With no number written, the row's span
or the ref's range decides. A negator earlier in the same comma-delimited clause makes the
claim a denial, and two adjacent negators cancel ("not without puncta" asserts them). A
denial may also FOLLOW the mention inside its clause, read through a parenthetical opening
directly after it, but only as one of a closed set: but|though|although|yet none, but|though|although|yet there is|are none,
none stands, none is present|written|there|found, none appears|exists, and is|are absent|lacking|missing at the
clause end - the set is DENIAL_COORD and DENIAL_COPULAR in citation_sweep.py; where this paragraph and the code differ,
the code is the contract and this paragraph is the defect. Dateline claims use the same test. A coordinated denial (`but none`, `none stands`, ...) denies only when the words
between the mention and the denial name no verse number or carry an expectation modal (would,
should, could, might, may, expected, anticipated); otherwise the mention is judged on the
numbers before the denial (`stand at 41:5 but none is present in ch 46` claims 41:5). So `45:18, where a dateline would be expected but none stands` is a denial,
while `opens no new year`, `none of` and `is missing its year word` are not, and a denial
behind a comma stays outside the clause. Digits that follow a letter directly (`R4.5`) are
an id, never a verse number. A
QERE tier accepts a Qere (which lives in the note layer, never in the verse bytes) only
when a ketiv/qere keyword stands in the same sentence within 160 characters of the quote,
and it compares the quote with the note's RAW bytes as split by `kq_split_bytes`: 66 of the
134 notes store their marks in non-canonical order, so an NFD comparison would reject a
byte-true Qere quote. A CALENDAR-DATE arm (citation_sweep, HARD; ruling G12(d)) fails a
row that opens at MT 45:20, 45:21 or 45:25 and any dateline claim that names one of the four
month+day dates without a year word (45:18, 45:20, 45:21, 45:25): in its comma-delimited
clause, in a parenthetical opening directly after it (`the dateline (45:18)`), in a list
running straight on from it, or - only when those name no number - as the number that ends
the immediately preceding comma clause (the apposition `45:18, a dateline-grade onset`); in
a ref's annotation a dateline claim
naming no number fails when the ref covers one of the four and no real dateline. A row may
open at 45:18, on its messenger formula; "not a dateline" and "non-dateline" pass. A
calendar date cited as onset evidence without the word "dateline" is not machine-checked.
An MT offset qualifier is read only in the closed form `(MT c:v)`. A
K/Q claim that names an editorial note may rest on an OSHB note recording a ketib/qere
relative to BHS; the WEB extract's footnote marker is a bare `[fn]`.

## Encoding + skeleton notes (READ before quoting Hebrew)

- The staged MT text is **NFC**. Match on a **consonantal skeleton** (strip
  `[֑-ׇ]` after NFD) when a form differs only in vocalisation —
  matching pointed text silently misses forms.
- **The extract carries no maqaf.** Words joined by maqaf in the source stand
  space-separated here. A pattern written with maqaf will match nothing; a claim
  that a maqaf is "absent from the text" is reading the extract, not the source.
- ezek_lib.skeleton() deletes U+05BE with the other points (POINTS spans U+0591-U+05C7), so a maqaf-joined quote never
  collates at any tier; its docstring sentence "maps maqaf to SPACE" is wrong and unasserted (T5-07, recorded as debt);
  write words space-separated, as the extract does.
- **No morphology layer in the staged extract.** Morph codes live in the XML;
  the tally in pmarks is a count, not a per-token layer you can query here.

## Standing rules (campaign governance)

- **No M7, comparison data, A/B lanes, or mixed-lane context — ever.** Re-derive
  every decision from the M8 witnesses.
- **Tier-4 metadata never drives a boundary** (E-23): translation punctuation,
  editorial headings, paragraphing.
- **Corpus-wide orders execute as their OWN sweep** (E-18), never folded per-row,
  with the narrowed-predicate label stamped in every report.
- **E-19 exact-path law**: no directory listings; open what your brief names, by
  exact path. Say so affirmatively in your report.
- **A cure is not cured because its author says so (OW-10)**: verification results
  must be bound to the exact resulting artifact (`artifact_sha256_at_run` = the
  shipped digest) plus a distinct-checker review. Enforced by
  `SP/campaign/_cure_verification.py`.
- **Every attempt records under its EXECUTION id** (`<attempt_id>#e<N>`), with
  layers A/B/C kept separate and never merged (OW-7/OW-8/OW-10;
  `SP/campaign/CAPTURE_CONTRACT.v3.md`).
- **Absence must be proven, not assumed.** Every "NONE" in the fabrication list
  above was byte-swept. If you need a new absence claim, sweep for it and cite
  the sweep.
