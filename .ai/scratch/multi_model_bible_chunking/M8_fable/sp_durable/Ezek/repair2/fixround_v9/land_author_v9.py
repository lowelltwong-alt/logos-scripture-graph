#!/usr/bin/env python3
"""Land the v9 bounded author (ezek_fixround_v9_author_a1#e1): transcribe its three outputs durable, measure both token
units, append the completion receipt.

TRANSCRIPTION. proposal.json, discharge.json and final_message.md are copied byte for byte from the scratch OUT into
author_a1/ beside this file (write-new: same bytes left, different bytes refused). The receipt records each sha256.

UNITS (OW-28 / E-55). Notification unit: the completion notification's subagent_tokens, passed on the command line
(REPORTED). Spend unit: input + cache_creation + output per unique message id, from the runtime transcript's usage
fields, by census v4's own method; cache reads beside it, never added (MEASURED). Only message.id, message.usage and
message.model are read from the transcript; no content is read or printed.

RECEIPT. One completion row amending the launch execution id, appended under an exclusive lock with the file's digest
pinned before, checked after, rolled back on mismatch (E-44: append, never edit).
usage: land_author_v9.py --notification N --tool-uses N --duration-ms N
"""
import argparse
import glob
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
OUTD = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
            r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_fixround_v9\author_a1")
DUR = HERE / "author_a1"
REC = HERE / "ezek_fixround_v9_attempt_receipts.jsonl"
AGENT, EXE, ATT = "a76e29eade8048032", "ezek_fixround_v9_author_a1#e1", "ezek_fixround_v9_author_a1"
PROJ = Path(os.path.expanduser("~")) / ".claude" / "projects" / "C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
FILES = ("proposal.json", "discharge.json", "final_message.md")
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731

ap = argparse.ArgumentParser()
ap.add_argument("--notification", type=int, required=True)
ap.add_argument("--tool-uses", type=int, required=True)
ap.add_argument("--duration-ms", type=int, required=True)
a = ap.parse_args()

rec_before = REC.read_bytes()
rows = [json.loads(l) for l in rec_before.decode("utf-8").splitlines() if l.strip()]
if any(r.get("amends_execution_id") == EXE for r in rows):
    raise SystemExit("REFUSED: a completion row for %s already exists" % EXE)
launch = [r for r in rows if r.get("execution_id") == EXE and r.get("record_kind") == "launch"]
if len(launch) != 1 or launch[0].get("agent_id") != AGENT:
    raise SystemExit("REFUSED: the launch row is not the one expected")

# 1. transcribe
DUR.mkdir(exist_ok=True)
outputs = {}
for fn in FILES:
    b = (OUTD / fn).read_bytes()
    p = DUR / fn
    if p.exists() and p.read_bytes() != b:
        raise SystemExit("REFUSED: %s exists durable with different bytes" % fn)
    if not p.exists():
        shutil.copyfile(OUTD / fn, p)
    if sha(p.read_bytes()) != sha(b):
        raise SystemExit("REFUSED: transcription of %s does not match" % fn)
    outputs[fn] = sha(b)
prop = json.loads((DUR / "proposal.json").read_text(encoding="utf-8"))

# 2. measure (census v4's method)
found = glob.glob(str(PROJ / "*" / "subagents" / ("agent-%s.jsonl" % AGENT)))
if len(found) != 1:
    raise SystemExit("REFUSED: expected one transcript for %s, found %d" % (AGENT, len(found)))
usage, models = {}, set()
with open(found[0], encoding="utf-8", errors="replace") as fh:
    for line in fh:
        try:
            d = json.loads(line)
        except ValueError:
            continue
        m = d.get("message") if isinstance(d, dict) else None
        if isinstance(m, dict) and m.get("id") and isinstance(m.get("usage"), dict):
            usage[m["id"]] = m["usage"]
            if m.get("model"):
                models.add(m["model"])
g = lambda k: sum(int(u.get(k) or 0) for u in usage.values())               # noqa: E731
spend = g("input_tokens") + g("cache_creation_input_tokens") + g("output_tokens")
meas = {"spend_unit": spend, "cache_read": g("cache_read_input_tokens"), "requests": len(usage),
        "input": g("input_tokens"), "cache_creation": g("cache_creation_input_tokens"), "output": g("output_tokens")}
if models != {"claude-opus-5-5"}:
    raise SystemExit("REFUSED: transcript models are %s, not claude-opus-5-5 only" % sorted(models))

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
row = {"schema": "m8_attempt_receipt.v1", "record_kind": "completion", "amends_execution_id": EXE, "attempt_id": ATT,
       "book": "Ezek", "lane": "fixround_v9_author", "outcome": "COMPLETED", "agent_id": AGENT,
       "model_ordered": "claude-opus-5-5", "model_actual": "claude-opus-5-5",
       "model_actual_tier": "MEASURED (message.model on every request of the runtime transcript)",
       "tokens_notification_unit": a.notification,
       "tokens_notification_tier": "REPORTED (completion notification, subagent_tokens; the OW-28 ceiling unit)",
       "tokens_spend_unit": spend, "tokens_spend_measure": meas,
       "tokens_spend_tier": "MEASURED (usage fields per unique message id, census v4 method; cache reads not added)",
       "tool_uses": a.tool_uses, "duration_ms": a.duration_ms, "interruptions": [],
       "durable_dir": "sp_durable/Ezek/repair2/fixround_v9/author_a1", "outputs": outputs,
       "proposal_rows": {k: sorted(v) for k, v in (prop.get("rows") or {}).items()},
       "proposal_bound_to": prop.get("rows_sha256"),
       "e19_selfreport": "no (REPORTED in final_message.md: no directory listed, globbed or searched)",
       "recorded_at": now}
add = (json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8")
after = rec_before + (b"" if rec_before.endswith(b"\n") else b"\n") + add
lock = REC.with_suffix(REC.suffix + ".lock")
fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
try:
    if REC.read_bytes() != rec_before:
        raise SystemExit("REFUSED: receipts changed under the lock")
    tmp = REC.with_suffix(REC.suffix + ".tmp")
    tmp.write_bytes(after)
    os.replace(tmp, REC)
    if sha(REC.read_bytes()) != sha(after):
        REC.write_bytes(rec_before)
        raise SystemExit("ROLLED BACK: receipt post-write check failed")
finally:
    os.close(fd)
    lock.unlink()
print(json.dumps({"outputs": outputs, "measure": meas, "notification": a.notification,
                  "ratio_spend_over_notification": round(spend / a.notification, 3),
                  "receipts_sha256": [sha(rec_before), sha(after)], "proposal_rows": row["proposal_rows"]}, indent=1))
