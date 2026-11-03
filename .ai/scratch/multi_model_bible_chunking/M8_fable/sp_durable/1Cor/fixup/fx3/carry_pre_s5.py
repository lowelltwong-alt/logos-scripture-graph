"""One-shot carrier update before the S5 brief is built (the ledger is a pinned input, E-69): appends E-78 and repoints
the resume cursor. The learning entry and CYCLE_STATE note go through carry_append.py.
usage: carry_pre_s5.py --ledger-pin SHA --resume-pin SHA"""
import argparse, hashlib, os
from pathlib import Path
HERE = Path(__file__).resolve().parent
SP = HERE.parents[2]
M = SP.parent
ap = argparse.ArgumentParser()
ap.add_argument("--ledger-pin", required=True)
ap.add_argument("--resume-pin", required=True)
a = ap.parse_args()
sha = lambda b: hashlib.sha256(b).hexdigest()
led, res = M / "ERROR_PATTERN_LEDGER.v1.md", M / "RESUME_PROMPT_CURRENT.md"
dl, dr = led.read_bytes(), res.read_bytes()
if sha(dl) != a.ledger_pin or sha(dr) != a.resume_pin:
    raise SystemExit("REFUSED: pin")
if b"## E-78 " in dl:
    raise SystemExit("REFUSED: E-78 present")
entry = (HERE / "e78_entry.md").read_bytes()
OLD = b"phase = 1COR_FIXUP3_PREPARING"
NEW = b"phase = 1COR_S5_PREPARING"
if dr.count(OLD) != 1:
    raise SystemExit("REFUSED: cursor")
start = dr.index(b"cursor: phase = 1COR_FIXUP3_PREPARING")
end = dr.index(b"\n", start)
line = ("cursor: phase = 1COR_S5_PREPARING (read SP/1Cor/freeze/CYCLE_STATE.md last section first; receipts lines are 1-BASED there; reconcile line 114+ of 1Cor/review/1cor_review_attempt_receipts.jsonl). "
        "NEXT AUTHORIZED JOB: FIXUP-3 is applied (1Cor/fixup/draft_rows_fixup3_applied.jsonl, built by land_fixup3.py apply). S5 is next: 1Cor/review/build_s5_launch.py, a fresh agent checking GATE-E4's thirteen s2_conditions; "
        "then the close port from Dan/close. Any commit, push or ref-moving fetch needs a fresh exact owner checkpoint first.").encode("utf-8")
def put(p, b):
    t = p.with_suffix(p.suffix + ".tmp_pre_s5")
    t.write_bytes(b)
    os.replace(t, p)
put(led, dl + (b"" if dl.endswith(b"\n") else b"\n") + entry)
put(res, dr[:start] + line + dr[end:])
print(sha(led.read_bytes()), sha(res.read_bytes()))
