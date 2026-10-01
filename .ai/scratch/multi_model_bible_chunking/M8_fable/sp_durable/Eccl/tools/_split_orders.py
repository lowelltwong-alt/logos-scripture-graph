#!/usr/bin/env python3
"""Orchestrator: split author phase-1 orders into per-part order files under
SP/Eccl/author/ for the three author agents."""
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
w = json.loads((SPBOOK / "work_orders.json").read_text(encoding="utf-8"))
outdir = SPBOOK / "author"
outdir.mkdir(exist_ok=True)
counts = {}
for part in ("p01", "p02", "p03"):
    orders = [o for o in w["author_phase1_orders"]
              if (o.get("row_id") or "").lower().startswith(part)]
    (outdir / f"{part}_orders.json").write_text(
        json.dumps({"part": part, "orders": orders, "count": len(orders),
                    "note": "phase-1 ordinary cures; boss-pending rows excluded"},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    counts[part] = len(orders)
print(json.dumps({"written": counts, "total": sum(counts.values())}, indent=1))
