#!/usr/bin/env python3
"""Orchestrator triage patch: reclassify boundary-flavored candidates.
True boss items (adoption/standard required): p02-013, p02-014 (ch-7 cluster
either/ors), P03-023+P03-024 (11:1-6 merger question), and the cross-cluster
skeleton-tier cohesion standard. Everything else is an ordinary cure ->
author roster. Boss-pending rows are excluded from author phase 1."""
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
p = SPBOOK / "work_orders.json"
w = json.loads(p.read_text(encoding="utf-8"))

BOSS_ROWS = {"p02-013", "p02-014", "P03-023", "P03-024"}
keep_boss = []
for d in w["boss_docket"]:
    if d.get("docket_class") == "cross_cluster_policy" or d.get("row_id") in BOSS_ROWS:
        keep_boss.append(d)
    else:
        d["docket_class"] = "ordinary_cure_reclassified"
        w["author_orders"].append(d)
w["boss_docket"] = keep_boss
w["boss_pending_rows"] = sorted(BOSS_ROWS)
w["author_phase1_orders"] = [o for o in w["author_orders"] if o.get("row_id") not in BOSS_ROWS]
w["triage_note"] = ("Orchestrator triage 2026-08-19: 18 boundary-flavored candidates were "
                    "ordinary cures (disclosure/re-tiering/gloss re-cut/rival strengthening) "
                    "and moved to the author roster; 5 true boss items remain (2 ch-7 cluster "
                    "either/ors, the 11:1-6 merger question spanning P03-023/024, and the "
                    "cross-cluster skeleton-tier cohesion standard). Rows p02-013, p02-014, "
                    "P03-023, P03-024 are BOSS-PENDING and excluded from author phase 1.")
p.write_text(json.dumps(w, ensure_ascii=False, indent=1), encoding="utf-8")

from collections import Counter
by_part = Counter((o.get("row_id") or "?")[:3].lower() for o in w["author_phase1_orders"])
print(json.dumps({"author_orders_total": len(w["author_orders"]),
                  "author_phase1": len(w["author_phase1_orders"]),
                  "phase1_by_part": dict(by_part),
                  "boss_items": len(keep_boss),
                  "boss_pending_rows": w["boss_pending_rows"]}, indent=1))
