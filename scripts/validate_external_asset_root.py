#!/usr/bin/env python3
"""Validate LOGOS_EXTERNAL_ASSET_ROOT safety and budget for SRC-PILOT-A acquisition."""
from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "data/candidate/source_catalog/primary_bible_witnesses/external_asset_root_validation_report.yaml"
LEDGER = ROOT / "data/candidate/source_catalog/primary_bible_witnesses/storage_ledger.yaml"
ENV_VAR = "LOGOS_EXTERNAL_ASSET_ROOT"
DEFAULT_BUDGET_BYTES = 53_687_091_200  # 50 GiB


def _is_inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _is_temp_path(path: Path) -> bool:
    lowered = str(path.resolve()).lower()
    temp_root = str(Path(tempfile.gettempdir()).resolve()).lower()
    return lowered.startswith(temp_root) or "\\appdata\\local\\temp" in lowered


def validate_external_asset_root(
    *,
    root: Path | None = None,
    require_env: bool = True,
    min_budget_bytes: int = DEFAULT_BUDGET_BYTES,
    repo_root: Path = ROOT,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    env_value = os.environ.get(ENV_VAR)
    resolved: Path | None = None
    free_bytes = 0

    if root is not None:
        resolved = root.expanduser().resolve()
    elif env_value:
        resolved = Path(env_value).expanduser().resolve()
    elif require_env:
        errors.append(f"{ENV_VAR} is not set")
    else:
        warnings.append(f"{ENV_VAR} is not set; acquisition remains blocked")

    checks: dict[str, bool | None] = {
        "env_var_set": bool(env_value or root is not None),
        "absolute_path": None,
        "exists": None,
        "writable": None,
        "outside_git": None,
        "outside_onedrive": None,
        "outside_workspace_repo": None,
        "not_temp_directory": None,
        "meets_budget_bytes": None,
    }

    if resolved is not None:
        checks["absolute_path"] = resolved.is_absolute()
        if not resolved.is_absolute():
            errors.append(f"{ENV_VAR} must resolve to an absolute path")
        checks["exists"] = resolved.exists()
        if not resolved.exists():
            errors.append(f"external asset root does not exist: {resolved}")
        checks["writable"] = os.access(resolved, os.W_OK) if resolved.exists() else False
        if resolved.exists() and not checks["writable"]:
            errors.append(f"external asset root is not writable: {resolved}")
        checks["outside_git"] = not _is_inside(resolved, repo_root)
        if _is_inside(resolved, repo_root):
            errors.append("external asset root must not be inside the Git repository")
        checks["outside_onedrive"] = "onedrive" not in str(resolved).lower()
        if "onedrive" in str(resolved).lower():
            errors.append("external asset root must not be inside OneDrive")
        checks["outside_workspace_repo"] = checks["outside_git"]
        checks["not_temp_directory"] = not _is_temp_path(resolved)
        if _is_temp_path(resolved):
            errors.append("external asset root must not be a temporary directory")
        if resolved.exists():
            usage = shutil.disk_usage(resolved)
            free_bytes = usage.free
            checks["meets_budget_bytes"] = free_bytes >= min_budget_bytes
            if free_bytes < min_budget_bytes:
                warnings.append(
                    f"free space {free_bytes} bytes is below configured budget {min_budget_bytes} bytes; "
                    "acquisition tooling must fail closed for full-budget downloads"
                )

    return {
        "validator": "validate_external_asset_root",
        "env_var": ENV_VAR,
        "configured_root": str(resolved) if resolved else None,
        "free_bytes": free_bytes,
        "min_budget_bytes": min_budget_bytes,
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
        "acquisition_allowed": not errors and bool(resolved),
        "ok": not errors,
    }


def write_report(result: dict[str, Any]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "object_type": "external_asset_root_validation_report",
        "authorization_id": "SRC-PILOT-A",
        "task_id": "T481",
        **result,
        "non_authorizing_scope_label": "storage_gate_report_not_download_authorization",
    }
    REPORT.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def assert_acquisition_gate_open() -> None:
    """Fail closed before any binary acquisition."""
    result = validate_external_asset_root(require_env=True)
    if not result["ok"]:
        raise RuntimeError("; ".join(result["errors"]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="Override path instead of env var")
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--allow-missing-env", action="store_true")
    args = parser.parse_args()
    override = Path(args.path) if args.path else None
    result = validate_external_asset_root(
        root=override,
        require_env=not args.allow_missing_env and override is None,
    )
    if args.write_report:
        write_report(result)
    for warning in result["warnings"]:
        print(f"WARNING: {warning}", file=sys.stderr)
    if result["errors"]:
        for err in result["errors"]:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(
        f"OK validate_external_asset_root root={result['configured_root']} "
        f"free_bytes={result['free_bytes']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
