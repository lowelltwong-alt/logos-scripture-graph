# T458 Handoff - AI-Agnostic Rust Subagent Charter

## Task
- task id: T458
- agent name: Codex
- mode: control-plane validation hardening
- branch: `codex/t458-rust-subagent-charter`

## Files Read
- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md` (read only)
- `.ai/control/PROJECT_STATUS.md`
- `config/agents/agent_roles.yaml`
- `config/agents/model_routing.yaml`
- `.ai/control/multi_agent_review_cadence.yaml`
- `.ai/control/coding_runtime_language_preflight.yaml`
- `scripts/validate_task_scope.py`
- `scripts/validate_dad_outbox.py`
- `.digital-asset/mail/outbox.jsonl`
- `.digital-asset/context-map.json`
- `.digital-asset/lessons/t424_rust_validation_layer.yaml`

## Files Changed
- `.ai/control/ai_agnostic_rust_subagent_charter.yaml`
- `.ai/control/chunking_lesson_index.yaml`
- `.ai/control/multi_agent_review_cadence.yaml`
- `.ai/tasks/T458.task.yaml`
- `.ai/handoffs/T458/handoff.md`
- `config/agents/agent_roles.yaml`
- `config/agents/model_routing.yaml`
- `.digital-asset/mail/outbox.jsonl`
- `.digital-asset/context-map.json`
- `.digital-asset/lessons/t458_ai_agnostic_rust_subagent_charter.yaml`
- `scripts/validate_ai_agnostic_rust_subagents.py`
- `scripts/validate_all.py`
- `tests/test_ai_agnostic_rust_subagents.py`

## Decisions Made
- Added five AI-agnostic Rust-support roles:
  - `rust_architecture_reviewer`
  - `outside_rust_research_scout`
  - `rust_engineer`
  - `rust_qa_tester`
  - `dad_lesson_reporter`
- Routed the roles by capability profile only: `reasoner`, `executor`, and `orchestrator`.
- Kept T458 itself Python-only because the new code validates small YAML/JSON governance semantics, not a large deterministic scan.
- Added a DAD candidate-only lesson triplet so scout findings and Rust rollout lessons are auditable outside chat.

## Scout/Subagent Notes
- Rust architecture scout recommended the five-role split, capability-profile routing, and validator assertions for role completeness, no vendor/model lock-in, Python/Rust parity, and DAD non-authority.
- QA/DAD scout confirmed DAD lessons should remain candidate-only, local-adoption-required, and include extra context about messy parallel repo/Rust rollout conditions.
- Both scouts were read-only and made no file changes.

## Validation Performed
- `python scripts/validate_ai_agnostic_rust_subagents.py` - passed
- `python scripts/validate_dad_outbox.py` - passed
- `python scripts/validate_task_scope.py --task-id T458` - passed
- `python scripts/agent/validate_handoffs.py` - passed
- `python -m pytest tests/test_ai_agnostic_rust_subagents.py -q` - 5 passed
- `python scripts/validate_chunking_lesson_index.py` - passed
- `python scripts/validate_all.py` - passed with repo-local `TMP`/`TEMP`/`CARGO_TARGET_DIR`
- `python -m pytest -q` - 759 passed with repo-local `TMP`/`TEMP`/`CARGO_TARGET_DIR`
- `python scripts/generate_data_map.py --check` - passed
- `git diff --check` - passed

## Risks Introduced
- DAD outbox/context files are active cross-PR surfaces. If T456/T457/T458 merge out of order, `.digital-asset/mail/outbox.jsonl` and `.digital-asset/context-map.json` may need straightforward conflict resolution.
- The charter records subagent roles but does not implement a central scheduler. That remains a future orchestration task if needed.

## Non-Authorizations Preserved
- No chunk output.
- No reviewed gold.
- No child spans.
- No route or evaluator behavior changes.
- No graph, retrieval, or vector truth.
- No embeddings, indexes, backend choice, or profile promotion.
- No source rows, manuscript rows, preferred reading, source-tradition choice, canon change, or theology authority.
- No DAD override of local governance.
- No vendor/model lock-in.

## Unresolved Questions
- Whether DAD should later promote the T458 role split into a central asset template for every repo doing Rust-heavy validator work.
- Whether the repo should add a broader automated scheduler/orchestrator that assigns these roles per task; T458 only records and validates the charter.

## Exact Next Action
Run the focused T458 gates, then `validate_all.py`, full pytest if time allows, data-map check, and diff check. If clean, commit and push `codex/t458-rust-subagent-charter`.
