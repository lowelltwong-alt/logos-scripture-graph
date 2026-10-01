#!/usr/bin/env python3
"""Shared library for the Ps OW-2 AUDIT toolkit (Tier-0, deterministic).

REBUILT 2026-09-03 for OW-2 item 2 from the raw witnesses. The original Ps
campaign toolkit lived in the 6a933340 session scratchpad, which no longer
exists on disk and was never mirrored durable (sp_durable/Ps holds only the
frozen cycle state + deliverables). Same lineage and API as the Song r3 lib
(song_lib.py) so the book-agnostic mechanical tools adapt unchanged.

Every audit brief points here. USE these tools; do NOT rebuild them.

NUMBERING (THE book hazard): Ps is NOT an identity book. Byte-PROVEN by
build_offset_map.py (per-psalm verse counts under the rule set from both
witnesses' bytes; title-presence consistency; Selah + proper-name content
anchors at the crosswalk-mapped MT refs; a falsification probe showing the
identity mapping fails hundreds of anchor checks; seam byte-review
assertions; and a secondary shipped-corpus dual-cite consistency probe —
see ../web_mt_offset_map.json):
  87 psalms IDENTITY;
  58 psalms SHIFT+1 (MT counts the title as v1: WEB N:v = MT N:v+1);
   4 psalms SHIFT+2 (51, 52, 54, 60: MT vv1-2 are the title: WEB N:v = MT N:v+2);
  Ps 13 SPLIT (equal counts but WEB 13:1-4 = MT 13:2-5 and WEB 13:5 AND
   13:6 BOTH = MT 13:6 — both halves dual-cite oshb:Ps.13.6).
TITLE PSEUDO-VERSES: 116 psalms carry a WEB title line; the campaign
convention is web:Ps.N.0 for the title, which maps to oshb:Ps.N.1 (shift+1),
oshb:Ps.N.1-2 (shift+2), or is the PREFIX of oshb:Ps.N.1 in the 54 titled
IDENTITY psalms (there the MT v1 carries title + first line together).
Ps 119's 22 [SUPERSCRIPTION] markers are ACROSTIC LETTER HEADERS (WEB
typography, owner-addendum tier 4) — NOT titles; Ps.119.0 does not exist
and "superscription" is NEVER the word for them. WEB [MAJOR-SECTION: BOOK n]
lines are modern editorial book headings (tier 4) — cataloged in
../editorial_headings_web.json only so claims can be audited AGAINST
leaning on them.
web_to_mt()/mt_to_web()/mt_to_web_all()/web_to_mt_all() implement the
crosswalk RANGE-GUARDED — always use them, never hand-assume, in BOTH
directions. Convention: bare/web: refs + row spans = WEB; oshb:/pmarks = MT.

MARKS: WLC Psalms carries NO petuchah/setumah segs at all (byte-verified by
build_pmarks.py) — any PE/SAMEKH claim in Ps is a fabrication. Seg-layer
objects that DO exist (single-witness, inventory-cited, never quotable as
verse bytes): paseq, inverted nuns (x-reversednun; MT 107 as the bytes have
them), the suspended ayin at MT 80:14 (x-suspended). K/Q notes per the
inventory. Selah is VERSE TEXT in both witnesses (no witness tag needed;
span-scoped symmetry applies).

There are NO Aramaic zones in Ps (every OSHB morph code is H-prefixed;
verified from bytes by build_pmarks.py).

SKELETON NOTE (owner lesson, campaign-wide): skeleton() maps maqaf to a
SPACE so consonantal sweeps are not maqaf-vs-space sensitive. The staged
extract is MAQAF-FREE at every tier (the extractor serialized the XML's
x-maqqef segs as SPACE — 0 U+05BE codepoints book-wide). accent_stripped
RETAINS meteg (U+05BD) — it strips cantillation (U+0591-05AF) only.
Final-letter allography is preserved exactly; sweep per attested spelling.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent          # SP/Ps
BOOK = "Ps"

_inv = json.loads((SPBOOK / "verse_inventory.json").read_text(encoding="utf-8"))
LAST_VERSE = {int(c): n for c, n in _inv["chapters"].items()}
TOTAL_VERSES = sum(LAST_VERSE.values())          # 2461

_omap = json.loads((SPBOOK / "web_mt_offset_map.json").read_text(encoding="utf-8"))
MT_LAST_VERSE = {int(c): p["mt_verses"] for c, p in _omap["chapters"].items()}
MT_TOTAL_VERSES = sum(MT_LAST_VERSE.values())    # 2527

# Per-psalm rule table (the historical Ps-lineage name; the mechanical tools
# only test rule != "identity"). Rules: identity | shift1 | shift2 | split13.
PSALM_RULES = {int(k): {"rule": v["rule"], "web_verses": v["web_verses"],
                        "mt_verses": v["mt_verses"], "titled": v["titled"]}
               for k, v in _omap["chapters"].items()}
TITLED = {c for c, p in PSALM_RULES.items() if p["titled"]}

HEB_RUN = re.compile(r"[֑-״]+(?:[ ־][֑-״]+)*")
POINTS = re.compile(r"[֑-ׇ]")          # cantillation + vowels + meteg etc.
ACCENTS = re.compile(r"[֑-֯]")          # cantillation only (meteg RETAINED)
REF = re.compile(r"\bPs\.(\d+)\.(\d+)\b")


def _rule(ch: int) -> str | None:
    p = PSALM_RULES.get(ch)
    return p["rule"] if p else None


def title_mt_refs(ch: int) -> list[tuple[int, int]]:
    """MT verse(s) that carry the WEB title (web:Ps.N.0). shift1 -> [(N,1)];
    shift2 -> [(N,1),(N,2)]; titled identity -> [(N,1)] (the title is the
    PREFIX of MT v1); untitled -> []."""
    if ch not in TITLED:
        return []
    r = _rule(ch)
    if r == "shift2":
        return [(ch, 1), (ch, 2)]
    return [(ch, 1)]


def web_to_mt(ch: int, v: int) -> tuple[int, int] | None:
    """WEB (ch, v) -> MT (ch, v). Crosswalk, range-guarded: None if out of range.
    v == 0 is the WEB title pseudo-verse of a titled psalm -> its first MT
    verse (use web_to_mt_all for the +2 psalms' two-verse title)."""
    if ch not in LAST_VERSE:
        return None
    if v == 0:
        t = title_mt_refs(ch)
        return t[0] if t else None
    if not (1 <= v <= LAST_VERSE[ch]):
        return None
    r = _rule(ch)
    if r == "identity":
        return (ch, v)
    if r == "shift1":
        return (ch, v + 1)
    if r == "shift2":
        return (ch, v + 2)
    if r == "split13":
        return (13, v + 1) if v <= 4 else (13, 6)
    return None


def web_to_mt_all(ch: int, v: int) -> list[tuple[int, int]]:
    """Every MT verse a WEB verse (or title pseudo-verse) maps onto."""
    if v == 0:
        return title_mt_refs(ch)
    m = web_to_mt(ch, v)
    return [m] if m else []


def mt_to_web(ch: int, v: int) -> tuple[int, int] | None:
    """MT (ch, v) -> WEB (ch, v). Crosswalk, range-guarded. MT title verses
    map to the WEB title pseudo-verse (ch, 0). For the Ps 13 split, MT 13:6
    returns its FIRST WEB half (13, 5); use mt_to_web_all for both halves."""
    if ch not in MT_LAST_VERSE or not (1 <= v <= MT_LAST_VERSE[ch]):
        return None
    r = _rule(ch)
    if r == "identity":
        return (ch, v)
    if r == "shift1":
        return (ch, 0) if v == 1 else (ch, v - 1)
    if r == "shift2":
        return (ch, 0) if v <= 2 else (ch, v - 2)
    if r == "split13":
        if v == 1:
            return (13, 0)
        return (13, v - 1) if v <= 5 else (13, 5)
    return None


def mt_to_web_all(ch: int, v: int) -> list[tuple[int, int]]:
    """Every WEB verse an MT verse maps onto (MT 13:6 -> WEB 13:5 AND 13:6)."""
    if _rule(ch) == "split13" and v == 6:
        return [(13, 5), (13, 6)]
    w = mt_to_web(ch, v)
    return [w] if w else []


def language_of(ch: int, v: int) -> str:
    return "Hebrew"                     # no Aramaic zones in Ps


def nfd(s: str) -> str:
    return unicodedata.normalize("NFD", s)


def strip_accents(s: str) -> str:
    return ACCENTS.sub("", nfd(s))


def skeleton(s: str) -> str:
    """Consonantal skeleton; maqaf becomes SPACE so consonantal sweeps are
    maqaf-agnostic. Final letters preserved."""
    return POINTS.sub("", nfd(s)).replace("־", " ")


def expand_ref_token(tok: str, last_verse: dict[int, int] | None = None) -> list[tuple[int, int]]:
    """'Ps.3.1' or 'Ps.3.1-Ps.3.8' or 'Ps.8.1-9' or 'Ps.3.0' -> [(c,v), ...].
    NON-IDENTITY BOOK: WEB and MT are DIFFERENT ref spaces in 63 psalms. The
    default space is WEB (where v == 0 is a titled psalm's title
    pseudo-verse); pass last_verse=MT_LAST_VERSE for oshb: refs (v == 0 is
    never valid there). The expansion never converts between spaces — use
    web_to_mt()/mt_to_web() per verse for that."""
    lv = last_verse or LAST_VERSE
    web_space = lv is LAST_VERSE
    tok = tok.strip()
    m = re.match(r"^Ps\.(\d+)\.(\d+)(?:-(?:Ps\.)?(\d+)(?:\.(\d+))?)?$", tok)
    if not m:
        return []
    c1, v1 = int(m.group(1)), int(m.group(2))
    if m.group(3) is None:
        if v1 == 0:
            return [(c1, 0)] if (web_space and c1 in TITLED) else []
        return [(c1, v1)]
    if m.group(4) is None:                     # Ps.8.1-9 (same-chapter shorthand)
        c2, v2 = c1, int(m.group(3))
    else:
        c2, v2 = int(m.group(3)), int(m.group(4))
    out = []
    for c in range(c1, c2 + 1):
        lo = v1 if c == c1 else 1
        hi = v2 if c == c2 else lv.get(c, 0)
        hi = min(hi, lv.get(c, 0))     # clamp: an invalid range END never
        if lo == 0 and not (web_space and c in TITLED):
            lo = 1                     # expands coverage past real verses
        lo = max(lo, 0)
        out.extend((c, v) for v in range(lo, hi + 1))
    return out


def load_verse_maps():
    """verse_map_web is WEB-keyed (incl. Ps.N.0 title pseudo-verses for the
    116 titled psalms); verse_map_oshb is MT-keyed. NON-IDENTITY book: the
    key spaces DIVERGE in 63 psalms — always use each entry's 'mt'/'web'
    back-reference or the crosswalk functions, never bare same-number
    assumptions."""
    web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
    oshb = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
    return web, oshb


def load_pmarks() -> dict:
    """MT-keyed inventories (../pmarks_Ps.json, byte-extracted from the OSHB
    XML). WLC Psalms carries NO petuchah/setumah segs — any PE/SAMEKH claim is
    a fabrication. Present layers: paseq (seg layer, count-only, never
    quotable), inverted nuns (x-reversednun, MT 107 as the bytes have them),
    the suspended ayin (x-suspended) at MT 80:14, ketiv/qere notes. Keys are
    MT refs: map WEB spans through web_to_mt() before lookups."""
    return json.loads((SPBOOK / "pmarks_Ps.json").read_text(encoding="utf-8"))


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
