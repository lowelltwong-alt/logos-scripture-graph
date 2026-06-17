# AI Audit And No-Context Review Entry

This folder is the repo-resident entry point for an independent AI or human reviewer who has no
chat context and needs to check another agent's work.

Start here after `AI_FRONT_DOOR.md`.

## Use Cases

- A/B check another agent's PR or local branch.
- Red-team a chunking, governance, roadmap, or data-plane change.
- Verify that an agent's claims are present in committed repo artifacts, not only in chat.
- Produce a review report that a future maintainer can audit later.

## Required Read Order

1. `AI_FRONT_DOOR.md`
2. `.ai/audits/README.md`
3. `.ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md`
4. `.ai/control/audit_surface_map.yaml`
5. `ROADMAP_STATE.yaml`
6. `.ai/control/PROJECT_STATUS.md`
7. `.ai/control/current_focus.yaml`
8. `.ai/tasks/<task_id>.task.yaml`
9. `.ai/handoffs/<task_id>/handoff.md`
10. Changed files from `git diff --name-status <base>...HEAD`
11. Decision and dependency surfaces named by the task.

## Repo-Resident Changelogs

- `.ai/control/roadmap_events.jsonl` - task state and roadmap event log.
- `.ai/control/handoff_ledger.jsonl` - handoff creation/refresh log.
- `.ai/control/PROJECT_STATUS.md` - human-readable operational change history.
- `ROADMAP_STATE.yaml` - machine-readable task state.
- Git history and PR metadata - commit, branch, and merge record.
- `eval/chunking_gold/review_packets/REVIEW_PACKET_INDEX.md` - review packet queue/index.
- `.ai/control/chunking_theological_decision_register.yaml` - theological/downstream decision log.
- `.ai/control/bible_chunking_readiness_map.yaml` - whole-Bible chunking readiness/dependency map.
- `.ai/control/audit_surface_map.yaml` - machine-readable audit surface inventory.
- `.ai/control/harness_upgrade_roadmap.yaml` - future harness upgrade candidates and watch conditions.

## Future Harness Watchlist

Before closing an audit, check `.ai/control/harness_upgrade_roadmap.yaml`.

If the review discovers a repeated failure mode, a local/CI mismatch, a protected-path ambiguity, an
owner-decision drift, a source-metadata authority risk, a cross-repo mirror drift, or a manual check
that future agents will need again, either:

- update the harness roadmap with a candidate or status change; or
- record why no harness is needed in the review report.

## Harness

Generate a no-context audit brief with:

```bash
python scripts/agent/no_context_audit_harness.py --task-id T344 --base-ref origin/main --print
```

Write a durable report draft with:

```bash
python scripts/agent/no_context_audit_harness.py --task-id T344 --base-ref origin/main --output .ai/audits/reports/YYYYMMDD-T344-review.md
```

## Review Outputs

Write durable review outputs under:

```text
.ai/audits/reports/
```

Use:

```text
.ai/audits/templates/REVIEW_REPORT_TEMPLATE.md
```

Do not treat a review report as authorization. A report can recommend, block, or ask questions, but
owner decisions, reviewed-gold promotion, output changes, boundary import, or master-context changes
still require their normal governed surfaces.
