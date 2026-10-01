#!/usr/bin/env python3
"""Generate the DISTINCT FABLE CHECK brief for strategy v2 (#e15 close clearance item 4: 'distinct-checked (OW-10)').

The check is an audit of a landed candidate against enumerated obligations, not a second authoring lane: every collected
order's disposition verified at the v2 location it names, every unordered edit the author flagged accepted or reverted on
the witness, the unit lists compared with the live rows' spans, and the register and convention statements read. Verdict
fit_to_accept or not_fit, with an exact correction for every defect so the orchestrator can apply it by guarded edit.

usage: python build_strategy_v2_check_brief.py
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
SP = EZ.parent
DELIV = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
             r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_strategy_v2_check")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
A = EZ / "author" / "strategy_v2"
PINS = [
    (A / "book_strategy_Ezek.v2.md", "THE CANDIDATE you audit (strategy v2, landed, not yet accepted)"),
    (A / "strategy_v2_dispositions.json", "the author's disposition for every collected order, and the unordered edits it flags"),
    (HERE / "strategy_v2_orders.v2.json", "every collected order, verbatim with its location (44 entries)"),
    (EZ / "book_strategy_Ezek.md", "strategy v1"),
    (EZ / "repair" / "rows_v7_cwo24.jsonl", "the live rows (138): the tiling v2 must describe"),
    (EZ / "author" / "e17" / "ruling_e17.json", "#e17"),
    (EZ / "author" / "e16" / "ruling_e16.json", "#e16"),
    (EZ / "ezek_controlling_agent_ruling_e15.v1.json", "#e15"),
    (EZ / "ezek_controlling_agent_ruling_e14.v1.json", "#e14"),
    (EZ / "ezek_controlling_agent_ruling_e13.v1.json", "#e13"),
    (EZ / "ezek_controlling_agent_ruling_e12.v1.json", "#e12"),
    (EZ / "ezek_device_inventory.v3.json", "the device census v3"),
    (EZ / "ezek_device_inventory.v2.json", "the device census v2"),
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
B = r"""# EZEKIEL STRATEGY v2 - DISTINCT CHECK (Fable)

Attempt `ezek_strategy_v2_check_a1`, execution `ezek_strategy_v2_check_a1#e1`. An Opus author wrote the book strategy's
next version from 44 collected orders; the close clearance requires it distinct-checked before it is accepted. You audit
the landed candidate. You do not rewrite it.

## What you verify, recorded in strategy_v2_check.json

1. **Every disposition** (44): an APPLIED order is present and correct at the v2 location named; a CITES_ONLY entry
   really orders no change to the strategy (a ruling that only cites the plan as a ground); nothing ordered was dropped.
   Per entry: CONFIRMED or DEFECT with the evidence.
2. **The six unordered edits the author flagged** (29:9 mid-verse recognition; 30:6 in the 30:1-19 messenger paragraphs;
   the 45:18 calendar-date rule against the 45:18-25 row; the dual-written chapter 20-21 seams; shortened glosses; removed
   process labels): ACCEPT or REVERT each, measured on the witness where it states a fact about the text.
3. **The tiling**: every unit list v2 gives agrees with the live rows' spans (138 rows, every WEB verse once).
4. **The cut sites and devices**: named cut sites are presented as licensing, named on no device, or resting on a
   byte-false premise exactly as the cut-site licensing ruling (#e17 K1) classes them; the therefore-turn and the
   said-to-me / transport-in-vision rulings (#e16 C3, C4) agree with the device list.
5. **Register and conventions**: the register rule holds in v2's body (a scholar-facing record: no rule ids, file or tool
   names, digests or repair narration outside the "What changed" section); where v2 states the row conventions it states
   them as ruled: DEF-A4-ARGUED with a ROLE token, face qualifier and seam pair (':merge' for a merge rival);
   "single-witness" on marks, a mark recorded on the verse it FOLLOWS; never hand-type Hebrew (SLICED from the witness);
   five or more WEB words in double curly quotes with a web: reference (A6-b); C2-amended (absent from BOTH pinned
   inputs); the zone MT 21:1-5 = WEB 20:45-49 on BOTH faces; no 7-gram in more than a handful of rows, at least 4
   distinct formulations.

## Verdict

`fit_to_accept` only if no DEFECT stands; otherwise `not_fit`, and every DEFECT carries an EXACT correction: the v2 text
to find (unique) and the text to replace it with, so the orchestrator can apply it by guarded edit and re-verify.

## Budget

The owner's token line for this book is close. Verify each disposition at the location it names; measure on the witness
only what an unordered edit or a cut-site statement rests on.

## Pinned inputs

%(table)s

Pin rows for the pre-launch check:

%(pins)s

## Output - write early, rewrite at every stage (E-29), digest after the final write

`%(deliv)s\strategy_v2_check.json`: `verdict`, `dispositions` (44), `unordered_edits` (6), `tiling`, `cut_sites_and_devices`,
`register_and_conventions`, `defects` (each with its exact correction), `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus, the candidate or any pinned file; no git, receipts or registry;
never list, glob or search directories. A digest that differs from the table: record both and stop.
""" % {"table": "\n".join(table), "pins": "\n".join(pins), "deliv": str(DELIV)}
out = HERE / "STRATEGY_V2_CHECK_BRIEF.md"
out.write_text(B, encoding="utf-8", newline="\n")
DELIV.mkdir(parents=True, exist_ok=True)
print(json.dumps({"brief_sha256": sha(out)}, indent=1))
