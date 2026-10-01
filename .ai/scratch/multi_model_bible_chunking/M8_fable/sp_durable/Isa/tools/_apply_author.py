"""Guarded apply of the author wave onto the frozen 225-row corpus. Run from SP/Isa.

Guards (hard-fail): corpus sha pinned; every one of the 200 ordered rows accounted
(198 replace + 2 retire, exactly once); immutable fields byte-equal; span changes only
on the four boss-adopted rows with exact boss targets; confidence changes only where
ordered (B-6 exact targets); frontier flag never True->False; changed-fields union
per row within the order's allowed set; boss strike-substrings absent post-apply.
Applies: replaces in canonical order, drops the two retires, renumbers
chunk_index_in_book 1..223, writes rows_v2.jsonl + _apply_author_report.json.
"""
import json, glob, hashlib, os, sys

CORPUS = "draft_rows_combined.jsonl"
PINNED_SHA16 = "bb7d0aed540114c4"
OUT = "rows_v2.jsonl"
RETIRES = {"P15-003", "P09-004"}
SPAN_TARGETS = {"P10-005": "Isa.36.21-Isa.36.22", "P10-006": "Isa.37.1-Isa.37.7",
                "P15-002": "Isa.53.1-Isa.53.12", "P09-003": "Isa.32.9-Isa.32.20"}
CONF_TARGETS = {r: "medium_low" for r in
                ["P02-009", "P03-014", "P04-008", "P05-005", "P05-009", "P09-001",
                 "P09-006", "P09-007", "P16-005", "P17-001", "P15-002", "P09-003"]}
CONF_FREE = {"P10-005", "P10-006"}  # boss ordered re-derive
FRONTIER_TRUE = {"P02-009", "P03-014", "P04-008", "P05-005", "P05-009", "P09-006",
                 "P09-007", "P16-005", "P17-001", "P15-002", "P09-003",
                 "P09-001", "P09-005", "P15-004"}
IMMUTABLE = ["decision_id", "book", "model_id", "chunk_index_in_book", "writer_part",
             "writer_decision_id", "writer_attempt_id", "non_authorizing",
             "parent_collection", "unit_type", "wj_or_red_letter_considered"]
STRIKES = {  # substrings that must be ABSENT from the named row post-apply (boss-ordered deletions)
    "P09-003": ["one sentence"],
    "P10-005": ["report-and-response", "chapter divisions never cutting"],
}

raw = open(CORPUS, "rb").read()
sha16 = hashlib.sha256(raw).hexdigest()[:16]
assert sha16 == PINNED_SHA16, f"corpus sha {sha16} != pinned {PINNED_SHA16}"
rows = [json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]
by_id = {r["writer_decision_id"]: r for r in rows}

allowed = {}
remedy_text = {}
ordered = set()
for f in sorted(glob.glob("author/orders_a*.json")):
    plan = json.load(open(f, encoding="utf-8"))
    for rid, o in plan["orders"].items():
        ordered.add(rid)
        allowed[rid] = set(o.get("allowed_fields", []))
        remedy_text[rid] = " ".join(str(o.get(k, "")) for k in
                                    ("remedy", "challenge_claim", "grounds")).lower()

ops = {}
for path in sorted(glob.glob("author/author_a*.jsonl")):
    for i, line in enumerate(open(path, encoding="utf-8")):
        line = line.strip()
        if not line: continue
        o = json.loads(line)
        rid = o["writer_decision_id"]
        if rid in ops: sys.exit(f"FAIL duplicate op for {rid} ({path})")
        ops[rid] = (o, path)

failures, changed_union = [], {}
missing = ordered - set(ops)
extra = set(ops) - ordered
if missing: failures.append(f"ordered rows without ops: {sorted(missing)}")
if extra: failures.append(f"ops for un-ordered rows: {sorted(extra)}")

for rid, (o, path) in sorted(ops.items()):
    if o.get("_op") == "retire":
        if rid not in RETIRES: failures.append(f"{rid} illegal retire")
        continue
    if rid in RETIRES:
        failures.append(f"{rid} must be retire"); continue
    orig = by_id[rid]
    rep = {k: v for k, v in o.items() if k != "_op"}
    changed = [k for k in orig if json.dumps(rep.get(k), ensure_ascii=False, sort_keys=True)
               != json.dumps(orig.get(k), ensure_ascii=False, sort_keys=True)]
    changed_union[rid] = changed
    for k in IMMUTABLE:
        if k in changed: failures.append(f"{rid} immutable field changed: {k}")
    if "span" in changed:
        tgt = SPAN_TARGETS.get(rid)
        if tgt is None: failures.append(f"{rid} span change not authorized ({orig['span']} -> {rep['span']})")
        elif rep["span"] != tgt: failures.append(f"{rid} span {rep['span']} != boss target {tgt}")
    elif rid in SPAN_TARGETS and rep.get("span") != SPAN_TARGETS[rid]:
        failures.append(f"{rid} expected boss span {SPAN_TARGETS[rid]}, still {rep.get('span')}")
    if "confidence" in changed:
        if rid in CONF_TARGETS:
            if rep["confidence"] != CONF_TARGETS[rid]:
                failures.append(f"{rid} confidence {rep['confidence']} != target {CONF_TARGETS[rid]}")
        elif rid not in CONF_FREE and "confidence" not in allowed.get(rid, set()):
            failures.append(f"{rid} confidence change not authorized ({orig['confidence']} -> {rep['confidence']})")
    elif rid in CONF_TARGETS and str(rep.get("confidence")) != CONF_TARGETS[rid]:
        failures.append(f"{rid} expected confidence {CONF_TARGETS[rid]}, still {rep.get('confidence')}")
    if "frontier_flag_considered" in changed:
        if str(orig["frontier_flag_considered"]) == "True" and str(rep["frontier_flag_considered"]) != "True":
            failures.append(f"{rid} frontier flag True->non-True")
    if rid in FRONTIER_TRUE and str(rep.get("frontier_flag_considered")) not in ("True", "true"):
        failures.append(f"{rid} frontier_flag_considered must end True")
    out_of_scope = [k for k in changed if k not in allowed.get(rid, set())
                    and k not in ("confidence", "frontier_flag_considered", "span")
                    and k.lower() not in remedy_text.get(rid, "")]
    if out_of_scope:
        failures.append(f"{rid} changed fields outside order scope: {out_of_scope}")
    for sub in STRIKES.get(rid, []):
        blob = json.dumps(rep, ensure_ascii=False)
        if sub.lower() in blob.lower():
            failures.append(f"{rid} boss-struck text still present: {sub!r}")

if failures:
    print(json.dumps({"status": "RED", "failures": failures}, indent=1)); sys.exit(1)

new_rows = []
for r in rows:
    rid = r["writer_decision_id"]
    if rid in RETIRES and rid in ops: continue
    if rid in ops and ops[rid][0].get("_op") == "replace":
        rep = {k: v for k, v in ops[rid][0].items() if k != "_op"}
        new_rows.append(rep)
    else:
        new_rows.append(r)
for i, r in enumerate(new_rows, 1):
    r["chunk_index_in_book"] = i
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    for r in new_rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
sha_out = hashlib.sha256(open(OUT, "rb").read()).hexdigest()[:16]
report = {"status": "GREEN", "rows_in": len(rows), "rows_out": len(new_rows),
          "replaced": sum(1 for _, (o, _p) in ops.items() if o.get("_op") == "replace"),
          "retired": sorted(r for r in RETIRES if r in ops), "out": OUT, "out_sha16": sha_out,
          "changed_fields_union": {r: c for r, c in sorted(changed_union.items())}}
with open("_apply_author_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in report.items() if k != "changed_fields_union"}, indent=1))
print("changed-fields histogram:", json.dumps(
    {f: sum(1 for c in changed_union.values() if f in c) for f in
     sorted({x for c in changed_union.values() for x in c})}))
