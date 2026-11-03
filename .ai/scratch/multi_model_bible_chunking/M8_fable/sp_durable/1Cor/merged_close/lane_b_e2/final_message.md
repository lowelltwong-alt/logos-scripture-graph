# MERGED_B2 final message (1 Corinthians merged-verdict close, reissue)

- Postcheck: fit_to_assemble. No high or medium row defect; 3 low residuals (W5-014 strategy l.87 wording; W1-011 pilcrows are pmarks facts, not in 1Cor_rp.txt; refs_mirror 3 flags).
- Final check: not_met. corpus 4287903015be9fcd...; grader_fallback (OW-25).
- Items 20-23: 20 fit (with reservations), 21 NOT fit, 22 NOT fit, 23 fit (with reservations).
- R2 (item 1): 0 of 7 sampled LF-supported rows defective, 0 LF-attributable; sample check MATCH.
- R3 (item 14): match; 23 E9 spans each applied once; replay equals the corpus on every row and field.
- R4 (item 25): 34 rows reviewed, 0 defects, 3 low notes. One pair blind to each other. Never count this pair as new blind lenses.

Medium residuals (close blockers):
1. Item 21: gen_method_v8.py --check FAILs (ROWS_SHA pinned to d175); checker on a copy 12/13; shipped method_record_check.v8.json claims 13/13 and is stale.
2. NQ-6: end-review packet 0f341eff built over d175 / sidecar a28e9a8f; installed sidecar 640f95ae; gen_fable_end_packet --check MISMATCH.
3. Items 22/24: deliverables README Status bullet 2 says the five feed rows lead from the recorded alternative alone; false for 011, 027, 052 after R9-LEADS.

Owner-ruled unmet: DEFERRED_OW28_FABLE_END_REVIEW; OWED_TRANSCRIPT_AUDIT (79 attempts, 0 transcripts, NOT_RUN).
DUE_AT_CLOSE_ACT: items 1, 14, 16, 18, 19, 25; none found NOT met by R2-R4.
Close-blocker named question: NQ-6.
Spend: 7,761,939 measured tokens across 61 of 98 runs, 37 unmeasured, the full spend unknown. No limit was set for 1 Corinthians; under OW-28 spend is tracked and does not block the close.

Limits: scholar-record ranges read by heading only; feed rows 039/040 and the cross_proposal_notes claim not tested; RP pilcrows tested against pmarks (EXTRACTED), not the RP CSV; one model family throughout; context compacted three times, rebuilt from OUT files only.
I ran no listing and no glob.
