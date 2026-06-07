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

Gold-related PRs must also state whether each cited artifact is scaffold/plan, executable reviewed
gold, characterization-only evidence, pending human review, or approved structural split under a
parent whole unit.

## Per-Form Gold Rule

Before any output-changing chunking skill work, the PR or handoff must cite a per-form gold file or
manifest under `eval/chunking_gold/`.

- A planning scaffold is enough to start analysis.
- Characterization-only evidence is enough to describe current behavior and risk.
- Neither scaffold nor characterization-only evidence is promoted expected output.
- Output-changing skill work requires executable/reviewed gold first.
- Promotion requires reviewed target-form output evidence and non-target controls.
- Weak evaluator levers, such as Ps.78's +0.5 composite upside, must not drive implementation
  without target-form evidence.
- Human-gated boundary decisions must remain `pending_human_review` until explicitly reviewed.
- Reviewed parent whole-unit plus child structural chunks are not bad fragmentation by default.
- Psalm 119 is the strong precedent; Psalm 78 is now a reviewed lighter case.
- Similar future cases must be reviewed through gold before evaluator or chunker changes.
- Evaluator policy may exclude reviewed structural splits from final bad-fragmentation scoring only
  when raw diagnostics remain visible and observed boundaries exactly match reviewed gold.
- Per-form gold manifests must pass semantic maturity validation before they are cited for
  output-changing work. Reviewed cases need explicit statuses; characterization-only and
  pending-human-review cases must not carry promoted-output flags; approved parent/child structural
  split cases need parent and child boundaries.
- Stress atlas cases are proposed candidates only. They do not authorize output-changing work,
  evaluator changes, or skill promotion until converted into reviewed gold, characterization-only
  evidence, or an explicit pending-human-review packet.

## Handoff Note

Chunking-related handoffs must record the methodology decision under `Decisions made` or the task's
increment-specific section. Use the exact PR note wording when possible so reviewers can find it.
For gold-related work, handoffs must also record whether target evidence is reviewed gold,
characterization-only, pending human review, or reviewed parent/child structural split.

## Related Workflow

- `.ai/workflows/chunking-skill-supply-chain.workflow.md`
- `pipelines/chunking/skills/SKILL_CREATION_PLAYBOOK.md`
