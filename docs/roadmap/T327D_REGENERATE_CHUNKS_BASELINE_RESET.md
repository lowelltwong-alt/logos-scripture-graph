# T327D Regenerate Chunks for Canonical 66 Baseline

## Status

- Task: T327D
- Mode: build
- Status: complete
- Branch: `t327d-regenerate-chunks-baseline-reset`
- Raw mutation: none
- Canonical passage/witness mutation: none
- Chunk regeneration: yes, ignored generated variant output
- Evaluator formula change: none
- T327E/F/G: not started

## Summary

T327D regenerates chunks from the corrected T327C 66-book canonical outputs and updates the
chunk/gold/score surfaces that directly depended on the pre-T327 wider corpus. This is
corpus-scope correction and baseline reset, not chunking improvement.

## Canonical Corpus Confirmation

T327C canonical outputs were already regenerated before this task. T327D confirmed the generated
canonical corpus contains:

| Surface | Count |
|---|---:|
| Canonical books | 66 |
| `passages.jsonl` records | 31,103 |
| `translation_witnesses.jsonl` records | 31,103 |
| `glossary_entries.jsonl` records | 0 |

The canonical passage/witness corpus excludes Tob, Jdt, AddEsth, Wis, Sir, Bar, 1Macc, 2Macc,
1Esd, PrMan, Ps151, 3Macc, 2Esd, 4Macc, and AddDan. `FRT` front matter and `GLO` glossary are not
canonical Scripture content.

## Chunk Regeneration Command

```bash
python pipelines/chunking/chunker.py --passages data/canonical/scripture/passages/passages.jsonl --witnesses data/canonical/translations/eng-web/translation_witnesses.jsonl --boundary-claims data/canonical/translations/eng-web/boundary_claims.jsonl --footnotes data/canonical/translations/eng-web/footnotes.jsonl --crossrefs data/canonical/translations/eng-web/editorial_cross_references.jsonl --out data/derived/chunks/variants/claude-opus-4.8__pass2__D_claude_pass2_post_t327__20260608T215149Z/chunks.jsonl
```

Generated output is intentionally under gitignored `data/derived/chunks/variants/`.

## Baseline Reset

| Field | Pre-T327 wider corpus | Post-T327 canonical-66 corpus |
|---|---:|---:|
| Chunk count | 1,374 | 1,131 |
| Chunk SHA-256 | `8c134378e6391be2034c9e534267df218f5dd20b04970b55660aae128c86c5e7` | `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025` |
| Token p50 | 729 | 728 |
| Token p90 | 907 | 898 |
| Token max | 1,441 | 1,152 |
| Composite | 93.5 | 93.6 |

The 93.5 to 93.6 movement is corpus-scope correction / baseline reset after excluded material left
the canonical corpus. It is not chunking improvement, and the evaluator formula remains unchanged
from T314.

## Gold and Test Updates

T327D removes the two temporary T327C xfails and restores them to normal assertions:

- `test_current_chunk_output_sha_matches_corrected_baseline`
- `test_non_target_poetry_books_remain_on_monolith_fallback`

The Psalm gold manifest now uses the post-T327 chunk SHA and run id. The non-target poetry controls
now cover only canonical books `Song` and `Lam`; `PrMan` and `Ps151` were removed because they are
outside the owner-approved 66-book corpus and must not be reintroduced as canonical controls.

## Score and Leaderboard Updates

Committed scorecards now carry `corpus_baseline` metadata:

- `pre_t327_wider_corpus`
- `post_t327_canonical_66_corpus`

The leaderboard displays `corpus_baseline` and warns that pre/post T327 rows should not be compared
as chunking improvement. The post-T327 row is the current canonical-66 corpus baseline.

## Scope Boundary

T327D does not:

- mutate `data/raw/**`;
- import texts;
- move excluded material to `logos-boundary-literature`;
- change canonical passage/witness outputs;
- change the chunking algorithm;
- change evaluator formula;
- change parser/chunker/orchestrator runtime behavior;
- start T327E/F/G.

## Follow-Up

T327E should clean gold/stress/observed/review-packet-index surfaces for residual non-66 references
that are not direct T327D baseline expectations. T327F remains boundary-source intake planning only
and should not be started before T327E.
