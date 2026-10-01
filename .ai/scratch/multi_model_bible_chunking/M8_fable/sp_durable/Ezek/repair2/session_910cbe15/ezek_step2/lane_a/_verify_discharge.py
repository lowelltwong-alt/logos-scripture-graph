import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sl = json.loads((HERE.parent / "step2_slices.v1.json").read_text(encoding="utf-8"))["slices"]
prop = json.loads((HERE / "proposal.json").read_text(encoding="utf-8"))
dis = json.loads((HERE / "discharge.json").read_text(encoding="utf-8"))
problems = []
tot_d = tot_s = 0
assert set(dis["rows"]) == set(sl), "row set mismatch"
for rid, ent in dis["rows"].items():
    orders = sl[rid]["THE_ORDERS_THAT_APPLY_TO_THIS_ROW"]
    otext = json.dumps(orders, ensure_ascii=False)
    # un-escape JSON string content for substring checks
    otext_plain = "\n".join(json.dumps(v, ensure_ascii=False) for v in orders.values())
    def plain(o):
        out = []
        def walk(x):
            if isinstance(x, dict):
                for k, v in x.items(): out.append(k); walk(v)
            elif isinstance(x, list):
                for v in x: walk(v)
            else: out.append(str(x))
        walk(o); return "\n".join(out)
    ptext = plain(orders)
    live = sl[rid]["live_prose"]
    cand = dict(live); cand.update(prop[rid])
    cand_all = "\n".join(cand.values())
    mine = "\n".join(prop[rid].values())
    keys_hit = set()
    entries = [("D", e) for e in ent["orders_discharged"]] + [("S", e) for e in ent["stops"]]
    tot_d += len(ent["orders_discharged"]); tot_s += len(ent["stops"])
    for kind, e in entries:
        o = e["order"]
        if " :: " not in o:
            problems.append((rid, kind, "no key separator", o[:60])); continue
        key, clause = o.split(" :: ", 1)
        hit = [k for k in orders if k.startswith(key)]
        if not hit:
            problems.append((rid, kind, "KEY NOT FOUND", key))
        keys_hit.update(hit)
        clause = re.sub(r"^span_question_routed — ", "", clause)
        for piece in [p.strip(" .") for p in re.split(r"\s*…\s*", clause) if p.strip(" .")]:
            if piece not in ptext:
                problems.append((rid, kind, "ORDER QUOTE NOT VERBATIM", piece[:90]))
        if kind == "D":
            s = e["the_sentence_that_discharges_it"]
            if s not in cand_all:
                problems.append((rid, kind, "DISCHARGE SENTENCE NOT IN CANDIDATE", s[:90]))
            elif s not in mine:
                problems.append((rid, kind, "note: discharge sentence is RETAINED live text, not new text", s[:70]))
            if e["tier"] not in ("MEASURED","EXTRACTED","REPORTED","INFERRED","ASSUMED","UNAVAILABLE"):
                problems.append((rid, kind, "BAD TIER", e["tier"]))
    for k in orders:
        if k not in keys_hit:
            problems.append((rid, "-", "ORDER KEY NOT COVERED", k))
    for d in ent["sentences_deleted_and_why"]:
        if d["deleted"] not in "\n".join(live.values()):
            problems.append((rid, "del", "DELETED TEXT NOT IN LIVE", d["deleted"][:80]))
        elif d["deleted"] in cand_all:
            problems.append((rid, "del", "DELETED TEXT STILL PRESENT", d["deleted"][:80]))
    for f in ent["fields_left_alone"]:
        if f in prop[rid]:
            problems.append((rid, "alone", "FIELD LISTED AS LEFT ALONE BUT CHANGED", f))
    for f in ("boundary_rationale","strongest_rejected_alternative","device_notes","literature_type_guess"):
        if f not in prop[rid] and f not in ent["fields_left_alone"]:
            problems.append((rid, "alone", "UNCHANGED PROSE FIELD NOT LISTED", f))
for p in problems:
    print(p)
print("discharged", tot_d, "stops", tot_s, "problems", len([p for p in problems if not p[2].startswith("note")]))
