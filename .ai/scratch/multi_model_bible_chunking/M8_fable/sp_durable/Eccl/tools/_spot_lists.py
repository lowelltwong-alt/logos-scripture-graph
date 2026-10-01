#!/usr/bin/env python3
"""Orchestrator: derive repaired-row and untouched-row lists for the spot wave."""
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
def ids(fname, want_ops=("replace",)):
    out = []
    for l in (SPBOOK / "author" / fname).read_text(encoding="utf-8").splitlines():
        if l.strip():
            e = json.loads(l)
            if e.get("_op") in want_ops:
                out.append(e["writer_decision_id"])
    return out

p1 = {f: ids(f) for f in ("p01_edits.jsonl", "p02_edits.jsonl", "p03_edits.jsonl")}
p2r = {f: ids(f) for f in ("p02_edits_r2.jsonl", "p03_edits_r2.jsonl")}
p2a = {f: ids(f, ("add",)) for f in ("p02_edits_r2.jsonl", "p03_edits_r2.jsonl")}
retired = {f: ids(f, ("retire",)) for f in ("p02_edits_r2.jsonl", "p03_edits_r2.jsonl")}

v2 = [json.loads(l)["writer_decision_id"] for l in (SPBOOK / "rows_v2.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
touched = set(sum(p1.values(), [])) | set(sum(p2r.values(), [])) | set(sum(p2a.values(), []))
untouched = [w for w in v2 if w not in touched]
print(json.dumps({
    "phase1_replaced": {k: sorted(v) for k, v in p1.items()},
    "phase2_replaced": p2r, "phase2_added": p2a, "retired": retired,
    "untouched_in_v2": untouched, "untouched_count": len(untouched),
    "rows_v2_total": len(v2)}, indent=1))
