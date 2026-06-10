# Task Handoff

## Task

- task_id: T340B
- title: Standardize post-merge verification
- phase: phase_4
- status: complete

## Agent

- agent_name: Codex
- mode: build
- stage: final
- updated_at: 2026-06-10T20:45:00Z
- note: `force_handoff.py` rejects alphanumeric task ids such as `T340B`, so this handoff was created manually using the repository-required handoff sections.

## Files read

- C:/Users/lowel/.codex/attachments/6fa25d5b-01c3-45f7-8e79-8ed88cc2edd6/pasted-text.txt
- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/current_focus.yaml
- .ai/control/roadmap_events.jsonl
- .ai/control/handoff_ledger.jsonl
- ROADMAP_STATE.yaml
- scripts/agent/
- scripts/validate_all.py
- scripts/validate_canonical_66_scope.py
- scripts/qa_canonical_corpus.py
- docs/workflows/AGENT_COORDINATION_WORKFLOW.md
- docs/workflows/ROADMAP_CHANGE_WORKFLOW.md
- .ai/tasks/T336B.task.yaml
- .ai/handoffs/T336B/handoff.md
- existing tests under tests/ for control-plane and workflow conventions

## Files changed

- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- ROADMAP_STATE.yaml
- .ai/control/PROJECT_STATUS.md
- .ai/control/current_focus.yaml
- .ai/control/roadmap_events.jsonl
- .ai/control/handoff_ledger.jsonl
- .ai/tasks/T340B.task.yaml
- .ai/handoffs/T340B/handoff.md
- .ai/templates/POST_MERGE_AND_NEXT_TASK_PROMPT.md
- .ai/templates/NEXT_TASK_HANDOFF_CHECKLIST.md
- docs/workflows/POST_MERGE_VERIFICATION_WORKFLOW.md
- docs/workflows/AGENT_COORDINATION_WORKFLOW.md
- docs/workflows/ROADMAP_CHANGE_WORKFLOW.md
- scripts/agent/post_merge_verify.py
- tests/test_post_merge_verification_workflow.py

## Decisions made

- Added a reusable post-merge verification script instead of continuing bespoke post-merge prompts.
- Kept the script verification-only: it syncs `main`, checks PR/commit state, validates, reports, and exits nonzero on failure.
- Added `--next-task` as a reporting aid only; the script does not start the next task or infer authorization.
- Added reusable prompt and checklist templates for gated next-task handoffs.
- Added workflow docs and entry-surface pointers.
- Did not mutate raw/canonical/generated data, regenerate chunks, change evaluator/chunker/orchestrator behavior, update leaderboard/scorecards, import boundary texts, start T327G, start Revelation implementation, promote the Psalm candidate skill, or change skill lifecycle status.

## Validation run

- command: python -m pytest tests/test_post_merge_verification_workflow.py -q
- result: passed; 3 passed
- failures: none
- command: python -m pytest tests/test_t337_selection_docs.py tests/test_t337a_psalm_review_packet.py tests/test_t341_revelation_atlas.py tests/test_post_merge_verification_workflow.py -q
- result: passed; 17 passed
- failures: none
- command: python scripts/agent/post_merge_verify.py --help
- result: passed; required CLI flags visible
- failures: none
- command: python scripts/validate_canonical_66_scope.py
- result: passed; Canonical 66 scope config validation passed.
- failures: none
- command: python scripts/qa_canonical_corpus.py
- result: passed; 66 canonical books, 31,103 passage records, 31,103 translation witness records.
- failures: none
- command: python scripts/validate_all.py
- result: passed; all validation gates passed, handoff validation passed for 52 referenced handoff path(s).
- failures: none
- command: python -m pytest -q
- result: passed; 189 passed.
- failures: none
- command: YAML parse checks
- result: passed; 39 YAML files parsed.
- failures: none
- command: JSONL parse checks
- result: passed; roadmap events 60 records and handoff ledger 75 records parsed.
- failures: none
- command: git diff --check
- result: passed.
- failures: none

## Known risks

- `force_handoff.py` still rejects alphanumeric suffix task ids such as `T340B`; this task follows the existing manual suffix-task convention.
- The new script uses local `git` and `gh`; agents still need authenticated GitHub CLI access to run it.
- `--skip-pytest` is available for exceptional local circumstances, but normal post-merge verification should run full pytest.

## Open questions

- Should future CI call `post_merge_verify.py --json` for release branches, or should it remain a local agent workflow?
- Should `force_handoff.py` be updated in a separate task to accept existing suffix task ids?

## Next agent instruction

Review T340B as workflow/tooling/control-plane only. If merged, use `scripts/agent/post_merge_verify.py` and `.ai/templates/POST_MERGE_AND_NEXT_TASK_PROMPT.md` for future post-merge gates. Do not start T342, Revelation implementation, T327G, boundary import, or Psalm candidate promotion from this PR.
