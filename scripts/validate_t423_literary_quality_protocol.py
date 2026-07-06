#!/usr/bin/env python3
"""Validate T423 literary-marker quality protocol and model artifacts."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / ".ai" / "control" / "multi_model_whole_bible_chunking_fork.yaml"
PROTOCOL = ROOT / ".ai" / "control" / "t423_literary_marker_quality_protocol.yaml"
PROMPT = ROOT / ".ai" / "prompts" / "multi_model_whole_bible_chunking_marathon_prompt.md"
TEMPLATE_MANIFEST = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "models" / "_TEMPLATE" / "model_manifest.yaml"
SPAN_FEATURES = ROOT / "build" / "observation_substrate" / "current" / "span_observation_features.jsonl"

LOW_CONFIDENCE = {"low", "medium_low"}
FRONTIER_BOOKS = {"Dan", "Rev"}
PILOT_FRAGILE_BOOKS = {"Gen", "Ps", "Phlm", "Jonah", "Dan", "Rev"}
MARKER_RICH_KEYS = {"q", "q1", "q2", "q3", "qr", "qc", "qs", "d", "b"}
REQUIRED_PROTOCOL_SIDEcars = (
    "book_strategy/<Book>.md",
    "low_confidence_register.jsonl",
    "frontier_escalation_queue.jsonl",
    "atlas_candidate_feed.jsonl",
    "model_quality_summary.md",
)

SPAN_RE = re.compile(
    r"^([1-4]?[A-Za-z][A-Za-z0-9]*)\.(\d+)\.(\d+)"
    r"(?:-([1-4]?[A-Za-z][A-Za-z0-9]*)\.(\d+)\.(\d+))?$"
)


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"{_rel(path)}: expected mapping")
    return data


def _iter_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{_rel(path)}:{line_no}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{_rel(path)}:{line_no}: expected JSON object")
            rows.append(row)
    return rows


def _parse_span(span: str) -> tuple[str, int, int, int, int] | None:
    match = SPAN_RE.match(span.strip())
    if not match:
        return None
    b1, c1, v1, b2, c2, v2 = match.groups()
    if b2 and b1 != b2:
        return None
    return b1, int(c1), int(v1), int(c2 or c1), int(v2 or v1)


def _span_key(book: str, chapter: int) -> str:
    return f"{book}.{chapter}"


def _load_chapter_features(book_filter: set[str] | None = None) -> dict[str, dict[str, Any]]:
    features: dict[str, dict[str, Any]] = {}
    if not SPAN_FEATURES.is_file():
        return features
    with SPAN_FEATURES.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            book = str(row.get("book_id", ""))
            if book_filter and book not in book_filter:
                continue
            parsed = _parse_span(f"{row.get('osis_start')}-{row.get('osis_end')}")
            if not parsed:
                continue
            _, start_chapter, _start_verse, end_chapter, _end_verse = parsed
            if start_chapter == end_chapter:
                features[_span_key(book, start_chapter)] = row
    return features


def _is_marker_rich(feature: dict[str, Any] | None) -> bool:
    if not feature:
        return False
    markers = feature.get("marker_counts", {})
    if isinstance(markers, dict) and any(int(markers.get(key, 0) or 0) > 0 for key in MARKER_RICH_KEYS):
        return True
    risk_flags = set(feature.get("risk_flags", []) or [])
    return "has_poetry_or_liturgy_marker" in risk_flags


def _is_chapter_rollup(record: dict[str, Any], feature: dict[str, Any] | None) -> bool:
    evidence = [str(item) for item in record.get("boundary_evidence_refs", []) if isinstance(item, str)]
    if any("span_kind:chapter_observed_feature_rollup" in item for item in evidence):
        return True
    if not feature:
        return False
    span = str(record.get("span", ""))
    return span == f"{feature.get('osis_start')}-{feature.get('osis_end')}"


def _row_key(row: dict[str, Any]) -> str:
    return str(row.get("chunk_decision_id") or row.get("decision_id") or "")


def _validate_sidecar_rows(
    *,
    model_folder: Path,
    filename: str,
    required_fields: list[str],
    required_ids: set[str],
    errors: list[str],
) -> list[dict[str, Any]]:
    path = model_folder / filename
    if required_ids and not path.is_file():
        errors.append(f"{_rel(path)} required for low-confidence/escalation rows")
        return []
    try:
        rows = _iter_jsonl(path)
    except ValueError as exc:
        errors.append(str(exc))
        return []
    seen = {_row_key(row) for row in rows}
    missing_ids = sorted(required_ids - seen)
    if missing_ids:
        errors.append(f"{_rel(path)} missing row(s) for chunk_decision_id: {', '.join(missing_ids)}")
    for index, row in enumerate(rows, start=1):
        prefix = f"{_rel(path)}:{index}"
        for field in required_fields:
            if field not in row:
                errors.append(f"{prefix}: missing required field {field}")
        if row.get("non_authorizing") is not True:
            errors.append(f"{prefix}: non_authorizing must be true")
    return rows


def validate_policy() -> list[str]:
    errors: list[str] = []
    for path in (POLICY, PROTOCOL, PROMPT, TEMPLATE_MANIFEST):
        if not path.is_file():
            errors.append(f"missing {_rel(path)}")
    if errors:
        return errors

    policy = _read_yaml(POLICY)
    protocol = _read_yaml(PROTOCOL)
    template = _read_yaml(TEMPLATE_MANIFEST)

    quality = policy.get("literary_marker_quality_protocol", {})
    if quality.get("strategy_id") != "literary_marker_aware_v2":
        errors.append("multi_model policy must require literary_marker_aware_v2")
    if quality.get("control") != ".ai/control/t423_literary_marker_quality_protocol.yaml":
        errors.append("multi_model policy must point to t423_literary_marker_quality_protocol.yaml")
    if quality.get("required_for_all_model_slots") is not True:
        errors.append("literary quality protocol must be required for all model slots")
    for sidecar in REQUIRED_PROTOCOL_SIDEcars:
        if sidecar not in quality.get("required_sidecars", []):
            errors.append(f"multi_model policy missing required sidecar {sidecar}")

    if protocol.get("strategy_id") != "literary_marker_aware_v2":
        errors.append("quality protocol strategy_id must be literary_marker_aware_v2")
    if protocol.get("sidecar_row_contracts", {}).get("atlas_candidate_feed", {}).get("required_fields") is None:
        errors.append("quality protocol must define atlas_candidate_feed required fields")
    if protocol.get("frontier_books", {}).get("books") != ["Dan", "Rev"]:
        errors.append("quality protocol frontier books must be Dan and Rev")
    independence = protocol.get("model_independence", {})
    if independence.get("rule") != "same_contract_different_judgments":
        errors.append("quality protocol must require same_contract_different_judgments")
    if independence.get("examples_are_schema_only") is not True:
        errors.append("quality protocol must say examples_are_schema_only")

    manifest_quality = template.get("quality_protocol", {})
    if manifest_quality.get("strategy_id") != "literary_marker_aware_v2":
        errors.append("template model_manifest.yaml must include quality_protocol.strategy_id literary_marker_aware_v2")
    for key in (
        "low_confidence_register_required",
        "frontier_escalation_queue_required",
        "atlas_candidate_feed_required",
        "book_strategy_required",
    ):
        if manifest_quality.get(key) is not True:
            errors.append(f"template model_manifest.yaml quality_protocol.{key} must be true")

    prompt_text = PROMPT.read_text(encoding="utf-8")
    for required in (
        "literary_marker_aware_v2",
        "atlas_candidate_feed.jsonl",
        "frontier_escalation_queue.jsonl",
        "low_confidence_register.jsonl",
        "chapter-only",
        "Ps 119",
        "not an answer key",
        "schema example only",
        "independent boundary rationale",
    ):
        if required not in prompt_text:
            errors.append(f"marathon prompt missing {required}")

    return errors


def validate_model_folder(model_folder: Path, *, books: set[str] | None = None, require_artifacts: bool = False) -> list[str]:
    errors = validate_policy()
    if not model_folder.is_dir():
        return [f"missing {_rel(model_folder)}"]

    manifest_path = model_folder / "model_manifest.yaml"
    if not manifest_path.is_file():
        return [f"missing {_rel(manifest_path)}"]
    manifest = _read_yaml(manifest_path)
    model_id = str(manifest.get("model_id", model_folder.name))

    book_chunks_root = model_folder / "book_chunks"
    if not book_chunks_root.is_dir():
        return errors

    quality = manifest.get("quality_protocol", {})
    if quality.get("strategy_id") != "literary_marker_aware_v2":
        errors.append(f"{_rel(manifest_path)}: quality_protocol.strategy_id must be literary_marker_aware_v2")

    candidate_books = {
        path.parent.name
        for path in book_chunks_root.glob("*/chunks.jsonl")
        if path.is_file()
    }
    if books is not None:
        candidate_books &= books
    if not candidate_books:
        return errors

    features = _load_chapter_features(candidate_books)
    protocol = _read_yaml(PROTOCOL)
    sidecars = protocol.get("sidecar_row_contracts", {})
    low_required = sidecars.get("low_confidence_register", {}).get("required_fields", [])
    frontier_required = sidecars.get("frontier_escalation_queue", {}).get("required_fields", [])
    atlas_required = sidecars.get("atlas_candidate_feed", {}).get("required_fields", [])

    low_ids: set[str] = set()
    frontier_ids: set[str] = set()
    atlas_ids: set[str] = set()
    frontier_books_seen: dict[str, int] = defaultdict(int)

    for book in sorted(candidate_books):
        strategy_path = model_folder / "book_strategy" / f"{book}.md"
        if require_artifacts and not strategy_path.is_file():
            errors.append(f"missing {_rel(strategy_path)}")
        if strategy_path.is_file():
            strategy_text = strategy_path.read_text(encoding="utf-8").lower()
            for needle in ("strong", "evidence", "strategy"):
                if needle not in strategy_text:
                    errors.append(f"{_rel(strategy_path)} must mention {needle}")

        rows = _iter_jsonl(book_chunks_root / book / "chunks.jsonl")
        if not rows:
            errors.append(f"{_rel(book_chunks_root / book / 'chunks.jsonl')}: no chunk rows")
            continue

        for row in rows:
            decision_id = str(row.get("decision_id", ""))
            prefix = f"{book} {decision_id or row.get('span')}"
            if row.get("model_id") != model_id:
                errors.append(f"{prefix}: model_id must match manifest model_id {model_id}")
            if row.get("non_authorizing") is not True:
                errors.append(f"{prefix}: non_authorizing must be true")
            if row.get("confidence") not in {"high", "medium", "medium_low", "low"}:
                errors.append(f"{prefix}: confidence must be high, medium, medium_low, or low")
            if book in FRONTIER_BOOKS:
                if row.get("frontier_flag_considered") is not True:
                    errors.append(f"{prefix}: frontier_flag_considered must be true for {book}")
                frontier_books_seen[book] += 1

            parsed = _parse_span(str(row.get("span", "")))
            feature = None
            chapter_only = False
            marker_rich = False
            if parsed:
                _, start_chapter, _start_verse, end_chapter, _end_verse = parsed
                if start_chapter == end_chapter:
                    feature = features.get(_span_key(book, start_chapter))
                    chapter_only = _is_chapter_rollup(row, feature)
                    marker_rich = _is_marker_rich(feature)

            fragile_chapter_fallback = chapter_only and (marker_rich or book in PILOT_FRAGILE_BOOKS)
            low_confidence = row.get("confidence") in LOW_CONFIDENCE
            if fragile_chapter_fallback and not low_confidence:
                errors.append(
                    f"{prefix}: chapter-only fallback on marker-rich/pilot-fragile span must use low or medium_low confidence"
                )
            if low_confidence or fragile_chapter_fallback:
                low_ids.add(decision_id)
                frontier_ids.add(decision_id)
                atlas_ids.add(decision_id)

    _validate_sidecar_rows(
        model_folder=model_folder,
        filename="low_confidence_register.jsonl",
        required_fields=list(low_required),
        required_ids=low_ids,
        errors=errors,
    )
    frontier_rows = _validate_sidecar_rows(
        model_folder=model_folder,
        filename="frontier_escalation_queue.jsonl",
        required_fields=list(frontier_required),
        required_ids=frontier_ids,
        errors=errors,
    )
    _validate_sidecar_rows(
        model_folder=model_folder,
        filename="atlas_candidate_feed.jsonl",
        required_fields=list(atlas_required),
        required_ids=atlas_ids,
        errors=errors,
    )

    frontier_books_with_rows = {str(row.get("book")) for row in frontier_rows if row.get("non_authorizing") is True}
    for book in frontier_books_seen:
        if book not in frontier_books_with_rows:
            errors.append(f"{book}: at least one frontier_escalation_queue row required for frontier book")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy-only", action="store_true")
    parser.add_argument("--model-folder", type=Path)
    parser.add_argument("--book", action="append", dest="books")
    parser.add_argument("--require-artifacts", action="store_true")
    args = parser.parse_args()

    try:
        if args.model_folder:
            books = set(args.books) if args.books else None
            errors = validate_model_folder(args.model_folder, books=books, require_artifacts=args.require_artifacts)
        else:
            errors = validate_policy()
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("T423 literary quality protocol: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
