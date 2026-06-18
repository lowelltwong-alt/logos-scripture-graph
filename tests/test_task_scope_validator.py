from __future__ import annotations

from pathlib import Path

import pytest

from scripts import validate_task_scope as validator


ROOT = Path(__file__).resolve().parents[1]
T344_TASK = ROOT / ".ai" / "tasks" / "T344.task.yaml"
T351_TASK = ROOT / ".ai" / "tasks" / "T351.task.yaml"
T353_TASK = ROOT / ".ai" / "tasks" / "T353.task.yaml"
T354_TASK = ROOT / ".ai" / "tasks" / "T354.task.yaml"
T355_TASK = ROOT / ".ai" / "tasks" / "T355.task.yaml"
T352_TASK = ROOT / ".ai" / "tasks" / "T352.task.yaml"


def test_t344_scope_accepts_harn_001_surfaces() -> None:
    result = validator.validate_task_scope(
        task_file=T344_TASK,
        changed_files=[
            "scripts/validate_task_scope.py",
            "tests/test_task_scope_validator.py",
            "scripts/validate_all.py",
            ".github/workflows/validate.yml",
            ".ai/control/harness_upgrade_roadmap.yaml",
            ".ai/tasks/T344.task.yaml",
            ".ai/handoffs/T344/handoff.md",
            ".ai/control/PROJECT_STATUS.md",
            ".ai/control/current_focus.yaml",
            ".ai/control/roadmap_events.jsonl",
            ".ai/control/handoff_ledger.jsonl",
            "AI_FRONT_DOOR.md",
            "AI_TABLE_OF_CONTENTS.md",
        ],
    )

    assert result["task_file"] == ".ai/tasks/T344.task.yaml"
    assert ".github/workflows/validate.yml" in result["protected_changed"]


def test_scope_rejects_forbidden_raw_or_chunking_paths() -> None:
    with pytest.raises(validator.TaskScopeError, match="forbids changed path"):
        validator.validate_task_scope(
            task_file=T344_TASK,
            changed_files=["data/raw/bible/eng-web/file.usfm"],
        )

    with pytest.raises(validator.TaskScopeError, match="forbids changed path"):
        validator.validate_task_scope(
            task_file=T344_TASK,
            changed_files=["pipelines/chunking/chunker.py"],
        )


def test_t351_scope_accepts_bible_wide_triage_surfaces() -> None:
    result = validator.validate_task_scope(
        task_file=T351_TASK,
        changed_files=[
            ".ai/control/bible_chunking_research_triage_map.yaml",
            "docs/roadmap/T351_BIBLE_WIDE_CHUNKING_RESEARCH_TRIAGE_ATLAS.md",
            "scripts/validate_bible_chunking_research_triage.py",
            "tests/test_t351_bible_wide_research_triage.py",
            ".ai/tasks/T344R.task.yaml",
            ".ai/handoffs/T344R/handoff.md",
            ".ai/tasks/T351.task.yaml",
            ".ai/handoffs/T351/handoff.md",
            "ROADMAP_STATE.yaml",
        ],
    )

    assert result["task_file"] == ".ai/tasks/T351.task.yaml"


def test_t353_scope_accepts_divine_capitalization_inventory_surfaces() -> None:
    result = validator.validate_task_scope(
        task_file=T353_TASK,
        changed_files=[
            ".ai/control/divine_capitalization_inventory.yaml",
            ".ai/control/chunking_agent_preflight.yaml",
            ".ai/control/chunking_theological_decision_register.yaml",
            ".ai/control/harness_upgrade_roadmap.yaml",
            ".ai/tasks/T352.task.yaml",
            ".ai/tasks/T353.task.yaml",
            ".ai/handoffs/T352/handoff.md",
            ".ai/handoffs/T353/handoff.md",
            "docs/roadmap/T353_DIVINE_CAPITALIZATION_INVENTORY_HARNESS.md",
            "docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md",
            "scripts/build_divine_capitalization_inventory.py",
            "scripts/validate_divine_capitalization_inventory.py",
            "scripts/validate_chunking_agent_preflight.py",
            "scripts/validate_task_scope.py",
            "scripts/validate_all.py",
            "tests/test_divine_capitalization_inventory.py",
            "tests/test_chunking_agent_preflight.py",
            "tests/test_task_scope_validator.py",
            "tests/test_ai_roadmap_table_of_contents.py",
            "tests/test_t337a_psalm_review_packet.py",
            "tests/test_t337_selection_docs.py",
            "tests/test_t342_revelation_candidate_selection.py",
            "tests/test_t344_revelation_owner_selection.py",
            "tests/test_t351_bible_wide_research_triage.py",
            "ROADMAP_STATE.yaml",
            "AI_FRONT_DOOR.md",
            "AI_TABLE_OF_CONTENTS.md",
        ],
    )

    assert result["task_file"] == ".ai/tasks/T353.task.yaml"


def test_t354_scope_accepts_wj_marker_inventory_surfaces() -> None:
    result = validator.validate_task_scope(
        task_file=T354_TASK,
        changed_files=[
            ".ai/control/wj_marker_inventory.yaml",
            ".ai/control/chunking_agent_preflight.yaml",
            ".ai/control/chunking_theological_decision_register.yaml",
            ".ai/control/bible_chunking_readiness_map.yaml",
            ".ai/control/bible_chunking_research_triage_map.yaml",
            ".ai/control/harness_upgrade_roadmap.yaml",
            ".ai/tasks/T353.task.yaml",
            ".ai/tasks/T354.task.yaml",
            ".ai/handoffs/T353/handoff.md",
            ".ai/handoffs/T354/handoff.md",
            "docs/roadmap/T354_WJ_MARKER_INVENTORY_HARNESS.md",
            "docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md",
            "scripts/build_wj_marker_inventory.py",
            "scripts/validate_wj_marker_inventory.py",
            "scripts/validate_chunking_agent_preflight.py",
            "scripts/validate_bible_chunking_readiness_map.py",
            "scripts/validate_owner_selection_implementation_gate.py",
            "scripts/validate_all.py",
            "tests/test_wj_marker_inventory.py",
            "tests/test_divine_capitalization_inventory.py",
            "tests/test_chunking_agent_preflight.py",
            "tests/test_task_scope_validator.py",
            "tests/test_ai_roadmap_table_of_contents.py",
            "tests/test_bible_chunking_readiness_map.py",
            "tests/test_owner_selection_implementation_gate.py",
            "tests/test_t337a_psalm_review_packet.py",
            "tests/test_t337_selection_docs.py",
            "tests/test_t342_revelation_candidate_selection.py",
            "tests/test_t343_revelation_review_packet.py",
            "tests/test_t344_revelation_owner_selection.py",
            "tests/test_t351_bible_wide_research_triage.py",
            "ROADMAP_STATE.yaml",
            "AI_FRONT_DOOR.md",
            "AI_TABLE_OF_CONTENTS.md",
        ],
    )

    assert result["task_file"] == ".ai/tasks/T354.task.yaml"


def test_t352_scope_accepts_epistle_packet_surfaces() -> None:
    result = validator.validate_task_scope(
        task_file=T352_TASK,
        changed_files=[
            "docs/roadmap/T352_EPISTLE_ARGUMENT_REVIEW_PACKETS.md",
            "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md",
            "eval/chunking_gold/review_packets/rom9_11_argument_review.md",
            "eval/chunking_gold/review_packets/heb7_10_priesthood_argument_review.md",
            "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
            "eval/chunking_gold/review_packets/REVIEW_PACKET_INDEX.md",
            "eval/chunking_gold/review_packets/review_packet_index.json",
            "eval/chunking_gold/stress_atlas/observed_stress_behavior.json",
            "scripts/validate_epistle_argument_review_packets.py",
            "tests/test_t352_epistle_argument_review_packets.py",
            ".ai/tasks/T352.task.yaml",
            ".ai/handoffs/T352/handoff.md",
            "ROADMAP_STATE.yaml",
        ],
    )

    assert result["task_file"] == ".ai/tasks/T352.task.yaml"


def test_t355_scope_accepts_wj_speaker_policy_surfaces() -> None:
    result = validator.validate_task_scope(
        task_file=T355_TASK,
        changed_files=[
            ".ai/control/wj_speaker_discourse_policy.yaml",
            ".ai/control/chunking_agent_preflight.yaml",
            ".ai/control/chunking_theological_decision_register.yaml",
            ".ai/control/bible_chunking_readiness_map.yaml",
            ".ai/tasks/T355.task.yaml",
            ".ai/handoffs/T355/handoff.md",
            "docs/roadmap/T355_WJ_SPEAKER_POLICY_AND_TARGET_SELECTION.md",
            "docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md",
            "scripts/validate_wj_speaker_discourse_policy.py",
            "scripts/validate_owner_selection_implementation_gate.py",
            "scripts/validate_chunking_agent_preflight.py",
            "scripts/validate_bible_chunking_readiness_map.py",
            "scripts/validate_all.py",
            "tests/test_wj_speaker_discourse_policy.py",
            "tests/test_owner_selection_implementation_gate.py",
            "tests/test_chunking_agent_preflight.py",
            "tests/test_task_scope_validator.py",
            "tests/test_ai_roadmap_table_of_contents.py",
            "tests/test_bible_chunking_readiness_map.py",
            "tests/test_t337a_psalm_review_packet.py",
            "tests/test_t337_selection_docs.py",
            "tests/test_t342_revelation_candidate_selection.py",
            "tests/test_t343_revelation_review_packet.py",
            "tests/test_t344_revelation_owner_selection.py",
            "tests/test_t351_bible_wide_research_triage.py",
            "ROADMAP_STATE.yaml",
            "AI_FRONT_DOOR.md",
            "AI_TABLE_OF_CONTENTS.md",
        ],
    )

    assert result["task_file"] == ".ai/tasks/T355.task.yaml"


def test_scope_rejects_paths_outside_allowed_scope() -> None:
    with pytest.raises(validator.TaskScopeError, match="does not allow"):
        validator.validate_task_scope(
            task_file=T344_TASK,
            changed_files=["README.md"],
        )


def test_scope_rejects_master_context_even_if_task_allows_it(tmp_path: Path) -> None:
    task_file = tmp_path / "T999.task.yaml"
    task_file.write_text(
        "\n".join(
            [
                "id: T999",
                "scope:",
                "  allowed_paths:",
                "    - .ai/control/MASTER_CONTEXT.md",
                "  forbidden_paths: []",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(validator.TaskScopeError, match="hard-forbidden"):
        validator.validate_task_scope(
            task_file=task_file,
            changed_files=[".ai/control/MASTER_CONTEXT.md"],
        )


def test_scope_accepts_directory_prefixes() -> None:
    validator.validate_task_scope(
        task_file=T344_TASK,
        changed_files=[".ai/audits/reports/example.md"],
    )


def test_default_task_id_reads_current_task_without_strict_yaml(tmp_path: Path) -> None:
    focus = tmp_path / "current_focus.yaml"
    focus.write_text(
        "current_task: T344\nnext_sprint: Owner chooses exactly one T344 option: REV-T344-A\n",
        encoding="utf-8",
    )

    assert validator.default_task_id(focus) == "T344"
