#!/usr/bin/env python3
"""Tier-0 validator suite runner (m8-mesh-r3), Eccl. Orchestrator-run:
 (a) over draft/frozen rows BEFORE primaries launch;
 (b) over revised rows INSTEAD of a full rev re-review.

Runs, in order: citation_sweep, hebrew normalize (dry-run), web quotes,
refs mirror, mark symmetry, universals, language zones, 7-gram gate.
Hard checks (citation_sweep, hebrew defects, ngram gate) set status RED;
the FLAGS checks feed the orchestrator triage queue.

Usage: run_validator_suite.py rows.jsonl [--reviews f1.json f2.json ...]
Writes <rows>.validator_report.json next to the rows file and prints a summary.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent


def run(script: str, *args: str) -> dict:
    proc = subprocess.run([sys.executable, str(TOOLS / script), *args],
                          capture_output=True, text=True, encoding="utf-8")
    try:
        out = json.loads(proc.stdout)
    except json.JSONDecodeError:
        out = {"status": "ERROR", "stdout": proc.stdout[-2000:], "stderr": proc.stderr[-2000:]}
    out["_exit"] = proc.returncode
    return out


def main() -> int:
    rows = sys.argv[1]
    extra = []
    if "--reviews" in sys.argv:
        extra = sys.argv[sys.argv.index("--reviews") + 1:]
    report = {
        "rows_file": rows,
        "citation_sweep": run("citation_sweep.py", rows),
        "hebrew_normalize_dryrun": run("normalize_hebrew_in_json.py", rows, *extra),
        "web_quotes": run("check_web_quotes.py", rows, *extra),
        "refs_mirror": run("check_refs_mirror.py", rows),
        "mark_symmetry": run("check_marks.py", rows),
        "universals": run("check_universals.py", rows, *extra),
        "language_zones": run("check_language_zones.py", rows, *extra),
        "ngram7": run("ngram7.py", rows),
    }
    hard_red = (report["citation_sweep"].get("status") == "RED"
                or report["ngram7"].get("status") == "RED"
                or report["hebrew_normalize_dryrun"].get("status") == "ERROR"
                or any(r.get("defect_count", 0) if isinstance(r, dict) else 0
                       for r in [report["hebrew_normalize_dryrun"]]))
    flag_total = sum(report[k].get("flag_count", 0)
                     for k in ("web_quotes", "refs_mirror", "mark_symmetry",
                               "universals", "language_zones"))
    report["summary"] = {"hard_status": "RED" if hard_red else "GREEN",
                         "triage_flags": flag_total}
    out_path = Path(rows).with_suffix(Path(rows).suffix + ".validator_report.json")
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"report": str(out_path), **report["summary"],
                      "per_check": {k: report[k].get("status", "?")
                                    for k in report if k not in ("rows_file", "summary")}},
                     indent=1))
    return 1 if hard_red else 0


if __name__ == "__main__":
    raise SystemExit(main())
