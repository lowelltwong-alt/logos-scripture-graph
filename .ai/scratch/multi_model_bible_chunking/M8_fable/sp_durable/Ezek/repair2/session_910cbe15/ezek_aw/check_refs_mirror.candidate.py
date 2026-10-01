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
        out.update(_colon_match_pairs(m))
    return out


def _colon_match_pairs(m) -> set[tuple[int, int]]:
    """The WEB verses ONE bare-cite match contributes. Extracted from colon_refs so the verse arm and the
    citation arm (string_citations) share one expansion and cannot drift apart."""
    out: set[tuple[int, int]] = set()
    c1, v1 = int(m.group(1)), int(m.group(2))
    if c1 not in LAST_VERSE or not (1 <= v1 <= LAST_VERSE[c1]):
        return out
    if m.group(3) is None:
        out.add((c1, v1))
        return out
    if m.group(4) is None:
        c2, v2 = c1, int(m.group(3))
    else:
        c2, v2 = int(m.group(3)), int(m.group(4))
    if c2 not in LAST_VERSE or not (1 <= v2 <= LAST_VERSE[c2]) or (c2, v2) < (c1, v1):
        out.add((c1, v1))                      # malformed range end: read the start only
        return out
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
        out.update(_mt_colon_match_pairs(m))
    return out


def _mt_colon_match_pairs(m) -> set[tuple[int, int]]:
    """The WEB verses ONE 'MT n:m' qualifier contributes. Extracted for the same reason as
    _colon_match_pairs: one expansion, two arms."""
    out: set[tuple[int, int]] = set()
    c, v1 = int(m.group(1)), int(m.group(2))
    c2 = int(m.group(3)) if m.group(3) else c
    v2 = int(m.group(4)) if m.group(4) else v1
    if (c2, v2) < (c, v1):
        c2, v2 = c, v1                         # malformed end: read start only
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


def parse_verse_expr_groups(expr: str) -> list[tuple[frozenset, str]]:
    """The SAME state machine as parse_verse_expr, returning the expression's CITATION GROUPS instead of a flat
    verse set: a dash join extends the current group (a range), a comma or "and" join STARTS A NEW ONE
    (DEF-A4-ARGUED clause 2). 'vv. 1-3, 5' -> [({1,2,3}, "range"), ({5}, "single")].

    The invariant that makes this safe to introduce: the UNION of the groups equals parse_verse_expr(expr)
    exactly. Citation granularity regroups what is argued; it must never change WHICH verses are argued. The
    selftest asserts it on vectors and analyze_row asserts it on every row of every run.

    Every guard of the original is preserved and for the same measured reasons: a non-ascending continuation
    numeral is a count, not a verse, and a numeral followed by a count-unit noun is a size.
    """
    groups: list[list[int]] = []
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
                groups.append([n])
            elif pending_range:
                if n > prev and groups:
                    groups[-1].extend(range(prev, n + 1))
                else:
                    pending_range = False
                    continue
            elif n > prev:
                groups.append([n])
            else:
                continue                        # descending = not a verse list
            pending_range = False
            prev = n
        elif tok in ("-", "\u2013"):
            pending_range = True
        else:                                   # comma or "and" - LIST join, so a NEW citation
            pending_range = False
    return [(frozenset(g), "range" if len(set(g)) > 1 else "single") for g in groups]


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


# --------------------------------------------------- CITATION granularity (#e14 Q1, DEF-A4-ARGUED)
# #e14 OVERRULED the framing that produced this section's need - "444 verses or the peers' 47" - as a false
# dichotomy produced by an INCOMPLETE P2. #e13 R1(i) had already ordered that a range counts as one citation;
# the orchestrator reported that clause applied when it was never implemented (queue E13-59, ledger E-31), and
# about 300 of the 444 verses were interior verses of argued ranges. Nothing in the corpus had to be chosen
# between; a clause had to be executed.
#
# DEF-A4-ARGUED, written by the controlling agent in #e14, binding for Ezekiel and proposed to method section 17:
#   1. an argued citation is any verse anchor a prose field carries, together with the assertion it anchors
#   2. a dash-range is ONE citation; a comma / "and" list is one citation PER MEMBER; the same verse-set cited
#      more than once in one row is ONE citation
#   3. mirrored = a refs entry covers its verse, or - for a range - either endpoint or the whole range,
#      compared in WEB space after witness conversion
#   4. an unmirrored citation with at least one verse inside the A4 window is a worklist item; one wholly
#      outside the window is far-side: recorded, never a defect (#e12 A4)
#   5. "argued" is NOT narrowed to "argued as evidence". The member judges MIRRORING; it never judges WEIGHT.
#
# ROLE tokens are not assigned here, and that is clause 6's point, not an omission: the evidentiary/narrative
# distinction peer_11 identified is real but is a distinction of ROLE, and it belongs in the entry a person
# writes and a reviewer reads. The vocabulary lives in this module because A4 is its home, so the worklist
# builder and the spot wave validate against ONE list.
ROLE_VOCABULARY = ("WARRANT-onset", "WARRANT-close", "WARRANT-rival", "WARRANT-absence-over-range",
                   "DISCLOSURE-kq", "DISCLOSURE-mark", "DISCLOSURE-paseq", "DISCLOSURE-note",
                   "DISCLOSURE-device", "QUOTE", "ANCHOR")
ROLE_UNASSIGNED = ("UNASSIGNED - the author assigns exactly one ROLE_VOCABULARY token; the member judges "
                   "mirroring, never weight (DEF-A4-ARGUED clause 5/6)")


def _cite(verses, raw, field, source):
    """One citation record. kind is a function of the VERSE SET and not of the surface form, so "vv. 4 and 5"
    and "4-5" are both ranges with the same endpoints - which is what clause 3's endpoint test needs. Endpoints
    are the min and max in WEB space; a witness conversion in the chs 20-21 divergence zone can make the
    expansion non-contiguous, and min/max remain the claim's two ends."""
    vs = frozenset(verses)
    if not vs:
        return None
    return {"verses": vs, "kind": "range" if len(vs) > 1 else "single",
            "endpoints": (min(vs), max(vs)), "raw": raw.strip()[:80], "field": field, "source": source}


def _fmt_cit(c) -> str:
    lo, hi = c["endpoints"]
    a = "Ezek.%d.%d" % lo
    return a if c["kind"] == "single" else "%s-Ezek.%d.%d" % (a, hi[0], hi[1])


def string_citations(s: str, span_chapters: set[int], field: str) -> list[dict]:
    """Every citation ONE prose string carries, through the same four parsers prose_refs uses, in the same
    order and with the same skips."""
    out = []
    for m in RANGE.finditer(s):
        tok = m.group(0)
        c = _cite(token_pairs_web(tok.replace("oshb:", ""), tok.startswith("oshb:")),
                  tok, field, "osis_token")
        if c:
            out.append(c)
    mt_spans = [(mm.start(), mm.end()) for mm in MT_COLON.finditer(s)]
    for m in COLON.finditer(s):
        if any(a <= m.start() < b for a, b in mt_spans):
            continue                            # an 'MT n:m' qualifier - the MT arm owns it
        c = _cite(_colon_match_pairs(m), m.group(0), field, "colon")
        if c:
            out.append(c)
    for m in MT_COLON.finditer(s):
        c = _cite(_mt_colon_match_pairs(m), m.group(0), field, "mt_colon")
        if c:
            out.append(c)
    if len(span_chapters) == 1:
        (ch,) = span_chapters
        for m in VERSE_WORD.finditer(s):
            for vs, _k in parse_verse_expr_groups(m.group(1)):
                c = _cite([(ch, v) for v in sorted(vs)
                           if ch in LAST_VERSE and 1 <= v <= LAST_VERSE[ch]],
                          m.group(0), field, "verse_word")
                if c:
                    out.append(c)
    return out


def prose_citations(row, span_chapters: set[int]) -> list[dict]:
    """Every argued citation in the row's prose, deduped by VERSE SET (clause 2: the same verse-set cited more
    than once in one row is one citation). The first occurrence keeps the record and counts its repeats, so the
    field the worklist points at is the one that names the citation first."""
    seen: dict[frozenset, dict] = {}
    order: list[frozenset] = []

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
            for c in string_citations(o, span_chapters, key or "?"):
                vs = c["verses"]
                if vs in seen:
                    seen[vs]["repeats"] += 1
                    continue
                c["repeats"] = 0
                seen[vs] = c
                order.append(vs)
    walk(row)
    return [seen[vs] for vs in order]


def citation_mirrored(cit: dict, cov: set) -> bool:
    """Clause 3. A single is mirrored when its verse is covered. A RANGE is mirrored when either endpoint or
    the whole range is covered - an endpoint suffices because a refs entry naming one end indexes the claim the
    range makes. This is the clause whose absence produced one flag per interior verse."""
    if cit["kind"] == "single":
        return next(iter(cit["verses"])) in cov
    lo, hi = cit["endpoints"]
    return lo in cov or hi in cov or cit["verses"] <= cov


def citation_mirrored_per_entry(cit: dict, row) -> bool:
    """Clause 3 read STRICTLY - ONE entry must do the covering by itself.

    Computed only to MEASURE whether the two readings differ on this corpus. The ruling's singular "a
    boundary_evidence_refs entry covers ... either endpoint" admits the strict reading; the union of entries
    admits the looser one; they differ only where two DIFFERENT entries cover the two endpoints of one range.
    The member reports every disagreement rather than letting the orchestrator pick a reading in silence."""
    for ref in row.get("boundary_evidence_refs", []):
        if citation_mirrored(cit, set(entry_pairs(ref))):
            return True
    return False


def classify_citation(cit: dict, window: set, own_span: set) -> str:
    """Clause 4 plus the ruling's three in-window classes. A citation whose in-window verses are ONLY seam
    verses is AT_SEAM even when its other verses lie far outside the window - those are the ruling's
    seam-touching ranges, and they are worklist items because a verse of theirs is in the window."""
    in_win = cit["verses"] & window
    if not in_win:
        return "FAR_SIDE"
    in_span = cit["verses"] & own_span
    return "MIXED" if (in_span and (in_win - own_span)) else ("IN_SPAN" if in_span else "AT_SEAM")


def analyze_row(row, fname="-") -> dict:
    """One row's A4 analysis at CITATION granularity. main and the selftest share this ONE path, so a fixture
    exercises exactly what a run does - the fixtures of the previous P2 could not have caught its omission
    because nothing tested the classification end to end."""
    own_span = set(expand_ref_token(str(row.get("span", "")).replace("web:", "")))
    span_chapters = {c for c, _ in own_span}
    cits = prose_citations(row, span_chapters)
    cov = covered(row)
    window, win_diag = a4_window(own_span)

    argued = prose_refs(row, span_chapters)
    union = set().union(*[c["verses"] for c in cits]) if cits else set()
    if union != argued:
        raise SystemExit("REFUSED: citation regrouping changed the ARGUED VERSE SET on %s - %d citation verses "
                         "against %d verse-arm verses; symmetric difference %r. Regrouping may change how "
                         "claims are counted and never which verses are argued."
                         % (row.get("decision_id", "?"), len(union), len(argued),
                            sorted(union ^ argued)[:8]))

    items, far, disagree = [], [], []
    for c in cits:
        union_m = citation_mirrored(c, cov)
        entry_m = citation_mirrored_per_entry(c, row)
        if union_m != entry_m:
            disagree.append({"decision_id": row.get("decision_id", "?"), "citation": _fmt_cit(c),
                             "union_reading": union_m, "strict_per_entry_reading": entry_m})
        if union_m:
            continue
        cls = classify_citation(c, window, own_span)
        rec = {"file": fname, "decision_id": row.get("decision_id", "?"),
               "citation": _fmt_cit(c), "kind": c["kind"], "class": cls,
               "verse_count": len(c["verses"]),
               # per-verse list KEPT AS A DIAGNOSTIC (O1) - it is what makes the citation auditable
               "verses_web": ["Ezek.%d.%d" % p for p in sorted(c["verses"])][:16],
               "field": c["field"], "raw": c["raw"], "source": c["source"],
               "repeats_in_row": c["repeats"], "role_token": ROLE_UNASSIGNED}
        (far if cls == "FAR_SIDE" else items).append(rec)

    # LEGACY VERSE-LEVEL AGGREGATE, kept so the citation figures stay comparable with the shipped member's
    # 444 / 131 / 817 and with the controlling agent's recount. Diagnostic only; never a flag.
    missing = sorted(argued - cov)
    legacy = {"missing_verses": len(missing),
              "in_window_verses": len([p for p in missing if p in window]),
              "in_span_verses": len([p for p in missing if p in window and p in own_span]),
              "at_seam_verses": len([p for p in missing if p in window and p not in own_span]),
              "far_side_verses": len([p for p in missing if p not in window])}
    return {"decision_id": row.get("decision_id", "?"), "items": items, "far_side": far,
            "mirror_reading_disagreements": disagree,
            "orphan_refs": orphan_refs(row, argued, own_span),
            "citations_read": len(cits), "argued_verses": len(argued),
            "window": win_diag, "legacy_verse_level": legacy}


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
    # ---- #e14 O2: the two RANGE fixtures. These are the regression for the clause that was reported applied
    # and never implemented. Fixture (a) is the one that matters: per-verse comparison produced one flag for
    # every interior verse of a range whose endpoint the refs list already named.
    SPAN = "Ezek.16.20-Ezek.16.30"
    row_a = {"decision_id": "FIXTURE-A", "span": SPAN,
             "boundary_evidence_refs": ["web:Ezek.16.26"],
             "rationale": "the unit runs 16:24-16:26 and closes there"}
    ra = analyze_row(row_a, "fixture")
    cases.append(("O2(a) a range with only its SECOND endpoint in refs yields ZERO flags",
                  not ra["items"] and not ra["far_side"]))
    cases.append(("O2(a) and the range was still READ as one citation over three verses",
                  ra["citations_read"] == 1 and ra["argued_verses"] == 3))
    cases.append(("O2(a) the legacy verse-level arm would have flagged the interior - which is the defect",
                  ra["legacy_verse_level"]["in_span_verses"] == 2))
    row_a1 = dict(row_a, decision_id="FIXTURE-A1", boundary_evidence_refs=["web:Ezek.16.24"])
    cases.append(("O2(a) the FIRST endpoint mirrors the range just as well",
                  not analyze_row(row_a1, "fixture")["items"]))

    row_b = dict(row_a, decision_id="FIXTURE-B", boundary_evidence_refs=["web:Ezek.16.20"])
    rb = analyze_row(row_b, "fixture")
    cases.append(("O2(b) a range with NEITHER endpoint in refs yields exactly ONE flag",
                  len(rb["items"]) == 1))
    cases.append(("O2(b) and the flag NAMES THE RANGE rather than its interior verses",
                  bool(rb["items"]) and rb["items"][0]["citation"] == "Ezek.16.24-Ezek.16.26"
                  and rb["items"][0]["kind"] == "range" and rb["items"][0]["verse_count"] == 3))
    cases.append(("O2(b) the flagged citation carries an UNASSIGNED role token, never a guessed one",
                  bool(rb["items"]) and rb["items"][0]["role_token"].startswith("UNASSIGNED")))

    # ---- clause 2: a comma / "and" list is one citation PER MEMBER, so a mirrored member discharges alone
    row_c = {"decision_id": "FIXTURE-C", "span": SPAN,
             "boundary_evidence_refs": ["web:Ezek.16.24"],
             "rationale": "see vv. 24 and 26 for the pair"}
    rc = analyze_row(row_c, "fixture")
    cases.append(("clause 2 a list is one citation per member: the mirrored member discharges, the other flags",
                  len(rc["items"]) == 1 and rc["items"][0]["citation"] == "Ezek.16.26"
                  and rc["citations_read"] == 2))

    # ---- clause 2: the same verse-set cited twice in one row is ONE citation
    row_d = {"decision_id": "FIXTURE-D", "span": SPAN,
             "boundary_evidence_refs": ["web:Ezek.16.20"],
             "rationale": "the unit runs 16:24-16:26",
             "strongest_rejected_alternative": "a cut at 16:24-16:26 was weighed and rejected"}
    rd = analyze_row(row_d, "fixture")
    cases.append(("clause 2 the same verse-set cited twice in one row is ONE citation, with repeats recorded",
                  rd["citations_read"] == 1 and len(rd["items"]) == 1
                  and rd["items"][0]["repeats_in_row"] == 1))

    # ---- clause 4: a citation wholly outside the window is far-side and never a defect; a range that reaches
    # the seam from outside IS a worklist item, because a verse of it is in the window
    row_e = {"decision_id": "FIXTURE-E", "span": SPAN, "boundary_evidence_refs": ["web:Ezek.16.20"],
             "rationale": "compare 16:5-16:8 elsewhere"}
    re_ = analyze_row(row_e, "fixture")
    cases.append(("clause 4 a citation wholly outside the window is FAR_SIDE, never a defect",
                  not re_["items"] and len(re_["far_side"]) == 1))
    row_f = {"decision_id": "FIXTURE-F", "span": SPAN, "boundary_evidence_refs": ["web:Ezek.16.20"],
             "rationale": "the material of 16:14-16:19 leads in"}
    rf = analyze_row(row_f, "fixture")
    cases.append(("clause 4 a range reaching the onset seam from outside IS a worklist item, class AT_SEAM",
                  len(rf["items"]) == 1 and rf["items"][0]["class"] == "AT_SEAM"))

    # ---- the regrouping invariant, on the expression parser directly
    for expr in ("1-3, 5", "24 and 26", "7-9", "10-11, 2 verses", "2 at verse 13, 3 at verse 14", "4"):
        g = parse_verse_expr_groups(expr)
        u = set().union(*[set(v) for v, _ in g]) if g else set()
        cases.append(("regrouping %r preserves the argued verse set exactly" % expr,
                      u == parse_verse_expr(expr)))
    cases.append(("a dash join is ONE group and a comma join is TWO",
                  [k for _, k in parse_verse_expr_groups("1-3, 5")] == ["range", "single"]))

    width = max(len(n) for n, _ in cases)
    for n, ok in cases:
        print("  %s  %s" % ("PASS" if ok else "FAIL", n.ljust(width)))
    bad = [n for n, ok in cases if not ok]
    print("\na4 window selftest: %d/%d passed" % (len(cases) - len(bad), len(cases)))
    return 1 if bad else 0


def main() -> int:
    _assert_declared_face("WEB")
    items, far_side, orphan_warns, disagree = [], [], [], []
    legacy = {"missing_verses": 0, "in_window_verses": 0, "in_span_verses": 0,
              "at_seam_verses": 0, "far_side_verses": 0}
    n = 0
    for f in sys.argv[1:]:
        for row in rows_from(Path(f)):
            if not isinstance(row, dict) or "boundary_evidence_refs" not in row:
                continue
            n += 1
            a = analyze_row(row, Path(f).name)
            items.extend(a["items"])
            far_side.extend(a["far_side"])
            disagree.extend(a["mirror_reading_disagreements"])
            for k in legacy:
                legacy[k] += a["legacy_verse_level"][k]
            if a["orphan_refs"]:
                orphan_warns.append({"file": Path(f).name, "decision_id": a["decision_id"],
                                     "orphan_refs": a["orphan_refs"]})

    def cnt(cls, kind=None):
        return len([i for i in items if i["class"] == cls and (kind is None or i["kind"] == kind)])

    def rows_with(*classes):
        return len({i["decision_id"] for i in items if i["class"] in classes})

    counts = {
        "in_span_citations": cnt("IN_SPAN"),
        "in_span_single_citations": cnt("IN_SPAN", "single"),
        "in_span_range_citations": cnt("IN_SPAN", "range"),
        "mixed_span_and_seam_citations": cnt("MIXED"),
        "at_seam_single_citations": cnt("AT_SEAM", "single"),
        "seam_touching_range_citations": cnt("AT_SEAM", "range"),
        "rows_with_an_in_span_or_mixed_citation": rows_with("IN_SPAN", "MIXED"),
        "rows_with_any_worklist_citation": rows_with("IN_SPAN", "MIXED", "AT_SEAM"),
        "worklist_citations_total": len(items),
        "far_side_citations": len(far_side),
        "far_side_citation_verses": sum(i["verse_count"] for i in far_side),
    }
    print(json.dumps({
        "rows_checked": n,
        "granularity": "CITATION (#e14 O1). The unit of every flag and every count is the argued citation: a "
                       "single verse is one, a dash-range is one, a comma/'and' list is one per member, and a "
                       "verse-set cited twice in a row is one.",
        "definition": "DEF-A4-ARGUED as written in ruling #e14; 'argued' is NOT narrowed to 'argued as "
                      "evidence' - this member judges mirroring and never weight",
        "role_vocabulary": list(ROLE_VOCABULARY),
        "role_assignment": ROLE_UNASSIGNED,
        "counts": counts,
        "a4_window_rule": "a citation is a worklist item when at least one of its verses lies in "
                          "[first-1, last+1]; a citation wholly outside that window is far-side and never a "
                          "defect (#e12 A4)",
        "mirror_reading": {
            "applied": "UNION of all boundary_evidence_refs entries",
            "why_reported": "DEF-A4-ARGUED clause 3's singular 'entry' also admits a strict per-entry reading; "
                            "the two differ only where two different entries cover the two endpoints of one "
                            "range. Both are computed on every citation and every disagreement is listed, so "
                            "the reading is settled by measurement rather than by the orchestrator's choice.",
            "disagreement_count": len(disagree),
            "disagreements": disagree,
        },
        "legacy_verse_level_aggregate": dict(
            legacy, note="DIAGNOSTIC ONLY, never a flag. Kept so these figures stay comparable with the "
                         "shipped member's 444 in-span / 131 at-seam / 817 far-side verses and with the "
                         "controlling agent's recount. The citation counts above are the worklist basis."),
        "worklist_citations": items,
        "far_side_citations_detail": far_side,
        "orphan_ref_warn_rows": len(orphan_warns),
        "orphan_ref_warn_count": sum(len(o["orphan_refs"]) for o in orphan_warns),
        "orphan_ref_warns": orphan_warns,
        "status": "GREEN" if not items else "FLAGS",
    }, ensure_ascii=False, indent=1))
    return 1 if items else 0


if __name__ == "__main__":
    if "--a4-selftest" in sys.argv:
        raise SystemExit(_a4_selftest())
    raise SystemExit(main())
