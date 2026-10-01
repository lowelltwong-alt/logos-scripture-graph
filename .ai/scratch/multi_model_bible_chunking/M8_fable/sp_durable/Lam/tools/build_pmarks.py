#!/usr/bin/env python3
"""Phase-0 Tier-0 extractor: pmarks_Lam.json from raw OSHB Lam.xml (WLC single witness).
Lam is in the WRITINGS (Megillot): petuchah/setumah segs are TIER-3 WEAK corroboration under the owner
addendum (parashah_in_prophets_or_writings), never a driver, always single-witness-disclosed. Whatever
WLC Lam carries is recorded from bytes; nothing is assumed. ALL KEYS ARE MT NUMBERING (identity with WEB)."""
from __future__ import annotations
import collections, json, re
from pathlib import Path
XML = Path(r"C:\wt\logos-t423-m8-fable\data\candidate\original_language_evidence\canonical_source_views\openscriptures_oshb\files\Lam.xml")
SPBOOK = Path(__file__).resolve().parent.parent
OUT = SPBOOK / "pmarks_Lam.json"
raw = XML.read_text(encoding="utf-8")
event_re = re.compile(r'<verse osisID="(Lam\.\d+\.\d+)"|<seg type="(x-pe|x-samekh|x-paseq|x-suspended|x-reversednun|x-large|x-small)">([^<]*)</seg>|<note type="(variant|exegesis|alternative)">|morph="([^"]+)"')
current = None
marks = collections.defaultdict(list); paseq = collections.Counter(); other_segs = collections.defaultdict(list)
kq = collections.Counter(); notes_other = collections.defaultdict(list); morph_prefixes = collections.Counter(); aramaic = collections.Counter()
for m in event_re.finditer(raw):
    if m.group(1): current = m.group(1)
    elif m.group(2):
        assert current is not None
        st, content = m.group(2), m.group(3)
        if st == "x-pe": marks[current].append("PE")
        elif st == "x-samekh": marks[current].append("SAMEKH")
        elif st == "x-paseq": paseq[current] += 1
        else: other_segs[current].append(f"{st}:{content}")
    elif m.group(4) == "variant": kq[current] += 1
    elif m.group(4): notes_other[current or "BEFORE_FIRST_VERSE"].append(m.group(4))
    elif m.group(5):
        morph_prefixes[m.group(5)[0]] += 1
        if m.group(5).startswith("A"): aramaic[current] += 1
pe_total = sum(1 for v in marks.values() for x in v if x == "PE"); sa_total = sum(1 for v in marks.values() for x in v if x == "SAMEKH")
assert dict(other_segs) == {}, dict(other_segs)
assert dict(morph_prefixes) == {"H": 1564}, dict(morph_prefixes)
assert dict(aramaic) == {}, dict(aramaic)
assert sum(kq.values()) == 22, sum(kq.values())
assert (pe_total, sa_total) == (5, 84), (pe_total, sa_total)
assert sum(paseq.values()) == 11, sum(paseq.values())
out = {"book": "Lam", "witness": "WLC (OSHB) - single witness; disclose on every citation",
       "numbering": "MT = WEB (identity in every chapter; byte-proven in web_mt_offset_map.json)",
       "marks": dict(marks),
       "marks_note": (f"Writings parashah layer: petuchah/setumah are TIER-3 WEAK corroboration (owner addendum: parashah_in_prophets_or_writings) - never a boundary driver, single-witness disclosure required, petuchah vs setumah never conflated. Extracted from bytes: {pe_total} PE / {sa_total} SAMEKH segs over {len(marks)} marked verses. Absence is NEVER counterevidence."),
       "selah_note": "NO selah exists in Lam (Psalter device). Any selah claim in Lam is a fabrication.",
       "paseq": dict(paseq), "paseq_note": "Seg layer, NOT quotable verse bytes; citable from this inventory only; COUNT-ONLY (no intra-verse positions).",
       "other_segs": {}, "other_segs_note": "WLC Lam carries NO special-letter seg of any class (no small/large/suspended/reversed-nun): any such claim in Lam is a fabrication.",
       "kq": dict(kq), "kq_note": f"K/Q inventory: {sum(kq.values())} variant notes over {len(kq)} verses; doubled-note verses: {sorted(k for k, n in kq.items() if n > 1)}. Check kq BEFORE counting or slicing in ANY K/Q verse.",
       "notes_other": dict(notes_other), "notes_other_note": "Exegesis/alternative notes are single-witness apparatus, not text bytes.",
       "morph_prefix_tally": dict(morph_prefixes), "aramaic_verses": [],
       "language_note": "Lam is Hebrew throughout (1,564 H-prefixed morph codes, 0 A-prefixed). Any Aramaic verse label in Lam is a flag."}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"pe_segs": pe_total, "samekh_segs": sa_total, "marked_verses": len(marks), "paseq_segs": sum(paseq.values()), "paseq_verses": len(paseq),
                  "kq_notes": sum(kq.values()), "kq_verses": len(kq), "kq_doubled": sorted(k for k, n in kq.items() if n > 1), "notes_other": dict(notes_other), "morph": dict(morph_prefixes)}, ensure_ascii=False, indent=1))
