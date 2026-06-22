from __future__ import annotations

from pathlib import Path

import pytest

from scripts.validate_chunking_lesson_index import (
    LessonIndexError,
    validate_changed_path_gate,
    validate_lesson_index,
)


ROOT = Path(__file__).resolve().parents[1]
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"


def test_chunking_lesson_index_validates_and_is_non_authorizing() -> None:
    data = validate_lesson_index(LESSON_INDEX)

    assert data["object_type"] == "chunking_lesson_index"
    assert data["trust_zone"] == "canonical"
    assert data["lifecycle_status"] == "active"
    assert data["authority"]["records_lessons"] is True
    assert data["authority"]["authorizes_chunk_output_change"] is False
    assert data["authority"]["authorizes_reviewed_gold_promotion"] is False
    assert data["authority"]["authorizes_route_behavior"] is False
    assert data["authority"]["authorizes_graph_edges"] is False
    assert data["authority"]["authorizes_retrieval_truth"] is False


def test_chunking_lesson_index_has_required_tags_and_use_when_routing() -> None:
    data = validate_lesson_index(LESSON_INDEX)
    by_id = {lesson["lesson_id"]: lesson for lesson in data["lessons"]}

    assert set(by_id) >= {f"LSN-{number:03d}" for number in range(1, 14)}
    assert "source-metadata" in by_id["LSN-001"]["tags"]
    assert "lessons-learned" in by_id["LSN-002"]["tags"]
    assert "ai-toc" in by_id["LSN-003"]["tags"]
    assert "original-language" in by_id["LSN-004"]["tags"]
    assert "orthodox-hermeneutic-firewall" in by_id["LSN-005"]["tags"]
    assert "textual-critical-policy" in by_id["LSN-006"]["tags"]
    assert "owner-projection" in by_id["LSN-007"]["tags"]
    assert "parent-first-pilot" in by_id["LSN-008"]["tags"]
    assert "graph" in by_id["LSN-009"]["tags"]
    assert "no-context-review" in by_id["LSN-010"]["tags"]
    assert "contextual-reading" in by_id["LSN-011"]["tags"]
    assert "historical-context" in by_id["LSN-011"]["tags"]
    assert "research-runway" in by_id["LSN-012"]["tags"]
    assert "authority-boundary" in by_id["LSN-012"]["tags"]
    assert "bible-wide-readiness" in by_id["LSN-013"]["tags"]
    assert "research-synthesis" in by_id["LSN-013"]["tags"]
    assert "human-decision-map" in by_id["LSN-013"]["tags"]
    assert "chunking-ready" in by_id["LSN-013"]["tags"]
    assert all(lesson["use_when"] for lesson in by_id.values())


def test_chunking_lesson_index_graph_references_known_lessons() -> None:
    data = validate_lesson_index(LESSON_INDEX)
    lesson_ids = {lesson["lesson_id"] for lesson in data["lessons"]}

    assert data["lesson_graph"]
    for edge in data["lesson_graph"]:
        assert edge["from"] in lesson_ids
        assert edge["to"] in lesson_ids
        assert edge["relation"] in {"governs_update_of", "constrains", "audits", "discovers"}


def test_lesson_changed_path_gate_requires_index_update() -> None:
    with pytest.raises(LessonIndexError, match="lesson index must be updated"):
        validate_changed_path_gate(
            changed_files=[".ai/control/chunking_agent_preflight.yaml"],
            index_updated=False,
        )

    validate_changed_path_gate(
        changed_files=[
            ".ai/control/chunking_agent_preflight.yaml",
            ".ai/control/chunking_lesson_index.yaml",
        ],
        index_updated=None,
    )
