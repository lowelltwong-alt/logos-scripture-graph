#!/usr/bin/env python3
"""Append one or more sections to an append-only markdown record (ledger, close gate), under the guarded protocol.

The target's whole-file sha256 is pinned (--expect-before). Each text file must open with a '## ' heading; a heading
already present in the target is refused (dedupe, run immediately before appending). The append happens under an
exclusive lock, by atomic replace; the result is checked byte for byte and rolled back on mismatch. Nothing before the
append point changes (E-44: append, never edit). --dry prints the plan only.

usage: _guarded_md_append.py --target PATH --expect-before SHA256 --text FILE [--text FILE ...] [--dry]
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731

ap = argparse.ArgumentParser()
ap.add_argument("--target", required=True)
ap.add_argument("--expect-before", required=True)
ap.add_argument("--text", action="append", required=True)
ap.add_argument("--dry", action="store_true")
a = ap.parse_args()
T = Path(a.target).resolve()
before = T.read_bytes()
if sha(before) != a.expect_before:
    raise SystemExit("REFUSED: %s is at %s, not the expected-before digest" % (T.name, sha(before)[:12]))
have = {l.strip() for l in before.decode("utf-8").splitlines() if l.startswith("## ")}
add, heads = b"", []
for f in a.text:
    t = Path(f).read_bytes().decode("utf-8").replace("\r\n", "\n").strip("\n")
    h = t.splitlines()[0].strip()
    if not h.startswith("## "):
        raise SystemExit("REFUSED: %s does not open with a '## ' heading" % f)
    if h in have or h in heads:
        raise SystemExit("REFUSED: heading already present: %s" % h[:90])
    heads.append(h)
    add += ("\n" + t + "\n").encode("utf-8")
after = before + (b"" if before.endswith(b"\n") else b"\n") + add
plan = {"target": T.name, "before": sha(before), "after": sha(after), "appended_bytes": len(after) - len(before),
        "headings": heads}
if a.dry:
    print(json.dumps(dict(plan, mode="dry"), ensure_ascii=False, indent=1))
    sys.exit(0)
lock = T.with_name(T.name + ".lock")
fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
try:
    if T.read_bytes() != before:
        raise SystemExit("REFUSED: target changed under the lock")
    tmp = T.with_name(T.name + ".tmp")
    tmp.write_bytes(after)
    os.replace(tmp, T)
    if T.read_bytes() != after:
        T.write_bytes(before)
        raise SystemExit("ROLLED BACK: post-write check failed")
finally:
    os.close(fd)
    lock.unlink()
print(json.dumps(dict(plan, mode="written"), ensure_ascii=False, indent=1))
