#!/usr/bin/env python3
"""Download T431 allowlisted original-language raw source packages."""
from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
ALLOWLIST = ROOT / ".ai" / "control" / "original_language_source_allowlist.yaml"
RAW_ROOT = ROOT / "data" / "raw" / "original_language"
UA = "logos-scripture-graph-t431-source-intake/1.0"


class DownloadError(RuntimeError):
    """Raised when a source cannot be downloaded or verified."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise DownloadError(f"{_rel(path)} must be a YAML mapping")
    return data


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _download(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def _git_commit(repository: str, ref: str) -> str:
    url = f"https://github.com/{repository}.git"
    result = subprocess.run(
        ["git", "ls-remote", url, ref],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise DownloadError(f"git ls-remote failed for {repository}@{ref}: {result.stderr.strip()}")
    first = result.stdout.splitlines()[0] if result.stdout.splitlines() else ""
    commit = first.split()[0] if first.split() else ""
    if len(commit) != 40:
        raise DownloadError(f"could not resolve {repository}@{ref}")
    return commit


def _source_dir(source: dict[str, Any], raw_root: Path) -> Path:
    language = str(source["language"])
    return raw_root / language / str(source["id"])


def _archive_name(source: dict[str, Any], commit: str | None = None) -> str:
    if source["download_kind"] == "direct_archive":
        return Path(str(source["source_url"])).name
    suffix = commit[:12] if commit else str(source["ref"])
    return f"{source['id']}-{suffix}.zip"


def _manifest(source: dict[str, Any], archive: Path, *, download_url: str, commit: str | None) -> dict[str, Any]:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    manifest = {
        "id": source["id"],
        "source_family": "original_language",
        "title": source["title"],
        "abbreviation": source["abbreviation"],
        "language": source["language"],
        "corpus_scope": source["corpus_scope"],
        "source_kind": source["source_kind"],
        "format": source["format"],
        "archive_path": _rel(archive),
        "license": source["license"],
        "license_url": source["license_url"],
        "source_url": source["source_url"],
        "download_url": download_url,
        "downloaded_at": now,
        "sha256": _sha256(archive),
        "size_bytes": archive.stat().st_size,
        "status": "verified",
        "attribution": source["attribution"],
        "source_text_storage_allowed": bool(source["source_text_storage_allowed"]),
        "redistribution_allowed": bool(source["redistribution_allowed"]),
        "contains_source_provided_morphology": bool(source.get("contains_source_provided_morphology", False)),
        "contains_source_provided_lemmas": bool(source.get("contains_source_provided_lemmas", False)),
        "contains_source_provided_strongs": bool(source.get("contains_source_provided_strongs", False)),
        "strongs_overlay_in_raw_allowed": False,
        "authority": {
            "authorizes_source_language_truth": False,
            "authorizes_lexical_truth": False,
            "authorizes_preferred_reading": False,
            "authorizes_source_tradition_preference": False,
            "authorizes_textual_critical_decision": False,
            "authorizes_canon_scope_change": False,
            "authorizes_chunk_boundaries": False,
            "authorizes_reviewed_gold": False,
            "authorizes_chunk_output": False,
            "authorizes_graph_edges": False,
            "authorizes_retrieval_truth": False,
            "authorizes_theology_authority": False,
        },
        "notes": "Raw source package only. Strong's, lemma, morphology, variants, and witness support are candidate evidence overlays outside raw.",
    }
    if commit:
        manifest["repository"] = source["repository"]
        manifest["ref"] = source["ref"]
        manifest["resolved_commit"] = commit
    for key in ("expected_version", "expected_build"):
        if key in source:
            manifest[key] = source[key]
    return manifest


def _write_manifest(path: Path, data: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")


def _download_source(source: dict[str, Any], raw_root: Path, *, check: bool) -> dict[str, Any]:
    source_dir = _source_dir(source, raw_root)
    raw_dir = source_dir / "raw"
    commit: str | None = None
    if source["download_kind"] == "github_archive":
        commit = _git_commit(str(source["repository"]), str(source["ref"]))
        download_url = f"https://codeload.github.com/{source['repository']}/zip/{commit}"
    elif source["download_kind"] == "direct_archive":
        download_url = str(source["source_url"])
    else:
        raise DownloadError(f"{source['id']}: unsupported download_kind {source['download_kind']}")

    archive = raw_dir / _archive_name(source, commit)
    manifest_path = source_dir / "source_manifest.yaml"
    if check:
        if not archive.exists():
            raise DownloadError(f"{_rel(archive)} is missing")
        if not manifest_path.exists():
            raise DownloadError(f"{_rel(manifest_path)} is missing")
        return {"id": source["id"], "archive": _rel(archive), "status": "present"}

    _download(download_url, archive)
    actual = _sha256(archive)
    expected_sha = source.get("expected_sha256")
    if expected_sha and actual != expected_sha:
        raise DownloadError(f"{source['id']}: sha256 {actual} != expected {expected_sha}")
    expected_size = source.get("expected_size_bytes")
    if expected_size and archive.stat().st_size != int(expected_size):
        raise DownloadError(f"{source['id']}: size {archive.stat().st_size} != expected {expected_size}")
    _write_manifest(manifest_path, _manifest(source, archive, download_url=download_url, commit=commit))
    return {"id": source["id"], "archive": _rel(archive), "sha256": actual, "status": "downloaded"}


def _write_manuscript_catalogs(data: dict[str, Any], raw_root: Path, *, check: bool) -> None:
    path = raw_root / "witness_catalogs" / "manuscript_libraries.yaml"
    if check:
        if not path.exists():
            raise DownloadError(f"{_rel(path)} is missing")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "object_type": "original_language_manuscript_library_catalog",
        "schema_version": "original_language_manuscript_library_catalog.v1",
        "task_id": "T431",
        "status": "catalog_only_no_bulk_download",
        "authority": {
            "authorizes_manuscript_transcription_storage": False,
            "authorizes_manuscript_image_storage": False,
            "authorizes_preferred_reading": False,
            "authorizes_source_tradition_preference": False,
            "authorizes_textual_critical_decision": False,
            "authorizes_theology_authority": False,
        },
        "catalogs": data.get("manuscript_catalogs", []),
    }
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")


def enabled_sources(data: dict[str, Any]) -> list[dict[str, Any]]:
    sources = data.get("sources")
    if not isinstance(sources, list):
        raise DownloadError("allowlist.sources must be a list")
    return [source for source in sources if source.get("enabled") is True]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allowlist", type=Path, default=ALLOWLIST)
    parser.add_argument("--out", type=Path, default=RAW_ROOT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    allowlist = args.allowlist if args.allowlist.is_absolute() else ROOT / args.allowlist
    raw_root = args.out if args.out.is_absolute() else ROOT / args.out

    try:
        data = _read_yaml(allowlist)
        results = [_download_source(source, raw_root, check=args.check) for source in enabled_sources(data)]
        _write_manuscript_catalogs(data, raw_root, check=args.check)
    except (OSError, DownloadError, subprocess.SubprocessError) as exc:
        print(f"T431 source download failed: {exc}", file=sys.stderr)
        return 1

    for result in results:
        print(f"{result['id']}: {result['status']} {result['archive']}")
    if args.check:
        print("T431 original-language source downloads are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
