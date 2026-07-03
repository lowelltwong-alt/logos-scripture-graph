#!/usr/bin/env python3
"""Merge per-book chunk files into whole_bible_chunk_map.jsonl for one model."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.t423_chunk_map_utils import (
    BOOK_CHUNKS_DIR,
    book_chunk_file,
    canonical_books,
    iter_jsonl,
    list_book_chunk_dirs,
    load_model_manifest,
)


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def merge_book_chunks(model_folder: Path, *, dedupe_decision_ids: bool = True) -> tuple[list[dict], list[str]]:
    errors: list[str] = []
    manifest = load_model_manifest(model_folder)
    expected_id = str(manifest.get("model_id", model_folder.name))
    seen_ids: set[str] = set()
    merged: list[dict] = []
    canon = canonical_books()

    for book in canon:
        path = book_chunk_file(model_folder, book)
        if not path.is_file():
            continue
        for line_no, record in iter_jsonl(path):
            prefix = f"{_rel(path)}:{line_no}"
            if record.get("model_id") != expected_id:
                errors.append(f"{prefix}: model_id must be {expected_id!r}")
            if str(record.get("book", "")) != book:
                errors.append(f"{prefix}: book must be {book!r}")
            did = record.get("decision_id")
            if isinstance(did, str):
                if dedupe_decision_ids and did in seen_ids:
                    continue
                seen_ids.add(did)
            merged.append(record)

    merged.sort(key=lambda r: (canon.index(str(r["book"])), int(r["chunk_index_in_book"])))
    return merged, errors


def write_merged_map(model_folder: Path, rows: list[dict]) -> Path:
    out = model_folder / "whole_bible_chunk_map.jsonl"
    with out.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model_folder", type=Path, help="Model folder e.g. M1_cursor")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    folder = args.model_folder
    if not folder.is_dir():
        print(f"ERROR: missing {_rel(folder)}", file=sys.stderr)
        return 1
    if not (folder / BOOK_CHUNKS_DIR).is_dir():
        print(f"ERROR: missing {_rel(folder / BOOK_CHUNKS_DIR)}", file=sys.stderr)
        return 1

    rows, errors = merge_book_chunks(folder)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    if not rows:
        print(f"ERROR: no book chunks under {_rel(folder / BOOK_CHUNKS_DIR)}", file=sys.stderr)
        return 1

    saved = list_book_chunk_dirs(folder)
    if args.dry_run:
        print(f"would merge {len(rows)} chunks from {len(saved)} books -> whole_bible_chunk_map.jsonl")
        return 0

    out = write_merged_map(folder, rows)
    print(f"OK: merged {len(rows)} chunks from {len(saved)} books -> {_rel(out)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
