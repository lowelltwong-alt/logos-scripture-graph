"""Append one finished line to a JSONL log under a pinned digest, for a landing that stopped before its log row went in.

usage (from sp_durable): python -B campaign/close_kit/append_log_line.py --target REL --expect-before SHA --line-file FILE
Refuses a stale digest, a file that is not exactly one JSON line, and an id the log already holds. Replaces atomically."""
import argparse
import hashlib
import json
import os
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--expect-before", required=True)
    ap.add_argument("--line-file", required=True)
    a = ap.parse_args()
    p = Path(a.target)
    raw = p.read_bytes()
    if hashlib.sha256(raw).hexdigest() != a.expect_before:
        raise SystemExit("REFUSED: target digest is not the pinned one")
    text = Path(a.line_file).read_text(encoding="utf-8").strip("\n")
    if "\n" in text:
        raise SystemExit("REFUSED: more than one line")
    row = json.loads(text)
    if ('"id": "%s"' % row["id"]).encode("utf-8") in raw:
        raise SystemExit("REFUSED: %s is already in the log" % row["id"])
    if not raw.endswith(b"\n"):
        raise SystemExit("REFUSED: the log does not end in a newline")
    tmp = p.with_suffix(".tmp")
    tmp.write_bytes(raw + text.encode("utf-8") + b"\n")
    os.replace(tmp, p)
    print("OK", row["id"], hashlib.sha256(p.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
