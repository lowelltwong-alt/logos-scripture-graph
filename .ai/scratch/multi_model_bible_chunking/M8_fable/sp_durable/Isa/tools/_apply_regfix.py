"""Guarded merge of register-fix outputs onto rows_v3.jsonl -> rows_v4.jsonl.
Same guards as _apply_micro: replace-only, prose+refs fields only, last-wins logged.
Run from SP/Isa."""
import json, glob, hashlib, sys

ALLOWED = {"boundary_rationale", "device_notes", "strongest_rejected_alternative",
           "boundary_evidence_refs", "observed_substrate_signals"}
rows = [json.loads(l) for l in open("rows_v3.jsonl", encoding="utf-8")]
by_id = {r["writer_decision_id"]: r for r in rows}
failures, applied, overrides = [], {}, []
for path in sorted(glob.glob("author/regfix_f*.jsonl")):
    for i, line in enumerate(open(path, encoding="utf-8-sig")):
        line = line.strip()
        if not line: continue
        o = json.loads(line)
        rid = o.get("writer_decision_id")
        if o.get("_op") != "replace":
            failures.append(f"{path}:{i+1} {rid} illegal op"); continue
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
with open("rows_v4.jsonl", "w", encoding="utf-8", newline="\n") as f:
    for r in out_rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
sha = hashlib.sha256(open("rows_v4.jsonl", "rb").read()).hexdigest()[:16]
print(json.dumps({"status": "GREEN", "rows": len(out_rows), "rows_replaced": len(applied),
                  "overrides": overrides, "out": "rows_v4.jsonl", "sha16": sha}, indent=1))
