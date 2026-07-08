from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from scripts.validate_t470_transparent_chunking_research_evidence_rubric import ROOT, validate_t470_package


def test_t470_package_validates_current_repo() -> None:
    assert validate_t470_package(ROOT) == []


def _copy_package(tmp_path: Path) -> Path:
    files = [
        ".ai/tasks/T470.task.yaml",
        ".ai/control/t470_transparent_chunking_research_evidence_rubric.yaml",
        ".ai/control/chunking_theological_decision_register.yaml",
        ".ai/control/chunking_lesson_index.yaml",
        ".ai/control/PROJECT_STATUS.md",
        ".ai/control/current_focus.yaml",
        ".ai/handoffs/T470/handoff.md",
        ".ai/context/agent_work/T470/research_source_notes.md",
        "docs/roadmap/T470_TRANSPARENT_CHUNKING_RESEARCH_EVIDENCE_RUBRIC.md",
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
    path = root / ".ai/control/t470_transparent_chunking_research_evidence_rubric.yaml"
    data = _read_yaml(path)
    data["authorization"]["authorizes_reviewed_gold"] = True
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    errors = validate_t470_package(root)
    assert any("authorizes_reviewed_gold must be false" in error for error in errors)


def test_rejects_missing_source_url(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / ".ai/control/t470_transparent_chunking_research_evidence_rubric.yaml"
    data = _read_yaml(path)
    data["well_supported_claims"][0]["source_refs"][0]["url"] = ""
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    errors = validate_t470_package(root)
    assert any("source ref URL must start with http" in error for error in errors)


def test_rejects_missing_mark16_debated_claim(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / ".ai/control/t470_transparent_chunking_research_evidence_rubric.yaml"
    data = _read_yaml(path)
    data["debated_claims"] = [claim for claim in data["debated_claims"] if claim["claim_id"] != "T470-DB-001"]
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    errors = validate_t470_package(root)
    assert any("missing Mark 16 debated claim" in error for error in errors)


def test_rejects_missing_windowdiff_recommendation(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / ".ai/control/t470_transparent_chunking_research_evidence_rubric.yaml"
    data = _read_yaml(path)
    for recommendation in data["t470_recommendations"]:
        recommendation["recommendation"] = recommendation["recommendation"].replace("WindowDiff", "boundary-distance")
        recommendation["recommendation"] = recommendation["recommendation"].replace("near-boundary", "boundary-distance")
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    errors = validate_t470_package(root)
    assert any("WindowDiff or near-boundary" in error for error in errors)
