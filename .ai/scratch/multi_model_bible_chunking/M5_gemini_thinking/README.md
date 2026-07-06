# Model folder template — copy to M6_<name> .. M10_<name>

Copy this folder to add another comparison model (up to **10 total**).

```bash
# Example: add 6th model
cp -r models/_TEMPLATE M6_gpt
# Edit model_manifest.yaml and README.md with model_id M6_gpt
```

## Required files

- `model_manifest.yaml` — set `model_id`, `agent_surface`, `model_profile`
- `marathon_progress.yaml`
- `whole_bible_chunk_map.jsonl` — append per chunk
- `layer_decision_log.jsonl`
- `model_summary.md`

## Rules

- Same `shared_research_baseline/` as all other models
- Independent marathon — do not read other models' maps until complete
- Register new slot in `manifest.yaml` under `models:`
- Init progress: `python scripts/t423_init_marathon_progress.py M6_<name>/`
