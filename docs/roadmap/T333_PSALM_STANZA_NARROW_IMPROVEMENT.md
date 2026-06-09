# T333 Psalm Stanza Narrow Improvement

**Status:** implemented on branch `t333-psalm-stanza-narrow-improvement`
**Date:** 2026-06-09
**Mode:** narrow implementation with reviewed-gold guardrail

## Purpose

T333 implements one narrow Psalm / poetry stanza improvement selected by T332:
the candidate Psalm skill now fails closed when the delegated monolith Psalm
output violates already reviewed Psalm gold.

This is not a broad Psalm rewrite. It does not introduce new Psalm boundaries,
regenerate chunks, retune the evaluator, change scorecards, or claim aggregate
score movement.

## Evidence Gate

T333 cites only reviewed Psalm evidence:

- `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- `eval/chunking_gold/review_packets/ps78_boundary_review.md`
- `eval/chunking_gold/review_packets/ps105_boundary_review.md`
- `eval/chunking_gold/review_packets/ps106_boundary_review.md`
- `docs/roadmap/T332_SELECT_NARROW_CHUNKING_TARGET.md`

The reviewed cases are:

- Ps.23 remains one whole-psalm chunk.
- Ps.3 superscription remains attached with no orphan title chunk.
- Ps.1, Ps.8, Ps.100, and Ps.117 remain one chunk each.
- Ps.119 remains exactly 22 reviewed acrostic sections.
- Ps.78 remains the approved parent whole-psalm unit with child chunks
  `Ps.78.1-69`, `Ps.78.70-71`, and `Ps.78.72`.
- Ps.105 remains a reviewed whole-psalm chunk.
- Ps.106 remains a reviewed whole-psalm chunk; `b` markers are evidence, not
  automatic split authority.

No proposed stress-atlas entry, characterization-only evidence, marker evidence
alone, weak evaluator upside, or aggregate score movement authorizes T333.

## Implemented Behavior

The candidate skill `psalm-whole-then-stanza-v1` still delegates to
`chunker.chunk_book(...)` with the same arguments and returns the same chunks.
After delegation, it validates exact reviewed Psalm spans when reviewed chapters
are present in the returned output.

If delegated output drifts from reviewed Psalm gold, the skill raises a
`ValueError` naming the reviewed case and observed spans. Partial Psalm inputs
that do not include reviewed chapters are not forced through unrelated reviewed
cases.

## Same-Baseline Scope

Expected chunk output remains the post-T327 canonical-66 baseline:

- D / Claude pass2 composite: 93.6 under unchanged T314 evaluator policy.
- Chunk SHA-256:
  `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025`.

Any score movement would require separate proof. T333 itself makes no chunking
improvement claim.

## Files

Implementation:

- `pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/algorithm.py`
- `pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/SKILL.md`
- `pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/SKILL_METADATA.json`

Tests:

- `tests/test_psalm_candidate_skill.py`

Control surfaces:

- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/roadmap_events.jsonl`
- `.ai/control/handoff_ledger.jsonl`
- `.ai/tasks/T333.task.yaml`
- `.ai/handoffs/T333/handoff.md`
- `ROADMAP_STATE.yaml`

## Protected Boundaries

T333 does not change:

- `data/raw/**`
- `data/canonical/**`
- generated canonical outputs
- committed chunk outputs
- `pipelines/chunking/chunker.py`
- `pipelines/chunking/orchestrator.py`
- evaluator formula
- leaderboard or scorecards
- boundary repo material
- source text import
- T327G

## T333 Stop Conditions

Stop rather than implement if a future change would:

- split Ps.105 or Ps.106 without a new explicit human-reviewed decision;
- merge Ps.78 to chase the fragmentation metric;
- alter Psalm 119 sectioning;
- use `\b`, `\wj`, `\qs`, punctuation, or other markers as automatic boundary
  authority;
- rely on aggregate score movement rather than reviewed target-form evidence;
- broaden from literal Psalms into Song, Lamentations, boundary texts, or all
  poetry.

## Next Task

After PR merge, the next safe lane is human review of a specific Psalm/stanza
packet or a separately scoped T334/T335 planning task. Do not start T327G,
boundary import, or broad chunking rewrites.
