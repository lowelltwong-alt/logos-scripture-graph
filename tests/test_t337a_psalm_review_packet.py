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


def test_t337a_roadmap_state_and_focus_advance_after_t341_atlas() -> None:
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
    assert tasks["T341"]["status"] == "complete"
    assert tasks["T341"]["required_handoff"] == ".ai/handoffs/T341/handoff.md"
    assert "T338" not in future
    assert "T339" not in future
    assert "T340" not in future
    assert "T341" not in future
    assert tasks["T342"]["status"] == "complete"
    assert tasks["T342"]["required_handoff"] == ".ai/handoffs/T342/handoff.md"
    assert "T342" not in future
    assert tasks["T343"]["status"] == "complete"
    assert tasks["T343"]["required_handoff"] == ".ai/handoffs/T343/handoff.md"
    assert "T343" not in future
    assert tasks["T344"]["status"] == "complete"
    assert tasks["T344"]["title"] == "Select One Revelation Behavior Target"
    assert tasks["T344"]["required_handoff"] == ".ai/handoffs/T344/handoff.md"
    assert "T344" not in future
    assert tasks["T351"]["status"] == "complete"
    assert tasks["T351"]["title"] == "Bible-Wide Chunking Research Triage Atlas"
    assert tasks["T351"]["required_handoff"] == ".ai/handoffs/T351/handoff.md"
    assert tasks["T352"]["status"] == "complete"
    assert tasks["T352"]["title"] == "Epistle Argument Review Packets"
    assert tasks["T352"]["required_handoff"] == ".ai/handoffs/T352/handoff.md"
    assert tasks["T353"]["status"] == "complete"
    assert tasks["T353"]["title"] == "Divine Capitalization Inventory Harness"
    assert tasks["T353"]["required_handoff"] == ".ai/handoffs/T353/handoff.md"
    assert tasks["T354"]["status"] == "complete"
    assert tasks["T354"]["title"] == "WJ Marker Inventory Harness"
    assert tasks["T354"]["required_handoff"] == ".ai/handoffs/T354/handoff.md"
    assert tasks["T355"]["status"] == "complete"
    assert tasks["T355"]["title"] == "WJ Speaker/Discourse Policy And Target Selection"
    assert tasks["T355"]["required_handoff"] == ".ai/handoffs/T355/handoff.md"
    assert tasks["T356"]["status"] == "complete"
    assert tasks["T356"]["title"] == "John 3 WJ Owner Review Docket"
    assert tasks["T356"]["required_handoff"] == ".ai/handoffs/T356/handoff.md"
    assert tasks["T358"]["status"] == "complete"
    assert tasks["T358"]["title"] == "Bible-Wide Chunking Research Registry"
    assert tasks["T358"]["required_handoff"] == ".ai/handoffs/T358/handoff.md"
    assert tasks["T359"]["status"] == "complete"
    assert tasks["T359"]["title"] == "Source Metadata Research Atlas"
    assert tasks["T359"]["required_handoff"] == ".ai/handoffs/T359/handoff.md"
    assert tasks["T360"]["status"] == "complete"
    assert tasks["T360"]["title"] == "Apocalyptic Prophetic Intertext Dossier Queue"
    assert tasks["T360"]["required_handoff"] == ".ai/handoffs/T360/handoff.md"
    assert tasks["T361"]["status"] == "complete"
    assert tasks["T361"]["title"] == "Epistle Argument Theological Issue Dossier Queue"
    assert tasks["T361"]["required_handoff"] == ".ai/handoffs/T361/handoff.md"
    assert tasks["T362"]["status"] == "complete"
    assert tasks["T362"]["title"] == "Gospel WJ Discourse Dossier Queue"
    assert tasks["T362"]["required_handoff"] == ".ai/handoffs/T362/handoff.md"
    assert tasks["T363"]["status"] == "complete"
    assert tasks["T363"]["title"] == "Narrative Legal Covenant Dossier Queue"
    assert tasks["T363"]["required_handoff"] == ".ai/handoffs/T363/handoff.md"
    assert tasks["T364"]["status"] == "complete"
    assert tasks["T364"]["title"] == "Wisdom Dialogue Poetry Dossier Queue"
    assert tasks["T364"]["required_handoff"] == ".ai/handoffs/T364/handoff.md"
    assert tasks["T365"]["status"] == "complete"
    assert tasks["T365"]["title"] == "Prophetic Oracle Vision Dossier Queue"
    assert tasks["T365"]["required_handoff"] == ".ai/handoffs/T365/handoff.md"
    assert tasks["T366"]["status"] == "complete"
    assert tasks["T366"]["title"] == "Textual Variant Source Tradition Dossier Queue"
    assert tasks["T366"]["required_handoff"] == ".ai/handoffs/T366/handoff.md"
    # The control plane has advanced past the T341 atlas to a later completed task; T341
    # remains recorded complete above, and the active focus is no longer the atlas itself.
    # (Asserted robustly so routine post-T341 task advancement does not require editing this test.)
    assert "current_task: T341" not in combined
