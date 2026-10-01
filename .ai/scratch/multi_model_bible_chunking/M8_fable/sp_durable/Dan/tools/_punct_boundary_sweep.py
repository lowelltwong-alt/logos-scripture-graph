#!/usr/bin/env python3
"""E-23 FLAGS sweep, Dan (OW-1 prospective arm, owner warning 2026-08-31).

Detects TRANSLATION-layer punctuation / paragraphing / capitalization doing
driver or corroboration work in the two driver fields (boundary_rationale,
strongest_rejected_alternative). Tier-4 metadata may never drive a boundary
(owner addendum); this sweep flags the language class so a model lane can
triage driver-use vs defensive mention (E-12 law: flags are candidates,
disposition by content, never auto-suppress, never auto-fail).

Runs at the rev round over revised rows (and on demand). Baseline run over
the frozen draft corpus recorded at the boss-round census.
Usage: _punct_boundary_sweep.py rows.jsonl [more...]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dan_lib import HEB_RUN

DRIVER_FIELDS = ("boundary_rationale", "strongest_rejected_alternative")

CLASSES = {
    "punctuation_token": re.compile(r"\bpunctuation\b", re.I),
    "period_fullstop_driver": re.compile(
        r"\bfull stop\b|"
        r"\bperiod\b(?=[^.;]{0,50}\b(?:ends?|closes?|divides?|marks?|separates?|boundar)\b)|"
        r"\b(?:ends?|closes?|divides?|separates?)\b[^.;]{0,50}\bperiod\b", re.I),
    "question_exclamation_driver": re.compile(
        r"\bquestion mark\b|\bexclamation (?:mark|point)\b", re.I),
    "quotation_mark_structure": re.compile(
        r"\bquotation marks?\b[^.;]{0,60}\b(?:open|close|end|begin|onset|boundar)|"
        r"\b(?:open|close|end|begin)\w*\b[^.;]{0,60}\bquotation marks?\b", re.I),
    # translation-layer only: "Masoretic paragraphing" is the tier-3 scribal
    # layer (mark-absence-as-evidence has its own lane, CWO-8/E-07), not E-23
    "paragraph_layer": re.compile(
        r"(?<!Masoretic )\bparagraph(?:ing|\s+break|\s+division)s?\b", re.I),
    "capitalization": re.compile(r"\bcapitali[sz](?:e|ed|ation)\b|\bcapital letter\b", re.I),
    "english_sentence_layer": re.compile(
        r"\b(?:WEB|English|translation)['’]?s?\b[^.;]{0,50}\bsentence\b|"
        r"\bsentence\b[^.;]{0,50}\b(?:WEB|English|translation)\b", re.I),
}


def rows_from(p: Path):
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    data = json.loads(text)
    if isinstance(data, dict):
        return data.get("decisions", [v for v in data.values() if isinstance(v, dict)])
    return data


def main() -> int:
    flags = []
    rows_n = 0
    for f in sys.argv[1:]:
        for row in rows_from(Path(f)):
            if not isinstance(row, dict):
                continue
            rows_n += 1
            did = row.get("writer_decision_id") or row.get("decision_id") or "?"
            for field in DRIVER_FIELDS:
                s = row.get(field)
                if not isinstance(s, str):
                    continue
                masked = HEB_RUN.sub(" ", s)
                masked = re.sub(r"“[^”]*”", lambda m: " " * len(m.group(0)), masked)
                for cls, pat in CLASSES.items():
                    for m in pat.finditer(masked):
                        flags.append({"file": Path(f).name, "decision_id": did,
                                      "field": field, "class": cls,
                                      "match": m.group(0)[:60],
                                      "context": s[max(0, m.start() - 60):m.start() + 90]})
    by_class = {}
    for fl in flags:
        by_class[fl["class"]] = by_class.get(fl["class"], 0) + 1
    print(json.dumps({"rows_checked": rows_n, "flag_count": len(flags),
                      "by_class": by_class, "flags": flags,
                      "status": "GREEN" if not flags else "FLAGS"},
                     ensure_ascii=False, indent=1))
    return 1 if flags else 0


if __name__ == "__main__":
    raise SystemExit(main())
