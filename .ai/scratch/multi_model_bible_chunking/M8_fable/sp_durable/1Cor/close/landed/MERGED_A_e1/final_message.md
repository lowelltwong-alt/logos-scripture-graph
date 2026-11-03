# 1 Corinthians merged close, lane MERGED_A

Three verdicts, one reader, one model family (claude-opus-5-5, grader_fallback OW-25).

- Postcheck: fit_to_assemble. No high or medium residual in the 70 rows read whole.
- Final check: fit_to_close, on the evidence I read only. Transcript audit owed, not met. Campaign-end review deferred, not met.
- Items 20-23: all fit_to_accept, each with reservations.

High or medium residuals in rows: none. 9 low.
NQ classed close_blocker: none.

Process findings at medium, recommended before --close:
- PF-1: before the merged lanes, FIXUP-5 prose was read whole by one audit lane; strategy count not met on it; E7 says S8 not owed; no owner ruling; 0 of 27 routed items say so.
- PF-2: R7-NOT-TESTABLE sits behind 'all MET', E7 says it goes to end review, and 0 routed items carry it.
- PF-3: 'read every final row': the brief fell short of E6, the coordinator's stated error; this lane now read 70 of 70 whole under its order; lane B's read record is unknown to me, so the condition stays open for the pair.

Limits:
- Rows: 18 read by script print, 52 by Read by line. rows_read is no proof of attention.
- Marks stand in pmarks; the CSV behind them is unpinned, so source bytes UNAVAILABLE.
- All lanes are one voice. I am blind to lane B.
- Session-limit stop, the coordinator's order and compactions are in lane_meta.json.
- Budget: about 140 calls, past the raised limit of 120, with no authorization past it. files_opened is rebuilt after the fact.
- I ran no listing and no glob.
