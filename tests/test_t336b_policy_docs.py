from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "methodology" / "LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md"
LESSONS = ROOT / "docs" / "methodology" / "WORKFLOW_LESSONS.md"
REVIEW = ROOT / "docs" / "methodology" / "UNINTENDED_CONSEQUENCE_REVIEW.md"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
T336_ROADMAP = ROOT / "docs" / "roadmap" / "T336_OPTIMIZED_WHOLE_BIBLE_CHUNKING_ROADMAP.md"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"

REQUIRED_QUESTION = (
    "What could this change accidentally authorize, weaken, contaminate, overfit, globalize, "
    "or make harder to reverse?"
)

REQUIRED_OUTPUTS = [
    "confirmed risks",
    "plausible risks",
    "unlikely but high-impact risks",
    "watch-later conditions",
    "tests or guards needed",
    "owner decisions needed",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def squish(text: str) -> str:
    return " ".join(text.split())


def test_unintended_consequence_review_gate_is_registered() -> None:
    registry = read(REGISTRY)
    lesson = read(LESSONS)
    review = read(REVIEW)

    assert "RISK-GATE-001" in registry
    assert "High-Leverage Changes Require Unintended-Consequence Review" in registry
    assert "WORKFLOW-LESSON-002" in lesson
    assert "High-Leverage Changes Need an Unintended-Consequence Map" in lesson
    assert REVIEW.exists()

    for text in [registry, lesson, review]:
        assert REQUIRED_QUESTION in text
        for category in REQUIRED_OUTPUTS:
            assert category in text


def test_unintended_consequence_review_is_discoverable() -> None:
    front = read(FRONT_DOOR)
    toc = read(TOC)
    assert "docs/methodology/UNINTENDED_CONSEQUENCE_REVIEW.md" in front
    assert "docs/methodology/UNINTENDED_CONSEQUENCE_REVIEW.md" in toc
    assert "RISK-GATE-001" in read(REGISTRY)


def test_t336_bible_first_hardening_claims_remain_locked() -> None:
    front = read(FRONT_DOOR)
    registry = read(REGISTRY)
    roadmap = read(T336_ROADMAP)
    state = read(ROADMAP_STATE)

    combined = "\n".join([front, registry, roadmap])
    front_flat = squish(front)

    assert "canonical 66-book Bible" in combined
    assert "Revelation is a future hard-book atlas/review-packet lane" in front_flat
    assert "Revelation implementation must wait until reviewed gold exists" in front_flat
    assert "must not leak globally" in combined
    assert "single shared cross-corpus optimization objective" in combined
    assert "Non-Bible training/eval cases must not tune canonical Bible behavior" in combined
    assert "No boundary import" in roadmap
    assert "No T327G" in roadmap
    assert "T337" in state and "status: planned" in state
    assert "T341" in state and "output_change_authorized: false" in state
