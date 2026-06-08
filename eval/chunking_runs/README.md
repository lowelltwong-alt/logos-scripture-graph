# Chunking runs — scorecards for multi-agent A/B

Each file here is one agent's chunking attempt, scored. **Many agents chunk the Bible;
each leaves a namespaced scorecard here; `leaderboard.py` ranks them so we converge on
the best chunking.**

## Naming convention

```
eval/chunking_runs/<agent>__pass<N>__<variant>__<UTCstamp>.json
```
- `<agent>` — your model/agent id (e.g. `codex-5.5`, `claude-opus-4.8`, `gemini-3`)
- `pass<N>` — pass number (an agent may submit more than one)
- `<variant>` — a short label for the strategy you tried
- `<UTCstamp>` — `YYYYMMDDThhmmssZ`

The big `chunks.jsonl` itself goes under `data/derived/chunks/variants/<run_id>/chunks.jsonl`
(gitignored — regenerable). **Only the small scorecard is committed**, so runs from
different agents / PRs / machines stay durably comparable.

Scorecards may span corpus baselines. Pre-T327 scorecards are wider-corpus baselines;
T327D adds the post-T327 canonical-66 corpus baseline. Movement between those baselines
is corpus-scope correction / baseline reset, not chunking improvement. Compare runs
within the same `corpus_baseline`.

## How to produce a scorecard

```bash
# 1. produce your chunks into your namespaced folder
python pipelines/chunking/chunker.py --passages ... --witnesses ... --boundary-claims ... \
  --out data/derived/chunks/variants/<run_id>/chunks.jsonl
# 2. score it (writes the committed scorecard here)
python pipelines/chunking/evaluate_chunks.py <variant>=data/derived/chunks/variants/<run_id>/chunks.jsonl \
  --scorecard-dir eval/chunking_runs --agent <agent> --pass-num <N>
# 3. rank everyone
python pipelines/chunking/leaderboard.py   # -> eval/LEADERBOARD.md
```

## Ranking

Hard gates (must pass to be eligible): 0 USFM leaks, 0 book crossings, 100% prose
sentence integrity, Psalm 23 = one whole-psalm chunk, Genesis 1 = no mid-sentence
split. Eligible runs ranked by a transparent composite using literal Psalm
fragmentation, size-fitness to ~600 tokens, and coverage. `poetry_books_fragmented`
remains visible as the broader poetry-book metric, and Psalm 119 intentional
sectioning is reported separately as `psalm119_section_chunks`. The human picks the
winner to promote to `data/derived/chunks/eng-web/chunks.jsonl`.
