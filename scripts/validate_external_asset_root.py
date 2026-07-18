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
AUTHORIZATION = ROOT / "data/candidate/source_catalog/primary_bible_witnesses/external_asset_root_owner_authorization.yaml"
ENV_VAR = "LOGOS_EXTERNAL_ASSET_ROOT"
DEFAULT_BUDGET_BYTES = 53_687_091_200  # 50 GiB
REQUIRED_NON_AUTHORIZATIONS = {
    "downloads",
    "OCR",
    "ingest",
    "embeddings",
    "vector_indexes",
    "publication",
    "email",
    "release",
    "canonical_text_change",
    "canon_scope_change",
    "preferred_reading",
    "source_tradition_selection",
    "theology_or_interpretation_authority",
}


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
    workspace_root: Path | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    env_value = os.environ.get(ENV_VAR)
    resolved: Path | None = None
    free_bytes = 0
    workspace_root = (workspace_root or repo_root.parent).resolve()

    if root is not None:
        resolved = root.expanduser().resolve()
    elif env_value:
        resolved = Path(env_value).expanduser().resolve()
    elif require_env:
        errors.append(f"{ENV_VAR} is not set")
    else:
        warnings.append(f"{ENV_VAR} is not set; acquisition remains blocked")

    checks: dict[str, bool | None] = {
        "env_var_set": bool(env_value),
        "path_override_supplied": root is not None,
        "absolute_path": None,
        "exists": None,
        "writable": None,
        "outside_git": None,
        "outside_workspace": None,
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
        checks["outside_workspace"] = not _is_inside(resolved, workspace_root)
        if _is_inside(resolved, workspace_root):
            errors.append("external asset root must not be inside the shared workspace")
        checks["outside_onedrive"] = "onedrive" not in str(resolved).lower()
        if "onedrive" in str(resolved).lower():
            errors.append("external asset root must not be inside OneDrive")
        checks["outside_workspace_repo"] = checks["outside_workspace"]
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
        "storage_preflight_passed": not errors and bool(resolved),
        "acquisition_allowed": False,
        "download_authorized": False,
        "ok": not errors,
    }


def load_owner_authorization(path: Path = AUTHORIZATION) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("external asset root owner authorization must be a mapping")
    return data


def validate_owner_authorization(path: Path = AUTHORIZATION) -> dict[str, Any]:
    errors: list[str] = []
    try:
        approval = load_owner_authorization(path)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return {"approval": None, "errors": [str(exc)], "ok": False}

    if approval.get("object_type") != "external_asset_root_owner_authorization":
        errors.append("owner authorization object_type is invalid")
    if approval.get("authority") != "Lowell Wong":
        errors.append("owner authorization authority must be Lowell Wong")
    if approval.get("environment_variable") != ENV_VAR:
        errors.append(f"owner authorization environment_variable must be {ENV_VAR}")
    approved_root = approval.get("exact_private_quarantine_root")
    if not isinstance(approved_root, str) or not approved_root:
        errors.append("owner authorization must record an exact private quarantine root")
    if set(approval.get("authorized_actions", [])) != {"record_exact_path", "preflight_exact_path"}:
        errors.append("owner authorization must be limited to recording and preflighting the path")
    if set(approval.get("non_authorizations", [])) != REQUIRED_NON_AUTHORIZATIONS:
        errors.append("owner authorization must preserve every explicit non-authorization")
    binding = approval.get("environment_binding", {})
    if binding.get("persistence_authorized") is not False or binding.get("persisted_by_task") is not False:
        errors.append("environment-variable persistence must remain unauthorized and unperformed")
    mutation = approval.get("root_mutation", {})
    if any(mutation.get(key) is not False for key in ("creation_authorized", "content_write_authorized", "performed_by_task")):
        errors.append("root creation and content writes must remain unauthorized and unperformed")
    return {"approval": approval, "errors": errors, "ok": not errors}


def validate_approved_external_asset_root(
    *, root: Path | None = None, require_env: bool = True
) -> dict[str, Any]:
    approval_result = validate_owner_authorization()
    if not approval_result["ok"]:
        result = validate_external_asset_root(root=root, require_env=require_env)
        result["errors"].extend(approval_result["errors"])
        result["ok"] = False
        result["storage_preflight_passed"] = False
        return result

    approval = approval_result["approval"]
    result = validate_external_asset_root(root=root, require_env=require_env)
    configured = result.get("configured_root")
    approved = str(Path(approval["exact_private_quarantine_root"]).resolve())
    result["approval_id"] = approval["approval_id"]
    result["approved_root"] = approved
    if configured is None and not require_env:
        result["storage_preflight_passed"] = False
        return result
    if configured != approved:
        result["errors"].append(
            f"configured root {configured!r} does not match owner-approved root {approved!r}"
        )
        result["ok"] = False
        result["storage_preflight_passed"] = False
    return result


def write_report(result: dict[str, Any]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "object_type": "external_asset_root_validation_report",
        "authorization_id": "SRC-PILOT-A",
        "owner_approval_id": "LOGOS-EXTERNAL-ROOT-2026-07-18",
        "task_id": "T514",
        **result,
        "non_authorizing_scope_label": "storage_gate_report_not_download_authorization",
    }
    REPORT.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def assert_acquisition_gate_open() -> None:
    """Fail closed before any binary acquisition."""
    result = validate_approved_external_asset_root(require_env=True)
    if not result["ok"]:
        raise RuntimeError("; ".join(result["errors"]))
    if result.get("download_authorized") is not True:
        raise RuntimeError("download is not authorized by the external-root owner approval")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="Override path instead of env var")
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--allow-missing-env", action="store_true")
    args = parser.parse_args()
    override = Path(args.path) if args.path else None
    result = validate_approved_external_asset_root(
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
