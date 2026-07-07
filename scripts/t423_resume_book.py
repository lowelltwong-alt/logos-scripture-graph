#!/usr/bin/env python3
"""Resume T423 marathon — next book to chunk; discard incomplete book segments."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.t423_chunk_map_utils import (
    BOOK_CHUNKS_DIR,
    book_chunk_file,
    canonical_books,
    completed_books,
    load_marathon_progress,
    load_model_manifest,
)
from scripts.validate_t423_literary_quality_protocol import validate_model_folder
from scripts.validate_whole_bible_chunk_map import validate_chunk_map

ROOT = Path(__file__).resolve().parent.parent


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _write_progress(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def next_book(model_folder: Path) -> str | None:
    progress = load_marathon_progress(model_folder)
    done = completed_books(model_folder)
    for book in canonical_books():
        if book not in done:
            return book
    return None


def discard_incomplete_book(model_folder: Path, book: str) -> bool:
    book_dir = model_folder / BOOK_CHUNKS_DIR / book
    if book_dir.is_dir():
        shutil.rmtree(book_dir)
        return True
    return False


def mark_book_complete(model_folder: Path, book: str, *, skip_validate: bool = False) -> list[str]:
    if not skip_validate:
        chunk_path = book_chunk_file(model_folder, book)
        if not chunk_path.is_file():
            return [f"missing book chunks: {_rel(chunk_path)}"]
        manifest = load_model_manifest(model_folder)
        model_id = str(manifest.get("model_id", model_folder.name))
        errors = validate_chunk_map(
            chunk_path,
            expected_model_id=model_id,
            allowed_books={book},
        )
        if errors:
            return errors
        quality_errors = validate_model_folder(
            model_folder,
            books={book},
            require_artifacts=True,
        )
        if quality_errors:
            return quality_errors

    path = model_folder / "marathon_progress.yaml"
    progress = load_marathon_progress(model_folder)
    completion = progress.get("book_completion", {})
    if not isinstance(completion, dict):
        completion = {}
    completion[book] = {"status": "complete"}
    progress["book_completion"] = completion
    done = completed_books(model_folder) | {book}
    progress["books_completed"] = len(done)
    progress["books_total"] = progress.get("books_total", 66)
    if len(done) >= int(progress["books_total"]):
        progress["marathon_status"] = "complete"
    else:
        progress["marathon_status"] = "in_progress"
    _write_progress(path, progress)
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model_folder", type=Path)
    parser.add_argument("--discard-incomplete", metavar="BOOK", help="Remove partial book_chunks/<Book>/ before re-chunk")
    parser.add_argument("--mark-complete", metavar="BOOK", help="Mark book complete in marathon_progress.yaml")
    parser.add_argument("--skip-validate", action="store_true", help="Tests only — skip chunk validation")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    folder = args.model_folder
    if not folder.is_dir():
        print(f"ERROR: missing {_rel(folder)}", file=sys.stderr)
        return 2

    manifest = load_model_manifest(folder)
    model_id = str(manifest.get("model_id", folder.name))

    if args.discard_incomplete:
        removed = discard_incomplete_book(folder, args.discard_incomplete)
        if args.json:
            print(json.dumps({"discarded": args.discard_incomplete, "removed": removed}))
        else:
            print(f"discard: {args.discard_incomplete} removed={removed}")
        return 0

    if args.mark_complete:
        errors = mark_book_complete(
            folder,
            args.mark_complete,
            skip_validate=args.skip_validate,
        )
        if errors:
            for err in errors:
                print(f"ERROR: {err}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps({"marked_complete": args.mark_complete, "validated": not args.skip_validate}))
        else:
            print(f"marked complete: {args.mark_complete}")
        return 0

    nxt = next_book(folder)
    progress = load_marathon_progress(folder)
    payload = {
        "model_id": model_id,
        "next_book": nxt,
        "marathon_status": progress.get("marathon_status", "pending_marathon_start"),
        "books_completed": progress.get("books_completed", len(completed_books(folder))),
        "books_total": progress.get("books_total", 66),
        "book_chunk_path": str(book_chunk_file(folder, nxt)) if nxt else None,
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    elif nxt:
        print(nxt)
        print(f"# write chunks to {_rel(book_chunk_file(folder, nxt))}")
    else:
        print("COMPLETE")
    return 0 if nxt or progress.get("marathon_status") == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
