from __future__ import annotations

import json
import shutil
from pathlib import Path

import yaml

from scripts.validate_t473_semantic_harness_pilot import (
    EXPECTED_PS119_STARTS,
    REQUIRED_FILES,
    ROOT,
    _ps119_raw_headings,
    validate_t473_artifact,
    validate_t473_package,
)


def _read_yaml(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        text = parts[1] + "\n" + parts[2]
    return yaml.safe_load(text)


def _write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8", newline="\n")


def _copy_package(tmp_path: Path) -> Path:
    for rel in REQUIRED_FILES.values():
        src = ROOT / rel
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return tmp_path


def _valid_candidate() -> dict:
    return {
        "artifact_type": "candidate_span",
        "schema_version": "t473_semantic_harness_pilot.v1",
        "candidate_id": "CANDIDATE-1",
        "scope_id": "T473-SCOPE-2JOHN",
        "span": "2John.1.12-2John.1.13",
        "origin_kind": "exact_observed_model_span",
        "source_model_id": "M4",
        "source_decision_id": "MODEL-DECISION-1",
        "observed_source_span": "2John.1.12-2John.1.13",
        "literary_evidence_ids": ["EVIDENCE-1"],
        "overlap_admission_id": "OVERLAP-1",
        "derived_from_region_or_vote": False,
        "non_authorizing": True,
        "candidate_eligible": False,
        "promotion_authority": "none",
    }


def test_t473_package_validates_current_repo() -> None:
    assert validate_t473_package(ROOT) == []


def test_raw_ps119_headings_precede_exact_eight_verse_starts() -> None:
    rows = _ps119_raw_headings(ROOT / REQUIRED_FILES["raw"])
    assert len(rows) == 22
    assert [row["next_verse"] for row in rows] == EXPECTED_PS119_STARTS


def test_schema_accepts_exact_typed_candidate() -> None:
    schema = json.loads((ROOT / REQUIRED_FILES["schema"]).read_text(encoding="utf-8"))
    assert validate_t473_artifact(schema, _valid_candidate()) == []


def test_schema_semantics_reject_region_inflation() -> None:
    schema = json.loads((ROOT / REQUIRED_FILES["schema"]).read_text(encoding="utf-8"))
    candidate = _valid_candidate()
    candidate["span"] = "2John.1.1-2John.1.13"
    errors = validate_t473_artifact(schema, candidate)
    assert "candidate span must equal observed source span" in errors


def test_rejects_pilot_execution_before_integrity_repair(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / REQUIRED_FILES["control"]
    data = _read_yaml(path)
    data["execution_state"]["pilot_execution_allowed"] = True
    _write_yaml(path, data)
    errors = validate_t473_package(root)
    assert "pilot execution must remain false" in errors


def test_rejects_chunk_output_authority(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / REQUIRED_FILES["task"]
    data = _read_yaml(path)
    data["authorization"]["authorizes_chunk_output"] = True
    _write_yaml(path, data)
    errors = validate_t473_package(root)
    assert "task.authorization.authorizes_chunk_output must be false" in errors


def test_rejects_source_repair_packet_that_authorizes_regeneration_now(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / REQUIRED_FILES["anchor_owner"]
    data = _read_yaml(path)
    data["owner_gate_effect"]["authorizes_canonical_regeneration_now"] = True
    _write_yaml(path, data)
    errors = validate_t473_package(root)
    assert "source owner packet authorizes_canonical_regeneration_now must be false" in errors


def test_rejects_missing_anchor_kind(tmp_path: Path) -> None:
    root = _copy_package(tmp_path)
    path = root / REQUIRED_FILES["anchor_audit"]
    data = json.loads(path.read_text(encoding="utf-8"))
    data["required_anchor_kinds"].remove("unresolved")
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    errors = validate_t473_package(root)
    assert "audit anchor kinds mismatch" in errors


def test_rejects_whole_letter_2john_candidate_provenance() -> None:
    schema = json.loads((ROOT / REQUIRED_FILES["schema"]).read_text(encoding="utf-8"))
    candidate = _valid_candidate()
    candidate["span"] = "2John.1.1-2John.1.13"
    candidate["observed_source_span"] = "2John.1.12-2John.1.13"
    assert validate_t473_artifact(schema, candidate)
