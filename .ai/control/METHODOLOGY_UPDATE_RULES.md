# Methodology Update Rules

This control-plane rule forces future chunking-related work to keep the living methodology current.

## Required Methodology Artifact

- `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md`

## Forced Update Rule

Any PR or patch touching the following paths must update or explicitly review the Chunking Skill
Supply Chain methodology:

- `pipelines/chunking/`
- `pipelines/chunking/skills/`
- `registry/chunking/`
- `config/chunking/`
- `eval/`
- `tests/*chunk*`
- `.ai/handoffs/T310/`
- `.ai/handoffs/T311/`

A patch is incomplete until one of these is true:

- the methodology artifact was updated, or
- the handoff records why no methodology update was needed.

## Evaluator Sanity Rule

Before any score-moving chunking skill PR, the agent must verify that the evaluator is not measuring
a confounded proxy. If the evaluator is wrong, the evaluator fix must land in a separate PR before
the skill PR claims improvement.

Corrected evaluator score movement must be described as evaluator-surface correction, not as
chunk-output improvement. T311 is the reference case: unchanged D / Claude pass2 output moved from
88.5 to 93.0 after `psalms_fragmented` stopped grouping Psalm-like chunks by bare chapter number.

## Branch Hygiene Rule

Keep evaluator fixes, skill changes, and methodology updates in separate branches/PRs unless the task
explicitly requires a combined patch.

## Required PR Note

Every chunking-related PR must include one of:

- `Methodology updated: yes`
- `Methodology reviewed: no change required - <rationale>`

Score-moving chunking PRs must also state whether evaluator sanity was checked and whether any score
movement reflects output improvement or evaluator-surface correction.

## Handoff Note

Chunking-related handoffs must record the methodology decision under `Decisions made` or the task's
increment-specific section. Use the exact PR note wording when possible so reviewers can find it.

## Related Workflow

- `.ai/workflows/chunking-skill-supply-chain.workflow.md`
- `pipelines/chunking/skills/SKILL_CREATION_PLAYBOOK.md`
