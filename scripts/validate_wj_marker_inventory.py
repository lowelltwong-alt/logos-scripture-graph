#!/usr/bin/env python3
"""Validate the words-of-Jesus marker inventory."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_wj_marker_inventory import KNOWN_WJ_CASE_IDS, OUTPUT, build_inventory

REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_jesus_speaker_attribution",
    "authorizes_speaker_boundary",
    "authorizes_discourse_boundary",
    "authorizes_chunk_boundaries",
    "authorizes_reviewed_gold",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_output_change",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "wj_marker_as_speaker_authority",
    "wj_marker_as_speaker_boundary",
    "wj_marker_as_discourse_boundary",
    "wj_marker_as_chunk_boundary",
    "wj_marker_as_reviewed_gold",
    "wj_marker_as_graph_edge",
    "wj_marker_as_retrieval_truth",
    "wj_marker_as_output_change",
    "red_letter_markup_as_theological_truth",
}

REQUIRED_BOOK_COUNTS = {
    "Matt": 12296,
    "Mark": 4802,
    "Luke": 11009,
    "John": 7738,
    "Acts": 474,
    "1Cor": 33,
    "2Cor": 11,
    "1Tim": 6,
    "Rev": 1725,
}


class WJMarkerInventoryError(ValueError):
    """Raised when the WJ marker inventory is missing, stale, or authorizing."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
        if text.startswith("---\n"):
            parts = text.split("---\n", 2)
            if len(parts) == 3:
                text = parts[1] + "\n" + parts[2]
        data = yaml.safe_load(text)
    except (OSError, yaml.YAMLError) as exc:
        raise WJMarkerInventoryError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise WJMarkerInventoryError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _validate_non_authorizing(data: dict[str, Any], path: Path) -> None:
    if data.get("object_type") != "wj_marker_inventory":
        raise WJMarkerInventoryError(f"{_rel(path)}: object_type must be wj_marker_inventory")
    if data.get("trust_zone") != "canonical":
        raise WJMarkerInventoryError(f"{_rel(path)}: trust_zone must be canonical")
    if data.get("lifecycle_status") != "active":
        raise WJMarkerInventoryError(f"{_rel(path)}: lifecycle_status must be active")
    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise WJMarkerInventoryError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_source_observations") is not True:
        raise WJMarkerInventoryError(f"{_rel(path)}: authority.records_source_observations must be true")
    if authority.get("may_surface_for_review") is not True:
        raise WJMarkerInventoryError(f"{_rel(path)}: authority.may_surface_for_review must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise WJMarkerInventoryError(f"{_rel(path)}: authority.{key} must be false")
    missing_non_auth = sorted(REQUIRED_NON_AUTHORIZATIONS - set(data.get("non_authorizations", [])))
    if missing_non_auth:
        raise WJMarkerInventoryError(f"{_rel(path)}: missing non_authorizations {missing_non_auth}")


def _validate_required_observations(data: dict[str, Any], path: Path) -> None:
    summary = data.get("summary")
    if not isinstance(summary, dict):
        raise WJMarkerInventoryError(f"{_rel(path)}: summary must be a mapping")
    if summary.get("wj_word_tokens") != 38094:
        raise WJMarkerInventoryError(f"{_rel(path)}: summary.wj_word_tokens must be 38094")
    if summary.get("wj_token_runs") != 675:
        raise WJMarkerInventoryError(f"{_rel(path)}: summary.wj_token_runs must be 675")
    if set(summary.get("books_with_wj", [])) != set(REQUIRED_BOOK_COUNTS):
        raise WJMarkerInventoryError(f"{_rel(path)}: books_with_wj mismatch")

    book_summaries = {
        str(item.get("book")): item
        for item in data.get("book_summaries", [])
        if isinstance(item, dict)
    }
    for book, expected_count in REQUIRED_BOOK_COUNTS.items():
        entry = book_summaries.get(book)
        if not isinstance(entry, dict):
            raise WJMarkerInventoryError(f"{_rel(path)}: missing book summary {book}")
        if entry.get("wj_word_tokens") != expected_count:
            raise WJMarkerInventoryError(f"{_rel(path)}: {book} wj_word_tokens must be {expected_count}")
        if int(entry.get("wj_token_runs", 0)) <= 0:
            raise WJMarkerInventoryError(f"{_rel(path)}: {book} must have WJ token runs")

    runs = data.get("wj_token_runs")
    if not isinstance(runs, list) or len(runs) != 675:
        raise WJMarkerInventoryError(f"{_rel(path)}: wj_token_runs must contain 675 runs")
    required_contiguous_runs = {
        ("Matt.5.3", "Matt.7.27"),
        ("Rev.1.17", "Rev.3.22"),
    }
    required_split_review_runs = {
        ("John.3.3", "John.3.3"),
        ("John.3.5", "John.3.8"),
        ("John.3.10", "John.3.21"),
        ("John.13.31", "John.13.35"),
        ("John.14.23", "John.16.16"),
        ("John.17.1", "John.17.26"),
    }
    observed_runs = {(str(run.get("start_ref")), str(run.get("end_ref"))) for run in runs if isinstance(run, dict)}
    missing_runs = sorted((required_contiguous_runs | required_split_review_runs) - observed_runs)
    if missing_runs:
        raise WJMarkerInventoryError(f"{_rel(path)}: missing expected WJ runs {missing_runs}")

    cases = {
        str(item.get("case_id")): item
        for item in data.get("known_review_cases", [])
        if isinstance(item, dict)
    }
    missing_cases = sorted(KNOWN_WJ_CASE_IDS - set(cases))
    if missing_cases:
        raise WJMarkerInventoryError(f"{_rel(path)}: missing known WJ cases {missing_cases}")
    for case_id, entry in cases.items():
        if entry.get("implementation_allowed") is not False:
            raise WJMarkerInventoryError(f"{_rel(path)}: {case_id}.implementation_allowed must be false")
        if int(entry.get("wj_word_token_refs_count", 0)) <= 0:
            raise WJMarkerInventoryError(f"{_rel(path)}: {case_id} must have WJ evidence refs")


def _validate_inventory_is_current(data: dict[str, Any], path: Path) -> None:
    expected = build_inventory()
    if data != expected:
        raise WJMarkerInventoryError(f"{_rel(path)} is stale; run python scripts/build_wj_marker_inventory.py --write")


def _validate_governed_links() -> None:
    register = _read_yaml(REGISTER)
    decisions = register.get("decisions")
    if not isinstance(decisions, list):
        raise WJMarkerInventoryError(f"{_rel(REGISTER)}: decisions must be a list")
    cd021 = next((item for item in decisions if isinstance(item, dict) and item.get("decision_id") == "CD-021"), None)
    if not isinstance(cd021, dict):
        raise WJMarkerInventoryError(f"{_rel(REGISTER)}: missing CD-021")
    for validator in ("scripts/validate_wj_marker_inventory.py", "tests/test_wj_marker_inventory.py"):
        if validator not in cd021.get("validators", []):
            raise WJMarkerInventoryError(f"{_rel(REGISTER)}: CD-021 validators missing {validator}")
    preflight = _read_yaml(PREFLIGHT)
    reading_paths = {
        str(item.get("path"))
        for item in preflight.get("mandatory_reading", [])
        if isinstance(item, dict)
    }
    if ".ai/control/wj_marker_inventory.yaml" not in reading_paths:
        raise WJMarkerInventoryError(f"{_rel(PREFLIGHT)}: WJ inventory must be mandatory reading")


def validate_wj_marker_inventory(path: Path = OUTPUT) -> dict[str, Any]:
    data = _read_yaml(path)
    _validate_non_authorizing(data, path)
    _validate_required_observations(data, path)
    _validate_inventory_is_current(data, path)
    _validate_governed_links()
    return data


def main() -> int:
    try:
        validate_wj_marker_inventory()
    except WJMarkerInventoryError as exc:
        print(f"WJ marker inventory validation failed: {exc}", file=sys.stderr)
        return 1
    print("WJ marker inventory validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
