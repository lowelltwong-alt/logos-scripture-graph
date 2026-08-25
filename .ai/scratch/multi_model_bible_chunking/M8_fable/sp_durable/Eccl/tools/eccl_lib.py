#!/usr/bin/env python3
"""Shared library for the Eccl r3 verification toolkit (Tier-0, deterministic).

Every agent brief points here. USE these tools; do NOT rebuild them.

NUMBERING: Eccl is NOT an identity book. Byte-PROVEN at Phase 0 (per-chapter
counts under the rule set, 113 content anchors incl. 11 in the offset zone,
a falsification probe showing identity FAILS 7 anchor checks in ch 5, and
the four seam byte-review assertions; see ../web_mt_offset_map.json):
  MT 4:17        = WEB 5:1    ("Guard your steps ... God's house")
  MT 5:1..5:19   = WEB 5:2..5:20
  every other chapter is identity; totals 222 = 222 across 12 chapters.
web_to_mt()/mt_to_web() implement the crosswalk RANGE-GUARDED — always use
them, never hand-assume, in BOTH directions. The OSHB KJV-variance note
layer is EMPTY for Eccl despite the real offset — absence of notes proves
nothing here. There are NO title pseudo-verses (no Eccl.N.0).

CROSS-TRADITION: LXX/Greek numbering follows MT at the 4:17/5:1 split; the
English chapter division follows the Vulgate-family tradition. Greek order
matches MT book-wide. All of it is cross-tradition METADATA in prose only,
never boundary evidence, never a refs entry.

There are NO Aramaic zones in Eccl: all 222 MT verses are Hebrew (every
OSHB morph code is H-prefixed; 2,999 codes, Phase 0 verified from bytes).

SKELETON NOTE (owner lesson, carried from Ps/Prov): skeleton() maps maqaf to
a SPACE so consonantal sweeps are not maqaf-vs-space sensitive. The staged
extract is MAQAF-FREE at every tier (byte-verified at Phase 0 — the
extractor serialized maqaf as SPACE). accent_stripped RETAINS meteg
(U+05BD) — it strips cantillation (U+0591-05AF) only. Final-letter
allography (ך ם ן ף ץ) is preserved exactly; sweep per attested spelling.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent          # SP/Eccl
BOOK = "Eccl"

_inv = json.loads((SPBOOK / "verse_inventory.json").read_text(encoding="utf-8"))
LAST_VERSE = {int(c): n for c, n in _inv["chapters"].items()}
TOTAL_VERSES = sum(LAST_VERSE.values())          # 222

_omap = json.loads((SPBOOK / "web_mt_offset_map.json").read_text(encoding="utf-8"))
MT_LAST_VERSE = {int(c): p["mt_verses"] for c, p in _omap["chapters"].items()}
MT_TOTAL_VERSES = sum(MT_LAST_VERSE.values())    # 222

# Per-chapter rule table for the Ps-lineage r3 tools (keeps the historical
# name; the tools only test rule != "identity"). REAL non-identity rules for
# chs 4 and 5 — do NOT flatten these to identity.
PSALM_RULES = {c: {"rule": p["rule"], "web_verses": p["web_verses"],
                   "mt_verses": p["mt_verses"]}
               for c, p in ((int(k), v) for k, v in _omap["chapters"].items())}

HEB_RUN = re.compile(r"[֑-״]+(?:[ ־][֑-״]+)*")
POINTS = re.compile(r"[֑-ׇ]")          # cantillation + vowels + meteg etc.
ACCENTS = re.compile(r"[֑-֯]")          # cantillation only (meteg RETAINED)
REF = re.compile(r"\bEccl\.(\d+)\.(\d+)\b")


def web_to_mt(ch: int, v: int) -> tuple[int, int] | None:
    """WEB (ch, v) -> MT (ch, v). Crosswalk, range-guarded: None if out of range.
    WEB 5:1 -> MT 4:17; WEB 5:v -> MT 5:(v-1); identity elsewhere."""
    if ch not in LAST_VERSE or not (1 <= v <= LAST_VERSE[ch]):
        return None
    if ch == 5:
        return (4, 17) if v == 1 else (5, v - 1)
    return (ch, v)


def mt_to_web(ch: int, v: int) -> tuple[int, int] | None:
    """MT (ch, v) -> WEB (ch, v). Crosswalk, range-guarded.
    MT 4:17 -> WEB 5:1; MT 5:v -> WEB 5:(v+1); identity elsewhere."""
    if ch not in MT_LAST_VERSE or not (1 <= v <= MT_LAST_VERSE[ch]):
        return None
    if ch == 4 and v == 17:
        return (5, 1)
    if ch == 5:
        return (5, v + 1)
    return (ch, v)


def mt_to_web_all(ch: int, v: int) -> list[tuple[int, int]]:
    """Every MT verse maps to exactly one WEB verse in Eccl."""
    w = mt_to_web(ch, v)
    return [w] if w else []


def language_of(ch: int, v: int) -> str:
    return "Hebrew"                     # no Aramaic zones in Eccl


def nfd(s: str) -> str:
    return unicodedata.normalize("NFD", s)


def strip_accents(s: str) -> str:
    return ACCENTS.sub("", nfd(s))


def skeleton(s: str) -> str:
    """Consonantal skeleton; maqaf becomes SPACE so consonantal sweeps are
    maqaf-agnostic. Final letters preserved."""
    return POINTS.sub("", nfd(s)).replace("־", " ")


def expand_ref_token(tok: str, last_verse: dict[int, int] | None = None) -> list[tuple[int, int]]:
    """'Eccl.3.1' or 'Eccl.3.1-Eccl.3.8' or 'Eccl.8.1-17' -> [(c,v), ...].
    NON-IDENTITY BOOK: WEB and MT are DIFFERENT ref spaces in chs 4-5. The
    default space is WEB; pass last_verse=MT_LAST_VERSE for oshb: refs.
    The expansion never converts between spaces — use web_to_mt()/mt_to_web()
    per verse for that."""
    lv = last_verse or LAST_VERSE
    tok = tok.strip()
    m = re.match(r"^Eccl\.(\d+)\.(\d+)(?:-(?:Eccl\.)?(\d+)(?:\.(\d+))?)?$", tok)
    if not m:
        return []
    c1, v1 = int(m.group(1)), int(m.group(2))
    if m.group(3) is None:
        return [(c1, v1)]
    if m.group(4) is None:                     # Eccl.8.1-17 (same-chapter shorthand)
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
    book: the key spaces DIVERGE in chs 4-5 — always use each entry's
    'mt'/'web' back-reference or the crosswalk functions, never bare
    same-number assumptions."""
    web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
    oshb = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
    return web, oshb


def load_pmarks() -> dict:
    """MT-keyed inventories. WLC Eccl carries a NEARLY-EMPTY parashah layer:
    1 PE (MT 1:11 — the prologue-poem close) + 3 SAMEKH (MT 3:1, 3:8 —
    bracketing the time catalogue — and 9:10) — TIER-3 WEAK corroboration
    (parashah_in_prophets_or_writings), never a driver, single-witness
    disclosure required, PE never conflated with SAMEKH. Also: paseq (11
    segs / 11 verses; seg layer, NOT quotable bytes), kq (12 notes / 12
    verses). NO selah, NO small/large/suspended/reversed-nun segs exist in
    WLC Eccl — all are fabrication classes. Keys are MT refs: map WEB spans
    through web_to_mt() before lookups."""
    return json.loads((SPBOOK / "pmarks_Eccl.json").read_text(encoding="utf-8"))


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
