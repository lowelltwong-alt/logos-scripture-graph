#!/usr/bin/env python3
"""Builds the post-FIXUP-2 CWO-06/07 coverage report and the FIXUP-3 gate rows, as the FIXUP-2 sequence did (lines 29, 30).
The report takes its lists from the installed sweep run on the FIXUP-2 applied rows and its hand classes from the E4 rulings'
coverage statement, carried here as data; every count is asserted against GATE-E4's. Writes OUTDIR/coverage.json and
OUTDIR/gate.json, and the report beside the other reports. Refuses when any lane is in flight.
usage: make_fx3_gate.py OUTDIR
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BK = HERE.parents[1]
SP = BK.parent
R = BK / "review"
out = Path(sys.argv[1])
os.makedirs(out, exist_ok=True)
SWEEP = R / "cwo_sweep_1cor.py"
ROWS = BK / "fixup/draft_rows_fixup2_applied.jsonl"
RUL = R / "1cor_controlling_agent_rulings_E4.v1.json"
REPORT = R / "cwo_1cor_post_fixup2_cwo0607_report.v1.json"
env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rel(p):
    return "sp_durable/" + Path(p).relative_to(SP).as_posix()


def fref(p):
    return {"path": rel(p), "sha256": sha(p)}


work = out / "sweep.json"
subprocess.run([sys.executable, "-B", str(SWEEP), str(ROWS), "--out", str(work)], check=True, env=env,
               capture_output=True, cwd=str(out))
s = json.loads(work.read_text(encoding="utf-8"))
HAND_TRUE = {("W2-003", "5:12"), ("W2-006", "7:1"), ("W2-009", "7:12"), ("W2-013", "7:35"), ("W2-014", "7:39"), ("W3-001", "9:1"),
             ("W3-002", "9:15"), ("W3-002", "9:3"), ("W3-003", "9:18"), ("W3-004", "9:23"), ("W3-005", "10:11"), ("W3-006", "10:23"),
             ("W3-008", "11:2"), ("W4-001", "11:17"), ("W5-009", "14:6"), ("W5-010", "14:13")}
HAND_FP = {("W2-008", "7:9"): "spelling", ("W6-004", "15:35"): "elision"}
hits = s["CWO06"]["list"]
keys = {(h["row"], ":".join(h["verse"].split(".")[1:])): h for h in hits}
if set(keys) != HAND_TRUE | set(HAND_FP) or len(hits) != 18:
    sys.exit("REFUSED: CWO06 hits do not equal the E4 hand classes: %s" % sorted(set(keys) ^ (HAND_TRUE | set(HAND_FP))))
assert (s["CWO06"]["hits"], s["CWO06"]["rows"]) == (18, 17) and (s["CWO07"]["unlisted"], s["CWO07"]["rows"]) == (63, 25)
rep = {"schema": "m8_cwo_coverage_report.v1", "book": "1Cor", "rows_file": fref(ROWS), "sweep_script": fref(SWEEP), "rulings_file": fref(RUL),
       "CWO05": s["CWO05"], "CWO06": {**s["CWO06"], "list": [dict(h, hand_class="false_positive:" + HAND_FP[k] if k in HAND_FP else "true")
                                                            for k, h in keys.items()]},
       "CWO07": s["CWO07"], "hand_classes": {"CWO06": {"true": 16, "false_positive": 2}},
       "note": "Hand classes are the E4 author's, carried from the rulings' coverage statement; rows with known limits of the predicate are handled by their named row orders."}
REPORT.write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
cap = subprocess.run([sys.executable, "-B", str(R / "tools/lane_cap.py"), "--book-dir", str(BK)], capture_output=True, text=True,
                     encoding="utf-8", env=env)
if cap.returncode != 0 or json.loads(cap.stdout).get("in_flight") not in ([], 0):
    sys.exit("REFUSED: lane_cap rc %d %s" % (cap.returncode, cap.stdout[:300]))
base = {"schema": "m8_attempt_receipt.v1", "book": "1Cor", "parent_agent_id": "orchestrator"}
(out / "coverage.json").write_text(json.dumps(
    {**base, "record_kind": "cwo_coverage_report", "ordered_by": "cor_controlling_rulings_r4_a1#e1 CWO-1COR-06, CWO-1COR-07 and GATE-E4",
     "report": fref(REPORT), "sweep_script": fref(SWEEP), "rows_file": fref(ROWS),
     "summary": {"cwo06_hits": 18, "rows": 17, "true_ordered": 16, "false_positive": 2, "cwo07_unlisted": 63, "cwo07_rows": 25,
                 "A": s["A"]["hits"], "B": s["B"]["hits"], "cwo02_fail": s["CWO02"]["fail"]},
     "outcome": "CWO-1COR-06 and -07 reported on the FIXUP-2 applied rows; every CWO-1COR-06 hit carries its E4 hand class",
     "effect": "the true hits and the unlisted verses are named per part in the FIXUP-3 briefs"}, ensure_ascii=False), encoding="utf-8", newline="\n")
(out / "gate.json").write_text(json.dumps(
    {**base, "record_kind": "gate_flip", "ordered_by": "cor_controlling_rulings_r4_a1#e1 GATE-E4 tool_fixes_before_fixup", "gate": "fixup_may_launch",
     "from": "False", "to": "True",
     "basis": ["tool_fix_install TF-4, line 98 of this file", "tool_fix_install TF-5, line 99 of this file", "cwo_coverage_report, the row above this one",
               {"rulings_file": fref(RUL), "rows_file": fref(ROWS),
                "lane_cap": {"tool": rel(R / "tools/lane_cap.py"), "sha256": sha(R / "tools/lane_cap.py"), "exit_code": cap.returncode, "output": cap.stdout.strip()[:400]}}],
     "scope": "FIXUP-3 on W1..W6 (GATE-E4 fixup_parts), at most three in flight; primaries_may_launch stays false; S5 runs only after every part has landed and the rows are applied"},
    ensure_ascii=False), encoding="utf-8", newline="\n")
print("report", sha(REPORT), "cap", cap.stdout.strip()[:200])
