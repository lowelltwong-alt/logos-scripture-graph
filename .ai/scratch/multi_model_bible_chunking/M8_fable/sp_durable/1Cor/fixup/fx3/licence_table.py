#!/usr/bin/env python3
"""Licence table for FIXUP-3: every field changed from the pinned rows, set against the orders that license it.
usage: licence_table.py ROWS OUT.json
A change is field_named when an order to that part names the row and the field (or its abbreviation), row_named when an order names
the row with no field word, cwo when the baseline sweep has a CWO-06 or CWO-07 hit in that row and field, and UNLICENSED otherwise.
Each changed text field is then cut into hunks on the old text; a hunk touching no named span of its row is listed under
outside_spans for a hand read, since an order that names a sentence or a clause carries no span the tool can test.
Every exact span of a row's orders is reported as gone or still_present in the new bytes (condition 12 of GATE-E4).
"""
import difflib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
BK = Path(__file__).resolve().parents[2]
R = BK / "review"
PINNED = BK / "fixup/draft_rows_fixup2_applied.jsonl"
BASE_SWEEP = R / "cwo_1cor_post_fixup2_cwo0607_report.v1.json"
PROSE = {"boundary_rationale", "strongest_rejected_alternative", "device_notes", "observed_substrate_signals", "boundary_evidence_refs"}
FIELDS = {"device_notes": ("device_notes", "DN"), "strongest_rejected_alternative": ("strongest_rejected_alternative", "SRA")}


def load(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


def text(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)


def orders():
    out = []
    for name in ("1cor_controlling_agent_rulings_E4.v1.json", "1cor_controlling_agent_rulings_E3.v1.json"):
        d = json.loads((R / name).read_text(encoding="utf-8"))
        for r in d["rulings"]:
            if name.count("_E3") and r["id"] != "S3-01":
                continue
            for o in r.get("orders") or []:
                if str(o.get("to", "")).startswith("author_fixup"):
                    out.append({"id": r["id"], "order": o["order"], "spans": o.get("exact_spans") or []})
    return out


def main():
    old = {r["decision_id"]: r for r in load(PINNED)}
    new = load(sys.argv[1])
    ords = orders()
    base = json.loads(BASE_SWEEP.read_text(encoding="utf-8"))
    hits = {(h["row"], h["field"]) for h in base["CWO06"]["list"]}
    cwo07_rows = {h["row"] for h in base["CWO07"]["list"]}
    table, span_rows = [], []
    for r in new:
        rid = r["decision_id"]
        was = old[rid]
        mine = [o for o in ords if rid in o["order"]]
        spans = [s for o in mine for s in o["spans"]]
        for k in was:
            if r.get(k) == was[k]:
                continue
            words = FIELDS.get(k, (k,))
            if any(w in o["order"] for o in mine for w in words):
                status = "field_named"
            elif (rid, k) in hits or (rid in cwo07_rows and k in PROSE):
                status = "cwo"
            elif mine:
                status = "row_named"
            else:
                status = "UNLICENSED"
            a, b = text(was[k]), text(r[k])
            at = [(a.find(s), a.find(s) + len(s)) for s in spans if a.find(s) >= 0]
            outside = []
            for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
                if tag != "equal" and not any(x < max(i2, i1 + 1) and i1 < y for x, y in at):
                    outside.append({"old": a[i1:i2][:100], "new": b[j1:j2][:100]})
            table.append({"row": rid, "field": k, "status": status, "orders": [o["id"] for o in mine], "outside_spans": outside[:12], "outside_count": len(outside)})
        now = " ".join(text(r.get(k)) for k in was)
        for s in spans:
            span_rows.append({"row": rid, "span": s, "state": "still_present" if s in now else "gone"})
    res = {"rows_file": str(sys.argv[1]), "changed_fields": len(table), "by_status": {}, "table": table, "spans": span_rows,
           "spans_still_present": sum(1 for s in span_rows if s["state"] == "still_present")}
    for t in table:
        res["by_status"][t["status"]] = res["by_status"].get(t["status"], 0) + 1
    Path(sys.argv[2]).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: res[k] for k in ("changed_fields", "by_status", "spans_still_present")}))


main()
