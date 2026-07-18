#!/usr/bin/env python3
"""Phase 6 completion validator for T479 acquisition artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_CATALOG_ARTIFACTS = (
    "rights_ledger.yaml",
    "codex_catalog.jsonl",
    "source_inventory.jsonl",
    "canvas_resource_map.jsonl",
    "SHA256SUMS",
    "acquisition_receipt.json",
    "transfer_events.jsonl",
    "collision_and_failure_report.jsonl",
    "residual_report.json",
    "storage_ledger.json",
    "manifest_capture.json",
    "permission_review_queue.jsonl",
    "phase_completion_report.json",
)

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".jpx", ".jp2", ".png", ".tif", ".tiff", ".bin"}
REQUIRED_NAS_ROOT_SUFFIX = ("01-Projects", "Logos")


def validate_nas_root(nas_root: Path) -> None:
    actual_parts = tuple(part.casefold() for part in nas_root.parts)
    expected_parts = tuple(part.casefold() for part in REQUIRED_NAS_ROOT_SUFFIX)
    if len(actual_parts) < len(expected_parts) or actual_parts[-len(expected_parts) :] != expected_parts:
        raise ValueError(f"NAS root must end with {'/'.join(REQUIRED_NAS_ROOT_SUFFIX)}: {nas_root}")
    if not nas_root.is_dir():
        raise ValueError(f"NAS root does not exist or is not a directory: {nas_root}")

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return rows
    for line in text.splitlines():
        rows.append(json.loads(line))
    return rows


def validate_catalog_artifacts(catalog_root: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_CATALOG_ARTIFACTS:
        path = catalog_root / name
        if not path.exists():
            errors.append(f"missing artifact: {name}")
            continue
        try:
            if name.endswith(".json"):
                json.loads(path.read_text(encoding="utf-8"))
            elif name.endswith(".jsonl"):
                parse_jsonl(path)
            elif name.endswith(".yaml"):
                yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"parse failed for {name}: {exc}")
    return errors


def validate_sha256sums(catalog_root: Path, nas_root: Path) -> list[str]:
    errors: list[str] = []
    sums_path = catalog_root / "SHA256SUMS"
    if not sums_path.exists():
        return ["SHA256SUMS missing"]
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        path = nas_root / rel.replace("/", "\\") if "\\" in str(nas_root) else nas_root / rel
        if not path.exists():
            errors.append(f"SHA256SUMS references missing file: {rel}")
            continue
        if sha256_file(path) != digest:
            errors.append(f"SHA256 mismatch: {rel}")
    return errors


def validate_no_worktree_binaries(worktree: Path) -> list[str]:
    errors: list[str] = []
    for path in worktree.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in IMAGE_SUFFIXES and "test" not in path.parts:
            rel = path.relative_to(worktree)
            if "node_modules" not in path.parts:
                errors.append(f"image binary in worktree: {rel}")
    return errors


def validate_phases(catalog_root: Path, nas_root: Path, worktree: Path) -> dict[str, Any]:
    phase_status = {
        "phase_1_acquisition_core": {"status": "complete", "note": "scripts/acquisition present"},
        "phase_2_rights_ledger": {"status": "pending"},
        "phase_3_metadata_catalog": {"status": "pending"},
        "phase_4_execution": {"status": "pending"},
        "phase_5_git_deliverables": {"status": "pending"},
        "phase_6_validation": {"status": "pending"},
    }
    errors: list[str] = []

    errors.extend(validate_catalog_artifacts(catalog_root))
    if (catalog_root / "rights_ledger.yaml").exists():
        data = yaml.safe_load((catalog_root / "rights_ledger.yaml").read_text(encoding="utf-8"))
        rows = data.get("rows", []) if isinstance(data, dict) else []
        phase_status["phase_2_rights_ledger"] = {"status": "complete", "rows": len(rows)}
    if (catalog_root / "codex_catalog.jsonl").exists():
        phase_status["phase_3_metadata_catalog"] = {
            "status": "complete",
            "rows": len(parse_jsonl(catalog_root / "codex_catalog.jsonl")),
        }
    residual_path = catalog_root / "residual_report.json"
    if residual_path.exists():
        residual = json.loads(residual_path.read_text(encoding="utf-8"))
        phase_status["phase_4_execution"] = {
            "status": residual.get("completion_state", "unknown"),
            "completed": residual.get("completed"),
            "total": residual.get("total_resources"),
        }
        if residual.get("remaining", 1) != 0 or residual.get("failed", 1) != 0:
            errors.append("phase 4 not complete_verified")

    errors.extend(validate_sha256sums(catalog_root, nas_root))
    errors.extend(validate_no_worktree_binaries(worktree))

    required_git = [
        worktree / "scripts/acquisition/run_acquisition.py",
        worktree / "tests/test_iiif_acquisition.py",
        worktree / ".ai/handoffs/T479/handoff.md",
        worktree / "docs/roadmap/T479_LEIPZIG_SINAITICUS_NAS_ACQUISITION.md",
    ]
    missing_git = [str(p.relative_to(worktree)) for p in required_git if not p.exists()]
    if missing_git:
        errors.append(f"phase 5 missing git deliverables: {missing_git}")
    else:
        phase_status["phase_5_git_deliverables"] = {"status": "complete"}

    phase_status["phase_6_validation"] = {
        "status": "complete" if not errors else "failed",
        "error_count": len(errors),
    }
    return {
        "phases": phase_status,
        "errors": errors,
        "completion_state": "complete_verified" if not errors else "incomplete",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog-root", default="Z:/01-Projects/Logos/manuscript-witnesses/catalog/T479")
    parser.add_argument("--nas-root", default="Z:/01-Projects/Logos")
    parser.add_argument("--worktree", default=str(ROOT))
    parser.add_argument("--report", default=None)
    args = parser.parse_args()

    catalog_root = Path(args.catalog_root)
    nas_root = Path(args.nas_root)
    worktree = Path(args.worktree)
    try:
        validate_nas_root(nas_root)
    except ValueError as exc:
        print(json.dumps({"completion_state": "blocked", "errors": [str(exc)]}, indent=2))
        return 2
    result = validate_phases(catalog_root, nas_root, worktree)
    report_path = Path(args.report) if args.report else catalog_root / "phase_6_validation_report.json"
    report_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["completion_state"] == "complete_verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
