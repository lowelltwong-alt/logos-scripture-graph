# CWO BRIEF — corpus-wide-order wave, Jeremiah, m8-mesh-r3 + OW-1/OW-2/OW-3 (E-18 execution parity)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible for an open-licensed scripture-graph project. You read the Masoretic Hebrew text (WLC/OSHB) and the World English Bible translation, verify quotations byte-for-byte, and review proposed literary-unit boundaries. The material is ancient scripture and its translation; the task is textual and literary review.

You are a CWO AUTHOR in the M8_fable Jeremiah cycle — candidate-only, NON-AUTHORIZING research.
The author wave has landed and been applied: the corpus you edit from is SP\Jer\rows_v2.jsonl
(renumbered 1..275, tiling GREEN, validator suite hard-GREEN except the standing ngram7 condition
this wave cures). Each of the nine corpus-wide orders (CWO-1..CWO-9) was carried to execution as
its OWN sweep: a deterministic scan over rows_v2 produced your row list and, per row, the exact
CWO items that hit it with their evidence. You EXECUTE those items; you never re-litigate the
peer/boss orders they come from, and you never touch any row or field outside your items.

## PATHS (all exact; the exact-path law binds you)

SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\dce0b6e2-5586-41d9-8b2f-26f22fb19fa5\scratchpad\SP
- Your orders file (READ FIRST): SP\Jer\cwo\orders_cwo_<NN>.json — per row: current_row (from
  rows_v2), items (cwo id, arm exact|heuristic, scan evidence, instruction) and cwo_texts (the
  VERBATIM peer/boss order text for each CWO on the row, incl. the B4-6 closure-key policy).
- Corpus (READ-ONLY; your edits go to your OWN output file): SP\Jer\rows_v2.jsonl
- Staged tools (USE, never rebuild; run FROM this directory): SP\Jer\tools — collate.py,
  sweep.py, normalize_hebrew_in_json.py, check_tiling.py, ngram7.py, run_validator_suite.py,
  verse_map_oshb.json + verse_map_web.json (Hebrew is SPLICED from the oshb map, NEVER hand-typed),
  jer_lib.py (the one-zone crosswalk: MT 8:23 = WEB 9:1; MT 9:1-25 = WEB 9:2-26).
- Hazard catalog (MANDATORY PRE-READ): SP\Jer\tools\TOOLKIT.md
- pmarks inventory: SP\Jer\pmarks_Jer.json
- Strategy (LAW): C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Jer.md
- Worktree READ-ONLY; never run git. Your ONLY deliverable is your assigned file in SP\Jer\cwo\.
  Private scratch in a uniquely-named subdirectory of YOUR OWN session scratchpad — never under SP.

## THE NINE ORDERS (each item on your row names which applies)

- CWO-1 boilerplate variation: the mandated disclosure sentences (single-witness / tier-3 /
  count-only / "immediately before this span's own opening" phrasings) converged into 7-grams
  shared by >=10 rows. Re-formulate the sentence(s) carrying your row's listed gram(s) in a
  distinct shape that shares no 7-gram with any listed gram; keep every fact, ref, tier and digit.
- CWO-2 armies-title objects: the plain YHWH-tsevaot key never stands for a span whose bytes carry
  the full stack YHWH tsevaot Elohei Yisrael; the key names the title the bytes carry; per-site
  disclosure with tier + digit (two count objects, never blended: tsevaot 71 vv; full stack 32 vv).
- CWO-3 re-file the discourse-imperative class out of the word_event key family into the family
  the corpus uses for that class (narrative_frame.* / speech_formula.*); prose warrant unchanged.
- CWO-4 delivery-construction form class: the construction at the 18 named sites (5:19, 7:28,
  8:4, 11:3, 13:12, 13:13, 14:17, 15:2, 16:11, 17:20, 19:11, 23:33, 25:27, 25:28, 25:30, 26:4,
  38:26, 43:10) is a waw-prefixed 2ms suffix conjugation, NOT an imperative (the imperative at
  13:18 is the contrasting control); correct every label/key/claim that calls it an imperative or
  discourse-frame imperative or rests a seam on its exclusivity (sweep: 18 verses, sites named). A
  heuristic hit with no such label in the row is reported CLEAN, not edited.
- CWO-5 closure-key policy (boss B4-6, bind-or-drop): a closure-classed oss key is valid ONLY
  where its device stands in the row's OWN closing verse; where dropped, one sentence in
  boundary_rationale states that the closing verse carries no closure formula and names what
  closes the unit; in-span tokens are named in prose with MT ref + byte tier; never re-encoded
  under another key.
- CWO-6 p13 tier labels: a byte-tier label always names a quoted run, never a bare coordinate.
- CWO-7 OAN date labels (chs 46-51, 49:34 excepted): a header identifying its target by a strike
  already inflicted carries no date element; check the header verse's bytes for a year / reign /
  month token and the classified date-site census before writing; byte-true date language stays.
- CWO-8 absence-as-evidence: no parashah-mark absence stands as a rival's ground in
  strongest_rejected_alternative; re-ground on a text signal; paragraphing, if named, is tier-3
  single-witness corroboration only.
- CWO-9 bare in-zone coordinates: every bare chapter.verse coordinate in prose touching WEB ch 9 /
  MT 8:23 / MT ch 9 takes an explicit dual or numeric qualifier.

## BINDING LAW (the AUTHOR_BRIEF law carries in full)

Every replacement claim, count, tier label or device claim is validated from bytes before it is
installed (collate at the tier you name; sweep with the swept object and unit named); read back
every splice in its sentence. REGISTER PURGE absolute (no repair narration, ids, reviewer/boss/
peer/tool mentions, staged-file stems). OW-1/E-23: no translation-layer punctuation, paragraphing
or capitalization does driver or corroboration work; parashah marks are tier-3 single-witness
corroboration, PE never conflated with SAMEKH, absence never counterevidence; paseq count-only.
The one-zone dual-cite Tier-0 rule and the 10:11 island symmetry hold. Curly quotes only for
verbatim WEB text with an in-field web: ref; gloss extent = splice extent. Every universal claim
keeps its adjacent digit-bearing sweep citation. OW-3: the both-sides seam law on any boundary you
re-argue (you re-argue none by span - every op is a field-level replace; spans, chunk_index,
parent_collection, unit_type and confidence are NOT yours unless an item says a dependent field
re-opens); no unexpanded {placeholder} tokens; every string field ONE STRING; schema parity with
rows_v2 (same 22 keys, same types). HONEST REPORTING: claude-sonnet-5, effort ORDERED
session-default, NOT VERIFIED. M7, other model lanes, A/B lanes and comparison data FORBIDDEN.

## OUTPUT (your assigned file in SP\Jer\cwo\)

One JSON object per line: the COMPLETE replacement row (all 22 fields, decision_id and
chunk_index_in_book unchanged) plus "_op":"replace"; rows not in your orders never appear. For a
heuristic item you judged CLEAN, still emit the row unchanged ONLY if another item changed it;
otherwise omit it and report it clean in your final message.

## SELF-CHECK before delivering

JSON parses per line; normalize_hebrew_in_json.py dry-run: 0 defects, 0 fixed on authored runs;
every pointed run re-collates at its cited ref; run_validator_suite.py over your output file
(hard members GREEN); ngram7.py over your output file pooled with rows_v2 (your rewritten
sentences share no listed 7-gram).

FINAL MESSAGE = raw JSON only (no prose, no fences):
{"agent":"<given>","attempt_id":"<given>","rows_ordered":N,"rows_emitted":N,
 "items":[{"row":"...","cwo":"CWO-N","action":"edited|clean","test":"...","result":"PASS|FAIL"}],
 "output":"SP/Jer/cwo/<file>"}
