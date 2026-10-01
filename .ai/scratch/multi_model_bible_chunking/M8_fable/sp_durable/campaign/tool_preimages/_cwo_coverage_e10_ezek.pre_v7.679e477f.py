#!/usr/bin/env python3
"""Coverage reports for the corpus-wide orders ruled by ezek_controlling_rulings_a1#e10. Each report is its own (E-18), over the rows
file the ruling names.

  --cwo CWO-EZ-22 --stage v5       over repair/rows_v5_fixup2.jsonl. Every hit is listed with row, field, arm, matched text, 80
                                   characters of context and its disposition: 'CWO-EZ-23 pair NN' when the hit lies inside that pair's
                                   old bytes in the same field, else 'FIXUP-3 author item'. The counts must equal the ruling's measured
                                   counts, and every hit in p05, p06, p09, p10 or p11 must be a pair.
  --cwo CWO-EZ-22 --stage v5cwo23  over repair/rows_v5_cwo23.jsonl. The residual must be exactly the ruled FIXUP-3 author items: the
                                   stated count, on the listed rows, with 0 on p05, p06, p09, p10 and p11.
  --cwo CWO-EZ-22 --stage v6       over repair/rows_v6_fixup3.jsonl. The residual must be 0 on all six arms.
  --cwo CWO-EZ-23 --stage v6       over repair/rows_v6_fixup3.jsonl. Each pair's new bytes must be present exactly once in its field
                                   and its old bytes absent, 33 of 33.

A report is never replaced by differing bytes. Exit 1 when the result is not what the ruling requires; that returns to the controlling
lane. Nothing here judges content.
Usage: _cwo_coverage_e10_ezek.py --cwo CWO-EZ-22|CWO-EZ-23 --stage v5|v5cwo23|v6 --rows <rows under SP/Ezek>
"""
import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

from _cwo22_arms import CONTENT_LIST_FIELDS, CONTENT_STR_FIELDS, PAIR_PARTS, WAVE_PARTS, arms, get_field, hits, pairs, ruled, ruled_counts

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
OUT_DIRS = {"v5": "cwo_coverage_v5", "v5cwo23": "cwo_coverage_v5cwo23", "v6": "cwo_coverage_v6"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cwo", required=True, choices=["CWO-EZ-22", "CWO-EZ-23"])
    ap.add_argument("--stage", required=True, choices=["v5", "v5cwo23", "v6"])
    ap.add_argument("--rows", required=True)
    a = ap.parse_args()
    if a.cwo == "CWO-EZ-23" and a.stage != "v6":
        raise SystemExit("ABORT: CWO-EZ-23's coverage report is the v6 verification; its sweep manifest is the record before v6")
    spec = ruled(a.cwo)
    rows_p = EZ / a.rows
    rows = [json.loads(l) for l in rows_p.read_text(encoding="utf-8").splitlines() if l.strip()]
    by_id = {r["decision_id"]: r for r in rows}
    report = {"schema": "m8_cwo_coverage.v1", "book": "Ezek", "cwo": a.cwo, "stage": a.stage,
              "ordered_by": "ezek_controlling_rulings_a1#e10 corpus_wide_orders",
              "ruled_predicate": spec["predicate"], "ruled_fields": spec["fields"], "ruled_remedy": spec["remedy"],
              "ruled_coverage_report": spec["coverage_report"],
              "executed_as": "its own coverage sweep (E-18) over the rows file the ruling names",
              "rows_file": {"path": "Ezek/" + a.rows.replace("\\", "/"), "sha256": sha(rows_p), "rows": len(rows)}}
    mp = rows_p.with_name(rows_p.stem + ".manifest.json")
    report["rows_manifest"] = {"path": "Ezek/" + str(mp.relative_to(EZ)).replace("\\", "/"), "sha256": sha(mp)} if mp.is_file() else None
    ok = True
    if a.cwo == "CWO-EZ-22":
        rc, found = ruled_counts(), hits(rows, arms())
        report["field_scope"] = "content fields only: %s, and every element of %s; identity fields excluded" % (
            ", ".join(CONTENT_STR_FIELDS), ", ".join(CONTENT_LIST_FIELDS))
        report["hit_count"], report["hit_rows"] = len(found), len({h["row"] for h in found})
        report["by_arm"] = dict(Counter(h["arm"] for h in found))
        if a.stage == "v5":
            olds = {}
            for p in pairs():
                if p["row"] in by_id:
                    s = get_field(by_id[p["row"]], p["field"])
                    i = s.find(p["old"])
                    olds.setdefault((p["row"], p["field"]), []).append((p["n"], i, i + len(p["old"]) if i >= 0 else -1))
            for h in found:
                pn = [n for n, i, j in olds.get((h["row"], h["field"]), []) if i >= 0 and h["start"] >= i and h["end"] <= j]
                h["disposition"] = ("CWO-EZ-23 pair %d" % pn[0]) if pn else "FIXUP-3 author item"
            undisposed = sorted({h["row"] for h in found if h["part"] not in WAVE_PARTS and not h["disposition"].startswith("CWO-EZ-23")})
            report["expected"] = rc["v5"]
            report["hits_outside_wave_parts_not_on_a_pair"] = undisposed
            ok = (len(found) == rc["v5"]["hits"] and report["hit_rows"] == rc["v5"]["rows"] and report["by_arm"] == rc["v5"]["by_arm"]
                  and not undisposed)
            report["verdict"] = "DISPOSITIONED" if ok else "RESIDUAL_DIFFERS"
        elif a.stage == "v5cwo23":
            rows_hit = sorted({h["row"] for h in found})
            for h in found:
                h["disposition"] = "FIXUP-3 author item"
            report["expected"] = rc["after_pairs"]
            report["hits_in_pair_parts"] = sorted({h["row"] for h in found if h["part"] in PAIR_PARTS})
            ok = len(found) == rc["after_pairs"]["hits"] and rows_hit == rc["after_pairs"]["row_ids"] and not report["hits_in_pair_parts"]
            report["verdict"] = "RESIDUAL_AS_RULED" if ok else "RESIDUAL_DIFFERS"
        else:
            ok = not found
            report["verdict"] = "COVERED" if ok else "RESIDUAL_DIFFERS"
        report["hits"] = found
    else:
        checks = []
        for p in pairs():
            s = get_field(by_id[p["row"]], p["field"])
            checks.append({"pair": p["n"], "row": p["row"], "field": p["field"], "new_count": s.count(p["new"]), "old_count": s.count(p["old"])})
        bad = [c for c in checks if c["new_count"] != 1 or c["old_count"] != 0]
        report["pair_checks"], report["pairs_verified"], report["pairs_failed"] = checks, len(checks) - len(bad), bad
        ok = not bad
        report["verdict"] = "COVERED" if ok else "RESIDUAL_DIFFERS"
    report["limit"] = "a residual count proves the predicate over the named rows file and nothing beyond it; it judges no content"
    out_dir = EZ / "repair" / OUT_DIRS[a.stage]
    out_dir.mkdir(exist_ok=True)
    out = out_dir / ("%s.json" % a.cwo)
    body = json.dumps(report, ensure_ascii=False, indent=1)
    if out.exists() and out.read_text(encoding="utf-8") != body:
        raise SystemExit("ABORT: %s exists with different content; never replaced" % out)
    out.write_text(body, encoding="utf-8", newline="\n")
    print(json.dumps({"cwo": a.cwo, "stage": a.stage, "rows": report["rows_file"], "verdict": report["verdict"],
                      **({"hit_count": report["hit_count"], "hit_rows": report["hit_rows"], "by_arm": report["by_arm"]} if a.cwo == "CWO-EZ-22"
                         else {"pairs_verified": report["pairs_verified"]}),
                      "report": str(out.relative_to(EZ)).replace("\\", "/")}, ensure_ascii=False, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
