"""Guarded merge of micro-round outputs onto rows_v2m.jsonl -> rows_v3.jsonl.

Files apply in sorted filename order; a later file's row supersedes an earlier one's
(last-wins, logged). Guards: _op=replace only; row must exist; ONLY prose fields
(boundary_rationale, device_notes, strongest_rejected_alternative) plus
boundary_evidence_refs and observed_substrate_signals may change vs the CURRENT
corpus state; everything else byte-immutable. Run from SP/Isa.
"""
import json, glob, hashlib, sys

ALLOWED = {"boundary_rationale", "device_notes", "strongest_rejected_alternative",
           "boundary_evidence_refs", "observed_substrate_signals"}
rows = [json.loads(l) for l in open("rows_v2m.jsonl", encoding="utf-8")]
by_id = {r["writer_decision_id"]: r for r in rows}
failures, applied, overrides = [], {}, []
for path in sorted(glob.glob("author/micro_m*.jsonl")):
    for i, line in enumerate(open(path, encoding="utf-8")):
        line = line.strip()
        if not line: continue
        o = json.loads(line)
        rid = o.get("writer_decision_id")
        if o.get("_op") != "replace":
            failures.append(f"{path}:{i+1} {rid} illegal op {o.get('_op')!r}"); continue
        if rid not in by_id:
            failures.append(f"{path} {rid} not in corpus"); continue
        rep = {k: v for k, v in o.items() if k != "_op"}
        cur = by_id[rid]
        changed = [k for k in cur if json.dumps(rep.get(k), ensure_ascii=False, sort_keys=True)
                   != json.dumps(cur.get(k), ensure_ascii=False, sort_keys=True)]
        bad = [k for k in changed if k not in ALLOWED]
        if bad:
            failures.append(f"{path} {rid} illegal field changes: {bad}"); continue
        if rid in applied:
            overrides.append(f"{rid}: {applied[rid]} -> {path}")
        applied[rid] = path
        by_id[rid] = rep
if failures:
    print(json.dumps({"status": "RED", "failures": failures}, indent=1)); sys.exit(1)
out_rows = [by_id[r["writer_decision_id"]] for r in rows]
with open("rows_v3.jsonl", "w", encoding="utf-8", newline="\n") as f:
    for r in out_rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
sha = hashlib.sha256(open("rows_v3.jsonl", "rb").read()).hexdigest()[:16]
print(json.dumps({"status": "GREEN", "rows": len(out_rows), "rows_replaced": len(applied),
                  "overrides": overrides, "out": "rows_v3.jsonl", "sha16": sha}, indent=1))
