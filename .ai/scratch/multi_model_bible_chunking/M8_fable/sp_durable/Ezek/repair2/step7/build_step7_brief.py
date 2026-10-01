#!/usr/bin/env python3
"""Generate the REPAIR-2 step-7 SPOT RE-READ briefs: three strides, TWO blind lanes per stride (OW-19).

#e15 orders "a SPOT RE-READ at FULL coverage of every row REPAIR-2 touched, three lanes interleaved by stride as before".
OW-19 (2026-09-15) bans single-lane review, and three lanes by stride read each row ONCE. The two are reconciled by
keeping the three strides and giving each stride two blind lanes over the same slice: every row is read twice,
independently, and interleaving still separates a reader from any one author's contiguous stretch. Recorded as the
orchestrator's reading (INFERRED), for the controlling agent to overrule.

Each lane answers an eight-item checklist per row, including the CONF-CAL audit member's question for that row
(the face it names and the basis), so #e16 receives read answers rather than bare mechanical flags.

usage: python build_step7_brief.py
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
SP = EZ.parent
DELIV = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
             r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step7")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
CC = HERE / "confcal_audit.v2.json"
cc = json.loads(CC.read_text(encoding="utf-8"))
if cc["inputs"]["rows_sha256"] != sha(ROWS):
    raise SystemExit("REFUSED: the CONF-CAL audit was run on other rows; re-run confcal_audit_v2.py on the live rows first")
out = {}
for n in (1, 2, 3):
    sl_p = HERE / ("step7_spot_lane_%d.v1.json" % n)
    sl = json.loads(sl_p.read_text(encoding="utf-8"))
    if sl["rows_sha256"] != sha(ROWS):
        raise SystemExit("REFUSED: stride %d slices were built on other rows; rebuild them first" % n)
    PINS = [
        (ROWS, "the live rows"),
        (sl_p, "YOUR ROWS: before/after of every field REPAIR-2 changed, per-sweep orders as data, and the CONF-CAL view"),
        (CC, "the CONF-CAL audit member's full output (the view in your slices is taken from it)"),
        (EZ / "ezek_controlling_agent_ruling_e15.v1.json", "the ruling that ordered REPAIR-2 and this re-read"),
        (EZ / "ezek_controlling_agent_ruling_e12.v1.json", "A-class rulings (A6, A7, A9, A10, A16) and C2"),
        (EZ / "ezek_controlling_agent_ruling_e14.v1.json", "DEF-A4-ARGUED and the #e14 Q2 refinement"),
        (EZ / "repair2" / "step5" / "step5_rule_substance.v1.json", "the substance of every barred rule id, verbatim"),
        (EZ / "Ezek_oshb.txt", "the Hebrew witness (WLC/OSHB)"),
        (EZ / "pmarks_Ezek.json", "marks, K/Q, paseq, notes (single witness)"),
        (EZ / "ezek_device_inventory.v2.json", "the device census"),
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
    B = r"""# REPAIR-2 STEP 7 - SPOT RE-READ, STRIDE %(n)d (two blind lanes on this stride)

You are ONE OF TWO BLIND LANES reading the same %(rows)d rows; you never see the other lane. Every row here was changed
by REPAIR-2 (confidence moves, grounds, measured-false repairs, the vocabulary installation, the register prose pass,
the transport batch). You READ; you write nothing to any row. Your findings go to the controlling agent and #e16.

## For every row, answer all eight - each with a verdict (OK | DEFECT | QUESTION), the evidence and its tier

1. **orders_executed** - each order in the row's per-sweep orders: DISCHARGED exactly, PARTIAL, NOT DONE, or an
   UNORDERED change (a field changed that no order names). Read the order's CONTENT against the edit, not its existence.
2. **conclusion_changed** - did any repair re-decide the boundary (a new ground, a new rival held differently, a grade
   moved without an order)? A grade that follows a newly disclosed fact is not a re-decision; say which it is.
3. **claims_true** - every factual claim in a changed field, re-measured against the witness, the marks and the census:
   verses, counts, Hebrew bytes, mark direction (a mark is recorded on the verse it FOLLOWS), K/Q and paseq; every
   mark, paseq or puncta mention carries the literal "single-witness" disclosure.
4. **new_absolutes** - any categorical claim ("never", "only", "every", "no ... anywhere"): sourced, or unsourced -
   C2-amended: unsourced means absent from BOTH pinned inputs.
5. **quotations** - five or more consecutive WEB words carry double curly quotes, a web: reference and the WEB's exact
   bytes; a counted device's fixed rendering is exempt (A6-b).
6. **role_tokens** - DEF-A4-ARGUED: every argued citation mirrored by a refs entry with a ROLE token; each WARRANT's
   face qualifier and each rival's seam pair true to verse, span and the prose; MT-borne devices on oshb:, English on
   web:; in the zone (MT 21:1-5 = WEB 20:45-49) entries on BOTH faces.
7. **register_and_english** - the register rule: a row is a scholar-facing record - no rule ids, ruling numbers, file,
   tool, record, census, plan or key names, review or wave talk, repair narration; and every changed field READ IN FULL
   as English (a doubled article, colliding phrases, a dropped clause boundary, a sentence that no longer parses);
   and ROTATION across your rows - a repair batch that wrote the same sentence into many rows breaks the rule that no
   7-gram appears in more than a handful of rows and that a repeated statement has at least 4 distinct formulations;
   report any template you see in cross_row_patterns.
8. **confidence** - the grade against the CONF-CAL view in your slice. Where the view asks a question ("census absence
   on the near face 2:7"), ANSWER it from reading: name the licensed signal a reader finds on that face (a refrain, a
   discourse turn, a scene change, "he said to me") with its verse and tier, or confirm there is none. Never propose a
   new grade; state what the evidence on each face is. No grade is raised unasked.

## Pinned inputs

%(table)s

Pin rows for the pre-launch check:

%(pins)s

## Output - write early and rewrite at every stage (E-29); digest after the final write

`findings.json`: `per_row` {row: {the eight items}}, `findings_total_by_severity` (HIGH | MEDIUM | LOW over DEFECTs),
`cross_row_patterns`, `confcal_answers` {row: [{face, reading, verse, tier}]}, `what_i_could_not_verify`,
`e19_selfreport`, `limit`. Hebrew you quote is SLICED from the witness, never typed.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. A digest
that differs from the table: record both and stop.
""" % {"n": n, "rows": sl["rows"], "table": "\n".join(table), "pins": "\n".join(pins)}
    p = HERE / ("STEP7_SPOT_BRIEF_STRIDE%d.md" % n)
    p.write_text(B, encoding="utf-8", newline="\n")
    for lane in ("a", "b"):
        (DELIV / ("s%d_lane_%s" % (n, lane))).mkdir(parents=True, exist_ok=True)
    out[n] = {"brief": str(p), "sha256": sha(p), "rows": sl["rows"]}
print(json.dumps(out, indent=1))
