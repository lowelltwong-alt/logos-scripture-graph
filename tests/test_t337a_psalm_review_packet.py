from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PS89 = ROOT / "eval" / "chunking_gold" / "review_packets" / "ps89_boundary_review.md"
PS136 = ROOT / "eval" / "chunking_gold" / "review_packets" / "ps136_boundary_review.md"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
CURRENT_FOCUS = ROOT / ".ai" / "control" / "current_focus.yaml"
PROJECT_STATUS = ROOT / ".ai" / "control" / "PROJECT_STATUS.md"


EXPECTED_PS89_SPANS = [
    "`Ps.89.1-Ps.89.4`",
    "`Ps.89.5-Ps.89.18`",
    "`Ps.89.19-Ps.89.37`",
    "`Ps.89.38-Ps.89.45`",
    "`Ps.89.46-Ps.89.48`",
    "`Ps.89.49-Ps.89.52`",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_t337a_selected_one_psalm_target_and_t337b_preserves_scope() -> None:
    ps89 = read(PS89)
    ps136 = read(PS136)

    assert "T337A selection: selected as the single Psalm target for human review" in ps89
    assert "T337A selection" not in ps136
    assert "Psalm 136 remains pending and non-authorizing" in ps89
    assert "T337B records the owner's Option C" in ps89
    assert "does not start T338" in ps89 or "T338 has not started" in ps89


def test_t337b_ps89_packet_has_exact_approved_spans_and_decision_box() -> None:
    ps89 = read(PS89)

    for span in EXPECTED_PS89_SPANS:
        assert span in ps89

    assert "human_review_decision:" in ps89
    assert "decision: approved_with_scope_note" in ps89
    assert "implementation_allowed: true" in ps89
    assert "output_change_authorized: true" in ps89
    assert "reviewed_gold_promoted: true" in ps89
    assert "T338 has not started" in ps89


def test_t337b_packet_preserves_guardrails_while_authorizing_ps89_only() -> None:
    ps89 = read(PS89)

    assert "Psalm 89 only" in ps89
    assert "No fresh chunk regeneration was performed for T337A." in ps89
    assert "Marker evidence is evidence only." in ps89
    assert "chunk output regeneration" in ps89
    assert "raw or canonical data mutation" in ps89
    assert "source text or boundary text imports" in ps89
    assert "T327G" in ps89
    assert "Revelation implementation" in ps89
    assert "chunking improvement claims" in ps89


def test_t337a_roadmap_state_and_focus_advance_after_t340_hold() -> None:
    state = yaml.safe_load(read(ROADMAP_STATE))
    phase_4 = state["phases"]["phase_4"]
    tasks = {task["id"]: task for task in phase_4["tasks"]}
    future = {task["id"]: task for task in phase_4["future_sequence"]}
    combined = "\n".join([read(CURRENT_FOCUS), read(PROJECT_STATUS)])

    assert tasks["T337A"]["status"] == "complete"
    assert tasks["T337A"]["required_handoff"] == ".ai/handoffs/T337A/handoff.md"
    assert tasks["T337B"]["status"] == "complete"
    assert tasks["T337B"]["required_handoff"] == ".ai/handoffs/T337B/handoff.md"
    assert tasks["T338"]["status"] == "complete"
    assert tasks["T338"]["required_handoff"] == ".ai/handoffs/T338/handoff.md"
    assert tasks["T339"]["status"] == "complete"
    assert tasks["T339"]["required_handoff"] == ".ai/handoffs/T339/handoff.md"
    assert tasks["T340"]["status"] == "complete"
    assert tasks["T340"]["required_handoff"] == ".ai/handoffs/T340/handoff.md"
    assert "T338" not in future
    assert "T339" not in future
    assert "T340" not in future
    assert future["T341"]["status"] == "planned"
    assert "T340 - Psalm candidate promotion decision recorded as hold" in combined
