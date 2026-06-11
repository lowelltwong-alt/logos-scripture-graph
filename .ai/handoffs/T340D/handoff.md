# Handoff - T340D Remove Post-Merge Verification Requirement

## Task

- task_id: T340D
- title: Remove post-merge verification requirement
- mode: build
- status: complete
- branch: t340d-remove-post-merge-verification

## Agent

- agent_name: Fable
- mode: build
- stage: final
- updated_at: 2026-06-11T00:00:00Z
- note: Owner-directed removal. `force_handoff.py` rejects alphanumeric task ids such as `T340D`, so this handoff was created manually using the repository-required handoff sections.

## Gate context

The owner (Lowell Wong, 2026-06-11) decided the mandatory post-merge verification gate added in
T340B and hardened in T340C is a workflow blocker and must be removed. The owner had locally
deleted `scripts/agent/post_merge_verify.py`; the agent initially restored it because an
uncommitted deletion of a tracked file looked accidental. After the owner stated the intent
explicitly, this task removed the requirement properly so the repo stays green and coherent:
deleting only the script would have left CI red because committed tests asserted the script and
its docs exist.

## Files read

- AI_FRONT_DOOR.md, AI_TABLE_OF_CONTENTS.md
- docs/workflows/AGENT_COORDINATION_WORKFLOW.md, docs/workflows/ROADMAP_CHANGE_WORKFLOW.md
- .ai/control/current_focus.yaml, .ai/control/PROJECT_STATUS.md
- tests/test_t337a_psalm_review_packet.py (confirmed no dependency on post-merge surfaces)
- full reference grep for post-merge mentions across tracked files

## Files changed

Deleted:

- scripts/agent/post_merge_verify.py
- docs/workflows/POST_MERGE_VERIFICATION_WORKFLOW.md
- .ai/templates/POST_MERGE_AND_NEXT_TASK_PROMPT.md
- .ai/templates/NEXT_TASK_HANDOFF_CHECKLIST.md
- tests/test_post_merge_verification_workflow.py
- tests/test_post_merge_verify_behavior.py

Edited (mandate blocks removed, principle retained):

- AI_FRONT_DOOR.md - removed the post-merge workflow pointer and the post-merge gate block; kept
  "a merged PR does not automatically authorize the next task" as plain guidance.
- AI_TABLE_OF_CONTENTS.md - removed the three deleted-file entries from Workflows And Templates.
- docs/workflows/AGENT_COORDINATION_WORKFLOW.md - removed Step 1a entirely.
- docs/workflows/ROADMAP_CHANGE_WORKFLOW.md - replaced the post-merge verification rule with a
  merge-state principle (merge records state; it does not authorize implementation).
- .ai/control/current_focus.yaml, .ai/control/PROJECT_STATUS.md, ROADMAP_STATE.yaml,
  .ai/control/roadmap_events.jsonl, .ai/control/handoff_ledger.jsonl - control-plane state.
- .ai/tasks/T340D.task.yaml, .ai/handoffs/T340D/handoff.md - this task.

## Decisions made

- Owner decision is the authority for this change; it is recorded in the task yaml
  (`authorized_by`) and PROJECT_STATUS. This is workflow tooling, not a protected canonical
  surface; no canonical, reviewed-gold, route-isolation, or boundary gate is affected.
- History preserved: T340B/T340C task files, handoffs, roadmap entries, and merged commits are
  untouched. The removal is forward-looking only.
- The non-authorization principle survives as guidance because it predates the script and is part
  of the reviewed-gold model, not the deleted tooling.
- Historical narrative mentions of post-merge verification in docs/roadmap/T33x files, old task
  yamls, and methodology lesson entries were left unchanged: they describe what happened, they do
  not mandate anything now.

## Validation run

- python scripts/validate_all.py
- python -m pytest -q
- git diff --check
- YAML/JSONL parse checks

(Results recorded in the final report and PR body.)

## Known risks

- Without the scripted gate, post-merge state (PR merged, commit on main, clean tree, green
  validation) is verified ad hoc by whoever starts the next task. The owner accepted this
  trade-off explicitly.
- Future agents reading older handoffs (T340B/T340C) will see references to the deleted tooling;
  those handoffs describe their own era and this handoff records the removal.

## Open questions

- None for this task. Whether any lighter-weight merge-state check is ever wanted again is an
  owner decision for the future.

## Next agent instruction

Do not treat removal of the verification gate as removal of any other gate. T342 remains
review-packet candidate selection only and must not start without an explicit gated prompt. Do not
start Revelation implementation, T327G, or boundary import; do not import boundary texts; do not
promote the Psalm candidate skill.
