from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / ".ai" / "control" / "t340_psalm_candidate_promotion_decision.yaml"
TASK = ROOT / ".ai" / "tasks" / "T340.task.yaml"
DOC = ROOT / "docs" / "roadmap" / "T340_PSALM_CANDIDATE_PROMOTION_DECISION.md"
CURRENT_FOCUS = ROOT / ".ai" / "control" / "current_focus.yaml"
PROJECT_STATUS = ROOT / ".ai" / "control" / "PROJECT_STATUS.md"
SKILL_METADATA = ROOT / "pipelines" / "chunking" / "skills" / "candidate" / \
    "psalm-whole-then-stanza-v1" / "SKILL_METADATA.json"
APPROVED_SKILLS = ROOT / "registry" / "chunking" / "approved-skills.json"
SKILL_TOC = ROOT / "registry" / "chunking" / "skill-toc.json"
SKILL_GRAPH = ROOT / "registry" / "chunking" / "skill-graph-index.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(read(path))


def load_json(path: Path) -> dict:
    return json.loads(read(path))


def test_t340_decision_is_machine_readable_hold() -> None:
    decision = load_yaml(DECISION)
    task = load_yaml(TASK)

    assert decision["schema_version"] == "t340-psalm-candidate-promotion-decision.v1"
    assert decision["decision"] in {"promote_limited", "hold", "reject"}
    assert decision["decision"] == "hold"
    assert decision["subject"]["skill_id"] == "psalm-whole-then-stanza-v1"
    assert task["decision"]["value"] == "hold"
    assert task["decision"]["decision_file"] == ".ai/control/t340_psalm_candidate_promotion_decision.yaml"
    assert task["decision"]["lifecycle_promotion_authorized"] is False
    assert task["decision"]["runtime_behavior_change_authorized"] is False
    assert task["decision"]["whole_bible_improvement_claim_authorized"] is False


def test_t340_hold_scope_preserves_ps89_only_authorization() -> None:
    decision = load_yaml(DECISION)
    scope = decision["authorization_scope"]

    assert scope["reviewed_psalm_route_only"] is True
    assert scope["approved_output_change_case_ids"] == ["ps89_owner_decision_option_c"]
    assert scope["ps89_parent"] == "Ps.89.1-Ps.89.52"
    assert scope["ps89_children"] == [
        "Ps.89.1-Ps.89.4",
        "Ps.89.5-Ps.89.18",
        "Ps.89.19-Ps.89.37",
        "Ps.89.38-Ps.89.45",
        "Ps.89.46-Ps.89.48",
        "Ps.89.49-Ps.89.52",
    ]
    assert scope["ps89_52_scope_note"] == "book_iii_doxology_scope_note"
    assert scope["no_ps89_52_orphan"] is True


def test_t340_explicitly_does_not_authorize_global_or_boundary_work() -> None:
    non_auth = load_yaml(DECISION)["explicit_non_authorizations"]

    for key in [
        "whole_bible_improvement_claim",
        "broad_psalm_optimization",
        "global_psalm_rule",
        "global_poetry_rule",
        "global_selah_rule",
        "global_blank_line_rule",
        "global_doxology_rule",
        "long_psalm_rule",
        "marker_only_boundary_authority",
        "psalm_136_change",
        "non_psalm_route_leakage",
        "revelation_implementation",
        "boundary_import",
        "t327g",
    ]:
        assert non_auth[key] is False


def test_t340_hold_does_not_promote_skill_metadata_or_registries() -> None:
    metadata = load_json(SKILL_METADATA)
    approved = load_json(APPROVED_SKILLS)
    toc = load_json(SKILL_TOC)
    graph = load_json(SKILL_GRAPH)

    assert metadata["lifecycle_state"] == "candidate"
    assert metadata["eval"]["quality_improvement_claimed"] is False
    assert metadata["quality"]["promotion_blocked_until"] == \
        "same-baseline Psalm 89-only evaluation and review pass"
    assert "psalm-whole-then-stanza-v1" not in {
        skill["skill_id"] for skill in approved["skills"]
    }
    toc_skill = next(skill for skill in toc["skills"] if skill["skill_id"] == "psalm-whole-then-stanza-v1")
    assert toc_skill["lifecycle_state"] == "candidate"
    graph_node = next(node for node in graph["nodes"] if node["id"] == "psalm-whole-then-stanza-v1")
    assert graph_node["lifecycle_state"] == "candidate"


def test_t340_status_and_docs_keep_hold_decision_narrow() -> None:
    combined = "\n".join([read(DOC), read(CURRENT_FOCUS), read(PROJECT_STATUS)])

    assert "Decision: `hold`" in combined
    assert "no lifecycle promotion" in combined or "lifecycle promotion" in combined
    assert "whole-Bible improvement" in combined
    assert "global Psalm" in combined
    assert "global poetry" in combined
    assert "global Selah" in combined
    assert "global blank-line" in combined
    assert "global doxology" in combined
    assert "boundary import" in combined
    assert "T327G" in combined
    assert "Revelation implementation" in combined


def test_t340_task_forbids_runtime_and_data_paths() -> None:
    task = load_yaml(TASK)
    forbidden = set(task["scope"]["forbidden_paths"])

    assert "data/raw/" in forbidden
    assert "data/canonical/" in forbidden
    assert "data/derived/" in forbidden
    assert "pipelines/chunking/skills/" in forbidden
    assert "pipelines/chunking/chunker.py" in forbidden
    assert "pipelines/chunking/orchestrator.py" in forbidden
    assert "pipelines/chunking/evaluate_chunks.py" in forbidden
    assert "eval/chunking_runs/" in forbidden
    assert "eval/LEADERBOARD.md" in forbidden
