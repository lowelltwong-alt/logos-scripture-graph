#!/usr/bin/env python3
"""Validate chunking gold manifest maturity and structural-split metadata."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST_DIR = ROOT / "eval" / "chunking_gold" / "per_form"

REVIEWED_STATUSES = {
    "reviewed_gold",
    "approved_structural_split_under_parent_whole_psalm",
}
NON_PROMOTED_STATUSES = {
    "characterization_only",
    "pending_human_review",
}
FORBIDDEN_NON_PROMOTED_FLAGS = {
    "approved_expected_output",
    "authorizes_output_change",
    "not_bad_fragmentation_gold",
    "reviewed_structural_split",
}


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _load_json(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - exact parser text is not stable.
        return None, [f"{_rel(path)}: invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return None, [f"{_rel(path)}: manifest root must be an object"]
    return data, []


def _bool_flag(value: Any) -> bool:
    return value is True


def _contains_promoted_flag(value: Any) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_NON_PROMOTED_FLAGS and _bool_flag(child):
                return True
            if _contains_promoted_flag(child):
                return True
    elif isinstance(value, list):
        return any(_contains_promoted_flag(child) for child in value)
    return False


def _validate_span_object(
    obj: Any,
    *,
    path: Path,
    case_id: str,
    field: str,
    failures: list[str],
) -> None:
    if not isinstance(obj, dict):
        failures.append(f"{_rel(path)}:{case_id}: {field} must be an object")
        return
    for key in ("osis_start", "osis_end"):
        if not isinstance(obj.get(key), str) or not obj[key]:
            failures.append(f"{_rel(path)}:{case_id}: {field}.{key} is required")


def _validate_structural_split(path: Path, case: dict[str, Any], failures: list[str]) -> None:
    case_id = str(case.get("case_id", "<missing-case-id>"))
    _validate_span_object(
        case.get("parent_literary_unit"),
        path=path,
        case_id=case_id,
        field="parent_literary_unit",
        failures=failures,
    )
    expected = case.get("expected")
    if not isinstance(expected, dict):
        failures.append(f"{_rel(path)}:{case_id}: expected object is required")
        return
    if expected.get("reviewed_structural_split") is not True:
        failures.append(f"{_rel(path)}:{case_id}: expected.reviewed_structural_split must be true")
    if expected.get("not_bad_fragmentation_gold") is not True:
        failures.append(f"{_rel(path)}:{case_id}: expected.not_bad_fragmentation_gold must be true")
    child_chunks = expected.get("child_chunks")
    if not isinstance(child_chunks, list) or not child_chunks:
        failures.append(f"{_rel(path)}:{case_id}: expected.child_chunks must be a non-empty list")
        return
    for idx, child in enumerate(child_chunks):
        _validate_span_object(
            child,
            path=path,
            case_id=case_id,
            field=f"expected.child_chunks[{idx}]",
            failures=failures,
        )


def _validate_case(path: Path, section: str, case: Any, failures: list[str]) -> None:
    if not isinstance(case, dict):
        failures.append(f"{_rel(path)}:{section}: each case must be an object")
        return
    case_id = case.get("case_id")
    if not isinstance(case_id, str) or not case_id:
        failures.append(f"{_rel(path)}:{section}: case_id is required")
        case_id = "<missing-case-id>"
    status = case.get("status")
    if not isinstance(status, str) or not status:
        failures.append(f"{_rel(path)}:{case_id}: explicit status is required")
        return

    if section == "reviewed_gold":
        if status in NON_PROMOTED_STATUSES:
            failures.append(f"{_rel(path)}:{case_id}: {status} cannot live under reviewed_gold")
        elif status not in REVIEWED_STATUSES:
            failures.append(f"{_rel(path)}:{case_id}: unsupported reviewed status {status!r}")
    elif section == "characterization_only":
        if status not in NON_PROMOTED_STATUSES:
            failures.append(f"{_rel(path)}:{case_id}: characterization_only case has promoted status {status!r}")
        if _contains_promoted_flag(case):
            failures.append(
                f"{_rel(path)}:{case_id}: characterization/pending cases must not carry promoted-output flags"
            )

    if status == "approved_structural_split_under_parent_whole_psalm":
        _validate_structural_split(path, case, failures)


def validate_manifest(path: Path) -> list[str]:
    manifest, failures = _load_json(path)
    if manifest is None:
        return failures

    for key in ("schema_version", "manifest_id", "target_form", "promotion_status"):
        if not isinstance(manifest.get(key), str) or not manifest[key]:
            failures.append(f"{_rel(path)}: {key} is required")

    for section in ("reviewed_gold", "characterization_only"):
        cases = manifest.get(section)
        if cases is None:
            failures.append(f"{_rel(path)}: {section} array is required")
            continue
        if not isinstance(cases, list):
            failures.append(f"{_rel(path)}: {section} must be an array")
            continue
        for case in cases:
            _validate_case(path, section, case, failures)

    return failures


def manifest_paths(root: Path = DEFAULT_MANIFEST_DIR) -> list[Path]:
    if root.is_file():
        return [root]
    if not root.exists():
        return []
    return sorted(root.glob("*_manifest.json"))


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    roots = [Path(arg) for arg in argv] if argv else [DEFAULT_MANIFEST_DIR]
    manifests: list[Path] = []
    for root in roots:
        manifests.extend(manifest_paths(root))

    failures: list[str] = []
    for path in manifests:
        failures.extend(validate_manifest(path))

    if failures:
        print("CHUNKING GOLD VALIDATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Chunking gold validation passed for {len(manifests)} manifest(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
