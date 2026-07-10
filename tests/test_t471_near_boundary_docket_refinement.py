from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from scripts.validate_t471_near_boundary_docket_refinement import ROOT, validate_t471_package


def test_t471_package_validates_current_repo() -> None:
    assert validate_t471_package(ROOT) == []


def _copy_package(tmp_path: Path) -> Path:
    files = [
        ".ai/tasks/T471.task.yaml",
        ".ai/control/t471_near_boundary_docket_refinement.yaml",
        ".ai/control/chunking_theological_decision_register.yaml",
        ".ai/control/chunking_lesson_index.yaml",
        ".ai/control/PROJECT_STATUS.md",
        ".ai/control/current_focus.yaml",
        ".ai/handoffs/T471/handoff.md",
        "docs/roadmap/T471_NEAR_BOUNDARY_DOCKET_REFINEMENT.md",
        "scripts/build_t471_near_boundary_docket_refinement.py",
        ".ai/context/agent_work/T471/near_boundary_delta_refinement.jsonl",
        ".ai/context/agent_work/T471/owner_candidate_support_debate_docket.yaml",
        ".ai/context/agent_work/T471/refinement_summary.md",
        ".ai/scratch/multi_model_bible_chunking/comparison/disagreement_delta.jsonl",
        ".ai/context/agent_work/T465/owner_candidate_docket.yaml",
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
    path = root / ".ai/control/t471_near_boundary_docket_refinement.yaml"
    data = _read_yaml(path)
    data["authorization"]["authorizes_reviewed_gold"] = True
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    errors = validate_t471_package(root)
    assert any("authorizes_reviewed_gold must be false" in error for error in errors)


def test_rejects_missing_delta_refinement_row(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / ".ai/context/agent_work/T471/near_boundary_delta_refinement.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(lines[:-1]) + "\n", encoding="utf-8")

    errors = validate_t471_package(root)
    assert any("row count must match" in error for error in errors)


def test_rejects_missing_candidate_source_refs(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / ".ai/context/agent_work/T471/owner_candidate_support_debate_docket.yaml"
    data = _read_yaml(path)
    data["candidates"][0]["t470_support_debate_table"][0]["source_refs"] = []
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    errors = validate_t471_package(root)
    assert any("source_refs must be non-empty" in error for error in errors)


def test_rejects_wrong_first_t472_candidate(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / ".ai/context/agent_work/T471/owner_candidate_support_debate_docket.yaml"
    data = _read_yaml(path)
    data["recommended_first_t472_candidate"]["source_id"] = "DELTA-1Chr-012"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    errors = validate_t471_package(root)
    assert any("recommended first T472 candidate" in error for error in errors)
