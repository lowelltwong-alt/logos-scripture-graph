# Codex Daily Prep Review Prompt

Use this prompt once per day (recommended) while an autonomous prep branch is active.

## Goal

Review Cursor overnight prep work on the active branch. Record a daily integrator verdict. Do not authorize reviewed gold, chunk output, child spans, or hold clearing.

## Required reads

1. `.ai/control/multi_agent_review_cadence.yaml`
2. `.ai/control/agent_review_ledger.jsonl` (last entry for this branch)
3. `.ai/handoffs/<TASK_ID>/handoff.md`
4. `.ai/tasks/<TASK_ID>.task.yaml`
5. Branch diff since last `codex_daily` ledger entry

## Checks

1. Task scope: no forbidden paths touched.
2. Draft non-authorizations: no reviewed gold, output, child spans, or hold clearing language.
3. Escalation handling: theology-sensitive candidates cite T411 escalation packets; no metadata-as-authority smuggling.
4. Efficiency: no whole-Bible raw USFM reread evidence; ledger-first inputs only.
5. Validators: run focused draft validators for the task; record results.

## Verdict (required)

Return exactly one:

- `APPROVE_PREP` — drafts are safe to keep on prep branch; may recommend owner docket.
- `HOLD_WITH_FINDINGS` — block further prep merge/integration until findings are addressed.

## Outputs

1. Append one JSONL line to `.ai/control/agent_review_ledger.jsonl`:

```json
{
  "review_tier": "codex_daily",
  "date": "YYYY-MM-DD",
  "branch": "codex/t4xx-...",
  "task_id": "T4xx",
  "verdict": "APPROVE_PREP",
  "reviewer": "codex",
  "subjects_reviewed": ["cursor_prep"],
  "finding_count_p0": 0,
  "finding_count_p1": 0,
  "finding_count_p2": 0,
  "prep_branch_head_sha_short": "<8-char>",
  "non_authorizing": true
}
```

2. Update handoff `last_codex_daily_review` and `codex_daily_verdict`.
3. If drafts are ready, record `recommended_owner_docket` only — do not authorize strengthening, gold, or output.

## Scratch lane promotion PRs

If the branch name starts with `scratch/` or the PR includes `.ai/scratch/submissions/SUB-*/promotion_packet.yaml`, switch to `.ai/prompts/codex_promotion_packet_review_prompt.md` and require `validate_promotion_packet.py` to pass.

## Non-authorizations

This daily review does not authorize reviewed gold promotion, chunk output, child spans, route/evaluator changes, hold clearing, or theology authority.
