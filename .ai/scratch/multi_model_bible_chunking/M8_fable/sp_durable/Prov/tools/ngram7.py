#!/usr/bin/env python3
"""7-gram cross-row template scanner (Hebrew-quotation-aware), Prov.

Tokenizes the authored prose of every row (lowercased alpha tokens), after
removing Hebrew runs and curly-quoted WEB quotations (quoting the source is
legitimate; templated AUTHORIAL prose is not). Any 7-gram shared by >= GATE
rows fails the gate. 7-grams that occur verbatim in the WEB book text are also
excluded (Prov repeats its speech-introduction formulas and parallelistic
phrasing heavily — quoting the source loosely is not templating).

REV-ROUND (attempt revround_tools_ps_r1): CITATION APPARATUS is stripped
before gram extraction — web:/oshb: refs, bare Prov.C.V tokens and "MT c:v" /
"WEB c:v" qualifiers tokenize into "web ps oshb ps …" chains that are mandated
by the dual-cite rule and carry zero lexical content. Un-stripped, consecutive
dual-cite chains produced the only gate-crossing grams over rows_v1
("web ps oshb ps web ps oshb" x10 rows) — a tool-scope artifact, not writer
templating (CYCLE_STATE ngram7 RED DISPOSITION).
Usage: ngram7.py rows.jsonl [--gate 10] [more files: rows are pooled]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prov_lib import HEB_RUN, load_verse_maps, norm_english

GATE = 10
# citation apparatus: witness-prefixed refs, bare Prov.C.V tokens, MT/WEB
# qualifiers. Stripped BEFORE tokenization (rev-round item 5).
REF_TOKENS = re.compile(
    r"\b(?:web|oshb):\s*Prov\.\d+\.\d+(?:\s*[-–]\s*(?:(?:web|oshb):)?(?:Prov\.)?\d+(?:\.\d+)?)?"
    r"|\bPs\.\d+\.\d+(?:\s*[-–]\s*(?:Prov\.)?\d+(?:\.\d+)?)?"
    r"|\b(?:MT|WEB)\s+\d+[:.]\d+(?:\s*[-–]\s*(?:\d+[:.])?\d+)?"
    r"|\b(?:web|oshb):", re.I)


def rows_from(p: Path):
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    data = json.loads(text)
    if isinstance(data, dict):
        return data.get("decisions", [v for v in data.values() if isinstance(v, dict)])
    return data


def prose(row) -> str:
    parts = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                # excluded: refs/ids/spans PLUS machine-added provenance keys
                # (writer_*/attempt/routing tokenize into shared frames — the
                # Neh lesson-d class; Tier-0 correction logged 2026-08-10,
                # Prov v0 run: 43-row false RED from combine-added provenance)
                # patch prov_tools_p2 (2026-08-18, corpus-run finding, same
                # class as p1): unit_type + parent_collection are mandated
                # structural enums/range-strings, not authored prose — their
                # fixed values ("single_proverb", "C2 Prov.10.1-...") tokenize
                # into shared frames across hundreds of rows. confidence is a
                # 1-token enum, excluded for the same reason.
                if k not in ("boundary_evidence_refs", "span", "decision_id",
                             "chunk_id", "writer_part", "writer_decision_id",
                             "writer_attempt_id", "attempt_id", "routing_used",
                             "unit_type", "parent_collection", "confidence"):
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str):
            parts.append(o)
    walk(row)
    return " ".join(parts)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    gate = GATE
    if "--gate" in sys.argv:
        gate = int(sys.argv[sys.argv.index("--gate") + 1])
        args = [a for a in args if a != str(gate)]
    web, _ = load_verse_maps()
    webtext = norm_english(" ".join(d["text"] for d in web.values())).lower()
    web_tokens = re.findall(r"[a-z]+", webtext)
    web_7grams = {" ".join(web_tokens[i:i + 7]) for i in range(len(web_tokens) - 6)}

    grams: dict[str, set[str]] = {}
    n = 0
    for f in args:
        for row in rows_from(Path(f)):
            if not isinstance(row, dict):
                continue
            rid = row.get("decision_id") or f"{Path(f).name}#{n}"
            n += 1
            s = prose(row)
            s = HEB_RUN.sub(" ", s)
            s = re.sub(r"“[^”]*”", " ", s)
            s = REF_TOKENS.sub(" ", s)          # rev-round: citation apparatus
            toks = re.findall(r"[a-z]+", norm_english(s).lower())
            for i in range(len(toks) - 6):
                g = " ".join(toks[i:i + 7])
                if g in web_7grams:
                    continue
                grams.setdefault(g, set()).add(rid)
    offenders = sorted(((g, sorted(ids)) for g, ids in grams.items() if len(ids) >= gate),
                       key=lambda x: -len(x[1]))
    worst = sorted(((len(ids), g) for g, ids in grams.items()), reverse=True)[:5]
    print(json.dumps({"rows": n, "gate": gate,
                      "offending_7grams": [{"gram": g, "rows": len(ids), "row_ids": ids[:15]}
                                           for g, ids in offenders],
                      "worst_reuse": [{"rows": c, "gram": g} for c, g in worst],
                      "status": "GREEN" if not offenders else "RED"},
                     ensure_ascii=False, indent=1))
    return 1 if offenders else 0


if __name__ == "__main__":
    raise SystemExit(main())
