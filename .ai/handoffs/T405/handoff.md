# Task Handoff

## Task

- task_id: T405
- title: Child Governance Dependency-Map Mirror
- phase: phase_4
- status: complete_local_governance_mirror_gate

## Agent

- agent_name: codex
- mode: build
- stage: final
- updated_at: 2026-06-29T00:00:00Z
- handoff_id: t405-governance-dependency-map-mirror

## Files read

- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- README.md
- AGENTS.md
- config/governance/repository_link_contract.yaml
- scripts/validate_repository_link_contract.py
- scripts/validate_all.py
- scripts/validate_chunking_lesson_index.py
- tests/test_chunking_lesson_index.py
- .ai/control/current_focus.yaml
- .ai/control/chunking_lesson_index.yaml
- .ai/tasks/T401.task.yaml

## Files changed

- .ai/control/governance_dependency_map_mirror.yaml
- .ai/control/chunking_lesson_index.yaml
- .ai/tasks/T405.task.yaml
- .ai/handoffs/T405/handoff.md
- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- README.md
- config/governance/repository_link_contract.yaml
- scripts/validate_governance_dependency_map_mirror.py
- scripts/validate_repository_link_contract.py
- scripts/validate_chunking_lesson_index.py
- scripts/validate_all.py
- tests/test_governance_dependency_map_mirror.py
- tests/test_chunking_lesson_index.py

## Decisions made

- Added a local child-repo mirror of upstream `logos-governance-architecture/governance/GOVERNANCE_DEPENDENCY_MAP.yaml` artifact `GD-014`.
- Wired the mirror into the repository link contract, front door, AI table of contents, README, aggregate validator, and focused pytest.
- Added `LSN-033` to the chunking lesson index so governance-facing child-repo mirror work is discoverable from the Scripture Graph preflight surfaces.
- Kept the mirror non-authorizing: it cannot override upstream governance, weaken governance, change Scripture data, change chunk output, import boundary material, or create graph/retrieval/vector truth.

## Validation run

- command: `python scripts/validate_governance_dependency_map_mirror.py`
- result: passed
- failures: none known
- command: `python scripts/validate_repository_link_contract.py`
- result: passed
- failures: none known
- command: `python scripts/validate_chunking_lesson_index.py`
- result: passed
- failures: none known
- command: `python scripts/validate_task_scope.py --task-id T405`
- result: passed
- failures: none known
- command: `python -m pytest -q tests/test_governance_dependency_map_mirror.py`
- result: passed
- failures: none known
- command: `python -m pytest -q tests/test_chunking_lesson_index.py`
- result: passed
- failures: none known
- command: `python scripts/validate_all.py`
- result: failed after all new governance/lesson gates passed
- failures: missing local canonical data artifacts in this isolated worktree: `data/canonical/translations/eng-web/word_tokens.jsonl`, `data/canonical/translations/eng-web/editorial_cross_references.jsonl`, `data/canonical/scripture/passages/passages.jsonl`, and `data/canonical/translations/eng-web/translation_witnesses.jsonl`

## Known risks

- The upstream governance map remains the source of truth; this local mirror must be updated when upstream governance says scripture-graph child mirrors changed.
- This task does not update live upstream governance or boundary literature; those are separate coordinated PRs.

## Open questions

- None.

## Next agent instruction

For future governance-facing scripture-graph changes, read `.ai/control/governance_dependency_map_mirror.yaml` and check upstream `logos-governance-architecture/governance/GOVERNANCE_DEPENDENCY_MAP.yaml` before editing. If upstream GD-014 or child-repo mirror obligations changed, update this local mirror, front-door/TOC discovery, validators, and tests in the same PR.
