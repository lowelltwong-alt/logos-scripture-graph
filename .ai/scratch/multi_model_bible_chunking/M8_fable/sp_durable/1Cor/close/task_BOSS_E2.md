You are the second execution of this book's boss audit; the close records you under the tag `e2`. You authored none of the
rows, the fix-ups, the review packets or the rulings. The first execution (e1, the pinned boss audit) returned three rows
and could not test four conditions, because its brief named none of the files they turn on. Round 7 (the pinned ruling
E7, item `R7-NOT-TESTABLE`) ruled what you do; read that item first, and where this task and the ruling differ, the
ruling stands. This lane runs on claude-opus-5-5 as a recorded `grader_fallback` (OW-25). It is not a Fable boss, and you
must not write as if it were.

Rules carried from e1: findings come from a measure of your own; lander figures and sweep reports are claims under test.
You have no span, confidence or unit_type authority and you change no row. A boundary or grade you think wrong goes in
`escalations`. **Severity:** high = a row states a basis for its boundary that the pinned bytes refute, or a seam is
broken; medium = a sentence makes a factual claim the bytes refute, carries a tier word that is not true, or an order of
a ruling is not carried out; low = imprecise wording with no false claim. Questions routed to `fable_end_review` are not
raised again unless bytes you read refute a fact the ruling rested on; give the routed id in `already_routed`.

Do these in order. Each number is a unit in `progress.json`.

1. **Pins and diff.** Check every pin, then diff the FIXUP-4 rows against the FIXUP-5 rows by script: each changed row, each
   changed field, and each of E7's 26 `exact_spans` applied once and accounted for. Record the result in `diff_f4_f5`:
   rows changed, rows byte-identical, any change no span covers. E1's CONFIRM on an unchanged row carries by that byte
   equality and by nothing else.
2. **The four conditions.** Give B3, B4, B7 and B8 **MET**, **NOT_MET** or **NOT_TESTABLE** in `conditions`, in that key
   and no others, each with `id`, `verdict`, `tier`, `how`, `evidence`, `bytes_read`. A clause whose named file fails its
   pin stays NOT_TESTABLE. The sweep clauses run on a private copy of the FIXUP-5 rows.
   - **B3:** read the TF-4 plant result and the two install receipt lines; run the sweep; re-class W1-011 on its bytes.
   - **B4:** read the TF-5 plant and mutant results and the receipt lines; run the sweep.
   - **B7:** script the confidence of every row from the FIXUP-2 rows to the FIXUP-5 rows: changed only for W6-007, W6-013
     and W6-014, each at medium, with the count of high at 3.
   - **B8:** script a field diff from the FIXUP-2 rows to the FIXUP-5 rows and set it against every licensed span applied
     between them: the FIXUP-3 licence table, the FIXUP-3 and FIXUP-4 manifests, the rulings they cite, and the FIXUP-5
     manifest with E7. Include S3-01's seven W4 spans. Recompute the RP and SBLGNT slices of all 70 rows against the
     witnesses. A change no pinned licence covers leaves B8 not MET.
3. **The thirteen conditions e1 met.** In `carried_conditions`, one entry for each of B1, B2, B5, B6 and B9 to B17:
   `id`, `touched` (yes or no), `why`, and on a yes the re-run and its result. Decide `touched` from what the condition
   measures and what FIXUP-5 changed. Run the suite, tiling, ngram7 at `--gate 10` and the sweep on a private copy of the
   FIXUP-5 rows whichever way you decide, and record them in `verification`.
4. **The 21 changed rows.** Read each whole, in file order. Give **CONFIRM** or **RETURN** in `rows`, with `row`, `verdict`,
   `why`, `findings` (`field`, `severity`, `claim`, `tier`, `evidence`, `already_routed`), and `work_order` on a RETURN. A
   low finding leaves the row at CONFIRM. Judge that the fields agree with one another and with the span, that each tier
   word is true of its sentence, that each quotation stands at the verse it cites, and that the row agrees with its
   neighbours at both seams. In `return_cleared`, state of W2-006, W3-001 and W3-002 by name whether e1's findings still
   stand, on the bytes, and read the rewritten claims hardest: E7's words are claims under test too.
5. **Result.** `verdict` is `CONFIRM` when B3, B4, B7 and B8 are all MET and no row is RETURN, otherwise `RETURN`. `overall`
   holds `verdict`, `conditions_met`, `rows_confirm`, `rows_return`, `rows_carried_by_byte_equality`, all by script. `book`
   is "1Cor", `role` is "boss_audit", `rows_file` is the path and digest of the FIXUP-5 bytes you read.
