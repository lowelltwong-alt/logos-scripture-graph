#!/usr/bin/env python3
"""Re-point close_check_mirror.py's atlas and suite plans at rows_v9_final.jsonl (v9 fix round, 2026-09-23).

check_atlas_rows.py now reads EZ/rows_v9_final.jsonl, so the atlas mirror must carry that file instead of
repair/rows_v7_cwo24.jsonl; the suite plan ran over rows_v8_final. The tool is saved as .pre_<sha12>, edited by exact
strings (each exactly once) plus a docstring amendment, then both plans are run into a scratch --dest and must return
bytes equal to the shipped record. Any failure restores the tool.
usage: patch_mirror_v9.py --dest <scratch dir outside M8>
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
EZ = HERE.parents[1]
SP = EZ.parent
T = HERE.parent / "close_check_mirror.py"
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731
EDITS = [
    ('+ [(EZ / "repair" / "rows_v7_cwo24.jsonl", "M8/sp_durable/Ezek/repair/rows_v7_cwo24.jsonl"),',
     '+ [(EZ / "rows_v9_final.jsonl", "M8/sp_durable/Ezek/rows_v9_final.jsonl"),'),
    ('"suite": ([(EZ / "rows_v8_final.jsonl", "suite/rows_v8_final.jsonl")],\n'
     '              [str(EZ / "tools" / "run_validator_suite.py"), "suite/rows_v8_final.jsonl"],\n'
     '              "suite/rows_v8_final.jsonl.validator_report.json", EZ / "rows_v8_final.jsonl.validator_report.json"),',
     '"suite": ([(EZ / "rows_v9_final.jsonl", "suite/rows_v9_final.jsonl")],\n'
     '              [str(EZ / "tools" / "run_validator_suite.py"), "suite/rows_v9_final.jsonl"],\n'
     '              "suite/rows_v9_final.jsonl.validator_report.json", EZ / "rows_v9_final.jsonl.validator_report.json"),'),
    ("Prints one JSON object:",
     "AMENDED 2026-09-23 (v9 fix round): the atlas and suite plans now carry rows_v9_final.jsonl, because the atlas\n"
     "checker reads it and it is the corpus the close tool pins. The earlier tool is kept as .pre_<sha12>.\n"
     "Prints one JSON object:"),
]
ap = argparse.ArgumentParser()
ap.add_argument("--dest", required=True)
a = ap.parse_args()
dest = Path(a.dest).resolve()
if SP.parent in dest.parents or dest == SP.parent:
    raise SystemExit("REFUSED: --dest is inside M8")
env = dict(os.environ, PYTHONUTF8="1")
g = subprocess.run([sys.executable, "-B", str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek",
                    "--target", "Ezek/repair2/close_check_mirror.py"], cwd=str(SP), capture_output=True, text=True,
                   encoding="utf-8", env=env)
if json.loads(g.stdout)["verdict"] != "CLEAR":
    raise SystemExit("REFUSED by pin guard: " + g.stdout[-300:])
before = T.read_bytes()
src = before.decode("utf-8")
for old, new in EDITS:
    if src.count(old) != 1:
        raise SystemExit("REFUSED: an anchor occurs %d times" % src.count(old))
    src = src.replace(old, new)
keep = T.with_name(T.name + ".pre_" + sha(before)[:12])
if keep.exists() and keep.read_bytes() != before:
    raise SystemExit("REFUSED: %s exists with different bytes" % keep.name)
keep.write_bytes(before)
T.write_bytes(src.encode("utf-8"))
res = {}
for plan in ("atlas", "suite"):
    r = subprocess.run([sys.executable, "-B", str(T), "--dest", str(dest / plan), "--check", plan], capture_output=True,
                       text=True, encoding="utf-8", env=env)
    try:
        out = json.loads(r.stdout)
    except ValueError:
        out = {"raw": (r.stdout + r.stderr)[-300:]}
    res[plan] = {k: out.get(k) for k in ("exit", "bytes_equal_to_shipped", "differs_from_shipped", "stdout_tail",
                                         "stderr_tail", "raw") if k in out}
    # the suite report records its own rows_file path, which is the mirror's path; that key alone may differ
    diff = out.get("differs_from_shipped") or {}
    ok = out.get("bytes_equal_to_shipped") or (plan == "suite" and set(diff.get("top_level", ["?"])) <= {"rows_file"}
                                               and out.get("produced_sha256"))
    if r.returncode or out.get("exit") or not ok:
        T.write_bytes(before)
        raise SystemExit("ROLLED BACK: %s plan did not reproduce the shipped record: %s" % (plan, json.dumps(res[plan])[:600]))
print(json.dumps({"tool": [sha(before), sha(T.read_bytes())], "kept": keep.name, "plans": res}, indent=1))
