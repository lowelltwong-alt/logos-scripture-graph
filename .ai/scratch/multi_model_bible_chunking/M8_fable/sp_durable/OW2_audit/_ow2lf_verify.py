#!/usr/bin/env python3
"""OW-2 LF-audit batch verifier — run after every audit batch.

Per batch: packet parses; attempt_id matches the slice; exactly one entry
per assigned row, none outside; verdict/severity vocabulary; findings on
every defect row; med/high + span-proposal routing queue extracted;
summary tallies recomputed; normalize dry-run byte-clean (Isa normalizer).
Usage: _ow2lf_verify.py b01 [b02 ...]
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ISA_TOOLS = HERE.parent / "Isa" / "tools"
SEVS = {"low", "medium", "high"}
# a proposed_change is a SPAN proposal only when it proposes boundary work;
# field-repair specs are findings for the remediation docket, not span
# proposals (OW-2 item 1 routes med/high + span changes + disagreements).
# Waves from b11 on also carry an explicit boolean "span_change" per finding
# (brief hardened after wave A1 exposed this schema gap).
SPAN_PAT = re.compile(
    r"respan|re-span|new span|span set|merge|merging|split|absorb|"
    r"boundary (?:change|move|relocat)|move the seam|retire", re.I)

args = sys.argv[1:]
if not args:
    print("usage: _ow2lf_verify.py b01 [b02 ...]")
    sys.exit(2)

results = {}
warns = []
census = {"rows": 0, "clean": 0, "defect_rows": 0,
          "low": 0, "medium": 0, "high": 0, "span_changes_proposed": 0,
          "files": 0}
routing_queue = []
hard_fail = False
for b in args:
    sl = json.load(open(HERE / "slices" / f"slice_{b}.json", encoding="utf-8"))
    out_path = HERE / sl["output_file"]
    fname = sl["output_file"]
    probs = []
    if not out_path.exists():
        results[fname] = {"status": "FAIL", "problems": ["output MISSING"]}
        hard_fail = True
        continue
    try:
        doc = json.load(open(out_path, encoding="utf-8"))
    except json.JSONDecodeError as e:
        results[fname] = {"status": "FAIL", "problems": [f"unparseable: {e}"]}
        hard_fail = True
        continue
    if doc.get("attempt_id") != sl["attempt_id"]:
        probs.append(f"attempt_id {doc.get('attempt_id')} != {sl['attempt_id']}")
    rows = doc.get("rows") or []
    got = [r.get("row_id") for r in rows]
    if got != sl["row_ids"]:
        probs.append(f"row ids {got} != assigned {sl['row_ids']}")
    tall = {"rows": 0, "clean": 0, "defect_rows": 0,
            "low": 0, "medium": 0, "high": 0, "span_changes_proposed": 0}
    for r in rows:
        rid = r.get("row_id")
        v = r.get("verdict")
        finds = r.get("findings") or []
        if v not in ("clean", "defect"):
            probs.append(f"{rid}: bad verdict {v}")
        if v == "defect" and not finds:
            probs.append(f"{rid}: defect with no findings")
        if v == "clean" and finds:
            probs.append(f"{rid}: clean but carries findings")
        tall["rows"] += 1
        tall["clean"] += v == "clean"
        tall["defect_rows"] += v == "defect"
        for f in finds:
            sev = f.get("severity")
            if sev not in SEVS:
                probs.append(f"{rid}: bad severity {sev}")
                continue
            if not (f.get("grounds") or "").strip():
                probs.append(f"{rid}: finding with empty grounds")
            tall[sev] += 1
            sc = f.get("proposed_change")
            explicit = f.get("span_change")
            is_span = (bool(explicit) if isinstance(explicit, bool)
                       else bool(sc) and bool(SPAN_PAT.search(str(sc))))
            if is_span:
                tall["span_changes_proposed"] += 1
            if sev in ("medium", "high") or is_span:
                routing_queue.append({"batch": b, "row_id": rid,
                                      "severity": sev,
                                      "claim": (f.get("claim") or "")[:160],
                                      "span_change": is_span})
    summ = doc.get("summary") or {}
    if summ.get("rows") != tall["rows"] or summ.get("clean") != tall["clean"] \
            or summ.get("defect_rows") != tall["defect_rows"]:
        probs.append(f"summary row tallies != recomputed {tall}")
    sf = summ.get("findings") or {}
    for k in ("low", "medium", "high"):
        if sf.get(k) != tall[k]:
            probs.append(f"summary findings.{k} {sf.get(k)} != {tall[k]}")
    if summ.get("span_changes_proposed") != tall["span_changes_proposed"]:
        # pattern detection can under/over-match a prose spec: surface for
        # orchestrator reconciliation rather than hard-failing the packet
        warns.append(f"{fname}: summary span_changes_proposed "
                     f"{summ.get('span_changes_proposed')} != detected "
                     f"{tall['span_changes_proposed']} — reconcile by reading")
    norm = subprocess.run(
        [sys.executable, str(ISA_TOOLS / "normalize_hebrew_in_json.py"),
         str(out_path)], capture_output=True, text=True, encoding="utf-8")
    try:
        nout = json.loads(norm.stdout)
        if nout.get("fixed", 0) or nout.get("defect_count", 0):
            probs.append(f"nfd: fixed={nout.get('fixed')} defects={nout.get('defect_count')}")
    except json.JSONDecodeError:
        probs.append(f"normalize unparseable: {norm.stdout[-200:]} {norm.stderr[-200:]}")
    status = "PASS" if not probs else "FAIL"
    if probs:
        hard_fail = True
    results[fname] = {"status": status, "problems": probs, "tally": tall}
    for k in tall:
        census[k] += tall[k]
    census["files"] += 1

print(json.dumps({"batch": args,
                  "verify": "FAIL" if hard_fail else "PASS",
                  "census": census,
                  "warns": warns,
                  "routing_queue_size": len(routing_queue),
                  "routing_queue": routing_queue,
                  "results": {k: {kk: vv for kk, vv in v.items()
                                  if kk != "tally"}
                              for k, v in results.items()}},
                 ensure_ascii=False, indent=1))
sys.exit(1 if hard_fail else 0)
