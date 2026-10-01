#!/usr/bin/env python3
"""Normalize legacy review-hold field names into the fidelity-field contract."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks"


def main() -> int:
    changed = 0
    for path in sorted(BASE.glob("*/chunks.jsonl")):
        rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
        for row in rows:
            if not row.get("cross_reference_holds"):
                legacy = row.get("translation_and_crossref_holds") or row.get("cross_reference_seed_refs") or []
                if isinstance(legacy, list) and legacy:
                    row["cross_reference_holds"] = list(legacy)
                else:
                    row["cross_reference_holds"] = ["internal and canonical relation leads require verification; no boundary authority"]
                changed += 1
            if not row.get("red_team_premortem_holds"):
                row["red_team_premortem_holds"] = ["test local form, translation, discourse, and closure signals rather than chapter numbering alone"]
                changed += 1
            row["working_title_is_boundary_authority"] = False
            row["candidate_only"] = True
            row["non_authorizing"] = True
        path.write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows), encoding="utf-8", newline="\n")
    print(json.dumps({"rows_or_fields_changed": changed, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
