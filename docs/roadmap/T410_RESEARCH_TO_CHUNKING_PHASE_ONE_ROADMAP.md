---
object_type: roadmap_report
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-30 by Codex during T410 as the governed bridge from Cursor research to Phase 1 chunking completion."
reason_for_inclusion: "Record how the repo moves from long-running research/prompt packs into exact owner-gated parent-only additive chunk overlays, then into Phase 2+."
---

# T410 Research-To-Chunking Phase One Roadmap

## Summary

T410 turns the T402/T404/T406 research runway into a governed conveyor belt. Cursor may run long
research and review-prep batches, Codex reviews and enriches the next prompt pack, Claude Opus or
an equivalent frontier reviewer checks hard cases, and only later owner-gated tasks may promote
reviewed gold or implement output.

Chunking Phase 1 means one governed, parent-only, additive low-risk chunk overlay per canonical
book where safe. Books that are not safe are explicitly deferred with evidence and next-phase
routing. T410 itself creates no chunks, reviewed gold, child spans, route behavior, evaluator
behavior, graph/retrieval/vector truth, source rows, canon changes, or theology authority.

## Phase Ladder

Every candidate follows the same ladder:

1. Research by Cursor.
2. Review packet prep by Cursor.
3. Codex review.
4. Frontier escalation when triggered.
5. Owner gate for exact target and parent span.
6. Reviewed-gold promotion by Codex after owner approval.
7. Route-isolated harness proof.
8. Output-changing additive parent overlay PR.
9. Post-pilot review.

Cursor may work through steps 1 and 2 only. Codex owns review and later implementation gates.
Claude Opus/frontier review is required for hard literary or theological cases before they move
toward authority.

## Phase 1 Completion

Phase 1 closes only when all 66 canonical books are deterministically accounted for as:

- `implemented_existing_pilot`
- `implemented_phase_one_overlay`
- `pending_phase_one_gate`
- `deferred_phase_two_or_frontier_default`

The completion audit must record implemented books, deferred books, reasons, output hashes,
non-target identity proofs, reviewed-gold/owner authorization references, validation results, and
Phase 2 routing.

## Parallel Safety

Parallelism is allowed only for isolated Cursor research and review-prep artifacts. Each batch uses
one task id, one branch, and one worktree. Cursor must run and record `git status --short --branch`,
run `python scripts/validate_parallel_execution_safety.py --task-id <TASK_ID> --require-task-branch`,
confirm no merge/rebase/cherry-pick/bisect state is active, and stop if artifacts from another task
id are present in the same worktree.

Cursor writes only `.ai/context/agent_work/<TASK_ID>/` and `.ai/handoffs/<TASK_ID>/`. Shared
control-plane files such as `PROJECT_STATUS.md`, `current_focus.yaml`, `ROADMAP_STATE.yaml`,
readiness maps, lesson indexes, and roadmap TOCs are serialized through one Codex integrator branch
with an explicit merge order.

T411 starts only after T410 is committed, merged to `main`, and the parallel safety checks validate.

## Validation Tiers

Cursor research batches use focused validators, task-scope checks, and handoff checks. Control-plane
or schema changes require the focused validator, focused pytest, task-scope validation, handoff
validation, and `python scripts/validate_all.py`. Data-pipeline, output-changing, merge, and
release work require the heavier gates recorded in
`.ai/control/cursor_to_codex_transparency_contract.yaml`, including full pytest where required.

## Prompt-Pack Templates

### Cursor Batch Prompt

Use this for long-running Cursor work:

```text
Task: <TASK_ID>
Mode: research-only / review-packet prep only
Allowed paths: .ai/context/agent_work/<TASK_ID>/ and .ai/handoffs/<TASK_ID>/
Books or candidates: <OWNER_OR_CODEX_SUPPLIED_LIST>

Read first:
- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md read-only
- .ai/control/PROJECT_STATUS.md
- .ai/control/parallel_chunking_research_program.yaml
- .ai/control/bible_book_literature_prompt_hints.yaml
- .ai/control/cursor_to_codex_transparency_contract.yaml
- .ai/control/frontier_chunking_escalation_policy.yaml
- .ai/control/chunking_phase_completion_plan.yaml

Preflight:
- run git status --short --branch
- run python scripts/validate_parallel_execution_safety.py --task-id <TASK_ID> --require-task-branch
- confirm no merge/rebase/cherry-pick/bisect state
- stop if artifacts from another task id are present
- record the preflight in audit_log.jsonl

Produce:
- cursor_notes_to_codex.md
- source_size_manifest.jsonl
- confidence_register.jsonl
- audit_log.jsonl
- claim_traceability_matrix.md
- escalation_packets/ when needed
- handoff.md

Stop before target selection, reviewed gold, chunk output, child spans, route/evaluator changes,
graph/retrieval/vector work, source rows, canon changes, source-tradition preference, or theology
authority.
```

### Codex Review Prompt

```text
Review the Cursor task as non-authorizing research/prep. Verify files read, source sizes, hashes,
audit logs, confidence, claim traceability, escalation packets, and compliance with T410. Decide
whether the work is ready for owner options, needs edits, needs frontier review, or should remain
deferred.
```

### Frontier Audit Prompt

```text
Audit the exact packet or batch for theological, literary, and architecture risk. Check faithfulness,
doxology, doctrinal consequences, source-metadata authority, original-language pressure, and hidden
theology smuggling. Recommend required changes or deferral. Do not authorize reviewed gold or output.
```

## Next Tasks

- T411: Cursor short-book research and review-packet prep batch.
- T412: Codex review of T411 and owner-selection docket for first exact batch.
- T413: Owner-approved parent-only reviewed-gold promotion for batch 1.
- T414: Route-isolated additive overlay implementation for batch 1.
- T415-T42x: Repeat by genre/risk until all 66 books are implemented or deferred.

## Validation

T410 is validated by:

```bash
python scripts/validate_parallel_chunking_prompt_pack.py
python -m pytest tests/test_parallel_chunking_prompt_pack.py -q
python scripts/validate_task_scope.py --task-id T410
python scripts/agent/validate_handoffs.py
python scripts/validate_all.py
```
