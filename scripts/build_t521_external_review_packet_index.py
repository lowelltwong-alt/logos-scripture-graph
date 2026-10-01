#!/usr/bin/env python3
"""Build a privacy-safe, blind external-review packet index for T521."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"
MAP = MODEL / "state/evidence/final/whole_bible_candidate_map.jsonl"
PROMPT = ROOT / "docs/governance/T521_EXTERNAL_CONVERGENCE_HANDOFF_PROMPT.md"
QUEUE = MODEL / "state/evidence/final/scaffold_hold_queue.jsonl"
OUT = MODEL / "state/evidence/final/external_review_packet_index.json"
BOOKS = ["Gen","Exod","Lev","Num","Deut","Josh","Judg","Ruth","1Sam","2Sam","1Kgs","2Kgs","1Chr","2Chr","Ezra","Neh","Esth","Job","Ps","Prov","Eccl","Song","Isa","Jer","Lam","Ezek","Dan","Hos","Joel","Amos","Obad","Jonah","Mic","Nah","Hab","Zeph","Hag","Zech","Mal","Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"]


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    rows = [json.loads(x) for x in MAP.read_text(encoding="utf-8").splitlines() if x.strip()]
    counts = {book: sum(row["book"] == book for row in rows) for book in BOOKS}
    index = {
        "schema_version": "t521_external_review_packet_index.v1",
        "model_id": "M7_sol",
        "candidate_only": True,
        "non_authorizing": True,
        "promotion_authorized": False,
        "independence_status": "awaiting_external_provider_or_human_receipt",
        "sibling_maps_read_before_review": False,
        "map": {"path": str(MAP), "sha256": digest(MAP), "books": len(BOOKS), "chunks": len(rows)},
        "prompt": {"path": str(PROMPT), "sha256": digest(PROMPT)},
        "scaffold_hold_queue": {"path": str(QUEUE), "sha256": digest(QUEUE), "rows": sum(1 for _ in QUEUE.read_text(encoding="utf-8").splitlines() if _.strip())} if QUEUE.exists() else None,
        "allowed_inputs": [
            str(MAP),
            str(PROMPT),
            str(QUEUE),
            "docs/governance/WHOLE_BIBLE_B01_TYPED_CONTRACT.md",
            "docs/governance/WHOLE_BIBLE_B01_REPLAY_RUNBOOK.md",
        ],
        "withhold_until_review_frozen": [
            "all sibling maps and their prompts",
            "Sol role reports and boss rulings",
            "other provider conclusions",
            "raw Scripture/source payloads outside the pinned local source route",
        ],
        "required_external_outputs": [
            "book-by-book literary seam findings",
            "Hebrew/Aramaic or Koine Greek translation-risk observations",
            "internal cross-reference and quotation/allusion leads",
            "red-team falsification tests and preserved dissent/appeals",
            "provider/model identity and independence declaration",
            "hash-bound receipt naming the exact map and prompt digests",
        ],
        "source_limitations": {
            "ot": "OSHB/UXLC routes are pinned for evidence; ancient-context corpus is gap-only unless separately qualified.",
            "nt": "Greek routes are corpus-level CNTR/SBLGNT/UGNT evidence; per-book Greek XML closure is not claimed.",
            "ancient_context": "No substantive rabbinic/Second Temple claim is authorized without a qualification receipt.",
        },
        "book_chunk_counts": counts,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"path": str(OUT), "map_sha256": index["map"]["sha256"], "books": len(BOOKS), "chunks": len(rows), "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
