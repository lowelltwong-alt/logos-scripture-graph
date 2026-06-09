# T335 Reviewed Psalm Stress Gold Expansion

**Status:** complete
**Date:** 2026-06-09
**Mode:** evidence/gold/stress expansion

## Purpose

T335 expands Psalm stress/gold coverage after T333 added the safe Psalm candidate-skill guardrail
and T334 confirmed that T333 caused no output/default behavior change or score movement.

This task is evidence-only. It does not change chunking behavior, regenerate chunks, change the
evaluator, promote a skill, or claim chunking improvement.

## T334 Post-Merge Verification

PR #40 / T334 was verified merged before T335 started:

- PR #40 state: `MERGED`.
- Merge commit: `4f9ce2f0ca6e7c8d53f3ea16af8bfbf94388195a`.
- T334 implementation commit present on `main`:
  `a748cf3a5d7ab78f9df860980eec57b38bb1f507`.
- GitHub `validate` check for PR #40 succeeded.
- `main` fast-forwarded cleanly.
- No merge or rebase state was present.

## Current Psalm Evidence State

Reviewed Psalm coverage before T335:

- Ps.23 whole-psalm hard gate.
- Ps.3 superscription attached with no orphan title chunk.
- Short Psalm holdouts: Ps.1, Ps.8, Ps.100, and Ps.117.
- Ps.119 reviewed 22-section acrostic parent/child precedent.
- Ps.78 approved parent whole-psalm unit with reviewed child chunks.
- Ps.105 reviewed whole-psalm preservation.
- Ps.106 reviewed whole-psalm preservation; `b` markers remain evidence only.
- Canonical non-target controls: Song and Lam.

Known gap:

- The repo still lacks reviewed Psalm stress coverage for a next behavior-changing target beyond
  the already settled Ps.78/Ps.105/Ps.106/Ps.119 cases.
- Selah / `\qs`, refrain/litany form, and additional long-Psalm parent/child candidates need
  review before they can authorize output-changing work.

## Cases Added

T335 adds two Psalm-only pending review packets and manifest characterization entries:

| Case | Category | Status | Why added |
| --- | --- | --- | --- |
| Ps.89 | Long royal/lament Psalm with Selah / `\qs`, `b`, and poetic-line evidence | `pending_human_review` / characterization-only | Tests whether a long Psalm with covenant/lament turns should stay whole or become a reviewed parent/child structural split. |
| Ps.136 | Refrain-driven litany Psalm | `pending_human_review` / characterization-only | Tests whether repeated refrain form should preserve whole-psalm unity or support exact child spans after review. |

Both cases are added as non-authorizing evidence. They are not reviewed gold and not approved
expected output.

## Updated Surfaces

Review packets:

- `eval/chunking_gold/review_packets/ps89_boundary_review.md`
- `eval/chunking_gold/review_packets/ps136_boundary_review.md`

Manifest and planning surfaces:

- `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- `eval/chunking_gold/per_form/psalms_gold_plan.md`
- `eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md`

Stress/index surfaces:

- `eval/chunking_gold/stress_atlas/observed_stress_behavior.json`
- `eval/chunking_gold/stress_atlas/OBSERVED_STRESS_BEHAVIOR.md`
- `eval/chunking_gold/review_packets/review_packet_index.json`
- `eval/chunking_gold/review_packets/REVIEW_PACKET_INDEX.md`

Tests:

- `tests/test_stress_review_packets.py`
- `tests/test_observed_stress_behavior.py`
- `tests/test_validate_chunking_gold.py`

## Authorization Status

T335 authorizes no behavior-changing work by itself.

Future output-changing Psalm work remains blocked until a human reviewer promotes a specific case
to reviewed gold or an approved parent/child structural split with exact expected spans and tests.

T335 does make the next selection step clearer:

- T336 may select exactly one Psalm behavior-change target only if reviewed gold or an explicit
  human-reviewed packet authorizes it.
- If no human review is available, T336 should remain planning/review only.

## Future Hard-Book Atlas Lane

Revelation is likely harder than Psalms interpretively because apocalyptic vision cycles, embedded
oracles, symbolic scenes, speaker shifts, and source/tradition questions can make chunk boundaries
carry theological and literary assumptions.

Revelation should receive a future hard-book stress atlas and review-packet lane after the Psalm
lane proves the workflow. This note does not create T340 files, start Revelation implementation,
authorize Revelation chunking behavior, or add Revelation expected output.

Any future Revelation-specific behavior must be routed to an apocalypse/Revelation skill or review
lane and must not leak globally into Psalms, poetry, prophecy, Gospel discourse, epistles, or the
monolith fallback. Revelation chunking must not be implemented until reviewed gold exists.

## Non-Authorizing Rules Preserved

- `\qs`, `\b`, `q1`, `q2`, and repeated refrain form are evidence, not automatic boundary
  authority.
- Current containment in one chunk is not automatically approved preservation.
- Current splitting is not automatically bad fragmentation.
- Stress-atlas and observed-audit evidence remain diagnostic until reviewed.
- Pending review packets do not authorize output-changing work.
- Non-66 material such as `PrMan` and `Ps151` is not reintroduced as canonical control.

## Protected Boundaries

T335 does not change:

- `data/raw/**`
- `data/canonical/**`
- generated canonical outputs
- generated chunk outputs
- `pipelines/chunking/chunker.py`
- `pipelines/chunking/orchestrator.py`
- evaluator formula
- leaderboard or scorecards
- chunk output
- source imports
- boundary corpus records
- T327G

## Methodology Review

Methodology reviewed: no change required - T335 applies existing rules for stress-atlas cases,
pending review packets, marker evidence, reviewed gold before output change, and non-authorizing
review queues. It adds no new reusable workflow rule.

## Recommendation

Review and merge T335 if validation is green. If the meaning of the new Psalm review packets is
considered material, use Claude Opus high for review.

Next safe task:

- T336 should select one Psalm behavior change only if reviewed gold authorizes it.
- Otherwise T336 should remain a review/planning task.
- A later Revelation hard-book atlas/review-packet lane should be created only as a separate future
  task, with no implementation until reviewed gold exists.

T336 later refines this into an optimized whole-Bible roadmap: Psalms remain the current
implementation lane, Revelation becomes an early hard-book atlas/review lane, and all future
book-specific skills must remain route-isolated.

Do not start T327G, boundary import, source acquisition, broad chunker rewrites, Revelation
implementation, or new Psalm boundaries from T335 alone.
