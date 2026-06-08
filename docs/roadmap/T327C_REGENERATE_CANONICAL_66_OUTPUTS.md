# T327C Regenerate Canonical 66 Outputs

## Status

- Task: T327C
- Mode: build
- Status: complete
- Branch: `t327c-regenerate-canonical-66-outputs`
- Raw mutation: none
- Canonical output regeneration: yes, local ignored generated outputs
- Chunk regeneration: none
- T327D/E/F/G: not started

## Summary

T327C regenerates canonical Scripture outputs with the T327B `--canonical-66-filter` and validates
the regenerated canonical JSONL outputs with the T327B.1 fail-closed canonical-scope validator.

## Regeneration Command

```bash
python pipelines/ingest/usfm_importer.py --canonical-66-filter --processed-root build/t327c_processed/usfm
```

Processed USFM reports were directed to ignored `build/` space so T327C did not update committed or
working-copy processed outputs.

## Corpus Counts

| Surface | Before | After |
|---|---:|---:|
| `passages.jsonl` records | 38,058 | 31,103 |
| `passages.jsonl` books | 81 | 66 |
| `translation_witnesses.jsonl` records | 38,058 | 31,103 |
| `translation_witnesses.jsonl` books | 81 | 66 |
| `boundary_claims.jsonl` records | 34,177 | 28,165 |
| `footnotes.jsonl` records | 1,855 | 1,130 |
| `editorial_cross_references.jsonl` records | 363 | 340 |
| `section_headings.jsonl` records | 314 | 283 |
| `glossary_entries.jsonl` records | 94 | 0 |
| `word_tokens.jsonl` records | 677,688 | 677,688 |

The passage/witness corpus removed 6,955 non-66 records.

## Excluded Material Removed

The regenerated canonical passage/witness outputs exclude:

- Tob
- Jdt
- AddEsth
- Wis
- Sir
- Bar
- 1Macc
- 2Macc
- 1Esd
- PrMan
- Ps151
- 3Macc
- 2Esd
- 4Macc
- AddDan

`FRT` front matter and `GLO` glossary are not emitted as canonical Scripture content. GLO glossary
entries are zero in regenerated canonical outputs.

## Validator Enforcement

T327C updates CI regeneration to use `--canonical-66-filter` and updates `validate_all` so present
canonical JSONL outputs are checked with `scripts/validate_canonical_66_scope.py`. The canonical
scope gate covers passages, witnesses, boundary claims, footnotes, editorial cross-references,
section headings, glossary entries, and word tokens.

Regenerated pre-verse sidecars now carry explicit book identity so T327B.1 can fail closed on truly
unclassified records without rejecting valid canonical sidecar evidence.

## Scope Boundary

T327C is corpus-scope correction, not chunking improvement.

T327C does not:

- mutate `data/raw/**`;
- change the raw WEB USFM archive;
- import texts;
- move excluded material to `logos-boundary-literature`;
- regenerate chunks;
- change chunk outputs;
- change evaluator formula;
- update leaderboard or scorecards;
- update gold/stress/review packet index surfaces;
- start T327D/E/F/G.

## Follow-Up

T327D owns chunk regeneration, scorecards, leaderboard, baseline language, and gold test hash/token
updates after the canonical corpus shrinkage.

Full pytest now has expected T327D fallout because the local regenerated 66-book corpus changes
chunk output and removes non-66 route-ledger controls:

- `tests/test_chunker_gold.py::test_current_chunk_output_sha_matches_corrected_baseline`
- `tests/test_chunker_gold.py::test_non_target_poetry_books_remain_on_monolith_fallback`

T327C deliberately does not update chunk/gold/baseline tests.

T327E owns gold/stress/observed/index cleanup.

T327F owns boundary-source intake planning only.

Any future score movement is baseline reset / corpus-scope correction, not chunker quality
improvement.
