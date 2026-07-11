#!/usr/bin/env python3
"""Fail-closed guard before primary-witness binary acquisition."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data/candidate/source_catalog/primary_bible_witnesses/acquisition_manifest.yaml"
LEDGER = ROOT / "data/candidate/source_catalog/primary_bible_witnesses/storage_ledger.yaml"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_external_asset_root import assert_acquisition_gate_open, validate_external_asset_root


REQUIRED_LEDGER_FIELDS = {
    "asset_id",
    "source_id",
    "sha256",
    "rights_status",
    "local_relative_path",
    "removal_owner",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must be a mapping")
    return data


def guard_download(*, source_id: str, planned_bytes: int, rights_status: str) -> dict[str, Any]:
    errors: list[str] = []
    try:
        assert_acquisition_gate_open()
    except RuntimeError as exc:
        errors.append(str(exc))

    root_result = validate_external_asset_root(require_env=True)
    if root_result["free_bytes"] < planned_bytes:
        errors.append(
            f"insufficient free bytes for planned download: need {planned_bytes}, "
            f"have {root_result['free_bytes']}"
        )

    manifest = _load_yaml(MANIFEST)
    if manifest.get("wave") == "W0" and manifest.get("status", "").startswith("metadata"):
        errors.append("Wave 0 manifest blocks binary acquisition")

    ledger = _load_yaml(LEDGER)
    budget = int(ledger.get("external_storage", {}).get("max_budget_bytes", 0))
    recorded = int(ledger.get("external_storage", {}).get("bytes_recorded", 0))
    if recorded + planned_bytes > budget:
        errors.append("download would exceed storage ledger budget")

    if rights_status not in {"approved_for_local_storage", "approved_noncommercial_pilot"}:
        errors.append(f"rights_status {rights_status!r} does not authorize download")

    return {
        "source_id": source_id,
        "planned_bytes": planned_bytes,
        "errors": errors,
        "ok": not errors,
    }


def validate_ledger_row(row: dict[str, Any]) -> list[str]:
    missing = REQUIRED_LEDGER_FIELDS - set(row)
    if missing:
        return [f"ledger row missing fields: {sorted(missing)}"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-gate-only", action="store_true")
    parser.add_argument("--source-id")
    parser.add_argument("--planned-bytes", type=int, default=0)
    parser.add_argument("--rights-status", default="metadata_only")
    args = parser.parse_args()
    if args.check_gate_only:
        result = validate_external_asset_root(require_env=True)
        if not result["ok"]:
            for err in result["errors"]:
                print(f"ERROR: {err}", file=sys.stderr)
            return 1
        print("OK acquisition gate closed until explicit approved download")
        return 0
    if not args.source_id:
        print("ERROR: --source-id required unless --check-gate-only", file=sys.stderr)
        return 2
    result = guard_download(
        source_id=args.source_id,
        planned_bytes=args.planned_bytes,
        rights_status=args.rights_status,
    )
    if result["errors"]:
        for err in result["errors"]:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
