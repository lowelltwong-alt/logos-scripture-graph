#!/usr/bin/env python3
"""Paragraph-mark/segment-disclosure symmetry checker (casing-normalized) for Ezek rows.

Adapted from the Jer tool (sp_durable/Jer/tools/check_marks.py). Ezek
(Prophets) carries 71 petuchah + 113 setumah over 183 marked verses,
byte-extracted into ../pmarks_Ezek.json (counts asserted by ezek_lib.py's
selftest); the paragraph-mark machinery applies unchanged:
 0. SELAH claims are fabrications in Ezek (selah occurs in neither witness).
    Likewise reversed-nun, suspended-letter, LARGE-letter AND SMALL-letter
    claims: WLC Ezek carries NO special-letter seg of any class (other_segs
    EMPTY), so every small-letter claim flags. PUNCTA arm (new for Ezek): the
    puncta extraordinaria are not segs - U+05C4 stands in the verse bytes at
    MT 41:20 and MT 46:22 only - so a puncta claim is judged on the verse numbers
    in its own clause within 60 characters (prose keeps that reach), or in a parenthetical opening directly after that clause, in the same field: all sites -> true,
    none -> false, a mix -> ambiguous (flagged); a claim naming no number is
    satisfied only when the row's span covers a site. A negation earlier in the
    same comma-delimited clause makes it an absence claim; adjacent negators cancel.
 1. Any petuchah/setumah claim naming a verse IN ITS OWN CLAUSE (C:V, C.V, 'MT C:V'
    or a dotted ref; S1-22) must match the marks inventory
    under the CORRECT mark type - PE and SAMEKH are never conflated (owner
    addendum). NON-IDENTITY BOOK: a cited verse number near a claim is
    checked under BOTH readings (direct MT and WEB-crosswalk-mapped MT) -
    outside WEB 20:45-21:32 / MT ch 21 the readings coincide; a claim passes
    if EITHER carries the mark. NEAREST-MATCH diagnostics: a failed claim
    reports whether MT V±1 carries a mark - the off-by-one signature.
    W1 (#e5 FLAGS-TF2-1): a mark of the claimed type after the verse BEFORE
    the named one also satisfies the claim (a mark closes the unit before an
    onset); the type test is untouched and absence claims never take it.
 2. SYMMETRY (unconditional): every span-relevant mark (front seam start-1,
    interior, end verse - WEB span crosswalk-mapped to MT keys) must be
    disclosed in the row's prose whether or not the prose engages the mark
    layer - tier-3 weak corroboration still requires disclosure when present
    (r3 contract: "all interior+edge marks vs pmarks").
 3. ABSENCE ARM: a "no petuchah/setumah" claim is checked against the verse,
    range or chapter its own clause names (S1-22); one naming none is checked
    WITHIN the span-relevant (MT-mapped) set. W6 (#e5): the letter-name form
    'no pe or samekh' is an absence phrase too, in mark talk only.
 4. ketiv/qere prose claims naming a verse must match the kq inventory
    (134 notes / 99 verses, MT-keyed; dual-reading like rule 1; ONE verse sits
    INSIDE the zone - MT 21:28 = WEB 21:23; 23 verses carry more than one note).
    A claim that speaks of an editorial note may instead rest on a verse whose
    OSHB note names ketib/qere (the notes_other layer). The claim binds to the
    numbers in its own clause (S1-22). A NEGATED K/Q claim is an absence claim,
    checked against the verses its clause names or the span's kq keys
    (false_kq_absence_claim).
    W2/W5 (#e5): a K/Q is negated only by a negator at most one word before it
    (two negators together cancel) or heading a comma list of short segments
    ('No parashah, K/Q or editorial note ...'); T4-03's closed-set denial
    after it still denies. 'no other K/Q' is checked against the span's K/Q
    verses that the row names nowhere.
 5. PASEQ-POSITION arm (WARN only): pmarks paseq is COUNT-ONLY (136 segs /
    121 verses; no offsets); intra-verse position claims are unsourceable.
Known limitation (Ezra finding, unchanged): the prose-window heuristic is
unreliable in BOTH directions in dense multi-ref prose - WARN-level only;
prose symmetry is model territory; structured-refs cites = citation_sweep.
Usage: check_marks.py rows.jsonl [more...]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ezek_lib import (LAST_VERSE, MT_LAST_VERSE, expand_ref_token,
                     load_pmarks, web_to_mt)

PARAMARK = re.compile(r"\b(petuchah|setumah)\b", re.I)
# bare pe/samekh flag only in mark-talk context (they are also letter names)
PARAMARK_LETTER = re.compile(r"\b(pe|samekh)\b(?!\w)", re.I)
MARKISH_CTX = re.compile(r"\b(?:mark|paragraph|division|petuchah|setumah|"
                         r"seg\b|layout|parashah)", re.I)
SELAH = re.compile(r"\bselah\b", re.I)
FABRICATED_SEGS = re.compile(r"\b(?:inverted|reversed)[\s-]?nun\b|"
                             r"\bsuspended\s+(?:letter|ayin|nun)\b", re.I)
# patch i1 lineage (p06 finding): the claim words are restricted to LETTER
# NAMES so mandatory verbatim WEB quotes cannot false-positive.
_LETTER_NAMES = (r"letter|nun|ayin|mem|yod|waw|vav|kaf|kaph|pe|tsadi|tzadi|"
                 r"qof|qoph|resh|shin|tav|taw|aleph|alef|bet|beth|gimel|"
                 r"dalet|daleth|he|het|chet|heth|tet|teth|lamed|samekh|zayin")
LARGE_LETTER = re.compile(rf"\b(?:large|x-large)\s+(?:{_LETTER_NAMES})\b|"
                          r"\bmajuscule\b", re.I)
SMALL_LETTER = re.compile(rf"\b(?:small|x-small)\s+(?:{_LETTER_NAMES})\b|"
                          r"\bnun\s+ze[i']?ira\b|\bze[i']?ira\b|\bminuscule\b", re.I)
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
PUNCTA_SITES = {(41, 20), (46, 22)}   # MT; asserted by ezek_lib's selftest
CHAPTER_NAMED = re.compile(r"\bch(?:apter|\.)?\s+(\d{1,2})\b", re.I)   # S1-22: 'chapter 10', 'ch 46'
# W1, W2, W5 and W6 (ezek_controlling_rulings_a1#e5 ruling FLAGS-TF2-1), check_marks only; the PUNCTA arm is untouched.
KQ_EXCLUSIVE = re.compile(r"other|further|additional|second|more", re.I)   # W2: an exclusivity word keeps the negation
# W6: the letter-name absence form, admitted only in mark talk (a MARKISH_CTX word within 60 characters, PARAMARK_LETTER's gate)
ABSENCE_LETTER = re.compile(r"\b(?:no|without)\s+(?:(?:a|any)\s+)?(?:pe|samekh)\b(?:\s+(?:or|and|nor)\s+(?:pe|samekh)\b)?", re.I)
EDGE_PUNCT = "()[]{},;:!?\u201c\u201d\u2018\u2019" + chr(34) + chr(39)


def before_readings(c, v):
    # W1: both MT readings of a cited verse and the verse before each. Before a chapter's first verse stands the previous
    # chapter's last MT verse, as relevant() computes the front seam.
    out = []
    for rc, rv in readings(c, v):
        for p in ((rc, rv), (rc, rv - 1) if rv > 1 else (rc - 1, MT_LAST_VERSE.get(rc - 1, 0))):
            if p not in out and p[0] in MT_LAST_VERSE and 1 <= p[1] <= MT_LAST_VERSE[p[0]]:
                out.append(p)
    return out


def letter_absences(text, lo=0, hi=None):
    # W6: every letter-name absence phrase in text[lo:hi] that stands in mark talk
    return [m for m in ABSENCE_LETTER.finditer(text, lo, len(text) if hi is None else hi)
            if MARKISH_CTX.search(text[max(0, m.start() - 60):m.start() + 60])]


def kq_negation(text, start):
    # W2 and W5, rule 4 only. Returns None, "plain" or "exclusive".
    # W2: inside the token's comma-delimited clause, a negator (NEG_WORD) with at most one word between it and the token negates
    # it. Two negators standing together cancel (T1-03). An exclusivity word as that one word returns "exclusive".
    # W5: a negator distributes across a comma list when its own comma-delimited segment is the negator plus at most two words,
    # every intervening segment is at most two words and names no verse, and the token's segment begins with the token
    # (optionally after and/or/nor).
    lo, _ = clause_bounds(text, start, start, NEG_CLAUSE_END)
    words = [w for w in (x.strip(EDGE_PUNCT) for x in text[lo:start].split()) if w]
    for gap in (0, 1):
        k = len(words) - 1 - gap
        if k >= 0 and NEG_WORD.fullmatch(words[k]):
            if k >= 1 and NEG_WORD.fullmatch(words[k - 1]):
                return None
            return "exclusive" if gap == 1 and KQ_EXCLUSIVE.fullmatch(words[-1]) else "plain"
    if [w.lower() for w in words] not in ([], ["and"], ["or"], ["nor"]):
        return None
    f_lo = field_bounds(text, start, start)[0]
    cut = lo
    while cut - 1 >= f_lo and text[cut - 1] == ",":
        seg_lo, _ = clause_bounds(text, cut - 1, cut - 1, NEG_CLAUSE_END)
        seg = text[seg_lo:cut - 1]
        seg_words = [w for w in (x.strip(EDGE_PUNCT) for x in seg.split()) if w]
        if seg_words and NEG_WORD.fullmatch(seg_words[0]) and len(seg_words) <= 3:
            return "plain"
        if len(seg_words) > 2 or RANGE_NUM.search(seg):
            return None
        cut = seg_lo
    return None


def row_named_mt_keys(text):
    # W2's exclusivity scope: the MT keys, under both readings, of every verse number written anywhere in the row. That means
    # C:V, C.V, MT C:V or dotted, in any field, the refs included; a written range names its two ends.
    keys = set()
    for m in RANGE_NUM.finditer(text):
        ends = [(int(m.group(1)), int(m.group(2)))]
        if m.group(4):
            ends.append((int(m.group(3)) if m.group(3) else int(m.group(1)), int(m.group(4))))
        for c0, v0 in ends:
            keys |= {f"Ezek.{rc}.{rv}" for rc, rv in readings(c0, v0)}
    return keys
KQ = re.compile(r"\b(?:ketiv|qere|K/Q)\b", re.I)
VERSE_NEAR = re.compile(r"Ezek\.(\d+)\.(\d+)")
RANGE = re.compile(r"Ezek\.\d+\.\d+(?:-(?:Ezek\.)?\d+(?:\.\d+)?)?")
ABSENCE = re.compile(
    r"\bno\s+(?:petuchah|setumah|parashah|paragraph\s+mark)\b|"
    r"\bwithout\s+(?:a\s+|any\s+)?(?:petuchah|setumah|parashah)\b|"
    r"\blacks?\s+(?:a\s+|any\s+)?(?:petuchah|setumah|parashah)\b|"
    r"\b(?:petuchah|setumah|parashah)\b[^.;]{0,40}?\b(?:is|are)?\s*(?:absent|lacking)\b|"
    r"\b(?:absent|absence)\b[^.;]{0,40}?\b(?:petuchah|setumah|parashah)\b|"
    r"\b(?:petuchah|setumah|parashah)\b[^.;]{0,25}?\babsent\s+from\b", re.I)
PASEQ_POS = re.compile(
    r"\bpaseq\b[^.;]{0,60}?\b(?:after|before|between|precedes|follows|divides|"
    r"separates|splits|mid[\s-]?verse|caesura|colon|cola|hemistich|atnach|"
    r"athnach|first\s+half|second\s+half|word[\s-]?index|offset|midpoint)\b|"
    r"\b(?:after|before|between|mid[\s-]?verse|caesura|colon|cola|hemistich|"
    r"atnach|athnach|word[\s-]?index|offset|midpoint)\b[^.;]{0,60}?\bpaseq\b|"
    r"\b(?:mid[\s-]?verse|verse[\s-](?:initial|final|medial)|first|second|"
    r"third)\s+paseq\b|"
    r"\bpaseq\b[^.;]{0,40}?\b(?:position|placement|located|location|stands\s+"
    r"(?:after|before|between|at))\b", re.I)
PASEQ_POS_NEG = re.compile(
    r"\bnot\s+a\s+positional\b|\bno\s+(?:offset|placement|position|word[\s-]?index)\b|"
    r"\brecords?\s+no\b|\bcount[\s-]only\b|\bbare\s+count\b", re.I)


def rows_from(p: Path):
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    data = json.loads(text)
    if isinstance(data, dict):
        return data.get("decisions", [v for v in data.values() if isinstance(v, dict)])
    return data


def span_pairs(row):
    """Row span pairs in WEB numbering."""
    span = row.get("span") or ""
    m = RANGE.search(span if isinstance(span, str) else "")
    if not m:
        refs = row.get("boundary_evidence_refs", [])
        allp = []
        for r in refs:
            if r.startswith("oshb:"):
                continue
            for mm in RANGE.finditer(r):
                allp.extend(expand_ref_token(mm.group(0)))
        return sorted(set(allp))
    return expand_ref_token(m.group(0))


def relevant(pairs, inv):
    """Inventory entries relevant to a WEB span (front seam + interior + end),
    looked up at the CROSSWALK-MAPPED MT keys."""
    if not pairs:
        return {}
    want = {}
    c0, v0 = pairs[0]
    prev = (c0, v0 - 1) if v0 > 1 else (c0 - 1, LAST_VERSE.get(c0 - 1, 0))
    for c, v in [prev] + pairs:
        if not (c in LAST_VERSE and 1 <= v <= LAST_VERSE.get(c, 0)):
            continue
        mt = web_to_mt(c, v)
        if mt is None:
            continue
        k = f"Ezek.{mt[0]}.{mt[1]}"
        if inv.get(k):
            want[k] = inv[k]
    return want


def prose_of(row) -> str:
    parts = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k != "boundary_evidence_refs":
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str):
            parts.append(o)
    walk(row)
    return "\n".join(parts)


def near_diag(inv, c, v):
    hits = [f"Ezek.{c}.{x}" for x in (v - 1, v + 1) if inv.get(f"Ezek.{c}.{x}")]
    return {"adjacent_mt_inventory_hits": hits} if hits else {}


def readings(c: int, v: int) -> list[tuple[int, int]]:
    """Both MT readings of a cited verse number: direct MT, and WEB->MT
    mapped. Coincide outside WEB 20:45-21:32 / MT ch 21."""
    out = []
    if c in MT_LAST_VERSE and 1 <= v <= MT_LAST_VERSE[c]:
        out.append((c, v))
    mt = web_to_mt(c, v)
    if mt and mt not in out:
        out.append(mt)
    return out


def main() -> int:
    pm = load_pmarks()
    marks, kq = pm["marks"], pm["kq"]
    small_inv = pm.get("other_segs", {})
    # Ezek: verses whose OSHB editorial note speaks of ketib/qere - backed by bytes, but not in the kq inventory
    kq_note_keys = {k for k, notes in pm.get("notes_other", {}).items()
                    if any(KQ_NOTE.search(n.get("text", "")) for n in notes)}
    flags = []
    warns = []
    n = cited = 0
    for f in sys.argv[1:]:
        for row in rows_from(Path(f)):
            if not isinstance(row, dict):
                continue
            n += 1
            did = row.get("decision_id", "?")
            text = prose_of(row) + " " + " ".join(row.get("boundary_evidence_refs", []))
            # Rule 0: fabricated seg classes for Ezek
            for m in SELAH.finditer(text):
                flags.append({"decision_id": did, "rule": "selah_claim_in_jer",
                              "note": "NO selah exists in Ezek (Psalter device)",
                              "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
            for m in FABRICATED_SEGS.finditer(text):
                flags.append({"decision_id": did, "rule": "nonexistent_seg_claim_in_jer",
                              "claim": m.group(0),
                              "note": "WLC Ezek carries no reversed-nun or suspended-letter segs",
                              "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
            for m in LARGE_LETTER.finditer(text):
                flags.append({"decision_id": did, "rule": "large_letter_claim_in_jer",
                              "claim": m.group(0),
                              "note": "WLC Ezek carries NO special-letter seg of any class",
                              "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
            # small-letter claims: valid ONLY when bound (window heuristic) to an
            # inventory site - Ezek has none, so every small-letter claim flags
            for m in SMALL_LETTER.finditer(text):
                lo = max(0, m.start() - 120)
                ctx = text[lo:m.start() + 120]
                cands = list(VERSE_NEAR.finditer(ctx))
                ok = any(small_inv.get(f"Ezek.{rc}.{rv}")
                         for vm in cands
                         for rc, rv in readings(int(vm.group(1)), int(vm.group(2))))
                if not ok:
                    flags.append({"decision_id": did, "rule": "small_letter_claim_in_jer",
                                  "claim": m.group(0),
                                  "note": ("WLC Ezek carries NO special-letter seg of any class - "
                                           "every small-letter claim is a fabrication"),
                                  "claim_context": text[lo:m.start() + 80]})
            # PUNCTA arm (Ezek): U+05C4 stands in the verse bytes at MT 41:20 and 46:22 only. A claim is judged on
            # the verse numbers in its own clause within 60 characters of the word (PROSE_REACH, kept for prose) and
            # every number in a parenthetical opening directly after that clause, in the same field (R4(ii),
            # ezek_controlling_rulings_a1#e3; a range counts as its
            # verses): all sites -> true, none -> false, a mix -> ambiguous, flagged (T2-01/02). A claim naming no
            # number is satisfied only when the row's span covers a site (T1-02). A negation earlier in the same
            # comma-delimited clause makes it an absence claim; adjacent negators cancel (T1-03, T2-03); so does a closed-set
            # denial later in the clause (T4-03).
            span_sites = sorted({web_to_mt(c, v) for c, v in span_pairs(row)} & PUNCTA_SITES)
            for m in PUNCTA.finditer(text):
                lo = max(0, m.start() - 120)
                verdict = puncta_verdict(puncta_claim_numbers(text, m.start(), m.end(), PROSE_REACH, upper=claim_upper(text, m.end())))
                at_site = bool(span_sites) if verdict is None else verdict
                if puncta_negated(text, m.start(), m.end()):
                    if at_site is True or at_site == "ambiguous":
                        flags.append({"decision_id": did, "rule": "false_puncta_absence_claim",
                                      "span_sites_mt": ["Ezek.%d.%d" % s for s in span_sites],
                                      "numbers_in_clause": verdict is not None,
                                      "claim_context": text[lo:m.start() + 80]})
                    continue
                if at_site is not True:
                    flags.append({"decision_id": did, "rule": "puncta_claim_in_ezek",
                                  "claim": m.group(0), "ambiguous": at_site == "ambiguous",
                                  "note": ("the puncta extraordinaria (U+05C4) stand only at MT 41:20 and MT 46:22 - "
                                           "the claim names another verse, mixes a site with another verse, or names "
                                           "none and its row covers neither"),
                                  "claim_context": text[lo:m.start() + 80]})
            # Rule 1: petuchah/setumah claims bind to the NEAREST windowed ref
            # under the CORRECT mark type, dual-reading (MT direct + WEB-mapped)
            markish = list(PARAMARK.finditer(text)) + [
                m for m in PARAMARK_LETTER.finditer(text)
                if MARKISH_CTX.search(text[max(0, m.start() - 60):m.start() + 60])]
            if markish:
                cited += 1
            for m in markish:
                word = m.group(0).lower()
                want_type = "PE" if word in ("petuchah", "pe") else "SAMEKH"
                # S1-22 (ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 (b)): the claim binds to the verse numbers written in
                # its OWN clause - C:V, C.V, 'MT C:V' or a dotted ref alike - plus a parenthetical opening directly after it; a
                # claim naming no number in its clause is left to rule 2 (symmetry)
                c_lo_, c_hi_ = clause_bounds(text, m.start(), m.end(), NUM_CLAUSE_END)
                named_ = [p for pairs in puncta_claim_numbers(text, m.start(), m.end()) for p in pairs]
                if not named_:
                    continue
                # W1 (ezek_controlling_rulings_a1#e5 ruling FLAGS-TF2-1): a mark of the claimed TYPE after N or after N-1 satisfies
                # the claim; the type test is untouched, and an absence claim never takes the N-1 acceptance (rule 3 reads N)
                if any(want_type in marks.get(f"Ezek.{rc}.{rv}", [])
                       for c0, v0 in named_
                       for rc, rv in before_readings(c0, v0)):
                    continue
                # W6 (#e5 FLAGS-TF2-1): the letter-name absence form is an absence phrase, so rule 1 skips its clause
                if ABSENCE.search(text[c_lo_:c_hi_]) or letter_absences(text, c_lo_, c_hi_):
                    continue
                c, v = named_[0]
                got = {f"Ezek.{rc}.{rv}": marks.get(f"Ezek.{rc}.{rv}", [])
                       for rc, rv in readings(c, v)}
                flags.append({"decision_id": did, "rule": "paragraph_mark_claim",
                              "claimed": want_type, "verse_cited": f"Ezek.{c}.{v}",
                              "inventory_under_both_readings": got,
                              "note": ("mark TYPE mismatch - PE and SAMEKH are never conflated"
                                       if any(got.values()) else "no mark at the cited verse under either reading"),
                              **near_diag(marks, c, v)})
            # Rule 3: absence arm, span-scoped
            # S1-22 (#e4 ruling TOOLFIX-2 (b)): an absence phrase is scoped to the verse, range or chapter its own clause
            # names; an absence phrase naming none keeps the span-scoped check
            for am in sorted(list(ABSENCE.finditer(text)) + letter_absences(text), key=lambda x: x.start()):   # W6 (#e5 FLAGS-TF2-1)
                named_ = [p for pairs in puncta_claim_numbers(text, am.start(), am.end()) for p in pairs]
                c_lo_, c_hi_ = clause_bounds(text, am.start(), am.end(), NUM_CLAUSE_END)
                for chm_ in CHAPTER_NAMED.finditer(text, c_lo_, c_hi_):
                    ch_ = int(chm_.group(1))
                    named_ += [(ch_, vv_) for vv_ in range(1, MT_LAST_VERSE.get(ch_, 0) + 1)]
                if named_:
                    scope_ = "named"
                    have = {f"Ezek.{rc}.{rv}": marks[f"Ezek.{rc}.{rv}"] for c0, v0 in named_ for rc, rv in readings(c0, v0)
                            if marks.get(f"Ezek.{rc}.{rv}")}
                else:
                    scope_ = "span"
                    have = relevant(span_pairs(row), marks)
                if have:
                    flags.append({"decision_id": did, "rule": "false_mark_absence_claim", "scope": scope_,
                                  "claim_context": text[max(0, am.start() - 60):am.start() + 80],
                                  "span_relevant_marks_mt_keys": have})
                    break
            # Rule 2: symmetry over the span-relevant set (unconditional)
            want = relevant(span_pairs(row), marks)
            for ref, types in want.items():
                _, c, v = ref.split(".")
                near = re.compile(rf"{re.escape(ref)}|\b{c}[:.]{v}\b")
                disclosed = any(
                    PARAMARK.search(text[max(0, m.start() - 160):m.start() + 160])
                    or PARAMARK_LETTER.search(text[max(0, m.start() - 160):m.start() + 160])
                    for m in near.finditer(text))
                if not disclosed:
                    flags.append({"decision_id": did, "rule": "mark_symmetry_gap",
                                  "undisclosed_mt_key": ref, "mark_types": types,
                                  "row_cites_marks": bool(markish)})
            # WARN: paseq position assertions (inventory is count-only)
            for pm_ in PASEQ_POS.finditer(text):
                lo = max(0, pm_.start() - 120)
                ctx = text[lo:pm_.end() + 120]
                if PASEQ_POS_NEG.search(ctx):
                    continue
                warns.append({"decision_id": did, "rule": "paseq_position_warn",
                              "claim": pm_.group(0)[:120],
                              "note": "pmarks paseq is COUNT-ONLY (no offsets/"
                                      "word indices) - position is unsourceable",
                              "claim_context": text[lo:pm_.end() + 80]})
            # Rule 4: K/Q prose claims bind to the NEAREST windowed ref,
            # dual-reading (MT direct + WEB-mapped)
            # S1-22 (#e4 ruling TOOLFIX-2 (b)): a K/Q claim binds to the verse numbers in its OWN clause (C:V, C.V, 'MT C:V'
            # or dotted); a NEGATED K/Q token is an absence claim, checked against the verses its clause names or, naming
            # none, the span's kq keys (rule false_kq_absence_claim)
            for m in KQ.finditer(text):
                lo = max(0, m.start() - 120)
                ctx = text[lo:m.start() + 120]
                named_ = [p for pairs in puncta_claim_numbers(text, m.start(), m.end()) for p in pairs]
                # W2 and W5 (ezek_controlling_rulings_a1#e5 ruling FLAGS-TF2-1): kq_negation reads the negation (a negator at most
                # one word before the token, or heading a short comma list); T4-03's closed-set denial after the token still
                # denies. An exclusivity word ('no other K/Q') narrows the scope to the span's kq keys the row names nowhere.
                neg_ = kq_negation(text, m.start()) or ("plain" if denied_after(text, m.end()) else None)
                if neg_:
                    if neg_ == "exclusive":
                        scope_ = "span_unnamed"
                        keys_ = {f"Ezek.{mt_[0]}.{mt_[1]}" for c0, v0 in span_pairs(row) for mt_ in [web_to_mt(c0, v0)] if mt_} - row_named_mt_keys(text)
                    elif named_:
                        scope_ = "named"
                        keys_ = {f"Ezek.{rc}.{rv}" for c0, v0 in named_ for rc, rv in readings(c0, v0)}
                    else:
                        scope_ = "span"
                        keys_ = {f"Ezek.{mt_[0]}.{mt_[1]}" for c0, v0 in span_pairs(row) for mt_ in [web_to_mt(c0, v0)] if mt_}
                    present_ = sorted(k_ for k_ in keys_ if kq.get(k_))
                    if present_:
                        flags.append({"decision_id": did, "rule": "false_kq_absence_claim", "scope": scope_,
                                      "kq_mt_keys": present_, "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
                    continue
                if not named_:
                    continue
                if any(kq.get(f"Ezek.{rc}.{rv}") or (f"Ezek.{rc}.{rv}" in kq_note_keys and NOTE_WORD.search(ctx))
                       for c0, v0 in named_
                       for rc, rv in readings(c0, v0)):
                    continue
                c, v = named_[0]
                flags.append({"decision_id": did, "rule": "kq_claim",
                              "verse_cited": f"Ezek.{c}.{v}", **near_diag(kq, c, v)})
    print(json.dumps({"rows_checked": n, "rows_citing_marks": cited,
                      "flag_count": len(flags), "flags": flags,
                      "warn_count": len(warns), "warns": warns,
                      "status": "GREEN" if not flags else "FLAGS"},
                     ensure_ascii=False, indent=1))
    return 1 if flags else 0


if __name__ == "__main__":
    raise SystemExit(main())
