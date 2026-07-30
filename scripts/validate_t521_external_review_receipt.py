#!/usr/bin/env python3
"""Fail-closed validation for a T521 external convergence receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = {"Gen","Exod","Lev","Num","Deut","Josh","Judg","Ruth","1Sam","2Sam","1Kgs","2Kgs","1Chr","2Chr","Ezra","Neh","Esth","Job","Ps","Prov","Eccl","Song","Isa","Jer","Lam","Ezek","Dan","Hos","Joel","Amos","Obad","Jonah","Mic","Nah","Hab","Zeph","Hag","Zech","Mal","Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"}


class ReceiptError(ValueError):
    pass


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def validate(receipt: dict, *, map_path: Path, prompt_path: Path) -> None:
    if receipt.get("schema_version") != "t521_external_review_receipt.v1":
        raise ReceiptError("wrong schema_version")
    provider = receipt.get("provider") or {}
    for key in ("provider_family", "model_or_system_id", "execution_id"):
        if not isinstance(provider.get(key), str) or not provider[key].strip():
            raise ReceiptError(f"missing provider.{key}")
    if receipt.get("map_sha256") != digest(map_path):
        raise ReceiptError("map hash does not match current map")
    if receipt.get("prompt_sha256") != digest(prompt_path):
        raise ReceiptError("prompt hash does not match current prompt")
    exact = {
        "book_count": 66,
        "sibling_maps_read_before_review": False,
        "independent_model_or_provider_evidence": True,
        "candidate_only": True,
        "non_authorizing": True,
        "promotion_authorized": False,
        "dissent_and_appeals_preserved": True,
    }
    for key, expected in exact.items():
        if receipt.get(key) != expected:
            raise ReceiptError(f"{key} must equal {expected!r}")
    reviews = receipt.get("book_reviews")
    if not isinstance(reviews, list) or len(reviews) < 66:
        raise ReceiptError("book_reviews must contain at least 66 rows")
    seen = []
    for row in reviews:
        if not isinstance(row, dict):
            raise ReceiptError("book review is not an object")
        book = row.get("book")
        if book not in BOOKS:
            raise ReceiptError(f"unknown book: {book}")
        if book in seen:
            raise ReceiptError(f"duplicate book: {book}")
        seen.append(book)
        for key in ("review_status", "literary_findings", "language_risks", "cross_reference_leads", "red_team_tests"):
            if key not in row:
                raise ReceiptError(f"{book}: missing {key}")
    if set(seen) != BOOKS:
        raise ReceiptError(f"book set incomplete: missing {sorted(BOOKS - set(seen))}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--map", dest="map_path", type=Path, default=ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl")
    parser.add_argument("--prompt", dest="prompt_path", type=Path, default=ROOT / "docs/governance/T521_EXTERNAL_CONVERGENCE_HANDOFF_PROMPT.md")
    args = parser.parse_args()
    try:
        validate(json.loads(args.receipt.read_text(encoding="utf-8")), map_path=args.map_path, prompt_path=args.prompt_path)
    except (OSError, json.JSONDecodeError, ReceiptError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print("OK: external receipt is hash-bound, blind, complete, and non-authorizing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
