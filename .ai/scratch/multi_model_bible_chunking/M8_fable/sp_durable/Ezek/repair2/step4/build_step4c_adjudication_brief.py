#!/usr/bin/env python3
"""Generate the REPAIR-2 step-4c Fable ADJUDICATION brief, once both blind lanes have landed durably.

Written through a file writer, not patched from the step-3 builder by shell substitution: that route mangled the
Windows path separators in its own replacement anchors and refused (the anchor check caught it before any write).
"""
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
SP = EZ.parent
DELIV = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
             r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step4c_adjudication")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

PINS = [
    ("Ezek\\repair\\rows_v7_cwo24.jsonl", "the live rows"),
    ("Ezek\\repair2\\step4\\step4c_slices.v1.json", "per row: span, prose, refs, owed items; clause 6 v2 verbatim"),
    ("Ezek\\repair2\\step4\\step4c_worklist.v1.json", "the worklist and the gate's scope"),
    ("Ezek\\repair2\\step4\\STEP4C_AUTHOR_BRIEF.md", "the brief both lanes held: clause 6 v2 and one worked example per token"),
    ("Ezek\\author\\repair2_step4c\\lane_a\\proposal.json", "blind lane A - proposal"),
    ("Ezek\\author\\repair2_step4c\\lane_a\\discharge.json", "blind lane A - per-item discharge"),
    ("Ezek\\author\\repair2_step4c\\lane_b\\proposal.json", "blind lane B - proposal"),
    ("Ezek\\author\\repair2_step4c\\lane_b\\discharge.json", "blind lane B - per-item discharge"),
    ("Ezek\\repair2\\step4\\check_candidate_v4.py", "YOUR GATE (v4)"),
    ("Ezek\\repair2\\step3\\check_candidate_v3_1.py", "imported by the gate"),
    ("Ezek\\repair2\\step3\\check_candidate_v3.py", "imported by the gate"),
    ("Ezek\\repair2\\step2_reconciliation\\check_candidate_v2.py", "imported by the gate"),
    ("Ezek\\repair2\\suite_delta.py", "imported by the gate"),
    ("Ezek\\tools\\run_validator_suite.py", "run by the gate, with the hard role_tokens member"),
    ("Ezek\\tools\\check_role_tokens.py", "verifies every face qualifier and seam pair"),
    ("Ezek\\tools\\role_tokens_phase.json", "the member's pinned phase"),
    ("Ezek\\tools\\check_register.py", "imported by the gate"),
    ("Ezek\\tools\\check_refs_mirror.py", "imported by the gate"),
    ("Ezek\\tools\\ezek_lib.py", "imported by the gate"),
    ("Ezek\\verse_inventory.json", "per-chapter verse counts, WEB face"),
    ("Ezek\\tools\\verse_map_web.json", "the English version by verse"),
    ("Ezek\\Ezek_oshb.txt", "the Hebrew witness (WLC/OSHB)"),
    ("Ezek\\pmarks_Ezek.json", "marks, K/Q, paseq, notes (single witness)"),
    ("Ezek\\ezek_device_inventory.v2.json", "the device census"),
    ("Ezek\\web_mt_offset_map.json", "the WEB/MT map"),
    ("Ezek\\ezek_controlling_agent_ruling_e15.v1.json", "the ruling whose clause 6 v2 is being installed"),
]
table = ["| input | sha256 | what it is |", "|---|---|---|"]
pins = []
for rel, what in PINS:
    p = SP / rel
    if not p.is_file():
        raise SystemExit("REFUSED: pinned input missing - land both lanes durably first: %s" % rel)
    table.append("| `SP\\%s` | `%s` | %s |" % (rel, sha(p), what))
    pins.append("| `SP\\%s` | `%s` |" % (rel, sha(p)))

B = r"""# REPAIR-2 STEP 4c - ADJUDICATION OF TWO BLIND VOCABULARY LANES (Fable)

Attempt `ezek_repair2_step4c_adjudication_a1`, execution `ezek_repair2_step4c_adjudication_a1#e1`. You are the
controlling adjudicator (OW-13: Fable adjudicates). Two blind Opus lanes answered the same 103 owed items on 64 rows
of the clause 6 v2 installation; you produce ONE proposal the orchestrator applies.

## What you decide, recorded in adjudication.json

1. Per item (S4-nnn): DISCHARGED (with the entry you adopt), NO_DEFECT (with evidence) or STOP (with evidence).
2. SEAM PAIRS: where the lanes name different seam pairs for a rival, read the row's rejected alternative and the
   bytes and decide which cut the row actually weighs; where both name the same pair but different qualifiers, the
   rule decides (:near on the rival's candidate onset verse, :far on the verse behind it). A seam pair neither lane can
   support from the row is a STOP.
3. TOKENS: for a disputed token, apply the three decided cases - content a rationale rests on is a WARRANT; an
   inventoried device the boundary does not rest on is DISCLOSURE-device, never ANCHOR; a device the census does not
   record is never DISCLOSURE-device (ANCHOR, or WARRANT-absence / DISCLOSURE-absence for a true absence, with the
   census verified EMPTY at the verse).
4. ROUTED: anything beyond this step - to #e16, the second Fable review of the flagged regions, or step 5 - listed
   with its reason.

## Where the lanes diverge - stated as the orchestrator found it, not as a preference

The lanes' statuses disagree on 20 items; read both discharge files, not this summary, before deciding.

1. **FORWARD-MERGE RIVALS - a class question.** S4-009, 012, 014, 017, 019, 026, 027, 028, 029, 030, 031, 060, 070,
   074, 076, 077, 078, and the qualifier part of S4-085: a WARRANT-rival whose rejected alternative keeps the row's
   onset and extends the row forward, with the entry on the verse after the row's last verse. Lane A qualified them
   with the seam the merge would dissolve on :near and labels that convention INFERRED. Lane B stopped: it holds the
   clause's rival :near ("the candidate onset verse for a rival") gives no truthful face there, cites #e15's
   own_seam_faces and the ruling's one worked merge rival (17.10/17.11), and names three class options with the exact
   entry under each. Decide it here ONLY if clause 6 v2 and #e15 as written decide it. If deciding needs a meaning the
   clause does not give, it is a vocabulary ruling: route it to #e16 with both readings and every affected entry,
   leave those rivals unqualified, and record each item as STOP with the routing. That the member's phase flip then
   waits for #e16 is not a reason to decide either way - quality and completion are the objective, budget a limit.
2. **S4-090 (P02-018).** Lane A: NO_DEFECT - the row's own device_notes answers the implication. Lane B: STOP - the
   implication stands, and every repair re-tokenises a pre-wave descriptive entry, which clause 6 v2's retro-
   qualification clause bars; it needs an exception ruling. P02-018 is already on the #e16 confidence-calibration list.
3. **S4-091 (P05-008).** Lane A: NO_DEFECT - uneven not false, and the order names no re-gloss. Lane B: DISCHARGED -
   one device_notes phrase evened with the rejected-alternative field. Decide whether the item's order reaches that
   field; if it does not, the prose pass owns it.
4. **RE-FACES NO ITEM ORDERED.** Lane A moved seven entries from web: to oshb: under the face rule (15.2, 16.2, 16.8,
   24.9, 24.25, 29.6, 29.8); Lane B five (15.2, 16.2, 24.9, 24.25, 29.6). "Change only what an owed item names" and
   the face rule both bind; decide per entry, and say which rule governed.
5. **ZONE SEAM PAIRS** are written in WEB numbering by both lanes; the role_tokens member skips zone entries, so the
   offset-map form check is the only verification. Say so in what_i_could_not_verify if you adopt them.
6. **NOTED, NOT YOURS TO REPAIR HERE:** SRA prose in P01-009, P02-003 and P03-007 uses near/far in the older before/
   after sense (the prose pass owns it); the universals triage member stops reading an annotation once a qualifier is
   present, so triage counts can fall with no claim changing (a member defect, already routed).

## Rules for the proposal (the lanes' brief is pinned and binds you identically)

Change only what an owed item names; no grade, span, identity or signals changes; face qualifiers only on WARRANT-
onset/close/rival; MT-borne devices on the oshb: face and English quotations on the web: face; in the zone (MT 21:1-5
= WEB 20:45-49) every entry is written on BOTH faces; annotations one to six words (seven when a rival's first word is
its seam pair); DEF-A4-ARGUED mirroring kept; "single-witness" on any mark, paseq or puncta mention; never hand-type
Hebrew - SLICED from the witness or the live row; double curly quotes and a web: reference for five or more WEB words
(A6-b); C2-amended - unsourced means absent from BOTH pinned inputs; a mark is recorded on the verse it FOLLOWS; the
register rule - a row is a scholar-facing record; no 7-gram in more than a handful of rows, at least 4 distinct
formulations.

## Pinned inputs

%(table)s

Pin rows for the pre-launch check:

%(pins)s

## The gate - clean verdict, and the completion measure driven to what the rows honestly allow

`python -B <SP>\Ezek\repair2\step4\check_candidate_v4.py %(deliv)s\proposal.json --work %(deliv)s\gate_work`

It checks form and introduced flags, runs the WHOLE pinned suite including the hard role_tokens member (which
verifies every face qualifier and seam pair and fails loud), and reports the warrants still unqualified on your
candidate. Every warrant left unqualified must be a recorded STOP.

## Outputs - write early, rewrite at every stage (E-29), digest after the final write

1. `%(deliv)s\proposal.json` - only changed fields; refs as FULL lists.
2. `%(deliv)s\adjudication.json` - per item the decision; per disputed seam pair or token the reading taken and why;
   top-level `gate` with the completion measure, `routed`, `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. Escalate
rather than write: any seam move, any grade you believe wrong, a pinned input that contradicts itself, a digest that
differs from the table.
""" % {"table": "\n".join(table), "pins": "\n".join(pins), "deliv": str(DELIV)}
out = HERE / "STEP4C_ADJUDICATION_BRIEF.md"
out.write_text(B, encoding="utf-8", newline="\n")
DELIV.mkdir(parents=True, exist_ok=True)
print("brief:", out, "sha256:", sha(out))
