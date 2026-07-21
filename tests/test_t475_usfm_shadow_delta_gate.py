from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import yaml

from scripts.validate_t475_usfm_shadow_delta_gate import T475ValidationError, validate_t475

ROOT = Path(__file__).resolve().parent.parent


def _copy_tree(tmp_path: Path) -> Path:
    for rel in (
        ".ai/tasks/T475.task.yaml",
        ".ai/control/t475_usfm_shadow_delta_gate.yaml",
        ".ai/control/ai_agnostic_rust_subagent_charter.yaml",
        ".ai/control/t474_usfm_marker_anchor_contract.yaml",
        ".ai/prompts/t475_independent_audit_prompt.md",
        "config/agents/model_routing.yaml",
        "config/agents/agent_roles.yaml",
        "config/canon/canonical_66_books.yaml",
        "config/ingest/usfm_marker_coverage.yaml",
        "data/raw/bible/eng-web/usfm/eng-web_usfm.zip",
        "data/raw/bible/eng-web/source_manifest.yaml",
        "scripts/run_t475_shadow_delta.py",
        "scripts/validate_t475_generated_transition_state.py",
    ):
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, target)
    return tmp_path


def _mutate_control(root: Path, mutate) -> None:
    path = root / ".ai/control/t475_usfm_shadow_delta_gate.yaml"
    text = path.read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    header = yaml.safe_load(parts[1])
    body = yaml.safe_load(parts[2])
    mutate(body)
    path.write_text("---\n" + yaml.safe_dump(header, sort_keys=False) + "---\n" + yaml.safe_dump(body, sort_keys=False), encoding="utf-8")


def test_t475_contract_passes_without_runtime_artifacts() -> None:
    result = validate_t475(ROOT)
    assert result["families"] == 12


def test_missing_output_family_fails(tmp_path: Path) -> None:
    root = _copy_tree(tmp_path)
    _mutate_control(root, lambda data: data["required_output_families"].pop())
    with pytest.raises(T475ValidationError, match="output families"):
        validate_t475(root)


def test_visible_scripture_text_fails(tmp_path: Path) -> None:
    root = _copy_tree(tmp_path)
    _mutate_control(root, lambda data: data["comparison_contract"].update(visible_scripture_text_allowed_in_reports=True))
    with pytest.raises(T475ValidationError, match="Scripture text"):
        validate_t475(root)


def test_chunker_execution_fails(tmp_path: Path) -> None:
    root = _copy_tree(tmp_path)
    _mutate_control(root, lambda data: data["chunk_impact_contract"].update(run_chunker=True))
    with pytest.raises(T475ValidationError, match="chunker"):
        validate_t475(root)


def test_require_artifacts_fails_before_frozen_bundle(tmp_path: Path) -> None:
    root = _copy_tree(tmp_path)
    with pytest.raises(T475ValidationError, match="required evidence missing"):
        validate_t475(root, require_artifacts=True)


def test_t475_frozen_evidence_passes() -> None:
    result = validate_t475(ROOT, require_artifacts=True)
    assert result["require_artifacts"] is True
    assert result["require_independent_audit"] is False


def test_independent_audit_gate_passes_after_pass_status() -> None:
    result = validate_t475(ROOT, require_artifacts=True, require_independent_audit=True)
    assert result["require_independent_audit"] is True


def test_independent_audit_gate_fails_while_pending(tmp_path: Path) -> None:
    root = _copy_tree(tmp_path)
    shutil.copytree(ROOT / ".ai/context/agent_work/T475", root / ".ai/context/agent_work/T475")
    audit_rel = Path(".ai/audits/reports/20260720-T475-independent-shadow-delta-audit-post-t519.md")
    audit_target = root / audit_rel
    audit_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / audit_rel, audit_target)
    _mutate_control(
        root,
        lambda data: data["required_evidence"].update(
            {"independent_audit_status": "pending_claude_audit"}
        ),
    )
    with pytest.raises(T475ValidationError, match="independent audit status does not permit"):
        validate_t475(root, require_independent_audit=True)


def test_broad_generated_validator_deferral_fails(tmp_path: Path) -> None:
    root = _copy_tree(tmp_path)
    transition_validator = root / "scripts/validate_t475_generated_transition_state.py"
    transition_validator.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "scripts/validate_t475_generated_transition_state.py", transition_validator)
    _mutate_control(
        root,
        lambda data: data["ci_generated_transition_policy"][
            "deferred_legacy_generated_validators"
        ].append("validate_unrelated_gate.py"),
    )
    with pytest.raises(T475ValidationError, match="deferred generated-validator set"):
        validate_t475(root)


def test_data_map_transition_delta_cannot_expand(tmp_path: Path) -> None:
    root = _copy_tree(tmp_path)
    _mutate_control(
        root,
        lambda data: data["ci_generated_transition_policy"]["data_map_candidate_delta"].update(
            {"unrelated_rows": {"baseline": 1, "candidate": 0}}
        ),
    )
    with pytest.raises(T475ValidationError, match="DATA_MAP delta changed"):
        validate_t475(root)


def test_pytest_transition_deferral_cannot_expand(tmp_path: Path) -> None:
    root = _copy_tree(tmp_path)
    _mutate_control(
        root,
        lambda data: data["ci_generated_transition_policy"]["deferred_pytest_nodes"].append(
            "tests/test_unrelated.py::test_unrelated"
        ),
    )
    with pytest.raises(T475ValidationError, match="deferred pytest node set changed"):
        validate_t475(root)
