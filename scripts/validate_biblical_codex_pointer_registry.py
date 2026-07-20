#!/usr/bin/env python3
"""Validate the metadata-only biblical codex pointer registry."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parent.parent
REGISTRY_ROOT = ROOT / "data" / "candidate" / "source_catalog" / "biblical_codex_pointers"
MANIFEST_PATH = REGISTRY_ROOT / "manifest.json"
FORBIDDEN_KEYS = {
    "text",
    "transcription",
    "translation",
    "ocr",
    "image_bytes",
    "local_path",
    "download_url",
}


class RegistryValidationError(ValueError):
    """Raised when the candidate pointer registry violates its contract."""


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RegistryValidationError(f"invalid JSON at {path.relative_to(ROOT)}: {exc}") from exc


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise RegistryValidationError(f"cannot read {path.relative_to(ROOT)}: {exc}") from exc
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            raise RegistryValidationError(f"blank JSONL line at {path.relative_to(ROOT)}:{line_number}")
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RegistryValidationError(
                f"invalid JSONL at {path.relative_to(ROOT)}:{line_number}: {exc}"
            ) from exc
        if not isinstance(row, dict):
            raise RegistryValidationError(f"record must be an object at {path.relative_to(ROOT)}:{line_number}")
        rows.append(row)
    return rows


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_registry() -> dict[str, Any]:
    manifest = _load_json(MANIFEST_PATH)
    schema_path = ROOT / manifest["schema_path"]
    schema = _load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    paths = {name: ROOT / rel for name, rel in manifest["files"].items()}
    roots = _load_jsonl(paths["catalog_roots"])
    direct = _load_jsonl(paths["direct_witnesses"])
    groups = {"catalog_roots": roots, "direct_witnesses": direct}
    rows = roots + direct

    expected_owner = manifest["repository_owner"]
    expected_lane = manifest["lane"]
    expected_prefix = "canonical:" if expected_lane == "canonical_66" else "boundary:"
    seen_ids: set[str] = set()
    mixed_count = 0

    for group_name, group_rows in groups.items():
        expected_type = "catalog_root_pointer" if group_name == "catalog_roots" else "direct_digital_copy_pointer"
        for index, row in enumerate(group_rows, start=1):
            errors = sorted(validator.iter_errors(row), key=lambda err: list(err.path))
            if errors:
                first = errors[0]
                location = ".".join(str(part) for part in first.path) or "<root>"
                raise RegistryValidationError(f"{group_name} row {index} schema error at {location}: {first.message}")
            pointer_id = row["pointer_id"]
            if pointer_id in seen_ids:
                raise RegistryValidationError(f"duplicate pointer_id: {pointer_id}")
            seen_ids.add(pointer_id)
            if not pointer_id.startswith(expected_prefix):
                raise RegistryValidationError(f"wrong identity namespace: {pointer_id}")
            if row["record_type"] != expected_type:
                raise RegistryValidationError(f"{pointer_id} is in the wrong JSONL file")
            if row["repository_owner"] != expected_owner or row["lane"] != expected_lane:
                raise RegistryValidationError(f"lane ownership mismatch: {pointer_id}")
            if row["download_authorized"] or row["rights_status"] != "not_reviewed_pointer_only":
                raise RegistryValidationError(f"rights authority leak: {pointer_id}")
            if row["item_level_complete"]:
                raise RegistryValidationError(f"unsupported completeness claim: {pointer_id}")
            forbidden = FORBIDDEN_KEYS.intersection(row)
            if forbidden:
                raise RegistryValidationError(f"forbidden payload field(s) in {pointer_id}: {sorted(forbidden)}")
            if row["content_scope"] == "mixed_physical_witness_split":
                mixed_count += 1
                if not row.get("companion_pointer_ids"):
                    raise RegistryValidationError(f"mixed witness lacks companion routing: {pointer_id}")

    counts = manifest["declared_counts"]
    observed = {"catalog_roots": len(roots), "direct_witnesses": len(direct), "total": len(rows)}
    if counts != observed:
        raise RegistryValidationError(f"declared count mismatch: declared={counts}, observed={observed}")

    expected_hashes = manifest["fingerprints"]
    observed_hashes = {
        "schema_sha256": _sha256(schema_path),
        "catalog_roots_sha256": _sha256(paths["catalog_roots"]),
        "direct_witnesses_sha256": _sha256(paths["direct_witnesses"]),
    }
    if expected_hashes != observed_hashes:
        raise RegistryValidationError(
            f"fingerprint mismatch: declared={expected_hashes}, observed={observed_hashes}"
        )
    if manifest["coverage"]["item_level_complete"]:
        raise RegistryValidationError("manifest may not claim item-level completeness")
    if manifest["authority"]["authorizes_downloads"] or manifest["authority"]["authorizes_reuse"]:
        raise RegistryValidationError("manifest leaks rights authority")

    return {"status": "valid", "counts": observed, "mixed_witness_rows": mixed_count}


def main() -> int:
    try:
        result = validate_registry()
    except (KeyError, OSError, RegistryValidationError) as exc:
        print(f"Biblical codex pointer registry validation failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
