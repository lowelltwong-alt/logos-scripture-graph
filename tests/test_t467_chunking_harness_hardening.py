from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from scripts.validate_t467_chunking_harness_hardening import ROOT, validate_t467_package


def test_t467_package_validates_current_repo() -> None:
    assert validate_t467_package(ROOT) == []


def _copy_package(tmp_path: Path) -> Path:
    files = [
        ".ai/tasks/T467.task.yaml",
        ".ai/control/t467_chunking_harness_hardening.yaml",
        ".ai/control/t423_literary_marker_quality_protocol.yaml",
        ".ai/control/multi_model_whole_bible_chunking_fork.yaml",
        ".ai/prompts/multi_model_whole_bible_chunking_marathon_prompt.md",
        ".ai/scratch/multi_model_bible_chunking/models/_TEMPLATE/model_manifest.yaml",
        ".ai/context/agent_work/T467/harness_hardening_notes.md",
        ".ai/handoffs/T467/handoff.md",
        "docs/roadmap/T467_CHUNKING_HARNESS_HARDENING.md",
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


def test_rejects_chunk_output_authority(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / ".ai/control/t467_chunking_harness_hardening.yaml"
    data = _read_yaml(path)
    data["authorization"]["authorizes_chunk_output"] = True
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    errors = validate_t467_package(root)
    assert any("authorizes_chunk_output must be false" in error for error in errors)


def test_rejects_missing_list_register_guard(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / ".ai/control/t467_chunking_harness_hardening.yaml"
    data = _read_yaml(path)
    data["hardening_rules"]["list_register_guard"]["affected_forms"].remove("tribal_allotment")
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    errors = validate_t467_package(root)
    assert any("list/register affected forms" in error for error in errors)


def test_rejects_missing_prompt_overlay(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / ".ai/prompts/multi_model_whole_bible_chunking_marathon_prompt.md"
    path.write_text(path.read_text(encoding="utf-8").replace("T467_literary_coherence_v1", "missing_overlay"), encoding="utf-8")

    errors = validate_t467_package(root)
    assert any("prompt missing required text 'T467_literary_coherence_v1'" in error for error in errors)
