#!/usr/bin/env python3
"""Validate the read-only DAD transport cutover for this Logos repository."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / ".digital-asset" / "dad-integration.json"
WRITE_POLICY = ROOT / ".digital-asset" / "dad-write-policy.json"
MAIL_GITIGNORE = ROOT / ".digital-asset" / "mail" / ".gitignore"
MAIL_README = ROOT / ".digital-asset" / "mail" / "README.md"
RUNTIME_OUTBOX = ".digital-asset/mail/outbox.jsonl"
FIXTURE = ROOT / "tests" / "fixtures" / "dad" / "candidate_messages.jsonl"
FIXTURE_MANIFEST = ROOT / "tests" / "fixtures" / "dad" / "candidate_messages.manifest.json"


class DadTransportContractError(ValueError):
    """Raised when the local transport or deny-write contract drifts."""


def _mapping(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DadTransportContractError(f"{path.relative_to(ROOT)}: unreadable JSON") from exc
    if not isinstance(value, dict):
        raise DadTransportContractError(f"{path.relative_to(ROOT)}: expected object")
    return value


def validate_dad_transport_contract(root: Path = ROOT, *, check_git_index: bool = True) -> None:
    root = root.resolve()
    contract = _mapping(root / CONTRACT.relative_to(ROOT))
    policy = _mapping(root / WRITE_POLICY.relative_to(ROOT))
    transport = contract.get("transport")
    if contract.get("repo_id") != "logos-scripture-graph":
        raise DadTransportContractError("contract repo_id mismatch")
    if transport != {
        "surface_version": "1.0.0",
        "implementation_version": "1.0.0-m0m1m2",
        "mode": "local_pull",
        "journal_fallback": True,
    }:
        raise DadTransportContractError("transport version or mode mismatch")
    if contract.get("approved_dad_managed_paths") != []:
        raise DadTransportContractError("Logos contract must grant no DAD-managed paths")
    if policy.get("repo_id") != "logos-scripture-graph" or policy.get("dad_write_allowed") is not False:
        raise DadTransportContractError("DAD write policy must deny all repository writes")
    if policy.get("approved_explicit_approval_ids") != []:
        raise DadTransportContractError("DAD write policy must contain no standing approval IDs")
    for key in ("dad_push_or_inbox_write_allowed", "rollout_approval_is_standing_write_permission"):
        if policy.get(key) is not False:
            raise DadTransportContractError(f"DAD write policy {key} must be false")
    mail_ignore = (root / MAIL_GITIGNORE.relative_to(ROOT)).read_text(encoding="utf-8")
    if "*.jsonl" not in mail_ignore:
        raise DadTransportContractError("mail .gitignore must ignore every JSONL spool")
    readme = (root / MAIL_README.relative_to(ROOT)).read_text(encoding="utf-8")
    if "DAD may not create, modify, deliver, archive, or delete" not in readme:
        raise DadTransportContractError("mail README must preserve the deny-write boundary")
    fixture = root / FIXTURE.relative_to(ROOT)
    if not fixture.is_file():
        raise DadTransportContractError("tracked candidate fixture missing")
    manifest = _mapping(root / FIXTURE_MANIFEST.relative_to(ROOT))
    rows = [line for line in fixture.read_text(encoding="utf-8").splitlines() if line.strip()]
    digest = hashlib.sha256(fixture.read_bytes()).hexdigest()
    if manifest.get("runtime_spool") is not False:
        raise DadTransportContractError("candidate fixture must deny runtime-spool status")
    if manifest.get("row_count") != len(rows) or manifest.get("sha256") != digest:
        raise DadTransportContractError("candidate fixture manifest count or hash mismatch")
    if check_git_index:
        ignored = subprocess.run(
            ["git", "-C", str(root), "check-ignore", "--quiet", "--no-index", RUNTIME_OUTBOX],
            capture_output=True,
            check=False,
            text=True,
        )
        if ignored.returncode != 0:
            raise DadTransportContractError("runtime DAD outbox is not ignored by Git")
        tracked = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--error-unmatch", "--", RUNTIME_OUTBOX],
            capture_output=True,
            check=False,
            text=True,
        )
        if tracked.returncode == 0:
            raise DadTransportContractError("runtime DAD outbox remains tracked in Git")


def main() -> int:
    try:
        validate_dad_transport_contract()
    except (DadTransportContractError, OSError) as exc:
        print(f"DAD transport contract validation failed: {exc}", file=sys.stderr)
        return 1
    print("DAD transport contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
