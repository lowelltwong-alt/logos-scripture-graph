#!/usr/bin/env python3
"""Validate T481 / SRC-PILOT-A primary Bible witness Wave 0 catalog scaffold."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CATALOG_ROOT = ROOT / "data" / "candidate" / "source_catalog" / "primary_bible_witnesses"
CONTROL = ROOT / ".ai" / "control" / "primary_bible_witness_catalog.yaml"
TASK = ROOT / ".ai" / "tasks" / "T481.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T481" / "handoff.md"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T481_SRC_PILOT_A_WAVE0.md"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

REQUIRED_FILES = [
    CATALOG_ROOT / "manifest.yaml",
    CATALOG_ROOT / "source_catalog_rows.jsonl",
    CATALOG_ROOT / "image_rights_review.yaml",
    CATALOG_ROOT / "text_acquisition_review.yaml",
    CATALOG_ROOT / "blocked_or_permission_needed.yaml",
    CATALOG_ROOT / "acquisition_manifest.yaml",
    CATALOG_ROOT / "storage_ledger.yaml",
    CATALOG_ROOT / "witness_passage_coverage.jsonl",
    CATALOG_ROOT / "permission_request_queue.yaml",
    CATALOG_ROOT / "removal_plan.yaml",
    CATALOG_ROOT / "wave_0a_existing_source_inventory.yaml",
    CATALOG_ROOT / "showcases" / "isaiah_53_10_12" / "scaffold.yaml",
    CATALOG_ROOT / "showcases" / "mark_16_8_20" / "scaffold.yaml",
]

REQUIRED_ROW_FIELDS = {
    "source_id",
    "title",
    "witness_family",
    "language",
    "biblical_scope",
    "primary_url",
    "image_access",
    "text_access",
    "observed_license",
    "allowed_storage_mode",
    "confidence",
    "review_status",
    "removal_instructions",
    "next_action",
    "non_authorizing_scope_label",
}

REUSE_SOURCE_IDS = {"eng-web", "sblgnt", "oshb_wlc"}

PROHIBITED_FIELD_NAMES = {
    "preferred_reading",
    "preferred_reading_id",
    "source_tradition_preference",
    "direct_ancestry",
    "direct_ancestry_assertion",
    "canonical_reading",
    "theological_conclusion",
}

PROHIBITED_PATH_FRAGMENTS = (
    "/restricted_images/",
    "/iiif_tiles/",
    "/manuscript_images/",
    "great_isaiah_scroll/images",
    "codex_vaticanus/images",
    "codex_alexandrinus/images",
)

REQUIRED_WIRING = {
    "ROADMAP_TOC": ["T481", "SRC-PILOT-A", "primary_bible_witnesses", "validate_primary_bible_witness_catalog.py"],
    "MAIN_TOC": ["primary_bible_witnesses", "SRC-PILOT-A", "T481"],
    "VALIDATE_ALL": ["validate_primary_bible_witness_catalog.py"],
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_raw_downloads",
    "authorizes_image_storage",
    "authorizes_transcription_storage",
    "authorizes_source_text_import",
    "authorizes_textual_critical_decision",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_theology_authority",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must be a mapping")
    return data


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{line_no} must be a JSON object")
        rows.append(row)
    return rows


def _is_inside_git(path: Path) -> bool:
    try:
        path.resolve().relative_to(ROOT.resolve())
        return True
    except ValueError:
        return False


def _is_onedrive_path(path: Path) -> bool:
    return "onedrive" in str(path.resolve()).lower()


def _validate_external_root_policy(ledger: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    ext = ledger.get("external_storage", {})
    max_budget = int(ext.get("max_budget_bytes", 0))
    recorded = int(ext.get("bytes_recorded", 0))
    if max_budget != 53_687_091_200:
        errors.append("storage_ledger external_storage.max_budget_bytes must be 50 GB (53687091200)")
    if recorded != 0:
        errors.append("Wave 0 storage_ledger.bytes_recorded must be 0")
    remaining = int(ext.get("remaining_budget_bytes", 0))
    if remaining != max_budget - recorded:
        errors.append("storage_ledger remaining_budget_bytes must equal max_budget_bytes - bytes_recorded")

    assets = ledger.get("assets", [])
    if assets:
        errors.append("Wave 0 storage_ledger.assets must be empty")

    env_root = os.environ.get("LOGOS_EXTERNAL_ASSET_ROOT")
    if env_root:
        root_path = Path(env_root).expanduser()
        if not root_path.is_absolute():
            errors.append("LOGOS_EXTERNAL_ASSET_ROOT must resolve to an absolute path")
        elif _is_inside_git(root_path):
            errors.append("LOGOS_EXTERNAL_ASSET_ROOT must not be inside the Git repository")
        elif _is_onedrive_path(root_path):
            errors.append("LOGOS_EXTERNAL_ASSET_ROOT must not be inside OneDrive")
        elif not root_path.exists() or not os.access(root_path, os.W_OK):
            errors.append("LOGOS_EXTERNAL_ASSET_ROOT must exist and be writable when set")

    for asset in assets:
        rel = asset.get("local_relative_path")
        if not rel:
            continue
        joined = str(rel).replace("\\", "/").lower()
        for frag in PROHIBITED_PATH_FRAGMENTS:
            if frag in joined:
                errors.append(f"prohibited restricted-image local path fragment in ledger: {rel}")
    return errors


def _validate_reuse_rows(rows: list[dict[str, Any]], inventory: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    by_id = {row["source_id"]: row for row in rows}
    checksums: dict[str, str] = {}
    for source_id in REUSE_SOURCE_IDS:
        if source_id not in by_id:
            errors.append(f"missing reuse source_id in catalog rows: {source_id}")
    inv_sources = {item["source_id"]: item for item in inventory.get("sources", []) if isinstance(item, dict)}
    for source_id in REUSE_SOURCE_IDS:
        row = by_id.get(source_id, {})
        inv = inv_sources.get(source_id, {})
        if row.get("text_access") != "already_present_in_repo":
            errors.append(f"{source_id} must have text_access already_present_in_repo")
        if row.get("duplication_status") == "duplicate_copy":
            errors.append(f"{source_id} must not be marked duplicate_copy")
        manifest = row.get("reuse_existing_manifest") or inv.get("source_manifest")
        if not manifest:
            errors.append(f"{source_id} must reference reuse_existing_manifest")
        elif not (ROOT / manifest).exists():
            errors.append(f"{source_id} reuse manifest missing on disk: {manifest}")
        sha = row.get("reuse_sha256") or inv.get("sha256")
        if sha:
            if sha in checksums.values() and checksums.get(source_id) != sha:
                errors.append(f"duplicate artifact checksum across reuse sources: {sha}")
            checksums[source_id] = sha
    return errors


def _scan_prohibited_fields(obj: Any, path: str = "") -> list[str]:
    errors: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_norm = str(key).lower()
            if key_norm in PROHIBITED_FIELD_NAMES:
                errors.append(f"prohibited field {path}.{key}")
            errors.extend(_scan_prohibited_fields(value, f"{path}.{key}" if path else key))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            errors.extend(_scan_prohibited_fields(item, f"{path}[{idx}]"))
    return errors


def _validate_wiring(check_wiring: bool) -> list[str]:
    if not check_wiring:
        return []
    errors: list[str] = []
    validate_all_text = VALIDATE_ALL.read_text(encoding="utf-8")
    if "validate_primary_bible_witness_catalog.py" not in validate_all_text:
        errors.append("scripts/validate_all.py must wire validate_primary_bible_witness_catalog.py")
    roadmap_doc = ROADMAP_DOC.read_text(encoding="utf-8") if ROADMAP_DOC.exists() else ""
    if "SRC-PILOT-A" not in roadmap_doc:
        errors.append("roadmap doc must mention SRC-PILOT-A")
    return errors


def validate_primary_bible_witness_catalog(*, check_wiring: bool = True) -> dict[str, Any]:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"missing required catalog file: {path.relative_to(ROOT)}")

    control = _load_yaml(CONTROL)
    for key in REQUIRED_FALSE_AUTHORITY:
        if control.get("authorization", {}).get(key) is not False:
            errors.append(f"primary_bible_witness_catalog.authorization.{key} must be false")

    rows = _load_jsonl(CATALOG_ROOT / "source_catalog_rows.jsonl")
    source_ids = [row.get("source_id") for row in rows]
    if len(source_ids) != len(set(source_ids)):
        errors.append("duplicate source_id in source_catalog_rows.jsonl")

    for row in rows:
        missing = REQUIRED_ROW_FIELDS - set(row)
        if missing:
            errors.append(f"source_id {row.get('source_id')} missing fields: {sorted(missing)}")
        label = row.get("non_authorizing_scope_label", "")
        if "authority" not in label and "not_" not in label:
            errors.append(f"source_id {row.get('source_id')} needs explicit non_authorizing_scope_label")

    inventory = _load_yaml(CATALOG_ROOT / "wave_0a_existing_source_inventory.yaml")
    errors.extend(_validate_reuse_rows(rows, inventory))

    ledger = _load_yaml(CATALOG_ROOT / "storage_ledger.yaml")
    errors.extend(_validate_external_root_policy(ledger))

    acquisition = _load_yaml(CATALOG_ROOT / "acquisition_manifest.yaml")
    if acquisition.get("wave") != "W0":
        errors.append("acquisition_manifest.wave must be W0")
    if acquisition.get("acquisition_units"):
        errors.append("Wave 0 acquisition_manifest.acquisition_units must be empty")

    coverage_rows = _load_jsonl(CATALOG_ROOT / "witness_passage_coverage.jsonl")
    showcase_ids = {row.get("showcase_id") for row in coverage_rows}
    if "SHOWCASE-A" not in showcase_ids or "SHOWCASE-B" not in showcase_ids:
        errors.append("witness_passage_coverage must include SHOWCASE-A and SHOWCASE-B rows")

    permission_queue = _load_yaml(CATALOG_ROOT / "permission_request_queue.yaml")
    if permission_queue.get("send_policy") != "draft_only_do_not_send_without_owner_approval":
        errors.append("permission_request_queue.send_policy must block automatic sending")

    for yaml_path in CATALOG_ROOT.rglob("*.yaml"):
        errors.extend(_scan_prohibited_fields(_load_yaml(yaml_path), str(yaml_path.relative_to(ROOT))))
    for jsonl_path in CATALOG_ROOT.rglob("*.jsonl"):
        errors.extend(_scan_prohibited_fields(_load_jsonl(jsonl_path), str(jsonl_path.relative_to(ROOT))))

    errors.extend(_validate_wiring(check_wiring))

    return {
        "validator": "validate_primary_bible_witness_catalog",
        "catalog_root": str(CATALOG_ROOT.relative_to(ROOT)),
        "source_row_count": len(rows),
        "coverage_row_count": len(coverage_rows),
        "errors": errors,
        "ok": not errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-wiring", action="store_true")
    args = parser.parse_args()
    result = validate_primary_bible_witness_catalog(check_wiring=not args.skip_wiring)
    if result["errors"]:
        for err in result["errors"]:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(
        "OK validate_primary_bible_witness_catalog "
        f"rows={result['source_row_count']} coverage={result['coverage_row_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
