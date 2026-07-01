# T422 Scratch Lane Handoff

## Task

- task_id: T422
- status: complete
- mode: control_plane_process_charter

## Deliverables

- `.ai/control/scratch_lane_policy.yaml`
- `scripts/validate_scratch_scope.py`
- `scripts/validate_promotion_packet.py`
- `scripts/validate_scratch_lane_policy.py`
- `.ai/prompts/codex_promotion_packet_review_prompt.md`
- `.ai/scratch/submissions/_template/promotion_packet.yaml`

## Usage

```bash
git worktree add ../logos-scratch -b scratch/my-lane origin/main
cd ../logos-scratch
python scripts/validate_scratch_scope.py --branch scratch/my-lane --file .ai/context/agent_work/T417/foo.md
```

## Next

Use scratch lane for batch2+3 experimentation; promote with `SUB-###` packet and Codex promotion review.
