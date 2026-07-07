#!/usr/bin/env python3
"""Build the T439 no-text full-Philemon alignment bridge pilot."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PILOT_ROOT = ROOT / "data" / "candidate" / "original_language_evidence" / "pilots" / "T439_phlm_alignment_bridge_expansion"
SBLGNT_VIEW = ROOT / "data" / "candidate" / "original_language_evidence" / "canonical_source_views" / "sblgnt" / "files" / "Phlm.xml"
SBLGNT_MANIFEST = ROOT / "data" / "candidate" / "original_language_evidence" / "canonical_source_views" / "sblgnt" / "canonical_source_view_manifest.yaml"
SBLGNT_INCLUDED = ROOT / "data" / "candidate" / "original_language_evidence" / "canonical_source_views" / "sblgnt" / "included_files.jsonl"
SBLGNT_SOURCE_MANIFEST = ROOT / "data" / "raw" / "original_language" / "greek" / "sblgnt" / "source_manifest.yaml"
WEB_WORD_TOKENS = ROOT / "data" / "canonical" / "translations" / "eng-web" / "word_tokens.jsonl"

TARGET_SPAN = "Phlm.1.1-Phlm.1.25"
CREATED_AT = "2026-07-05T00:00:00Z"
CREATED_BY = "codex"

TOKEN_NON_AUTHS = [
    "source_language_truth",
    "lexical_truth",
    "word_level_alignment_truth",
    "strongs_number_as_source_text",
    "lemma_or_morphology_population",
    "preferred_reading",
    "source_tradition_preference",
    "translation_judgment",
    "chunk_boundary",
    "graph_or_retrieval_truth",
    "theology_authority",
]

ALIGNMENT_NON_AUTHS = [
    "translation_faithfulness_judgment",
    "source_language_truth",
    "lexical_truth",
    "word_level_alignment_truth",
    "strongs_number_as_source_text",
    "chunk_boundary",
    "graph_or_retrieval_truth",
    "theology_authority",
]

EDITORIAL_NON_AUTHS = [
    "autograph_certainty",
    "speaker_resolution",
    "preferred_reading",
    "source_tradition_preference",
    "chunk_boundary",
    "theology_authority",
]


class T439BuildError(RuntimeError):
    """Raised when T439 pilot rows cannot be built."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise T439BuildError(f"{_rel(path)} must be a YAML mapping")
    return data


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise T439BuildError(f"{_rel(path)} contains a non-object JSONL row")
                rows.append(row)
    return rows


def _jsonl_text(rows: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)


def _manifest_text(data: dict[str, Any]) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def _osis_from_sblgnt(verse_id: str) -> str:
    prefix = "Philemon "
    if not verse_id.startswith(prefix):
        raise T439BuildError(f"Unexpected SBLGNT verse id: {verse_id}")
    chapter, verse = verse_id.removeprefix(prefix).split(":", 1)
    return f"Phlm.{chapter}.{verse}"


def _source_context() -> dict[str, Any]:
    manifest = _read_yaml(SBLGNT_MANIFEST)
    source_manifest = _read_yaml(SBLGNT_SOURCE_MANIFEST)
    included = [row for row in _read_jsonl(SBLGNT_INCLUDED) if row.get("book_id") == "Phlm"]
    if len(included) != 1:
        raise T439BuildError("Expected exactly one SBLGNT Phlm included-file row")
    row = included[0]
    if row.get("view_path") != _rel(SBLGNT_VIEW):
        raise T439BuildError("SBLGNT Phlm view path mismatch")
    for field in ("contains_source_provided_strongs", "contains_source_provided_lemmas", "contains_source_provided_morphology"):
        if manifest.get(field) is not False:
            raise T439BuildError(f"SBLGNT T439 expects {field}=false")
    return {"view_manifest": manifest, "source_manifest": source_manifest, "included_row": row}


def _token_authority() -> dict[str, bool]:
    return {
        "authorizes_source_language_truth": False,
        "authorizes_lexical_truth": False,
        "authorizes_word_level_alignment_truth": False,
        "authorizes_preferred_reading": False,
        "authorizes_source_tradition_preference": False,
        "authorizes_translation_judgment": False,
        "authorizes_chunk_boundary": False,
        "authorizes_graph_or_retrieval_truth": False,
        "authorizes_theology_authority": False,
    }


def _alignment_authority() -> dict[str, bool]:
    return {
        "authorizes_translation_judgment": False,
        "authorizes_source_language_truth": False,
        "authorizes_lexical_truth": False,
        "authorizes_chunk_boundary": False,
        "authorizes_graph_or_retrieval_truth": False,
        "authorizes_theology_authority": False,
    }


def _editorial_authority() -> dict[str, bool]:
    return {
        "authorizes_autograph_certainty": False,
        "authorizes_speaker_resolution": False,
        "authorizes_chunk_boundary": False,
        "authorizes_theology_authority": False,
    }


def _token_provenance(context: dict[str, Any]) -> dict[str, str]:
    source_manifest = context["source_manifest"]
    included = context["included_row"]
    return {
        "created_by": CREATED_BY,
        "created_at": CREATED_AT,
        "basis": "Observed SBLGNT XML <w> token positions from T431 canonical source view for full Philemon; visible token text is not stored in T439 rows.",
        "source_url": str(source_manifest["source_url"]),
        "source_sha256": str(included["sha256"]),
        "version_or_commit": str(source_manifest["resolved_commit"]),
    }


def _editorial_provenance(context: dict[str, Any]) -> dict[str, str]:
    source_manifest = context["source_manifest"]
    return {
        "created_by": CREATED_BY,
        "created_at": CREATED_AT,
        "basis": "Observed source-edition paragraphing, versification, punctuation/suffix presence, and sigla shape from SBLGNT Philemon XML; visible values are not stored.",
        "source_url": str(source_manifest["source_url"]),
        "license": str(source_manifest["license"]),
    }


def _source_token_row(
    *,
    context: dict[str, Any],
    osis_ref: str,
    source_token_id: str,
    token_index: int,
    verse_token_index: int,
    token_text: str,
) -> dict[str, Any]:
    source_manifest = context["source_manifest"]
    included = context["included_row"]
    return {
        "id": f"source-token:t439:sblgnt:{osis_ref}:{verse_token_index:06d}",
        "type": "SourceLanguageToken",
        "schema_version": "source_language_token.v1",
        "source_id": "sblgnt",
        "source_manifest": "data/raw/original_language/greek/sblgnt/source_manifest.yaml",
        "canonical_source_view_manifest": _rel(SBLGNT_MANIFEST),
        "source_archive_path": str(included["source_archive_path"]),
        "source_view_path": _rel(SBLGNT_VIEW),
        "source_file_sha256": str(included["sha256"]),
        "license": str(source_manifest["license"]),
        "language": "greek",
        "book_id": "Phlm",
        "osis_ref": osis_ref,
        "source_token_id": source_token_id,
        "token_index": token_index,
        "verse_token_index": verse_token_index,
        "token_text_sha256": _sha256_text(token_text),
        "token_char_count": len(token_text),
        "lemma": None,
        "morphology": None,
        "strong_id": None,
        "phrase_clause_context": "Not assigned in T439; phrase/clause context requires later review.",
        "discourse_context": "Full Philemon verse-level bridge only; no discourse, theology, or translation-faithfulness claim is authorized.",
        "evidence_mode": "observed_source_view",
        "inferred_vs_observed": "observed",
        "text_storage_policy": {
            "stores_source_text": False,
            "license_authorized_for_storage": True,
            "storage_note": "T439 stores token IDs and token hashes only; visible SBLGNT token text is not stored in this expanded pilot.",
        },
        "textual_variant_dependency": "none_known",
        "witness_support_summary": "Observed from SBLGNT canonical source view only; no manuscript witness support row is asserted in T439.",
        "confidence": "high",
        "trust_zone": "candidate",
        "status": "candidate",
        "provenance": _token_provenance(context),
        "authority": _token_authority(),
        "non_authorizations": TOKEN_NON_AUTHS,
    }


def _editorial_row(
    *,
    context: dict[str, Any],
    row_id: str,
    layer_kind: str,
    osis_ref: str,
    source_marker_or_field: str,
    raw_value: str,
    applies_to_source_token_ids: list[str] | None = None,
) -> dict[str, Any]:
    included = context["included_row"]
    return {
        "id": row_id,
        "type": "EditorialLayer",
        "schema_version": "editorial_layer.v1",
        "layer_kind": layer_kind,
        "source_id": "sblgnt",
        "source_manifest": "data/raw/original_language/greek/sblgnt/source_manifest.yaml",
        "canonical_source_view_manifest": _rel(SBLGNT_MANIFEST),
        "source_view_path": _rel(SBLGNT_VIEW),
        "source_file_sha256": str(included["sha256"]),
        "osis_ref": osis_ref,
        "applies_to_source_token_ids": applies_to_source_token_ids or [],
        "observed_value": "redacted_no_text_value_present",
        "observed_value_sha256": _sha256_text(raw_value),
        "observed_value_char_count": len(raw_value),
        "source_marker_or_field": source_marker_or_field,
        "editorial_origin": "source_edition",
        "is_editorial_not_autograph_certainty": True,
        "evidence_mode": "observed_source_view",
        "confidence": "high",
        "trust_zone": "candidate",
        "status": "candidate",
        "provenance": _editorial_provenance(context),
        "authority": _editorial_authority(),
        "non_authorizations": EDITORIAL_NON_AUTHS,
    }


def _parse_sblgnt(context: dict[str, Any]) -> tuple[list[str], list[dict[str, Any]], list[dict[str, Any]]]:
    root = ET.parse(SBLGNT_VIEW).getroot()
    refs: list[str] = []
    tokens: list[dict[str, Any]] = []
    editorial_layers: list[dict[str, Any]] = []
    for paragraph_index, paragraph in enumerate(root.findall("p"), start=1):
        paragraph_refs = [
            _osis_from_sblgnt(str(elem.attrib.get("id", "")))
            for elem in paragraph.iter()
            if elem.tag == "verse-number"
        ]
        if not paragraph_refs:
            continue
        span = paragraph_refs[0] if len(paragraph_refs) == 1 else f"{paragraph_refs[0]}-{paragraph_refs[-1]}"
        editorial_layers.append(
            _editorial_row(
                context=context,
                row_id=f"editorial:t439:sblgnt:{span}:paragraphing:{paragraph_index:03d}",
                layer_kind="paragraphing",
                osis_ref=span,
                source_marker_or_field="p",
                raw_value=span,
            )
        )
    current_ref: str | None = None
    verse_counts: defaultdict[str, int] = defaultdict(int)
    last_token_id_by_ref: dict[str, str] = {}
    editorial_index = len(editorial_layers)
    token_index = 0

    for elem in root.iter():
        if elem.tag == "verse-number":
            current_ref = _osis_from_sblgnt(str(elem.attrib.get("id", "")))
            refs.append(current_ref)
            editorial_index += 1
            editorial_layers.append(
                _editorial_row(
                    context=context,
                    row_id=f"editorial:t439:sblgnt:{current_ref}:versification:{editorial_index:03d}",
                    layer_kind="versification",
                    osis_ref=current_ref,
                    source_marker_or_field="verse-number",
                    raw_value=str(elem.text or ""),
                )
            )
            continue
        if current_ref is None:
            continue
        if elem.tag == "w":
            verse_counts[current_ref] += 1
            verse_token_index = verse_counts[current_ref]
            source_token_id = f"sblgnt:Phlm:{current_ref}:{verse_token_index:06d}"
            tokens.append(
                _source_token_row(
                    context=context,
                    osis_ref=current_ref,
                    source_token_id=source_token_id,
                    token_index=token_index,
                    verse_token_index=verse_token_index,
                    token_text=str(elem.text or ""),
                )
            )
            last_token_id_by_ref[current_ref] = source_token_id
            token_index += 1
        elif elem.tag in {"prefix", "suffix"} and elem.text:
            editorial_index += 1
            applies = []
            if elem.tag == "suffix" and current_ref in last_token_id_by_ref:
                applies = [last_token_id_by_ref[current_ref]]
            editorial_layers.append(
                _editorial_row(
                    context=context,
                    row_id=f"editorial:t439:sblgnt:{current_ref}:{elem.tag}:{editorial_index:03d}",
                    layer_kind="punctuation",
                    osis_ref=current_ref,
                    source_marker_or_field=elem.tag,
                    raw_value=str(elem.text),
                    applies_to_source_token_ids=applies,
                )
            )
    expected = [f"Phlm.1.{i}" for i in range(1, 26)]
    if refs != expected:
        raise T439BuildError(f"SBLGNT Philemon refs must be {expected}, got {refs}")
    token_refs = {str(row["osis_ref"]) for row in tokens}
    if token_refs != set(expected):
        raise T439BuildError("SBLGNT token parse did not cover all Philemon refs")
    return refs, tokens, editorial_layers


def _web_tokens(target_refs: list[str]) -> dict[str, list[dict[str, Any]]]:
    if not WEB_WORD_TOKENS.exists():
        raise T439BuildError(
            f"{_rel(WEB_WORD_TOKENS)} is missing; run pipelines/ingest/usfm_importer.py --canonical-66-filter first"
        )
    grouped: dict[str, list[dict[str, Any]]] = {ref: [] for ref in target_refs}
    with WEB_WORD_TOKENS.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            ref = row.get("osis_ref")
            if ref in grouped:
                grouped[ref].append(row)
    missing = [ref for ref, rows in grouped.items() if not rows]
    if missing:
        raise T439BuildError(f"Missing WEB word tokens for {missing}")
    return grouped


def _alignment_records(target_refs: list[str], tokens: list[dict[str, Any]], context: dict[str, Any]) -> list[dict[str, Any]]:
    by_ref: dict[str, list[dict[str, Any]]] = {ref: [] for ref in target_refs}
    for row in tokens:
        by_ref[row["osis_ref"]].append(row)
    web = _web_tokens(target_refs)
    source_manifest = context["source_manifest"]
    rows: list[dict[str, Any]] = []
    for ref in target_refs:
        web_rows = web[ref]
        strong_ids = sorted({str(row.get("strong")) for row in web_rows if row.get("strong")})
        rows.append(
            {
                "id": f"alignment:t439:eng-web:sblgnt:{ref}",
                "type": "AlignmentRecord",
                "schema_version": "alignment_record.v2",
                "passage_id": f"scripture:{ref}",
                "osis_ref": ref,
                "translation_id": "eng-web",
                "translation_token_ids": [str(row["id"]) for row in web_rows],
                "source": {
                    "language": "greek",
                    "source_id": "sblgnt",
                    "canonical_source_view_manifest": _rel(SBLGNT_MANIFEST),
                    "strong": None,
                    "source_token_ids": [str(row["source_token_id"]) for row in by_ref[ref]],
                },
                "alignment_type": "many_to_many",
                "alignment_basis": "source_token_order",
                "method": "source_view_bridge",
                "evidence_mode": "inferred",
                "inferred_vs_observed": "inferred",
                "confidence": "low",
                "trust_zone": "candidate",
                "review_status": "unreviewed",
                "translation_side_strong_hints": strong_ids,
                "translation_strong_hints_are_source_text": False,
                "translation_text_stored": False,
                "translation_strong_hints_note": "Observed from WEB word-token sidecars only; not written into SBLGNT source tokens and not translation judgment.",
                "provenance": {
                    "created_by": CREATED_BY,
                    "created_at": CREATED_AT,
                    "basis": "Verse-level no-text bridge from observed SBLGNT token IDs to WEB word-token IDs; not word-level alignment truth.",
                    "source_manifest": "data/raw/original_language/greek/sblgnt/source_manifest.yaml",
                    "license": str(source_manifest["license"]),
                },
                "authority": _alignment_authority(),
                "non_authorizations": ALIGNMENT_NON_AUTHS,
                "status": "candidate",
            }
        )
    return rows


def build_outputs() -> dict[str, str]:
    context = _source_context()
    refs, tokens, editorial_layers = _parse_sblgnt(context)
    alignments = _alignment_records(refs, tokens, context)
    manifest = {
        "object_type": "t439_phlm_alignment_bridge_expansion_manifest",
        "schema_version": "t439_phlm_alignment_bridge_expansion_manifest.v1",
        "task_id": "T439",
        "status": "candidate_pilot",
        "trust_zone": "candidate",
        "pilot_span": TARGET_SPAN,
        "exact_refs": refs,
        "source_id": "sblgnt",
        "source_manifest": "data/raw/original_language/greek/sblgnt/source_manifest.yaml",
        "canonical_source_view_manifest": _rel(SBLGNT_MANIFEST),
        "source_view_path": _rel(SBLGNT_VIEW),
        "source_file_sha256": str(context["included_row"]["sha256"]),
        "source_archive_path": str(context["included_row"]["source_archive_path"]),
        "license": str(context["source_manifest"]["license"]),
        "source_url": str(context["source_manifest"]["source_url"]),
        "version_or_commit": str(context["source_manifest"]["resolved_commit"]),
        "counts": {
            "source_language_tokens": len(tokens),
            "editorial_layers": len(editorial_layers),
            "alignment_records": len(alignments),
            "refs": len(refs),
        },
        "no_text_policy": {
            "stores_source_text": False,
            "stores_translation_text": False,
            "stores_token_text_hashes": True,
            "stores_punctuation_values": False,
        },
        "web_strongs_policy": "WEB Strong's IDs are translation-side hints only and are not source text, lexical truth, translation judgment, or theology authority.",
        "rust_policy": "No Rust in T439; T439 is the Python parity fixture for a future Rust no-text alignment coverage index.",
        "authority": {
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
            "creates_reviewed_gold": False,
            "creates_chunk_output": False,
            "changes_route_behavior": False,
            "changes_evaluator_behavior": False,
            "creates_graph_or_retrieval_truth": False,
            "runs_embeddings_or_builds_indexes": False,
            "authorizes_theology_authority": False,
        },
        "outputs": {
            "source_language_tokens": "source_language_tokens.jsonl",
            "editorial_layers": "editorial_layers.jsonl",
            "alignment_records": "alignment_records.jsonl",
        },
    }
    return {
        "manifest.yaml": _manifest_text(manifest),
        "source_language_tokens.jsonl": _jsonl_text(tokens),
        "editorial_layers.jsonl": _jsonl_text(editorial_layers),
        "alignment_records.jsonl": _jsonl_text(alignments),
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
        raise T439BuildError("T439 pilot outputs are not current: " + "; ".join(details))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate generated files without rewriting them.")
    args = parser.parse_args(argv)
    try:
        if args.check:
            check_outputs()
            print("T439 Philemon alignment bridge expansion outputs are current.")
        else:
            outputs = write_outputs()
            print(f"T439 Philemon alignment bridge expansion built in {_rel(PILOT_ROOT)} ({len(outputs)} files).")
    except (OSError, ET.ParseError, json.JSONDecodeError, yaml.YAMLError, T439BuildError) as exc:
        print(f"T439 Philemon alignment bridge expansion build failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
