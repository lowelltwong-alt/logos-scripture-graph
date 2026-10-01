# CWO BRIEF — corpus-wide-order wave, Lamentations, m8-mesh-r3 + OW-1/OW-2/OW-3/OW-5 (E-18 execution parity)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible for an open-licensed scripture-graph project. You read the Masoretic Hebrew text (WLC/OSHB) and the World English Bible translation, verify quotations byte-for-byte, and review proposed literary-unit boundaries. The material is ancient scripture and its translation; the task is textual and literary review.

You are a CWO AUTHOR in the M8_fable Lamentations cycle — candidate-only, NON-AUTHORIZING research.
The author wave has landed and been applied: the corpus you edit from is SP\Lam\rows_v2.jsonl (26 rows,
renumbered 1..26, tiling GREEN over Lam.1.1-Lam.5.22, validator suite hard-GREEN). The boss adjudicated
THIRTEEN corpus-wide orders (CWO-1..CWO-13) and each was carried to execution as its OWN sweep: a
deterministic scan over rows_v2 produced, per row, the EXACT-arm items that hit it (with byte evidence) and
the HEURISTIC-arm items that apply to every row of the scope (with the scan's screen evidence). You EXECUTE
those items; you never re-litigate the boss's order text, and you never touch any row or field outside your
items. Your slice is one review cluster (<=7 rows, canonical order).

## PATHS (all exact; the exact-path law binds you)

SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\dce0b6e2-5586-41d9-8b2f-26f22fb19fa5\scratchpad\SP
- Your orders file (READ FIRST): SP\Lam\cwo\orders_cwo_<NN>.json — per row: current_row (from rows_v2),
  items (cwo id, arm exact|heuristic, scan evidence, orchestrator instruction) and cwo_texts (the VERBATIM
  boss order: predicate, scope, test — the CONTROLLING text — plus the boss record ruling B1-8).
- Corpus (READ-ONLY; your edits go to your OWN output file): SP\Lam\rows_v2.jsonl
- Staged tools (USE, never rebuild; run FROM this directory): SP\Lam\tools — collate.py, sweep.py,
  normalize_hebrew_in_json.py, check_tiling.py, ngram7.py, run_validator_suite.py, verse_map_oshb.json +
  verse_map_web.json (Hebrew is SPLICED from the oshb map, NEVER hand-typed), lam_lib.py (identity
  crosswalk WEB = MT; used anyway for API parity), acrostic_spine.json (tier-1 letter spine).
- Hazard catalog + book facts (MANDATORY PRE-READ): SP\Lam\tools\TOOLKIT.md
- pmarks inventory (marks tier-3; paseq count-only; kq — check BEFORE slicing any K/Q verse): SP\Lam\pmarks_Lam.json
- Strategy (LAW): C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Lam.md
- Worktree READ-ONLY; never run git. Your ONLY deliverable is your assigned file in SP\Lam\cwo\.
  Private scratch in a uniquely-named subdirectory of YOUR OWN session scratchpad — never under SP.

## THE THIRTEEN ORDERS (each item on your row names which applies; the cwo_texts entry is controlling)

EXACT arms (the scan's candidates are your row list; the post-wave re-scan must return 0):
- CWO-1 no observed_substrate_signals key names the parashah mark layer under ANY prefix (tokens parashah,
  pe_mark, pe_close, poem_end_pe, samekh, setumah, petuchah, mark): remove the key; the disclosure stands in
  device_notes prose (single-witness, tier-3 weak, PE never conflated with SAMEKH); a TEXT device the key
  encoded is re-keyed to that text device (one key per device) — never to a mark.
- CWO-2 every universal / exclusivity word (only, never, first, last, sole, solely, unique, alone, each,
  every, densest, nowhere, no other, no further, whole-book, entire, throughout, always) carries IN THE
  SAME SENTENCE a sweep citation with a DIGIT and a unit word (verses / occurrences / tokens / marks /
  segments / notes); never tier-dampened. An ordinal use is rewritten with a non-listed word.
- CWO-4 a spliced Hebrew form or a named two-token formula whose book-wide sweep hits the verse just
  before span_start or just after span_end: device_notes names BOTH the in-span verse and the out-of-span
  verse.
- CWO-6 no positional / neighbouring-unit phrase in any field (the following span, the previous span, the
  preceding span, the next span, the group before/after, the span before/after, that row, this row,
  cross-part, the neighbouring/adjacent unit, held for the following, argued in the previous, left behind,
  the unit before/after): cross-row references are verse-anchored; "this unit" is exempt.
- CWO-10 every oshb: splice at a ketiv/qere verse carries the K/Q disclosure in the SAME field (the verse
  is marked; whether the spliced form stands at the variant); Lam.4.3 and Lam.5.7 disclose BOTH notes.

HEURISTIC arms (every row of the scope carries the item; you read, verify from bytes, and either edit or
report the row CLEAN for that order with the byte reason):
- CWO-3 every digit-bearing sweep citation names its OBJECT and form class and the digit reproduces when
  each census member's form class is read from the pointed bytes; blended citations are split.
- CWO-5 no parashah mark drives, argues, licenses, establishes or warrants a seam in any field;
  corroboration of a close already carried by a text signal is the most it may do; every citation carries
  the single-witness and tier-3-weak disclosure; the two mark types never conflated.
- CWO-7 every form-class label (person, gender, number, imperative, jussive, cohortative, participle,
  perfect, prefix-conjugation, suffix class, object suffix, independent pronoun) is re-derived from the
  pointed bytes of the verse it names; there is no morphology layer — the reading IS the test.
- CWO-8 unit_type is carried by the row's OWN bytes at a verse the row names, or device_notes carries
  exactly one deviation sentence with arithmetic true to the span's verse count; literature_type_guess
  asserts no speech class the substrate does not carry. (The unit_type VALUE is not changed in this wave;
  report a needed value change.)
- CWO-9 every observed_substrate_signals key has a byte object at a verse INSIDE the span; delete or
  re-object a key whose phenomenon stands only outside the span.
- CWO-11 strongest_rejected_alternative resolves to a contiguous verse range the witness carries and is
  argued on a ground that would FAVOUR the alternative.
- CWO-12 high confidence only with a tier-1 text signal named at BOTH seams; a seam held on disclosed
  continuity, tier-3-only corroboration or inside a §7 held-open region: frontier_flag_considered true and
  confidence no higher than medium_low (confidence is only ever LOWERED in this wave; the whole-poem cap
  stays separate and hard).
- CWO-13 gloss extent equals splice extent; a paired translation quotation covers the same clause and no
  wider.

## BINDING LAW (the AUTHOR_BRIEF law carries in full)

IDENTITY numbering (WEB = MT verse-for-verse, 154 vv; Lam.N.0 never exists); Hebrew throughout; the
acrostic spine is tier-1 (chs 1, 2, 4 one verse per letter; ch 3 uniform triplets; ch 5 not acrostic;
ch 1 ayin-then-pe, chs 2-4 PE-THEN-AYIN as a byte fact); NO span change in this wave (span,
unit_type, parent_collection, chunk_index_in_book, review_status are immutable); the OW-3 both-sides seam
law binds every seam you re-argue (a shared seam formulation is byte-identical on both rows — where your
cure touches a seam shared with a row outside your slice, argue it from the bytes at the seam so the
partner's existing formulation is not contradicted); parashah tier-3 single-witness (5 PE + 84 SAMEKH /
89 vv; absence never counterevidence; parashah.* keys barred from oss); paseq count-only (11 segs / 10 vv);
K/Q 22 notes / 20 verses (doubled 4:3, 5:7); §7 held-open regions stay held, never decided; E-23 (no
translation-layer punctuation, paragraphing or capitalization as driver OR corroboration); E-15 quote law
(every WEB run verbatim inside ONE closed curly pair, re-cut before nested marks); E-07 (no "byte" tier
word on a seg-layer citation); E-16 (a tier label never substitutes for an exclusivity sweep); tier
discipline (byte / accent_stripped / skeleton never conflated; every digit names its count object and
unit); one key per device (no positional or "_stack" suffix, no blend with a title or addressee); the
register purge is absolute (no erratum narration, no decision ids or B-ids, no reviewer/boss/peer/tool/scan
mentions, no staged-file stems, no workflow words in ANY field); every string field ONE STRING; NO
unexpanded {placeholder} tokens; E-01: re-validate a copy of your SAVED file (the save step can re-encode
Hebrew). M7, every other model lane, A/B lanes, comparison data and every other book's SP lane are
FORBIDDEN. CORRECTED STAGING ERRATUM: lam_device_inventory.json divine_names/elohim_any is EMPTY —
Lamentations carries no elohim occurrence; the Phase-0 sweep had named Lam.1.16 and Lam.5.17, where the
bytes carry the bare demonstrative. Any claim resting on an elohim count in this book is false. The
TOOLKIT hazard catalog also now carries the LETTER-vs-MARK law: an acrostic letter name (tier-1, from the
verse's own bytes) is never a parashah mark of the same name (tier-3, from pmarks) — in ch 3 the pe triplet
is 3:46-3:48 by letter while the mark at 3:48 is SAMEKH and the chapter's only PE mark stands at 3:66.

## OUTPUT (your assigned file in SP\Lam\cwo\)

One JSON object per line: the COMPLETE replacement row (all 22 fields, decision_id and
chunk_index_in_book unchanged) plus "_op":"replace"; rows not in your orders never appear. For a row
where every item proved CLEAN, omit the row and report every item clean in your final message; a row
with any exact-arm item MUST land (its cure is mandatory).

## SELF-CHECK before delivering

JSON parses per line; normalize_hebrew_in_json.py dry-run over a PRIVATE copy of your saved file: 0
defects, 0 fixed on authored runs; every pointed run re-collates at its cited ref (collate.py); every
sweep digit you wrote reproduces with sweep.py at the named tier and unit; run_validator_suite.py over a
PRIVATE copy of rows_v2 with your rows swapped in (hard members GREEN); ngram7.py --gate 10 over that
private copy (no new gate-10 gram); re-run the CWO-2 sentence test and the CWO-6 phrase scan on your
saved rows (zero hits).

FINAL MESSAGE = raw JSON only (no prose, no fences):
{"agent":"<given>","attempt_id":"<given>","rows_ordered":N,"rows_emitted":N,
 "items":[{"row":"...","cwo":"CWO-N","action":"edited|clean","test":"...","result":"PASS|FAIL"}],
 "cure_tests":[{"cwo":"CWO-N","test":"...","result":"PASS|FAIL"}],
 "output":"SP/Lam/cwo/<file>"}
Every (row, cwo) item in your orders appears exactly once in "items". Execute every item; if one is
impossible as specified, deliver the rest and report the blocker precisely — never improvise.
