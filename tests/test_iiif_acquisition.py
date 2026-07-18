#!/usr/bin/env python3
"""Tests for IIIF acquisition core (no network)."""
from __future__ import annotations

from pathlib import Path

import pytest

import scripts.acquisition.iiif_acquisition_core as acquisition_core
from scripts.acquisition.validate_phase_completion import validate_nas_root
from scripts.acquisition.iiif_acquisition_core import (
    build_download_url,
    classify_canvas_label,
    detect_media_signature,
    ensure_storage_reserve,
    load_config,
    parse_manifest_resources,
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


def test_phase_validator_rejects_wrong_nas_root(tmp_path: Path) -> None:
    approved_root = tmp_path / "01-Projects" / "Logos"
    approved_root.mkdir(parents=True)
    validate_nas_root(approved_root)

    wrong_root = tmp_path / "wrong-root"
    wrong_root.mkdir()
    with pytest.raises(ValueError, match="must end with"):
        validate_nas_root(wrong_root)
