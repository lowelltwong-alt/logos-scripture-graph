# MERGED_B3: 1 Corinthians merged-verdict close, re-check of a2

Attempt cor_merged_close_lane_b_a3, execution #e1, claude-opus-5-5, grader_fallback (OW-25). Authority OW-36.

## Verdicts
- Postcheck: fit_to_assemble. Carried from a2; the corpus is unchanged at 4287903.
- Final check (OW-6): fit_to_close over corpus 4287903. a2 wrote `not_met`, which is not an allowed value; a3 corrects it.
- Items 20-23: all four fit. Items 20 and 23 are carried. Items 21 and 22 were re-judged and are now fit.

## The three a2 medium defects, re-judged from current bytes (MEASURED)
- Method record: gen_method_v8.py (17adf438) `--check` MATCHes 53601c73. On the work\m8copy copy, check_method_record.py passes 13/13 and its record is byte-equal to the shipped 57089818. `--selftest` passes.
- End packet: gen_fable_end_packet `--check` MATCHes a94c9338 over corpus 4287903 and sidecar 640f95ae.
- README (58a184db): the lead-basis sentence now matches R9-LEADS for 5 of 5 rows. The README counts match the files.

## Still unmet (8 entries, all fixed types)
- DEFERRED_OW28_FABLE_END_REVIEW. DEFERRED is never MET.
- OWED_TRANSCRIPT_AUDIT: 81 attempts, 0 with a transcript, 81 without.
- DUE_AT_CLOSE_ACT for items 1, 14, 16, 18, 19 and 25. close_evidence d8cb5c1d still has no value for items 16, 18 and 19.

## Residuals: 5, all low, no high or medium
- Carried: W5-014 strategy l.87; W1-011 pilcrow attribution; W4-002/W4-004 refs_mirror; v8 header "7 controlling rulings".
- New: v8 l.38-43 says "measured cause". close_evidence states that for P04 and P06 no measured cause exists, and corrects this by statement only. That absence is REPORTED; I did not test it.

## Process findings (low)
- The dry gate calls `--acf` "the owner's choice", but OW-37 point 3 (ledger l.3541) already fixes `--acf item22`.
- The receipt preview omits the OW-38 rule, which has the orchestrator report to the owner before `--close` for 1 Corinthians (gate addendum l.636). See NQ-5.
- The 2026-11-03 gate addendum's citations match ledger l.3412, 3525, 3572 and 3598. It waives nothing.

## Spend
7,761,939 measured tokens across 61 of 98 runs, 37 unmeasured, the full spend unknown. No limit was set for 1 Corinthians; under OW-28 spend is tracked and does not block the close.

## Blindness and E-19
One pair blind to each other. Never count this pair as new blind lenses.
- Exposure: the pinned gates.json and close_evidence carry summary values of the other lane, and I read some of them before switching to structure-only reads. My items 1, 14 and 25 findings (R2-R4) are carried from a2, which predates that exposure.
- I ran no listing and no glob, no existence check and no recursive search.
- I opened no transcript.
- I wrote nothing under SP, ran no git, wrote no receipt and touched no registry.
