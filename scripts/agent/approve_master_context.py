#!/usr/bin/env python3
"""Human-only: approve MASTER_CONTEXT.md and update the lock file checksum."""
from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / ".ai" / "control" / "MASTER_CONTEXT.md"
LOCK = ROOT / ".ai" / "control" / "MASTER_CONTEXT.lock.yaml"

# NOTE: the name blocklist is tamper-EVIDENCE, not access control. A local
# script cannot truly gate the agent running it (see CP-1 / ADR-0009). Real
# enforcement is CODEOWNERS + branch protection on the forge. The recorded
# approved_commit lets CI verify the lock change landed via a reviewed commit.
FORBIDDEN_APPROVERS = {"ai", "agent", "codex", "claude", "gpt", "opus", "auto"}


def sha256_file(path: Path) -> str:
    # read_text normalizes newlines to \n, so the hash is stable across CRLF/LF
    # checkouts. validate_control_plane.py uses the identical computation.
    digest = hashlib.sha256()
    digest.update(path.read_text(encoding="utf-8").encode("utf-8"))
    return digest.hexdigest()


def current_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "uncommitted"


def main() -> int:
    parser = argparse.ArgumentParser(description="Human approval for MASTER_CONTEXT.md")
    parser.add_argument("--approved-by", required=True, help="Human reviewer name (not an AI agent id)")
    parser.add_argument("--note", default="", help="Optional approval note")
    args = parser.parse_args()

    approver = args.approved_by.strip()
    if approver.lower() in FORBIDDEN_APPROVERS:
        print(f"ERROR: approved_by must be a human identifier, not '{approver}'", file=sys.stderr)
        return 1

    if not MASTER.exists():
        print(f"ERROR: Missing {MASTER}", file=sys.stderr)
        return 1

    sha = sha256_file(MASTER)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    note = args.note or "Human-reviewed master context update"

    commit = current_commit()
    content = f"""# Human approval lock for MASTER_CONTEXT.md
# AI agents must NOT edit this file. Humans update after reviewing MASTER_CONTEXT.md changes.
# Enforcement is CODEOWNERS + branch protection (ADR-0009); this lock is tamper-evidence.
version: 1
file: .ai/control/MASTER_CONTEXT.md
sha256: {sha}
approved_by: {approver}
approved_at: "{now}"
approved_commit: {commit}
approval_note: "{note.replace('"', "'")}"
"""
    LOCK.write_text(content, encoding="utf-8")
    print(f"Lock updated: sha256={sha}")
    print(f"Approved by: {approver} at {now} (commit {commit})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
