#!/usr/bin/env python3
"""Initialize marathon_progress.yaml with all 66 books pending for set-and-forget runs."""
from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

from scripts.t423_chunk_map_utils import SCRATCH_ROOT, canonical_books, load_model_manifest

ROOT = Path(__file__).resolve().parent.parent


def init_progress(model_folder: Path) -> None:
    manifest = load_model_manifest(model_folder)
    model_id = str(manifest.get("model_id", model_folder.name))
    books = canonical_books()
    progress = {
        "model_id": model_id,
        "marathon_status": "in_progress",
        "books_completed": 0,
        "books_total": 66,
        "current_book": books[0],
        "last_updated": datetime.now(UTC).isoformat(),
        "book_completion": {book: {"status": "pending", "chunks": 0} for book in books},
        "notes": "Update each book to status complete after chunking; set marathon_status complete at end.",
    }
    out = model_folder / "marathon_progress.yaml"
    out.write_text(yaml.safe_dump(progress, sort_keys=False, allow_unicode=True), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model_folder", type=Path, help="e.g. .ai/scratch/multi_model_bible_chunking/M1_cursor")
    args = parser.parse_args()
    folder = args.model_folder
    if not folder.is_dir():
        folder = SCRATCH_ROOT / args.model_folder
    if not folder.is_dir():
        print(f"ERROR: folder not found: {folder}", file=sys.stderr)
        return 1
    init_progress(folder)
    print(f"OK: {folder / 'marathon_progress.yaml'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
