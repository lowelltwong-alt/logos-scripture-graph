#!/usr/bin/env python3
"""Run the pinned validator suite on the LIVE rows and diff it ITEM BY ITEM against a baseline report.

Used after every REPAIR-2 apply. The live rows are copied byte-for-byte to a work directory OUTSIDE the corpus
(the suite writes its report beside the rows file it reads), digest-checked, and judged with UTF-8 mode on for the whole
process tree (the suite decodes members' output as UTF-8; on Windows a piped child writes the ANSI codepage otherwise).

Every flag list is compared as a multiset of canonical items with the run's own file name stripped (a count comparison
can hide a lane that clears one flag and adds another). A comparison over zero flag lists refuses (E-36).

usage: python suite_delta.py --baseline-report <path> --work <dir> [--label <name>] [--out <json>]
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
LIVE = EZ / "repair" / "rows_v7_cwo24.jsonl"
SUITE = EZ / "tools" / "run_validator_suite.py"
HARD = ("citation_sweep", "hebrew_normalize_dryrun", "language_zones", "ngram7", "cap_sweep", "refs_mirror")
sha = lambda b: hashlib.sha256(b).hexdigest()                                  # noqa: E731


def strip_file(x):
    if isinstance(x, dict):
        return {k: strip_file(v) for k, v in x.items() if k not in ("file", "rows_file")}
    if isinstance(x, list):
        return [strip_file(v) for v in x]
    return x


def members(rep):
    out = {}
    for name, m in rep.items():
        if name == "summary" or not isinstance(m, dict):
            continue
        sc, ls = {}, {}
        for k, v in m.items():
            if k in ("_exit", "rows_file", "file", "stdout", "stderr"):
                continue
            if isinstance(v, list):
                ls[k] = Counter(json.dumps(strip_file(i), ensure_ascii=False, sort_keys=True) for i in v)
            else:
                sc[k] = json.dumps(v, ensure_ascii=False, sort_keys=True)
        out[name] = (sc, ls)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline-report", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--label", default="live")
    ap.add_argument("--out")
    a = ap.parse_args()
    work = Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    b = LIVE.read_bytes()
    rows = work / ("rows_%s.jsonl" % a.label)
    rows.write_bytes(b)
    if sha(rows.read_bytes()) != sha(b):
        raise SystemExit("REFUSED: the work copy does not match the live rows")
    proc = subprocess.run([sys.executable, "-B", str(SUITE), str(rows)], cwd=str(SUITE.parent), capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          env=dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8"))
    rep_p = Path(str(rows) + ".validator_report.json")
    if not rep_p.exists():
        raise SystemExit("the suite wrote no report: %s" % proc.stderr[-600:])
    rep = json.loads(rep_p.read_text(encoding="utf-8"))
    base = json.loads(Path(a.baseline_report).read_text(encoding="utf-8"))
    bm, cm = members(base), members(rep)
    delta, lists = {}, 0
    for name in sorted(set(bm) | set(cm)):
        bs, bl = bm.get(name, ({}, {}))
        cs, cl = cm.get(name, ({}, {}))
        d = {}
        for k in sorted(set(bs) | set(cs)):
            if bs.get(k) != cs.get(k):
                d.setdefault("scalars", {})[k] = {"baseline": (bs.get(k) or "<absent>")[:300],
                                                  "now": (cs.get(k) or "<absent>")[:300]}
        for k in sorted(set(bl) | set(cl)):
            lists += 1
            added = list((cl.get(k, Counter()) - bl.get(k, Counter())).elements())
            removed = list((bl.get(k, Counter()) - cl.get(k, Counter())).elements())
            if added or removed:
                d.setdefault("lists", {})[k] = {"added_n": len(added), "removed_n": len(removed),
                                                "added": [json.loads(x) for x in added][:30],
                                                "removed": [json.loads(x) for x in removed][:30]}
        if d:
            delta[name] = d
    if lists == 0:
        raise SystemExit("REFUSED: zero flag lists compared (E-36)")
    # ONLY FLAG LISTS COUNT. My first version counted any list that gained items, so refs_mirror's informational
    # far_side_citations_detail (not a flag) was reported as a hard regression while the member stayed GREEN.
    FLAG_LISTS = {"problems", "flags", "defects", "failures", "offending_7grams", "worklist_citations",
                  "orphan_ref_warn_rows", "prose_pair_problems"}
    regressions = [n for n in HARD if n in delta and any(v["added_n"] for k, v in delta[n].get("lists", {}).items()
                                                         if k in FLAG_LISTS)]
    status = {n: json.loads(cm[n][0].get("status", "null")) for n in cm if "status" in cm[n][0]}
    out = {"rows_sha256": sha(b), "summary_now": rep.get("summary"), "summary_baseline": base.get("summary"),
           "member_status_now": status, "flag_lists_compared": lists, "members_that_moved": delta,
           "hard_members_with_ADDED_flags": regressions,
           "verdict": ("NO HARD MEMBER GAINED A FLAG" if not regressions else
                       "HARD MEMBERS GAINED FLAGS: %s - read each before the next step" % ", ".join(regressions))}
    if a.out:
        Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    brief = {"summary_now": out["summary_now"], "summary_baseline": out["summary_baseline"],
             "member_status_now": status, "verdict": out["verdict"],
             "moved": {n: {"scalars": list((d.get("scalars") or {}).keys()),
                           "lists": {k: "+%d -%d" % (v["added_n"], v["removed_n"]) for k, v in (d.get("lists") or {}).items()}}
                       for n, d in delta.items()}}
    print(json.dumps(brief, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
