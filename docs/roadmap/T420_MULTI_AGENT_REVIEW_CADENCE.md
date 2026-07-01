---
object_type: roadmap_report
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-07-02 during T420 to codify the multi-agent review cadence for whole-Bible Phase 1 prep."
reason_for_inclusion: "Human-readable charter for Cursor daily prep, Codex daily integration, and Claude weekly architecture/chunking audits."
---

# T420 Multi-Agent Review Cadence

## Summary

T420 records the canonical operating model for autonomous whole-Bible prep:

- **Cursor** runs long prep sessions until the active backlog is empty (8–20h+ acceptable; stop early when done).
- **Codex** integrates prep branches about once per day.
- **Claude Opus 4.8** audits architecture and chunking-error patterns about once per week, including rollup of Cursor prep and Codex daily verdicts.
- **Owner** retains authority gates for docket confirmation, reviewed gold, and output pilots.

This charter is evidence and process only. It does not authorize reviewed gold, chunk output, child spans, hold clearing, or theology authority.

## Control surfaces

- Cadence contract: `.ai/control/multi_agent_review_cadence.yaml`
- Review ledger: `.ai/control/agent_review_ledger.jsonl`
- Processor efficiency rules: `.ai/control/autonomous_corpus_processor.yaml`
- Active run queue: `.ai/control/autonomous_run_queue.yaml`
- Conveyor belt: `.ai/control/parallel_chunking_research_program.yaml`

## Prompt templates

| Agent | Prompt |
|-------|--------|
| Codex daily | `.ai/prompts/codex_daily_prep_review_prompt.md` |
| Claude weekly | `.ai/prompts/claude_weekly_architecture_chunking_audit_prompt.md` |

## Daily Codex runbook

1. Read cadence yaml and ledger last entry for the active prep branch.
2. Review branch diff since last `codex_daily` entry.
3. Run focused validators for the active task.
4. Record `APPROVE_PREP` or `HOLD_WITH_FINDINGS`.
5. Append ledger line; update handoff `last_codex_daily_review`.
6. Recommend owner docket if ready — do not authorize strengthening, gold, or output.

## Weekly Claude runbook

1. Read all `codex_daily` ledger entries since last `claude_weekly`.
2. Audit Cursor prep throughput and escalation handling.
3. Architecture P0–P2 review and chunking-error pattern checklist.
4. Write weekly audit under `.ai/audits/reports/weekly/`.
5. Record `APPROVE_WEEKLY`, `HOLD_WITH_FINDINGS`, or `ESCALATE_OWNER`.
6. Append ledger line; update handoff `last_claude_weekly_review`.

## Cursor resume runbook

1. Read `autonomous_run_queue.yaml` and handoff progress table.
2. Continue next incomplete `work_unit`.
3. Stop when backlog empty or hard stop fires.
4. On session close, update handoff and await Codex daily review before merge to main.

## Relationship to T410 ladder

The T410 nine-step phase ladder remains authoritative for **what** happens (research → prep → codex review → frontier triggers → owner → gold → harness → output → post-pilot). T420 adds **when** integrator and auditor tiers review parallel prep work between owner gates.

## Validation

```bash
python scripts/validate_multi_agent_review_cadence.py
python scripts/validate_task_scope.py --task-id T420
python -m pytest tests/test_multi_agent_review_cadence.py -q
```

## Non-authorizations

- reviewed_gold_promotion
- chunk_output_change
- child_span_selection
- hold_clearing
- whole_bible_output_pass
- theology_authority_change
