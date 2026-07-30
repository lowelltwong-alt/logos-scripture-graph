#!/usr/bin/env python3
"""Aggregate per-book candidate chunks into a single non-authorizing feed."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"
BOOKS = ["Gen","Exod","Lev","Num","Deut","Josh","Judg","Ruth","1Sam","2Sam","1Kgs","2Kgs","1Chr","2Chr","Ezra","Neh","Esth","Job","Ps","Prov","Eccl","Song","Isa","Jer","Lam","Ezek","Dan","Hos","Joel","Amos","Obad","Jonah","Mic","Nah","Hab","Zeph","Hag","Zech","Mal","Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"]

def main() -> int:
    out = MODEL / "state/evidence/final/whole_bible_candidate_map.jsonl"; out.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for book in BOOKS:
        path = MODEL / "book_chunks" / book / "chunks.jsonl"
        if not path.is_file(): raise SystemExit(f"missing candidate book: {book}")
        rows.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    out.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":"))+"\n" for row in rows),encoding="utf-8",newline="\n")
    print(json.dumps({"books":len(BOOKS),"chunks":len(rows),"candidate_only":True,"non_authorizing":True,"promotion_qualified":False},sort_keys=True)); print(out); return 0
if __name__ == "__main__": raise SystemExit(main())
