from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
T337_DOC = ROOT / "docs" / "roadmap" / "T337_SELECT_ONE_PSALM_BEHAVIOR_CHANGE.md"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
PROJECT_STATUS = ROOT / ".ai" / "control" / "PROJECT_STATUS.md"
CURRENT_FOCUS = ROOT / ".ai" / "control" / "current_focus.yaml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_t337_records_no_authorized_behavior_change_target() -> None:
    doc = read(T337_DOC)

    assert "T337 is selection/planning/control-plane work only." in doc
    assert "No Psalm behavior-changing implementation target is selected." in doc
    assert "No reviewed-gold-supported Psalm behavior-change target is available" in doc
    assert "No chunking improvement claim or score movement is made." in doc
    assert "T338 is blocked" in doc


def test_t337_rejects_pending_and_preservation_only_evidence() -> None:
    doc = read(T337_DOC)

    assert "Psalm 78 parent/child structural split" in doc
    assert "Preserve current parent whole-Psalm" in doc
    assert "Psalm 105 whole-Psalm preservation" in doc
    assert "Psalm 106 whole-Psalm preservation" in doc
    assert "Psalm 89 royal lament" in doc
    assert "Pending human review only" in doc
    assert "Psalm 136 refrain litany" in doc
    assert "Characterization-only; output change not authorized" in doc
    assert "marker evidence without human boundary review" in doc


def test_t337_locks_protected_path_and_no_start_rules() -> None:
    doc = read(T337_DOC)
    combined = "\n".join([doc, read(PROJECT_STATUS), read(CURRENT_FOCUS)])

    assert "change chunking behavior" in doc
    assert "mutate `data/raw/**` or `data/canonical/**`" in doc
    assert "start T327G" in doc
    assert "start Revelation implementation" in doc
    assert "import source texts or boundary texts" in doc
    assert "do not start Revelation implementation, T327G, or boundary import" in combined


def test_t337_roadmap_state_completed_and_t342_next_after_t341() -> None:
    state = yaml.safe_load(read(ROADMAP_STATE))
    phase_4 = state["phases"]["phase_4"]
    tasks = {task["id"]: task for task in phase_4["tasks"]}
    future = {task["id"]: task for task in phase_4["future_sequence"]}

    assert tasks["T337"]["status"] == "complete"
    assert tasks["T337"]["required_handoff"] == ".ai/handoffs/T337/handoff.md"
    assert tasks["T338"]["status"] == "complete"
    assert tasks["T338"]["required_handoff"] == ".ai/handoffs/T338/handoff.md"
    assert tasks["T339"]["status"] == "complete"
    assert tasks["T339"]["required_handoff"] == ".ai/handoffs/T339/handoff.md"
    assert tasks["T340"]["status"] == "complete"
    assert tasks["T340"]["required_handoff"] == ".ai/handoffs/T340/handoff.md"
    assert tasks["T341"]["status"] == "complete"
    assert tasks["T341"]["required_handoff"] == ".ai/handoffs/T341/handoff.md"
    assert "T337" not in future
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
