#!/usr/bin/env python3
"""Shared library for the Jer r3 verification toolkit (Tier-0, deterministic).

Every agent brief points here. USE these tools; do NOT rebuild them.

NUMBERING: Jer carries EXACTLY ONE offset zone, byte-PROVEN at Phase 0
(per-chapter counts under the rule set, content anchors incl. in-zone hits,
falsification probes showing identity FAILS inside the zone, and seam
byte-review assertions; see ../web_mt_offset_map.json):

  ZONE (chs 8-9) - pure renumbering, NO split:
    MT 8:23        = WEB 9:1    ("Oh that my head were waters ... spring of
                                 tears" - the weeping-prophet line)
    MT 9:1..9:25   = WEB 9:2..9:26

Every other chapter is identity; totals WEB 1364 / MT 1364 over 52 chapters
(EQUAL totals - unlike Isa there is NO split verse anywhere; web_to_mt is
INJECTIVE for Jer). web_to_mt()/mt_to_web()/mt_to_web_all() implement the
crosswalk RANGE-GUARDED - always use them, never hand-assume, in BOTH
directions. mt_to_web_all() exists for API parity with prior books and
always returns exactly ONE ref in Jer. The OSHB KJV-variance note layer is
EMPTY for Jer despite the real offset zone (the FOURTH book running: Eccl,
Song, Isa, Jer) - absence of notes proves nothing. There are NO title
pseudo-verses (no Jer.N.0): Jer 1:1 (the divrei-Yirmeyahu superscription)
is an ordinary counted verse in BOTH witnesses.

CROSS-TRADITION: LXX Jeremiah is FAMOUSLY divergent from MT - roughly
one-eighth shorter, with the oracles-against-nations block placed after
25:13 and internally re-ordered; 4QJer-b/d attest a short Hebrew text
type. NONE of that touches this campaign's two witnesses: WEB and MT both
follow the MT arrangement, and the ONLY WEB/MT numbering divergence is the
chs 8-9 seam above. All LXX/Old Greek/Vulgate/Peshitta/Targum/DSS/Qumran
material is cross-tradition METADATA in prose only, never boundary
evidence, never a refs entry.

LANGUAGE: Jer carries EXACTLY ONE Aramaic verse - MT 10:11 = WEB 10:11
(identity numbering; byte-proven: 15 A-prefixed OSHB morph codes, all in
that verse; the other 21,961 codes are H-prefixed). It is a self-contained
Aramaic island inside a Hebrew oracle. language_of() knows it.

SKELETON NOTE (owner lesson, carried from Ps/Prov/Eccl/Song/Isa):
skeleton() maps maqaf to a SPACE so consonantal sweeps are not
maqaf-vs-space sensitive. The staged extract is MAQAF-FREE at every tier
(byte-verified at Phase 0: 0 x U+05BE - the extractor serialized maqaf as
SPACE; OSHB Jer carries 3,471 x-maqqef segs in the XML, all serialized to
spaces here). accent_stripped RETAINS meteg (U+05BD) - it strips
cantillation (U+0591-05AF) only. Final-letter allography is preserved
exactly; sweep per attested spelling and build every hand-written needle
FINALS-NORMALIZED (E-11 discipline).
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent          # SP/Jer
BOOK = "Jer"

_inv = json.loads((SPBOOK / "verse_inventory.json").read_text(encoding="utf-8"))
LAST_VERSE = {int(c): n for c, n in _inv["chapters"].items()}
TOTAL_VERSES = sum(LAST_VERSE.values())          # 1364

_omap = json.loads((SPBOOK / "web_mt_offset_map.json").read_text(encoding="utf-8"))
MT_LAST_VERSE = {int(c): p["mt_verses"] for c, p in _omap["chapters"].items()}
MT_TOTAL_VERSES = sum(MT_LAST_VERSE.values())    # 1364

# Per-chapter rule table for the Ps-lineage r3 tools (keeps the historical
# name; the tools only test rule != "identity"). REAL non-identity rules for
# chs 8 and 9 only.
PSALM_RULES = {c: {"rule": p["rule"], "web_verses": p["web_verses"],
                   "mt_verses": p["mt_verses"]}
               for c, p in ((int(k), v) for k, v in _omap["chapters"].items())}

HEB_RUN = re.compile(r"[֑-״]+(?:[ ־][֑-״]+)*")
POINTS = re.compile(r"[֑-ׇ]")          # cantillation + vowels + meteg etc.
ACCENTS = re.compile(r"[֑-֯]")          # cantillation only (meteg RETAINED)
REF = re.compile(r"\bJer\.(\d+)\.(\d+)\b")

# API parity with prior books' toolsets: Jer has NO split verse. These
# sentinels keep any split-aware arm inert ((ch, v) == SPLIT_MT is never
# true; SPLIT_WEB is empty).
SPLIT_MT = None
SPLIT_WEB: list = []

# The single Aramaic verse (identity-zone numbering, so MT and WEB agree).
ARAMAIC_VERSES = {(10, 11)}


def web_to_mt(ch: int, v: int) -> tuple[int, int] | None:
    """WEB (ch, v) -> MT (ch, v). Crosswalk, range-guarded: None if out of
    range. INJECTIVE in Jer (no split verse)."""
    if ch not in LAST_VERSE or not (1 <= v <= LAST_VERSE[ch]):
        return None
    if ch == 9:
        return (8, 23) if v == 1 else (9, v - 1)
    return (ch, v)


def mt_to_web(ch: int, v: int) -> tuple[int, int] | None:
    """MT (ch, v) -> the WEB counterpart (exactly one in Jer). Crosswalk,
    range-guarded."""
    if ch not in MT_LAST_VERSE or not (1 <= v <= MT_LAST_VERSE[ch]):
        return None
    if ch == 8 and v == 23:
        return (9, 1)
    if ch == 9:
        return (9, v + 1)
    return (ch, v)


def mt_to_web_all(ch: int, v: int) -> list[tuple[int, int]]:
    """EVERY WEB verse an MT verse maps to - exactly one everywhere in Jer
    (kept for API parity with split-bearing books)."""
    w = mt_to_web(ch, v)
    return [] if w is None else [w]


def language_of(ch: int, v: int) -> str:
    """Language of a verse. Jer is Hebrew EXCEPT the single Aramaic island
    at 10:11 (identity numbering - the same coordinates in both witnesses;
    byte-proven from OSHB morph codes)."""
    return "Aramaic" if (ch, v) in ARAMAIC_VERSES else "Hebrew"


def nfd(s: str) -> str:
    return unicodedata.normalize("NFD", s)


def strip_accents(s: str) -> str:
    return ACCENTS.sub("", nfd(s))


def skeleton(s: str) -> str:
    """Consonantal skeleton; maqaf becomes SPACE so consonantal sweeps are
    maqaf-agnostic. Final letters preserved exactly as written."""
    return POINTS.sub("", nfd(s)).replace("־", " ")


def expand_ref_token(tok: str, last_verse: dict[int, int] | None = None) -> list[tuple[int, int]]:
    """'Jer.2.7' or 'Jer.2.7-Jer.3.5' or 'Jer.8.1-14' -> [(c,v), ...].
    NON-IDENTITY BOOK: WEB and MT are DIFFERENT ref spaces in chs 8-9.
    The default space is WEB; pass last_verse=MT_LAST_VERSE for oshb:
    refs. The expansion never converts between spaces - use
    web_to_mt()/mt_to_web() per verse for that."""
    lv = last_verse or LAST_VERSE
    tok = tok.strip()
    m = re.match(r"^Jer\.(\d+)\.(\d+)(?:-(?:Jer\.)?(\d+)(?:\.(\d+))?)?$", tok)
    if not m:
        return []
    c1, v1 = int(m.group(1)), int(m.group(2))
    if m.group(3) is None:
        return [(c1, v1)]
    if m.group(4) is None:                     # Jer.8.1-14 (same-chapter shorthand)
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
    """verse_map_web is WEB-keyed; verse_map_oshb is MT-keyed. NON-IDENTITY
    book: the key spaces DIVERGE in chs 8-9 - always use each entry's
    'mt'/'web' back-reference or the crosswalk functions, never bare
    same-number assumptions."""
    web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
    oshb = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
    return web, oshb


def load_pmarks() -> dict:
    """MT-keyed inventories. WLC Jer carries the campaign's LARGEST layers in
    EVERY apparatus class: parashah 58 PE + 246 SAMEKH segs (Prophets:
    TIER-3 WEAK corroboration under the owner addendum
    (parashah_in_prophets_or_writings) - never a driver, single-witness
    disclosure required on every citation, PE never conflated with SAMEKH;
    absence is NEVER counterevidence); paseq 157 segs (seg layer, NOT
    quotable bytes, COUNT-ONLY); kq 141 variant notes over 124 verses (the
    campaign's largest K/Q inventory - check kq BEFORE counting or slicing
    in ANY K/Q verse; twelve doubled-note verses); exactly ONE special
    letter - a SMALL NUN at MT 39:13 (every OTHER special-letter claim is a
    fabrication); NO selah / large-letter / suspended / reversed-nun segs.
    Keys are MT refs: map WEB spans through web_to_mt() before lookups."""
    return json.loads((SPBOOK / "pmarks_Jer.json").read_text(encoding="utf-8"))


def norm_english(s: str) -> str:
    """Normalize English for quote comparison: typographic quotes/apostrophes/
    dashes to ASCII, [fn ...] removed, whitespace collapsed."""
    s = re.sub(r"\[fn [^\]]*\]", " ", s)
    s = (s.replace("“", '"').replace("”", '"')
           .replace("‘", "'").replace("’", "'")
           .replace("—", "-").replace("–", "-"))
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def collate_hebrew(quoted: str, source_text: str) -> str:
    """Return the strongest matching tier of quoted against source_text:
    'byte' | 'nfd' | 'accent_stripped' | 'skeleton' | 'none'.
    Ellipsis-aware: fragments split on … or ... must match IN ORDER."""
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
