from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t401_eph1_output_pilot as validator


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".ai" / "control" / "t401_eph1_output_pilot_manifest.yaml"


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t401_eph1_output_pilot_validates_current_repo() -> None:
    data = validator.validate_t401_eph1_output_pilot(MANIFEST)

    assert data["object_type"] == "t401_eph1_output_pilot_manifest"
    assert data["task_id"] == "T401"
    assert data["status"] == "complete_output_changed_eph1_parent_overlay"
    assert data["selected_parent"] == "Eph.1.3-Eph.1.14"
    assert data["selected_children"] == []
    assert data["output_change"]["baseline_chunk_count"] == 1137
    assert data["output_change"]["candidate_chunk_count"] == 1138
    assert data["overlay_record"]["decision_register_entry"] == "CD-076"


def test_t401_manifest_records_only_one_eph1_overlay() -> None:
    data = validator.validate_t401_eph1_output_pilot(MANIFEST)
    overlay = data["overlay_record"]

    assert data["output_change"]["changed_output_ids"] == [validator.OVERLAY_ID]
    assert data["output_change"]["changed_spans"] == ["Eph.1.3-Eph.1.14"]
    assert data["output_change"]["changed_existing_output_ids"] == []
    assert data["output_change"]["removed_output_ids"] == []
    assert overlay["id"] == validator.OVERLAY_ID
    assert overlay["osis_start"] == "Eph.1.3"
    assert overlay["osis_end"] == "Eph.1.14"
    assert overlay["selected_children"] == []
    assert overlay["baseline_chunks_preserved_byte_identical"] is True
    assert overlay["non_truth_bearing_overlay"] is True
    assert overlay["graph_retrieval_truth_authorized"] is False
    assert overlay["child_span_authorized"] is False


def test_t401_manifest_records_route_isolation_proof() -> None:
    data = validator.validate_t401_eph1_output_pilot(MANIFEST)
    route = data["route_isolation"]

    assert route["harness"] == "scripts/chunking/route_isolation_harness.py"
    assert route["target_span"] == "Eph.1.3-Eph.1.14"
    assert route["changed_keys"] == []
    assert route["added_keys"] == [validator.OVERLAY_ID]
    assert route["removed_keys"] == []
    assert route["changed_spans"] == ["Eph.1.3-Eph.1.14"]
    assert route["non_target_byte_identical"] is True
    assert route["child_spans_authorized"] is False


def test_t401_manifest_rejects_child_span_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t401_eph1_output_pilot(MANIFEST))
    data["authority"]["authorizes_child_spans"] = True
    candidate = tmp_path / "manifest.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T401OutputPilotError, match="authorizes_child_spans"):
        validator.validate_t401_eph1_output_pilot(candidate)


def test_t401_manifest_rejects_extra_changed_output(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t401_eph1_output_pilot(MANIFEST))
    data["output_change"]["changed_output_ids"].append("chunk--unexpected")
    candidate = tmp_path / "manifest.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T401OutputPilotError, match="changed_output_ids"):
        validator.validate_t401_eph1_output_pilot(candidate)
