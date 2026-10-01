#!/usr/bin/env python3
"""Per-CWO coverage sweeps after the author wave (E-18). The corpus-wide items were routed into the per-part author
executions under ruling R2, each carrying its CWO label. Each corpus-wide order's narrowed predicate is re-evaluated here
as its OWN sweep over the applied rows, and each gets its own report stamped with the predicate label verbatim. A CWO is
covered only when its residual is empty. This tool judges nothing beyond its predicates and edits nothing.

  CWO-EZ-01 refs form, narrowed to its predicate (object entries and the routed unprefixed strings): every
            boundary_evidence_refs entry is a string opening on a witness-prefixed ref, and citation_sweep reports no
            malformed ref. Entries outside the strict ruling-R1 shape are listed as triage, not residual.
  CWO-EZ-02 Hebrew binding: citation_sweep reports no Hebrew run lacking an oshb: ref in its field, and none that fails
            to collate
  CWO-EZ-04 K/Q bytes: the normalizer (E-01) reports 0 defects and 0 fixed
  CWO-EZ-05 marks and paseq: citation_sweep reports no pe/samekh/paseq claim the inventory contradicts; check_marks'
            paragraph_mark_claim flags are listed (FLAGS, triage for primaries)
  CWO-EZ-06 tags vocabulary (ruling P5): every tags entry is 1-5 words of Hebrew with an oshb: ref, no Strong's number
  CWO-EZ-07 boilerplate: ngram7 reports no 7-gram shared by 10 or more rows
  CWO-EZ-08 register: check_register reports 0 flags
  CWO-EZ-09 cap: cap_sweep reports 0 failures
CWO-EZ-03 is ruled by the controlling agent, not re-evaluated here.

Usage: _cwo_coverage_ezek.py --rows <applied rows> --report <suite report over those exact bytes> --out <dir>
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
sys.path.insert(0, str(EZ / "tools"))
from ezek_lib import HEB_RUN  # noqa: E402

RULINGS = EZ / "ezek_controlling_agent_rulings.v1.json"
REF_ONE = r"(?:oshb|web):Ezek\.\d+\.\d+(?:-Ezek\.\d+\.\d+)?"
CANON_REF = re.compile(r"^%s(?:\s*=\s*%s)?(?:\s+\(.*\))?$" % (REF_ONE, REF_ONE), re.S)   # strict R1 shape (triage)
WITNESS_PREFIX = re.compile(r"^(?:oshb|web):Ezek\.\d+\.\d+")                               # CWO-EZ-01's narrowed predicate
STRONGS = re.compile(r"\b[HG]\d{2,5}\b")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--orders-index", help="author orders index, to name the executions that carried each CWO's items (E18-1)")
    ap.add_argument("--author-receipts", help="author attempt receipts, for the LANDED execution id of each part")
    a = ap.parse_args()
    rows_p = Path(a.rows) if Path(a.rows).is_absolute() else EZ / a.rows
    rep_p = Path(a.report) if Path(a.report).is_absolute() else EZ / a.report
    out_dir = Path(a.out) if Path(a.out).is_absolute() else EZ / a.out
    rows = [json.loads(l) for l in rows_p.read_text(encoding="utf-8").splitlines() if l.strip()]
    rep = json.loads(rep_p.read_text(encoding="utf-8"))
    if sha(rep["rows_file"]) != sha(rows_p):
        raise SystemExit("ABORT: the report was not produced over the exact bytes of the rows file")
    cwo = {c["id"]: c for c in json.loads(RULINGS.read_text(encoding="utf-8"))["corpus_wide_orders"]}
    cs = rep["citation_sweep"]["problems"]

    def cs_class(*needles):
        return [p for p in cs if any(n in p for n in needles)]

    residual = {
        # the NARROWED predicate: object entries converted, and the routed unprefixed strings given a witness prefix
        "CWO-EZ-01": [{"row": r["decision_id"], "entry": e} for r in rows for e in r.get("boundary_evidence_refs", [])
                      if not (isinstance(e, str) and WITNESS_PREFIX.match(e.strip()))] + [{"citation_sweep": p} for p in cs_class("malformed ref")],
        "CWO-EZ-02": [{"citation_sweep": p} for p in cs_class("has NO oshb: ref", "does not collate")],
        "CWO-EZ-04": ([{"normalizer_defect": d} for d in rep["hebrew_normalize_dryrun"].get("defects", [])]
                      + ([{"normalizer_fixed": rep["hebrew_normalize_dryrun"]["fixed"]}] if rep["hebrew_normalize_dryrun"].get("fixed") else [])),
        "CWO-EZ-05": [{"citation_sweep": p} for p in cs_class("claims pe but", "claims samekh but", "claims paseq but",
                                                               "claims petuchah but", "claims setumah but")],
        "CWO-EZ-06": [],
        "CWO-EZ-07": [{"gram": g["gram"], "rows": g["rows"], "row_ids": g.get("row_ids")} for g in rep["ngram7"].get("offending_7grams", [])],
        "CWO-EZ-08": [{k: f.get(k) for k in ("decision_id", "field", "class", "match")} for f in rep["register"].get("flags", [])],
        "CWO-EZ-09": [{"cap_sweep": f} for f in rep["cap_sweep"].get("failures", [])],
    }
    for r in rows:
        for i, e in enumerate(r.get("strong_or_hebrew_tags_used") or []):
            heb = HEB_RUN.findall(e) if isinstance(e, str) else []
            words = sum(len(h.split()) for h in heb)
            why = [w for w, bad in (("no Hebrew", not heb), ("more than 5 Hebrew words", words > 5),
                                    ("no oshb: ref in the entry", "oshb:Ezek." not in str(e)),
                                    ("a Strong's number", bool(STRONGS.search(str(e))))) if bad]
            if why:
                residual["CWO-EZ-06"].append({"row": r["decision_id"], "field": "strong_or_hebrew_tags_used[%d]" % i, "why": why})
    # triage: listed in the CWO's report, never counted as its residual (outside the narrowed predicate)
    triage = {"CWO-EZ-05": [{k: f.get(k) for k in ("decision_id", "rule", "claimed", "verse_cited")}
                            for f in rep["mark_symmetry"].get("flags", []) if f.get("rule") == "paragraph_mark_claim"],
              "CWO-EZ-01": [{"row": r["decision_id"], "entry": e, "why": "outside the strict ruling-R1 shape (ref, optional "
                             "dual, then a parenthesised disclosure)"} for r in rows for e in r.get("boundary_evidence_refs", [])
                            if isinstance(e, str) and WITNESS_PREFIX.match(e.strip()) and not CANON_REF.match(e.strip())]}

    # E18-1 condition (3) of ezek_controlling_rulings_a1#e3: each report names the author executions that carried its items
    carriers = {}
    if a.orders_index and a.author_receipts:
        idx_p = Path(a.orders_index) if Path(a.orders_index).is_absolute() else EZ / a.orders_index
        rec_p = Path(a.author_receipts) if Path(a.author_receipts).is_absolute() else EZ / a.author_receipts
        idx = json.loads(idx_p.read_text(encoding="utf-8"))
        landed = {}
        for rr in (json.loads(l) for l in rec_p.read_text(encoding="utf-8").splitlines() if l.strip()):
            if rr.get("outcome") == "LANDED":
                landed[rr["attempt_id"]] = rr["execution_id"]
        for part, v in idx["parts"].items():
            aid = "ezek_author_%s_a1" % part
            for key in v.get("item_counts", {}):
                if key.startswith("CWO-EZ-"):
                    carriers.setdefault(key, []).append(landed.get(aid, "%s (no LANDED execution)" % aid))
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = {}
    for cid, res in residual.items():
        doc = {"schema": "m8_cwo_coverage.v1", "book": "Ezek", "cwo": cid,
               "narrowed_predicate_label": cwo[cid]["predicate"], "order": cwo[cid]["order"],
               "executed_as": "its own post-wave coverage sweep (E-18); items were routed into the per-part author "
                              "executions under ruling R2 with this label",
               "rows_file": {"path": str(rows_p), "sha256": sha(rows_p), "rows": len(rows)},
               "suite_report": {"path": str(rep_p), "sha256": sha(rep_p)},
               "carried_by_executions": sorted(carriers.get(cid, [])) if carriers else "not supplied (pre-wave baseline)",
               "residual_count": len(res), "residual": res, "triage_flags": triage.get(cid, []),
               "verdict": "COVERED" if not res else "NOT_COVERED"}
        p = out_dir / ("%s.json" % cid)
        body = json.dumps(doc, ensure_ascii=False, indent=1)
        if p.exists() and p.read_text(encoding="utf-8") != body:
            raise SystemExit("ABORT: %s exists with different content" % p)
        p.write_text(body, encoding="utf-8", newline="\n")
        summary[cid] = {"verdict": doc["verdict"], "residual": len(res), "triage_flags": len(doc["triage_flags"])}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0 if all(v["verdict"] == "COVERED" for v in summary.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
