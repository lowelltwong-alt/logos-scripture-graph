from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t397_eph1_route_isolation_harness as validator


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t397_harness_record_validates_current_repo() -> None:
    data = validator.validate_t397_eph1_route_isolation_harness()

    assert data["object_type"] == "eph1_route_isolation_harness_record"
    assert data["task_id"] == "T397"
    assert data["status"] == "complete_non_output_changing_route_isolation_harness_prep"
    assert data["goal6_scope"]["selected_parent"] == "Eph.1.3-Eph.1.14"
    assert data["goal6_scope"]["selected_children"] == []
    assert data["authority"]["records_harness_prep"] is True
    assert data["authority"]["authorizes_chunk_output_change"] is False
    assert data["authority"]["authorizes_implementation"] is False
    assert data["decision_register_entry"] == "CD-074"
    assert data["lesson_recorded"]["lesson_id"] == "LSN-028"


def test_t397_record_lists_executable_harnesses() -> None:
    data = validator.validate_t397_eph1_route_isolation_harness()
    by_id = {item["harness_id"]: item for item in data["harnesses"]}

    assert set(by_id) == validator.REQUIRED_HARNESSES
    assert by_id["T397-HARN-001"]["script"] == "scripts/chunking/route_isolation_harness.py"
    assert by_id["T397-HARN-001"]["test"] == "tests/test_route_isolation_harness.py"
    assert "non_target_record_bytes_change" in by_id["T397-HARN-001"]["must_fail_if"]
    assert "child_subspan_added_without_owner_authorization" in by_id["T397-HARN-003"]["must_fail_if"]
    assert "target_end_moves_after_Eph_1_14" in by_id["T397-HARN-004"]["must_fail_if"]


def test_t397_record_requires_future_owner_gate_before_output() -> None:
    data = validator.validate_t397_eph1_route_isolation_harness()
    requirements = data["future_output_pilot_requirements"]["before_any_candidate_output_change"]

    assert "explicit_owner_output_pilot_authorization_for_Eph_1_3_Eph_1_14" in requirements
    assert "route_isolation_harness_passes_on_real_baseline_candidate_outputs" in requirements
    assert "same_baseline_evaluation_passes_or_records_no_improvement_claim" in requirements
    assert data["future_output_pilot_requirements"]["default_if_missing"] == "stop_before_implementation_or_output_change"


def test_t397_record_rejects_output_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t397_eph1_route_isolation_harness())
    data["authority"]["authorizes_chunk_output_change"] = True
    candidate = tmp_path / "t397.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T397HarnessError, match="authorizes_chunk_output_change"):
        validator.validate_t397_eph1_route_isolation_harness(candidate)


def test_t397_record_rejects_child_span_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t397_eph1_route_isolation_harness())
    data["authority"]["authorizes_child_spans"] = True
    candidate = tmp_path / "t397.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T397HarnessError, match="authorizes_child_spans"):
        validator.validate_t397_eph1_route_isolation_harness(candidate)
