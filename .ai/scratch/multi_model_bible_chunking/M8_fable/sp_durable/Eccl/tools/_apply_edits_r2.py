#!/usr/bin/env python3
"""Orchestrator: apply phase-2 edit files (replace/retire/add) over rows_v1
-> SP/Eccl/rows_v2.jsonl in canonical span order. Expect 85 -4 +5 = 86 rows."""
import json
import re
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
rows = [json.loads(l) for l in (SPBOOK / "rows_v1.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
by_id = {r["writer_decision_id"]: r for r in rows}

ops = {"replace": 0, "retire": 0, "add": 0}
adds = []
for name in ("p02_edits_r2.jsonl", "p03_edits_r2.jsonl"):
    for l in (SPBOOK / "author" / name).read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        e = json.loads(l)
        op = e.pop("_op")
        ops[op] += 1
        if op == "retire":
            wid = e["writer_decision_id"]
            assert wid in by_id, f"retire targets unknown row {wid}"
            del by_id[wid]
        elif op == "replace":
            wid = e["writer_decision_id"]
            assert wid in by_id, f"replace targets unknown row {wid}"
            missing = set(by_id[wid].keys()) - set(e.keys())
            assert not missing, f"{wid} replacement drops fields: {missing}"
            by_id[wid] = e
        elif op == "add":
            wid = e["writer_decision_id"]
            assert wid not in by_id, f"add collides with existing id {wid}"
            assert len(e.keys()) >= 20, f"add {wid} looks schema-incomplete ({len(e)} fields)"
            by_id[wid] = e
            adds.append(wid)

SPAN = re.compile(r"^Eccl\.(\d+)\.(\d+)-Eccl\.(\d+)\.(\d+)$")
def spankey(r):
    m = SPAN.match(r["span"])
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))

final = sorted(by_id.values(), key=spankey)
for i, r in enumerate(final, 1):
    r["chunk_index_in_book"] = i
out = SPBOOK / "rows_v2.jsonl"
with out.open("w", encoding="utf-8", newline="\n") as fh:
    for r in final:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print(json.dumps({"rows_v1": len(rows), "ops": ops, "rows_v2": len(final),
                  "added_ids": adds, "out": out.name}, indent=1))
