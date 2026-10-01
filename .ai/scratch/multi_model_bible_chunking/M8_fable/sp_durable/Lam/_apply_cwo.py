#!/usr/bin/env python3
"""Guarded apply of the Lamentations CWO wave onto the base corpus (rows_v2, 26 rows) -> rows_v3.jsonl (the Jer
_apply_cwo.py guard pattern; E-18 execution parity; OW-2 item 4 role separation). Run from SP/Lam:
_apply_cwo.py --base rows_v2.jsonl --pin <sha16> --out rows_v3.jsonl --check|--apply

Guards (hard-fail): base sha pinned; every op is "replace" on a row inside its slice's assignment, exactly once; no op
outside the ordered set; a deterministic unify layer cwo/cwo_unify_c[0-9].jsonl (orchestrator; supersedes slice ops
row-wise) is admitted; IMMUTABLE fields byte-equal (decision_id, book, model_id, chunk_index_in_book, span,
parent_collection, unit_type, writer_part, writer_decision_id, writer_attempt_id, non_authorizing,
wj_or_red_letter_considered, review_status); confidence changes ONLY on rows carrying a CWO-12 item and ONLY downward
(high > medium > medium_low > low); frontier_flag_considered ONLY False -> True and only under CWO-12; every other
changed field inside the CWO-open set (boundary_rationale, strongest_rejected_alternative, device_notes,
observed_substrate_signals, boundary_evidence_refs, literature_type_guess, strong_or_hebrew_tags_used); no unexpanded
{placeholder}; every field's TYPE matches the base schema; every string field ONE STRING; in --apply every row carrying
an EXACT-arm item has an op (heuristic-only rows may be omitted = reported clean). Apply: replaces in place (order +
chunk_index preserved, asserted 1..N), writes the out file, runs check_tiling over Lam.1.1-Lam.5.22 (must be GREEN),
writes _apply_cwo_report.json with the changed-fields histogram + per-row changed fields."""
import glob
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

A = sys.argv[1:]
CORPUS = A[A.index("--base") + 1] if "--base" in A else "rows_v2.jsonl"
OUT = A[A.index("--out") + 1] if "--out" in A else "rows_v3.jsonl"
PIN = A[A.index("--pin") + 1] if "--pin" in A else None
# 2026-09-07: the bounded correction round applies over rows_v3 with its own orders dir; defaults keep the first wave identical
ORDERS_GLOB = A[A.index("--orders-glob") + 1] if "--orders-glob" in A else "cwo/orders_cwo_[0-9][0-9].json"
OPS_GLOB = A[A.index("--ops-glob") + 1] if "--ops-glob" in A else "cwo/cwo_[0-9][0-9].jsonl"
UNIFY_GLOB = A[A.index("--unify-glob") + 1] if "--unify-glob" in A else "cwo/cwo_unify_c[0-9].jsonl"
REPORT = A[A.index("--report") + 1] if "--report" in A else "_apply_cwo_report.json"
IMMUTABLE = ["decision_id", "book", "model_id", "chunk_index_in_book", "span", "parent_collection", "unit_type",
             "writer_part", "writer_decision_id", "writer_attempt_id", "non_authorizing", "wj_or_red_letter_considered", "review_status"]
CWO_OPEN = {"boundary_rationale", "strongest_rejected_alternative", "device_notes", "observed_substrate_signals",
            "boundary_evidence_refs", "literature_type_guess", "strong_or_hebrew_tags_used"}
CONF_RANK = {"high": 3, "medium": 2, "medium_low": 1, "low": 0}
PLACEHOLDER = re.compile(r"\{[A-Za-z0-9_]+\}")
SPAN = re.compile(r"^Lam\.(\d+)\.(\d+)-Lam\.(\d+)\.(\d+)$")

mode = "--apply" if "--apply" in A else "--check"
assert PIN, "pass --pin <sha16 of the base corpus>"
raw = open(CORPUS, "rb").read()
sha16 = hashlib.sha256(raw).hexdigest()[:16]
assert sha16 == PIN, f"corpus sha {sha16} != pinned {PIN}"
rows = [json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]
by_id = {r["decision_id"]: r for r in rows}
N = len(rows)
assert [r["chunk_index_in_book"] for r in rows] == list(range(1, N + 1))

ordered, exact_rows, cwo12_rows, slice_of = {}, set(), set(), {}
for f in sorted(glob.glob(ORDERS_GLOB)):
    plan = json.load(open(f, encoding="utf-8"))
    for rid in plan["row_ids"]:
        assert rid not in ordered, f"{rid} ordered twice"
        o = plan["orders"][rid]
        ordered[rid] = o["op"]
        slice_of[rid] = plan["agent"]
        if any(it["arm"] == "exact" for it in o["items"]):
            exact_rows.add(rid)
        if any(it["cwo"] == "CWO-12" for it in o["items"]):
            cwo12_rows.add(rid)
assert ordered, "no orders found under cwo/"
assert all(v == "replace" for v in ordered.values())

ops, landed_slices = {}, set()
for path in sorted(glob.glob(OPS_GLOB)):
    landed_slices.add(path)
    for i, line in enumerate(open(path, encoding="utf-8-sig"), 1):
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        rid = o.get("decision_id")
        if rid in ops:
            sys.exit(f"FAIL duplicate op for {rid} ({path} line {i})")
        ops[rid] = (o, path)
superseded = []
for path in sorted(glob.glob(UNIFY_GLOB)):
    for i, line in enumerate(open(path, encoding="utf-8-sig"), 1):
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        rid = o.get("decision_id")
        if rid not in ordered:
            sys.exit(f"FAIL unify layer row {rid} is not an ordered row ({path} line {i})")
        if rid in ops:
            superseded.append({"row": rid, "slice_file": ops[rid][1], "by": path})
        ops[rid] = (o, path)
failures, changed_union = [], {}
extra = set(ops) - set(ordered)
if extra:
    failures.append(f"ops for un-ordered rows: {sorted(extra)}")
if mode == "--apply":
    n_slices = len(glob.glob(ORDERS_GLOB))
    if len(landed_slices) != n_slices:
        failures.append(f"slices landed {len(landed_slices)} != ordered {n_slices}")
    missing_exact = sorted(exact_rows - set(ops))
    if missing_exact:
        failures.append(f"EXACT-arm rows without ops: {missing_exact}")
for rid, (o, path) in sorted(ops.items()):
    if o.get("_op") != "replace":
        failures.append(f"{rid} op {o.get('_op')!r} != replace"); continue
    if rid not in ordered:
        continue
    digits = re.sub(r"\D", "", Path(path).stem)
    if "unify" not in path and digits and slice_of[rid][-len(digits):] != digits:
        failures.append(f"{rid} landed in {path} but ordered on slice {slice_of[rid]}")
    rep = {k: v for k, v in o.items() if k != "_op"}
    if PLACEHOLDER.search(json.dumps(rep, ensure_ascii=False)):
        failures.append(f"{rid} carries an unexpanded {{placeholder}} token")
    orig = by_id[rid]
    if set(rep) != set(orig):
        failures.append(f"{rid} schema mismatch missing={sorted(set(orig)-set(rep))} extra={sorted(set(rep)-set(orig))}"); continue
    for k, v in rep.items():
        if type(v) is not type(orig[k]):
            failures.append(f"{rid} field {k} type {type(v).__name__} != schema type {type(orig[k]).__name__}")
        if isinstance(orig[k], list) and isinstance(v, list) and any(not isinstance(x, str) for x in v):
            failures.append(f"{rid} field {k} carries a non-string list member")
    changed = [k for k in orig if json.dumps(rep.get(k), ensure_ascii=False, sort_keys=True)
               != json.dumps(orig.get(k), ensure_ascii=False, sort_keys=True)]
    changed_union[rid] = changed
    for k in IMMUTABLE:
        if k in changed:
            failures.append(f"{rid} immutable field changed: {k} ({orig.get(k)!r} -> {rep.get(k)!r})")
    if "confidence" in changed:
        if rid not in cwo12_rows:
            failures.append(f"{rid} confidence change without a CWO-12 item ({orig['confidence']} -> {rep['confidence']})")
        elif CONF_RANK.get(rep["confidence"], 99) >= CONF_RANK.get(orig["confidence"], -1):
            failures.append(f"{rid} confidence not lowered ({orig['confidence']} -> {rep['confidence']}); the wave never raises confidence")
    if "frontier_flag_considered" in changed:
        if rid not in cwo12_rows or orig["frontier_flag_considered"] is not False or rep["frontier_flag_considered"] is not True:
            failures.append(f"{rid} frontier_flag_considered change not admitted ({orig['frontier_flag_considered']!r} -> {rep['frontier_flag_considered']!r})")
    out_of_scope = [k for k in changed if k not in CWO_OPEN and k not in ("confidence", "frontier_flag_considered") and k not in IMMUTABLE]
    if out_of_scope:
        failures.append(f"{rid} changed fields outside the CWO-open set: {out_of_scope}")
    if not SPAN.match(rep.get("span", "")):
        failures.append(f"{rid} malformed span {rep.get('span')!r}")

summary = {"mode": mode, "base": CORPUS, "corpus_sha16": sha16, "rows": N, "ordered": len(ordered), "exact_arm_rows": len(exact_rows),
           "slices_landed": len(landed_slices), "ops_landed": len(ops),
           "rows_unchanged_ops": sorted(r for r, c in changed_union.items() if not c), "unify_layer_supersessions": superseded, "failures": failures}
if failures or mode == "--check":
    summary["status"] = "RED" if failures else "GREEN"
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    print("changed-fields histogram:", json.dumps(
        {f: sum(1 for c in changed_union.values() if f in c) for f in sorted({x for c in changed_union.values() for x in c})}))
    sys.exit(1 if failures else 0)

new_rows = []
for r in rows:
    rid = r["decision_id"]
    new_rows.append({k: v for k, v in ops[rid][0].items() if k != "_op"} if rid in ops else r)
assert [r["chunk_index_in_book"] for r in new_rows] == list(range(1, N + 1))
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    for r in new_rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
sha_out = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
tiling = subprocess.run([sys.executable, "tools/check_tiling.py", OUT, "--range", "Lam.1.1-Lam.5.22"],
                        capture_output=True, text=True, encoding="utf-8")
report = {"status": "GREEN" if tiling.returncode == 0 else "RED_TILING", "base": CORPUS, "rows_in": N, "rows_out": len(new_rows),
          "replaced": len(ops), "ordered": len(ordered), "exact_arm_rows": len(exact_rows),
          "heuristic_only_rows_omitted": sorted(set(ordered) - set(ops)), "unify_layer_supersessions": superseded, "unify_layer_files": sorted(glob.glob(UNIFY_GLOB)),
          "out": OUT, "out_sha256": sha_out, "corpus_sha16": sha16,
          "tiling": "GREEN" if tiling.returncode == 0 else (tiling.stdout or tiling.stderr)[-500:],
          "confidence_changes": {r: [by_id[r]["confidence"], ops[r][0]["confidence"]] for r in sorted(ops) if "confidence" in changed_union.get(r, [])},
          "frontier_flag_changes": sorted(r for r in ops if "frontier_flag_considered" in changed_union.get(r, [])),
          "changed_fields_histogram": {f: sum(1 for c in changed_union.values() if f in c) for f in
                                       sorted({x for c in changed_union.values() for x in c})},
          "changed_fields_union": {r: c for r, c in sorted(changed_union.items())}}
with open(REPORT, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in report.items() if k != "changed_fields_union"}, ensure_ascii=False, indent=1))
sys.exit(0 if report["status"] == "GREEN" else 1)
