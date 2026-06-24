# T399 Focused Bible-Wide Research Queue

## Summary

T399 completes Goal 2 as a non-output-changing focused research queue. It starts from the T398
phase-one whole-corpus synthesis, T386 passage flags, existing dossier queues, source metadata and
original-language policies, contextual reading policy, manuscript/source catalog planning, and the
Orthodox Hermeneutic Firewall.

The machine-readable queue is:

```text
.ai/control/t399_focused_bible_wide_research_queue.yaml
```

T399 does not select a final target, promote reviewed gold, add child spans, implement chunk output,
change routes/evaluators, create graph/retrieval/vector truth, import boundary material, select
preferred readings/source traditions, change canon scope, create source/manuscript rows, or
authorize theology authority.

## What T399 Adds

The queue records:

- 22 ranked candidate lanes/passages across epistle, Gospel/WJ, Acts, Revelation, Torah/covenant,
  wisdom/poetry, prophetic/oracle, textual-variant/source-tradition, and original-language pressure
  lanes.
- A scoring model that distinguishes research priority from review-strengthening safety.
- Per-candidate theological/hermeneutical risks.
- Per-candidate variant/source-tradition dependency or non-dependency status.
- Per-candidate source metadata and original-language phrase/context needs.
- Per-candidate likely owner decisions before promotion or implementation.
- Per-candidate review-only safety status.
- Eight owner-decision prompts for the next human gates.

## Highest Queue Items

The highest review-only candidates are:

1. `1Cor.11.17-1Cor.14.40`
2. `Gal.2.15-Gal.3.29`
3. `Rom.9.1-Rom.11.36`
4. `John.3.1-John.3.36`
5. `Acts.2.1-Acts.2.47`

These are recommendations for owner review, not owner selections.

## Blocked But Important

Some items score high because they are important, not because they are safe to promote:

- `Deut.32.1-Deut.32.43` / `Deut.32.8-Deut.32.9`
- `Dan.7.1-Dan.12.13`
- `Mark.16.9-Mark.16.20`
- `John.7.53-John.8.11`
- `Jer.30.1-Jer.33.26`
- `1John.5.6-1John.5.8`

These remain blocked before any reviewed-gold promotion or implementation until exact
variant/source-tradition case dockets and owner confirmations exist.

## Next Safe Moves

T397 remains the separate Goal 6 route-isolated harness prep for `Eph.1.3-Eph.1.14`.

For Goal 2 follow-up, the owner should choose one T399 owner-decision option before any new
review-packet strengthening PR. The queue recommends `T399-HDM-001-A`
(`1Cor.11.17-1Cor.14.40`) as the next review-only packet if the owner wants to continue the epistle
lane, but that recommendation is not selection.

## Validation

T399 is validated by:

```bash
python scripts/validate_t399_focused_bible_wide_research_queue.py
python -m pytest tests/test_t399_focused_bible_wide_research_queue.py -q
python scripts/validate_all.py
```

## Non-Authorizations

T399 authorizes no target selection, reviewed-gold promotion, child spans, chunk output,
route/evaluator behavior, graph/retrieval/vector truth, boundary import, preferred reading,
source-tradition preference, canon-scope change, source/manuscript rows, whole-Bible output, or
theology authority.
