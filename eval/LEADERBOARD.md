# Chunking Leaderboard (generated)

**Generated:** 2026-06-05T20:47:18+00:00  |  **Runs:** 4  |  target p50=600 tokens

Hard gates (must pass to rank): 0 USFM leaks, 0 book crossings, 100% prose
sentence integrity, Psalm 23 = one whole-psalm chunk, Genesis 1 = no mid-sentence
split. Ineligible runs shown last.

| rank | agent | pass | eligible | composite | chunks | tok_p50 | psalms_fragmented | literal_psalms_fragmented | poetry_books_fragmented | psalm119_section_chunks | sent_pct | leaks | crossings | run_id |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | claude-opus-4.8 | 2 | yes | 93.0 | 1374 | 729 | 1 | 1 | 1 | 22 | 100.0 | 0 | 0 | claude-opus-4.8__pass2__D_claude_pass2__20260605T112450Z |
| 2 | claude-opus-4.8 | 1 | yes | 85.4 | 1271 | 745 | 0 | 0 | 0 | 1 | 100.0 | 0 | 0 | claude-opus-4.8__pass1__A_genre_default__20260605T034131Z |
| 3 | claude-opus-4.8 | 1 | yes | 82.7 | 2174 | 410 | 1 | 1 | 3 | 1 | 100.0 | 0 | 0 | claude-opus-4.8__pass1__B_genre_tight__20260605T034131Z |
| 4 | claude-opus-4.8 | 1 | yes | 67.2 | 983 | 1109 | 0 | 0 | 0 | 1 | 100.0 | 0 | 0 | claude-opus-4.8__pass1__C_naive_window__20260605T034131Z |

> Big chunk outputs live under `data/derived/chunks/variants/<run_id>/` (gitignored).
> Only these scorecards are committed. The human picks the winner to promote.

