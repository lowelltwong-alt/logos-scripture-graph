# Terra T475 Parity Report

## Verdict

Measurement parity is green. Sol advances the bundle to
READY_FOR_INDEPENDENT_AUDIT after T519 restored heading footnotes.

## Reconciliation

- Totals: {"added": 0, "modified": 102793, "modified_file": 1, "removed": 2, "unchanged": 741402}.
- Footnotes: {"added": 0, "modified": 0, "removed": 0, "unchanged": 1130}.
- Word tokens: {"added": 0, "modified": 0, "removed": 2, "unchanged": 677686}.
- All three baseline trials share one output hash.
- All three candidate trials share one output hash.
- Baseline median runtime was 45.220773 seconds.
- Candidate median runtime was 49.522366 seconds.
- Runtime is non-authorizing and is not a Rust benchmark.
- Reports expose hashes and safe metadata, not Scripture text.
- The chunker was not run and no chunk output was emitted.

## Surface Results

Unchanged footnotes: 1130 (zero removals after T519).
Retained tokens: 677686 with exactly two known bogus
Psalm 119 heading-derived token removals.

## Non-Authorizations

This report does not authorize committed regeneration, reviewed gold, chunk
output, source-tradition preference, canon change, route/evaluator behavior,
graph/retrieval/vector truth, or theology authority.
