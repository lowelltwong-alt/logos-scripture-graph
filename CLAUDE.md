# Claude Project Instructions

This repo is the Bible semantic substrate. Start with `AI_FRONT_DOOR.md` before editing.

## Non-negotiables

- Read `.ai/control/MASTER_CONTEXT.md` at task start — **do not edit it** (human-gated).
- **Before any ingest/chunking/graph work, inspect the real raw documents first:** read `.ai/control/RAW_SOURCE_INVENTORY.md`, re-scan with `python scripts/scan_raw_sources.py`, and confirm every marker is classified in `config/ingest/usfm_marker_coverage.yaml`. Enforced by `scripts/validate_raw_coverage.py` (CI fails on an unclassified marker).
- Treat `data/raw/` as immutable source evidence.
- Never overwrite canonical source text while chunking.
- Chunks are derived retrieval objects, not canonical truth.
- Every task needs a deterministic handoff under `.ai/handoffs/<task_id>/handoff.md`.
- Update `PROJECT_STATUS.md` and roadmap state through `ROADMAP_STATE.yaml` and `.ai/control/roadmap_events.jsonl`, not loose notes.
- Run `python scripts/validate_all.py` before stopping.
- Prefer small, reviewable changes with explicit provenance.
- If architecture seems wrong, propose master context change or create/update an ADR; do not silently refactor.

## Required task flow

1. Read `AI_FRONT_DOOR.md`, `MASTER_CONTEXT.md`, `PROJECT_STATUS.md`.
2. Identify task ID from `ROADMAP_STATE.yaml` or create one using `.ai/tasks/_TEMPLATE.task.yaml`.
3. Run `python scripts/agent/force_handoff.py --task-id <ID> --agent claude --stage start`.
4. Work only in the declared task scope.
5. Run `python scripts/validate_all.py` and `python -m pytest -q`.
6. Update handoff, PROJECT_STATUS, and next-agent instruction.

## Chunking principle

Do not split in the middle of an English sentence, Hebrew poetic colon, Greek clause, direct quotation, psalm superscription, section heading unit, or literary form unless the split is explicitly represented as a continuation and justified in metadata.

The chunker must be designed against the markers that **actually appear** in
`.ai/control/RAW_SOURCE_INVENTORY.md` (e.g. words-of-Jesus `\wj`, Selah `\qs`,
superscriptions `\d`, alternate readings `\fqa`), not against assumed structure.
