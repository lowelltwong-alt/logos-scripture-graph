# Chunking Leaderboard (generated)

**Generated:** 2026-06-08T22:01:25+00:00  |  **Runs:** 5  |  target p50=600 tokens

Hard gates (must pass to rank): 0 USFM leaks, 0 book crossings, 100% prose
sentence integrity, Psalm 23 = one whole-psalm chunk, Genesis 1 = no mid-sentence
split. Ineligible runs shown last.

Scoring provenance: T311 corrected Psalm fragmentation grouping from bare chapter to
`(book, chapter)`. The unchanged D / Claude pass2 output scored 88.5 under the old
evaluator and 93.0 under the T311 book/chapter evaluator. T314 excludes reviewed
parent/child structural Psalm splits, such as Ps.78, from the bad-fragmentation penalty;
the same unchanged output now scores 93.5. These are evaluator-policy corrections, not
chunk-output improvement.

Corpus provenance: pre-T327 scorecards are wider-corpus baselines produced before
the owner-approved 66-book canonical scope correction. T327D introduces the
post-T327 canonical-66 corpus baseline after T327C removed non-66 canonical outputs.
Movement between pre-T327 and post-T327 rows is corpus-scope correction / baseline
reset, not chunking improvement. Compare leaderboard rows within the same
`corpus_baseline`.

| rank | agent | pass | corpus_baseline | eligible | composite | chunks | tok_p50 | psalms_fragmented | literal_psalms_fragmented_raw | reviewed_structural_splits | literal_psalms_fragmented | poetry_books_fragmented | psalm119_section_chunks | sent_pct | leaks | crossings | run_id |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | claude-opus-4.8 | 2 | post_t327_canonical_66_corpus | yes | 93.6 | 1131 | 728 | 0 | 1 | 1 | 0 | 1 | 22 | 100.0 | 0 | 0 | claude-opus-4.8__pass2__D_claude_pass2_post_t327__20260608T215149Z |
| 2 | claude-opus-4.8 | 2 | pre_t327_wider_corpus | yes | 93.5 | 1374 | 729 | 0 | 1 | 1 | 0 | 1 | 22 | 100.0 | 0 | 0 | claude-opus-4.8__pass2__D_claude_pass2__20260605T112450Z |
| 3 | claude-opus-4.8 | 1 | pre_t327_wider_corpus | yes | 85.4 | 1271 | 745 | 0 | 0 | 0 | 0 | 0 | 1 | 100.0 | 0 | 0 | claude-opus-4.8__pass1__A_genre_default__20260605T034131Z |
| 4 | claude-opus-4.8 | 1 | pre_t327_wider_corpus | yes | 82.7 | 2174 | 410 | 1 | 1 | 0 | 1 | 3 | 1 | 100.0 | 0 | 0 | claude-opus-4.8__pass1__B_genre_tight__20260605T034131Z |
| 5 | claude-opus-4.8 | 1 | pre_t327_wider_corpus | yes | 67.2 | 983 | 1109 | 0 | 0 | 0 | 0 | 0 | 1 | 100.0 | 0 | 0 | claude-opus-4.8__pass1__C_naive_window__20260605T034131Z |

> Big chunk outputs live under `data/derived/chunks/variants/<run_id>/` (gitignored).
> Only these scorecards are committed. The human picks the winner to promote.

