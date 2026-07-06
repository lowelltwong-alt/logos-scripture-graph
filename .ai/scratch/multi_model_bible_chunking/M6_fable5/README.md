# Model Folder Template

Copy this folder to add another T423 comparison model, up to 10 total.

```bash
# Example: add 6th model
cp -r models/_TEMPLATE M6_gpt
# Edit model_manifest.yaml and README.md with model_id M6_gpt
```

## Required Files

- `model_manifest.yaml` - set `model_id`, `agent_surface`, `model_profile`, and `quality_protocol`.
- `marathon_progress.yaml`
- `book_chunks/<Book>/chunks.jsonl` - write one validated book at a time.
- `book_strategy/<Book>.md` - required before each book is marked complete.
- `low_confidence_register.jsonl`
- `frontier_escalation_queue.jsonl`
- `atlas_candidate_feed.jsonl`
- `layer_decision_log.jsonl`
- `model_quality_summary.md`
- `model_summary.md`

## Rules

- Same `shared_research_baseline/` as all other models.
- Same template does not mean same chunks. The template is a schema/evidence contract only.
- Make independent boundary decisions after considering substrate markers, biblical literature type, Strong's metadata as evidence-only, and known low-confidence triggers.
- Use `literary_marker_aware_v2`.
- Chapter-only fallback must be logged and low-confidence when markers, stress, mixed-genre, or frontier signals exist.
- Low-confidence chunks must be reported to the low-confidence register, frontier queue, and atlas candidate feed.
- Atlas candidate feed rows are consideration-only; do not edit the governed stress atlas.
- Independent marathon: do not read other models' maps until complete.
- Register new slot in `manifest.yaml` under `models:`.
- Init progress: `python scripts/t423_init_marathon_progress.py M6_<name>/`.
