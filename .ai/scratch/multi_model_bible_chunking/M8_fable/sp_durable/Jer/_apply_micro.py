#!/usr/bin/env python3
"""Guarded apply of the Jeremiah micro round onto rows_v3 -> rows_v4.jsonl (the _apply_cwo.py guard pattern).
Run from SP/Jer. Modes: --check | --apply. Guards: rows_v3 sha pinned; every op is "replace" on a row inside its
micro slice's assignment, exactly once; a deterministic unify layer spot/micro_unify_c[0-9].jsonl (orchestrator; observed_substrate_signals ONLY, may touch un-ordered rows,
supersedes slice ops row-wise); IMMUTABLE fields byte-equal (decision_id, book, model_id, chunk_index_in_book,
span, parent_collection, unit_type, confidence, writer_*, non_authorizing, wj_or_red_letter_considered,
frontier_flag_considered); every changed field inside the micro-open set (boundary_rationale,
strongest_rejected_alternative, device_notes, observed_substrate_signals, boundary_evidence_refs,
literature_type_guess, strong_or_hebrew_tags_used, review_status); no placeholder; type parity; in --apply every
ordered row has an op. Apply: replace in place (order + chunk_index preserved), write rows_v4.jsonl, check_tiling
GREEN, write _apply_micro_report.json."""
import glob, hashlib, json, re, subprocess, sys
CORPUS = "rows_v3.jsonl"; OUT = "rows_v4.jsonl"
IMMUTABLE = ["decision_id", "book", "model_id", "chunk_index_in_book", "span", "parent_collection", "unit_type", "confidence",
             "writer_part", "writer_decision_id", "writer_attempt_id", "non_authorizing", "wj_or_red_letter_considered", "frontier_flag_considered"]
OPEN = {"boundary_rationale", "strongest_rejected_alternative", "device_notes", "observed_substrate_signals", "boundary_evidence_refs", "literature_type_guess", "strong_or_hebrew_tags_used", "review_status"}
PLACEHOLDER = re.compile(r"\{[A-Za-z0-9_]+\}"); SPAN = re.compile(r"^Jer\.(\d+)\.(\d+)-Jer\.(\d+)\.(\d+)$")
mode = "--apply" if "--apply" in sys.argv else "--check"
raw = open(CORPUS, "rb").read(); sha16 = hashlib.sha256(raw).hexdigest()[:16]
PIN = "bd04e0b572b3d1b0"
assert sha16 == PIN, f"corpus sha {sha16} != pinned {PIN}"
rows = [json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]; by_id = {r["decision_id"]: r for r in rows}
assert len(rows) == 275 and [r["chunk_index_in_book"] for r in rows] == list(range(1, 276))
ordered, slice_of = {}, {}
for f in sorted(glob.glob("spot/orders_micro_[0-9][0-9].json")):
    plan = json.load(open(f, encoding="utf-8"))
    for rid in plan["row_ids"]:
        assert rid not in ordered, f"{rid} ordered twice"; ordered[rid] = "replace"; slice_of[rid] = plan["agent"]
ops = {}
for path in sorted(glob.glob("spot/micro_[0-9][0-9].jsonl")):
    for i, line in enumerate(open(path, encoding="utf-8-sig"), 1):
        line = line.strip()
        if not line: continue
        o = json.loads(line); rid = o.get("decision_id")
        if rid in ops: sys.exit(f"FAIL duplicate op for {rid} ({path} line {i})")
        ops[rid] = (o, path)
superseded, unify_rows, slice_rep = [], set(), {}
for path in sorted(glob.glob("spot/micro_unify_c[0-9].jsonl")):   # deterministic systemic layer (orchestrator; E-17 cross-row key consistency, gate-verified placement); supersedes slice ops row-wise; observed_substrate_signals ONLY
    for i, line in enumerate(open(path, encoding="utf-8-sig"), 1):
        line = line.strip()
        if not line: continue
        o = json.loads(line); rid = o.get("decision_id")
        if rid in ops: superseded.append({"row": rid, "slice_file": ops[rid][1], "by": path}); slice_rep[rid] = {k: v for k, v in ops[rid][0].items() if k != "_op"}
        ops[rid] = (o, path); unify_rows.add(rid)
failures, changed_union = [], {}
extra = set(ops) - set(ordered) - unify_rows
if extra: failures.append(f"ops for un-ordered rows: {sorted(extra)}")
if mode == "--apply":
    missing = sorted(set(ordered) - set(ops))
    if missing: failures.append(f"ordered rows without ops: {missing}")
for rid, (o, path) in sorted(ops.items()):
    if o.get("_op") != "replace": failures.append(f"{rid} op {o.get('_op')!r} != replace"); continue
    if rid not in ordered and rid not in unify_rows: continue
    if "unify" not in path and slice_of[rid].replace("m", "micro_") not in path.replace("\\", "/"): failures.append(f"{rid} landed in {path} but ordered on {slice_of[rid]}")
    rep = {k: v for k, v in o.items() if k != "_op"}
    if PLACEHOLDER.search(json.dumps(rep, ensure_ascii=False)): failures.append(f"{rid} carries an unexpanded placeholder")
    orig = by_id[rid]
    if set(rep) != set(orig): failures.append(f"{rid} schema mismatch missing={sorted(set(orig)-set(rep))} extra={sorted(set(rep)-set(orig))}"); continue
    for k, v in rep.items():
        if type(v) is not type(orig[k]): failures.append(f"{rid} field {k} type {type(v).__name__} != {type(orig[k]).__name__}")
    changed = [k for k in orig if json.dumps(rep.get(k), ensure_ascii=False, sort_keys=True) != json.dumps(orig.get(k), ensure_ascii=False, sort_keys=True)]
    changed_union[rid] = changed
    for k in IMMUTABLE:
        if k in changed: failures.append(f"{rid} immutable field changed: {k} ({orig.get(k)!r} -> {rep.get(k)!r})")
    oos = [k for k in changed if k not in OPEN and k not in IMMUTABLE]
    if oos: failures.append(f"{rid} changed fields outside the micro-open set: {oos}")
    if "unify" in path:   # the layer supersedes the slice row it was built from: its OWN delta is measured against that row (or rows_v3 when no slice op exists)
        base = slice_rep.get(rid, orig); udelta = [k for k in base if json.dumps(rep.get(k), ensure_ascii=False, sort_keys=True) != json.dumps(base.get(k), ensure_ascii=False, sort_keys=True)]
        if [k for k in udelta if k != "observed_substrate_signals"]: failures.append(f"{rid} unify layer changed a field other than observed_substrate_signals (vs the superseded slice row): {udelta}")
    if not SPAN.match(rep.get("span", "")): failures.append(f"{rid} malformed span")
summary = {"mode": mode, "corpus_sha16": sha16, "ordered": len(ordered), "ops_landed": len(ops), "unify_layer_rows": sorted(unify_rows), "unify_layer_supersessions": superseded, "rows_unchanged_ops": sorted(r for r, c in changed_union.items() if not c), "failures": failures}
if failures or mode == "--check":
    summary["status"] = "RED" if failures else "GREEN"; print(json.dumps(summary, ensure_ascii=False, indent=1))
    print("changed-fields histogram:", json.dumps({f: sum(1 for c in changed_union.values() if f in c) for f in sorted({x for c in changed_union.values() for x in c})}))
    sys.exit(1 if failures else 0)
new_rows = [({k: v for k, v in ops[r["decision_id"]][0].items() if k != "_op"} if r["decision_id"] in ops else r) for r in rows]
assert [r["chunk_index_in_book"] for r in new_rows] == list(range(1, 276))
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    for r in new_rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
sha_out = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
tiling = subprocess.run([sys.executable, "tools/check_tiling.py", OUT, "--range", "Jer.1.1-Jer.52.34"], capture_output=True, text=True, encoding="utf-8")
report = {"status": "GREEN" if tiling.returncode == 0 else "RED_TILING", "rows_in": len(rows), "rows_out": len(new_rows), "replaced": len(ops), "ordered": len(ordered), "unify_layer_rows": sorted(unify_rows), "unify_layer_supersessions": superseded, "unify_layer_files": sorted(glob.glob("spot/micro_unify_c[0-9].jsonl")), "out": OUT, "out_sha256": sha_out, "corpus_sha16": sha16,
          "tiling": "GREEN" if tiling.returncode == 0 else (tiling.stdout or tiling.stderr)[-500:],
          "changed_fields_histogram": {f: sum(1 for c in changed_union.values() if f in c) for f in sorted({x for c in changed_union.values() for x in c})}, "changed_fields_union": {r: c for r, c in sorted(changed_union.items())}}
json.dump(report, open("_apply_micro_report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in report.items() if k != "changed_fields_union"}, ensure_ascii=False, indent=1)); sys.exit(0 if report["status"] == "GREEN" else 1)
