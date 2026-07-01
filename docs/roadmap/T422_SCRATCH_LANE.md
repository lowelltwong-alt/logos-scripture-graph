# T422 Scratch Lane

## Purpose

Fast git worktree lane (`scratch/*`) for non-authorizing prep without `validate_all` on every commit.

## Flow

1. `git worktree add ../logos-scratch -b scratch/<lane> origin/main`
2. Work only under allowed paths (see `.ai/control/scratch_lane_policy.yaml`).
3. Before each commit: `python scripts/validate_scratch_scope.py`
4. Copy submission to `.ai/scratch/submissions/SUB-###/promotion_packet.yaml`
5. Open PR to `main` with packet; Codex uses `.ai/prompts/codex_promotion_packet_review_prompt.md`

## Lanes

| Lane | Validates in scratch | Promotion default |
|------|----------------------|-------------------|
| Scratch | `validate_scratch_scope.py` | `prep_artifacts_only` |
| Main | `validate_all.py` | per task owner gates |

## Non-authorizations

Scratch lane does not authorize reviewed gold, chunk output, or theology authority.
