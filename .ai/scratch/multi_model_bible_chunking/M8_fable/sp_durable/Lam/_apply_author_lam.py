#!/usr/bin/env python3
"""Guarded apply of the Lamentations author wave onto the frozen corpus (the Jer _apply_author_jer.py lineage with the
hand-coded boss targets replaced by author_overrides.json: {"retires": {row: ruling}, "new_rows": {row: {"span", "unit_type",
"parent_collection", "writer_part"}}, "span_targets": {row: span}, "unit_type_targets": {row: unit_type}}). Run from
SP/Lam. Modes: --check | --apply. --pin <sha16> pins the frozen corpus (draft_rows_combined.jsonl). Guards (hard-fail):
corpus sha pinned; every landed op maps to an ordered row with the ordered op, exactly once; in --apply every ordered row
is accounted; immutable fields byte-equal on replace rows; span changes ONLY on rows with a boss span target (and those
rows MUST carry the target; every new seam on a poem boundary or letter/triplet boundary is the boss's law, checked by the
sweep and the postcheck); unit_type changes only where a boss target or the embedded order names unit_type;
parent_collection never changes; frontier flag never True->non-True; confidence changes only where the order names
confidence; every changed field named in the embedded order text or in the always-open prose set; new rows exact to their
spec with chunk_index sentinel 0; retires exactly the override set; no unexpanded {placeholder}; type parity. Apply:
replace in place, drop retires, insert new rows, renumber chunk_index_in_book 1..N by span order, write rows_v2.jsonl,
check_tiling over Lam.1.1-Lam.5.22 (must be GREEN), write _apply_author_report.json."""
import glob, hashlib, json, re, subprocess, sys
CORPUS = "draft_rows_combined.jsonl"; OUT = "rows_v2.jsonl"
A = sys.argv[1:]; PIN = A[A.index("--pin") + 1] if "--pin" in A else None
ov = json.load(open("author_overrides.json", encoding="utf-8")) if glob.glob("author_overrides.json") else {}
RETIRES = set(ov.get("retires", {})); NEW_ROWS = ov.get("new_rows", {}); SPAN_TARGETS = ov.get("span_targets", {}); UNIT_TYPE_TARGETS = ov.get("unit_type_targets", {})
IMMUTABLE = ["decision_id", "book", "model_id", "chunk_index_in_book", "writer_part", "writer_decision_id", "writer_attempt_id", "non_authorizing", "parent_collection", "wj_or_red_letter_considered"]
ALWAYS_OPEN = {"boundary_rationale", "boundary_evidence_refs", "strongest_rejected_alternative", "device_notes", "observed_substrate_signals", "literature_type_guess", "review_status", "strong_or_hebrew_tags_used"}
PLACEHOLDER = re.compile(r"\{[A-Za-z0-9_]+\}"); SPAN = re.compile(r"^Lam\.(\d+)\.(\d+)-Lam\.(\d+)\.(\d+)$")
mode = "--apply" if "--apply" in A else "--check"
raw = open(CORPUS, "rb").read(); sha16 = hashlib.sha256(raw).hexdigest()[:16]
assert PIN, "pass --pin <sha16 of the frozen corpus>"; assert sha16 == PIN, f"corpus sha {sha16} != pinned {PIN}"
rows = [json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]; by_id = {r["writer_decision_id"]: r for r in rows}; N = len(rows)
ordered, order_text, out_files = {}, {}, []
for f in sorted(glob.glob("author/orders_a*.json")):
    plan = json.load(open(f, encoding="utf-8"))
    out_files.append(plan["output_file"])   # 2026-09-07 s3: the ORDERED output file per agent, never a bare glob - a split attempt writes author_aNN_aK.jsonl and is byte-merged into the agent file before the apply, so a glob would double-count its rows
    for rid, o in plan["orders"].items():
        assert rid not in ordered, f"{rid} ordered twice"; ordered[rid] = o["op"]; order_text[rid] = json.dumps({k: o[k] for k in ("docket", "boss_rulings") if k in o}, ensure_ascii=False).lower()
ops = {}
for path in sorted(out_files):
    for i, line in enumerate(open(path, encoding="utf-8-sig"), 1):
        line = line.strip()
        if not line: continue
        o = json.loads(line); rid = o.get("writer_decision_id") or o.get("decision_id")
        if rid in ops: sys.exit(f"FAIL duplicate op for {rid} ({path} line {i})")
        ops[rid] = (o, path)
failures, changed_union = [], {}
extra = set(ops) - set(ordered)
if extra: failures.append(f"ops for un-ordered rows: {sorted(extra)}")
if mode == "--apply":
    missing = set(ordered) - set(ops)
    if missing: failures.append(f"ordered rows without ops: {sorted(missing)}")
for rid, (o, path) in sorted(ops.items()):
    op = o.get("_op")
    if op != ordered.get(rid): failures.append(f"{rid} op {op} != ordered {ordered.get(rid)}"); continue
    if op == "retire":
        if rid not in RETIRES: failures.append(f"{rid} illegal retire")
        continue
    rep = {k: v for k, v in o.items() if k != "_op"}
    if PLACEHOLDER.search(json.dumps(rep, ensure_ascii=False)): failures.append(f"{rid} carries an unexpanded placeholder token")
    ref_row = by_id.get(rid) or next(iter(by_id.values()))
    for k, v in rep.items():
        if k in ref_row and type(v) is not type(ref_row[k]): failures.append(f"{rid} field {k} type {type(v).__name__} != frozen-schema type {type(ref_row[k]).__name__}")
    if op == "new_row":
        spec = NEW_ROWS.get(rid)
        if spec is None: failures.append(f"{rid} unauthorized new_row"); continue
        for k, want in spec.items():
            if rep.get(k) != want: failures.append(f"{rid} new_row {k} {rep.get(k)!r} != boss {want!r}")
        if rep.get("chunk_index_in_book") != 0: failures.append(f"{rid} new_row chunk_index sentinel must be 0")
        if set(rep) != set(ref_row): failures.append(f"{rid} new_row schema mismatch missing={sorted(set(ref_row) - set(rep))} extra={sorted(set(rep) - set(ref_row))}")
        continue
    orig = by_id[rid]
    if set(rep) != set(orig): failures.append(f"{rid} schema mismatch missing={sorted(set(orig) - set(rep))} extra={sorted(set(rep) - set(orig))}"); continue
    changed = [k for k in orig if json.dumps(rep.get(k), ensure_ascii=False, sort_keys=True) != json.dumps(orig.get(k), ensure_ascii=False, sort_keys=True)]
    changed_union[rid] = changed
    for k in IMMUTABLE:
        if k in changed: failures.append(f"{rid} immutable field changed: {k} ({orig.get(k)!r} -> {rep.get(k)!r})")
    if "span" in changed:
        tgt = SPAN_TARGETS.get(rid)
        if tgt is None: failures.append(f"{rid} span change not authorized ({orig['span']} -> {rep['span']})")
        elif rep["span"] != tgt: failures.append(f"{rid} span {rep['span']} != boss target {tgt}")
    elif rid in SPAN_TARGETS and rep.get("span") != SPAN_TARGETS[rid]: failures.append(f"{rid} expected boss span {SPAN_TARGETS[rid]}, still {rep.get('span')}")
    if "unit_type" in changed:
        if rid in UNIT_TYPE_TARGETS:
            if rep["unit_type"] != UNIT_TYPE_TARGETS[rid]: failures.append(f"{rid} unit_type {rep['unit_type']} != boss target {UNIT_TYPE_TARGETS[rid]}")
        elif "unit_type" not in order_text.get(rid, ""): failures.append(f"{rid} unit_type change not named by its order ({orig['unit_type']} -> {rep['unit_type']})")
    elif rid in UNIT_TYPE_TARGETS and rep.get("unit_type") != UNIT_TYPE_TARGETS[rid]: failures.append(f"{rid} expected boss unit_type {UNIT_TYPE_TARGETS[rid]}, still {rep.get('unit_type')}")
    if "confidence" in changed and "confidence" not in order_text.get(rid, ""): failures.append(f"{rid} confidence change not named by its order ({orig['confidence']} -> {rep['confidence']})")
    if "frontier_flag_considered" in changed and str(orig["frontier_flag_considered"]) == "True" and str(rep["frontier_flag_considered"]) != "True": failures.append(f"{rid} frontier flag True->non-True")
    oos = [k for k in changed if k not in ALWAYS_OPEN and k not in ("span", "unit_type", "confidence", "frontier_flag_considered") and k.lower() not in order_text.get(rid, "")]
    if oos: failures.append(f"{rid} changed fields outside order scope: {oos}")
    if not SPAN.match(rep.get("span", "")): failures.append(f"{rid} malformed span {rep.get('span')!r}")
summary = {"mode": mode, "corpus_sha16": sha16, "rows_in": N, "ordered": len(ordered), "ops_landed": len(ops), "landed_by_op": {k: sum(1 for o, _ in ops.values() if o.get("_op") == k) for k in ("replace", "retire", "new_row")}, "failures": failures}
if failures or mode == "--check":
    summary["status"] = "RED" if failures else "GREEN"; print(json.dumps(summary, ensure_ascii=False, indent=1))
    print("changed-fields histogram:", json.dumps({f: sum(1 for c in changed_union.values() if f in c) for f in sorted({x for c in changed_union.values() for x in c})})); sys.exit(1 if failures else 0)
new_rows = []
for r in rows:
    rid = r["writer_decision_id"]
    if rid in RETIRES: continue
    new_rows.append({k: v for k, v in ops[rid][0].items() if k != "_op"} if rid in ops and ops[rid][0].get("_op") == "replace" else r)
for rid, (o, _p) in ops.items():
    if o.get("_op") == "new_row": new_rows.append({k: v for k, v in o.items() if k != "_op"})
def span_key(r): m = SPAN.match(r["span"]); return (int(m.group(1)), int(m.group(2)))
new_rows.sort(key=span_key)
for i, r in enumerate(new_rows, 1): r["chunk_index_in_book"] = i
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    for r in new_rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
sha_out = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
tiling = subprocess.run([sys.executable, "tools/check_tiling.py", OUT, "--range", "Lam.1.1-Lam.5.22"], capture_output=True, text=True, encoding="utf-8")
report = {"status": "GREEN" if tiling.returncode == 0 else "RED_TILING", "rows_in": N, "rows_out": len(new_rows), "replaced": summary["landed_by_op"]["replace"], "retired": sorted(RETIRES), "new_rows": sorted(NEW_ROWS), "out": OUT, "out_sha256": sha_out, "corpus_sha16": sha16,
          "tiling": "GREEN" if tiling.returncode == 0 else (tiling.stdout or tiling.stderr)[-500:], "changed_fields_histogram": {f: sum(1 for c in changed_union.values() if f in c) for f in sorted({x for c in changed_union.values() for x in c})}, "changed_fields_union": {r: c for r, c in sorted(changed_union.items())}}
with open("_apply_author_report.json", "w", encoding="utf-8") as f: json.dump(report, f, ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in report.items() if k != "changed_fields_union"}, ensure_ascii=False, indent=1)); sys.exit(0 if report["status"] == "GREEN" else 1)
