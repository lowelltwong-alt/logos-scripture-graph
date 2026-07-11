from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml

from scripts import validate_llos_v1_adapter as validator


ROOT = Path(__file__).resolve().parents[1]


def test_dad_repo_write_policy_is_fail_closed_without_standing_approval() -> None:
    policy = json.loads((ROOT / ".digital-asset/dad-write-policy.json").read_text(encoding="utf-8"))
    assert policy["dad_write_allowed"] is False
    assert policy["approved_explicit_approval_ids"] == []
    assert policy["logos_local_outbox_write_allowed"] is True
    assert policy["logos_local_dad_central_read_allowed"] is True
    assert policy["dad_push_or_inbox_write_allowed"] is False
    assert policy["rollout_approval_is_standing_write_permission"] is False
CONTROL = ROOT / ".ai" / "control" / "llos_v1_adapter.yaml"


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_llos_v1_adapter_validates_current_repo() -> None:
    data = validator.validate_llos_v1_adapter()

    assert data["adapter_scope"]["mode"] == "metadata_only"
    assert data["upstream_governance"]["surface_version"] == "1.0.0"
    assert data["asymmetric_transport_boundary"]["logos_local_tooling"]["may_write_own_outbox"] is True
    assert data["asymmetric_transport_boundary"]["dad_central"]["may_push_or_write_any_file_into_logos"] is False


def test_rejects_dad_write_into_logos(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_llos_v1_adapter())
    data["asymmetric_transport_boundary"]["dad_central"]["may_push_or_write_any_file_into_logos"] = True
    candidate = tmp_path / "llos.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.LlosAdapterError, match="may_push_or_write_any_file_into_logos"):
        validator.validate_llos_v1_adapter(candidate)


def test_rejects_unpinned_or_non_reference_upstream_surface(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_llos_v1_adapter())
    data["upstream_governance"]["surface_version"] = "latest"
    candidate = tmp_path / "llos.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.LlosAdapterError, match="surface_version"):
        validator.validate_llos_v1_adapter(candidate)


def test_rejects_canonical_data_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_llos_v1_adapter())
    data["authority"]["authorizes_canonical_or_source_data_change"] = True
    candidate = tmp_path / "llos.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.LlosAdapterError, match="authorizes_canonical_or_source_data_change"):
        validator.validate_llos_v1_adapter(candidate)
