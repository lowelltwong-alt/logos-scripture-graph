#!/usr/bin/env python3
"""Guarded apply of the Jeremiah CWO wave onto rows_v2 (275 rows) -> rows_v3.jsonl (built on the
_apply_author_jer.py guard pattern; E-18 execution parity; OW-2 item 4 role separation).
Run from SP/Jer. Modes: --check (guards only over whatever slices have landed; no write) |
--apply (every slice landed; every EXACT-arm row carries an op; writes rows_v3.jsonl + report).

Guards (hard-fail): rows_v2 sha pinned; every op is "replace" on a row inside its slice's assignment,
exactly once; no op outside the ordered set; IMMUTABLE fields byte-equal (decision_id, book, model_id,
chunk_index_in_book, span, parent_collection, unit_type, writer_part, writer_decision_id,
writer_attempt_id, non_authorizing, wj_or_red_letter_considered, frontier_flag_considered);
confidence/review_status changes only where an item's instruction or cwo_text names that field;
every changed field inside the CWO-open set (boundary_rationale, strongest_rejected_alternative,
device_notes, observed_substrate_signals, boundary_evidence_refs, literature_type_guess,
strong_or_hebrew_tags_used); no unexpanded {placeholder}; every field's TYPE matches the rows_v2
schema; in --apply every row carrying an EXACT-arm item has an op (heuristic-only rows may be
omitted = reported clean). Apply: replaces in place (order + chunk_index preserved, asserted 1..275),
writes rows_v3.jsonl, runs check_tiling over Jer.1.1-Jer.52.34 (must be GREEN), writes
_apply_cwo_report.json with the changed-fields histogram + per-row changed fields."""
import glob
import hashlib
import json
import re
import subprocess
import sys

CORPUS = "rows_v2.jsonl"
PINNED_SHA16 = "d66eef22bf895c7c"
OUT = "rows_v3.jsonl"
IMMUTABLE = ["decision_id", "book", "model_id", "chunk_index_in_book", "span", "parent_collection", "unit_type",
             "writer_part", "writer_decision_id", "writer_attempt_id", "non_authorizing",
             "wj_or_red_letter_considered", "frontier_flag_considered"]
CWO_OPEN = {"boundary_rationale", "strongest_rejected_alternative", "device_notes", "observed_substrate_signals",
            "boundary_evidence_refs", "literature_type_guess", "strong_or_hebrew_tags_used"}
NAMED_ONLY = {"confidence", "review_status"}
PLACEHOLDER = re.compile(r"\{[A-Za-z0-9_]+\}")
SPAN = re.compile(r"^Jer\.(\d+)\.(\d+)-Jer\.(\d+)\.(\d+)$")

mode = "--apply" if "--apply" in sys.argv else "--check"
raw = open(CORPUS, "rb").read()
sha16 = hashlib.sha256(raw).hexdigest()[:16]
assert sha16 == PINNED_SHA16, f"corpus sha {sha16} != pinned {PINNED_SHA16}"
rows = [json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]
by_id = {r["decision_id"]: r for r in rows}
assert len(rows) == 275, len(rows)
assert [r["chunk_index_in_book"] for r in rows] == list(range(1, 276))

ordered, exact_rows, order_text, slice_of = {}, set(), {}, {}
for f in sorted(glob.glob("cwo/orders_cwo_[0-9][0-9].json")):
    plan = json.load(open(f, encoding="utf-8"))
    for rid in plan["row_ids"]:
        assert rid not in ordered, f"{rid} ordered twice"
        o = plan["orders"][rid]
        ordered[rid] = o["op"]
        slice_of[rid] = plan["agent"]
        if any(it["arm"] == "exact" for it in o["items"]):
            exact_rows.add(rid)
        order_text[rid] = json.dumps({"items": o["items"], "cwo_texts": o["cwo_texts"]}, ensure_ascii=False).lower()
assert len(ordered) == 165, len(ordered)
assert all(v == "replace" for v in ordered.values())

ops, landed_slices = {}, set()
for path in sorted(glob.glob("cwo/cwo_[0-9][0-9].jsonl")):   # slices only; the unify layer loads below
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
for path in sorted(glob.glob("cwo/cwo_unify_c[0-9].jsonl")):   # deterministic systemic layer (orchestrator; E-17 consistency); supersedes slice ops row-wise
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
    n_slices = len(glob.glob("cwo/orders_cwo_[0-9][0-9].json"))
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
    if "unify" not in path and slice_of[rid] not in path.replace("\\", "/").replace("cwo/cwo_", "cwo").replace(".jsonl", ""):
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
    changed = [k for k in orig if json.dumps(rep.get(k), ensure_ascii=False, sort_keys=True)
               != json.dumps(orig.get(k), ensure_ascii=False, sort_keys=True)]
    changed_union[rid] = changed
    for k in IMMUTABLE:
        if k in changed:
            failures.append(f"{rid} immutable field changed: {k} ({orig.get(k)!r} -> {rep.get(k)!r})")
    for k in NAMED_ONLY:
        if k in changed and k not in order_text.get(rid, ""):
            failures.append(f"{rid} {k} change not named by its items ({orig[k]!r} -> {rep[k]!r})")
    out_of_scope = [k for k in changed if k not in CWO_OPEN and k not in NAMED_ONLY and k not in IMMUTABLE]
    if out_of_scope:
        failures.append(f"{rid} changed fields outside the CWO-open set: {out_of_scope}")
    if not SPAN.match(rep.get("span", "")):
        failures.append(f"{rid} malformed span {rep.get('span')!r}")

summary = {"mode": mode, "corpus_sha16": sha16, "ordered": len(ordered), "exact_arm_rows": len(exact_rows),
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
assert [r["chunk_index_in_book"] for r in new_rows] == list(range(1, 276))
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    for r in new_rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
sha_out = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
tiling = subprocess.run([sys.executable, "tools/check_tiling.py", OUT, "--range", "Jer.1.1-Jer.52.34"],
                        capture_output=True, text=True, encoding="utf-8")
report = {"status": "GREEN" if tiling.returncode == 0 else "RED_TILING", "rows_in": len(rows), "rows_out": len(new_rows),
          "replaced": len(ops), "ordered": len(ordered), "exact_arm_rows": len(exact_rows),
          "heuristic_only_rows_omitted": sorted(set(ordered) - set(ops)), "unify_layer_supersessions": superseded, "unify_layer_files": sorted(glob.glob("cwo/cwo_unify_c[0-9].jsonl")),
          "out": OUT, "out_sha256": sha_out, "corpus_sha16": sha16,
          "tiling": "GREEN" if tiling.returncode == 0 else (tiling.stdout or tiling.stderr)[-500:],
          "changed_fields_histogram": {f: sum(1 for c in changed_union.values() if f in c) for f in
                                       sorted({x for c in changed_union.values() for x in c})},
          "changed_fields_union": {r: c for r, c in sorted(changed_union.items())}}
with open("_apply_cwo_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in report.items() if k != "changed_fields_union"}, ensure_ascii=False, indent=1))
sys.exit(0 if report["status"] == "GREEN" else 1)
