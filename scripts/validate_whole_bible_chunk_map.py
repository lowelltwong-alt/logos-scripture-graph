#!/usr/bin/env python3
"""Validate T423 whole_bible_chunk_map.jsonl records and book coverage."""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.t423_chunk_map_utils import (
    REQUIRED_CHUNK_FIELDS,
    canonical_books,
    iter_jsonl,
    normalize_book_id,
    normalize_span,
    parse_span,
)


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def validate_chunk_map(
    path: Path,
    *,
    expected_model_id: str | None = None,
    require_full_bible: bool = False,
    allowed_books: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"missing {_rel(path)}"]

    by_book: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_decision_ids: set[str] = set()

    for line_no, record in iter_jsonl(path):
        prefix = f"{_rel(path)}:{line_no}"
        for field in REQUIRED_CHUNK_FIELDS:
            if field not in record:
                errors.append(f"{prefix}: missing required field {field}")
        if record.get("non_authorizing") is not True:
            errors.append(f"{prefix}: non_authorizing must be true")

        model_id = record.get("model_id")
        if expected_model_id and model_id != expected_model_id:
            errors.append(f"{prefix}: model_id {model_id!r} != expected {expected_model_id!r}")

        book = normalize_book_id(str(record.get("book", "")))
        if allowed_books is not None and book not in allowed_books:
            errors.append(f"{prefix}: book {book!r} not in allowed scope")
        if book not in canonical_books():
            errors.append(f"{prefix}: unknown book {book!r}")

        span = record.get("span")
        if isinstance(span, str):
            try:
                parsed = parse_span(span)
                if parsed.book != book:
                    errors.append(f"{prefix}: span book {parsed.book!r} != record book {book!r}")
                record["_normalized_span"] = normalize_span(span)
            except ValueError as exc:
                errors.append(f"{prefix}: {exc}")
        else:
            errors.append(f"{prefix}: span must be string")

        decision_id = record.get("decision_id")
        if isinstance(decision_id, str):
            if decision_id in seen_decision_ids:
                errors.append(f"{prefix}: duplicate decision_id {decision_id}")
            seen_decision_ids.add(decision_id)

        chunk_index = record.get("chunk_index_in_book")
        if not isinstance(chunk_index, int) or chunk_index < 1:
            errors.append(f"{prefix}: chunk_index_in_book must be positive int")

        evidence = record.get("boundary_evidence_refs")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{prefix}: boundary_evidence_refs must be non-empty list")

        by_book[book].append(record)

    for book, chunks in by_book.items():
        chunks.sort(key=lambda r: int(r["chunk_index_in_book"]))
        indices = [int(c["chunk_index_in_book"]) for c in chunks]
        if indices != list(range(1, len(indices) + 1)):
            errors.append(f"{_rel(path)} book {book}: chunk_index_in_book must be contiguous from 1")
        for i in range(len(chunks) - 1):
            try:
                cur = parse_span(str(chunks[i]["span"]))
                nxt = parse_span(str(chunks[i + 1]["span"]))
                if cur.end.key() >= nxt.start.key():
                    errors.append(
                        f"{_rel(path)} book {book}: chunk {i + 1} overlaps or inverts order with chunk {i + 2}"
                    )
            except ValueError:
                pass

    if require_full_bible:
        missing = set(canonical_books()) - set(by_book)
        if missing:
            errors.append(f"{_rel(path)}: missing books: {', '.join(sorted(missing))}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="whole_bible_chunk_map.jsonl or model folder")
    parser.add_argument("--model-id", help="Expected model_id in every record")
    parser.add_argument("--require-full-bible", action="store_true")
    parser.add_argument("--book", action="append", dest="books", help="Limit validation to book(s)")
    parser.add_argument(
        "--python-only",
        action="store_true",
        help="Run the original Python implementation directly. Used by Rust wrapper fallback/parity.",
    )
    parser.add_argument("--summary-json", type=Path, help="Forwarded to the Rust fast validator.")
    parser.add_argument("--cargo-bin", default="cargo", help="Cargo binary for the Rust fast validator.")
    parser.add_argument("--require-rust", action="store_true", help="Fail if the Rust fast validator is unavailable.")
    parser.add_argument(
        "--compare-python",
        action="store_true",
        help="Run Rust and Python validators and fail if their pass/fail verdicts diverge.",
    )
    args = parser.parse_args()

    if not args.python_only:
        from scripts import validate_fast_chunk_map

        forwarded = [str(args.path)]
        if args.model_id:
            forwarded.extend(["--model-id", args.model_id])
        if args.require_full_bible:
            forwarded.append("--require-full-bible")
        for book in args.books or []:
            forwarded.extend(["--book", book])
        if args.summary_json:
            forwarded.extend(["--summary-json", str(args.summary_json)])
        if args.cargo_bin:
            forwarded.extend(["--cargo-bin", args.cargo_bin])
        if args.require_rust:
            forwarded.append("--require-rust")
        else:
            forwarded.append("--python-fallback")
        if args.compare_python:
            forwarded.append("--compare-python")
        return validate_fast_chunk_map.main(forwarded)

    path = args.path
    if path.is_dir():
        path = path / "whole_bible_chunk_map.jsonl"
        if not args.model_id:
            manifest = path.parent / "model_manifest.yaml"
            if manifest.is_file():
                import yaml

                data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
                if isinstance(data, dict) and data.get("model_id"):
                    args.model_id = str(data["model_id"])

    allowed = set(args.books) if args.books else None
    errors = validate_chunk_map(
        path,
        expected_model_id=args.model_id,
        require_full_bible=args.require_full_bible,
        allowed_books=allowed,
    )
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print(f"OK: {_rel(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
