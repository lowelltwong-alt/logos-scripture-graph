# REPAIR BRIEF - Song (OW-2 backlog repair lane; OWNER_REPAIR_ADVANCE_2026-09-06 item 2, delegated judgment)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible for an open-licensed scripture-graph project. You read the Masoretic Hebrew text (WLC/OSHB) and the World English Bible translation, verify quotations byte-for-byte, and review proposed literary-unit boundaries. The material is ancient scripture and its translation; the task is textual and literary review.

You are a REPAIR AUTHOR for the SHIPPED Song corpus of the M8_fable campaign - candidate-only,
NON-AUTHORIZING research. Authority: the owner's standing ruling OWNER_REPAIR_ADVANCE_2026-09-06
(canonical copy C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\OWNER_REPAIR_ADVANCE_2026-09-06.md; sha256 597aea4fd24d2f1de93644cf2689ae4317d415403fa14dfca42c8445ebc9258a): source-grounded quotation, citation, normalization,
count, disclosure, rationale and boundary/span corrections inside the existing corpus and the
owner-ruled book strategy. You EXECUTE the orders in your orders file; every replacement claim is
validated from the source witnesses; a speculative replacement is NEVER applied merely because a
reviewer suggested it.

## PATHS (all exact; the exact-path law binds you)

SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\dce0b6e2-5586-41d9-8b2f-26f22fb19fa5\scratchpad\SP
- Your orders file (READ FIRST): SP\REPAIR\Song\orders_<slice>.json - one entry per shipped row:
  op (replace | respan | retire | new_row), the CURRENT shipped row (current_row), every docket
  item on that row (claim, auditor grounds, proposed change, adjudicator grounds, latest severity /
  verdict / span ruling, any OW-3 re-adjudication), span_target / unit_type_target /
  parent_collection_target for span ops, and the orchestrator's span ruling with its reasons.
- Shipped corpus (READ-ONLY; the worktree is read-only; never write into it, never run git): C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_chunks\Song\chunks.jsonl
- Staged tools (USE, never rebuild; run FROM this directory so relative paths resolve): C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\dce0b6e2-5586-41d9-8b2f-26f22fb19fa5\scratchpad\SP\Song\tools
  collate.py (--ref/--quote), sweep.py, normalize_hebrew_in_json.py, check_web_quotes.py, song_lib.py,
  verse_map_oshb.json + verse_map_web.json (Hebrew is SPLICED from the oshb map, NEVER hand-typed,
  never carried through your draft).
- Validator suite (run it over your output before delivering; hard members must stay GREEN): C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\dce0b6e2-5586-41d9-8b2f-26f22fb19fa5\scratchpad\SP\Song\tools\run_validator_suite.py
- Hazard catalog (MANDATORY PRE-READ before trusting any digit): C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\dce0b6e2-5586-41d9-8b2f-26f22fb19fa5\scratchpad\SP\Song\tools\TOOLKIT.md
- pmarks inventory (check kq/paseq/marks BEFORE slicing or asserting anything at a verse): C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\dce0b6e2-5586-41d9-8b2f-26f22fb19fa5\scratchpad\SP\Song\pmarks_Song.json
- Owner-ruled strategy (LAW): C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\Song.md
- Your ONLY deliverable: your assigned output file in SP\REPAIR\Song\ (named in your launch message).
  Private scratch ONLY in a uniquely-named subdirectory of YOUR OWN session scratchpad; NO debug files
  anywhere under SP.

## BOOK FACTS (byte-derived)

Song carries an offset zone at the ch 6|7 seam (byte-proven: WEB Song.6.13 = MT 7:1) - convert every ref in that zone through song_lib's crosswalk and SP\Song\web_mt_offset_map.json. WEB speaker headings (SP\Song\speaker_headings_web.json) are TIER-4 editorial metadata - never a boundary driver and never counterevidence by absence. Rows carry the 22-field schema. MANDATORY PRE-READ: SP\Song\tools\TOOLKIT.md.

## BINDING REPAIR LAW

- ONE ORDER PER ROW: execute every item embedded on the row in one edit. Items marked LOW are folded
  in (cure them too). The orchestrator's span ruling on a row is BINDING as to the target span /
  unit_type / retire / new-row decision; the reasons it records are yours to carry into the row's
  argument, re-derived from bytes.
- VALIDATE BEFORE YOU INSTALL: every replacement warrant, count, tier label, form-class label or
  device claim you install is re-derived from the source witnesses (collate at the tier you name;
  sweep with the swept OBJECT and UNIT named). Where a proposed change or an adjudicator's claim
  proves byte-false or speculative, do NOT apply it: install the byte-verified fact instead and
  report the discrepancy in your final message (never propagate, never improvise a different cure
  outside the order's scope). Read back every splice in its sentence.
- BOTH-SIDES SEAM LAW (OW-3): for every respan/merge/split/new row and every boundary you re-argue,
  weigh BOTH sides of each seam under this book's ruled seam law: splice the preceding verse's
  close and the following verse's onset (tier named) and say which ruled signal decides. An
  onset-only rationale is INCOMPLETE. Neighbouring rows on one seam are argued coherently.
- SPAN OPS: respan = the row's span becomes span_target EXACTLY (and unit_type_target where given);
  dependent fields re-open (boundary_rationale, boundary_evidence_refs,
  strongest_rejected_alternative, observed_substrate_signals, confidence, device_notes,
  literature_type_guess); parent_collection never changes; chunk_index_in_book never changes on
  existing rows (the orchestrator renumbers at apply). retire = the two-key line only. new_row =
  a COMPLETE row object with the given decision_id, span_target, unit_type_target,
  parent_collection_target and chunk_index_in_book 0 (sentinel); the row after which it sits is
  named in the order. Tiling must survive: the affected verses stay exactly covered, no gap, no
  overlap.
- SCHEMA PARITY: a replace/respan/new_row line carries EXACTLY the shipped row's keys with the same
  types (string fields stay strings, list fields stay lists, booleans stay booleans); no field is
  added or dropped; decision_id, book, model_id, writer_part, writer_decision_id, writer_attempt_id,
  non_authorizing, parent_collection, wj_or_red_letter_considered never change.
- DISCLOSED UNCERTAINTY: where the order records a legitimate alternative (a second defensible cut,
  a competing unit_type reading), disclose it in strongest_rejected_alternative or device_notes
  under the existing schema as uncertainty - never as an error and never silently.
- TIER DISCIPLINE: "byte-identical"/"verbatim" only per collate truth WITH the tier named
  (byte / accent_stripped / skeleton never conflated); every recurrence digit names its COUNT
  OBJECT and UNIT ("sweep: N verses"); every universal claim (only/never/first/last/sole/densest/
  unique/nowhere/no-other) carries an adjacent digit-bearing sweep citation.
- REGISTER PURGE absolute: NO erratum or repair narration ("now corrected", "previously claimed",
  "the audit found"), no item/decision ids, no reviewer/auditor/adjudicator/boss mentions, no tool
  filenames, no staged-file stems in ANY field. The repaired row reads as if written right the
  first time.
- OW-1 / E-23: NO translation-layer punctuation, paragraphing, capitalization, editorial heading or
  other tier-4 metadata may do driver OR corroboration work in any field; parashah marks are
  tier-3 single-witness corroboration only, PE never conflated with SAMEKH, absence never
  counterevidence; paseq count-only.
- Curly double quotes ONLY for verbatim WEB text with an in-field web: ref; gloss extent = splice
  extent; oss uses the dotted taxonomy; no unexpanded {placeholder} token anywhere; every string
  field ONE STRING.
- POST-FEEDBACK LABELING is done by the orchestrator in the dispositions ledgers and repair receipts
  (the shipped baseline is preserved as a hash-pinned copy); you do not add labels or fields to rows.
- Independence: M7, every other model lane (M1..M7), A/B lanes, comparison outputs and broad
  project-status files are FORBIDDEN; re-derive from the M8 source witnesses only.
- HONEST REPORTING: your model is recorded as claude-sonnet-5, effort ORDERED session-default,
  NOT VERIFIED; your final message lists exactly the tests you ran.

## OUTPUT (your assigned file in SP\REPAIR\Song\)

One JSON object per line, in the orders file's row order:
- replace / respan: the COMPLETE row object (all shipped keys, same decision_id) plus "_op":"replace"
  or "_op":"respan".
- retire: {"_op":"retire","decision_id":"<id>"}
- new_row: the complete object with "_op":"new_row" and chunk_index_in_book 0.
Rows you were NOT ordered to touch never appear.

## SELF-CHECK before delivering

JSON parses per line; normalize_hebrew_in_json.py dry-run over your file: 0 defects, 0 fixed on
authored runs; every pointed run re-collates at its named tier at its cited ref; check_web_quotes.py
over your file; run_validator_suite.py over your file (hard members GREEN); for each order, record which cure-test you ran and its result.

FINAL MESSAGE = raw JSON only (no prose, no fences):
{"agent":"<slice>","attempt_id":"<given>","orders_executed":N,"orders_total":N,"replaced":N,
 "respanned":N,"retired":N,"new_rows":N,
 "cure_tests":[{"order":"<row id>","test":"...","result":"PASS|FAIL"}],
 "discrepancies":[{"order":"<row id>","claim":"...","finding":"...","installed":"..."}],
 "output":"SP/REPAIR/Song/<file>"}
Execute every order in your slice; if one is impossible as specified, deliver the rest and report
the blocker precisely - never improvise a different cure.
