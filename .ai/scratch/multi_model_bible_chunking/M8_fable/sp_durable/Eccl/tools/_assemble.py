#!/usr/bin/env python3
"""Orchestrator: verify debug-artifact containment, assemble the combined
draft corpus in canonical order, census it. (Phase-2 assembly step.)"""
import collections
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
W = SPBOOK / "writer"

# 1. containment: the stray debug row must exist (same id) in the deliverable
dbg = (W / "_debug_row3.jsonl").read_text(encoding="utf-8").strip()
dbg_id = json.loads(dbg.splitlines()[0])["decision_id"]
p03_ids = [json.loads(l)["decision_id"] for l in (W / "p03_rows.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
assert dbg_id in p03_ids, f"debug row {dbg_id} NOT contained in p03 deliverable — do not delete"
print(f"containment OK: {dbg_id} present in p03_rows.jsonl")

# 2. assemble in canonical order
rows = []
for part in ("p01", "p02", "p03"):
    for l in (W / f"{part}_rows.jsonl").read_text(encoding="utf-8").splitlines():
        if l.strip():
            rows.append(json.loads(l))
combined = SPBOOK / "draft_rows_combined.jsonl"
with combined.open("w", encoding="utf-8", newline="\n") as fh:
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")

# 3. census
ut = collections.Counter(r["unit_type"] for r in rows)
conf = collections.Counter(r["confidence"] for r in rows)
pc = collections.Counter(r["parent_collection"].split()[0] for r in rows)
ids_ok = all(r["decision_id"] == r["writer_decision_id"] for r in rows)
print(json.dumps({"rows": len(rows), "unit_type": dict(ut.most_common()),
                  "confidence": dict(conf.most_common()),
                  "parents": dict(pc), "ids_consistent": ids_ok,
                  "combined": str(combined.name)}, ensure_ascii=False, indent=1))
