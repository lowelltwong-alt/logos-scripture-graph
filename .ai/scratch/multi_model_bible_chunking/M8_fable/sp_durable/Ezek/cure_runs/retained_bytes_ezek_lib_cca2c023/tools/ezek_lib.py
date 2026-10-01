#!/usr/bin/env python3
"""Shared library for the Ezek r3 verification toolkit (Tier-0, deterministic).

Every agent brief points here. USE these tools; do NOT rebuild them.

EVERY FACT IN THIS DOCSTRING IS ASSERTED BY _selftest() BELOW against the verified Phase-0 artifacts. Run
`python ezek_lib.py` - it exits non-zero if any statement here has drifted from the data. This is deliberate: the
Ezekiel cycle has repeatedly found explanatory prose carrying false claims that no sweep checked, so this library
does not ask to be believed.

NUMBERING - one offset zone, pure renumbering, NO split verse:
    MT 21:1-5    = WEB 20:45-49
    MT 21:6-37   = WEB 21:1-32
Identity in every other chapter; 48 chapters; totals WEB 1273 / MT 1273. web_to_mt() is INJECTIVE. The crosswalk
functions are RANGE-GUARDED - always use them, never hand-assume, in BOTH directions. mt_to_web_all() exists for API
parity with split-bearing books and always returns exactly one ref here. There is no title pseudo-verse: no
Ezek.N.0 key exists in either extract.

MT_LAST_VERSE and PSALM_RULES are SYNTHESIZED in memory from ../web_mt_verse_check.json (per-chapter counts in both
witnesses). The verified ../web_mt_offset_map.json is NOT modified to fit the Jeremiah-lineage schema; _selftest
cross-checks this crosswalk against that map's zone pairs instead. PSALM_RULES keeps its historical name because the
lineage tools test only rule != "identity"; chapters 20 and 21 carry rule "zone".

LANGUAGE: Hebrew throughout. ARAMAIC_VERSES is empty: the OSHB morph layer is H-prefixed on every token.

APPARATUS (MT-keyed, from ../pmarks_Ezek.json): parashah 113 SAMEKH + 71 PE = 184 occurrences over 183 verses (MT
43:27 carries two); paseq 136 over 121 verses, COUNT-ONLY; K/Q 134 notes over 99 verses, 23 doubled. Special marks:
puncta extraordinaria (U+05C4) stand IN THE VERSE BYTES at MT 41:20 (five) and MT 46:22 (seven), nowhere else, and
U+05C5 does not occur. No selah, no large or small letters, no reversed or suspended nun.

K/Q SPLITTING: the OSHB note layer concatenates ketiv and qere with NO delimiter. kq_split() separates them
identically for every lane: the ketiv is the unpointed lead, the qere starts at the first letter carrying a mark.
That rule alone is WRONG once in this book - at MT 41:8 the qere's first letter carries no mark (its vowel sits on
the following vav) - so the split backs off letter by letter until the ketiv is found in the verse's consonantal
text. Over all 134 notes: 132 first-marked, 1 backtrack (MT 41:8), 1 ketiv-only (MT 48:16), all lossless, none
unanchored. Writers in the first wave split these by hand in different ways, and one declined to quote any Qere;
this function exists so that never recurs.

SKELETON NOTE: skeleton() maps maqaf to SPACE so consonantal sweeps are maqaf-agnostic. The staged extract is
MAQAF-FREE (0 x U+05BE); the OSHB XML carries 2352 x-maqqef segs, all serialized to spaces. POINTS spans
U+0591-U+05C7 and therefore strips U+05C4 at the skeleton tier - the byte tier keeps it. accent_stripped retains
meteg (U+05BD) and strips cantillation (U+0591-U+05AF) only. Final-letter allography is preserved exactly.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent          # SP/Ezek
BOOK = "Ezek"

_inv = json.loads((SPBOOK / "verse_inventory.json").read_text(encoding="utf-8"))
LAST_VERSE = {int(c): n for c, n in _inv["chapters"].items()}
TOTAL_VERSES = sum(LAST_VERSE.values())          # 1273

_check = json.loads((SPBOOK / "web_mt_verse_check.json").read_text(encoding="utf-8"))
MT_LAST_VERSE = {int(c): p["mt"] for c, p in _check["per_chapter"].items()}
MT_TOTAL_VERSES = sum(MT_LAST_VERSE.values())    # 1273

ZONE_CHAPTERS = {20, 21}
PSALM_RULES = {c: {"rule": ("zone" if c in ZONE_CHAPTERS else "identity"),
                   "web_verses": LAST_VERSE[c], "mt_verses": MT_LAST_VERSE[c]}
               for c in sorted(LAST_VERSE)}

HEB_RUN = re.compile("[֑-״]+(?:[ ־][֑-״]+)*")
POINTS = re.compile("[֑-ׇ]")          # cantillation + vowels + meteg + puncta etc.
ACCENTS = re.compile("[֑-֯]")          # cantillation only (meteg RETAINED)
REF = re.compile(r"\bEzek\.(\d+)\.(\d+)\b")

# API parity with prior books' toolsets: Ezek has NO split verse.
SPLIT_MT = None
SPLIT_WEB: list = []

ARAMAIC_VERSES: set = set()


def web_to_mt(ch: int, v: int) -> tuple[int, int] | None:
    """WEB (ch, v) -> MT (ch, v). Range-guarded: None if out of range. INJECTIVE in Ezek."""
    if ch not in LAST_VERSE or not (1 <= v <= LAST_VERSE[ch]):
        return None
    if ch == 20 and v >= 45:
        return (21, v - 44)
    if ch == 21:
        return (21, v + 5)
    return (ch, v)


def mt_to_web(ch: int, v: int) -> tuple[int, int] | None:
    """MT (ch, v) -> the WEB counterpart (exactly one in Ezek). Range-guarded."""
    if ch not in MT_LAST_VERSE or not (1 <= v <= MT_LAST_VERSE[ch]):
        return None
    if ch == 21 and v <= 5:
        return (20, v + 44)
    if ch == 21:
        return (21, v - 5)
    return (ch, v)


def mt_to_web_all(ch: int, v: int) -> list[tuple[int, int]]:
    """EVERY WEB verse an MT verse maps to - exactly one everywhere in Ezek (API parity)."""
    w = mt_to_web(ch, v)
    return [w] if w else []


def language_of(ch: int, v: int) -> str:
    """Ezek is Hebrew throughout; ARAMAIC_VERSES is empty (asserted against the morph layer)."""
    return "Aramaic" if (ch, v) in ARAMAIC_VERSES else "Hebrew"


def nfd(s: str) -> str:
    return unicodedata.normalize("NFD", s)


def strip_accents(s: str) -> str:
    return ACCENTS.sub("", nfd(s))


def skeleton(s: str) -> str:
    """Consonantal skeleton; maqaf becomes SPACE so consonantal sweeps are maqaf-agnostic. Final letters kept."""
    return POINTS.sub("", nfd(s)).replace("־", " ")


def expand_ref_token(tok: str, last_verse: dict[int, int] | None = None) -> list[tuple[int, int]]:
    """'Ezek.2.7' or 'Ezek.2.7-Ezek.3.5' or 'Ezek.8.1-14' -> [(c,v), ...].
    NON-IDENTITY BOOK: WEB and MT are DIFFERENT ref spaces in chs 20-21. The default space is WEB; pass
    last_verse=MT_LAST_VERSE for oshb: refs. The expansion never converts between spaces - use
    web_to_mt()/mt_to_web() per verse for that."""
    lv = last_verse or LAST_VERSE
    tok = tok.strip()
    m = re.match(r"^Ezek\.(\d+)\.(\d+)(?:-(?:Ezek\.)?(\d+)(?:\.(\d+))?)?$", tok)
    if not m:
        return []
    c1, v1 = int(m.group(1)), int(m.group(2))
    if m.group(3) is None:
        return [(c1, v1)]
    if m.group(4) is None:                     # Ezek.8.1-14 (same-chapter shorthand)
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
    """verse_map_web is WEB-keyed; verse_map_oshb is MT-keyed. The key spaces DIVERGE in chs 20-21 - always use
    each entry's back-reference or the crosswalk functions, never bare same-number assumptions."""
    web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
    oshb = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
    return web, oshb


def load_pmarks() -> dict:
    """MT-keyed inventories (see the module docstring for the asserted counts). Parashah marks are TIER-3 WEAK
    corroboration in the Prophets under the owner addendum - never a driver, single-witness disclosure on every
    citation, PE never conflated with SAMEKH, absence never counterevidence. Keys are MT refs: map WEB spans
    through web_to_mt() before lookups.

    API parity with jer_lib: the Jer tools read pm["paseq"] as a dict {MT ref: count}. pmarks_Ezek.json stores it
    as a list with one entry per occurrence (MT 3:27 appears twice), so it is converted here, losslessly, and the
    file on disk is never changed."""
    pm = json.loads((SPBOOK / "pmarks_Ezek.json").read_text(encoding="utf-8"))
    if isinstance(pm.get("paseq"), list):
        counts: dict[str, int] = {}
        for ref in pm["paseq"]:
            counts[ref] = counts.get(ref, 0) + 1
        pm["paseq"] = counts
    return pm


def norm_english(s: str) -> str:
    """Normalize English for quote comparison: typographic quotes/apostrophes/dashes to ASCII, footnote markers removed
    (the Ezek extract writes a bare [fn] at all 38 sites; the [fn ...] form of earlier extracts is removed too),
    whitespace collapsed."""
    s = re.sub(r"\[fn(?: [^\]]*)?\]", " ", s)
    s = (s.replace("“", '"').replace("”", '"')
           .replace("‘", "'").replace("’", "'")
           .replace("—", "-").replace("–", "-"))
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def collate_hebrew(quoted: str, source_text: str) -> str:
    """Return the strongest matching tier of quoted against source_text:
    'byte' | 'nfd' | 'accent_stripped' | 'skeleton' | 'none'. Ellipsis-aware: fragments must match IN ORDER."""
    frags = [f.strip() for f in re.split(r"…|\.\.\.", quoted) if f.strip()]
    if not frags:
        return "none"

    def ordered(hay: str, needles: list[str]) -> bool:
        pos = 0
        for n in needles:
            i = hay.find(n, pos)
            if i < 0:
                return False
            pos = i + len(n)
        return True

    for tier, xf in (("byte", lambda s: s),
                     ("nfd", nfd),
                     ("accent_stripped", strip_accents),
                     ("skeleton", skeleton)):
        if ordered(xf(source_text), [xf(f) for f in frags]):
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
    (MT 41:8 is the one such case). method is 'first_marked', 'verse_anchored_backtrack', 'ketiv_only', or
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
    """kq_split, returned in the note's RAW bytes (D3). kq_split works on nfd(note), but 66 of the 134 stored notes keep a
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
    omap = json.loads((SPBOOK / "web_mt_offset_map.json").read_text(encoding="utf-8"))
    kjv = json.loads((SPBOOK / "ezek_kjv_variance_crosscheck.json").read_text(encoding="utf-8"))
    oshb = dict(l.split("\t", 1) for l in (SPBOOK / "Ezek_oshb.txt").read_text(encoding="utf-8").splitlines())
    joined = "".join(oshb.values())
    checks = []

    checks.append(("48 chapters in both witnesses", len(LAST_VERSE) == 48 and len(MT_LAST_VERSE) == 48))
    checks.append(("totals 1273 / 1273", TOTAL_VERSES == 1273 and MT_TOTAL_VERSES == 1273))
    checks.append(("non-identity chapters are exactly 20 and 21",
                   {c for c in LAST_VERSE if LAST_VERSE[c] != MT_LAST_VERSE[c]} == ZONE_CHAPTERS))
    bij = True
    for c in LAST_VERSE:
        for v in range(1, LAST_VERSE[c] + 1):
            m = web_to_mt(c, v)
            if m is None or mt_to_web(*m) != (c, v) or mt_to_web_all(*m) != [(c, v)]:
                bij = False
    checks.append(("crosswalk round-trips every WEB verse", bij))
    images = [web_to_mt(c, v) for c in LAST_VERSE for v in range(1, LAST_VERSE[c] + 1)]
    checks.append(("web_to_mt is injective", len(images) == len(set(images))))
    checks.append(("WEB 20:45-49 = MT 21:1-5", [web_to_mt(20, v) for v in range(45, 50)] == [(21, i) for i in range(1, 6)]))
    checks.append(("WEB 21:1-32 = MT 21:6-37", [web_to_mt(21, v) for v in range(1, 33)] == [(21, i) for i in range(6, 38)]))
    checks.append(("out-of-range refs return None", web_to_mt(8, 19) is None and mt_to_web(20, 45) is None
                   and web_to_mt(49, 1) is None and web_to_mt(1, 0) is None))
    pairs_ok = all(web_to_mt(int(p["web"].split(".")[1]), int(p["web"].split(".")[2]))
                   == (int(p["mt"].split(".")[1]), int(p["mt"].split(".")[2])) for p in omap["zone_pairs"])
    checks.append(("agrees with every zone pair in the verified offset map", pairs_ok and omap["verification"]["verdict"] == "GREEN"))
    checks.append(("OSHB KJV-variance layer 37/37 agreement on record",
                   kjv["kjv_variance_notes_found"] == 37 and kjv["agree_with_my_offset_map"] == 37))
    checks.append(("no Ezek.N.0 key in the MT extract", all(int(k.split(".")[2]) >= 1 for k in oshb)))
    checks.append(("Hebrew throughout: ARAMAIC_VERSES empty and morph H only",
                   ARAMAIC_VERSES == set() and pm["aramaic_verses"] == [] and pm["morph_prefix_tally"] == {"H": 18866}))
    checks.append(("parashah 113 SAMEKH + 71 PE over 183 verses",
                   pm["marks_tally"]["SAMEKH"] == 113 and pm["marks_tally"]["PE"] == 71
                   and pm["marks_tally"]["verses_carrying_a_mark"] == 183))
    checks.append(("MT 43:27 carries two SAMEKH", pm["marks"].get("Ezek.43.27") == ["SAMEKH", "SAMEKH"]))
    checks.append(("paseq 136 over 121 verses",
                   pm["paseq_tally"]["occurrences"] == 136 and pm["paseq_tally"]["verses"] == 121))
    raw_paseq = json.loads((SPBOOK / "pmarks_Ezek.json").read_text(encoding="utf-8"))["paseq"]
    checks.append(("REGRESSION load_pmarks gives paseq as {ref: count} (Jer tool contract), lossless vs the stored list",
                   isinstance(pm["paseq"], dict) and sum(pm["paseq"].values()) == len(raw_paseq) == 136
                   and len(pm["paseq"]) == 121 and pm["paseq"].get("Ezek.3.27") == 2))
    doubled = [k for k, v in pm["kq"].items() if len(v) > 1]
    checks.append(("K/Q 134 notes over 99 verses, 23 doubled",
                   pm["kq_tally"]["notes"] == 134 and pm["kq_tally"]["verses"] == 99 and len(doubled) == 23))
    checks.append(("U+05C4 five at MT 41:20, seven at MT 46:22, nowhere else",
                   oshb["Ezek.41.20"].count("ׄ") == 5 and oshb["Ezek.46.22"].count("ׄ") == 7
                   and sum(1 for t in oshb.values() if "ׄ" in t) == 2))
    checks.append(("U+05C5 does not occur", joined.count("ׅ") == 0))
    checks.append(("extract is maqaf-free", joined.count("־") == 0))
    checks.append(("2352 x-maqqef segs in the XML", pm["seg_totals_in_xml"].get("x-maqqef") == 2352))
    checks.append(("skeleton strips U+05C4 while the byte tier keeps it",
                   "ׄ" not in skeleton(oshb["Ezek.41.20"]) and "ׄ" in oshb["Ezek.41.20"]))
    checks.append(("collate_hebrew returns byte for a verbatim verse", collate_hebrew(oshb["Ezek.1.1"], joined) == "byte"))
    web_clean = (SPBOOK / "Ezek_web_clean.txt").read_text(encoding="utf-8")
    checks.append(("REGRESSION norm_english strips the bare [fn] marker (38 sites) and the [fn ...] form",
                   web_clean.count("[fn]") == 38 and norm_english("Yahweh’s[fn] word") == "Yahweh's word"
                   and norm_english("a[fn note text] b") == "a b" and "[fn" not in norm_english(web_clean)))

    # Facts the book-specific tools' docstrings cite, asserted here so those docstrings cannot drift from the bytes.
    bare_mt = "\n".join(re.sub(r"[֑-ׇ]", "", t) for t in oshb.values())
    checks.append(("selah occurs in neither witness",
                   not re.search(r"\bSelah\b", web_clean, flags=re.I)
                   and not re.search(r"(?<![א-ת])סלה(?![א-ת])", bare_mt)))
    checks.append(("no special-letter seg of any class: other_segs empty, XML seg types paseq/maqqef/sof-pasuq/samekh/pe only",
                   pm["other_segs"] == {}
                   and set(pm["seg_totals_in_xml"]) == {"x-paseq", "x-maqqef", "x-sof-pasuq", "x-samekh", "x-pe"}))
    checks.append(("the one K/Q verse inside the numbering zone is MT 21:28 = WEB 21:23",
                   [k for k in pm["kq"] if k.split(".")[1] == "21"] == ["Ezek.21.28"] and mt_to_web(21, 28) == (21, 23)))

    kq_methods, kq_lossless = {}, True
    for ref, notes in pm["kq"].items():
        for note in notes:
            k, q, m = kq_split(note, oshb.get(ref, ""))
            kq_methods[m] = kq_methods.get(m, 0) + 1
            if m == "UNANCHORED" or nfd(note) != k + q:
                kq_lossless = False
    checks.append(("kq_split resolves all 134 notes losslessly, none UNANCHORED",
                   kq_lossless and sum(kq_methods.values()) == 134 and "UNANCHORED" not in kq_methods))
    checks.append(("kq_split methods: 132 first_marked, 1 backtrack, 1 ketiv_only",
                   kq_methods == {"first_marked": 132, "verse_anchored_backtrack": 1, "ketiv_only": 1}))
    k, q, m = kq_split(pm["kq"]["Ezek.41.8"][0], oshb["Ezek.41.8"])
    checks.append(("REGRESSION MT 41:8 - unmarked first qere letter, split backs off",
                   skeleton(k) == "\u05de\u05d9\u05e1\u05d3\u05d5\u05ea" and m == "verse_anchored_backtrack"
                   and skeleton(q).startswith("\u05de")))
    raw_ok, raw_methods_same, noncanonical = True, True, 0
    for ref, notes in pm["kq"].items():
        for note in notes:
            kb, qb, mb = kq_split_bytes(note, oshb.get(ref, ""))
            _k, _q, mn = kq_split(note, oshb.get(ref, ""))
            raw_ok = raw_ok and mb != "UNANCHORED" and kb + qb == note
            raw_methods_same = raw_methods_same and mb == mn
            noncanonical += note != unicodedata.normalize("NFC", note)
    checks.append(("REGRESSION D3 kq_split_bytes splits all 134 notes losslessly in RAW bytes, same methods as kq_split",
                   raw_ok and raw_methods_same))
    checks.append(("REGRESSION D3 66 of the 134 stored notes keep a non-canonical mark order", noncanonical == 66))
    k, q, m = kq_split(pm["kq"]["Ezek.48.16"][0], oshb["Ezek.48.16"])
    checks.append(("MT 48:16 is ketiv-only", q == "" and m == "ketiv_only"))
    k, q, m = kq_split(pm["kq"]["Ezek.42.9"][0], oshb["Ezek.42.9"])
    checks.append(("MT 42:9 two-word ketiv splits on the first marked letter", m == "first_marked" and " " in k))

    failed = [n for n, ok in checks if not ok]
    print(json.dumps({"module": "ezek_lib", "checks": len(checks), "passed": len(checks) - len(failed),
                      "failed": failed, "verdict": "GREEN" if not failed else "RED"}, ensure_ascii=False, indent=1))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(_selftest())
