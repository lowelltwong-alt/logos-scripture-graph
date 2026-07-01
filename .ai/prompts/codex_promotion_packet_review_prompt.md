# Codex Promotion Packet Review Prompt

Use when a PR from `scratch/*` promotes work into `main`.

## Goal

Review the promotion packet and diff. Record a promotion integrator verdict. Do not authorize more than `requested_promotion` in the packet.

## Required reads

1. `.ai/control/scratch_lane_policy.yaml`
2. `.ai/scratch/submissions/<SUB-ID>/promotion_packet.yaml` (linked in PR body)
3. PR diff vs `main`
4. `.ai/control/agent_review_ledger.jsonl` (append new line)

## Checks

1. `python scripts/validate_promotion_packet.py --packet <path>` passes.
2. Every `decisions[]` entry has honest `might_be_wrong` premortem text.
3. `risk_summary.high` is empty unless PR is documentation/control-plane only.
4. No hard-forbidden paths touched (`data/canonical`, `eval/chunking_gold`, `pipelines/chunking`, etc.).
5. `requested_promotion` matches actual diff (no gold/output smuggling).
6. `vendor_imports` disclosed if scratch lane copied external tools.

## Verdict (required)

Return exactly one:

- `APPROVE_PROMOTION_PACKET` — packet matches diff; safe to merge per requested promotion level.
- `HOLD_WITH_FINDINGS` — fix packet or diff before merge.
- `ESCALATE_OWNER` — authority-changing promotion needs owner or standing policy.

## Ledger line

```json
{
  "review_tier": "codex_promotion_packet",
  "date": "YYYY-MM-DD",
  "branch": "scratch/...",
  "pr_number": 0,
  "submission_id": "SUB-###",
  "verdict": "APPROVE_PROMOTION_PACKET",
  "reviewer": "codex",
  "requested_promotion": "prep_artifacts_only",
  "finding_count_p0": 0,
  "finding_count_p1": 0,
  "finding_count_p2": 0,
  "non_authorizing": true
}
```

## Non-authorizations

This review does not exceed `requested_promotion` in the packet. It does not activate standing owner policy or clear holds unless owner has separately recorded approval.
