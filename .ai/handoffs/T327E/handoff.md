# Task Handoff

## Task

- task_id: T327E
- title: Clean Old-Corpus Eval Surfaces
- phase: phase_4
- status: complete

## Agent

- agent_name: Codex
- mode: cleanup
- stage: final
- updated_at: 2026-06-09T00:30:00+00:00
- handoff_id: t327e-codex-20260609

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- ROADMAP_STATE.yaml
- eval/chunking_gold/stress_atlas/chunking_stress_cases.json
- eval/chunking_gold/stress_atlas/BIBLICAL_CHUNKING_STRESS_ATLAS.md
- eval/chunking_gold/stress_atlas/observed_stress_behavior.json
- eval/chunking_gold/stress_atlas/OBSERVED_STRESS_BEHAVIOR.md
- eval/chunking_gold/review_packets/review_packet_index.json
- eval/chunking_gold/review_packets/REVIEW_PACKET_INDEX.md
- eval/chunking_gold/per_form/psalms_gold_manifest.json
- eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md
- pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/SKILL.md
- pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/SKILL_METADATA.json
- tests/test_review_packet_index.py
- tests/test_chunking_stress_atlas.py
- tests/test_observed_stress_behavior.py

## Files changed

- eval/chunking_gold/stress_atlas/chunking_stress_cases.json
- eval/chunking_gold/stress_atlas/BIBLICAL_CHUNKING_STRESS_ATLAS.md
- eval/chunking_gold/stress_atlas/observed_stress_behavior.json
- eval/chunking_gold/stress_atlas/OBSERVED_STRESS_BEHAVIOR.md
- pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/SKILL.md
- pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/SKILL_METADATA.json
- docs/roadmap/T327E_CLEAN_OLD_CORPUS_EVAL_SURFACES.md
- docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/roadmap_events.jsonl
- .ai/tasks/T327E.task.yaml
- .ai/handoffs/T327E/handoff.md
- ROADMAP_STATE.yaml

## Search inventory

Searched `eval/chunking_gold`, `docs`, `.ai`, `tests`, `pipelines`, `config`, and `scripts` for:

- `PrMan`, `Ps151`, `Tob`, `Jdt`, `AddEsth`, `Wis`, `Sir`, `Bar`, `1Macc`, `2Macc`, `1Esd`,
  `2Esd`, `3Macc`, `4Macc`, `AddDan`
- `81`, `38,058`, `38058`, `6,955`, `6955`
- `apocrypha`, `deuterocanonical`, `non-66`, `wider corpus`

The detailed counts are recorded in `docs/roadmap/T327E_CLEAN_OLD_CORPUS_EVAL_SURFACES.md`.

## Classification summary

- ACTIVE_CONTROL_TO_REMOVE: Psalm candidate skill docs/metadata still listed `PrMan`/`Ps151` as
  non-target controls.
- STALE_BASELINE_TO_UPDATE: stress atlas and observed behavior audit root baseline language still
  pointed at the pre-T327 93.5 wider-corpus row.
- HISTORICAL_AUDIT_TO_KEEP: T327A/T327B/T327C docs, old handoffs, patch/source inventories, and
  older design notes.
- EXCLUSION_TEST_TO_KEEP: canonical 66 config, validator, T327A/T327B tests, and validator scripts.
- BOUNDARY_ROUTING_POLICY_TO_KEEP: boundary material routing and contamination-control references.
- UNCLEAR_REVIEW: none after classification.

## Decisions made

- Updated stress atlas baseline language to the post-T327 canonical-66 93.6 baseline.
- Marked T318 observed behavior as historical pre-T327 wider-corpus diagnostic evidence requiring
  refresh before future output-changing work cites current behavior.
- Removed `PrMan`/`Ps151` from active Psalm candidate skill non-target controls; retained only
  canonical `Song`/`Lam`.
- Preserved historical audit, exclusion-test, source-inventory, and boundary-routing references.
- Did not regenerate canonical outputs or chunks.
- Did not change evaluator formula, leaderboard scoring logic, chunking algorithm, or boundary repo
  content.
- Did not start T327F/G.

## Validation run

- command: `python scripts/validate_canonical_66_scope.py`
- result: passed, canonical 66 scope config validation passed.
- command: `python scripts/validate_all.py`
- result: passed, all validation gates passed; handoff validation passed for 32 referenced paths,
  chunking gold validation passed for 1 manifest, canonical 66 scope validation passed for 8 JSONL
  files, and JSONL validation passed for 63,959 records.
- command: `python -m pytest -q`
- result: passed, `134 passed`.
- command: `git diff --check`
- result: passed.

## Known risks

- The observed stress audit still contains pre-T327 observed row data. It is labeled historical and
  must be refreshed before it is used as current post-T327 behavior for any output-changing work.
- Historical design notes still mention non-66 forms and broader-corpus possibilities. They are
  preserved as history, not current canonical controls.

## Open questions

- Whether a future post-T327 observed behavior audit should be a T327F prerequisite or a separate
  T327E follow-up before boundary-source intake planning.

## Next agent instruction

Claude review next. Merge if approved and green. Then T327F planning only. Do not import or move
boundary texts.
