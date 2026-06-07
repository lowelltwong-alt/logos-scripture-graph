# Task Handoff

## Task

- task_id: T316c
- title: Words-of-Jesus marker stress cases
- phase: phase_4
- status: complete

## Agent

- agent_name: Codex
- mode: build
- stage: final
- updated_at: 2026-06-07T21:47:35+00:00
- handoff_id: manual-t316c-20260607

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/DATA_MAP.md
- .ai/control/RAW_SOURCE_INVENTORY.md
- ROADMAP_STATE.yaml
- HANDOFF_PROTOCOL.md
- .ai/control/METHODOLOGY_UPDATE_RULES.md
- docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md
- eval/chunking_gold/stress_atlas/chunking_stress_cases.json
- eval/chunking_gold/stress_atlas/BIBLICAL_CHUNKING_STRESS_ATLAS.md
- eval/chunking_gold/review_packets/
- eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md
- tests/test_chunking_stress_atlas.py
- data/canonical/translations/eng-web/boundary_claims.jsonl
- data/canonical/translations/eng-web/word_tokens.jsonl
- schemas/handoff.schema.json
- scripts/agent/force_handoff.py

## Files changed

- eval/chunking_gold/stress_atlas/chunking_stress_cases.json
- eval/chunking_gold/stress_atlas/BIBLICAL_CHUNKING_STRESS_ATLAS.md
- eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md
- eval/chunking_gold/README.md
- docs/roadmap/T316_BIBLICAL_CHUNKING_STRESS_ATLAS.md
- docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md
- .ai/control/METHODOLOGY_UPDATE_RULES.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/roadmap_events.jsonl
- .ai/control/handoff_ledger.jsonl
- ROADMAP_STATE.yaml
- .ai/tasks/T316c.task.yaml
- .ai/handoffs/T316c/handoff.md
- .ai/handoffs/T310/handoff.md
- tests/test_chunking_stress_atlas.py

## Decisions made

- Methodology updated: yes.
- Added seven proposed marker-sensitive stress cases:
  - `gospels_wj_marker_spans`
  - `psalms_selah_qs_markers`
  - `john3_wj_speaker_boundary`
  - `matt5_7_sermon_on_mount_wj_discourse`
  - `john13_17_wj_farewell_discourse_marker_focus`
  - `synoptic_apocalyptic_wj_discourses`
  - `john7_53_8_11_wj_variant_speech`
- All added cases are `status: proposed` and `implementation_allowed: false`.
- `\wj` is recorded as evidence, not speaker-attribution authority.
- `\qs` is recorded as liturgical-rubric evidence, not an automatic chunk boundary.
- Speaker attribution, theological interpretation, textual-critical status, source-language scope,
  canon/boundary-text decisions, and tradition-scoped interpretations require explicit human
  authorization and reviewed evidence/gold before implementation.
- No reviewed gold, chunk output change, evaluator formula change, raw/canonical mutation,
  chunker/orchestrator behavior change, runtime skill change, or skill promotion was added.
- `python scripts/agent/force_handoff.py --task-id T316c --agent Codex --stage start --mode build`
  was attempted and failed because the helper enforces `^T[0-9]{3,}$`; the requested T316c handoff
  was created manually with the required sections.
- Leaderboard was not run because no score/evaluator/leaderboard/scorecard/manifest-boundary or
  chunk-output-affecting file changed.

## Validation run

- command: `python -m pytest -q tests/test_chunking_stress_atlas.py`
- result: passed, `8 passed`.
- command: `python scripts/validate_all.py`
- result: passed, all validation gates passed with 21 referenced handoff paths.
- command: `python -m pytest -q`
- result: passed, `79 passed`.
- failures: none.

## Known risks

- Marker-sensitive cases are proposed stress cases only, not reviewed gold.
- Words-of-Jesus red-letter conventions vary by edition and translation.
- Selah / `\qs` spans may be performance or liturgical evidence rather than structural boundaries.
- John 3, John 7:53-8:11, and Synoptic apocalyptic discourse cases require human review before any
  speaker, textual-critical, or boundary decision.

## Open questions

- Which marker-sensitive case should become a pending review packet first?
- Should `\wj` and `\qs` eventually have dedicated diagnostics separate from boundary decisions?
- Should marker-sensitive review wait for a formal TextSpan or speaker-attribution layer?

## Next agent instruction

Review/accept the T316c proposed marker-sensitive stress cases. Do not start output-changing work
until a selected case is promoted by human review into reviewed gold, characterization-only evidence,
or a pending review packet with explicit target behavior.
