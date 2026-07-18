#!/usr/bin/env python3
"""Tests for IIIF acquisition core (no network)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import scripts.acquisition.iiif_acquisition_core as acquisition_core
from scripts.acquisition.validate_phase_completion import validate_nas_root
from scripts.acquisition.run_acquisition import refresh_storage_ledger_free_after
from scripts.acquisition.iiif_acquisition_core import (
    AcquisitionRunner,
    ProgressState,
    build_download_url,
    classify_canvas_label,
    detect_media_signature,
    ensure_storage_reserve,
    load_config,
    parse_manifest_resources,
    sha256_file,
)


SAMPLE_MANIFEST = {
    "@id": "https://example.test/0000061851/manifest.json",
    "sequences": [
        {
            "canvases": [
                {
                    "@id": "https://example.test/0000061851/canvas/00000001",
                    "label": "1r (Q35-f. 1r)",
                    "images": [
                        {
                            "@id": "https://example.test/anno/1",
                            "resource": {
                                "@type": "oa:Choice",
                                "default": {
                                    "@id": "https://example.test/00000001.jpg",
                                    "format": "image/jpeg",
                                    "width": 100,
                                    "height": 100,
                                    "label": [{"@language": "en", "@value": "Reproduction"}],
                                    "service": {
                                        "@id": "https://example.test/iiif/00000001.jpx",
                                        "profile": "http://iiif.io/api/image/2/level1.json",
                                    },
                                },
                                "item": [
                                    {
                                        "@id": "https://example.test/special/00000001.jpg",
                                        "format": "image/jpeg",
                                        "width": 100,
                                        "height": 100,
                                        "label": [{"@language": "en", "@value": "Raking light"}],
                                        "service": {
                                            "@id": "https://example.test/iiif/special/00000001.jpx",
                                            "profile": "http://iiif.io/api/image/2/level1.json",
                                        },
                                    }
                                ],
                            },
                        }
                    ],
                }
            ]
        }
    ],
}


def test_parse_manifest_expands_choice() -> None:
    resources = parse_manifest_resources(SAMPLE_MANIFEST, "codex_sinaiticus_leipzig_iiif")
    assert len(resources) == 2
    types = {r.capture_type for r in resources}
    assert types == {"reproduction", "raking_light"}


def test_build_download_url_from_service() -> None:
    resource = parse_manifest_resources(SAMPLE_MANIFEST, "x")[0]
    url = build_download_url(resource, None)
    assert url.endswith("/full/full/0/default.jpg")


def test_classify_canvas_uncertain_by_default() -> None:
    assert classify_canvas_label("1r (Q35-f. 1r)") == "mixed_or_uncertain"


def test_detect_jpeg_signature(tmp_path: Path) -> None:
    p = tmp_path / "x.jpg"
    p.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 12)
    assert detect_media_signature(p) == "jpeg"


def test_load_config_requires_approved_root_suffix(tmp_path: Path) -> None:
    config_path = Path(__file__).resolve().parents[1] / "scripts/acquisition/config/leipzig_0000061851.yaml"
    approved_root = tmp_path / "01-Projects" / "Logos"
    approved_root.mkdir(parents=True)
    cfg = load_config(config_path, "T479", approved_root)
    assert cfg.workspace_root == tmp_path
    assert cfg.ops_manifest_root == tmp_path / "08-AI-Operations" / "manifests" / "T479"

    wrong_root = tmp_path / "wrong-root"
    wrong_root.mkdir()
    with pytest.raises(ValueError, match="must end with"):
        load_config(config_path, "T479", wrong_root)


def test_storage_reserve_fails_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config_path = Path(__file__).resolve().parents[1] / "scripts/acquisition/config/leipzig_0000061851.yaml"
    approved_root = tmp_path / "01-Projects" / "Logos"
    approved_root.mkdir(parents=True)
    cfg = load_config(config_path, "T479", approved_root)
    monkeypatch.setattr(
        acquisition_core,
        "disk_free_bytes",
        lambda _path: cfg.minimum_free_reserve_bytes - 1,
    )
    with pytest.raises(RuntimeError, match="reserve breached"):
        ensure_storage_reserve(cfg)


def test_windows_adapter_verifies_unas_mapping() -> None:
    adapter = (
        Path(__file__).resolve().parents[1]
        / "scripts/acquisition/adapters/Invoke-LeipzigAcquisition.ps1"
    ).read_text(encoding="utf-8")
    assert "Get-PSDrive -Name Z" in adapter
    assert r"\\UNAS-Pro\AI.Workspace" in adapter
    assert "Join-Path $PSScriptRoot '../../..'" in adapter


def test_phase_validator_rejects_wrong_nas_root(tmp_path: Path) -> None:
    approved_root = tmp_path / "01-Projects" / "Logos"
    approved_root.mkdir(parents=True)
    validate_nas_root(approved_root)

    wrong_root = tmp_path / "wrong-root"
    wrong_root.mkdir()
    with pytest.raises(ValueError, match="must end with"):
        validate_nas_root(wrong_root)


def _test_runner(tmp_path: Path) -> AcquisitionRunner:
    config_path = Path(__file__).resolve().parents[1] / "scripts/acquisition/config/leipzig_0000061851.yaml"
    approved_root = tmp_path / "01-Projects" / "Logos"
    approved_root.mkdir(parents=True)
    cfg = load_config(config_path, "T479", approved_root)
    cfg.catalog_root.mkdir(parents=True)
    rights_path = tmp_path / "rights_ledger.yaml"
    rights_path.write_text(
        "rows:\n"
        "  - source_id: codex_sinaiticus_leipzig_iiif\n"
        "    decision: acquire\n",
        encoding="utf-8",
    )
    return AcquisitionRunner(cfg, rights_path)


@pytest.mark.parametrize("mutation", ["missing", "changed"])
def test_verify_rehashes_recorded_files(tmp_path: Path, mutation: str) -> None:
    runner = _test_runner(tmp_path)
    image = runner.cfg.source_originals_root / "images" / "resource.jpg"
    image.parent.mkdir(parents=True)
    image.write_bytes(b"original-image")
    event = {
        "local_relative_path": image.relative_to(runner.cfg.nas_root).as_posix(),
        "sha256": sha256_file(image),
    }
    runner._save_progress(
        ProgressState(
            run_id="test-run",
            started_at="2026-07-18T00:00:00+00:00",
            updated_at="2026-07-18T00:00:00+00:00",
            manifest_sha256="test-manifest",
            completed={"resource": event},
        )
    )
    captured = runner.cfg.staging_root / "iiif" / "manifest.captured.json"
    captured.parent.mkdir(parents=True, exist_ok=True)
    captured.write_text('{"sequences": []}\n', encoding="utf-8")

    if mutation == "missing":
        image.unlink()
    else:
        image.write_bytes(b"changed-image")

    result = runner.verify()
    assert result["completion_state"] == "incomplete_resumable"
    assert result["integrity_failure_count"] == 1
    expected_reason = "missing_file" if mutation == "missing" else "sha256_mismatch"
    assert result["integrity_failures"][0]["reason"] == expected_reason


def test_status_counts_failed_resource_as_remaining(tmp_path: Path) -> None:
    runner = _test_runner(tmp_path)
    captured = runner.cfg.staging_root / "iiif" / "manifest.captured.json"
    captured.parent.mkdir(parents=True, exist_ok=True)
    captured.write_text(json.dumps(SAMPLE_MANIFEST), encoding="utf-8")
    runner._save_progress(
        ProgressState(
            run_id="test-run",
            started_at="2026-07-18T00:00:00+00:00",
            updated_at="2026-07-18T00:00:00+00:00",
            manifest_sha256="test-manifest",
            failed={"failed-resource": {"reason": "transient"}},
        )
    )
    status = runner.status()
    assert status["failed"] == 1
    assert status["remaining"] == 2


def test_loading_progress_clears_stale_failure_after_success(tmp_path: Path) -> None:
    runner = _test_runner(tmp_path)
    event = {"local_relative_path": "source-originals/resource.jpg", "sha256": "abc"}
    runner._save_progress(
        ProgressState(
            run_id="test-run",
            started_at="2026-07-18T00:00:00+00:00",
            updated_at="2026-07-18T00:00:00+00:00",
            manifest_sha256="test-manifest",
            completed={"resource": event},
            failed={"resource": {"reason": "transient"}},
        )
    )
    assert runner._load_progress().failed == {}


def test_refresh_storage_ledger_remains_strict_json(tmp_path: Path) -> None:
    ledger = tmp_path / "storage_ledger.json"
    ledger.write_text(
        json.dumps({"task_id": "T479", "free_bytes_before": 100, "free_bytes_after": None}),
        encoding="utf-8",
    )
    refresh_storage_ledger_free_after(ledger, 90)
    parsed = json.loads(ledger.read_text(encoding="utf-8"))
    assert parsed["free_bytes_after"] == 90
