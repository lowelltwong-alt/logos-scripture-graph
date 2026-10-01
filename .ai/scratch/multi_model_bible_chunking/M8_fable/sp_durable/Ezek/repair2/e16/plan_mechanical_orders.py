#!/usr/bin/env python3
"""Plan #e16's MECHANICAL orders as one guarded sweep proposal, plus the grade moves the section-7 check allows. Plan only.

An order is executed mechanically ONLY when it parses to exact before/after strings ("replace exact 'X' with 'Y'") and
'X' occurs EXACTLY ONCE in the named field of the named row on the live rows (list fields: in exactly one element).
Anything else - a class-wide order, a field the text names loosely, a string found zero or several times - is ROUTED
to the author batch with its reason; a mechanical sweep never guesses.

Grade moves: every unconditional #e16 move, plus the conditional moves section7_check.v1.json APPLIED; the moves are
emitted separately (confidence is written by the harness's own confidence operation, with each ground owed in prose
in the same final batch, as #e15's rule requires).

usage: python plan_mechanical_orders.py
"""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
R16 = EZ / "author" / "e16" / "ruling_e16.json"
S7 = HERE / "section7_check.v1.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
rows = {r["decision_id"]: r for r in (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}
r16 = json.loads(R16.read_text(encoding="utf-8-sig"))
s7 = json.loads(S7.read_text(encoding="utf-8"))
REPL = re.compile(r"replace exact '(.+?)' with '(.*?)'(?:\s*$|[;.]\s)", re.S)
FIELDS = {"boundary_evidence_refs", "boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess"}

proposal, planned, routed = {}, [], []
# #e17 supersedes #e16 where it rules: rows it retires take no mechanical order or grade move here (the re-tiling authors
# carry them); its own mechanical orders are added in its notation "'X' -> 'Y'"; its grade decisions replace #e16's.
R17 = EZ / "author" / "e17" / "ruling_e17.json"
T3 = HERE / "t3_low_ground_check.v1.json"
r17 = json.loads(R17.read_text(encoding="utf-8-sig"))
retired = {x for t in r17["retiling_orders"] for x in t["retire"]}
REPL17 = re.compile(r"^'(.+)' -> '(.*)'$", re.S)
expanded = []
for src, rr in (("#e16", r16), ("#e17", r17)):
    for o in rr["orders_for_final_remediation"]:
        if str(o.get("kind")).lower() != "mechanical":
            continue
        ids = re.findall(r"P\d\d-\d\d\d", str(o.get("row", "")))
        # an order naming several rows in one field is executed per row (each row's strings must be found exactly once)
        expanded.extend([dict(o, row=i, src=src) for i in ids] if len(ids) > 1 else [dict(o, src=src)])
for o in expanded:
    rid, field, text = o.get("row"), o.get("field"), o.get("order", "")
    pairs = REPL.findall(text) or REPL17.findall(text.strip())
    why = None
    if rid in retired:
        routed.append({"id": o.get("id"), "src": o["src"], "row": rid, "field": field, "why": "row retired by #e17 re-tiling - carried to the new row's authors", "order": text})
        continue
    if rid not in rows:
        why = "row not in the corpus"
    elif field not in FIELDS:
        why = "field named loosely (%r) - not a single exact field" % field
    elif not pairs:
        why = "the order does not parse to exact before/after strings"
    if why:
        routed.append({"id": o.get("id"), "row": rid, "field": field, "why": why, "order": text})
        continue
    cur = proposal.get(rid, {}).get(field, rows[rid].get(field))
    ok = True
    for before, after in pairs:
        if isinstance(cur, list):
            hits = [i for i, e in enumerate(cur) if before in e]
            if len(hits) != 1 or cur[hits[0]].count(before) != 1:
                ok, why = False, "'before' found in %d entries" % len(hits)
                break
            cur = list(cur)
            cur[hits[0]] = cur[hits[0]].replace(before, after)
        else:
            if not isinstance(cur, str) or cur.count(before) != 1:
                ok, why = False, "'before' found %d times" % (cur.count(before) if isinstance(cur, str) else 0)
                break
            cur = cur.replace(before, after)
    if not ok:
        routed.append({"id": o.get("id"), "row": rid, "field": field, "why": why, "order": text})
        continue
    proposal.setdefault(rid, {})[field] = cur
    planned.append({"id": o.get("id"), "row": rid, "field": field, "replacements": len(pairs), "source_item": o.get("source_item")})

applied_cond = set(s7["applied"])
t3 = json.loads(T3.read_text(encoding="utf-8"))
applied_cond |= {x["row"] for x in t3["records"] if x["decision"].startswith("MOVE")}
dec17 = {d["row"]: d for d in r17["grade_decisions"]}
moves = []
candidates = list(r16["grade_moves"])
for d in r17["grade_decisions"]:
    if str(d.get("decision", "")).startswith("SUPERSEDE") and "MOVE" in str(d.get("decision")) and not any(g["row"] == d["row"] for g in candidates):
        candidates.append({"row": d["row"], "from": rows[d["row"]].get("confidence"), "to": d["to"], "ground": d.get("faces"), "by": "#e17"})
for g in candidates:
    d = dec17.get(g["row"])
    if g["row"] in retired or (d and str(d.get("decision")).startswith("SUPERSEDED by RT")):
        continue
    if d and "MOVE" in str(d.get("decision")):
        g = dict(g, to=d["to"], ground=d.get("faces") or g.get("ground"), by="#e17")
        g.pop("condition", None)
    if "condition" in g and g["row"] not in applied_cond:
        continue
    if rows[g["row"]].get("confidence") != g["from"]:
        routed.append({"row": g["row"], "field": "confidence", "why": "live grade %r is not the move's 'from' %r" % (rows[g["row"]].get("confidence"), g["from"])})
        continue
    moves.append({"row": g["row"], "from": g["from"], "to": g["to"], "ground": g.get("ground"), "conditional_applied": "condition" in g})
out_dir = HERE / "mechanical"
out_dir.mkdir(exist_ok=True)
(out_dir / "proposal.json").write_text(json.dumps(proposal, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
(out_dir / "plan.json").write_text(json.dumps({"schema": "ezek_e16_mechanical_plan.v1", "rows_sha256": sha(ROWS), "ruling_sha256": sha(R16),
                                               "section7_check_sha256": sha(S7), "planned": planned, "routed_to_authors": routed,
                                               "grade_moves": moves}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"rows_sha256": sha(ROWS), "mechanical_planned": len(planned), "rows_in_proposal": len(proposal),
                  "routed_to_authors": len(routed), "routed_reasons": [r["why"][:60] for r in routed], "grade_moves": len(moves),
                  "proposal_sha256": sha(out_dir / "proposal.json")}, ensure_ascii=False, indent=1))
