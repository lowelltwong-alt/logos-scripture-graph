#!/usr/bin/env python3
"""Append landing carriers: one learning-log entry (a JSON file) and one CYCLE_STATE section (a text file).
Each write refuses unless the file is at its pin, then replaces atomically; no CR bytes are accepted.
usage: carry_append.py --log-pin SHA --state-pin SHA [--log-entry FILE.json] [--state-note FILE.md]
"""
import argparse
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SP = HERE.parents[2]
M = SP.parent
ap = argparse.ArgumentParser()
ap.add_argument("--log-pin", required=True)
ap.add_argument("--state-pin", required=True)
ap.add_argument("--log-entry")
ap.add_argument("--state-note")
a = ap.parse_args()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def put(p, b):
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_bytes(b)
    os.replace(tmp, p)
    print(p.name, sha(b))


log, state = M / "orchestration_learning_log.v1.jsonl", SP / "1Cor/freeze/CYCLE_STATE.md"
lb, sb = log.read_bytes(), state.read_bytes()
for name, b, pin in (("log", lb, a.log_pin), ("state", sb, a.state_pin)):
    if sha(b) != pin or b"\r" in b:
        raise SystemExit("REFUSED: %s is at %s" % (name, sha(b)[:12]))
if a.log_entry:
    e = json.loads(Path(a.log_entry).read_text(encoding="utf-8"))
    last = json.loads(lb.decode("utf-8").splitlines()[-1])
    if int(e["id"][2:]) != int(last["id"][2:]) + 1 or set(e) != set(last):
        raise SystemExit("REFUSED: entry id or keys do not follow %s" % last["id"])
    put(log, lb + (json.dumps(e, ensure_ascii=False) + "\n").encode("utf-8"))
if a.state_note:
    n = Path(a.state_note).read_bytes()
    if b"\r" in n:
        raise SystemExit("REFUSED: the note carries CR bytes")
    put(state, sb + b"\n" + n)
