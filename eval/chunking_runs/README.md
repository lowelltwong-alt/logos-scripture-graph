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
sentence integrity, Psalm 23 = one whole-psalm chunk. Eligible runs ranked by a
transparent composite (psalm fragmentation + size-fitness to ~600 tokens + coverage).
The human picks the winner to promote to `data/derived/chunks/eng-web/chunks.jsonl`.
