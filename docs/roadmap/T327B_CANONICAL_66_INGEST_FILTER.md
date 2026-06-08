# T327B Canonical 66-Book Ingest Filter

## Status

- Task: T327B
- Mode: build
- Status: complete
- Branch: `t327b-canonical-66-ingest-filter`
- Data mutation: none
- Output regeneration: none
- T327C/D/E/F/G: not started

## Summary

T327B adds a canonical 66-book allow-list and ingest/build filter mechanism to prevent non-66 books,
FRT front matter, and GLO glossary material from entering canonical Scripture outputs going forward.

## What Changed

- Added `config/canon/canonical_66_books.yaml`.
- Added dependency-light canonical-scope helpers in `pipelines/util/canonical_scope.py`.
- Added `scripts/validate_canonical_66_scope.py`.
- Added an explicit WEB USFM importer `--canonical-66-filter` flag so T327C can regenerate
  canonical passages, witnesses, and canonical sidecars only for allowed 66-book Scripture books.
- Added synthetic tests for allow-list integrity, mixed-input filtering, and fail-closed validation.

## T327B.1 Validator Hardening

T327B.1 adds `CANON-SCOPE-VALIDATOR-001`: canonical-scope validation fails closed on unclassified
records. When optional JSONL files are supplied to `scripts/validate_canonical_66_scope.py`, every
record must expose a valid canonical 66-book identity. Records without `book`, `osis_book`,
`usfm_book`, `osis_ref`, or `passage_id` do not silently pass.

Glossary, front-matter, concordance, and source metadata may be preserved only as separately scoped
non-scripture supporting/reference artifacts. They must not pass as canonical Scripture passages,
canonical chunks, canonical witness text, leaderboard inputs, scorecard inputs, or default
Scripture retrieval text.

## Non-Regeneration Boundary

Existing generated outputs may still contain non-66 records until T327C regeneration. Default CI
regeneration remains pre-T327C unless the explicit filter flag is used.

T327B does not regenerate canonical outputs, chunks, scorecards, leaderboard, or gold/stress/index
surfaces. It does not mutate raw/canonical data, import texts, move excluded material to the
boundary repo, or claim chunking improvement.

## Deferred Sequence

- T327C regenerates canonical outputs after this filter is merged.
- T327D regenerates chunks, scorecards, leaderboard, and score language as corpus-scope correction.
- T327E cleans gold/stress/observed/index surfaces.
- T327F plans boundary repo source intake.
- T327G optionally plans raw source artifact replacement or migration.

## Current Baseline Language

The current official score remains the pre-corpus-scope-correction baseline:

```text
D / Claude pass2 = 93.5 under T314 reviewed-structural-split evaluator policy.
```

Future score movement after T327C/T327D is corpus-scope correction, not chunking improvement.
