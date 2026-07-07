from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from scripts.validate_t465_multi_model_reconciliation_gate import (
    EXPECTED_CANDIDATE_IDS,
    ROOT,
    validate_t465_package,
)


def test_t465_package_validates_current_repo() -> None:
    assert validate_t465_package(ROOT) == []


def _copy_minimal_package(tmp_path: Path) -> Path:
    files = [
        ".ai/tasks/T465.task.yaml",
        ".ai/control/t465_multi_model_reconciliation_gate.yaml",
        "docs/roadmap/T465_MULTI_MODEL_CHUNKING_RECONCILIATION_GATE.md",
        ".ai/handoffs/T465/handoff.md",
        ".ai/context/agent_work/T465/harness_triage.md",
        ".ai/context/agent_work/T465/mark16_specialist_packet.md",
        ".ai/context/agent_work/T465/owner_candidate_docket.yaml",
        ".ai/prompts/t465_mark16_frontier_specialist_review_prompt.md",
        ".ai/scratch/multi_model_bible_chunking/comparison/owner_decision_docket.yaml",
        ".ai/scratch/multi_model_bible_chunking/comparison/frontier_review_queue.jsonl",
    ]
    for rel in files:
        src = ROOT / rel
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return tmp_path


def _load_yaml_without_markers(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8").replace("---\n", "", 2))


def test_validator_rejects_output_authority(tmp_path: Path) -> None:
    root = _copy_minimal_package(tmp_path)
    path = root / ".ai/control/t465_multi_model_reconciliation_gate.yaml"
    data = _load_yaml_without_markers(path)
    data["authorization"]["authorizes_chunk_output"] = True
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    errors = validate_t465_package(root)
    assert any("authorizes_chunk_output must be false" in error for error in errors)


def test_validator_rejects_missing_mark16_layout_terms(tmp_path: Path) -> None:
    root = _copy_minimal_package(tmp_path)
    path = root / ".ai/context/agent_work/T465/mark16_specialist_packet.md"
    text = path.read_text(encoding="utf-8").replace("letters-per-column", "column metric")
    path.write_text(text, encoding="utf-8")

    errors = validate_t465_package(root)
    assert any("letters-per-column" in error for error in errors)


def test_validator_rejects_docket_id_drift(tmp_path: Path) -> None:
    root = _copy_minimal_package(tmp_path)
    path = root / ".ai/context/agent_work/T465/owner_candidate_docket.yaml"
    data = _load_yaml_without_markers(path)
    data["candidates"][0]["source_id"] = "DELTA-FAKE-001"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    errors = validate_t465_package(root)
    assert any("candidate IDs mismatch" in error for error in errors)
    assert "DELTA-FAKE-001" not in EXPECTED_CANDIDATE_IDS
