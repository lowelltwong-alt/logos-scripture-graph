#!/usr/bin/env python3
"""Write the orchestrator's queue for one controlling round from a review deliverable and an items file (TE-1: one tool, any round).

Items are {"id","route","proposal"} with an optional "finding": the review's finding id, whose object is copied byte for
byte into review_finding. Every new finding of the review must be queued, and GATE-E<Q> must be an item. Proposals only;
the controlling execution rules. An existing queue with different bytes is REFUSED.

usage: make_ctl_queue.py --round Q --review FILE --rows FILE --items FILE --prior E5.json [--prior E4.json ...] [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
SP = HERE.parent.parent
sha = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731
ap = argparse.ArgumentParser()
for k in ("--review", "--rows", "--items"):
    ap.add_argument(k, required=True)
ap.add_argument("--round", required=True, type=int)
ap.add_argument("--prior", action="append", required=True)
ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()
rel = lambda n: Path(n).resolve().relative_to(SP).as_posix()  # noqa: E731
review = json.loads(Path(a.review).read_text(encoding="utf-8"))
found = {f["id"]: f for f in review.get("new_findings") or []}
raw = json.loads(Path(a.items).read_text(encoding="utf-8"))
ids = [i["id"] for i in raw]
if len(set(ids)) != len(ids) or any(not {"id", "route", "proposal"} <= set(i) <= {"id", "route", "proposal", "finding"} for i in raw):
    raise SystemExit("REFUSED: items must be unique {id, route, proposal[, finding]} objects")
missing = sorted(set(found) - {i.get("finding") for i in raw})
if missing or "GATE-E%d" % a.round not in ids:
    raise SystemExit("REFUSED: not queued: %s" % (missing or "GATE-E%d" % a.round))
items = []
for i in raw:
    row = {"id": i["id"], "route": i["route"], "proposal": i["proposal"]}
    if "finding" in i:
        row["review_finding"] = found[i["finding"]]
    items.append(row)
queue = {"schema": "m8_controlling_queue.v1", "book": "1Cor", "for_execution": "cor_controlling_rulings_r%d_a1#e1" % a.round,
         "status": "proposed_by_orchestrator",
         "review_deliverable": {"path": rel(a.review), "sha256": sha(Path(a.review).read_bytes())},
         "prior_rulings": [{"path": rel(p), "sha256": sha(Path(p).read_bytes())} for p in a.prior],
         "rows_under_review": {"path": rel(a.rows), "sha256": sha(Path(a.rows).read_bytes())},
         "measured_context": {"readiness": review.get("readiness"), "changes_required": len(review.get("changes_required") or []),
                              "new_findings": len(found)},
         "items": items}
b = (json.dumps(queue, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
out = HERE / ("1cor_controlling_agent_queue_e%d.v1.json" % a.round)
if a.dry_run:
    print(json.dumps({"dry_run": True, "items": len(items), "bytes": len(b)}))
    raise SystemExit(0)
if out.exists() and out.read_bytes() != b:
    raise SystemExit("REFUSED: %s exists with different bytes" % out.name)
tmp = out.with_name(out.name + ".tmp")
tmp.write_bytes(b)
os.replace(tmp, out)
print(json.dumps({"queue": out.name, "sha256": sha(b), "items": len(items)}))
