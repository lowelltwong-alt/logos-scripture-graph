#!/usr/bin/env python3
"""Universal-claim detector (Isa; lexicon WIDENED per Job lesson j on top of
the Ezra lesson-f tightening).

Flags only / always / never / unique(ly) / densest / first / last / sole(ly) /
exclusively / nowhere (else) / anywhere else / singleton / shared by no / no
other — PLUS the Job-lesson-j classes: every / all / each / none, no new /
no comparable, verbatim / identical / matched, "not ... until", and
superlatives (-est forms, most/least + adjective) — in authored prose lacking
an ADJACENT sweep citation (same string field, +-160 chars). A sweep citation
REQUIRES A DIGIT: "sweep: N" / "sweeps: N", "N of M", "N times", "xN",
"N occurrences", "book-wide (N)", "N book-wide", "all N", "across N verses".

Matches inside curly-quoted WEB quotations and Hebrew runs are ignored (the
source text may itself say "first"). Flags are candidates for review, not
auto-fails. Usage: check_universals.py file...

REV-ROUND UPGRADES (attempt revround_tools_ps_r1; each item live-proven in
CYCLE_STATE before the change):
 a) ALTERNATION BOUNDARY FIX — every plain alternative now carries a trailing
    \\b. Before this, "never" fired inside "nevertheless" (and first/last
    inside firstly/lastly/firstborn) because only the group start was bounded.
 b) SENTENCE-SCOPED SWEEP — the +-160-char context window laundered any digit
    anywhere near a claim (a "2 verses" 150 chars away cleared an unrelated
    unswept claim). The sweep must now sit in the SAME sentence as the claim;
    sentences split on [.;] with citation periods (Isa.C.V, "vv.", "cf.")
    masked so a ref never severs a sentence.
 c) LEXICON ADDS — absent(-from), without comparable/other/further/new/
    parallel, no parallel, unbroken/uninterrupted/continuous, rare(ly)/
    isolated; SWEEP accepts spelled numerals one..ten as digit-equivalents.
 d) EST_ALLOW loses "best-" (reception superlatives were never flaggable).
 e) DOMAIN-SIZE digits are rejected: "remaining 7 verses" / "of the 8 verses"
    state the domain's size and perform no sweep, so they no longer satisfy
    the gate on their own.
 f) TIER-VOCABULARY DAMPENER — a claim whose sentence names a collate tier
    (byte / nfd / accent_stripped / skeleton) beside a specific ref is
    grounded in a byte comparison; those are counted, not flagged (they are
    the mandated tier words tripping the heuristic — the 42-of-47 residual
    class the author wave triaged by hand).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from isa_lib import HEB_RUN

# EVERY plain alternative is \b-terminated (rev-round item a)
UNIV = re.compile(r"\b(only\b|always\b|never\b|unique(?:ly|ness)?\b|densest\b|"
                  r"first\b|last\b|"
                  r"sole(?:ly)?\b|exclusively\b|nowhere(?: else)?\b|anywhere else\b|"
                  r"singleton\b|single(?!-witness|\s+witness)(?:\s+occurrence)?\b|"
                  r"shared (?:by|with) no\b[^.;]{0,40}|no other\b[^.;]{0,40}|"
                  r"every\b|all\b|each\b|none\b|"
                  r"no (?:new|comparable|further|other)\b[^.;]{0,40}|"
                  r"(?:with|has|have|carr(?:y|ies)) no\b[^.;]{0,40}|"
                  r"verbatim\b|identical(?:ly)?\b|match(?:es|ed)\b|"
                  r"entirely\b|throughout\b|across the whole\b|peak\b|"
                  r"not\b[^.;]{0,60}?\buntil\b|"
                  # rev-round lexicon adds (item c)
                  r"absent(?:\s+from)?\b|"
                  r"without\s+(?:any\s+)?(?:comparable|other|further|new|parallel|an?\s+(?:addressee|person|address)\s+change)\b|"
                  r"no\s+parallel\b|"
                  r"unbroken\b|uninterrupted\b|continuous(?:ly)?\b|"
                  r"rare(?:ly)?\b|isolated\b|"
                  r"\w{3,}est\b|(?:most|least)\s+\w+)", re.I)
# spelled numerals count as digits in a sweep citation (rev-round item c)
NUM = r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)"
SWEEP = re.compile(r"(sweeps?[:\s(][^.;]{0,30}?\d|"
                   rf"\b{NUM}\s*(?:of|/)\s*(?:the\s+)?{NUM}\b|"
                   rf"\b{NUM}\s*(?:times|hits|occurrences?|instances?|notes?|tokens?)\b|"
                   rf"[x×]\s*\d+|\ball\s+{NUM}\b|\b\d+x\b|book-?wide\s*[:(]?\s*\d|"
                   rf"\b{NUM}\s+book-?wide|(?:across|in)\s+{NUM}\s+verses?\b|"
                   rf"\b{NUM}\s+(?:\w+\s+)?verses?\b)", re.I)
# DOMAIN-SIZE digits state how big the domain is and sweep nothing (item e):
# a SWEEP hit lying WHOLLY inside one of these does not satisfy the gate.
DOMAIN_SIZE = re.compile(rf"\b(?:remaining|of\s+the|the\s+other|its\s+own)\s+"
                         rf"{NUM}\s+(?:\w+\s+)?verses?\b", re.I)
# TIER-VOCABULARY dampener (item f): a collate tier named beside a specific
# ref in the same sentence = the claim rests on a byte comparison.
TIER_WORD = re.compile(r"\b(?:byte|nfd|accent[_\s-]?stripped|skeleton)\b", re.I)
REF_TOKEN = re.compile(r"Isa\.\d+\.\d+|\b\d{1,3}:\d{1,3}\b")
# periods that are NOT sentence ends (item b): citation and abbreviation dots
PROTECT = re.compile(r"Isa\.\d+\.\d+|\bPs\.|\bvv?\.|\bcf\.|\bch\.|\bvs\.|"
                     r"\bno\.|\be\.g\.|\bi\.e\.|\d\.\d", re.I)
# -est false-positive dampener: ordinary lexical -est words that are not
# superlative claims (byte-diagnosed during smoke; extend as needed).
# rev-round item d: "best-" REMOVED — reception superlatives ("best-attested")
# are claims like any other and were never meant to be unflaggable.
EST_ALLOW = re.compile(r"\b(?:rest|west|test|guest|priest|harvest|"
                       r"request|forest|honest|modest|nearest\s+ms|interest|"
                       r"protest|contest|conquest|manifest|earnest)\b", re.I)
# Dampeners added from the p10 flag triage (2026-08-12):
# 1. grammatical person terms ("first-person", "first person") are not
#    exclusivity claims;
# 2. the brief-MANDATED parent-grouping sentence necessarily uses all/every/
#    single ("All rows of this psalm belong to a single parent unit") — a
#    'parent' within the match context marks that boilerplate.
PERSON_AFTER = re.compile(r"^[-\s]person\b", re.I)
PARENT_CTX = re.compile(r"\bparent\b", re.I)


def iter_strings(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "independence_scope":     # brief-mandated verbatim frame
                continue
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


def sentence_spans(s: str) -> list[tuple[int, int]]:
    """Split on [.;], but never inside a citation/abbreviation dot (Isa.3.1,
    'vv.', 'cf.') — otherwise a ref would sever a claim from its own sweep."""
    mask = bytearray(len(s))
    for m in PROTECT.finditer(s):
        for i in range(m.start(), m.end()):
            mask[i] = 1
    out = []
    start = 0
    for i, ch in enumerate(s):
        if (ch == "." or ch == ";") and not mask[i]:
            out.append((start, i + 1))
            start = i + 1
    out.append((start, len(s)))
    return [(a, b) for a, b in out if b > a]


def sentence_of(spans: list[tuple[int, int]], pos: int) -> tuple[int, int]:
    for a, b in spans:
        if a <= pos < b:
            return (a, b)
    return spans[-1] if spans else (0, 0)


def swept(sent: str) -> bool:
    """A sweep citation in this sentence that is NOT purely a domain-size
    statement ("remaining 7 verses" / "of the 8 verses")."""
    dom = [(m.start(), m.end()) for m in DOMAIN_SIZE.finditer(sent)]
    for m in SWEEP.finditer(sent):
        if any(a <= m.start() and m.end() <= b for a, b in dom):
            continue
        return True
    return False


def main() -> int:
    flags = []
    checked = 0
    tier_dampened = 0
    for f in sys.argv[1:]:
        for path, s in iter_strings(load_any(Path(f))):
            s2 = HEB_RUN.sub(" ", s)
            s2 = re.sub(r"“[^”]*”", lambda m: " " * len(m.group(0)), s2)
            spans = sentence_spans(s2)
            for m in UNIV.finditer(s2):
                if m.group(1) and m.group(1).lower().endswith("est") and \
                        EST_ALLOW.search(m.group(1)):
                    continue
                if PERSON_AFTER.match(s2[m.end():m.end() + 10]):
                    continue
                if PARENT_CTX.search(s2[max(0, m.start() - 80):m.start() + 80]):
                    continue
                checked += 1
                a, b = sentence_of(spans, m.start())
                sent = s2[a:b]
                if swept(sent):
                    continue
                if TIER_WORD.search(sent) and REF_TOKEN.search(sent):
                    tier_dampened += 1        # grounded in a byte comparison
                    continue
                flags.append({"file": Path(f).name, "path": path,
                              "claim": m.group(1),
                              "context": s[max(0, m.start() - 60):m.start() + 80]})
    print(json.dumps({"claims_seen": checked, "flag_count": len(flags),
                      "tier_vocabulary_dampened": tier_dampened, "flags": flags,
                      "status": "GREEN" if not flags else "FLAGS"},
                     ensure_ascii=False, indent=1))
    return 1 if flags else 0


if __name__ == "__main__":
    raise SystemExit(main())
