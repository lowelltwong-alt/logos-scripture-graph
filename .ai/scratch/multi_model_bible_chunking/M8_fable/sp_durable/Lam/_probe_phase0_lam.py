#!/usr/bin/env python3
"""Phase-0 EXPLORATORY probe for Lam (orchestrator-only, throwaway). From bytes only: OSHB apparatus
(segs by type, K/Q notes, morph language prefixes, KJV-variance notes, maqaf), WEB extract hygiene
(apparatus lines, [fn] sites, poetry lines), per-verse first letters (acrostic landscape incl. the
pe/ayin order per chapter), chapter verse counts both witnesses."""
import collections, json, re, unicodedata
from pathlib import Path
SP = Path(__file__).resolve().parent
XML = Path(r"C:\wt\logos-t423-m8-fable\data\candidate\original_language_evidence\canonical_source_views\openscriptures_oshb\files\Lam.xml")
raw = XML.read_text(encoding="utf-8")
POINTS = re.compile(r"[\u0591-\u05C7]")
out = {}
out["verses_xml"] = len(re.findall(r'<verse[^>]*osisID="Lam\.', raw))
segs = collections.Counter(re.findall(r'<seg type="([^"]+)"', raw))
out["segs_by_type"] = dict(segs)
notes = re.findall(r'<note[^>]*type="([^"]*)"[^>]*>(.*?)</note>', raw, flags=re.S)
out["notes_by_type"] = dict(collections.Counter(t for t, _ in notes))
out["kq_notes"] = sum(1 for t, b in notes if "variant" in t.lower() or "K" in b[:3] or "Q" in b[:3])
morph = collections.Counter(m[0] for m in re.findall(r'morph="([A-Za-z])', raw))
out["morph_prefix"] = dict(morph)
out["maqaf_in_xml"] = raw.count("\u05BE")
out["x_maqqef_segs"] = raw.count('type="x-maqqef"')
# per-verse Aramaic check
ar = [v for v in re.findall(r'<verse[^>]*osisID="(Lam\.\d+\.\d+)"(.*?)</verse>', raw, flags=re.S) if 'morph="A' in v[1]]
out["aramaic_verses"] = [v[0] for v in ar]
# extract hygiene
web = (SP / "Lam_web_clean.txt").read_text(encoding="utf-8").splitlines()
out["web_lines"] = len(web)
out["apparatus_lines"] = collections.Counter(re.match(r"\s*\[([A-Z-]+)", l).group(1) for l in web if re.match(r"\s*\[[A-Z-]+", l))
out["fn_sites"] = sum(l.count("[fn") for l in web)
out["poetry_q_lines"] = sum(1 for l in web if "|q" in l)
oshb = {}
for line in (SP / "Lam_oshb.txt").read_text(encoding="utf-8").splitlines():
    if "\t" in line:
        ref, text = line.split("\t", 1); oshb[ref] = text
out["verses_oshb"] = len(oshb)
out["maqaf_in_extract"] = sum(t.count("\u05BE") for t in oshb.values())
inv = json.loads((SP / "verse_inventory.json").read_text(encoding="utf-8"))
out["web_chapters"] = inv["chapters"]
mt_ch = collections.Counter(int(r.split(".")[1]) for r in oshb)
out["mt_chapters"] = dict(sorted(mt_ch.items()))
# acrostic landscape: first consonant of each verse (skeleton), per chapter
def skel(s): return POINTS.sub("", unicodedata.normalize("NFD", s))
ALEF = ord("\u05D0")
acro = {}
for c in range(1, 6):
    letters = []
    for v in range(1, mt_ch[c] + 1):
        t = skel(oshb[f"Lam.{c}.{v}"]).strip()
        letters.append(t[0] if t else "?")
    acro[str(c)] = "".join(letters)
out["first_letters_by_chapter"] = acro
# expected 22-letter order and the pe/ayin swap check
order = "".join(chr(ALEF + i) for i in range(22)).replace("\u05DA", "").replace("\u05DD", "").replace("\u05DF", "").replace("\u05E3", "").replace("\u05E5", "")
out["alef_bet_22"] = order
def diag(c, step):
    s = acro[str(c)]
    seq = s[::step] if step > 1 else s
    return {"len": len(s), "sampled": seq, "matches_standard": seq == order, "ayin_pe_swapped": seq == order.replace("\u05E2\u05E4", "\u05E4\u05E2")}
out["acrostic_diag"] = {"1": diag(1, 1), "2": diag(2, 1), "3": diag(3, 3), "4": diag(4, 1), "5": {"len": len(acro["5"]), "note": "22 verses, no acrostic expected", "matches_standard": acro["5"] == order}}
# ch 3 triplets: verses 3k-2,3k-1,3k share a letter?
tri_ok = all(len(set(acro["3"][i:i+3])) == 1 for i in range(0, 66, 3))
out["ch3_triplets_uniform"] = tri_ok
print(json.dumps(out, ensure_ascii=False, indent=1))
