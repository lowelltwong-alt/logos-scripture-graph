#!/usr/bin/env python3
"""REPAIR-2 step-7 SPOT RE-READ SLICES: FULL coverage of every row REPAIR-2 touched, three lanes interleaved by stride.

#e15: "7_validators_and_spot: full suite; then a SPOT RE-READ at FULL coverage of every row REPAIR-2 touched, three
lanes interleaved by stride as before, each slice carrying the per-row ORDERS as data (Q1 cure) and the CONF-CAL
audit view for its rows; then #e16 on the CONF-CAL audit list and the class question."

WHAT IS MEASURED HERE, and how:
  * TOUCHED ROWS: every REPAIR-2 sweep receipt (sweep name starting 'repair2_') names its pre-image backup; each
    sweep's post-image is the next sweep's pre-image, or the live rows for the last. Each pre/post digest is checked
    against the receipt before its diff is trusted, and each sweep's diff must reproduce its receipt's rows_touched.
  * PER ROW: every field that differs between the REPAIR-2 baseline (the first sweep's pre-image) and the live row,
    both values in full; and per sweep, which fields that sweep changed.
  * ORDERS AS DATA: every dict in each step's order files whose "row" (or decision_id) is the row, verbatim - the
    orders the author and the adjudicator worked from. Q1's cure: the reader sees what was ordered, not only what
    changed, so an unordered change and an undischarged order are both visible.
  * CONF-CAL VIEW: the audit member's per-row record if it has been built on the live rows; otherwise the slice says
    UNAVAILABLE and why - never a blank.
Lanes: rows in corpus order, lane = index mod 3 ("interleaved by stride": an author lane was a contiguous stretch,
so a contiguous spot lane would re-read one author's work with one reader).

usage: python build_step7_slices.py [--probe]
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
PROBE = "--probe" in sys.argv
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step7_probe")
BASE = SCR if PROBE else HERE
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
CONFCAL = HERE / "confcal_audit.v2.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
R2 = EZ / "repair2"
ORDER_FILES = {
    "repair2_step1": [EZ / "ezek_controlling_agent_ruling_e15.v1.json"],
    "repair2_step2": [R2 / "step2_reconciliation" / "reconciliation.v1.json",
                      R2 / "step2_reconciliation" / "adjudication_a1" / "adjudication.json"],
    "repair2_step3": [R2 / "step3" / "step3_worklist.v1.json", R2 / "step3" / "adjudication_a1" / "adjudication.json"],
    "repair2_step4a": [R2 / "step4" / "mechanical_proposal.v1.json"],
    "repair2_step4c": [R2 / "step4" / "step4c_worklist.v1.json", EZ / "author" / "repair2_step4c" / "adjudication" / "adjudication.json"],
    "repair2_step5": [R2 / "step5" / "step5_worklist.v1.json",
                      EZ / "author" / "repair2_step5" / "h1_adjudication" / "adjudication.json",
                      EZ / "author" / "repair2_step5" / "h2_adjudication" / "adjudication.json"],
    "repair2_step6": [R2 / "step6" / "step6_worklist.v1.json",
                      EZ / "author" / "repair2_step6" / "h1_adjudication" / "adjudication.json",
                      EZ / "author" / "repair2_step6" / "h2_adjudication" / "adjudication.json"],
}


def load(p):
    return {r["decision_id"]: r for r in (json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip())}


live = load(ROWS)
order_ids = [json.loads(l)["decision_id"] for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
recs = [json.loads(l) for l in (EZ / "author" / "ezek_author_wave_sweep_receipts.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
r2 = [(i, r) for i, r in enumerate(recs) if str(r.get("sweep", "")).startswith("repair2_")]
if not r2:
    raise SystemExit("REFUSED: no REPAIR-2 sweep receipts")
per_sweep = []
for n, (i, rec) in enumerate(r2):
    pre = EZ / "repair" / rec["preimage_backup"]
    post = (EZ / "repair" / recs[i + 1]["preimage_backup"]) if i + 1 < len(recs) else ROWS
    if sha(pre) != rec["preimage_sha256"] or sha(post) != rec["postimage_sha256_measured_from_disk"]:
        raise SystemExit("REFUSED: sweep %s pre/post digests do not match its receipt" % rec["sweep"])
    a, b = load(pre), load(post)
    ch = {rid: sorted(f for f in set(a[rid]) | set(b[rid]) if a[rid].get(f) != b[rid].get(f)) for rid in b}
    ch = {k: v for k, v in ch.items() if v}
    if len(ch) != rec["rows_touched"]:
        raise SystemExit("REFUSED: sweep %s diff finds %d rows, its receipt %s" % (rec["sweep"], len(ch), rec["rows_touched"]))
    per_sweep.append((rec["sweep"], ch))
if sha(ROWS) != r2[-1][1]["postimage_sha256_measured_from_disk"]:
    raise SystemExit("REFUSED: the live rows are not the last REPAIR-2 sweep's post-image; a write happened outside a receipt")
base = load(EZ / "repair" / r2[0][1]["preimage_backup"])


def orders_for(rid, sweep):
    key = next((k for k in ORDER_FILES if sweep.startswith(k)), None)
    found = []
    for p in ORDER_FILES.get(key, []):
        if not p.is_file():
            found.append({"source": str(p.relative_to(EZ)), "UNAVAILABLE": "order file not on disk at build time"})
            continue
        d = json.loads(p.read_text(encoding="utf-8"))

        def walk(o, path):
            if isinstance(o, dict):
                if (o.get("row") == rid or o.get("decision_id") == rid or o.get("row_id") == rid) and len(json.dumps(o, ensure_ascii=False)) < 12000:
                    found.append({"source": "%s %s" % (p.relative_to(EZ), path), "order": o})
                    return
                for k, v in o.items():
                    if k == rid and isinstance(v, (dict, list)):
                        found.append({"source": "%s %s.%s" % (p.relative_to(EZ), path, k), "order": v})
                    else:
                        walk(v, "%s.%s" % (path, k))
            elif isinstance(o, list):
                for j, v in enumerate(o):
                    walk(v, "%s[%d]" % (path, j))
        walk(d, "")
    return found


touched = sorted({rid for _, ch in per_sweep for rid in ch}, key=order_ids.index)
confcal = json.loads(CONFCAL.read_text(encoding="utf-8")) if CONFCAL.is_file() else None
lanes = {1: {}, 2: {}, 3: {}}
for k, rid in enumerate(touched):
    changed = sorted({f for f in set(base[rid]) | set(live[rid]) if base[rid].get(f) != live[rid].get(f)})
    sl = {"row": rid, "span": live[rid].get("span"),
          "confidence": {"at_repair2_baseline": base[rid].get("confidence"), "now": live[rid].get("confidence")},
          "fields_changed_by_repair2": {f: {"before": base[rid].get(f), "after": live[rid].get(f)} for f in changed},
          "unchanged_prose_now": {f: live[rid].get(f) for f in ("boundary_rationale", "strongest_rejected_alternative", "device_notes") if f not in changed},
          "refs_now": live[rid].get("boundary_evidence_refs"),
          "per_sweep": [{"sweep": s, "fields": ch[rid], "orders": orders_for(rid, s)} for s, ch in per_sweep if rid in ch],
          "confcal_view": (next((x for x in confcal.get("all", []) if x.get("row") == rid), {"UNAVAILABLE": "the audit carries no record for this row"})
                           if confcal else {"UNAVAILABLE": "the CONF-CAL audit member v2 is built on the rows after steps 4c-6; this is a probe build"})}
    lanes[k % 3 + 1][rid] = sl
out = {}
for n, sl in lanes.items():
    p = BASE / ("step7_spot_lane_%d.v1.json" % n)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"schema": "ezek_repair2_step7_spot_slices.v1", "lane": n, "rows_sha256": sha(ROWS),
                             "repair2_baseline_sha256": r2[0][1]["preimage_sha256"], "sweeps": [s for s, _ in per_sweep],
                             "rows": len(sl), "slices": sl}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    out[n] = {"rows": len(sl), "sha256": sha(p), "unavailable_orders": sum(1 for s in sl.values() for w in s["per_sweep"] for o in w["orders"] if "UNAVAILABLE" in o),
              "rows_with_no_order_found": sorted(r for r, s in sl.items() if not any(o.get("order") for w in s["per_sweep"] for o in w["orders"]))}
print(json.dumps({"probe": PROBE, "rows_touched_by_repair2": len(touched), "sweeps": {s: len(ch) for s, ch in per_sweep},
                  "confcal_view": "present" if confcal else "UNAVAILABLE (probe)", "lanes": out}, indent=1))
