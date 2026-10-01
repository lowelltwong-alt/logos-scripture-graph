#!/usr/bin/env python3
"""Generate the REPAIR-2 step-3 Fable ADJUDICATION brief once both blind lanes have LANDED durably.

Run only after each lane's proposal.json and discharge.json are copied to Ezek/author/repair2_step3/lane_{a,b}/ and
receipted; the pin table binds those durable copies, so a brief can never pin a scratchpad file a clear would lose.

usage: python build_step3_adjudication_brief.py [--preview]
"""
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
SP = EZ.parent
DELIV = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
             r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step3_adjudication")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

PINS = [
    ("Ezek\\repair\\rows_v7_cwo24.jsonl", "the live rows"),
    ("Ezek\\repair2\\step3\\step3_slices.v1.json", "per row: live fields and every owed item with its measured fact"),
    ("Ezek\\repair2\\step3\\step3_worklist.v1.json", "the worklist and the gate's scope"),
    ("Ezek\\repair2\\step3\\distinct_checks_q10.v1.json", "the 13 reproduced facts"),
    ("Ezek\\author\\repair2_step3\\lane_a\\proposal.json", "blind lane A - proposal"),
    ("Ezek\\author\\repair2_step3\\lane_a\\discharge.json", "blind lane A - per-item discharge"),
    ("Ezek\\author\\repair2_step3\\lane_b\\proposal.json", "blind lane B - proposal"),
    ("Ezek\\author\\repair2_step3\\lane_b\\discharge.json", "blind lane B - per-item discharge"),
    ("Ezek\\repair2\\step3\\check_candidate_v3_1.py", "YOUR GATE (v3.1) - per-row checks as a delta against the live row, plus the whole pinned suite"),
    ("Ezek\\repair2\\step3\\check_candidate_v3.py", "imported by v3.1 (the gate both lanes ran)"),
    ("Ezek\\repair2\\step2_reconciliation\\check_candidate_v2.py", "imported by the gate"),
    ("Ezek\\repair2\\suite_delta.py", "imported by the gate"),
    ("Ezek\\tools\\run_validator_suite.py", "run by the gate"),
    ("Ezek\\tools\\check_register.py", "imported by the gate"),
    ("Ezek\\tools\\check_refs_mirror.py", "imported by the gate"),
    ("Ezek\\tools\\ezek_lib.py", "imported by the gate"),
    ("Ezek\\tools\\verse_map_web.json", "the English version by verse ('clean')"),
    ("Ezek\\Ezek_oshb.txt", "the Hebrew witness (WLC/OSHB)"),
    ("Ezek\\pmarks_Ezek.json", "marks, K/Q, paseq, notes (single witness)"),
    ("Ezek\\ezek_device_inventory.v2.json", "the device census"),
    ("Ezek\\web_mt_offset_map.json", "the WEB/MT map"),
    ("Ezek\\ezek_controlling_agent_ruling_e15.v1.json", "the controlling ruling"),
    ("Ezek\\repair2\\step3\\STEP3_AUTHOR_BRIEF.md", "the brief both lanes held"),
]
table = ["| input | sha256 | what it is |", "|---|---|---|"]
pins = []
for rel, what in PINS:
    p = SP / rel
    if not p.is_file():
        raise SystemExit("REFUSED: pinned input missing - land both lanes durably first: %s" % rel)
    table.append("| `SP\\%s` | `%s` | %s |" % (rel, sha(p), what))
    pins.append("| `SP\\%s` | `%s` |" % (rel, sha(p)))

B = r"""# REPAIR-2 STEP 3 - ADJUDICATION OF TWO BLIND AUTHOR LANES (Fable)

Attempt `ezek_repair2_step3_adjudication_a1`, execution `ezek_repair2_step3_adjudication_a1#e1`. You are the
controlling adjudicator for this step (OW-13: Fable adjudicates). Two blind Opus lanes answered the same 73 owed items
on 43 rows from the same slices. You see both, and you produce ONE proposal the orchestrator applies.

## The gate changed after the lanes ran - and why that matters for their STOPs

Both lanes ran gate v3, which had two defects the lanes found. (1) It refused edits to fields no item named, yet marked
a row unclean for register flags anywhere in it, so P02-003, P08-013 and P09-002 - which carry pre-existing flags in
untouched fields - could never be clean: lane A stopped eight items on it (S3-001, S3-065, S3-066, S3-067..S3-071) and
lane B left the rows out, putting their candidate text in its discharge record. (2) It treated the worklist's
field lists as binding, and four claims sit in a field the list did not name (lane A: S3-009, S3-010, S3-014, S3-016).
Your gate is v3.1: it judges only the flags a proposal INTRODUCES, and it scopes by row. So those twelve STOPs are not
evidence that the items cannot be done - DECIDE THEM ON THE MERITS, using both lanes' would-write text.

Lane A's two other escalations stand on their own: two quotation items name a verse outside their row (S3-024 names
41:26 on P10-005; S3-025 names 40:38 on P01-002) - read what the row actually quotes and decide; and two items touch a
grade's ground (S3-010, S3-029) - a removal that would leave a grade without its ground is a STOP, and a HIGH row's
register rewrites belong to step 5.

## What you decide, item by item, recorded in adjudication.json

1. For every item (S3-nnn): DISCHARGED (with the sentence or entry you adopt), NO_DEFECT (with evidence), or STOP
   (with evidence). Where the lanes agree on status and substance, say so; where they differ, decide on the bytes and
   say which reading you took and why.
2. A lane's claim that a fact reproduces is not proof: re-read the witness, the marks record, the census or the WEB
   verse map by exact path for every fact the adopted text asserts and the slice does not already carry as MEASURED.
   A false only-ground is a STOP, never a substitution.
3. Items routed beyond step 3 - to #e16, to the second Fable review of the flagged regions, or to step 4 - are listed
   under `routed`, each with its reason.

## Rules for what the proposal may say (identical to the lanes' brief, which is pinned)

- No grade, span or identity changes. Refs may be reworded or removed only where an owed item names the entry; a new or
  changed entry uses the vocabulary pinned today (one ROLE token, NO face qualifier - step 4 installs those, a one-to-
  six-word annotation, MT-borne devices on the oshb: face, quotations on the web: face, DEF-A4-ARGUED mirroring). In
  the zone (MT 21:1-5 = WEB 20:45-49) every entry is written on BOTH faces.
- observed_substrate_signals change only on P03-019 and P09-010, as their items name.
- A mark is recorded on the verse it FOLLOWS; any mention of a mark, paseq or puncta carries "single-witness".
- Never hand-type Hebrew: SLICED from the witness or the live row. Five or more WEB words take double curly quotes and
  a web: reference (A6-b exempts a formula rendering only where the row names the device). C2-amended: a claim that
  something is unsourced must be absent from BOTH pinned inputs.
- The register rule: row prose is a scholar-facing record - no rule identifiers, ruling numbers, file or tool names,
  digests, review or wave talk, repair narration. Rotation: no 7-gram in more than a handful of rows, at least 4 distinct formulations.

## Pinned inputs

%(table)s

Pin rows for the pre-launch check:

%(pins)s

## The gate - run until ALL_CLEAN

`python -B <SP>\Ezek\repair2\step3\check_candidate_v3_1.py %(deliv)s\proposal.json --work %(deliv)s\gate_work`

It runs per-row checks and the WHOLE pinned suite on the candidate; no hard member may gain a flag. It is a floor.

## Outputs - write early, rewrite at every stage (E-29), digest after the final write

1. `%(deliv)s\proposal.json` - `{"<row>": {"<field>": <full new value>}}`, only changed fields; refs and signals FULL.
2. `%(deliv)s\adjudication.json` - per item the decision above; per row the lane base or merge; top-level `gate`,
   `routed`, `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory. Never modify the corpus or a pinned file; never run git, write a receipt or touch a
registry. Escalate rather than write: any seam move, any grade you believe wrong, a pinned input that contradicts
itself, a digest that differs from the table.
""" % {"table": "\n".join(table), "pins": "\n".join(pins), "deliv": str(DELIV)}

if "--preview" in sys.argv:
    print(B[:2500])
    raise SystemExit(0)
out = HERE / "STEP3_ADJUDICATION_BRIEF.md"
out.write_text(B, encoding="utf-8", newline="\n")
DELIV.mkdir(parents=True, exist_ok=True)
print("brief:", out, "sha256:", sha(out))
