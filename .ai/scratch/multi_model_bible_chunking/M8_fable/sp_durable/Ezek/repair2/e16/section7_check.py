#!/usr/bin/env python3
"""#e16 rule R-5: the orchestrator's SECTION-7 CHECK for every conditional grade move, with the section-7 text it checked.

#e16's docket rule (confcal_docket.how_read): "'MOVE_CONDITIONAL' = apply unless the pinned strategy's section 7 names the
span (or a region containing it) as a held question or directs low/medium_low for it; the orchestrator records the
section-7 text checked (rule R-5)." For P03-012 and P09-011 the condition is narrower: "unless the strategy names 17:19 /
39:25 as a cut site by verse" - "a named cut, not a held question or region".

Each decision below quotes the exact section-7 text (asserted present in the pinned strategy by substring) that decides it.
Applied literally: a region named as a held question BLOCKS the move whatever direction the move takes.

usage: python section7_check.py
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
STRAT = EZ / "book_strategy_Ezek.md"
R16 = EZ / "author" / "e16" / "ruling_e16.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
text = STRAT.read_text(encoding="utf-8")
s7 = text[text.index("## §7 Expected low-confidence regions"):text.index("## §8 Register")]
E02 = "whole-chapter spans sit at medium_low/low + frontier flag + cap disclosure"
DEC = {
    "P03-001": ("BLOCKED", [E02, "(chs 15, 19, 27, 31, 34 and the\n36:1-15 half-chapter are the candidates)"], "whole chapter 15, directed medium_low/low"),
    "P03-009": ("BLOCKED", ["16:59 (messenger + covenant turn); whether 16:59-63 is `salvation_oracle`\n  or the allegory's close"], "the span is a named held question"),
    "P03-012": ("APPLIED", ["17: 17:1-10 / 17:11-21 / 17:22-24 as one, two or three rows"], "17:19 is not named as a cut site by verse; it sits inside a held question only"),
    "P06-002": ("BLOCKED", ["25: four short OAN (Ammon 2-7 with TWO\n  recognition closes at 25:5 and 25:7; Moab 8-11; Edom 12-14; Philistia 15-17)"], "the ch-25 tiling is a named held question"),
    "P06-003": ("BLOCKED", ["Edom 12-14"], "the ch-25 tiling is a named held question"),
    "P06-004": ("BLOCKED", ["Philistia 15-17) — four rows of 3-6\n  verses, or two, or one 17-verse row"], "the ch-25 tiling is a named held question"),
    "P07-004": ("BLOCKED", ["30:1-19 undated with four messenger paragraphs (30:2, 30:10,\n  30:13) inside"], "a region containing the span is named"),
    "P07-009": ("BLOCKED", ["30:1-19 undated with four messenger paragraphs"], "a region containing the span is named"),
    "P07-006": ("BLOCKED", ["31 one cedar allegory under a dateline (unit type 5 or 7)", E02], "named, and a whole-chapter candidate directed medium_low/low"),
    "P08-007": ("BLOCKED", ["**35:1-36:15** one word-event unit across the\n  chapter break"], "a region containing the span is named"),
    "P09-011": ("APPLIED", ["39:25-29 is the Gog unit's coda or the P7 close"], "39:25 appears only inside a held question, not as a named cut site"),
    "P01-001": ("BLOCKED", ["1:1-3 — two datelines in two systems"], "the chs 1-3 region is flagged and the span's head is a named held question"),
    "P01-012": ("BLOCKED", ["7:1-4 / 7:5-27 (pe at 7:4;"], "the ch-7 tiling is a named held question"),
    "P01-013": ("BLOCKED", ["7:1-4 / 7:5-27 (pe at 7:4;"], "a region containing the span is named"),
    "P01-014": ("BLOCKED", ["7:1-4 / 7:5-27 (pe at 7:4;"], "a region containing the span is named"),
    "P02-006": ("BLOCKED", ["Whether ch 10's wheel description (10:9-17, echoing ch 1) is a row or\n  texture."], "the span is a named held question"),
    "P02-018": ("APPLIED", [], "section 7 names nothing in chapter 13 (its short-disputation bullet names 12:21-25 / 12:26-28 only)"),
    "P03-020": ("BLOCKED", ["19: one qinah row (never\n  split;", E02], "named, and a whole-chapter candidate directed medium_low/low"),
    "P08-015": ("BLOCKED", ["34 as one unit with internal messenger paragraphs (34:7-10, 34:11-16, 34:17-19,\n  34:20-31) — the cap disclosure or a cut at 34:17"], "a region containing the span is named"),
    "P09-002": ("BLOCKED", ["37:15-28 two-sticks sign-act\n  with the salvation burden 37:21-28"], "the span is named in the expected low-confidence list"),
    "P10-013": ("BLOCKED", ["43:1-12 glory return +\n  torah of the house"], "a region containing the span is named"),
}
r16 = json.loads(R16.read_text(encoding="utf-8-sig"))
cond = {g["row"]: g for g in r16["grade_moves"] if "condition" in g}
if set(cond) != set(DEC):
    raise SystemExit("REFUSED: conditional moves %s != decided rows %s" % (sorted(cond), sorted(DEC)))
records = []
for rid, (verdict, quotes, why) in sorted(DEC.items()):
    for q in quotes:
        if q not in s7:
            raise SystemExit("REFUSED: quoted section-7 text not found verbatim for %s: %r" % (rid, q[:60]))
    g = cond[rid]
    records.append({"row": rid, "move": "%s -> %s" % (g["from"], g["to"]), "condition": g["condition"], "verdict": verdict,
                    "section7_text_checked": quotes, "why": why})
out = {"schema": "ezek_e16_section7_check.v1", "rule": "#e16 R-5 (confcal_docket.how_read)", "strategy": {"file": "Ezek/book_strategy_Ezek.md", "sha256": sha(STRAT)},
       "ruling": {"file": "Ezek/author/e16/ruling_e16.json", "sha256": sha(R16)}, "reading": "literal: a named region or held question blocks the move in either direction",
       "applied": [x["row"] for x in records if x["verdict"] == "APPLIED"], "blocked": [x["row"] for x in records if x["verdict"] == "BLOCKED"],
       "records": records, "tier": "the quoted text is EXTRACTED (asserted present verbatim); whether a quoted passage 'names the span' is the orchestrator's reading under R-5"}
p = HERE / "section7_check.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"applied": out["applied"], "blocked": len(out["blocked"]), "sha256": sha(p)}, indent=1))
