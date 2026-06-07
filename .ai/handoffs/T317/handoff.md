# Task Handoff

## Task

- task_id: T317
- title: Psalm gold, WJ review packets, and token policy analysis
- phase: phase_4
- status: complete

## Agent

- agent_name: Codex
- mode: build
- stage: final
- updated_at: 2026-06-07T22:36:32+00:00
- handoff_id: t317-codex-20260607

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/DATA_MAP.md
- .ai/control/RAW_SOURCE_INVENTORY.md
- ROADMAP.md
- ROADMAP_STATE.yaml
- HANDOFF_PROTOCOL.md
- docs/architecture/ARCHITECTURE.md
- docs/chunking/CHUNKING_DESIGN.md
- config/agents/agent_roles.yaml
- .ai/control/METHODOLOGY_UPDATE_RULES.md
- docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md
- .ai/workflows/chunking-skill-supply-chain.workflow.md
- pipelines/chunking/skills/SKILL_CREATION_PLAYBOOK.md
- eval/chunking_gold/per_form/psalms_gold_manifest.json
- eval/chunking_gold/per_form/psalms_gold_plan.md
- eval/chunking_gold/review_packets/ps105_boundary_review.md
- eval/chunking_gold/review_packets/ps106_boundary_review.md
- eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md
- eval/chunking_gold/README.md
- eval/chunking_runs/claude-opus-4.8__pass2__D_claude_pass2__20260605T112450Z.json
- docs/roadmap/T313_TOKEN_SIZE_EVALUATOR_POLICY_ALIGNMENT.md
- pipelines/chunking/evaluate_chunks.py
- pipelines/chunking/leaderboard.py
- config/chunking/chunking_policy.yaml
- tests/test_chunker_gold.py
- tests/test_stress_review_packets.py
- tests/test_chunking_stress_atlas.py
- scripts/validate_chunking_gold.py
- data/canonical/translations/eng-web/boundary_claims.jsonl
- data/canonical/translations/eng-web/word_tokens.jsonl
- data/canonical/translations/eng-web/section_headings.jsonl

## Files changed

- eval/chunking_gold/per_form/psalms_gold_manifest.json
- eval/chunking_gold/per_form/psalms_gold_plan.md
- eval/chunking_gold/review_packets/ps105_boundary_review.md
- eval/chunking_gold/review_packets/ps106_boundary_review.md
- eval/chunking_gold/review_packets/john3_wj_speaker_boundary_review.md
- eval/chunking_gold/review_packets/matt5_7_wj_discourse_review.md
- eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md
- eval/chunking_gold/README.md
- docs/roadmap/T313_TOKEN_SIZE_EVALUATOR_POLICY_ALIGNMENT.md
- docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md
- .ai/workflows/chunking-skill-supply-chain.workflow.md
- pipelines/chunking/skills/SKILL_CREATION_PLAYBOOK.md
- .ai/control/METHODOLOGY_UPDATE_RULES.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/roadmap_events.jsonl
- .ai/control/handoff_ledger.jsonl
- .ai/handoffs/T310/handoff.md
- .ai/handoffs/T317/handoff.md
- .ai/tasks/T317.task.yaml
- ROADMAP_STATE.yaml
- tests/test_chunker_gold.py
- tests/test_stress_review_packets.py

## Decisions made

- Methodology updated: yes.
- Ps.105 current whole-psalm chunk `Ps.105.1-Ps.105.45` is reviewed gold.
- Ps.106 current whole-psalm chunk `Ps.106.1-Ps.106.48` is reviewed gold.
- Ps.106 `b` markers are internal formatting/stanza evidence, not automatic split authority.
- John 3 WJ speaker-boundary packet remains `pending_human_review` with `Decision: pending`.
- Matthew 5-7 WJ discourse packet remains `pending_human_review` with `Decision: pending`.
- `\wj` is evidence, not authority; speaker attribution requires human review.
- T313 token-size analysis is analysis only and does not authorize evaluator changes or chunking
  retunes.
- No chunk output change, evaluator formula change, raw/canonical mutation, chunker/orchestrator
  behavior change, runtime skill change, or skill promotion was made.
- Leaderboard was not run because no evaluator, leaderboard, scorecard, or chunk-output-affecting
  file changed. The Psalm manifest additions are reviewed whole-psalm cases and do not add
  structural-split score exclusions or alter evaluator policy.

## Validation run

- command: `python scripts/validate_chunking_gold.py`
- result: passed, `Chunking gold validation passed for 1 manifest(s).`
- command: `python -m pytest -q tests/test_stress_review_packets.py`
- result: passed, `4 passed`.
- command: `python -m pytest -q tests/test_chunker_gold.py`
- result: passed, `15 passed`.
- command: `python scripts/validate_all.py`
- result: passed, all validation gates passed.
- command: `python -m pytest -q`
- result: passed, `83 passed`.
- failures: none.

## Known risks

- John 3 speaker-boundary interpretation remains human-gated.
- Matthew 5-7 parent/child discourse structure remains human-gated.
- Ps.105/Ps.106 future child chunks would require a new human decision and exact child spans.
- T313 p50 headroom is broad and risky; implementation without reviewed target gold would be metric
  chasing.

## Open questions

- Should John 3 or Matthew 5-7 be promoted first into reviewed parent/child gold after human review?
- Should token-size target alignment move the evaluator target, the chunking policy target, or both?
- Should future WJ diagnostics become separate from boundary decisions?

## Next agent instruction

Claude review T317. Merge if validation and review are green. Do not start output-changing work
until a selected case has reviewed target gold that explicitly authorizes it.

---

## Handoff refresh: final

- agent_name: Codex
- mode: build
- updated_at: 2026-06-07T22:40:00+00:00
- handoff_id: 47627af671fb8635
