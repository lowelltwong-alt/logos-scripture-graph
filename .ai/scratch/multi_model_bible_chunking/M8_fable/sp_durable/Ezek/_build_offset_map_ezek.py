#!/usr/bin/env python3
"""EZEKIEL WEB<->MT numbering crosswalk, derived and PROVEN from bytes.

WHAT THE BYTES SAID. Per-chapter verse counts from the two staged extracts agree everywhere except:

    ch 20:  WEB 49   MT 44      (WEB has five more)
    ch 21:  WEB 32   MT 37      (MT has five more)

Totals are equal at 1,273, so this is a SHIFT, not a gap or a surplus: the five verses English prints as the tail
of chapter 20 are printed by the Hebrew as the head of chapter 21.

    MT 21:1-5   =  WEB 20:45-49
    MT 21:6-37  =  WEB 21:1-32
    identity everywhere else

CONTENT CONFIRMS IT, and the content is the evidence - the arithmetic alone would also fit a five-verse gap:
MT 21:1 is `vayehi devar-YHWH elay lemor` ("Yahweh's word came to me, saying"), which WEB prints at 20:45;
MT 21:2 is `ben-adam sim panekha derekh teimanah` ("Son of man, set your face toward the south"), WEB 20:46;
MT 21:3 is `ve'amarta le-ya'ar ha-negev` ("Tell the forest of the south"), WEB 20:47.

THIS IS NOT JEREMIAH'S ZONE AND WAS NOT ASSUMED FROM IT. Jeremiah's offset sits at MT 8:23 = WEB 9:1 and was
derived the same way, from its own bytes. Ezekiel was checked independently and its zone landed in a different
place; a book that inherits its predecessor's map is a book whose map was never derived.

TIER-0 CONSEQUENCE, carried into TOOLKIT.md: any structured reference touching WEB ch 20 v45-49, WEB ch 21, or
MT ch 21 MUST carry an explicit dual or numeric qualifier (`web:Ezek.20.45 = oshb:Ezek.21.1`, or `(MT 21:1)` after
a web: ref). Bare coordinates are ambiguous across witnesses exactly there, and only there.
"""
import json
import re
import sys
from pathlib import Path

SP = Path(__file__).resolve().parent
BOOK = "Ezek"
ZONE_LEN = 5


def load():
    oshb = {}
    for line in (SP / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").splitlines():
        r, t = line.split("\t", 1)
        oshb[r] = t
    web, ch = {}, None
    for line in (SP / f"{BOOK}_web_clean.txt").read_text(encoding="utf-8").splitlines():
        m = re.match(r"===== EZEK (\d+) =====", line)
        if m:
            ch = int(m.group(1))
            continue
        m = re.match(r"\[v\] (\d+) (.*)$", line)
        if m and ch:
            web["%s.%d.%s" % (BOOK, ch, m.group(1))] = m.group(2)
    return web, oshb


def web_to_mt(c, v):
    if c == 20 and v >= 45:
        return (21, v - 44)
    if c == 21:
        return (21, v + ZONE_LEN)
    return (c, v)


def mt_to_web(c, v):
    if c == 21 and v <= ZONE_LEN:
        return (20, v + 44)
    if c == 21:
        return (21, v - ZONE_LEN)
    return (c, v)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    web, oshb = load()
    problems = []

    # ---- bijection proof: every WEB verse maps to an existing MT verse, and back to itself ----
    for k in web:
        _, c, v = k.split(".")
        c, v = int(c), int(v)
        mt = web_to_mt(c, v)
        mk = "%s.%d.%d" % (BOOK, *mt)
        if mk not in oshb:
            problems.append("WEB %d.%d -> MT %d.%d which does not exist" % (c, v, *mt))
        elif mt_to_web(*mt) != (c, v):
            problems.append("round trip WEB %d.%d -> MT %d.%d -> WEB %s" % (c, v, *mt, mt_to_web(*mt)))
    for k in oshb:
        _, c, v = k.split(".")
        c, v = int(c), int(v)
        wb = mt_to_web(c, v)
        wk = "%s.%d.%d" % (BOOK, *wb)
        if wk not in web:
            problems.append("MT %d.%d -> WEB %d.%d which does not exist" % (c, v, *wb))
        elif web_to_mt(*wb) != (c, v):
            problems.append("round trip MT %d.%d -> WEB %d.%d -> MT %s" % (c, v, *wb, web_to_mt(*wb)))

    # ---- injectivity: no two WEB verses may land on one MT verse ----
    seen = {}
    for k in web:
        _, c, v = k.split(".")
        mk = web_to_mt(int(c), int(v))
        if mk in seen:
            problems.append("MT %s claimed by both WEB %s and WEB %s" % (mk, seen[mk], k))
        seen[mk] = k

    zone_pairs = [{"web": "web:%s.20.%d" % (BOOK, 44 + i), "mt": "oshb:%s.21.%d" % (BOOK, i),
                   "web_text_head": web["%s.20.%d" % (BOOK, 44 + i)][:60]} for i in range(1, ZONE_LEN + 1)]

    out = {
        "schema": "m8_web_mt_offset_map.v1",
        "book": BOOK,
        "derived_from": ["Ezek_web_clean.txt", "Ezek_oshb.txt"],
        "totals": {"web": len(web), "mt": len(oshb), "equal": len(web) == len(oshb)},
        "rule": {
            "identity_outside_the_zone": True,
            "zone": {
                "what": "the five verses WEB prints as Ezek 20:45-49 are printed by MT as Ezek 21:1-5",
                "mt_21_1_to_5": "= WEB 20:45-49",
                "mt_21_6_to_37": "= WEB 21:1-32",
                "web_chapter_20_verses": 49, "mt_chapter_20_verses": 44,
                "web_chapter_21_verses": 32, "mt_chapter_21_verses": 37,
                "shift_not_gap": "totals are equal at 1273; nothing is added or missing, the chapter break moves",
            },
            "tier0_disclosure": ("any structured ref touching WEB 20:45-49, WEB ch 21, or MT ch 21 MUST carry an "
                                 "explicit dual or numeric qualifier; bare coordinates are ambiguous there and "
                                 "only there"),
        },
        "zone_pairs": zone_pairs,
        "content_anchors": {
            "mt:Ezek.21.1": "vayehi devar-YHWH elay lemor = web:Ezek.20.45 'Yahweh's word came to me, saying'",
            "mt:Ezek.21.2": "ben-adam sim panekha derekh teimanah = web:Ezek.20.46 'set your face toward the south'",
            "mt:Ezek.21.3": "ve'amarta le-ya'ar ha-negev = web:Ezek.20.47 'Tell the forest of the south'",
            "why_content_and_not_only_arithmetic": ("equal totals with a +5/-5 chapter split would also fit a "
                                                    "five-verse gap plus a five-verse surplus; only the text "
                                                    "shows it is one shift"),
        },
        "verification": {"problems": problems,
                         "checks": ["every WEB verse maps to an existing MT verse and round-trips",
                                    "every MT verse maps to an existing WEB verse and round-trips",
                                    "the map is injective - no two WEB verses share an MT verse"],
                         "verdict": "GREEN" if not problems else "RED"},
    }
    (SP / "web_mt_offset_map.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                               encoding="utf-8", newline="\n")

    check = {"schema": "m8_web_mt_verse_check.v1", "book": BOOK,
             "per_chapter": {str(c): {"web": sum(1 for k in web if int(k.split(".")[1]) == c),
                                      "mt": sum(1 for k in oshb if int(k.split(".")[1]) == c)}
                             for c in range(1, 49)},
             "divergent_chapters": [c for c in range(1, 49)
                                    if sum(1 for k in web if int(k.split(".")[1]) == c)
                                    != sum(1 for k in oshb if int(k.split(".")[1]) == c)],
             "verdict": "GREEN" if not problems else "RED"}
    (SP / "web_mt_verse_check.json").write_text(json.dumps(check, ensure_ascii=False, indent=1),
                                                encoding="utf-8", newline="\n")

    print(json.dumps({"web_verses": len(web), "mt_verses": len(oshb),
                      "divergent_chapters": check["divergent_chapters"],
                      "zone": "MT 21:1-5 = WEB 20:45-49; MT 21:6-37 = WEB 21:1-32",
                      "problems": problems, "verdict": out["verification"]["verdict"]},
                     ensure_ascii=False, indent=1))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
