from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import zipfile

import pytest
import yaml

from scripts import validate_original_language_raw_sources as validator


ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = ROOT / ".ai" / "control" / "original_language_source_allowlist.yaml"


def test_t431_raw_sources_validate_current_repo() -> None:
    summary = validator.validate_original_language_raw_sources()

    assert summary["source_count"] == 5
    assert set(summary["sources"]) == {"tanach_us_uxlc", "openscriptures_oshb", "sblgnt", "ugnt", "cntr_sr"}
    assert summary["catalog_count"] >= 4
    assert summary["canonical_source_view_count"] == 5


def _write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _minimal_root(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path
    archive = root / "data/raw/original_language/greek/cntr_sr/raw/demo.zip"
    archive.parent.mkdir(parents=True, exist_ok=True)
    source_bytes = b"ref\ttext\nMatt.1.1\tDemo\n"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr("SR.tsv", source_bytes)
        zf.writestr("README.md", "demo documentation\n")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    allowlist = {
        "object_type": "original_language_source_allowlist",
        "schema_version": "original_language_source_allowlist.v1",
        "authority": {
            "authorizes_allowlisted_raw_downloads": True,
            "authorizes_source_text_mutation": False,
            "authorizes_strongs_overlay_in_raw": False,
            "authorizes_source_language_witness_rows": False,
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
        "download_policy": {
            "strongs_overlay_in_raw_allowed": False,
            "manuscript_bulk_download_allowed": False,
        },
        "sources": [
            {
                "id": "cntr_sr",
                "enabled": True,
                "language": "greek",
                "download_kind": "direct_archive",
                "source_url": "https://example.test/demo.zip",
                "license_url": "https://example.test/license",
                "license": "CC0-1.0",
                "attribution": "Demo",
                "source_text_storage_allowed": True,
                "redistribution_allowed": True,
                "strongs_overlay_in_raw_allowed": False,
            }
        ],
    }
    manifest = {
        "id": "cntr_sr",
        "language": "greek",
        "archive_path": "data/raw/original_language/greek/cntr_sr/raw/demo.zip",
        "license": "CC0-1.0",
        "license_url": "https://example.test/license",
        "source_url": "https://example.test/demo.zip",
        "sha256": digest,
        "size_bytes": archive.stat().st_size,
        "attribution": "Demo",
        "source_text_storage_allowed": True,
        "strongs_overlay_in_raw_allowed": False,
        "contains_source_provided_morphology": False,
        "contains_source_provided_lemmas": False,
        "contains_source_provided_strongs": False,
        "authority": {key: False for key in validator.FALSE_AUTHORITY},
    }
    catalog = {
        "object_type": "original_language_manuscript_library_catalog",
        "authority": {
            "authorizes_manuscript_transcription_storage": False,
            "authorizes_manuscript_image_storage": False,
            "authorizes_preferred_reading": False,
            "authorizes_source_tradition_preference": False,
            "authorizes_textual_critical_decision": False,
            "authorizes_theology_authority": False,
        },
        "catalogs": [
            {
                "id": "catalog",
                "storage_mode": "catalog_only",
                "bulk_download_authorized": False,
                "transcription_storage_allowed": False,
                "image_storage_allowed": False,
            }
        ],
    }
    allowlist_path = root / "allowlist.yaml"
    _write_yaml(allowlist_path, allowlist)
    _write_yaml(root / "data/raw/original_language/greek/cntr_sr/source_manifest.yaml", manifest)
    _write_yaml(root / "data/raw/original_language/witness_catalogs/manuscript_libraries.yaml", catalog)
    view_file = root / "data/candidate/original_language_evidence/canonical_source_views/cntr_sr/files/GreekNT.tsv"
    view_file.parent.mkdir(parents=True, exist_ok=True)
    view_file.write_bytes(source_bytes)
    view_digest = hashlib.sha256(view_file.read_bytes()).hexdigest()
    view_root = root / "data/candidate/original_language_evidence/canonical_source_views/cntr_sr"
    _write_yaml(
        view_root / "canonical_source_view_manifest.yaml",
        {
            "object_type": "original_language_canonical_source_view_manifest",
            "schema_version": "original_language_canonical_source_view_manifest.v1",
            "task_id": "T431",
            "source_id": "cntr_sr",
            "source_manifest": "data/raw/original_language/greek/cntr_sr/source_manifest.yaml",
            "source_archive": "data/raw/original_language/greek/cntr_sr/raw/demo.zip",
            "source_archive_sha256": digest,
            "view_root": "data/candidate/original_language_evidence/canonical_source_views/cntr_sr",
            "included_count": 1,
            "excluded_count": 1,
            "expected_book_count": 1,
            "book_scope": ["GreekNT"],
            "contains_source_provided_morphology": False,
            "contains_source_provided_lemmas": False,
            "contains_source_provided_strongs": False,
            "status": "candidate_canonical_only_view",
            "noncanonical_or_extra_material_excluded": True,
            "authority": {
                "authorizes_source_language_truth": False,
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
        },
    )
    (view_root / "included_files.jsonl").write_text(
        '{"book_id":"GreekNT","classification":"included_canonical_bible_text","sha256":"'
        + view_digest
        + '","size_bytes":'
        + str(view_file.stat().st_size)
        + ',"source_archive_path":"SR.tsv","view_path":"data/candidate/original_language_evidence/canonical_source_views/cntr_sr/files/GreekNT.tsv",'
        + '"contains_source_provided_morphology":false,"contains_source_provided_lemmas":false,'
        + '"contains_source_provided_strongs":false}\n',
        encoding="utf-8",
    )
    (view_root / "excluded_files.jsonl").write_text(
        '{"classification":"excluded_documentation_or_media","source_archive_path":"README.md"}\n',
        encoding="utf-8",
    )
    return root, allowlist_path


def test_validator_accepts_minimal_canonical_source_view(tmp_path: Path) -> None:
    root, allowlist = _minimal_root(tmp_path)

    summary = validator.validate_original_language_raw_sources(root, allowlist)

    assert summary["canonical_source_view_count"] == 1


def test_validator_rejects_canonical_view_that_omits_archive_member(tmp_path: Path) -> None:
    root, allowlist = _minimal_root(tmp_path)
    excluded = root / "data/candidate/original_language_evidence/canonical_source_views/cntr_sr/excluded_files.jsonl"
    excluded.write_text("", encoding="utf-8")

    with pytest.raises(validator.OriginalLanguageRawSourceError, match="exclusion ledger|view ledgers"):
        validator.validate_original_language_raw_sources(root, allowlist)


def test_validator_rejects_duplicate_canonical_view_archive_paths(tmp_path: Path) -> None:
    root, allowlist = _minimal_root(tmp_path)
    included = root / "data/candidate/original_language_evidence/canonical_source_views/cntr_sr/included_files.jsonl"
    included.write_text(included.read_text(encoding="utf-8") * 2, encoding="utf-8")

    with pytest.raises(validator.OriginalLanguageRawSourceError, match="duplicate source_archive_path|included rows"):
        validator.validate_original_language_raw_sources(root, allowlist)


def test_validator_rejects_mutated_source_view_even_if_ledger_is_updated(tmp_path: Path) -> None:
    root, allowlist = _minimal_root(tmp_path)
    view_file = root / "data/candidate/original_language_evidence/canonical_source_views/cntr_sr/files/GreekNT.tsv"
    view_file.write_bytes(b"ref\ttext\nMatt.1.1\tMutated candidate view\n")
    included = root / "data/candidate/original_language_evidence/canonical_source_views/cntr_sr/included_files.jsonl"
    row = json.loads(included.read_text(encoding="utf-8"))
    row["sha256"] = hashlib.sha256(view_file.read_bytes()).hexdigest()
    row["size_bytes"] = view_file.stat().st_size
    included.write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")

    with pytest.raises(validator.OriginalLanguageRawSourceError, match="archive member"):
        validator.validate_original_language_raw_sources(root, allowlist)


def test_validator_rejects_strongs_overlay_files_in_raw(tmp_path: Path) -> None:
    root, allowlist = _minimal_root(tmp_path)
    overlay = root / "data/raw/original_language/greek/cntr_sr/strongs_overlay.jsonl"
    overlay.write_text("{}", encoding="utf-8")

    with pytest.raises(validator.OriginalLanguageRawSourceError, match="raw original-language tree"):
        validator.validate_original_language_raw_sources(root, allowlist)


def test_validator_rejects_unexpected_raw_tree_files_without_magic_filename(tmp_path: Path) -> None:
    root, allowlist = _minimal_root(tmp_path)
    overlay = root / "data/raw/original_language/greek/cntr_sr/source_tokens.jsonl"
    overlay.write_text("{}", encoding="utf-8")

    with pytest.raises(validator.OriginalLanguageRawSourceError, match="raw original-language tree"):
        validator.validate_original_language_raw_sources(root, allowlist)


def test_validator_rejects_authority_leak_in_manifest(tmp_path: Path) -> None:
    root, allowlist = _minimal_root(tmp_path)
    manifest_path = root / "data/raw/original_language/greek/cntr_sr/source_manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["authority"]["authorizes_preferred_reading"] = True
    _write_yaml(manifest_path, manifest)

    with pytest.raises(validator.OriginalLanguageRawSourceError, match="authorizes_preferred_reading"):
        validator.validate_original_language_raw_sources(root, allowlist)


def test_validator_rejects_manuscript_bulk_download_authority(tmp_path: Path) -> None:
    root, allowlist = _minimal_root(tmp_path)
    catalog_path = root / "data/raw/original_language/witness_catalogs/manuscript_libraries.yaml"
    catalog = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    catalog["catalogs"][0]["bulk_download_authorized"] = True
    _write_yaml(catalog_path, catalog)

    with pytest.raises(validator.OriginalLanguageRawSourceError, match="bulk_download_authorized"):
        validator.validate_original_language_raw_sources(root, allowlist)


def test_allowlist_rejects_raw_strongs_overlay_authority(tmp_path: Path) -> None:
    data = copy.deepcopy(yaml.safe_load(ALLOWLIST.read_text(encoding="utf-8")))
    data["download_policy"]["strongs_overlay_in_raw_allowed"] = True
    path = tmp_path / "allowlist.yaml"
    _write_yaml(path, data)

    with pytest.raises(validator.OriginalLanguageRawSourceError, match="strongs_overlay_in_raw_allowed"):
        validator.validate_allowlist(path)
