#!/usr/bin/env python3
"""Boss-round batch verifier (m8-mesh-r3, Lam; book-agnostic copy of the Jer build) — run after every boss batch.

Per boss agent: output JSON parses; attempt_id/role match the slice; ruling
ids exactly the slice's item ids in order; decision/consequence/severity
vocabulary; decision-kind coherence; consequence rows present on every
span/cwo/sample item; summary tallies match recomputed counts; normalize
dry-run over the file is byte-clean (E-01 applies to ruling prose too).
Usage: _boss_verify.py b1 [b2 b3 b4 ...]   (agent letters, positional only)
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE / "tools"

DECISIONS = {"adopt", "decline", "record", "owner_escalation"}
KINDS = {"adopt_change", "disclosure_cure", "no_action", "record",
         "owner_escalation", "corpus_wide_order"}   # Lam: the E-18 CWO adjudication kind
COHERENCE = {"adopt": {"adopt_change", "corpus_wide_order"},
             "decline": {"disclosure_cure", "no_action"},
             "record": {"record", "corpus_wide_order"},
             "owner_escalation": {"owner_escalation"}}
ROWS_REQUIRED = {"boundary_proposal", "boundary_proposal_pair", "corpus_wide_orders", "sample_defect_record"}   # Lam item kinds
SEVS = {"high", "medium", "low"}

args = [a for a in sys.argv[1:]]
if not args:
    print("usage: _boss_verify.py b1 [b2 ...]")
    sys.exit(2)

results = {}
census = {"ruled": 0, "adopted_changes": 0, "cures": 0, "no_action": 0,
          "records": 0, "owner_escalations": 0, "files": 0}
hard_fail = False
for a in args:
    slice_path = HERE / f"boss_docket_{a}.json"
    probs = []
    sl = json.load(open(slice_path, encoding="utf-8"))
    expect_ids = [i["item_id"] for i in sl["items"]]
    kinds_by_id = {i["item_id"]: i["kind"] for i in sl["items"]}
    out_path = HERE / sl["output_file"]
    fname = sl["output_file"]
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
    if doc.get("role") != "boss":
        probs.append(f"role {doc.get('role')} != boss")
    rulings = doc.get("rulings") or []
    got_ids = [r.get("id") for r in rulings]
    if got_ids != expect_ids:
        probs.append(f"ruling ids {got_ids} != assigned {expect_ids}")
    tall = {"ruled": 0, "adopted_changes": 0, "cures": 0, "no_action": 0,
            "records": 0, "owner_escalations": 0}
    for r in rulings:
        rid = r.get("id")
        dec = r.get("decision")
        cons = r.get("consequence") or {}
        kind = cons.get("kind")
        if dec not in DECISIONS:
            probs.append(f"{rid}: bad decision {dec}")
        if kind not in KINDS:
            probs.append(f"{rid}: bad consequence.kind {kind}")
        if dec in COHERENCE and kind not in COHERENCE[dec]:
            probs.append(f"{rid}: decision {dec} incoherent with kind {kind}")
        if kinds_by_id.get(rid) in ROWS_REQUIRED and not cons.get("rows"):
            probs.append(f"{rid}: consequence.rows empty on {kinds_by_id.get(rid)}")
        if r.get("severity") not in SEVS:
            probs.append(f"{rid}: bad severity {r.get('severity')}")
        if not (r.get("grounds") or "").strip():
            probs.append(f"{rid}: empty grounds")
        if not (cons.get("spec") or "").strip():
            probs.append(f"{rid}: empty consequence.spec")
        tall["ruled"] += 1
        tall["adopted_changes"] += kind == "adopt_change"
        tall["cures"] += kind == "disclosure_cure"
        tall["no_action"] += kind == "no_action"
        tall["records"] += dec == "record"   # Lam: a record DECISION (incl. the corpus_wide_order kind) counts as a record
        tall["owner_escalations"] += kind == "owner_escalation"
    summ = doc.get("summary") or {}
    for k in tall:
        if summ.get(k) != tall[k]:
            probs.append(f"summary {k} {summ.get(k)} != recomputed {tall[k]}")
    norm = subprocess.run(
        [sys.executable, str(TOOLS / "normalize_hebrew_in_json.py"), str(out_path)],
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
    results[fname] = {"status": status, "problems": probs, "tally": tall}
    for k in tall:
        census[k] += tall[k]
    census["files"] += 1

print(json.dumps({"batch": args,
                  "verify": "FAIL" if hard_fail else "PASS",
                  "census": census, "results": results},
                 ensure_ascii=False, indent=1))
sys.exit(1 if hard_fail else 0)
