#!/usr/bin/env python3
"""Shared library for the Dan verification toolkit (Tier-0, deterministic).

Every agent brief points here. USE these tools; do NOT rebuild them.

EVERY FACT IN THIS DOCSTRING IS ASSERTED BY _selftest() BELOW against the verified Phase-0 artifacts. Run
`python dan_lib.py`: it exits non-zero if any statement here has drifted from the data. Explanatory prose has
repeatedly carried false claims that no sweep checked, so this library does not ask to be believed.

LINEAGE. Adapted from Ezek/tools/ezek_lib.py. The book-neutral functions (nfd through kq_split_bytes) are copied
from it with exact-count substitutions only: the book token, the zone chapters, the pmarks file name, the
parashah-tier wording, and the Daniel facts re-measured for the docstrings. The header, the crosswalk, the
language layer and _selftest are Daniel's own.

NUMBERING - two offset zones, pure renumbering, NO split verse:
    MT 3:31-33  = WEB 4:1-3        MT 4:1-34  = WEB 4:4-37
    MT 6:1      = WEB 5:31         MT 6:2-29  = WEB 6:1-28
Identity in every other chapter; 12 chapters; totals WEB 357 / MT 357. web_to_mt() is INJECTIVE. The crosswalk
functions are RANGE-GUARDED; always use them, never hand-assume, in BOTH directions. mt_to_web_all() exists for API
parity with split-bearing books and always returns exactly one ref here. There is no title pseudo-verse: no Dan.N.0
key exists in either extract.

MT_LAST_VERSE and PSALM_RULES are SYNTHESIZED in memory from ../web_mt_verse_check.json. PSALM_RULES keeps its
historical name because the lineage tools test only rule != "identity"; chapters 3, 4, 5 and 6 carry rule "zone".

LANGUAGE - one Aramaic island with a MID-VERSE entry (../dan_language_zones.json, EXTRACTED from the OSHB morph
codes, main-text words only):
    Hebrew   MT 1:1 word 1  - MT 2:4 word 4     (345 words)
    Aramaic  MT 2:4 word 5  - MT 7:28 word 16   (3599 words)
    Hebrew   MT 8:1 word 1  - MT 12:13 word 8   (1975 words)
MT 2:4 is the ONLY mixed verse: 12 words, 4 Hebrew then 8 Aramaic, the switch falling before word 5. 199 verses are
wholly Aramaic (MT 2:5-7:28) and 157 wholly Hebrew. The island sits entirely inside chapters 2-7 and both numbering
zones sit inside it, so language_of() gives the same answer in WEB and in MT coordinates for every verse of either
witness. A verse-granular tool CANNOT express the 2:4 boundary; MIXED_VERSES carries it and every tool that cites
2:4 must say which half it means (2:4a Hebrew, 2:4b Aramaic). Apparatus notes carry words of their own (103 A, 13
H); they are outside the zone map.

APPARATUS (MT-keyed, from ../pmarks_Dan.json): parashah 8 SAMEKH + 22 PE over 30 verses, none carrying two; paseq 44
over 40 verses, COUNT-ONLY, with MT 4:15, 6:27, 9:18 and 9:19 carrying two each; K/Q 116 notes over 80 verses, 27
carrying more than one and none more than four; 21 K/Q verses and 5 mark-bearing verses sit inside the MT
numbering zones. The OSHB also carries 66 KJV-variance notes, all inside the zones and all agreeing with the
crosswalk. No puncta extraordinaria (U+05C4, U+05C5), no selah, no special-letter seg of any class.

K/Q SPLITTING: the OSHB note layer concatenates ketiv and qere with NO delimiter. kq_split() separates them
identically for every lane: the ketiv is the unpointed lead, the qere starts at the first letter carrying a mark.
That rule alone is WRONG once in this book, at MT 1:4, so the split backs off letter by letter until the ketiv is
found in the verse's consonantal text. Over all 116 notes: 115 first-marked, 1 backtrack (MT 1:4), all lossless,
none unanchored.

SKELETON NOTE: skeleton() maps maqaf to SPACE so consonantal sweeps are maqaf-agnostic. The staged extract is
MAQAF-FREE (0 x U+05BE); the OSHB XML carries 646 x-maqqef segs, all serialized to spaces. accent_stripped retains
meteg (U+05BD) and strips cantillation (U+0591-U+05AF) only. Final-letter allography is preserved exactly.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent          # SP/Dan
BOOK = "Dan"

_inv = json.loads((SPBOOK / "verse_inventory.json").read_text(encoding="utf-8"))
LAST_VERSE = {int(c): n for c, n in _inv["chapters"].items()}
TOTAL_VERSES = sum(LAST_VERSE.values())          # 357

_check = json.loads((SPBOOK / "web_mt_verse_check.json").read_text(encoding="utf-8"))
MT_LAST_VERSE = {int(c): p["mt"] for c, p in _check["per_chapter"].items()}
MT_TOTAL_VERSES = sum(MT_LAST_VERSE.values())    # 357

ZONE_CHAPTERS = {3, 4, 5, 6}
PSALM_RULES = {c: {"rule": ("zone" if c in ZONE_CHAPTERS else "identity"),
                   "web_verses": LAST_VERSE[c], "mt_verses": MT_LAST_VERSE[c]}
               for c in sorted(LAST_VERSE)}

HEB_RUN = re.compile("[֑-״]+(?:[ ־][֑-״]+)*")
POINTS = re.compile("[֑-ׇ]")          # cantillation + vowels + meteg + puncta etc.
ACCENTS = re.compile("[֑-֯]")          # cantillation only (meteg RETAINED)
REF = re.compile(r"\bDan\.(\d+)\.(\d+)\b")

# API parity with prior books' toolsets: Dan has NO split verse.
SPLIT_MT = None
SPLIT_WEB: list = []

_zones = json.loads((SPBOOK / "dan_language_zones.json").read_text(encoding="utf-8"))
# MT-keyed from the zone map; the same pairs in WEB space because the island contains both numbering zones.
ARAMAIC_VERSES = {tuple(int(x) for x in k.split(".")[1:]) for k, lang in _zones["verse_language"].items() if lang == "A"}
MIXED_VERSES = {tuple(int(x) for x in m["ref"].split(".")[1:]): {"words": m["words"], "sequence": m["sequence"],
                                                                "switch_before_word": m["switch_before_word"]}
                for m in _zones["mixed_verses"]}


def web_to_mt(ch: int, v: int) -> tuple[int, int] | None:
    """WEB (ch, v) -> MT (ch, v). Range-guarded: None if out of range. INJECTIVE in Dan."""
    if ch not in LAST_VERSE or not (1 <= v <= LAST_VERSE[ch]):
        return None
    if ch == 4 and v <= 3:
        return (3, v + 30)
    if ch == 4:
        return (4, v - 3)
    if ch == 5 and v == 31:
        return (6, 1)
    if ch == 6:
        return (6, v + 1)
    return (ch, v)


def mt_to_web(ch: int, v: int) -> tuple[int, int] | None:
    """MT (ch, v) -> the WEB counterpart (exactly one in Dan). Range-guarded."""
    if ch not in MT_LAST_VERSE or not (1 <= v <= MT_LAST_VERSE[ch]):
        return None
    if ch == 3 and v >= 31:
        return (4, v - 30)
    if ch == 4:
        return (4, v + 3)
    if ch == 6 and v == 1:
        return (5, 31)
    if ch == 6:
        return (6, v - 1)
    return (ch, v)


def mt_to_web_all(ch: int, v: int) -> list[tuple[int, int]]:
    """EVERY WEB verse an MT verse maps to - exactly one everywhere in Dan (API parity)."""
    w = mt_to_web(ch, v)
    return [w] if w else []


def language_of(ch: int, v: int) -> str:
    """'Hebrew', 'Aramaic', or 'mixed' (MT/WEB 2:4 only). Numbering-invariant: the same answer in WEB and MT
    coordinates, asserted over every verse of both witnesses. For 2:4 read MIXED_VERSES, never guess a half."""
    if (ch, v) in MIXED_VERSES:
        return "mixed"
    return "Aramaic" if (ch, v) in ARAMAIC_VERSES or (ch == 2 and v >= 5) or 3 <= ch <= 7 else "Hebrew"


def nfd(s: str) -> str:
    return unicodedata.normalize("NFD", s)


def strip_accents(s: str) -> str:
    return ACCENTS.sub("", nfd(s))


def skeleton(s: str) -> str:
    """Consonantal skeleton; maqaf becomes SPACE so consonantal sweeps are maqaf-agnostic. Final letters kept."""
    return POINTS.sub("", nfd(s)).replace("־", " ")


def expand_ref_token(tok: str, last_verse: dict[int, int] | None = None) -> list[tuple[int, int]]:
    """'Dan.2.7' or 'Dan.2.7-Dan.3.5' or 'Dan.8.1-14' -> [(c,v), ...].
    NON-IDENTITY BOOK: WEB and MT are DIFFERENT ref spaces in chs 3-6. The default space is WEB; pass
    last_verse=MT_LAST_VERSE for oshb: refs. The expansion never converts between spaces - use
    web_to_mt()/mt_to_web() per verse for that."""
    lv = last_verse or LAST_VERSE
    tok = tok.strip()
    m = re.match(r"^Dan\.(\d+)\.(\d+)(?:-(?:Dan\.)?(\d+)(?:\.(\d+))?)?$", tok)
    if not m:
        return []
    c1, v1 = int(m.group(1)), int(m.group(2))
    if m.group(3) is None:
        return [(c1, v1)]
    if m.group(4) is None:                     # Dan.8.1-14 (same-chapter shorthand)
        c2, v2 = c1, int(m.group(3))
    else:
        c2, v2 = int(m.group(3)), int(m.group(4))
    out = []
    for c in range(c1, c2 + 1):
        lo = v1 if c == c1 else 1
        hi = v2 if c == c2 else lv.get(c, 0)
        hi = min(hi, lv.get(c, 0))     # clamp: an invalid range END never
        lo = max(lo, 1)                # expands coverage past real verses
        out.extend((c, v) for v in range(lo, hi + 1))
    return out


def load_verse_maps():
    """verse_map_web is WEB-keyed; verse_map_oshb is MT-keyed. The key spaces DIVERGE in chs 3-6 - always use
    each entry's back-reference or the crosswalk functions, never bare same-number assumptions."""
    web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
    oshb = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
    return web, oshb


def load_pmarks() -> dict:
    """MT-keyed inventories (see the module docstring for the asserted counts). Parashah marks are TIER-3 WEAK
    corroboration under the owner addendum, as in both the Prophets and the Writings - never a driver, single-witness disclosure on every
    citation, PE never conflated with SAMEKH, absence never counterevidence. Keys are MT refs: map WEB spans
    through web_to_mt() before lookups.

    API parity with jer_lib: the Jer tools read pm["paseq"] as a dict {MT ref: count}. pmarks_Dan.json stores it
    as a list with one entry per occurrence (MT 4:15 appears twice), so it is converted here, losslessly, and the
    file on disk is never changed."""
    pm = json.loads((SPBOOK / "pmarks_Dan.json").read_text(encoding="utf-8"))
    if isinstance(pm.get("paseq"), list):
        counts: dict[str, int] = {}
        for ref in pm["paseq"]:
            counts[ref] = counts.get(ref, 0) + 1
        pm["paseq"] = counts
    return pm


def norm_english(s: str) -> str:
    """Normalize English for quote comparison: typographic quotes/apostrophes/dashes to ASCII, footnote markers removed
    (the Dan extract writes a bare [fn] at all 10 sites; the [fn ...] form of earlier extracts is removed too),
    whitespace collapsed."""
    s = re.sub(r"\[fn(?: [^\]]*)?\]", " ", s)
    s = (s.replace("“", '"').replace("”", '"')
           .replace("‘", "'").replace("’", "'")
           .replace("—", "-").replace("–", "-"))
    s = re.sub(r"\s+", " ", s)
    return s.strip()


HEB_LETTER = re.compile("[\u05d0-\u05ea\u05f0-\u05f2]")


def is_mark(ch: str) -> bool:
    """A combining mark (Unicode Mn): points, accents, dagesh, the shin and sin dots, U+05C4. Maqaf, paseq and sof pasuq
    are not marks."""
    return unicodedata.category(ch) == "Mn"


def is_letter(ch: str) -> bool:
    return bool(HEB_LETTER.match(ch))


def bounded_find(hay: str, needle: str, pos: int = 0, marks: bool = True) -> int:
    """The first index >= pos where needle occurs in hay on word boundaries (S1-07; Ezekiel's ezek_controlling_rulings_a1#e4 ruling
    TOOLFIX-2 (b)). With marks=True (the byte, nfd and accent_stripped tiers) the match is neither preceded nor followed by a
    Hebrew letter or a combining mark; with marks=False (the skeleton tier) it is neither preceded nor followed by a Hebrew
    letter. -1 when there is none."""
    if not needle:
        return -1
    edge = (lambda ch: is_letter(ch) or is_mark(ch)) if marks else is_letter
    i = hay.find(needle, pos)
    while i != -1:
        j = i + len(needle)
        if (i == 0 or not edge(hay[i - 1])) and (j >= len(hay) or not edge(hay[j])):
            return i
        i = hay.find(needle, i + 1)
    return -1


def bounded_in(needle: str, hay: str, marks: bool = True) -> bool:
    return bounded_find(hay, needle, 0, marks) != -1


def collate_hebrew(quoted: str, source_text: str) -> str:
    """Return the strongest matching tier of quoted against source_text:
    'byte' | 'nfd' | 'accent_stripped' | 'skeleton' | 'none'. Ellipsis-aware: fragments must match IN ORDER. Every fragment
    matches on word boundaries (bounded_find): no Hebrew letter or combining mark beside it at the byte, nfd and
    accent_stripped tiers, no Hebrew letter beside it at the skeleton tier (S1-07)."""
    frags = [f.strip() for f in re.split(r"…|\.\.\.", quoted) if f.strip()]
    if not frags:
        return "none"

    def ordered(hay: str, needles: list[str], marks: bool) -> bool:
        pos = 0
        for n in needles:
            i = bounded_find(hay, n, pos, marks)
            if i < 0:
                return False
            pos = i + len(n)
        return True

    for tier, xf in (("byte", lambda s: s),
                     ("nfd", nfd),
                     ("accent_stripped", strip_accents),
                     ("skeleton", skeleton)):
        if ordered(xf(source_text), [xf(f) for f in frags], tier != "skeleton"):
            return tier
    return "none"


def web_quote_found(quoted: str, verse_texts: list[str]) -> bool:
    """Ellipsis-aware verbatim membership of an English quote in folded WEB text."""
    hay = norm_english(" ".join(verse_texts))
    frags = [norm_english(f) for f in re.split(r"…|\.\.\.", quoted)]
    frags = [f for f in frags if f]
    pos = 0
    for f in frags:
        i = hay.find(f, pos)
        if i < 0:
            return False
        pos = i + len(f)
    return True



_LETTER = re.compile("[\u05D0-\u05EA]")


def kq_split(note: str, verse_text: str) -> tuple[str, str, str]:
    """Split one OSHB K/Q note into (ketiv, qere, method). The note concatenates the unpointed ketiv and the pointed
    qere with no delimiter. The qere normally starts at the first letter that carries a mark; where the ketiv that
    split implies is not found in the verse's consonantal text, the split backs off one letter at a time until it is
    (MT 1:4 is the one such case in Daniel). method is 'first_marked', 'verse_anchored_backtrack', 'ketiv_only', or
    'UNANCHORED' - the last is returned rather than guessed, with empty strings, and must be treated as unsplittable.
    Morpheme separators '/' are preserved in both halves; strip them when quoting."""
    s = nfd(note)
    first_mark = next((i for i, ch in enumerate(s) if POINTS.match(ch)), None)
    if first_mark is None:
        return s, "", "ketiv_only"
    letters = [i for i, ch in enumerate(s) if _LETTER.match(ch)]
    owners = [i for i in letters if i < first_mark]
    if not owners:
        return "", "", "UNANCHORED"
    owner = max(owners)
    vsk = skeleton(verse_text).replace(" ", "")

    def cons(x: str) -> str:
        return skeleton(x).replace("/", "").replace(" ", "")

    for n, sp in enumerate(sorted((i for i in letters if 0 < i <= owner), reverse=True)):
        k = s[:sp]
        if cons(k) and cons(k) in vsk and POINTS.search(s[sp:]):
            return k, s[sp:], ("first_marked" if n == 0 else "verse_anchored_backtrack")
    return "", "", "UNANCHORED"

def kq_split_bytes(note: str, verse_text: str) -> tuple[str, str, str]:
    """kq_split, returned in the note's RAW bytes (D3). kq_split works on nfd(note), but 59 of the 116 stored notes keep a
    non-canonical mark order, and a Qere quoted 'with its note bytes exactly' carries THOSE bytes. The split falls on a
    base letter, and canonical reordering never moves a mark across a base letter, so kq_split's character offset
    splits the raw note. Verified on every call: a mismatch returns UNANCHORED rather than a guess."""
    k, q, method = kq_split(note, verse_text)
    if method == "UNANCHORED":
        return "", "", method
    k_raw, q_raw = note[:len(k)], note[len(k):]
    if nfd(k_raw) != k or nfd(q_raw) != q:
        return "", "", "UNANCHORED"
    return k_raw, q_raw, method


def _selftest() -> int:
    """Assert every fact in the module docstring against the verified artifacts. Exit non-zero on any drift."""
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    pm = load_pmarks()
    raw_pm = json.loads((SPBOOK / "pmarks_Dan.json").read_text(encoding="utf-8"))
    omap = json.loads((SPBOOK / "web_mt_offset_map.json").read_text(encoding="utf-8"))
    oshb = dict(l.split("\t", 1) for l in (SPBOOK / "Dan_oshb.txt").read_text(encoding="utf-8").splitlines())
    web_clean = (SPBOOK / "Dan_web_clean.txt").read_text(encoding="utf-8")
    joined = "".join(oshb.values())
    checks = []

    def mt(key):
        return tuple(int(x) for x in key.split(".")[1:])

    def in_mt_zone(c, v):
        return (c == 3 and v >= 31) or c in (4, 6)

    # ---- numbering ----
    checks.append(("12 chapters in both witnesses", len(LAST_VERSE) == 12 and len(MT_LAST_VERSE) == 12))
    checks.append(("totals 357 / 357", TOTAL_VERSES == 357 and MT_TOTAL_VERSES == 357 and len(oshb) == 357))
    checks.append(("non-identity chapters are exactly 3, 4, 5 and 6",
                   {c for c in LAST_VERSE if LAST_VERSE[c] != MT_LAST_VERSE[c]} == ZONE_CHAPTERS))
    bij = all((m := web_to_mt(c, v)) is not None and mt_to_web(*m) == (c, v) and mt_to_web_all(*m) == [(c, v)]
              for c in LAST_VERSE for v in range(1, LAST_VERSE[c] + 1))
    checks.append(("crosswalk round-trips every WEB verse", bij))
    images = [web_to_mt(c, v) for c in LAST_VERSE for v in range(1, LAST_VERSE[c] + 1)]
    checks.append(("web_to_mt is injective and onto the MT extract",
                   len(images) == len(set(images)) == 357 and {"Dan.%d.%d" % i for i in images} == set(oshb)))
    checks.append(("WEB 4:1-3 = MT 3:31-33", [web_to_mt(4, v) for v in (1, 2, 3)] == [(3, 31), (3, 32), (3, 33)]))
    checks.append(("WEB 4:4-37 = MT 4:1-34", [web_to_mt(4, v) for v in range(4, 38)] == [(4, i) for i in range(1, 35)]))
    checks.append(("WEB 5:31 = MT 6:1", web_to_mt(5, 31) == (6, 1) and mt_to_web(6, 1) == (5, 31)))
    checks.append(("WEB 6:1-28 = MT 6:2-29", [web_to_mt(6, v) for v in range(1, 29)] == [(6, i) for i in range(2, 30)]))
    checks.append(("out-of-range refs return None",
                   web_to_mt(3, 31) is None and mt_to_web(4, 35) is None and mt_to_web(5, 31) is None
                   and web_to_mt(13, 1) is None and web_to_mt(1, 0) is None and mt_to_web(3, 34) is None))
    pairs_ok = all(web_to_mt(*mt(p["web"].split(":", 1)[1])) == mt(p["mt"].split(":", 1)[1]) for p in omap["zone_pairs"])
    checks.append(("agrees with every zone pair in the verified offset map",
                   pairs_ok and len(omap["zone_pairs"]) == 8 and omap["verification"]["verdict"] == "GREEN"))
    kx = omap["kjv_variance_crosscheck"]
    checks.append(("OSHB KJV-variance layer: 66 notes, all inside the zones, 0 disagreements",
                   kx["notes"] == 66 and kx["notes_inside_zones"] == 66 and kx["disagreements"] == []
                   and len(raw_pm["kjv_variance"]) == 66))
    checks.append(("every KJV-variance note agrees with this crosswalk",
                   all(mt_to_web(*mt(k)) == mt(e) for k, e in raw_pm["kjv_variance"].items())))
    checks.append(("no Dan.N.0 key in the MT extract", all(int(k.split(".")[2]) >= 1 for k in oshb)))

    # ---- language ----
    vl = _zones["verse_language"]
    island = {(2, v) for v in range(5, MT_LAST_VERSE[2] + 1)} | {(c, v) for c in range(3, 8)
                                                                  for v in range(1, MT_LAST_VERSE[c] + 1)}
    checks.append(("199 wholly Aramaic verses, exactly MT 2:5-7:28", ARAMAIC_VERSES == island and len(island) == 199))
    checks.append(("157 wholly Hebrew verses and one mixed verse",
                   sum(1 for x in vl.values() if x == "H") == 157 and [k for k, x in vl.items() if x == "mixed"] == ["Dan.2.4"]))
    checks.append(("MT 2:4 is 12 words, 4 H then 8 A, switch before word 5",
                   MIXED_VERSES == {(2, 4): {"words": 12, "sequence": "HHHHAAAAAAAA", "switch_before_word": [5]}}))
    runs = [(r["lang"], r["start"], r["end"], r["words"]) for r in _zones["runs"]]
    checks.append(("three runs: H 1:1w1-2:4w4 (345), A 2:4w5-7:28w16 (3599), H 8:1w1-12:13w8 (1975)",
                   runs == [("H", "Dan.1.1 w1", "Dan.2.4 w4", 345), ("A", "Dan.2.4 w5", "Dan.7.28 w16", 3599),
                            ("H", "Dan.8.1 w1", "Dan.12.13 w8", 1975)]))
    checks.append(("main-text word totals A 3599 / H 2320; note words A 103 / H 13",
                   _zones["word_totals"] == {"H": 2320, "A": 3599} and _zones["note_word_totals"] == {"A": 103, "H": 13}))
    checks.append(("pmarks morph tally including notes = main text + notes exactly",
                   raw_pm["morph_prefix_tally_including_note_words"] == {"H": 2320 + 13, "A": 3599 + 103}))
    checks.append(("language_of agrees with the zone map on every MT verse",
                   all(language_of(*mt(k)) == {"H": "Hebrew", "A": "Aramaic", "mixed": "mixed"}[x] for k, x in vl.items())))
    checks.append(("language_of is numbering-invariant over every WEB verse",
                   all(language_of(c, v) == language_of(*web_to_mt(c, v))
                       for c in LAST_VERSE for v in range(1, LAST_VERSE[c] + 1))))
    checks.append(("both numbering zones sit inside the island",
                   all(language_of(c, v) == "Aramaic" for c in ZONE_CHAPTERS for v in range(1, LAST_VERSE[c] + 1))))

    # ---- apparatus ----
    checks.append(("parashah 8 SAMEKH + 22 PE over 30 verses, none carrying two",
                   pm["marks_tally"] == {"SAMEKH": 8, "PE": 22, "REVERSED_NUN": 0, "verses_carrying_a_mark": 30}
                   and all(len(v) == 1 for v in pm["marks"].values())
                   and raw_pm["arithmetic"]["verses_with_more_than_one_mark"] == {}))
    checks.append(("paseq 44 over 40 verses", pm["paseq_tally"] == {"occurrences": 44, "verses": 40}))
    checks.append(("REGRESSION load_pmarks gives paseq as {ref: count} (Jer tool contract), lossless vs the stored list",
                   isinstance(pm["paseq"], dict) and sum(pm["paseq"].values()) == len(raw_pm["paseq"]) == 44
                   and len(pm["paseq"]) == 40
                   and sorted(k for k, n in pm["paseq"].items() if n > 1) == ["Dan.4.15", "Dan.6.27", "Dan.9.18", "Dan.9.19"]
                   and all(n <= 2 for n in pm["paseq"].values())))
    checks.append(("K/Q 116 notes over 80 verses, 27 carrying more than one, none more than four",
                   pm["kq_tally"] == {"verses": 80, "notes": 116}
                   and sum(1 for v in pm["kq"].values() if len(v) > 1) == 27
                   and max(len(v) for v in pm["kq"].values()) == 4))
    checks.append(("21 K/Q verses and 5 mark-bearing verses sit inside the MT numbering zones",
                   sum(1 for k in pm["kq"] if in_mt_zone(*mt(k))) == 21
                   and sorted((k for k in pm["marks"] if in_mt_zone(*mt(k))), key=mt)
                   == ["Dan.4.25", "Dan.4.34", "Dan.6.6", "Dan.6.11", "Dan.6.29"]))
    checks.append(("U+05C4 and U+05C5 do not occur", joined.count("ׄ") == 0 and joined.count("ׅ") == 0))
    checks.append(("extract is maqaf-free, paseq-free, sof-pasuq-free and separator-free",
                   all(joined.count(ch) == 0 for ch in ("־", "׀", "׃", "/"))))
    checks.append(("646 x-maqqef segs and 357 x-sof-pasuq segs in the XML; one sof pasuq per verse",
                   pm["seg_totals_in_xml"].get("x-maqqef") == 646 and pm["seg_totals_in_xml"].get("x-sof-pasuq") == 357
                   and raw_pm["arithmetic"]["sof_pasuq_absent_verses"] == []))
    checks.append(("no special-letter seg of any class: other_segs empty, XML seg types paseq/maqqef/sof-pasuq/samekh/pe only",
                   pm["other_segs"] == {}
                   and set(pm["seg_totals_in_xml"]) == {"x-paseq", "x-maqqef", "x-sof-pasuq", "x-samekh", "x-pe"}))
    bare_mt = "\n".join(re.sub(r"[֑-ׇ]", "", t) for t in oshb.values())
    checks.append(("selah occurs in neither witness",
                   not re.search(r"\bSelah\b", web_clean, flags=re.I)
                   and not re.search(r"(?<![א-ת])סלה(?![א-ת])", bare_mt)))
    checks.append(("REGRESSION norm_english strips the bare [fn] marker (10 sites) and the [fn ...] form",
                   web_clean.count("[fn]") == 10 and len(re.findall(r"\[fn", web_clean)) == 10
                   and norm_english("Yahweh’s[fn] word") == "Yahweh's word"
                   and norm_english("a[fn note text] b") == "a b" and "[fn" not in norm_english(web_clean)))
    checks.append(("WEB 2:4 names the language 'Syrian', which the language guard's label pattern covers",
                   "in the Syrian language" in web_clean))
    checks.append(("collate_hebrew returns byte for a verbatim verse",
                   collate_hebrew(oshb["Dan.1.1"], " | ".join(oshb.values())) == "byte"))
    checks.append(("expand_ref_token clamps to real verses in WEB space and in MT space",
                   expand_ref_token("Dan.3.29-Dan.4.2") == [(3, 29), (3, 30), (4, 1), (4, 2)]
                   and expand_ref_token("Dan.3.29-Dan.4.2", MT_LAST_VERSE)
                   == [(3, 29), (3, 30), (3, 31), (3, 32), (3, 33), (4, 1), (4, 2)]
                   and expand_ref_token("Dan.5.30-40") == [(5, 30), (5, 31)]))

    # ---- K/Q splitting ----
    kq_methods, kq_lossless = {}, True
    for ref, notes in pm["kq"].items():
        for note in notes:
            k, q, m = kq_split(note, oshb.get(ref, ""))
            kq_methods[m] = kq_methods.get(m, 0) + 1
            if m == "UNANCHORED" or nfd(note) != k + q:
                kq_lossless = False
    checks.append(("kq_split resolves all 116 notes losslessly, none UNANCHORED",
                   kq_lossless and sum(kq_methods.values()) == 116 and "UNANCHORED" not in kq_methods))
    checks.append(("kq_split methods: 115 first_marked, 1 backtrack", kq_methods == {"first_marked": 115,
                                                                                     "verse_anchored_backtrack": 1}))
    back = [ref for ref, notes in pm["kq"].items() for n in notes
            if kq_split(n, oshb[ref])[2] == "verse_anchored_backtrack"]
    k, q, m = kq_split(pm["kq"]["Dan.1.4"][0], oshb["Dan.1.4"])
    checks.append(("REGRESSION MT 1:4 is the one backtrack, and its ketiv is found in the verse's consonants",
                   back == ["Dan.1.4"] and m == "verse_anchored_backtrack"
                   and skeleton(k).replace(" ", "") in skeleton(oshb["Dan.1.4"]).replace(" ", "")
                   and bool(POINTS.search(q))))
    raw_ok, raw_methods_same, noncanonical = True, True, 0
    for ref, notes in pm["kq"].items():
        for note in notes:
            kb, qb, mb = kq_split_bytes(note, oshb.get(ref, ""))
            _k, _q, mn = kq_split(note, oshb.get(ref, ""))
            raw_ok = raw_ok and mb != "UNANCHORED" and kb + qb == note
            raw_methods_same = raw_methods_same and mb == mn
            noncanonical += note != unicodedata.normalize("NFC", note)
    checks.append(("REGRESSION D3 kq_split_bytes splits all 116 notes losslessly in RAW bytes, same methods as kq_split",
                   raw_ok and raw_methods_same))
    checks.append(("REGRESSION D3 59 of the 116 stored notes keep a non-canonical mark order", noncanonical == 59))

    # S1-07 word boundaries. Every case is found in the bytes, never typed.
    def _cases():
        found = {}
        for key in sorted(oshb, key=mt):
            verse = oshb[key]
            for w in verse.split(" "):
                letters = [i for i, ch in enumerate(w) if is_letter(ch)]
                if len(letters) < 4:
                    continue
                if "end" not in found and is_mark(w[-1]):
                    k = len(w)
                    while k and is_mark(w[k - 1]):
                        k -= 1
                    if not bounded_in(w[:k], verse):
                        found["end"] = (verse, w, w[:k])
                if "shin" not in found and "שׁ" in w[-4:]:
                    k = w.rfind("ׁ")
                    if not bounded_in(w[:k], verse) and w[:k]:
                        found["shin"] = (verse, w, w[:k])
                if "start" not in found:
                    rest = w[letters[1]:]
                    if not bounded_in(rest, verse):
                        found["start"] = (verse, w, rest)
                if "root" not in found:
                    sk = skeleton(w).replace(" ", "")
                    inner = sk[1:-1]
                    if len(inner) >= 3 and not bounded_in(inner, skeleton(verse), marks=False):
                        found["root"] = (verse, w, inner)
                if len(found) == 4:
                    return found
        return found
    cases = _cases()
    checks.append(("REGRESSION S1-07 a splice cut before its word's final marks is not byte; the whole word is",
                   "end" in cases and collate_hebrew(cases["end"][2], cases["end"][0]) != "byte"
                   and collate_hebrew(cases["end"][1], cases["end"][0]) == "byte"))
    checks.append(("REGRESSION S1-07 a shin written without its shin dot is not byte",
                   "shin" in cases and collate_hebrew(cases["shin"][2], cases["shin"][0]) != "byte"))
    checks.append(("S1-07 a quote that begins inside a word (its first letter dropped) is not byte",
                   "start" in cases and collate_hebrew(cases["start"][2], cases["start"][0]) != "byte"))
    checks.append(("S1-07 an unpointed root inside a longer word does not collate at skeleton tier",
                   "root" in cases and collate_hebrew(cases["root"][2], cases["root"][0]) == "none"))
    w11 = oshb["Dan.1.1"].split(" ")
    checks.append(("S1-07 whole words, an ellipsis of whole words, and an unpointed whole word still collate",
                   collate_hebrew(w11[1], oshb["Dan.1.1"]) == "byte"
                   and collate_hebrew(w11[1] + " … " + w11[3], oshb["Dan.1.1"]) == "byte"
                   and collate_hebrew(skeleton(w11[1]), oshb["Dan.1.1"]) == "skeleton"))
    checks.append(("S1-07 skeleton() keeps word spaces (the word boundary depends on it)", " " in skeleton(oshb["Dan.1.1"])))

    failed = [n for n, ok in checks if not ok]
    print(json.dumps({"module": "dan_lib", "checks": len(checks), "passed": len(checks) - len(failed),
                      "failed": failed, "verdict": "GREEN" if not failed else "RED"}, ensure_ascii=False, indent=1))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(_selftest())
