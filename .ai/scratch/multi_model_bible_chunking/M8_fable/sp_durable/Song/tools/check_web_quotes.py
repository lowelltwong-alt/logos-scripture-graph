#!/usr/bin/env python3
"""WEB-quote verbatim checker (gloss-as-WEB detector), Song.

SONG NOTE: Song is NOT an identity book (byte-proven at Phase 0): MT 7:1 =
WEB 6:13 and MT 7:2-14 = WEB 7:1-13; PSALM_RULES marks chs 6-7 non-identity.
The NEIGHBOR-ONLY WARN arm below is therefore LIVE in WEB chs 6-7, where an
MT number written under a web: prefix is exactly one verse off.

Scans every string field of the given JSON/JSONL file(s) for curly-quoted
English spans ("…") that sit within 200 chars of a web:Song.C.V ref in the
same field, and verifies each span is a verbatim (ellipsis-aware, punctuation-
normalized) substring of the folded WEB text of that ref (range-aware, plus
one-verse slack on each side for quotes crossing the cited edge).

Hebrew-majority quoted spans are skipped (collation's job). Flags are
candidates for orchestrator review, not auto-fails: a flagged span is either a
paraphrase/gloss presented with quote marks near a ref (the 2Chr systemic
class, again the dominant Ezra repair-site class) or a quote with a wrong ref.
Spans of fewer than 2 words are ignored.

REV-ROUND (attempt revround_tools_ps_r1): NEIGHBOR-ONLY WARN arm. The +-1
verse slack that legitimately absorbs quotes crossing a cited edge also
exactly cancels the MT-number-under-WEB-prefix hazard: in Song's offset zone
(WEB chs 6-7), "web:Song.7.3" written for MT 7:3 is actually WEB 7:2, and the
slack makes that wrong ref pass silently. A quote that matches ONLY in a
widened neighbor of a NON-IDENTITY chapter (rule != identity: chs 6-7) is
therefore reported in neighbor_only_warns (WARN only — never a flag, never a
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
from song_lib import (LAST_VERSE, PSALM_RULES, expand_ref_token, load_verse_maps,
                    web_quote_found)

QUOTE = re.compile(r"“([^”]+)”")
WREF = re.compile(r"web:(Song\.\d+\.\d+(?:-(?:Song\.)?\d+(?:\.\d+)?)?)")


def widen(pairs):
    """Neighbor-widen a ref's verse set. v=0 (the Song.N.0 WEB title
    pseudo-verse) is a VALID pair — it must survive the filter so a quoted
    title compares against the title's own text (p01 writer erratum,
    2026-08-12)."""
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


def main() -> int:
    web, _ = load_verse_maps()
    flags = []
    neighbor_only_warns = []      # rev-round: WARN only, never a flag
    checked = 0
    for f in sys.argv[1:]:
        data = load_any(Path(f))
        for path, s in iter_strings(data):
            refs = [(m.start(), m.group(1)) for m in WREF.finditer(s)]
            # OL-c42 false-positive fix: WEB itself sets nested speech in
            # single curly quotes (e.g. web:Song.89.26) — a single-curly span
            # wholly inside a double-curly WEB quote is the source's own
            # punctuation, not delimiter evasion. Skip those.
            dq_spans = [(m.start(), m.end()) for m in QUOTE.finditer(s)]
            for sq in re.finditer(r"‘([^’]{6,})’", s):
                if any(a <= sq.start() and sq.end() <= b for a, b in dq_spans):
                    continue
                span1 = sq.group(1).strip()
                if len(span1.split()) >= 3 and re.search(r"[A-Za-z]{3}", span1) and refs:
                    # flag ONLY when the span verbatim-matches WEB near a ref
                    # (true delimiter evasion). Glosses — the legitimate
                    # single-curly idiom — won't match verbatim.
                    hit = False
                    for pos, r in refs:
                        pairs = widen(expand_ref_token(r))
                        texts = [web[f"Song.{c}.{v}"]["text"] for c, v in pairs]
                        if web_quote_found(span1, texts):
                            hit = True
                            break
                    if hit:
                        checked += 1
                        flags.append({"file": Path(f).name, "path": path,
                                      "quote": span1[:90],
                                      "issue": "verbatim WEB text in SINGLE curly quotes (delimiter evasion — rows use double curly + inline web: ref)"})
            for qm in QUOTE.finditer(s):
                span = qm.group(1).strip()
                if len(span.split()) < 2:
                    continue
                heb = len(re.findall(r"[֐-׿]", span))
                lat = len(re.findall(r"[A-Za-z]", span))
                if heb > lat:
                    continue
                # OL-c29 arm: WEB-looking English in SINGLE curly quotes in
                # row prose evades the double-curly scanner — flag spans of
                # 3+ English words in U+2018/U+2019 near web: refs as a
                # convention breach (review packets legitimately use single
                # curly for row prose; rows must not).
                # OL-c03 hardening: a curly English quote with NO web: ref in
                # its field used to be silently skipped — the mandatory
                # quote+inline-ref convention makes that itself a flag.
                if not refs:
                    checked += 1
                    flags.append({"file": Path(f).name, "path": path,
                                  "quote": span[:90],
                                  "refs_nearby": [],
                                  "issue": "curly quote with NO web: ref in its field"})
                    continue
                # bind refs near EITHER quote edge — a long quote's own
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
                    if web_quote_found(span, [web[f"Song.{c}.{v}"]["text"]
                                              for c, v in exact]):
                        ok = True
                        break
                if not ok:
                    # PASS 2: only now does the +-1 slack decide the match —
                    # so neighbor-only is judged against EVERY nearby ref, not
                    # merely the first one tried.
                    for r in near:
                        exact = expand_ref_token(r)
                        pairs = widen(exact)
                        if web_quote_found(span, [web[f"Song.{c}.{v}"]["text"]
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
