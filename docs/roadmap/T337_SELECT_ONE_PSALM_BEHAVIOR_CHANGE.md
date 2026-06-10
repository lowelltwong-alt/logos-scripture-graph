# T337 Select One Psalm Behavior Change

**Date:** 2026-06-09
**Task type:** selection/control-plane only
**Status:** complete

## Decision

T337 does not authorize an output-changing Psalm implementation target.

No reviewed-gold-supported Psalm behavior-change target is available in the current repo state. The reviewed Psalm evidence currently approves preservation of known behavior or exact existing structural splits. The pending Psalm stress cases remain characterization-only and cannot be promoted into implementation authority by T337.

The next implementation task, T338, must not start until a follow-up human review promotes exactly one Psalm target with exact expected spans, executable checks, and explicit output-change authorization.

## Scope Boundary

T337 is selection/planning/control-plane work only.

T337 did not:

- change chunking behavior;
- implement new Psalm boundaries;
- regenerate chunks or generated outputs;
- change evaluator formulas;
- change leaderboard or scorecards;
- edit chunker, evaluator, or orchestrator code;
- mutate `data/raw/**` or `data/canonical/**`;
- import source texts or boundary texts;
- start T327G;
- start Revelation implementation.

No chunking improvement claim or score movement is made.

## Evidence Reviewed

T337 used only existing reviewed-gold and pending-review surfaces:

- `docs/roadmap/T332_SELECT_NARROW_CHUNKING_TARGET.md`
- `docs/roadmap/T335_REVIEWED_PSALM_STRESS_GOLD_EXPANSION.md`
- `docs/roadmap/T336_OPTIMIZED_WHOLE_BIBLE_CHUNKING_ROADMAP.md`
- `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- `eval/chunking_gold/per_form/psalms_gold_plan.md`
- `eval/chunking_gold/review_packets/ps78_boundary_review.md`
- `eval/chunking_gold/review_packets/ps105_boundary_review.md`
- `eval/chunking_gold/review_packets/ps106_boundary_review.md`
- `eval/chunking_gold/review_packets/ps89_boundary_review.md`
- `eval/chunking_gold/review_packets/ps136_boundary_review.md`
- `pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/SKILL_METADATA.json`
- `pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/algorithm.py`
- `tests/test_psalm_candidate_skill.py`

## Candidate Review

| Candidate | Evidence status | Current decision | T337 result |
| --- | --- | --- | --- |
| Psalm 78 parent/child structural split | Reviewed gold | Preserve current parent whole-Psalm with child spans `Ps.78.1-69`, `Ps.78.70-71`, `Ps.78.72` | Not an output-changing target; merging would contradict reviewed gold and metric-chase. |
| Psalm 105 whole-Psalm preservation | Reviewed gold | Preserve `Ps.105.1-45` as one chunk | Not an output-changing target; child chunks require new human review. |
| Psalm 106 whole-Psalm preservation with `b` marker note | Reviewed gold | Preserve `Ps.106.1-48` as one chunk; `b` markers are evidence only | Not an output-changing target; child chunks require new human review. |
| Psalm 119 acrostic sections | Reviewed gold | Preserve exact 22-section behavior | Not an output-changing target; already a guardrail/preservation case. |
| Short Psalm and superscription holdouts | Reviewed gold | Preserve known whole-Psalm behavior | Not an output-changing target; already a guardrail/preservation case. |
| Psalm 89 royal lament | Pending human review only | Characterization-only; output change not authorized | Not authorized. |
| Psalm 136 refrain litany | Pending human review only | Characterization-only; output change not authorized | Not authorized. |

## Selected Target

No Psalm behavior-changing implementation target is selected.

This is an intentional selection result, not a deferral by convenience. Selecting any current candidate as behavior-changing work would either:

- contradict reviewed gold that says preserve the current behavior;
- rely on marker evidence without human boundary review;
- promote pending characterization-only material;
- or convert a guardrail/preservation seam into implementation authorization.

## T338 Gate

T338 is blocked until a T335-style follow-up or equivalent human review promotes exactly one Psalm target with:

- exact expected spans;
- executable reviewed-gold checks;
- explicit `implementation_allowed: true`;
- explicit `output_change_authorized: true`;
- non-target identity preservation requirements;
- risk review for accidental global leakage or metric chasing.

If a future implementation changes behavior, it must preserve non-target byte identity or explain every diff as a reviewed-gold-authorized change.

## RISK-GATE-001 Map

Required question: What could this change accidentally authorize, weaken, contaminate, overfit, globalize, or make harder to reverse?

### Confirmed Risks

- Forcing a Psalm target now would promote pending or preservation-only evidence into behavior-change authority.
- Treating `\qs`, `\b`, Selah, refrain, or acrostic evidence as automatic boundary authority would weaken the reviewed-gold gate.
- Merging Psalm 78 for score movement would contradict the reviewed structural-split decision.

### Plausible Risks

- A future Psalm-specific rule could leak into non-Psalm poetry if route and skill isolation are weakened.
- A future master chunker could tune toward non-Bible or aggregate objectives and degrade canonical Bible behavior.
- T338 could be mistaken as already authorized because T337 exists in the implementation lane.

### Unlikely But High-Impact Risks

- Pending Psalm evidence could be generalized into Gospel discourse, Revelation, or prophecy without reviewed-gold support.
- Boundary or noncanonical source material could be imported as supposed supporting evidence for canonical Psalm boundaries.

### Watch-Later Conditions

- Any PR that edits chunker, orchestrator, evaluator, leaderboard, scorecards, generated chunks, or canonical data while claiming to continue T337.
- Any PR that names Ps89 or Ps136 as implementation targets before human review promotes exact spans.
- Any global poetry heuristic or master-chunker objective that is not isolated to the selected route.

### Tests Or Guards Needed

- Deterministic policy tests should keep T337 selection wording locked as no current output-changing target authorized.
- Future T338 tests must assert reviewed target spans and non-target identity preservation.
- Future implementation tests must fail closed if pending-only evidence is promoted.

### Owner Decisions Needed

- Human review must choose whether Ps89, Ps136, or another Psalm case receives exact reviewed-gold spans.
- Owner or reviewer must explicitly authorize any output-changing Psalm implementation before T338.
- Claude risk review is recommended before any future Psalm behavior-changing implementation PR.

## Next Recommendation

Create a T335 follow-up review task to promote exactly one Psalm behavior target, likely from pending Psalm evidence or a new reviewed packet, before any T338 implementation. Continue the Psalm lane only after that review. Do not start Revelation implementation, T327G, or boundary import.
