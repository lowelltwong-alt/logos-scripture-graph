#!/usr/bin/env python3
"""One-shot carrier update before the FIXUP-3 briefs are built (the ledger is a pinned input, E-69): appends E-77, the
CYCLE_STATE section and the learning-log entry, and moves the resume cursor. Each write is byte-exact and refuses unless
the file is at its --pin value or the anchor occurs exactly once.
usage: carry_pre_fixup3.py --ledger-pin SHA --state-pin SHA --log-pin SHA --resume-pin SHA --phase PHASE
"""
import argparse
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SP = HERE.parents[2]
M = SP.parent
ap = argparse.ArgumentParser()
for k in ("ledger-pin", "state-pin", "log-pin", "resume-pin", "phase"):
    ap.add_argument("--" + k, required=True)
a = ap.parse_args()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def put(p, b):
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_bytes(b)
    os.replace(tmp, p)
    print(p.name, sha(b))


files = {"ledger": M / "ERROR_PATTERN_LEDGER.v1.md", "state": SP / "1Cor/freeze/CYCLE_STATE.md",
         "log": M / "orchestration_learning_log.v1.jsonl", "resume": M / "RESUME_PROMPT_CURRENT.md"}
pins = {"ledger": a.ledger_pin, "state": a.state_pin, "log": a.log_pin, "resume": a.resume_pin}
data = {k: p.read_bytes() for k, p in files.items()}
for k in files:
    if sha(data[k]) != pins[k]:
        raise SystemExit("REFUSED: %s is at %s" % (k, sha(data[k])[:12]))
    if b"\r" in data[k]:
        raise SystemExit("REFUSED: %s carries CR bytes" % k)
entry = (HERE / "e77_entry.md").read_bytes()
state = """
## 2026-11-01: rulings landed, tool fixes in, FIXUP-3 next

- CTL_E4 landed and installed: receipts lines 96, 97. Rulings 1cor_controlling_agent_rulings_E4.v1.json, sha 33ac5724, 61 rulings, CWO-1COR-06 and -07, GATE-E4. It stopped once on the session limit and was resumed as the same execution; the landing row says so.
- Pin guard's rule narrowed: a not-yet-written file in an existing SP folder is allowed; selftest 29 GREEN. The earlier line here saying a target naming no file is refused is superseded (E-77).
- TF-4 and TF-5 installed: receipts lines 98, 99. Sweep now reports CWO05, CWO06, CWO07. On draft_rows_fixup2_applied.jsonl: A 0, B 5, CWO02 0, CWO04 48, CWO05 11 in 10 rows, CWO06 18 in 17 rows, CWO07 63 in 25 rows.
- The next check after FIXUP-3 is S5, not S4: GATE-E4's thirteen s2_conditions are what S5 checks. Tools for FIXUP-3 live in fixup/fx3 and are durable (E-76).
- Baseline on the FIXUP-2 applied rows, rerun 2026-11-01: suite rc 0, ngram7 --gate 10 GREEN, tiling GREEN.
- Commit or push still needs a fresh exact owner checkpoint: any ref move makes the validators fail by design. Owner decisions 2 and 3 are unanswered.
""".lstrip("\n").encode("utf-8")
log = {"schema": "m8_orchestration_learning.v1", "date": "2026-11-01", "book": "1Cor", "supersedes": None, "id": "L-0092",
       "stage": "controlling_round_4", "element": "tool_fixes",
       "observation": "TF-4 and TF-5 went in as added sections copied from the reference bytes and compared with the reference on a recorded baseline. That comparison, not the plants, caught the only defect, a pattern that matched nothing. The round's other real find was the pin guard clearing a target it could not locate; the first fix to it broke a caller.",
       "recommendation": "Build a sweep install by copying from the reference, and require a baseline count that would fail at 0 hits. Treat no-match in a guard as its own outcome, and run every caller of a guard after changing it.",
       "verdict": "worked", "metric": {"tf4_hits": 11, "tf5_hits": 18, "tf5_unlisted": 63, "tf5_plants": 10, "tf5_mutants_red": 4},
       "evidence_refs": ["sp_durable/1Cor/review/1cor_review_attempt_receipts.jsonl lines 96-99", "ERROR_PATTERN_LEDGER.v1.md E-77"]}
resume = data["resume"].decode("utf-8")
old_tok = "1COR_CTL_E4_RUNNING"
if resume.count(old_tok) != 2:
    raise SystemExit("REFUSED: cursor token count %d" % resume.count(old_tok))
lines = resume.split("\n")
idx = [i for i, x in enumerate(lines) if x.startswith("cursor: phase = ")]
if len(idx) != 1:
    raise SystemExit("REFUSED: cursor line count %d" % len(idx))
lines[idx[0]] = ("cursor: phase = %s (read SP/1Cor/freeze/CYCLE_STATE.md last section first; receipts lines are 1-BASED there; "
                 "reconcile line 100+ of 1Cor/review/1cor_review_attempt_receipts.jsonl). NEXT AUTHORIZED JOB: GATE-E4 is the controlling "
                 "order: FIXUP-3 on W1..W6 at most three in flight, tools in 1Cor/fixup/fx3 (build_fixup3.py, land_fixup3.py, apply_fixup3.py); "
                 "then S5, a fresh agent on the applied rows, checking GATE-E4's thirteen s2_conditions; then the close port from Dan/close. "
                 "Any commit, push or ref-moving fetch needs a fresh exact owner checkpoint first." % a.phase)
resume = "\n".join(lines).replace(old_tok, a.phase)
put(files["ledger"], data["ledger"] + (b"" if data["ledger"].endswith(b"\n") else b"\n") + entry)
put(files["state"], data["state"] + (b"" if data["state"].endswith(b"\n") else b"\n") + b"\n" + state)
put(files["log"], data["log"] + (b"" if data["log"].endswith(b"\n") else b"\n") + (json.dumps(log, ensure_ascii=False) + "\n").encode("utf-8"))
put(files["resume"], resume.encode("utf-8"))
