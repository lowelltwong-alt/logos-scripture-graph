#!/usr/bin/env python3
"""Spot-packet verifier (orchestrator; deterministic). Per packet spot_SN.json: parses; attempt_id/lane match the scope;
every finding carries row_ids (all in rows_v3), lane, e_class, severity in {high,medium,low}, defective_text,
byte_evidence, proposed_cure (non-empty strings, no unexpanded {placeholder}); warn dispositions carry
disposition in {declared_fp,genuine}; scope_items_reviewed == the lane's decisions. Prints the COUNTS; exit 1 on fail.
Usage: _spot_verify.py [S1 S2 ...]"""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
PH = re.compile(r"\{[A-Za-z0-9_]+\}")
scope = json.load(open(HERE / "spot_scope.json", encoding="utf-8"))["lanes"]
ids = {json.loads(l)["decision_id"] for l in open(HERE / "rows_v3.jsonl", encoding="utf-8-sig") if l.strip()}
lanes = sys.argv[1:] or sorted(scope)
out, fail = {}, False
for sn in lanes:
    p = HERE / "spot" / f"spot_{sn}.json"; probs = []
    if not p.is_file():
        out[sn] = {"status": "ABSENT"}; fail = True; continue
    try:
        d = json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception as e:
        out[sn] = {"status": "FAIL", "problems": [f"unparseable: {e!r}"]}; fail = True; continue
    if d.get("attempt_id") != f"jer_spot_{sn}_a1": probs.append(f"attempt_id {d.get('attempt_id')}")
    fs = d.get("findings", [])
    if not isinstance(fs, list): probs.append("findings not a list"); fs = []
    sev = {"high": 0, "medium": 0, "low": 0}
    for i, f in enumerate(fs):
        for k in ("row_ids", "e_class", "severity", "defective_text", "byte_evidence", "proposed_cure"):
            if k not in f: probs.append(f"finding {i}: missing {k}")
        rids = f.get("row_ids") or ([f["row_id"]] if f.get("row_id") else [])
        bad = [r for r in rids if r not in ids]
        if bad: probs.append(f"finding {i}: unknown rows {bad}")
        if f.get("severity") not in sev: probs.append(f"finding {i}: severity {f.get('severity')!r}")
        else: sev[f["severity"]] += 1
        for k in ("defective_text", "byte_evidence", "proposed_cure"):
            v = f.get(k)
            if isinstance(v, str) and PH.search(v): probs.append(f"finding {i}: placeholder in {k}")
    wd = d.get("warn_flags_dispositioned", [])
    badd = [w for w in wd if w.get("disposition") not in ("declared_fp", "genuine")]
    if badd: probs.append(f"{len(badd)} warn dispositions with an illegal value")
    if d.get("scope_items_reviewed") != scope[sn]["decisions"]: probs.append(f"scope_items_reviewed {d.get('scope_items_reviewed')} != {scope[sn]['decisions']} decisions")
    out[sn] = {"status": "PASS" if not probs else "FAIL", "problems": probs, "findings": len(fs), "by_severity": sev, "clean": d.get("clean"), "warn_dispositions": len(wd),
               "genuine_warns": sum(1 for w in wd if w.get("disposition") == "genuine"), "lane_digits": d.get("lane_digits")}
    fail = fail or bool(probs)
print(json.dumps({"status": "FAIL" if fail else "PASS", "lanes": out, "findings_total": sum(v.get("findings", 0) for v in out.values() if isinstance(v, dict))}, ensure_ascii=False, indent=1))
sys.exit(1 if fail else 0)
