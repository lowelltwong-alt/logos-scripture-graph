#!/usr/bin/env python3
"""Shared library for the Isa r3 verification toolkit (Tier-0, deterministic).

Every agent brief points here. USE these tools; do NOT rebuild them.

NUMBERING: Isa is NOT an identity book — it carries TWO offset zones with
DIFFERENT SHAPES, byte-PROVEN at Phase 0 (per-chapter counts under the rule
set, 959 content anchors incl. 34 in the zones, falsification probes showing
identity FAILS 23 anchor checks in zone A and 9 in zone B, a SPLIT
discriminator, and 17 seam byte-review assertions; see
../web_mt_offset_map.json):

  ZONE A (chs 8-9) — pure renumbering:
    MT 8:23        = WEB 9:1    (Zebulun/Naphtali/Galilee line)
    MT 9:1..9:20   = WEB 9:2..9:21
  ZONE B (chs 63-64) — a genuine SPLIT (WEB 1292 vs MT 1291):
    MT 63:19       = WEB 63:19 + WEB 64:1   (one MT verse, TWO WEB verses:
                     "never ruled / not called by your name" at WEB 63:19;
                     "tear the heavens ... mountains quake" at WEB 64:1)
    MT 64:1..64:11 = WEB 64:2..64:12

Every other chapter is identity; totals WEB 1292 / MT 1291 over 66 chapters.
web_to_mt()/mt_to_web()/mt_to_web_all() implement the crosswalk RANGE-GUARDED
— always use them, never hand-assume, in BOTH directions. BECAUSE OF THE
SPLIT, web_to_mt is NOT injective (WEB 63:19 and WEB 64:1 BOTH map to MT
63:19) and mt_to_web_all(63, 19) returns TWO refs — any content claim about
MT 63:19 must say which WEB half it lives in. The OSHB KJV-variance note
layer is EMPTY for Isa despite two real offset zones (the THIRD book running:
Eccl, Song, Isa) — absence of notes proves nothing here. There are NO title
pseudo-verses (no Isa.N.0): Isa 1:1 (the chazon superscription) is an
ordinary counted verse in BOTH witnesses.

CROSS-TRADITION: MT (and LXX-order) numbering differs from the English
Vulgate-family chapter division at both seams. All of it is cross-tradition
METADATA in prose only, never boundary evidence, never a refs entry.

There are NO Aramaic zones in Isa: all 1,291 MT verses are Hebrew (every
OSHB morph code is H-prefixed; 16,988 codes, Phase 0 verified from bytes).
Aramaic-influence DISCUSSION is legitimate; labeling a VERSE as Aramaic is
flagged.

SKELETON NOTE (owner lesson, carried from Ps/Prov/Eccl/Song): skeleton()
maps maqaf to a SPACE so consonantal sweeps are not maqaf-vs-space
sensitive. The staged extract is MAQAF-FREE at every tier (byte-verified at
Phase 0 — the extractor serialized maqaf as SPACE). accent_stripped RETAINS
meteg (U+05BD) — it strips cantillation (U+0591-05AF) only. Final-letter
allography (ך ם ן ף ץ) is preserved exactly; sweep per attested spelling —
AND Isa carries the campaign's flagship allography hazard: MT 9:6 לםרבה has
a FINAL MEM IN MEDIAL POSITION in the letter bytes themselves, staged as a
DOUBLED token pair (לםרבה למרבה, K/Q apparatus) — see the TOOLKIT hazard
catalog before any mem-sensitive sweep.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent          # SP/Isa
BOOK = "Isa"

_inv = json.loads((SPBOOK / "verse_inventory.json").read_text(encoding="utf-8"))
LAST_VERSE = {int(c): n for c, n in _inv["chapters"].items()}
TOTAL_VERSES = sum(LAST_VERSE.values())          # 1292

_omap = json.loads((SPBOOK / "web_mt_offset_map.json").read_text(encoding="utf-8"))
MT_LAST_VERSE = {int(c): p["mt_verses"] for c, p in _omap["chapters"].items()}
MT_TOTAL_VERSES = sum(MT_LAST_VERSE.values())    # 1291

# Per-chapter rule table for the Ps-lineage r3 tools (keeps the historical
# name; the tools only test rule != "identity"). REAL non-identity rules for
# chs 8, 9, 63, 64 — do NOT flatten these to identity. Ch 63 is numbering-
# identity but carries the SPLIT tail (MT 63:19 spans WEB 63:19 + 64:1), so
# it stays non-identity here to keep the WARN arms live there.
PSALM_RULES = {c: {"rule": p["rule"], "web_verses": p["web_verses"],
                   "mt_verses": p["mt_verses"]}
               for c, p in ((int(k), v) for k, v in _omap["chapters"].items())}

HEB_RUN = re.compile(r"[֑-״]+(?:[ ־][֑-״]+)*")
POINTS = re.compile(r"[֑-ׇ]")          # cantillation + vowels + meteg etc.
ACCENTS = re.compile(r"[֑-֯]")          # cantillation only (meteg RETAINED)
REF = re.compile(r"\bIsa\.(\d+)\.(\d+)\b")

# The one split verse (MT side), as a constant every tool can name.
SPLIT_MT = (63, 19)
SPLIT_WEB = [(63, 19), (64, 1)]


def web_to_mt(ch: int, v: int) -> tuple[int, int] | None:
    """WEB (ch, v) -> MT (ch, v). Crosswalk, range-guarded: None if out of
    range. NOT injective: WEB 63:19 and WEB 64:1 both return MT 63:19."""
    if ch not in LAST_VERSE or not (1 <= v <= LAST_VERSE[ch]):
        return None
    if ch == 9:
        return (8, 23) if v == 1 else (9, v - 1)
    if ch == 64:
        return (63, 19) if v == 1 else (64, v - 1)
    return (ch, v)


def mt_to_web(ch: int, v: int) -> tuple[int, int] | None:
    """MT (ch, v) -> the FIRST WEB counterpart. Crosswalk, range-guarded.
    For the split verse MT 63:19 this returns WEB 63:19 (the first half) —
    use mt_to_web_all() whenever the second half (WEB 64:1) matters."""
    if ch not in MT_LAST_VERSE or not (1 <= v <= MT_LAST_VERSE[ch]):
        return None
    if ch == 8 and v == 23:
        return (9, 1)
    if ch == 9:
        return (9, v + 1)
    if ch == 64:
        return (64, v + 1)
    return (ch, v)


def mt_to_web_all(ch: int, v: int) -> list[tuple[int, int]]:
    """EVERY WEB verse an MT verse maps to. Exactly one everywhere except the
    split verse MT 63:19 -> [WEB 63:19, WEB 64:1]."""
    w = mt_to_web(ch, v)
    if w is None:
        return []
    if (ch, v) == SPLIT_MT:
        return [(63, 19), (64, 1)]
    return [w]


def language_of(ch: int, v: int) -> str:
    return "Hebrew"                     # no Aramaic zones in Isa


def nfd(s: str) -> str:
    return unicodedata.normalize("NFD", s)


def strip_accents(s: str) -> str:
    return ACCENTS.sub("", nfd(s))


def skeleton(s: str) -> str:
    """Consonantal skeleton; maqaf becomes SPACE so consonantal sweeps are
    maqaf-agnostic. Final letters preserved (NB the MT 9:6 medial final-mem
    survives here exactly as written — see the TOOLKIT hazard catalog)."""
    return POINTS.sub("", nfd(s)).replace("־", " ")


def expand_ref_token(tok: str, last_verse: dict[int, int] | None = None) -> list[tuple[int, int]]:
    """'Isa.2.7' or 'Isa.2.7-Isa.3.5' or 'Isa.8.1-14' -> [(c,v), ...].
    NON-IDENTITY BOOK: WEB and MT are DIFFERENT ref spaces in chs 8-9 and
    63-64. The default space is WEB; pass last_verse=MT_LAST_VERSE for oshb:
    refs. The expansion never converts between spaces — use
    web_to_mt()/mt_to_web_all() per verse for that."""
    lv = last_verse or LAST_VERSE
    tok = tok.strip()
    m = re.match(r"^Isa\.(\d+)\.(\d+)(?:-(?:Isa\.)?(\d+)(?:\.(\d+))?)?$", tok)
    if not m:
        return []
    c1, v1 = int(m.group(1)), int(m.group(2))
    if m.group(3) is None:
        return [(c1, v1)]
    if m.group(4) is None:                     # Isa.8.1-14 (same-chapter shorthand)
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
    book: the key spaces DIVERGE in chs 8-9 and 63-64 — always use each
    entry's 'mt'/'web' back-reference or the crosswalk functions, never bare
    same-number assumptions. The split verse MT 63:19's entry carries BOTH
    WEB back-references."""
    web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
    oshb = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
    return web, oshb


def load_pmarks() -> dict:
    """MT-keyed inventories. WLC Isa carries the campaign's LARGEST parashah
    layer so far: 41 PE + 168 SAMEKH segs (Prophets: parashah layer is
    TIER-3 WEAK corroboration under the owner addendum
    (parashah_in_prophets_or_writings) — never a driver, single-witness
    disclosure required on every citation, PE never conflated with SAMEKH;
    absence is NEVER counterevidence). Also: paseq (95 segs; seg layer, NOT
    quotable bytes, COUNT-ONLY), kq (53 notes over 49 verses — the
    campaign's largest K/Q inventory, incl. TWO INSIDE offset zone A: MT 9:2
    and the לםרבה pair at MT 9:6), exactly ONE x-small seg (small NUN at MT
    44:14 — the book's only special letter; every OTHER special-letter claim
    is a fabrication), NO selah / large-letter / suspended / reversed-nun
    segs. Keys are MT refs: map WEB spans through web_to_mt() before
    lookups; remember MT 63:19 has TWO WEB halves."""
    return json.loads((SPBOOK / "pmarks_Isa.json").read_text(encoding="utf-8"))


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
