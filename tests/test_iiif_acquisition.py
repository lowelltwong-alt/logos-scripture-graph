#!/usr/bin/env python3
"""Tests for IIIF acquisition core (no network)."""
from __future__ import annotations

from pathlib import Path

from scripts.acquisition.iiif_acquisition_core import (
    build_download_url,
    classify_canvas_label,
    detect_media_signature,
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
