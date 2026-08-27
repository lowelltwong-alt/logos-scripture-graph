#!/usr/bin/env python3
"""Phase-0 Tier-0 extractor: pmarks_Isa.json from raw OSHB Isa.xml (WLC single witness).

Isa is in the PROPHETS: petuchah/setumah segs are parashah divisions —
TIER-3 WEAK corroboration under the owner addendum
(parashah_in_prophets_or_writings), never a driver, always
single-witness-disclosed. Whatever WLC Isa actually carries is recorded here
from bytes; nothing is assumed. No selah is expected in Isa (Psalter device)
— the extraction verifies. ALL KEYS ARE MT NUMBERING. Isa is NOT an identity
book: MT 8:23 = WEB 9:1, MT 9:1-20 = WEB 9:2-21, MT 63:19 spans WEB 63:19 +
64:1 (SPLIT), MT 64:1-11 = WEB 64:2-12 (byte-proven in
web_mt_offset_map.json). Use isa_lib.mt_to_web_all()/web_to_mt() to move
between spaces.
"""
from __future__ import annotations

import collections
import json
import re
from pathlib import Path

XML = Path(r"C:\wt\logos-t423-m8-fable\data\candidate\original_language_evidence\canonical_source_views\openscriptures_oshb\files\Isa.xml")
SPBOOK = Path(__file__).resolve().parent.parent
OUT = SPBOOK / "pmarks_Isa.json"

raw = XML.read_text(encoding="utf-8")

event_re = re.compile(
    r'<verse osisID="(Isa\.\d+\.\d+)"'
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

# Phase-0 hard expectations from the probe (fail loudly if the source moved)
assert dict(other_segs) == {"Isa.44.14": ["x-small:ן"]}, \
    f"special-letter inventory moved: {dict(other_segs)}"
assert morph_prefixes == {"H": 16988}, f"morph tally moved: {dict(morph_prefixes)}"
assert sum(kq.values()) == 53 and len(kq) == 49, \
    f"K/Q inventory moved: {sum(kq.values())} notes / {len(kq)} verses"

out = {
    "book": "Isa",
    "witness": "WLC (OSHB) — single witness; disclose on every citation",
    "numbering": ("MT (NOT identical to WEB: MT 8:23 = WEB 9:1; MT 9:1-20 = WEB 9:2-21; "
                  "MT 63:19 SPANS WEB 63:19 + 64:1; MT 64:1-11 = WEB 64:2-12; use isa_lib "
                  "crosswalk — mt_to_web_all for the split verse)"),
    "marks": dict(marks),
    "marks_note": (
        "Prophets parashah layer — the campaign's LARGEST so far: petuchah/setumah here are "
        "TIER-3 WEAK corroboration (owner addendum: parashah_in_prophets_or_writings) — never "
        "a boundary driver, single-witness disclosure required, petuchah vs setumah never "
        f"conflated. Extracted from bytes: {pe_total} PE / {sa_total} SAMEKH segs. "
        "Absence is NEVER counterevidence."
    ),
    "selah_note": "NO selah exists in Isa (Psalter device). Any selah claim in Isa is a fabrication.",
    "paseq": dict(paseq),
    "paseq_note": "Seg layer, NOT quotable verse bytes; citable from this inventory only; COUNT-ONLY (no intra-verse positions).",
    "other_segs": dict(other_segs),
    "other_segs_note": (
        "Exactly ONE special-letter seg in WLC Isa: a SMALL NUN (x-small ן) at MT 44:14 — the "
        "book's only special letter. Small-letter claims are valid ONLY there; any large-letter, "
        "suspended-letter, or reversed-nun claim anywhere in Isa is a fabrication. (The famous "
        "MT 9:6 medial final-mem in לםרבה is in the LETTER BYTES, not a seg — see the TOOLKIT "
        "hazard catalog.)"
    ),
    "kq": dict(kq),
    "kq_note": (
        "The campaign's LARGEST K/Q inventory: 53 variant notes over 49 verses. TWO sit INSIDE "
        "offset zone A: MT 9:2 (= WEB 9:3) and MT 9:6 (= WEB 9:7, the לםרבה medial-final-mem "
        "pair, staged as a DOUBLED token). NONE in zone B (the split verse MT 63:19 is NOT "
        "K/Q-bearing). Check kq before counting or slicing in ANY K/Q verse."
    ),
    "notes_other": dict(notes_other),
    "notes_other_note": "ONE exegesis note at MT 9:5 (= WEB 9:6, the throne-names verse) — single-witness apparatus, not text bytes; also inside zone A.",
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
