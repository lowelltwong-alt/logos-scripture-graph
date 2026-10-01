#!/usr/bin/env python3
"""Tier-0 extractor: ../pmarks_<Book>.json from the raw OSHB <Book>.xml (WLC
single witness). Book-parametrized rebuild (2026-09-03, OW-2 item-2 audit
toolkits for Ps and Job) of the Prov/Eccl/Song lineage extractor.

Ps expectations (book_strategy/Ps.md §4, byte-derived at the Ps Phase 0 and
RE-ASSERTED here from the same XML): NO petuchah/setumah segs at all; paseq
522 segs / 481 verses; x-reversednun 7 (MT 107); x-suspended 1 (MT 80:14);
K/Q 68 notes / 65 verses; morph all H (no Aramaic).
Job expectations (book_strategy/Job.md §4): 26 PE + 13 SAMEKH; paseq 98 / 93;
x-suspended 2 (MT 38:13, 38:15); K/Q 53 / 49; morph all H.
A mismatch against the strategy record is SURFACED (assertion), never
silently accepted — the bytes rule, but the discrepancy must be explained.
All keys are MT numbering (map WEB spans through <book>_lib.web_to_mt()).
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
BOOK = SPBOOK.name
XML = Path(r"C:\wt\logos-t423-m8-fable\data\candidate\original_language_evidence"
           r"\canonical_source_views\openscriptures_oshb\files") / f"{BOOK}.xml"
OUT = SPBOOK / f"pmarks_{BOOK}.json"

EXPECT = {
    "Ps": {"pe": 0, "samekh": 0, "paseq_segs": 522, "paseq_verses": 481,
           "reversednun": 7, "suspended": 1, "kq_notes": 68, "kq_verses": 65},
    "Job": {"pe": 26, "samekh": 13, "paseq_segs": 98, "paseq_verses": 93,
            "reversednun": 0, "suspended": 2, "kq_notes": 53, "kq_verses": 49},
}[BOOK]

raw = XML.read_text(encoding="utf-8")

event_re = re.compile(
    rf'<verse osisID="({BOOK}\.\d+\.\d+)"'
    r'|<seg type="(x-pe|x-samekh|x-paseq|x-suspended|x-reversednun|x-large|x-small)">([^<]*)</seg>'
    r'|<note type="(variant|exegesis|alternative)">'
)

current = None
marks: dict[str, list[str]] = collections.defaultdict(list)
paseq: dict[str, int] = collections.Counter()
other_segs: dict[str, list[str]] = collections.defaultdict(list)
kq: dict[str, int] = collections.Counter()
notes_other: dict[str, list[str]] = collections.defaultdict(list)

for m in event_re.finditer(raw):
    if m.group(1):
        current = m.group(1)
    elif m.group(2):
        seg_type, content = m.group(2), m.group(3)
        if current is None:
            raise SystemExit(f"seg {seg_type} before any verse — extractor assumption broken")
        if seg_type == "x-pe":
            marks[current].append("PE")
        elif seg_type == "x-samekh":
            marks[current].append("SAMEKH")
        elif seg_type == "x-paseq":
            paseq[current] += 1
        else:
            other_segs[current].append(f"{seg_type}:{content}")
    elif m.group(4) == "variant":
        if current is None:
            raise SystemExit("variant note before any verse")
        kq[current] += 1
    elif m.group(4):
        notes_other[current or "BEFORE_FIRST_VERSE"].append(m.group(4))

morph_prefixes = collections.Counter(v[0] for v in re.findall(r'morph="([^"]+)"', raw))

pe_total = sum(1 for v in marks.values() for x in v if x == "PE")
sa_total = sum(1 for v in marks.values() for x in v if x == "SAMEKH")
rn_total = sum(1 for v in other_segs.values() for x in v if x.startswith("x-reversednun"))
su_total = sum(1 for v in other_segs.values() for x in v if x.startswith("x-suspended"))
got = {"pe": pe_total, "samekh": sa_total, "paseq_segs": sum(paseq.values()),
       "paseq_verses": len(paseq), "reversednun": rn_total, "suspended": su_total,
       "kq_notes": sum(kq.values()), "kq_verses": len(kq)}
mismatch = {k: (EXPECT[k], got[k]) for k in EXPECT if EXPECT[k] != got[k]}
assert not mismatch, f"{BOOK} pmarks vs strategy record MISMATCH (expected, got): {mismatch}"
assert set(morph_prefixes) == {"H"}, f"non-Hebrew morph prefixes present: {dict(morph_prefixes)}"

if BOOK == "Ps":
    marks_note = ("WLC Psalms carries NO petuchah/setumah segs AT ALL (byte-verified here): the "
                  "parashah layer is ABSENT; absence is never counterevidence, and ANY positive "
                  "pe/samekh claim in Ps is a fabrication (hard error).")
    selah_note = ("Selah is VERSE TEXT in both witnesses (WEB 'Selah' / MT סלה) — no witness tag "
                  "needed; span-scoped symmetry applies (every Selah inside a row's span is "
                  "disclosable). Word-bound sweep: see sweep.py --skel.")
    numbering = "MT (NOT = WEB in 63 psalms: title verses + the Ps 13 split — map WEB through ps_lib.web_to_mt())"
else:
    marks_note = ("Writings parashah layer: petuchah/setumah here are TIER-3 WEAK corroboration "
                  "(owner addendum: parashah_in_prophets_or_writings) — never a boundary driver, "
                  "single-witness disclosure required, petuchah vs setumah never conflated. "
                  f"Extracted from bytes: {pe_total} PE / {sa_total} SAMEKH segs; the mark FOLLOWS "
                  "its verse. Absence is NEVER counterevidence (chs 4, 6, 9, 12, 13, 16, 23, 27, 29, "
                  "30, 36, 38 carry no marks).")
    selah_note = "NO selah exists in Job (Psalter device). Any selah claim in Job is a fabrication."
    numbering = "MT (= WEB except the zone: WEB 41:1-8 = MT 40:25-32, WEB 41:9-34 = MT 41:1-26 — map through job_lib.web_to_mt())"

out = {
    "book": BOOK,
    "witness": "WLC (OSHB) — single witness; disclose on every citation",
    "numbering": numbering,
    "marks": dict(marks),
    "marks_note": marks_note,
    "selah_note": selah_note,
    "paseq": dict(paseq),
    "paseq_note": "Seg layer, NOT quotable verse bytes; citable from this inventory only; COUNT-ONLY — intra-verse position claims are unsourceable.",
    "other_segs": dict(other_segs),
    "other_segs_note": "x-reversednun / x-suspended / x-large / x-small segs AS THE BYTES HAVE THEM (traditions differ on placement — cite the inventory, single-witness).",
    "kq": dict(kq),
    "kq_note": "Ketiv/qere variant-note count per MT verse; the staged extract carries ketiv+qere adjacent — check before counting or slicing in a K/Q verse.",
    "notes_other": dict(notes_other),
    "morph_prefix_tally": dict(morph_prefixes),
    "strategy_record_reasserted": EXPECT,
}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"book": BOOK, **got, "other_segs_sites": {k: v for k, v in other_segs.items()},
                  "notes_other": dict(notes_other), "morph": dict(morph_prefixes),
                  "strategy_record": "MATCH"}, ensure_ascii=False, indent=1))
