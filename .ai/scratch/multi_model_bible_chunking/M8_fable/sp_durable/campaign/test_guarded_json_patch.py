#!/usr/bin/env python3
"""Regression test for campaign/_guarded_json_patch.py (E-60). Runs on throwaway files in a temp dir; touches no
campaign file. Exit 0 = all pass.

  1. a plan that addresses one key twice is REFUSED in dry run and in apply, and the file is byte-identical after
  2. a write whose postvalidation goes RED is rolled back to the exact preimage (a tuple value does not survive JSON,
     which is the cheapest way to force the RED path)
  3. a normal add still APPLIES and moves only the addressed key
"""
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location("gjp", Path(__file__).with_name("_guarded_json_patch.py"))
gjp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gjp)
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()                   # noqa: E731
fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        fails.append(name)


with tempfile.TemporaryDirectory() as d:
    t = Path(d) / "store.json"
    t.write_text(json.dumps({"k0": 0}, indent=1) + "\n", encoding="utf-8")
    s0 = sha(t)
    dup = {"target": str(t), "expect_file_sha256": s0,
           "edits": [{"key": "k1", "expect_before": "__ABSENT__", "set": 1},
                     {"key": "k1", "expect_before": "__ABSENT__", "set": 2}]}
    for mode in (False, True):
        out, code = gjp.run(dup, mode)
        check(f"duplicate key refused (apply={mode})", code == 1 and out["status"] == "REFUSED"
              and out.get("duplicate_keys") == ["k1"] and sha(t) == s0)

    red = {"target": str(t), "expect_file_sha256": s0,
           "edits": [{"key": "k2", "expect_before": "__ABSENT__", "set": (1, 2)}]}
    out, code = gjp.run(red, True)
    check("RED write rolled back to the exact preimage", code == 1 and out["status"] == "RED"
          and out.get("rollback") == "restored the preimage" and sha(t) == s0)

    ok = {"target": str(t), "expect_file_sha256": s0,
          "edits": [{"key": "k3", "expect_before": "__ABSENT__", "set": {"a": 1}}]}
    out, code = gjp.run(ok, True)
    after = json.loads(t.read_text(encoding="utf-8"))
    check("normal add applies", code == 0 and out["status"] == "APPLIED" and after == {"k0": 0, "k3": {"a": 1}}
          and "rollback" not in out)

print("ALL PASS" if not fails else f"{len(fails)} FAILED")
sys.exit(1 if fails else 0)
