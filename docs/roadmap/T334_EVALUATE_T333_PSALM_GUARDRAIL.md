# T334 Evaluate T333 Psalm Guardrail

**Status:** complete
**Date:** 2026-06-09
**Mode:** same-baseline evaluation / reporting

## Purpose

T334 evaluates merged PR #39 / T333 against the post-T327 canonical-66 baseline.
It verifies whether the T333 candidate Psalm skill guardrail changed default
chunking behavior, changed chunk output, moved score, or authorized new Psalm
boundaries.

T334 is evaluation/reporting only. It does not implement new chunking behavior,
does not regenerate chunks, does not change the evaluator, and does not modify
raw or canonical data.

## T333 Post-Merge Verification

PR #39 was verified merged into `main` before T334 started:

- PR #39 state: `MERGED`.
- Merge commit: `ade6f267cf6459ae93fdfabe3e584f3d136279c1`.
- T333 implementation commit present on `main`:
  `3bb9396bdf6fd9c1286cbe77d944bee3b5b53507`.
- `main` fast-forwarded cleanly.
- No merge or rebase state was present.
- GitHub `validate` check for PR #39 was successful.

## T333 Behavior Review

T333 added a reviewed-gold guardrail to the candidate Psalm skill
`psalm-whole-then-stanza-v1`.

Confirmed behavior:

- The skill handles literal Book of Psalms only: `book == "Ps"`.
- The skill rejects non-`Ps` inputs.
- The skill delegates to `pipelines.chunking.chunker.chunk_book(...)` with the
  same arguments the monolith path receives.
- After delegation, the skill validates reviewed Psalm postconditions when the
  reviewed endpoints are present in the input.
- The skill raises `ValueError` if delegated output drifts from reviewed Psalm
  spans.
- Partial inputs that do not include reviewed Psalm endpoints are not forced
  through unrelated reviewed cases.
- `Song` and `Lam` remain non-target canonical poetry controls.
- `PrMan`, `Ps151`, and other non-66 material are not used as canonical controls.

## Evidence Gate

T333 cites reviewed Psalm evidence only:

- `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- `eval/chunking_gold/review_packets/ps78_boundary_review.md`
- `eval/chunking_gold/review_packets/ps105_boundary_review.md`
- `eval/chunking_gold/review_packets/ps106_boundary_review.md`
- `docs/roadmap/T332_SELECT_NARROW_CHUNKING_TARGET.md`

The reviewed cases guarded by T333 are:

- Ps.23 whole-psalm behavior.
- Ps.3 superscription-attached behavior.
- Short Psalm holdouts: Ps.1, Ps.8, Ps.100, and Ps.117.
- Ps.119 exact 22 reviewed acrostic sections.
- Ps.78 approved parent whole-psalm unit with reviewed child chunks
  `Ps.78.1-69`, `Ps.78.70-71`, and `Ps.78.72`.
- Ps.105 whole-psalm behavior.
- Ps.106 whole-psalm behavior, with `b` markers treated as evidence rather than
  automatic split authority.

No proposed stress-atlas entry, characterization-only evidence, marker evidence
alone, weak evaluator upside, or aggregate score movement authorizes behavior
change.

## Same-Baseline Evaluation

Post-T327 canonical-66 baseline:

- Run lineage: D / Claude pass2, post-T327 canonical-66 corpus.
- Chunk count: 1,131.
- Chunk SHA-256:
  `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025`.
- Composite: 93.6 under unchanged T314 evaluator policy.

T334 finding:

- Default chunking behavior changed: no.
- Chunk output changed: no evidence of output change.
- Chunk regeneration performed: no.
- Evaluator formula changed: no.
- Leaderboard or scorecard changed: no.
- Score movement present: no.
- Chunking improvement claimed: no.

The focused orchestrator tests still prove the orchestrated path remains
byte-identical to `chunker.py` on smoke inputs and the real corpus when local
canonical data is present. The T333 candidate-skill tests prove delegated output
passes when reviewed spans match and fails closed when reviewed Ps.78, Ps.106, or
Ps.119 behavior drifts.

## Test Additions

T334 adds small read-only assertions to `tests/test_psalm_candidate_skill.py`:

- The Psalm skill delegates to `chunker.chunk_book(...)` with unchanged argument
  objects.
- Reviewed guardrail spans remain literal `Ps` references and do not reintroduce
  `PrMan` or `Ps151`.
- Skill metadata cites the reviewed Psalm manifest/review packets, keeps
  `handles_books` to `["Ps"]`, keeps `excluded_books` to `["Song", "Lam"]`, and
  records that no quality improvement is claimed.

These tests do not change runtime behavior.

## Methodology Review

Methodology reviewed: no change required - T334 is same-baseline evaluation and
adds no new reusable workflow rule. It follows the existing rules that
behavior-preserving skill seams must avoid output claims, output-changing Psalm
work requires reviewed target evidence, and boundary/source imports remain out
of scope.

## Protected Boundaries

T334 does not change:

- `data/raw/**`
- `data/canonical/**`
- generated canonical outputs
- generated chunk outputs
- `pipelines/chunking/chunker.py`
- `pipelines/chunking/orchestrator.py`
- evaluator formula
- leaderboard or scorecards
- Psalm boundaries
- source imports
- boundary corpus records
- T327G

## Recommendation

Review and merge T334 if CI is green.

If T333 caused no output/default behavior change, the next safe task should be
T335: expand or refresh reviewed Psalm stress/gold coverage before any
behavior-changing Psalm work. Do not start T327G, boundary import, or broad
chunker rewrites.
