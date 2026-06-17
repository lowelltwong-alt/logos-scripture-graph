from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "docs" / "roadmap" / "T341_REVELATION_HARD_BOOK_ATLAS.md"
AUDIT = ROOT / "docs" / "roadmap" / "T341_REVELATION_OBSERVED_BEHAVIOR_AUDIT.md"
TASK = ROOT / ".ai" / "tasks" / "T341.task.yaml"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
CURRENT_FOCUS = ROOT / ".ai" / "control" / "current_focus.yaml"
PROJECT_STATUS = ROOT / ".ai" / "control" / "PROJECT_STATUS.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def squish(text: str) -> str:
    return " ".join(text.split())


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(read(path))


def test_t341_docs_exist_and_are_non_authorizing() -> None:
    atlas = squish(read(ATLAS))
    audit = squish(read(AUDIT))
    combined = f"{atlas} {audit}"

    assert "T341 creates a Revelation hard-book atlas" in atlas
    assert "No protected output was regenerated" in audit
    assert "does not authorize Revelation implementation" in combined
    assert "does not implement Revelation chunking" in combined
    assert "No reviewed gold exists for Revelation behavior change" in combined
    assert "No route, skill, evaluator, leaderboard, scorecard, or generated-output behavior changed" in combined


def test_t341_blocks_boundary_import_t327g_and_global_rules() -> None:
    combined = squish("\n".join([read(ATLAS), read(AUDIT), read(TASK)]))

    required = [
        "boundary import",
        "boundary/apocryphal material",
        "T327G",
        "global apocalypse",
        "global apocalypse, prophecy, poetry, words-of-Jesus, discourse",
        "global rules",
        "whole-Bible improvement claims",
        "boundary/apocalyptic literature",
    ]
    for phrase in required:
        assert phrase in combined


def test_t341_requires_reviewed_gold_before_output_change() -> None:
    atlas = squish(read(ATLAS))
    audit = squish(read(AUDIT))

    assert "promote exact spans to reviewed gold by human decision" in atlas
    assert "set `implementation_allowed: true` and `output_change_authorized: true`" in atlas
    assert "`implementation_allowed: false`" in audit
    assert "`output_change_authorized: false`" in audit
    assert "`reviewed_gold_promoted: false`" in audit


def test_t341_risk_gate_map_has_required_categories() -> None:
    atlas = read(ATLAS)

    assert "RISK-GATE-001 question" in atlas
    for heading in [
        "Confirmed Risks",
        "Plausible Risks",
        "Unlikely But High-Impact Risks",
        "Watch-Later Conditions",
        "Tests Or Guards Needed",
        "Owner Decisions Needed",
    ]:
        assert heading in atlas


def test_t341_task_forbids_protected_paths_and_authorizations() -> None:
    task = load_yaml(TASK)
    forbidden = set(task["scope"]["forbidden_paths"])
    auth = task["authorization"]

    for path in [
        "data/raw/",
        "data/canonical/",
        "data/derived/",
        "pipelines/chunking/chunker.py",
        "pipelines/chunking/orchestrator.py",
        "pipelines/chunking/evaluate_chunks.py",
        "pipelines/chunking/skills/",
        "eval/chunking_runs/",
        "eval/LEADERBOARD.md",
    ]:
        assert path in forbidden

    assert auth["revelation_implementation_allowed"] is False
    assert auth["output_change_authorized"] is False
    assert auth["reviewed_gold_promoted"] is False
    assert auth["boundary_import_allowed"] is False
    assert auth["boundary_apocryphal_material_import_allowed"] is False
    assert auth["global_rule_allowed"] is False
    assert auth["t327g_allowed"] is False


def test_t341_status_points_next_to_review_packet_not_implementation() -> None:
    state = read(ROADMAP_STATE)
    focus = read(CURRENT_FOCUS)
    status = read(PROJECT_STATUS)
    combined = squish("\n".join([state, focus, status, read(ATLAS), read(AUDIT)]))

    assert "id: T341" in state
    assert "status: complete" in state
    assert "T342 Revelation review-packet candidate selection" in combined
    assert "T343" in combined
    assert "T344" in combined
    assert "do not start Revelation implementation" in combined
    assert "do not import boundary texts" in combined
