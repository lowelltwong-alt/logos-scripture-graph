#!/usr/bin/env python3
"""Supervisor status for one-model T423 marathon (book-at-a-time, no cross-model compare)."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.t423_chunk_map_utils import (
    SCRATCH_ROOT,
    completed_books,
    discover_model_folders,
    load_marathon_progress,
    load_model_manifest,
    model_is_complete,
)
from scripts.t423_resume_book import next_book

ROOT = Path(__file__).resolve().parent.parent


def supervisor_status(model_folder: Path) -> dict:
    manifest = load_model_manifest(model_folder)
    progress = load_marathon_progress(model_folder)
    model_id = str(manifest.get("model_id", model_folder.name))
    done = sorted(completed_books(model_folder))
    nxt = next_book(model_folder)
    complete = model_is_complete(model_folder)
    return {
        "model_id": model_id,
        "folder": model_folder.name,
        "marathon_status": progress.get("marathon_status", "pending_marathon_start"),
        "books_completed": len(done),
        "books_total": progress.get("books_total", 66),
        "completed_books": done,
        "next_book": nxt,
        "marathon_complete": complete,
        "compare_allowed": False,
        "compare_note": "Batch verse-coverage compare runs only after all models save 66 books locally",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model_folder", type=Path, nargs="?", help="Single model folder")
    parser.add_argument("--scratch-root", type=Path, default=SCRATCH_ROOT)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--merge-if-complete", action="store_true", help="Run merge script when 66 books done")
    args = parser.parse_args()

    if args.model_folder:
        folders = [args.model_folder]
    else:
        folders = discover_model_folders(args.scratch_root)

    if not folders:
        print("ERROR: no model folders", file=sys.stderr)
        return 2

    reports = [supervisor_status(f) for f in folders]

    if args.merge_if_complete:
        for folder, report in zip(folders, reports, strict=True):
            if report["marathon_complete"]:
                subprocess.run(
                    [sys.executable, str(ROOT / "scripts" / "t423_merge_book_chunks.py"), str(folder)],
                    check=False,
                )

    if args.json:
        all_complete = all(r["marathon_complete"] for r in reports)
        print(json.dumps({"models": reports, "all_models_complete": all_complete}, indent=2))
    else:
        for r in reports:
            print(f"{r['model_id']}: {r['books_completed']}/{r['books_total']} next={r['next_book']}")

    if any(not r["marathon_complete"] and r["next_book"] for r in reports):
        return 0
    if all(r["marathon_complete"] for r in reports):
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
