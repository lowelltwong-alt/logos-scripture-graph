# T397 Eph.1.3-Eph.1.14 Route-Isolation Harness

## Summary

T397 completes Goal 6 as non-output-changing harness prep for the already promoted
parent-only reviewed-gold target `Eph.1.3-Eph.1.14`.

The machine-readable record is:

```text
.ai/control/t397_eph1_route_isolation_harness.yaml
```

The executable harness is:

```text
scripts/chunking/route_isolation_harness.py
```

T397 does not implement chunk output, activate route behavior, add child spans, change evaluator
behavior, create graph/retrieval/vector truth, import boundary material, select preferred readings
or source traditions, create source/manuscript rows, or authorize theology authority.

## What The Harness Proves

The harness compares baseline and candidate chunk JSONL files and fails unless:

- all non-target records remain byte-identical;
- any changed/added/removed record is limited to the exact `Eph.1.3-Eph.1.14` target shape;
- child/subspan records fail while child spans are unauthorized;
- adjacent spillover beyond `Eph.1.3-Eph.1.14` fails;
- the report records counts, sha256s, changed keys, changed spans, and non-target identity status.

## Next Gate

The next output-changing step is still blocked. A future pilot requires explicit owner authorization
for the exact Eph.1.3-Eph.1.14 output change, confirmation that the parent span may be used as a
chunk boundary for that exact pilot, current reviewed-gold status, route-isolation proof on real
baseline/candidate outputs, same-baseline evaluation, no-context audit, decision-register update,
and task scope that explicitly allows output paths.

## Validation

T397 is validated by:

```bash
python scripts/validate_t397_eph1_route_isolation_harness.py
python -m pytest tests/test_t397_eph1_route_isolation_harness.py tests/test_route_isolation_harness.py -q
python scripts/validate_all.py
```

## Non-Authorizations

T397 authorizes no parent span as chunk boundary, child spans, reviewed-gold promotion, chunk
output, implementation, route/evaluator behavior, graph/retrieval/vector truth, boundary import,
preferred reading, source-tradition preference, canon-scope change, source/manuscript rows,
whole-Bible output, or theology authority.
