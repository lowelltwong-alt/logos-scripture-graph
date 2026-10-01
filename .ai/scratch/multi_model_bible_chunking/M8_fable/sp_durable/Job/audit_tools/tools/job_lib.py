#!/usr/bin/env python3
"""Shared library for the Job OW-2 AUDIT toolkit (Tier-0, deterministic).

REBUILT 2026-09-03 for OW-2 item 2 from the raw witnesses. The original Job
campaign toolkit lived in a 2026-08-11/12 session scratchpad that no longer
exists on disk and was never mirrored durable (there is no sp_durable/Job).
Same lineage and API as the Song r3 lib so the mechanical tools adapt.

Every audit brief points here. USE these tools; do NOT rebuild them.

NUMBERING: Job is NOT an identity book — ONE offset zone at the WEB 40|41
break (byte-PROVEN by build_offset_map.py: per-chapter counts under the rule
set, content anchors at the crosswalk-mapped refs incl. every zone verse
with an anchor, a falsification probe under identity, seam byte-review
assertions, and a secondary shipped-corpus dual-cite probe):
  WEB 41:1-8  = MT 40:25-32   (the Leviathan poem's opening: MT ch 40 runs to 32)
  WEB 41:9-34 = MT 41:1-26
  ALL else identity; totals 1070 = 1070 over 42 chapters.
The Behemoth poem (40:15-24) sits BEFORE the zone in both numberings; the
Leviathan poem IS the zone (WEB 41 = MT 40:25-41:26). The WEB 40|41 chapter
break itself is tier-4 metadata — never a seam warrant. Original-language
cites inside the zone MUST dual-cite (web:Job.41.V = oshb:Job.MTc.MTv).
web_to_mt()/mt_to_web() implement the crosswalk RANGE-GUARDED — always use
them, never hand-assume, in BOTH directions. There are NO title
pseudo-verses (no Job.N.0). Convention: bare/web: refs + row spans = WEB;
oshb:/pmarks = MT.

MARKS (book_strategy/Job.md §4, re-asserted from bytes by build_pmarks.py):
26 PE + 13 SAMEKH (Writings: TIER-3 weak corroboration at most, never a
driver, single-witness, PE never conflated with SAMEKH, absence never
counterevidence; the mark FOLLOWS its verse); paseq 98 segs / 93 verses
(count-only); suspended ayin x2 (MT 38:13, 38:15); K/Q 53 notes / 49
verses. NO selah in Job (fabrication class).

There are NO Aramaic zones in Job (every OSHB morph code is H-prefixed;
verified from bytes).

SKELETON NOTE (campaign-wide): skeleton() maps maqaf to a SPACE. The staged
extract is MAQAF-FREE at every tier (the extractor serialized maqaf as
SPACE). accent_stripped RETAINS meteg (U+05BD). Final-letter allography is
preserved exactly; sweep per attested spelling.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent          # SP/Job
BOOK = "Job"

_inv = json.loads((SPBOOK / "verse_inventory.json").read_text(encoding="utf-8"))
LAST_VERSE = {int(c): n for c, n in _inv["chapters"].items()}
TOTAL_VERSES = sum(LAST_VERSE.values())          # 1070

_omap = json.loads((SPBOOK / "web_mt_offset_map.json").read_text(encoding="utf-8"))
MT_LAST_VERSE = {int(c): p["mt_verses"] for c, p in _omap["chapters"].items()}
MT_TOTAL_VERSES = sum(MT_LAST_VERSE.values())    # 1070

# Per-chapter rule table (historical Ps-lineage name; tools test rule != "identity").
PSALM_RULES = {int(k): {"rule": v["rule"], "web_verses": v["web_verses"],
                        "mt_verses": v["mt_verses"]}
               for k, v in _omap["chapters"].items()}

HEB_RUN = re.compile(r"[֑-״]+(?:[ ־][֑-״]+)*")
POINTS = re.compile(r"[֑-ׇ]")          # cantillation + vowels + meteg etc.
ACCENTS = re.compile(r"[֑-֯]")          # cantillation only (meteg RETAINED)
REF = re.compile(r"\bJob\.(\d+)\.(\d+)\b")


def web_to_mt(ch: int, v: int) -> tuple[int, int] | None:
    """WEB (ch, v) -> MT (ch, v). Crosswalk, range-guarded: None if out of range.
    WEB 41:1-8 -> MT 40:25-32; WEB 41:9-34 -> MT 41:1-26; identity elsewhere."""
    if ch not in LAST_VERSE or not (1 <= v <= LAST_VERSE[ch]):
        return None
    if ch == 41:
        return (40, 24 + v) if v <= 8 else (41, v - 8)
    return (ch, v)


def web_to_mt_all(ch: int, v: int) -> list[tuple[int, int]]:
    m = web_to_mt(ch, v)
    return [m] if m else []


def mt_to_web(ch: int, v: int) -> tuple[int, int] | None:
    """MT (ch, v) -> WEB (ch, v). Crosswalk, range-guarded.
    MT 40:25-32 -> WEB 41:1-8; MT 41:1-26 -> WEB 41:9-34; identity elsewhere."""
    if ch not in MT_LAST_VERSE or not (1 <= v <= MT_LAST_VERSE[ch]):
        return None
    if ch == 40 and v >= 25:
        return (41, v - 24)
    if ch == 41:
        return (41, v + 8)
    return (ch, v)


def mt_to_web_all(ch: int, v: int) -> list[tuple[int, int]]:
    """Every MT verse maps to exactly one WEB verse in Job."""
    w = mt_to_web(ch, v)
    return [w] if w else []


def title_mt_refs(ch: int) -> list[tuple[int, int]]:
    return []                           # no title pseudo-verses in Job


def language_of(ch: int, v: int) -> str:
    return "Hebrew"                     # no Aramaic zones in Job


def nfd(s: str) -> str:
    return unicodedata.normalize("NFD", s)


def strip_accents(s: str) -> str:
    return ACCENTS.sub("", nfd(s))


def skeleton(s: str) -> str:
    """Consonantal skeleton; maqaf becomes SPACE so consonantal sweeps are
    maqaf-agnostic. Final letters preserved."""
    return POINTS.sub("", nfd(s)).replace("־", " ")


def expand_ref_token(tok: str, last_verse: dict[int, int] | None = None) -> list[tuple[int, int]]:
    """'Job.3.1' or 'Job.3.1-Job.3.26' or 'Job.28.1-28' -> [(c,v), ...].
    NON-IDENTITY BOOK: WEB and MT are DIFFERENT ref spaces in chs 40-41. The
    default space is WEB; pass last_verse=MT_LAST_VERSE for oshb: refs. The
    expansion never converts between spaces — use web_to_mt()/mt_to_web()
    per verse for that."""
    lv = last_verse or LAST_VERSE
    tok = tok.strip()
    m = re.match(r"^Job\.(\d+)\.(\d+)(?:-(?:Job\.)?(\d+)(?:\.(\d+))?)?$", tok)
    if not m:
        return []
    c1, v1 = int(m.group(1)), int(m.group(2))
    if m.group(3) is None:
        return [(c1, v1)]
    if m.group(4) is None:                     # Job.28.1-28 (same-chapter shorthand)
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
    book: the key spaces DIVERGE in chs 40-41 — always use each entry's
    'mt'/'web' back-reference or the crosswalk functions."""
    web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
    oshb = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
    return web, oshb


def load_pmarks() -> dict:
    """MT-keyed inventories (../pmarks_Job.json, byte-extracted): 26 PE + 13
    SAMEKH (tier-3 weak corroboration, single-witness, PE never conflated
    with SAMEKH, absence never counterevidence), paseq (count-only, never
    quotable), suspended ayin x2 (MT 38:13, 38:15), K/Q notes. NO selah, NO
    reversed-nun / small / large segs exist in WLC Job — fabrication classes.
    Keys are MT refs: map WEB spans through web_to_mt() before lookups."""
    return json.loads((SPBOOK / "pmarks_Job.json").read_text(encoding="utf-8"))


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
