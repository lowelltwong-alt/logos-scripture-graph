#!/usr/bin/env python3
"""Validate per-book B01 packet source-routing and artifact completeness."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"
BOOKS = ["Gen","Exod","Lev","Num","Deut","Josh","Judg","Ruth","1Sam","2Sam","1Kgs","2Kgs","1Chr","2Chr","Ezra","Neh","Esth","Job","Ps","Prov","Eccl","Song","Isa","Jer","Lam","Ezek","Dan","Hos","Joel","Amos","Obad","Jonah","Mic","Nah","Hab","Zeph","Hag","Zech","Mal","Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"]
NT = {"Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"}
ROLES = ["role-original_language_translation_scout.json", "role-literary_form_scout.json", "role-canonical_relations_and_premortem_scout.json", "role-second_temple_rabbinic_context_scout.json"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-root", type=Path, default=MODEL)
    args = parser.parse_args()
    errors: list[str] = []
    for book in BOOKS:
        root = args.model_root / "state/r8" / book / f"{book.lower()}-r8-held-1"
        packet = root / "packet"
        manifest = root / "packet" / "input-manifest.json"
        if not manifest.is_file():
            errors.append(f"{book}: missing input-manifest.json")
            continue
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{book}: invalid manifest: {exc}")
            continue
        # Manifest source_ids are canonicalized absolute paths, so match case-insensitively.
        source_ids = [str(x).lower() for x in data.get("source_ids", [])]
        sources = "\n".join(source_ids)
        if book in NT:
            required = ("cntr", "sblgnt", "ugnt")
            if not all(x in sources for x in required):
                errors.append(f"{book}: Greek source family missing")
        else:
            required = ("oshb", "uxlc")
            if not all(x in sources for x in required):
                errors.append(f"{book}: Hebrew source family missing")
        for name in ROLES:
            if not (packet / name).is_file():
                errors.append(f"{book}: missing {name}")
        for name in ("redteam-note.json", "boss-authorization.json"):
            if not (root / name).is_file() and not (packet / name).is_file():
                errors.append(f"{book}: missing {name}")
    if errors:
        print(json.dumps({"status": "FAIL", "books": len(BOOKS), "errors": errors[:30], "error_count": len(errors)}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "OK", "books": len(BOOKS), "candidate_only": True, "non_authorizing": True, "independence_claimed": False}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
