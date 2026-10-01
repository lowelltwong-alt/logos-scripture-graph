#!/usr/bin/env python3
"""Refs-mirror checker: every Eccl verse argued in a row's prose must appear in
that row's boundary_evidence_refs (as web: or oshb:, ranges expanded).

ECCL NOTE: Eccl is NOT an identity book (byte-proven at Phase 0): MT 4:17 =
WEB 5:1 and MT 5:1-19 = WEB 5:2-20. The non-identity arms below are LIVE in
chs 4-5 — the witness-prefix-aware matching (rev-round e) and the
MT-qualifier conversion are exactly what keeps an MT-numbered token from
mirroring an argued WEB verse of the same numerals in the offset zone.

All comparison happens in WEB space: oshb:-prefixed tokens and "MT n:m"
qualifiers are MT-numbered and are converted via mt_to_web before comparison;
bare Eccl.C.V tokens and bare C:V colon cites are read as WEB numbering
(validated against WEB ranges; invalid readings are skipped, not flagged).

Prose fields scanned: every string field EXCEPT boundary_evidence_refs entries,
span fields, and id fields.

IN-CHAPTER "VERSE N" ARM (lesson j): bare "verse 7" / "v. 7" / "vv. 3-5"
mentions are resolved against the row's own span psalm (only when the span
sits in exactly ONE psalm — multi-psalm spans skip this arm) and must be
mirrored like any other argued verse. Bare numbers are read as WEB numbering.

REV-ROUND ARMS (attempt revround_tools_ps_r1):
 a) VERSE_WORD also captures conjunction/comma LISTS ("vv7 and 9", "vv1, 3",
    "vv. 1-3, 5") capturing every numeral. A DASH join is a RANGE; a comma or
    "and" join is a LIST — the peer-diagnosed "vv1, 3" over-capture (which
    charged the unargued middle verse) is fixed by construction.
 b) MT_COLON accepts chapter-qualified range ends ("MT 88:11-88:13"); the old
    single-end-number pattern read the trailing chapter as a verse.
 c) the no-space fix is retained (optional period, OPTIONAL space after the
    keyword): "vv.6-7" and "v.7" stay visible.
 d) ORPHAN-REFS ARM (WARN only, never a flag): a boundary_evidence_refs entry
    whose verses are argued nowhere in prose AND lie outside the row's own
    span is reported in orphan_ref_warns — refs that carry a claim the prose
    no longer makes are invisible to every other Tier-0 gate.
 e) WITNESS-PREFIX-AWARE matching: an unprefixed Eccl.C.V token inside a refs
    entry inherits the entry's last explicit witness prefix instead of
    defaulting to WEB, so an oshb: (MT-numbered) token can never mirror an
    argued web: verse of the same numerals in a NON-IDENTITY psalm.
Usage: check_refs_mirror.py rows.jsonl [more...]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eccl_lib import (LAST_VERSE, MT_LAST_VERSE, PSALM_RULES, expand_ref_token,
                    mt_to_web)

SKIP_KEYS = {"boundary_evidence_refs", "span", "osis_start", "osis_end",
             "decision_id", "chunk_id", "attempt_id",
             # Campaign schema (patch prov_tools_p1, 2026-08-18, P04 ablation
             # finding, carried to Eccl at Phase 0 per lesson b):
             # parent_collection's MANDATED value is a range-shaped string
             # (e.g. "F1 Eccl.1.1-Eccl.1.11") — structural metadata, not an
             # argued citation; without this skip every row flags ~all of its
             # section's verses as unmirrored.
             "parent_collection", "writer_part", "writer_decision_id",
             "writer_attempt_id"}
RANGE = re.compile(r"(oshb:)?Eccl\.\d+\.\d+(?:-(?:Eccl\.)?\d+(?:\.\d+)?)?")
# rev-round (e): witness prefixes with optional whitespace, so a token can be
# attributed to the witness that governs it even when written "oshb: Eccl.x.y"
PREFIXED = re.compile(r"\b(web|oshb):\s*(?=Eccl\.)|(?<![\w.])(Eccl\.\d+\.\d+)")
COLON = re.compile(r"\b(\d{1,3}):(\d{1,3})(?:[-–](\d{1,3})(?::(\d{1,3}))?)?\b")
# rev-round (b): chapter-qualified range ends ("MT 88:11-88:13") — the old
# pattern read the "88" of the end ref as a VERSE and over-captured 11..18
MT_COLON = re.compile(r"\bMT\s+(\d{1,3})[:.](\d{1,3})"
                      r"(?:\s*[-–]\s*(?:(\d{1,3})[:.])?(\d{1,3}))?")
# OL-c16 fix: the previous pattern could not match the doubled "vv." form.
# rev-round (a): the keyword now governs a whole numeral EXPRESSION — dash
# joins are ranges, comma/"and" joins are lists.
VERSE_WORD = re.compile(
    r"\b(?:vv?|verses?)\.?\s*"
    r"(\d{1,3}(?:\s*(?:[-–]\s*\d{1,3}|,\s*\d{1,3}|\s+and\s+\d{1,3}))*)", re.I)
VERSE_PART = re.compile(r"\d{1,3}|[-–]|,|\band\b", re.I)
# a numeral followed by one of these is a COUNT/SIZE, not a verse number
COUNT_UNIT = re.compile(r"\s*(?:verses?|times|instances?|occurrences?|tokens?|"
                        r"marks?|words?|letters?|cola|colon|hemistichs?|"
                        r"paseq|selah|segs?)\b", re.I)


def rows_from(p: Path):
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    data = json.loads(text)
    if isinstance(data, dict):
        if "decisions" in data:
            return data["decisions"]
        return [v for v in data.values() if isinstance(v, dict)]
    return data


def colon_refs(s: str) -> set[tuple[int, int]]:
    """Bare C:V / C:V-V / C:V-C:V verse citations, WEB space (validated against
    WEB ranges). Colon cites inside an 'MT n:m' qualifier are handled by
    mt_colon_refs and skipped here."""
    mt_spans = [(m.start(), m.end()) for m in MT_COLON.finditer(s)]
    out = set()
    for m in COLON.finditer(s):
        if any(a <= m.start() < b for a, b in mt_spans):
            continue
        c1, v1 = int(m.group(1)), int(m.group(2))
        if c1 not in LAST_VERSE or not (1 <= v1 <= LAST_VERSE[c1]):
            continue
        if m.group(3) is None:
            out.add((c1, v1))
            continue
        if m.group(4) is None:
            c2, v2 = c1, int(m.group(3))
        else:
            c2, v2 = int(m.group(3)), int(m.group(4))
        if c2 not in LAST_VERSE or not (1 <= v2 <= LAST_VERSE[c2]) or (c2, v2) < (c1, v1):
            out.add((c1, v1))
            continue
        for c in range(c1, c2 + 1):
            lo = v1 if c == c1 else 1
            hi = v2 if c == c2 else LAST_VERSE[c]
            out.update((c, v) for v in range(lo, hi + 1))
    return out


def mt_colon_refs(s: str) -> set[tuple[int, int]]:
    """'MT n:m(-k)' / 'MT n:m-n:k' qualifiers -> WEB pairs via mt_to_web."""
    out = set()
    for m in MT_COLON.finditer(s):
        c, v1 = int(m.group(1)), int(m.group(2))
        c2 = int(m.group(3)) if m.group(3) else c
        v2 = int(m.group(4)) if m.group(4) else v1
        if (c2, v2) < (c, v1):
            c2, v2 = c, v1                     # malformed end: read start only
        for ch in range(c, c2 + 1):
            lo = v1 if ch == c else 1
            hi = v2 if ch == c2 else MT_LAST_VERSE.get(ch, 0)
            for v in range(lo, hi + 1):
                if ch in MT_LAST_VERSE and 1 <= v <= MT_LAST_VERSE[ch]:
                    w = mt_to_web(ch, v)
                    if w:
                        out.add(w)
    return out


def parse_verse_expr(expr: str) -> set[int]:
    """'6-7' -> {6,7} (RANGE); '1, 3' -> {1,3} and '7 and 9' -> {7,9} (LISTS —
    never the unargued middle verse); '1-3, 5' -> {1,2,3,5}.

    GUARDS (measured against rows_v1, which produced two false charges without
    them): a continuation numeral counts only when it ASCENDS ("2 at verse 13,
    3 at verse 14" — the 3 is a paseq COUNT, not verse 3; "verses 10-11, 2
    verses" — the 2 is a span SIZE), and a numeral immediately followed by a
    count-unit noun is dropped (see COUNT_UNIT)."""
    out: set[int] = set()
    prev = None
    pending_range = False
    for m in VERSE_PART.finditer(expr):
        tok = m.group(0)
        if tok.isdigit():
            n = int(tok)
            if COUNT_UNIT.match(expr[m.end():]):
                pending_range = False
                continue
            if prev is None:
                out.add(n)
            elif pending_range:
                if n > prev:
                    out.update(range(prev, n + 1))
                else:
                    pending_range = False
                    continue
            elif n > prev:
                out.add(n)
            else:
                continue                        # descending = not a verse list
            pending_range = False
            prev = n
        elif tok in ("-", "–"):
            pending_range = True
        else:                                   # comma or "and" — LIST join
            pending_range = False
    return out


def verse_word_refs(s: str, span_chapters: set[int]) -> set[tuple[int, int]]:
    """Lesson-j arm: bare 'verse N' / 'vv. N-M' / 'vv7 and 9' / 'vv1, 3'
    resolved against the row's single span psalm (WEB numbering; skipped for
    multi-psalm spans)."""
    if len(span_chapters) != 1:
        return set()
    (c,) = span_chapters
    out = set()
    for m in VERSE_WORD.finditer(s):
        for v in parse_verse_expr(m.group(1)):
            if c in LAST_VERSE and 1 <= v <= LAST_VERSE[c]:
                out.add((c, v))
    return out


def token_pairs_web(tok: str, is_oshb: bool) -> list[tuple[int, int]]:
    if not is_oshb:
        return expand_ref_token(tok)
    pairs = expand_ref_token(tok, MT_LAST_VERSE)
    return [w for c, v in pairs if (w := mt_to_web(c, v))]


def prose_refs(row, span_chapters: set[int]) -> set[tuple[int, int]]:
    out = set()

    def walk(o, key=None):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in SKIP_KEYS:
                    continue
                walk(v, k)
        elif isinstance(o, list):
            for v in o:
                walk(v, key)
        elif isinstance(o, str):
            for m in RANGE.finditer(o):
                tok = m.group(0)
                is_oshb = tok.startswith("oshb:")
                out.update(token_pairs_web(tok.replace("oshb:", ""), is_oshb))
            out.update(colon_refs(o))
            out.update(mt_colon_refs(o))
            out.update(verse_word_refs(o, span_chapters))
    walk(row)
    return out


ENTRY_SCAN = re.compile(r"\b(web|oshb):\s*|Eccl\.\d+\.\d+(?:-(?:Eccl\.)?\d+(?:\.\d+)?)?")


def entry_pairs(ref: str) -> list[tuple[int, int]]:
    """WEB-space verses one refs ENTRY contributes.

    OL-c18 fix retained: the witness prefix is read PER TOKEN, so a dual-cite
    entry ("web:Eccl.42.5 = oshb:Eccl.42.6") never lets its MT token stand as WEB
    coverage. REV-ROUND (e): a token written WITHOUT a prefix inherits the
    entry's last explicit prefix (covers "oshb: Eccl.108.6" and continuation
    tokens) instead of defaulting to WEB — that default is what let an
    MT-numbered token mirror an argued WEB verse of the same numerals in a
    non-identity psalm ("mirror satisfied lexically, not semantically")."""
    out: list[tuple[int, int]] = []
    cur_oshb = False
    for m in ENTRY_SCAN.finditer(ref):
        if m.group(1):
            cur_oshb = m.group(1) == "oshb"
            continue
        out.extend(token_pairs_web(m.group(0), cur_oshb))
    return out


def covered(row) -> set[tuple[int, int]]:
    out = set()
    for ref in row.get("boundary_evidence_refs", []):
        out.update(entry_pairs(ref))
    return out


def seam_pairs(own_span: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """The structurally-mandated seam verses of a span (front seam, rear seam,
    and the title pseudo-verses on either side). These are boundary evidence by
    construction, so they are NEVER orphans even when prose never numbers
    them; without this exclusion the arm reports 81 hits, 69 of them seams."""
    if not own_span:
        return set()
    so = sorted(own_span)
    c0, v0 = so[0]
    c1, v1 = so[-1]
    out = {(c0, 0), (c1 + 1, 0)}
    out.add((c0, v0 - 1) if v0 > 1 else (c0 - 1, LAST_VERSE.get(c0 - 1, 0)))
    out.add((c1, v1 + 1) if v1 < LAST_VERSE.get(c1, 0) else (c1 + 1, 1))
    return out


def orphan_refs(row, argued: set[tuple[int, int]],
                own_span: set[tuple[int, int]]) -> list[dict]:
    """WARN-only arm: refs entries with no prose function. An entry whose
    verses are argued nowhere in prose, lie outside the row's own span AND are
    not its seam verses is carrying a claim the prose does not make (the
    M8-Eccl-404 class: refs that exist only to support a sweep-failed claim are
    invisible to every other Tier-0 gate). NEVER a flag — author triage."""
    out = []
    skip = own_span | seam_pairs(own_span)
    for ref in row.get("boundary_evidence_refs", []):
        pairs = set(entry_pairs(ref))
        if not pairs or pairs & argued or pairs & skip:
            continue
        out.append({"ref": ref,
                    "verses_web": [f"Eccl.{c}.{v}" for c, v in sorted(pairs)][:12]})
    return out


def main() -> int:
    flags = []
    orphan_warns = []
    n = 0
    for f in sys.argv[1:]:
        for row in rows_from(Path(f)):
            if not isinstance(row, dict) or "boundary_evidence_refs" not in row:
                continue
            n += 1
            own_span = set(expand_ref_token(str(row.get("span", "")).replace("web:", "")))
            span_chapters = {c for c, _ in own_span}
            argued = prose_refs(row, span_chapters)
            missing = sorted(argued - covered(row) - own_span)
            if missing:
                flags.append({"file": Path(f).name,
                              "decision_id": row.get("decision_id", "?"),
                              "argued_but_unmirrored": [f"Eccl.{c}.{v}" for c, v in missing]})
            orphans = orphan_refs(row, argued, own_span)
            if orphans:
                orphan_warns.append({"file": Path(f).name,
                                     "decision_id": row.get("decision_id", "?"),
                                     "orphan_refs": orphans})
    print(json.dumps({"rows_checked": n, "flag_count": len(flags), "flags": flags,
                      "orphan_ref_warn_rows": len(orphan_warns),
                      "orphan_ref_warn_count": sum(len(o["orphan_refs"])
                                                   for o in orphan_warns),
                      "orphan_ref_warns": orphan_warns,
                      "status": "GREEN" if not flags else "FLAGS"},
                     ensure_ascii=False, indent=1))
    return 1 if flags else 0


if __name__ == "__main__":
    raise SystemExit(main())
