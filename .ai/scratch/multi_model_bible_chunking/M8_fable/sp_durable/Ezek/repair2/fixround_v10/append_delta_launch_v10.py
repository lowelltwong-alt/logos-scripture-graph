#!/usr/bin/env python3
"""Append the launch receipt of one v10 delta re-check lane (the author launch row's shape; agent_id, never parent_agent_id).

The receipts file's whole-file digest is pinned by --expect-before. The row is appended under an exclusive lock with an
atomic replace and a post-write check. It refuses if the attempt already has a row, if the brief is not at --brief-sha,
or if the pin guard is not CLEAR.
usage: append_delta_launch_v10.py --lane a|b --agent-id ID --brief-sha SHA --expect-before SHA --launched-at ISO
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
SP = HERE.parents[2]
REC = HERE / "ezek_fixround_v10_attempt_receipts.jsonl"
SCR = (r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
       r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_fixround_v10")
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731
ap = argparse.ArgumentParser()
ap.add_argument("--lane", required=True, choices=("a", "b"))
ap.add_argument("--agent-id", required=True)
ap.add_argument("--brief-sha", required=True)
ap.add_argument("--expect-before", required=True)
ap.add_argument("--launched-at", required=True)
a = ap.parse_args()
L = a.lane
brief = HERE / ("DELTA_BRIEF_V10_%s.md" % L.upper())
if sha(brief.read_bytes()) != a.brief_sha:
    raise SystemExit("REFUSED: the brief is not at --brief-sha")
g = subprocess.run([sys.executable, "-B", str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek", "--target",
                    "Ezek/repair2/fixround_v10/" + REC.name], cwd=str(SP), capture_output=True, text=True,
                   encoding="utf-8", env=dict(os.environ, PYTHONUTF8="1"))
if json.loads(g.stdout)["verdict"] != "CLEAR":
    raise SystemExit("REFUSED by pin guard: " + g.stdout[-300:])
before = REC.read_bytes()
if sha(before) != a.expect_before:
    raise SystemExit("REFUSED: receipts are at %s, not --expect-before" % sha(before)[:12])
att = "ezek_fixround_v10_delta_lane_%s_a1" % L
if any(json.loads(x).get("attempt_id") == att for x in before.decode("utf-8").splitlines() if x.strip()):
    raise SystemExit("REFUSED: %s already has a row" % att)
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
row = {"schema": "m8_attempt_receipt.v1", "record_kind": "launch", "attempt_id": att, "execution_id": att + "#e1",
       "execution_of": att, "execution_ordinal": 1, "previous_execution_id": None, "retry_of": None, "book": "Ezek",
       "lane": "fixround_v10_delta_" + L,
       "role": ("blind delta re-check lane %s over rows_v10_final (OW-19 floor of two; OW-28; OW-30): lineage v9->v10, "
                "the eight ruled holds as implemented, derived records, item 22, both verdicts. "
                "Checks and reports; applies nothing" % L.upper()),
       "producer": "the v10 hold round (Fable's OW-30 ruling, implemented by the orchestrator's builds)",
       "catcher": "this lane and its blind sibling; Fable at the campaign-end review (OW-28)",
       "agent": "general-purpose subagent", "agent_id": a.agent_id, "parent_agent_id": None, "model": "claude-opus-5-5",
       "model_actual": "PENDING - read from the completion usage block", "effort": "inherited",
       "orders": "inline 4 lines: verify brief sha, read it whole, execute; write only OUT; E-19",
       "brief": "sp_durable/Ezek/repair2/fixround_v10/" + brief.name, "brief_sha256": a.brief_sha,
       "launched_at": a.launched_at, "recorded_at": now, "outcome": "RUNNING",
       "output_dir": SCR + "\\delta_" + L,
       "tokens_unit_note": "at landing record BOTH units: notification (the ceiling unit, OW-28) and spend (usage fields, E-55)"}
after = before + (b"" if not before or before.endswith(b"\n") else b"\n") + (json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8")
lock = REC.with_suffix(REC.suffix + ".lock")
fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
try:
    if REC.read_bytes() != before:
        raise SystemExit("REFUSED: receipts changed under the lock")
    tmp = REC.with_suffix(REC.suffix + ".tmp")
    tmp.write_bytes(after)
    os.replace(tmp, REC)
    if sha(REC.read_bytes()) != sha(after):
        REC.write_bytes(before)
        raise SystemExit("ROLLED BACK: receipt post-write check failed")
finally:
    os.close(fd)
    lock.unlink()
print(json.dumps({"appended": att, "receipts": [sha(before), sha(after)]}))
