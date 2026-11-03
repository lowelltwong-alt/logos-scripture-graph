# Close kit (TE-7)

Book-agnostic task text for the close lanes D1, D2, D3 and D5, ported once from the Daniel close. A book's lane spec names
one of these as its `task` and fills its tokens with `task_fill`; `{{` left over refuses the build. No later book rewrites
these; a change that belongs to all books is made here once.

Order, corrected 2026-11-01 from the Daniel pins: BOSS on the hard track reads the last applied rows; the final rows are
then struck with that audit as their basis (only `review_status` changes and the two hold fields are added; see
`Dan/rows_v1_final.manifest.json` `change_rule`); then D1, D2 and D3 in parallel (each pins the final rows, the boss
record, the landed-outputs manifest and the routed items), then D5 on D3's output, then the two blind merged lanes.

Before building D1, D2, D3 or D5, copy the landed manifest to `<book>_landed_outputs_manifest.frozen_for_close_lanes.v1.json`
and pin only that copy. The live manifest moves at every landing, so a lane or generator pinned to it stops (1Cor D2,
2026-11-02). The live file is rebuilt at the close and read by the close gates; the frozen copy never moves.
