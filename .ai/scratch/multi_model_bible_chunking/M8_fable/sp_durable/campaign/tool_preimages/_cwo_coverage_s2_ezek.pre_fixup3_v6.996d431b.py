#!/usr/bin/env python3
"""Coverage reports for the three corpus-wide orders ruled by ezek_controlling_rulings_a1#e9 (CWO-EZ-19, CWO-EZ-20, CWO-EZ-21),
each its own report (E-18) over the rows file the ruling names:
  - stage v4: CWO-EZ-19 over repair/rows_v4_cwo19.jsonl and CWO-EZ-20 over repair/rows_v4_cwo20.jsonl must read residual 0;
    CWO-EZ-21 over repair/rows_v4_cwo21.jsonl must read residual exactly the fifteen author-half hits the ruling lists;
  - stage v5: all three over repair/rows_v5_fixup2.jsonl must read residual 0, and CWO-EZ-19's v5 report also carries the
    close-key mark_symmetry check for the seven rows the ruling names (--suite-report is required for it).
A report is never replaced by differing bytes. Exit 1 when the residual is not what the ruling requires; that returns to the
controlling lane. Nothing here judges content.
Usage: _cwo_coverage_s2_ezek.py --cwo CWO-EZ-19|CWO-EZ-20|CWO-EZ-21 --stage v4|v5 --rows <rows under SP/Ezek>
       [--suite-report <validator report under SP/Ezek>]
"""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
RULINGS_E9 = EZ / "ezek_controlling_agent_rulings_e9.v1.json"
OSS_RE = re.compile(r"closure\.(?:parashah_\w+|pe|samekh)\b")
ONE_RE = re.compile("“([^“”\\s]+)”")
ENN = re.compile(r"\bE-\d{2}\b")
CAMP = re.compile(r"\bcampaign\b", re.I)
AUTHOR_HALF = Counter({("P03-001", "E-02"): 1, ("P03-020", "E-02"): 1, ("P08-010", "E-02"): 1,
                       **{(r, "campaign"): 1 for r in ("P01-006", "P03-003", "P03-007", "P03-014", "P03-020", "P04-001", "P04-002",
                                                        "P04-004", "P04-007", "P08-002", "P09-002", "P09-007")}})
SPAN = re.compile(r"^Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)$")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def leaves(o, path=""):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, ("%s.%s" % (path, k)) if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, "%s[%d]" % (path, i))


def residual(cwo, rows):
    out = []
    for r in rows:
        rid = r["decision_id"]
        if cwo == "CWO-EZ-19":
            for i, k in enumerate(r.get("observed_substrate_signals") or []):
                if isinstance(k, str) and OSS_RE.search(k):
                    out.append({"row": rid, "field": "observed_substrate_signals[%d]" % i, "match": k})
            continue
        for p, s in leaves(r):
            if cwo == "CWO-EZ-20":
                if "web:" not in s:
                    out += [{"row": rid, "field": p, "match": m.group(0)} for m in ONE_RE.finditer(s)]
            else:
                out += [{"row": rid, "field": p, "match": m.group(0)} for m in ENN.finditer(s)]
                out += [{"row": rid, "field": p, "match": m.group(0)} for m in CAMP.finditer(s)]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cwo", required=True, choices=["CWO-EZ-19", "CWO-EZ-20", "CWO-EZ-21"])
    ap.add_argument("--stage", required=True, choices=["v4", "v5"])
    ap.add_argument("--rows", required=True)
    ap.add_argument("--suite-report")
    a = ap.parse_args()
    e9 = json.loads(RULINGS_E9.read_text(encoding="utf-8"))
    ruled = next(c for c in e9["corpus_wide_orders"] if c["id"] == a.cwo)
    rows_p = EZ / a.rows
    rows = [json.loads(l) for l in rows_p.read_text(encoding="utf-8").splitlines() if l.strip()]
    res = residual(a.cwo, rows)
    report = {"schema": "m8_cwo_coverage.v1", "book": "Ezek", "cwo": a.cwo, "stage": a.stage,
              "ordered_by": "ezek_controlling_rulings_a1#e9 corpus_wide_orders",
              "ruled_predicate": ruled["predicate"], "ruled_fields": ruled["fields"], "ruled_remedy": ruled["remedy"],
              "ruled_coverage_report": ruled["coverage_report"],
              "executed_as": "its own coverage sweep (E-18) over the rows file the ruling names",
              "rows_file": {"path": "Ezek/" + a.rows.replace("\\", "/"), "sha256": sha(rows_p), "rows": len(rows)}}
    mp = rows_p.with_name(rows_p.stem + ".manifest.json")
    report["rows_manifest"] = {"path": "Ezek/" + str(mp.relative_to(EZ)).replace("\\", "/"), "sha256": sha(mp)} if mp.is_file() else None
    report["residual_count"], report["residual"] = len(res), res
    ok = True
    if a.cwo == "CWO-EZ-21" and a.stage == "v4":
        found = Counter((h["row"], "campaign" if h["match"].casefold() == "campaign" else h["match"]) for h in res)
        report["expected_residual"] = "exactly the fifteen author-half hits the ruling lists, routed to FIXUP-2"
        report["expected_residual_rows"] = sorted("%s %s" % k for k in AUTHOR_HALF)
        ok = found == AUTHOR_HALF
        report["verdict"] = "RESIDUAL_AS_RULED" if ok else "RESIDUAL_DIFFERS"
    else:
        ok = not res
        report["verdict"] = "COVERED" if ok else "RESIDUAL_DIFFERS"
    if a.cwo == "CWO-EZ-19" and a.stage == "v5":
        if not a.suite_report:
            raise SystemExit("ABORT: the v5 CWO-EZ-19 report requires --suite-report for the close-key check")
        rp = EZ / a.suite_report
        flags = json.loads(rp.read_text(encoding="utf-8"))["mark_symmetry"]["flags"]
        ruled_rows = sorted(set(re.findall(r"P\d\d-\d{3}", ruled["remedy"])))
        by_id = {r["decision_id"]: r for r in rows}
        checks = []
        for rid in ruled_rows:
            c2, v2 = map(int, SPAN.match(by_id[rid]["span"]).groups()[2:])
            key = "Ezek.%d.%d" % (c2, v2)
            hit = [f for f in flags if f.get("rule") == "mark_symmetry_gap" and f.get("decision_id") == rid and f.get("undisclosed_mt_key") == key]
            checks.append({"row": rid, "close_key": key, "mark_symmetry_gap_at_close_key": bool(hit)})
        report["suite_report"] = {"path": "Ezek/" + a.suite_report.replace("\\", "/"), "sha256": sha(rp)}
        report["close_key_check"] = checks
        if any(c["mark_symmetry_gap_at_close_key"] for c in checks):
            ok = False
            report["verdict"] = "RESIDUAL_DIFFERS"
    report["field_scope"] = ("observed_substrate_signals elements only" if a.cwo == "CWO-EZ-19"
                             else "every string leaf of every field, boundary_evidence_refs entries and tags included")
    report["limit"] = "a residual count proves the predicate over the named rows file and nothing beyond it; it judges no content"
    out_dir = EZ / "repair" / ("cwo_coverage_%s" % a.stage)
    out_dir.mkdir(exist_ok=True)
    out = out_dir / ("%s.json" % a.cwo)
    body = json.dumps(report, ensure_ascii=False, indent=1)
    if out.exists() and out.read_text(encoding="utf-8") != body:
        raise SystemExit("ABORT: %s exists with different content; never replaced" % out)
    out.write_text(body, encoding="utf-8", newline="\n")
    print(json.dumps({"cwo": a.cwo, "stage": a.stage, "rows": report["rows_file"], "residual_count": len(res),
                      "verdict": report["verdict"], "report": str(out.relative_to(EZ)).replace("\\", "/")}, ensure_ascii=False, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
