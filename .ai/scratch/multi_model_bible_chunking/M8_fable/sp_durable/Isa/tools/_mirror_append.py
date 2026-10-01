"""Append argued-but-unmirrored refs (from the last validator report) to
boundary_evidence_refs in the witness form the row's prose uses (bare = WEB).
Edits rows_v4.jsonl in place. Run from SP/Isa."""
import json

rep = json.load(open("rows_v4.jsonl.validator_report.json", encoding="utf-8"))
rm = rep.get("refs_mirror", {})
flags = rm.get("flags") or rm.get("warnings") or []
missing = {f["decision_id"]: f["argued_but_unmirrored"] for f in flags}
rows = [json.loads(l) for l in open("rows_v4.jsonl", encoding="utf-8")]
log = {}
for r in rows:
    rid = r["writer_decision_id"]
    if rid not in missing:
        continue
    prose = " ".join(str(r.get(k, "")) for k in
                     ("boundary_rationale", "device_notes", "strongest_rejected_alternative"))
    added = []
    for tok in missing[rid]:
        if f"oshb:{tok}" in prose and f"web:{tok}" not in prose:
            form = f"oshb:{tok}"
        else:
            form = f"web:{tok}"
        if form not in r["boundary_evidence_refs"]:
            r["boundary_evidence_refs"].append(form)
            added.append(form)
    log[rid] = added
with open("rows_v4.jsonl", "w", encoding="utf-8", newline="\n") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(json.dumps(log, ensure_ascii=False, indent=1))
