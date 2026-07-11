#!/usr/bin/env python3
"""Fail-closed validation for the W1-W4 pre-download readiness packet."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PACKET = ROOT / "data" / "candidate" / "source_catalog" / "primary_bible_witnesses" / "pre_download_readiness.yaml"

REQUIRED_PREREQUISITES = {
    "LOGOS_EXTERNAL_ASSET_ROOT exists outside Git, OneDrive, workspace, and temp paths",
    "external root has at least 50 GB free",
    "validate_external_asset_root.py passes",
    "per-source license snapshot, URL, expected size, and SHA-256 are recorded before download",
    "guard_primary_witness_acquisition.py passes for each unit",
    "every artifact remains outside Git and all canonical/graph/retrieval/vector paths",
}

EXPECTED_WAVES = {
    "W1": {"readiness": "storage_blocked_only", "sources": {"codex_sinaiticus_xml", "clementine_vulgate", "swete_lxx"}},
    "W2": {"readiness": "storage_blocked_only", "sources": {"leningrad_codex_color_images", "codex_sassoon_1053_color_images", "bl_or_4445_torah", "biblia_sacra_vulgatae_1592"}},
    "W3": {"readiness": "permission_pending", "sources": {"codex_sinaiticus_images", "codex_vaticanus", "great_isaiah_scroll_1qisa", "codex_alexandrinus", "csntm_papyri"}},
    "W4": {"readiness": "catalog_disposition_complete", "sources": {"leiden_peshitta_electronic", "samaritan_pentateuch_manchester", "sahidic_coptic_old_testament"}},
}

REQUIRED_NON_AUTHORIZATIONS = {
    "download_now",
    "source_text_import",
    "OCR_now",
    "embeddings",
    "vector_indexes",
    "graph_truth",
    "preferred_readings",
    "theology_authority",
}


def _load_packet() -> dict[str, Any]:
    data = yaml.safe_load(PACKET.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("pre-download readiness packet must be a mapping")
    return data


def validate_pre_download_readiness() -> dict[str, Any]:
    packet = _load_packet()
    errors: list[str] = []

    if packet.get("object_type") != "primary_witness_pre_download_readiness":
        errors.append("object_type must be primary_witness_pre_download_readiness")
    if packet.get("binary_acquisition_authorized") is not False:
        errors.append("binary_acquisition_authorized must remain false")
    if set(packet.get("global_prerequisites", [])) != REQUIRED_PREREQUISITES:
        errors.append("global_prerequisites must match the required storage and rights gates")
    if set(packet.get("non_authorizations", [])) != REQUIRED_NON_AUTHORIZATIONS:
        errors.append("non_authorizations must preserve every prohibited downstream use")

    layout = packet.get("quarantine_layout")
    if not isinstance(layout, dict) or layout.get("root") != "LOGOS_EXTERNAL_ASSET_ROOT/primary_witnesses/":
        errors.append("quarantine_layout.root must be under LOGOS_EXTERNAL_ASSET_ROOT/primary_witnesses/")
    if not isinstance(layout, dict) or layout.get("metadata_journal") != "acquisition_journal.jsonl":
        errors.append("quarantine_layout must require acquisition_journal.jsonl")

    waves = packet.get("waves")
    if not isinstance(waves, dict) or set(waves) != set(EXPECTED_WAVES):
        errors.append("waves must contain exactly W1, W2, W3, and W4")
        waves = {}
    for wave_name, expected in EXPECTED_WAVES.items():
        wave = waves.get(wave_name, {})
        if wave.get("readiness") != expected["readiness"]:
            errors.append(f"{wave_name}.readiness must be {expected['readiness']}")
        units = wave.get("units", [])
        if not isinstance(units, list):
            errors.append(f"{wave_name}.units must be a list")
            continue
        source_ids = {unit.get("source_id") for unit in units if isinstance(unit, dict)}
        if source_ids != expected["sources"]:
            errors.append(f"{wave_name}.units must contain the expected source IDs")
        for unit in units:
            if not isinstance(unit, dict):
                errors.append(f"{wave_name}.units entries must be mappings")
                continue
            if not unit.get("gate"):
                errors.append(f"{wave_name} source {unit.get('source_id')} is missing its gate")
            target = unit.get("target")
            if wave_name in {"W1", "W2"}:
                if not isinstance(target, str) or not target or target.startswith(("/", "\\")) or ".." in target:
                    errors.append(f"{wave_name} source {unit.get('source_id')} needs a safe relative quarantine target")
            elif target is not None:
                errors.append(f"{wave_name} source {unit.get('source_id')} must not declare a local target before permission/route review")

    return {"validator": "validate_pre_download_readiness", "packet": str(PACKET.relative_to(ROOT)), "errors": errors, "ok": not errors}


def main() -> int:
    result = validate_pre_download_readiness()
    if result["errors"]:
        for error in result["errors"]:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK {result['validator']} packet={result['packet']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
