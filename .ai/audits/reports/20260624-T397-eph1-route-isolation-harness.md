# T397 No-Context Audit Surface

## Scope

Audit `.ai/control/t397_eph1_route_isolation_harness.yaml` and
`scripts/chunking/route_isolation_harness.py` as the Goal 6 non-output-changing route-isolation
harness prep for `Eph.1.3-Eph.1.14`.

## Claims To Verify

- T397 depends on the T394 parent-only reviewed-gold promotion for `Eph.1.3-Eph.1.14`.
- The harness compares baseline and candidate chunk JSONL files without generating chunks.
- The harness proves non-target byte identity.
- The harness fails on non-target edits, adjacent spillover, unauthorized child subspans, and
  child-span payloads while child spans are not authorized.
- T397 records CD-074 and LSN-028 for downstream audit.
- T397 authorizes no parent span as chunk boundary, child spans, chunk output, implementation,
  route/evaluator behavior, graph/retrieval/vector truth, boundary import, preferred reading,
  source-tradition preference, canon-scope change, source/manuscript rows, whole-Bible output, or
  theology authority.

## Required Commands

```bash
python scripts/validate_t397_eph1_route_isolation_harness.py
python -m pytest tests/test_t397_eph1_route_isolation_harness.py tests/test_route_isolation_harness.py -q
python scripts/validate_all.py
```

## Audit Notes

The harness proves output-diff shape only. It does not authorize a future output pilot, and it does
not make the parent span a chunk boundary until a separate owner output authorization says so.
