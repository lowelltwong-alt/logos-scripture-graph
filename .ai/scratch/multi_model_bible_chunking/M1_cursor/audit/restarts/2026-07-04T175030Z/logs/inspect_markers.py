#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
VO = ROOT / "build/observation_substrate/current/verse_observations.jsonl"


def list_markers(book: str) -> None:
    with VO.open(encoding="utf-8") as handle:
        for line in handle:
            r = json.loads(line)
            if r.get("book_id") != book:
                continue
            mc = r.get("marker_counts") or {}
            keys = [k for k, v in mc.items() if k != "v" and k != "w" and int(v or 0) > 0]
            if keys:
                print(r["osis_ref"], keys)


for book in ["Phlm", "Jonah", "Ps", "Rev"]:
    print(f"\n--- {book} marker verses ---")
    list_markers(book)
