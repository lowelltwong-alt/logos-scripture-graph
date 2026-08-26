#!/usr/bin/env python3
"""Orchestrator: apply phase-2 (boss-consequence) edit files over rows_v1 ->
SP/Song/rows_v2.jsonl. Handles _op replace/retire/add; verifies targets
exist, no duplicate ops per row, retires match the boss-dissolved set
exactly, respans match the boss ledger span specs, and no field is dropped
on replace."""
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
EXPECT_RETIRE = {"P02-007", "P02-015", "P02-017"}
EXPECT_RESPAN = {"P02-006": "Song.6.4-Song.6.10",
                 "P02-018": "Song.8.5-Song.8.7",
                 "P02-014": "Song.7.11-Song.8.3",
                 "P02-013": "Song.7.10-Song.7.10"}

rows = [json.loads(l) for l in (SPBOOK / "rows_v1.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
by_id = {r["writer_decision_id"]: i for i, r in enumerate(rows)}

seen = set()
retired = set()
added = []
ops = {"replace": 0, "retire": 0, "add": 0}
for name in ("p01_edits_r2.jsonl", "p02_edits_r2.jsonl"):
    f = SPBOOK / "author" / name
    for l in f.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        e = json.loads(l)
        op = e.pop("_op")
        ops[op] += 1
        wid = e["writer_decision_id"]
        assert wid not in seen, f"duplicate op for {wid}"
        seen.add(wid)
        if op == "retire":
            assert wid in EXPECT_RETIRE, f"unexpected retire {wid}"
            assert wid in by_id, f"retire targets unknown row {wid}"
            retired.add(wid)
        elif op == "replace":
            assert wid in by_id, f"replace targets unknown row {wid}"
            if wid in EXPECT_RESPAN:
                assert e["span"] == EXPECT_RESPAN[wid], \
                    f"{wid} span {e['span']!r} != boss spec {EXPECT_RESPAN[wid]!r}"
            missing = set(rows[by_id[wid]].keys()) - set(e.keys())
            assert not missing, f"{wid} replacement drops fields: {missing}"
            rows[by_id[wid]] = e
        elif op == "add":
            added.append(e)
        else:
            raise AssertionError(f"unknown op {op}")

assert retired == EXPECT_RETIRE, f"retire set mismatch: got {sorted(retired)}"
out_rows = [r for r in rows if r["writer_decision_id"] not in retired] + added
out = SPBOOK / "rows_v2.jsonl"
with out.open("w", encoding="utf-8", newline="\n") as fh:
    for r in out_rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print(json.dumps({"rows_in": len(rows), "rows_out": len(out_rows), "ops": ops,
                  "retired": sorted(retired), "added": len(added),
                  "out": out.name}, indent=1))
