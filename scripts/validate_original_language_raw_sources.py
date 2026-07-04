#!/usr/bin/env python3
"""Validate T431 original-language raw source intake."""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.build_original_language_canonical_source_views import CanonicalSourceViewError, build_views  # noqa: E402

ALLOWLIST = ROOT / ".ai" / "control" / "original_language_source_allowlist.yaml"
RAW_ROOT = ROOT / "data" / "raw" / "original_language"
CATALOG = RAW_ROOT / "witness_catalogs" / "manuscript_libraries.yaml"
CANONICAL_VIEW_ROOT = ROOT / "data" / "candidate" / "original_language_evidence" / "canonical_source_views"

FALSE_AUTHORITY = {
    "authorizes_source_language_truth",
    "authorizes_lexical_truth",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_textual_critical_decision",
    "authorizes_canon_scope_change",
    "authorizes_chunk_boundaries",
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_theology_authority",
}


class OriginalLanguageRawSourceError(ValueError):
    """Raised when T431 raw source intake is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise OriginalLanguageRawSourceError(f"{_rel(path)}: unreadable YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise OriginalLanguageRawSourceError(f"{_rel(path)}: expected YAML mapping")
    return data


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _require_false(mapping: dict[str, Any], keys: set[str], label: str) -> None:
    for key in sorted(keys):
        if mapping.get(key) is not False:
            raise OriginalLanguageRawSourceError(f"{label}.{key} must be false")


def _enabled_sources(allowlist: dict[str, Any]) -> list[dict[str, Any]]:
    sources = allowlist.get("sources")
    if not isinstance(sources, list) or not sources:
        raise OriginalLanguageRawSourceError("allowlist.sources must be a non-empty list")
    return [source for source in sources if source.get("enabled") is True]


def validate_allowlist(path: Path = ALLOWLIST) -> dict[str, Any]:
    data = _read_yaml(path)
    if data.get("object_type") != "original_language_source_allowlist":
        raise OriginalLanguageRawSourceError(f"{_rel(path)}: object_type is wrong")
    if data.get("schema_version") != "original_language_source_allowlist.v1":
        raise OriginalLanguageRawSourceError(f"{_rel(path)}: schema_version is wrong")
    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise OriginalLanguageRawSourceError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("authorizes_allowlisted_raw_downloads") is not True:
        raise OriginalLanguageRawSourceError(f"{_rel(path)}: raw download authorization flag must be true")
    _require_false(
        authority,
        {
            "authorizes_source_text_mutation",
            "authorizes_strongs_overlay_in_raw",
            "authorizes_source_language_witness_rows",
            "authorizes_preferred_reading",
            "authorizes_source_tradition_preference",
            "authorizes_textual_critical_decision",
            "authorizes_canon_scope_change",
            "authorizes_chunk_boundaries",
            "authorizes_reviewed_gold",
            "authorizes_chunk_output",
            "authorizes_graph_edges",
            "authorizes_retrieval_truth",
            "authorizes_theology_authority",
        },
        f"{_rel(path)}: authority",
    )
    policy = data.get("download_policy")
    if not isinstance(policy, dict):
        raise OriginalLanguageRawSourceError(f"{_rel(path)}: download_policy must be a mapping")
    if policy.get("strongs_overlay_in_raw_allowed") is not False:
        raise OriginalLanguageRawSourceError("download_policy.strongs_overlay_in_raw_allowed must be false")
    if policy.get("manuscript_bulk_download_allowed") is not False:
        raise OriginalLanguageRawSourceError("download_policy.manuscript_bulk_download_allowed must be false")
    for source in _enabled_sources(data):
        for key in ("id", "language", "download_kind", "source_url", "license_url", "license", "attribution"):
            if not isinstance(source.get(key), str) or not source[key].strip():
                raise OriginalLanguageRawSourceError(f"source {source.get('id')}: {key} must be non-empty")
        if source["language"] not in {"hebrew", "greek"}:
            raise OriginalLanguageRawSourceError(f"source {source['id']}: unsupported language")
        if source.get("source_text_storage_allowed") is not True:
            raise OriginalLanguageRawSourceError(f"source {source['id']}: source_text_storage_allowed must be true")
        if source.get("redistribution_allowed") is not True:
            raise OriginalLanguageRawSourceError(f"source {source['id']}: redistribution_allowed must be true")
        if source.get("strongs_overlay_in_raw_allowed") is not False:
            raise OriginalLanguageRawSourceError(f"source {source['id']}: strongs_overlay_in_raw_allowed must be false")
    return data


def validate_manifests(root: Path = ROOT, allowlist_path: Path = ALLOWLIST) -> list[dict[str, Any]]:
    allowlist = validate_allowlist(allowlist_path)
    records = []
    raw_root = root / "data" / "raw" / "original_language"
    for source in _enabled_sources(allowlist):
        source_dir = raw_root / source["language"] / source["id"]
        manifest_path = source_dir / "source_manifest.yaml"
        manifest = _read_yaml(manifest_path)
        if manifest.get("id") != source["id"]:
            raise OriginalLanguageRawSourceError(f"{_rel(manifest_path)}: id does not match allowlist")
        if manifest.get("language") != source["language"]:
            raise OriginalLanguageRawSourceError(f"{_rel(manifest_path)}: language does not match allowlist")
        for key in ("archive_path", "license", "license_url", "source_url", "sha256", "size_bytes", "attribution"):
            if key not in manifest or manifest[key] in ("", None):
                raise OriginalLanguageRawSourceError(f"{_rel(manifest_path)}: missing {key}")
        if manifest.get("license") != source["license"]:
            raise OriginalLanguageRawSourceError(f"{_rel(manifest_path)}: license does not match allowlist")
        if manifest.get("source_text_storage_allowed") is not True:
            raise OriginalLanguageRawSourceError(f"{_rel(manifest_path)}: source_text_storage_allowed must be true")
        if manifest.get("strongs_overlay_in_raw_allowed") is not False:
            raise OriginalLanguageRawSourceError(f"{_rel(manifest_path)}: strongs_overlay_in_raw_allowed must be false")
        for key in (
            "contains_source_provided_morphology",
            "contains_source_provided_lemmas",
            "contains_source_provided_strongs",
        ):
            if manifest.get(key, False) is not bool(source.get(key, False)):
                raise OriginalLanguageRawSourceError(f"{_rel(manifest_path)}: {key} does not match allowlist")
        authority = manifest.get("authority")
        if not isinstance(authority, dict):
            raise OriginalLanguageRawSourceError(f"{_rel(manifest_path)}: authority must be a mapping")
        _require_false(authority, FALSE_AUTHORITY, f"{_rel(manifest_path)}: authority")
        archive = root / str(manifest["archive_path"])
        if not archive.exists():
            raise OriginalLanguageRawSourceError(f"{_rel(manifest_path)}: archive missing at {manifest['archive_path']}")
        if _sha256(archive) != manifest["sha256"]:
            raise OriginalLanguageRawSourceError(f"{_rel(archive)}: sha256 does not match manifest")
        if archive.stat().st_size != int(manifest["size_bytes"]):
            raise OriginalLanguageRawSourceError(f"{_rel(archive)}: size does not match manifest")
        if source.get("expected_sha256") and manifest["sha256"] != source["expected_sha256"]:
            raise OriginalLanguageRawSourceError(f"{_rel(manifest_path)}: expected_sha256 mismatch")
        records.append(manifest)
    return records


def validate_catalog_only(root: Path = ROOT) -> dict[str, Any]:
    path = root / "data" / "raw" / "original_language" / "witness_catalogs" / "manuscript_libraries.yaml"
    data = _read_yaml(path)
    if data.get("object_type") != "original_language_manuscript_library_catalog":
        raise OriginalLanguageRawSourceError(f"{_rel(path)}: object_type is wrong")
    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise OriginalLanguageRawSourceError(f"{_rel(path)}: authority must be a mapping")
    _require_false(
        authority,
        {
            "authorizes_manuscript_transcription_storage",
            "authorizes_manuscript_image_storage",
            "authorizes_preferred_reading",
            "authorizes_source_tradition_preference",
            "authorizes_textual_critical_decision",
            "authorizes_theology_authority",
        },
        f"{_rel(path)}: authority",
    )
    catalogs = data.get("catalogs")
    if not isinstance(catalogs, list) or not catalogs:
        raise OriginalLanguageRawSourceError(f"{_rel(path)}: catalogs must be a non-empty list")
    for entry in catalogs:
        if not isinstance(entry, dict):
            raise OriginalLanguageRawSourceError(f"{_rel(path)}: catalog entry must be a mapping")
        if entry.get("storage_mode") != "catalog_only":
            raise OriginalLanguageRawSourceError(f"{entry.get('id')}: storage_mode must be catalog_only")
        for key in ("bulk_download_authorized", "transcription_storage_allowed", "image_storage_allowed"):
            if entry.get(key) is not False:
                raise OriginalLanguageRawSourceError(f"{entry.get('id')}: {key} must be false")
    return data


def validate_raw_tree_shape(root: Path = ROOT, manifests: list[dict[str, Any]] | None = None) -> None:
    raw_root = root / "data" / "raw" / "original_language"
    if not raw_root.exists():
        raise OriginalLanguageRawSourceError(f"{_rel(raw_root)} is missing")
    if manifests is None:
        manifests = validate_manifests(root)
    raw_root_resolved = raw_root.resolve()
    allowed_files = {(raw_root / "witness_catalogs" / "manuscript_libraries.yaml").resolve()}
    for manifest in manifests:
        source_dir = raw_root / str(manifest["language"]) / str(manifest["id"])
        allowed_files.add((source_dir / "source_manifest.yaml").resolve())
        archive = (root / str(manifest["archive_path"])).resolve()
        archive_dir = (source_dir / "raw").resolve()
        try:
            archive.relative_to(raw_root_resolved)
        except ValueError as exc:
            raise OriginalLanguageRawSourceError(
                f"{manifest['id']}: declared raw archive must stay under data/raw/original_language"
            ) from exc
        if archive.parent != archive_dir:
            raise OriginalLanguageRawSourceError(
                f"{manifest['id']}: declared raw archive must be under {_rel(source_dir / 'raw')}"
            )
        allowed_files.add(archive)
    offenders = [path for path in raw_root.rglob("*") if path.is_file() and path.resolve() not in allowed_files]
    if offenders:
        raise OriginalLanguageRawSourceError(
            "raw original-language tree may contain only source_manifest.yaml, raw/<declared archive>, "
            "and witness_catalogs/manuscript_libraries.yaml; unexpected file(s): "
            + ", ".join(_rel(path) for path in offenders)
        )


def validate_original_language_raw_sources(root: Path = ROOT, allowlist_path: Path = ALLOWLIST) -> dict[str, Any]:
    manifests = validate_manifests(root, allowlist_path)
    catalog = validate_catalog_only(root)
    validate_raw_tree_shape(root, manifests)
    try:
        views = build_views(
            allowlist_path=allowlist_path,
            raw_root=root / "data" / "raw" / "original_language",
            out_root=root / "data" / "candidate" / "original_language_evidence" / "canonical_source_views",
            check=True,
        )
    except CanonicalSourceViewError as exc:
        raise OriginalLanguageRawSourceError(str(exc)) from exc
    return {
        "source_count": len(manifests),
        "catalog_count": len(catalog["catalogs"]),
        "canonical_source_view_count": views["source_count"],
        "sources": [record["id"] for record in manifests],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--allowlist", type=Path, default=ALLOWLIST)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    allowlist = args.allowlist if args.allowlist.is_absolute() else root / args.allowlist
    try:
        summary = validate_original_language_raw_sources(root, allowlist)
    except OriginalLanguageRawSourceError as exc:
        print(f"T431 original-language raw source validation failed: {exc}", file=sys.stderr)
        return 1
    print(
        "T431 original-language raw source validation passed: "
        f"{summary['source_count']} source(s), {summary['catalog_count']} catalog-only manuscript source(s), "
        f"{summary['canonical_source_view_count']} canonical source view(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
