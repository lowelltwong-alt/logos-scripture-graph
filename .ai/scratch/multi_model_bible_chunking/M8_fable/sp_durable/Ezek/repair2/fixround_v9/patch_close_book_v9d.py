#!/usr/bin/env python3
"""Amend _close_book.py (v9d, 2026-09-23): fix v9c's operator precedence in the coverage gate's stale test.

Why. v9c appended its review_packet_final_state test with a bare `or`, so it bound as (in low_ids and any(...)) or
(state test). The state test then ran on rows outside the low/medium_low set: MEASURED on the v9c dry run, M8-Ezek-082
was reported both orphan and stale, and a row naming a chunk not in this book would raise KeyError in by_id instead of
failing its gate. Own defect, caught by the first dry run after v9c, disclosed. The fix parenthesises the two tests so
both apply only inside the low/medium_low set, as the validator's loop does (expected_low_ids & sidecar & packets).

Pins the tool BEFORE, runs the pin guard, applies exact-once edits, compiles, keeps .pre_<sha12>, rolls back on failure.
usage: patch_close_book_v9d.py
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
EZ = HERE.parents[1]
SP = EZ.parent
T = EZ / "_close_book.py"
BEFORE = "4c68ab3e7454d82d0de9ce7f13d6db047614967a62e452e4c077309421f45a74"
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731

EDITS = [
    ('opt if x.get("chunk_decision_id") in low_ids and any(\n',
     'opt if x.get("chunk_decision_id") in low_ids and (any(\n'),
    ('            else "held_lower_confidence")]\n',
     '            else "held_lower_confidence"))]\n'),
    ("  the chunk's hold implies (accepted_candidate when the hold is null, else held_lower_confidence).\n",
     "  the chunk's hold implies (accepted_candidate when the hold is null, else held_lower_confidence).\n"
     "  AMENDED 2026-09-23 (v9d): both stale tests apply only inside the low/medium_low set (v9c's bare `or` let the\n"
     "  state test run on orphans too).\n"),
]

g = subprocess.run([sys.executable, "-B", str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek", "--target",
                    "Ezek/_close_book.py"], cwd=str(SP), capture_output=True, text=True, encoding="utf-8",
                   env=dict(os.environ, PYTHONUTF8="1"))
if json.loads(g.stdout)["verdict"] != "CLEAR":
    raise SystemExit("REFUSED by pin guard: " + g.stdout[-300:])
before = T.read_bytes()
if sha(before) != BEFORE:
    raise SystemExit("REFUSED: _close_book.py is at %s, not the expected-before digest" % sha(before)[:12])
src = before.decode("utf-8")
for old, new in EDITS:
    if src.count(old) != 1:
        raise SystemExit("REFUSED: an anchor occurs %d times: %r" % (src.count(old), old[:70]))
    src = src.replace(old, new)
keep = T.with_name(T.name + ".pre_" + BEFORE[:12])
if keep.exists() and keep.read_bytes() != before:
    raise SystemExit("REFUSED: %s exists with different bytes" % keep.name)
keep.write_bytes(before)
try:
    compile(src, str(T), "exec")
except SyntaxError as e:
    raise SystemExit("REFUSED: the amended tool does not compile: %s" % e)
tmp = T.with_suffix(".py.tmp")
tmp.write_bytes(src.encode("utf-8"))
os.replace(tmp, T)
after = T.read_bytes()
if after != src.encode("utf-8"):
    T.write_bytes(before)
    raise SystemExit("ROLLED BACK: post-write check failed")
print(json.dumps({"tool": [BEFORE, sha(after)], "kept": keep.name, "edits": len(EDITS)}))
