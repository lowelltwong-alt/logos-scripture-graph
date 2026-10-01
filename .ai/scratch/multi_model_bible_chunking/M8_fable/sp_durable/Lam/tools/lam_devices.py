#!/usr/bin/env python3
"""Rebuilds ../lam_device_inventory.json from bytes (orchestrator-run; agents consume the JSON).
Every count NAMES its object; every needle is FINALS-NORMALIZED (E-11 discipline) and swept against
the finals-normalized skeleton index; MT keys (= WEB keys, identity book).

The Lamentations structural spine this inventory serves:
 - THE ACROSTIC (tier-1 inclusio_refrain_acrostic signal): chs 1, 2, 4 one verse per letter; ch 3
   three verses per letter; ch 5 not acrostic; ch 1 standard ayin-pe order, chs 2-4 pe-ayin.
 - EIKHAH openings (the book's onset word) and where else the form recurs.
 - VOICE markers: first-person singular onsets (ani ha-gever 3:1), the 'daughter of ...' formulas
   (bat-Tsiyon / bat-Yehudah / bat-ammi / betulat bat-...), second-person address to YHWH.
 - The 'no comforter' refrain (ein menachem) and the 'day of anger' formula.
 - Divine names: YHWH, Adonai, El/Elohim; the 5:19-22 close.
 - Chapter texture: verses opening poetry lines, paseq, K/Q, parashah per chapter.
"""
from __future__ import annotations
import json, re, sys, unicodedata
from pathlib import Path
TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent
BOOK = "Lam"
POINTS = re.compile(r"[\u0591-\u05C7]")
FINALS = str.maketrans("\u05DA\u05DD\u05DF\u05E3\u05E5", "\u05DB\u05DE\u05E0\u05E4\u05E6")
def skel(s): return POINTS.sub("", unicodedata.normalize("NFD", s)).replace("\u05BE", " ").translate(FINALS)
oshb = {}
for line in (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").splitlines():
    if "\t" in line:
        ref, text = line.split("\t", 1); oshb[ref.split(".", 1)[1]] = text
SK = {k: skel(v) for k, v in oshb.items()}
TOK = {k: v.split() for k, v in SK.items()}
KEY = lambda k: tuple(map(int, k.split(".")))
web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
pm = json.loads((SPBOOK / "pmarks_Lam.json").read_text(encoding="utf-8"))
spine = json.loads((TOOLS / "acrostic_spine.json").read_text(encoding="utf-8"))
H = lambda s: s.translate(FINALS)
def verses_with_token(needle, prefixes=True):
    """verses whose skeleton carries a token equal to needle, or needle behind a single prefix letter
    (vav/he/bet/lamed/kaf/mem/shin) - explicit per-length test, never a blind stripper."""
    n = H(needle); out = []
    for k, toks in TOK.items():
        for t in toks:
            if t == n or (prefixes and len(t) == len(n) + 1 and t[0] in "\u05d5\u05d4\u05d1\u05dc\u05db\u05de\u05e9" and t[1:] == n):
                out.append(k); break
    return sorted(set(out), key=KEY)
def verses_with_phrase(*needles):
    ns = [H(x) for x in needles]; out = []
    for k, toks in TOK.items():
        for i in range(len(toks) - len(ns) + 1):
            if all(toks[i + j] == ns[j] or (len(toks[i + j]) == len(ns[j]) + 1 and toks[i + j][0] in "\u05d5\u05d4\u05d1\u05dc\u05db\u05de\u05e9" and toks[i + j][1:] == ns[j]) for j in range(len(ns))):
                out.append(k); break
    return sorted(set(out), key=KEY)
def verse_initial(needle):
    n = H(needle); return sorted([k for k, t in TOK.items() if t and (t[0] == n)], key=KEY)
inv = {"book": BOOK, "numbering": "identity (WEB == MT, 154 verses, 5 chapters)", "acrostic_spine": spine}
inv["eikhah"] = {"verse_initial": verse_initial("\u05d0\u05d9\u05db\u05d4"), "any_position": verses_with_token("\u05d0\u05d9\u05db\u05d4", prefixes=False),
                 "note": "eikhah opens the book and the acrostics of chs 2 and 4 (aleph line); verse-initial sites are the byte census"}
inv["first_person_onset"] = {"ani_hagever_3_1": verses_with_phrase("\u05d0\u05e0\u05d9", "\u05d4\u05d2\u05d1\u05e8"),
                             "ani_token_verses": verses_with_token("\u05d0\u05e0\u05d9", prefixes=False),
                             "note": "3:1 'I am the man' opens the first-person lament; ani/anokhi sites are a voice census, not seams by themselves"}
inv["daughter_formulas"] = {"bat_tsiyon": verses_with_phrase("\u05d1\u05ea", "\u05e6\u05d9\u05d5\u05df"), "bat_yehudah": verses_with_phrase("\u05d1\u05ea", "\u05d9\u05d4\u05d5\u05d3\u05d4"),
                            "bat_ammi": verses_with_phrase("\u05d1\u05ea", "\u05e2\u05de\u05d9"), "bat_yerushalam": verses_with_phrase("\u05d1\u05ea", "\u05d9\u05e8\u05d5\u05e9\u05dc\u05dd"),
                            "betulat_bat": verses_with_phrase("\u05d1\u05ea\u05d5\u05dc\u05ea", "\u05d1\u05ea"), "bat_edom": verses_with_phrase("\u05d1\u05ea", "\u05d0\u05d3\u05d5\u05dd"),
                            "note": "personification address formulas (vocative/apostrophe shifts); counts are verse censuses of the two-token phrase with single-letter prefix tolerance on the first token"}
inv["refrains"] = {"ein_menachem": verses_with_phrase("\u05d0\u05d9\u05df", "\u05de\u05e0\u05d7\u05dd"), "menachem_token": verses_with_token("\u05de\u05e0\u05d7\u05dd"),
                   "yom_af": verses_with_phrase("\u05d9\u05d5\u05dd", "\u05d0\u05e3"), "af_token": verses_with_token("\u05d0\u05e3", prefixes=True),
                   "note": "ein menachem = the ch-1 'no comforter' refrain (refrains CLOSE units under the owner-ruled seam law, weighed from both sides); yom af = day-of-anger formula"}
inv["divine_names"] = {"yhwh": verses_with_token("\u05d9\u05d4\u05d5\u05d4", prefixes=True), "adonai": verses_with_token("\u05d0\u05d3\u05e0\u05d9", prefixes=True),
                       "el": verses_with_token("\u05d0\u05dc", prefixes=False), "elohim_any": [k for k in sorted(TOK, key=KEY) if any(t.startswith("\u05d0\u05dc\u05d4") for t in TOK[k])],
                       "note": "YHWH and Adonai verse censuses (prefix-tolerant); 'el' bare-token count includes the preposition homograph - a review list, not a divine-name count"}
inv["imperatives_to_yhwh"] = {"zekhor": verses_with_token("\u05d6\u05db\u05e8", prefixes=False), "reeh": verses_with_token("\u05e8\u05d0\u05d4", prefixes=False), "habitah": verses_with_token("\u05d4\u05d1\u05d9\u05d8\u05d4", prefixes=False),
                              "note": "petition onsets ('remember / look / behold') - candidate tier-1 discourse-frame signals (ch 5 opens with zekhor YHWH)"}
texture = {}
for c in range(1, 6):
    keys = [k for k in sorted(TOK, key=KEY) if KEY(k)[0] == c]
    texture[str(c)] = {"verses": len(keys), "poetry_line_verses": sum(1 for k in keys if web[f"{BOOK}.{k}"]["poetry_lines"]),
                       "pe": sum(1 for k in keys for m in pm["marks"].get(f"{BOOK}.{k}", []) if m == "PE"), "samekh": sum(1 for k in keys for m in pm["marks"].get(f"{BOOK}.{k}", []) if m == "SAMEKH"),
                       "paseq": sum(pm["paseq"].get(f"{BOOK}.{k}", 0) for k in keys), "kq_notes": sum(pm["kq"].get(f"{BOOK}.{k}", 0) for k in keys),
                       "yhwh": sum(1 for k in keys if k in set(inv["divine_names"]["yhwh"])), "adonai": sum(1 for k in keys if k in set(inv["divine_names"]["adonai"])),
                       "acrostic": spine[str(c)]["order"]}
inv["chapter_texture"] = texture
inv["chapter_texture_note"] = "staging profile for the part plan; writers re-derive, never row evidence"
# Phase-0 hard expectations (pinned from the first byte pass 2026-09-07; fail loudly if the source moves)
assert inv["eikhah"]["verse_initial"] == ["1.1", "2.1", "4.1"], inv["eikhah"]["verse_initial"]
assert inv["first_person_onset"]["ani_hagever_3_1"] == ["3.1"], inv["first_person_onset"]["ani_hagever_3_1"]
assert inv["refrains"]["ein_menachem"] == ["1.9", "1.17", "1.21"] and len(inv["refrains"]["menachem_token"]) == 5, (inv["refrains"]["ein_menachem"], inv["refrains"]["menachem_token"])
assert len(inv["divine_names"]["yhwh"]) == 32 and len(inv["divine_names"]["adonai"]) == 13, (len(inv["divine_names"]["yhwh"]), len(inv["divine_names"]["adonai"]))
assert len(inv["daughter_formulas"]["bat_tsiyon"]) == 8 and len(inv["daughter_formulas"]["bat_ammi"]) == 5, "daughter formula census moved"
assert texture["3"]["poetry_line_verses"] == 57 and texture["5"]["samekh"] == 0 and sum(t["pe"] for t in texture.values()) == 5, "texture moved"
(SPBOOK / "lam_device_inventory.json").write_text(json.dumps(inv, ensure_ascii=False, indent=1), encoding="utf-8")
summary = {k: ({kk: (len(vv) if isinstance(vv, list) else vv) for kk, vv in v.items() if kk != "note"} if isinstance(v, dict) and k != "acrostic_spine" and k != "chapter_texture" else None) for k, v in inv.items()}
summary = {k: v for k, v in summary.items() if v is not None}
summary["eikhah_sites"] = inv["eikhah"]["verse_initial"]; summary["ein_menachem_sites"] = inv["refrains"]["ein_menachem"]; summary["ani_hagever"] = inv["first_person_onset"]["ani_hagever_3_1"]
summary["chapter_texture"] = texture
print(json.dumps(summary, ensure_ascii=False, indent=1))
