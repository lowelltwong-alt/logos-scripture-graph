#!/usr/bin/env python3
"""Phase-0 Tier-0 extractor: pmarks_Jer.json from raw OSHB Jer.xml (WLC single witness).

Jer is in the PROPHETS: petuchah/setumah segs are parashah divisions -
TIER-3 WEAK corroboration under the owner addendum
(parashah_in_prophets_or_writings), never a driver, always
single-witness-disclosed. Whatever WLC Jer actually carries is recorded here
from bytes; nothing is assumed. No selah is expected in Jer (Psalter device)
- the extraction verifies. ALL KEYS ARE MT NUMBERING. Jer is NOT an identity
book: MT 8:23 = WEB 9:1, MT 9:1-25 = WEB 9:2-26 (byte-proven in
web_mt_offset_map.json; ONE zone, NO split). Use jer_lib.mt_to_web()/
web_to_mt() to move between spaces.

Jer ALSO records the language layer here: the single Aramaic verse MT 10:11
(byte-proven from morph codes - 15 A-prefixed codes, all in that verse).
"""
from __future__ import annotations

import collections
import json
import re
from pathlib import Path

XML = Path(r"C:\wt\logos-t423-m8-fable\data\candidate\original_language_evidence\canonical_source_views\openscriptures_oshb\files\Jer.xml")
SPBOOK = Path(__file__).resolve().parent.parent
OUT = SPBOOK / "pmarks_Jer.json"

raw = XML.read_text(encoding="utf-8")

event_re = re.compile(
    r'<verse osisID="(Jer\.\d+\.\d+)"'
    r'|<seg type="(x-pe|x-samekh|x-paseq|x-suspended|x-reversednun|x-large|x-small)">([^<]*)</seg>'
    r'|<note type="(variant|exegesis|alternative)">'
    r'|morph="([^"]+)"'
)

current = None
marks: dict[str, list[str]] = collections.defaultdict(list)
paseq: dict[str, int] = collections.Counter()
other_segs: dict[str, list[str]] = collections.defaultdict(list)
kq: dict[str, int] = collections.Counter()
notes_other: dict[str, list[str]] = collections.defaultdict(list)
morph_prefixes: dict[str, int] = collections.Counter()
aramaic_verses: dict[str, int] = collections.Counter()

for m in event_re.finditer(raw):
    if m.group(1):
        current = m.group(1)
    elif m.group(2):
        seg_type, content = m.group(2), m.group(3)
        if current is None:
            raise SystemExit(f"seg {seg_type} before any verse - extractor assumption broken")
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
    elif m.group(5):
        morph_prefixes[m.group(5)[0]] += 1
        if m.group(5).startswith("A"):
            aramaic_verses[current] += 1

pe_total = sum(1 for v in marks.values() for x in v if x == "PE")
sa_total = sum(1 for v in marks.values() for x in v if x == "SAMEKH")

# Phase-0 hard expectations from the probe (fail loudly if the source moved)
assert dict(other_segs) == {"Jer.39.13": ["x-small:\u05DF\u0599"]}, \
    f"special-letter inventory moved: {dict(other_segs)}"
assert dict(morph_prefixes) == {"H": 21961, "A": 15}, \
    f"morph tally moved: {dict(morph_prefixes)}"
assert dict(aramaic_verses) == {"Jer.10.11": 15}, \
    f"Aramaic verse inventory moved: {dict(aramaic_verses)}"
assert sum(kq.values()) == 141 and len(kq) == 124, \
    f"K/Q inventory moved: {sum(kq.values())} notes / {len(kq)} verses"
assert (pe_total, sa_total) == (58, 246), \
    f"parashah inventory moved: {pe_total} PE / {sa_total} SAMEKH"
assert sum(paseq.values()) == 157, f"paseq inventory moved: {sum(paseq.values())}"

out = {
    "book": "Jer",
    "witness": "WLC (OSHB) - single witness; disclose on every citation",
    "numbering": ("MT (NOT identical to WEB: MT 8:23 = WEB 9:1; MT 9:1-25 = WEB 9:2-26; "
                  "every other chapter identity; NO split - use jer_lib crosswalk)"),
    "marks": dict(marks),
    "marks_note": (
        "Prophets parashah layer - the campaign's LARGEST yet (surpassing Isa's 209 segs): "
        "petuchah/setumah here are TIER-3 WEAK corroboration (owner addendum: "
        "parashah_in_prophets_or_writings) - never a boundary driver, single-witness "
        "disclosure required, petuchah vs setumah never conflated. Extracted from bytes: "
        f"{pe_total} PE / {sa_total} SAMEKH segs over {len(marks)} marked verses. "
        "Absence is NEVER counterevidence."
    ),
    "selah_note": "NO selah exists in Jer (Psalter device). Any selah claim in Jer is a fabrication.",
    "paseq": dict(paseq),
    "paseq_note": "Seg layer, NOT quotable verse bytes; citable from this inventory only; COUNT-ONLY (no intra-verse positions).",
    "other_segs": dict(other_segs),
    "other_segs_note": (
        "Exactly ONE special-letter seg in WLC Jer: a SMALL NUN (x-small) at MT 39:13 - the "
        "book's only special letter (the seg content carries its accent mark in the source "
        "bytes). Small-letter claims are valid ONLY there; any large-letter, suspended-letter, "
        "or reversed-nun claim anywhere in Jer is a fabrication."
    ),
    "kq": dict(kq),
    "kq_note": (
        "The campaign's LARGEST K/Q inventory by a wide margin: 141 variant notes over 124 "
        "verses (Isa's 53/49 was the previous record). Twelve doubled-note verses: MT 3:19, "
        "4:19, 6:25, 13:20, 14:14, 22:23, 48:7, 48:20, 49:39, 50:6, 50:11, 51:34. NONE of the "
        "zone verses MT 8:23 / MT ch 9 carry K/Q notes IF the inventory says so - CHECK the "
        "inventory, never assume, and check kq BEFORE counting or slicing in ANY K/Q verse."
    ),
    "notes_other": dict(notes_other),
    "notes_other_note": "Exegesis notes are single-witness apparatus, not text bytes - see the keys recorded here.",
    "morph_prefix_tally": dict(morph_prefixes),
    "aramaic_verses": sorted(aramaic_verses),
    "language_note": (
        "EXACTLY ONE Aramaic verse in Jer: MT 10:11 = WEB 10:11 (identity numbering) - a "
        "self-contained Aramaic island (15 A-prefixed morph codes) inside the ch-10 idol "
        "polemic. Labeling ANY other verse Aramaic is flagged; labeling 10:11 Hebrew is a "
        "defect; Aramaism/Aramaic-influence discussion elsewhere is legitimate."
    ),
}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

zone_kq = sorted(k for k in kq if k.startswith("Jer.8.23") or k.startswith("Jer.9."))
print(json.dumps({
    "pe_segs": pe_total, "samekh_segs": sa_total, "marked_verses": len(marks),
    "paseq_segs": sum(paseq.values()), "paseq_verses": len(paseq),
    "other_segs": {k: v for k, v in other_segs.items()},
    "kq_notes": sum(kq.values()), "kq_verses": len(kq),
    "kq_doubled": sorted(k for k, n in kq.items() if n > 1),
    "kq_in_offset_zone_mt_keys": zone_kq,
    "notes_other": dict(notes_other), "morph": dict(morph_prefixes),
    "aramaic_verses": sorted(aramaic_verses),
}, ensure_ascii=False, indent=1))
