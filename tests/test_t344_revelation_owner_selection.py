from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "roadmap" / "T344_REVELATION_OWNER_SELECTION_DOCKET.md"
TASK = ROOT / ".ai" / "tasks" / "T344.task.yaml"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> dict:
    text = read(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    return yaml.safe_load(text)


def test_t344_docket_lists_owner_options_without_selecting() -> None:
    doc = read(DOC)

    assert "owner_selection_status: pending" in doc
    assert "Rev.12.1-Rev.14.20" in doc
    for option in ["REV-T344-A", "REV-T344-B", "REV-T344-C", "REV-T344-D", "REV-T344-E"]:
        assert option in doc
    assert "Only one option may be selected." in doc
    assert "These spans are not approved unless the owner selects `REV-T344-C`." in doc


def test_t344_is_non_authorizing_until_owner_selection() -> None:
    doc = read(DOC)
    task = load_yaml(TASK)
    auth = task["authorization"]

    assert auth["owner_selection_required"] is True
    assert auth["owner_selection_status"] == "pending"
    assert auth["selected_option"] == "pending"
    assert auth["revelation_implementation_allowed"] is False
    assert auth["output_change_authorized"] is False
    assert auth["reviewed_gold_promoted"] is False
    assert auth["graph_edge_generation_allowed"] is False
    assert auth["embedding_or_vector_work_allowed"] is False
    assert "This docket does not authorize:" in doc
    assert "reviewed-gold promotion" in doc
    assert "generated chunk regeneration" in doc


def test_t344_preserves_revelation_hermeneutic_neutrality() -> None:
    doc = read(DOC)

    for phrase in [
        "preserve orthodox interpretive possibilities",
        "linear or non-linear chronology",
        "premillennial",
        "amillennial",
        "postmillennial",
        "preterist",
        "historicist",
        "futurist",
        "idealist",
        "symbolic identities",
        "Daniel or other cross-references",
    ]:
        assert phrase in doc


def test_t344_updates_readiness_and_decision_register() -> None:
    readiness = load_yaml(READINESS)
    register = read(REGISTER)
    by_lane = {lane["lane_id"]: lane for lane in readiness["lane_sequence"]}
    target = by_lane["revelation_apocalyptic"]["selected_review_target"]

    assert target["owner_selection_status"] == "pending"
    assert target["selected_option"] == "pending"
    assert target["owner_selection_docket"] == "docs/roadmap/T344_REVELATION_OWNER_SELECTION_DOCKET.md"
    assert readiness["next_route"]["task_id"] == "T344"
    assert readiness["next_route"]["owner_selection_status"] == "pending"
    assert readiness["next_route"]["implementation_authorized"] is False
    assert readiness["next_route"]["output_change_authorized"] is False
    assert "CD-016" in register
    assert "Revelation owner selection is required before reviewed gold or implementation" in register


def test_t344_moves_from_future_sequence_to_active_task() -> None:
    state = load_yaml(ROADMAP_STATE)
    phase_4 = state["phases"]["phase_4"]
    tasks = {task["id"]: task for task in phase_4["tasks"]}
    future = {task["id"]: task for task in phase_4["future_sequence"]}

    assert tasks["T344"]["status"] == "in_progress"
    assert tasks["T344"]["required_handoff"] == ".ai/handoffs/T344/handoff.md"
    assert tasks["T344"]["owner_selection_status"] == "pending"
    assert tasks["T344"]["output_change_authorized"] is False
    assert "T344" not in future
    assert future["T345"]["status"] == "planned"
