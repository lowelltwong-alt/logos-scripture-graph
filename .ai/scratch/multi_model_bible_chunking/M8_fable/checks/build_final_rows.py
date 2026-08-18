#!/usr/bin/env python3
"""Build frozen_rows_final.jsonl from v0 rows + boss rulings + author final edits (Tier-0).

Applies retirements, splits/merges/shifts, renumbers indices, bumps review_revision on
changed rows, and re-verifies exact verse coverage and gate constraints.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PASSAGES = ROOT / "data" / "canonical" / "scripture" / "passages" / "passages.jsonl"
LOW = {"low", "medium_low"}


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def span_key(span: str, positions: dict[str, int]) -> tuple[int, int]:
    start_raw, end_raw = span.split("-")
    sb, sc, sv = start_raw.split(".")
    eb, ec, ev = end_raw.split(".")
    return positions[f"{sb}.{int(sc)}.{int(sv)}"], positions[f"{eb}.{int(ec)}.{int(ev)}"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    args = parser.parse_args()
    book = args.book
    work = args.work_dir

    v0 = {row["decision_id"]: row for row in read_jsonl(work / "frozen_rows_v0.jsonl")}
    rulings = json.loads((work / "boss_rulings.json").read_text(encoding="utf-8"))
    edits = json.loads((work / "final_rows_edits.json").read_text(encoding="utf-8"))
    appeals_path = work / "appeals.json"
    appeals = json.loads(appeals_path.read_text(encoding="utf-8")) if appeals_path.is_file() else {}

    refs = [row["osis_ref"] for row in read_jsonl(PASSAGES) if row.get("book") == book]
    positions = {ref: index for index, ref in enumerate(refs)}

    rows = []
    retired = []
    for decision_id, ruling in rulings.items():
        if decision_id.startswith("_"):
            continue
        if ruling["final_state"] == "superseded":
            retired.append(decision_id)
            continue
        base = dict(v0.get(decision_id, {
            "model_id": "M8_fable", "book": book,
            "strong_or_hebrew_tags_used": False,
            "wj_or_red_letter_considered": True,
            "frontier_flag_considered": True,
            "non_authorizing": True,
        }))
        base["decision_id"] = decision_id
        edit = edits.get(decision_id)
        directives = ruling.get("final_directives", {})
        changed = False
        if edit:
            for field in ("span", "literature_type_guess", "confidence",
                          "boundary_rationale", "strongest_rejected_alternative",
                          "boundary_evidence_refs"):
                if field in edit:
                    value = edit[field]
                    if field == "span" and isinstance(value, str) and " (" in value:
                        # normalize: MT pairing belongs in evidence refs, not the span field
                        value = value.split(" (")[0].strip()
                    if value != base.get(field):
                        base[field] = value
                        changed = True
        for field in ("span", "literature_type_guess", "confidence"):
            if directives.get(field) and base.get(field) != directives[field]:
                raise SystemExit(f"{decision_id}: author edit {field}={base.get(field)!r} contradicts boss directive {directives[field]!r}")
        if "span" not in base or "confidence" not in base:
            raise SystemExit(f"{decision_id}: incomplete row (new decision missing edit?)")
        base["review_revision"] = 1 if (changed or decision_id not in v0) else 0
        rows.append(base)

    rows.sort(key=lambda row: span_key(row["span"], positions))
    covered = []
    for index, row in enumerate(rows, start=1):
        row["chunk_index_in_book"] = index
        a, b = span_key(row["span"], positions)
        covered.extend(refs[a : b + 1])
    if covered != refs:
        covered_set = set(covered)
        missing = [r for r in refs if r not in covered_set][:8]
        dupes = sorted({r for r in covered if covered.count(r) > 1})[:8]
        raise SystemExit(f"coverage FAIL: expected={len(refs)} covered={len(covered)} missing={missing} dupes={dupes}")

    chapter_last = {}
    for ref in refs:
        _, ch, v = ref.split(".")
        chapter_last[int(ch)] = int(v)
    chapter_spans = {f"{book}.{ch}.1-{book}.{ch}.{last}" for ch, last in chapter_last.items()}
    chapter_shaped = [row for row in rows if row["span"] in chapter_spans]
    bad_caps = [row["decision_id"] for row in chapter_shaped if row["confidence"] not in LOW]
    if bad_caps:
        raise SystemExit(f"chapter-shaped rows lacking low/medium_low cap: {bad_caps}")

    low_ids = sorted(row["decision_id"] for row in rows if row["confidence"] in LOW)

    out = work / "frozen_rows_final.jsonl"
    with out.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    superseded = []
    for decision_id in retired:
        superseded.append({
            "decision_id": decision_id,
            "superseded_by": rulings[decision_id]["final_directives"].get("merged_into"),
            "frozen_row_v0": v0.get(decision_id, {"note": "decision created and retired within the review rounds; no v0 row"}),
            "boss_ruling": rulings[decision_id],
            "non_authorizing": True,
        })
    with (work / "superseded_decisions.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for row in superseded:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    revised = [row["decision_id"] for row in rows if row["review_revision"] == 1]
    span_changed = [
        row["decision_id"] for row in rows
        if row["decision_id"] not in v0 or row["span"] != v0[row["decision_id"]]["span"]
    ]
    print(json.dumps({
        "book": book,
        "active_decisions": len(rows),
        "retired": retired,
        "coverage": f"{len(covered)}/{len(refs)}",
        "chapter_shaped": [row["span"] for row in chapter_shaped],
        "low_confidence_ids": low_ids,
        "revised_rows": len(revised),
        "span_changed": span_changed,
        "appealed": sorted(appeals.keys()),
    }, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
