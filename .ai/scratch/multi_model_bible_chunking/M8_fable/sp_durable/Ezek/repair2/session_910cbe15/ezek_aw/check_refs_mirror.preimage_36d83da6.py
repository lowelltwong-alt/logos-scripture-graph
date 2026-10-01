#!/usr/bin/env python3
"""Refs-mirror checker: every Ezek verse argued in a row's prose must appear in
that row's boundary_evidence_refs (as web: or oshb:, ranges expanded).

EZEK NOTE: Ezek is NOT an identity book (byte-proven at Phase 0) and carries
EXACTLY ONE offset zone - pure renumbering, NO split: MT 21:1-5 = WEB 20:45-49
with MT 21:6-37 = WEB 21:1-32. The non-identity arms below are LIVE in chs
20-21 — the witness-prefix-aware matching (rev-round e) and the MT-qualifier
conversion are exactly what keeps an MT-numbered token from mirroring an
argued WEB verse of the same numerals in the zone. MT-side tokens expand
through mt_to_web_all(), which returns exactly ONE WEB ref everywhere in
Ezek (injective crosswalk; the split-aware machinery of prior books
degrades to plain single mirroring here).

All comparison happens in WEB space: oshb:-prefixed tokens and "MT n:m"
qualifiers are MT-numbered and are converted via mt_to_web before comparison;
bare Ezek.C.V tokens and bare C:V colon cites are read as WEB numbering
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
 e) WITNESS-PREFIX-AWARE matching: an unprefixed Ezek.C.V token inside a refs
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
# #e13 R2: every arithmetic consumer ASSERTS the numbering face it expects. LAST_VERSE is built from
# verse_inventory.json, which previously carried a face and declared none - the silence broke four separate
# adjacency computations in a consumer and could not be detected from inside one.
def _assert_declared_face(expected="WEB"):
    import json as _json
    from pathlib import Path as _P
    inv = _json.loads((_P(__file__).resolve().parent.parent / "verse_inventory.json")
                      .read_text(encoding="utf-8"))
    got = inv.get("numbering_face")
    if got != expected:
        raise SystemExit("REFUSED: this tool does verse arithmetic on the %s face and verse_inventory.json "
                         "declares %r. A face mismatch is the wrong verse, not a rounding error." % (expected, got))


from ezek_lib import (LAST_VERSE, MT_LAST_VERSE, PSALM_RULES, expand_ref_token,
                    mt_to_web_all)

SKIP_KEYS = {"boundary_evidence_refs", "span", "osis_start", "osis_end",
             "decision_id", "chunk_id", "attempt_id",
             # Campaign schema (patch prov_tools_p1, 2026-08-18, P04 ablation
             # finding, carried to Jer at Phase 0 per lesson b, inherited by Ezek):
             # parent_collection's MANDATED value is a range-shaped string
             # (e.g. "F1 Ezek.1.1-Ezek.1.11") — structural metadata, not an
             # argued citation; without this skip every row flags ~all of its
             # section's verses as unmirrored.
             "parent_collection", "writer_part", "writer_decision_id",
             "writer_attempt_id"}
RANGE = re.compile(r"(oshb:)?Ezek\.\d+\.\d+(?:-(?:Ezek\.)?\d+(?:\.\d+)?)?")
# rev-round (e): witness prefixes with optional whitespace, so a token can be
# attributed to the witness that governs it even when written "oshb: Ezek.x.y"
PREFIXED = re.compile(r"\b(web|oshb):\s*(?=Ezek\.)|(?<![\w.])(Ezek\.\d+\.\d+)")
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
    """'MT n:m(-k)' / 'MT n:m-n:k' qualifiers -> WEB pairs via mt_to_web_all
    (exactly one WEB ref per MT verse in Ezek - injective crosswalk)."""
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
                    out.update(mt_to_web_all(ch, v))
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
    # mt_to_web_all: exactly one WEB ref per MT verse in Ezek (injective)
    return [w for c, v in pairs for w in mt_to_web_all(c, v)]


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


ENTRY_SCAN = re.compile(r"\b(web|oshb):\s*|Ezek\.\d+\.\d+(?:-(?:Ezek\.)?\d+(?:\.\d+)?)?")


def entry_pairs(ref: str) -> list[tuple[int, int]]:
    """WEB-space verses one refs ENTRY contributes.

    OL-c18 fix retained: the witness prefix is read PER TOKEN, so a dual-cite
    entry ("web:Ezek.20.45 = oshb:Ezek.21.1") never lets its MT token stand as WEB
    coverage. REV-ROUND (e): a token written WITHOUT a prefix inherits the
    entry's last explicit prefix (covers "oshb: Ezek.21.6" and continuation
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
    M8-Jer-404 class (a Jeremiah row): refs that exist only to support a sweep-failed claim are
    invisible to every other Tier-0 gate). NEVER a flag — author triage."""
    out = []
    skip = own_span | seam_pairs(own_span)
    for ref in row.get("boundary_evidence_refs", []):
        pairs = set(entry_pairs(ref))
        if not pairs or pairs & argued or pairs & skip:
            continue
        out.append({"ref": ref,
                    "verses_web": [f"Ezek.{c}.{v}" for c, v in sorted(pairs)][:12]})
    return out


# ---------------------------------------------------------------- A4 window (ruling #e12)
def _prev_verse(ch, vs):
    """The verse immediately BEFORE (ch, vs), crossing a chapter boundary correctly."""
    if vs > 1:
        return (ch, vs - 1)
    return (ch - 1, LAST_VERSE[ch - 1]) if (ch - 1) in LAST_VERSE else None


def _next_verse(ch, vs):
    """The verse immediately AFTER (ch, vs), crossing a chapter boundary correctly."""
    if vs < LAST_VERSE.get(ch, 0):
        return (ch, vs + 1)
    return (ch + 1, 1) if (ch + 1) in LAST_VERSE else None


def a4_window(own_span):
    """A4's window: the row's whole span PLUS the onset-seam verse and the close-seam verse.

    #e13 R1 removed the own_span subtraction upstream, so the window is no longer reducible to the two
    seam verses - it CONTAINS the span, which is what makes an in-span argued-but-unmirrored verse a
    defect the member can see. Four peers measured that class by hand while the member could not reach it.

    Returns (window, diagnostics). A boundary that does not exist - the book's first or last verse has no
    neighbour - is reported in the diagnostics and NEVER silently collapses the window: the previous guard
    binned every reference out-of-window whenever either boundary was unresolvable, which cost the one row
    whose span ends at the book's final verse all of its references.
    """
    if not own_span:
        return set(), {"resolved": False, "why": "the row has no resolvable span"}
    ordered = sorted(own_span)
    lo, hi = _prev_verse(*ordered[0]), _next_verse(*ordered[-1])
    win = set(ordered)
    diag = {"resolved": True, "span_verses": len(ordered),
            "onset_seam": ("Ezek.%d.%d" % lo) if lo else "NONE - the span opens the book",
            "close_seam": ("Ezek.%d.%d" % hi) if hi else "NONE - the span closes the book"}
    if lo is not None:
        win.add(lo)
    if hi is not None:
        win.add(hi)
    if lo is None or hi is None:
        diag["boundary_at_the_book_edge"] = True
    return win, diag


def _a4_selftest():
    """Vectors for the window, including the chapter-boundary cases naive arithmetic gets wrong."""
    cases = []
    # mid-chapter span
    span = {(16, 24), (16, 25), (16, 34)}
    w, d = a4_window(span)
    cases.append(("the window CONTAINS the span", span <= w))
    cases.append(("and adds both seam verses", {(16, 23), (16, 35)} <= w))
    cases.append(("a verse two away from the span is outside the window", (40, 23) not in w))
    # a span opening a chapter reaches back across the boundary
    w, d = a4_window({(16, 1), (16, 2)})
    cases.append(("a span opening a chapter finds its onset seam in the previous chapter",
                  (15, LAST_VERSE[15]) in w))
    # a span closing a chapter reaches forward across the boundary
    w, d = a4_window({(15, LAST_VERSE[15] - 1), (15, LAST_VERSE[15])})
    cases.append(("a span closing a chapter finds its close seam in the next chapter", (16, 1) in w))
    # BOOK EDGES: the boundary is reported, and the span is NEVER swallowed. This is the regression for the
    # guard that binned every reference out-of-window whenever a boundary could not be resolved - it cost the
    # one row whose span ends at the book's final verse all of its references.
    w, d = a4_window({(1, 1)})
    cases.append(("a span opening the book keeps its own verse in the window", (1, 1) in w))
    cases.append(("and reports that it has no onset seam rather than collapsing",
                  d["onset_seam"].startswith("NONE") and d.get("boundary_at_the_book_edge") is True))
    last_ch = max(LAST_VERSE)
    w, d = a4_window({(last_ch, LAST_VERSE[last_ch])})
    cases.append(("a span closing the book keeps its own verse in the window",
                  (last_ch, LAST_VERSE[last_ch]) in w))
    cases.append(("and reports that it has no close seam rather than collapsing",
                  d["close_seam"].startswith("NONE") and d.get("boundary_at_the_book_edge") is True))
    w, d = a4_window(set())
    cases.append(("an unresolvable span reports unresolved rather than returning a silent empty window",
                  w == set() and d["resolved"] is False))
    width = max(len(n) for n, _ in cases)
    for n, ok in cases:
        print("  %s  %s" % ("PASS" if ok else "FAIL", n.ljust(width)))
    bad = [n for n, ok in cases if not ok]
    print("\na4 window selftest: %d/%d passed" % (len(cases) - len(bad), len(cases)))
    return 1 if bad else 0


def main() -> int:
    _assert_declared_face("WEB")
    flags = []
    orphan_warns = []
    far_side_refs = []
    n = 0
    for f in sys.argv[1:]:
        for row in rows_from(Path(f)):
            if not isinstance(row, dict) or "boundary_evidence_refs" not in row:
                continue
            n += 1
            own_span = set(expand_ref_token(str(row.get("span", "")).replace("web:", "")))
            span_chapters = {c for c, _ in own_span}
            argued = prose_refs(row, span_chapters)
            # #e13 R1: own_span is NOT subtracted. An argued verse the reference list omits is a candidate
            # defect whether it lies inside the span or at either seam; only verses OUTSIDE the window are
            # discharged. This is the change that makes the in-span class visible at all.
            missing = sorted(argued - covered(row))
            window, win_diag = a4_window(own_span)
            in_window = [p for p in missing if p in window]
            far_side = [p for p in missing if p not in window]
            in_span = [p for p in in_window if p in own_span]
            at_seam = [p for p in in_window if p not in own_span]
            if in_window:
                flags.append({"file": Path(f).name,
                              "decision_id": row.get("decision_id", "?"),
                              "argued_but_unmirrored": [f"Ezek.{c}.{v}" for c, v in in_window],
                              "in_span": [f"Ezek.{c}.{v}" for c, v in in_span],
                              "at_a_seam": [f"Ezek.{c}.{v}" for c, v in at_seam],
                              "window": dict(win_diag,
                                             rule="A4 as ruled in #e13 R1: the window is the span plus both "
                                                  "seam verses; own_span is not subtracted")})
            if far_side:
                far_side_refs.append({"file": Path(f).name,
                                      "decision_id": row.get("decision_id", "?"),
                                      "argued_but_unmirrored_far_side": [f"Ezek.{c}.{v}"
                                                                         for c, v in far_side],
                                      "note": "outside the A4 window - NOT a defect (#e12 ruling A4)"})
            orphans = orphan_refs(row, argued, own_span)
            if orphans:
                orphan_warns.append({"file": Path(f).name,
                                     "decision_id": row.get("decision_id", "?"),
                                     "orphan_refs": orphans})
    print(json.dumps({"rows_checked": n, "flag_count": len(flags), "flags": flags,
                      "a4_window_rule": "a refs_mirror flag is a defect only for a verse inside "
                                        "[first-1, last+1]; range expansions and comparison verses "
                                        "outside that window are not defects (#e12 ruling A4)",
                      "far_side_ref_rows": len(far_side_refs),
                      "far_side_ref_count": sum(len(r["argued_but_unmirrored_far_side"])
                                                for r in far_side_refs),
                      "far_side_refs": far_side_refs,
                      "orphan_ref_warn_rows": len(orphan_warns),
                      "orphan_ref_warn_count": sum(len(o["orphan_refs"])
                                                   for o in orphan_warns),
                      "orphan_ref_warns": orphan_warns,
                      "status": "GREEN" if not flags else "FLAGS"},
                     ensure_ascii=False, indent=1))
    return 1 if flags else 0


if __name__ == "__main__":
    if "--a4-selftest" in sys.argv:
        raise SystemExit(_a4_selftest())
    raise SystemExit(main())
