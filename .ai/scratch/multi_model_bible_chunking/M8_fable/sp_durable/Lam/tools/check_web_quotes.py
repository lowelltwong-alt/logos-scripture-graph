#!/usr/bin/env python3
"""WEB-quote verbatim checker (gloss-as-WEB detector), Lam.

LAM NOTE: Lam is an IDENTITY book (byte-proven at Phase 0): WEB and MT
agree verse-for-verse (154/154), NO offset zone, NO split; PSALM_RULES is
identity in every chapter, so the NEIGHBOR-ONLY WARN arm below is INERT here
(kept for API parity).

Scans every string field of the given JSON/JSONL file(s) for curly-quoted
English spans ("…") that sit within 200 chars of a web:Lam.C.V ref in the
same field, and verifies each span is a verbatim (ellipsis-aware, punctuation-
normalized) substring of the folded WEB text of that ref (range-aware, plus
one-verse slack on each side for quotes crossing the cited edge).

Hebrew-majority quoted spans are skipped by the VERBATIM arm (collation's
job) but caught by the E-15 arms below. Flags are candidates for
orchestrator review, not auto-fails: a flagged span is either a
paraphrase/gloss presented with quote marks near a ref (the 2Chr systemic
class, again the dominant Ezra repair-site class) or a quote with a wrong
ref. Spans of fewer than 2 words are ignored by the verbatim arm.

E-15 ARMS (NEW for Lam, per the error-pattern ledger - the Isa spot wave
proved the closed-pair matcher leaves unclosed/uncurly quotes OUTSIDE
Tier-0 coverage, and Hebrew inside curly pairs corrupts pairing enough to
MASK well-formed English quotes; 4 masked binding defects surfaced there):
 e15a UNBALANCED/BROKEN CURLY PAIRING per string field: counts of “ and ”
      must match AND alternate in order (no ” before an open, no double-
      open) - a broken field is flagged AND its quotes are invisible to the
      pair scanner, so the flag is the only Tier-0 signal.
 e15b HEBREW INSIDE CURLY DOUBLE QUOTES: the campaign convention is curly
      double quotes for WEB English ONLY (Hebrew is spliced bare; row/tool
      wording uses straight quotes). Any “…” span containing a Hebrew
      codepoint is flagged (this is also exactly the interleaving that
      masked the Isa defects).
 e15c WEB TEXT IN STRAIGHT DOUBLE QUOTES near a web: ref: a "…" span of 3+
      English words that verbatim-matches the cited WEB text evades the
      curly scanner - flagged as delimiter evasion (parallel to the
      single-curly arm).

REV-ROUND (attempt revround_tools_ps_r1): NEIGHBOR-ONLY WARN arm. The +-1
verse slack that legitimately absorbs quotes crossing a cited edge also
exactly cancels the MT-number-under-WEB-prefix hazard in an offset-bearing book
(none in Lam), "web:Lam.9.3" written for MT 9:3 is actually WEB 9:4, and the
slack makes that wrong ref pass silently. A quote that matches ONLY in a
widened neighbor of a NON-IDENTITY chapter (rule != identity: 8/9) is
therefore reported in neighbor_only_warns (WARN only - never a flag, never a
status change); identity-chapter neighbor matches stay silent, since there
the ref is simply off by one with no witness hazard.
Usage: check_web_quotes.py file1.json [file2.jsonl ...]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lam_lib import (LAST_VERSE, PSALM_RULES, expand_ref_token, load_verse_maps,
                     web_quote_found)

QUOTE = re.compile(r"“([^”]+)”")
WREF = re.compile(r"web:(Lam\.\d+\.\d+(?:-(?:Lam\.)?\d+(?:\.\d+)?)?)")
HEBREW_CP = re.compile(r"[֐-׿]")
STRAIGHT_Q = re.compile(r'"([^"]+)"')


def widen(pairs):
    """Neighbor-widen a ref's verse set. (Historical Ps-lineage note: the
    v=0 handling below is inert in Lam - Lam has NO title pseudo-verses and
    citation_sweep bans Lam.N.0 refs outright; kept for tool parity.)"""
    out = set(pairs)
    if pairs:
        c, v = pairs[0]
        if v > 1:
            out.add((c, v - 1))
        elif v == 1:
            out.add((c - 1, LAST_VERSE.get(c - 1, 0)))
        c, v = pairs[-1]
        out.add((c, v + 1) if v < LAST_VERSE.get(c, 0) else (c + 1, 1))
    valid = {(c, v) for c in LAST_VERSE for v in range(1, LAST_VERSE[c] + 1)}
    valid |= {(c, 0) for c in LAST_VERSE}
    return sorted(p for p in out if p in valid)


def iter_strings(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from iter_strings(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from iter_strings(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o


def load_any(p: Path):
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    return json.loads(text)


def curly_pairing_broken(s: str):
    """E-15a: returns a reason string when the curly-double pairing of a
    field is unbalanced or out of order; None when clean."""
    depth = 0
    for ch in s:
        if ch == "“":
            depth += 1
            if depth > 1:
                return "double-open (nested “ before close)"
        elif ch == "”":
            depth -= 1
            if depth < 0:
                return "close ” with no open"
    if depth != 0:
        return f"unclosed “ ({depth} open at field end)"
    return None


def main() -> int:
    web, _ = load_verse_maps()
    flags = []
    neighbor_only_warns = []      # rev-round: WARN only, never a flag
    checked = 0
    for f in sys.argv[1:]:
        data = load_any(Path(f))
        for path, s in iter_strings(data):
            refs = [(m.start(), m.group(1)) for m in WREF.finditer(s)]
            # ---- E-15a: pairing integrity BEFORE any pair-based scanning ----
            if "“" in s or "”" in s:
                broken = curly_pairing_broken(s)
                if broken:
                    flags.append({"file": Path(f).name, "path": path,
                                  "issue": f"e15a_curly_pairing_broken: {broken}",
                                  "note": ("field's quotes are INVISIBLE to the pair "
                                           "scanner until pairing is repaired")})
            # ---- E-15b: Hebrew inside curly double quotes ----
            for qm in QUOTE.finditer(s):
                if HEBREW_CP.search(qm.group(1)):
                    flags.append({"file": Path(f).name, "path": path,
                                  "quote": qm.group(1)[:60],
                                  "issue": ("e15b_hebrew_in_curly_quotes (curly double "
                                            "quotes are for WEB English ONLY; Hebrew is "
                                            "spliced bare - this interleaving also masks "
                                            "English-quote pairing)")})
            # ---- E-15c: WEB text in straight double quotes near a ref ----
            for sm in STRAIGHT_Q.finditer(s):
                span_s = sm.group(1).strip()
                if len(span_s.split()) < 3 or HEBREW_CP.search(span_s):
                    continue
                if not refs:
                    continue
                for pos, r in refs:
                    if abs(pos - sm.start()) > 200 and abs(pos - sm.end()) > 200:
                        continue
                    pairs = widen(expand_ref_token(r))
                    texts = [web[f"Lam.{c}.{v}"]["text"] for c, v in pairs]
                    if web_quote_found(span_s, texts):
                        flags.append({"file": Path(f).name, "path": path,
                                      "quote": span_s[:90],
                                      "issue": ("e15c_web_text_in_straight_quotes "
                                                "(delimiter evasion - WEB quotes use "
                                                "curly double + inline web: ref)")})
                        break
            # OL-c42 false-positive fix: WEB itself sets nested speech in
            # single curly quotes - a single-curly span wholly inside a
            # double-curly WEB quote is the source's own punctuation, not
            # delimiter evasion. Skip those.
            dq_spans = [(m.start(), m.end()) for m in QUOTE.finditer(s)]
            for sq in re.finditer(r"‘([^’]{6,})’", s):
                if any(a <= sq.start() and sq.end() <= b for a, b in dq_spans):
                    continue
                span1 = sq.group(1).strip()
                if len(span1.split()) >= 3 and re.search(r"[A-Za-z]{3}", span1) and refs:
                    # flag ONLY when the span verbatim-matches WEB near a ref
                    # (true delimiter evasion). Glosses - the legitimate
                    # single-curly idiom - won't match verbatim.
                    hit = False
                    for pos, r in refs:
                        pairs = widen(expand_ref_token(r))
                        texts = [web[f"Lam.{c}.{v}"]["text"] for c, v in pairs]
                        if web_quote_found(span1, texts):
                            hit = True
                            break
                    if hit:
                        checked += 1
                        flags.append({"file": Path(f).name, "path": path,
                                      "quote": span1[:90],
                                      "issue": "verbatim WEB text in SINGLE curly quotes (delimiter evasion - rows use double curly + inline web: ref)"})
            for qm in QUOTE.finditer(s):
                span = qm.group(1).strip()
                if len(span.split()) < 2:
                    continue
                heb = len(HEBREW_CP.findall(span))
                lat = len(re.findall(r"[A-Za-z]", span))
                if heb > lat:
                    continue
                # OL-c03 hardening: a curly English quote with NO web: ref in
                # its field used to be silently skipped - the mandatory
                # quote+inline-ref convention makes that itself a flag.
                if not refs:
                    checked += 1
                    flags.append({"file": Path(f).name, "path": path,
                                  "quote": span[:90],
                                  "refs_nearby": [],
                                  "issue": "curly quote with NO web: ref in its field"})
                    continue
                # bind refs near EITHER quote edge - a long quote's own
                # trailing ref sits beyond 200 chars of its START (p10 triage)
                near = [r for pos, r in refs
                        if abs(pos - qm.start()) <= 200 or abs(pos - qm.end()) <= 200]
                if not near:
                    continue
                checked += 1
                ok = False
                neighbor_only = None
                # PASS 1: does ANY nearby ref carry the quote in its own verses?
                for r in near:
                    exact = expand_ref_token(r)
                    if web_quote_found(span, [web[f"Lam.{c}.{v}"]["text"]
                                              for c, v in exact]):
                        ok = True
                        break
                if not ok:
                    # PASS 2: only now does the +-1 slack decide the match -
                    # so neighbor-only is judged against EVERY nearby ref, not
                    # merely the first one tried.
                    for r in near:
                        exact = expand_ref_token(r)
                        pairs = widen(exact)
                        if web_quote_found(span, [web[f"Lam.{c}.{v}"]["text"]
                                                  for c, v in pairs]):
                            ok = True
                            if exact and PSALM_RULES.get(exact[0][0], {}).get(
                                    "rule") != "identity":
                                neighbor_only = r
                            break
                if neighbor_only:
                    neighbor_only_warns.append(
                        {"file": Path(f).name, "path": path, "quote": span[:90],
                         "ref": neighbor_only,
                         "issue": "quote matches only in a WIDENED neighbor of a "
                                  "NON-IDENTITY chapter (candidate MT number under "
                                  "a web: prefix, or an edge-crossing quote whose "
                                  "ref should be extended)"})
                if not ok:
                    flags.append({"file": Path(f).name, "path": path,
                                  "quote": span[:90], "refs_nearby": near})
    print(json.dumps({"quotes_checked": checked, "flag_count": len(flags),
                      "flags": flags,
                      "neighbor_only_warn_count": len(neighbor_only_warns),
                      "neighbor_only_warns": neighbor_only_warns,
                      "status": "GREEN" if not flags else "FLAGS"},
                     ensure_ascii=False, indent=1))
    return 1 if flags else 0


if __name__ == "__main__":
    raise SystemExit(main())
