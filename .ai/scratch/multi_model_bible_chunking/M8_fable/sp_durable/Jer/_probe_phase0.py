#!/usr/bin/env python3
"""Phase-0 EXPLORATORY probe for Jer (orchestrator-only, throwaway).
Answers, from bytes only: the WEB/MT offset landscape at the ch 8-9 seam,
the OSHB apparatus layers (segs / K-Q / morph language codes / KJV-variance
notes), extract hygiene (apparatus lines, maqaf, pseudo-verses).
Feeds the hand-written build_offset_map.py assertions — never assumed."""
from __future__ import annotations

import collections
import json
import re
import unicodedata
from pathlib import Path

SP = Path(__file__).resolve().parent
XML = Path(r"C:\wt\logos-t423-m8-fable\data\candidate\original_language_evidence\canonical_source_views\openscriptures_oshb\files\Jer.xml")

POINTS = re.compile(r"[\u0591-\u05C7]")
FINALS = str.maketrans("\u05DA\u05DD\u05DF\u05E3\u05E5", "\u05DB\u05DE\u05E0\u05E4\u05E6")


def skeleton(s: str) -> str:
    return POINTS.sub("", unicodedata.normalize("NFD", s)).replace("\u05BE", " ")


def anorm(s: str) -> str:
    return s.translate(FINALS)


inv = json.loads((SP / "verse_inventory.json").read_text(encoding="utf-8"))
web_last = {int(c): n for c, n in inv["chapters"].items()}

oshb: dict[str, str] = {}
mt_last: dict[int, int] = {}
for line in (SP / "Jer_oshb.txt").read_text(encoding="utf-8").splitlines():
    if "\t" not in line:
        continue
    ref, text = line.split("\t", 1)
    _, c, v = ref.split(".")
    c, v = int(c), int(v)
    mt_last[c] = max(mt_last.get(c, 0), v)
    oshb[f"{c}.{v}"] = text

out: dict = {}
out["totals"] = {"web": sum(web_last.values()), "mt": sum(mt_last.values()),
                 "web_ch": len(web_last), "mt_ch": len(mt_last)}
out["diff_chapters"] = {c: {"web": web_last.get(c), "mt": mt_last.get(c)}
                        for c in sorted(set(web_last) | set(mt_last))
                        if web_last.get(c) != mt_last.get(c)}

web_text: dict[str, str] = {}
ch = None
cur = None
clean = (SP / "Jer_web_clean.txt").read_text(encoding="utf-8")
for line in clean.splitlines():
    h = re.match(r"===== JER (\d+) =====", line)
    if h:
        ch = int(h.group(1)); cur = None
        continue
    body = re.sub(r"^(\u00B6[\u00BB\u203A]?\([^)]*\)|\u00B6|\s*\u2022|\s*\|[a-z0-9]+(?:\([^)]*\))?)\s*", "", line)
    parts = re.split(r"\[v\] (\d+)\s*", body)
    if parts[0].strip() and cur:
        web_text[cur] += " " + parts[0].strip()
    i = 1
    while i < len(parts):
        cur = f"{ch}.{int(parts[i])}"
        web_text[cur] = parts[i + 1].strip()
        i += 2

out["web_parsed_verses"] = len(web_text)
appar = [l.strip()[:70] for l in clean.splitlines()
         if re.match(r"\s*\[(SUPERSCRIPTION|MAJOR-SECTION|HEADING|SPEAKER)", l.strip())]
out["apparatus_lines"] = {"count": len(appar), "sample": appar[:6]}
out["fn_sites"] = clean.count("[fn ")
out["pseudo_verses"] = {"web_dot0": [r for r in web_text if r.endswith(".0")],
                        "mt_dot0": [r for r in oshb if r.endswith(".0")]}
out["maqaf_in_staged_oshb"] = (SP / "Jer_oshb.txt").read_text(encoding="utf-8").count("\u05BE")

seam = {}
for label, key, src in [
    ("MT_8_22", "8.22", oshb), ("WEB_8_22", "8.22", web_text),
    ("MT_8_23", "8.23", oshb), ("WEB_9_1", "9.1", web_text),
    ("MT_9_1", "9.1", oshb), ("WEB_9_2", "9.2", web_text),
    ("MT_9_16", "9.16", oshb), ("WEB_9_17", "9.17", web_text),
    ("MT_9_20", "9.20", oshb), ("WEB_9_21", "9.21", web_text),
    ("MT_9_24", "9.24", oshb), ("WEB_9_25", "9.25", web_text),
    ("MT_9_25", "9.25", oshb), ("WEB_9_26", "9.26", web_text),
    ("MT_10_1", "10.1", oshb), ("WEB_10_1", "10.1", web_text),
    ("MT_10_11", "10.11", oshb), ("WEB_10_11", "10.11", web_text),
    ("MT_10_12", "10.12", oshb), ("WEB_10_12", "10.12", web_text),
]:
    t = src.get(key, "<MISSING>")
    seam[label] = (skeleton(t) if src is oshb else t)[:150]
out["seam"] = seam

raw = XML.read_text(encoding="utf-8")
out["morph_prefixes"] = dict(collections.Counter(m[0] for m in re.findall(r'morph="([^"]+)"', raw)))
out["seg_types"] = dict(collections.Counter(re.findall(r'<seg type="(x-[a-z]+)"', raw)))
out["note_types"] = dict(collections.Counter(re.findall(r'<note type="([a-z]+)"', raw)))
kjv = re.findall(r'type="KJV">([^<]*)<', raw)
out["kjv_variance"] = {"count": len(kjv), "sample": kjv[:10]}

cur = None
aram: dict[str, int] = collections.Counter()
kq: dict[str, int] = collections.Counter()
other_segs: dict[str, list] = collections.defaultdict(list)
for m in re.finditer(r'<verse osisID="(Jer\.\d+\.\d+)"'
                     r'|morph="([^"]+)"'
                     r'|<seg type="(x-small|x-large|x-suspended|x-reversednun)">([^<]*)</seg>'
                     r'|<note type="(variant)">', raw):
    if m.group(1):
        cur = m.group(1)
    elif m.group(2):
        if m.group(2).startswith("A"):
            aram[cur] += 1
    elif m.group(3):
        other_segs[cur].append(f"{m.group(3)}:{m.group(4)}")
    elif m.group(5):
        kq[cur] += 1
out["aramaic_morph_verses"] = dict(aram)
out["special_segs"] = dict(other_segs)
out["kq"] = {"notes": sum(kq.values()), "verses": len(kq),
             "doubled": sorted(k for k, n in kq.items() if n > 1)}

print(json.dumps(out, ensure_ascii=False, indent=1))
