#!/usr/bin/env python3
"""Create an incomplete external-review receipt template; never claim review."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl"
PROMPT = ROOT / "docs/governance/T521_EXTERNAL_REVIEWER_COPY_PASTE_PROMPT.md"
OUT = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/external_review_receipt.template.json"
BOOKS = ["Gen","Exod","Lev","Num","Deut","Josh","Judg","Ruth","1Sam","2Sam","1Kgs","2Kgs","1Chr","2Chr","Ezra","Neh","Esth","Job","Ps","Prov","Eccl","Song","Isa","Jer","Lam","Ezek","Dan","Hos","Joel","Amos","Obad","Jonah","Mic","Nah","Hab","Zeph","Hag","Zech","Mal","Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"]


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    rows = [json.loads(x) for x in MAP.read_text(encoding="utf-8").splitlines() if x.strip()]
    receipt = {
        "schema_version": "t521_external_review_receipt.v1",
        "provider": {"provider_family": "FILL_EXTERNAL_PROVIDER", "model_or_system_id": "FILL_MODEL_OR_SYSTEM", "execution_id": "FILL_EXECUTION_ID"},
        "map_sha256": digest(MAP),
        "prompt_sha256": digest(PROMPT),
        "book_count": 66,
        "chunk_count": len(rows),
        "sibling_maps_read_before_review": False,
        "independent_model_or_provider_evidence": False,
        "candidate_only": True,
        "non_authorizing": True,
        "promotion_authorized": False,
        "book_reviews": [{"book": book, "review_status": "review_incomplete", "literary_findings": [], "language_risks": [], "cross_reference_leads": [], "red_team_tests": []} for book in BOOKS],
        "dissent_and_appeals_preserved": True,
        "receipt_status": "review_incomplete",
        "template_only": True,
    }
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"path": str(OUT), "books": 66, "chunks": len(rows), "candidate_only": True, "non_authorizing": True, "review_status": "review_incomplete"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
