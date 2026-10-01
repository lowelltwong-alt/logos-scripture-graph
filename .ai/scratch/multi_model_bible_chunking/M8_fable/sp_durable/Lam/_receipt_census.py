#!/usr/bin/env python3
"""Census every attempt this book actually ran, counted from the ARTIFACTS ON DISK, and flag any without a receipt.

WHY THE COUNT OBJECT MATTERS, which is the whole finding: when I wrote the fourteen missing receipts I built the
list from the transcript map - the launch record - and asked "which mapped attempts lack a receipt?". The third
final check found an attempt that answer could never reach: lam_cwo_corr_03_a1, the third order-correction, which
EDITED THE CORPUS (rows_v6 -> rows_v7, one row) and appears in its own orders file, its deliverable, its apply
report and the parity records, but was never in the launch map. It had no receipt, no manifest entry and no cycle-log
wave entry. My census counted the wrong object, so it returned a confident and incomplete answer.

This tool asks the right question: which attempt ids appear ANYWHERE in this book's artifacts - orders files,
deliverable packets, apply reports, parity records, the cycle log, the transcript manifests, the launch map - and
which of those lack a receipt? An attempt that touched the corpus and left an artifact is an attempt, whether or not
anyone remembered to write it down at launch.

Digits are this tool's COUNTS over files it opened, and it names every file it scanned.
Usage: _receipt_census.py [--json]"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SC = HERE.parent.parent
AID = re.compile(r"\b(?:lam|jer)_[a-z0-9_]*?_?[a-zA-Z0-9]+_a\d\b")
SKIP_PREFIX = ("jer_",)


def ids_in(path):
    try:
        return set(AID.findall(path.read_text(encoding="utf-8-sig", errors="replace")))
    except Exception:
        return set()


def main():
    scanned, seen = [], {}

    def note(p, where):
        for a in ids_in(p):
            if a.startswith(SKIP_PREFIX):
                continue
            seen.setdefault(a, set()).add(where)

    for pat, where in (("spot/orders_*.json", "orders"), ("cwo/orders_*.json", "orders"),
                       ("cwo/corr*/orders_*.json", "orders"), ("author/orders_*.json", "orders"),
                       ("spot/*.jsonl", "deliverable"), ("cwo/*.jsonl", "deliverable"),
                       ("cwo/corr*/*.jsonl", "deliverable"), ("author/*.jsonl", "deliverable"),
                       ("writer/*.jsonl", "deliverable"), ("reviews/*.json", "packet"),
                       ("postcheck/*.json", "packet"), ("final_check/*.json", "packet"),
                       ("_apply_*_report.json", "apply_report"), ("cwo/cwo_parity*.json", "parity"),
                       ("freeze/CYCLE_STATE.md", "cycle_log"), ("transcript_manifest.v*.json", "manifest")):
        for p in sorted(HERE.glob(pat)):
            scanned.append(str(p.relative_to(HERE)).replace("\\", "/"))
            note(p, where)
    lm = SC / "_transcript_map.json"
    if lm.is_file():
        scanned.append("(orchestrator scratch)/_transcript_map.json")
        note(lm, "launch_map")

    have = set()
    for p in sorted(HERE.rglob("*_attempt_receipts.jsonl")):
        scanned.append(str(p.relative_to(HERE)).replace("\\", "/"))
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                a = json.loads(line).get("attempt_id")
                if a:
                    have.add(a)

    missing = sorted(a for a in seen if a not in have)
    orphan = sorted(a for a in have if a not in seen)
    res = {"schema": "m8_receipt_census.v1", "book": "Lam",
           "count_object": "attempt ids appearing in ANY artifact of this book on disk - orders, deliverables, "
                           "packets, apply reports, parity records, the cycle log, the manifests and the launch map "
                           "- NOT the launch map alone",
           "why": "an earlier census counted the launch map and therefore could not see lam_cwo_corr_03_a1, an "
                  "attempt that edited the corpus and left four artifacts but was never mapped at launch",
           "files_scanned": len(scanned), "attempts_found": len(seen), "receipts_found": len(have),
           "attempts_without_a_receipt": missing,
           "receipts_for_attempts_no_artifact_names": orphan,
           "attempt_sources": {a: sorted(v) for a, v in sorted(seen.items())},
           "verdict": "GREEN" if not missing else "RED"}
    sys.stdout.reconfigure(encoding="utf-8")
    if "--json" in sys.argv:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        print(json.dumps({k: v for k, v in res.items() if k != "attempt_sources"}, ensure_ascii=False, indent=1))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
