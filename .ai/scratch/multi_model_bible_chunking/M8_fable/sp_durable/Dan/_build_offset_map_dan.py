#!/usr/bin/env python3
"""DANIEL WEB<->MT numbering crosswalk, derived and PROVEN from bytes.

Adapted from Ezek/_build_offset_map_ezek.py. The bijection and injectivity proof is unchanged; the zones are
Daniel's own.

WHAT THE BYTES SAID (dan_stage_report.json, MEASURED 2026-09-23). Per-chapter verse counts agree everywhere except:

    ch 3:  WEB 30   MT 33      ch 4:  WEB 37   MT 34      (a three-verse shift across the 3/4 break)
    ch 5:  WEB 31   MT 30      ch 6:  WEB 28   MT 29      (a one-verse shift across the 5/6 break)

Totals are equal at 357. The rule this builder tests is two SHIFTS:

    MT 3:31-33 = WEB 4:1-3      MT 4:1-34 = WEB 4:4-37
    MT 6:1     = WEB 5:31       MT 6:2-29 = WEB 6:1-28
    identity everywhere else

The counts alone would also fit a gap plus a surplus. The rule is therefore tested two ways that did not build it:
  - the OSHB's own KJV-variance note layer (`KJV:Dan.c.v` notes on MT verses), which is read here from the XML and
    must agree on every note;
  - the zone-boundary text heads of both witnesses, emitted as zone_pairs for a reader to compare. They are
    EXTRACTED; this script does not judge them.

No other book's zone was assumed. Ezekiel's zone sits at its 20/21 break, Jeremiah's at MT 8:23 = WEB 9:1, and
Daniel's was derived from its own counts.

TIER-0 CONSEQUENCE: any structured reference touching WEB 4:1-37, WEB 5:31, WEB ch 6, MT 3:31-33, MT ch 4 or MT
ch 6 MUST carry an explicit dual or numeric qualifier. Bare coordinates are ambiguous across witnesses there.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

SP = Path(__file__).resolve().parent
BOOK = "Dan"
REPO = Path(r"C:\wt\logos-t423-m8-fable")
OSHB_XML = REPO / "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/files/Dan.xml"
CHAPTERS = range(1, 13)


def load():
    oshb = {}
    for line in (SP / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").splitlines():
        r, t = line.split("\t", 1)
        oshb[r] = t
    web, ch = {}, None
    for line in (SP / f"{BOOK}_web_clean.txt").read_text(encoding="utf-8").splitlines():
        m = re.match(r"===== DAN (\d+) =====", line)
        if m:
            ch = int(m.group(1))
            continue
        m = re.match(r"\[v\] (\d+) (.*)$", line)
        if m and ch:
            web["%s.%d.%s" % (BOOK, ch, m.group(1))] = m.group(2)
    return web, oshb


def web_to_mt(c, v):
    if c == 4 and v <= 3:
        return (3, v + 30)
    if c == 4:
        return (4, v - 3)
    if c == 5 and v == 31:
        return (6, 1)
    if c == 6:
        return (6, v + 1)
    return (c, v)


def mt_to_web(c, v):
    if c == 3 and v >= 31:
        return (4, v - 30)
    if c == 4:
        return (4, v + 3)
    if c == 6 and v == 1:
        return (5, 31)
    if c == 6:
        return (6, v - 1)
    return (c, v)


VERSE = re.compile(r'<verse[^>]*osisID="Dan\.(\d+)\.(\d+)"[^>]*>(.*?)(?=<verse|</chapter)', re.S)
KJV = re.compile(r"<note[^>]*>\s*KJV:Dan\.(\d+)\.(\d+)\s*</note>")


def kjv_crosscheck():
    """Every `KJV:Dan.c.v` note on MT verse (C, V) must equal mt_to_web(C, V). The note layer played no part in
    deriving the rule, so agreement is corroboration and not a restatement."""
    raw = OSHB_XML.read_bytes()
    notes, disagree = [], []
    for c, v, body in VERSE.findall(raw.decode("utf-8")):
        for kc, kv in KJV.findall(body):
            mt, en = (int(c), int(v)), (int(kc), int(kv))
            notes.append(mt)
            if mt_to_web(*mt) != en:
                disagree.append({"mt": "%d:%d" % mt, "kjv_note": "%d:%d" % en, "map": "%d:%d" % mt_to_web(*mt)})
    return {"source_sha256": hashlib.sha256(raw).hexdigest(), "notes": len(notes),
            "notes_inside_zones": sum(1 for n in notes if mt_to_web(*n) != n),
            "disagreements": disagree}


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

    kx = kjv_crosscheck()
    if kx["disagreements"]:
        problems.append("%d KJV-variance notes disagree with the map" % len(kx["disagreements"]))

    boundary = [(4, 1), (4, 3), (4, 4), (4, 37), (5, 30), (5, 31), (6, 1), (6, 28)]
    zone_pairs = [{"web": "web:%s.%d.%d" % (BOOK, c, v), "mt": "oshb:%s.%d.%d" % (BOOK, *web_to_mt(c, v)),
                   "web_text_head": web["%s.%d.%d" % (BOOK, c, v)][:70],
                   "mt_text_head": " ".join(oshb["%s.%d.%d" % (BOOK, *web_to_mt(c, v))].split()[:4])}
                  for c, v in boundary]

    def count(d, c):
        return sum(1 for k in d if int(k.split(".")[1]) == c)

    out = {
        "schema": "m8_web_mt_offset_map.v1",
        "book": BOOK,
        "numbering_face": ("WEB (English) coordinates are the campaign's row face; an MT coordinate is written only "
                           "with an explicit oshb: prefix or an (MT c:v) qualifier"),
        "derived_from": ["Dan_web_clean.txt", "Dan_oshb.txt"],
        "totals": {"web": len(web), "mt": len(oshb), "equal": len(web) == len(oshb)},
        "rule": {
            "identity_outside_the_zones": True,
            "zones": [
                {"what": "the three verses WEB prints as Dan 4:1-3 are printed by MT as Dan 3:31-33",
                 "mt_3_31_to_33": "= WEB 4:1-3", "mt_4_1_to_34": "= WEB 4:4-37",
                 "web_chapter_3_verses": 30, "mt_chapter_3_verses": 33,
                 "web_chapter_4_verses": 37, "mt_chapter_4_verses": 34},
                {"what": "the verse WEB prints as Dan 5:31 is printed by MT as Dan 6:1",
                 "mt_6_1": "= WEB 5:31", "mt_6_2_to_29": "= WEB 6:1-28",
                 "web_chapter_5_verses": 31, "mt_chapter_5_verses": 30,
                 "web_chapter_6_verses": 28, "mt_chapter_6_verses": 29}],
            "shift_not_gap": "totals are equal at 357; nothing is added or missing, two chapter breaks move",
            "tier0_disclosure": ("any structured ref touching WEB 4:1-37, WEB 5:31, WEB ch 6, MT 3:31-33, MT ch 4 or "
                                 "MT ch 6 MUST carry an explicit dual or numeric qualifier; bare coordinates are "
                                 "ambiguous there and only there"),
        },
        "zone_pairs": zone_pairs,
        "kjv_variance_crosscheck": kx,
        "verification": {"problems": problems,
                         "checks": ["every WEB verse maps to an existing MT verse and round-trips",
                                    "every MT verse maps to an existing WEB verse and round-trips",
                                    "the map is injective - no two WEB verses share an MT verse",
                                    "every OSHB KJV-variance note agrees with the map"],
                         "verdict": "GREEN" if not problems else "RED"},
    }
    (SP / "web_mt_offset_map.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                                               encoding="utf-8", newline="\n")

    check = {"schema": "m8_web_mt_verse_check.v1", "book": BOOK,
             "per_chapter": {str(c): {"web": count(web, c), "mt": count(oshb, c)} for c in CHAPTERS},
             "divergent_chapters": [c for c in CHAPTERS if count(web, c) != count(oshb, c)],
             "verdict": "GREEN" if not problems else "RED"}
    (SP / "web_mt_verse_check.json").write_text(json.dumps(check, ensure_ascii=False, indent=1) + "\n",
                                                encoding="utf-8", newline="\n")

    print(json.dumps({"web_verses": len(web), "mt_verses": len(oshb),
                      "divergent_chapters": check["divergent_chapters"],
                      "kjv_notes": kx["notes"], "kjv_notes_inside_zones": kx["notes_inside_zones"],
                      "kjv_disagreements": kx["disagreements"][:5],
                      "zone_pairs": [(p["web"], p["mt"], p["web_text_head"], p["mt_text_head"]) for p in zone_pairs],
                      "problems": problems[:10], "verdict": out["verification"]["verdict"]},
                     ensure_ascii=False, indent=1))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
