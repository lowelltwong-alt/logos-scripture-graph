# 1 Corinthians merged close, lane A, re-check a3 (cor_merged_close_lane_a_a3#e1)
Model claude-opus-5-5, grader_fallback (OW-25). Re-check of my a2 outputs (1Cor/merged_close/lane_a_e2/).
Corpus 4287903015be9fcd088e8d4d1c6c6c2ce564c8af46e7f994e5a2768d554cf9ea, unchanged; 98 pins, 0 mismatches.

## Verdicts
- Postcheck: fit_to_assemble (carried from a2; the a3 delta does not touch the row bytes). Three low residuals carried.
- Final check (OW-6): fit_to_close on the evidence read. The stage-1 transcript audit is OWED, NOT MET; the campaign-end review is DEFERRED (OW-28), and deferred is never met.
- Items 20-23: all fit_to_accept. Item 21 moves from false to true. Item 22 feed 5d81467f.

## What the delta cured (a2 blockers)
- Fable end packet a94c9338 reproduces over this corpus: dry gates MATCH, 20/20 rows, 27 routed, sidecars 640f95ae.
- gen_method_v8.py re-pinned to 4287903015be: --check MATCH 53601c73 (copy); checker PASS, selftest PASS, record unchanged.
- Landed-outputs manifest 06b1c6a8 pinned and MET.

## Re-judged
- Close-gate assessment: item 21 is now DEFERRED_OW28_FABLE_END_REVIEW; packet and manifest entries met; new entry for the 2026-11-03 gate addendum (met, two low citation notes); OW-29 noted against OW-38.
- NQ-4 (the atlas feed is now a shared write of the close act), NQ-5 (receipt silent on OW-38), NQ-6 (8 unmet, none a row defect). NQ-14 carried; the v7 rule-2 gap and the E7 flag are still recorded in none of the changed files (0 hits).
- README audit: every measured claim I tested is true; some claims are REPORTED only.
- Everything else carried_from_a2 with its a2 sha256; reissue_item_1, _14 and _25 carried.

## New low residuals
- Gate addendum: the 5-hour-limit sentence is cited to OW-37 point 3 but sits in its 'What it does not grant' paragraph; two clauses of point 3 omitted.
- close_params authority_text omits OW-38's report-before-close for 1 Corinthians.
- README line 5 names OW-29 for the merge, not OW-38.

## Still standing before --close (not mine to clear)
- The close tool raises in its lane group: TypeError 'int' object is not iterable. Lane A's gates evaluated before it, so the raise point is INFERRED outside lane A's data.
- The other lane's verdicts; close evidence items 16, 18, 19 (due at the act); --next-book (John, OW-36) and --acf.
- Under OW-38 the gate results and blockers go to the owner before --close.

## Disclosures
- One pair blind to each other. Never count this pair as new blind lenses.
- Spend: 7,761,939 measured tokens across 61 of 98 runs, 37 unmeasured, the full spend unknown. No limit was set for 1 Corinthians; under OW-28 spend is tracked and does not block the close.
- I ran no listing and no glob; see lane_meta.e19_selfreport.
