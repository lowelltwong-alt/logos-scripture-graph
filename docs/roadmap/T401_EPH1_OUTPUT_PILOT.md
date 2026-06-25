---
object_type: roadmap_report
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-25 during T401 after Lowell authorized the exact Eph.1.3-Eph.1.14 parent-only output-changing pilot."
reason_for_inclusion: "Give future agents and no-context auditors a readable summary of the exact output change, route-isolation proof, same-baseline results, non-authorizations, and next post-pilot review gate."
---

# T401 Eph.1.3-Eph.1.14 Output Pilot

## Summary

T401 implements the owner-authorized Goal 7 pilot for `Eph.1.3-Eph.1.14` only.

The machine-readable manifest is:

```text
.ai/control/t401_eph1_output_pilot_manifest.yaml
```

The output change appends one additive, parent-only, non-truth-bearing overlay:

```text
chunk--eng-web--chunk-policy-v0.1.0--epistles-parent-overlay--Eph.1.3--Eph.1.14--T401-EPH1-PILOT
```

T401 preserves all pre-T401 baseline records byte-identical as the candidate prefix. It does not
delete or replace existing chunks, add child spans, broaden epistle behavior, change evaluator
formulas, generate graph/retrieval/vector truth, import boundaries, select preferred readings or
source traditions, change canon scope, create source/manuscript rows, or authorize theology authority.

## Proof

- Baseline: 1137 chunks; sha256 `681a0840edd8513daeb204579ed0a1b0b0f818c910abfc83a7890317c3b481e7`.
- Candidate: 1138 chunks; sha256 `6b0f0210ac6a31090b5ceb42d104278e8d93fc53be098535f231b04b8fcab6f7`.
- Preserved baseline prefix sha256: `681a0840edd8513daeb204579ed0a1b0b0f818c910abfc83a7890317c3b481e7`.
- Route-isolation changed keys: none.
- Route-isolation added key: the single T401 overlay ID above.
- Route-isolation changed span: `Eph.1.3-Eph.1.14`.
- Child spans authorized: false.

## Validation

```bash
python scripts/validate_t401_eph1_output_pilot.py
python -m pytest tests/test_t401_eph1_output_pilot.py tests/test_chunking_orchestrator.py -q
python scripts/validate_all.py
python -m pytest -q
```

## Next Gate

The next safe step is a post-pilot review for `Eph.1.3-Eph.1.14`: review the same-baseline output,
no-context audit findings, and whether child spans are necessary. That review must not add child
spans, graph/retrieval/vector truth, evaluator changes, preferred readings, source-tradition
preference, boundary imports, broader epistle generalization, whole-Bible output, source/manuscript
rows, canon-scope change, or theology authority without a later exact owner gate.
