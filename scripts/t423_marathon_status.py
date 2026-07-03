#!/usr/bin/env python3
"""Report T423 marathon readiness — which models can be compared."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from scripts.t423_chunk_map_utils import (
    SCRATCH_ROOT,
    canonical_books,
    completed_books,
    discover_model_folders,
    load_marathon_progress,
    load_model_manifest,
    model_is_complete,
)

ROOT = Path(__file__).resolve().parent.parent


def status_report(scratch_root: Path) -> dict:
    folders = discover_model_folders(scratch_root)
    models = []
    for folder in folders:
        manifest = load_model_manifest(folder)
        progress = load_marathon_progress(folder)
        model_id = str(manifest.get("model_id", folder.name))
        done = completed_books(folder)
        models.append(
            {
                "model_id": model_id,
                "folder": folder.name,
                "marathon_status": progress.get("marathon_status", "unknown"),
                "books_completed": progress.get("books_completed", len(done)),
                "books_total": progress.get("books_total", 66),
                "complete": model_is_complete(folder),
                "research_baseline_read": manifest.get("research_baseline_read", False),
            }
        )
    complete_count = sum(1 for m in models if m["complete"])
    return {
        "models": models,
        "complete_model_count": complete_count,
        "all_66_books": canonical_books(),
        "ready_for_default_compare": complete_count >= 5,
        "ready_for_minimum_compare": complete_count >= 3,
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
