#!/usr/bin/env python3
"""Phase-0 toolkit smoke test for Prov (orchestrator only; artifacts removed
after). Two clean rows must pass every validator; one deliberately-bad row
must be caught on EVERY planted defect class. Hebrew is byte-spliced from
verse_map_oshb.json (never hand-typed); English is spliced from
verse_map_web.json."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
oshb = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
pm = json.loads((TOOLS.parent / "pmarks_Prov.json").read_text(encoding="utf-8"))

heb_1_2 = oshb["Prov.1.2"]["text"]                   # full pointed verse
heb_3_2 = oshb["Prov.3.2"]["text"]                   # full pointed verse
web_1_1 = re.sub(r"\[fn [^\]]*\]", " ", web["Prov.1.1"]["text"]).strip()
web_24_20 = re.sub(r"\[fn [^\]]*\]", " ", web["Prov.24.20"]["text"]).strip()
web_3_7 = re.sub(r"\[fn [^\]]*\]", " ", web["Prov.3.7"]["text"]).strip()

# preconditions for CLEAN rows (fail loudly if the data moves)
assert pm["marks"].get("Prov.1.7") == ["PE"], "smoke precondition: PE at 1:7"
assert pm["marks"].get("Prov.24.22") == ["SAMEKH"], "smoke precondition: SAMEKH at 24:22"
for k in ("Prov.1.1", "Prov.1.2", "Prov.24.20", "Prov.24.23"):
    assert not pm["kq"].get(k), f"smoke precondition: {k} must be K/Q-free"
assert not pm["marks"].get("Prov.3.9"), "smoke precondition: no mark at 3:9 (bad row)"
assert pm["marks"].get("Prov.3.4") == ["PE"], "smoke precondition: PE at 3:4 (bad row absence arm)"
assert not pm["kq"].get("Prov.3.3"), "smoke precondition: 3:3 K/Q-free (bad row)"
assert not pm["paseq"].get("Prov.3.3"), "smoke precondition: 3:3 paseq-free (bad row)"

rows = [
    # clean row A: header seam, PE at 1:7 disclosed, identity dual-cite,
    # byte-spliced Hebrew bound to its cited ref, proper X-X span
    {
        "decision_id": "SMOKE-A",
        "span": "Prov.1.1-Prov.1.7",
        "boundary_evidence_refs": [
            "web:Prov.1.1 = oshb:Prov.1.1",
            "oshb:Prov.1.2",
            "oshb:Prov.1.7 (petuchah, single-witness)",
        ],
        "boundary_reason": ("The book title opens the unit: “" + web_1_1 + "” "
                            "(web:Prov.1.1). The purpose clause runs " + heb_1_2 +
                            " (oshb:Prov.1.2); a petuchah closes the unit at "
                            "oshb:Prov.1.7 (single-witness)."),
        "rejected_alternative": "A cut after web:Prov.1.6 was rejected; the fear-of-Yahweh motto at web:Prov.1.7 caps the prologue.",
    },
    # clean row B: the wise-appendix seam — SAMEKH at 24:22 disclosed
    {
        "decision_id": "SMOKE-B",
        "span": "Prov.24.20-Prov.24.22",
        "boundary_evidence_refs": [
            "web:Prov.24.20 = oshb:Prov.24.20",
            "oshb:Prov.24.22 (setumah/samekh, single-witness)",
            "web:Prov.24.23 = oshb:Prov.24.23",
        ],
        "boundary_reason": ("The admonition closes: “" + web_24_20 + "” "
                            "(web:Prov.24.20). A setumah (samekh, single-witness) "
                            "stands at oshb:Prov.24.22, the last verse before the "
                            "second wise-sayings header."),
        "rejected_alternative": "Extending through web:Prov.24.23 was rejected; the new header opens a fresh collection there.",
    },
    # bad row: every planted defect class, one row
    {
        "decision_id": "SMOKE-BAD",
        "span": "Prov.3.5",                                 # (1) not X-X form
        "boundary_evidence_refs": [
            "web:Prov.3.5 = oshb:Prov.3.6",                 # (2) identity dual-cite wrong
            "oshb:Prov.3.2 (selah)",                        # (4) selah fabrication in Prov
            "oshb:Prov.3.3 (paseq)",                        # (5) no paseq at 3:3 + no disclosure
            "web:Prov.2.1-Prov.2.99",                       # (6) range END out of range
            "oshb:Prov.3.3 (qere)",                         # (7) false K/Q claim
            "LXX Prov 2:1",                                 # (8) cross-tradition in refs
            "web:Prov.5.0",                                 # (14) zero-verse pseudo-ref invalid
            "oshb:Prov.3.9 (petuchah, single-witness)",     # (3) mark claim at markless verse
        ],
        "boundary_reason": ("The book's only length-of-days promise — no other "  # (11) universal, no digit
                            "chapter does this. Verse 7 confirms the arc, and "    # (10) unmirrored bare verse
                            "Prov.4.2 echoes it. The quoted line " + heb_3_2 +     # (9) Hebrew bound to WRONG ref
                            " (oshb:Prov.3.5) proves it. Prov.3.2 is in Aramaic "  # (12) Aramaic label
                            "here, and there is no petuchah anywhere in this "     # (13) false absence claim (PE at 3:4 front seam)
                            "span."),
        "rejected_alternative": "“" + web_3_7 + "” (web:Prov.3.4)",  # misquote: 3:7's text, wrong ref
    },
]

out = TOOLS / "_smoke_rows.jsonl"
out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows),
               encoding="utf-8")
proc = subprocess.run([sys.executable, str(TOOLS / "run_validator_suite.py"), str(out)],
                      capture_output=True, text=True, encoding="utf-8")
print(proc.stdout)
report = json.loads(out.with_suffix(".jsonl.validator_report.json").read_text(encoding="utf-8"))

expected = {
    "citation_sweep": ["span not in full X-X form", "dual-cite arithmetic wrong",
                       "claims petuchah but the marks inventory", "claims selah",
                       "claims paseq", "single-witness", "range END out of range",
                       "ketiv/qere", "cross-tradition", "does not collate",
                       "always invalid"],
    "mark_symmetry": ["selah_claim_in_prov", "paragraph_mark_claim",
                      "false_mark_absence_claim"],
    "refs_mirror": ["Prov.4.2", "Prov.3.7"],
    "universals": ["only"],
    "language_zones": ["aramaic_label"],
    "web_quotes": ["Prov.3.4"],
}
blob = {k: json.dumps(report.get(k, {}), ensure_ascii=False) for k in expected}
missed = [(k, pat) for k, pats in expected.items() for pat in pats
          if pat not in blob[k]]
clean_hit = []
for k in ("citation_sweep", "mark_symmetry", "refs_mirror", "universals",
          "language_zones", "web_quotes"):
    # word-boundary match — "SMOKE-B" must not match "SMOKE-BAD"
    if re.search(r"SMOKE-[AB]\b", blob[k]):
        clean_hit.append(k)
print(json.dumps({"planted_defects_missed": missed,
                  "clean_rows_flagged_by": clean_hit,
                  "verdict": "PASS" if not missed and not clean_hit else "FAIL"},
                 ensure_ascii=False, indent=1))
