from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from scripts.validate_dad_transport_contract import (
    DadTransportContractError,
    validate_dad_transport_contract,
)

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    ".digital-asset/dad-integration.json",
    ".digital-asset/dad-write-policy.json",
    ".digital-asset/mail/.gitignore",
    ".digital-asset/mail/README.md",
    "tests/fixtures/dad/candidate_messages.jsonl",
    "tests/fixtures/dad/candidate_messages.manifest.json",
)


def _fixture_root(tmp_path: Path) -> Path:
    for relative in FILES:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    return tmp_path


def test_current_dad_transport_contract_passes() -> None:
    validate_dad_transport_contract(ROOT)


def test_rejects_standing_dad_write_approval(tmp_path: Path) -> None:
    root = _fixture_root(tmp_path)
    path = root / ".digital-asset/dad-write-policy.json"
    policy = json.loads(path.read_text(encoding="utf-8"))
    policy["approved_explicit_approval_ids"] = ["standing-bypass"]
    path.write_text(json.dumps(policy), encoding="utf-8")

    with pytest.raises(DadTransportContractError, match="standing approval"):
        validate_dad_transport_contract(root, check_git_index=False)


def test_rejects_transport_version_drift(tmp_path: Path) -> None:
    root = _fixture_root(tmp_path)
    path = root / ".digital-asset/dad-integration.json"
    contract = json.loads(path.read_text(encoding="utf-8"))
    contract["transport"]["implementation_version"] = "stale"
    path.write_text(json.dumps(contract), encoding="utf-8")

    with pytest.raises(DadTransportContractError, match="version or mode"):
        validate_dad_transport_contract(root, check_git_index=False)


def test_rejects_candidate_fixture_drift(tmp_path: Path) -> None:
    root = _fixture_root(tmp_path)
    path = root / "tests/fixtures/dad/candidate_messages.jsonl"
    path.write_text(path.read_text(encoding="utf-8") + "{}\n", encoding="utf-8")

    with pytest.raises(DadTransportContractError, match="manifest count or hash"):
        validate_dad_transport_contract(root, check_git_index=False)
