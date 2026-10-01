#!/usr/bin/env python3
"""Append the landing receipt of one Daniel Phase 0 execution to SP/Dan/dan_phase0_attempt_receipts.jsonl.

A landing row closes one launched execution, whether it completed, failed or was stopped. It takes the shape of Ezekiel's
v10 completion rows: record_kind "completion", naming its execution by amends_execution_id. The in-flight pin guard treats
the execution as landed once this row exists. The script refuses unless all of the following hold:
  - the row file holds one JSON object with schema m8_attempt_receipt.v1, record_kind "completion", book "Dan", an
    amends_execution_id, an attempt_id matching that execution, and a non-empty outcome;
  - the named execution has a launch row, and no landing row yet;
  - the pin guard is CLEAR on the receipts file;
  - the receipts file is at --expect-before.
It stamps recorded_at, then appends under an exclusive lock with an atomic replace and a post-write check.

usage: append_landing_row.py --row-file FILE --expect-before SHA
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
from _inflight_pin_guard import lands  # noqa: E402  one landing rule, shared with the pin guard (2026-09-24)
REC = SP / "Dan" / "dan_phase0_attempt_receipts.jsonl"
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731
ap = argparse.ArgumentParser()
ap.add_argument("--row-file", required=True)
ap.add_argument("--expect-before", required=True)
a = ap.parse_args()
row = json.loads(Path(a.row_file).read_text(encoding="utf-8"))
need = {"schema": "m8_attempt_receipt.v1", "record_kind": "completion", "book": "Dan"}
bad = [k for k, v in need.items() if row.get(k) != v]
eid = row.get("amends_execution_id") or ""
if bad or not eid or row.get("attempt_id") != eid.split("#")[0] or not str(row.get("outcome") or "").strip():
    raise SystemExit("REFUSED: the row is malformed (%s)" % (bad or "amends_execution_id/attempt_id/outcome"))
env = dict(os.environ, PYTHONUTF8="1")
g = json.loads(subprocess.run([sys.executable, "-B", "campaign/_inflight_pin_guard.py", "--book", "Dan", "--target",
                               "Dan/" + REC.name], cwd=str(SP), capture_output=True, text=True, encoding="utf-8",
                              env=env).stdout)
if g["verdict"] != "CLEAR":
    raise SystemExit("REFUSED by pin guard: %s" % json.dumps(g)[-300:])
before = REC.read_bytes()
if sha(before) != a.expect_before:
    raise SystemExit("REFUSED: receipts are at %s, not --expect-before" % sha(before)[:12])
rows = [json.loads(x) for x in before.decode("utf-8").splitlines() if x.strip()]
if not any(r.get("record_kind") == "launch" and r.get("execution_id") == eid for r in rows):
    raise SystemExit("REFUSED: %s has no launch row" % eid)
if any(lands(r) and eid in (r.get("execution_id"), r.get("amends_execution_id")) for r in rows):
    raise SystemExit("REFUSED: %s already has a landing row" % eid)
row["recorded_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
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
print(json.dumps({"landed": eid, "outcome": row["outcome"][:60], "receipts": [sha(before), sha(after)]}))
