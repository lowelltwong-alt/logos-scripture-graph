# Task Handoff

## Task

- task_id: T355
- title: WJ Speaker/Discourse Policy And Target Selection
- phase: phase_4
- status: complete

## Agent

- agent_name: codex
- mode: implementation
- stage: final
- updated_at: 2026-06-18T02:20:00+00:00
- handoff_id: t355-final

## Files read

- AGENTS.md
- AI_FRONT_DOOR.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/chunking_agent_preflight.yaml
- .ai/control/chunking_theological_decision_register.yaml
- .ai/control/bible_chunking_readiness_map.yaml
- .ai/control/bible_chunking_research_triage_map.yaml
- .ai/control/wj_marker_inventory.yaml
- .ai/tasks/T354.task.yaml
- .ai/handoffs/T354/handoff.md
- ROADMAP_STATE.yaml
- docs/roadmap/T354_WJ_MARKER_INVENTORY_HARNESS.md
- eval/chunking_gold/review_packets/john3_wj_speaker_boundary_review.md

## Files changed

- .ai/control/wj_speaker_discourse_policy.yaml
- scripts/validate_wj_speaker_discourse_policy.py
- tests/test_wj_speaker_discourse_policy.py
- .ai/control/chunking_agent_preflight.yaml
- scripts/validate_chunking_agent_preflight.py
- tests/test_chunking_agent_preflight.py
- .ai/control/chunking_theological_decision_register.yaml
- .ai/control/bible_chunking_readiness_map.yaml
- .ai/control/bible_chunking_research_triage_map.yaml
- scripts/validate_bible_chunking_readiness_map.py
- scripts/validate_owner_selection_implementation_gate.py
- tests/test_bible_chunking_readiness_map.py
- docs/roadmap/T355_WJ_SPEAKER_POLICY_AND_TARGET_SELECTION.md
- docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md
- .ai/tasks/T355.task.yaml
- .ai/handoffs/T355/handoff.md
- ROADMAP_STATE.yaml
- .ai/control/current_focus.yaml
- .ai/control/PROJECT_STATUS.md
- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- scripts/validate_all.py
- tests/test_task_scope_validator.py
- tests/test_ai_roadmap_table_of_contents.py
- roadmap-state tests that assert the current non-authorizing route
- .ai/control/roadmap_events.jsonl
- .ai/control/handoff_ledger.jsonl

## Decisions made

- Red-letter / WJ evidence is useful evidence, but not sufficient authority for Jesus speaker attribution, speaker boundaries, discourse boundaries, graph edges, chunk boundaries, retrieval truth, reviewed gold, or output changes.
- John.3.1-John.3.36 / `john3_wj_speaker_boundary` is the first exact owner-review target because a pending packet already exists, the scope is small enough to review before larger discourses, and the WJ evidence is split.
- The John 3 selection does not decide whether John.3.10-John.3.21 is Jesus speech, narrator commentary, or unresolved for chunking.
- Larger WJ cases remain queued and non-authorizing: Matthew 5-7, John 13-17, Matthew 24-25, John 7:53-8:11, and Revelation WJ voice-shift cases.
- T355 does not implement chunks, promote reviewed gold, generate graph edges, build indexes, alter canonical data, or change output.

## Validation run

- command: python scripts/validate_wj_speaker_discourse_policy.py
- result: passed
- failures: none

- command: python scripts/validate_chunking_agent_preflight.py
- result: passed
- failures: none

- command: python scripts/validate_bible_chunking_readiness_map.py
- result: passed
- failures: none

- command: python scripts/validate_chunking_theological_decision_register.py --changed-file docs/roadmap/T355_WJ_SPEAKER_POLICY_AND_TARGET_SELECTION.md --changed-file .ai/control/chunking_theological_decision_register.yaml
- result: passed
- failures: none

- command: python scripts/validate_task_scope.py --task-id T355
- result: passed
- failures: none

- command: python scripts/validate_owner_selection_implementation_gate.py
- result: passed
- failures: none

- command: python -m pytest -q tests\test_wj_speaker_discourse_policy.py tests\test_chunking_agent_preflight.py tests\test_bible_chunking_readiness_map.py tests\test_task_scope_validator.py tests\test_ai_roadmap_table_of_contents.py tests\test_t351_bible_wide_research_triage.py tests\test_t344_revelation_owner_selection.py tests\test_t343_revelation_review_packet.py tests\test_t342_revelation_candidate_selection.py tests\test_t337_selection_docs.py tests\test_t337a_psalm_review_packet.py
- result: 61 passed
- failures: none

- command: python scripts/validate_all.py
- result: all validation gates passed
- failures: none

- command: python -m pytest -q
- result: 326 passed
- failures: none

## Known risks

- Future agents may still overread red-letter markup as speaker authority unless they read preflight and the T355 policy.
- John 3 is especially sensitive because the Jesus/narrator boundary can affect discourse scope and downstream chunk labels.
- Revelation WJ voice-shift cases remain research/prep-only and must not inherit Gospel speaker assumptions.

## Open questions

- Does the owner approve any exact John 3 parent or child speaker/discourse boundary after reviewing the packet?
- Should Matthew 5-7 or John 13-17 become the next WJ review-packet target after John 3 owner review?

## Next agent instruction

T355 is complete as non-output-changing policy/target-selection work once validation passes. Do not
implement WJ-driven chunks, Jesus speaker attribution, graph edges, retrieval truth, reviewed gold,
Revelation behavior, or output changes from this policy. The next safe human action is owner review
of `John.3.1-John.3.36` using the existing pending review packet.
