#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
VO = ROOT / "build/observation_substrate/current/verse_observations.jsonl"


def sample(book: str, chapters: list[int] | None = None, limit: int = 8) -> None:
    rows = []
    with VO.open(encoding="utf-8") as handle:
        for line in handle:
            r = json.loads(line)
            if r.get("book_id") != book:
                continue
            if chapters and r["chapter"] not in chapters:
                continue
            rows.append(r)
    print(f"=== {book} verses={len(rows)} ===")
    for r in rows[:limit]:
        mc = r.get("marker_counts", {})
        ff = r.get("feature_flags", [])
        print(f"{r['osis_ref']} mc={mc} flags={ff}")


for b, ch in [
    ("Ps", [1, 119, 150]),
    ("Phlm", [1]),
    ("Jonah", [1, 2, 3, 4]),
    ("Rev", [1, 4, 21]),
    ("Gen", [1, 49]),
]:
    sample(b, ch, 5)
    print()
