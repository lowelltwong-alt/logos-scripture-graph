#!/usr/bin/env python3
"""Orchestrator re-verification of a primary-review wave (never trust
self-reports). Usage: _pr_wave_verify.py c01 c02 c03

Per cluster x role: JSON parses; role/cluster fields match the filename;
rows_reviewed == the cluster assignment exactly; exactly one item per
assigned row; verdict vocabulary; severity present iff challenge; summary
tallies match recomputed counts; normalize dry-run over the review file is
byte-clean (E-01 applies to review prose too)."""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE / "tools"
REVIEWS = HERE / "reviews"

clusters = {c["id"]: c for c in json.loads(
    (HERE / "review_clusters.json").read_text(encoding="utf-8"))["clusters"]}

VERDICTS = {"support", "challenge"}
SEVERITIES = {"high", "medium", "low"}

wave = sys.argv[1:]
assert wave, "pass cluster ids, e.g. _pr_wave_verify.py c01 c02 c03"
results = {}
census = {"rows": 0, "supports": 0, "challenges": 0,
          "by_severity": {"high": 0, "medium": 0, "low": 0}, "files": 0}
hard_fail = False
for cid in wave:
    assigned = clusters[cid]["row_ids"]
    for role in ("LF", "OL"):
        fname = f"rev_{role}_{cid}.json"
        path = REVIEWS / fname
        probs = []
        if not path.is_file():
            results[fname] = {"status": "MISSING"}
            hard_fail = True
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            results[fname] = {"status": "UNPARSEABLE", "error": str(e)}
            hard_fail = True
            continue
        if doc.get("role") != f"primary_{role}":
            probs.append(f"role={doc.get('role')}")
        if doc.get("cluster") != cid:
            probs.append(f"cluster={doc.get('cluster')}")
        rr = doc.get("rows_reviewed") or []
        if sorted(rr) != sorted(assigned):
            probs.append(f"rows_reviewed mismatch: {rr}")
        items = doc.get("items") or []
        item_rows = [i.get("row_id") for i in items]
        if sorted(item_rows) != sorted(assigned):
            probs.append(f"items rows mismatch: {item_rows}")
        if len(item_rows) != len(set(item_rows)):
            probs.append("duplicate item row_ids")
        sup = ch = 0
        sev = {"high": 0, "medium": 0, "low": 0}
        for i in items:
            v = i.get("verdict")
            if v not in VERDICTS:
                probs.append(f"{i.get('row_id')}: bad verdict {v!r}")
                continue
            if v == "support":
                sup += 1
                if i.get("severity") in SEVERITIES:
                    probs.append(f"{i.get('row_id')}: severity on a support")
            else:
                ch += 1
                s = i.get("severity")
                if s not in SEVERITIES:
                    probs.append(f"{i.get('row_id')}: challenge missing severity ({s!r})")
                else:
                    sev[s] += 1
            if not (i.get("claim") and i.get("evidence")):
                probs.append(f"{i.get('row_id')}: empty claim/evidence")
        summ = doc.get("summary") or {}
        if summ.get("supports") != sup or summ.get("challenges") != ch:
            probs.append(f"summary tallies {summ.get('supports')}/{summ.get('challenges')} != recomputed {sup}/{ch}")
        declared_sev = {k: v for k, v in (summ.get("by_severity") or {}).items() if v}
        recomputed_sev = {k: v for k, v in sev.items() if v}
        if declared_sev != recomputed_sev:
            probs.append(f"summary by_severity {declared_sev} != recomputed {recomputed_sev}")
        norm = subprocess.run(
            [sys.executable, str(TOOLS / "normalize_hebrew_in_json.py"), str(path)],
            capture_output=True, text=True, encoding="utf-8")
        try:
            nout = json.loads(norm.stdout)
            if nout.get("fixed", 0) or nout.get("defect_count", 0):
                probs.append(f"nfd: fixed={nout.get('fixed')} defects={nout.get('defect_count')}")
        except json.JSONDecodeError:
            probs.append(f"normalize unparseable: {norm.stdout[-200:]} {norm.stderr[-200:]}")
        status = "PASS" if not probs else "FAIL"
        if probs:
            hard_fail = True
        results[fname] = {"status": status, "problems": probs,
                          "supports": sup, "challenges": ch, "by_severity": recomputed_sev}
        census["rows"] += len(items)
        census["supports"] += sup
        census["challenges"] += ch
        for k, v in sev.items():
            census["by_severity"][k] += v
        census["files"] += 1
print(json.dumps({"wave": wave, "verify": "PASS" if not hard_fail else "FAIL",
                  "census": census, "files": results}, ensure_ascii=False, indent=1))
sys.exit(1 if hard_fail else 0)
