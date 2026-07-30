#!/usr/bin/env python3
"""Validate uniform candidate-only literary review fields across Sol's map."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate(path: Path) -> tuple[int, list[str]]:
    rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    errors: list[str] = []
    for i, row in enumerate(rows, 1):
        prefix = f"row {i} {row.get('book')} {row.get('span')}"
        if row.get("candidate_only") is not True:
            errors.append(prefix + ": candidate_only must be true")
        if row.get("non_authorizing") is not True:
            errors.append(prefix + ": non_authorizing must be true")
        if row.get("working_title_is_boundary_authority") is not False:
            errors.append(prefix + ": working_title_is_boundary_authority must be false")
        for key in ("candidate_internal_seams", "cross_reference_holds", "red_team_premortem_holds"):
            if not isinstance(row.get(key), list) or not row[key]:
                errors.append(prefix + f": missing nonempty {key}")
        if row.get("book") in {"Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"}:
            if not isinstance(row.get("koine_greek_translation_holds"), list) or not row["koine_greek_translation_holds"]:
                errors.append(prefix + ": missing Koine holds")
        else:
            if not isinstance(row.get("original_language_translation_holds"), list) and not isinstance(row.get("translation_and_crossref_holds"), list):
                errors.append(prefix + ": missing Hebrew/Aramaic or translation holds")
    return len(rows), errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("map_path", type=Path)
    args = parser.parse_args()
    count, errors = validate(args.map_path)
    if errors:
        print(json.dumps({"status": "FAIL", "rows": count, "errors": errors[:20], "error_count": len(errors)}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "OK", "rows": count, "candidate_only": True, "non_authorizing": True, "independence_claimed": False}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
