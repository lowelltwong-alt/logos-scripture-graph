#!/usr/bin/env python3
"""Shared library for the Lam r3 verification toolkit (Tier-0, deterministic).

Every agent brief points here. USE these tools; do NOT rebuild them.

NUMBERING: Lam is an IDENTITY book - WEB and MT agree verse-for-verse in
all five chapters (22 / 22 / 66 / 22 / 22 = 154 both witnesses), byte-PROVEN
at Phase 0 (per-chapter counts in both witnesses, content anchors at the
identity ref, and the OSHB variance layer; see ../web_mt_offset_map.json).
web_to_mt()/mt_to_web()/mt_to_web_all() exist for API parity with the
offset-bearing books and are the identity here (range-guarded). There is NO
split verse and NO title pseudo-verse (no Lam.N.0): Lam 1:1 (the eikhah
opening) is an ordinary counted verse in BOTH witnesses.

STRUCTURE (byte-proven at Phase 0, from the first consonant of every verse):
chs 1, 2 and 4 are 22-verse ALPHABETIC ACROSTICS; ch 3 is a 66-verse
TRIPLE acrostic (three consecutive verses per letter, 22 x 3); ch 5 has 22
verses but is NOT acrostic. Letter ORDER: ch 1 runs ayin-then-pe (the
standard order); chs 2, 3 and 4 run PE-THEN-AYIN (the reversed order) - a
byte fact of this witness, never to be "corrected". The acrostic letter is
a tier-1 text signal (inclusio_refrain_acrostic in the owner addendum) and
the primary structural spine of chs 1-4; verse divisions themselves stay
tier-4 metadata.

CROSS-TRADITION: LXX Lamentations carries a prose superscription before 1:1
(the Jeremiah-ascription) that MT/WLC and WEB do NOT carry; the Hebrew
canon places the book in the Writings (Megillot). All LXX/Vulgate/Peshitta/
Targum/DSS (4QLam, 3QLam, 5QLam) material is cross-tradition METADATA in
prose only, never boundary evidence, never a refs entry.

LANGUAGE: Lam is Hebrew throughout - every OSHB morph code is H-prefixed
(1,564 codes, 0 A-prefixed; byte-proven). language_of() always returns
"Hebrew"; any "Aramaic" verse label in Lam is a flag.

SKELETON NOTE (owner lesson, carried from Ps/Prov/Eccl/Song/Isa/Jer):
skeleton() maps maqaf to a SPACE so consonantal sweeps are not
maqaf-vs-space sensitive. The staged extract is MAQAF-FREE at every tier
(byte-verified at Phase 0: 0 x U+05BE; OSHB Lam carries 165 x-maqqef segs
in the XML, all serialized to spaces here). accent_stripped RETAINS meteg
(U+05BD) - it strips cantillation (U+0591-05AF) only. Final-letter
allography is preserved exactly; sweep per attested spelling and build
every hand-written needle FINALS-NORMALIZED (E-11 discipline).
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent          # SP/Lam
BOOK = "Lam"

_inv = json.loads((SPBOOK / "verse_inventory.json").read_text(encoding="utf-8"))
LAST_VERSE = {int(c): n for c, n in _inv["chapters"].items()}
TOTAL_VERSES = sum(LAST_VERSE.values())          # 154

_omap = json.loads((SPBOOK / "web_mt_offset_map.json").read_text(encoding="utf-8"))
MT_LAST_VERSE = {int(c): p["mt_verses"] for c, p in _omap["chapters"].items()}
MT_TOTAL_VERSES = sum(MT_LAST_VERSE.values())    # 154

# Per-chapter rule table for the Ps-lineage r3 tools (keeps the historical
# name; the tools only test rule != "identity"). Lam: identity everywhere.
PSALM_RULES = {c: {"rule": p["rule"], "web_verses": p["web_verses"],
                   "mt_verses": p["mt_verses"]}
               for c, p in ((int(k), v) for k, v in _omap["chapters"].items())}

HEB_RUN = re.compile(r"[\u0591-\u05F4]+(?:[ \u05BE][\u0591-\u05F4]+)*")
POINTS = re.compile(r"[\u0591-\u05C7]")          # cantillation + vowels + meteg etc.
ACCENTS = re.compile(r"[\u0591-\u05AF]")          # cantillation only (meteg RETAINED)
REF = re.compile(r"\bLam\.(\d+)\.(\d+)\b")

# API parity with prior books' toolsets: Lam has NO split verse and NO
# offset zone. These sentinels keep any split/zone-aware arm inert.
SPLIT_MT = None
SPLIT_WEB: list = []
ARAMAIC_VERSES: set = set()

# Acrostic spine (byte-proven at Phase 0; pinned again by build_verse_maps).
ACROSTIC_CHAPTERS = {1: 1, 2: 1, 3: 3, 4: 1}     # chapter -> verses per letter
REVERSED_PE_AYIN_CHAPTERS = {2, 3, 4}            # pe precedes ayin
NON_ACROSTIC_CHAPTERS = {5}


def web_to_mt(ch: int, v: int) -> tuple[int, int] | None:
    """WEB (ch, v) -> MT (ch, v). Identity in Lam, range-guarded."""
    if ch not in LAST_VERSE or not (1 <= v <= LAST_VERSE[ch]):
        return None
    return (ch, v)


def mt_to_web(ch: int, v: int) -> tuple[int, int] | None:
    """MT (ch, v) -> WEB (ch, v). Identity in Lam, range-guarded."""
    if ch not in MT_LAST_VERSE or not (1 <= v <= MT_LAST_VERSE[ch]):
        return None
    return (ch, v)


def mt_to_web_all(ch: int, v: int) -> list[tuple[int, int]]:
    """EVERY WEB verse an MT verse maps to - exactly one everywhere in Lam
    (kept for API parity with split-bearing books)."""
    w = mt_to_web(ch, v)
    return [] if w is None else [w]


def language_of(ch: int, v: int) -> str:
    """Language of a verse. Lam is Hebrew throughout (byte-proven from OSHB
    morph codes: 0 A-prefixed)."""
    return "Hebrew"


def nfd(s: str) -> str:
    return unicodedata.normalize("NFD", s)


def strip_accents(s: str) -> str:
    return ACCENTS.sub("", nfd(s))


def skeleton(s: str) -> str:
    """Consonantal skeleton; maqaf becomes SPACE so consonantal sweeps are
    maqaf-agnostic. Final letters preserved exactly as written."""
    return POINTS.sub("", nfd(s)).replace("\u05BE", " ")


def expand_ref_token(tok: str, last_verse: dict[int, int] | None = None) -> list[tuple[int, int]]:
    """'Lam.2.7' or 'Lam.2.7-Lam.3.5' or 'Lam.3.1-14' -> [(c,v), ...].
    IDENTITY BOOK: WEB and MT share one ref space; the last_verse argument
    is kept for API parity."""
    lv = last_verse or LAST_VERSE
    tok = tok.strip()
    m = re.match(r"^Lam\.(\d+)\.(\d+)(?:-(?:Lam\.)?(\d+)(?:\.(\d+))?)?$", tok)
    if not m:
        return []
    c1, v1 = int(m.group(1)), int(m.group(2))
    if m.group(3) is None:
        return [(c1, v1)]
    if m.group(4) is None:                     # Lam.3.1-14 (same-chapter shorthand)
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
    """verse_map_web is WEB-keyed; verse_map_oshb is MT-keyed. IDENTITY book:
    the key spaces coincide; each entry still carries its 'mt'/'web'
    back-reference for API parity."""
    web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
    oshb = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
    return web, oshb


def load_pmarks() -> dict:
    """MT-keyed inventories (identity numbering). WLC Lam carries: parashah
    5 PE + 84 SAMEKH segs (Writings: TIER-3 WEAK corroboration under the
    owner addendum (parashah_in_prophets_or_writings) - never a driver,
    single-witness disclosure required on every citation, PE never
    conflated with SAMEKH; absence is NEVER counterevidence); paseq 11 segs
    (seg layer, NOT quotable bytes, COUNT-ONLY); kq 22 variant notes (check
    kq BEFORE counting or slicing in ANY K/Q verse); NO special-letter,
    selah, large/small/suspended/reversed-nun segs (any such claim is a
    fabrication)."""
    return json.loads((SPBOOK / "pmarks_Lam.json").read_text(encoding="utf-8"))


def norm_english(s: str) -> str:
    """Normalize English for quote comparison: typographic quotes/apostrophes/
    dashes to ASCII, [fn ...] removed, whitespace collapsed."""
    s = re.sub(r"\[fn [^\]]*\]", " ", s)
    s = (s.replace("\u201c", '"').replace("\u201d", '"')
           .replace("\u2018", "'").replace("\u2019", "'")
           .replace("\u2014", "-").replace("\u2013", "-"))
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def collate_hebrew(quoted: str, source_text: str) -> str:
    """Return the strongest matching tier of quoted against source_text:
    'byte' | 'nfd' | 'accent_stripped' | 'skeleton' | 'none'.
    Ellipsis-aware: fragments split on \u2026 or ... must match IN ORDER."""
    frags = [f.strip() for f in re.split(r"\u2026|\.\.\.", quoted) if f.strip()]
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
    frags = [norm_english(f) for f in re.split(r"\u2026|\.\.\.", quoted)]
    frags = [f for f in frags if f]
    pos = 0
    for f in frags:
        i = hay.find(f, pos)
        if i < 0:
            return False
        pos = i + len(f)
    return True
