from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_ai_agnostic_rust_subagents import (  # noqa: E402
    RustSubagentCharterError,
    validate_ai_agnostic_rust_subagents,
)

FILES_TO_COPY = [
    ".ai/control/ai_agnostic_rust_subagent_charter.yaml",
    ".ai/control/multi_agent_review_cadence.yaml",
    "config/agents/agent_roles.yaml",
    "config/agents/model_routing.yaml",
    "tests/fixtures/dad/candidate_messages.jsonl",
    ".digital-asset/context-map.json",
    ".digital-asset/lessons/t458_ai_agnostic_rust_subagent_charter.yaml",
    "scripts/validate_all.py",
    "scripts/validate_ai_agnostic_rust_subagents.py",
]


def _copy_fixture_root(tmp_path: Path) -> Path:
    for rel in FILES_TO_COPY:
        src = ROOT / rel
        dest = tmp_path / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    return tmp_path


def _read_yaml(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            data = yaml.safe_load(parts[1])
            data.update(yaml.safe_load(parts[2]))
            return data
    return yaml.safe_load(text)


def _write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_current_ai_agnostic_rust_subagent_charter_passes() -> None:
    validate_ai_agnostic_rust_subagents(ROOT)


def test_validator_rejects_missing_required_role(tmp_path: Path) -> None:
    root = _copy_fixture_root(tmp_path)
    path = root / ".ai/control/ai_agnostic_rust_subagent_charter.yaml"
    data = _read_yaml(path)
    del data["roles"]["rust_qa_tester"]
    _write_yaml(path, data)

    with pytest.raises(RustSubagentCharterError, match="missing roles"):
        validate_ai_agnostic_rust_subagents(root)


def test_validator_rejects_vendor_specific_role_binding(tmp_path: Path) -> None:
    root = _copy_fixture_root(tmp_path)
    path = root / "config/agents/agent_roles.yaml"
    data = _read_yaml(path)
    data["roles"]["rust_engineer"]["preferred_model"] = "claude-opus-4.8"
    _write_yaml(path, data)

    with pytest.raises(RustSubagentCharterError, match="vendor/model-specific"):
        validate_ai_agnostic_rust_subagents(root)


def test_validator_rejects_missing_dad_outbox_row(tmp_path: Path) -> None:
    root = _copy_fixture_root(tmp_path)
    path = root / "tests/fixtures/dad/candidate_messages.jsonl"
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    rows = [
        row
        for row in rows
        if row.get("message_id") != "msg-20260706-t458-ai-agnostic-rust-subagent-charter"
    ]
    path.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")

    with pytest.raises(RustSubagentCharterError, match="outbox row missing"):
        validate_ai_agnostic_rust_subagents(root)


def test_validator_rejects_validate_all_not_wired(tmp_path: Path) -> None:
    root = _copy_fixture_root(tmp_path)
    path = root / "scripts/validate_all.py"
    text = path.read_text(encoding="utf-8").replace("validate_ai_agnostic_rust_subagents.py", "")
    path.write_text(text, encoding="utf-8")

    with pytest.raises(RustSubagentCharterError, match="validate_all.py must include"):
        validate_ai_agnostic_rust_subagents(root)
