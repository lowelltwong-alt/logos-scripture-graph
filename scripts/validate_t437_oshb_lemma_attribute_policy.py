#!/usr/bin/env python3
"""Validate the T437 OSHB lemma-attribute policy-cover fix."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
ALLOWLIST = ROOT / ".ai" / "control" / "original_language_source_allowlist.yaml"
OSHB_SOURCE_MANIFEST = ROOT / "data" / "raw" / "original_language" / "hebrew" / "openscriptures_oshb" / "source_manifest.yaml"
OSHB_VIEW_MANIFEST = (
    ROOT
    / "data"
    / "candidate"
    / "original_language_evidence"
    / "canonical_source_views"
    / "openscriptures_oshb"
    / "canonical_source_view_manifest.yaml"
)
OSHB_INCLUDED = (
    ROOT
    / "data"
    / "candidate"
    / "original_language_evidence"
    / "canonical_source_views"
    / "openscriptures_oshb"
    / "included_files.jsonl"
)
T436_PARITY = (
    ROOT
    / "data"
    / "candidate"
    / "original_language_evidence"
    / "pilots"
    / "T436_jonah_hebrew_observation_parity"
    / "parity_summary.json"
)
CONTROL = ROOT / ".ai" / "control" / "t437_oshb_lemma_attribute_policy.yaml"
TASK = ROOT / ".ai" / "tasks" / "T437.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T437" / "handoff.md"
ROADMAP = ROOT / "docs" / "roadmap" / "T437_OSHB_LEMMA_ATTRIBUTE_POLICY.md"
DAD_PREFLIGHT = ROOT / ".ai" / "context" / "agent_work" / "T437" / "dad_preflight.md"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

POLICY = {
    "contains_source_provided_lemmas": False,
    "contains_source_provided_lemma_attributes": True,
    "contains_source_provided_strong_lookup_hints": True,
    "contains_source_provided_strongs": False,
    "lemma_attribute_interpretation": "strong_lookup_hint",
    "lemma_attribute_authority": "metadata_only_not_local_lemma_or_strong_authority",
}


class T437PolicyError(ValueError):
    """Raised when the T437 policy contract is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise T437PolicyError(f"{_rel(path)} unreadable YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise T437PolicyError(f"{_rel(path)} must be a YAML mapping")
    return data


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise T437PolicyError(f"{_rel(path)} unreadable JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise T437PolicyError(f"{_rel(path)} must be a JSON object")
    return data


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                if line.strip():
                    row = json.loads(line)
                    if not isinstance(row, dict):
                        raise T437PolicyError(f"{_rel(path)}:{line_no} must be a JSON object")
                    rows.append(row)
    except (OSError, json.JSONDecodeError) as exc:
        raise T437PolicyError(f"{_rel(path)} unreadable JSONL: {exc}") from exc
    return rows


def _require_policy(mapping: dict[str, Any], label: str) -> None:
    for key, expected in POLICY.items():
        if mapping.get(key) != expected:
            raise T437PolicyError(f"{label}.{key} must be {expected!r}, got {mapping.get(key)!r}")


def _oshb_allowlist_source(root: Path) -> dict[str, Any]:
    data = _read_yaml(root / ALLOWLIST.relative_to(ROOT))
    sources = data.get("sources")
    if not isinstance(sources, list):
        raise T437PolicyError("allowlist.sources must be a list")
    matches = [source for source in sources if isinstance(source, dict) and source.get("id") == "openscriptures_oshb"]
    if len(matches) != 1:
        raise T437PolicyError("allowlist must contain exactly one openscriptures_oshb source")
    return matches[0]


def validate_t436_policy_coverage(parity: dict[str, Any]) -> None:
    coverage = parity.get("metadata_policy_coverage")
    if not isinstance(coverage, dict):
        raise T437PolicyError("T436 parity summary metadata_policy_coverage missing")
    for key, expected in (
        ("manifest_contains_source_provided_lemmas", False),
        ("manifest_contains_source_provided_lemma_attributes", True),
        ("manifest_contains_source_provided_strong_lookup_hints", True),
        ("lemma_attribute_interpretation", "strong_lookup_hint"),
        ("lemma_attribute_authority", "metadata_only_not_local_lemma_or_strong_authority"),
        ("observed_lemma_attr_count", 688),
        ("policy_covers_observed_lemma_attribute", True),
        ("requires_policy_before_rust_expansion", False),
        ("requires_source_specific_parser_before_rust_expansion", True),
    ):
        if coverage.get(key) != expected:
            raise T437PolicyError(f"T436 parity coverage {key} must be {expected!r}")
    if parity.get("rust_expansion_allowed") is not False:
        raise T437PolicyError("T436/T437 still must not authorize Rust expansion")


def validate_t437_oshb_lemma_attribute_policy(root: Path = ROOT) -> dict[str, Any]:
    for path in (CONTROL, TASK, HANDOFF, ROADMAP, DAD_PREFLIGHT):
        local = root / path.relative_to(ROOT)
        if not local.exists():
            raise T437PolicyError(f"{_rel(local)} is missing")

    control = _read_yaml(root / CONTROL.relative_to(ROOT))
    if control.get("object_type") != "t437_oshb_lemma_attribute_policy":
        raise T437PolicyError("T437 control object_type is wrong")
    authority = control.get("authority")
    if not isinstance(authority, dict) or any(
        key.startswith("authorizes_") and value is not False for key, value in authority.items()
    ):
        raise T437PolicyError("T437 control authority flags must be false")

    _require_policy(_oshb_allowlist_source(root), "allowlist.openscriptures_oshb")
    _require_policy(_read_yaml(root / OSHB_SOURCE_MANIFEST.relative_to(ROOT)), "oshb_source_manifest")
    _require_policy(_read_yaml(root / OSHB_VIEW_MANIFEST.relative_to(ROOT)), "oshb_view_manifest")

    rows = _read_jsonl(root / OSHB_INCLUDED.relative_to(ROOT))
    if len(rows) != 39:
        raise T437PolicyError(f"OSHB included rows must be 39, got {len(rows)}")
    for row in rows:
        _require_policy(row, f"oshb_included.{row.get('book_id', '<missing-book>')}")

    validate_t436_policy_coverage(_read_json(root / T436_PARITY.relative_to(ROOT)))

    validate_all_text = (root / VALIDATE_ALL.relative_to(ROOT)).read_text(encoding="utf-8")
    if "validate_t437_oshb_lemma_attribute_policy.py" not in validate_all_text:
        raise T437PolicyError("validate_all.py must run the T437 validator")

    roadmap_text = (root / ROADMAP.relative_to(ROOT)).read_text(encoding="utf-8").lower()
    for phrase in ("strong lookup", "not local lemma", "no rust expansion", "no theology authority"):
        if phrase not in roadmap_text:
            raise T437PolicyError(f"{_rel(ROADMAP)} missing phrase {phrase!r}")

    return {"status": "pass", "oshb_included_rows": len(rows)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        validate_t437_oshb_lemma_attribute_policy(args.root.resolve())
    except T437PolicyError as exc:
        print(f"T437 OSHB lemma-attribute policy validation failed: {exc}", file=sys.stderr)
        return 1
    print("T437 OSHB lemma-attribute policy validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
