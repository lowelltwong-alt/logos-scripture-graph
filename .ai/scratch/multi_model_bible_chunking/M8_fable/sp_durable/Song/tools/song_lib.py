#!/usr/bin/env python3
"""Shared library for the Song r3 verification toolkit (Tier-0, deterministic).

Every agent brief points here. USE these tools; do NOT rebuild them.

NUMBERING: Song is NOT an identity book. Byte-PROVEN at Phase 0 (per-chapter
counts under the rule set, 104 content anchors incl. 18 in the offset zone,
a falsification probe showing identity FAILS 18 anchor checks in the zone,
and six seam byte-review assertions; see ../web_mt_offset_map.json):
  MT 7:1         = WEB 6:13   ("Return, return, Shulammite!")
  MT 7:2..7:14   = WEB 7:1..7:13
every other chapter is identity; totals 117 = 117 across 8 chapters.
web_to_mt()/mt_to_web() implement the crosswalk RANGE-GUARDED — always use
them, never hand-assume, in BOTH directions. The OSHB KJV-variance note
layer is EMPTY for Song despite the real offset (exactly as in Eccl) —
absence of notes proves nothing here. There are NO title pseudo-verses
(no Song.N.0): Song 1:1 (the shir-hashirim superscription) is an ordinary
counted verse in BOTH witnesses.

CROSS-TRADITION: LXX/Greek numbering follows MT at the 6:13/7:1 seam; the
English chapter division follows the Vulgate-family tradition. Greek order
matches MT book-wide. All of it is cross-tradition METADATA in prose only,
never boundary evidence, never a refs entry.

There are NO Aramaic zones in Song: all 117 MT verses are Hebrew (every
OSHB morph code is H-prefixed; 1,255 codes, Phase 0 verified from bytes).
Aramaic-influence DISCUSSION (the she- relative register, the Persian loan
pardes 4:13) is legitimate; labeling a VERSE as Aramaic is flagged.

WEB SPEAKER HEADINGS (Song-specific tier-4 hazard): the WEB extract carries
[SPEAKER: Lover/Beloved/Friends/Relatives/Brothers] apparatus lines. They
are MODERN EDITORIAL metadata (owner addendum tier 4) — NEVER boundary
evidence, NEVER voice-attribution evidence, NEVER counterevidence by
absence. The staged tools strip them from verse text and catalog them in
../speaker_headings_web.json purely so claims can be audited AGAINST
leaning on them. Voice attribution is argued from the text's own signals
(vocatives, grammatical gender, addressee forms) per the owner gate policy.

SKELETON NOTE (owner lesson, carried from Ps/Prov/Eccl): skeleton() maps
maqaf to a SPACE so consonantal sweeps are not maqaf-vs-space sensitive.
The staged extract is MAQAF-FREE at every tier (byte-verified at Phase 0 —
the extractor serialized maqaf as SPACE). accent_stripped RETAINS meteg
(U+05BD) — it strips cantillation (U+0591-05AF) only. Final-letter
allography (ך ם ן ף ץ) is preserved exactly; sweep per attested spelling.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent          # SP/Song
BOOK = "Song"

_inv = json.loads((SPBOOK / "verse_inventory.json").read_text(encoding="utf-8"))
LAST_VERSE = {int(c): n for c, n in _inv["chapters"].items()}
TOTAL_VERSES = sum(LAST_VERSE.values())          # 117

_omap = json.loads((SPBOOK / "web_mt_offset_map.json").read_text(encoding="utf-8"))
MT_LAST_VERSE = {int(c): p["mt_verses"] for c, p in _omap["chapters"].items()}
MT_TOTAL_VERSES = sum(MT_LAST_VERSE.values())    # 117

# Per-chapter rule table for the Ps-lineage r3 tools (keeps the historical
# name; the tools only test rule != "identity"). REAL non-identity rules for
# chs 6 and 7 — do NOT flatten these to identity.
PSALM_RULES = {c: {"rule": p["rule"], "web_verses": p["web_verses"],
                   "mt_verses": p["mt_verses"]}
               for c, p in ((int(k), v) for k, v in _omap["chapters"].items())}

HEB_RUN = re.compile(r"[֑-״]+(?:[ ־][֑-״]+)*")
POINTS = re.compile(r"[֑-ׇ]")          # cantillation + vowels + meteg etc.
ACCENTS = re.compile(r"[֑-֯]")          # cantillation only (meteg RETAINED)
REF = re.compile(r"\bSong\.(\d+)\.(\d+)\b")


def web_to_mt(ch: int, v: int) -> tuple[int, int] | None:
    """WEB (ch, v) -> MT (ch, v). Crosswalk, range-guarded: None if out of range.
    WEB 6:13 -> MT 7:1; WEB 7:v -> MT 7:(v+1); identity elsewhere."""
    if ch not in LAST_VERSE or not (1 <= v <= LAST_VERSE[ch]):
        return None
    if ch == 6 and v == 13:
        return (7, 1)
    if ch == 7:
        return (7, v + 1)
    return (ch, v)


def mt_to_web(ch: int, v: int) -> tuple[int, int] | None:
    """MT (ch, v) -> WEB (ch, v). Crosswalk, range-guarded.
    MT 7:1 -> WEB 6:13; MT 7:v -> WEB 7:(v-1) for v in 2..14; identity elsewhere."""
    if ch not in MT_LAST_VERSE or not (1 <= v <= MT_LAST_VERSE[ch]):
        return None
    if ch == 7:
        return (6, 13) if v == 1 else (7, v - 1)
    return (ch, v)


def mt_to_web_all(ch: int, v: int) -> list[tuple[int, int]]:
    """Every MT verse maps to exactly one WEB verse in Song."""
    w = mt_to_web(ch, v)
    return [w] if w else []


def language_of(ch: int, v: int) -> str:
    return "Hebrew"                     # no Aramaic zones in Song


def nfd(s: str) -> str:
    return unicodedata.normalize("NFD", s)


def strip_accents(s: str) -> str:
    return ACCENTS.sub("", nfd(s))


def skeleton(s: str) -> str:
    """Consonantal skeleton; maqaf becomes SPACE so consonantal sweeps are
    maqaf-agnostic. Final letters preserved."""
    return POINTS.sub("", nfd(s)).replace("־", " ")


def expand_ref_token(tok: str, last_verse: dict[int, int] | None = None) -> list[tuple[int, int]]:
    """'Song.2.7' or 'Song.2.7-Song.3.5' or 'Song.8.1-14' -> [(c,v), ...].
    NON-IDENTITY BOOK: WEB and MT are DIFFERENT ref spaces in chs 6-7. The
    default space is WEB; pass last_verse=MT_LAST_VERSE for oshb: refs.
    The expansion never converts between spaces — use web_to_mt()/mt_to_web()
    per verse for that."""
    lv = last_verse or LAST_VERSE
    tok = tok.strip()
    m = re.match(r"^Song\.(\d+)\.(\d+)(?:-(?:Song\.)?(\d+)(?:\.(\d+))?)?$", tok)
    if not m:
        return []
    c1, v1 = int(m.group(1)), int(m.group(2))
    if m.group(3) is None:
        return [(c1, v1)]
    if m.group(4) is None:                     # Song.8.1-14 (same-chapter shorthand)
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
    book: the key spaces DIVERGE in chs 6-7 — always use each entry's
    'mt'/'web' back-reference or the crosswalk functions, never bare
    same-number assumptions."""
    web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
    oshb = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
    return web, oshb


def load_pmarks() -> dict:
    """MT-keyed inventories. WLC Song carries a RICH, refrain-tracking
    parashah layer (contrast Eccl's near-empty one): 1 PE (MT 8:10) + 19
    SAMEKH (MT 1:4, 1:8, 1:14, 2:7, 2:13, 2:14, 2:17, 3:5, 3:8, 3:11, 4:7,
    4:11, 5:1, 6:3, 6:9, 6:10, 7:11, 8:4, 8:7) — TIER-3 WEAK corroboration
    (parashah_in_prophets_and_writings), never a driver, single-witness
    disclosure required, PE never conflated with SAMEKH. Note the layer
    shadows the refrain skeleton (SAMEKH at all three adjuration sites MT
    2:7 / 3:5 / 8:4 and at the mutual-belonging sites MT 6:3 / 7:11) — the
    tier does NOT rise for that; the refrains themselves are the tier-1
    evidence. MT 7:11 = WEB 7:10 (offset zone). Also: paseq (12 segs / 12
    verses; seg layer, NOT quotable bytes), kq (4 notes / 4 verses: MT 1:17,
    2:11, 2:13, 4:9 — NONE in the offset zone). NO selah, NO small/large/
    suspended/reversed-nun segs exist in WLC Song — all are fabrication
    classes. Keys are MT refs: map WEB spans through web_to_mt() before
    lookups."""
    return json.loads((SPBOOK / "pmarks_Song.json").read_text(encoding="utf-8"))


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
