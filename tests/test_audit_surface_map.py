from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.validate_audit_surface_map import validate_audit_surface_map


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / ".ai" / "control" / "audit_surface_map.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
LESSONS = ROOT / "docs" / "methodology" / "WORKFLOW_LESSONS.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_audit_surface_map_validates_and_is_non_authorizing() -> None:
    data = validate_audit_surface_map(MAP)

    assert data["object_type"] == "audit_surface_map"
    assert data["trust_zone"] == "canonical"
    assert data["authority"]["records_audit_surfaces"] is True
    assert data["authority"]["authorizes_code_change"] is False
    assert data["authority"]["authorizes_chunk_output_change"] is False
    assert data["authority"]["authorizes_reviewed_gold_promotion"] is False
    assert data["authority"]["authorizes_owner_decision"] is False
    assert data["future_harness_roadmap"] == ".ai/control/harness_upgrade_roadmap.yaml"


def test_front_door_and_toc_expose_no_context_audit_path() -> None:
    front_door = read(FRONT_DOOR)
    toc = read(TOC)

    for phrase in [
        ".ai/audits/README.md",
        ".ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md",
        "no-context A/B/red-team",
    ]:
        assert phrase in front_door

    for phrase in [
        ".ai/audits/README.md",
        ".ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md",
        ".ai/audits/templates/REVIEW_REPORT_TEMPLATE.md",
        ".ai/control/audit_surface_map.yaml",
        ".ai/control/harness_upgrade_roadmap.yaml",
        ".ai/control/governance_memory_durability_policy.yaml",
        ".ai/control/owner_decision_projection_policy.yaml",
        "scripts/agent/no_context_audit_harness.py",
        "scripts/validate_task_scope.py",
    ]:
        assert phrase in toc


def test_workflow_lesson_records_audit_path() -> None:
    lessons = read(LESSONS)

    assert "WORKFLOW-LESSON-003 - No-Context Review Requires A Repo-Resident Audit Path" in lessons
    assert "Chat-only rationale is unproven" in lessons
    assert "scripts/agent/no_context_audit_harness.py" in lessons
    assert ".ai/control/harness_upgrade_roadmap.yaml" in lessons


def test_no_context_audit_harness_prints_brief() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "agent" / "no_context_audit_harness.py"),
            "--task-id",
            "T344",
            "--base-ref",
            "origin/main",
            "--print",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "# No-Context Audit Brief" in result.stdout
    assert ".ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md" in result.stdout
    assert "[committed-vs-base]" in result.stdout
    assert "[untracked]" in result.stdout
    assert "git/PR state" in result.stdout
    assert ".ai/control/harness_upgrade_roadmap.yaml" in result.stdout
    assert ".ai/control/governance_memory_durability_policy.yaml" in result.stdout
    assert ".ai/control/owner_decision_projection_policy.yaml" in result.stdout
    assert "python scripts/validate_governance_memory_durability.py" in result.stdout
    assert "python scripts/validate_owner_decision_projection_policy.py" in result.stdout
    assert "python scripts/validate_audit_surface_map.py" in result.stdout


def test_harness_upgrade_roadmap_records_future_watch_items() -> None:
    data = validate_audit_surface_map(MAP)
    roadmap = (ROOT / data["future_harness_roadmap"]).read_text(encoding="utf-8")

    for harness_id in [
        "HARN-001",
        "HARN-002",
        "HARN-003",
        "HARN-004",
        "HARN-005",
        "HARN-006",
        "HARN-007",
        "HARN-008",
        "HARN-009",
        "HARN-010",
        "HARN-011",
        "HARN-012",
        "HARN-015",
    ]:
        assert harness_id in roadmap
    assert "promote_issue_to_harness_when" in roadmap
    assert "local_validation_and_ci_validation_disagree" in roadmap
    assert "HARN-001" in roadmap
    assert "status: implemented_v1" in roadmap
    assert "scripts/validate_task_scope.py" in roadmap
    assert "Owner-pattern projection conflict scanner" in roadmap
