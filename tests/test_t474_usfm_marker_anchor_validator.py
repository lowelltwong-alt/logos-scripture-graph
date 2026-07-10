from __future__ import annotations

import json
import shutil
from pathlib import Path

import yaml

from scripts.validate_t474_usfm_marker_anchor_contract import (
    REQUIRED_FILES,
    ROOT,
    validate_t474_package,
)


def _read_yaml(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        text = parts[1] + "\n" + parts[2]
    return yaml.safe_load(text)


def _write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8", newline="\n")


def _copy_package(tmp_path: Path) -> Path:
    for rel in REQUIRED_FILES.values():
        source = ROOT / rel
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return tmp_path


def test_t474_package_validates_current_repo() -> None:
    assert validate_t474_package(ROOT) == []


def test_rejects_canonical_regeneration_authority(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / REQUIRED_FILES["task"]
    data = _read_yaml(path)
    data["authorization"]["regenerates_committed_canonical_data"] = True
    _write_yaml(path, data)
    assert "task.authorization.regenerates_committed_canonical_data must be false" in validate_t474_package(root)


def test_rejects_missing_owner_selection(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / REQUIRED_FILES["owner_packet"]
    data = _read_yaml(path)
    data["owner_selection"] = "pending"
    _write_yaml(path, data)
    assert "owner packet must select T473-ANCHOR-A" in validate_t474_package(root)


def test_rejects_semantic_pilot_bypass(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / REQUIRED_FILES["t473_control"]
    data = _read_yaml(path)
    data["execution_state"]["pilot_execution_allowed"] = True
    _write_yaml(path, data)
    assert "T473 semantic pilot must remain blocked" in validate_t474_package(root)


def test_rejects_qs_as_structural_line_marker(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / REQUIRED_FILES["importer"]
    text = path.read_text(encoding="utf-8")
    needle = '    "d",\n    "b",'
    assert needle in text
    path.write_text(text.replace(needle, '    "d",\n    "qs",\n    "b",'), encoding="utf-8", newline="\n")
    assert "inline qs must not remain a structural line marker" in validate_t474_package(root)


def test_rejects_required_anchor_fields_before_migration(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / REQUIRED_FILES["event_schema"]
    data = json.loads(path.read_text(encoding="utf-8"))
    data["required"].append("anchor_kind")
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    errors = validate_t474_package(root)
    assert any("anchor fields must remain optional in T474" in error for error in errors)


def test_rejects_missing_source_event_link(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / REQUIRED_FILES["boundary_schema"]
    data = json.loads(path.read_text(encoding="utf-8"))
    data["properties"].pop("source_event_id")
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    assert "boundary_schema missing source_event_id" in validate_t474_package(root)

def test_rejects_legacy_nonverse_sidecar_parser_reintroduction(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / REQUIRED_FILES["importer"]
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write("\n\ndef extract_nonverse_inline_sidecars():\n    pass\n")
    assert "legacy non-verse canonical sidecar parser must remain removed" in validate_t474_package(root)
