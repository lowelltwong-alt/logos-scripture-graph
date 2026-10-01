#!/usr/bin/env python3
"""Atomically bind every active review packet to one final checker attempt."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    parser.add_argument("--checker-attempt-id", required=True)
    parser.add_argument("--expected-packets-sha256", required=True)
    args = parser.parse_args()
    path = MODEL / "reviews" / args.book / "review_packets.jsonl"
    actual = digest(path)
    if actual != args.expected_packets_sha256:
        raise SystemExit(f"stale packet migration input: expected {args.expected_packets_sha256}, found {actual}")
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    expected_ref = f"reviews/{args.book}/post_resolution_check_v2.json"
    for row in rows:
        postcheck = row.get("post_resolution_check")
        if not isinstance(postcheck, dict):
            raise SystemExit(f"{row.get('decision_id')}: post_resolution_check missing")
        postcheck["checker_attempt_id"] = args.checker_attempt_id
        postcheck["evidence_refs"] = [expected_ref]

    temporary = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"bound {len(rows)} {args.book} packets to {args.checker_attempt_id}; sha256={digest(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())