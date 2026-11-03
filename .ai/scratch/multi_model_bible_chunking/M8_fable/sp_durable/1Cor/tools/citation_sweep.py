#!/usr/bin/env python3
"""1Cor citation sweep + dual-cite arithmetic checker (deterministic Tier-0).

Adapted from the predecessor book's citation_sweep.py by _adapt_tools_1cor.py with the extra spec of lane T1
(cor_p0_toolport_t1_a1#e3). Every fact below was MEASURED on the pinned Phase-0 files and is asserted by
_test_tools_1cor.py.

NUMBERING. Three ref spaces: web: (1Cor_web_clean.txt), rp: (Robinson-Pierpont, 1Cor_rp.txt) and sbl: (SBLGNT,
1Cor_sbl.txt). Each holds 437 verses in 16 chapters with equal per-chapter counts (web_greek_verse_check.json), and
web_greek_offset_map.json records identity_throughout: true. So no verse of the book is in an offset zone:
web_pairs_in_offset_zone and greek_pairs_in_offset_zone return False ON THEIR FACE and never call the crosswalk, and
the exhaustive property test checks that statement against cor_lib for all three spaces. Dual cites stay checked
through the range-guarded identity crosswalk: `web:1Cor.a.b = rp:1Cor.c.d` (or sbl:), `rp:1Cor.a.b = web:1Cor.c.d`,
the qualifiers `(RP n:m)` / `(SBL n:m)` on a web: ref and `(WEB n:m)` on an rp:/sbl: ref. A wrong pairing is RED.

ARMS (RED unless marked WARN):
- REFS: the grammar `(web|rp|sbl):1Cor.C.V[-...]`, the X-X span form, chapter and verse range per space, verse 0,
  the range end, the dual arithmetic and the zone-disclosure arm (inert here: no zone).
- CROSS (E-23): papyri, majuscules and their sigla, minuscules, versions, other critical editions and the Septuagint
  (Swete is reference-only, OW-35) are cross-tradition metadata. They may stand in prose, never in
  boundary_evidence_refs. RP and SBLGNT are the book's own witnesses and never match.
- GREEK QUOTE BINDING: every Greek run of three or more letters binds to the nearest rp:/sbl: ref in its own field
  (in a ref entry: to that entry's own ref) and is collated with cor_lib.collate against THAT ref's own witness. A
  web: ref never binds a Greek quote, and a Greek run with no rp:/sbl: ref in its field is RED. Required tier: byte.
  An nfc-tier match is an NFD copy of the witness bytes: the copy-degradation class nfd_degraded (the predecessor's
  rule for pointed quotes; substrate E-01). accent_stripped, skeleton and none are RED (the substrate's overclaim
  rule: a quote may not stand for a stronger tier than it collates at). Against sbl: a quote may carry the SBLGNT
  critical signs (it then collates at byte) or omit them; a sign-free quote that collates at byte against the verse
  with its signs removed is accepted and listed under sbl_sigla_stripped, because the signs are apparatus, not text.
- HEBREW CLAIM ARMS are fabrication classes. No 1Cor witness carries Hebrew (0 Hebrew letters in 1Cor_rp.txt and
  1Cor_sbl.txt), so the inherited site sets and inventories are EMPTY and every positive claim in a ref annotation is
  RED, while every denial (the inherited negation logic, unchanged) passes. A Hebrew run inside a ref entry is RED.
- DEVICE arm (the predecessor's calendar-date arm, re-pointed): the <FAMILY>_PAIRS constants, FRAME_IN_BODY_PAIRS,
  FRAME_edges and DEVICE_NO_ONSET are read at run time from ../1cor_device_inventory.json citation_sweep_constants
  (face WEB, equal to the Greek face). DEVICE_NO_ONSET is empty, so the onset arm never fires. A topic-marker claim
  (the Greek peri de formula, 'peri de', 'topic marker') that names a verse outside TOPIC_MARKER_PAIRS is RED, in a
  ref annotation and in prose; a denial passes. No other family carries a claim arm (see DEVICE_CLAIM_FAMILIES).
- WEB FOOTNOTE QUOTE (WARN; the predecessor's WEB-quote warn, re-pointed): a curly-quoted WEB span near a web: ref
  that falls in a WEB footnote verse (pmarks_1Cor.json web_footnote_verses, 13 verses), in a row that discloses no
  footnote anywhere.
- PROSE dual-pair arithmetic (reported apart from problems, as inherited).
Usage: citation_sweep.py ROWS (.jsonl, a JSON array or {"decisions": [...]}).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cor_lib import (GREEK_LAST_VERSE, LAST_VERSE, SIGLA, collate, expand_ref_token, greek_to_web,
                     load_pmarks, load_witnesses, web_quote_found, web_to_greek)

TOOLS = Path(__file__).resolve().parent
SP = TOOLS.parent

REF_RE = re.compile(
    r"^(web|rp|sbl):1Cor\.(\d+)\.(\d+)(?:-(?:1Cor\.)?(\d+)(?:\.(\d+))?)?(.*)$")
# E-23 / OW-35: cross-tradition witnesses are prose-only metadata. Septuagint (Swete is reference-only), papyri,
# majuscules by name, symbol or Gregory-Aland number, minuscules, versions, other critical editions, and the Hebrew
# and Qumran sources of the book's scripture quotations. RP (Byzantine Textform) and SBLGNT never match.
CROSS = re.compile(
    r"\bLXX\b|\bSeptuagint\b|\bOld Greek\b|\bSwete\b|\bRahlfs\b|\bG(?:ö|oe?)ttingen\b"
    r"|\bpapyr(?:us|i)\b|\U0001d513\s?\d|\bP(?:11|14|15|34|46|61|68|123)\b"
    r"|\b(?:majuscules?|minuscules?|uncials?|codex|codices)\b"
    r"|\b(?:Sinaiticus|Alexandrinus|Vaticanus|Ephraemi|Claromontanus|Augiensis|Boernerianus|Mosquensis|Angelicus"
    r"|Porphyrianus)\b|ℵ|\u05d0|(?<![\w.:-])0(?:1|2|3|4|6|10|12|18|20|25|44|121|243)\b"
    r"|\b(?:Vulgate|Old Latin|Itala|Peshitta|Syriac|Harklean|Coptic|Sahidic|Bohairic|Gothic|Armenian|Ethiopic"
    r"|Georgian)\b"
    r"|\bNA2[5-8]\b|\bUBS[345]?\b|\bTHGNT\b|\bTyndale House\b|\bECM\b|\bWestcott\b|\bHort\b|\bTischendorf\b"
    r"|\bTregelles\b|\bTextus Receptus\b|\bScrivener\b|\bStephanus\b|\bNestle\b"
    r"|\bMasoretic\b|\bTargums?\b|\bDSS\b|\bQumran\b", re.I)
HEB_RUN = re.compile(r"[\u0591-\u05f4]{2,}(?:[ \u05be][\u0591-\u05f4]+)*")
HEB_LETTER = re.compile(r"[\u05d0-\u05ea]")
_GL = "Ͱ-Ͽἀ-῿"                       # Greek and Greek Extended
_GW = _GL + "̀-ͯʼ’"                  # a word: letters, combining marks, the elision marks
_SG = re.escape(SIGLA)                                   # the SBLGNT critical signs
SIGLA_RE = re.compile("[%s]" % _SG)
# a Greek run: words joined by spaces, punctuation and critical signs; a sign may open the run
GREEK_QUOTE = re.compile("[%s]*[%s][%s]*(?:[ ,.·;%s]+[%s][%s]*)*" % (_SG, _GL, _GW, _SG, _GL, _GW))
GREEK_REF = re.compile(r"(?<![\w.])(rp|sbl):1Cor\.(\d+)\.(\d+)(?:-(?:1Cor\.)?(\d+)(?:\.(\d+))?)?")
PROSE_PAIR = re.compile(
    r"web:1Cor\.(\d+)\.(\d+)(?:\s*[-–]\s*(?:1Cor\.)?(?:(\d+)\.)?(\d+))?"
    r"\s*[=(]+\s*(?:=\s*)?"
    r"(?:rp|sbl):1Cor\.(\d+)\.(\d+)(?:\s*[-–]\s*(?:1Cor\.)?(?:(\d+)\.)?(\d+))?")
QUOTE = re.compile(r"“([^”]+)”")
WREF = re.compile(r"web:1Cor\.\d+\.\d+(?:-(?:1Cor\.)?\d+(?:\.\d+)?)?")
KQ_WORD = re.compile(r"\b(?:ketiv|qere|K/Q)\b", re.I)
MARK_WORD = re.compile(r"\b(petuchah|setumah)\b|\b(pe|samekh)\b(?!\w)", re.I)
PUNCTA = re.compile(r"\bpuncta\b|\bextraordinar(?:y|ia)\s+(?:points?|dots?)\b|\bupper\s+dots?\b|U\+05C4", re.I)
PUNCTA_NEG = re.compile(r"\b(?:no|not|nor|never|without|absent|lacks?|lacking|none)\b(?:\s+[\w/-]+){0,2}\s*$", re.I)   # adjacent negation only
NEG_WORD = re.compile(r"\b(?:no|not|nor|never|without|absent|lacks?|lacking|none)\b", re.I)
PUNCTA_NUM = re.compile(r"(?<![A-Za-z\d])(\d{1,2})[:.](\d{1,2})(?!\d)")
SINGLE_WITNESS = re.compile(r"\bsingle[-\s]+witness", re.I)   # T4-04: the disclosure, hyphenated or spaced
SELAH = re.compile(r"\bselah\b", re.I)
REVERSED_NUN = re.compile(r"\b(?:inverted|reversed)[\s-]*nun\b|\bsuspended\b", re.I)
# patch i1 letter-name whitelist. 'majuscule' and 'minuscule' left these two arms: in a Greek book they name
# manuscript classes, which CROSS now refuses in a ref.
_LETTERS = (r"(?:letter|nun|ayin|mem|yod|waw|vav|kaf|pe|tsadi|qof|resh|shin|tav|aleph|alef|bet|gimel|dalet|he|het|tet|"
            r"lamed|samekh|zayin)\b")
LARGE_LETTER = re.compile(r"\b(?:large|x-large)\s+" + _LETTERS, re.I)
SMALL_LETTER = re.compile(r"\b(?:small|x-small)\s+" + _LETTERS + r"|\bze[i']?ira\b", re.I)
PASEQ_WORD = re.compile(r"\bpaseq\b", re.I)
# #e15 Q6(b): a ROLE token carries its own device name ("[DISCLOSURE-paseq]"), so the token must be stripped
# before any device-word match or the token fires its own arm. Measured cause of one false defect.
ROLE_TOKEN = re.compile(r"\[(?:WARRANT|DISCLOSURE|QUOTE|ANCHOR)[A-Za-z:-]*\]")
# #e15 Q6(a): each quoted run is collated against the reference governing ITS OWN clause. Sentence bounds are
# terminal punctuation; a clause is the run of text between them.
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _sentence_bounds(text, pos):
    """The (start, end) of the sentence containing `pos`."""
    start = 0
    for m in SENT_SPLIT.finditer(text):
        if m.end() <= pos:
            start = m.end()
        else:
            break
    end = len(text)
    m = SENT_SPLIT.search(text, pos)
    if m:
        end = m.start()
    return start, end


def field_bounds(text, start, end):
    """The span of the one field a match sits in: check_marks joins every row field with newlines, so a window that
    crossed a newline would read another field - the span string included - as part of the claim."""
    nl = text.find("\n", end)
    return text.rfind("\n", 0, start) + 1, (nl if nl != -1 else len(text))


# Clause and sentence marks. A period ends a clause only before whitespace or the end (so 1Cor.7.25 and 7.25 never
# split); a colon only when no digit follows (so 7:25 never splits); ';', ',', '(' and ')' always - including right
# after a digit, as in '7:25;' (the first version's digit lookbehind let a decoy number leak across that semicolon).
NEG_CLAUSE_END = re.compile(r"\.(?=\s|$)|:(?!\d)|[;,()]")   # a negation's scope ends at any clause mark
NUM_CLAUSE_END = re.compile(r"\.(?=\s|$)|[;()]")            # a claim's numbers stay together across commas
# T4-01: digits that follow a letter directly ('R4.5', a ruling or row id) are an id, never a verse number
RANGE_NUM = re.compile(r"(?<![A-Za-z\d])(\d{1,2})[:.](\d{1,2})(?:\s*[-–]\s*(?:(\d{1,2})[:.])?(\d{1,2}))?(?!\d)")
SENT_END = re.compile(r"\.(?=\s|$)|;|\n")
PUNCTA_SITE_PAIRS = set()   # EMPTY in 1Cor: U+05C4 and U+05C5 each counted 0 in 1Cor_rp.txt and 1Cor_sbl.txt (no Hebrew at all)


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
    mention's end, a denial LATER in the clause also counts, but only one DENIAL_AFTER reads (T4-03: '10:4, where a
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
# 'is lacking' or 'is missing' deny only at the clause end ('the dateline at 10:4 is missing its year word' still names
# a dateline). #e4 amendments: A1 - the clause end may be a newline (check_marks joins fields with newlines); A2 - a
# COORDINATED denial with a verse number and no expectation modal between the mention and the denial does not deny: the
# mention is a positive claim over the numbers before the denial ('stand at 8:5 but none is present in ch 9' claims 8:5).
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
# check_marks' PROSE arm keeps a 60-character reach inside the clause. Read without a limit, the source book's real row P10-008 ("the
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
    every number in a parenthetical that opens directly after that clause ('puncta extraordinaria (8:5)'), all inside
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
    ok = [any(p in PUNCTA_SITE_PAIRS or web_to_greek(*p) in PUNCTA_SITE_PAIRS for p in pairs) for pairs in items]
    return True if all(ok) else (False if not any(ok) else "ambiguous")
PUNCTA_KEYS = set()   # verse keys; EMPTY in 1Cor (no 1Cor witness carries Hebrew)
# DEVICE arm (the predecessor's calendar-date arm, re-pointed). Every constant is READ AT RUN TIME from the pinned
# inventory ../1cor_device_inventory.json, citation_sweep_constants (face WEB, face_equals_greek true; sha256 at the
# port 62c608d775710f56040d3889db9c2cc2a98f40589d15e9b11b8ba2af9b3795ad), and section 7 of _test_tools_1cor.py
# asserts each against that file with its count. Numbering is identity, so one set serves web:, rp: and sbl:.
INVENTORY = TOOLS.parent / "1cor_device_inventory.json"
_CSC = json.loads(INVENTORY.read_text(encoding="utf-8"))["citation_sweep_constants"]


def _pairset(key):
    return frozenset(tuple(p) for p in _CSC[key])


DEVICE_FAMILIES = tuple(sorted(k[:-6] for k in _CSC if k.endswith("_PAIRS")   # every family with a *_PAIRS key
                               and not k.endswith("_SBL_ONLY_PAIRS") and k != "FRAME_IN_BODY_PAIRS"))
PAIRSETS = {k: _pairset(k) for k in _CSC if k.endswith("_PAIRS")}   # every *_PAIRS key, read at run time
DEVICE_PAIRS = {fam: _pairset(fam + "_PAIRS") for fam in DEVICE_FAMILIES}
DEVICE_SBL_ONLY_PAIRS = {fam: _pairset(fam + "_SBL_ONLY_PAIRS") for fam in DEVICE_FAMILIES
                         if fam + "_SBL_ONLY_PAIRS" in _CSC}
TOPIC_MARKER_PAIRS = DEVICE_PAIRS["TOPIC_MARKER"]   # 6 at the port: 7:1, 7:25, 8:1, 12:1, 16:1, 16:12
DEVICE_NO_ONSET = _pairset("DEVICE_NO_ONSET")       # EMPTY: no 1Cor ruling restricts onsets at any device
FRAME_IN_BODY_PAIRS = _pairset("FRAME_IN_BODY_PAIRS")   # 10:32: a frame-family form inside the body, never a frame edge
FRAME_EDGES = {k: tuple(p) for k, p in _CSC["FRAME_edges"].items()}   # opening_before 1:10, closing_from 16:19
# Which families carry a claim arm. Only TOPIC_MARKER: its trigger is a closed formula (Greek peri de, 'peri de',
# 'topic marker') and every member is a boundary-grade onset in the inventory. The others stay constants only:
# 'disclosure', 'appeal', 'tradition', 'praise', 'slogan', 'frame' and 'thanksgiving' are ordinary English words in
# a rationale ('disclosure' is also the campaign's own single-witness vocabulary), so an arm keyed on them would fire
# on prose that makes no device claim; SLOGAN_PAIRS holds only the lexical 'all things are lawful' verses while
# scholarship names other Corinthian slogans, so a slogan arm would turn a defensible reading RED; FRAME is bounded by
# FRAME_edges (opening_before 1:10, closing_from 16:19), not by FRAME_PAIRS (7 member verses), and 10:32 is a
# frame-family form in the body (FRAME_IN_BODY_PAIRS), so a pairs-keyed frame arm would misread both edges.
DEVICE_CLAIM_FAMILIES = ("TOPIC_MARKER",)
TOPIC_MARKER = re.compile(r"(?<!non-)(?<!non )(?:\b[πΠ]ερ[ιὶίί]\s+"
                          r"δ[εὲέέ]|\bperi\s+de\b|\btopic[-\s]markers?\b)", re.I)
LIST_NEXT = re.compile(r"\s*(?:,\s*(?:and\s+)?|\s+and\s+)(?=\d{1,2}[:.]\d)")
APPOSITION_NUM = re.compile(r"(?<![A-Za-z\d])(\d{1,2})[:.](\d{1,2})(?:\s*[-–]\s*(?:(\d{1,2})[:.])?(\d{1,2}))?\s*$")

def dateline_claim_numbers(text, start, end, reach=60, upper=None):
    """The verse numbers a dateline claim names:
      - those in its own COMMA-delimited clause within `reach` characters ('unlike the dateline at 10:1, the date at
        10:4 ...' names 10:1 only);
      - a parenthetical opening directly after that clause ('the dateline (10:4)');
      - a list written straight on from the last of them ('datelines at 9:1, 9:2 and 10:4' names all three);
      - only when none of those names a number, the number that ENDS the immediately preceding comma clause (the
        apposition '10:4, a dateline-grade onset').
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


def pair_ok_web_to_greek(wc: int, wv: int, gc: int, gv: int) -> bool:
    """A WEB/Greek pairing is right iff the crosswalk maps it (identity in 1Cor: 437 WEB verses onto 437 Greek verses)."""
    return web_to_greek(wc, wv) == (gc, gv)


def web_pairs_in_offset_zone(pairs) -> bool:
    return False   # no web: verse of 1Cor is in an offset zone (web_greek_offset_map.json identity_throughout), on its face


def greek_pairs_in_offset_zone(pairs) -> bool:
    return False   # no rp: or sbl: verse of 1Cor is in an offset zone, on its face


VERSES = frozenset((c, v) for c in LAST_VERSE for v in range(1, LAST_VERSE[c] + 1))


def positive_claim(text, rx):
    """The first mention of rx that the inherited negation logic does not deny, or None. These arms have no site in
    1Cor, so a denied mention is a TRUE absence claim and passes, and any other mention is RED."""
    for m in rx.finditer(text):
        if not puncta_negated(text, m.start(), m.end()):
            return m
    return None


def greek_runs(text):
    """(run, start, end) for every Greek run of three or more letters."""
    return [(m.group(0), m.start(), m.end()) for m in GREEK_QUOTE.finditer(text)
            if sum(ch.isalpha() for ch in m.group(0)) >= 3]


def ref_pairs(token):
    """Every (chapter, verse) a written ref token names inside the book, or [] when it names none."""
    try:
        return [p for p in expand_ref_token(token) if p in VERSES]
    except Exception:
        return []


def bind(run, kind, text):
    """(verdict, tier) of a Greek run against the joined text of its bound ref, in that ref's own witness:
    'ok' at byte; 'sigla_stripped' for a sign-free run that is byte-true against the sbl: verse with its critical signs
    removed; 'nfd' at nfc tier (copy degradation); 'red' at accent_stripped, skeleton or none."""
    tier = collate(run, text) if text else "none"
    if tier == "byte":
        return "ok", tier
    if kind == "sbl" and text and not SIGLA_RE.search(run):
        if collate(run, re.sub(" {2,}", " ", SIGLA_RE.sub("", text))) == "byte":
            return "sigla_stripped", "byte"
    if tier == "nfc":
        return "nfd", tier
    return "red", tier


def main() -> int:
    rows_path = Path(sys.argv[1]) if len(sys.argv) > 1 else SP / "freeze" / "frozen_rows_final.jsonl"
    pm = load_pmarks()
    # The predecessor's Hebrew inventories (marks, paseq, kq, other_segs, notes_other) have no 1Cor counterpart:
    # pmarks_1Cor.json carries none of those keys. They are EMPTY, so each Hebrew claim arm below is a fabrication class.
    marks, paseq, kq, small_letter_keys = {}, {}, {}, {}
    fn_verses = {tuple(int(x) for x in k.split(".")[1:]) for k in pm.get("web_footnote_verses", {})}
    wit = load_witnesses()
    problems: list[str] = []
    prose_pair_problems: list[str] = []
    nfd_degraded: list[str] = []
    sbl_sigla_stripped: list[str] = []
    web_footnote_quote_warns: list[str] = []
    rows = rows_from(rows_path)

    def judge(did, run, kind, pairs, where, label, own):
        verdict, tier = bind(run, kind, " | ".join(wit[kind].get(p, "") for p in pairs))
        if verdict == "ok":
            return
        if verdict == "sigla_stripped":
            sbl_sigla_stripped.append(f"{did}: Greek quote {run[:25]!r}… in {where} is byte-true against {label} "
                                      f"with the SBLGNT critical signs removed")
        elif verdict == "nfd":
            nfd_degraded.append(f"{did}: Greek quote {run[:25]!r}… in {where} collates against {label} at nfc tier "
                                f"only (an NFD copy: copy degradation - re-copy the witness bytes)")
        elif own:
            problems.append(f"{did}: Greek {run[:25]!r}… in ref entry {where} does not collate against its own ref "
                            f"at byte tier ({label}, tier {tier}; the required tier is byte)")
        else:
            problems.append(f"{did}: Greek quote {run[:25]!r}… in {where} does not collate against any nearby cited "
                            f"ref at byte tier (bound to {label}, tier {tier}; the required tier is byte)")

    for row in rows:
        did = row.get("decision_id", "?")
        # DEVICE arm, onset (the predecessor's calendar onset arm): no row may open at a DEVICE_NO_ONSET verse. The set
        # is EMPTY in 1Cor (the inventory's DEVICE_NO_ONSET_statement), so this arm never fires here.
        dev_on = re.match(r"^(?:(?:web|rp|sbl):)?1Cor\.(\d+)\.(\d+)-", str(row.get("span") or "").strip())
        dev_pair = web_to_greek(int(dev_on.group(1)), int(dev_on.group(2))) if dev_on else None
        if dev_pair in DEVICE_NO_ONSET:
            problems.append(f"{did}: row opens at {dev_pair[0]}:{dev_pair[1]} - DEVICE_NO_ONSET names the device "
                            f"verses at which no 1Cor unit opens")
        # X-X span-form arm: row spans use the full 1Cor.a.b-1Cor.c.d form
        span = row.get("span")
        if isinstance(span, str) and span.strip():
            s = span.strip().replace("web:", "")
            if not re.match(r"^1Cor\.\d+\.\d+-1Cor\.\d+\.\d+$", s):
                problems.append(f"{did}: span not in full X-X form "
                                f"(1Cor.a.b-1Cor.c.d, single verses included): {span!r}")
        for ref in row.get("boundary_evidence_refs", []):
            if CROSS.search(ref):
                problems.append(f"{did}: cross-tradition material in "
                                f"boundary_evidence_refs: {ref!r}")
                continue
            m = REF_RE.match(ref)
            if not m:
                problems.append(f"{did}: non-1Cor or malformed ref {ref!r}")
                continue
            kind = m.group(1)
            ch, v = int(m.group(2)), int(m.group(3))
            e1, e2, tail = m.group(4), m.group(5), m.group(6)
            space = LAST_VERSE if kind == "web" else GREEK_LAST_VERSE
            last = space.get(ch)
            if last is None:
                problems.append(f"{did}: {ref!r} chapter out of range")
                continue
            if v == 0:
                problems.append(f"{did}: {ref!r} - 1Cor.{ch}.0 is always invalid "
                                f"(no title pseudo-verses exist in 1Cor)")
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

            # dual/qualifier arithmetic via the crosswalk (identity book, range-guarded)
            has_disclosure = False
            pair = re.search(r"=\s*(rp|sbl):1Cor\.(\d+)\.(\d+)", tail)
            if kind == "web" and pair:
                has_disclosure = True
                got = (int(pair.group(2)), int(pair.group(3)))
                want = web_to_greek(ch, v)
                if got != want:
                    problems.append(f"{did}: dual-cite arithmetic wrong (crosswalk - expected "
                                    f"{pair.group(1)}:1Cor.{want[0]}.{want[1]}): {ref!r}")
            wpair = re.search(r"=\s*web:1Cor\.(\d+)\.(\d+)", tail)
            if kind != "web" and wpair:
                has_disclosure = True
                got = (int(wpair.group(1)), int(wpair.group(2)))
                want = greek_to_web(ch, v)
                if got != want:
                    problems.append(f"{did}: dual-cite arithmetic wrong (crosswalk - "
                                    f"expected web:1Cor.{want[0]}.{want[1]}): {ref!r}")
            off = re.search(r"\((RP|SBL)\s+(\d+)[:.](\d+)\)", tail)
            if off:
                if kind != "web":
                    problems.append(f"{did}: Greek qualifier on a non-web ref: {ref!r}")
                else:
                    has_disclosure = True
                    want = web_to_greek(ch, v)
                    if (int(off.group(2)), int(off.group(3))) != want:
                        problems.append(f"{did}: Greek qualifier wrong (crosswalk - "
                                        f"expected {off.group(1)} {want[0]}:{want[1]}): {ref!r}")
            woff = re.search(r"\(WEB\s+(\d+)[:.](\d+)\)", tail)
            if woff:
                if kind == "web":
                    problems.append(f"{did}: WEB qualifier on a web ref: {ref!r}")
                else:
                    has_disclosure = True
                    want = greek_to_web(ch, v)
                    if (int(woff.group(1)), int(woff.group(2))) != want:
                        problems.append(f"{did}: WEB qualifier wrong (crosswalk - "
                                        f"expected WEB {want[0]}:{want[1]}): {ref!r}")

            # OFFSET-ZONE DISCLOSURE arm (inherited, inert: both predicates are False on their face in 1Cor)
            zone_pairs = [(ch, v), end_pair]
            in_zone = (web_pairs_in_offset_zone(zone_pairs) if kind == "web"
                       else greek_pairs_in_offset_zone(zone_pairs))
            if in_zone and not has_disclosure:
                problems.append(f"{did}: offset-zone ref lacks dual-cite/qualifier disclosure: {ref!r}")

            key = f"1Cor.{ch}.{v}"   # one numbering: the web: key is the Greek key
            covered, (c_, v_) = [], (ch, v)
            while (c_, v_) <= end_pair and c_ in space:
                covered.append((c_, v_))
                c_, v_ = (c_, v_ + 1) if v_ < space[c_] else (c_ + 1, 1)

            # HEBREW CLAIM ARMS (inherited, fabrication classes). The role token is stripped first (#e15 Q6(b)). Each
            # arm keeps its trigger words; the inherited negation logic decides, so a denial passes and any other
            # mention is RED, because each inventory is EMPTY in 1Cor.
            tail_nt = ROLE_TOKEN.sub(" ", tail)
            mm = positive_claim(tail_nt, MARK_WORD)
            if mm:
                word = (mm.group(1) or mm.group(2)).lower()
                want_type = "PE" if word in ("petuchah", "pe") else "SAMEKH"
                if want_type not in marks.get(key, []):
                    problems.append(f"{did}: {ref!r} claims {word} but no 1Cor witness carries a Masoretic paragraph "
                                    f"mark (nothing at {key}; fabrication)")
            if positive_claim(tail_nt, SELAH):
                problems.append(f"{did}: {ref!r} claims selah - NO selah exists "
                                f"in 1Cor (Psalter device; fabrication)")
            if positive_claim(tail_nt, REVERSED_NUN):
                problems.append(f"{did}: {ref!r} claims a reversed-nun/suspended "
                                f"seg - no 1Cor witness carries either")
            if positive_claim(tail_nt, LARGE_LETTER):
                problems.append(f"{did}: {ref!r} claims a large letter - 1Cor "
                                f"carries NO special-letter segs of any class")
            if positive_claim(tail_nt, SMALL_LETTER) and not small_letter_keys.get(key):
                problems.append(f"{did}: {ref!r} claims a small letter but 1Cor "
                                f"carries NO special-letter segs of any class (nothing at {key})")
            if positive_claim(tail_nt, PASEQ_WORD) and not paseq.get(key):
                problems.append(f"{did}: {ref!r} claims paseq but no 1Cor witness carries one (nothing at {key})")
            if positive_claim(tail_nt, KQ_WORD) and not kq.get(key):
                problems.append(f"{did}: {ref!r} claims ketiv/qere but no 1Cor witness carries one (nothing at {key})")
            # PUNCTA arm (inherited, logic unchanged): U+05C4 stands in no 1Cor verse, so PUNCTA_KEYS and
            # PUNCTA_SITE_PAIRS are EMPTY and every positive claim is RED. A claim is judged on every verse number in its
            # own clause of the annotation, at any distance, and in a parenthetical opening directly after that clause
            # (R4(ii); a range counts as its verses): all sites -> true, none -> false, a mix -> ambiguous, RED
            # (T2-01/02). Only a claim naming no number falls back to whether the ref's range covers a site (T1-01). A
            # negation earlier in the same comma-delimited clause makes it an absence claim; adjacent negators cancel
            # (T1-03, T2-03); so does a closed-set denial later in the clause (T4-03). A true claim needs single-witness
            # disclosure in the annotation (T4-04).
            pm_ = PUNCTA.search(tail)
            if pm_:
                sites = {f"1Cor.{c_}.{v_}" for c_, v_ in covered} & PUNCTA_KEYS
                verdict = puncta_verdict(puncta_claim_numbers(tail, pm_.start(), pm_.end(), upper=claim_upper(tail, pm_.end())))
                at_site = bool(sites) if verdict is None else verdict
                if puncta_negated(tail, pm_.start(), pm_.end()):
                    if at_site is True or at_site == "ambiguous":
                        problems.append(f"{did}: {ref!r} denies puncta extraordinaria at a verse that carries them")
                elif at_site == "ambiguous":
                    problems.append(f"{did}: {ref!r} puncta claim is ambiguous: its clause names both a site and "
                                    f"another verse")
                elif not at_site:
                    problems.append(f"{did}: {ref!r} claims puncta extraordinaria but U+05C4 stands in no 1Cor verse "
                                    f"({'no verse number is named and the ref covers no site' if verdict is None else 'the claim names a verse that carries none'})")
                elif not SINGLE_WITNESS.search(tail):
                    problems.append(f"{did}: puncta ref lacks single-witness disclosure: {ref!r}")
            # DEVICE arm, refs: a topic-marker claim in the annotation is RED when it names a verse outside
            # TOPIC_MARKER_PAIRS (dateline_claim_numbers: its clause, a parenthetical, a list, an apposition), or, naming
            # no number, when the ref covers no TOPIC_MARKER_PAIRS verse. A denial ('not a topic marker',
            # 'non-topic-marker') passes.
            for dm_ in TOPIC_MARKER.finditer(tail):
                if puncta_negated(tail, dm_.start(), dm_.end()):
                    continue
                named_ = {p for pairs in dateline_claim_numbers(tail, dm_.start(), dm_.end(), upper=claim_upper(tail, dm_.end())) for p in pairs}
                if not named_:
                    named_ = set() if set(covered) & TOPIC_MARKER_PAIRS else set(covered)
                off_ = sorted(named_ - TOPIC_MARKER_PAIRS)
                if off_:
                    problems.append(f"{did}: {ref!r} claims a topic marker at " + ", ".join("%d:%d" % p for p in off_[:5])
                                    + " - not a TOPIC_MARKER_PAIRS verse (1cor_device_inventory.json)")
                    break
            # REF QUOTE arm (the predecessor's REF HEBREW arm, S1-06, re-pointed): every Greek run inside a ref entry binds
            # to that entry's OWN ref - every verse of its range - in that ref's own witness. A web: ref never binds Greek.
            if [r_ for r_ in HEB_RUN.findall(tail) if len(HEB_LETTER.findall(r_)) >= 3]:
                problems.append(f"{did}: Hebrew run in ref entry {ref!r} - no 1Cor witness carries Hebrew")
            for r_, _p0, _p1 in greek_runs(tail):
                if kind == "web":
                    problems.append(f"{did}: Greek {r_[:25]!r}… in ref entry {ref!r} - a web: ref never binds a Greek "
                                    f"quote; cite rp: or sbl:")
                    continue
                judge(did, r_, kind, covered, repr(ref), f"{kind}:{key}" + ("" if end_pair == (ch, v) else "-%d.%d" % end_pair), True)

        # ---- prose EXPLICIT-PAIR arithmetic arm: a written "web:1Cor.a.b = rp:1Cor.c.d" (or sbl:) asserts arithmetic
        # wherever it appears; validated per endpoint for ranges.
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
                    ok = pair_ok_web_to_greek(wc, wv1, oc, ov1)
                    if wv2 is not None or ov2 is not None:
                        we = (wc2, wv2) if wv2 is not None else (wc, wv1)
                        oe = (oc2, ov2) if ov2 is not None else (oc, ov1)
                        ok = ok and pair_ok_web_to_greek(we[0], we[1], oe[0], oe[1])
                    if not ok:
                        prose_pair_problems.append(
                            f"{did}: prose dual-cite arithmetic wrong in {path} "
                            f"(identity crosswalk: every WEB verse is the same Greek verse): {m.group(0)!r}")
        prose_pair_check(row)

        # ---- DEVICE arm, prose: a topic-marker claim that names a verse outside TOPIC_MARKER_PAIRS in its own
        # comma-delimited clause, or in a list running straight on from it, is RED. A claim naming no number is not
        # judged here (the ref arm judges refs by their coverage).
        def prose_topic_check(o, path="row"):
            if isinstance(o, dict):
                for k2, v2 in o.items():
                    if k2 != "boundary_evidence_refs":
                        prose_topic_check(v2, f"{path}.{k2}")
            elif isinstance(o, list):
                for i, v2 in enumerate(o):
                    prose_topic_check(v2, f"{path}[{i}]")
            elif isinstance(o, str):
                for m in TOPIC_MARKER.finditer(o):
                    if puncta_negated(o, m.start(), m.end()):
                        continue
                    bad = sorted({p for pairs in dateline_claim_numbers(o, m.start(), m.end(), upper=claim_upper(o, m.end())) for p in pairs}
                                 - TOPIC_MARKER_PAIRS)
                    if bad:
                        problems.append(f"{did}: {path} claims a topic marker at " + ", ".join("%d:%d" % p for p in bad[:5])
                                        + " - not a TOPIC_MARKER_PAIRS verse (1cor_device_inventory.json)")
        prose_topic_check(row)

        # ---- GREEK-QUOTE binding arm over every prose field (the predecessor's Hebrew-quote binding, re-pointed) ----
        def walk(o, path="row"):
            if isinstance(o, dict):
                for k2, v2 in o.items():
                    if k2 != "boundary_evidence_refs":
                        walk(v2, f"{path}.{k2}")
            elif isinstance(o, list):
                for i, v2 in enumerate(o):
                    walk(v2, f"{path}[{i}]")
            elif isinstance(o, str):
                runs = greek_runs(o)
                if not runs:
                    return
                refs = list(GREEK_REF.finditer(o))
                # #e15 Q6(a): EVERY occurrence is judged at ITS OWN position, against the ref that governs its own
                # sentence; 1Cor binds to that ONE nearest ref (the predecessor tried the three nearest).
                for run, pos, end in runs:
                    if not refs:
                        problems.append(f"{did}: Greek quote {run[:25]!r}… in {path} has NO rp:/sbl: ref in its field "
                                        f"(a web: ref never binds a Greek quote)")
                        continue
                    _s, _e = _sentence_bounds(o, pos)
                    in_sentence = [mm for mm in refs if _s <= mm.start() < _e]
                    scope = in_sentence or refs

                    def keyf(mm):
                        follows = 0 <= mm.start() - end <= 40
                        precedes_in_sentence = bool(in_sentence) and mm.start() < pos
                        dist = min(abs(mm.start() - pos), abs(mm.start() - end))
                        return (not (follows or precedes_in_sentence), dist)
                    near = sorted(scope, key=keyf)[0]
                    judge(did, run, near.group(1), ref_pairs(near.group(0)), path, near.group(0), False)
        walk(row)

        # ---- WEB FOOTNOTE quote arm (WARN; the predecessor's note-layer WEB-quote warn, re-pointed): a curly-quoted WEB span
        # that stands in a WEB footnote verse, in a row that names no footnote anywhere.
        if not re.search(r"\bfootnotes?\b|\[fn\]", json.dumps(row, ensure_ascii=False), re.I):
            covered_fn: dict[tuple, str] = {}

            def fn_web_walk(o, path="row"):
                if isinstance(o, dict):
                    for k2, v2 in o.items():
                        if k2 != "boundary_evidence_refs":
                            fn_web_walk(v2, f"{path}.{k2}")
                elif isinstance(o, list):
                    for i, v2 in enumerate(o):
                        fn_web_walk(v2, f"{path}[{i}]")
                elif isinstance(o, str):
                    refs = [(m.start(), m.group(0)) for m in WREF.finditer(o)]
                    if not refs:
                        return
                    for qm in QUOTE.finditer(o):
                        qspan = qm.group(1).strip()
                        if len(qspan.split()) < 2 or greek_runs(qspan):
                            continue
                        near = [r for pos, r in refs if abs(pos - qm.start()) <= 200 or abs(pos - qm.end()) <= 200]
                        for r in near:
                            for p in ref_pairs(r):
                                t = wit["web"].get(p, "")
                                if p in fn_verses and t and web_quote_found(qspan, [t]):
                                    covered_fn.setdefault(p, f"{path} {qspan[:60]!r} via {r}")
            fn_web_walk(row)
            for p, where in covered_fn.items():
                web_footnote_quote_warns.append(f"{did}: WEB quote covers WEB footnote verse web:1Cor.{p[0]}.{p[1]} "
                                                f"with no footnote disclosure anywhere in the row ({where})")

    print(json.dumps({"rows": len(rows), "rows_file": rows_path.name, "problems": problems,
                      "prose_pair_problem_count": len(prose_pair_problems),
                      "prose_pair_problems": prose_pair_problems[:20],
                      "nfd_degraded_count": len(nfd_degraded),
                      "nfd_degraded": nfd_degraded[:20],
                      "sbl_sigla_stripped_count": len(sbl_sigla_stripped),
                      "sbl_sigla_stripped": sbl_sigla_stripped[:20],
                      "web_footnote_quote_warn_count": len(web_footnote_quote_warns),
                      "web_footnote_quote_warns": web_footnote_quote_warns[:20],
                      "status": "GREEN" if not problems else "RED"}, ensure_ascii=False, indent=1))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
