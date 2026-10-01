#!/usr/bin/env python3
"""Whole-chapter confidence-cap sweep, Lam - Tier-0 HARD suite member (E-02).

Campaign law (Isa boss B-6 lineage, five books of evidence): a row whose
span is exactly one whole WEB chapter is a CHAPTER-FALLBACK unit and must
carry confidence in {medium_low, low}, frontier_flag_considered True, and a
cap disclosure in its own prose (heuristic: the chapter's verse count cited
AND a cap/whole-chapter phrasing). In Isa this rule lived in prose only and
shipped 12 violations - 4 found by NO reviewer, only the boss's sweep. It
is machine-checkable, so it is a validator now (durability law:
validator > gate > contract > chat).

Rows without a span field are skipped (review packets etc.). Row id key:
writer_decision_id or decision_id. Any failure = RED.
Usage: cap_sweep.py rows.jsonl
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lam_lib import LAST_VERSE

SPAN = re.compile(r"^(?:web:)?Lam\.(\d+)\.(\d+)-Lam\.(\d+)\.(\d+)$")
PROSE_FIELDS = ("boundary_rationale", "device_notes", "strongest_rejected_alternative")


def rows_from(p: Path):
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    data = json.loads(text)
    if isinstance(data, dict):
        return data.get("decisions", [v for v in data.values() if isinstance(v, dict)])
    return data


def main() -> int:
    assert len(LAST_VERSE) == 5 and sum(LAST_VERSE.values()) == 154, \
        (len(LAST_VERSE), sum(LAST_VERSE.values()))
    rows_file = sys.argv[1] if len(sys.argv) > 1 else "rows.jsonl"
    found = []
    failures = []
    skipped = 0
    for r in rows_from(Path(rows_file)):
        if not isinstance(r, dict):
            continue
        span = r.get("span")
        if not isinstance(span, str):
            skipped += 1
            continue
        m = SPAN.match(span.strip())
        if not m:
            continue                      # span-form errors are citation_sweep's arm
        c1, v1, c2, v2 = map(int, m.groups())
        if not (c1 == c2 and v1 == 1 and v2 == LAST_VERSE.get(c1, -1)):
            continue
        rid = r.get("writer_decision_id") or r.get("decision_id") or "?"
        found.append(rid)
        prose = " ".join(str(r.get(f, "")) for f in PROSE_FIELDS)
        if r.get("confidence") not in ("medium_low", "low"):
            failures.append(f"{rid} whole-chapter (ch {c1}) at confidence {r.get('confidence')!r} "
                            f"- the chapter-fallback cap is medium_low")
        if str(r.get("frontier_flag_considered")) not in ("True", "true"):
            failures.append(f"{rid} whole-chapter (ch {c1}) without frontier flag")
        has_count = str(LAST_VERSE[c1]) in prose
        has_cap = re.search(r"whole[- ]chapter|chapter[- ]fallback|capped|cap\b", prose, re.I)
        if not (has_count and has_cap):
            failures.append(f"{rid} cap disclosure missing/incomplete "
                            f"(count-cited={has_count}, cap-phrase={bool(has_cap)})")
    print(json.dumps({"whole_chapter_rows": sorted(found),
                      "rows_without_span_skipped": skipped,
                      "failures": failures,
                      "status": "GREEN" if not failures else "RED"}, indent=1))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
