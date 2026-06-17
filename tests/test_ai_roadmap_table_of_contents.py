from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_main_toc_links_to_local_roadmap_toc() -> None:
    assert "docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md" in read(MAIN_TOC)


def test_local_roadmap_toc_links_back_to_main_toc() -> None:
    assert "AI_TABLE_OF_CONTENTS.md" in read(ROADMAP_TOC)


def test_local_roadmap_toc_exposes_t337a_actual_artifact_trail() -> None:
    toc = read(ROADMAP_TOC)

    assert ".ai/tasks/T337A.task.yaml" in toc
    assert ".ai/handoffs/T337A/handoff.md" in toc
    assert "eval/chunking_gold/review_packets/ps89_boundary_review.md" in toc


def test_local_roadmap_toc_exposes_t342_and_next_route() -> None:
    toc = read(ROADMAP_TOC)

    assert "docs/roadmap/T342_REVELATION_REVIEW_PACKET_CANDIDATE_SELECTION.md" in toc
    assert ".ai/tasks/T342.task.yaml" in toc
    assert ".ai/handoffs/T342/handoff.md" in toc
    assert "T343 - Revelation Review Packets and Gold Candidates" in toc
    assert "Rev.12.1-Rev.14.20" in toc
