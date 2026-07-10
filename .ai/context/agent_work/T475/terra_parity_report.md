# Terra T475 Parity Report

## Verdict

Measurement parity is internally green. T475 overall remains HOLD_WITH_FINDINGS
because Sol identified a blocking editorial-sidecar preservation regression.

## Reconciliation

- The compressed mismatch ledger has 102,799 rows.
- It reconciles exactly to 102,793 modified records, five removed records, and
  one modified non-JSON report file.
- All three baseline trials share one output hash.
- All three candidate trials share one output hash.
- Baseline median runtime was 55.885653 seconds.
- Candidate median runtime was 52.033347 seconds.
- Runtime is non-authorizing and is not a Rust benchmark.
- Reports expose hashes and safe metadata, not Scripture text.
- The chunker was not run and no chunk output was emitted.

## Surface Results

Unchanged: 31,103 passages, 340 cross-references, 1,127 scoped footnotes,
677,686 retained tokens, extracted source files, extraction manifest,
unsupported-marker rows, and glossary rows.

Expected repair effects: 48 witness text hashes changed only in 21 Psalm 119
prior-heading contaminations and 27 Song prior-speaker contaminations; two
bogus Psalm 119 heading-derived tokens were removed; all 28,165 boundary
claims, 283 headings, and 74,297 events received or changed explicit anchor
metadata.

The 2,727 unresolved event rows are confined to excluded/noncanonical files and
remain fail-closed with null Scripture refs.

## Escalated Disagreement

Terra initially classified three unscoped footnotes from Psalm descriptive
heading lines as expected editorial cleanup. Sol overruled that classification:
editorial-only means excluded from witness text and tokens, not erased from the
typed editorial/source sidecar. The raw marker remains recoverable, but normal
footnote consumers would lose the typed records.

This disagreement was escalated rather than averaged. Sol owns architecture, so
the P1 preservation finding controls the T475 verdict.

## Non-Authorizations

This report does not authorize committed regeneration, reviewed gold, chunk
output, source-tradition preference, canon change, route/evaluator behavior,
graph/retrieval/vector truth, or theology authority.
