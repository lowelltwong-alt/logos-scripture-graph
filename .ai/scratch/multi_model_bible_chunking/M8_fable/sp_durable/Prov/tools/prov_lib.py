#!/usr/bin/env python3
"""Shared library for the Prov r3 verification toolkit (Tier-0, deterministic).

Every agent brief points here. USE these tools; do NOT rebuild them.

NUMBERING: Prov is an IDENTITY book — WEB and MT verse numbering coincide at
all 915 verses across 31 chapters, byte-PROVEN at Phase 0 (per-chapter count
equality, 123 content anchors with the single miss byte-reviewed as a
rendering divergence, zero OSHB KJV-variance notes, and the eshet-chayil
acrostic as a 22-point ch-31 alignment anchor; see ../web_mt_offset_map.json).
web_to_mt()/mt_to_web() are range-guarded identities — still USE them, never
hand-assume, so out-of-range refs are caught. There are NO title pseudo-verses
(no Prov.N.0): the collection headers (1:1, 10:1, 22:17, 24:23, 25:1, 30:1,
31:1) are ordinary counted verses in BOTH witnesses.

CROSS-TRADITION: LXX reorders 24:23-34 and chs 30-31 relative to MT. Both
staged witnesses follow MT order — Greek ordering is cross-tradition METADATA
in prose only, never boundary evidence, never a refs entry.

There are NO Aramaic zones in Prov: all 915 MT verses are Hebrew (every OSHB
morph code is H-prefixed; Phase 0 verified from bytes).

SKELETON NOTE (owner lesson j, carried from Ps): skeleton() maps maqaf to a
SPACE, so consonantal sweeps are not maqaf-vs-space sensitive. The staged
extract is MAQAF-FREE at every tier (the extractor serialized maqaf as
SPACE). accent_stripped RETAINS meteg (U+05BD) — it strips cantillation
(U+0591-05AF) only. Final-letter allography (ך ם ן ף ץ) is preserved
exactly; sweep per attested spelling.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent          # SP/Prov
BOOK = "Prov"

_inv = json.loads((SPBOOK / "verse_inventory.json").read_text(encoding="utf-8"))
LAST_VERSE = {int(c): n for c, n in _inv["chapters"].items()}
TOTAL_VERSES = sum(LAST_VERSE.values())          # 915

_omap = json.loads((SPBOOK / "web_mt_offset_map.json").read_text(encoding="utf-8"))
MT_LAST_VERSE = {int(c): p["mt_verses"] for c, p in _omap["chapters"].items()}
MT_TOTAL_VERSES = sum(MT_LAST_VERSE.values())    # 915

# Compatibility shim for the Ps-lineage r3 tools: every Prov chapter is an
# identity "psalm rule" with no title pseudo-verse, so the tools'
# non-identity/title arms are verified NO-OPS here (byte-proven identity —
# see ../web_mt_offset_map.json). Do not add non-identity rules.
PSALM_RULES = {c: {"rule": "identity", "web_verses": LAST_VERSE[c],
                   "mt_verses": MT_LAST_VERSE[c]} for c in LAST_VERSE}

HEB_RUN = re.compile(r"[֑-״]+(?:[ ־][֑-״]+)*")
POINTS = re.compile(r"[֑-ׇ]")          # cantillation + vowels + meteg etc.
ACCENTS = re.compile(r"[֑-֯]")          # cantillation only (meteg RETAINED)
REF = re.compile(r"\bProv\.(\d+)\.(\d+)\b")


def web_to_mt(ch: int, v: int) -> tuple[int, int] | None:
    """WEB (ch, v) -> MT (ch, v). Identity, range-guarded: None if out of range."""
    if ch in LAST_VERSE and 1 <= v <= LAST_VERSE[ch]:
        return (ch, v)
    return None


def mt_to_web(ch: int, v: int) -> tuple[int, int] | None:
    """MT (ch, v) -> WEB (ch, v). Identity, range-guarded."""
    if ch in MT_LAST_VERSE and 1 <= v <= MT_LAST_VERSE[ch]:
        return (ch, v)
    return None


def mt_to_web_all(ch: int, v: int) -> list[tuple[int, int]]:
    """Identity book: at most one WEB verse per MT verse."""
    w = mt_to_web(ch, v)
    return [w] if w else []


def language_of(ch: int, v: int) -> str:
    return "Hebrew"                     # no Aramaic zones in Prov


def nfd(s: str) -> str:
    return unicodedata.normalize("NFD", s)


def strip_accents(s: str) -> str:
    return ACCENTS.sub("", nfd(s))


def skeleton(s: str) -> str:
    """Consonantal skeleton; maqaf becomes SPACE (owner lesson j) so
    consonantal sweeps are maqaf-agnostic. Final letters preserved."""
    return POINTS.sub("", nfd(s)).replace("־", " ")


def expand_ref_token(tok: str, last_verse: dict[int, int] | None = None) -> list[tuple[int, int]]:
    """'Prov.3.1' or 'Prov.3.1-Prov.3.8' or 'Prov.8.1-36' -> [(c,v), ...].
    Identity book: WEB and MT ranges share the same space; pass
    last_verse=MT_LAST_VERSE for oshb refs (defaults to WEB — same values)."""
    lv = last_verse or LAST_VERSE
    tok = tok.strip()
    m = re.match(r"^Prov\.(\d+)\.(\d+)(?:-(?:Prov\.)?(\d+)(?:\.(\d+))?)?$", tok)
    if not m:
        return []
    c1, v1 = int(m.group(1)), int(m.group(2))
    if m.group(3) is None:
        return [(c1, v1)]
    if m.group(4) is None:                     # Prov.8.1-36 (same-chapter shorthand)
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
    """verse_map_web is WEB-keyed; verse_map_oshb is MT-keyed. Identity book:
    the key spaces coincide — still use each entry's 'mt'/'web' back-reference
    in prose, never bare arithmetic claims."""
    web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
    oshb = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
    return web, oshb


def load_pmarks() -> dict:
    """MT-keyed inventories. Prov (Writings) DOES carry a WLC parashah layer:
    51 petuchah + 1 setumah segs over 52 verses — TIER-3 WEAK corroboration
    (parashah_in_prophets_or_writings), never a driver, single-witness
    disclosure required, PE never conflated with SAMEKH. Also: paseq (60 segs
    / 57 verses; seg layer, NOT quotable bytes), kq (69 notes / 63 verses),
    one x-small nun at Prov.16.28. NO selah exists in Prov."""
    return json.loads((SPBOOK / "pmarks_Prov.json").read_text(encoding="utf-8"))


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
