#!/usr/bin/env python3
"""Phase-0 helper (orchestrator only): stage citation_sweep.py and check_marks.py for Ezek from the Jer tools.

Both Jer tools carry one-zone crosswalk logic that Ezekiel also needs, so they are the source. What differs is replaced
by exact-count substitution, and a mismatch aborts before anything is written:
  - the docstring, rewritten for Ezekiel's inventory (counts asserted by ezek_lib.py's selftest);
  - the zone predicates and zone messages (WEB 20:45-21:32 / MT ch 21 in place of WEB ch 9 / MT 8:23 + ch 9);
  - the special-letter messages (Ezek has no special-letter seg of any class; Jer had one small nun);
  - the cross-tradition sigla (Ezekiel's Qumran and Masada sigla in place of Jeremiah's);
  - a PUNCTA arm in each tool, new for Ezek: U+05C4 stands in the verse bytes at MT 41:20 and 46:22 only;
  - a CALENDAR-DATE arm in citation_sweep, new for Ezek (strategy section 10, ruling G12(d)): no row opens at MT
    45:20, 45:21 or 45:25, and no dateline claim names any of the four month+day dates without a year word.
Rule ids are kept unchanged (the Lam tools kept them too) so downstream consumers keep working.

The remaining "Jer" identifier tokens are swept to "Ezek" in the CODE only, before the new docstring is inserted:
sweeping the docstring would turn its lineage ("adapted from the Jer tool") into false provenance, the hazard recorded
for the first twelve adapted tools. Each output is compiled, then scanned for stale Jer facts and for any Jer token
left in code. Never overwrites a differing existing file. Never touches ezek_lib.py, TOOLKIT.md or _toolkit_selfcheck.py.
"""
import hashlib
import py_compile
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
DST = Path(__file__).resolve().parent
JER = DST.parent.parent / "Jer" / "tools"
PROTECTED = {"ezek_lib.py", "TOOLKIT.md", "_toolkit_selfcheck.py"}


def abort(msg):
    raise SystemExit("ABORT " + msg)


def sub_exact(text, old, new, expected, label):
    n = text.count(old)
    if n != expected:
        abort("%s: expected %d occurrence(s), found %d" % (label, expected, n))
    return text.replace(old, new)


def sub_ws(text, old, new, expected, label):
    """Like sub_exact, but any run of whitespace in old matches any run of whitespace in the source."""
    pat = r"\s+".join(re.escape(p) for p in old.split())
    out, n = re.subn(pat, lambda m: new, text)
    if n != expected:
        abort("%s: expected %d occurrence(s), found %d" % (label, expected, n))
    return out


def split_doc(text, starts_with):
    head, rest = text.split('"""', 1)
    doc, tail = rest.split('"""', 1)
    if not doc.startswith(starts_with):
        abort("docstring: source does not start with %r" % starts_with)
    return head, tail


def join_doc(head, tail, new_doc):
    head = re.sub(r"\bJer\b", "Ezek", head)
    tail = re.sub(r"\bJer\b", "Ezek", tail)
    return head + '"""' + new_doc + '"""' + tail


PUNCTA_RE = r'''PUNCTA = re.compile(r"\bpuncta\b|\bextraordinar(?:y|ia)\s+(?:points?|dots?)\b|\bupper\s+dots?\b|U\+05C4", re.I)
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
'''

KQ_NOTE_KEYS_LINE = """    # Ezek: verses whose OSHB editorial note speaks of ketib/qere - backed by bytes, but not in the kq inventory
    kq_note_keys = {k for k, notes in pm.get("notes_other", {}).items()
                    if any(KQ_NOTE.search(n.get("text", "")) for n in notes)}
"""

CS_DOC = """Ezek citation sweep + dual-cite arithmetic checker (deterministic Tier-0).

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

CM_DOC = """Paragraph-mark/segment-disclosure symmetry checker (casing-normalized) for Ezek rows.

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

CS_PUNCTA_ARM = """            # PUNCTA arm (Ezek): U+05C4 stands in the verse bytes at MT 41:20 and 46:22 only. A claim is judged on
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
"""

CS_QERE_TIER = """                        # QERE tier (Ezek; mirrors SP/Ezek/_validate_writer_part.py): a Qere lives in the
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
"""

CS_QERE_REPORT = """                    if qere_undisclosed is not None:
                        problems.append(
                            f"{did}: Hebrew quote {run[:25]!r}… in {path} matches the Qere at "
                            f"oshb:{qere_undisclosed} but its field carries no ketiv/qere disclosure")
                        continue
"""

CM_PUNCTA_ARM = """            # PUNCTA arm (Ezek): U+05C4 stands in the verse bytes at MT 41:20 and 46:22 only. A claim is judged on
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
"""

CAL_CONSTANTS = r'''# CALENDAR-DATE arm (Ezek; strategy section 10 as clarified by ruling G12(d)). MT pairs, asserted against
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
'''

CS_REF_HEBREW_ARM = r"""            # REF HEBREW arm (Ezek; S1-06, ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 (b)) [CWO-EZ-16]: every Hebrew
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
"""

CS_CAL_ONSET = r"""        # CALENDAR-DATE arm, onset (Ezek; strategy section 10, ruling G12(d)): MT 45:20, 45:21 and 45:25 carry a
        # month+day date with no year word and no formula, so no row opens there. A row MAY open at 45:18 on the
        # messenger formula that shares the verse with the date; the date itself is never onset evidence.
        cal_on = re.match(r"^(?:web:)?Ezek\.(\d+)\.(\d+)-", str(row.get("span") or "").strip())
        cal_mt = web_to_mt(int(cal_on.group(1)), int(cal_on.group(2))) if cal_on else None
        if cal_mt in CAL_NO_ONSET:
            problems.append(f"{did}: row opens at a calendar date with no formula (MT {cal_mt[0]}:{cal_mt[1]}) - MT 45:20, "
                            f"45:21 and 45:25 open no unit; a row may open at 45:18 only on its messenger formula")
"""

CS_CAL_REF_ARM = r"""            # CALENDAR-DATE arm, refs (Ezek; strategy section 10, ruling G12(d)): a dateline claim in the annotation is
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
"""

CS_CAL_PROSE_ARM = r"""
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
"""


def stage_citation_sweep():
    src = (JER / "citation_sweep.py").read_text(encoding="utf-8")
    head, t = split_doc(src, "Jer citation sweep + dual-cite arithmetic checker")
    t = sub_exact(t, "from jer_lib import (", "from ezek_lib import (kq_split_bytes, ", 1, "cs import")
    # A3 (#e4 ruling T4-04): the mark, small-letter and paseq ref checks accept the SINGLE_WITNESS form the puncta check
    # accepts (hyphenated or spaced); the elif is replaced first because the plain form is a substring of it
    t = sub_exact(t, 'elif "single-witness" not in tail:', "elif not SINGLE_WITNESS.search(tail):", 1, "cs A3 small-letter")
    t = sub_exact(t, 'if "single-witness" not in tail:', "if not SINGLE_WITNESS.search(tail):", 2, "cs A3 mark and paseq")
    # T2-05: only a CLOSED '(MT n:m)' / '(WEB n:m)' is a numbering qualifier; '(MT 46.22 puncta ...' is prose
    t = sub_exact(t, r'off = re.search(r"\(MT\s+(\d+)[:.](\d+)", tail)',
                  r'off = re.search(r"\(MT\s+(\d+)[:.](\d+)\)", tail)', 1, "cs mt qualifier closed")
    t = sub_exact(t, r'woff = re.search(r"\(WEB\s+(\d+)[:.](\d+)", tail)',
                  r'woff = re.search(r"\(WEB\s+(\d+)[:.](\d+)\)", tail)', 1, "cs web qualifier closed")
    t = sub_exact(t, "                    nfd_hit = None\n                    vkey = None\n",
                  "                    nfd_hit = None\n                    qere_undisclosed = None\n                    vkey = None\n",
                  1, "cs qere init")
    t = sub_exact(t, '                        if pointed and tier == "nfd" and nfd_hit is None:\n',
                  CS_QERE_TIER + '                        if pointed and tier == "nfd" and nfd_hit is None:\n', 1, "cs qere tier")
    t = sub_exact(t, "                    if not ok and nfd_hit is not None:\n",
                  CS_QERE_REPORT + "                    if not ok and nfd_hit is not None:\n", 1, "cs qere report")
    t = sub_exact(t, r'r"|\bPeshitta\b|\bTargum\b|\bDSS\b|\bQumran\b|\b4QJer|\b2QJer"',
                  r'r"|\bPeshitta\b|\bTargum\b|\bDSS\b|\bQumran\b|\bMasada\b|\bMasEzek|\b\d{1,2}QEzek"', 1, "cs sigla")
    anchor = r'''MARK_WORD = re.compile(r"\b(petuchah|setumah)\b|\b(pe|samekh)\b(?!\w)", re.I)
'''
    t = sub_exact(t, anchor, anchor + PUNCTA_RE + 'PUNCTA_KEYS = {"Ezek.41.20", "Ezek.46.22"}   # MT keys; asserted by ezek_lib\'s selftest\n'
                  + CAL_CONSTANTS, 1, "cs puncta + calendar constants")
    did_line = '    for row in rows:\n        did = row.get("decision_id", "?")\n'
    t = sub_exact(t, did_line, did_line + CS_CAL_ONSET, 1, "cs calendar onset arm")
    t = sub_exact(t, "        prose_pair_check(row)\n", "        prose_pair_check(row)\n" + CS_CAL_PROSE_ARM, 1, "cs calendar prose arm")
    t = sub_exact(t, "    return any(c == 9 for c, v in pairs)\n",
                  "    return any((c == 20 and v >= 45) or c == 21 for c, v in pairs)   # WEB 20:45-49 and WEB 21:1-32\n",
                  1, "cs web zone")
    t = sub_exact(t, "    return any((c == 8 and v == 23) or c == 9 for c, v in pairs)\n",
                  "    return any(c == 21 for c, v in pairs)   # MT 21:1-37\n", 1, "cs mt zone")
    t = sub_exact(t, 'f"disclosure (WEB ch 9 and MT 8:23 / MT ch 9 are DIFFERENT "',
                  'f"disclosure (WEB 20:45-21:32 and MT ch 21 are DIFFERENT "', 1, "cs zone message")
    t = sub_exact(t, '"(crosswalk book - WEB 9:1 = MT 8:23, WEB 9:2-26 = "',
                  '"(crosswalk book - WEB 20:45-49 = MT 21:1-5, WEB 21:1-32 = "', 1, "cs pair message a")
    t = sub_exact(t, 'f"MT 9:1-25): {m.group(0)!r}")', 'f"MT 21:6-37): {m.group(0)!r}")', 1, "cs pair message b")
    t = sub_ws(t, 'f"carries NO large-letter segs (its only special " f"letter is the small nun at MT 39:13)")',
               'f"carries NO special-letter segs of any class")', 1, "cs large-letter message")
    t = sub_ws(t, 'f"Jer\'s only special-letter seg is the small " f"nun at Jer.39.13 (nothing at {key})")',
               'f"Ezek carries NO special-letter segs of any class "\n                                    f"(nothing at {key})")',
               1, "cs small-letter message")
    kq_line = r'''            if re.search(r"\b(?:ketiv|qere|K/Q)\b", tail, re.I) and not kq.get(key):
'''
    kq_line_ezek = r'''            if (re.search(r"\b(?:ketiv|qere|K/Q)\b", tail, re.I) and not kq.get(key)
                    and not (key in kq_note_keys and NOTE_WORD.search(tail))):
'''
    t = sub_exact(t, kq_line, CS_PUNCTA_ARM + CS_CAL_REF_ARM + CS_REF_HEBREW_ARM + kq_line_ezek, 1, "cs puncta arm + calendar ref arm + kq editorial-note tier")
    small = '    small_letter_keys = {k: v for k, v in pm.get("other_segs", {}).items()}\n'
    t = sub_exact(t, small, small + KQ_NOTE_KEYS_LINE, 1, "cs kq_note_keys")
    return "citation_sweep.py", join_doc(head, t, CS_DOC), t


CHAPTER_NAMED_RE = r"""CHAPTER_NAMED = re.compile(r"\bch(?:apter|\.)?\s+(\d{1,2})\b", re.I)   # S1-22: 'chapter 10', 'ch 46'
"""

CM_W_RE = r'''# W1, W2, W5 and W6 (ezek_controlling_rulings_a1#e5 ruling FLAGS-TF2-1), check_marks only; the PUNCTA arm is untouched.
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
            keys |= {f"Jer.{rc}.{rv}" for rc, rv in readings(c0, v0)}
    return keys
'''


CM_RULE1_OLD = """                lo = max(0, m.start() - 120)
                ctx = text[lo:m.start() + 120]
                cands = list(VERSE_NEAR.finditer(ctx))
                if not cands:
                    continue
                rel = m.start() - lo
                cands.sort(key=lambda vm: abs(vm.start() - rel))
                if any(want_type in marks.get(f"Jer.{rc}.{rv}", [])
                       for vm in cands
                       for rc, rv in readings(int(vm.group(1)), int(vm.group(2)))):
                    continue
                if ABSENCE.search(ctx):
                    continue
                vm = cands[0]
                c, v = int(vm.group(1)), int(vm.group(2))
"""
CM_RULE1_NEW = """                # S1-22 (ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 (b)): the claim binds to the verse numbers written in
                # its OWN clause - C:V, C.V, 'MT C:V' or a dotted ref alike - plus a parenthetical opening directly after it; a
                # claim naming no number in its clause is left to rule 2 (symmetry)
                c_lo_, c_hi_ = clause_bounds(text, m.start(), m.end(), NUM_CLAUSE_END)
                named_ = [p for pairs in puncta_claim_numbers(text, m.start(), m.end()) for p in pairs]
                if not named_:
                    continue
                # W1 (ezek_controlling_rulings_a1#e5 ruling FLAGS-TF2-1): a mark of the claimed TYPE after N or after N-1 satisfies
                # the claim; the type test is untouched, and an absence claim never takes the N-1 acceptance (rule 3 reads N)
                if any(want_type in marks.get(f"Jer.{rc}.{rv}", [])
                       for c0, v0 in named_
                       for rc, rv in before_readings(c0, v0)):
                    continue
                # W6 (#e5 FLAGS-TF2-1): the letter-name absence form is an absence phrase, so rule 1 skips its clause
                if ABSENCE.search(text[c_lo_:c_hi_]) or letter_absences(text, c_lo_, c_hi_):
                    continue
                c, v = named_[0]
"""
CM_RULE3_OLD = """            for am in ABSENCE.finditer(text):
                have = relevant(span_pairs(row), marks)
                if have:
                    flags.append({"decision_id": did, "rule": "false_mark_absence_claim",
                                  "claim_context": text[max(0, am.start() - 60):am.start() + 80],
                                  "span_relevant_marks_mt_keys": have})
                    break
"""
CM_RULE3_NEW = """            # S1-22 (#e4 ruling TOOLFIX-2 (b)): an absence phrase is scoped to the verse, range or chapter its own clause
            # names; an absence phrase naming none keeps the span-scoped check
            for am in sorted(list(ABSENCE.finditer(text)) + letter_absences(text), key=lambda x: x.start()):   # W6 (#e5 FLAGS-TF2-1)
                named_ = [p for pairs in puncta_claim_numbers(text, am.start(), am.end()) for p in pairs]
                c_lo_, c_hi_ = clause_bounds(text, am.start(), am.end(), NUM_CLAUSE_END)
                for chm_ in CHAPTER_NAMED.finditer(text, c_lo_, c_hi_):
                    ch_ = int(chm_.group(1))
                    named_ += [(ch_, vv_) for vv_ in range(1, MT_LAST_VERSE.get(ch_, 0) + 1)]
                if named_:
                    scope_ = "named"
                    have = {f"Jer.{rc}.{rv}": marks[f"Jer.{rc}.{rv}"] for c0, v0 in named_ for rc, rv in readings(c0, v0)
                            if marks.get(f"Jer.{rc}.{rv}")}
                else:
                    scope_ = "span"
                    have = relevant(span_pairs(row), marks)
                if have:
                    flags.append({"decision_id": did, "rule": "false_mark_absence_claim", "scope": scope_,
                                  "claim_context": text[max(0, am.start() - 60):am.start() + 80],
                                  "span_relevant_marks_mt_keys": have})
                    break
"""
CM_RULE4_OLD = """            for m in KQ.finditer(text):
                lo = max(0, m.start() - 120)
                ctx = text[lo:m.start() + 120]
                cands = list(VERSE_NEAR.finditer(ctx))
                if not cands:
                    continue
                rel = m.start() - lo
                cands.sort(key=lambda vm: abs(vm.start() - rel))
                if any(kq.get(f"Jer.{rc}.{rv}") or (f"Jer.{rc}.{rv}" in kq_note_keys and NOTE_WORD.search(ctx))
                       for vm in cands
                       for rc, rv in readings(int(vm.group(1)), int(vm.group(2)))):
                    continue
                vm = cands[0]
                c, v = int(vm.group(1)), int(vm.group(2))
"""
CM_RULE4_NEW = """            # S1-22 (#e4 ruling TOOLFIX-2 (b)): a K/Q claim binds to the verse numbers in its OWN clause (C:V, C.V, 'MT C:V'
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
                        keys_ = {f"Jer.{mt_[0]}.{mt_[1]}" for c0, v0 in span_pairs(row) for mt_ in [web_to_mt(c0, v0)] if mt_} - row_named_mt_keys(text)
                    elif named_:
                        scope_ = "named"
                        keys_ = {f"Jer.{rc}.{rv}" for c0, v0 in named_ for rc, rv in readings(c0, v0)}
                    else:
                        scope_ = "span"
                        keys_ = {f"Jer.{mt_[0]}.{mt_[1]}" for c0, v0 in span_pairs(row) for mt_ in [web_to_mt(c0, v0)] if mt_}
                    present_ = sorted(k_ for k_ in keys_ if kq.get(k_))
                    if present_:
                        flags.append({"decision_id": did, "rule": "false_kq_absence_claim", "scope": scope_,
                                      "kq_mt_keys": present_, "claim_context": text[max(0, m.start() - 60):m.start() + 80]})
                    continue
                if not named_:
                    continue
                if any(kq.get(f"Jer.{rc}.{rv}") or (f"Jer.{rc}.{rv}" in kq_note_keys and NOTE_WORD.search(ctx))
                       for c0, v0 in named_
                       for rc, rv in readings(c0, v0)):
                    continue
                c, v = named_[0]
"""


def stage_check_marks():
    src = (JER / "check_marks.py").read_text(encoding="utf-8")
    head, t = split_doc(src, "Paragraph-mark/segment-disclosure symmetry checker")
    t = sub_exact(t, "from jer_lib import (", "from ezek_lib import (", 1, "cm import")
    anchor = r'''                          r"\bnun\s+ze[i']?ira\b|\bze[i']?ira\b|\bminuscule\b", re.I)
'''
    t = sub_exact(t, anchor, anchor + PUNCTA_RE + "PUNCTA_SITES = {(41, 20), (46, 22)}   # MT; asserted by ezek_lib's selftest\n" + CHAPTER_NAMED_RE + CM_W_RE,
                  1, "cm puncta constants")
    t = sub_ws(t, '"note": ("WLC Jer carries NO large-letter segs; its only " "special letter is the small nun at MT 39:13"),',
               '"note": "WLC Ezek carries NO special-letter seg of any class",', 1, "cm large-letter note")
    t = sub_ws(t, "# small-letter claims: valid ONLY when bound (window heuristic) to # the one inventory site MT 39:13",
               "# small-letter claims: valid ONLY when bound (window heuristic) to an\n"
               "            # inventory site - Ezek has none, so every small-letter claim flags", 1, "cm small-letter comment")
    t = sub_ws(t, '"note": ("WLC Jer\'s only special-letter seg is the small " "nun at MT 39:13 - no nearby cited verse carries " "one"),',
               '"note": ("WLC Ezek carries NO special-letter seg of any class - "\n'
               '                                           "every small-letter claim is a fabrication"),', 1, "cm small-letter note")
    t = sub_ws(t, 'mapped. Coincide outside chs 8-9."""', 'mapped. Coincide outside WEB 20:45-21:32 / MT ch 21."""', 1, "cm readings doc")
    t = sub_exact(t, '    small_inv = pm.get("other_segs", {})\n',
                  '    small_inv = pm.get("other_segs", {})\n' + KQ_NOTE_KEYS_LINE, 1, "cm kq_note_keys")
    t = sub_exact(t, '                if any(kq.get(f"Jer.{rc}.{rv}")\n',
                  '                if any(kq.get(f"Jer.{rc}.{rv}") or (f"Jer.{rc}.{rv}" in kq_note_keys and NOTE_WORD.search(ctx))\n',
                  1, "cm kq editorial-note tier")
    rule1 = "            # Rule 1: petuchah/setumah claims bind to the NEAREST windowed ref\n"
    t = sub_exact(t, rule1, CM_PUNCTA_ARM + rule1, 1, "cm puncta arm")
    t = sub_exact(t, CM_RULE1_OLD, CM_RULE1_NEW, 1, "cm S1-22 rule 1 own-clause binding")
    t = sub_exact(t, CM_RULE3_OLD, CM_RULE3_NEW, 1, "cm S1-22 rule 3 scoped absence")
    t = sub_exact(t, CM_RULE4_OLD, CM_RULE4_NEW, 1, "cm S1-22 rule 4 own-clause binding and negated K/Q")
    return "check_marks.py", join_doc(head, t, CM_DOC), t


STALE_FACTS = re.compile(r"8:23|\b9:1\b|9:2-26|9:1-25|chs 8-9|39:13|39\.13|\b1364\b|\b52 chapters|4QJer|2QJer|Yirmeyahu|"
                         r"small nun|MT 9:7|\b303\b|\b246\b|\b157\b|\b141\b|\b124\b|DENSEST|twelve doubled")


def main():
    # --replace NAME=SHA256 ... permits replacing a staged file only when its current bytes carry exactly that digest
    # (a pinned expected-before value), so an edited or unknown file is never overwritten.
    pinned = dict(a.split("=", 1) for a in sys.argv[sys.argv.index("--replace") + 1:]) if "--replace" in sys.argv else {}
    staged = [stage_citation_sweep(), stage_check_marks()]
    for name, text, _ in staged:
        assert name not in PROTECTED
        out = DST / name
        if out.exists() and out.read_text(encoding="utf-8") != text:
            have = hashlib.sha256(out.read_bytes()).hexdigest()
            if pinned.get(name) != have:
                abort("%s exists with different content (sha256 %s) and no matching --replace pin; nothing overwritten"
                      % (name, have))
            print("replacing %s: expected-before sha256 matched the pin" % name)
    for name, text, code in staged:
        (DST / name).write_text(text, encoding="utf-8", newline="\n")
        py_compile.compile(str(DST / name), doraise=True)
        stale = [(i, l.strip()[:110]) for i, l in enumerate(text.splitlines(), 1) if STALE_FACTS.search(l)]
        jer_in_code = [l.strip()[:110] for l in re.sub(r"\bJer\b", "Ezek", code).splitlines() if re.search(r"\bJer\b|jer_lib", l)]
        print("%-18s written | compile ok | stale-fact lines: %d | Jer tokens left in code: %d"
              % (name, len(stale), len(jer_in_code)))
        for i, l in stale:
            print("      %d: %s" % (i, l))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
