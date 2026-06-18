from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_governance_memory_durability as validator


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / ".ai" / "control" / "governance_memory_durability_policy.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
TASK_SCOPE = ROOT / "scripts" / "validate_task_scope.py"


def test_governance_memory_durability_validates_current_repo() -> None:
    data = validator.validate_governance_memory_durability(POLICY)

    assert data["object_type"] == "governance_memory_durability_policy"
    assert data["authority"]["records_protected_memory_surfaces"] is True
    assert data["authority"]["authorizes_register_deletion"] is False
    assert data["authority"]["authorizes_chunk_output_change"] is False


def test_decision_register_is_critical_non_deletable_memory() -> None:
    data = validator.validate_governance_memory_durability(POLICY)
    surfaces = {item["surface_id"]: item for item in data["protected_memory_surfaces"]}
    register = surfaces["chunking_theological_decision_register"]

    assert register["path"] == ".ai/control/chunking_theological_decision_register.yaml"
    assert register["protection_level"] == "critical_non_deletable_governance_memory"
    assert "AI_FRONT_DOOR.md" in register["must_be_discoverable_from"]
    assert "AI_TABLE_OF_CONTENTS.md" in register["must_be_discoverable_from"]
    assert "scripts/validate_chunking_theological_decision_register.py" in register["required_validators"]
    assert REGISTER.exists()


def test_task_scope_marks_decision_register_as_protected() -> None:
    text = TASK_SCOPE.read_text(encoding="utf-8")

    assert ".ai/control/chunking_theological_decision_register.yaml" in text
    assert ".ai/control/governance_memory_durability_policy.yaml" in text
    assert ".ai/control/owner_decision_projection_policy.yaml" in text


def test_durability_policy_rejects_register_deletion_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_governance_memory_durability(POLICY))
    data["authority"]["authorizes_register_deletion"] = True
    candidate = tmp_path / "durability.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.GovernanceMemoryError, match="authorizes_register_deletion"):
        validator.validate_governance_memory_durability(candidate)
