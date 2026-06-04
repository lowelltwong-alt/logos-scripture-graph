#!/usr/bin/env python3
"""Validate a source manifest and verify archive checksum when declared.

Dependency-light: parses YAML scalars line-by-line without PyYAML.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_KEYS = (
    "id",
    "source_family",
    "title",
    "language",
    "format",
    "license",
    "archive_path",
    "status",
)

SCALAR_RE = re.compile(r"^([A-Za-z0-9_]+):\s*(.*)$")
SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")


def parse_yaml_scalars(text: str) -> dict[str, str]:
    """Parse top-level scalar key/value pairs from a simple YAML file."""
    data: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = SCALAR_RE.match(stripped)
        if not match:
            continue
        key, raw_value = match.group(1), match.group(2).strip()
        if raw_value.startswith('"') and raw_value.endswith('"'):
            raw_value = raw_value[1:-1].replace('\\"', '"')
        elif raw_value.startswith("'") and raw_value.endswith("'"):
            raw_value = raw_value[1:-1]
        data[key] = raw_value
    return data


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_archive_path(manifest_path: Path, archive_path: str) -> Path:
    candidate = Path(archive_path)
    if candidate.is_absolute():
        return candidate
    return (ROOT / archive_path).resolve()


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_manifest.py <manifest.yaml>", file=sys.stderr)
        return 2

    manifest_path = Path(argv[1])
    if not manifest_path.exists():
        print(f"Missing manifest: {manifest_path}", file=sys.stderr)
        return 1

    text = manifest_path.read_text(encoding="utf-8")
    data = parse_yaml_scalars(text)
    failures: list[str] = []

    for key in REQUIRED_KEYS:
        if key not in data:
            failures.append(f"missing required key: {key}")

    sha256 = data.get("sha256", "")
    if sha256 and sha256 != "null":
        if not SHA256_RE.match(sha256):
            failures.append("sha256 must be 64 hex chars or null")
    elif data.get("status") not in {"raw_pending_checksum", "null", ""}:
        failures.append("sha256 is required when status is not raw_pending_checksum")

    archive_path = data.get("archive_path", "")
    if archive_path:
        archive = resolve_archive_path(manifest_path, archive_path)
        if not archive.exists():
            failures.append(f"archive not found: {archive_path}")
        elif sha256 and sha256 != "null" and SHA256_RE.match(sha256):
            actual = sha256_file(archive)
            if actual.lower() != sha256.lower():
                failures.append(
                    f"archive sha256 mismatch: manifest={sha256} actual={actual}"
                )

    if failures:
        print("MANIFEST VALIDATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Manifest validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
