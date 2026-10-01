#!/usr/bin/env python3
"""Build the #e16 PACKET (compact, from the records) and the #e16 controlling-agent BRIEF.

#e15 close clearance item 2: "#e16: the CONF-CAL audit list (grade/limb disagreements) and the lakhen-turn messenger
class, decided once". Since then two more class questions were routed to #e16 (the step-4c adjudication's forward-merge
rival face; the step-7 readers' merge-rival pairing convention), the CONF-CAL member's own coverage was questioned by
the readers, and the step-7 re-read produced 92 questions and per-row CONF-CAL answers. The packet carries each item
verbatim or trimmed with its source path, so the ruling agent rules from the record, not from a summary.

usage: python build_e16_brief.py
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
SP = EZ.parent
DELIV = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
             r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_e16_out")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
CC = EZ / "repair2" / "step7" / "confcal_audit.v2.json"
REC = EZ / "repair2" / "step7" / "step7_reconciled.v1.json"
DOCK = HERE / "e16_docket.v1.json"
ADJ4C = EZ / "author" / "repair2_step4c" / "adjudication" / "adjudication.json"
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"


def trim(o, n=600):
    s = json.dumps(o, ensure_ascii=False)
    return o if len(s) <= n else s[:n] + " ...[trimmed; full text in the source]"


cc, rec, dock, adj4c = (json.loads(p.read_text(encoding="utf-8")) for p in (CC, REC, DOCK, ADJ4C))
for name, d in (("CONF-CAL audit", cc), ):
    if d["inputs"]["rows_sha256"] != sha(ROWS):
        raise SystemExit("REFUSED: the %s was built on other rows" % name)
queue = {json.loads(l)["id"]: json.loads(l) for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()}
fm_items = {k: v for k, v in adj4c["items"].items() if "FORWARD-MERGE" in json.dumps(v, ensure_ascii=False)}
cross = {s: v["cross_row_patterns"] for s, v in rec["strides"].items()}
packet = {
    "schema": "ezek_e16_packet.v1", "rows_sha256": sha(ROWS),
    "classes": {
        "C1_forward_merge_rival_face": {"source": "Ezek/author/repair2_step4c/adjudication/adjudication.json class_decision + items",
                                        "class_decision_verbatim": adj4c["class_decision"],
                                        "affected_items": {k: trim(v, 900) for k, v in fm_items.items()}},
        "C2_merge_rival_pairing_convention": {"source": "Ezek/repair2/step7/step7_reconciled.v1.json strides.*.cross_row_patterns (both readers of each stride)",
                                              "note": "readers found merge rivals tokenised four ways in step 4c; the ruling's worked P03-012 17.10/17.11 form; backward merges paired at the absorbing unit's onset (P01-013 7.4/7.5, P06-011 27.36/28.1, P08-005 33.22/33.23, P08-011 35.15/36.1); seam pairs the prose never argues (P02-006 9.11/10.1, P03-003 15.8/16.1, P06-002 24.27/25.1)",
                                              "cross_row_patterns_verbatim": cross},
        "C3_lakhen_turn_messenger_onsets": {"source": "Ezek/ezek_controlling_agent_queue_e13.v1.jsonl E13-97", "verbatim": queue["E13-97"]},
        "C4_confcal_member_coverage": {"source": "step-7 readers (cross_row_patterns) and the member's own tiers",
                                       "member_tiers": cc["tiers"],
                                       "reader_observations": "the view does not treat 'he said to me' inside a vision, or interior transport verses, as licensed onsets; it misses interior rivals the rejected-alternative prose weighs when no rival token exists (P02-019, P06-007, P08-002, P11-001) - see cross_row_patterns"},
    },
    "confcal_docket": [{"row": x["row"], "span_mt": x["span_mt"], "grade": x["grade"], "derived_range": x["derived_range"],
                        "state": x["state"], "disagreeing_faces": x["disagreeing_faces"],
                        "reader_answers": trim(rec["confcal_answers"].get(x["row"]), 1600)} for x in cc["rows_for_e16"]],
    "confcal_rows_within_reader_range": [{"row": x["row"], "grade": x["grade"], "reader_needed": x["reader_needed"],
                                          "reader_answers": trim(rec["confcal_answers"].get(x["row"]), 900)} for x in cc["rows_needing_a_reader"]],
    "step7_questions": [{"row": q["row"], "item": q["item"], "A": trim(q["A"], 500), "B": trim(q["B"], 500)} for q in rec["questions"]],
    "routed_entries": [{"source": e["source"], "path": e["path"], "rows_named": e["rows_named"], "entry": trim(e["entry"], 900)} for e in dock["entries"]],
}
pk = HERE / "e16_packet.v1.json"
pk.write_text(json.dumps(packet, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")

PINS = [
    (ROWS, "the live rows"),
    (pk, "THE PACKET: the four class questions, the CONF-CAL docket with both step-7 readers' answers, the 92 step-7 questions, the 57 routed entries"),
    (CC, "the CONF-CAL audit member v2's full output (faces, ranges, bases)"),
    (REC, "the step-7 reconciliation in full (both readers' evidence per row and item)"),
    (DOCK, "the #e16 docket collector's full output"),
    (ADJ4C, "the step-4c adjudication (the forward-merge class and its entries)"),
    (Q, "the e13 queue (E13-97 lakhen table; E13-106..109 on REPAIR-2 steps 4c-7)"),
    (EZ / "ezek_controlling_agent_ruling_e15.v1.json", "#e15 - Q2's unified rival definitions and CONF-CAL high limb, Q5 clause 6 v2"),
    (EZ / "ezek_controlling_agent_ruling_e14.v1.json", "#e14 - Q2's mid-verse refinement"),
    (EZ / "ezek_controlling_agent_ruling_e13.v1.json", "#e13 - CONF-CAL and CUT-RULE as ruled"),
    (EZ / "ezek_controlling_agent_ruling_e12.v1.json", "#e12 - the A/C/D class rulings"),
    (EZ / "AUTHOR_WAVE_BRIEF.v1.md", "CONF-CAL, CUT-RULE and precedence as briefed (its 13.2 phrase list is superseded by #e15 Q9(a))"),
    (EZ / "ezek_device_inventory.v2.json", "the device census"),
    (EZ / "Ezek_oshb.txt", "the Hebrew witness (WLC/OSHB)"),
    (EZ / "pmarks_Ezek.json", "marks, K/Q, paseq, notes (single witness)"),
    (EZ / "tools" / "verse_map_web.json", "the English version by verse"),
    (EZ / "web_mt_offset_map.json", "the WEB/MT map"),
]
table, pins = ["| input | sha256 | what it is |", "|---|---|---|"], []
for p, what in PINS:
    if not Path(p).is_file():
        raise SystemExit("REFUSED: pinned input missing %s" % p)
    rel = "SP\\" + str(Path(p).resolve().relative_to(SP))
    table.append("| `%s` | `%s` | %s |" % (rel, sha(p), what))
    pins.append("| `%s` | `%s` |" % (rel, sha(p)))

B = r"""# CONTROLLING-AGENT RULING #e16 - EZEKIEL (Fable)

Attempt `ezek_controlling_agent_ruling_e16_a1`, execution `ezek_controlling_agent_ruling_e16_a1#e1`. Under OW-6b you are
the CONTROLLING agent for Ezekiel: boundary decisions, grade decisions, class rulings and escalations are your calls.
You write ONE ruling file; you mutate no row. The orchestrator executes your orders - mechanically where an order is
deterministic, through two blind author lanes and a Fable adjudication otherwise - in the final remediation batch.

## What #e16 decides (each in its own section of ruling_e16.json)

1. **C3 - the lakhen-turn messenger onsets** (17:19, 20:30, 39:25; #e15 Q2 held the class "decided once"). All three are
   their row's FIRST verse, so the ruling reaches three shipped seams, not only grades. Decide whether such a turn, with
   no addressee change and no verse-final close-role formula before it, is a licensed onset; state what follows for each
   of the three rows (seam stands and its ground / grade, or the escalation a seam move requires - you may not move a
   seam silently; a seam move is an escalation with its evidence).
2. **C1 - the forward-merge rival face** (17 entries plus S4-085's qualifier; the step-4c adjudicator routed both
   readings and every entry). Decide the grammar - one of the named options or a better one you state - so that every
   WARRANT carries a verified face; order the exact entry for each affected row; say whether the role_tokens member needs
   a new arm (a tool order) and the condition under which its phase flips from pre to post.
3. **C2 - the merge-rival pairing convention** the readers found applied four ways; rule one convention and order each
   row that departs from it.
4. **C4 - the CONF-CAL member's coverage**: whether "he said to me" inside a vision and an interior transport verse are
   licensed onsets for the scale; whether an interior rival weighed in prose with no rival token must be tokenised; any
   tool order for the member.
5. **THE CONF-CAL DOCKET**: for each of the 46 rows, and each within-reader-range row whose readers' answers settle it,
   KEEP the grade with its stated ground, or MOVE it with the ground and the faces named. The readers' answers are
   readings, not rulings; a grade the evidence does not support moves; no grade moves without a ground. The scale's
   rule stands: no grade is raised unasked - you are asked here.
6. **THE 92 STEP-7 QUESTIONS AND THE ROUTED ENTRIES**: answer each that needs a ruling; mark the rest as author work
   for the remediation batch with the exact order, or NO_ACTION with the reason.

## Orders - the form the orchestrator can execute

`orders_for_final_remediation`: a list of `{"row", "field", "order", "kind": "mechanical" | "author", "tier",
"source_item"}`. A mechanical order names an exact before/after string or an exact token change; an author order
names the claim to correct and the evidence. `grade_moves`: `{"row", "from", "to", "ground", "faces"}`. `tool_orders`:
member changes with the fixture that must fail before and pass after. `escalations`: anything that needs a seam move
or the owner.

## Rules that bind every order you issue (the authors will be gated on them)

The register rule: a row is a scholar-facing record - no rule ids, ruling numbers, file or record names, repair
narration; state substance, name the witness and its layers. OW-18 tiers on every claim. "single-witness" on any mark,
paseq or puncta mention; a mark is recorded on the verse it FOLLOWS; never hand-type Hebrew - SLICE it from the witness;
five or more WEB words take double curly quotes and a web: reference (A6-b exempts a counted device's fixed rendering);
C2-amended - unsourced means absent from BOTH pinned inputs; DEF-A4-ARGUED - every argued citation mirrored by a refs
entry with a ROLE token whose face qualifier and seam pair are verified; the zone - MT 21:1-5 = WEB 20:45-49 - on BOTH
faces; rotation - no 7-gram in more than a handful of rows, at least 4 distinct formulations.

## Pinned inputs

%(table)s

Pin rows for the pre-launch check:

%(pins)s

## Output - write early, rewrite at every stage (E-29), digest after the final write

`%(deliv)s\ruling_e16.json` with sections `c1_forward_merge`, `c2_merge_pairing`, `c3_lakhen_turn`, `c4_confcal_member`,
`confcal_docket`, `questions_and_routed`, `orders_for_final_remediation`, `grade_moves`, `tool_orders`, `escalations`,
`role_tokens_phase_flip`, `what_i_could_not_verify`, `e19_selfreport`, `limit`. Every byte fact MEASURED over the pinned
inputs and labelled; every reading labelled as a reading.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. A digest that
differs from the table: record both and stop.
""" % {"table": "\n".join(table), "pins": "\n".join(pins), "deliv": str(DELIV)}
out = HERE / "E16_RULING_BRIEF.md"
out.write_text(B, encoding="utf-8", newline="\n")
DELIV.mkdir(parents=True, exist_ok=True)
print(json.dumps({"brief": str(out), "brief_sha256": sha(out), "packet_sha256": sha(pk), "packet_bytes": pk.stat().st_size,
                  "confcal_docket": len(packet["confcal_docket"]), "within_range": len(packet["confcal_rows_within_reader_range"]),
                  "questions": len(packet["step7_questions"]), "routed": len(packet["routed_entries"]),
                  "forward_merge_items": len(fm_items)}, indent=1))
