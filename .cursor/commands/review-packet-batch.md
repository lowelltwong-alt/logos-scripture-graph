# Review Packet Batch

Use this Cursor command only after the owner or Codex supplies exact candidates or spans. This is
review-packet prep only; it is not reviewed gold and not chunk output.

## Required Preflight

Read:

- `.ai/control/parallel_chunking_research_program.yaml`
- `.ai/control/cursor_to_codex_transparency_contract.yaml`
- `.ai/control/frontier_chunking_escalation_policy.yaml`
- `.ai/control/bible_book_literature_prompt_hints.yaml`
- `.ai/control/whole_bible_low_complexity_chunking_candidate_queue.yaml`
- prior relevant review packets and owner decisions

Before packet prep:

- run `git status --short --branch`
- confirm no merge, rebase, cherry-pick, or bisect state is active
- stop if untracked artifacts from another task id are present
- use one task id, one branch, and one worktree
- record the preflight result in `.ai/context/agent_work/<TASK_ID>/audit_log.jsonl`

Cursor may write only `.ai/context/agent_work/<TASK_ID>/` and `.ai/handoffs/<TASK_ID>/`.
Shared control-plane edits are serialized through a Codex integrator.

## Allowed Work

- summarize source evidence
- record marker and Strong's metadata as evidence only
- identify confidence and limitations
- prepare Codex-readable packet notes
- create escalation packets for hard issues

## Disallowed Work

Stop before any of the following:

- choosing candidates
- promoting reviewed gold
- adding child spans
- changing chunk output
- changing route/evaluator behavior
- creating graph/retrieval/vector truth
- deciding theology
- treating source metadata as boundary authority
- dirty files outside allowed paths
- artifacts from another task id in the same worktree

## Deliverable

Produce `cursor_notes_to_codex.md` and the required T410 machine logs. Mark the packet
non-authorizing and include exact next action:
Codex review, owner options, frontier escalation, or defer.
