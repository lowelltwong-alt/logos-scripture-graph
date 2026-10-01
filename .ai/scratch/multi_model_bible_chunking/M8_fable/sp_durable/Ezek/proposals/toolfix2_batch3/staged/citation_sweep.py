#!/usr/bin/env python3
"""Ezek citation sweep + dual-cite arithmetic checker (deterministic Tier-0).

Adapted from the Jer tool (sp_durable/Jer/tools/citation_sweep.py): every arm is
unchanged except where Ezekiel's bytes differ. Ezek facts (Phase 0 byte-verified;
../web_mt_offset_map.json is authority; the counts are asserted by ezek_lib.py's
selftest): Ezek is NOT an identity book and carries EXACTLY ONE numbering zone -
pure renumbering, NO split: MT 21:1-5 = WEB 20:45-49; MT 21:6-37 = WEB 21:1-32.
Every other chapter is identity; totals WEB 1273 / MT 1273 / 48 chapters (EQUAL
totals - web_to_mt is INJECTIVE in Ezek). There are NO title pseudo-refs:
Ezek.N.0 is ALWAYS invalid. Therefore:
 - web:Ezek.C.V and oshb:Ezek.C.V are DIFFERENT ref spaces in WEB 20:45-21:32 and
   MT ch 21; each is range-guarded against its own witness space
   (web:Ezek.20.49 exists, oshb:Ezek.20.49 does not)
 - RANGES are validated INCLUDING the end: both ends in range, start <= end,
   and single-verse spans must use the X-X form
 - any dual ref "web:Ezek.a.b = oshb:Ezek.c.d" must satisfy
   web_to_mt(a,b) == (c,d); "oshb:Ezek.c.d = web:Ezek.a.b" must satisfy
   (a,b) == mt_to_web(c,d); "(MT n:m)" / "(WEB n:m)" qualifiers likewise
   via the crosswalk
 - OFFSET-ZONE DISCLOSURE (the Jer rule, carried): a structured ref whose START
   or END verse lies in the zone (WEB 20:45-21:32 for web: refs; MT ch 21 for
   oshb: refs) MUST carry an explicit dual or numeric qualifier in that entry -
   bare coordinates are ambiguous across witnesses exactly there. Elsewhere
   duals stay optional, but a written dual must be arithmetically right.
 - petuchah/setumah claims are VALIDATED against the marks inventory (71 PE +
   113 SAMEKH over 183 verses - Prophets: tier-3 weak): claimed TYPE must match
   the bytes (PE never conflated with SAMEKH), single-witness disclosure
   required, and lookups happen at the MT KEY (web: refs are crosswalk-mapped
   first)
 - SELAH claims are ERRORS ANYWHERE (selah occurs in neither witness); likewise
   reversed-nun, suspended-letter, LARGE-letter AND SMALL-letter claims - WLC
   Ezek carries NO special-letter seg of any class (other_segs EMPTY)
 - PUNCTA arm (new for Ezek): the puncta extraordinaria are not segs - U+05C4
   stands in the verse bytes at MT 41:20 (five) and MT 46:22 (seven) and nowhere
   else. A puncta claim on a ref is judged on every verse number written in its
   own clause of the annotation, at any distance, and in a parenthetical opening
   directly after that clause (a range counts as its verses):
   all sites -> true, none -> false, a mix -> ambiguous (RED); only a claim naming
   no number falls back to whether the ref's range covers a site. A negation
   earlier in the same comma-delimited clause makes it an absence claim, and two
   adjacent negators cancel. Only a closed '(MT n:m)' or '(WEB n:m)' counts as a
   numbering qualifier.
 - CALENDAR-DATE arm (new for Ezek; strategy section 10 as clarified by ruling
   G12(d)): MT 45:18, 45:20, 45:21 and 45:25 carry a month+day date with no year
   word (ezek_device_inventory.json calendar_dates_not_datelines). A row may
   never open at 45:20, 45:21 or 45:25; it may open at 45:18, on the messenger
   formula. A dateline claim that names one of the four is RED: in prose, when
   one of them is written in the claim's comma-delimited clause, in a
   parenthetical opening directly after it, in a list running straight on from
   it, or - only when those name no number - at the end of the immediately
   preceding comma clause (an apposition); in a ref's annotation likewise, or, naming no
   number, when the ref covers one of them and no real dateline. "not a
   dateline" and "non-dateline" are denials and pass. NOT machine-checked: a
   calendar date cited as onset evidence without the word "dateline" (review
   territory).
 - paseq claims must match the inventory (136 segs / 121 verses; seg layer,
   never quotable as verse bytes; COUNT-ONLY); single-witness disclosure
   required
 - ketiv/qere claims at a ref must match the kq inventory (134 notes / 99
   verses, 23 of them with more than one note; ONE verse sits INSIDE the zone:
   MT 21:28 = WEB 21:23); a ref that names an OSHB editorial note may instead
   rest on a verse whose note speaks of ketib/qere (the notes_other layer)
 - cross-tradition material in boundary_evidence_refs is an ERROR: LXX /
   Septuagint / Old Greek / Vulgate / Peshitta / Targum / DSS / Qumran /
   Masada and the nQEzek / MasEzek sigla. All of it stays cross-tradition
   METADATA in prose only (E-23), never a refs entry, and it does NOT touch the
   WEB/MT numbering pair
 - HEBREW-QUOTE BINDING: every Hebrew run quoted in a row's prose must
   byte-collate against the verse of the NEAREST oshb: ref in the same field
   (pointed quotes must reach BYTE tier, so a pointed quote from MT 41:20 or
   46:22 must keep its U+05C4 marks; nfd -> the nfd_degraded class =
   copy-degradation cured by normalize_hebrew_in_json, HARD at the writer gate
   per E-01; unpointed runs reach skeleton). A Hebrew quote with no oshb: ref in
   its field is flagged. QERE TIER (new for Ezek, mirroring the landing
   validator): a Qere lives in the note layer, never in the verse bytes; a
   quote matching a Qere of the bound verse (pmarks kq split by
   ezek_lib.kq_split, morpheme "/" removed) at the same tier passes when its
   field carries a ketiv/qere keyword within 160 characters of the quote and inside its sentence (Qere readings compared in the note's raw bytes), and is RED
   without one.
 - no ref may leave the Ezek substrate
REV-ROUND ARMS carried from the Jer tool:
 - prose_pair_check validates prose dual-cites INCLUDING range forms with
   per-endpoint CROSSWALK arithmetic (LIVE here, one zone)
 - prose-dual context window +-120 chars
 - input: .jsonl OR pretty-printed JSON array/object (sibling rows_from)
 - kq_web_quote_warn: a curly-quoted WEB span bound to a web: ref that covers
   a K/Q verse (MT key via crosswalk), with no ketiv/qere keyword in the row
Usage: citation_sweep.py [rows_file] (default freeze/frozen_rows_final.jsonl;
also accepts any JSONL or JSON-array file of rows with boundary_evidence_refs)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ezek_lib import (kq_split_bytes, LAST_VERSE, MT_LAST_VERSE, collate_hebrew,
                     expand_ref_token, load_pmarks, mt_to_web, mt_to_web_all,
                     web_quote_found, web_to_mt)

TOOLS = Path(__file__).resolve().parent
SP = TOOLS.parent

REF_RE = re.compile(
    r"^(web|oshb):Ezek\.(\d+)\.(\d+)(?:-(?:Ezek\.)?(\d+)(?:\.(\d+))?)?(.*)$")
CROSS = re.compile(r"\bLXX\b|\bSeptuagint\b|\bOld Greek\b|\bVulgate\b|\bGallican\b"
                   r"|\bPeshitta\b|\bTargum\b|\bDSS\b|\bQumran\b|\bMasada\b|\bMasEzek|\b\d{1,2}QEzek"
                   r"|\b4Q\d|\b11Q|\b2Q\d", re.I)
HEB_RUN = re.compile(r"[֑-״]{2,}(?:[ ־][֑-״]+)*")
POINTED = re.compile(r"[ְ-ּׁׂ֑-֯]")
OSHB_REF = re.compile(r"oshb:Ezek\.(\d+)\.(\d+)")
PROSE_PAIR = re.compile(
    r"web:Ezek\.(\d+)\.(\d+)(?:\s*[-–]\s*(?:Ezek\.)?(?:(\d+)\.)?(\d+))?"
    r"\s*[=(]+\s*(?:=\s*)?"
    r"oshb:Ezek\.(\d+)\.(\d+)(?:\s*[-–]\s*(?:Ezek\.)?(?:(\d+)\.)?(\d+))?")
QUOTE = re.compile(r"“([^”]+)”")
WREF = re.compile(r"web:Ezek\.\d+\.\d+(?:-(?:Ezek\.)?\d+(?:\.\d+)?)?")
KQ_WORD = re.compile(r"\b(?:ketiv|qere|K/Q)\b", re.I)
MARK_WORD = re.compile(r"\b(petuchah|setumah)\b|\b(pe|samekh)\b(?!\w)", re.I)
PUNCTA = re.compile(r"\bpuncta\b|\bextraordinar(?:y|ia)\s+(?:points?|dots?)\b|\bupper\s+dots?\b|U\+05C4", re.I)
PUNCTA_NEG = re.compile(r"\b(?:no|not|nor|never|without|absent|lacks?|lacking|none)\b(?:\s+[\w/-]+){0,2}\s*$", re.I)   # adjacent negation only
NEG_WORD = re.compile(r"\b(?:no|not|nor|never|without|absent|lacks?|lacking|none)\b", re.I)
PUNCTA_NUM = re.compile(r"(?<![A-Za-z\d])(\d{1,2})[:.](\d{1,2})(?!\d)")
SINGLE_WITNESS = re.compile(r"\bsingle[-\s]+witness", re.I)   # T4-04: the disclosure, hyphenated or spaced


def field_bounds(text, start, end):
    """The span of the one field a match sits in: check_marks joins every row field with newlines, so a window that
    crossed a newline would read another field - the span string included - as part of the claim."""
    nl = text.find("\n", end)
    return text.rfind("\n", 0, start) + 1, (nl if nl != -1 else len(text))


# Clause and sentence marks. A period ends a clause only before whitespace or the end (so Ezek.41.20 and 41.20 never
# split); a colon only when no digit follows (so 41:20 never splits); ';', ',', '(' and ')' always - including right
# after a digit, as in '41:20;' (the first version's digit lookbehind let a decoy number leak across that semicolon).
NEG_CLAUSE_END = re.compile(r"\.(?=\s|$)|:(?!\d)|[;,()]")   # a negation's scope ends at any clause mark
NUM_CLAUSE_END = re.compile(r"\.(?=\s|$)|[;()]")            # a claim's numbers stay together across commas
# T4-01: digits that follow a letter directly ('R4.5', a ruling or row id) are an id, never a verse number
RANGE_NUM = re.compile(r"(?<![A-Za-z\d])(\d{1,2})[:.](\d{1,2})(?:\s*[-–]\s*(?:(\d{1,2})[:.])?(\d{1,2}))?(?!\d)")
SENT_END = re.compile(r"\.(?=\s|$)|;|\n")
PUNCTA_SITE_PAIRS = {(41, 20), (46, 22)}


def clause_bounds(text, start, end, ends):
    f_lo, f_hi = field_bounds(text, start, end)
    lo = max([m.end() for m in ends.finditer(text, f_lo, start)] or [f_lo])
    nxt = ends.search(text, end, f_hi)
    return lo, (nxt.start() if nxt else f_hi)


def sentence_bounds(text, start, end):
    """The sentence holding [start, end), bounded by a period or semicolon that is not inside a dotted number (T2-04)."""
    lo = max([m.end() for m in SENT_END.finditer(text, 0, start)] or [0])
    nxt = SENT_END.search(text, end)
    return lo, (nxt.start() if nxt else len(text))


def puncta_negated(text, start, end=None):
    """Negation anywhere EARLIER in the mention's own comma-delimited clause (T2-03: an adjacency-only test dropped a
    distant 'not'). Two negators standing next to each other cancel ('not without', 'never lacking': T1-03). Given the
    mention's end, a denial LATER in the clause also counts, but only one DENIAL_AFTER reads (T4-03: '45:18, where a
    dateline would be expected but none stands'); a bare later 'no' or 'not' does not."""
    if end is not None and denied_after(text, end):
        return True
    lo, _ = clause_bounds(text, start, start, NEG_CLAUSE_END)
    negs = list(NEG_WORD.finditer(text, lo, start))
    if not negs:
        return False
    if len(negs) >= 2 and not text[negs[-2].end():negs[-1].start()].strip():
        return False
    return True


PAREN_AFTER = re.compile(r"\s*\(")
# T4-03: the closed set of denials that may FOLLOW a mention inside its clause. 'none of' is a partitive, and 'is absent',
# 'is lacking' or 'is missing' deny only at the clause end ('the dateline at 45:18 is missing its year word' still names
# a dateline). #e4 amendments: A1 - the clause end may be a newline (check_marks joins fields with newlines); A2 - a
# COORDINATED denial with a verse number and no expectation modal between the mention and the denial does not deny: the
# mention is a positive claim over the numbers before the denial ('stand at 41:5 but none is present in ch 46' claims 41:5).
DENIAL_COORD = re.compile(r"\b(?:but|though|although|yet)\s+(?:there\s+(?:is|are)\s+)?none\b(?!\s+of\b)"
                          r"|\bnone\s+(?:stands?|is\s+(?:present|written|there|found)|appears?|exists?)\b", re.I)
DENIAL_COPULAR = re.compile(r"\b(?:is|are)\s+(?:absent|lacking|missing)\s*(?=[.;,()\n]|$)", re.I)
EXPECT_MODAL = re.compile(r"\b(?:would|should|could|might|may|expected|anticipated)\b", re.I)


def _denial_window_end(text, end):
    """The end of the mention's clause, reading through a parenthetical that opens directly after it."""
    f_hi = field_bounds(text, end, end)[1]
    _, hi = clause_bounds(text, end, end, NEG_CLAUSE_END)
    p = PAREN_AFTER.match(text, hi)
    if p and p.end() <= f_hi:
        close = text.find(")", p.end(), f_hi)
        if close != -1:
            nxt = NEG_CLAUSE_END.search(text, close + 1, f_hi)
            hi = nxt.start() if nxt else f_hi
    return hi


def denial_after(text, end):
    """(kind, start) of the first closed-set denial after a mention inside its clause. 'copular' always denies;
    'coordinated' denies because the words between the mention and the denial name no verse number or carry an expectation
    modal; 'positive' is a coordinated form that does NOT deny (A2), and start bounds the mention's own numbers.
    (None, None) when the clause carries no closed-set denial."""
    hi = _denial_window_end(text, end)
    found = [m for m in (DENIAL_COPULAR.search(text, end, hi), DENIAL_COORD.search(text, end, hi)) if m]
    if not found:
        return None, None
    first = min(found, key=lambda m: m.start())
    if first.re is DENIAL_COPULAR:
        return "copular", first.start()
    between = text[end:first.start()]
    if not RANGE_NUM.search(between) or EXPECT_MODAL.search(between):
        return "coordinated", first.start()
    return "positive", first.start()


def denied_after(text, end):
    return denial_after(text, end)[0] in ("copular", "coordinated")


def claim_upper(text, end):
    """A2: where a mention's own number window stops - the start of a coordinated denial that does not deny - or None."""
    kind, start = denial_after(text, end)
    return start if kind == "positive" else None
# check_marks' PROSE arm keeps a 60-character reach inside the clause. Read without a limit, the real row P10-008 ("the
# word carrying the book's puncta extraordinaria -- ... -- a natural summary line before 41:21 returns to ...") binds its
# TRUE claim to the next verse, 41:21, and flags; the regression vector cm_real_row_distant_next_verse_number_ok pins that.
# citation_sweep's REF arm reads the whole clause, which is one short annotation per ref. The split is an implementation
# deviation from R4(ii) order (2), recorded for the distinct review (T4) and the controlling agent.
PROSE_REACH = 60


def _range_items(text, lo, hi):
    """Each C:V or C.V number in text[lo:hi] as a list of (chapter, verse) pairs; a written range counts as all its verses."""
    items = []
    for m in RANGE_NUM.finditer(text, lo, hi):
        c1, v1 = int(m.group(1)), int(m.group(2))
        if m.group(4):
            c2, v2 = (int(m.group(3)) if m.group(3) else c1), int(m.group(4))
            pairs, cc, vv = [], c1, v1
            while (cc, vv) <= (c2, v2) and len(pairs) < 80 and LAST_VERSE.get(cc):
                pairs.append((cc, vv))
                cc, vv = (cc, vv + 1) if vv < LAST_VERSE[cc] else (cc + 1, 1)
            if pairs:
                items.append(pairs)
                continue
        items.append([(c1, v1)])
    return items


def puncta_claim_numbers(text, start, end, reach=None, ends=NUM_CLAUSE_END, with_paren=True, upper=None):
    """The verse numbers a claim names (T2-01/02; ruling R4(ii) of ezek_controlling_rulings_a1#e3). That is EVERY C:V or
    C.V number in the mention's own clause, at any distance (a 60-character reach let a distant number go unseen), and
    every number in a parenthetical that opens directly after that clause ('puncta extraordinaria (41:5)'), all inside
    the same field. Each is a list of (chapter, verse) pairs; a written range counts as all its verses. `ends` names the
    clause marks (the calendar-date arm passes the comma-delimited set); `reach`, when given, narrows the clause window
    to that many characters either side of the mention. citation_sweep's ref arm passes none; check_marks' prose arm
    passes PROSE_REACH."""
    lo, hi = clause_bounds(text, start, end, ends)
    if upper is not None:   # A2: numbers after a coordinated denial belong to the denial; no parenthetical past it
        hi, with_paren = min(hi, upper), False
    items = _range_items(text, lo if reach is None else max(lo, start - reach), hi if reach is None else min(hi, end + reach))
    if with_paren:
        f_hi = field_bounds(text, start, end)[1]
        p = PAREN_AFTER.match(text, hi)
        if p and p.end() <= f_hi:
            close = text.find(")", p.end(), f_hi)
            if close != -1:
                items += _range_items(text, p.end(), close)
    return items


def puncta_verdict(items):
    """None when no number is written; True when every written verse is a site and every written range holds one;
    False when none does; 'ambiguous' when one clause mixes site and non-site numbers (T2-01/02)."""
    if not items:
        return None
    ok = [any(p in PUNCTA_SITE_PAIRS or web_to_mt(*p) in PUNCTA_SITE_PAIRS for p in pairs) for pairs in items]
    return True if all(ok) else (False if not any(ok) else "ambiguous")
KQ_NOTE = re.compile(r"\bketi[bv]\b|\bqere\b|\bK/Q\b", re.I)   # the OSHB notes spell it "ketib"
NOTE_WORD = re.compile(r"\bnotes?\b|\beditorial\b", re.I)
PUNCTA_KEYS = {"Ezek.41.20", "Ezek.46.22"}   # MT keys; asserted by ezek_lib's selftest
# CALENDAR-DATE arm (Ezek; strategy section 10 as clarified by ruling G12(d)). MT pairs, asserted against
# ezek_device_inventory.json by _test_zone_tools_ezek.py.
CAL_DATE_PAIRS = {(45, 18), (45, 20), (45, 21), (45, 25)}   # calendar_dates_not_datelines: month+day, no year word
CAL_NO_ONSET = CAL_DATE_PAIRS - {(45, 18)}                 # 45:18 may open a row, on its messenger formula
DATELINE_PAIRS = {(1, 1), (1, 2), (8, 1), (20, 1), (24, 1), (26, 1), (29, 1), (29, 17), (30, 20), (31, 1), (32, 1),
                  (32, 17), (33, 21), (40, 1)}             # dated_oracles: a year word with a month or day term
DATELINE = re.compile(r"(?<!non-)(?<!non )\bdatelines?\b", re.I)   # "non-dateline" is itself a denial
LIST_NEXT = re.compile(r"\s*(?:,\s*(?:and\s+)?|\s+and\s+)(?=\d{1,2}[:.]\d)")
APPOSITION_NUM = re.compile(r"(?<![A-Za-z\d])(\d{1,2})[:.](\d{1,2})(?:\s*[-–]\s*(?:(\d{1,2})[:.])?(\d{1,2}))?\s*$")


def dateline_claim_numbers(text, start, end, reach=60, upper=None):
    """The verse numbers a dateline claim names:
      - those in its own COMMA-delimited clause within `reach` characters ('unlike the dateline at 40:1, the date at
        45:18 ...' names 40:1 only);
      - a parenthetical opening directly after that clause ('the dateline (45:18)');
      - a list written straight on from the last of them ('datelines at 40:1, 45:18 and 45:20' names all three);
      - only when none of those names a number, the number that ENDS the immediately preceding comma clause (the
        apposition '45:18, a dateline-grade onset').
    The last two readings follow CAL-1 of ezek_controlling_rulings_a1#e3."""
    lo, hi = clause_bounds(text, start, end, NEG_CLAUSE_END)
    if upper is not None:   # A2
        hi = min(hi, upper)
    items = puncta_claim_numbers(text, start, end, reach, NEG_CLAUSE_END, upper=upper)
    found = list(RANGE_NUM.finditer(text, max(lo, start - reach), min(hi, end + reach)))
    j = found[-1].end() if found else None
    while j is not None:
        nx = LIST_NEXT.match(text, j)
        m = RANGE_NUM.match(text, nx.end()) if nx else None
        if not m or (upper is not None and m.end() > upper):
            break
        items += puncta_claim_numbers(text, m.start(), m.end(), 0, NEG_CLAUSE_END, with_paren=False)
        j = m.end()
    if not items and lo > 0 and text[lo - 1] == ",":
        m = APPOSITION_NUM.search(text, field_bounds(text, start, end)[0], lo - 1)
        if m:
            items += _range_items(text, m.start(), m.end())
    return items


def rows_from(p: Path):
    """Sibling-tool input contract: .jsonl one row per line, or a
    pretty-printed JSON array / {"decisions": [...]} object."""
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    data = json.loads(text)
    if isinstance(data, dict):
        if "decisions" in data:
            return data["decisions"]
        return [v for v in data.values() if isinstance(v, dict)]
    return data


def pair_ok_web_to_mt(wc: int, wv: int, oc: int, ov: int) -> bool:
    """A WEB/MT pairing is right iff the crosswalk maps it (injective in Ezek)."""
    return web_to_mt(wc, wv) == (oc, ov)


def web_pairs_in_offset_zone(pairs) -> bool:
    return any((c == 20 and v >= 45) or c == 21 for c, v in pairs)   # WEB 20:45-49 and WEB 21:1-32


def mt_pairs_in_offset_zone(pairs) -> bool:
    return any(c == 21 for c, v in pairs)   # MT 21:1-37


def main() -> int:
    rows_path = Path(sys.argv[1]) if len(sys.argv) > 1 else SP / "freeze" / "frozen_rows_final.jsonl"
    pm = load_pmarks()
    marks, paseq, kq = pm["marks"], pm["paseq"], pm["kq"]
    small_letter_keys = {k: v for k, v in pm.get("other_segs", {}).items()}
    # Ezek: verses whose OSHB editorial note speaks of ketib/qere - backed by bytes, but not in the kq inventory
    kq_note_keys = {k for k, notes in pm.get("notes_other", {}).items()
                    if any(KQ_NOTE.search(n.get("text", "")) for n in notes)}
    problems: list[str] = []
    prose_dual_warns: list[str] = []
    prose_pair_problems: list[str] = []
    nfd_degraded: list[str] = []
    kq_web_quote_warns: list[str] = []
    rows = rows_from(rows_path)

    oshb_texts = None
    web_texts = None

    for row in rows:
        did = row.get("decision_id", "?")
        # CALENDAR-DATE arm, onset (Ezek; strategy section 10, ruling G12(d)): MT 45:20, 45:21 and 45:25 carry a
        # month+day date with no year word and no formula, so no row opens there. A row MAY open at 45:18 on the
        # messenger formula that shares the verse with the date; the date itself is never onset evidence.
        cal_on = re.match(r"^(?:web:)?Ezek\.(\d+)\.(\d+)-", str(row.get("span") or "").strip())
        cal_mt = web_to_mt(int(cal_on.group(1)), int(cal_on.group(2))) if cal_on else None
        if cal_mt in CAL_NO_ONSET:
            problems.append(f"{did}: row opens at a calendar date with no formula (MT {cal_mt[0]}:{cal_mt[1]}) - MT 45:20, "
                            f"45:21 and 45:25 open no unit; a row may open at 45:18 only on its messenger formula")
        # X-X span-form arm: row spans use the full Ezek.a.b-Ezek.c.d form
        span = row.get("span")
        if isinstance(span, str) and span.strip():
            s = span.strip().replace("web:", "")
            if not re.match(r"^Ezek\.\d+\.\d+-Ezek\.\d+\.\d+$", s):
                problems.append(f"{did}: span not in full X-X form "
                                f"(Ezek.a.b-Ezek.c.d, single verses included): {span!r}")
        for ref in row.get("boundary_evidence_refs", []):
            if CROSS.search(ref):
                problems.append(f"{did}: cross-tradition material in "
                                f"boundary_evidence_refs: {ref!r}")
                continue
            m = REF_RE.match(ref)
            if not m:
                problems.append(f"{did}: non-Ezek or malformed ref {ref!r}")
                continue
            kind = m.group(1)
            ch, v = int(m.group(2)), int(m.group(3))
            e1, e2, tail = m.group(4), m.group(5), m.group(6)
            space = LAST_VERSE if kind == "web" else MT_LAST_VERSE
            last = space.get(ch)
            if last is None:
                problems.append(f"{did}: {ref!r} chapter out of range")
                continue
            if v == 0:
                problems.append(f"{did}: {ref!r} - Ezek.{ch}.0 is always invalid "
                                f"(no title pseudo-verses exist in Ezek)")
                continue
            if not (1 <= v <= last):
                problems.append(f"{did}: {ref!r} out of range for {kind.upper()} numbering")
                continue
            # range-END arm
            end_pair = (ch, v)
            if e1 is not None:
                ec, ev = (ch, int(e1)) if e2 is None else (int(e1), int(e2))
                elast = space.get(ec)
                if elast is None or not (1 <= ev <= elast):
                    problems.append(f"{did}: range END out of range: {ref!r}")
                elif (ec, ev) < (ch, v):
                    problems.append(f"{did}: range END precedes start: {ref!r}")
                else:
                    end_pair = (ec, ev)

            # dual/qualifier arithmetic via the crosswalk (injective book)
            has_disclosure = False
            pair = re.search(r"=\s*oshb:Ezek\.(\d+)\.(\d+)", tail)
            if kind == "web" and pair:
                has_disclosure = True
                got = (int(pair.group(1)), int(pair.group(2)))
                want = web_to_mt(ch, v)
                if got != want:
                    problems.append(f"{did}: dual-cite arithmetic wrong (crosswalk "
                                    f"book - expected oshb:Ezek.{want[0]}.{want[1]}): {ref!r}")
            wpair = re.search(r"=\s*web:Ezek\.(\d+)\.(\d+)", tail)
            if kind == "oshb" and wpair:
                has_disclosure = True
                got = (int(wpair.group(1)), int(wpair.group(2)))
                want = mt_to_web(ch, v)
                if got != want:
                    problems.append(f"{did}: dual-cite arithmetic wrong (crosswalk "
                                    f"book - expected web:Ezek.{want[0]}.{want[1]}): {ref!r}")
            off = re.search(r"\(MT\s+(\d+)[:.](\d+)\)", tail)
            if off:
                if kind != "web":
                    problems.append(f"{did}: MT qualifier on a non-web ref: {ref!r}")
                else:
                    has_disclosure = True
                    want = web_to_mt(ch, v)
                    if (int(off.group(1)), int(off.group(2))) != want:
                        problems.append(f"{did}: MT qualifier wrong (crosswalk - "
                                        f"expected MT {want[0]}:{want[1]}): {ref!r}")
            woff = re.search(r"\(WEB\s+(\d+)[:.](\d+)\)", tail)
            if woff:
                if kind != "oshb":
                    problems.append(f"{did}: WEB qualifier on a non-oshb ref: {ref!r}")
                else:
                    has_disclosure = True
                    want = mt_to_web(ch, v)
                    if (int(woff.group(1)), int(woff.group(2))) != want:
                        problems.append(f"{did}: WEB qualifier wrong (crosswalk - "
                                        f"expected WEB {want[0]}:{want[1]}): {ref!r}")

            # OFFSET-ZONE DISCLOSURE arm
            zone_pairs = [(ch, v), end_pair]
            in_zone = (web_pairs_in_offset_zone(zone_pairs) if kind == "web"
                       else mt_pairs_in_offset_zone(zone_pairs))
            if in_zone and not has_disclosure:
                problems.append(
                    f"{did}: offset-zone ref lacks dual-cite/qualifier "
                    f"disclosure (WEB 20:45-21:32 and MT ch 21 are DIFFERENT "
                    f"numbering spaces - bare coordinates are ambiguous "
                    f"there): {ref!r}")

            # MT key for inventory lookups (web: refs crosswalk-mapped first)
            if kind == "web":
                mtc, mtv = web_to_mt(ch, v)
            else:
                mtc, mtv = ch, v
            key = f"Ezek.{mtc}.{mtv}"

            # marks arm - claims validated under TYPE against the rich layer
            mm = MARK_WORD.search(tail)
            if mm:
                word = (mm.group(1) or mm.group(2)).lower()
                want_type = "PE" if word in ("petuchah", "pe") else "SAMEKH"
                got_types = marks.get(key, [])
                if want_type not in got_types:
                    problems.append(
                        f"{did}: {ref!r} claims {word} but the marks inventory "
                        f"has {got_types or 'none'} at {key} "
                        f"(PE and SAMEKH are never conflated)")
                if not SINGLE_WITNESS.search(tail):
                    problems.append(f"{did}: parashah-mark ref lacks single-witness "
                                    f"disclosure (tier-3 in Prophets): {ref!r}")
            if re.search(r"\bselah\b", tail, re.I):
                problems.append(f"{did}: {ref!r} claims selah - NO selah exists "
                                f"in Ezek (Psalter device; fabrication)")
            if re.search(r"\b(?:inverted|reversed)[\s-]*nun\b|\bsuspended\b", tail, re.I):
                problems.append(f"{did}: {ref!r} claims a reversed-nun/suspended "
                                f"seg - WLC Ezek carries neither")
            # patch i1 parity with check_marks: letter-name whitelist, no
            # catch-all [a-z]+ arm (the "small vessel" WEB-English class)
            if re.search(r"\b(?:large|x-large)\s+(?:letter|nun|ayin|mem|yod|waw|vav|kaf|pe|"
                         r"tsadi|qof|resh|shin|tav|aleph|alef|bet|gimel|dalet|he|het|tet|"
                         r"lamed|samekh|zayin)\b"
                         r"|\bmajuscule\b", tail, re.I):
                problems.append(f"{did}: {ref!r} claims a large letter - WLC Ezek "
                                f"carries NO special-letter segs of any class")
            if re.search(r"\b(?:small|x-small)\s+(?:letter|nun|ayin|mem|yod|waw|vav|kaf|pe|"
                         r"tsadi|qof|resh|shin|tav|aleph|alef|bet|gimel|dalet|he|het|tet|"
                         r"lamed|samekh|zayin)\b"
                         r"|\bze[i']?ira\b|\bminuscule\b", tail, re.I):
                if not small_letter_keys.get(key):
                    problems.append(f"{did}: {ref!r} claims a small letter but WLC "
                                    f"Ezek carries NO special-letter segs of any class "
                                    f"(nothing at {key})")
                elif not SINGLE_WITNESS.search(tail):
                    problems.append(f"{did}: small-letter ref lacks single-witness "
                                    f"disclosure: {ref!r}")
            if re.search(r"\bpaseq\b", tail, re.I):
                if not paseq.get(key):
                    problems.append(f"{did}: {ref!r} claims paseq but OSHB carries "
                                    f"none at {key}")
                if not SINGLE_WITNESS.search(tail):
                    problems.append(f"{did}: paseq ref lacks single-witness disclosure: {ref!r}")
            # PUNCTA arm (Ezek): U+05C4 stands in the verse bytes at MT 41:20 and 46:22 only. A claim is judged on
            # every verse number in its own clause of the annotation, at any distance, and in a parenthetical opening
            # directly after that clause (R4(ii), ezek_controlling_rulings_a1#e3; a range counts as
            # its verses): all sites -> true, none -> false, a mix -> ambiguous, RED (T2-01/02). Only a claim naming
            # no number falls back to whether the ref's range covers a site (T1-01). A negation earlier in the same
            # comma-delimited clause makes it an absence claim; adjacent negators cancel (T1-03, T2-03); so does a closed-set
            # denial later in the clause (T4-03). A true claim needs single-witness disclosure in the annotation, as mark,
            # small-letter and paseq refs do (T4-04).
            pm_ = PUNCTA.search(tail)
            if pm_:
                covered, (c_, v_) = set(), (ch, v)
                while (c_, v_) <= end_pair and c_ in space:
                    mk = web_to_mt(c_, v_) if kind == "web" else (c_, v_)
                    if mk:
                        covered.add(f"Ezek.{mk[0]}.{mk[1]}")
                    c_, v_ = (c_, v_ + 1) if v_ < space[c_] else (c_ + 1, 1)
                sites = covered & PUNCTA_KEYS
                verdict = puncta_verdict(puncta_claim_numbers(tail, pm_.start(), pm_.end(), upper=claim_upper(tail, pm_.end())))
                at_site = bool(sites) if verdict is None else verdict
                if puncta_negated(tail, pm_.start(), pm_.end()):
                    if at_site is True or at_site == "ambiguous":
                        problems.append(f"{did}: {ref!r} denies puncta extraordinaria at a verse that carries them")
                elif at_site == "ambiguous":
                    problems.append(f"{did}: {ref!r} puncta claim is ambiguous: its clause names both a site and "
                                    f"another verse (MT 41:20 and 46:22 are the only sites)")
                elif not at_site:
                    problems.append(f"{did}: {ref!r} claims puncta extraordinaria but they stand only at MT 41:20 "
                                    f"and MT 46:22 ({'the ref covers neither' if verdict is None else 'the claim names another verse'})")
                elif not SINGLE_WITNESS.search(tail):
                    problems.append(f"{did}: puncta ref lacks single-witness disclosure: {ref!r}")
            # CALENDAR-DATE arm, refs (Ezek; strategy section 10, ruling G12(d)): a dateline claim in the annotation is
            # RED when it names MT 45:18, 45:20, 45:21 or 45:25 (dateline_claim_numbers), or, naming no number, when the
            # ref covers one of them and no real dateline. 'not a dateline' and 'non-dateline' are denials and pass.
            for dm_ in DATELINE.finditer(tail):
                if puncta_negated(tail, dm_.start(), dm_.end()):
                    continue
                named_ = {p for pairs in dateline_claim_numbers(tail, dm_.start(), dm_.end(), upper=claim_upper(tail, dm_.end())) for p in pairs}
                if not named_:
                    covered_, (c_, v_) = set(), (ch, v)
                    while (c_, v_) <= end_pair and c_ in space:
                        covered_.add(web_to_mt(c_, v_) if kind == "web" else (c_, v_))
                        c_, v_ = (c_, v_ + 1) if v_ < space[c_] else (c_ + 1, 1)
                    named_ = set() if covered_ & DATELINE_PAIRS else covered_
                cal_ = sorted(named_ & CAL_DATE_PAIRS)
                if cal_:
                    problems.append(f"{did}: {ref!r} claims a dateline at " + ", ".join("MT %d:%d" % p for p in cal_)
                                    + " - a calendar date with no year word is never a dateline")
                    break
            # REF HEBREW arm (Ezek; S1-06, ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 (b)) [CWO-EZ-16]: every Hebrew
            # run inside a ref entry binds to that entry's OWN (first) ref - every verse of its range - with walk()'s functions:
            # collate_hebrew (byte tier if pointed, any tier if unpointed), the verse's Qere from the raw note bytes, and a
            # ketiv/qere keyword in the run's own sentence within 160 characters.
            ref_runs_ = [r_ for r_ in HEB_RUN.findall(tail) if len(re.sub(r"[^א-ת]", "", r_)) >= 3]
            if ref_runs_:
                if oshb_texts is None:
                    oshb_texts = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
                keys_, (c_, v_) = [], (ch, v)
                while (c_, v_) <= end_pair and c_ in space:
                    mk_ = web_to_mt(c_, v_) if kind == "web" else (c_, v_)
                    if mk_:
                        keys_.append(f"Ezek.{mk_[0]}.{mk_[1]}")
                    c_, v_ = (c_, v_ + 1) if v_ < space[c_] else (c_ + 1, 1)
                texts_ = " | ".join(oshb_texts.get(k_, {}).get("text", "") for k_ in keys_)
                qere_ = " | ".join(kq_split_bytes(n_, oshb_texts.get(k_, {}).get("text", ""))[1].replace("/", "")
                                   for k_ in keys_ for n_ in kq.get(k_, []))
                for r_ in ref_runs_:
                    pointed_ = bool(POINTED.search(r_))
                    t_ = collate_hebrew(r_, texts_)
                    if (t_ == "byte") if pointed_ else t_ != "none":
                        continue
                    tq_ = collate_hebrew(r_, qere_) if qere_.strip(" |") else "none"
                    if (tq_ == "byte") if pointed_ else tq_ != "none":
                        p_ = tail.find(r_)
                        s_lo_, s_hi_ = sentence_bounds(tail, p_, p_ + len(r_))
                        if KQ_WORD.search(tail[max(s_lo_, p_ - 160):min(s_hi_, p_ + len(r_) + 160)]):
                            continue
                        problems.append(f"{did}: Hebrew {r_[:25]!r}… in ref entry {ref!r} matches the Qere of its own ref "
                                        f"but its sentence carries no ketiv/qere disclosure [CWO-EZ-16]")
                        continue
                    problems.append(f"{did}: Hebrew {r_[:25]!r}… in ref entry {ref!r} does not collate against its own ref "
                                    f"(tier {t_}, qere tier {tq_}, {'pointed' if pointed_ else 'unpointed'}) [CWO-EZ-16]")
            if (re.search(r"\b(?:ketiv|qere|K/Q)\b", tail, re.I) and not kq.get(key)
                    and not (key in kq_note_keys and NOTE_WORD.search(tail))):
                problems.append(f"{did}: {ref!r} claims ketiv/qere but the kq "
                                f"inventory has none at {key}")

        # ---- prose EXPLICIT-PAIR arithmetic arm: a written
        # "web:Ezek.a.b = oshb:Ezek.c.d" asserts arithmetic wherever it
        # appears; crosswalk book - validated per endpoint for ranges.
        def prose_pair_check(o, path="row"):
            if isinstance(o, dict):
                for k2, v2 in o.items():
                    if k2 != "boundary_evidence_refs":
                        prose_pair_check(v2, f"{path}.{k2}")
            elif isinstance(o, list):
                for i, v2 in enumerate(o):
                    prose_pair_check(v2, f"{path}[{i}]")
            elif isinstance(o, str):
                for m in PROSE_PAIR.finditer(o):
                    g = m.groups()
                    wc, wv1 = int(g[0]), int(g[1])
                    wc2 = int(g[2]) if g[2] else wc
                    wv2 = int(g[3]) if g[3] else None
                    oc, ov1 = int(g[4]), int(g[5])
                    oc2 = int(g[6]) if g[6] else oc
                    ov2 = int(g[7]) if g[7] else None
                    ok = pair_ok_web_to_mt(wc, wv1, oc, ov1)
                    if wv2 is not None or ov2 is not None:
                        we = (wc2, wv2) if wv2 is not None else (wc, wv1)
                        oe = (oc2, ov2) if ov2 is not None else (oc, ov1)
                        ok = ok and pair_ok_web_to_mt(we[0], we[1], oe[0], oe[1])
                    if not ok:
                        prose_pair_problems.append(
                            f"{did}: prose dual-cite arithmetic wrong in {path} "
                            f"(crosswalk book - WEB 20:45-49 = MT 21:1-5, WEB 21:1-32 = "
                            f"MT 21:6-37): {m.group(0)!r}")
        prose_pair_check(row)

        # ---- CALENDAR-DATE arm, prose (Ezek; strategy section 10, ruling G12(d)): a dateline claim that names MT
        # 45:18, 45:20, 45:21 or 45:25 in its own comma-delimited clause, or in a list running straight on from it, is
        # RED. A claim naming no number is not judged here (the ref arm judges refs by their coverage).
        def prose_dateline_check(o, path="row"):
            if isinstance(o, dict):
                for k2, v2 in o.items():
                    if k2 != "boundary_evidence_refs":
                        prose_dateline_check(v2, f"{path}.{k2}")
            elif isinstance(o, list):
                for i, v2 in enumerate(o):
                    prose_dateline_check(v2, f"{path}[{i}]")
            elif isinstance(o, str):
                for m in DATELINE.finditer(o):
                    if puncta_negated(o, m.start(), m.end()):
                        continue
                    cal = sorted({p for pairs in dateline_claim_numbers(o, m.start(), m.end(), upper=claim_upper(o, m.end())) for p in pairs}
                                 & CAL_DATE_PAIRS)
                    if cal:
                        problems.append(f"{did}: {path} claims a dateline at " + ", ".join("MT %d:%d" % p for p in cal)
                                        + " - a calendar date with no year word is never a dateline")
        prose_dateline_check(row)

        # ---- Hebrew-quote binding arm over every prose field ----
        def walk(o, path="row"):
            nonlocal oshb_texts
            if isinstance(o, dict):
                for k2, v2 in o.items():
                    if k2 != "boundary_evidence_refs":
                        walk(v2, f"{path}.{k2}")
            elif isinstance(o, list):
                for i, v2 in enumerate(o):
                    walk(v2, f"{path}[{i}]")
            elif isinstance(o, str):
                runs = [r for r in HEB_RUN.findall(o)
                        if len(re.sub(r"[^א-ת]", "", r)) >= 3]
                if not runs:
                    return
                refs = list(OSHB_REF.finditer(o))
                if oshb_texts is None:
                    oshb_texts = json.loads(
                        (TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
                for run in runs:
                    if not refs:
                        problems.append(f"{did}: Hebrew quote {run[:25]!r}… in "
                                        f"{path} has NO oshb: ref in its field")
                        continue
                    pos = o.find(run)
                    end = pos + len(run)
                    def keyf(mm):
                        follows = 0 <= mm.start() - end <= 40
                        dist = min(abs(mm.start() - pos), abs(mm.start() - end))
                        return (not follows, dist)
                    cands = sorted(refs, key=keyf)[:3]
                    pointed = bool(POINTED.search(run))
                    best = None
                    ok = False
                    nfd_hit = None
                    qere_undisclosed = None
                    vkey = None
                    for near in cands:
                        vkey = f"Ezek.{near.group(1)}.{near.group(2)}"
                        src = oshb_texts.get(vkey, {}).get("text", "")
                        tier = collate_hebrew(run, src)
                        if best is None:
                            best = (vkey, tier)
                        if (tier == "byte") if pointed else tier != "none":
                            ok = True
                            break
                        # QERE tier (Ezek; mirrors SP/Ezek/_validate_writer_part.py): a Qere lives in the
                        # OSHB note layer, not in the verse bytes, and is legitimate when its field discloses it
                        qere_src = " | ".join(kq_split_bytes(n, src)[1].replace("/", "") for n in kq.get(vkey, []))   # D3: raw note bytes
                        qtier = collate_hebrew(run, qere_src) if qere_src.strip(" |") else "none"
                        if (qtier == "byte") if pointed else qtier != "none":
                            s_lo, s_hi = sentence_bounds(o, pos, end)
                            if KQ_WORD.search(o[max(s_lo, pos - 160):min(s_hi, end + 160)]):   # T1-04, T2-04: THIS quote's sentence
                                ok = True
                            else:
                                qere_undisclosed = vkey
                            break
                        if pointed and tier == "nfd" and nfd_hit is None:
                            nfd_hit = vkey
                    if qere_undisclosed is not None:
                        problems.append(
                            f"{did}: Hebrew quote {run[:25]!r}… in {path} matches the Qere at "
                            f"oshb:{qere_undisclosed} but its field carries no ketiv/qere disclosure")
                        continue
                    if not ok and nfd_hit is not None:
                        vkey = nfd_hit
                        nfd_degraded.append(
                            f"{did}: pointed Hebrew quote {run[:25]!r}… in {path} "
                            f"collates against oshb:{nfd_hit} at NFD tier only "
                            f"(copy degradation - cure with "
                            f"normalize_hebrew_in_json.py --write)")
                    elif not ok:
                        problems.append(
                            f"{did}: Hebrew quote {run[:25]!r}… in {path} does not "
                            f"collate against any nearby cited ref (best "
                            f"oshb:{best[0]}, tier={best[1]}, "
                            f"{'pointed' if pointed else 'unpointed'})")
                    if (ok or nfd_hit is not None) and kq.get(vkey) and not re.search(
                            r"\b(?:ketiv|qere|K/Q)\b", o, re.I):
                        prose_dual_warns.append(
                            f"{did}: Hebrew quote in {path} binds to K/Q verse "
                            f"oshb:{vkey} with no ketiv/qere disclosure in-field")
        walk(row)

        # ---- K/Q WEB-quote arm (WARN) - MT keys via the crosswalk ----
        if not KQ_WORD.search(json.dumps(row, ensure_ascii=False)):
            covered_kq: dict[str, str] = {}

            def kq_web_walk(o, path="row"):
                nonlocal web_texts
                if isinstance(o, dict):
                    for k2, v2 in o.items():
                        if k2 != "boundary_evidence_refs":
                            kq_web_walk(v2, f"{path}.{k2}")
                elif isinstance(o, list):
                    for i, v2 in enumerate(o):
                        kq_web_walk(v2, f"{path}[{i}]")
                elif isinstance(o, str):
                    refs = [(m.start(), m.group(0)[4:]) for m in WREF.finditer(o)]
                    if not refs:
                        return
                    for qm in QUOTE.finditer(o):
                        span = qm.group(1).strip()
                        if len(span.split()) < 2:
                            continue
                        if len(re.findall(r"[֐-׿]", span)) > len(
                                re.findall(r"[A-Za-z]", span)):
                            continue
                        near = [r for pos, r in refs
                                if abs(pos - qm.start()) <= 200
                                or abs(pos - qm.end()) <= 200]
                        if not near:
                            continue
                        if web_texts is None:
                            web_texts = json.loads(
                                (TOOLS / "verse_map_web.json").read_text(
                                    encoding="utf-8"))
                        for r in near:
                            for c2, v2 in expand_ref_token(r):
                                t = web_texts.get(f"Ezek.{c2}.{v2}", {}).get("text", "")
                                if not t or not web_quote_found(span, [t]):
                                    continue
                                mt = web_to_mt(c2, v2)
                                mtk = f"Ezek.{mt[0]}.{mt[1]}"
                                if kq.get(mtk):
                                    covered_kq.setdefault(
                                        mtk,
                                        f"{path} {span[:60]!r} via web:Ezek.{c2}.{v2}")
            kq_web_walk(row)
            for mtk, where in covered_kq.items():
                kq_web_quote_warns.append(
                    f"{did}: WEB quote covers K/Q verse oshb:{mtk} with no "
                    f"ketiv/qere disclosure anywhere in the row ({where})")

    print(json.dumps({"rows": len(rows), "rows_file": rows_path.name, "problems": problems,
                      "prose_dual_warn_count": len(prose_dual_warns),
                      "prose_pair_problem_count": len(prose_pair_problems),
                      "prose_pair_problems": prose_pair_problems[:20],
                      "prose_dual_warns": prose_dual_warns[:20],
                      "nfd_degraded_count": len(nfd_degraded),
                      "nfd_degraded": nfd_degraded[:20],
                      "kq_web_quote_warn_count": len(kq_web_quote_warns),
                      "kq_web_quote_warns": kq_web_quote_warns[:20],
                      "status": "GREEN" if not problems else "RED"}, ensure_ascii=False, indent=1))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
