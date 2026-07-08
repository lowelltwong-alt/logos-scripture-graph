from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from scripts.validate_t468_owner_faithful_chunking_policy import ROOT, validate_t468_package


def test_t468_package_validates_current_repo() -> None:
    assert validate_t468_package(ROOT) == []


def _copy_package(tmp_path: Path) -> Path:
    files = [
        ".ai/tasks/T468.task.yaml",
        ".ai/control/t468_owner_faithful_chunking_policy.yaml",
        ".ai/control/chunking_theological_decision_register.yaml",
        ".ai/control/chunking_lesson_index.yaml",
        ".ai/control/PROJECT_STATUS.md",
        ".ai/control/current_focus.yaml",
        ".ai/handoffs/T468/handoff.md",
        "docs/roadmap/T468_OWNER_FAITHFUL_CHUNKING_POLICY.md",
    ]
    for rel in files:
        src = ROOT / rel
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return tmp_path


def _read_yaml(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        text = parts[1] + "\n" + parts[2]
    return yaml.safe_load(text)


def test_rejects_reviewed_gold_authority(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / ".ai/control/t468_owner_faithful_chunking_policy.yaml"
    data = _read_yaml(path)
    data["authorization"]["authorizes_reviewed_gold"] = True
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    errors = validate_t468_package(root)
    assert any("authorizes_reviewed_gold must be false" in error for error in errors)


def test_rejects_missing_hard_exception(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / ".ai/control/t468_owner_faithful_chunking_policy.yaml"
    data = _read_yaml(path)
    data["hard_exceptions_not_downgraded"].remove("mark_16_longer_ending")
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    errors = validate_t468_package(root)
    assert any("hard exceptions list" in error for error in errors)


def test_rejects_unfaithful_route_decision(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / ".ai/control/t468_owner_faithful_chunking_policy.yaml"
    data = _read_yaml(path)
    data["approved_decisions"][2]["selected_route"] = "retrieval_convenience_route"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    errors = validate_t468_package(root)
    assert any("selected_route must be faithful_route" in error for error in errors)
