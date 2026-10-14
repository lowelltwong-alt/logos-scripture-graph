#!/usr/bin/env python3
"""Greek Tier-0 suite runner, fail closed. Modelled on sp_durable/Dan/tools/run_validator_suite.py (read only).

Members (all HARD): citation_sweep, normalize dry-run, stray_sweep.
  E-68 / Dan D1: a member is DEAD when its stdout is not exactly one JSON object, the object has no status in
       {GREEN, RED, FLAGS}, or its exit code disagrees with its status (GREEN must exit 0, RED must not). A dead
       member is missing evidence: the suite is RED and the member is listed in summary.dead_members.
  E-01: a normalize dry-run with fixed > 0, or a citation_sweep nfd_degraded_count > 0, is HARD.
  E-20: a flag-shaped or missing first argument writes no report.

Usage: run_suite.py rows.jsonl       writes <rows>.validator_report.json and prints the summary
       run_suite.py --selftest       includes adversarial dead members (crash, non-JSON, statusless, exit lie)
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
MEMBERS = [("citation_sweep", TOOLS / "citation_sweep.py", True),
           ("normalize_dryrun", TOOLS / "normalize_greek_in_json.py", True),
           ("stray_sweep", TOOLS / "stray_sweep.py", False)]          # (name, script, takes rows arg)
STATUSES = {"GREEN", "RED", "FLAGS"}


def run(script: Path, *args: str) -> dict:
    try:
        p = subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, encoding="utf-8",
                           timeout=600, env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"status": "ERROR", "dead_reason": f"not run: {e}"[:300], "_exit": None}
    lines = [l for l in p.stdout.splitlines() if l.strip()]
    try:
        out = json.loads(p.stdout)
        if not isinstance(out, dict):
            raise ValueError
    except ValueError:
        return {"status": "ERROR", "dead_reason": f"stdout is not one JSON object ({len(lines)} lines)",
                "stderr_tail": p.stderr[-400:], "_exit": p.returncode}
    out["_exit"] = p.returncode
    st = out.get("status")
    if st not in STATUSES:
        out["dead_reason"] = f"status {st!r} not in {sorted(STATUSES)}"
        out["status"] = "ERROR"
    elif (st == "GREEN") != (p.returncode == 0):
        out["dead_reason"] = f"exit {p.returncode} contradicts status {st}"
        out["status"] = "ERROR"
    return out


def suite(rows: str, members=MEMBERS) -> dict:
    report = {name: run(script, rows) if takes_rows else run(script) for name, script, takes_rows in members}
    dead = sorted(k for k, v in report.items() if v.get("status") == "ERROR")
    e01 = bool(report.get("normalize_dryrun", {}).get("fixed", 0)) or \
        bool(report.get("citation_sweep", {}).get("nfd_degraded_count", 0))
    red = sorted(k for k, v in report.items() if v.get("status") in ("RED", "FLAGS", "ERROR"))
    report["summary"] = {"hard_status": "RED" if (red or dead or e01) else "GREEN", "red_members": red,
                         "dead_members": dead, "nfd_hard_e01": e01, "members_run": len(members)}
    return report


def selftest() -> int:
    fails = []
    fx = TOOLS.parent / "fixture"
    good = suite(str(fx / "rows.good.jsonl"))["summary"]
    if good["hard_status"] != "GREEN":
        fails.append(f"good fixture: {good}")
    bad = suite(str(fx / "rows.bad.jsonl"))["summary"]
    if bad["hard_status"] != "RED" or bad["dead_members"] or not bad["nfd_hard_e01"] or \
            set(bad["red_members"]) != {"citation_sweep", "normalize_dryrun"}:
        fails.append(f"bad fixture: {bad}")
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        dead_src = {"crash": "raise SystemExit(__import__('json').loads('{'))",
                    "nonjson": "print('all good')",
                    "twojson": "print('{\"status\": \"GREEN\"}'); print('{\"status\": \"GREEN\"}')",
                    "statusless": "print('{\"ok\": 3}')",
                    "exitlie": "print('{\"status\": \"GREEN\"}'); raise SystemExit(1)",
                    "missing": None}
        members = [m for m in MEMBERS]
        for name, src in dead_src.items():
            p = t / f"{name}.py"
            if src is not None:
                p.write_text(src, encoding="utf-8")
            members.append((name, p, False))
        s = suite(str(fx / "rows.good.jsonl"), members)["summary"]
        if s["hard_status"] != "RED" or s["dead_members"] != sorted(dead_src):
            fails.append(f"dead members not all HARD: {s}")
        only_dead = suite(str(fx / "rows.good.jsonl"), MEMBERS[:1] + [("nonjson", t / "nonjson.py", False)])
        if only_dead["summary"]["hard_status"] != "RED":
            fails.append("a single dead member beside a GREEN member must make the suite RED")
    print(json.dumps({"status": "GREEN" if not fails else "RED", "selftest": "run_suite", "fails": fails}))
    return 0 if not fails else 1


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        return selftest()
    if len(sys.argv) != 2 or sys.argv[1].startswith("-"):
        print(json.dumps({"status": "RED", "usage": "run_suite.py rows.jsonl | --selftest",
                          "error": "first argument must be the rows file; no report is written"}))
        return 2
    rows = sys.argv[1]
    report = {"rows_file": Path(rows).name, **suite(rows)}
    out = Path(rows).with_suffix(Path(rows).suffix + ".validator_report.json")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    s = report["summary"]
    print(json.dumps({"status": s["hard_status"], "report": out.name, **s,
                      "per_member": {k: v.get("status") for k, v in report.items() if isinstance(v, dict)
                                     and k != "summary"}}))
    return 0 if s["hard_status"] == "GREEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
