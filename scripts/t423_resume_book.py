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


def _write_manifest(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def _completed_from_ledger(completion: dict) -> set[str]:
    """Read literal completion facts without the cross-file fail-closed guard."""
    return {
        str(book)
        for book, info in completion.items()
        if isinstance(info, dict) and info.get("status") == "complete"
    }


def _hydrate_completion_info(model_folder: Path, book: str, info: dict) -> dict:
    """Restore receipt-backed progress metadata without replacing existing facts."""
    receipt_path = model_folder / "receipts" / f"{book}_completion_v2.json"
    if not receipt_path.is_file():
        return info
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return info
    fields = {
        "completion_state": "completion_state",
        "chunks": "chunk_count",
        "canonical_verses": "canonical_verse_count",
        "exact_ordered_coverage": "exact_ordered_coverage",
        "review_packets": "review_packet_count",
        "passed_decisions": "accepted_decision_count",
        "held_decisions": "held_decision_count",
        "unresolved_appeals": "unresolved_appeal_count",
    }
    for progress_key, receipt_key in fields.items():
        if receipt_key in receipt:
            info.setdefault(progress_key, receipt[receipt_key])
    info.setdefault("receipt", _rel(receipt_path))
    return info


def _sync_manifest_with_progress(model_folder: Path, progress: dict, done: set[str]) -> None:
    manifest_path = model_folder / "model_manifest.yaml"
    manifest = load_model_manifest(model_folder)
    books_total = int(progress.get("books_total", 66))
    complete = len(done) >= books_total
    manifest["status"] = "marathon_complete" if complete else "marathon_in_progress"
    manifest["books_completed"] = len(done)
    manifest["books_total"] = books_total
    manifest["current_book"] = next((book for book in canonical_books() if book not in done), None)
    _write_manifest(manifest_path, manifest)


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
    existing = completion.get(book, {})
    info = dict(existing) if isinstance(existing, dict) else {}
    info["status"] = "complete"
    completion[book] = _hydrate_completion_info(model_folder, book, info)
    progress["book_completion"] = completion
    done = _completed_from_ledger(completion)
    progress["books_completed"] = len(done)
    progress["books_total"] = progress.get("books_total", 66)
    if len(done) >= int(progress["books_total"]):
        progress["marathon_status"] = "complete"
    else:
        progress["marathon_status"] = "in_progress"
    progress["current_book"] = next((candidate for candidate in canonical_books() if candidate not in done), None)
    _write_progress(path, progress)
    _sync_manifest_with_progress(model_folder, progress, done)
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
