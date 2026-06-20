from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import validate_t374_additive_parent_overlay as validator


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".ai" / "control" / "t374_additive_parent_overlay_manifest.yaml"


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_t374_additive_parent_overlay_validates_current_repo() -> None:
    data = validator.validate_t374_additive_parent_overlay(MANIFEST)

    assert data["object_type"] == "t374_additive_parent_overlay_manifest"
    assert data["task_id"] == "T374"
    assert data["status"] == "complete_output_changed_additive_parent_overlay"
    assert data["selected_option"] == "T374-OVERLAP-B"
    assert data["selected_parent"] == "1Cor.8.1-1Cor.10.33"
    assert data["selected_children"] == []
    assert data["output_change"]["baseline_chunk_count"] == 1136
    assert data["output_change"]["candidate_chunk_count"] == 1137
    assert data["overlay_record"]["decision_register_entry"] == "CD-056"


def test_t374_manifest_records_only_one_additive_overlay() -> None:
    data = validator.validate_t374_additive_parent_overlay(MANIFEST)
    overlay = data["overlay_record"]

    assert data["output_change"]["changed_output_ids"] == [validator.OVERLAY_ID]
    assert data["output_change"]["changed_spans"] == ["1Cor.8.1-1Cor.10.33"]
    assert overlay["id"] == validator.OVERLAY_ID
    assert overlay["osis_start"] == "1Cor.8.1"
    assert overlay["osis_end"] == "1Cor.10.33"
    assert overlay["selected_children"] == []
    assert overlay["baseline_chunks_preserved_byte_identical"] is True
    assert overlay["non_truth_bearing_overlay"] is True
    assert overlay["graph_retrieval_truth_authorized"] is False
    assert overlay["child_span_authorized"] is False


def test_t374_manifest_rejects_child_span_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t374_additive_parent_overlay(MANIFEST))
    data["authority"]["authorizes_child_spans"] = True
    candidate = tmp_path / "manifest.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T374OverlayError, match="authorizes_child_spans"):
        validator.validate_t374_additive_parent_overlay(candidate)


def test_t374_manifest_rejects_extra_changed_output(tmp_path: Path) -> None:
    data = copy.deepcopy(validator.validate_t374_additive_parent_overlay(MANIFEST))
    data["output_change"]["changed_output_ids"].append("chunk--unexpected")
    candidate = tmp_path / "manifest.yaml"
    write_yaml(candidate, data)

    with pytest.raises(validator.T374OverlayError, match="changed_output_ids"):
        validator.validate_t374_additive_parent_overlay(candidate)
