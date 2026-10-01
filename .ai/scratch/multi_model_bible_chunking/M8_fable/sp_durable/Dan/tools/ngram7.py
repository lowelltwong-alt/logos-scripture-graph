#!/usr/bin/env python3
"""7-gram cross-row template scanner (Hebrew-quotation-aware), Dan.

Tokenizes the authored prose of every row (lowercased alpha tokens), after
removing Hebrew runs and curly-quoted WEB quotations (quoting the source is
legitimate; templated AUTHORIAL prose is not). Any 7-gram shared by >= GATE
rows fails the gate. 7-grams that occur verbatim in the WEB book text are also
excluded (Jer repeats its refrains heavily — the stretched-out-hand refrain
"his anger is not turned away, but his hand is stretched out still", the
כה-אמר-יהוה speech frames, the hoy series openings; quoting the source
loosely is not templating).

REV-ROUND (attempt revround_tools_ps_r1): CITATION APPARATUS is stripped
before gram extraction — web:/oshb: refs, bare Dan.C.V tokens and "MT c:v" /
"WEB c:v" qualifiers tokenize into "web ps oshb ps …" chains that are mandated
by the dual-cite rule and carry zero lexical content. Un-stripped, consecutive
dual-cite chains produced the only gate-crossing grams over rows_v1
("web ps oshb ps web ps oshb" x10 rows) — a tool-scope artifact, not writer
templating (CYCLE_STATE ngram7 RED DISPOSITION).

Dan amendment (controlling ruling S1-07, 2026-09-29) - a NARROWING of this HARD member, stated in words: before
tokenizing, each whole-identifier occurrence of an exact underscore-bearing device-class key of
dan_device_inventory.json (every key of "formulae" that contains "_", plus the top-level keys
year_word_but_not_a_dateline, calendar_dates_not_datelines, month_or_day_word_not_a_date,
month_or_day_substring_artifacts) is removed, matched case-sensitively with (?<![A-Za-z0-9_]) and (?![A-Za-z0-9_])
boundaries, and replaced by a SEGMENT BREAK so that no 7-gram bridges a removed key. The key set is read from the
inventory at run time. A generic snake_case strip is rejected (it could hide author-coined identifiers used as
templating). Without this, the key month_or_day_word_not_a_date tokenized as the prose gram "month or day word not a
date" in 10 rows.
Usage: ngram7.py rows.jsonl [--gate 10] [more files: rows are pooled]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dan_lib import HEB_RUN, load_verse_maps, norm_english

GATE = 10
# citation apparatus: witness-prefixed refs, bare Dan.C.V tokens, MT/WEB
# qualifiers. Stripped BEFORE tokenization (rev-round item 5).
REF_TOKENS = re.compile(
    r"\b(?:web|oshb):\s*Dan\.\d+\.\d+(?:\s*[-–]\s*(?:(?:web|oshb):)?(?:Dan\.)?\d+(?:\.\d+)?)?"
    r"|\bPs\.\d+\.\d+(?:\s*[-–]\s*(?:Dan\.)?\d+(?:\.\d+)?)?"
    r"|\b(?:MT|WEB)\s+\d+[:.]\d+(?:\s*[-–]\s*(?:\d+[:.])?\d+)?"
    r"|\b(?:web|oshb):", re.I)

INVENTORY = Path(__file__).resolve().parent.parent / "dan_device_inventory.json"
TOP_LEVEL_KEYS = ("year_word_but_not_a_dateline", "calendar_dates_not_datelines", "month_or_day_word_not_a_date",
                  "month_or_day_substring_artifacts")


def device_key_pattern():
    """S1-07: the exact device-class keys (read at run time), longest first, whole-identifier boundaries."""
    inv = json.loads(INVENTORY.read_text(encoding="utf-8"))
    keys = [k for k in inv["formulae"] if "_" in k]
    for k in TOP_LEVEL_KEYS:
        if k not in inv:
            raise SystemExit(f"ngram7: device key {k} missing from {INVENTORY.name}")
        keys.append(k)
    keys = sorted(set(keys), key=lambda k: (-len(k), k))
    pat = re.compile(r"(?<![A-Za-z0-9_])(?:" + "|".join(re.escape(k) for k in keys) + r")(?![A-Za-z0-9_])")
    return pat, len(keys)


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
                # Jer v0 run: 43-row false RED from combine-added provenance)
                # patch prov_tools_p2 (2026-08-18, corpus-run finding, same
                # class as p1): unit_type + parent_collection are mandated
                # structural enums/range-strings, not authored prose — their
                # fixed values ("single_proverb", "C2 Dan.1.1-...") tokenize
                # into shared frames across hundreds of rows. confidence is a
                # 1-token enum, excluded for the same reason.
                # patch eccl_tools_p4 (2026-08-19, rows_v1 rev-round finding,
                # same class as p2): wj_or_red_letter_considered carries the
                # MANDATED fixed 6-token sentence ("not applicable in the OT
                # substrate") on every row — it concatenates into the next
                # string field and crossed the gate once phase-1 repairs made
                # 12 rows' following-field openings uniform. review_status is
                # a mandated 1-token enum, excluded on the same ground. Fixed
                # mandated field VALUES are not authored prose.
                # patch isa_tools_i4 (2026-08-26, combined-corpus run, same
                # class as p2/p4): book + model_id carry the MANDATED fixed
                # values "Jer" / "M8_fable" on every row (the Jer run; Dan rows carry "Dan" and are excluded the same way) — they chained into
                # the next field's common opener ("jer m fable this unit
                # opens at", 19 rows) at 225-row scale. Fixed mandated field
                # VALUES are not authored prose.
                if k not in ("boundary_evidence_refs", "span", "decision_id",
                             "chunk_id", "writer_part", "writer_decision_id",
                             "writer_attempt_id", "attempt_id", "routing_used",
                             "unit_type", "parent_collection", "confidence",
                             "wj_or_red_letter_considered", "review_status",
                             "book", "model_id"):
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
    full_ids = "--full-ids" in sys.argv   # 2026-09-06 opt-in: list EVERY row id per offending gram (CWO-1 order building)
    web, _ = load_verse_maps()
    webtext = norm_english(" ".join(d["text"] for d in web.values())).lower()
    web_tokens = re.findall(r"[a-z]+", webtext)
    web_7grams = {" ".join(web_tokens[i:i + 7]) for i in range(len(web_tokens) - 6)}

    keys_re, n_keys = device_key_pattern()
    no_strip = "--no-key-strip" in sys.argv   # regression/equality fixture only; the gate always strips
    grams: dict[str, set[str]] = {}
    n = 0
    for f in args:
        for row in rows_from(Path(f)):
            if not isinstance(row, dict):
                continue
            rid = row.get("decision_id") or f"{Path(f).name}#{n}"
            n += 1
            s = prose(row)
            segments = [s] if no_strip else keys_re.split(s)   # S1-07: a removed key is a segment break
            for seg in segments:
                seg = HEB_RUN.sub(" ", seg)
                seg = re.sub(r"“[^”]*”", " ", seg)
                seg = REF_TOKENS.sub(" ", seg)          # rev-round: citation apparatus
                toks = re.findall(r"[a-z]+", norm_english(seg).lower())
                for i in range(len(toks) - 6):
                    g = " ".join(toks[i:i + 7])
                    if g in web_7grams:
                        continue
                    grams.setdefault(g, set()).add(rid)
    offenders = sorted(((g, sorted(ids)) for g, ids in grams.items() if len(ids) >= gate),
                       key=lambda x: -len(x[1]))
    worst = sorted(((len(ids), g) for g, ids in grams.items()), reverse=True)[:5]
    if "--dump-grams" in sys.argv:   # fixture support: every gram with its row set
        print(json.dumps({g: sorted(ids) for g, ids in grams.items()}, ensure_ascii=False))
        return 0
    print(json.dumps({"rows": n, "gate": gate, "device_keys_stripped": 0 if no_strip else n_keys,
                      "offending_7grams": [{"gram": g, "rows": len(ids), "row_ids": (ids if full_ids else ids[:15])}
                                           for g, ids in offenders],
                      "worst_reuse": [{"rows": c, "gram": g} for c, g in worst],
                      "status": "GREEN" if not offenders else "RED"},
                     ensure_ascii=False, indent=1))
    return 1 if offenders else 0


if __name__ == "__main__":
    raise SystemExit(main())
