#!/usr/bin/env python3
"""check_marks.py - 1Cor (T3 port of the predecessor's check_marks; the tool name, rule ids and selftest flag are kept).

1 Corinthians is a Greek book. pmarks_1Cor.json carries three mark-like claim types, never conflated here:
  RP   Byzantine RP pilcrows (rp_paragraph_starts, 35 verses), keyed at the verse that BEGINS a paragraph
  WEB  WEB paragraphs (web_paragraph_starts, 87, plus web_paragraph_midverse, 1), keyed the same way
  SBL  SBLGNT critical signs (sbl_variant_sites, 220 verses), keyed at the verse that carries the sign
The claim vocabulary (MARK_CLAIM): 'RP / Robinson-Pierpont / Byzantine paragraph|pilcrow|¶', a bare 'pilcrow', '¶'
or 'paragraph mark' (RP, the primary witness), 'WEB paragraph|pilcrow|section break', 'SBL(GNT) sign|sigla|siglum|
variant site', 'critical|variant sign', and a standalone sign glyph (a glyph touching a letter belongs to a quoted
SBLGNT run and is no claim). A bare 'paragraph' is never a claim.
The Hebrew-witness device arms keep their rule ids over EMPTY inventories (PE/SAMEKH petuchah and setumah, K/Q, paseq,
special letters, puncta, selah): a positive claim is RED and a denial passes.
The crosswalk is the identity (web_greek_offset_map.json: identity_throughout true, zones []), so the direct and the
mapped reading of every verse number coincide; --marks3d-selftest and _test_marks_tools_1cor.py test all 437 verses.

Rules:
  0  selah, special letters, fabricated segs, puncta: fabrication classes (no site in 1Cor).
  1  a mark claim binds to the verse numbers in its own clause (S1-22) under its own type. W1 per keying: an RP or
     WEB claim at N is met by a start at N or N+1 ('a pilcrow after 1:3' names the start keyed at 1:4); an SBL claim
     reads N only. A claim naming no number is left to rules 2 and 3, except a PE/SAMEKH claim, which is RED.
  2  symmetry, RP only: an RP start at the row's onset seam, interior or close seam that the row does not disclose with
     an RP claim near that verse number is flagged. WEB and SBL take no symmetry duty here.
  3  absence: each absence phrase is typed (absence_types) and judged against its own type only, scoped to the verses
     its clause names or else to the span interior under the type's keying.
  4  K/Q (no layer): a positive claim, numbered or not, is RED; a denial passes.
  paseq (no layer): a presence claim, numbered or not, is RED; a denial passes; position claims stay WARN.

Lineage: ported by _adapt_tools_1cor.py with spec_t3.py from the predecessor toolkit's check_marks.py; the rule ids
(selah_claim_in_jer, puncta_claim_in_ezek and the rest) and the ruling ids (S1-22, W1-W6, MARKS-3D, T1-T4, R4(ii)) are kept.

Usage: check_marks.py rows.jsonl [...] | --marks3d-selftest
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cor_lib import (LAST_VERSE, MT_LAST_VERSE, expand_ref_token,
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

# T3 (1Cor): the three claim types of pmarks_1Cor.json, never conflated (module docstring). The WEB arm is tried at the
# qualifier, so 'WEB pilcrow' is a WEB claim; a bare pilcrow, ¶ or paragraph mark is RP; a bare 'paragraph' is no claim.
MARK_CLAIM = re.compile(
    r"(?P<WEB>\b(?-i:WEB)(?:'s)?\s+(?:paragraph|pilcrow|¶|section\s+break)s?(?!\w))"
    r"|(?P<RP>\b(?:(?-i:RP)|Robinson[-\s]Pierpont|Byzantine)(?:'s)?\s+(?:paragraph|pilcrow|¶)s?(?!\w)"
    r"|¶|\bpilcrows?\b|\bparagraph\s+marks?\b)"
    r"|(?P<SBL>\b(?-i:SBL(?:GNT)?)(?:'s)?\s+(?:critical\s+|variant\s+)?(?:signs?|sigla|siglum|variant\s+sites?)\b"
    r"|\b(?:critical|variant)\s+(?:signs?|sigla|siglum)\b|[⸀-⸅])", re.I)
SIGN_GLYPH = re.compile(r"[⸀-⸅]")
# T3: where each type is keyed. 'start': a start keyed at N begins verse N (RP, WEB). 'verse': a sign keyed at N stands
# inside N (SBL). 'after': a mark keyed at N stands after N (the predecessor's PE/SAMEKH; empty in 1Cor).
KEYING = {"RP": "start", "WEB": "start", "SBL": "verse", "PE": "after", "SAMEKH": "after"}


def build_marks(pm):
    """{key: [types]} from pmarks_1Cor.json: RP from rp_paragraph_starts, WEB from web_paragraph_starts plus
    web_paragraph_midverse, SBL from the keys of sbl_variant_sites."""
    out = {}

    def add(k, t):
        ts = out.setdefault(k, [])
        if t not in ts:
            ts.append(t)
    for k in pm.get("rp_paragraph_starts", []):
        add(k, "RP")
    for k in list(pm.get("web_paragraph_starts", [])) + list(pm.get("web_paragraph_midverse", [])):
        add(k, "WEB")
    for k in pm.get("sbl_variant_sites", {}):
        add(k, "SBL")
    return out


def _sign_in_run(text, i, j):
    """A sign glyph touching a letter or a combining mark is part of a quoted SBLGNT run, not a claim about a sign."""
    near = (text[i - 1] if i > 0 else "") + (text[j] if j < len(text) else "")
    return any(unicodedata.category(ch)[0] in "LM" for ch in near)


def mark_claims(text):
    """[(type, match)] in text order: the RP, WEB and SBL claims (MARK_CLAIM) and the PE/SAMEKH claims (PARAMARK, and a
    bare pe or samekh only in mark talk, PARAMARK_LETTER's gate)."""
    out = []
    for m in MARK_CLAIM.finditer(text):
        if SIGN_GLYPH.fullmatch(m.group(0)) and _sign_in_run(text, m.start(), m.end()):
            continue
        out.append((m.lastgroup, m))
    for m in PARAMARK.finditer(text):
        out.append(("PE" if m.group(1).lower() == "petuchah" else "SAMEKH", m))
    for m in PARAMARK_LETTER.finditer(text):
        if MARKISH_CTX.search(text[max(0, m.start() - 60):m.start() + 60]):
            out.append(("PE" if m.group(1).lower() == "pe" else "SAMEKH", m))
    return sorted(out, key=lambda x: x[1].start())


def field_bounds(text, start, end):
    """The span of the one field a match sits in: check_marks joins every row field with newlines, so a window that
    crossed a newline would read another field - the span string included - as part of the claim."""
    nl = text.find("\n", end)
    return text.rfind("\n", 0, start) + 1, (nl if nl != -1 else len(text))


# Clause and sentence marks. A period ends a clause only before whitespace or the end (so 1Cor.4.20 and 4.20 never
# split); a colon only when no digit follows (so 4:20 never splits); ';', ',', '(' and ')' always - including right
# after a digit, as in '4:20;' (the first version's digit lookbehind let a decoy number leak across that semicolon).
NEG_CLAUSE_END = re.compile(r"\.(?=\s|$)|:(?!\d)|[;,()]")   # a negation's scope ends at any clause mark
NUM_CLAUSE_END = re.compile(r"\.(?=\s|$)|[;()]")            # a claim's numbers stay together across commas
# T4-01: digits that follow a letter directly ('R4.5', a ruling or row id) are an id, never a verse number
RANGE_NUM = re.compile(r"(?<![A-Za-z\d])(\d{1,2})[:.](\d{1,2})(?:\s*[-–]\s*(?:(\d{1,2})[:.])?(\d{1,2}))?(?!\d)")
SENT_END = re.compile(r"\.(?=\s|$)|;|\n")
PUNCTA_SITE_PAIRS = set()   # 1Cor: no Hebrew code point stands in 1Cor_rp.txt or 1Cor_sbl.txt (_test_marks_tools_1cor.py asserts it)


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
KQ_NOTE = re.compile(r"\bketi[bv]\b|\bqere\b|\bK/Q\b", re.I)   # lineage: the predecessor's note route; closed in 1Cor (kq_note_keys is empty)
NOTE_WORD = re.compile(r"\bnotes?\b|\beditorial\b", re.I)
PUNCTA_SITES = set()   # EMPTY in 1Cor: no Hebrew code point in either Greek witness (the T3 test asserts it)
CHAPTER_NAMED = re.compile(r"\bch(?:apter|\.)?\s+(\d{1,2})\b", re.I)   # S1-22: 'chapter 10', 'ch 46'
# W1, W2, W5 and W6 (ezek_controlling_rulings_a1#e5 ruling FLAGS-TF2-1), check_marks only; the PUNCTA arm is untouched.
KQ_EXCLUSIVE = re.compile(r"other|further|additional|second|more", re.I)   # W2: an exclusivity word keeps the negation
# W6: the letter-name absence form, admitted only in mark talk (a MARKISH_CTX word within 60 characters, PARAMARK_LETTER's gate)
ABSENCE_LETTER = re.compile(r"\b(?:no|without)\s+(?:(?:a|any)\s+)?(?:pe|samekh)\b(?:\s+(?:or|and|nor)\s+(?:pe|samekh)\b)?", re.I)
EDGE_PUNCT = "()[]{},;:!?\u201c\u201d\u2018\u2019" + chr(34) + chr(39)


def before_readings(c, v, mtype=None):
    # W1, per keying (T3). After-keyed PE/SAMEKH (the predecessor's reading): the cited verse and the verse before it,
    # across a chapter start. Start-keyed RP/WEB: the cited verse and the verse after it, across a chapter end ('a
    # pilcrow after 1:3' names the start keyed at 1:4). Verse-keyed SBL: the cited verse only.
    keying = KEYING.get(mtype, "after")
    out = []
    for rc, rv in readings(c, v):
        if keying == "verse":
            cand = ((rc, rv),)
        elif keying == "start":
            cand = ((rc, rv), (rc, rv + 1) if rv < MT_LAST_VERSE.get(rc, 0) else (rc + 1, 1))
        else:
            cand = ((rc, rv), (rc, rv - 1) if rv > 1 else (rc - 1, MT_LAST_VERSE.get(rc - 1, 0)))
        for p in cand:
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
            keys |= {f"1Cor.{rc}.{rv}" for rc, rv in readings(c0, v0)}
    return keys
KQ = re.compile(r"\b(?:ketiv|qere|K/Q)\b", re.I)
VERSE_NEAR = re.compile(r"1Cor\.(\d+)\.(\d+)")
RANGE = re.compile(r"1Cor\.\d+\.\d+(?:-(?:1Cor\.)?\d+(?:\.\d+)?)?")
# T3: the absence vocabulary covers the three Greek-book claim types and the predecessor's Hebrew mark words; each
# phrase is typed by absence_types and judged only against its own type (rule 3)
_MW = (r"(?:petuchah|setumah|parashah|pilcrows?|¶|paragraph\s+(?:marks?|starts?|breaks?)"
       r"|(?-i:RP|WEB)(?:'s)?\s+(?:paragraph|pilcrow)(?:\s+(?:start|break|mark))?s?"
       r"|(?:(?-i:SBL(?:GNT)?)(?:'s)?\s+)?(?:critical|variant)\s+(?:signs?|sigla|siglum)"
       r"|(?-i:SBL(?:GNT)?)(?:'s)?\s+(?:signs?|sigla|siglum))")
ABSENCE = re.compile(
    rf"(?<!\w)no\s+{_MW}(?!\w)|"
    rf"(?<!\w)without\s+(?:a\s+|any\s+)?{_MW}(?!\w)|"
    rf"(?<!\w)lacks?\s+(?:a\s+|any\s+)?{_MW}(?!\w)|"
    rf"(?<!\w){_MW}[^.;]{{0,40}}?(?<!\w)(?:is|are)?\s*(?:absent|lacking)(?!\w)|"
    rf"(?<!\w)(?:absent|absence)(?!\w)[^.;]{{0,40}}?{_MW}(?!\w)|"
    rf"(?<!\w){_MW}[^.;]{{0,25}}?(?<!\w)absent\s+from(?!\w)", re.I)
_HEB_MARK_WORD = re.compile(r"petuchah|setumah|parashah|(?<!\w)(?:pe|samekh)(?!\w)", re.I)
_SBL_WORD = re.compile(r"(?-i:SBL)|critical|variant", re.I)
_WEB_WORD = re.compile(r"(?<!\w)WEB(?!\w)")
AFTER_WORD = re.compile(r"\b(?:after|follows?|following)\b", re.I)


def absence_types(phrase):
    """T3: the one claim type an absence phrase denies. An unqualified pilcrow, ¶ or paragraph mark denies an RP start
    (RP is the primary witness); a WEB paragraph a WEB start; an SBL, critical or variant sign an SBLGNT sign; a
    Masoretic mark word the empty PE/SAMEKH layer."""
    if _HEB_MARK_WORD.search(phrase):
        return {"PE", "SAMEKH"}
    if _SBL_WORD.search(phrase):
        return {"SBL"}
    if _WEB_WORD.search(phrase):
        return {"WEB"}
    return {"RP"}


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
PASEQ_PRESENCE = re.compile(r"\bpaseq\s+(?:(?:at|in)\s+)?(?:MT\s+)?(\d{1,2})[:.](\d{1,3})\b", re.I)   # S1-08 (c)
PASEQ_ABSENT_BEFORE = re.compile(r"\b(?:no|not|nor|without|lacks?|lacking|absent)\b[^.;\n]*$", re.I)
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
            # T3: 1Cor has no Hebrew-witness ref space; web:/rp:/sbl: refs share one identity numbering
            for mm in RANGE.finditer(r):
                allp.extend(expand_ref_token(mm.group(0)))
        return sorted(set(allp))
    return expand_ref_token(m.group(0))


# ------------------------------------------------- MARKS-3D (#e12 ruling): label each mark's direction
#
# The ruled vocabulary, which is what makes the three duties separable:
#   onset_seam  the verse BEFORE the row's first verse - a mark there stands at the onset
#   interior    first verse through LAST-BUT-ONE - a mark there is weighed and never cuts alone
#   close_seam  the row's LAST verse - a mark there stands at the close, NOT inside the span
#
# Before this, an absence claim scoped to "the span" was tested against all three, so a row that truly had no
# interior mark was flagged for a mark sitting at its close seam. That is a false positive by construction.
DIRECTION_VOCABULARY = {
    "onset_seam": "the verse before the row's first verse; a mark there stands at the onset seam",
    "interior": "first verse through last-but-one; a mark there is weighed and never cuts alone",
    "close_seam": "the row's last verse; a mark there stands at the close seam and is NOT inside the span",
}


DIRECTION_VOCABULARY_START = {
    "onset_seam": "the row's first verse; a start there opens the row at the onset seam",
    "interior": "second verse through last; a start there is a break inside the row, weighed and never cutting alone",
    "close_seam": "the verse after the row's last; a start there opens the next row and is NOT inside the span",
}


def relevant_by_direction(pairs, inv, keying="after"):
    """Same set as relevant(), with each key tagged by its direction. Returns {ref: (types, direction)}.
    T3 keying: 'after' is the predecessor's (a mark keyed at N stands after N: onset = the verse before the first,
    interior = first..last-but-one, close = last); 'start' is RP/WEB (a start keyed at N begins N: onset = first,
    interior = second..last, close = the verse after the last, across a chapter end); 'verse' is SBL (a sign keyed at
    N stands inside N: every span verse is interior and there is no seam)."""
    if not pairs:
        return {}
    out = {}
    if keying == "start":
        cl, vl = pairs[-1]
        nxt = (cl, vl + 1) if vl < LAST_VERSE.get(cl, 0) else (cl + 1, 1)
        tagged = [(pairs[0], "onset_seam")] + [(p, "interior") for p in pairs[1:]] + [(nxt, "close_seam")]
    elif keying == "verse":
        tagged = [(p, "interior") for p in pairs]
    else:
        c0, v0 = pairs[0]
        prev = (c0, v0 - 1) if v0 > 1 else (c0 - 1, LAST_VERSE.get(c0 - 1, 0))
        tagged = [(prev, "onset_seam")] + [(p, "interior") for p in pairs[:-1]] + [(pairs[-1], "close_seam")]
    for (c, v), direction in tagged:
        if not (c in LAST_VERSE and 1 <= v <= LAST_VERSE.get(c, 0)):
            continue
        mt = web_to_mt(c, v)
        if mt is None:
            continue
        ref = "1Cor.%d.%d" % mt
        types = inv.get(ref)
        if types:
            out[ref] = (types, direction)
    return out


def interior_only(pairs, inv, keying="after"):
    """The marks a span-scoped ABSENCE claim is judged against, under the ruled vocabulary and the type's keying."""
    return {r: t for r, (t, d) in relevant_by_direction(pairs, inv, keying).items() if d == "interior"}


def _marks3d_selftest():
    cases = []
    inv = {}
    # lineage cases (the predecessor's after-keyed vocabulary, keying 'after'): a fabricated inventory over a 5-verse
    # span in one chapter, with a mark at each direction
    span = [(9, 10), (9, 11), (9, 12), (9, 13), (9, 14)]
    for c, v in [(9, 9)] + span:
        inv["1Cor.%d.%d" % (c, v)] = ["setumah"]
    tagged = relevant_by_direction(span, inv)
    cases.append(("the verse before the first is the onset seam",
                  tagged.get("1Cor.9.9", (None, None))[1] == "onset_seam"))
    cases.append(("the last verse is the close seam, not interior",
                  tagged.get("1Cor.9.14", (None, None))[1] == "close_seam"))
    cases.append(("the first verse is interior",
                  tagged.get("1Cor.9.10", (None, None))[1] == "interior"))
    cases.append(("last-but-one is interior",
                  tagged.get("1Cor.9.13", (None, None))[1] == "interior"))
    io = interior_only(span, inv)
    cases.append(("an interior-only view excludes the close seam", "1Cor.9.14" not in io))
    cases.append(("an interior-only view excludes the onset seam", "1Cor.9.9" not in io))
    cases.append(("an interior-only view keeps the four interior verses", len(io) == 4))
    inv2 = {"1Cor.9.14": ["setumah"]}
    cases.append(("a row whose only mark is at its close seam has NO interior mark - "
                  "this is the false positive the ruling found",
                  interior_only(span, inv2) == {}))
    cases.append(("and that mark is still reported, as the close seam",
                  relevant_by_direction(span, inv2)["1Cor.9.14"][1] == "close_seam"))
    one = [(9, 20)]
    inv3 = {"1Cor.9.19": ["pe"], "1Cor.9.20": ["setumah"]}
    t1 = relevant_by_direction(one, inv3)
    cases.append(("a one-verse row has an onset seam and a close seam and no interior",
                  t1["1Cor.9.19"][1] == "onset_seam" and t1["1Cor.9.20"][1] == "close_seam"
                  and interior_only(one, inv3) == {}))
    # T3 identity (replaces the predecessor's zone case): the 1Cor crosswalk is the identity, so a WEB verse is read
    # at its own key, the direct and mapped readings coincide, and a neighbour stays outside the span
    zspan = [(4, 1), (4, 2)]
    zkey = "1Cor.%d.%d" % web_to_mt(4, 1)
    zinv = {zkey: ["setumah"], "1Cor.4.3": ["pe"]}
    zt = relevant_by_direction(zspan, zinv)
    cases.append(("identity: WEB 4:1 is read at its own key 1Cor.4.1 (interior), and 4:3 stays outside the span",
                  zkey == "1Cor.4.1" and zt.get(zkey, (None, None))[1] == "interior" and "1Cor.4.3" not in zt))
    allv = [(c, v) for c in sorted(LAST_VERSE) for v in range(1, LAST_VERSE[c] + 1)]
    cases.append(("identity over every verse (%d): web_to_mt is the identity and readings() is one pair" % len(allv),
                  all(web_to_mt(c, v) == (c, v) and readings(c, v) == [(c, v)] for c, v in allv)))
    op = [(9, 1), (9, 2)]
    inv4 = {"1Cor.8.%d" % LAST_VERSE[8]: ["pe"]}
    cases.append(("a span opening a chapter finds its onset seam in the previous chapter",
                  relevant_by_direction(op, inv4).get("1Cor.8.%d" % LAST_VERSE[8],
                                                      (None, None))[1] == "onset_seam"))
    # T3 start keying (RP, WEB): a start keyed at N begins N
    sinv = {"1Cor.9.%d" % v: ["RP"] for v in range(10, 16)}
    st = relevant_by_direction(span, sinv, "start")
    cases.append(("start: the first verse is the onset seam", st.get("1Cor.9.10", (None, None))[1] == "onset_seam"))
    cases.append(("start: the second through the last verse are interior",
                  all(st.get("1Cor.9.%d" % v, (None, None))[1] == "interior" for v in range(11, 15))))
    cases.append(("start: the verse after the last is the close seam", st.get("1Cor.9.15", (None, None))[1] == "close_seam"))
    cases.append(("start: an interior-only view keeps the second through the last verse",
                  sorted(interior_only(span, sinv, "start")) == ["1Cor.9.%d" % v for v in range(11, 15)]))
    cases.append(("start: a one-verse row has no interior",
                  interior_only([(9, 20)], {"1Cor.9.20": ["RP"], "1Cor.9.21": ["RP"]}, "start") == {}))
    cend = [(8, LAST_VERSE[8] - 1), (8, LAST_VERSE[8])]
    cases.append(("start: a row closing a chapter has its close seam at the next chapter's first verse",
                  relevant_by_direction(cend, {"1Cor.9.1": ["RP"]}, "start").get("1Cor.9.1", (None, None))[1] == "close_seam"))
    vinv = dict(sinv, **{"1Cor.9.9": ["SBL"]})
    cases.append(("verse: every span verse is interior and nothing outside the span is read",
                  interior_only(span, vinv, "verse") == {k: x for k, x in sinv.items() if k != "1Cor.9.15"}))
    cases.append(("W1 start reads N and N+1; verse keying reads N only",
                  before_readings(1, 3, "RP") == [(1, 3), (1, 4)] and before_readings(1, 3, "SBL") == [(1, 3)]))
    cases.append(("W1 start across a chapter end reads the next chapter's first verse",
                  before_readings(1, LAST_VERSE[1], "WEB") == [(1, LAST_VERSE[1]), (2, 1)]))
    width = max(len(n) for n, _ in cases)
    for n, ok in cases:
        print("  %s  %s" % ("PASS" if ok else "FAIL", n.ljust(width)))
    bad = [n for n, ok in cases if not ok]
    print("\nMARKS-3D selftest: %d/%d passed" % (len(cases) - len(bad), len(cases)))
    return 1 if bad else 0


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
        k = f"1Cor.{mt[0]}.{mt[1]}"
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
    hits = [f"1Cor.{c}.{x}" for x in (v - 1, v + 1) if inv.get(f"1Cor.{c}.{x}")]
    return {"adjacent_mt_inventory_hits": hits} if hits else {}


def readings(c: int, v: int) -> list[tuple[int, int]]:
    """Both readings of a cited verse number: direct, and WEB->Greek mapped. T3: the 1Cor crosswalk is the identity
    (web_greek_offset_map.json: identity_throughout true, zones []), so the two readings coincide for every verse."""
    out = []
    if c in MT_LAST_VERSE and 1 <= v <= MT_LAST_VERSE[c]:
        out.append((c, v))
    mt = web_to_mt(c, v)
    if mt and mt not in out:
        out.append(mt)
    return out


def main() -> int:
    pm = load_pmarks()
    # T3 (1Cor): the three claim types of pmarks_1Cor.json, never conflated - RP pilcrows (rp_paragraph_starts), WEB
    # paragraphs (web_paragraph_starts + web_paragraph_midverse) and SBLGNT critical signs (sbl_variant_sites). The
    # Hebrew-witness layers (PE/SAMEKH, K/Q, special letters, paseq, editorial notes) have no 1Cor site: each inventory
    # below is EMPTY, so a positive claim is RED and a denial passes.
    marks = build_marks(pm)
    by_type = {t: {k: [t] for k, ts in marks.items() if t in ts} for t in ("RP", "WEB", "SBL", "PE", "SAMEKH")}
    kq = {}
    small_inv = {}
    paseq_verses = set()
    # T3: the note route is closed. The predecessor accepted a numbered K/Q claim at a verse whose editorial note spoke
    # of ketib/qere; web_footnote_verses are WEB translation footnotes and never a K/Q note, so no verse qualifies
    kq_note_keys = set()
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
            # Rule 0: fabrication classes for 1Cor (the rule ids are the predecessor toolkit's: lineage)
            for m in SELAH.finditer(text):
                flags.append({"decision_id": did, "rule": "selah_claim_in_jer",
                              "note": "NO selah exists in 1Cor (Psalter device)",
                              "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
            for m in FABRICATED_SEGS.finditer(text):
                flags.append({"decision_id": did, "rule": "nonexistent_seg_claim_in_jer",
                              "claim": m.group(0),
                              "note": "1Cor is a Greek book: no witness (RP, SBLGNT, WEB) carries a reversed-nun or suspended-letter seg",
                              "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
            for m in LARGE_LETTER.finditer(text):
                flags.append({"decision_id": did, "rule": "large_letter_claim_in_jer",
                              "claim": m.group(0),
                              "note": "1Cor is a Greek book: no witness carries a special-letter seg of any class",
                              "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
            # small-letter claims: valid ONLY when bound (window heuristic) to an
            # inventory site - 1Cor has none (small_inv is empty), so every small-letter claim flags
            for m in SMALL_LETTER.finditer(text):
                lo = max(0, m.start() - 120)
                ctx = text[lo:m.start() + 120]
                cands = list(VERSE_NEAR.finditer(ctx))
                ok = any(small_inv.get(f"1Cor.{rc}.{rv}")
                         for vm in cands
                         for rc, rv in readings(int(vm.group(1)), int(vm.group(2))))
                if not ok:
                    flags.append({"decision_id": did, "rule": "small_letter_claim_in_jer",
                                  "claim": m.group(0),
                                  "note": ("1Cor is a Greek book: no witness carries a special-letter seg of any class - "
                                           "every small-letter claim is a fabrication"),
                                  "claim_context": text[lo:m.start() + 80]})
            # PUNCTA arm (1Cor): U+05C4 stands in neither Greek witness (_test_marks_tools_1cor.py asserts that no Hebrew
            # code point does); both site sets are empty. A claim is judged on the verse numbers in its own clause within
            # 60 characters of the word (PROSE_REACH, kept for prose) and every number in a parenthetical opening directly
            # after that clause, in the same field (R4(ii), ezek_controlling_rulings_a1#e3; a range counts as its
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
                                      "span_sites_mt": ["1Cor.%d.%d" % s for s in span_sites],
                                      "numbers_in_clause": verdict is not None,
                                      "claim_context": text[lo:m.start() + 80]})
                    continue
                if at_site is not True:
                    flags.append({"decision_id": did, "rule": "puncta_claim_in_ezek",
                                  "claim": m.group(0), "ambiguous": at_site == "ambiguous",
                                  "note": ("1Cor carries NO puncta extraordinaria (no Hebrew code point stands in either "
                                           "Greek witness) - every positive puncta claim in a 1Cor row is a fabrication"),
                                  "claim_context": text[lo:m.start() + 80]})
            # Rule 1 (T3): a mark claim binds to the verse numbers in its own clause under its OWN type - RP, WEB, SBL and
            # the empty PE/SAMEKH layer - and the types are never conflated
            claims = mark_claims(text)
            if claims:
                cited += 1
            for want_type, m in claims:
                c_lo_, c_hi_ = clause_bounds(text, m.start(), m.end(), NUM_CLAUSE_END)
                # S1-22 (ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 (b)): the claim binds to the verse numbers written in
                # its OWN clause - C:V, C.V or a dotted ref alike - plus a parenthetical opening directly after it
                named_ = [p for pairs in puncta_claim_numbers(text, m.start(), m.end()) for p in pairs]
                # W6 (#e5 FLAGS-TF2-1): the letter-name absence form is an absence phrase, so rule 1 skips its clause
                absent_ = bool(ABSENCE.search(text[c_lo_:c_hi_]) or letter_absences(text, c_lo_, c_hi_))
                if not named_:
                    # S1-22 kept for RP, WEB and SBL: a claim naming no number is left to rules 2 and 3. T3: the PE/SAMEKH
                    # layer is empty in 1Cor, so a positive Masoretic mark claim naming no verse is false wherever it stands
                    if want_type in ("PE", "SAMEKH") and not absent_ and not puncta_negated(text, m.start(), m.end()):
                        flags.append({"decision_id": did, "rule": "paragraph_mark_claim",
                                      "claimed": want_type, "verse_cited": None,
                                      "note": "1Cor has no PE/SAMEKH layer: a positive Masoretic mark claim is false at every verse",
                                      "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
                    continue
                # W1 (ezek_controlling_rulings_a1#e5 ruling FLAGS-TF2-1), per keying (before_readings): a mark of the
                # claimed TYPE satisfies the claim; the type test is untouched, and an absence claim never takes W1
                if any(want_type in marks.get(f"1Cor.{rc}.{rv}", [])
                       for c0, v0 in named_
                       for rc, rv in before_readings(c0, v0, want_type)):
                    continue
                if absent_:
                    continue
                c, v = named_[0]
                got = {f"1Cor.{rc}.{rv}": marks.get(f"1Cor.{rc}.{rv}", [])
                       for rc, rv in readings(c, v)}
                flags.append({"decision_id": did, "rule": "paragraph_mark_claim",
                              "claimed": want_type, "verse_cited": f"1Cor.{c}.{v}",
                              "inventory_under_both_readings": got,
                              "note": ("mark TYPE mismatch - RP, WEB and SBL (and PE/SAMEKH) are never conflated"
                                       if any(got.values()) else "no mark at the cited verse under either reading"),
                              **near_diag(by_type[want_type], c, v)})
            # Rule 3: absence arm, typed (T3: absence_types) and span-scoped
            # S1-22 (#e4 ruling TOOLFIX-2 (b)): an absence phrase is scoped to the verse, range or chapter its own clause
            # names; an absence phrase naming none keeps the span-scoped check
            for am in sorted(list(ABSENCE.finditer(text)) + letter_absences(text), key=lambda x: x.start()):   # W6 (#e5 FLAGS-TF2-1)
                types_ = absence_types(am.group(0))
                named_ = [p for pairs in puncta_claim_numbers(text, am.start(), am.end()) for p in pairs]
                c_lo_, c_hi_ = clause_bounds(text, am.start(), am.end(), NUM_CLAUSE_END)
                for chm_ in CHAPTER_NAMED.finditer(text, c_lo_, c_hi_):
                    ch_ = int(chm_.group(1))
                    named_ += [(ch_, vv_) for vv_ in range(1, MT_LAST_VERSE.get(ch_, 0) + 1)]
                if named_:
                    # MARKS-3D applies to a NAMED range too (peer_09 measured the false positive): the row's own seam verse
                    # is dropped - its LAST verse for an after-keyed mark (the predecessor's close seam), its FIRST verse
                    # for a start-keyed RP or WEB start (T3: a start there is the onset seam); a verse-keyed SBL sign has
                    # no seam. T3: 'after N' or 'follows N' also reads N+1 for a start-keyed type.
                    _sp = span_pairs(row)
                    _seam = {}
                    if _sp:
                        _seam = {"after": "1Cor.%d.%d" % web_to_mt(*_sp[-1]), "start": "1Cor.%d.%d" % web_to_mt(*_sp[0])}
                    _after = bool(AFTER_WORD.search(text, c_lo_, c_hi_))
                    scope_ = "named_interior"
                    have = {}
                    for c0, v0 in named_:
                        for t_ in sorted(types_):
                            cand_ = list(readings(c0, v0))
                            if _after and KEYING[t_] == "start":
                                cand_ += [p for p in before_readings(c0, v0, t_) if p not in cand_]
                            for rc, rv in cand_:
                                k_ = f"1Cor.{rc}.{rv}"
                                if t_ in marks.get(k_, []) and k_ != _seam.get(KEYING[t_]):
                                    have.setdefault(k_, [])
                                    if t_ not in have[k_]:
                                        have[k_].append(t_)
                else:
                    # MARKS-3D vocabulary: a span-scoped absence claim means the span interior, under the type's keying
                    scope_ = "span_interior"
                    have = {}
                    for t_ in sorted(types_):
                        for k_, ts_ in interior_only(span_pairs(row), by_type[t_], KEYING[t_]).items():
                            have.setdefault(k_, []).extend(ts_)
                if have:
                    flags.append({"decision_id": did, "rule": "false_mark_absence_claim", "scope": scope_,
                                  "absence_types": sorted(types_),
                                  "claim_context": text[max(0, am.start() - 60):am.start() + 80],
                                  "span_relevant_marks_mt_keys": have})
                    break
            # Rule 2 (T3): symmetry over RP pilcrows only, start-keyed directions. WEB paragraphs are tier-4 formatting
            # that never drives a boundary (pmarks web_paragraph_note) and an SBLGNT sign is verse-located with a
            # span-scoped disclosure note, not a seam duty (sbl_variant_note): neither takes this rule (T3 report)
            want_dir = relevant_by_direction(span_pairs(row), by_type["RP"], "start")
            rp_claims = [mm for t, mm in claims if t == "RP"]
            for ref, (types, direction) in want_dir.items():
                _, c, v = ref.split(".")
                near = re.compile(rf"{re.escape(ref)}|\b{c}[:.]{v}\b")
                disclosed = any(n_.start() - 160 <= r_.start() and r_.end() <= n_.end() + 160
                                for n_ in near.finditer(text) for r_ in rp_claims)
                if not disclosed:
                    flags.append({"decision_id": did, "rule": "mark_symmetry_gap",
                                  "undisclosed_mt_key": ref, "mark_types": types,
                                  "direction": direction,
                                  "direction_means": DIRECTION_VOCABULARY_START[direction],
                                  "row_cites_marks": bool(claims)})
            # WARN: paseq position assertions (inventory is count-only)
            # S1-08 (c) (dan_controlling_agent_rulings_E1): the scan runs over one string per line (refs included), and
            # a match that crosses a line joins a positional keyword from ANOTHER string (lineage: a PE claim on one string and a paseq claim on the next)
            # - not a position claim; a presence claim "paseq (at|in) C:V" is instead checked against the pmarks
            # paseq verse list (both MT readings) and FLAGGED when neither reading is on it
            ptext = prose_of(row) + "\n" + "\n".join(row.get("boundary_evidence_refs", []))
            for pp_ in PASEQ_PRESENCE.finditer(ptext):
                if PASEQ_ABSENT_BEFORE.search(ptext[max(0, pp_.start() - 30):pp_.start()]):
                    continue   # "no paseq at 8:27" is an absence statement, not a presence claim
                cv_ = readings(int(pp_.group(1)), int(pp_.group(2)))
                if not any(f"1Cor.{c_}.{v_}" in paseq_verses for c_, v_ in cv_):
                    flags.append({"decision_id": did, "rule": "paseq_false_presence",
                                  "claim": pp_.group(0),
                                  "note": "no paseq on this verse in pmarks paseq (MT direct or WEB-mapped)",
                                  "claim_context": ptext[max(0, pp_.start() - 80):pp_.end() + 80]})
            # T3: pmarks_1Cor.json has no paseq layer, so a paseq presence claim naming no verse is false too; a denial
            # (a negator just before it, or a negation in its clause) passes
            for pw_ in re.finditer(r"\bpaseq\b", ptext, re.I):
                if any(pp_.start() <= pw_.start() < pp_.end() for pp_ in PASEQ_PRESENCE.finditer(ptext)):
                    continue
                if (PASEQ_ABSENT_BEFORE.search(ptext[max(0, pw_.start() - 30):pw_.start()])
                        or puncta_negated(ptext, pw_.start(), pw_.end())):
                    continue
                flags.append({"decision_id": did, "rule": "paseq_false_presence",
                              "claim": pw_.group(0), "verse_cited": None,
                              "note": "1Cor has no paseq layer: a positive paseq claim is false at every verse",
                              "claim_context": ptext[max(0, pw_.start() - 80):pw_.end() + 80]})
            for pm_ in PASEQ_POS.finditer(ptext):
                if "\n" in pm_.group(0):
                    continue
                lo = max(0, pm_.start() - 120)
                ctx = ptext[lo:pm_.end() + 120]
                if PASEQ_POS_NEG.search(ctx):
                    continue
                warns.append({"decision_id": did, "rule": "paseq_position_warn",
                              "claim": pm_.group(0)[:120],
                              "note": "pmarks paseq is COUNT-ONLY (no offsets/"
                                      "word indices) - position is unsourceable",
                              "claim_context": ptext[lo:pm_.end() + 80]})
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
                        keys_ = {f"1Cor.{mt_[0]}.{mt_[1]}" for c0, v0 in span_pairs(row) for mt_ in [web_to_mt(c0, v0)] if mt_} - row_named_mt_keys(text)
                    elif named_:
                        scope_ = "named"
                        keys_ = {f"1Cor.{rc}.{rv}" for c0, v0 in named_ for rc, rv in readings(c0, v0)}
                    else:
                        scope_ = "span"
                        keys_ = {f"1Cor.{mt_[0]}.{mt_[1]}" for c0, v0 in span_pairs(row) for mt_ in [web_to_mt(c0, v0)] if mt_}
                    present_ = sorted(k_ for k_ in keys_ if kq.get(k_))
                    if present_:
                        flags.append({"decision_id": did, "rule": "false_kq_absence_claim", "scope": scope_,
                                      "kq_mt_keys": present_, "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
                    continue
                if not named_:
                    # T3: pmarks_1Cor.json has no K/Q layer, so a positive K/Q claim naming no verse is false wherever
                    # it stands (the predecessor left it to the span: S1-22)
                    if not kq:
                        flags.append({"decision_id": did, "rule": "kq_claim", "verse_cited": None,
                                      "note": "1Cor has no K/Q layer: a positive K/Q claim is false at every verse",
                                      "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
                    continue
                if any(kq.get(f"1Cor.{rc}.{rv}") or (f"1Cor.{rc}.{rv}" in kq_note_keys and NOTE_WORD.search(ctx))
                       for c0, v0 in named_
                       for rc, rv in readings(c0, v0)):
                    continue
                c, v = named_[0]
                flags.append({"decision_id": did, "rule": "kq_claim",
                              "verse_cited": f"1Cor.{c}.{v}", **near_diag(kq, c, v)})
    print(json.dumps({"rows_checked": n, "rows_citing_marks": cited,
                      "flag_count": len(flags), "flags": flags,
                      "warn_count": len(warns), "warns": warns,
                      "status": "GREEN" if not flags else "FLAGS"},
                     ensure_ascii=False, indent=1))
    return 1 if flags else 0


if __name__ == "__main__":
    if "--marks3d-selftest" in sys.argv:
        raise SystemExit(_marks3d_selftest())
    raise SystemExit(main())
