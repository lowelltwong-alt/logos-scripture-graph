#!/usr/bin/env python3
"""Guarded apply of the Jeremiah author wave onto the frozen 276-row corpus (Isa
_apply_author.py lineage, adapted to the Jer orders schema + the seven boss adoptions).
Run from SP/Jer.  Modes: --check (guards only, over whatever patch files have landed;
no write) | --apply (all 220 orders must be present; writes rows_v2.jsonl + report).

Guards (hard-fail): frozen corpus sha pinned; every landed op maps to an ordered row with the
ordered op, exactly once; in --apply every ordered row is accounted (217 replace + 2 retire +
1 new_row); immutable fields byte-equal on replace rows; span changes ONLY on the boss-adopted
rows with EXACT boss targets (and those rows MUST carry the target); unit_type changes only on
P06-011 (boss B2-5) or where the embedded order text names unit_type; parent_collection never
changes; frontier flag never True->False; confidence changes only where the embedded order
text names confidence; every changed field named in the embedded order text or in the
always-open prose set; the new row P02-017b exact (span Jer.6.8-Jer.6.8, judgment_oracle,
M1, p02, chunk_index sentinel 0); retires exactly {P06-012, P14-008}; no unexpanded
{placeholder}; every field's TYPE matches the frozen schema (string fields stay strings, list fields stay lists). Apply: replaces in place, drops retires, inserts
the new row, renumbers chunk_index_in_book 1..275 by span order, writes rows_v2.jsonl, runs
check_tiling over Jer.1.1-Jer.52.34 (must be GREEN), writes _apply_author_report.json with the
changed-fields histogram."""
import glob
import hashlib
import json
import re
import subprocess
import sys

CORPUS = "draft_rows_combined.jsonl"
PINNED_SHA16 = None   # filled at first run from the frozen corpus; asserted against FROZEN_SHA below
FROZEN_SHA16 = "b565f9ccc84ed708"
OUT = "rows_v2.jsonl"
RETIRES = {"P06-012", "P14-008"}
NEW_ROWS = {"P02-017b": {"span": "Jer.6.8-Jer.6.8", "unit_type": "judgment_oracle",
                         "parent_collection": "M1 Jer.1.4-Jer.6.30", "writer_part": "p02"}}
SPAN_TARGETS = {
    "P02-017": "Jer.6.6-Jer.6.7",
    "P03-007": "Jer.8.18-Jer.9.3", "P03-008": "Jer.9.4-Jer.9.6",
    "P06-011": "Jer.18.1-Jer.18.17",
    "P10-012": "Jer.29.15-Jer.29.19", "P10-013": "Jer.29.20-Jer.29.23",
    "P14-007": "Jer.38.14-Jer.38.23",
    "P18-005": "Jer.49.14-Jer.49.19", "P18-006": "Jer.49.20-Jer.49.22",
    "P18-008": "Jer.49.28-Jer.49.29", "P18-009": "Jer.49.30-Jer.49.33",
}
UNIT_TYPE_TARGETS = {"P06-011": "symbolic_act_report"}
IMMUTABLE = ["decision_id", "book", "model_id", "chunk_index_in_book", "writer_part",
             "writer_decision_id", "writer_attempt_id", "non_authorizing", "parent_collection",
             "wj_or_red_letter_considered"]
ALWAYS_OPEN = {"boundary_rationale", "boundary_evidence_refs", "strongest_rejected_alternative",
               "device_notes", "observed_substrate_signals", "literature_type_guess", "review_status",
               "strong_or_hebrew_tags_used"}
PLACEHOLDER = re.compile(r"\{[A-Za-z0-9_]+\}")
SPAN = re.compile(r"^Jer\.(\d+)\.(\d+)-Jer\.(\d+)\.(\d+)$")

mode = "--apply" if "--apply" in sys.argv else "--check"
raw = open(CORPUS, "rb").read()
sha16 = hashlib.sha256(raw).hexdigest()[:16]
if FROZEN_SHA16 != "__FROZEN__":
    assert sha16 == FROZEN_SHA16, f"corpus sha {sha16} != pinned {FROZEN_SHA16}"
rows = [json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]
by_id = {r["writer_decision_id"]: r for r in rows}
assert len(rows) == 276, len(rows)

ordered, order_text = {}, {}
for f in sorted(glob.glob("author/orders_a*.json")):
    plan = json.load(open(f, encoding="utf-8"))
    for rid, o in plan["orders"].items():
        assert rid not in ordered, f"{rid} ordered twice"
        ordered[rid] = o["op"]
        order_text[rid] = json.dumps({k: o[k] for k in ("docket", "boss_rulings") if k in o}, ensure_ascii=False).lower()
assert len(ordered) == 220, len(ordered)

ops = {}
for path in sorted(glob.glob("author/author_a*.jsonl")):
    for i, line in enumerate(open(path, encoding="utf-8-sig"), 1):
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        rid = o.get("writer_decision_id") or o.get("decision_id")
        if rid in ops:
            sys.exit(f"FAIL duplicate op for {rid} ({path} line {i})")
        ops[rid] = (o, path)

failures, changed_union = [], {}
extra = set(ops) - set(ordered)
if extra:
    failures.append(f"ops for un-ordered rows: {sorted(extra)}")
if mode == "--apply":
    missing = set(ordered) - set(ops)
    if missing:
        failures.append(f"ordered rows without ops: {sorted(missing)}")


def is_placeholder_free(obj):
    return not PLACEHOLDER.search(json.dumps(obj, ensure_ascii=False))


for rid, (o, path) in sorted(ops.items()):
    op = o.get("_op")
    if op != ordered.get(rid):
        failures.append(f"{rid} op {op} != ordered {ordered.get(rid)}"); continue
    if op == "retire":
        if rid not in RETIRES:
            failures.append(f"{rid} illegal retire")
        continue
    rep = {k: v for k, v in o.items() if k != "_op"}
    if not is_placeholder_free(rep):
        failures.append(f"{rid} carries an unexpanded {{placeholder}} token")
    ref_row = by_id.get(rid) or next(iter(by_id.values()))
    for k, v in rep.items():
        if k in ref_row and type(v) is not type(ref_row[k]):
            failures.append(f"{rid} field {k} type {type(v).__name__} != frozen-schema type {type(ref_row[k]).__name__}")
    if op == "new_row":
        spec = NEW_ROWS.get(rid)
        if spec is None:
            failures.append(f"{rid} unauthorized new_row"); continue
        for k, want in spec.items():
            if rep.get(k) != want:
                failures.append(f"{rid} new_row {k} {rep.get(k)!r} != boss {want!r}")
        if rep.get("chunk_index_in_book") != 0:
            failures.append(f"{rid} new_row chunk_index sentinel must be 0")
        continue
    orig = by_id[rid]
    changed = [k for k in orig if json.dumps(rep.get(k), ensure_ascii=False, sort_keys=True)
               != json.dumps(orig.get(k), ensure_ascii=False, sort_keys=True)]
    changed_union[rid] = changed
    for k in IMMUTABLE:
        if k in changed:
            failures.append(f"{rid} immutable field changed: {k} ({orig.get(k)!r} -> {rep.get(k)!r})")
    if "span" in changed:
        tgt = SPAN_TARGETS.get(rid)
        if tgt is None:
            failures.append(f"{rid} span change not authorized ({orig['span']} -> {rep['span']})")
        elif rep["span"] != tgt:
            failures.append(f"{rid} span {rep['span']} != boss target {tgt}")
    elif rid in SPAN_TARGETS and rep.get("span") != SPAN_TARGETS[rid]:
        failures.append(f"{rid} expected boss span {SPAN_TARGETS[rid]}, still {rep.get('span')}")
    if "unit_type" in changed:
        if rid in UNIT_TYPE_TARGETS:
            if rep["unit_type"] != UNIT_TYPE_TARGETS[rid]:
                failures.append(f"{rid} unit_type {rep['unit_type']} != boss target {UNIT_TYPE_TARGETS[rid]}")
        elif "unit_type" not in order_text.get(rid, ""):
            failures.append(f"{rid} unit_type change not named by its order ({orig['unit_type']} -> {rep['unit_type']})")
    elif rid in UNIT_TYPE_TARGETS and rep.get("unit_type") != UNIT_TYPE_TARGETS[rid]:
        failures.append(f"{rid} expected boss unit_type {UNIT_TYPE_TARGETS[rid]}, still {rep.get('unit_type')}")
    if "confidence" in changed and "confidence" not in order_text.get(rid, ""):
        failures.append(f"{rid} confidence change not named by its order ({orig['confidence']} -> {rep['confidence']})")
    if "frontier_flag_considered" in changed:
        if str(orig["frontier_flag_considered"]) == "True" and str(rep["frontier_flag_considered"]) != "True":
            failures.append(f"{rid} frontier flag True->non-True")
    out_of_scope = [k for k in changed if k not in ALWAYS_OPEN
                    and k not in ("span", "unit_type", "confidence", "frontier_flag_considered")
                    and k.lower() not in order_text.get(rid, "")]
    if out_of_scope:
        failures.append(f"{rid} changed fields outside order scope: {out_of_scope}")
    if not SPAN.match(rep.get("span", "")):
        failures.append(f"{rid} malformed span {rep.get('span')!r}")

summary = {"mode": mode, "corpus_sha16": sha16, "ordered": len(ordered), "ops_landed": len(ops),
           "landed_by_op": {k: sum(1 for o, _ in ops.values() if o.get("_op") == k) for k in ("replace", "retire", "new_row")},
           "failures": failures}
if failures or mode == "--check":
    summary["status"] = "RED" if failures else "GREEN"
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    print("changed-fields histogram:", json.dumps(
        {f: sum(1 for c in changed_union.values() if f in c) for f in
         sorted({x for c in changed_union.values() for x in c})}))
    sys.exit(1 if failures else 0)

new_rows = []
for r in rows:
    rid = r["writer_decision_id"]
    if rid in RETIRES:
        continue
    if rid in ops and ops[rid][0].get("_op") == "replace":
        new_rows.append({k: v for k, v in ops[rid][0].items() if k != "_op"})
    else:
        new_rows.append(r)
for rid, (o, _p) in ops.items():
    if o.get("_op") == "new_row":
        new_rows.append({k: v for k, v in o.items() if k != "_op"})


def span_key(r):
    m = SPAN.match(r["span"]); return (int(m.group(1)), int(m.group(2)))


new_rows.sort(key=span_key)
for i, r in enumerate(new_rows, 1):
    r["chunk_index_in_book"] = i
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    for r in new_rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
sha_out = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
tiling = subprocess.run([sys.executable, "tools/check_tiling.py", OUT, "--range", "Jer.1.1-Jer.52.34"],
                        capture_output=True, text=True, encoding="utf-8")
report = {"status": "GREEN" if tiling.returncode == 0 else "RED_TILING", "rows_in": len(rows), "rows_out": len(new_rows),
          "replaced": summary["landed_by_op"]["replace"], "retired": sorted(RETIRES), "new_rows": sorted(NEW_ROWS),
          "out": OUT, "out_sha256": sha_out, "corpus_sha16": sha16,
          "tiling": "GREEN" if tiling.returncode == 0 else (tiling.stdout or tiling.stderr)[-500:],
          "changed_fields_histogram": {f: sum(1 for c in changed_union.values() if f in c) for f in
                                       sorted({x for c in changed_union.values() for x in c})},
          "changed_fields_union": {r: c for r, c in sorted(changed_union.items())}}
with open("_apply_author_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in report.items() if k != "changed_fields_union"}, ensure_ascii=False, indent=1))
sys.exit(0 if report["status"] == "GREEN" else 1)
