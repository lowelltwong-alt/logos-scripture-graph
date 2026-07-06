#!/usr/bin/env python3
"""Generate one book's scratch chunk map from observation substrate (linear marathon step 1)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.t423_chunk_map_utils import load_yaml

MODEL_ID = "M1_cursor"
SUBSTRATE = ROOT / "build" / "observation_substrate/current/span_observation_features.jsonl"
GENRES_PATH = ROOT / "config" / "chunking" / "book_genres.yaml"


def book_genre(book: str) -> str:
    data = load_yaml(GENRES_PATH)
    genres = data.get("genres", {})
    return str(genres.get(book, "narrative"))


def decision_prefix(book: str) -> str:
    return f"M1-{book.upper()}"


def generate_book(model_folder: Path, book: str) -> int:
    lit = book_genre(book)
    chapters: list[tuple[int, dict]] = []
    with SUBSTRATE.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            if record.get("book_id") != book:
                continue
            if record.get("span_kind") != "chapter_observed_feature_rollup":
                continue
            match = re.match(rf"{re.escape(book)}\.(\d+)\.", record["osis_start"])
            if not match:
                continue
            chapters.append((int(match.group(1)), record))
    chapters.sort(key=lambda item: item[0])
    if not chapters:
        print(f"ERROR: no chapter rollups for {book}", file=sys.stderr)
        return 1

    out = model_folder / "book_chunks" / book / "chunks.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    prefix = decision_prefix(book)
    rows: list[dict] = []
    for idx, (_, record) in enumerate(chapters, start=1):
        start = record["osis_start"]
        end = record["osis_end"]
        span = start if start == end else f"{start}-{end}"
        marker_counts = record.get("marker_counts") or {}
        risk_flags = record.get("risk_flags") or []
        evidence = [
            f"observation_substrate:{start}",
            "span_kind:chapter_observed_feature_rollup",
            f"book_genre:{lit}",
        ]
        if "has_footnote" in risk_flags or marker_counts.get("f", 0) > 0:
            evidence.append("marker:footnote_present_evidence_only")
        if marker_counts.get("q1") or marker_counts.get("q2"):
            evidence.append("marker:poetry_or_liturgy_present_evidence_only")
        rows.append(
            {
                "model_id": MODEL_ID,
                "book": book,
                "span": span,
                "chunk_index_in_book": idx,
                "literature_type_guess": lit,
                "boundary_evidence_refs": evidence,
                "strong_or_hebrew_tags_used": bool(marker_counts.get("wh") or marker_counts.get("wg")),
                "wj_or_red_letter_considered": False,
                "frontier_flag_considered": False,
                "confidence": "medium",
                "decision_id": f"{prefix}-{idx:03d}",
                "non_authorizing": True,
            }
        )

    with out.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")

    first = rows[0]["span"]
    last = rows[-1]["span"]
    log_path = model_folder / "layer_decision_log.jsonl"
    entry = {
        "decision_id": f"{prefix}-STRATEGY",
        "book": book,
        "span": f"{first} to {last}",
        "action": "chunk_strategy",
        "notes": (
            f"{len(rows)} chapter-level chunks from observation_substrate chapter rollups; "
            f"literature_type_guess={lit}; processed linearly (generate only)."
        ),
        "boundary_evidence_refs": [
            "observation_substrate",
            "span_kind:chapter_observed_feature_rollup",
            f"book_genre:{lit}",
        ],
        "non_authorizing": True,
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")

    print(f"OK: {book} wrote {len(rows)} chunks -> {out.relative_to(ROOT)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("book", help="Canonical book id e.g. Josh")
    parser.add_argument(
        "--model-folder",
        type=Path,
        default=ROOT / ".ai/scratch/multi_model_bible_chunking/M1_cursor",
    )
    args = parser.parse_args()
    return generate_book(args.model_folder, args.book)


if __name__ == "__main__":
    raise SystemExit(main())
