#!/usr/bin/env python3
"""FINAL REMEDIATION WORKLIST: every owed correction after REPAIR-2 step 7, from its record, grouped by row.

Sources, each read from the record that holds it:
  S7DEF    the step-7 reconciled defects (both readers' evidence; a one-reader defect is a candidate to re-measure)
  S7OUT    the step-7 readers' out-of-scope observations (e.g. #e12 per-row orders still undone)
  R6       the step-6 adjudicators' routed corrections (concrete repairs; #e16 class questions excluded - they are #e16's)
  E16      #e16's author orders (orders_for_final_remediation with kind 'author'); mechanical orders and grade moves are
           executed by the orchestrator separately and are NOT author items
An item whose row no longer exists refuses the build. Items are grouped by row so one author reads a row once.

usage: python build_final_worklist.py [--probe]    (--probe: #e16 not required; writes to scratch)
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
PROBE = "--probe" in sys.argv
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_final_probe")
OUT = (SCR if PROBE else HERE) / "final_worklist.v1.json"
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
REC = EZ / "repair2" / "step7" / "step7_reconciled.v2.json"
E16 = EZ / "author" / "e16" / "ruling_e16.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
PID = re.compile(r"P\d\d-\d\d\d")
PROSE = ["boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess"]
REFS = "boundary_evidence_refs"

rows = {r["decision_id"]: r for r in (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}
items = []


def add(cls, row, order, data, source):
    if row not in rows:
        raise SystemExit("REFUSED: %s names a row the corpus does not carry: %r" % (cls, row))
    items.append({"id": None, "class": cls, "row": row, "fields_hint": PROSE + [REFS], "order": order, "data": data,
                  "source": source, "status": "PENDING"})


rec = json.loads(REC.read_text(encoding="utf-8"))
for d in rec["defects"]:
    add("S7DEF", d["row"],
        ("A step-7 reader found this %s defect (%s; raised by %s). RE-MEASURE against the witness first: repair what "
         "reproduces with the smallest change that makes the row true; NO_DEFECT with evidence what does not." %
         (d["item"], d["max_severity"], {"BOTH": "both readers", "A_ONLY": "one reader", "B_ONLY": "one reader"}[d["agreement"]])),
        {"item": d["item"], "agreement": d["agreement"], "severity": d["max_severity"], "reader_A": d["A"], "reader_B": d["B"]},
        "Ezek/repair2/step7/step7_reconciled.v1.json")
for s, v in rec["strides"].items():
    for lane in ("A", "B"):
        obs = v.get("outside_scope", {}).get(lane)
        flat = obs if isinstance(obs, list) else [x for vals in (obs or {}).values() for x in (vals if isinstance(vals, list) else [vals])]
        for o in flat:
            txt = json.dumps(o, ensure_ascii=False)
            for rid in sorted(set(PID.findall(txt))):
                if rid in rows:
                    add("S7OUT", rid, "A step-7 reader observed this outside the changed fields. RE-MEASURE; repair what reproduces; NO_DEFECT with evidence otherwise.",
                        {"stride": s, "reader": lane, "observation": o}, "Ezek/repair2/step7/step7_reconciled.v1.json strides.%s.outside_scope" % s)
for h in (1, 2):
    adj = EZ / "author" / "repair2_step6" / ("h%d_adjudication" % h) / "adjudication.json"
    for e in json.loads(adj.read_text(encoding="utf-8")).get("routed") or []:
        txt = json.dumps(e, ensure_ascii=False)
        if re.search(r"for #e16|to #e16|#e16:|class question|confidence observation", txt, re.I) and not re.search(r"exact repair|replace|->|-&gt;|add ", txt, re.I):
            continue
        for rid in sorted(set(PID.findall(txt))):
            if rid in rows:
                add("R6", rid, "ROUTED by a step-6 adjudicator with its repair, verbatim below. RE-MEASURE; make the repair if it reproduces; NO_DEFECT with evidence otherwise.",
                    {"routed_entry": e}, str(adj.relative_to(EZ)))
if E16.is_file():
    r16 = json.loads(E16.read_text(encoding="utf-8"))
    mech = json.loads((EZ / "repair2" / "e16" / "mechanical" / "plan.json").read_text(encoding="utf-8"))
    routed_ids = {(r.get("id"), r.get("row")) for r in mech["routed_to_authors"]}
    for o in r16.get("orders_for_final_remediation") or []:
        kind = str(o.get("kind", "")).lower()
        for rid in sorted(set(re.findall(r"P\d\d-\d\d\d", str(o.get("row", ""))))):
            # author orders, and mechanical orders the planner could not execute exactly, become author items per row
            if rid in rows and (kind == "author" or (o.get("id"), rid) in routed_ids or (o.get("id"), o.get("row")) in routed_ids):
                add("E16", rid, "ORDERED by #e16 (the controlling agent): execute exactly; STOP with evidence if the order cannot be made true.",
                    {"order": o, "was_mechanical_routed": kind != "author"}, "Ezek/author/e16/ruling_e16.json")
    for g in mech["grade_moves"]:
        add("E16GROUND", g["row"], ("#e16 moves this row's grade %s -> %s (applied mechanically in the same batch). Write the ground into the "
                                    "row's prose so the text states the grade it carries: %s" % (g["from"], g["to"], g.get("ground"))),
            {"grade_move": g}, "Ezek/repair2/e16/mechanical/plan.json")
elif not PROBE:
    raise SystemExit("REFUSED: #e16 has not landed at %s; build with --probe only" % E16)
for n, it in enumerate(items, 1):
    it["id"] = "F-%03d" % n
by_class, by_row = {}, {}
for it in items:
    by_class[it["class"]] = by_class.get(it["class"], 0) + 1
    by_row[it["row"]] = by_row.get(it["row"], 0) + 1
out = {"schema": "ezek_final_remediation_worklist.v1", "probe": PROBE, "rows_sha256": sha(ROWS), "e16_landed": E16.is_file(),
       "items_by_class": by_class, "rows_owed": len(by_row), "items": items}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"probe": PROBE, "items": len(items), "items_by_class": by_class, "rows_owed": len(by_row),
                  "rows_with_most_items": sorted(by_row.items(), key=lambda x: -x[1])[:8], "out": str(OUT), "sha256": sha(OUT)}, indent=1))
