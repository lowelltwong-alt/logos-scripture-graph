# Task Handoff

## Task

- task_id: T344R
- title: Revelation Research Prep After Owner Decision E
- phase: phase_4
- status: planned

## Agent

- agent_name: codex
- mode: plan
- stage: seed
- updated_at: 2026-06-17T21:55:00+00:00
- handoff_id: t344r-seed

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- docs/roadmap/T344_REVELATION_OWNER_SELECTION_DOCKET.md
- eval/chunking_gold/review_packets/rev12_14_symbolic_scenes_review.md
- .ai/control/bible_chunking_readiness_map.yaml
- .ai/control/chunking_theological_decision_register.yaml
- .ai/control/chunking_agent_preflight.yaml
- .ai/control/harness_upgrade_roadmap.yaml

## Files changed

- None yet; this handoff seeds the planned task created by the T344 owner decision update.

## Decisions made

- Lowell Wong selected `REV-T344-E` on 2026-06-17.
- Revelation may continue as research/prep only.
- Non-output-changing harnesses, review packets, and lane prep are authorized.
- Revelation implementation, reviewed-gold promotion, output change, graph/vector/index work, boundary import, and generated chunk regeneration remain unauthorized.
- Epistle argument boundaries are the next review lane after Revelation research prep.

## Validation run

- command: not run for this planned seed handoff
- result: validation belongs to the PR that created the task shell
- failures: none known

## Known risks

- Revelation research/prep can be mistaken for reviewed gold or implementation authority.
- Cross-references, Greek lexical rarity, source metadata, speaker shifts, and repeated structures can become hidden authority if not kept evidence-only.
- A Revelation-specific observation could leak into epistle, prophecy, Gospel discourse, or Bible-wide behavior.

## Open questions

- Which exact additional Revelation research/prep packet should be created first?
- What evidence threshold should later count as strong enough to reconsider `REV-T344-B` or `REV-T344-C`?
- Which epistle argument case should be selected first after Revelation research prep: `Eph.1.3-Eph.1.14`, `Rom.9-Rom.11`, `Heb.7-Heb.10`, or `1Cor.8-1Cor.10`?

## Next agent instruction

Start from `AI_FRONT_DOOR.md`, read the T344 owner decision box, and keep work non-output-changing. Continue Revelation research/prep only: review packets, metadata/allusion prep, harnesses, and lane planning. Do not start T345 implementation or touch chunker/generated output/evaluator surfaces. After Revelation prep, move to epistle argument boundary review packets as the next review lane.
