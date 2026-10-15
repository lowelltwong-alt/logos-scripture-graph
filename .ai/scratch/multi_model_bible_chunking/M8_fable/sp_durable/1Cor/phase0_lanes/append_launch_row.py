#!/usr/bin/env python3
"""Append the launch receipt of one 1 Corinthians Phase 0 lane to SP/1Cor/1cor_phase0_attempt_receipts.jsonl.

Ported 2026-10-14 from Dan/phase0_lanes/append_launch_row.py; the refusal rules are Daniel's, unchanged. The row takes the
shape of Daniel's launch rows (m8_attempt_receipt.v1), plus the launch-message file and its sha256 (ledger E-62). The
lane's runtime id goes in agent_id, never in parent_agent_id, which holds "orchestrator" (ledger E-63). The orders field
names OW-36, the owner's grant for this book, in place of Daniel's OW-11 exception. It refuses unless all of the
following hold:
  - the brief is at --brief-sha;
  - the message file is at --message-sha, and `_launch_message_check.py --book 1Cor` still returns MATCH on it;
  - the pin guard is CLEAR on the receipts file;
  - the receipts file is at --expect-before (ABSENT for the first row);
  - the execution has no launch row yet;
  - for --execution N > 1, execution N-1 has a launch row AND a landing row (one the pin guard's lands() accepts).
It appends under an exclusive lock with an atomic replace and a post-write check.

usage: append_launch_row.py --lane D|T2|T1|T3|S|C1|C2|K1|K2 --agent-id ID --brief-sha SHA --message-sha SHA --expect-before SHA|ABSENT
                            --launched-at ISO [--execution N --retry-reason TEXT]
"""
import argparse
import hashlib
import json
import os
import re
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
REC = SP / "1Cor" / "1cor_phase0_attempt_receipts.jsonl"
SCR = (r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
       r"\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_p0")
LANES = {
    "D": ("cor_p0_device_inventory_a1", "device_inventory",
          "1 Corinthians device inventory: port Daniel's builder to a Greek-skeleton, self-asserting 1 Corinthians "
          "builder measured on RP and SBLGNT, and write 1cor_device_inventory.json (WEB face = Greek face by identity, "
          "citation_sweep device-arm constants, DEVICE_NO_ONSET empty with its reason). Builds in OUT only; installs "
          "nothing"),
    "T2": ("cor_p0_toolport_t2_a1", "toolport_t2",
           "write _adapt_tools_1cor.py and its spec, classify fourteen Daniel tools as token-portable, portable with a "
           "logic change or Greek-bound, port the portable ones to residual 0, and test them in an OUT mirror. Stages in "
           "OUT only; installs nothing"),
    "T1": ("cor_p0_toolport_t1_a1", "toolport_t1",
           "port citation_sweep.py and its test (_test_tools_1cor.py, from _test_zone_tools_dan.py) onto the Greek "
           "witnesses through an extra spec for the installed adapter: three ref spaces, Greek quote binding by tier, "
           "Hebrew claim arms as fabrication classes, the device arm bound to 1cor_device_inventory.json, and NT "
           "cross-tradition metadata; test in an OUT mirror. Stages in OUT only; installs nothing"),
    "T3": ("cor_p0_toolport_t3_a1", "toolport_t3",
           "port check_marks.py, the byte normalizer (normalize_greek_in_json.py, from normalize_hebrew_in_json.py) and "
           "run_validator_suite.py onto the Greek witnesses through an extra spec for the installed adapter: three "
           "never-conflated mark types (RP pilcrows, WEB paragraph starts, SBLGNT sign sites), Hebrew-only arms as "
           "fabrication classes, and the suite without language_zones; write _test_marks_tools_1cor.py; test in an OUT "
           "mirror. Stages in OUT only; installs nothing"),
    "S": ("cor_strategy_a1", "book_strategy",
          "write book_strategy_1Cor.md and strategy_plan_1Cor.json in the controlling role (grader_fallback, OW-25): "
          "test the rival macro-structures against the bytes, byte-anchor the parents, tile the writer parts, cover the "
          "7 prepared scrutiny targets and the 8 device review items, record the lens count (OW-19), and validate with "
          "_validate_strategy_1cor.py. Writes in OUT only"),
    "C1": ("cor_strategy_check_c1_a1", "strategy_check_c1",
           "blind strategy check lane 1 of 2 (OW-19), by the bytes: re-measure every fact the candidate strategy states. "
           "Writes in OUT only"),
    "C2": ("cor_strategy_check_c2_a1", "strategy_check_c2",
           "blind strategy check lane 2 of 2 (OW-19), text first: a pre-registered reading of the book, then the "
           "candidate tested against it. Writes in OUT only"),
    "K1": ("cor_toolkit_review_k1_a1", "toolkit_review_k1",
           "blind toolkit review lane 1 of 2 (OW-19), by the bytes: re-measure every figure, absence and rule "
           "TOOLKIT.md states against the witnesses and Phase 0 artifacts. Writes in OUT only"),
    "K2": ("cor_toolkit_review_k2_a1", "toolkit_review_k2",
           "blind toolkit review lane 2 of 2 (OW-19), by the code: check every tool contract TOOLKIT.md states against "
           "the tools' source, running no pinned file (E-67). Writes in OUT only"),
}
# Per-lane producer and catcher. Every lane must have an explicit entry: until 2026-10-15 these tables were empty and a
# default naming the toolkit port was written for every lane, so the D (device inventory) and S (strategy) launch rows
# recorded a wrong producer and catcher (corrected by amendment rows; E-75 candidate).
_PORT = "this lane (1 Corinthians Phase 0 toolkit port)"
_PORT_CATCH = ("the orchestrator's review and install gates; the two blind toolkit review lanes (OW-19); Fable at the "
               "campaign-end review (OW-28)")
_CHECK = ("the orchestrator's reconciliation of the two blind check lanes, byte-verifying every correction before "
          "applying it; Fable at the campaign-end review (OW-28)")
PRODUCER = {"D": "this lane (1 Corinthians device inventory)", "T2": _PORT, "T1": _PORT, "T3": _PORT,
            "S": "this lane (1 Corinthians book strategy, controlling role on grader_fallback)",
            "C1": "this lane (1 Corinthians strategy check, bytes)",
            "C2": "this lane (1 Corinthians strategy check, text first)"}
CATCHER = {"D": "the orchestrator's landing review; the strategy check lane that re-measures every device count the "
                "strategy cites (OW-19); Fable at the campaign-end review (OW-28)",
           "T2": _PORT_CATCH, "T1": _PORT_CATCH, "T3": _PORT_CATCH,
           "S": "the orchestrator's review and _validate_strategy_1cor.py; the two blind strategy check lanes (OW-19); "
                "Fable at the campaign-end review (OW-28)", "C1": _CHECK, "C2": _CHECK}
_KCHECK = ("the orchestrator's reconciliation of the two blind toolkit review lanes, byte-verifying every correction "
           "before applying it; Fable at the campaign-end review (OW-28)")
PRODUCER.update({"K1": "this lane (1 Corinthians toolkit review, bytes)",
                 "K2": "this lane (1 Corinthians toolkit review, code)"})
CATCHER.update({"K1": _KCHECK, "K2": _KCHECK})
if set(PRODUCER) != set(LANES) or set(CATCHER) != set(LANES):
    raise SystemExit("REFUSED: every lane needs an explicit PRODUCER and CATCHER entry (missing: %s)"
                     % sorted((set(LANES) - set(PRODUCER)) | (set(LANES) - set(CATCHER))))
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731
ap = argparse.ArgumentParser()
ap.add_argument("--lane", required=True, choices=sorted(LANES))
ap.add_argument("--agent-id", required=True)
ap.add_argument("--brief-sha", required=True)
ap.add_argument("--message-sha", required=True)
ap.add_argument("--expect-before", required=True)
ap.add_argument("--launched-at", required=True)
ap.add_argument("--execution", type=int, default=1)
ap.add_argument("--retry-reason")
a = ap.parse_args()
att, lane, role = LANES[a.lane]
if a.execution < 1 or (a.execution > 1) != bool(a.retry_reason):
    raise SystemExit("REFUSED: --execution must be >= 1, and --retry-reason is required exactly when it is > 1")
eid = "%s#e%d" % (att, a.execution)
prev = "%s#e%d" % (att, a.execution - 1) if a.execution > 1 else None
tag = "" if a.execution == 1 else "_e%d" % a.execution
brief = HERE / ("BRIEF_%s%s.md" % (a.lane, tag))
msg = Path(SCR) / ("launch_message_%s%s.txt" % (a.lane, tag))
# a launch time must be MEASURED: ISO, no earlier than the message file it launched (written before the gate), and no
# later than now. Added 2026-10-14 after lane D #e1 was recorded with a placeholder midnight (E-75 candidate).
_now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
_floor = datetime.fromtimestamp(msg.stat().st_mtime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", a.launched_at) or not _floor <= a.launched_at <= _now:
    raise SystemExit("REFUSED: --launched-at %s is not a measured time in [%s, %s]" % (a.launched_at, _floor, _now))
if sha(brief.read_bytes()) != a.brief_sha:
    raise SystemExit("REFUSED: the brief is not at --brief-sha")
if sha(msg.read_bytes()) != a.message_sha:
    raise SystemExit("REFUSED: the launch message is not at --message-sha")
env = dict(os.environ, PYTHONUTF8="1")
run = lambda *x: subprocess.run([sys.executable, "-B", *x], cwd=str(SP), capture_output=True, text=True,  # noqa: E731
                                encoding="utf-8", env=env)
lm = json.loads(run("campaign/_launch_message_check.py", "--book", "1Cor", "--message", str(msg)).stdout)
if lm["verdict"] != "MATCH":
    raise SystemExit("REFUSED: the launch message no longer MATCHes: %s" % lm["gaps"])
g = json.loads(run("campaign/_inflight_pin_guard.py", "--book", "1Cor", "--target", "1Cor/" + REC.name).stdout)
if g["verdict"] != "CLEAR":
    raise SystemExit("REFUSED by pin guard: %s" % json.dumps(g)[-300:])
before = REC.read_bytes() if REC.exists() else None
if (a.expect_before == "ABSENT") != (before is None) or (before is not None and sha(before) != a.expect_before):
    raise SystemExit("REFUSED: receipts are at %s, not --expect-before"
                     % (sha(before)[:12] if before is not None else "ABSENT"))
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
       "retry_reason": a.retry_reason, "book": "1Cor",
       "lane": "phase0_" + lane, "role": role,
       "producer": PRODUCER[a.lane], "catcher": CATCHER[a.lane],
       "agent": "general-purpose subagent", "agent_id": a.agent_id, "parent_agent_id": "orchestrator",
       "model": "claude-opus-5-5", "model_actual": "PENDING - read from the completion usage block", "effort": "inherited",
       "orders": "launch message file (E-62): verify the brief sha, read it whole, execute; OW-36 grant; E-13 (NT "
                 "preamble); E-19; M8-EFFICIENCY-V1",
       "launch_message": str(msg), "launch_message_sha256": a.message_sha,
       "brief": "sp_durable/1Cor/phase0_lanes/" + brief.name, "brief_sha256": a.brief_sha,
       "launched_at": a.launched_at, "recorded_at": now, "outcome": "RUNNING",
       "output_dir": SCR + "\\lane_" + a.lane + tag,
       "tokens_unit_note": "at landing record BOTH units: notification (the ceiling unit, OW-28) and spend (usage "
                           "fields, E-55)"}
after = (before + (b"" if not before or before.endswith(b"\n") else b"\n")
         + (json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8"))
lock = REC.with_suffix(REC.suffix + ".lock")
fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
try:
    if (REC.read_bytes() if REC.exists() else b"") != before:
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
print(json.dumps({"appended": eid, "receipts": [sha(before), sha(after)]}))
