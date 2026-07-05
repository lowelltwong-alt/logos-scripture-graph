from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t438_alignment_bridge_goal as validator


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / ".ai/control/t438_alignment_bridge_goal.yaml"


def test_t438_alignment_bridge_goal_validates_current_repo() -> None:
    data = validator.validate_t438_alignment_bridge_goal()

    assert data["goal_selection"]["primary_goal_option_id"] == "option_1_alignment_bridge"
    assert data["parallel_goal_option"]["option_id"] == "option_2_manuscript_custody_chain"
    assert data["authority"]["authorizes_translation_judgment"] is False


def test_t438_rejects_alignment_truth_authority() -> None:
    data = copy.deepcopy(yaml.safe_load(CONTROL.read_text(encoding="utf-8")))
    data["alignment_bridge_contract"]["candidate_row_policy"]["alignment_truth_authorized"] = True

    root = _minimal_repo(data)
    with pytest.raises(validator.T438AlignmentBridgeGoalError, match="alignment_truth_authorized"):
        validator.validate_t438_alignment_bridge_goal(root)


def test_t438_rejects_raw_archive_direct_consumption() -> None:
    data = copy.deepcopy(yaml.safe_load(CONTROL.read_text(encoding="utf-8")))
    data["alignment_bridge_contract"]["input_policy"]["raw_archive_direct_consumption_allowed"] = True

    root = _minimal_repo(data)
    with pytest.raises(validator.T438AlignmentBridgeGoalError, match="raw archive"):
        validator.validate_t438_alignment_bridge_goal(root)


def test_t438_rejects_missing_rust_leaf_stage() -> None:
    data = copy.deepcopy(yaml.safe_load(CONTROL.read_text(encoding="utf-8")))
    data["next_task_sequence"] = [
        item for item in data["next_task_sequence"] if item["task_id"] != "T441"
    ]

    root = _minimal_repo(data)
    with pytest.raises(validator.T438AlignmentBridgeGoalError, match="next_task_sequence"):
        validator.validate_t438_alignment_bridge_goal(root)


def _minimal_repo(control: dict) -> Path:
    import tempfile

    root = Path(tempfile.mkdtemp())
    (root / ".ai/control").mkdir(parents=True)
    (root / ".ai/tasks").mkdir(parents=True)
    (root / ".ai/handoffs/T438").mkdir(parents=True)
    (root / ".ai/context/agent_work/T438").mkdir(parents=True)
    (root / "docs/roadmap").mkdir(parents=True)
    (root / "scripts").mkdir(parents=True)

    (root / ".ai/control/t438_alignment_bridge_goal.yaml").write_text(
        yaml.safe_dump(control, sort_keys=False),
        encoding="utf-8",
    )
    substrate = {
        "pilot_lanes": [
            {
                "task_id": "T438",
                "rule": "T438 records the alignment bridge route and does not authorize production rows.",
            }
        ]
    }
    (root / ".ai/control/original_language_evidence_substrate.yaml").write_text(
        yaml.safe_dump(substrate),
        encoding="utf-8",
    )
    task = {
        "id": "T438",
        "authorization": {
            "records_goal_selection": True,
            "opens_production_candidate_roots": False,
            "creates_source_token_rows": False,
            "creates_alignment_rows": False,
            "authorizes_translation_judgment": False,
        },
        "rust_policy": {
            "rust_added_in_t438": False,
            "rust_preferred_for_future_leaf_tools": True,
        },
    }
    (root / ".ai/tasks/T438.task.yaml").write_text(yaml.safe_dump(task), encoding="utf-8")
    (root / ".ai/handoffs/T438/handoff.md").write_text("handoff\n", encoding="utf-8")
    (root / ".ai/context/agent_work/T438/dad_preflight.md").write_text(
        "Separate goal selection, parser semantics, and Rust acceleration.\n",
        encoding="utf-8",
    )
    (root / "docs/roadmap/T438_ALIGNMENT_BRIDGE_GOAL.md").write_text(
        "Greek/Hebrew-to-English alignment bridge. Manuscript custody-chain. "
        "Rust speed is not authority. Do not treat Strong's numbers as Greek/Hebrew source text.\n",
        encoding="utf-8",
    )
    (root / "docs/roadmap/T430_ORIGINAL_LANGUAGE_GOAL_OPTIONS.md").write_text("options\n", encoding="utf-8")
    (root / "scripts/validate_all.py").write_text(
        "validate_t438_alignment_bridge_goal.py\n",
        encoding="utf-8",
    )
    return root
