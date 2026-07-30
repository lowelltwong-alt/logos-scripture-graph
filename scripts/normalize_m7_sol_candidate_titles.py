#!/usr/bin/env python3
"""Give fallback candidates reviewable titles without changing their spans.

Only existing ``boundary_rationale`` or ``structural_unit_type`` fields are
used.  This is metadata normalization, not literary adjudication.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def normalize(row: dict) -> bool:
    title = str(row.get("working_title", ""))
    if "structural frame (draft)" not in title and not title.lower().startswith("chapter "):
        return False
    rationale = str(row.get("boundary_rationale", "")).strip()
    if rationale:
        candidate = rationale.split(";", 1)[0].split(". ", 1)[0].strip()
    else:
        candidate = str(row.get("structural_unit_type", "candidate structural unit")).replace("_", " ").strip()
    if not candidate:
        candidate = "candidate structural unit"
    row["working_title"] = candidate[:180]
    row["working_title_origin"] = "existing_boundary_rationale_only"
    row["working_title_is_boundary_authority"] = False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("map_path", type=Path)
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.map_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed = sum(normalize(row) for row in rows)
    args.map_path.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8", newline="\n")
    print(json.dumps({"rows": len(rows), "titles_normalized": changed, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
