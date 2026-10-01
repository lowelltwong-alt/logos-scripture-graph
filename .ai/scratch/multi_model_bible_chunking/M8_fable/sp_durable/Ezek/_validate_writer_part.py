#!/usr/bin/env python3
"""Deterministic validation of one Ezekiel writer part.

A DETERMINISTIC PASS IS NOT SEMANTIC VERIFICATION - standing campaign rule. This tool proves the mechanical
invariants so the peer and boss rounds spend their attention on the seams rather than on arithmetic and schema.
What it cannot judge is whether a boundary is RIGHT; only whether it is well-formed, disclosed, and byte-true.

Checks, in the order a failure most likely matters:

  TILING      the part's rows cover its assigned WEB range exactly - no gap, no overlap, no stray verse
  SEAMS       no row straddles a parent seam or a hard seam (the 14 datelines, the vision onsets)
  ZONE        every ref touching WEB 20:45-49 or WEB ch 21 carries an explicit oshb dual (Tier-0)
  HEBREW      every Hebrew run quoted in a row is a byte substring of Ezek_oshb.txt - the check that catches a
              fabricated quotation, which is the defect class this campaign fears most
  DISCLOSURE  every K/Q verse a span covers is disclosed somewhere in that row
  SCHEMA      the 22 fields, unit_type in the closed 12, confidence in the closed 4, non_authorizing true

Usage: _validate_writer_part.py <draft.jsonl> --part pNN
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

SP = Path(__file__).resolve().parent
POINTS = re.compile(r"[֑-ׇ]")
HEB_RUN = re.compile(r"[֐-׿][֐-׿\s‏]*[֐-׿]")

FIELDS = ["decision_id", "book", "model_id", "chunk_index_in_book", "span", "boundary_rationale",
          "boundary_evidence_refs", "strongest_rejected_alternative", "literature_type_guess", "confidence",
          "strong_or_hebrew_tags_used", "wj_or_red_letter_considered", "frontier_flag_considered",
          "non_authorizing", "review_status", "parent_collection", "unit_type", "writer_part",
          "writer_decision_id", "writer_attempt_id", "observed_substrate_signals", "device_notes"]
UNIT_TYPES = {"vision_report", "commission_narrative", "sign_act", "judgment_oracle", "oracle_against_nation",
              "lament_qinah", "parable_allegory", "disputation_oracle", "salvation_oracle",
              "temple_measurement", "temple_law", "land_allotment"}
CONFIDENCE = {"high", "medium", "medium_low", "low"}

# MT datelines -> WEB, and the parent seams from book_strategy/Ezek.md §5
DATELINES_MT = [(1, 1), (1, 2), (8, 1), (20, 1), (24, 1), (26, 1), (29, 1), (29, 17), (30, 20), (31, 1),
                (32, 1), (32, 17), (33, 21), (40, 1)]
PARENT_STARTS = [(1, 1), (4, 1), (8, 1), (12, 1), (20, 1), (25, 1), (33, 1), (40, 1)]


def mt_to_web(c, v):
    if c == 21 and v <= 5:
        return (20, v + 44)
    if c == 21:
        return (21, v - 5)
    return (c, v)


def parse_ref(s):
    m = re.match(r"Ezek\.(\d+)\.(\d+)$", s.strip())
    return (int(m.group(1)), int(m.group(2))) if m else None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--part", required=True)
    a = ap.parse_args()

    parts = json.loads((SP / "writer_parts.json").read_text(encoding="utf-8"))
    part = next(r for r in parts["rows"] if r["part_id"] == a.part)
    inv = {int(k): v for k, v in
           json.loads((SP / "verse_inventory.json").read_text(encoding="utf-8"))["chapters"].items()}
    pm = json.loads((SP / "pmarks_Ezek.json").read_text(encoding="utf-8"))
    oshb = dict(l.split("\t", 1) for l in (SP / "Ezek_oshb.txt").read_text(encoding="utf-8").splitlines())
    raw_all = "\n".join(oshb.values())
    skel_all = POINTS.sub("", unicodedata.normalize("NFD", raw_all))
    # A QERE IS NOT IN THE VERSE BYTES. It lives in the OSHB note layer, and citing one is exactly what this
    # campaign wants at a textual-variant site. An earlier version of this file checked verse bytes only and
    # flagged two correctly-disclosed Qere citations in p01 as fabrications - a checker defect that, left in,
    # would have trained writers away from disclosing variants at all. The note layer carries morpheme
    # separators; they are stripped for comparison exactly as the verse extract has them stripped.
    kq_raw = " ".join(n for v in pm["kq"].values() for n in v).replace("/", "")
    kq_skel = POINTS.sub("", unicodedata.normalize("NFD", kq_raw))

    rows = [json.loads(l) for l in Path(a.draft).read_text(encoding="utf-8").splitlines() if l.strip()]
    problems, warnings = [], []

    def seq(c1, v1, c2, v2):
        out = []
        for c in range(c1, c2 + 1):
            for v in range(v1 if c == c1 else 1, (v2 if c == c2 else inv[c]) + 1):
                out.append((c, v))
        return out

    want = seq(*parse_ref(part["first"]), *parse_ref(part["last"]))
    covered, seen = [], {}
    for r in rows:
        m = re.match(r"Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)$", r.get("span", ""))
        if not m:
            problems.append("%s: unparseable span %r" % (r.get("decision_id"), r.get("span")))
            continue
        c1, v1, c2, v2 = (int(x) for x in m.groups())
        vs = seq(c1, v1, c2, v2)
        for x in vs:
            if x in seen:
                problems.append("overlap at Ezek.%d.%d (%s and %s)" % (*x, seen[x], r.get("decision_id")))
            seen[x] = r.get("decision_id")
        covered += vs

        # seams: a parent start or dateline strictly inside a row is a straddle
        for (pc, pv) in PARENT_STARTS:
            if (pc, pv) != (c1, v1) and (pc, pv) in vs:
                problems.append("%s: row straddles PARENT seam Ezek.%d.%d" % (r.get("decision_id"), pc, pv))
        for (dc, dv) in DATELINES_MT:
            # MT 1:1-3 is ONE superscription - two datelines in two dating systems plus the third-person
            # word-event - and book_strategy/Ezek.md rules it is never split. So MT 1:2 inside a row that opens
            # at 1:1 is correct, not a straddle. Every OTHER dateline remains a hard seam.
            if (dc, dv) == (1, 2) and (c1, v1) == (1, 1):
                continue
            w = mt_to_web(dc, dv)
            if w != (c1, v1) and w in vs:
                problems.append("%s: row straddles HARD seam (dateline MT %d:%d = WEB %d.%d)"
                                % (r.get("decision_id"), dc, dv, *w))

        # schema
        for f in FIELDS:
            if f not in r:
                problems.append("%s: missing field %s" % (r.get("decision_id"), f))
        if r.get("unit_type") not in UNIT_TYPES:
            problems.append("%s: unit_type %r not in the closed 12" % (r.get("decision_id"), r.get("unit_type")))
        if r.get("confidence") not in CONFIDENCE:
            problems.append("%s: confidence %r not in the closed set" % (r.get("decision_id"), r.get("confidence")))
        if r.get("non_authorizing") is not True:
            problems.append("%s: non_authorizing must be true" % r.get("decision_id"))

        blob = json.dumps(r, ensure_ascii=False)

        # zone duals
        for line in re.findall(r"[^\"]*web:Ezek\.(?:21\.\d+|20\.4[5-9])[^\"]*", blob):
            if "oshb:Ezek.21." not in line:
                problems.append("%s: zone ref without an oshb dual: %s" % (r.get("decision_id"), line[:70]))

        # every Hebrew run must be byte-true
        for run in HEB_RUN.findall(blob):
            run = run.strip()
            if len(run) < 2:
                continue
            if run in raw_all:
                continue
            run_sk = POINTS.sub("", unicodedata.normalize("NFD", run))
            if run_sk in skel_all:
                continue
            if run in kq_raw or run_sk in kq_skel:
                continue  # a Qere from the note layer - legitimate, and disclosed
            problems.append("%s: Hebrew run in neither the verse bytes nor the K/Q note layer: %r"
                            % (r.get("decision_id"), run[:40]))

        # K/Q disclosure for covered verses
        for (c, v) in vs:
            mt = "Ezek.%d.%d" % (c, v) if not (c == 20 and v >= 45) and c != 21 else None
            if mt and mt in pm["kq"] and ("%d:%d" % (c, v)) not in blob and mt not in blob:
                warnings.append("%s: covers K/Q verse %s without naming it" % (r.get("decision_id"), mt))

    missing = [x for x in want if x not in seen]
    extra = [x for x in seen if x not in set(want)]
    if missing:
        problems.append("TILING GAP: %d verses uncovered, first %s" % (len(missing), missing[:5]))
    if extra:
        problems.append("TILING OVERRUN: %d verses outside the part, first %s" % (len(extra), extra[:5]))

    print(json.dumps({
        "part": a.part, "draft": str(a.draft), "rows": len(rows),
        "assigned_verses": len(want), "covered_verses": len(set(seen)),
        "tiling": "EXACT" if not missing and not extra else "BROKEN",
        "confidence_spread": {k: sum(1 for r in rows if r.get("confidence") == k) for k in sorted(CONFIDENCE)},
        "unit_types_used": sorted({r.get("unit_type") for r in rows if r.get("unit_type")}),
        "problems": problems, "warnings": warnings,
        "verdict": "GREEN" if not problems else "RED",
        "limit": "a deterministic pass is NOT semantic verification; it proves form, not judgment",
    }, ensure_ascii=False, indent=1))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
