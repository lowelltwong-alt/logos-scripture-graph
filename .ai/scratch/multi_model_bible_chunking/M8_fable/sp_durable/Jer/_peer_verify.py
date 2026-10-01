#!/usr/bin/env python3
"""Orchestrator re-verification of a peer-adjudication batch (never trust
self-reports). Usage: _peer_verify.py 01 02 03 [--attempt 1]

Per peer attempt: JSON parses; attempt_id/clusters match peer_scope.json;
exactly one ruling per assigned r1 row, none outside the assignment; ruling
and severity vocabulary; deferred_row_ids equals the scope's split exactly;
supported_sample stays inside the assigned sample; summary tallies match
recomputed counts; normalize dry-run over the file is byte-clean (E-01
applies to ruling prose too)."""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE / "tools"
REVIEWS = HERE / "reviews"

SCOPE = json.loads((HERE / "peer_scope.json").read_text(encoding="utf-8"))
peers = {p["peer_id"]: p for p in SCOPE["peers"]}

argv = list(sys.argv[1:])
attempt_n = 1
if "--attempt" in argv:
    _i = argv.index("--attempt")
    attempt_n = int(argv[_i + 1])
    del argv[_i:_i + 2]
args = [a for a in argv if not a.startswith("--")]
assert args, "pass peer numbers, e.g. _peer_verify.py 01 02 03"

RULINGS = {"uphold", "refine", "refute", "escalate"}
SEVS = {"high", "medium", "low", "n/a"}

results = {}
census = {"rulings": 0, "uphold": 0, "refine": 0, "refute": 0, "escalate": 0,
          "new_findings": 0, "sample_checks": 0, "sample_defects": 0, "files": 0}
hard_fail = False
for n in args:
    pid = f"peer_{n}"
    scope = peers[pid]
    split = scope["attempt_splits"][attempt_n - 1]
    fname = scope["output"] if attempt_n == 1 else scope["followon_outputs"][attempt_n - 2]
    path = HERE / fname
    probs = []
    if not path.is_file():
        results[fname] = {"status": "MISSING"}
        hard_fail = True
        continue
    try:
        pk = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        results[fname] = {"status": "FAIL", "problems": [f"json: {e}"]}
        hard_fail = True
        continue
    if pk.get("attempt_id") != split["attempt_id"]:
        probs.append(f"attempt_id {pk.get('attempt_id')} != {split['attempt_id']}")
    if sorted(pk.get("clusters") or []) != sorted(scope["clusters"]):
        probs.append(f"clusters {pk.get('clusters')} != {scope['clusters']}")
    rulings = pk.get("rulings") or []
    if len(rulings) > 8:
        probs.append(f"{len(rulings)} rulings exceeds the hard cap 8")
    ruled = [r.get("row_id") for r in rulings]
    if sorted(ruled) != sorted(set(ruled)):
        probs.append("duplicate row_id in rulings")
    want = split["r1_row_ids"]
    if set(ruled) != set(want):
        probs.append(f"ruled set != assigned r1 set (missing {sorted(set(want)-set(ruled))}, extra {sorted(set(ruled)-set(want))})")
    tall = {"uphold": 0, "refine": 0, "refute": 0, "escalate": 0}
    for r in rulings:
        if r.get("ruling") not in RULINGS:
            probs.append(f"{r.get('row_id')}: bad ruling {r.get('ruling')}")
        else:
            tall[r["ruling"]] += 1
        if r.get("severity_final") not in SEVS:
            probs.append(f"{r.get('row_id')}: bad severity_final {r.get('severity_final')}")
        if r.get("ruling") in ("uphold", "refine") and not r.get("remedy"):
            probs.append(f"{r.get('row_id')}: {r.get('ruling')} without remedy")
    if sorted(pk.get("deferred_row_ids") or []) != sorted(split["deferred_row_ids"]):
        probs.append(f"deferred list != scope split")
    samp = pk.get("supported_sample") or []
    extra_samp = [s.get("row_id") for s in samp if s.get("row_id") not in scope["sample_row_ids"]]
    if extra_samp:
        probs.append(f"sample rows outside assignment: {extra_samp}")
    summ = pk.get("summary") or {}
    if summ.get("challenges_adjudicated") not in (len(rulings), None) and summ.get("challenges_adjudicated") != len(rulings):
        probs.append(f"summary adjudicated {summ.get('challenges_adjudicated')} != {len(rulings)}")
    for k in ("uphold", "refine", "refute", "escalate"):
        if summ.get(k) != tall[k]:
            probs.append(f"summary {k} {summ.get(k)} != recomputed {tall[k]}")
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
    results[fname] = {"status": status, "problems": probs, "tally": tall,
                      "new_findings": summ.get("new_findings", 0)}
    census["rulings"] += len(rulings)
    for k in tall:
        census[k] += tall[k]
    census["new_findings"] += summ.get("new_findings", 0) or 0
    census["sample_checks"] += len(samp)
    census["sample_defects"] += sum(1 for s in samp if s.get("result") == "defect_found")
    census["files"] += 1

print(json.dumps({"batch": args, "attempt": attempt_n,
                  "verify": "FAIL" if hard_fail else "PASS",
                  "census": census, "files": results}, indent=1, ensure_ascii=False))
sys.exit(1 if hard_fail else 0)
