#!/usr/bin/env python3
"""Phase-0 Tier-0 extractor: pmarks_Prov.json from raw OSHB Prov.xml (WLC single witness).

Prov is in the Writings: petuchah/setumah segs, IF present, are parashah
divisions in the Writings — TIER-3 WEAK corroboration under the owner
addendum (never a driver, always single-witness-disclosed). Unlike Ps
(marks empty by extraction), whatever WLC Prov actually carries is recorded
here from bytes. No selah exists in Prov. All keys are MT numbering
(= WEB numbering; identity book, byte-verified in web_mt_offset_map.json).
"""
from __future__ import annotations

import collections
import json
import re
from pathlib import Path

XML = Path(r"C:\wt\logos-t423-m8-fable\data\candidate\original_language_evidence\canonical_source_views\openscriptures_oshb\files\Prov.xml")
SPBOOK = Path(__file__).resolve().parent.parent
OUT = SPBOOK / "pmarks_Prov.json"

raw = XML.read_text(encoding="utf-8")

event_re = re.compile(
    r'<verse osisID="(Prov\.\d+\.\d+)"'
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

out = {
    "book": "Prov",
    "witness": "WLC (OSHB) — single witness; disclose on every citation",
    "numbering": "MT (= WEB; identity book)",
    "marks": dict(marks),
    "marks_note": (
        "Writings parashah layer: petuchah/setumah here are TIER-3 WEAK corroboration "
        "(owner addendum: parashah_in_prophets_or_writings) — never a boundary driver, "
        "single-witness disclosure required, petuchah vs setumah never conflated. "
        f"Extracted from bytes: {pe_total} PE / {sa_total} SAMEKH segs. "
        "Absence is NEVER counterevidence."
    ),
    "selah_note": "NO selah exists in Prov (Psalter device). Any selah claim in Prov is a fabrication.",
    "paseq": dict(paseq),
    "paseq_note": "Seg layer, NOT quotable verse bytes; citable from this inventory only.",
    "other_segs": dict(other_segs),
    "kq": dict(kq),
    "notes_other": dict(notes_other),
    "morph_prefix_tally": dict(morph_prefixes),
}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({
    "pe_segs": pe_total, "samekh_segs": sa_total, "marked_verses": len(marks),
    "paseq_segs": sum(paseq.values()), "paseq_verses": len(paseq),
    "other_segs": {k: v for k, v in other_segs.items()},
    "kq_notes": sum(kq.values()), "kq_verses": len(kq),
    "notes_other": dict(notes_other), "morph": dict(morph_prefixes),
}, ensure_ascii=False, indent=1))
