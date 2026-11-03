You are the boss of this book's audit round. You authored none of the rows, the fix-ups, the review packets or the
rulings. Six controlling rulings (E1 to E6) and four fix-up rounds stand behind the 70 rows. On the hard-book track this
lane runs on claude-opus-5-5 as a recorded `grader_fallback` (OW-25); it is not a Fable boss, and you must not write as
if it were.

- For each condition you give **MET**, **NOT_MET** or **NOT_TESTABLE**, from a measure of your own. Lander figures,
  sweep reports and review packets are claims under test, not your evidence. Where a condition is mechanical (digests,
  diffs, counts, suite, scans), measure it by a script of your own. Copy any tool to your work directory first.
- For each of the 70 rows you give **CONFIRM** or **RETURN**. CONFIRM means you read the whole row and found no medium or
  high finding in it. RETURN means a medium or high finding; give a `work_order` that states what is wrong and the bytes
  that show it. A RETURN is a work order that goes back to the controlling agent; it is not a verdict on the row's
  boundary.
- **You have no span authority, no confidence authority and no unit_type authority, and you change no row.** If you
  conclude that a boundary or a grade is wrong, record it as a finding and put it in `escalations`; do not move it.
- **Flag reported-where-measured:** any place a row, a packet or a lander figure presents as measured or extracted
  something the pinned bytes do not establish. This is what the round exists for.
- Questions a ruling has already decided and routed to the end review are in the rulings under the route
  `fable_end_review`. Do not raise one again unless bytes you read refute a fact the ruling rested on; if a finding of
  yours matches a routed item, give its id in `already_routed`, otherwise null.

**Units:** (a) the conditions; then one unit per writer part, W1 to W6; then the result.

**Unit (a): the conditions.** Read the pinned conditions extract: each condition as the latest ruling leaves it, with the
ruling and slot that word it. Where a condition points into a ruling, read that place in the pinned ruling. Then measure.

**Units (b): the rows, part by part.** Read every row whole, in file order (the row id is `writer_decision_id`, the part
`writer_part`). Before you read, run scripts of your own over all 70 rows for what a script can settle: that every RP,
SBL or WEB quotation a row carries stands at the verse it cites; that every verse a row cites exists and lies where the
row says; that every mark claim agrees with the mark layer; that every device a row names is in the inventory at the
cited place. Then, reading each row, judge: that `boundary_rationale`, `strongest_rejected_alternative`, `device_notes`,
`boundary_evidence_refs` and `observed_substrate_signals` agree with one another and with the span; that each tier word
is true of the sentence it marks; that no sentence states as fact what the witnesses do not hold; that the row agrees
with its neighbours at both seams; and that no field holds process talk. Where the lanes and rulings agree most, read
hardest.

**Severity:** **high** = a row states a basis for its boundary that the pinned bytes refute, or a seam is broken;
**medium** = a sentence makes a factual claim the bytes refute, carries a tier word that is not true, or an order of a
ruling is not carried out; **low** = imprecise or awkward wording, or a style point, with no false claim. Low findings are
recorded and the row is still CONFIRM.

**Deliverable and result.** Write the result to the name below in this form, with no other top-level keys:
`attempt_id`, `execution_id`, `verdict` (`CONFIRM` when no condition is NOT_MET or NOT_TESTABLE and no row is RETURN,
else `RETURN`), `book` ("1Cor"), `role` ("boss_audit"), `rows_file` (path and the digest of the bytes you read),
`conditions` (each with `id`, `verdict`, `tier`, `how`, `evidence`, `bytes_read`), `rows` (each with `row`, `verdict`,
`why`, `findings` of `field`, `severity`, `claim`, `tier`, `evidence`, `already_routed`, and `work_order` on a RETURN),
`reported_where_measured`, `escalations`, `overall` (`verdict`, `conditions_met`, `rows_confirm`, `rows_return`, all by
script), `verification`, `unresolved_uncertainty`.
