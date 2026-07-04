#!/usr/bin/env python3
"""Validate the T430/T431 original-language evidence substrate controls."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / ".ai" / "control" / "original_language_evidence_substrate.yaml"
ALLOWLIST = ROOT / ".ai" / "control" / "original_language_source_allowlist.yaml"
ROADMAP = ROOT / "docs" / "roadmap" / "T431_ORIGINAL_LANGUAGE_RAW_INTAKE.md"
DAD_PREFLIGHT = ROOT / ".ai" / "context" / "agent_work" / "T431" / "dad_preflight.md"

FALSE_AUTHORITY = {
    "authorizes_source_language_truth",
    "authorizes_lexical_truth",
    "authorizes_source_text_mutation",
    "authorizes_strongs_overlay_in_raw",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_textual_critical_decision",
    "authorizes_canon_scope_change",
    "authorizes_translation_judgment",
    "authorizes_chunk_boundaries",
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_route_behavior",
    "authorizes_evaluator_behavior",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embeddings_or_indexes",
    "authorizes_theology_authority",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "source_language_truth",
    "lexical_truth",
    "isolated_word_theology",
    "strongs_number_as_source_text",
    "strongs_number_as_theology_authority",
    "source_text_mutation",
    "preferred_reading",
    "source_tradition_preference",
    "oldest_witness_as_automatic_authority",
    "manuscript_catalog_as_transcription_authority",
    "punctuation_as_autograph_certainty",
    "red_letter_as_original_speaker_authority",
    "translation_judgment",
    "canon_scope_change",
    "chunk_boundary",
    "reviewed_gold",
    "chunk_output",
    "graph_edge",
    "retrieval_truth",
}


class T430EvidenceSubstrateError(ValueError):
    """Raised when T430/T431 controls are invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise T430EvidenceSubstrateError(f"{_rel(path)}: unreadable YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise T430EvidenceSubstrateError(f"{_rel(path)}: expected YAML mapping")
    return data


def _require_false(mapping: dict[str, Any], keys: set[str], label: str) -> None:
    for key in sorted(keys):
        if mapping.get(key) is not False:
            raise T430EvidenceSubstrateError(f"{label}.{key} must be false")


def validate_t430_original_language_evidence_substrate(root: Path = ROOT) -> dict[str, Any]:
    control = _read_yaml(root / CONTROL.relative_to(ROOT))
    if control.get("object_type") != "original_language_evidence_substrate":
        raise T430EvidenceSubstrateError("original_language_evidence_substrate object_type is wrong")
    if control.get("schema_version") != "original_language_evidence_substrate.v1":
        raise T430EvidenceSubstrateError("original_language_evidence_substrate schema_version is wrong")
    authority = control.get("authority")
    if not isinstance(authority, dict):
        raise T430EvidenceSubstrateError("authority must be a mapping")
    if authority.get("authorizes_allowlisted_raw_downloads_via_t431") is not True:
        raise T430EvidenceSubstrateError("T431 allowlisted raw download flag must be true")
    _require_false(authority, FALSE_AUTHORITY, "authority")
    non_auth = control.get("non_authorizations")
    if not isinstance(non_auth, list):
        raise T430EvidenceSubstrateError("non_authorizations must be a list")
    missing = sorted(REQUIRED_NON_AUTHORIZATIONS - {str(item) for item in non_auth})
    if missing:
        raise T430EvidenceSubstrateError(f"non_authorizations missing {missing}")
    layers = control.get("evidence_layers")
    if not isinstance(layers, list) or not layers:
        raise T430EvidenceSubstrateError("evidence_layers must be a non-empty list")
    layer_ids = {str(layer.get("layer_id")) for layer in layers if isinstance(layer, dict)}
    for required in ("source_text_archive", "canonical_source_view", "strongs_alignment", "textual_variants", "manuscript_witness_support", "editorial_layers"):
        if required not in layer_ids:
            raise T430EvidenceSubstrateError(f"missing evidence layer {required}")
    allowlist = _read_yaml(root / ALLOWLIST.relative_to(ROOT))
    if allowlist.get("object_type") != "original_language_source_allowlist":
        raise T430EvidenceSubstrateError("allowlist object_type is wrong")
    dad = root / DAD_PREFLIGHT.relative_to(ROOT)
    if not dad.exists() or "dad_bridge_not_present_on_origin_main" not in dad.read_text(encoding="utf-8"):
        raise T430EvidenceSubstrateError("T431 DAD preflight record is missing or incomplete")
    roadmap = root / ROADMAP.relative_to(ROOT)
    text = roadmap.read_text(encoding="utf-8").lower()
    for phrase in (
        "strong's",
        "oldest witness",
        "editorial layers",
        "never silently normalized",
        "no preferred readings",
    ):
        if phrase not in text:
            raise T430EvidenceSubstrateError(f"{_rel(roadmap)} missing phrase {phrase!r}")
    return control


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        validate_t430_original_language_evidence_substrate(args.root.resolve())
    except T430EvidenceSubstrateError as exc:
        print(f"T430 original-language evidence substrate validation failed: {exc}", file=sys.stderr)
        return 1
    print("T430 original-language evidence substrate validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
