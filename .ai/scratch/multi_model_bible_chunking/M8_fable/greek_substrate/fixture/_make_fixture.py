#!/usr/bin/env python3
"""Generate the small validation fixture from the staged RP and SBLGNT bytes (never from Swete).

rows.good.jsonl  every row should pass every suite member.
rows.bad.jsonl   each row carries "_expect": the member and defect it must trigger (adversarial cases).
Quotes are short (<= 4 words) excerpts; RP is public domain (Unlicense) and SBLGNT is CC BY 4.0 with the
attribution recorded in ../STAGING_RECEIPT.v1.json. No Swete wording is ever written here (owner terms).

Usage: python _make_fixture.py
"""
from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import greek_lib as g


def w(sp, b, c, v, a, n):
    return " ".join(g.verse(sp, b, c, v).split()[a:a + n])


def main() -> int:
    good = [
        {"decision_id": "G-3JN-1", "span": "web:3John.1.1-3John.1.14",
         "text": "Letter opening and close; compare rp:3John.1.1 and sbl:3John.1.15.",
         "quotes": [{"ref": "rp:3John.1.1", "greek": w("rp", "3John", 1, 1, 0, 3), "tier": "byte"},
                    {"ref": "sbl:3John.1.15", "greek": w("sbl", "3John", 1, 15, 0, 2), "tier": "byte"}],
         "verse_existence_disclosure": ["3John.1.15"]},
        {"decision_id": "G-PHM-1", "span": "web:Phlm.1.1-Phlm.1.25", "text": "Whole letter.",
         "quotes": [{"ref": "sbl:Phlm.1.1-1.2", "greek": w("sbl", "Phlm", 1, 1, 0, 2) + " … " +
                     w("sbl", "Phlm", 1, 2, 0, 2), "tier": "byte"},
                    {"ref": "rp:Phlm.1.25", "greek": g.strip_accents(w("rp", "Phlm", 1, 25, 0, 3)),
                     "tier": "accent_stripped"}],
         "verse_existence_disclosure": []},
        {"decision_id": "G-JHN-PA", "span": "web:John.7.53-John.8.11", "text": "Pericope; rp:John.8.3.",
         "quotes": [{"ref": "rp:John.8.3", "greek": w("rp", "John", 8, 3, 0, 3), "tier": "byte"}],
         "verse_existence_disclosure": ["John.7.53", "John.8.1", "John.8.2", "John.8.3", "John.8.4", "John.8.5",
                                        "John.8.6", "John.8.7", "John.8.9", "John.8.10", "John.8.11"]},
        {"decision_id": "G-ACT-8", "span": "web:Acts.8.36-Acts.8.38", "text": "Eunuch; verse 37 disclosed.",
         "quotes": [], "verse_existence_disclosure": ["Acts.8.37"]},
        {"decision_id": "G-ACT-24", "span": "web:Acts.24.6-Acts.24.8", "text": "Tertullus.",
         "quotes": [{"ref": "rp:Acts.24.7", "greek": w("rp", "Acts", 24, 7, 0, 3), "tier": "byte"}],
         "verse_existence_disclosure": ["Acts.24.6", "Acts.24.7", "Acts.24.8"]},
    ]
    nfd = unicodedata.normalize("NFD", w("rp", "3John", 1, 1, 0, 3))
    bad = [
        {"decision_id": "B-REF", "span": "web:3John.1.1-3John.1.15", "text": "range end not in WEB",
         "quotes": [], "verse_existence_disclosure": ["3John.1.15"],
         "_expect": ["citation_sweep", "span_end_absent"]},
        {"decision_id": "B-RPREF", "span": "web:3John.1.14", "text": "see rp:3John.1.15",
         "quotes": [], "verse_existence_disclosure": ["3John.1.15"],
         "_expect": ["citation_sweep", "ref_absent_in_witness"]},
        {"decision_id": "B-OVERCLAIM", "span": "web:Phlm.1.25", "text": "overclaimed tier",
         "quotes": [{"ref": "rp:Phlm.1.25", "greek": g.strip_accents(w("rp", "Phlm", 1, 25, 0, 3)), "tier": "byte"}],
         "verse_existence_disclosure": [], "_expect": ["citation_sweep", "tier_overclaim"]},
        {"decision_id": "B-NODISC", "span": "web:Acts.8.36-Acts.8.38", "text": "no disclosure",
         "quotes": [], "verse_existence_disclosure": [], "_expect": ["citation_sweep", "missing_disclosure"]},
        {"decision_id": "B-NFD", "span": "web:3John.1.1", "text": "decomposed quote",
         "quotes": [{"ref": "rp:3John.1.1", "greek": nfd, "tier": "nfc"}], "verse_existence_disclosure": [],
         "_expect": ["normalize_dryrun", "fixed"]},
        {"decision_id": "B-WRONGVERSE", "span": "web:3John.1.2", "text": "quote from another verse",
         "quotes": [{"ref": "rp:3John.1.2", "greek": w("rp", "3John", 1, 1, 0, 3), "tier": "byte"}],
         "verse_existence_disclosure": [], "_expect": ["citation_sweep", "quote_not_at_ref"]},
    ]
    for name, rows in (("rows.good.jsonl", good), ("rows.bad.jsonl", bad)):
        (HERE / name).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    print(json.dumps({"status": "GREEN", "good": len(good), "bad": len(bad)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
