from __future__ import annotations

import json
from pathlib import Path

from scripts import validate_t423_pilot_gate as validator


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def _patch_empty_model_discovery(monkeypatch) -> None:
    monkeypatch.setattr(validator, "discover_model_folders", lambda root: [])


def test_pilot_gate_accepts_batch2_span_inside_delta_region(tmp_path: Path, monkeypatch) -> None:
    comparison = tmp_path / "comparison"
    comparison.mkdir()
    (comparison / "model_agreement_matrix.yaml").write_text("ok: true\n", encoding="utf-8")
    _write_jsonl(comparison / "agreement_chunks.jsonl", [])
    _write_jsonl(
        comparison / "disagreement_delta.jsonl",
        [{"delta_id": "DELTA-Phlm-001", "book": "Phlm", "region": "Phlm.1.1-Phlm.1.25"}],
    )
    monkeypatch.setattr(validator, "COMPARISON", comparison)
    monkeypatch.setattr(validator, "AGREEMENT", comparison / "agreement_chunks.jsonl")
    monkeypatch.setattr(validator, "DELTAS", comparison / "disagreement_delta.jsonl")
    _patch_empty_model_discovery(monkeypatch)

    errors = validator.validate_pilot_gate(
        policy={
            "pilot_gate": {
                "status": "go",
                "required_books": ["Phlm"],
                "required_checks": {
                    "batch2_span_surfaces": [{"book": "Phlm", "span": "Phlm.1.1-Phlm.1.7"}]
                },
            }
        },
        scratch_root=tmp_path,
    )

    assert errors == []


def test_pilot_gate_reports_batch2_span_not_overlapping_outputs(tmp_path: Path, monkeypatch) -> None:
    comparison = tmp_path / "comparison"
    comparison.mkdir()
    (comparison / "model_agreement_matrix.yaml").write_text("ok: true\n", encoding="utf-8")
    _write_jsonl(comparison / "agreement_chunks.jsonl", [])
    _write_jsonl(
        comparison / "disagreement_delta.jsonl",
        [{"delta_id": "DELTA-Phlm-001", "book": "Phlm", "region": "Phlm.1.8-Phlm.1.25"}],
    )
    monkeypatch.setattr(validator, "COMPARISON", comparison)
    monkeypatch.setattr(validator, "AGREEMENT", comparison / "agreement_chunks.jsonl")
    monkeypatch.setattr(validator, "DELTAS", comparison / "disagreement_delta.jsonl")
    _patch_empty_model_discovery(monkeypatch)

    errors = validator.validate_pilot_gate(
        policy={
            "pilot_gate": {
                "status": "go",
                "required_books": ["Phlm"],
                "required_checks": {
                    "batch2_span_surfaces": [{"book": "Phlm", "span": "Phlm.1.1-Phlm.1.7"}]
                },
            }
        },
        scratch_root=tmp_path,
    )

    assert errors == ["batch2 span not in agreement or delta ledgers: Phlm Phlm.1.1-Phlm.1.7"]
