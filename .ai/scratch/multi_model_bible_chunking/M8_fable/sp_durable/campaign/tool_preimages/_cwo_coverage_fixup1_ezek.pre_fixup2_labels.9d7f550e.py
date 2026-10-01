#!/usr/bin/env python3
"""Per-CWO coverage sweeps after FIXUP-1 for CWO-EZ-14..18 (E-18). ezek_controlling_rulings_a1#e4 ordered these five
corpus-wide orders and #e6 amended CWO-EZ-18. Their author items went into the per-part FIXUP-1 executions, each stamped with its
CWO id (#e4 FIXUP-1 (1)). Each order is re-evaluated here as its OWN sweep over the applied rows and gets its own report,
stamped with its predicate verbatim. A CWO is covered only when its residual is empty. This tool judges nothing beyond its
predicates and edits nothing.

  CWO-EZ-14 register: check_register reports 0 flags. The report also states in words the coverage limit that #e5 REG-TF2-1 and
            #e6 T5-REGISTER (b) require, with the ruled text: the rows and shapes no arm sees are proven by S2's read-back.
  CWO-EZ-15 grapheme and word boundaries: the normalizer (E-01) reports 0 defects and 0 fixed, and citation_sweep reports no
            problem of the class the FIXUP-1 orders builder bound to this id ('does not collate against any nearby cited ref',
            outside [CWO-EZ-16]).
  CWO-EZ-16 refs-entry binding: citation_sweep reports no problem stamped [CWO-EZ-16].
  CWO-EZ-17 unbalanced curly double quotes: check_web_quotes reports no e15d flag.
  CWO-EZ-18 curly quotes without a web: ref: check_web_quotes' class 'curly quote with NO web: ref in its field' reads 0 across
            all fields. #e7 ruling CWO18-R1-1's final_check on P08-013 is evaluated too, and a failed check counts as residual.
Every suite member these predicates read must stand at its TOOLFIX-2 install digest (ezek_tools_install_toolfix2_batch3.json),
the digests T5 reviewed; otherwise the tool aborts. The orders index must have been built on the chain head given.

Usage: _cwo_coverage_fixup1_ezek.py --rows <applied rows> --report <suite report over those exact bytes> --out <dir>
       --chain-head repair/rows_v3_cwo18.jsonl --cwo01 <CWO-EZ-01 coverage report over the same rows>
       [--orders-index fixup1/orders_index.json] [--fixup-receipts fixup1/ezek_author_fixup_attempt_receipts.jsonl]
"""
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
SP = EZ.parent
_spec = importlib.util.spec_from_file_location("cwo_coverage_ezek", EZ / "_cwo_coverage_ezek.py")
_cov = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cov)
CANON_REF = _cov.CANON_REF

RULINGS_E4 = EZ / "ezek_controlling_agent_rulings_e4.v1.json"
RULINGS_E5 = EZ / "ezek_controlling_agent_rulings_e5.v1.json"
RULINGS_E6 = EZ / "ezek_controlling_agent_rulings_e6.v1.json"
RULINGS_E7 = EZ / "ezek_controlling_agent_rulings_e7.v1.json"
TF2_RECEIPT = SP / "campaign" / "receipts" / "ezek_tools_install_toolfix2_batch3.json"
MEMBERS = ("citation_sweep.py", "check_register.py", "check_web_quotes.py", "normalize_hebrew_in_json.py", "ezek_lib.py")
SWEEP_MANIFESTS = (("CWO-EZ-13", "repair/rows_v3_cwo13.manifest.json"), ("CWO-EZ-18", "repair/rows_v3_cwo18.manifest.json"))
CWO15_PROBLEM = ("does not collate against any nearby cited ref",)   # the needle _build_fixup_orders_ezek.py bound its items by
CWO16_MARK = "[CWO-EZ-16]"
E15D = "e15d_unequal_curly_double_quotes"
NO_REF = "curly quote with NO web: ref in its field"
R1_ROW, R1_INDEX = "P08-013", 1   # #e7 CWO18-R1-1: the one pinned boundary_evidence_refs entry outside the strict R1 shape
LIMIT_MARKS = ((RULINGS_E5, "COVERAGE LIMIT stated for CWO-EZ-14:", None),
               (RULINGS_E6, "(b) T5's five evasions", "(c) under CWO-EZ-14"))
LIMIT_SENTENCE = ("COVERAGE LIMIT: this residual-0 sweep proves the classes check_register's arms see, over the whole corpus, and "
                  "nothing beyond them. The three S1-05 rows no arm can see, P07-009, P09-002 and P10-007, were FIXUP-1 author items "
                  "carrying S1's quoted text, and S2's read-back proves them. T5's five evasions, 'the prior reading of this unit', "
                  "'as first drafted', 'the earlier span', 'the second of three rows' and 'previously held to 30:19', are row talk "
                  "that S1-05 and CWO-EZ-14 still bar although no arm sees them, and S2's read-back is the proof for those shapes.")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def at(p):
    p = Path(p)
    return p if p.is_absolute() else EZ / p


def ruled_text(path, start, end):
    doc = json.loads(path.read_text(encoding="utf-8"))
    hits = [r for r in doc.get("rulings", []) if start in str(r.get("decision", ""))]
    if len(hits) != 1:
        raise SystemExit("ABORT: %d rulings in %s carry %r" % (len(hits), path.name, start))
    text = hits[0]["decision"][hits[0]["decision"].index(start):]
    if end is not None:
        if end not in text:
            raise SystemExit("ABORT: %r not found after %r in %s" % (end, start, path.name))
        text = text[:text.index(end)]
    return hits[0].get("id"), text.rstrip(" ;")


def final_check_order():
    found = []

    def walk(o):
        if isinstance(o, dict):
            if o.get("to") == "final_check" and isinstance(o.get("order"), str):
                found.append(o["order"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(json.loads(RULINGS_E7.read_text(encoding="utf-8")))
    if len(found) != 1:
        raise SystemExit("ABORT: #e7 carries %d final_check orders, not 1" % len(found))
    return found[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--chain-head", required=True, help="the rows the FIXUP-1 orders were built on")
    ap.add_argument("--cwo01", required=True, help="CWO-EZ-01's coverage report over the same rows (#e7 final_check)")
    ap.add_argument("--orders-index", default="fixup1/orders_index.json")
    ap.add_argument("--fixup-receipts", default="fixup1/ezek_author_fixup_attempt_receipts.jsonl")
    a = ap.parse_args()
    rows_p, rep_p, out_dir, head_p, c01_p, idx_p, rec_p = map(at, (a.rows, a.report, a.out, a.chain_head, a.cwo01, a.orders_index,
                                                                  a.fixup_receipts))
    rows = [json.loads(l) for l in rows_p.read_text(encoding="utf-8").splitlines() if l.strip()]
    rep = json.loads(rep_p.read_text(encoding="utf-8"))
    if sha(rep["rows_file"]) != sha(rows_p):
        raise SystemExit("ABORT: the report was not produced over the exact bytes of the rows file")
    tf2 = json.loads(TF2_RECEIPT.read_text(encoding="utf-8"))["files"]
    members = {}
    for m in MEMBERS:
        got, want = sha(EZ / "tools" / m), tf2[m]["after"]
        if got != want:
            raise SystemExit("ABORT: tools/%s is %s, not its TOOLFIX-2 install digest %s" % (m, got[:16], want[:16]))
        members["tools/" + m] = got
    idx = json.loads(idx_p.read_text(encoding="utf-8"))
    if idx["sources"]["rows"]["sha256"] != sha(head_p):
        raise SystemExit("ABORT: the orders index was not built on %s" % head_p.name)
    c01 = json.loads(c01_p.read_text(encoding="utf-8"))
    if c01.get("cwo") != "CWO-EZ-01" or c01["rows_file"]["sha256"] != sha(rows_p):
        raise SystemExit("ABORT: %s is not CWO-EZ-01's report over these rows" % c01_p.name)
    e4 = {c["id"]: c for c in json.loads(RULINGS_E4.read_text(encoding="utf-8"))["corpus_wide_orders"]}
    e6 = {c["id"]: c for c in json.loads(RULINGS_E6.read_text(encoding="utf-8"))["corpus_wide_orders"]}
    cs = rep["citation_sweep"]
    cs_all = [str(p) for p in (cs.get("problems") or []) + (cs.get("nfd_degraded") or []) + (cs.get("prose_pair_problems") or [])]
    nd = rep["hebrew_normalize_dryrun"]
    wq = rep["web_quotes"].get("flags") or []

    def row_at(path):
        m = re.match(r"\[(\d+)\]", str(path))
        return rows[int(m.group(1))]["decision_id"] if m else None

    residual = {
        "CWO-EZ-14": [{k: f.get(k) for k in ("decision_id", "field", "class", "match")} for f in rep["register"].get("flags") or []],
        "CWO-EZ-15": ([{"normalizer_defect": x} for x in nd.get("defects") or []]
                      + ([{"normalizer_fixed": nd["fixed"]}] if nd.get("fixed") else [])
                      + [{"citation_sweep": p} for p in cs_all if CWO16_MARK not in p and any(n in p for n in CWO15_PROBLEM)]),
        "CWO-EZ-16": [{"citation_sweep": p} for p in cs_all if CWO16_MARK in p],
        "CWO-EZ-17": [{"row": row_at(f.get("path")), "path": f.get("path"), "issue": f.get("issue")} for f in wq
                      if str(f.get("issue", "")).startswith(E15D)],
        "CWO-EZ-18": [{"row": row_at(f.get("path")), "path": f.get("path"), "quote": f.get("quote")} for f in wq
                      if f.get("issue") == NO_REF],
    }

    # #e7 CWO18-R1-1 final_check on P08-013
    pos = {r["decision_id"]: i for i, r in enumerate(rows)}
    i13 = pos[R1_ROW]
    after = rows[i13]["boundary_evidence_refs"][R1_INDEX]
    head = {}
    for l in head_p.read_text(encoding="utf-8").splitlines():
        if l.strip():
            r = json.loads(l)
            head[r["decision_id"]] = r
    before = head[R1_ROW]["boundary_evidence_refs"][R1_INDEX]
    on_row = [f for f in wq if f.get("issue") == NO_REF and str(f.get("path", "")).startswith("[%d]." % i13)]
    reshaped = bool(CANON_REF.match(after.strip()))
    fc = {"ordered_by": "ezek_controlling_rulings_a1#e7 ruling CWO18-R1-1", "order_verbatim": final_check_order(),
          "row": R1_ROW, "entry": "[%d].boundary_evidence_refs[%d]" % (i13, R1_INDEX),
          "entry_before_fixup1": before, "entry_after_fixup1": after,
          "no_ref_class_on_row_all_fields": len(on_row), "reshaped_to_strict_r1_shape": reshaped}
    if reshaped:
        row_problems = [p for p in cs_all if p.split(":", 1)[0] == R1_ROW]
        fc["citation_sweep_problems_on_row"] = len(row_problems)
        ok = not on_row and not row_problems
    else:
        names_same = any(t.get("row") == R1_ROW and t.get("entry") == after for t in c01.get("triage_flags") or [])
        fc["cwo01_report"] = {"path": str(c01_p), "sha256": sha(c01_p)}
        fc["cwo01_triage_names_same_entry"] = names_same
        ok = not on_row and names_same
    fc["satisfied"] = ok
    if not ok:
        residual["CWO-EZ-18"].append({"e7_final_check": "not satisfied",
                                      "detail": {k: v for k, v in fc.items() if k != "order_verbatim"}})

    landed = {}
    for l in rec_p.read_text(encoding="utf-8").splitlines():
        if l.strip():
            rr = json.loads(l)
            if rr.get("outcome") == "LANDED":
                landed[rr["attempt_id"]] = rr["execution_id"]
    carriers, routed = {}, {}
    for part, v in sorted(idx["parts"].items()):
        aid = "ezek_author_fixup_%s_a1" % part
        for key, n in v.get("item_counts", {}).items():
            if key.startswith("CWO-EZ-"):
                carriers.setdefault(key, []).append(landed.get(aid, "%s (no LANDED execution)" % aid))
                routed[key] = routed.get(key, 0) + n
    manifests = [{"cwo": c, "path": "Ezek/" + m, "sha256": sha(EZ / m)} for c, m in SWEEP_MANIFESTS]
    limit_text = {}
    for p, s, e in LIMIT_MARKS:
        rid, text = ruled_text(p, s, e)
        limit_text["ezek_controlling_rulings_a1#%s ruling %s" % (p.name.split("_")[-1].split(".")[0], rid)] = text

    out_dir.mkdir(parents=True, exist_ok=True)
    summary = {}
    for cid, res in residual.items():
        src = e6[cid] if cid == "CWO-EZ-18" else e4[cid]
        doc = {"schema": "m8_cwo_coverage.v1", "book": "Ezek", "cwo": cid,
               "ordered_by": ("ezek_controlling_rulings_a1#e4 corpus_wide_orders, as amended by #e6" if cid == "CWO-EZ-18"
                              else "ezek_controlling_rulings_a1#e4 corpus_wide_orders"),
               "narrowed_predicate_label": src["predicate"], "order": src["order"],
               "executed_as": "its own post-FIXUP-1 coverage sweep (E-18); its author items were routed into the per-part FIXUP-1 "
                              "executions stamped with this id (#e4 FIXUP-1 (1))",
               "rows_file": {"path": str(rows_p), "sha256": sha(rows_p), "rows": len(rows)},
               "suite_report": {"path": str(rep_p), "sha256": sha(rep_p)},
               "suite_members_at_toolfix2_install_digest": members,
               "orders_index": {"path": str(idx_p), "sha256": sha(idx_p), "built_on": idx["sources"]["rows"]},
               "author_items_routed": routed.get(cid, 0),
               "carried_by_executions": sorted(carriers.get(cid, [])),
               "residual_count": len(res), "residual": res,
               "verdict": "COVERED" if not res else "NOT_COVERED"}
        if cid == "CWO-EZ-14":
            doc["coverage_limit"] = LIMIT_SENTENCE
            doc["coverage_limit_ruled_text"] = limit_text
        if cid == "CWO-EZ-18":
            doc["amends"] = src.get("amends")
            doc["e4_order_verbatim"], doc["e4_predicate_verbatim"] = e4[cid]["order"], e4[cid]["predicate"]
            doc["sweep_manifests"] = manifests
            doc["e7_final_check"] = fc
        p = out_dir / ("%s.json" % cid)
        body = json.dumps(doc, ensure_ascii=False, indent=1)
        if p.exists() and p.read_text(encoding="utf-8") != body:
            raise SystemExit("ABORT: %s exists with different content" % p)
        p.write_text(body, encoding="utf-8", newline="\n")
        summary[cid] = {"verdict": doc["verdict"], "residual": len(res), "author_items_routed": doc["author_items_routed"],
                        "carriers": len(doc["carried_by_executions"])}
    summary["e7_final_check_satisfied"] = fc["satisfied"]
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0 if all(v["verdict"] == "COVERED" for k, v in summary.items() if k.startswith("CWO-")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
