#!/usr/bin/env python3
"""Change a close spec by exact text pairs under a digest pin: no reserialization, and the result must still parse.

Input is a JSON list of [old, new] pairs. Each old string must occur exactly once. The file is pinned by --expect-before,
replaced atomically, and the printout names the facts that changed, so a dry run shows the semantic change. Book-agnostic (TE-7).

usage (from SP): python -B campaign/close_kit/set_spec_text.py --spec REL --expect-before SHA --pairs FILE [--dry-run]
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--expect-before", required=True)
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    target = SP / a.spec
    raw = target.read_bytes()
    if hashlib.sha256(raw).hexdigest() != a.expect_before:
        raise SystemExit("REFUSED: %s is not at the pinned digest" % a.spec)
    text = raw.decode("utf-8")
    before = json.loads(text)
    for old, new in json.loads(Path(a.pairs).read_text(encoding="utf-8")):
        if text.count(old) != 1:
            raise SystemExit("REFUSED: %d occurrences of %r" % (text.count(old), old[:60]))
        text = text.replace(old, new)
    after = json.loads(text)
    changed = sorted(k for k in set(before["facts"]) | set(after["facts"]) if before["facts"].get(k) != after["facts"].get(k))
    pending = sorted(set(before.get("pending_facts", {})) - set(after.get("pending_facts", {})))
    data = text.encode("utf-8")
    if not a.dry_run:
        tmp = target.with_suffix(target.suffix + ".tmp")
        tmp.write_bytes(data)
        os.replace(tmp, target)
    print(json.dumps({"dry_run": a.dry_run, "facts_changed": changed, "pending_cleared": pending,
                      "sha256": hashlib.sha256(data).hexdigest()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
