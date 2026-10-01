#!/usr/bin/env python3
"""Author-wave landing census (m8-mesh-r3 + OW-1, Lam; book-agnostic copy of the Jer build) — run at every wave close.

Per agent: output parses per line; ops legal and match the orders file
exactly; every assigned row lands exactly once, none outside the
assignment; replace/new_row lines carry the full 22-field schema;
chunk_index_in_book unchanged on replace rows (new row carries the 0
sentinel); retire lines exact two-key format; normalize dry-run over the
file byte-clean (E-01 applies to authored prose too).
Usage: _author_census.py a01 [a02 ...]   (agent ids, positional only)
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE / "tools"

FIELDS = {"book", "boundary_evidence_refs", "boundary_rationale",
          "chunk_index_in_book", "confidence", "decision_id", "device_notes",
          "frontier_flag_considered", "literature_type_guess", "model_id",
          "non_authorizing", "observed_substrate_signals", "parent_collection",
          "review_status", "span", "strong_or_hebrew_tags_used",
          "strongest_rejected_alternative", "unit_type",
          "wj_or_red_letter_considered", "writer_attempt_id",
          "writer_decision_id", "writer_part"}

corpus = {}
for line in open(HERE / "draft_rows_combined.jsonl", encoding="utf-8"):
    r = json.loads(line)
    corpus[r["decision_id"]] = r

args = sys.argv[1:]
if not args:
    print("usage: _author_census.py a01 [a02 ...]")
    sys.exit(2)

results = {}
census = {"agents": 0, "rows_landed": 0, "replaced": 0, "retired": 0,
          "new_rows": 0}
hard_fail = False
for a in args:
    probs = []
    sl = json.load(open(HERE / "author" / f"orders_{a}.json", encoding="utf-8"))
    expected = {rid: sl["orders"][rid]["op"] for rid in sl["row_ids"]}
    out_path = HERE / sl["output_file"]
    fname = sl["output_file"]
    if not out_path.exists():
        results[fname] = {"status": "FAIL", "problems": ["output MISSING"]}
        hard_fail = True
        continue
    landed = {}
    for i, line in enumerate(out_path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            probs.append(f"line {i}: unparseable ({e})")
            continue
        op = obj.get("_op")
        rid = obj.get("decision_id") or obj.get("writer_decision_id")
        if op not in ("replace", "retire", "new_row"):
            probs.append(f"line {i}: bad _op {op}")
            continue
        if rid in landed:
            probs.append(f"{rid}: appears more than once")
        landed[rid] = op
        if rid not in expected:
            probs.append(f"{rid}: NOT in this agent's assignment")
            continue
        if op != expected[rid]:
            probs.append(f"{rid}: op {op} != ordered {expected[rid]}")
        if op == "retire":
            if set(obj.keys()) != {"_op", "writer_decision_id"}:
                probs.append(f"{rid}: retire line must be exactly two keys")
        else:
            missing = FIELDS - set(obj.keys())
            extra = set(obj.keys()) - FIELDS - {"_op"}
            if missing:
                probs.append(f"{rid}: missing fields {sorted(missing)}")
            if extra:
                probs.append(f"{rid}: extra fields {sorted(extra)}")
            if obj.get("decision_id") != obj.get("writer_decision_id"):
                probs.append(f"{rid}: decision_id != writer_decision_id")
            if op == "replace":
                cur = corpus.get(rid)
                if cur and obj.get("chunk_index_in_book") != cur["chunk_index_in_book"]:
                    probs.append(f"{rid}: chunk_index changed "
                                 f"{cur['chunk_index_in_book']} -> {obj.get('chunk_index_in_book')}")
            if op == "new_row" and obj.get("chunk_index_in_book") != 0:
                probs.append(f"{rid}: new_row chunk_index sentinel must be 0")
    not_landed = set(expected) - set(landed)
    if not_landed:
        probs.append(f"assigned rows not landed: {sorted(not_landed)}")
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
    tally = {"rows": len(landed),
             "replaced": sum(1 for v in landed.values() if v == "replace"),
             "retired": sum(1 for v in landed.values() if v == "retire"),
             "new_rows": sum(1 for v in landed.values() if v == "new_row")}
    results[fname] = {"status": status, "problems": probs, "tally": tally}
    census["agents"] += 1
    census["rows_landed"] += tally["rows"]
    census["replaced"] += tally["replaced"]
    census["retired"] += tally["retired"]
    census["new_rows"] += tally["new_rows"]

print(json.dumps({"batch": args,
                  "census_status": "FAIL" if hard_fail else "PASS",
                  "census": census, "results": results},
                 ensure_ascii=False, indent=1))
sys.exit(1 if hard_fail else 0)
