# T311 psalms_fragmented before/after

Date: 2026-06-05
Agent: codex-5
Mode: build

Inputs inspected:

- `data/derived/chunks/variants/A_genre_default/chunks.jsonl`
- `data/derived/chunks/variants/B_genre_tight/chunks.jsonl`
- `data/derived/chunks/variants/C_naive_window/chunks.jsonl`
- `data/derived/chunks/variants/D_claude_pass2/chunks.jsonl`
- `eval/chunking_runs/*.json`

No chunk outputs, raw data, or canonical data were modified.

## Metric design decision

T311 adopts the split-metric design:

- `psalms_fragmented`: backward-compatible alias for `literal_psalms_fragmented`.
- `literal_psalms_fragmented`: literal `Ps` book fragmentation, grouped by `(book, chapter)`.
- `poetry_books_fragmented`: broader `genre == "psalms"` / poetry-book fragmentation, grouped by `(book, chapter)`.
- `psalm119_section_chunks`: explicit non-penalty signal for intentional Psalm 119 sectioning.

Psalm 119 is excluded from fragmentation penalties and reported separately because
the D candidate intentionally emits 22 chunks with boundary basis
`["poetic_stanza", "whole_psalm_split"]`.

## Leaderboard impact

| Variant | Current `psalms_fragmented` | Fixed `psalms_fragmented` | Fixed `literal_psalms_fragmented` | Fixed `poetry_books_fragmented` | Psalm 119 section chunks | Current composite | Fixed composite | Rank change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| D_claude_pass2 | 10 | 1 | 1 | 1 | 22 | 88.5 | 93.0 | 1 -> 1 |
| A_genre_default | 8 | 0 | 0 | 0 | 1 | 81.4 | 85.4 | 2 -> 2 |
| B_genre_tight | 9 | 1 | 1 | 3 | 1 | 78.7 | 82.7 | 3 -> 3 |
| C_naive_window | 8 | 0 | 0 | 0 | 1 | 63.2 | 67.2 | 4 -> 4 |

All four candidates remain eligible. Rankings do not change. Scores increase
because the composite now penalizes literal Psalm fragmentation only, while
Psalm 119 stanza sectioning is measured but not penalized.

## Cause classification

| Variant | Old count | Literal Psalm fragmentation | Intentional Psalm 119 split | Cross-book collision groups | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| A_genre_default | 8 | 0 | 0 | 8 | Chapters 1-8 collided across `Ps`, `Song`, `Lam`, plus `PrMan`/`Ps151` for chapter 1. |
| B_genre_tight | 9 | 1 (`Ps.89`) | 0 | 8 | Chapters 2 and 3 also contain real `Lam` same-chapter splits, hence fixed `poetry_books_fragmented = 3`. |
| C_naive_window | 8 | 0 | 0 | 8 | Same cross-book chapter collision pattern as A. |
| D_claude_pass2 | 10 | 1 (`Ps.78`) | 1 (`Ps.119`) | 8 | Psalm 119 has 22 stanza chunks; chapters 1-8 are cross-book collisions. |

Classification limitation: this is exact for cross-book collisions and same
book/chapter fragmentation from OSIS references. "Intentional" is recognized only
for Psalm 119 by explicit evaluator rule plus the candidate's boundary basis; the
repo does not yet have a curated general-purpose intentional-section registry.
