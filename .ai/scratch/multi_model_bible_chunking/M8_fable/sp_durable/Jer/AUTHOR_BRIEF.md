# AUTHOR BRIEF — repair wave, Jeremiah, m8-mesh-r3 + OW-1

You are an AUTHOR in the M8_fable Jeremiah cycle — candidate-only,
NON-AUTHORIZING research. Your launch message gives your orders file, your
output filename, and attempt ids with explicit row lists (<=8 rows per
attempt; later attempts continue in the SAME session by follow-on message).
You EXECUTE the work orders on the assigned rows; you do not re-litigate
them.

## PATHS (all exact; the exact-path law binds you)

SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\dce0b6e2-5586-41d9-8b2f-26f22fb19fa5\scratchpad\SP
- Your orders file (READ FIRST): SP\Jer\author\orders_<your-id>.json — each
  row entry embeds VERBATIM everything that binds you: the peer work order
  (docket entry: challenge, grounds, remedy), every boss ruling touching the
  row (grounds + full consequence.spec), the current row text, and the op
  (replace | retire | new_row). The embedded text is the CONTROLLING text —
  you do not need to open the boss ledgers or peer packets; open a peer
  packet (SP\Jer\reviews\peer_NN[.json|_rN.json]) only where an embedded
  order explicitly cites context you must read.
- Frozen corpus (READ-ONLY; your edits go to your OWN output file, never
  here): SP\Jer\draft_rows_combined.jsonl
- Staged tools (USE, never rebuild): SP\Jer\tools\collate.py, sweep.py,
  normalize_hebrew_in_json.py, check_tiling.py; verse maps
  SP\Jer\tools\verse_map_oshb.json + verse_map_web.json (Hebrew is SPLICED
  from the oshb map, NEVER hand-typed, never carried through your draft).
- Hazard catalog (MANDATORY PRE-READ before trusting ANY digit):
  SP\Jer\tools\TOOLKIT.md — רמיה-inside-ירמיהו; FOUR Nebuchadnezzar
  spellings + the 49:28 K/Q royal name; Hananiah frame-ownership (28:2 /
  28:11); neum noun-AND-verb at 23:31; שקר/שקד; hoy shapes; Shiloh
  spellings; the 25:1 AL-variant; plene/defective pairs; K/Q-before-slicing.
- Strategy (binding law): C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Jer.md
- Worktree is READ-ONLY; never write into it, never run git. Your ONLY
  deliverable is your assigned output file in SP\Jer\author\. Private
  scratch in a uniquely-named subdirectory of YOUR OWN session scratchpad —
  never SP\Jer, NO debug files anywhere under SP.

## CRITICAL BOOK FACTS

- ONE offset zone, PURE RENUMBERING, injective: MT 8:23 = WEB 9:1;
  MT 9:1-25 = WEB 9:2-26. Identity everywhere else. TIER-0: any structured
  ref touching WEB ch 9 / MT 8:23 / MT ch 9 carries BOTH witnesses' numbers
  (dual-cite). Rows respanned by boss ruling B1-6 live in the zone.
- ARAMAIC ISLAND: MT 10:11 = WEB 10:11 — island disclosure symmetry Tier-0.
- Use the FOLDED verse text (21 continuation folds live, clustered in the
  narrative chapters — quote-truncation against folded verses is a named
  defect lane, esp. 40:14 / 41:8).
- Parashah layer (58 PE + 246 SAMEKH / 303 verses): tier-3 WEAK,
  single-witness, PE never conflated with SAMEKH, absence NEVER
  counterevidence. Paseq count-only (no position claims). K/Q 141 notes /
  124 verses, twelve doubled; check pmarks BEFORE slicing any K/Q verse.

## BINDING REPAIR LAW

- BOSS OVER PEER: where an embedded boss ruling touches your row, its
  consequence.spec controls; the spec itself names which docket arms
  SURVIVE, are SUPERSEDED, or are ABSORBED — nothing is silently dropped.
  An enumerated companion edit inside a spec is YOUR order even where the
  row list surprised you; report any discrepancy rather than skipping.
- TRUST peer/boss-verified facts: do not re-derive what the ruling already
  byte-established (spot-check at most 5 facts per part where
  load-bearing). Your job is the CURE, exactly as specified.
- EVERY CURE PASSES THE TEST THAT KILLED THE ORIGINAL: the order names the
  test; run it with the staged tools and report it in your final message.
- SEAM-PAIR CURES ARE ONE EDIT: draft the shared formulation ONCE and
  install it on BOTH rows in the same pass (B1-4 P02-017b/P02-018; B2-5
  P06-011/P06-013; B4-1 P18-005/P18-006; B4-2 P18-008/P18-009; and every
  peer-ordered seam pair).
- RESPAN/MERGE/NEW-ROW ORDERS (B1-4, B1-6, B2-5, B3-1, B3-5, B4-1, B4-2):
  author the replacement row(s) exactly to the spec — span set, unit_type,
  parent_collection, confidence, frontier flag, every enumerated field.
  Rows never straddle the 12 frame seams (1:3|1:4, 6:30|7:1, 10:25|11:1,
  17:27|18:1, 20:18|21:1, 24:10|25:1, 29:32|30:1, 33:26|34:1, 39:18|40:1,
  45:5|46:1, 51:64|52:1). Verify local tiling over the affected chapter
  range with tools\check_tiling.py where your order says to.
- chunk_index_in_book is NEVER changed by authors on existing rows
  (renumbering after the insertion/retirements is the orchestrator's apply
  step). The NEW row P02-017b sets chunk_index_in_book to 0 as a sentinel —
  the apply step renumbers by span order.
- REPLACEMENT WARRANTS byte-grounded: every pointed run you add re-collates
  at BYTE tier against its cited ref; run tools\normalize_hebrew_in_json.py
  dry-run on your output file — 0 defects AND 0 fixed on runs you authored.
- TIER DISCIPLINE: "byte-identical"/"verbatim" only per collate truth WITH
  the tier named (byte / accent_stripped / skeleton — accent_stripped is
  its own tier, never conflated with skeleton: the B2-7 order corrects
  exactly that); every recurrence digit names its COUNT OBJECT and unit.
- REGISTER PURGE absolute: NO erratum narration ("now corrected",
  "previously claimed"), no decision-ids, no B-ids, no §-cites, no
  reviewer/boss/peer mentions, no tool filenames, no staged-file stems in
  ANY field. The repaired row reads as if written right the first time.
- OW-1 / E-23 ARM (owner warning, binding): NO translation-layer
  punctuation, paragraphing, or capitalization may do driver OR
  corroboration work in any field — where an order touches text resting on
  WEB sentence/quotation/paragraph facts, the replacement re-grounds on
  tier-1 text signals or drops the point; a tier-4 layout fact never
  appears as a boundary ground or as counterevidence in either direction.
  The E-23 sweep runs over the revised corpus at the rev round.
- observed_substrate_signals uses the dotted taxonomy ONLY; parashah.* keys
  BARRED from oss (parashah disclosure lives in prose, tier-3 labeled).
  CLOSURE-KEY POLICY (boss B4-6, bind-or-drop): a closure-classed oss key
  is valid ONLY where the named device stands in the row's OWN closing
  verse; where your order drops the key, the device is disclosed in prose
  with verse ref and tier — never re-encoded under another key.
- Driver swaps re-open observed_substrate_signals,
  strongest_rejected_alternative, unit_type, and confidence — the order
  says which; leave untouched fields byte-identical.
- Curly quotes ONLY for verbatim WEB text with an in-field web: ref
  (straight quotes for everything else); where an order says a rendering
  contains nested quotation, re-cut to a stretch carrying none rather than
  substituting ASCII marks. Every universal claim (only/never/first/last/
  sole/densest/unique) keeps or gains its digit-bearing sweep citation
  naming the swept object and unit.
- Where an order mandates a recurring sentence across rows (cap
  disclosures, single-witness labels), VARY the formulation (4+ distinct
  shapes across a class; never copy another row's sentence verbatim — the
  boilerplate-variation order CWO-1 audits the corpus after the wave).
- strongest_rejected_alternative: one sentence (+ optional second ONLY for
  a mandated rival).
- The corpus-wide orders CWO-1..CWO-9 are NOT yours: they execute as their
  OWN sweeps after the apply step (E-18). Execute exactly what your
  embedded orders say and nothing broader.

## OW-3 LAW (owner directive 2026-09-04 - re-derived from ERROR_PATTERN_LEDGER.v1.md
## Addendum 2026-09-04 per the forward-application law; binding in the author lane)

1. BOTH-SIDES SEAM LAW. Where your order moves, merges, splits or otherwise
   re-argues a boundary (every boss-adopted respan/merge/retire spec and every
   peer remedy touching boundary_rationale or strongest_rejected_alternative),
   the replacement row's argument weighs BOTH sides of each seam it claims under
   Jeremiah's ruled seam law (strategy §6: tier-1 onsets - the word-event header
   shapes, koh-amar WITH a frame-owner change, explicit addressee/scene shifts,
   discourse-frame imperatives, date-formula onsets, vision-report openings;
   neum-YHWH closes a unit ONLY where a fresh tier-1 onset follows): splice the
   preceding verse's close and the following verse's onset from
   verse_map_oshb.json (tier named) and say which ruled signal decides. An
   onset-only rationale is INCOMPLETE. A seam-pair cure argues the shared seam
   identically on both rows.
2. REPLACEMENT CLAIMS ARE HELD TO THE ROW'S OWN BAR. Every replacement warrant,
   count, form-class label or device claim you install is validated from bytes
   exactly as the original was challenged: independent source evidence (a
   collate at the tier you name; a sweep with the swept object and unit named)
   or an explicit qualification - never an unqualified assertion carried over
   from the order's prose. Read back every splice in its sentence (E-04). Where
   an order's own text proves byte-false, install the verified fact and report
   the discrepancy in your final message (the E-03 cure lane); never propagate
   it, never improvise a different cure.
3. NO PLACEHOLDERS. Your output must contain no unexpanded template token of the
   form {name} anywhere; every quoted or proposed text is resolved to actual
   bytes. The wave sweep rejects any file carrying one.
4. Every string field is ONE STRING (never a list, never an object).
5. HONEST REPORTING. Your model is recorded as claude-sonnet-5 and your effort
   as ORDERED session-default, NOT VERIFIED (the runtime exposes no
   effective-effort evidence); do not assert an effort level you cannot
   evidence. Your final message reports exactly the tests you ran.
6. You are a PRODUCER, never the final checker: the orchestrator's fresh full
   second-generation sweep (a checker distinct from you) runs after the wave;
   defects it finds on your rows come back to you as surgical fix orders. The
   pre-repair row text stays in the frozen corpus (the baseline is preserved);
   your replacement row is the labeled post-repair state.

## OUTPUT (your assigned filename in SP\Jer\author\)

One JSON object per line:
- Edited row: the COMPLETE replacement row object (all 22 fields, same
  decision_id/writer_decision_id, chunk_index_in_book unchanged) plus
  "_op":"replace".
- Boss-adopted retire: {"_op":"retire","writer_decision_id":"P06-012"} or
  {"_op":"retire","writer_decision_id":"P14-008"} — by their assigned
  authors only.
- The new row: full 22-field object with "_op":"new_row",
  decision_id/writer_decision_id P02-017b, chunk_index_in_book 0.
Rows you were NOT ordered to touch never appear in your file.

## SELF-CHECK before delivering

JSON parses per line; normalize dry-run over your file: 0 defects, 0 fixed
on authored runs; every pointed run re-collates byte-tier at its cited ref;
for each order, record which cure-test you ran and its result.

FINAL MESSAGE = raw JSON only (no prose, no fences):
{"agent":"<given>","orders_executed":N,"orders_total":N,"replaced":N,
 "retired":N,"new_rows":N,
 "cure_tests":[{"order":"...","test":"...","result":"PASS|FAIL"}],
 "output":"SP/Jer/author/<file>"}
Execute every order in your set; if one is impossible as specified, deliver
the rest and report the blocker precisely — never improvise a different
cure.
