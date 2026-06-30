# Verse Ledger Batch

Use this command for a Cursor long-running research batch. It is research-only and non-authorizing.

## Required Preflight

Read:

- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md` read-only
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/parallel_chunking_research_program.yaml`
- `.ai/control/bible_book_literature_prompt_hints.yaml`
- `.ai/control/cursor_to_codex_transparency_contract.yaml`
- `.ai/control/frontier_chunking_escalation_policy.yaml`
- `.ai/control/chunking_phase_completion_plan.yaml`
- `.ai/control/whole_bible_low_complexity_chunking_candidate_queue.yaml`
- `.ai/control/test_runtime_preflight.yaml`

Before reading or writing batch artifacts:

- run `git status --short --branch`
- run `python scripts/validate_parallel_execution_safety.py --task-id <TASK_ID> --require-task-branch`
- confirm no merge, rebase, cherry-pick, or bisect state is active
- stop if untracked artifacts from another task id are present
- use one task id, one branch, and one worktree
- record the preflight result in `.ai/context/agent_work/<TASK_ID>/audit_log.jsonl`

Cursor may write only `.ai/context/agent_work/<TASK_ID>/` and `.ai/handoffs/<TASK_ID>/`.
Shared control-plane files are for the Codex integrator, not parallel Cursor batch edits.

## Inputs

The owner or Codex must supply:

- exact task id
- exact book list or candidate list
- allowed output paths

Cursor must not choose the target list.

## Output Contract

Write under `.ai/context/agent_work/<TASK_ID>/` and `.ai/handoffs/<TASK_ID>/`:

- `source_size_manifest.jsonl`
- `confidence_register.jsonl`
- `audit_log.jsonl`
- `claim_traceability_matrix.md`
- `escalation_packets/` when needed
- `cursor_notes_to_codex.md`
- `handoff.md`

Every claim needs evidence refs, confidence, and `non_authorizing: true`.

## Continue Gate

Move to the next book only when the current book has complete source-size, confidence, audit, and
traceability records. If a hard issue appears, write an escalation packet and continue only if the
rest of the batch is unaffected.

## Stop Conditions

Stop before target selection, reviewed-gold promotion, chunk output, child spans, route/evaluator
changes, graph/retrieval/vector work, embeddings, index builds, boundary imports, source rows,
canon changes, source-tradition preference, theology authority, dirty files outside allowed paths,
or artifacts from another task id in the same worktree.
