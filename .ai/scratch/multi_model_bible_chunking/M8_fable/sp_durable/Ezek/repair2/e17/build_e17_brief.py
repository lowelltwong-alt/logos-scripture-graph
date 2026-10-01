#!/usr/bin/env python3
"""#e17: the controlling agent's ruling on the OW-6b(b) second review - packet (computed) and brief.

The two blind Fable reviewers escalated seam moves (which only the controlling agent may order), disagreed with some of
#e16's grades, and found claims to repair. The packet sets their escalations and grade findings side by side by row, marks
where both reviewers agree, and carries #e16's own decisions on the same rows. #e17 decides every seam question once,
issues exact orders (span/identity changes as re-tiling orders with the new rows' spans), and settles each grade.

usage: python build_e17_brief.py
"""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
SP = EZ.parent
DELIV = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
             r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_e17_out")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
A = EZ / "author" / "second_review"
ra = json.loads((A / "lane_a" / "review.json").read_text(encoding="utf-8-sig"))
rb = json.loads((A / "lane_b" / "review.json").read_text(encoding="utf-8-sig"))
r16 = json.loads((EZ / "author" / "e16" / "ruling_e16.json").read_text(encoding="utf-8-sig"))
PID = re.compile(r"P\d\d-\d\d\d")


def rows_of(x):
    return sorted(set(PID.findall(json.dumps(x, ensure_ascii=False))))


def trim(o, n=1200):
    s = json.dumps(o, ensure_ascii=False)
    return o if len(s) <= n else s[:n] + " ...[trimmed; full text in the review]"


by_row = {}
for lane, rv in (("A", ra), ("B", rb)):
    for e in rv.get("escalations") or []:
        for rid in rows_of(e):
            by_row.setdefault(rid, {"A": {"escalations": [], "grade": []}, "B": {"escalations": [], "grade": []}})[lane]["escalations"].append(trim(e))
    for g in rv.get("grade_findings") or []:
        for rid in rows_of(g):
            by_row.setdefault(rid, {"A": {"escalations": [], "grade": []}, "B": {"escalations": [], "grade": []}})[lane]["grade"].append(trim(g, 600))
e16_moves = {g["row"]: g for g in r16["grade_moves"]}
packet = {"schema": "ezek_e17_packet.v1",
          "rows": {rid: dict(v, both_reviewers_raised=bool(v["A"]["escalations"] or v["A"]["grade"]) and bool(v["B"]["escalations"] or v["B"]["grade"]),
                             e16_grade_move=e16_moves.get(rid)) for rid, v in sorted(by_row.items())},
          "cross_row_patterns": {"A": trim(ra.get("cross_row_patterns"), 4000), "B": trim(rb.get("cross_row_patterns"), 4000)}}
pk = HERE / "e17_packet.v1.json"
pk.write_text(json.dumps(packet, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
PINS = [(EZ / "repair" / "rows_v7_cwo24.jsonl", "the live rows (#e16's grade moves and mechanical orders are NOT yet applied)"),
        (pk, "THE PACKET: both reviewers' escalations and grade findings side by side by row, with #e16's move on each row"),
        (A / "lane_a" / "review.json", "second review, blind lane A, in full"), (A / "lane_b" / "review.json", "second review, blind lane B, in full"),
        (EZ / "author" / "e16" / "ruling_e16.json", "#e16 - your previous ruling"),
        (EZ / "repair2" / "e16" / "section7_check.v1.json", "the orchestrator's section-7 check of #e16's conditional moves (R-5)"),
        (EZ / "ezek_device_inventory.v3.json", "the device census v3 (said_to_me_in_vision, colophons, vision returns)"),
        (EZ / "book_strategy_Ezek.md", "the division plan v1 (section 7 holds these regions)"),
        (EZ / "Ezek_oshb.txt", "the Hebrew witness (WLC/OSHB)"), (EZ / "pmarks_Ezek.json", "marks, K/Q, paseq, notes (single witness)"),
        (EZ / "tools" / "verse_map_web.json", "the English version by verse"), (EZ / "web_mt_offset_map.json", "the WEB/MT map"),
        (EZ / "verse_inventory.json", "per-chapter verse counts, WEB face")]
table, pins = ["| input | sha256 | what it is |", "|---|---|---|"], []
for p, what in PINS:
    if not Path(p).is_file():
        raise SystemExit("REFUSED: pinned input missing %s" % p)
    rel = "SP\\" + str(Path(p).resolve().relative_to(SP))
    table.append("| `%s` | `%s` | %s |" % (rel, sha(p), what))
    pins.append("| `%s` | `%s` |" % (rel, sha(p)))
both = [r for r, v in packet["rows"].items() if v["both_reviewers_raised"]]
B = r"""# CONTROLLING-AGENT RULING #e17 - THE SECOND REVIEW'S SEAM AND GRADE QUESTIONS (Fable)

Attempt `ezek_controlling_agent_ruling_e17_a1`, execution `ezek_controlling_agent_ruling_e17_a1#e1`. You are Ezekiel's
controlling agent (OW-6b). Two blind Fable reviewers read the flagged regions after #e16 and escalated SEAM MOVES, which only
you may order, plus grade disagreements with #e16 and claim repairs. %(n)d rows are raised; both reviewers raised %(nb)d of
them. You write ONE ruling file; you mutate no row.

## Decide, once each

1. **Every seam question** (the chapter-18 tiling; P08-011's fold-back into 36:1-15; the two-verse rows P04-007 and
   P06-013 against the over-split guard; 16:44-50 | 16:51-58; 17:11-21; the ch-20 sequence 20:27-44; 43:1-12; 44:1-3 |
   44:4-31; and any other a reviewer raised): MOVE or HOLD, with the faces measured on the witness. A MOVE is a RE-TILING
   ORDER: the rows it retires (by id), the new rows' spans (WEB face, as the corpus writes spans), each new row's grade
   with its ground, and which live row's prose each new row starts from. Keep the book's tiling exact: every verse in
   exactly one row.
2. **Every grade disagreement** between a reviewer and #e16: KEEP #e16's move or SUPERSEDE it, with the faces.
3. **Claim repairs** the reviewers measured (false face claims, apparatus gaps such as undisclosed K/Q and paseq in
   chs 44-48): order each exactly for the final remediation batch, or NO_ACTION with reason.
4. **Your own earlier text** the reviewers corrected (e.g. #e16's 44:15 'mid-verse', R-7's 'every near face', R-6's
   fixture width): record each correction.

## Orders - the executable form

`retiling_orders`: [{"retire": [row ids], "new_rows": [{"span", "grade", "ground", "prose_from"}], "faces"}].
`grade_decisions`: [{"row", "e16_move", "decision": "KEEP|SUPERSEDE", "to", "faces"}].
`orders_for_final_remediation`: [{"row", "field", "order", "kind": "mechanical|author", "tier"}] - a mechanical order names
exact before/after strings. `corrections_to_earlier_rulings`, `escalations_to_owner` (only what you cannot decide).

## Rules that bind every order

The register rule: a row is a scholar-facing record - no rule ids, ruling numbers, file or record names, repair narration.
OW-18 tiers on claims. "single-witness" on any mark, paseq or puncta mention; a mark is recorded on the verse it FOLLOWS;
never hand-type Hebrew - SLICE it from the witness; five or more WEB words take double curly quotes and a web: reference
(A6-b exempts a counted device's fixed rendering); C2-amended - unsourced means absent from BOTH pinned inputs;
DEF-A4-ARGUED - every argued citation mirrored by a refs entry with a ROLE token, a verified face qualifier and seam pair
(':merge' for a merge rival, #e16 C1); the zone - MT 21:1-5 = WEB 20:45-49 - on BOTH faces; rotation - no 7-gram in more
than a handful of rows, at least 4 distinct formulations.

## Budget

The owner has set a hard token line for Ezekiel and it is close. Rule from the packet and the two reviews; measure only
what a decision rests on; do not re-review rows no reviewer raised.

## Pinned inputs

%(table)s

Pin rows for the pre-launch check:

%(pins)s

## Output - write early, rewrite at every stage (E-29), digest after the final write

`%(deliv)s\ruling_e17.json` with the sections named above plus `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. A digest that
differs from the table: record both and stop.
""" % {"n": len(packet["rows"]), "nb": len(both), "table": "\n".join(table), "pins": "\n".join(pins), "deliv": str(DELIV)}
out = HERE / "E17_RULING_BRIEF.md"
out.write_text(B, encoding="utf-8", newline="\n")
DELIV.mkdir(parents=True, exist_ok=True)
print(json.dumps({"rows_raised": len(packet["rows"]), "both_raised": len(both), "packet_bytes": pk.stat().st_size,
                  "brief_sha256": sha(out), "packet_sha256": sha(pk)}, indent=1))
