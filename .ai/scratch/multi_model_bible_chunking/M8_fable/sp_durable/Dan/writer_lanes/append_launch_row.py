#!/usr/bin/env python3
"""Append the launch receipt of one Daniel writer part to SP/Dan/dan_writer_attempt_receipts.jsonl.

A copy of ../phase0_lanes/append_launch_row.py for the writer wave: the same row shape and the same refusals, with its
own receipts file, scratch root and lanes. It refuses unless all of the following hold:
  - the brief is at --brief-sha;
  - the message file is at --message-sha, and `_launch_message_check.py` still returns MATCH on it;
  - the pin guard is CLEAR on the receipts file;
  - the receipts file is at --expect-before (ABSENT for the first row);
  - the execution has no launch row yet;
  - for --execution N > 1, execution N-1 has a launch row AND a landing row (one the pin guard's lands() accepts).
It appends under an exclusive lock with an atomic replace and a post-write check; a failed first write leaves the file
absent again.

usage: append_launch_row.py --part W1..W6 --agent-id ID --brief-sha SHA --message-sha SHA --expect-before SHA|ABSENT
                            --launched-at ISO [--execution N --retry-reason TEXT]
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
SP = HERE.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(SP / "campaign"))
from _inflight_pin_guard import lands  # noqa: E402  one landing rule, shared with the pin guard
REC = SP / "Dan" / "dan_writer_attempt_receipts.jsonl"
SCR = (r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
       r"\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_w")
PARTS = ["W%d" % n for n in range(1, 7)]
ROLE = ("Daniel writer part: tile the part's WEB range with candidate chunk rows per book_strategy_Dan.md, GREEN on "
        "_validate_writer_part_dan.py. Writes in OUT only")
PRODUCER = "this lane (Daniel writer part)"
CATCHER = ("the orchestrator's independent re-run of _validate_writer_part_dan.py, check_tiling.py and the validator "
           "suite; the S1 spot review; Fable at the campaign-end review (OW-28)")
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731
ap = argparse.ArgumentParser()
ap.add_argument("--part", required=True, choices=PARTS)
ap.add_argument("--agent-id", required=True)
ap.add_argument("--brief-sha", required=True)
ap.add_argument("--message-sha", required=True)
ap.add_argument("--expect-before", required=True)
ap.add_argument("--launched-at", required=True)
ap.add_argument("--execution", type=int, default=1)
ap.add_argument("--retry-reason")
a = ap.parse_args()
att = "dan_writer_%s_a1" % a.part
if a.execution < 1 or (a.execution > 1) != bool(a.retry_reason):
    raise SystemExit("REFUSED: --execution must be >= 1, and --retry-reason is required exactly when it is > 1")
eid = "%s#e%d" % (att, a.execution)
prev = "%s#e%d" % (att, a.execution - 1) if a.execution > 1 else None
tag = "" if a.execution == 1 else "_e%d" % a.execution
brief = HERE / ("BRIEF_%s%s.md" % (a.part, tag))
msg = Path(SCR) / ("launch_message_%s%s.txt" % (a.part, tag))
if sha(brief.read_bytes()) != a.brief_sha:
    raise SystemExit("REFUSED: the brief is not at --brief-sha")
if sha(msg.read_bytes()) != a.message_sha:
    raise SystemExit("REFUSED: the launch message is not at --message-sha")
env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
run = lambda *x: subprocess.run([sys.executable, "-B", *x], cwd=str(SP), capture_output=True, text=True,  # noqa: E731
                                encoding="utf-8", env=env)
lm = json.loads(run("campaign/_launch_message_check.py", "--book", "Dan", "--message", str(msg)).stdout)
if lm["verdict"] != "MATCH":
    raise SystemExit("REFUSED: the launch message no longer MATCHes: %s" % lm["gaps"])
g = json.loads(run("campaign/_inflight_pin_guard.py", "--book", "Dan", "--target", "Dan/" + REC.name).stdout)
if g["verdict"] != "CLEAR":
    raise SystemExit("REFUSED by pin guard: %s" % json.dumps(g)[-300:])
existed = REC.exists()
before = REC.read_bytes() if existed else None
if (a.expect_before == "ABSENT") != (before is None) or (before is not None and sha(before) != a.expect_before):
    raise SystemExit("REFUSED: receipts are at %s, not --expect-before" % (sha(before)[:12] if before is not None else "ABSENT"))
before = before or b""
rows = [json.loads(x) for x in before.decode("utf-8").splitlines() if x.strip()]
launched = {r.get("execution_id") for r in rows if r.get("record_kind") == "launch"}
landed = {x for r in rows if lands(r) for x in (r.get("execution_id"), r.get("amends_execution_id")) if x}
if eid in launched:
    raise SystemExit("REFUSED: %s already has a launch row" % eid)
if prev and not (prev in launched and prev in landed):
    raise SystemExit("REFUSED: %s needs a launch row and a landing row before %s may launch" % (prev, eid))
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
row = {"schema": "m8_attempt_receipt.v1", "record_kind": "launch", "attempt_id": att, "execution_id": eid,
       "execution_of": att, "execution_ordinal": a.execution, "previous_execution_id": prev, "retry_of": prev,
       "retry_reason": a.retry_reason, "book": "Dan", "lane": "writer_" + a.part, "role": ROLE,
       "producer": PRODUCER, "catcher": CATCHER,
       "agent": "general-purpose subagent", "agent_id": a.agent_id, "parent_agent_id": "orchestrator", "model": "claude-opus-5-5",
       "model_actual": "PENDING - read from the completion usage block", "effort": "inherited",
       "orders": "launch message file (E-62): verify the brief sha, read it whole, execute; OW-11 exception; E-13; E-19",
       "launch_message": str(msg), "launch_message_sha256": a.message_sha,
       "brief": "sp_durable/Dan/writer_lanes/" + brief.name, "brief_sha256": a.brief_sha,
       "launched_at": a.launched_at, "recorded_at": now, "outcome": "RUNNING",
       "output_dir": SCR + "\\lane_" + a.part,
       "tokens_unit_note": "at landing record BOTH units: notification (the ceiling unit, OW-28) and spend (usage fields, E-55)"}
after = before + (b"" if not before or before.endswith(b"\n") else b"\n") + (json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8")
lock = REC.with_suffix(REC.suffix + ".lock")
fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
try:
    if (REC.read_bytes() if REC.exists() else b"") != before or REC.exists() != existed:
        raise SystemExit("REFUSED: receipts changed under the lock")
    tmp = REC.with_suffix(REC.suffix + ".tmp")
    tmp.write_bytes(after)
    os.replace(tmp, REC)
    if sha(REC.read_bytes()) != sha(after):
        if existed:
            REC.write_bytes(before)
        else:
            REC.unlink()
        raise SystemExit("ROLLED BACK: receipt post-write check failed")
finally:
    os.close(fd)
    lock.unlink()
print(json.dumps({"appended": eid, "receipts": [sha(before) if existed else "ABSENT", sha(after)]}))
