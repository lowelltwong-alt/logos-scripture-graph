#!/usr/bin/env python3
"""Collect every SIGNALS finding the landed adjudications routed, with its evidence, into one place.

WHY. observed_substrate_signals is outside the authoring pass's writable scope by design (the gate admits it on no
row), so a false signal element can only be reported, never repaired, by a lane or an adjudicator. Five executions have
now reported one. This gathers them from the landed adjudication files - never from a lane's file, since the
adjudication is the reconciled record - so the orchestrator can measure each one and apply a separate guarded sweep.

It extracts, per adjudication: the routed entries and item records whose text names observed_substrate_signals or a
signal element (a dotted lowercase token such as closure.formula_final), keeping the verbatim text as evidence.

usage: python collect_signals_findings.py
"""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
A = EZ / "author" / "final"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
SIG = re.compile(r"observed_substrate_signals|\b[a-z_]+\.[a-z_]+\b")
PID = re.compile(r"P\d\d-\d\d\d")
rows = {r["decision_id"]: r for r in (json.loads(l) for l in (EZ / "repair" / "rows_v7_cwo24.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}
found, sources = [], {}


SCOPE = ("routed", "items", "per_item", "grade_questions", "stops")


def walk(o, path, adj):
    # only the sections that carry findings; an agent's own 'limit' or 'e19_selfreport' prose names rows without
    # reporting anything about their signals, and matching it produced eight false hits on the first run
    if path.count(".") == 1 and path.split(".")[-1] not in SCOPE:
        return
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, "%s.%s" % (path, k), adj)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, "%s[%d]" % (path, i), adj)
    elif isinstance(o, str) and ("observed_substrate_signals" in o
                                 or ("signal" in o.lower() and PID.search(o))
                                 or any(e in o for r in PID.findall(o) for e in (rows.get(r, {}).get("observed_substrate_signals") or []))):
        ids = sorted(set(PID.findall(o)))
        elements = sorted({m for m in re.findall(r"\b[a-z_]+\.[a-z_]+\b", o)
                           if any(m in (rows.get(r, {}).get("observed_substrate_signals") or []) for r in ids)})
        found.append({"adjudication": adj, "at": path, "rows_named": ids, "signal_elements_live_on_those_rows": elements,
                      "verbatim": o[:1200]})


for k in (1, 2, 3, 4, 5, 6):
    p = A / ("s%d_adjudication" % k) / "adjudication.json"
    if not p.is_file():
        continue
    sources["s%d" % k] = sha(p)
    walk(json.loads(p.read_text(encoding="utf-8")), "s%d" % k, "s%d" % k)
by_row = {}
for f in found:
    for r in f["rows_named"]:
        by_row.setdefault(r, {"row": r, "live_signals": rows.get(r, {}).get("observed_substrate_signals"), "reports": []})
        by_row[r]["reports"].append({"adjudication": f["adjudication"], "at": f["at"], "elements": f["signal_elements_live_on_those_rows"],
                                     "verbatim": f["verbatim"]})
out = {"schema": "ezek_signals_findings.v1", "adjudications_read": sources, "rows_sha256": sha(EZ / "repair" / "rows_v7_cwo24.jsonl"),
       "reports": len(found), "rows_with_a_signals_report": sorted(by_row), "by_row": by_row,
       "note": ("a report is EVIDENCE, not an order: each element is re-measured on the witness before any sweep, and a "
                "removal is applied only where the measurement shows the element false for that span")}
p = HERE / "signals_findings.v1.json"
data = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
if p.exists() and p.read_bytes() != data and "--overwrite" not in __import__("sys").argv:
    raise SystemExit("REFUSED: %s exists with different bytes (E-41); pass --overwrite once the earlier copy is recorded" % p.name)
p.write_bytes(data)
print(json.dumps({"adjudications_read": sorted(sources), "reports": len(found), "rows": sorted(by_row),
                  "elements_by_row": {r: v["reports"][0]["elements"] for r, v in by_row.items()}, "sha256": sha(p)}, indent=1))
