# Task Handoff

## Task

- task_id: T327A1
- title: Three-Repo Routing Guardrails
- phase: phase_4
- status: complete

## Agent

- agent_name: Codex
- mode: plan
- stage: final
- updated_at: 2026-06-08T15:50:00+00:00
- handoff_id: t327a1-codex-20260608

## Files read

- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/METHODOLOGY_UPDATE_RULES.md
- docs/roadmap/CANONICAL_66_BOOK_SCOPE_POLICY.md
- docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md
- docs/roadmap/T327A_FORENSIC_CANONICAL_CORPUS_SCOPE_AUDIT.md
- boundary repo AI_FRONT_DOOR.md
- boundary repo README.md
- boundary repo governance/CANON_AND_AUTHORITY_POLICY.md
- boundary repo governance/TRUST_HIERARCHY.md
- boundary repo governance/CONTAMINATION_CONTROLS.md
- boundary repo governance/CROSS_REPO_CONTRACT_WITH_LOGOS_SCRIPTURE_GRAPH.md
- boundary repo governance/RULES_REGISTRY.md
- governance repo status/log, read only

## Files changed

- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- .ai/control/boundary_material_routing.yaml
- .ai/control/PROJECT_STATUS.md
- .ai/control/METHODOLOGY_UPDATE_RULES.md
- .ai/control/roadmap_events.jsonl
- docs/roadmap/CANONICAL_66_BOOK_SCOPE_POLICY.md
- docs/roadmap/T327A1_THREE_REPO_ROUTING_GUARDRAILS.md
- docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md
- .ai/tasks/T327A1.task.yaml
- .ai/handoffs/T327A1/handoff.md
- ROADMAP_STATE.yaml
- tests/test_boundary_material_routing_policy.py
- boundary repo AI_FRONT_DOOR.md
- boundary repo README.md
- boundary repo .ai/control/PROJECT_STATUS.md
- boundary repo .ai/control/boundary_material_routing.yaml
- boundary repo governance/CANON_AND_AUTHORITY_POLICY.md
- boundary repo governance/CONTAMINATION_CONTROLS.md
- boundary repo governance/CROSS_REPO_CONTRACT_WITH_LOGOS_SCRIPTURE_GRAPH.md
- boundary repo governance/RULES_REGISTRY.md
- boundary repo governance/THREE_REPO_ROUTING_GUARDRAILS.md
- boundary repo .ai/tasks/T002_THREE_REPO_ROUTING_GUARDRAILS.task.yaml
- boundary repo .ai/handoffs/T002_THREE_REPO_ROUTING_GUARDRAILS.md
- boundary repo tests/test_three_repo_routing_guardrails.py

## Decisions made

- `logos-scripture-graph` remains canonical 66-book Scripture authority.
- `logos-boundary-literature` is supporting boundary/reception authority under, or at minimum never above, canonical Scripture authority.
- `logos-governance-architecture` owns cross-repo policy, authority contracts, update rules, and validation patterns.
- The merged governance registry at `logos-governance-architecture/governance/LOGOS_REPO_REGISTRY.yaml` is the source of truth for repo registry and relationship contracts.
- Boundary material may provide background, comparison, reception history, refutation targets, commentary/reception claims, and tradition-scoped claims.
- Boundary material must not override, contaminate, or become equal authority to canonical Scripture.
- If a task appears to require boundary material to modify canonical Scripture outputs, stop and report.
- Governance repo registry work is now merged; this Scripture-side routing policy mirrors that registry locally for agent routing.
- No data, text import, output, evaluator, scorecard, parser/chunker/orchestrator, or T327B work occurred.

## Validation run

- command: `python -m pytest -q tests/test_boundary_material_routing_policy.py`
- result: passed, `6 passed`.
- command: `python scripts/validate_all.py`
- result: passed, all validation gates passed.
- command: `python -m pytest -q`
- result: passed, `115 passed`.
- command: boundary repo schema parse / pytest
- result: passed, `python -m pytest -q` reported `4 passed`; schema parse reported `Schema parse passed`.
- command: protected path checks in Scripture repo and boundary repo
- result: no protected data/runtime/output paths changed.
- failures: none.

## Known risks

- Child repos may need later mirror updates if the governance registry changes.
- The Scripture branch is stacked on T327A because T327A introduced the canonical scope policy used by this routing patch.
- Boundary repo currently has lightweight tests only; fuller validation remains future work.

## Open questions

- Should child repos consume a governance-owned registry schema directly, or continue to mirror local routing policies?
- Should future PRs coordinate all three repos in one review cycle or land Scripture/boundary first and governance later?

## Next agent instruction

Claude review this main-based Scripture routing guardrail PR if needed. Do not start T327B until T327A/T327A1 are accepted on main. After merge, run T327B canonical 66-book allow-list / ingest filter.
