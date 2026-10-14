#!/usr/bin/env python3
"""Stray sweep of greek_substrate/ (E-21 sense: an expected-manifest allowlist sweep). HARD member of run_suite.

  stray             a file matching no ALLOW pattern (__pycache__ excluded)
  swete_misplaced   a Swete file (tlg0527* or First1KGreek license.md copy) outside swete_lxx_REFERENCE_ONLY/
                    (owner isolation terms 2026-09-29)
  staging_drift     a staged witness file missing or re-hashing differently from STAGING_RECEIPT.v1.json

Usage: stray_sweep.py [DIR] | --selftest       (DIR defaults to greek_substrate/; receipt check only there)
"""
from __future__ import annotations

import fnmatch
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import greek_lib as g

ALLOW = [
    "README.md", "STAGING_RECEIPT.v1.json", "_build_receipt.py", "_stage_and_verify.py",
    "byzantine_rp_PRIMARY/*", "sblgnt_SECONDARY/*", "sblgnt_apparatus/*", "swete_lxx_REFERENCE_ONLY/*",
    "tools/greek_lib.py", "tools/build_crosswalk.py", "tools/collate.py", "tools/word_index.py",
    "tools/normalize_greek_in_json.py", "tools/citation_sweep.py", "tools/stray_sweep.py", "tools/run_suite.py",
    "fixture/_make_fixture.py", "fixture/rows.good.jsonl", "fixture/rows.bad.jsonl",
    "fixture/rows.*.jsonl.validator_report.json", "derived/crosswalk.v1.json",
]
SWETE_DIR = "swete_lxx_REFERENCE_ONLY/"


def sweep(root: Path, check_receipt: bool) -> dict:
    problems = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or "__pycache__" in p.parts:
            continue
        rel = p.relative_to(root).as_posix()
        if not any(fnmatch.fnmatchcase(rel, a) and ("/" in a or "/" not in rel) for a in ALLOW):
            problems.append({"kind": "stray", "path": rel})
        if p.name.startswith("tlg0527") and not rel.startswith(SWETE_DIR):
            problems.append({"kind": "swete_misplaced", "path": rel})
    if check_receipt:
        problems += [{"kind": "staging_drift", "detail": d} for d in g.verify_staged()]
    return {"status": "GREEN" if not problems else "RED", "root": root.name, "problem_count": len(problems),
            "problems": problems[:30]}


def selftest() -> int:
    fails = []
    real = sweep(g.SUB, True)
    if real["status"] != "GREEN":
        fails.append(f"live tree not clean: {real['problems'][:5]}")
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        (t / "tools").mkdir()
        (t / "tools" / "greek_lib.py").write_text("x")
        (t / "tools" / "scratch_notes.txt").write_text("x")
        (t / "derived").mkdir()
        (t / "derived" / "tlg0527.tlg053.1st1K-grc1.xml").write_text("x")
        (t / "tools" / "__pycache__").mkdir()
        (t / "tools" / "__pycache__" / "a.pyc").write_text("x")
        r = sweep(t, False)
        kinds = sorted((p["kind"], p["path"]) for p in r["problems"])
        want = [("stray", "derived/tlg0527.tlg053.1st1K-grc1.xml"), ("stray", "tools/scratch_notes.txt"),
                ("swete_misplaced", "derived/tlg0527.tlg053.1st1K-grc1.xml")]
        if kinds != want:
            fails.append(f"adversarial tree: got {kinds}")
    print(json.dumps({"status": "GREEN" if not fails else "RED", "selftest": "stray_sweep", "fails": fails}))
    return 0 if not fails else 1


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        return selftest()
    if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1].startswith("-")):
        print(json.dumps({"status": "RED", "usage": "stray_sweep.py [DIR] | --selftest"}))
        return 2
    root = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else g.SUB
    r = sweep(root, root == g.SUB)
    print(json.dumps(r, ensure_ascii=False))
    return 0 if r["status"] == "GREEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
