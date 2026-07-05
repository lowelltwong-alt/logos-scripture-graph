#!/usr/bin/env python3
"""Build canonical-only candidate source views from T431 raw archives."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
ALLOWLIST = ROOT / ".ai" / "control" / "original_language_source_allowlist.yaml"
RAW_ROOT = ROOT / "data" / "raw" / "original_language"
OUT_ROOT = ROOT / "data" / "candidate" / "original_language_evidence" / "canonical_source_views"

HEBREW_39 = {
    "Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg", "Ruth", "1Sam", "2Sam",
    "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth", "Job", "Ps", "Prov",
    "Eccl", "Song", "Isa", "Jer", "Lam", "Ezek", "Dan", "Hos", "Joel", "Amos",
    "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal",
}

GREEK_NT_27 = {
    "Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal", "Eph",
    "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm", "Heb", "Jas",
    "1Pet", "2Pet", "1John", "2John", "3John", "Jude", "Rev",
}

TANACH_BOOKS = {
    "Genesis": "Gen",
    "Exodus": "Exod",
    "Leviticus": "Lev",
    "Numbers": "Num",
    "Deuteronomy": "Deut",
    "Joshua": "Josh",
    "Judges": "Judg",
    "Ruth": "Ruth",
    "Samuel_1": "1Sam",
    "Samuel_2": "2Sam",
    "Kings_1": "1Kgs",
    "Kings_2": "2Kgs",
    "Chronicles_1": "1Chr",
    "Chronicles_2": "2Chr",
    "Ezra": "Ezra",
    "Nehemiah": "Neh",
    "Esther": "Esth",
    "Job": "Job",
    "Psalms": "Ps",
    "Proverbs": "Prov",
    "Ecclesiastes": "Eccl",
    "Song_of_Songs": "Song",
    "Isaiah": "Isa",
    "Jeremiah": "Jer",
    "Lamentations": "Lam",
    "Ezekiel": "Ezek",
    "Daniel": "Dan",
    "Hosea": "Hos",
    "Joel": "Joel",
    "Amos": "Amos",
    "Obadiah": "Obad",
    "Jonah": "Jonah",
    "Micah": "Mic",
    "Nahum": "Nah",
    "Habakkuk": "Hab",
    "Zephaniah": "Zeph",
    "Haggai": "Hag",
    "Zechariah": "Zech",
    "Malachi": "Mal",
}

SBLGNT_BOOKS = {book: book for book in GREEK_NT_27}

UGNT_BOOKS = {
    "41MATWHT.SFM": "Matt",
    "42MRKWHT.SFM": "Mark",
    "43LUKWHT.SFM": "Luke",
    "44JHNWHT.SFM": "John",
    "45ACTWHT.SFM": "Acts",
    "46ROMWHT.SFM": "Rom",
    "471COWHT.SFM": "1Cor",
    "482COWHT.SFM": "2Cor",
    "49GALWHT.SFM": "Gal",
    "50EPHWHT.SFM": "Eph",
    "51PHPWHT.SFM": "Phil",
    "52COLWHT.SFM": "Col",
    "531THWHT.SFM": "1Thess",
    "542THWHT.SFM": "2Thess",
    "551TIWHT.SFM": "1Tim",
    "562TIWHT.SFM": "2Tim",
    "57TITWHT.SFM": "Titus",
    "58PHMWHT.SFM": "Phlm",
    "59HEBWHT.SFM": "Heb",
    "60JASWHT.SFM": "Jas",
    "611PEWHT.SFM": "1Pet",
    "622PEWHT.SFM": "2Pet",
    "631JNWHT.SFM": "1John",
    "642JNWHT.SFM": "2John",
    "653JNWHT.SFM": "3John",
    "66JUDWHT.SFM": "Jude",
    "67REVWHT.SFM": "Rev",
}


class CanonicalSourceViewError(RuntimeError):
    """Raised when a canonical-only source view cannot be built."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _root_from_raw_root(raw_root: Path) -> Path:
    parts = raw_root.parts
    if len(parts) >= 3 and parts[-3:] == ("data", "raw", "original_language"):
        return raw_root.parent.parent.parent
    return ROOT


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise CanonicalSourceViewError(f"{_rel(path)} must be a YAML mapping")
    return data


def _enabled_sources(path: Path) -> list[dict[str, Any]]:
    data = _read_yaml(path)
    return [source for source in data.get("sources", []) if source.get("enabled") is True]


def _classify_extra(name: str) -> str:
    lower = name.lower()
    suffix = Path(name).suffix.lower()
    if suffix in {".md", ".pdf", ".html", ".css", ".jpg", ".jpeg", ".png", ".svg", ".ico", ".db"}:
        return "excluded_documentation_or_media"
    if suffix in {".js", ".py", ".pl", ".rb", ".json", ".xsd", ".sty", ".ssf", ".lds"}:
        return "excluded_code_or_app_metadata"
    if suffix in {".zip", ".xlsx", ".csv"}:
        return "excluded_packaged_or_tabular_extra"
    if "index" in lower or "header" in lower or "versemap" in lower:
        return "excluded_metadata"
    if "/text/" in lower or "/sblgntapp/" in lower or "/html/" in lower or "/json/" in lower:
        return "excluded_duplicate_or_app_rendering"
    if lower.endswith(".dh.xml"):
        return "excluded_duplicate_divine_name_variant"
    return "excluded_unselected_source_material"


def _include_for_source(source_id: str, name: str) -> tuple[str, str] | None:
    path = Path(name)
    stem = path.stem
    filename = path.name
    normalized = name.replace("\\", "/")
    if source_id == "tanach_us_uxlc":
        if normalized.startswith("Books/") and filename.endswith(".xml") and not filename.endswith(".DH.xml"):
            book = TANACH_BOOKS.get(stem)
            if book:
                return book, f"{book}.xml"
    if source_id == "openscriptures_oshb":
        if "/wlc/" in normalized and filename.endswith(".xml") and stem in HEBREW_39:
            return stem, f"{stem}.xml"
    if source_id == "sblgnt":
        if "/data/sblgnt/xml/" in normalized and filename.endswith(".xml") and stem in SBLGNT_BOOKS:
            return stem, f"{stem}.xml"
    if source_id == "ugnt":
        if "/data/WH USFM/" in normalized and filename in UGNT_BOOKS:
            book = UGNT_BOOKS[filename]
            return book, f"{book}.SFM"
    if source_id == "cntr_sr":
        if filename == "SR.tsv":
            return "GreekNT", "GreekNT.tsv"
    return None


def _expected_books(source_id: str) -> set[str]:
    if source_id in {"tanach_us_uxlc", "openscriptures_oshb"}:
        return HEBREW_39
    if source_id in {"sblgnt", "ugnt"}:
        return GREEK_NT_27
    if source_id == "cntr_sr":
        return {"GreekNT"}
    raise CanonicalSourceViewError(f"no expected book set for {source_id}")


def _source_metadata_flags(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "contains_source_provided_morphology": bool(source.get("contains_source_provided_morphology", False)),
        "contains_source_provided_lemmas": bool(source.get("contains_source_provided_lemmas", False)),
        "contains_source_provided_strongs": bool(source.get("contains_source_provided_strongs", False)),
        "contains_source_provided_lemma_attributes": bool(
            source.get("contains_source_provided_lemma_attributes", False)
        ),
        "contains_source_provided_strong_lookup_hints": bool(
            source.get("contains_source_provided_strong_lookup_hints", False)
        ),
        "lemma_attribute_interpretation": str(source.get("lemma_attribute_interpretation", "none")),
        "lemma_attribute_authority": str(source.get("lemma_attribute_authority", "not_applicable")),
    }


def _included_classification(source: dict[str, Any]) -> str:
    flags = _source_metadata_flags(source)
    if any(value is True for value in flags.values()):
        return "included_canonical_bible_text_with_source_metadata"
    return "included_canonical_bible_text"


def _validate_source_specific_metadata_policy(
    source_id: str,
    view_manifest: dict[str, Any],
    included: list[dict[str, Any]],
    repo_root: Path,
) -> None:
    if source_id != "openscriptures_oshb":
        return
    required_policy = {
        "contains_source_provided_lemma_attributes": True,
        "contains_source_provided_strong_lookup_hints": True,
        "lemma_attribute_interpretation": "strong_lookup_hint",
        "lemma_attribute_authority": "metadata_only_not_local_lemma_or_strong_authority",
    }
    for key, expected in required_policy.items():
        if view_manifest.get(key) != expected:
            raise CanonicalSourceViewError(
                f"{source_id}: {key} must be {expected!r} because OSHB maps //w/@lemma to Strong metadata"
            )
    for row in included:
        for key, expected in required_policy.items():
            if row.get(key) != expected:
                raise CanonicalSourceViewError(f"{source_id}: included row {key} must be {expected!r}")
        text = (repo_root / str(row["view_path"])).read_text(encoding="utf-8")
        if 'path="//w/@lemma" osisWork="Strong"' not in text:
            raise CanonicalSourceViewError(f"{source_id}: OSHB view file is missing w@lemma Strong workPrefix")
        if " lemma=" not in text:
            raise CanonicalSourceViewError(f"{source_id}: OSHB view file is missing observed w@lemma attributes")


def build_views(
    *,
    allowlist_path: Path = ALLOWLIST,
    raw_root: Path = RAW_ROOT,
    out_root: Path = OUT_ROOT,
    check: bool = False,
) -> dict[str, Any]:
    sources = _enabled_sources(allowlist_path)
    if check:
        return _check_views(sources, raw_root, out_root)
    out_root.mkdir(parents=True, exist_ok=True)
    summaries = []
    for source in sources:
        source_id = str(source["id"])
        source_dir = raw_root / str(source["language"]) / source_id
        manifest = _read_yaml(source_dir / "source_manifest.yaml")
        archive = ROOT / str(manifest["archive_path"])
        view_dir = out_root / source_id
        if view_dir.exists():
            shutil.rmtree(view_dir)
        files_dir = view_dir / "files"
        files_dir.mkdir(parents=True, exist_ok=True)
        included = []
        excluded = []
        seen_books = set()
        with zipfile.ZipFile(archive) as zf:
            for name in sorted(n for n in zf.namelist() if not n.endswith("/")):
                selected = _include_for_source(source_id, name)
                if selected:
                    book, out_name = selected
                    data = zf.read(name)
                    target = files_dir / out_name
                    target.write_bytes(data)
                    seen_books.add(book)
                    included.append(
                        {
                            "source_archive_path": name,
                            "view_path": _rel(target),
                            "book_id": book,
                            "classification": _included_classification(source),
                            **_source_metadata_flags(source),
                            "sha256": _sha256_bytes(data),
                            "size_bytes": len(data),
                        }
                    )
                else:
                    excluded.append(
                        {
                            "source_archive_path": name,
                            "classification": _classify_extra(name),
                        }
                    )
        expected = _expected_books(source_id)
        missing = sorted(expected - seen_books)
        extra = sorted(seen_books - expected)
        if missing or extra:
            raise CanonicalSourceViewError(f"{source_id}: expected books mismatch missing={missing} extra={extra}")
        manifest_out = {
            "object_type": "original_language_canonical_source_view_manifest",
            "schema_version": "original_language_canonical_source_view_manifest.v1",
            "task_id": "T431",
            "source_id": source_id,
            "source_manifest": _rel(source_dir / "source_manifest.yaml"),
            "source_archive": _rel(archive),
            "source_archive_sha256": manifest["sha256"],
            "view_root": _rel(view_dir),
            "included_count": len(included),
            "excluded_count": len(excluded),
            "expected_book_count": len(expected),
            "book_scope": sorted(expected),
            **_source_metadata_flags(source),
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
        }
        (view_dir / "canonical_source_view_manifest.yaml").write_text(
            yaml.safe_dump(manifest_out, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
            newline="\n",
        )
        _write_jsonl(view_dir / "included_files.jsonl", included)
        _write_jsonl(view_dir / "excluded_files.jsonl", excluded)
        summaries.append({"source_id": source_id, "included": len(included), "excluded": len(excluded)})
    return {"source_count": len(summaries), "sources": summaries}


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
        newline="\n",
    )


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _check_views(sources: list[dict[str, Any]], raw_root: Path, out_root: Path) -> dict[str, Any]:
    summaries = []
    repo_root = _root_from_raw_root(raw_root)
    for source in sources:
        source_id = str(source["id"])
        source_dir = raw_root / str(source["language"]) / source_id
        raw_manifest = _read_yaml(source_dir / "source_manifest.yaml")
        view_dir = out_root / source_id
        view_manifest = _read_yaml(view_dir / "canonical_source_view_manifest.yaml")
        included = _read_jsonl(view_dir / "included_files.jsonl")
        excluded = _read_jsonl(view_dir / "excluded_files.jsonl")
        expected = _expected_books(source_id)
        archive = repo_root / str(raw_manifest["archive_path"])
        with zipfile.ZipFile(archive) as zf:
            archive_entries = {name for name in zf.namelist() if not name.endswith("/")}
        ledger_entries = [
            str(row.get("source_archive_path", ""))
            for row in [*included, *excluded]
            if row.get("source_archive_path")
        ]
        ledger_entry_set = set(ledger_entries)
        if len(ledger_entries) != len(ledger_entry_set):
            raise CanonicalSourceViewError(f"{source_id}: duplicate source_archive_path rows in view ledgers")
        if ledger_entry_set != archive_entries:
            missing = sorted(archive_entries - ledger_entry_set)[:10]
            extra = sorted(ledger_entry_set - archive_entries)[:10]
            raise CanonicalSourceViewError(
                f"{source_id}: view ledgers do not cover archive members missing={missing} extra={extra}"
            )
        with zipfile.ZipFile(archive) as zf:
            included_archive_bytes = {
                str(row["source_archive_path"]): zf.read(str(row["source_archive_path"]))
                for row in included
            }
        books = {str(row["book_id"]) for row in included}
        if books != expected:
            raise CanonicalSourceViewError(f"{source_id}: included books do not match expected canonical scope")
        if len(included) != len(expected):
            raise CanonicalSourceViewError(f"{source_id}: included rows must equal expected book count")
        if view_manifest.get("expected_book_count") != len(expected):
            raise CanonicalSourceViewError(f"{source_id}: expected_book_count mismatch")
        if set(view_manifest.get("book_scope", [])) != expected:
            raise CanonicalSourceViewError(f"{source_id}: book_scope mismatch")
        if view_manifest.get("source_archive_sha256") != raw_manifest.get("sha256"):
            raise CanonicalSourceViewError(f"{source_id}: source archive sha mismatch")
        if view_manifest.get("included_count") != len(included):
            raise CanonicalSourceViewError(f"{source_id}: included_count mismatch")
        if view_manifest.get("excluded_count") != len(excluded):
            raise CanonicalSourceViewError(f"{source_id}: excluded_count mismatch")
        if view_manifest.get("noncanonical_or_extra_material_excluded") is not True:
            raise CanonicalSourceViewError(f"{source_id}: extra-material exclusion flag must be true")
        authority = view_manifest.get("authority")
        if not isinstance(authority, dict) or any(value is not False for value in authority.values()):
            raise CanonicalSourceViewError(f"{source_id}: all authority flags must be false")
        for key, value in _source_metadata_flags(source).items():
            if isinstance(value, bool):
                if view_manifest.get(key) is not value:
                    raise CanonicalSourceViewError(f"{source_id}: {key} mismatch")
                if bool(raw_manifest.get(key, False)) is not value:
                    raise CanonicalSourceViewError(f"{source_id}: raw manifest {key} mismatch")
            else:
                if view_manifest.get(key) != value:
                    raise CanonicalSourceViewError(f"{source_id}: {key} mismatch")
                if str(raw_manifest.get(key, value)) != value:
                    raise CanonicalSourceViewError(f"{source_id}: raw manifest {key} mismatch")
        seen_books: set[str] = set()
        seen_view_paths: set[str] = set()
        expected_classification = _included_classification(source)
        for row in included:
            book_id = str(row.get("book_id", ""))
            if book_id in seen_books:
                raise CanonicalSourceViewError(f"{source_id}: duplicate included book_id {book_id}")
            seen_books.add(book_id)
            view_path = str(row.get("view_path", ""))
            if view_path in seen_view_paths:
                raise CanonicalSourceViewError(f"{source_id}: duplicate included view_path {view_path}")
            seen_view_paths.add(view_path)
            target = repo_root / view_path
            if not target.exists():
                raise CanonicalSourceViewError(f"{source_id}: missing included file {row['view_path']}")
            source_archive_path = str(row.get("source_archive_path", ""))
            archive_bytes = included_archive_bytes.get(source_archive_path)
            if archive_bytes is None:
                raise CanonicalSourceViewError(f"{source_id}: missing archive bytes for {source_archive_path}")
            archive_sha = _sha256_bytes(archive_bytes)
            if archive_sha != row["sha256"]:
                raise CanonicalSourceViewError(f"{source_id}: included row sha does not match archive member {source_archive_path}")
            if int(row.get("size_bytes", -1)) != len(archive_bytes):
                raise CanonicalSourceViewError(f"{source_id}: included row size does not match archive member {source_archive_path}")
            target_bytes = target.read_bytes()
            if target_bytes != archive_bytes:
                raise CanonicalSourceViewError(
                    f"{source_id}: included view file does not match raw archive member {row['view_path']}"
                )
            if _sha256_bytes(target_bytes) != row["sha256"]:
                raise CanonicalSourceViewError(f"{source_id}: included file sha mismatch {row['view_path']}")
            if row.get("classification") != expected_classification:
                raise CanonicalSourceViewError(f"{source_id}: included file classification is wrong")
            for key, value in _source_metadata_flags(source).items():
                if row.get(key) is not value:
                    if isinstance(value, bool):
                        raise CanonicalSourceViewError(f"{source_id}: included row {key} mismatch")
                    if row.get(key) != value:
                        raise CanonicalSourceViewError(f"{source_id}: included row {key} mismatch")
        _validate_source_specific_metadata_policy(source_id, view_manifest, included, repo_root)
        if not excluded:
            raise CanonicalSourceViewError(f"{source_id}: expected an exclusion ledger")
        for row in excluded:
            if not str(row.get("classification", "")).startswith("excluded_"):
                raise CanonicalSourceViewError(f"{source_id}: excluded row classification is wrong")
        summaries.append({"source_id": source_id, "included": len(included), "excluded": len(excluded)})
    return {"source_count": len(summaries), "sources": summaries}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allowlist", type=Path, default=ALLOWLIST)
    parser.add_argument("--raw-root", type=Path, default=RAW_ROOT)
    parser.add_argument("--out", type=Path, default=OUT_ROOT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        summary = build_views(
            allowlist_path=args.allowlist if args.allowlist.is_absolute() else ROOT / args.allowlist,
            raw_root=args.raw_root if args.raw_root.is_absolute() else ROOT / args.raw_root,
            out_root=args.out if args.out.is_absolute() else ROOT / args.out,
            check=args.check,
        )
    except (OSError, zipfile.BadZipFile, CanonicalSourceViewError, json.JSONDecodeError) as exc:
        print(f"T431 canonical source view build failed: {exc}", file=sys.stderr)
        return 1
    action = "validated" if args.check else "built"
    print(f"T431 canonical source views {action}: {summary['source_count']} source(s).")
    for item in summary["sources"]:
        print(f"- {item['source_id']}: included={item['included']} excluded={item['excluded']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
