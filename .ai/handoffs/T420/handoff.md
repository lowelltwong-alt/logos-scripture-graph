# Task Handoff

## Task

- task_id: T420
- title: Multi-Agent Review Cadence Charter
- phase: phase_4
- status: CHARTER_RECORDED

## Agent

- agent_name: Cursor
- mode: control_plane_cadence_charter
- stage: final
- updated_at: 2026-07-02T00:00:00Z
- handoff_id: t420-multi-agent-review-cadence

## Files read

- `.ai/control/autonomous_corpus_processor.yaml`
- `.ai/control/autonomous_run_queue.yaml`
- `.ai/control/parallel_chunking_research_program.yaml`
- `.ai/control/frontier_chunking_escalation_policy.yaml`
- `.ai/handoffs/T416/handoff.md`
- `docs/roadmap/T410_RESEARCH_TO_CHUNKING_PHASE_ONE_ROADMAP.md`

## Files changed

- `.ai/control/multi_agent_review_cadence.yaml`
- `.ai/control/agent_review_ledger.jsonl`
- `.ai/prompts/codex_daily_prep_review_prompt.md`
- `.ai/prompts/claude_weekly_architecture_chunking_audit_prompt.md`
- `.ai/tasks/T420.task.yaml`
- `.ai/handoffs/T420/handoff.md`
- `docs/roadmap/T420_MULTI_AGENT_REVIEW_CADENCE.md`
- `scripts/validate_multi_agent_review_cadence.py`
- `tests/test_multi_agent_review_cadence.py`
- `.ai/control/chunking_theological_decision_register.yaml` (CD-084)
- `.ai/control/chunking_lesson_index.yaml` (LSN-039)
- `.ai/handoffs/AGENT_ROUTING_GUIDE.md`
- `AI_FRONT_DOOR.md`
- `AI_TABLE_OF_CONTENTS.md`
- `ROADMAP_STATE.yaml`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/current_focus.yaml`
- `.ai/control/chunking_agent_preflight.yaml`

## Decisions made

- Cursor prep runs until backlog empty; Codex integrates prep branches daily; Claude Opus 4.8 audits weekly.
- Review ledger is append-only at `.ai/control/agent_review_ledger.jsonl`.
- T417 prep branch may co-locate T420 charter surfaces under integrator scope.
- No reviewed gold, chunk output, child spans, or hold clearing from this charter.

## Validation run

- `python scripts/validate_multi_agent_review_cadence.py` -> passed
- `python scripts/validate_task_scope.py --task-id T420` -> passed
- `python scripts/validate_chunking_lesson_index.py` -> passed
- `python scripts/validate_chunking_theological_decision_register.py --base-ref origin/main` -> passed
- `python -m pytest tests/test_multi_agent_review_cadence.py -q` -> passed

## Known risks

- Staleness policy is advisory-only in v1; daily/weekly reviews are not CI-enforced yet.
- T417 and T420 may share a prep branch; integrator must keep task scopes aligned.

## Open questions

- Whether to schedule Cursor Automations for daily Codex / weekly Claude (deferred).

## Next agent instruction

- **Cursor:** Continue T417 backlog units on `codex/t417-autonomous-batch2-prep`; stop when empty.
- **Codex:** Run `.ai/prompts/codex_daily_prep_review_prompt.md` after prep commits; append ledger.
- **Claude Opus 4.8:** Run weekly prompt; write audit under `.ai/audits/reports/weekly/`.
- **Owner:** Confirm batch2 docket before strengthening/gold/output.

## Review cadence template

```yaml
last_codex_daily_review: null
codex_daily_verdict: pending
last_claude_weekly_review: null
claude_weekly_verdict: pending
ledger_refs: []
```
