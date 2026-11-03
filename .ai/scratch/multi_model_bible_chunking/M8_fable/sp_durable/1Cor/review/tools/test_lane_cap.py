"""Regression test for lane_cap.in_flight and its wiring into prelaunch_gate.py. Replays both measured breaches
(2026-10-20 FIXUP-2: W1 and W4 launched with only W5 landed; 2026-10-15 Phase 0: C2 launched with T1-e2, T3-e2 and C1 in
flight) and requires the cap to refuse the fourth lane. Fixture dirs under ./lane_cap_fixtures only.
usage: test_lane_cap.py --result FILE"""
import ast
import json
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from lane_cap import CAP, in_flight  # noqa: E402

FX = HERE / "lane_cap_fixtures"
L = lambda x: {"record_kind": "launch", "execution_id": x}  # noqa: E731
C = lambda x: {"record_kind": "completion", "amends_execution_id": x}  # noqa: E731
C2 = lambda x: {"record_kind": "completion", "execution_id": x}  # noqa: E731


def book(name, files):
    d = FX / name
    d.mkdir(parents=True)
    for rel, rows in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8", newline="\n")
    return d


def may_launch(d):
    return len(in_flight(d)) < CAP


if FX.exists():
    shutil.rmtree(FX)
res = {}
fx2 = [L("W5#e1"), L("W6#e1"), L("W3#e1"), C("W5#e1")]
res["fx2_first_extra_allowed"] = may_launch(book("a", {"review/x_attempt_receipts.jsonl": fx2}))
res["fx2_second_extra_refused"] = not may_launch(book("b", {"review/x_attempt_receipts.jsonl": fx2 + [L("W1#e1")]}))
p0 = [L("T1#e1"), L("T3#e1"), C("T1#e1"), C("T3#e1"), L("T1#e2"), L("T3#e2"), L("C1#e1")]
res["phase0_c2_refused"] = not may_launch(book("c", {"p0_attempt_receipts.jsonl": p0}))
res["across_files_counted"] = not may_launch(book("d", {"p_attempt_receipts.jsonl": [L("a#e1"), L("b#e1")],
                                                         "review/r_attempt_receipts.jsonl": [L("c#e1")]}))
res["execution_id_close_counts"] = may_launch(book("e", {"r_attempt_receipts.jsonl": [L("a#e1"), L("b#e1"), L("c#e1"),
                                                                                         C2("c#e1")]}))
res["pre_copies_ignored"] = may_launch(book("f", {"r_attempt_receipts.jsonl": [L("a#e1")],
                                                   "r_attempt_receipts.jsonl.pre_0123456789ab": [L("b#e1"), L("c#e1")]}))
res["retry_open_after_prior_close"] = in_flight(book("g", {"r_attempt_receipts.jsonl": [L("a#e1"), C("a#e1"),
                                                                                         L("a#e2")]})) == ["a#e2"]
tree = ast.parse((HERE / "prelaunch_gate.py").read_text(encoding="utf-8"))
src = (HERE / "prelaunch_gate.py").read_text(encoding="utf-8")
res["gate_checks_cap_before_reading_message"] = (
    any(isinstance(n, ast.ImportFrom) and n.module == "lane_cap" for n in ast.walk(tree))
    and 0 < src.index("in_flight(SP / A.book)") < src.index("msg = Path(A.message).read_bytes()"))
shutil.rmtree(FX)
out = {"test": "test_lane_cap", "cases": res, "passed": sum(res.values()), "of": len(res),
       "verdict": "PASS" if all(res.values()) else "FAIL"}
Path(sys.argv[sys.argv.index("--result") + 1]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8",
                                                          newline="\n")
print(json.dumps({k: out[k] for k in ("passed", "of", "verdict")}), [k for k, v in res.items() if not v])
