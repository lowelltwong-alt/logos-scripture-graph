#!/usr/bin/env python3
"""Install one landed 1 Corinthians review-lane output byte-identical into 1Cor/review/ by receipt.

Derived 2026-10-20 from step 1 of build_ctl_launch.py (the S1 install), generalized to any review execution. It refuses
unless: the review receipts are at --expect-before and hold no CR bytes; exactly one completion row amends --execution
and it names exactly one output; the scratch output is at that row's digest; the destination name is a plain file name
in 1Cor/review/; the pin guard is CLEAR on the destination and on the receipts. An existing destination with other
bytes is REFUSED; with the same bytes and an install row already present, the run is a no-op. It appends an install
row under an exclusive lock with an atomic replace and a post-write check.

usage: install_review_output.py --execution ID --name FILE --expect-before SHA [--dry-run]
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
SP = HERE.parents[1]
REC = HERE / "1cor_review_attempt_receipts.jsonl"
env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
sha = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731


def guard(p):
    rel = str(p.resolve().relative_to(SP)).replace("\\", "/")
    g = subprocess.run([sys.executable, "-B", str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "1Cor",
                        "--target", rel], capture_output=True, text=True, encoding="utf-8", cwd=str(SP), env=env)
    if '"verdict": "CLEAR"' not in g.stdout:
        raise SystemExit("REFUSED by pin guard on %s: %s" % (rel, g.stdout[-300:]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--execution", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--expect-before", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if Path(a.name).name != a.name or not a.name.endswith(".json"):
        raise SystemExit("REFUSED: --name must be a plain .json file name")
    dst = HERE / a.name
    before = REC.read_bytes()
    if sha(before) != a.expect_before:
        raise SystemExit("REFUSED: review receipts are at %s, not --expect-before" % sha(before)[:12])
    if b"\r" in before:
        raise SystemExit("REFUSED: CR bytes in the review receipts")
    old = [json.loads(x) for x in before.decode("utf-8").splitlines() if x.strip()]
    done = [r for r in old if r.get("record_kind") == "completion" and r.get("amends_execution_id") == a.execution]
    if len(done) != 1 or len(done[0].get("outputs") or []) != 1:
        raise SystemExit("REFUSED: need exactly one completion row with one output for %s" % a.execution)
    src = Path(done[0]["outputs"][0]["path"])
    osha = done[0]["outputs"][0]["sha256"]
    b = src.read_bytes()
    if sha(b) != osha:
        raise SystemExit("REFUSED: the scratch output is not at the completion row's digest")
    if b"\r" in b:
        raise SystemExit("REFUSED: CR bytes in the output")
    installed = any(r.get("record_kind") == "install" and r.get("installs_execution_id") == a.execution
                    and r.get("output_sha256") == osha for r in old)
    if dst.exists() and dst.read_bytes() != b:
        raise SystemExit("REFUSED: %s exists with different bytes" % dst.name)
    if installed and dst.exists():
        print(json.dumps({"noop": "already installed", "installed": osha[:12], "receipts": sha(before)[:12]}))
        return
    guard(dst)
    guard(REC)
    if a.dry_run:
        print(json.dumps({"dry_run": True, "would_install": str(dst.name), "sha256": osha[:12]}))
        return
    if not dst.exists():
        tmp = dst.with_name(dst.name + ".tmp")
        tmp.write_bytes(b)
        os.replace(tmp, dst)
    if sha(dst.read_bytes()) != osha:
        raise SystemExit("REFUSED: the installed copy is not at the completion row's digest")
    row = {"schema": "m8_attempt_receipt.v1", "record_kind": "install", "book": "1Cor",
           "attempt_id": a.execution.split("#")[0], "installs_execution_id": a.execution,
           "source": str(src), "installed_path": "sp_durable/1Cor/review/" + dst.name, "output_sha256": osha,
           "method": "byte-identical copy by 1Cor/review/install_review_output.py; pin guard CLEAR",
           "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    after = before + (b"" if not before or before.endswith(b"\n") else b"\n") + \
        (json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8")
    lock = REC.with_name(REC.name + ".lock")
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        if REC.read_bytes() != before:
            raise SystemExit("REFUSED: receipts changed under the lock")
        tmp = REC.with_name(REC.name + ".tmp_append")
        tmp.write_bytes(after)
        os.replace(tmp, REC)
        if sha(REC.read_bytes()) != sha(after):
            REC.write_bytes(before)
            raise SystemExit("ROLLED BACK: receipt post-write check failed")
    finally:
        os.close(fd)
        os.remove(lock)
    print(json.dumps({"installed": dst.name, "sha256": osha[:12], "receipts": [sha(before)[:12], sha(after)[:12]]}))


if __name__ == "__main__":
    main()
