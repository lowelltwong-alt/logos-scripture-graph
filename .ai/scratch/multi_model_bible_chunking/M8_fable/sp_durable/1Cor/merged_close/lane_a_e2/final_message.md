# MERGED_A2 — 1 Corinthians merged-verdict close, lane A (reissue a2)

Model claude-opus-5-5, grader_fallback (OW-25). Corpus rows_v1_final.jsonl sha256 4287903015be…f9ea (pinned; 90 pins, 0 mismatches).

## Verdicts
1. Postcheck: **fit_to_assemble**, blocking []. 39 rows read whole, 31 held by byte equality (all equal). Residuals all low: W3-004, W2-014/W2-015, W5-013/W5-014.
2. Final check: **not_fit**. Fit on the rows; not fit to close until the blockers below are cured. Transcript audit OWED, NOT MET; campaign-end review DEFERRED (OW-28).
3. Items 20-23: 20 fit (reservations), **21 NOT fit**, 22 fit, 23 fit (reservations).

## Reissue keys
- R2 item 1: 0 of 7 sampled LF-supported rows defective, 0 LF-attributable.
- R3 item 14: match. 23 E9 spans re-applied independently reproduce the corpus bytes; no unordered or missing change.
- R4 item 25: 34 rows, 0 defects (5 low notes).
- E-23: both W1-002 'period' uses name the rhetorical period, not a full stop.

## High or medium residuals
None.

## Close blockers (NQ-6)
- A. The fable end packet is built over d1751369 (pre-FIXUP-6): MISMATCH, wrong corpus, stale sidecars. Cure: regenerate with gen_fable_end_packet.py --book 1Cor and re-pin.
- B. Item 21: gen_method_v8.py pins ROWS_SHA d1751369, so --check FAILs. The shipped method_record_check.v8.json is stale (my copy: 12/13). Cure: re-pin ROWS_SHA to 4287903015… (regenerates v8 identically, 53601c73), then re-run the checker.
- C. The landed outputs manifest predates a change to 1cor_review_attempt_receipts.jsonl. Rebuild or re-pin it.

## Disclosed, owner-facing
- The WEB licence term and edition are stated nowhere (NQ-2, NQ-12).
- The strategy's lens count of 3 was not met for FIXUP-6. One pair blind to each other. Never count this pair as new blind lenses.
- The v7 rule-2 gap and the E7 'S8 not owed' flag are recorded nowhere in the close record (NQ-14).
- Spend: 7,761,939 measured tokens across 61 of 98 runs, 37 unmeasured, the full spend unknown. No limit was set for 1 Corinthians; under OW-28 spend is tracked and does not block the close.

## Limits
- One reader carries all three verdicts. Same-family lanes are one voice.
- RP pilcrows tested via pmarks only.
- Five of the six scholar ranges were tested by script only.
- Items 2-12 rest on the dry report.
- E-19 slips are self-reported in lane_meta.json.
