#!/usr/bin/env python3
"""Amend _close_book.py (v9c, 2026-09-23): the coverage gate also checks review_packet_final_state.

Why. v9b's gate was named for the coverage validator's per-book feed rule but measured four of its five mirrored
fields; it skipped review_packet_final_state (validator line 189), so its name overclaimed (own near-miss, disclosed).
The validator compares that field with reviews/<book>/review_packets.jsonl, which no close tool from Job onward writes
(MEASURED 2026-09-23: the validator fails for Job, Ps, Prov, Eccl, Song, Isa, Jer and Lam on that missing file). So the
gate checks the state the chunk's own hold implies: accepted_candidate when the hold is null, held_lower_confidence
otherwise, which is what every held and unheld row of the shared feed carries.

Pins the tool BEFORE, runs the pin guard, applies exact-once edits, compiles, keeps .pre_<sha12>, rolls back on failure.
usage: patch_close_book_v9c.py
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
BEFORE = "01d540bdedaf96aeeaef9b87430e45c2016efd24cc7d95801ce00e9544cf3bd7"
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731

EDITS = [
    ("  existing shapes by book, so a question about the choice is sourced from the report.\n",
     "  existing shapes by book, so a question about the choice is sourced from the report.\n"
     "  AMENDED 2026-09-23 (v9c): the gate also checks review_packet_final_state. The validator compares it with\n"
     "  reviews/<book>/review_packets.jsonl, which no close tool from Job onward writes, so here it must be the state\n"
     "  the chunk's hold implies (accepted_candidate when the hold is null, else held_lower_confidence).\n"),
    ('                ("candidate_hold_state", "candidate_hold_state")))]\n',
     '                ("candidate_hold_state", "candidate_hold_state"))) or x.get("review_packet_final_state") != (\n'
     '            "accepted_candidate" if by_id[x["chunk_decision_id"]].get("candidate_hold_state") is None\n'
     '            else "held_lower_confidence")]\n'),
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
