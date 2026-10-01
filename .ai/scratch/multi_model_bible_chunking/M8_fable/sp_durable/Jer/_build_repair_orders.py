#!/usr/bin/env python3
"""Docket backlog -> repair orders (OWNER_REPAIR_ADVANCE_2026-09-06 item 2, delegated judgment).

Reads the three owner-triage dockets (read-only baselines) and their dispositions ledgers
(latest adjudication incl. the OW-3 re-adjudication outcomes), classifies every OPEN item
deterministically, folds the orchestrator's recorded span rulings in, dedupes per shipped row
across dockets (Prov rows sit in two dockets), embeds the CURRENT shipped row, and writes
per-book order slices (<=8 rows per attempt) under SP/REPAIR/<Book>/ plus the plan record
receipts/OW2_repair_plan.v1.json (classification counts, span rulings with reasons + evidence,
input hashes). Nothing here touches any shipped corpus.

Classification of an OPEN item (latest adjudication):
  REJECTED       verdict refute or final severity none  -> resolved_no_change (adjudicator grounds)
  LOW            final low -> folded into the row's order if the row is repaired anyway, else
                 resolved_retained_low (OW-3 explicit handling; ruling: completed books, not perfection)
  SPAN_ACCEPTED  endorse_proposal + orchestrator ACCEPT -> respan/retire/new_row orders
  SPAN_REJECTED  endorse_proposal + orchestrator REJECT -> resolved_no_change (reasons recorded)
  REPAIR         final medium/high (span n/a or decline_proposal) -> field-level repair order
Usage: _build_repair_orders.py [--dry-run]"""
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent            # SP/Jer
SP = HERE.parent
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
REP = SP / "REPAIR"
RULING = "OWNER_REPAIR_ADVANCE_2026-09-06.md"
DOCKETS = {
    "isaiah_lf": ("receipts/OW2_isa_lf_remediation_docket.v1.json", "receipts/OW2_isa_lf_remediation_dispositions.v1.json", "Isa"),
    "five_book": ("receipts/OW2_five_book_remediation_docket.v1.json", "receipts/OW2_five_book_remediation_dispositions.v1.json", None),
    "prov38": ("receipts/OW2_prov38_remediation_docket.v1.json", "receipts/OW2_prov38_remediation_dispositions.v1.json", "Prov"),
}

# ORCHESTRATOR SPAN RULINGS (delegated judgment; reasons + evidence pointers; alternatives recorded
# as disclosed uncertainty). Every ruling stays inside the owner-ruled book strategy.
SPAN_RULINGS = {
    "M8-Job-093#1": {"decision": "ACCEPT", "route": "merge",
        "orders": [{"row": "M8-Job-092", "op": "respan", "span": "Job.22.21-Job.22.30"},
                   {"row": "M8-Job-093", "op": "retire"}],
        "reasons": "Job strategy §6 seams rows at tier-1 signals ONLY; the shipped seam Job.22.25|Job.22.26 carries none (waw-qatal consequent -> ki-az continuation inside one 2ms address, no vocative/formula/protasis/mark); both outer edges of the merged unit are ruled devices (address shift at Job.22.21 after the quoted 3mp saying of 22:20; Job's speech formula at Job.23.1; the PE after Job.22.30 corroborates at tier-3). The auditor's option (b) (a cut at 22:24|22:25) is NOT adopted: it would cut a conditional sentence between condition and consequence, which is not a §6 protasis/apodosis-block edge. 10 verses sits inside the §6 4-12 guide.",
        "evidence": ["OW2_five_book_remediation_docket.v1.json#M8-Job-093#1 (auditor grounds + Fable adjudication, both-sides assessed)"]},
    "M8-Prov-027#1": {"decision": "ACCEPT", "route": "seam_move",
        "orders": [{"row": "M8-Prov-026", "op": "respan", "span": "Prov.6.20-Prov.6.26"},
                   {"row": "M8-Prov-027", "op": "respan", "span": "Prov.6.27-Prov.6.29"}],
        "reasons": "Seam relocation 6:23|6:24 -> 6:26|6:27 as one coherent seam-pair edit: the shipped seam cuts the lamed-infinitive purpose clause (לִשְׁמָרְךָ, oshb:Prov.6.24) from its governing motive clause at 6:23 - the book's own lecture template binds that purpose clause to the exordium (byte-identical token at oshb:Prov.7.5 closing the 7:1-5 exordium; oshb:Prov.5.2 likewise) - while 6:26 is a complete motive clause closing under the PE at Prov.6.26 (tier-3 single-witness corroboration only) and 6:27 opens the self-contained question-question-application figure 6:27-29. The merge alternative (Prov.6.20-6.29) is NOT adopted (it would bury the one parashah-corroborated interior seam the C1 rule names) and is recorded as the disclosed alternative. The 3-verse unit stands on its own construction; the C1 ~4-8 guide is a guide, not a bar.",
        "evidence": ["OW2_five_book_remediation_docket.v1.json#M8-Prov-027#1 (auditor grounds + Fable adjudication with independent template evidence)"]},
    "M8-Prov-289#1": {"decision": "ACCEPT", "route": "atomize",
        "orders": [{"row": "M8-Prov-289", "op": "respan", "span": "Prov.19.6-Prov.19.6", "unit_type": "single_proverb"},
                   {"row": "M8-Prov-289b", "op": "new_row", "span": "Prov.19.7-Prov.19.7", "unit_type": "single_proverb",
                    "parent_collection": "C2 Prov.10.1-Prov.22.16", "after": "M8-Prov-289"}],
        "reasons": "The cluster's only load-bearing warrant (an a-fortiori dependency running from 19:6 into 19:7) is byte-false: oshb:Prov.19.7 opens on the quantifier כָּל and the pair אַף כִּי stands verse-internally at tokens 5-6 with the etnahta on מִמֶּנּוּ (the same intra-verse shape at all 6 book-wide sites); 19:6|19:7 share 0 skeleton tokens; the residual friend-root is cognate-only and hubs on the NON-adjacent 19:4. Under C2's ruled default (single_proverb; proverb_cluster only on byte-grounded cohesion NAMED in the rationale) the atomic default reasserts itself. Both dockets (M8-Prov-289#1 and M8-Prov-289#p38-1) reached the same ruling; ONE edit resolves both, every item link retained. The fallback (retain the cluster on root-level glue at low band) is recorded as the weaker disclosed alternative.",
        "evidence": ["OW2_five_book_remediation_docket.v1.json#M8-Prov-289#1", "OW2_prov38_remediation_docket.v1.json#M8-Prov-289#p38-1"]},
    "M8-Prov-289#p38-1": {"decision": "ACCEPT", "route": "atomize", "same_edit_as": "M8-Prov-289#1", "orders": [],
        "reasons": "Same row, same byte finding, same ruling as M8-Prov-289#1 - resolved by that one edit (deduplicated; both finding and receipt links retained).",
        "evidence": ["OW2_prov38_remediation_docket.v1.json#M8-Prov-289#p38-1"]},
    "M8-Prov-432#1": {"decision": "ACCEPT", "route": "merge",
        "orders": [{"row": "M8-Prov-431", "op": "respan", "span": "Prov.25.9-Prov.25.10", "unit_type": "admonition_unit"},
                   {"row": "M8-Prov-432", "op": "retire"}],
        "reasons": "oshb:Prov.25.10 opens on the subordinator פֶּן and contains no governing clause; its prohibition אַל תְּגָל closes 25:9; book-wide byte control: all 7 verse-initial פן sites depend on the previous verse. Owner precedent B-10 (a syntactically continuous single sentence spanning two verses is ONE proverb-unit regardless of verse count) is directly on point, so the 25:9 row absorbs 25:10 and the 25:10 row retires; rear edge 25:10|25:11 shares 0 tokens and opens a new image; the 25:8|25:9 join stays optional (ruled coherently with M8-Prov-430#1). unit_type: admonition_unit per precedent B-8 (25:9 carries the imperative רִיב plus the vetitive אַל תְּגָל and 25:10 is their motive clause - the command-plus-motive shape), with the required one-sentence deviation disclosure in C5 and the single_proverb reading (B-10) recorded as the disclosed alternative; confidence medium.",
        "evidence": ["OW2_five_book_remediation_docket.v1.json#M8-Prov-432#1"]},
    "M8-Prov-437#1": {"decision": "ACCEPT", "route": "cluster_pair",
        "orders": [{"row": "M8-Prov-437", "op": "respan", "span": "Prov.25.16-Prov.25.17", "unit_type": "proverb_cluster"},
                   {"row": "M8-Prov-438", "op": "retire"}],
        "reasons": "Arm (b) adopted: the C5 rule permits a proverb_cluster on a NAMED byte-grounded construction run, and here the lest-particle plus object-suffixed yiqtol of the sin-dotted שבע root is confined to exactly these two adjacent verses book-wide (the other 2 of the 4 lest+yiqtol sites are unsuffixed), inside a fully shared frame (imperative / פֶּן / suffixed yiqtol / suffixed consequence verb) with the byte-identical token פֶּן straddling the seam; the outer seams 25:15|25:16 and 25:17|25:18 share 0 tokens. This rests on more than the shipped 25:11-12 pair (1 content token + adjacency). The shipped rival ground ('share no skeleton token with this verse') was byte-false for 25:17 and undisclosed. Arm (a) (atomic rows retained with the dead warrant replaced and the straddling device disclosed) is byte-compliant too and is recorded as the disclosed alternative in strongest_rejected_alternative; confidence medium, not high.",
        "evidence": ["OW2_five_book_remediation_docket.v1.json#M8-Prov-437#1"]},
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_rows(book):
    p = M8 / "book_chunks" / book / "chunks.jsonl"
    rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    return rows, sha(p)


def latest(disp_item):
    ra = disp_item.get("readjudication") or {}
    adj = disp_item["adjudicated"]
    return {"verdict": ra.get("verdict") or adj.get("verdict"),
            "final_severity": ra.get("final_severity") or adj.get("final_severity"),
            "span_ruling": ra.get("span_ruling") or adj.get("span_ruling"),
            "readjudicated": bool(ra)}


def main():
    dry = "--dry-run" in sys.argv
    shipped = {}
    shipped_sha = {}
    for b in ("Isa", "Ps", "Job", "Prov", "Eccl", "Song"):
        rows, h = load_rows(b)
        shipped[b] = {r["decision_id"]: r for r in rows}
        if b == "Isa":
            shipped[b].update({r["writer_decision_id"]: r for r in rows})   # docket keys Isa by writer id
        shipped_sha[b] = h

    per_row = defaultdict(lambda: {"items": [], "ops": []})   # key (book, decision_id)
    classified = []
    inputs = {}
    for dk, (dpath, spath, fixed_book) in DOCKETS.items():
        docket = json.load(open(M8 / dpath, encoding="utf-8"))
        disp = json.load(open(M8 / spath, encoding="utf-8"))
        inputs[dk] = {"docket": {"path": dpath, "sha256": sha(M8 / dpath)}, "dispositions": {"path": spath, "sha256": sha(M8 / spath)}}
        ditems = {i["item_id"]: i for i in docket["items"]}
        for di in disp["items"]:
            if di.get("disposition") != "open":
                continue
            it = ditems[di["item_id"]]
            book = fixed_book or it["book"]
            row = shipped[book][it["row_id"]]
            key = (book, row["decision_id"])
            lat = latest(di)
            sev, sr, vd = lat["final_severity"], lat["span_ruling"], lat["verdict"]
            entry = {"item_id": it["item_id"], "docket": dk, "row_id": it["row_id"], "shipped_decision_id": row["decision_id"],
                     "class": it.get("class"), "filed_severity": it.get("filed_severity"), "latest": lat,
                     "claim": it.get("claim"), "auditor_grounds": it.get("grounds") or it.get("auditor_grounds"),
                     "proposed_change": it.get("proposed_change") or it.get("auditor_proposed_change"),
                     "adjudicator_grounds": (it.get("adjudication") or {}).get("grounds") or it.get("adjudicator_grounds"),
                     "readjudication": di.get("readjudication")}
            if vd == "refute" or sev == "none":
                entry["classification"] = "REJECTED"
            elif sr == "endorse_proposal":
                rul = SPAN_RULINGS.get(it["item_id"])
                assert rul, "endorsed span proposal without an orchestrator ruling: " + it["item_id"]
                entry["classification"] = "SPAN_ACCEPTED" if rul["decision"] == "ACCEPT" else "SPAN_REJECTED"
                entry["span_ruling_orchestrator"] = rul
                if rul["decision"] == "ACCEPT":
                    for o in rul["orders"]:
                        per_row[(book, o["row"])]["ops"].append({**o, "from_item": it["item_id"]})
                    per_row[key]["items"].append(entry)
            elif sev == "low":
                entry["classification"] = "LOW"
                per_row[key]["items"].append(entry)      # folded only if the row is repaired anyway
            elif sev in ("medium", "high"):
                entry["classification"] = "REPAIR"
                per_row[key]["items"].append(entry)
            else:
                raise SystemExit(f"unclassifiable item {it['item_id']}: {lat}")
            classified.append(entry)

    # build orders per row: a row is REPAIRED if it has any REPAIR/SPAN item or a span op; LOW-only rows are retained
    orders = defaultdict(dict)     # book -> decision_id -> order
    retained_low = []
    for (book, did), v in per_row.items():
        repairable = any(e["classification"] in ("REPAIR", "SPAN_ACCEPTED") for e in v["items"]) or bool(v["ops"])
        if not repairable:
            for e in v["items"]:
                if e["classification"] == "LOW":
                    retained_low.append(e["item_id"])
            continue
        ops = v["ops"]
        op = "replace"
        span_target = unit_type = parent = None
        after = None
        if any(o["op"] == "retire" for o in ops):
            op = "retire"
        elif any(o["op"] == "new_row" for o in ops):
            o = next(o for o in ops if o["op"] == "new_row")
            op, span_target, unit_type, parent, after = "new_row", o["span"], o.get("unit_type"), o.get("parent_collection"), o.get("after")
        elif any(o["op"] == "respan" for o in ops):
            o = next(o for o in ops if o["op"] == "respan")
            op, span_target, unit_type = "respan", o["span"], o.get("unit_type")
        cur = shipped[book].get(did)
        orders[book][did] = {
            "row_id": did, "book": book, "op": op, "span_target": span_target, "unit_type_target": unit_type,
            "parent_collection_target": parent, "insert_after": after,
            "current_row": cur, "items": v["items"], "span_ops_from": [o["from_item"] for o in ops],
            "low_items_folded": [e["item_id"] for e in v["items"] if e["classification"] == "LOW"],
        }
    # new rows carry the source row's items via the accepted ruling; make sure their entry exists
    for iid, rul in SPAN_RULINGS.items():
        if rul["decision"] != "ACCEPT":
            continue
        for o in rul["orders"]:
            book = "Job" if o["row"].startswith("M8-Job") else "Prov"
            if o["row"] not in orders[book]:
                orders[book][o["row"]] = {"row_id": o["row"], "book": book, "op": o["op"], "span_target": o.get("span"),
                                          "unit_type_target": o.get("unit_type"), "parent_collection_target": o.get("parent_collection"),
                                          "insert_after": o.get("after"), "current_row": shipped[book].get(o["row"]),
                                          "items": [], "span_ops_from": [iid], "low_items_folded": []}

    # slices per book in chunk order (<=8 rows per attempt); new rows follow their anchor
    def order_key(book, did):
        r = shipped[book].get(did)
        if r:
            return (r["chunk_index_in_book"], 0)
        anchor = orders[book][did]["insert_after"]
        return (shipped[book][anchor]["chunk_index_in_book"], 1)

    plan_slices = {}
    if not dry:
        REP.mkdir(exist_ok=True)
    for book, od in orders.items():
        ids = sorted(od, key=lambda d: order_key(book, d))
        # keep seam pairs / merge pairs inside one attempt: chunk of 8 but never split consecutive span-op rows
        chunks, cur_chunk = [], []
        for d in ids:
            cur_chunk.append(d)
            if len(cur_chunk) >= 8 and not (od[d]["span_ops_from"] and ids.index(d) + 1 < len(ids) and od[ids[ids.index(d) + 1]]["span_ops_from"]):
                chunks.append(cur_chunk); cur_chunk = []
        if cur_chunk:
            chunks.append(cur_chunk)
        plan_slices[book] = []
        for n, ch in enumerate(chunks, 1):
            sl = {"schema": "m8_repair_orders_slice.v1", "book": book, "slice": f"rep_{book}_{n:02d}",
                  "attempt_id": f"rep_{book}_{n:02d}_a1", "output_file": f"REPAIR/{book}/repair_{book}_{n:02d}.jsonl",
                  "row_ids": ch, "orders": {d: od[d] for d in ch},
                  "authority": {"ruling": RULING, "sha256": sha(M8 / RULING)},
                  "shipped_corpus_sha256": shipped_sha[book]}
            plan_slices[book].append({"slice": sl["slice"], "attempt_id": sl["attempt_id"], "rows": ch,
                                      "ops": Counter(od[d]["op"] for d in ch), "items": sum(len(od[d]["items"]) for d in ch)})
            if not dry:
                (REP / book).mkdir(parents=True, exist_ok=True)
                (REP / book / f"orders_{sl['slice']}.json").write_text(json.dumps(sl, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")

    plan = {
        "schema": "m8_ow2_repair_plan.v1", "built": datetime.now(timezone.utc).isoformat(),
        "authority": {"ruling": RULING, "sha256": sha(M8 / RULING), "clause": "item 2 (repair with delegated judgment) + item 3 (finish the backlog)"},
        "inputs": inputs, "shipped_corpora_sha256": shipped_sha,
        "classification_counts": Counter(e["classification"] for e in classified),
        "classification_by_docket": {dk: Counter(e["classification"] for e in classified if e["docket"] == dk) for dk in DOCKETS},
        "span_rulings": SPAN_RULINGS,
        "resolved_no_change_items": [e["item_id"] for e in classified if e["classification"] in ("REJECTED", "SPAN_REJECTED")],
        "retained_low_items_not_repaired": retained_low,
        "rows_to_repair": {b: len(od) for b, od in orders.items()},
        "ops_by_book": {b: Counter(o["op"] for o in od.values()) for b, od in orders.items()},
        "slices": plan_slices,
        "dedupe_note": "one order per shipped row across dockets; the eight Prov rows present in both the five-book and the Prov-38 dockets carry every item of both; M8-Prov-289#1 and M8-Prov-289#p38-1 resolve by one edit",
        "statement": "PLAN ONLY - nothing applied to any shipped corpus; every disposition is written to the ledgers only after the repair wave's fresh distinct-checker sweep and the r3 targeted semantic check pass.",
    }
    out = M8 / "receipts" / "OW2_repair_plan.v1.json"
    if not dry:
        out.write_text(json.dumps(plan, ensure_ascii=False, indent=1, default=lambda o: dict(o) if isinstance(o, Counter) else str(o)), encoding="utf-8", newline="\n")
    print(json.dumps({k: plan[k] for k in ("classification_counts", "classification_by_docket", "rows_to_repair", "ops_by_book", "slices", "retained_low_items_not_repaired", "resolved_no_change_items")},
                     ensure_ascii=False, indent=1, default=lambda o: dict(o) if isinstance(o, Counter) else str(o)))
    if not dry:
        print("plan written:", out, sha(out)[:16])


if __name__ == "__main__":
    main()
