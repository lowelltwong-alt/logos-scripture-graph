# Task Handoff

## Task

- task_id: T316b
- title: Stress-case review packets
- phase: phase_4
- status: complete

## Agent

- agent_name: Codex
- mode: build
- stage: final
- updated_at: 2026-06-07T17:39:59+00:00
- handoff_id: manual-t316b-20260607

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/DATA_MAP.md
- .ai/control/RAW_SOURCE_INVENTORY.md
- ROADMAP.md
- ROADMAP_STATE.yaml
- HANDOFF_PROTOCOL.md
- eval/chunking_gold/stress_atlas/chunking_stress_cases.json
- eval/chunking_gold/stress_atlas/BIBLICAL_CHUNKING_STRESS_ATLAS.md
- eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md
- eval/chunking_gold/README.md
- eval/chunking_gold/per_form/psalms_gold_manifest.json
- eval/chunking_gold/review_packets/ps78_boundary_review.md
- eval/chunking_runs/claude-opus-4.8__pass2__D_claude_pass2__20260605T112450Z.json
- tests/test_chunker_gold.py
- tests/test_chunking_stress_atlas.py
- docs/roadmap/T316_BIBLICAL_CHUNKING_STRESS_ATLAS.md
- docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md
- .ai/control/METHODOLOGY_UPDATE_RULES.md
- .ai/handoffs/T310/handoff.md
- schemas/handoff.schema.json
- scripts/agent/force_handoff.py
- scripts/agent/validate_handoffs.py

## Files changed

- eval/chunking_gold/review_packets/ps105_boundary_review.md
- eval/chunking_gold/review_packets/ps106_boundary_review.md
- eval/chunking_gold/review_packets/isa52_13_53_12_boundary_review.md
- eval/chunking_gold/review_packets/mark16_9_20_textual_variant_review.md
- eval/chunking_gold/review_packets/john7_53_8_11_textual_variant_review.md
- tests/test_stress_review_packets.py
- eval/chunking_gold/README.md
- eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md
- docs/roadmap/T316_BIBLICAL_CHUNKING_STRESS_ATLAS.md
- docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md
- .ai/control/METHODOLOGY_UPDATE_RULES.md
- .ai/control/PROJECT_STATUS.md
- ROADMAP_STATE.yaml
- .ai/control/roadmap_events.jsonl
- .ai/control/handoff_ledger.jsonl
- .ai/tasks/T316b.task.yaml
- .ai/handoffs/T316b/handoff.md
- .ai/handoffs/T310/handoff.md

## Decisions made

- Methodology updated: yes.
- Created pending review packets for the five selected T316 stress-atlas cases.
- All packets are `pending_human_review`.
- All packets include `Decision: pending`.
- All packets state: `This packet does not authorize output-changing work.`
- No selected case was marked as reviewed gold, approved expected output, or reviewed structural
  split.
- Current behavior was inspected from a temporary chunker output in the system temp directory.
- Local marker/footnote evidence was read from existing canonical sidecars and raw-derived boundary
  claims only; no external textual-critical data was imported.
- `python scripts/agent/force_handoff.py --task-id T316b --agent Codex --stage start` was attempted
  and failed because the helper enforces `^T[0-9]{3,}$`; the requested `T316b` handoff was therefore
  created manually with the required sections.
- No chunk output, evaluator formula, raw/canonical data, chunker/orchestrator behavior, runtime
  skill code, or skill promotion changed.
- Leaderboard was not run because no score/evaluator/leaderboard/scorecard/manifest-boundary or
  chunk-output-affecting file changed.

## Validation run

- command: `python -m pytest -q tests/test_stress_review_packets.py`
- result: passed, `2 passed`.
- command: `python scripts/validate_all.py`
- result: passed, all validation gates passed with 20 referenced handoff paths.
- command: `python -m pytest -q`
- result: passed, `76 passed`.
- failures: none.

## Known risks

- Review packets are evidence packets, not reviewed gold.
- Psalm 105 and Psalm 106 child boundaries remain unresolved.
- Isaiah 52:13-53:12 needs human review before any cross-chapter parent unit is approved.
- Mark 16:9-20 and John 7:53-8:11 require textual-criticism review before any variant-aware gold or
  policy change.
- The `T316b` task suffix does not match the current force-handoff helper's numeric task-id regex.

## Open questions

- Should Psalm 105 stay one whole-psalm chunk or become a parent/child structural split?
- Should Psalm 106 use observed `b` markers as child-boundary evidence after human review?
- Should Isaiah 52:13-53:12 become a reviewed cross-chapter parent unit?
- Should major textual-variant zones be isolated as chunks, represented as metadata overlays, or
  handled through context packets?

## Next agent instruction

Review/accept the T316b review packets. Do not start output-changing work until a human decision
promotes a packet into reviewed gold, characterization-only evidence, or an approved parent/child
structural split with exact target behavior.
