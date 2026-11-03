#!/usr/bin/env python3
"""Append the launch receipt of one 1 Corinthians primary-review lane (one lens on one cluster) to
SP/1Cor/review/1cor_review_attempt_receipts.jsonl.

Derived 2026-10-20 by exact replacements (scratch derive_primary_appender.py) from append_review_launch_row.py
ef5e8874b7a5, itself derived from ../writer_lanes/append_launch_row.py; its refusal rules are kept and one is added. The row takes the shape of
the Phase 0 launch rows (m8_attempt_receipt.v1), plus the launch-message file and its sha256 (ledger E-62). The part's
runtime id goes in agent_id, never in parent_agent_id, which holds "orchestrator" (ledger E-63). The orders field names
OW-36, the owner's grant for this book. It refuses unless all of the following hold:
  - --launched-at is a measured ISO time no earlier than the message file and no later than now;
  - the brief is at --brief-sha;
  - the message file is at --message-sha, and `_launch_message_check.py --book 1Cor` still returns MATCH on it;
  - the pin guard is CLEAR on the receipts file;
  - the receipts file is at --expect-before (ABSENT for the first row);
  - the execution has no launch row yet;
  - for --execution N > 1, execution N-1 has a launch row AND a landing row (one the pin guard's lands() accepts).
  - fewer than three executions in this receipts file have a launch row and no landing row (the lane cap,
    OW-31, checked here before the write and not only by the orchestrator's prelaunch gate).
It appends under an exclusive lock with an atomic replace and a post-write check.

usage: append_primary_launch_row.py --lane PRIM_OL_c01 --agent-id ID --brief-sha SHA --message-sha SHA --expect-before SHA|ABSENT
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
REC = SP / "1Cor" / "review" / "1cor_review_attempt_receipts.jsonl"
SCR = (r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
       r"\af84b702-d913-4495-8e57-252cf7894c63\scratchpad")
PARTS, OUTDIR, BRIEFNAME = {}, {}, {}
# One part per lens per cluster of 1Cor/review_clusters.json (a393f453f58d); RT only on its reception_lens clusters.
PARTS['PRIM_OL_c01'] = ('cor_primary_ol_c01_a1', 'primary_OL_c01',
            '1 Corinthians primary review, OL lens (original language), cluster c01 (W1-001..W1-008, 1Cor.1.1-1Cor.3.4), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_OL_c01'] = 'cor_prim\\OL_c01'
BRIEFNAME['PRIM_OL_c01'] = 'primaries/PRIMARY_BRIEF_OL_c01'
PARTS['PRIM_LF_c01'] = ('cor_primary_lf_c01_a1', 'primary_LF_c01',
            '1 Corinthians primary review, LF lens (literary form and discourse), cluster c01 (W1-001..W1-008, 1Cor.1.1-1Cor.3.4), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_LF_c01'] = 'cor_prim\\LF_c01'
BRIEFNAME['PRIM_LF_c01'] = 'primaries/PRIMARY_BRIEF_LF_c01'
PARTS['PRIM_OL_c02'] = ('cor_primary_ol_c02_a1', 'primary_OL_c02',
            '1 Corinthians primary review, OL lens (original language), cluster c02 (W1-009..W1-015, 1Cor.3.5-1Cor.4.21), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_OL_c02'] = 'cor_prim\\OL_c02'
BRIEFNAME['PRIM_OL_c02'] = 'primaries/PRIMARY_BRIEF_OL_c02'
PARTS['PRIM_LF_c02'] = ('cor_primary_lf_c02_a1', 'primary_LF_c02',
            '1 Corinthians primary review, LF lens (literary form and discourse), cluster c02 (W1-009..W1-015, 1Cor.3.5-1Cor.4.21), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_LF_c02'] = 'cor_prim\\LF_c02'
BRIEFNAME['PRIM_LF_c02'] = 'primaries/PRIMARY_BRIEF_LF_c02'
PARTS['PRIM_OL_c03'] = ('cor_primary_ol_c03_a1', 'primary_OL_c03',
            '1 Corinthians primary review, OL lens (original language), cluster c03 (W2-001..W2-008, 1Cor.5.1-1Cor.7.9), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_OL_c03'] = 'cor_prim\\OL_c03'
BRIEFNAME['PRIM_OL_c03'] = 'primaries/PRIMARY_BRIEF_OL_c03'
PARTS['PRIM_LF_c03'] = ('cor_primary_lf_c03_a1', 'primary_LF_c03',
            '1 Corinthians primary review, LF lens (literary form and discourse), cluster c03 (W2-001..W2-008, 1Cor.5.1-1Cor.7.9), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_LF_c03'] = 'cor_prim\\LF_c03'
BRIEFNAME['PRIM_LF_c03'] = 'primaries/PRIMARY_BRIEF_LF_c03'
PARTS['PRIM_OL_c04'] = ('cor_primary_ol_c04_a1', 'primary_OL_c04',
            '1 Corinthians primary review, OL lens (original language), cluster c04 (W2-009..W2-015, 1Cor.7.10-1Cor.7.40), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_OL_c04'] = 'cor_prim\\OL_c04'
BRIEFNAME['PRIM_OL_c04'] = 'primaries/PRIMARY_BRIEF_OL_c04'
PARTS['PRIM_LF_c04'] = ('cor_primary_lf_c04_a1', 'primary_LF_c04',
            '1 Corinthians primary review, LF lens (literary form and discourse), cluster c04 (W2-009..W2-015, 1Cor.7.10-1Cor.7.40), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_LF_c04'] = 'cor_prim\\LF_c04'
BRIEFNAME['PRIM_LF_c04'] = 'primaries/PRIMARY_BRIEF_LF_c04'
PARTS['PRIM_OL_c05'] = ('cor_primary_ol_c05_a1', 'primary_OL_c05',
            '1 Corinthians primary review, OL lens (original language), cluster c05 (W3-001..W3-008, 1Cor.8.1-1Cor.11.1), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_OL_c05'] = 'cor_prim\\OL_c05'
BRIEFNAME['PRIM_OL_c05'] = 'primaries/PRIMARY_BRIEF_OL_c05'
PARTS['PRIM_LF_c05'] = ('cor_primary_lf_c05_a1', 'primary_LF_c05',
            '1 Corinthians primary review, LF lens (literary form and discourse), cluster c05 (W3-001..W3-008, 1Cor.8.1-1Cor.11.1), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_LF_c05'] = 'cor_prim\\LF_c05'
BRIEFNAME['PRIM_LF_c05'] = 'primaries/PRIMARY_BRIEF_LF_c05'
PARTS['PRIM_OL_c06'] = ('cor_primary_ol_c06_a1', 'primary_OL_c06',
            '1 Corinthians primary review, OL lens (original language), cluster c06 (W4-001..W4-004, 1Cor.11.2-1Cor.11.34), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_OL_c06'] = 'cor_prim\\OL_c06'
BRIEFNAME['PRIM_OL_c06'] = 'primaries/PRIMARY_BRIEF_OL_c06'
PARTS['PRIM_LF_c06'] = ('cor_primary_lf_c06_a1', 'primary_LF_c06',
            '1 Corinthians primary review, LF lens (literary form and discourse), cluster c06 (W4-001..W4-004, 1Cor.11.2-1Cor.11.34), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_LF_c06'] = 'cor_prim\\LF_c06'
BRIEFNAME['PRIM_LF_c06'] = 'primaries/PRIMARY_BRIEF_LF_c06'
PARTS['PRIM_RT_c06'] = ('cor_primary_rt_c06_a1', 'primary_RT_c06',
            '1 Corinthians primary review, RT lens (reception tradition), cluster c06 (W4-001..W4-004, 1Cor.11.2-1Cor.11.34), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_RT_c06'] = 'cor_prim\\RT_c06'
BRIEFNAME['PRIM_RT_c06'] = 'primaries/PRIMARY_BRIEF_RT_c06'
PARTS['PRIM_OL_c07'] = ('cor_primary_ol_c07_a1', 'primary_OL_c07',
            '1 Corinthians primary review, OL lens (original language), cluster c07 (W5-001..W5-007, 1Cor.12.1-1Cor.13.13), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_OL_c07'] = 'cor_prim\\OL_c07'
BRIEFNAME['PRIM_OL_c07'] = 'primaries/PRIMARY_BRIEF_OL_c07'
PARTS['PRIM_LF_c07'] = ('cor_primary_lf_c07_a1', 'primary_LF_c07',
            '1 Corinthians primary review, LF lens (literary form and discourse), cluster c07 (W5-001..W5-007, 1Cor.12.1-1Cor.13.13), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_LF_c07'] = 'cor_prim\\LF_c07'
BRIEFNAME['PRIM_LF_c07'] = 'primaries/PRIMARY_BRIEF_LF_c07'
PARTS['PRIM_RT_c07'] = ('cor_primary_rt_c07_a1', 'primary_RT_c07',
            '1 Corinthians primary review, RT lens (reception tradition), cluster c07 (W5-001..W5-007, 1Cor.12.1-1Cor.13.13), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_RT_c07'] = 'cor_prim\\RT_c07'
BRIEFNAME['PRIM_RT_c07'] = 'primaries/PRIMARY_BRIEF_RT_c07'
PARTS['PRIM_OL_c08'] = ('cor_primary_ol_c08_a1', 'primary_OL_c08',
            '1 Corinthians primary review, OL lens (original language), cluster c08 (W5-008..W5-014, 1Cor.14.1-1Cor.14.40), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_OL_c08'] = 'cor_prim\\OL_c08'
BRIEFNAME['PRIM_OL_c08'] = 'primaries/PRIMARY_BRIEF_OL_c08'
PARTS['PRIM_LF_c08'] = ('cor_primary_lf_c08_a1', 'primary_LF_c08',
            '1 Corinthians primary review, LF lens (literary form and discourse), cluster c08 (W5-008..W5-014, 1Cor.14.1-1Cor.14.40), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_LF_c08'] = 'cor_prim\\LF_c08'
BRIEFNAME['PRIM_LF_c08'] = 'primaries/PRIMARY_BRIEF_LF_c08'
PARTS['PRIM_RT_c08'] = ('cor_primary_rt_c08_a1', 'primary_RT_c08',
            '1 Corinthians primary review, RT lens (reception tradition), cluster c08 (W5-008..W5-014, 1Cor.14.1-1Cor.14.40), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_RT_c08'] = 'cor_prim\\RT_c08'
BRIEFNAME['PRIM_RT_c08'] = 'primaries/PRIMARY_BRIEF_RT_c08'
PARTS['PRIM_OL_c09'] = ('cor_primary_ol_c09_a1', 'primary_OL_c09',
            '1 Corinthians primary review, OL lens (original language), cluster c09 (W6-001..W6-007, 1Cor.15.1-1Cor.16.4), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_OL_c09'] = 'cor_prim\\OL_c09'
BRIEFNAME['PRIM_OL_c09'] = 'primaries/PRIMARY_BRIEF_OL_c09'
PARTS['PRIM_LF_c09'] = ('cor_primary_lf_c09_a1', 'primary_LF_c09',
            '1 Corinthians primary review, LF lens (literary form and discourse), cluster c09 (W6-001..W6-007, 1Cor.15.1-1Cor.16.4), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_LF_c09'] = 'cor_prim\\LF_c09'
BRIEFNAME['PRIM_LF_c09'] = 'primaries/PRIMARY_BRIEF_LF_c09'
PARTS['PRIM_OL_c10'] = ('cor_primary_ol_c10_a1', 'primary_OL_c10',
            '1 Corinthians primary review, OL lens (original language), cluster c10 (W6-008..W6-014, 1Cor.16.5-1Cor.16.24), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_OL_c10'] = 'cor_prim\\OL_c10'
BRIEFNAME['PRIM_OL_c10'] = 'primaries/PRIMARY_BRIEF_OL_c10'
PARTS['PRIM_LF_c10'] = ('cor_primary_lf_c10_a1', 'primary_LF_c10',
            '1 Corinthians primary review, LF lens (literary form and discourse), cluster c10 (W6-008..W6-014, 1Cor.16.5-1Cor.16.24), blind, on the FIXUP-2 applied rows (1Cor/fixup/draft_rows_fixup2_applied.jsonl); candidate-only. Writes in OUT only')
OUTDIR['PRIM_LF_c10'] = 'cor_prim\\LF_c10'
BRIEFNAME['PRIM_LF_c10'] = 'primaries/PRIMARY_BRIEF_LF_c10'
# Every part needs an explicit producer and catcher (the Phase 0 tables once defaulted a wrong pair; E-75).
PRODUCER = {p: "this lane (1 Corinthians primary lane %s, claude-opus-5-5 on grader_fallback, OW-25)" % p for p in PARTS}
CATCHER = {p: ("the orchestrator's landing check of the deliverable against the primary contract (one item "
               "per cluster row, the field names, severity exactly on a challenge, the summary recount, both "
               "triage answers, the rows digest, every Greek run found in its witness, no CR bytes); the "
               "next controlling round weighs the lanes against each other") for p in PARTS}

if set(PRODUCER) != set(PARTS) or set(CATCHER) != set(PARTS):
    raise SystemExit("REFUSED: every part needs an explicit PRODUCER and CATCHER entry")
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731
ap = argparse.ArgumentParser()
ap.add_argument("--lane", dest="part", required=True, choices=sorted(PARTS))
ap.add_argument("--agent-id", required=True)
ap.add_argument("--brief-sha", required=True)
ap.add_argument("--message-sha", required=True)
ap.add_argument("--expect-before", required=True)
ap.add_argument("--launched-at", required=True)
ap.add_argument("--execution", type=int, default=1)
ap.add_argument("--retry-reason")
ap.add_argument("--message-rebuilt", action="store_true",
                help="the message file was purged and rebuilt byte-identical by the generator, so its mtime is no floor; "
                     "the digest checks below still bind it and the row says so")
a = ap.parse_args()
att, lane, role = PARTS[a.part]
if a.execution < 1 or (a.execution > 1) != bool(a.retry_reason):
    raise SystemExit("REFUSED: --execution must be >= 1, and --retry-reason is required exactly when it is > 1")
eid = "%s#e%d" % (att, a.execution)
prev = "%s#e%d" % (att, a.execution - 1) if a.execution > 1 else None
tag = "" if a.execution == 1 else "_e%d" % a.execution
brief = HERE / ("%s%s.md" % (BRIEFNAME[a.part], tag))
msg = Path(SCR) / "cor_review_msgs" / ("launch_message_%s%s.txt" % (a.part, tag))
_now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
_floor = datetime.fromtimestamp(msg.stat().st_mtime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", a.launched_at) or not (a.message_rebuilt or _floor <= a.launched_at) or a.launched_at > _now:
    raise SystemExit("REFUSED: --launched-at %s is not a measured time in [%s, %s]" % (a.launched_at, _floor, _now))
if sha(brief.read_bytes()) != a.brief_sha:
    raise SystemExit("REFUSED: the brief is not at --brief-sha")
if sha(msg.read_bytes()) != a.message_sha:
    raise SystemExit("REFUSED: the launch message is not at --message-sha")
env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
run = lambda *x: subprocess.run([sys.executable, "-B", *x], cwd=str(SP), capture_output=True, text=True,  # noqa: E731
                                encoding="utf-8", env=env)
lm = json.loads(run("campaign/_launch_message_check.py", "--book", "1Cor", "--message", str(msg)).stdout)
if lm["verdict"] != "MATCH":
    raise SystemExit("REFUSED: the launch message no longer MATCHes: %s" % lm["gaps"])
g = json.loads(run("campaign/_inflight_pin_guard.py", "--book", "1Cor", "--target", "1Cor/review/" + REC.name).stdout)
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
live = sorted(launched - landed)
if len(live) >= 3:
    raise SystemExit("REFUSED: %d executions launched without landing (cap 3, OW-31): %s" % (len(live), live))
if eid in launched:
    raise SystemExit("REFUSED: %s already has a launch row" % eid)
if prev and not (prev in launched and prev in landed):
    raise SystemExit("REFUSED: %s needs a launch row and a landing row before %s may launch" % (prev, eid))
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
row = {"schema": "m8_attempt_receipt.v1", "record_kind": "launch", "attempt_id": att, "execution_id": eid,
       "execution_of": att, "execution_ordinal": a.execution, "previous_execution_id": prev, "retry_of": prev,
       "retry_reason": a.retry_reason, "book": "1Cor",
       "lane": lane, "role": role,
       "producer": PRODUCER[a.part], "catcher": CATCHER[a.part],
       "agent": "general-purpose subagent", "agent_id": a.agent_id, "parent_agent_id": "orchestrator",
       "model": "claude-opus-5-5", "model_actual": "PENDING - read from the completion usage block", "effort": "inherited",
       "orders": "launch message file (E-62): verify the brief sha, read it whole, execute; OW-36 grant; E-13 (NT "
                 "preamble); E-19; M8-EFFICIENCY-V1",
       "launch_message": str(msg), "launch_message_sha256": a.message_sha,
       "brief": "sp_durable/1Cor/review/primaries/" + brief.name, "brief_sha256": a.brief_sha,
       "launch_message_rebuilt": a.message_rebuilt,
       "launched_at": a.launched_at, "recorded_at": now, "outcome": "RUNNING",
       "output_dir": SCR + "\\" + OUTDIR[a.part] + "_e%d" % a.execution,
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
