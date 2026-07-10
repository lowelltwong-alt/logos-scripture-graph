from __future__ import annotations

import json
import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator
from uuid import uuid4

import yaml

from scripts.validate_t472_model_panel_calibration_gate import REQUIRED_FILES, ROOT, validate_t472


def test_current_t472_calibration_validates() -> None:
    assert validate_t472(ROOT) == []


@contextmanager
def _copy_package() -> Iterator[Path]:
    root = ROOT / "build" / "test_tmp" / f"t472-calibration-{uuid4().hex}"
    root.mkdir(parents=True, exist_ok=False)
    try:
        for rel in REQUIRED_FILES.values():
            src = ROOT / rel
            dst = root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _yaml(path: Path) -> dict:
    docs = [doc for doc in yaml.safe_load_all(path.read_text(encoding="utf-8")) if isinstance(doc, dict)]
    merged = {}
    for doc in docs:
        merged.update(doc)
    return merged


def _write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_rejects_inflated_2john_pair_span() -> None:
    with _copy_package() as root:
        path = root / ".ai/context/agent_work/T472/corrected_legacy_19_docket.yaml"
        data = _yaml(path)
        row = next(item for item in data["rows"] if item["source_id"] == "DELTA-2John-001")
        row["actual_pair_span"] = "2John.1.1-2John.1.13"
        _write_yaml(path, data)
        assert any("actual pair span" in error for error in validate_t472(root, verify_frozen_sources=False))


def test_rejects_model_voting_eligibility() -> None:
    with _copy_package() as root:
        path = root / ".ai/context/agent_work/T472/model_panel_calibration.yaml"
        data = _yaml(path)
        row = next(item for item in data["models"] if item["model_id"] == "M1_cursor")
        row["eligible_for_confidence_or_majority"] = True
        _write_yaml(path, data)
        assert any("voting eligibility" in error for error in validate_t472(root, verify_frozen_sources=False))


def test_rejects_owner_ready_legacy_row() -> None:
    with _copy_package() as root:
        path = root / ".ai/context/agent_work/T472/corrected_legacy_19_docket.yaml"
        data = _yaml(path)
        data["owner_ready_count"] = 1
        _write_yaml(path, data)
        assert any("owner_ready_count" in error for error in validate_t472(root, verify_frozen_sources=False))


def test_rejects_classification_loss() -> None:
    with _copy_package() as root:
        path = root / ".ai/context/agent_work/T472/all_delta_mechanical_classification.jsonl"
        lines = path.read_text(encoding="utf-8").splitlines()
        path.write_text("\n".join(lines[:-1]) + "\n", encoding="utf-8")
        assert any("1048 rows" in error for error in validate_t472(root, verify_frozen_sources=False))


def test_rejects_dad_authority_leak() -> None:
    with _copy_package() as root:
        path = root / ".digital-asset/mail/outbox.jsonl"
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        row = next(item for item in rows if item["message_id"] == "msg-20260710-t472-model-panel-calibration-lessons")
        row["trust_zone"] = "canonical"
        path.write_text("\n".join(json.dumps(item) for item in rows) + "\n", encoding="utf-8")
        assert any("DAD lesson must remain candidate" in error for error in validate_t472(root, verify_frozen_sources=False))


def test_rejects_frozen_manifest_authorization() -> None:
    with _copy_package() as root:
        path = root / ".ai/context/agent_work/T472/frozen_artifact_manifest.yaml"
        data = _yaml(path)
        data["artifacts"][0]["mutation_allowed_by_T472"] = True
        _write_yaml(path, data)
        assert any("mutation must be forbidden" in error for error in validate_t472(root, verify_frozen_sources=False))

def test_rejects_later_focus_that_drops_t472_correction_surface() -> None:
    with _copy_package() as root:
        path = root / ".ai/control/current_focus.yaml"
        data = _yaml(path)
        data["current_task"] = "T473"
        data.pop("t472_correction_overlay", None)
        _write_yaml(path, data)
        errors = validate_t472(root, verify_frozen_sources=False)
        assert any("must retain T472 task, control, and correction overlay" in error for error in errors)
