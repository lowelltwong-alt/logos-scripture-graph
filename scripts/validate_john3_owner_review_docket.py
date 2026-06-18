#!/usr/bin/env python3
"""Validate the John 3 WJ owner-review docket."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCKET = ROOT / ".ai" / "control" / "john3_wj_owner_review_docket.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T356_JOHN3_WJ_OWNER_REVIEW_DOCKET.md"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS_MAP = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
T356_TASK = ROOT / ".ai" / "tasks" / "T356.task.yaml"

REQUIRED_OPTIONS = {
    "JOHN3-T356-A",
    "JOHN3-T356-B",
    "JOHN3-T356-C",
    "JOHN3-T356-D",
    "JOHN3-T356-E",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_jesus_speaker_attribution",
    "authorizes_speaker_boundary",
    "authorizes_discourse_boundary",
    "authorizes_parent_span",
    "authorizes_child_spans",
    "authorizes_reviewed_gold",
    "authorizes_chunk_boundaries",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_output_change",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "john3_parent_span_approval",
    "john3_child_span_approval",
    "john3_jesus_speaker_attribution",
    "john3_narrator_boundary_decision",
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


class John3DocketError(ValueError):
    """Raised when the John 3 owner-review docket is stale or authorizing."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise John3DocketError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise John3DocketError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise John3DocketError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _extract_markdown_yaml(path: Path, required_key: str) -> dict[str, Any]:
    text = _read_text(path)
    blocks = re.findall(r"```yaml\s*\n(.*?)\n```", text, flags=re.DOTALL)
    for block in blocks:
        try:
            data = yaml.safe_load(block)
        except yaml.YAMLError as exc:
            raise John3DocketError(f"{_rel(path)}: fenced YAML unreadable: {exc}") from exc
        if isinstance(data, dict) and required_key in data:
            value = data[required_key]
            if not isinstance(value, dict):
                raise John3DocketError(f"{_rel(path)}: {required_key} must be a mapping")
            return value
    raise John3DocketError(f"{_rel(path)}: missing fenced YAML key {required_key}")


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise John3DocketError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise John3DocketError(f"{label} missing {missing}")


def _validate_docket(data: dict[str, Any], path: Path) -> None:
    if data.get("object_type") != "john3_wj_owner_review_docket":
        raise John3DocketError(f"{_rel(path)}: object_type must be john3_wj_owner_review_docket")
    if data.get("trust_zone") != "canonical":
        raise John3DocketError(f"{_rel(path)}: trust_zone must be canonical")
    if data.get("lifecycle_status") != "active":
        raise John3DocketError(f"{_rel(path)}: lifecycle_status must be active")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise John3DocketError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_owner_review_options") is not True:
        raise John3DocketError(f"{_rel(path)}: authority.records_owner_review_options must be true")
    if authority.get("may_surface_for_review") is not True:
        raise John3DocketError(f"{_rel(path)}: authority.may_surface_for_review must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise John3DocketError(f"{_rel(path)}: authority.{key} must be false")

    target = data.get("target")
    if not isinstance(target, dict):
        raise John3DocketError(f"{_rel(path)}: target must be a mapping")
    expected_target = {
        "target_id": "john3_wj_speaker_boundary",
        "passage": "John.3.1-John.3.36",
        "review_packet": "eval/chunking_gold/review_packets/john3_wj_speaker_boundary_review.md",
        "prior_policy_task": "T355",
        "owner_review_task": "T356",
        "status": "owner_selection_pending",
    }
    for key, value in expected_target.items():
        if target.get(key) != value:
            raise John3DocketError(f"{_rel(path)}: target.{key} must be {value}")

    selection = data.get("owner_selection")
    if not isinstance(selection, dict):
        raise John3DocketError(f"{_rel(path)}: owner_selection must be a mapping")
    if selection.get("owner_selection_status") != "pending":
        raise John3DocketError(f"{_rel(path)}: owner_selection_status must be pending")
    if selection.get("selected_option") != "pending":
        raise John3DocketError(f"{_rel(path)}: selected_option must be pending")
    for key in ("implementation_allowed", "output_change_authorized", "reviewed_gold_promoted"):
        if selection.get(key) is not False:
            raise John3DocketError(f"{_rel(path)}: owner_selection.{key} must be false")

    option_ids = {
        str(item.get("option_id"))
        for item in data.get("options", [])
        if isinstance(item, dict)
    }
    missing_options = sorted(REQUIRED_OPTIONS - option_ids)
    if missing_options:
        raise John3DocketError(f"{_rel(path)}: missing owner options {missing_options}")
    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data.get("non_authorizations"), "non_authorizations")


def _validate_roadmap_doc() -> None:
    text = _read_text(ROADMAP_DOC)
    for phrase in (
        "owner_selection_status: pending",
        "selected_option: pending",
        "JOHN3-T356-A",
        "JOHN3-T356-B",
        "JOHN3-T356-C",
        "JOHN3-T356-D",
        "JOHN3-T356-E",
        "John.3.9-John.3.21",
        "This docket does not authorize",
    ):
        if phrase not in text:
            raise John3DocketError(f"{_rel(ROADMAP_DOC)}: missing phrase {phrase!r}")
    decision_box = _extract_markdown_yaml(ROADMAP_DOC, "john3_owner_review")
    if decision_box.get("owner_selection_status") != "pending":
        raise John3DocketError(f"{_rel(ROADMAP_DOC)}: decision box owner_selection_status must be pending")
    if decision_box.get("selected_option") != "pending":
        raise John3DocketError(f"{_rel(ROADMAP_DOC)}: decision box selected_option must be pending")
    for key in ("implementation_allowed", "output_change_authorized", "reviewed_gold_promoted"):
        if decision_box.get(key) is not False:
            raise John3DocketError(f"{_rel(ROADMAP_DOC)}: decision box {key} must be false")


def _validate_governed_links() -> None:
    register = _read_yaml(REGISTER)
    cd023 = next(
        (
            item
            for item in register.get("decisions", [])
            if isinstance(item, dict) and item.get("decision_id") == "CD-023"
        ),
        None,
    )
    if not isinstance(cd023, dict):
        raise John3DocketError(f"{_rel(REGISTER)}: missing CD-023")
    for validator in ("scripts/validate_john3_owner_review_docket.py", "tests/test_john3_owner_review_docket.py"):
        if validator not in cd023.get("validators", []):
            raise John3DocketError(f"{_rel(REGISTER)}: CD-023 validators missing {validator}")

    preflight = _read_yaml(PREFLIGHT)
    reading_paths = {
        str(item.get("path"))
        for item in preflight.get("mandatory_reading", [])
        if isinstance(item, dict)
    }
    if ".ai/control/john3_wj_owner_review_docket.yaml" not in reading_paths:
        raise John3DocketError(f"{_rel(PREFLIGHT)}: John 3 docket must be mandatory reading")

    readiness = _read_yaml(READINESS_MAP)
    next_route = readiness.get("next_route")
    if not isinstance(next_route, dict):
        raise John3DocketError(f"{_rel(READINESS_MAP)}: next_route must be a mapping")
    expected = {
        "task_id": "T356",
        "route_type": "john3_wj_owner_review_docket",
        "selected_target": "john3_wj_speaker_boundary",
        "john3_owner_selection_status": "pending",
        "john3_selected_option": "pending",
        "docket": ".ai/control/john3_wj_owner_review_docket.yaml",
        "review_packet": "eval/chunking_gold/review_packets/john3_wj_speaker_boundary_review.md",
    }
    for key, value in expected.items():
        if next_route.get(key) != value:
            raise John3DocketError(f"{_rel(READINESS_MAP)}: next_route.{key} must be {value}")
    for key in ("output_change_authorized", "implementation_authorized", "reviewed_gold_promoted"):
        if next_route.get(key) is not False:
            raise John3DocketError(f"{_rel(READINESS_MAP)}: next_route.{key} must be false")

    if not T356_TASK.exists():
        raise John3DocketError(f"{_rel(T356_TASK)}: T356 task file is missing")


def validate_john3_owner_review_docket(path: Path = DOCKET) -> dict[str, Any]:
    data = _read_yaml(path)
    _validate_docket(data, path)
    _validate_roadmap_doc()
    _validate_governed_links()
    return data


def main() -> int:
    try:
        validate_john3_owner_review_docket()
    except John3DocketError as exc:
        print(f"John 3 owner-review docket validation failed: {exc}", file=sys.stderr)
        return 1
    print("John 3 owner-review docket validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
