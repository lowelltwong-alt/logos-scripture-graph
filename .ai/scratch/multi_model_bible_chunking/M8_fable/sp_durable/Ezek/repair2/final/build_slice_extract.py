#!/usr/bin/env python3
"""Build the WITNESS EXTRACT for one final-remediation slice (OW-24 token economy).

WHY. A lane that opens Ezek_oshb.txt (331 KB), verse_map_web.json (609 KB) and pmarks_Ezek.json (29 KB) carries about a
megabyte of witness in its context, and that context is re-read by every one of its own tool calls. Measured on the
pilot: 79-93 tool calls per lane. The verses a slice can possibly need are its rows' spans plus a margin on each side,
so the extract holds exactly those and nothing else - typically a tenth of the bytes, with the same text, byte for byte,
SLICED from the pinned witnesses (never retyped).

Each verse carries: the OSHB consonantal-plus-pointing line verbatim, the WEB 'text' field verbatim, the marks the
apparatus records on that verse (a mark is recorded on the verse it FOLLOWS), and its K/Q and paseq entries. The MT and
WEB keys are both given for a verse in the chapter 20-21 zone, taken from the offset map, never computed here.

usage: python build_slice_extract.py --slice K [--margin 3]
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
sys.path.insert(0, str(EZ / "tools"))
from ezek_lib import LAST_VERSE                                                 # noqa: E402

K = int(sys.argv[sys.argv.index("--slice") + 1])
MARGIN = int(sys.argv[sys.argv.index("--margin") + 1]) if "--margin" in sys.argv else 3
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
OSHB, PM, VM = EZ / "Ezek_oshb.txt", EZ / "pmarks_Ezek.json", EZ / "tools" / "verse_map_web.json"
OFF = EZ / "web_mt_offset_map.json"
SPAN = re.compile(r"^Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)$")

sl = json.loads((HERE / ("final_slices_s%d_laneA.v1.json" % K)).read_text(encoding="utf-8"))


def walk(c, v, n):
    """n verses forward (n<0 backward) in the WEB numbering, clamped to the book."""
    while n > 0:
        c, v, n = (c, v + 1, n - 1) if v < LAST_VERSE[c] else ((c + 1, 1, n - 1) if c + 1 in LAST_VERSE else (c, v, 0))
    while n < 0:
        c, v, n = (c, v - 1, n + 1) if v > 1 else ((c - 1, LAST_VERSE[c - 1], n + 1) if c - 1 in LAST_VERSE else (c, v, 0))
    return c, v


wanted = []
for r in sl["slices"].values():
    m = SPAN.match(r["span"])
    c1, v1, c2, v2 = (int(x) for x in m.groups())
    c, v = walk(c1, v1, -MARGIN)
    end = walk(c2, v2, MARGIN)
    while (c, v) <= end:
        if (c, v) not in wanted:
            wanted.append((c, v))
        c, v = (c, v + 1) if v < LAST_VERSE[c] else (c + 1, 1)
        if c not in LAST_VERSE:
            break
wanted = sorted(set(wanted))

oshb = {}
for line in OSHB.read_text(encoding="utf-8").splitlines():
    if "\t" in line:
        k, t = line.split("\t", 1)
        oshb[k] = t
vm = json.loads(VM.read_text(encoding="utf-8"))
pm = json.loads(PM.read_text(encoding="utf-8"))
offs = json.loads(OFF.read_text(encoding="utf-8"))
# the map's zone_pairs carry the only WEB->MT divergence in the book, as 'web:Ezek.c.v' / 'oshb:Ezek.c.v' pairs
web_to_mt = {}
for pair in (offs.get("zone_pairs") or []):
    w, m = str(pair.get("web", "")), str(pair.get("mt", ""))
    if w.startswith("web:Ezek.") and m.startswith("oshb:Ezek."):
        web_to_mt[w.split(":", 1)[1]] = m.split(":", 1)[1]
# MT 21:6-37 = WEB 21:1-32 is the same shift, stated by the map's rule; derive it from the rule's own numbers
zr = ((offs.get("rule") or {}).get("zone") or {})
if zr.get("mt_21_6_to_37") == "= WEB 21:1-32":
    for v in range(1, int(zr.get("web_chapter_21_verses", 32)) + 1):
        web_to_mt["Ezek.21.%d" % v] = "Ezek.21.%d" % (v + 5)
def by_verse(value, label):
    """pmarks carries a mapping (marks: ref -> mark), a plain list of refs (paseq), or a list of records."""
    out = {}
    if isinstance(value, dict):
        for ref, v in value.items():
            out.setdefault(str(ref), []).append(v if not isinstance(v, (dict, list)) else v)
    elif isinstance(value, list):
        for e in value:
            if isinstance(e, str):
                out.setdefault(e, []).append(label)
            elif isinstance(e, dict):
                ref = e.get("verse") or e.get("ref") or e.get("after_verse")
                if ref:
                    out.setdefault(str(ref), []).append(e)
    return out


marks_by_verse = by_verse(pm.get("marks"), "mark")
paseq_by_verse = by_verse(pm.get("paseq"), "paseq recorded within this verse (count only)")
kq_by_verse = {}
for key in ("kq", "notes_other", "other_segs"):
    for ref, v in by_verse(pm.get(key), key).items():
        kq_by_verse.setdefault(ref, []).extend([{"field": key, "entry": x} for x in v])

verses, missing = {}, []
for c, v in wanted:
    web_key = "Ezek.%d.%d" % (c, v)
    mt_key = web_to_mt.get(web_key, web_key)
    rec = {}
    if mt_key in oshb:
        rec["oshb_mt_key"] = mt_key
        rec["hebrew"] = oshb[mt_key]
    else:
        missing.append(mt_key)
    w = vm.get(web_key)
    if w:
        rec["web_text"] = w.get("text")
        if w.get("para_before"):
            rec["web_para_before"] = w["para_before"]
        if w.get("poetry_lines"):
            rec["web_poetry_lines"] = w["poetry_lines"]
    # THE APPARATUS IS MT-NUMBERED. An earlier version fell back to the WEB key when the MT key held nothing, and in the
    # chapter 20-21 zone that attached another verse's entry: WEB 21:3 (= MT 21:8, which has no paseq) picked up the paseq
    # recorded at MT 21:3 (= WEB 20:47). Two lanes then disclosed a paseq that does not exist, and the slice-5
    # adjudicator caught it. There is no fallback: the MT key is the only key.
    for label, src in (("marks_recorded_on_this_verse", marks_by_verse), ("paseq", paseq_by_verse), ("kq_and_notes", kq_by_verse)):
        hit = src.get(mt_key)
        if hit:
            rec[label] = hit
    verses[web_key] = rec
out = {"schema": "ezek_final_slice_extract.v1", "slice": K, "margin_verses": MARGIN,
       "numbering": "keys are WEB references; 'oshb_mt_key' gives the MT reference the Hebrew line was sliced from (they differ only in the chapter 20-21 zone)",
       "sliced_from": {"Ezek_oshb.txt": sha(OSHB), "verse_map_web.json": sha(VM), "pmarks_Ezek.json": sha(PM), "web_mt_offset_map.json": sha(OFF)},
       "rule": ("every string here is verbatim from the file named above: Hebrew is SLICED, never retyped; a mark is listed on the verse it "
                "FOLLOWS, and every mark, paseq or puncta mention in a row carries 'single-witness'"),
       "verses_count": len(verses), "verses_missing_from_the_witness": missing, "verses": verses}
p = HERE / ("final_extract_s%d.v1.json" % K)
data = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
if p.exists() and p.read_bytes() != data:
    raise SystemExit("REFUSED: %s exists with different bytes (E-41)" % p.name)
p.write_bytes(data)
print(json.dumps({"slice": K, "verses": len(verses), "missing": len(missing), "bytes": len(data), "sha256": sha(p)}, indent=1))
