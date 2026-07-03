#!/usr/bin/env python3
"""Report T423 marathon readiness — per-model book progress; batch compare when all done."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.t423_chunk_map_utils import (
    SCRATCH_ROOT,
    canonical_books,
    completed_books,
    discover_model_folders,
    list_book_chunk_dirs,
    load_fork_policy,
    load_marathon_progress,
    load_model_manifest,
    model_is_complete,
)
from scripts.t423_resume_book import next_book


def status_report(scratch_root: Path) -> dict:
    policy = load_fork_policy()
    pilot_books = list(policy.get("pilot_gate", {}).get("required_books", []))
    folders = discover_model_folders(scratch_root)
    models = []
    for folder in folders:
        manifest = load_model_manifest(folder)
        progress = load_marathon_progress(folder)
        model_id = str(manifest.get("model_id", folder.name))
        done = completed_books(folder)
        saved = set(list_book_chunk_dirs(folder))
        pilot_done = [b for b in pilot_books if b in done]
        models.append(
            {
                "model_id": model_id,
                "folder": folder.name,
                "marathon_status": progress.get("marathon_status", "unknown"),
                "books_completed": progress.get("books_completed", len(done)),
                "books_total": progress.get("books_total", 66),
                "book_chunks_saved": len(saved),
                "complete": model_is_complete(folder),
                "next_book": next_book(folder),
                "pilot_books_complete": pilot_done,
                "pilot_books_required": pilot_books,
                "research_baseline_read": manifest.get("research_baseline_read", False),
            }
        )
    complete_count = sum(1 for m in models if m["complete"])
    all_pilot = all(
        set(m["pilot_books_complete"]) >= set(pilot_books) for m in models if m["folder"].startswith("M")
    ) if pilot_books and models else False
    return {
        "models": models,
        "complete_model_count": complete_count,
        "all_66_books": canonical_books(),
        "pilot_books": pilot_books,
        "all_models_pilot_complete": all_pilot,
        "ready_for_batch_compare": complete_count >= 3,
        "ready_for_default_compare": complete_count >= 5,
        "compare_mode": "batch_offline_after_all_models_complete",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch-root", type=Path, default=SCRATCH_ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = status_report(args.scratch_root)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(yaml.safe_dump(report, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
