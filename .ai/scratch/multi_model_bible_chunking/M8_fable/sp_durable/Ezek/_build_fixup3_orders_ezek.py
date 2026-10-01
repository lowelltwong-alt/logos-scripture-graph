#!/usr/bin/env python3
"""FIXUP-3 work orders for Ezekiel, one file per part (ezek_controlling_rulings_a1#e10 ruling S3-ROUTING (3)). Deterministic: it embeds,
per row and VERBATIM, every item that binds the row. It judges nothing and never edits a row. Modeled on _build_fixup2_orders_ezek.py.

Item sources (#e10 S3-ROUTING (3); S3-03, S3-16, S3-17, S3-18, TOOLFIX-5):
  - #e10 ruling orders addressed to author_fixup. An order naming rows or exact spans binds to those rows; one naming neither is a
    general writing rule, carried as brief_rules. The general writing rules of #e6, #e7 and #e9 are brief_rules too; their row-bound
    orders belonged to earlier waves and are never re-issued.
  - S3's findings routed to author_fixup on the six wave parts, verbatim, bound to the rows they name. S3-11, S3-14 and S3-15 (p05, p10,
    p11) were EXECUTED by CWO-EZ-23 (#e10 S3-ROUTING (1)); the index records them, and they are never ordered.
  - S3's replaced_rows defect entries for rows in the wave parts, verbatim (kind s3_row_defect).
  - CWO-EZ-22 author items: the residual hits of repair/cwo_coverage_v5cwo23/CWO-EZ-22.json, stamped CWO-EZ-22 with the line #e10 S3-16
    rules.
  - TOOLFIX-5's impact hits over rows_v5_cwo23: each must coincide with a CWO-EZ-22 item (same row, field and match) or be added as its
    own item; the index records the cross-reference.
  - p03: the twelve S3-03 prose-disclosure items (from p03's FIXUP-2 S2-14 items, restamped S3-03 and checked against #e10 S3-03's list),
    plus the v5 ngram7 worst_reuse grams as grams not to reuse. #e10 S3-03's author order binds to the rows that list names. Where the
    order's exact_spans misstate those rows, the index and p03's orders record the discrepancy (E-03 lane) and the spans are never
    propagated. Every other order whose named rows and exact_spans disagree is a problem.
  - p04: #e10 S3-17 (3)'s non-pre-emption sentence on P04-008, verbatim.
  - p08: #e10 S3-18's verified verse list and corrected citation on P08-004, verbatim.

Parts are those with items, and they must equal the six #e10 names. Attempt ids are ezek_author_fixup3_pNN_a1, execution #e1. It writes
<out>/orders_ezek_author_fixup3_<part>_a1.json and <out>/orders_index.json after the in-flight pin guard. A differing existing file is
never replaced. --dry-run writes nothing.

Usage: _build_fixup3_orders_ezek.py --rows repair/rows_v5_cwo23.jsonl --out fixup3 [--dry-run]"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
SP = EZ.parent
R10 = EZ / "ezek_controlling_agent_rulings_e10.v1.json"
RULE_RULINGS = [EZ / "ezek_controlling_agent_rulings_e6.v1.json", EZ / "ezek_controlling_agent_rulings_e7.v1.json",
                EZ / "ezek_controlling_agent_rulings_e9.v1.json"]
S3 = EZ / "ezek_fixup2_wave_review_S3.json"
M23 = EZ / "repair" / "rows_v5_cwo23.manifest.json"
COV22 = EZ / "repair" / "cwo_coverage_v5cwo23" / "CWO-EZ-22.json"
IMPACT = EZ / "proposals" / "toolfix5_batch1" / "impact" / "rows_v5_cwo23.impact.json"
TF5_RECEIPT = SP / "campaign" / "receipts" / "ezek_tools_install_toolfix5_batch1.json"
P03_FX2 = EZ / "fixup2" / "orders_ezek_author_fixup2_p03_a1.json"
SUITE_V5 = EZ / "repair" / "suite_v5_6c843b14" / "rows.jsonl.validator_report.json"
RID = re.compile(r"\bP\d{2}-\d{3}\b")
WAVE, ORDERED_BY = "FIXUP-3", "ezek_controlling_rulings_a1#e10 ruling S3-ROUTING"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def js(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)
    elif isinstance(o, str):
        yield o


def cut(text, start, end, label):
    i = text.find(start)
    j = text.find(end, i + len(start)) if i >= 0 else -1
    if i < 0 or j < 0:
        raise SystemExit("ABORT: %s was not found between its markers" % label)
    return text[i:j + len(end)]


def author_orders(doc, tag_default):
    xid = doc.get("execution_id") or tag_default
    tag = xid.split("#")[-1] if "#" in xid else tag_default
    out = []
    for r in doc.get("rulings", []):
        n = 0
        for o in r.get("orders", []):
            n += 1
            if str(o.get("to", "")).startswith("author_fixup"):
                out.append({"ref": "%s:%s#%d" % (tag, r["id"], n), "execution": xid, "ruling_id": r["id"], "ruling": r.get("ruling"),
                            "decision": r.get("decision"), "reason": r.get("reason"), "evidence": r.get("evidence", []),
                            "order": o["order"], "exact_spans": o.get("exact_spans", [])})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    rows_p, out_dir = EZ / a.rows, EZ / a.out
    rows = [json.loads(l) for l in rows_p.read_text(encoding="utf-8").splitlines() if l.strip()]
    m23 = js(M23)
    if sha(rows_p) != m23["output"]["sha256"]:
        raise SystemExit("ABORT: %s is not CWO-EZ-23's output" % a.rows)
    cov = js(COV22)
    if cov["verdict"] != "RESIDUAL_AS_RULED" or cov["rows_file"]["sha256"] != sha(rows_p):
        raise SystemExit("ABORT: CWO-EZ-22's coverage over the chain head is not RESIDUAL_AS_RULED")
    rec = js(TF5_RECEIPT)
    if rec["impact"]["rows_v5_cwo23"]["sha256"] != sha(IMPACT):
        raise SystemExit("ABORT: the TOOLFIX-5 impact report is not the one its install receipt names")
    imp = js(IMPACT)
    if imp["rows_file"]["sha256"] != sha(rows_p) or imp["undispositioned"] != 0:
        raise SystemExit("ABORT: the TOOLFIX-5 impact report is not over the chain head, or has undispositioned hits")
    by_id = {r["decision_id"]: r for r in rows}
    order_of = {r["decision_id"]: i for i, r in enumerate(rows)}
    part_of = {r["decision_id"]: r["writer_part"] for r in rows}
    spans = {r["span"]: r["decision_id"] for r in rows}
    items = {r["decision_id"]: [] for r in rows}
    part_findings, problems = {}, []

    def add(did, item):
        if did not in items:
            problems.append("item for unknown row %r: %s" % (did, json.dumps(item, ensure_ascii=False)[:160]))
            return
        if item not in items[did]:
            items[did].append(item)

    d10 = js(R10)
    r10 = {r["id"]: r for r in d10["rulings"]}
    routing = {"execution": d10.get("execution_id"), "ruling": r10["S3-ROUTING"]["ruling"], "decision": r10["S3-ROUTING"]["decision"]}
    m = re.search(r"PARTS: SIX, not nine - ((?:p\d\d, )+p\d\d)\.", routing["decision"])
    if not m:
        raise SystemExit("ABORT: S3-ROUTING (1) does not name the six parts in the expected form")
    ruled_parts = [x.strip() for x in m.group(1).split(",")]
    cwo_text = {c["id"]: {k: c.get(k) for k in ("predicate", "fields", "remedy", "coverage_report")} | {"issued_by": d10.get("execution_id")}
                for c in d10.get("corpus_wide_orders", [])}

    # ---- 0. #e10 S3-03's ruled item list: it names each p03 item by row, and it governs S3-03's author order ----
    s303 = r10["S3-03"]["decision"]
    ruled_items = set()
    for rid, cvs in re.findall(r"(P03-\d{3}) ((?:\d+:\d+(?: and )?)+)", cut(s303, "The twelve p03 items (", "verified by this execution", "#e10 S3-03 item list")):
        for cv in re.findall(r"\d+:\d+", cvs):
            c, v = cv.split(":")
            ruled_items.add((rid, "Ezek.%s.%s" % (c, v)))
    item_rows = sorted({rid for rid, _ in ruled_items}, key=order_of.get)
    f303_rows = sorted(set(RID.findall(next(f for f in js(S3)["new_findings"] if f["id"] == "S3-03")["row_or_artifact"])), key=order_of.get)
    if f303_rows != item_rows:
        problems.append("#e10 S3-03's item rows %s differ from S3-03's finding rows %s" % (item_rows, f303_rows))

    def rows_tiling(span):
        a_, b_ = span.split("-")
        i = [k for k, r in enumerate(rows) if r["span"].split("-")[0] == a_]
        j = [k for k, r in enumerate(rows) if r["span"].split("-")[1] == b_]
        return [rows[k]["decision_id"] for k in range(i[0], j[0] + 1)] if len(i) == 1 and len(j) == 1 and i[0] <= j[0] else None

    # ---- 1. #e10 ruling orders to author_fixup, and the general writing rules ----
    orders = author_orders(d10, "e10")
    orders_by_ref = {o["ref"]: o for o in orders}
    brief_rules, bindings, discrepancies = [], {}, []
    for o in orders:
        named = [d for d in RID.findall(o["order"]) if d in by_id]
        on_span = [spans[s] for s in o["exact_spans"] if s in spans]
        missing = [s for s in o["exact_spans"] if s not in spans and not any(s in x for d in named for x in strings(by_id[d]))]
        if not RID.findall(o["order"]) and not o["exact_spans"]:
            brief_rules.append(o["ref"])
            continue
        if o["ruling_id"] == "S3-03":
            # #e10 S3-03 order 1 puts the items into p03's orders by row, so the ruled item list controls. Where this order's exact_spans
            # misstate the item rows, the verified binding is installed and the misstatement is REPORTED, never propagated (E-03 lane).
            hit = item_rows
            unions = [{"span": s, "rows_tiling_it": rows_tiling(s)} for s in missing]
            if any(u["rows_tiling_it"] is None for u in unions):
                problems.append("%s: a span no row carries is not tiled by consecutive current rows: %s" % (o["ref"], unions))
            covered = set(on_span) | {d for u in unions for d in (u["rows_tiling_it"] or [])}
            if set(on_span) != set(item_rows) or missing:
                discrepancies.append({
                    "ref": o["ref"], "execution": o["execution"], "field": "exact_spans", "exact_spans_as_ruled": o["exact_spans"],
                    "governing_ruled_text": "#e10 ruling S3-03's decision names the twelve items by row ('The twelve p03 items (...)'), its order 1 "
                                            "puts them into p03's orders by row, and S3-03's finding names the same eleven rows",
                    "bound_rows": [{"row": d, "span": by_id[d]["span"]} for d in item_rows],
                    "spans_no_current_row_carries": [dict(u, rows_outside_the_item_list=[d for d in (u["rows_tiling_it"] or []) if d not in item_rows])
                                                     for u in unions],
                    "spans_on_rows_outside_the_item_list": [{"span": s, "row": spans[s]} for s in o["exact_spans"] if s in spans and spans[s] not in item_rows],
                    "item_rows_absent_from_exact_spans": [{"row": d, "span": by_id[d]["span"]} for d in item_rows if d not in covered],
                    "disposition": "the order binds to the item rows; the exact_spans list is reported here and never propagated; no span changes "
                                   "(#e4 FIXUP-1 (3)); the author acts only on rows_with_orders"})
        else:
            if named and on_span and set(named) != set(on_span):
                problems.append("%s names rows %s, but its exact_spans are carried by %s" % (o["ref"], named, on_span))
            if missing:
                problems.append("%s names spans no current row carries (no span change is allowed): %s" % (o["ref"], missing))
            hit = named or on_span
        if not hit:
            problems.append("%s binds to no current row" % o["ref"])
        bindings[o["ref"]] = {"named_rows": named, "exact_span_rows": on_span, "bound": sorted(set(hit), key=order_of.get)}
        for d in sorted(set(hit), key=order_of.get):
            add(d, {"kind": "ruling_order", "ref": o["ref"], "op": "replace", "target_span": by_id[d]["span"]})
    for p in RULE_RULINGS:
        for o in author_orders(js(p), p.stem):
            if not RID.findall(o["order"]) and not o["exact_spans"]:
                orders_by_ref[o["ref"]] = o
                brief_rules.append(o["ref"])

    # ---- 2. S3's routed findings, and its replaced_rows defect text ----
    s3 = js(S3)
    executed_by_cwo23 = []
    for f in s3["new_findings"]:
        parts = [x.split(":", 1)[1] for x in f["route"].split("|") if x.startswith("author_fixup:")]
        if not parts:
            continue
        entry = {"kind": "s3_finding", "id": f["id"], "severity": f["severity"], "route": f["route"], "row_or_artifact": f["row_or_artifact"],
                 "claim": f["claim"], "evidence": f["evidence"], "suggested_fix": f.get("suggested_fix")}
        named = set(RID.findall(str(f.get("row_or_artifact", ""))))
        for part in parts:
            if part not in ruled_parts:
                executed_by_cwo23.append({"id": f["id"], "part": part, "rows": sorted(named),
                                          "executed_by": {"cwo": "CWO-EZ-23", "manifest": "repair/" + M23.name, "sha256": sha(M23)}})
                continue
            hit = sorted((d for d in named if part_of.get(d) == part), key=order_of.get)
            if hit:
                for d in hit:
                    add(d, entry)
            else:
                part_findings.setdefault(part, []).append(entry)
    outside_defects = []
    for x in s3["replaced_rows"]:
        if x.get("verdict") != "defect":
            continue
        if x["part"] in ruled_parts:
            add(x["row"], {"kind": "s3_row_defect", "id": "S3 replaced_rows", "row": x["row"], "part": x["part"], "findings": x["findings"]})
        else:
            outside_defects.append({"row": x["row"], "part": x["part"],
                                    "cwo_ez_23_pairs_on_this_row": [c["pair"] for c in m23["changes"] if c["row"] == x["row"]]})

    # ---- 3. CWO-EZ-22 author items, and TOOLFIX-5's impact cross-reference ----
    cov_items = []
    for h in cov["hits"]:
        it = {"kind": "cwo_item", "cwo": "CWO-EZ-22", "routed_by": "repair/cwo_coverage_v5cwo23/CWO-EZ-22.json residual",
              "line_ruled": "ezek_controlling_rulings_a1#e10 ruling S3-16",
              "verbatim": {k: h[k] for k in ("row", "field", "arm", "match", "context")}}
        cov_items.append(it)
        add(h["row"], it)
    crossref, tf5_added = [], 0
    for h in imp["hits"]:
        match = [c for c in cov_items if c["verbatim"]["row"] == h["row"] and c["verbatim"]["field"] == h["field"]
                 and (str(h["match"]) in c["verbatim"]["match"] or c["verbatim"]["match"] in str(h["match"]))]
        if match:
            crossref.append({"row": h["row"], "field": h["field"], "class": h["class"], "covered_by": "CWO-EZ-22 item (%s)" % match[0]["verbatim"]["arm"]})
        else:
            tf5_added += 1
            add(h["row"], {"kind": "toolfix5_impact_item", "id": "TOOLFIX-5", "ordered_by": "ezek_controlling_rulings_a1#e10 ruling TOOLFIX-5 (3)",
                           "verbatim": {k: h.get(k) for k in ("tool", "row", "field", "class", "match", "context")}})
            crossref.append({"row": h["row"], "field": h["field"], "class": h["class"], "covered_by": "its own toolfix5_impact_item"})

    # ---- 4. p03: the S3-03 prose-disclosure items and the grams not to reuse ----
    fx2_marks =[it for e in js(P03_FX2)["rows_with_orders"] for it in e["items"] if it.get("kind") == "mark_item"]
    got_items = {(it["row"], it["pmarks_key"]) for it in fx2_marks}
    if len(fx2_marks) != 12 or got_items != ruled_items:
        problems.append("p03's twelve S2-14 items %s differ from #e10 S3-03's list %s" % (sorted(got_items), sorted(ruled_items)))
    in_prose = cut(s303, "DEFINED in words", "never carries it alone.", "#e10 S3-03 definition")
    for it in fx2_marks:
        item = {"kind": "mark_item", "id": "S3-03", "ordered_by": "ezek_controlling_rulings_a1#e10 ruling S3-03", "row": it["row"],
                "pmarks_key": it["pmarks_key"], "mark_types": it["mark_types"], "role": it["role"], "in_prose": in_prose}
        if it["role"] == "interior":
            item["reason_in_prose"] = "required: the reason the unit does not cut at this interior mark is written in prose (#e10 S3-03)"
        add(it["row"], item)
    worst = js(SUITE_V5)["ngram7"]["worst_reuse"]
    named_grams = [g["gram"] for g in worst if "samekh recorded on this" in g["gram"]]
    if len(named_grams) != 3:
        problems.append("the v5 worst_reuse list does not carry the three samekh grams #e10 S3-03 names: %s" % worst)

    # ---- 5. p04's S3-17 sentence and p08's S3-18 scope ----
    s317 = cut(r10["S3-17"]["decision"], "(3) The p04 orders say in words", "reports it outside the row.", "#e10 S3-17 (3)")
    add("P04-008", {"kind": "s3_17_note", "id": "S3-17", "ordered_by": "ezek_controlling_rulings_a1#e10 ruling S3-17", "row": "P04-008", "text": s317})
    s318 = r10["S3-18"]["decision"]
    scope = cut(s318, "The corrected scope is RECORDED here", "across chs. 6, 19 and 33-39)'.", "#e10 S3-18 scope")
    control = cut(s318, "CONTROL, binding FIXUP-3 and Daniel:", "for every installed digit.", "#e10 S3-18 control")
    verses = re.findall(r"Ezek\.\d+\.\d+|(?<=, )\d+\.\d+", cut(s318, "recurs in 15 verses of Ezekiel - ", " - across chapters", "#e10 S3-18 list"))
    verses = [v if v.startswith("Ezek.") else "Ezek." + v for v in verses]
    if len(verses) != 15:
        problems.append("#e10 S3-18's verified list parsed to %d verses, not 15" % len(verses))
    add("P08-004", {"kind": "s3_18_scope", "id": "S3-18", "ordered_by": "ezek_controlling_rulings_a1#e10 ruling S3-18", "row": "P08-004",
                    "verified_verses": verses, "citation": "(sweep: 15 verses across chs. 6, 19 and 33-39)", "ruled_text": scope, "control": control})

    # ---- write one file per part ----
    stray = sorted(d for d, its in items.items() if its and part_of[d] not in ruled_parts)
    if stray:
        problems.append("items landed on rows outside the six wave parts: %s" % stray)
    src = {"rulings": [{"path": "Ezek/" + R10.name, "sha256": sha(R10)}],
           "rule_rulings": [{"path": "Ezek/" + p.name, "sha256": sha(p)} for p in RULE_RULINGS],
           "rows": {"path": "Ezek/" + a.rows, "sha256": sha(rows_p)},
           "cwo_ez_23_manifest": {"path": "Ezek/repair/" + M23.name, "sha256": sha(M23)},
           "cwo_ez_22_coverage": {"path": "Ezek/repair/cwo_coverage_v5cwo23/CWO-EZ-22.json", "sha256": sha(COV22)},
           "toolfix5_impact": {"path": "Ezek/proposals/toolfix5_batch1/impact/rows_v5_cwo23.impact.json", "sha256": sha(IMPACT)},
           "toolfix5_receipt": {"path": "campaign/receipts/" + TF5_RECEIPT.name, "sha256": sha(TF5_RECEIPT)},
           "s3_review": {"path": "Ezek/" + S3.name, "sha256": sha(S3)},
           "p03_fixup2_orders": {"path": "Ezek/fixup2/" + P03_FX2.name, "sha256": sha(P03_FX2)},
           "v5_suite_report": {"path": "Ezek/repair/suite_v5_6c843b14/rows.jsonl.validator_report.json", "sha256": sha(SUITE_V5)}}
    parts = []
    for r in rows:
        if r["writer_part"] not in parts:
            parts.append(r["writer_part"])
    index = {"schema": "m8_fixup_orders_index.v1", "wave": WAVE, "book": "Ezek", "ordered_by": ORDERED_BY, "sources": src, "parts": {},
             "parts_without_items": [], "findings_executed_by_cwo_ez_23": executed_by_cwo23, "row_defects_outside_the_wave": outside_defects,
             "toolfix5_impact_crossref": {"hits": len(imp["hits"]), "covered_by_cwo_ez_22_items": sum(1 for c in crossref if c["covered_by"].startswith("CWO-EZ-22")),
                                          "own_items": tf5_added, "entries": crossref},
             "order_bindings": bindings, "ruling_text_discrepancies": discrepancies,
             "problems": problems, "brief_rules": {k: orders_by_ref[k] for k in brief_rules}}
    docs = {}
    for part in parts:
        prow = [r for r in rows if r["writer_part"] == part]
        entries = []
        for i, r in enumerate(prow):
            if not items[r["decision_id"]]:
                continue
            entries.append({"decision_id": r["decision_id"], "writer_decision_id": r["writer_decision_id"], "span": r["span"],
                            "ops": sorted({it.get("op", "replace") for it in items[r["decision_id"]]}),
                            "previous_row": {k: prow[i - 1][k] for k in ("decision_id", "span")} if i else None,
                            "next_row": {k: prow[i + 1][k] for k in ("decision_id", "span")} if i + 1 < len(prow) else None,
                            "items": items[r["decision_id"]], "current_row": r})
        if not entries and not part_findings.get(part):
            index["parts_without_items"].append(part)
            continue
        aid = "ezek_author_fixup3_%s_a1" % part
        used_refs = sorted({it["ref"] for e in entries for it in e["items"] if it.get("kind") == "ruling_order"})
        used_cwos = sorted({it["cwo"] for e in entries for it in e["items"] if it.get("cwo")})
        counts = Counter()
        for e in entries:
            for it in e["items"]:
                counts[it.get("cwo") or it.get("id") or it["kind"]] += 1
        counts["part_findings"] = len(part_findings.get(part, []))
        doc = {"schema": "m8_fixup_orders.v1", "wave": WAVE, "book": "Ezek", "part": part, "attempt_id": aid, "execution_id": aid + "#e1",
               "ordered_by": ORDERED_BY, "fixup3_ruling": routing, "sources": src,
               "ruling_orders": {k: orders_by_ref[k] for k in used_refs},
               "brief_rules": {k: orders_by_ref[k] for k in brief_rules},
               "corpus_wide_orders": {k: cwo_text[k] for k in used_cwos if k in cwo_text},
               "part_findings": part_findings.get(part, []),
               "part_rows": [{"decision_id": r["decision_id"], "span": r["span"]} for r in prow],
               "ruling_text_discrepancies": [x for x in discrepancies if x["ref"] in used_refs],
               "rows_with_orders": entries, "new_rows": [], "retire": [], "holds": [],
               "item_counts": dict(sorted(counts.items()))}
        if part == "p03":
            doc["do_not_reuse_grams"] = {"ordered_by": "ezek_controlling_rulings_a1#e10 ruling S3-03",
                                         "source": "Ezek/repair/suite_v5_6c843b14/rows.jsonl.validator_report.json ngram7.worst_reuse",
                                         "grams_named_by_the_ruling": named_grams, "all_worst_reuse": worst}
        docs[part] = doc
        missing_cwo = [k for k in used_cwos if k not in cwo_text]
        if missing_cwo:
            problems.append("%s: CWO ids with no order text in #e10: %s" % (part, missing_cwo))
    if sorted(docs) != sorted(ruled_parts):
        problems.append("parts with items %s differ from the six #e10 names %s" % (sorted(docs), sorted(ruled_parts)))
    summary = {p: {"rows_with_orders": len(d["rows_with_orders"]), "item_counts": d["item_counts"]} for p, d in docs.items()}
    if a.dry_run or problems:
        print(json.dumps({"mode": "DRY_RUN" if a.dry_run else "REFUSED_PROBLEMS", "parts": summary, "parts_without_items": index["parts_without_items"],
                          "executed_by_cwo23": executed_by_cwo23, "outside_defects": outside_defects,
                          "toolfix5_crossref": {k: v for k, v in index["toolfix5_impact_crossref"].items() if k != "entries"},
                          "bindings": bindings, "discrepancies": discrepancies, "brief_rules": brief_rules, "problems": problems},
                         ensure_ascii=False, indent=1))
        return 1 if problems else 0
    targets = [out_dir / ("orders_%s.json" % d["attempt_id"]) for d in docs.values()] + [out_dir / "orders_index.json"]
    g = subprocess.run([sys.executable, str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek"] + sum([["--target", str(t)] for t in targets], []),
                       capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if g.returncode != 0:
        raise SystemExit("ABORT: an orders target is pinned:\n" + g.stdout)
    out_dir.mkdir(parents=True, exist_ok=True)
    for part, doc in docs.items():
        p = out_dir / ("orders_%s.json" % doc["attempt_id"])
        body = json.dumps(doc, ensure_ascii=False, indent=1)
        if p.exists() and p.read_text(encoding="utf-8") != body:
            raise SystemExit("ABORT: %s exists with different content; orders are never silently replaced" % p.name)
        p.write_text(body, encoding="utf-8", newline="\n")
        index["parts"][part] = {"file": p.name, "sha256": sha(p), **summary[part]}
    ip = out_dir / "orders_index.json"
    body = json.dumps(index, ensure_ascii=False, indent=1)
    if ip.exists() and ip.read_text(encoding="utf-8") != body:
        raise SystemExit("ABORT: orders_index.json exists with different content")
    ip.write_text(body, encoding="utf-8", newline="\n")
    print(json.dumps({"mode": "WRITTEN", "index_sha256": sha(ip), "parts": summary, "ruling_text_discrepancies": [d["ref"] for d in discrepancies],
                      "problems": problems}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
