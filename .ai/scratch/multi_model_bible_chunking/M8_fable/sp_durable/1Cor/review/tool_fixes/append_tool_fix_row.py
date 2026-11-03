#!/usr/bin/env python3
"""Append one tool_fix_install or gate_flip receipt to SP/1Cor/review/1cor_review_attempt_receipts.jsonl. Refuses unless the
row is schema m8_attempt_receipt.v1, book 1Cor, of one of those kinds, with a non-empty outcome or gate; the pin guard is
CLEAR on the receipts file; and the file is at --expect-before. Stamps recorded_at, then appends under an exclusive lock
with an atomic replace and a post-write check, as append_review_landing_row.py does.
usage: append_tool_fix_row.py --row-file FILE --expect-before SHA
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REC = HERE.parent / "1cor_review_attempt_receipts.jsonl"
SP = HERE.parents[2]


def sha(b):
    return hashlib.sha256(b).hexdigest()


ap = argparse.ArgumentParser()
ap.add_argument("--row-file", required=True)
ap.add_argument("--expect-before", required=True)
a = ap.parse_args()
row = json.loads(Path(a.row_file).read_text(encoding="utf-8"))
if row.get("schema") != "m8_attempt_receipt.v1" or row.get("book") != "1Cor" \
        or row.get("record_kind") not in ("tool_fix_install", "gate_flip", "cwo_coverage_report") or not (row.get("outcome") or row.get("gate")):
    raise SystemExit("REFUSED: the row is malformed")
env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
g = json.loads(subprocess.run([sys.executable, "-B", "campaign/_inflight_pin_guard.py", "--book", "1Cor", "--target",
                               "1Cor/review/" + REC.name], cwd=str(SP), capture_output=True, text=True, encoding="utf-8",
                              env=env).stdout)
if g["verdict"] != "CLEAR":
    raise SystemExit("REFUSED by pin guard: %s" % json.dumps(g)[-300:])
before = REC.read_bytes()
if sha(before) != a.expect_before:
    raise SystemExit("REFUSED: receipts are at %s, not --expect-before" % sha(before)[:12])
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
finally:
    os.close(fd)
    lock.unlink()
if sha(REC.read_bytes()) != sha(after):
    raise SystemExit("POST-CHECK FAILED")
print("appended line", after.count(b"\n"), "sha", sha(after))
