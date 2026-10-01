#!/usr/bin/env python3
"""Decision packet v2 section 2 pass 1: evidence that the #e16 ruling was applied, item by item.

Read-only over pinned inputs. Traces every part of `author/e16/ruling_e16.json` to where it was executed:
  - 80 orders_for_final_remediation -> the mechanical sweep (byte-checked on the pre/post row images where the order
    is a literal replace) or the final-wave worklist items that carried it, with each item's adjudicated status;
  - 57 grade_moves -> the applied/blocked record, #e17's later grade decision, the K3 caps, and the live grade;
  - 4 tool_orders -> the artifact that carries each change (EXTRACTED: file present + marker present);
  - 6 escalations -> where each was answered, or NOT_EVIDENCED.
Writes `e16_application_trace.v1.json` beside this script and prints a short summary. Exit 0 when nothing is UNTRACED
or UNEXPLAINED, else 1. Tiers: MEASURED (byte comparisons on pinned files), EXTRACTED (strings found in records).
"""
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

EZ = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("e16_application_trace.v1.json")

PINS = {
    "author/e16/ruling_e16.json": "20fb77b8f6d8314eed1557c254f1654a8766a2d44b4d568d14a0aa3554d497eb",
    "author/e17/ruling_e17.json": "499fb7807d0eccff8f6ec4501f45120de6dfc93af6200b94011fdc3cdb519790",
    "repair2/e16/mechanical/plan.json": "76ff5f8375be888f449c8be7d3bcf6251744c8d9eca7329288660b953120cb89",
    "repair2/e16/section7_check.v1.json": "4d368ccf6a41a7c273fcde0e4b3f8ccd1f74d5d352c7de017e8fa403e0933726",
    "repair2/e17/retile_e17.manifest.json": "b8fc010d5659184e277646268f04f96c2f8675ae9f0b9292b04e53f28b41f23d",
    "repair2/step7/step7_reconciled.v2.json": "31d90d9362c000a074e9ac6f4e13507e87e60632f071a51c878c209b35c69a12",
    "repair2/e16/t3_low_ground_check.v1.json": "fc1966eebcb8faffbae1b4e584b58bb07871d669d8605dec32e93e9e8e4fb4ed",
}
# The three corpus-wide orders name no row; each names the step-7 cross-row pattern it answers. Their targets are
# parsed from that pattern's evidence text and re-measured on the live rows.
UMBRELLA = {"O-65": "X1", "O-70": "X10", "O-72": "X14"}
DEVICE_WORD = re.compile(r"\b(?:pe|samekh|petuchah|petuhah|setumah|setumah|paseq|puncta|parashah|mark|formula|"
                         r"dateline|transport|small letter)\b", re.I)
SINGLE_WITNESS = re.compile(r"\bsingle[-\s]+witness", re.I)  # the disclosure as tools/citation_sweep.py:127 accepts it
PRE_MECH = "repair/rows_v7_cwo24.jsonl.pre_78a092c3a2eb"   # image the mechanical sweep read
POST_MECH = "repair/rows_v7_cwo24.jsonl.pre_5d55bb085092"  # image the sweep wrote (backed up before the next write)
LIVE = "repair/rows_v7_cwo24.jsonl"
LITERAL = re.compile(r"replace exact '(.*)' with '(.*)'", re.S)


def sha(p):
    return hashlib.sha256((EZ / p).read_bytes()).hexdigest()


def load(p):
    return json.loads((EZ / p).read_text(encoding="utf-8"))


def rows(p):
    return {r["decision_id"]: r for r in map(json.loads, (EZ / p).read_text(encoding="utf-8").splitlines()) if r}


def refs_at(row, verse):
    return [e for e in row["boundary_evidence_refs"] if e.split(" ")[0].endswith(f"Ezek.{verse}")]


def umbrella(oid, key, pattern, live, retired, carried):
    """Re-measure one corpus-wide order on the live rows against the targets its step-7 pattern names."""
    ev = pattern.get(key)
    if ev is None:
        return {"pattern": key, "verdict": "UNTRACED (pattern evidence not found in the pinned step-7 record)"}
    out = {"pattern": key}
    if oid == "O-65":
        named = []
        for rid, inner in re.findall(r"(P\d\d-\d{3}) \(([^)]*)\)", ev.split("Step-4c")[0]):
            named += [(rid, v) for v in re.findall(r"\d+\.\d+(?! rival)", inner)]
        left = [(r, v) for r, v in named if r in live
                and any(re.match(r"web:\S+ \[WARRANT-(?:onset|close)", e) for e in refs_at(live[r], v))]
        residue = [(r["decision_id"], e) for r in live.values() for e in r["boundary_evidence_refs"]
                   if re.match(r"web:\S+ \[WARRANT-(?:onset|close)", e) and DEVICE_WORD.search(e.split("]", 1)[1])]
        out.update(named=len(named), named_rows_retired=sorted({r for r, _ in named if r in retired}),
                   named_still_web_faced=left, device_named_web_warrants_live=residue,
                   verdict="MEASURED_DISCHARGED" if not left and not residue else "MEASURED_GAP")
    elif oid == "O-70":
        ids = sorted(set(re.findall(r"\b(?:ADJ-R\d\d|RT-\d\d)\b", ev)))
        hits = {i: carried(i) for i in ids}
        # quote marks, not possessive apostrophes ("P11-012's"): a quote opens after a non-word and closes before one
        phrase = re.findall(r"(?<!\w)'([^']+)'(?!\w)", ev.split("Not routed at all")[-1])
        blob = "\n".join(json.dumps(r, ensure_ascii=False) for r in live.values())
        still = [p for p in phrase if p in blob]
        ok = all(hits[i] and all(h["status"] in ("DISCHARGED", "NO_DEFECT", "STOP") for h in hits[i]) for i in ids)
        out.update(routed_items={i: [h["item"] + ":" + h["status"] for h in hits[i]] for i in ids},
                   unrouted_phrases=phrase, unrouted_phrase_still_live=still,
                   verdict="MEASURED_DISCHARGED" if ok and not still else "MEASURED_GAP")
    elif oid == "O-72":
        named = re.findall(r"(P\d\d-\d{3}) \((\d+):(\d+)\)", ev)
        res = []
        for rid, c, v in named:
            if rid not in live:
                res.append({"row": rid, "verse": f"{c}:{v}", "state": "retired" if rid in retired else "absent"})
                continue
            ents = refs_at(live[rid], f"{c}.{v}")
            res.append({"row": rid, "verse": f"{c}:{v}", "entries": len(ents),
                        "all_disclosed": bool(ents) and all(SINGLE_WITNESS.search(e) for e in ents)})
        ok = bool(named) and all(r.get("all_disclosed") or r.get("state") == "retired" for r in res)
        out.update(named=res, verdict="MEASURED_DISCHARGED" if ok else "MEASURED_GAP")
    return out


def main():
    bound = {p: sha(p) for p in PINS}
    moved = {p: h for p, h in bound.items() if h != PINS[p]}
    if moved:
        raise SystemExit(f"PINNED INPUT MOVED: {moved}")
    for img, pre in ((PRE_MECH, "78a092c3a2eb"), (POST_MECH, "5d55bb085092")):
        if not sha(img).startswith(pre):
            raise SystemExit(f"row image {img} does not hash to its name")
    wl_path = "repair2/final/final_worklist.v2.json"
    adj_paths = [f"author/final/s{i}_adjudication/adjudication.json" for i in range(1, 7)]
    k3_path = "repair2/final/k3_caps_plan.v1.json"
    for p in [wl_path, *adj_paths, k3_path, LIVE]:
        bound[p] = sha(p)

    e16, e17, plan = load("author/e16/ruling_e16.json"), load("author/e17/ruling_e17.json"), load("repair2/e16/mechanical/plan.json")
    s7, retile, wl, k3 = load("repair2/e16/section7_check.v1.json"), load("repair2/e17/retile_e17.manifest.json"), load(wl_path), load(k3_path)
    pre, post, live = rows(PRE_MECH), rows(POST_MECH), rows(LIVE)

    status = {}
    for p in adj_paths:
        for fid, it in load(p)["items"].items():
            status[fid] = it
    items = wl["items"]
    blob = {i["id"]: json.dumps(i, ensure_ascii=False) for i in items}

    def carried(oid):
        hits = [i["id"] for i in items if re.search(r"(?<![\w-])" + re.escape(oid) + r"(?![\w-])", blob[i["id"]])]
        return [{"item": f, "row": status.get(f, {}).get("row"), "status": status.get(f, {}).get("status", "NOT_ADJUDICATED")} for f in hits]

    step7 = load("repair2/step7/step7_reconciled.v2.json")
    pattern = {}

    def walk(node):
        if isinstance(node, dict):
            if node.get("id") in UMBRELLA.values() and isinstance(node.get("evidence"), str):
                pattern.setdefault(node["id"], node["evidence"])
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    walk(step7)
    retired_ids = set(retile["retired"])
    planned = {p["id"]: p for p in plan["planned"]}
    orders = []
    for o in e16["orders_for_final_remediation"]:
        rec = {"id": o["id"], "row": o["row"], "field": o["field"], "kind": o["kind"]}
        if o["id"] in planned:
            rec["route"] = "MECHANICAL_SWEEP"
            m = LITERAL.fullmatch(o["order"])
            if m and o["row"] in pre and o["row"] in post:
                x, y = m.groups()
                fp = json.dumps(pre[o["row"]].get(o["field"]), ensure_ascii=False)
                fq = json.dumps(post[o["row"]].get(o["field"]), ensure_ascii=False)
                ok = x in fp and y in fq and (fq.count(x) < fp.count(x) or x in y)
                rec["byte_check"] = "MEASURED_APPLIED" if ok else "MEASURED_NOT_FOUND"
            else:
                rec["byte_check"] = "NOT_BYTE_CHECKED (order is not a literal replace on one row field)"
        elif o["id"] in UMBRELLA:
            rec["route"] = "CORPUS_WIDE_MEASURED"
            rec["umbrella"] = umbrella(o["id"], UMBRELLA[o["id"]], pattern, live, retired_ids, carried)
        else:
            hits = carried(o["id"])
            rec["route"] = "FINAL_WAVE_WORKLIST" if hits else "UNTRACED"
            rec["carried_by"] = hits
        orders.append(rec)

    retired = set(retile["retired"])
    plan_gm = {g["row"]: g for g in plan["grade_moves"]}
    blocked, applied7 = set(s7["blocked"]), set(s7["applied"])
    gd = {g["row"]: g for g in e17["grade_decisions"]}
    caps = {c["row"]: c for c in k3["caps"]}
    t3_moves = {x["row"] for x in load("repair2/e16/t3_low_ground_check.v1.json")["records"] if x["decision"].startswith("MOVE")}
    grades = []
    for g in e16["grade_moves"]:
        r = g["row"]
        rec = {"row": r, "e16": f"{g['from']} -> {g['to']}", "conditional": "condition" in g}
        if r in retired:
            rec.update(basis="RETIRED_BY_E17_RETILING (successor row graded afresh by #e17)", verdict="EXPLAINED")
            grades.append(rec)
            continue
        if r in plan_gm:
            want, basis = g["to"], "mechanical set_confidence (applied)"
            if rec["conditional"] and r in blocked and r in t3_moves:
                basis += ("; section-7 BLOCKED, moved under #e17 K3/T-3 - the low-ground reading is the "
                          "orchestrator's (t3_low_ground_check.v1.json), so it is a named question for the blind checkers")
                rec["orchestrator_reading"] = True
        elif r in blocked:
            want, basis = g["from"], "section-7 blocked (held at from)"
        else:
            want, basis = None, "NOT IN PLAN OR SECTION-7 RECORD"
        if r in gd:
            want, basis = gd[r]["to"], basis + f"; #e17 {gd[r]['decision']} -> {gd[r]['to']}"
        if r in caps:
            want, basis = caps[r]["to"], basis + f"; K3 cap -> {caps[r]['to']}"
        now = live.get(r, {}).get("confidence")
        rec.update(basis=basis, expected=want, live=now,
                   verdict="EXPLAINED" if want is not None and want == now else "UNEXPLAINED")
        grades.append(rec)

    tools = []
    checks = [("role_tokens :merge arm", "tools/check_role_tokens.py", "merge"),
              ("CONF-CAL audit v3+", "repair2/step7/confcal_audit_v4.py", "MERGE_CONTESTS_OWN_SEAM"),
              ("device inventory v3", "ezek_device_inventory.v3.json", "said_to_me_in_vision"),
              ("register schema-vocabulary arm", "tools/check_register.py", "schema_vocabulary")]
    for (name, p, marker), t in zip(checks, e16["tool_orders"]):
        f = EZ / p
        present = f.exists() and marker in f.read_text(encoding="utf-8", errors="replace")
        tools.append({"tool_order": t.get("member"), "artifact": p, "marker": marker,
                      "verdict": "EXTRACTED_PRESENT" if present else "NOT_FOUND",
                      "sha256": sha(p) if f.exists() else None})

    e17_text = json.dumps(e17, ensure_ascii=False)
    esc = []
    for e in e16["escalations"]:
        named = sorted(set(re.findall(r"P\d\d-\d{3}", e["what"])))
        if "review" in e["to"]:
            found = [r for r in named if r in e17_text]
            v = "ANSWERED_IN_E17" if (not named or len(found) == len(named)) else "PARTLY_ANSWERED"
            esc.append({"id": e["id"], "to": e["to"], "rows_named": named, "rows_found_in_e17": found, "verdict": v})
        else:
            esc.append({"id": e["id"], "to": e["to"], "verdict": "NOT_EVIDENCED (no delivered owner report names it)"})

    e16_items = [i["id"] for i in items if i["class"] == "E16"]
    open_items = [{"item": f, "row": it.get("row"), "class": it.get("class"), "status": it["status"],
                   "evidence": str(it.get("evidence") or it.get("adjudication") or "")[:300]}
                  for f, it in sorted(status.items()) if it.get("status") in ("STOP", "GRADE_QUESTION")]
    summary = {
        "orders": dict(Counter(o["route"] for o in orders)),
        "mechanical_byte_checks": dict(Counter(o.get("byte_check", "-").split(" ")[0] for o in orders if o["route"] == "MECHANICAL_SWEEP")),
        "corpus_wide": {o["id"]: o["umbrella"]["verdict"] for o in orders if "umbrella" in o},
        "orders_carried_item_status": dict(Counter(h["status"] for o in orders for h in o.get("carried_by", []))),
        "e16_class_items": len(e16_items),
        "e16_class_item_status": dict(Counter(status.get(f, {}).get("status", "NOT_ADJUDICATED") for f in e16_items)),
        "grade_moves": dict(Counter(g["verdict"] for g in grades)),
        "section7_applied_vs_plan_conditional_applied": [len(applied7), sum(1 for g in plan["grade_moves"] if g["conditional_applied"])],
        "grade_moves_on_orchestrator_reading": [g["row"] for g in grades if g.get("orchestrator_reading")],
        "tool_orders": dict(Counter(t["verdict"] for t in tools)),
        "escalations": dict(Counter(e["verdict"].split(" ")[0] for e in esc)),
        "final_wave_stop_or_grade_question": len(open_items),
    }
    bad = summary["orders"].get("UNTRACED", 0) + summary["grade_moves"].get("UNEXPLAINED", 0) \
        + summary["mechanical_byte_checks"].get("MEASURED_NOT_FOUND", 0) + summary["tool_orders"].get("NOT_FOUND", 0) \
        + sum(1 for v in summary["corpus_wide"].values() if v != "MEASURED_DISCHARGED")
    out = {"schema": "ezek_e16_application_trace.v1", "pass": "decision packet v2 section 2 pass 1",
           "inputs_sha256": bound, "row_images": {"pre_mechanical": PRE_MECH, "post_mechanical": POST_MECH},
           "summary": summary, "verdict": "APPLICATION_EVIDENCED" if not bad else "GAPS_FOUND",
           "orders": orders, "grade_moves": grades, "tool_orders": tools, "escalations": esc,
           "final_wave_open_items": open_items}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"verdict": out["verdict"], **summary}, ensure_ascii=False, indent=1))
    print("wrote", OUT.name, hashlib.sha256(OUT.read_bytes()).hexdigest())
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
