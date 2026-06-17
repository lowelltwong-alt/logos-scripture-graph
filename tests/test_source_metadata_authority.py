from __future__ import annotations

from pathlib import Path

import pytest

from scripts import validate_source_metadata_authority as validator


ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
T344_TASK = ROOT / ".ai" / "tasks" / "T344.task.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
HARNESS_ROADMAP = ROOT / ".ai" / "control" / "harness_upgrade_roadmap.yaml"


def test_source_metadata_authority_validator_passes_current_repo() -> None:
    validator.validate_source_metadata_authority()


def test_scanner_rejects_explicit_source_metadata_authority_true(tmp_path: Path) -> None:
    candidate = tmp_path / "bad.yaml"
    candidate.write_text("source_metadata_authority_allowed: true\n", encoding="utf-8")

    with pytest.raises(validator.SourceMetadataAuthorityError, match="source metadata authority allowed"):
        validator.scan_forbidden_authority([candidate])


def test_scanner_rejects_metadata_policy_authorizing_graph_edges(tmp_path: Path) -> None:
    candidate = tmp_path / "bad.yaml"
    candidate.write_text("authorizes_graph_edges: true\n", encoding="utf-8")

    with pytest.raises(validator.SourceMetadataAuthorityError, match="metadata authority policy set true"):
        validator.scan_forbidden_authority([candidate])


def test_preflight_policy_requires_metadata_to_remain_non_authorizing(tmp_path: Path) -> None:
    text = PREFLIGHT.read_text(encoding="utf-8").replace("authorizes_graph_edges: false", "authorizes_graph_edges: true")
    candidate = tmp_path / "preflight.yaml"
    candidate.write_text(text, encoding="utf-8")

    with pytest.raises(validator.SourceMetadataAuthorityError, match="authorizes_graph_edges must be false"):
        validator.validate_preflight_policy(candidate)


def test_t344_task_metadata_authority_flags_must_stay_false(tmp_path: Path) -> None:
    text = T344_TASK.read_text(encoding="utf-8").replace(
        "source_metadata_authority_allowed: false",
        "source_metadata_authority_allowed: true",
    )
    candidate = tmp_path / "T344.task.yaml"
    candidate.write_text(text, encoding="utf-8")

    with pytest.raises(validator.SourceMetadataAuthorityError, match="source_metadata_authority_allowed must be false"):
        validator.validate_task_flags([candidate])


def test_cd015_must_name_source_metadata_validator(tmp_path: Path) -> None:
    text = REGISTER.read_text(encoding="utf-8").replace(
        "      - scripts/validate_source_metadata_authority.py\n",
        "",
    )
    candidate = tmp_path / "register.yaml"
    candidate.write_text(text, encoding="utf-8")

    with pytest.raises(validator.SourceMetadataAuthorityError, match="CD-015 validators"):
        validator.validate_decision_register(candidate)


def test_harn_006_must_be_marked_implemented(tmp_path: Path) -> None:
    text = HARNESS_ROADMAP.read_text(encoding="utf-8").replace(
        "  - harness_id: HARN-006\n"
        "    title: Source-metadata authority scanner\n"
        "    status: implemented_v1",
        "  - harness_id: HARN-006\n"
        "    title: Source-metadata authority scanner\n"
        "    status: candidate_not_started",
    )
    candidate = tmp_path / "harness.yaml"
    candidate.write_text(text, encoding="utf-8")

    with pytest.raises(validator.SourceMetadataAuthorityError, match="HARN-006.status"):
        validator.validate_harn_006(candidate)
