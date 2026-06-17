from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "roadmap" / "T342_REVELATION_REVIEW_PACKET_CANDIDATE_SELECTION.md"
TASK = ROOT / ".ai" / "tasks" / "T342.task.yaml"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> dict:
    text = read(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    return yaml.safe_load(text)


def test_t342_selects_rev12_14_only() -> None:
    doc = read(DOC)

    assert "T342 selects exactly one Revelation review-packet target" in doc
    assert "Rev.12-Rev.14" in doc
    assert "Rev.12.1-Rev.14.20" in doc
    assert "rev12_14_symbolic_scenes" in doc
    assert "T343 should create a pending, non-authorizing review packet" in doc


def test_t342_is_non_authorizing() -> None:
    doc = read(DOC)
    task = load_yaml(TASK)
    auth = task["authorization"]

    assert "does not create a review packet" in doc
    assert "does not authorize" in doc
    assert auth["revelation_implementation_allowed"] is False
    assert auth["output_change_authorized"] is False
    assert auth["reviewed_gold_promoted"] is False
    assert auth["review_packet_created"] is False
    assert auth["boundary_import_allowed"] is False
    assert auth["boundary_apocryphal_material_import_allowed"] is False
    assert auth["global_rule_allowed"] is False
    assert auth["t327g_allowed"] is False


def test_t342_and_t343_remain_complete_while_live_route_points_to_t351() -> None:
    state = load_yaml(ROADMAP_STATE)
    readiness = load_yaml(READINESS)
    tasks = {task["id"]: task for task in state["phases"]["phase_4"]["tasks"]}
    future = {task["id"]: task for task in state["phases"]["phase_4"]["future_sequence"]}

    assert tasks["T342"]["status"] == "complete"
    assert tasks["T342"]["required_handoff"] == ".ai/handoffs/T342/handoff.md"
    assert "T342" not in future
    assert tasks["T343"]["status"] == "complete"
    assert tasks["T343"]["required_handoff"] == ".ai/handoffs/T343/handoff.md"
    assert "T343" not in future
    assert tasks["T344"]["status"] == "complete"
    assert tasks["T344"]["required_handoff"] == ".ai/handoffs/T344/handoff.md"
    assert "T344" not in future
    assert tasks["T351"]["status"] == "complete"
    assert tasks["T351"]["required_handoff"] == ".ai/handoffs/T351/handoff.md"
    assert tasks["T352"]["status"] == "in_progress"
    assert tasks["T352"]["required_handoff"] == ".ai/handoffs/T352/handoff.md"
    assert readiness["next_route"]["task_id"] == "T352"
    assert readiness["next_route"]["selected_option"] == "REV-T344-E"
    assert readiness["next_route"]["output_change_authorized"] is False
    assert readiness["next_route"]["implementation_authorized"] is False


def test_t342_risk_gate_categories_present() -> None:
    doc = read(DOC)

    for heading in [
        "Confirmed Risks",
        "Plausible Risks",
        "Unlikely But High-Impact Risks",
        "Watch-Later Conditions",
        "Tests Or Guards Needed",
        "Owner Decisions Needed",
    ]:
        assert heading in doc
