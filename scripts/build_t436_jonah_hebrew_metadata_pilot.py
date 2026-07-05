#!/usr/bin/env python3
"""Build the T436 Jonah Hebrew no-text observation/parity pilot."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PILOT_ROOT = (
    ROOT
    / "data"
    / "candidate"
    / "original_language_evidence"
    / "pilots"
    / "T436_jonah_hebrew_observation_parity"
)

UXLC_VIEW_ROOT = ROOT / "data" / "candidate" / "original_language_evidence" / "canonical_source_views" / "tanach_us_uxlc"
OSHB_VIEW_ROOT = (
    ROOT / "data" / "candidate" / "original_language_evidence" / "canonical_source_views" / "openscriptures_oshb"
)
UXLC_VIEW = UXLC_VIEW_ROOT / "files" / "Jonah.xml"
OSHB_VIEW = OSHB_VIEW_ROOT / "files" / "Jonah.xml"
UXLC_MANIFEST = UXLC_VIEW_ROOT / "canonical_source_view_manifest.yaml"
OSHB_MANIFEST = OSHB_VIEW_ROOT / "canonical_source_view_manifest.yaml"
UXLC_INCLUDED = UXLC_VIEW_ROOT / "included_files.jsonl"
OSHB_INCLUDED = OSHB_VIEW_ROOT / "included_files.jsonl"
UXLC_SOURCE_MANIFEST = ROOT / "data" / "raw" / "original_language" / "hebrew" / "tanach_us_uxlc" / "source_manifest.yaml"
OSHB_SOURCE_MANIFEST = (
    ROOT / "data" / "raw" / "original_language" / "hebrew" / "openscriptures_oshb" / "source_manifest.yaml"
)

BOOK_ID = "Jonah"
EXPECTED_CHAPTERS = 4
EXPECTED_VERSES = 48
EXPECTED_TOKENS = 688
SPOTLIGHT_REFS = ("Jonah.1.1", "Jonah.1.2", "Jonah.1.3")
CREATED_AT = "2026-07-04T00:00:00Z"
CREATED_BY = "codex"

OSIS_NS = {"osis": "http://www.bibletechnologies.net/2003/OSIS/namespace"}

NON_AUTHS = [
    "source_language_truth",
    "lexical_truth",
    "word_level_alignment_truth",
    "strongs_number_as_source_text",
    "lemma_or_morphology_population",
    "preferred_reading",
    "source_tradition_preference",
    "textual_critical_decision",
    "manuscript_witness_support",
    "translation_faithfulness_judgment",
    "chunk_boundary",
    "reviewed_gold",
    "chunk_output",
    "graph_or_retrieval_truth",
    "theology_authority",
]


class T436BuildError(RuntimeError):
    """Raised when T436 pilot rows cannot be built."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def _read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise T436BuildError(f"{_rel(path)} must be a YAML mapping")
    return data


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _jsonl_text(rows: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)


def _manifest_text(data: dict[str, Any]) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def _authority() -> dict[str, bool]:
    return {
        "authorizes_source_language_truth": False,
        "authorizes_lexical_truth": False,
        "authorizes_word_level_alignment_truth": False,
        "authorizes_strongs_as_source_text": False,
        "authorizes_lemma_or_morphology_population": False,
        "authorizes_preferred_reading": False,
        "authorizes_source_tradition_preference": False,
        "authorizes_textual_critical_decision": False,
        "authorizes_manuscript_witness_support": False,
        "authorizes_canon_scope_change": False,
        "authorizes_translation_judgment": False,
        "authorizes_chunk_boundary": False,
        "authorizes_reviewed_gold": False,
        "authorizes_chunk_output": False,
        "authorizes_route_behavior": False,
        "authorizes_evaluator_behavior": False,
        "authorizes_graph_or_retrieval_truth": False,
        "authorizes_embeddings_or_indexes": False,
        "authorizes_theology_authority": False,
    }


def _context(source_id: str) -> dict[str, Any]:
    if source_id == "tanach_us_uxlc":
        view, manifest_path, included_path, source_manifest_path = UXLC_VIEW, UXLC_MANIFEST, UXLC_INCLUDED, UXLC_SOURCE_MANIFEST
    elif source_id == "openscriptures_oshb":
        view, manifest_path, included_path, source_manifest_path = OSHB_VIEW, OSHB_MANIFEST, OSHB_INCLUDED, OSHB_SOURCE_MANIFEST
    else:
        raise T436BuildError(f"Unknown source {source_id}")

    manifest = _read_yaml(manifest_path)
    source_manifest = _read_yaml(source_manifest_path)
    rows = [row for row in _read_jsonl(included_path) if row.get("book_id") == BOOK_ID]
    if len(rows) != 1:
        raise T436BuildError(f"Expected exactly one {source_id} Jonah included row")
    included = rows[0]
    if included.get("view_path") != _rel(view):
        raise T436BuildError(f"{source_id} Jonah included view_path mismatch")
    actual_sha = _sha256_file(view)
    if included.get("sha256") != actual_sha:
        raise T436BuildError(f"{source_id} Jonah source-view checksum mismatch")
    return {
        "source_id": source_id,
        "view": view,
        "manifest_path": manifest_path,
        "included_path": included_path,
        "source_manifest_path": source_manifest_path,
        "manifest": manifest,
        "source_manifest": source_manifest,
        "included": included,
        "actual_sha": actual_sha,
    }


def _file_observation(ctx: dict[str, Any], *, parser_profile: str) -> dict[str, Any]:
    included = ctx["included"]
    manifest = ctx["manifest"]
    return {
        "id": f"source-view-file:t436:{ctx['source_id']}:Jonah",
        "object_type": "t436_source_view_file_observation",
        "task_id": "T436",
        "source_id": ctx["source_id"],
        "language": "hebrew",
        "book_id": BOOK_ID,
        "parser_profile": parser_profile,
        "canonical_source_view_manifest": _rel(ctx["manifest_path"]),
        "included_files_ledger": _rel(ctx["included_path"]),
        "source_manifest": _rel(ctx["source_manifest_path"]),
        "source_view_path": _rel(ctx["view"]),
        "source_archive_path": str(included["source_archive_path"]),
        "source_file_sha256": ctx["actual_sha"],
        "size_bytes": int(included["size_bytes"]),
        "manifest_flags": {
            "contains_source_provided_morphology": bool(manifest.get("contains_source_provided_morphology")),
            "contains_source_provided_lemmas": bool(manifest.get("contains_source_provided_lemmas")),
            "contains_source_provided_strongs": bool(manifest.get("contains_source_provided_strongs")),
        },
        "stores_source_text": False,
        "consumes_raw_archive_directly": False,
        "trust_zone": "candidate",
        "status": "candidate",
        "provenance": {
            "created_by": CREATED_BY,
            "created_at": CREATED_AT,
            "basis": "Observed from the T431 canonical source view and included-files ledger, not from raw archive extraction.",
            "source_url": str(ctx["source_manifest"].get("source_url", "")),
            "source_sha256": str(included["sha256"]),
            "version_or_commit": str(
                ctx["source_manifest"].get("resolved_commit")
                or ctx["source_manifest"].get("expected_version")
                or ctx["source_manifest"].get("expected_build")
                or "not_recorded"
            ),
        },
        "authority": _authority(),
        "non_authorizations": NON_AUTHS,
    }


def _token_row(
    *,
    source_id: str,
    osis_ref: str,
    token_index: int,
    verse_token_index: int,
    token_text: str,
    attr_keys: list[str],
    nested_tags: list[str],
) -> dict[str, Any]:
    source_token_id = f"{source_id}:Jonah:{osis_ref}:{verse_token_index:06d}"
    return {
        "id": f"token-shape:t436:{source_id}:{osis_ref}:{verse_token_index:06d}",
        "object_type": "t436_token_shape_observation",
        "task_id": "T436",
        "source_id": source_id,
        "language": "hebrew",
        "book_id": BOOK_ID,
        "osis_ref": osis_ref,
        "source_token_id": source_token_id,
        "token_index": token_index,
        "verse_token_index": verse_token_index,
        "token_text_sha256": _sha256_text(token_text),
        "token_char_count": len(token_text),
        "attribute_keys": attr_keys,
        "has_morph_attr": "morph" in attr_keys,
        "has_lemma_attr": "lemma" in attr_keys,
        "has_strong_attr": "strong" in attr_keys,
        "has_nested_markup": bool(nested_tags),
        "nested_tags": nested_tags,
        "stores_source_text": False,
        "stores_morphology_value": False,
        "stores_lemma_value": False,
        "stores_strongs_value": False,
        "trust_zone": "candidate",
        "status": "candidate",
        "authority": _authority(),
        "non_authorizations": NON_AUTHS,
    }


def _verse_row(source_id: str, osis_ref: str, token_ids: list[str], token_hashes: list[str]) -> dict[str, Any]:
    return {
        "id": f"verse-observation:t436:{source_id}:{osis_ref}",
        "object_type": "t436_verse_token_observation",
        "task_id": "T436",
        "source_id": source_id,
        "language": "hebrew",
        "book_id": BOOK_ID,
        "osis_ref": osis_ref,
        "token_count": len(token_ids),
        "source_token_ids": token_ids,
        "token_hash_chain_sha256": _sha256_text("|".join(token_hashes)),
        "stores_source_text": False,
        "trust_zone": "candidate",
        "status": "candidate",
        "authority": _authority(),
        "non_authorizations": NON_AUTHS,
    }


def _editorial_row(source_id: str, marker_kind: str, count: int, refs: list[str] | None = None) -> dict[str, Any]:
    return {
        "id": f"editorial-shape:t436:{source_id}:{marker_kind}",
        "object_type": "t436_editorial_metadata_shape_observation",
        "task_id": "T436",
        "source_id": source_id,
        "language": "hebrew",
        "book_id": BOOK_ID,
        "marker_kind": marker_kind,
        "count": count,
        "refs": refs or [],
        "is_editorial_not_autograph_certainty": True,
        "stores_source_text": False,
        "trust_zone": "candidate",
        "status": "candidate",
        "authority": _authority(),
        "non_authorizations": NON_AUTHS,
    }


def _parse_uxlc(ctx: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    root = ET.parse(ctx["view"]).getroot()
    token_rows: list[dict[str, Any]] = []
    verse_rows: list[dict[str, Any]] = []
    editorial_rows: list[dict[str, Any]] = []
    token_index = 0
    chapter_refs: set[str] = set()
    marker_counts: Counter[str] = Counter()
    nested_token_refs: list[str] = []

    for chapter in root.findall(".//c"):
        chapter_no = str(chapter.attrib.get("n", ""))
        if chapter_no:
            chapter_refs.add(f"Jonah.{chapter_no}")
        for verse in chapter.findall("v"):
            verse_no = str(verse.attrib.get("n", ""))
            osis_ref = f"Jonah.{chapter_no}.{verse_no}"
            token_ids: list[str] = []
            token_hashes: list[str] = []
            for verse_token_index, word in enumerate(verse.findall("w"), start=1):
                token_text = "".join(word.itertext())
                nested_tags = sorted({str(child.tag) for child in list(word)})
                if nested_tags:
                    nested_token_refs.append(osis_ref)
                row = _token_row(
                    source_id="tanach_us_uxlc",
                    osis_ref=osis_ref,
                    token_index=token_index,
                    verse_token_index=verse_token_index,
                    token_text=token_text,
                    attr_keys=sorted(word.attrib.keys()),
                    nested_tags=nested_tags,
                )
                token_rows.append(row)
                token_ids.append(str(row["source_token_id"]))
                token_hashes.append(str(row["token_text_sha256"]))
                token_index += 1
            verse_rows.append(_verse_row("tanach_us_uxlc", osis_ref, token_ids, token_hashes))

    for tag in ("samekh", "pe", "vs", "correction", "note"):
        marker_counts[tag] = len(root.findall(f".//{tag}"))
    marker_counts["chaptering"] = len(chapter_refs)
    marker_counts["versification"] = len(verse_rows)
    marker_counts["nested_token_markup"] = len(nested_token_refs)
    marker_counts["vowel_or_accent_presence"] = len(token_rows)

    for marker_kind, count in sorted(marker_counts.items()):
        editorial_rows.append(_editorial_row("tanach_us_uxlc", marker_kind, count, sorted(set(nested_token_refs))))

    return token_rows, verse_rows, editorial_rows


def _parse_oshb(ctx: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    root = ET.parse(ctx["view"]).getroot()
    token_rows: list[dict[str, Any]] = []
    verse_rows: list[dict[str, Any]] = []
    editorial_rows: list[dict[str, Any]] = []
    token_index = 0
    chapter_count = 0
    marker_counts: Counter[str] = Counter()

    for chapter in root.findall(".//osis:chapter", OSIS_NS):
        chapter_id = str(chapter.attrib.get("osisID", ""))
        if chapter_id.startswith("Jonah."):
            chapter_count += 1
        for verse in chapter.findall("osis:verse", OSIS_NS):
            osis_ref = str(verse.attrib.get("osisID", ""))
            if not osis_ref.startswith("Jonah."):
                continue
            token_ids: list[str] = []
            token_hashes: list[str] = []
            for child in list(verse):
                local = child.tag.split("}", 1)[-1]
                if local == "w":
                    token_text = "".join(child.itertext())
                    row = _token_row(
                        source_id="openscriptures_oshb",
                        osis_ref=osis_ref,
                        token_index=token_index,
                        verse_token_index=len(token_ids) + 1,
                        token_text=token_text,
                        attr_keys=sorted(child.attrib.keys()),
                        nested_tags=sorted({grand.tag.split("}", 1)[-1] for grand in list(child)}),
                    )
                    token_rows.append(row)
                    token_ids.append(str(row["source_token_id"]))
                    token_hashes.append(str(row["token_text_sha256"]))
                    token_index += 1
                elif local == "seg":
                    marker_counts[f"seg:{child.attrib.get('type', 'unknown')}"] += 1
            verse_rows.append(_verse_row("openscriptures_oshb", osis_ref, token_ids, token_hashes))

    marker_counts["chaptering"] = chapter_count
    marker_counts["versification"] = len(verse_rows)
    marker_counts["morph_attr_presence"] = sum(1 for row in token_rows if row["has_morph_attr"])
    marker_counts["lemma_attr_presence"] = sum(1 for row in token_rows if row["has_lemma_attr"])
    marker_counts["strong_attr_presence"] = sum(1 for row in token_rows if row["has_strong_attr"])
    marker_counts["vowel_or_accent_presence"] = len(token_rows)

    for marker_kind, count in sorted(marker_counts.items()):
        editorial_rows.append(_editorial_row("openscriptures_oshb", marker_kind, count))

    return token_rows, verse_rows, editorial_rows


def _by_ref(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row["osis_ref"]): row for row in rows}


def _parity_summary(
    uxlc_tokens: list[dict[str, Any]],
    uxlc_verses: list[dict[str, Any]],
    oshb_tokens: list[dict[str, Any]],
    oshb_verses: list[dict[str, Any]],
    uxlc_ctx: dict[str, Any],
    oshb_ctx: dict[str, Any],
) -> dict[str, Any]:
    uxlc_by_ref = _by_ref(uxlc_verses)
    oshb_by_ref = _by_ref(oshb_verses)
    refs_match = set(uxlc_by_ref) == set(oshb_by_ref)
    per_verse_token_counts_match = refs_match and all(
        uxlc_by_ref[ref]["token_count"] == oshb_by_ref[ref]["token_count"] for ref in sorted(uxlc_by_ref)
    )
    token_hashes_match = [
        str(uxlc_tokens[index]["token_text_sha256"]) == str(oshb_tokens[index]["token_text_sha256"])
        for index in range(min(len(uxlc_tokens), len(oshb_tokens)))
    ]
    observed_lemma_count = sum(1 for row in oshb_tokens if row["has_lemma_attr"])
    observed_morph_count = sum(1 for row in oshb_tokens if row["has_morph_attr"])
    return {
        "object_type": "t436_jonah_hebrew_observation_parity_summary",
        "task_id": "T436",
        "book_id": BOOK_ID,
        "sources": ["tanach_us_uxlc", "openscriptures_oshb"],
        "spotlight_refs": list(SPOTLIGHT_REFS),
        "expected_counts": {
            "chapters": EXPECTED_CHAPTERS,
            "verses_per_source": EXPECTED_VERSES,
            "tokens_per_source": EXPECTED_TOKENS,
        },
        "observed_counts": {
            "uxlc_verses": len(uxlc_verses),
            "oshb_verses": len(oshb_verses),
            "uxlc_tokens": len(uxlc_tokens),
            "oshb_tokens": len(oshb_tokens),
            "oshb_morph_attr_count": observed_morph_count,
            "oshb_lemma_attr_count": observed_lemma_count,
            "oshb_strong_attr_count": sum(1 for row in oshb_tokens if row["has_strong_attr"]),
        },
        "refs_match": refs_match,
        "per_verse_token_counts_match": per_verse_token_counts_match,
        "exact_token_hashes_all_match": len(token_hashes_match) == len(uxlc_tokens) == len(oshb_tokens)
        and all(token_hashes_match),
        "metadata_flag_drift": {
            "source_id": "openscriptures_oshb",
            "manifest_contains_source_provided_lemmas": bool(
                oshb_ctx["manifest"].get("contains_source_provided_lemmas")
            ),
            "observed_lemma_attr_count": observed_lemma_count,
            "requires_policy_before_rust_expansion": observed_lemma_count > 0
            and not bool(oshb_ctx["manifest"].get("contains_source_provided_lemmas")),
            "note": "OSHB w@lemma is observed as a source XML attribute, but T436 does not copy it into local lemma, strong_id, lexeme, or morphology production rows.",
        },
        "source_view_checksums": {
            "tanach_us_uxlc": uxlc_ctx["actual_sha"],
            "openscriptures_oshb": oshb_ctx["actual_sha"],
        },
        "rust_expansion_allowed": False,
        "stores_source_text": False,
        "authority": _authority(),
        "non_authorizations": NON_AUTHS,
    }


def build_outputs() -> dict[str, str]:
    uxlc_ctx = _context("tanach_us_uxlc")
    oshb_ctx = _context("openscriptures_oshb")
    uxlc_tokens, uxlc_verses, uxlc_editorial = _parse_uxlc(uxlc_ctx)
    oshb_tokens, oshb_verses, oshb_editorial = _parse_oshb(oshb_ctx)
    file_rows = [
        _file_observation(uxlc_ctx, parser_profile="uxlc_tanach_xml"),
        _file_observation(oshb_ctx, parser_profile="oshb_osis_xml"),
    ]
    token_rows = uxlc_tokens + oshb_tokens
    verse_rows = uxlc_verses + oshb_verses
    editorial_rows = uxlc_editorial + oshb_editorial
    parity = _parity_summary(uxlc_tokens, uxlc_verses, oshb_tokens, oshb_verses, uxlc_ctx, oshb_ctx)
    manifest = {
        "object_type": "t436_jonah_hebrew_observation_parity_manifest",
        "schema_version": "t436_jonah_hebrew_observation_parity_manifest.v1",
        "task_id": "T436",
        "status": "candidate_pilot",
        "trust_zone": "candidate",
        "book_id": BOOK_ID,
        "source_ids": ["tanach_us_uxlc", "openscriptures_oshb"],
        "pilot_root": _rel(PILOT_ROOT),
        "no_text_ledgers": True,
        "consumes_raw_archives_directly": False,
        "counts": {
            "source_view_file_observations": len(file_rows),
            "verse_token_observations": len(verse_rows),
            "token_shape_index": len(token_rows),
            "editorial_metadata_shape_index": len(editorial_rows),
        },
        "metadata_flag_drift": parity["metadata_flag_drift"],
        "rust_policy": "No Rust expansion in T436; future Rust must wait for this Hebrew no-text parity pilot and the OSHB lemma-attribute drift decision.",
        "authority": _authority(),
        "outputs": {
            "source_view_file_observations": "source_view_file_observations.jsonl",
            "verse_token_observations": "verse_token_observations.jsonl",
            "token_shape_index": "token_shape_index.jsonl",
            "editorial_metadata_shape_index": "editorial_metadata_shape_index.jsonl",
            "parity_summary": "parity_summary.json",
        },
    }
    return {
        "manifest.yaml": _manifest_text(manifest),
        "source_view_file_observations.jsonl": _jsonl_text(file_rows),
        "verse_token_observations.jsonl": _jsonl_text(verse_rows),
        "token_shape_index.jsonl": _jsonl_text(token_rows),
        "editorial_metadata_shape_index.jsonl": _jsonl_text(editorial_rows),
        "parity_summary.json": json.dumps(parity, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    }


def write_outputs() -> dict[str, str]:
    outputs = build_outputs()
    PILOT_ROOT.mkdir(parents=True, exist_ok=True)
    for name, text in outputs.items():
        (PILOT_ROOT / name).write_text(text, encoding="utf-8", newline="\n")
    return outputs


def check_outputs() -> None:
    outputs = build_outputs()
    missing: list[str] = []
    stale: list[str] = []
    for name, expected in outputs.items():
        path = PILOT_ROOT / name
        if not path.exists():
            missing.append(_rel(path))
            continue
        if path.read_text(encoding="utf-8") != expected:
            stale.append(_rel(path))
    if missing or stale:
        details = []
        if missing:
            details.append("missing=" + ", ".join(missing))
        if stale:
            details.append("stale=" + ", ".join(stale))
        raise T436BuildError("T436 pilot outputs are not current: " + "; ".join(details))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate generated files without rewriting them.")
    args = parser.parse_args(argv)
    try:
        if args.check:
            check_outputs()
            print("T436 Jonah Hebrew observation parity outputs are current.")
        else:
            outputs = write_outputs()
            print(f"T436 Jonah Hebrew observation parity pilot built in {_rel(PILOT_ROOT)} ({len(outputs)} files).")
    except (OSError, ET.ParseError, json.JSONDecodeError, yaml.YAMLError, T436BuildError) as exc:
        print(f"T436 Jonah Hebrew observation parity build failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
