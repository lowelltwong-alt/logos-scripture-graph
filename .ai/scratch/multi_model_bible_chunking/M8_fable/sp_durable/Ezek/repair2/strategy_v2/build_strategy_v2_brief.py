#!/usr/bin/env python3
"""Generate the STRATEGY v2 author brief (#e15 close clearance item 4; OW-10 distinct check follows as a separate Fable lane).

The author writes the book strategy's next version as a NEW file (v1 is never overwritten) and a disposition for every
collected order: APPLIED (with the v2 section it landed in), CITES_ONLY (a ruling cites the plan as a ground and orders no
change) or NOT_APPLIED (with the reason). The tiling v2 describes is measured from the live rows, not from memory.

usage: python build_strategy_v2_brief.py
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
SP = EZ.parent
DELIV = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
             r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_strategy_v2")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
ORD = HERE / "strategy_v2_orders.v2.json"
od = json.loads(ORD.read_text(encoding="utf-8"))
PINS = [
    (EZ / "book_strategy_Ezek.md", "strategy v1 - the text you revise (never modified)"),
    (ORD, "EVERY collected order for v2, verbatim with its location (%d phrase-matched + %d structural)" % (len(od["orders"]), len(od["structural_orders"]))),
    (EZ / "repair" / "rows_v7_cwo24.jsonl", "the live rows (138): the tiling v2 describes is read from their spans"),
    (EZ / "repair2" / "e17" / "retile_e17.manifest.json", "the re-tiling record (retired and new rows)"),
    (EZ / "author" / "e17" / "ruling_e17.json", "#e17"),
    (EZ / "author" / "e16" / "ruling_e16.json", "#e16"),
    (EZ / "ezek_controlling_agent_ruling_e15.v1.json", "#e15 (close clearance item 4 names v2's contents)"),
    (EZ / "ezek_controlling_agent_ruling_e14.v1.json", "#e14"),
    (EZ / "ezek_controlling_agent_ruling_e13.v1.json", "#e13"),
    (EZ / "ezek_controlling_agent_ruling_e12.v1.json", "#e12"),
    (EZ / "ezek_device_inventory.v3.json", "the device census v3 (additive over v2)"),
    (EZ / "ezek_device_inventory.v2.json", "the device census v2 (the transport class, 33 verses / 46 occurrences)"),
]
table, pins = ["| input | sha256 | what it is |", "|---|---|---|"], []
for p, what in PINS:
    if not Path(p).is_file():
        raise SystemExit("REFUSED: pinned input missing %s" % p)
    rel = "SP\\" + str(Path(p).resolve().relative_to(SP))
    table.append("| `%s` | `%s` | %s |" % (rel, sha(p), what))
    pins.append("| `%s` | `%s` |" % (rel, sha(p)))
B = r"""# EZEKIEL BOOK STRATEGY v2 - author brief (Opus)

Attempt `ezek_strategy_v2_author_a1`, execution `ezek_strategy_v2_author_a1#e1`. The controlling agent's close clearance
for Ezekiel owes "strategy v2 (CUT-RULE once; the transport predicate and 33; the Q2 unified rival definitions; the 33:20
tiers; the section-6/section-2b transport reconciliation; the ch-18 and other Track-D corrections already ordered) and the
inventory note, distinct-checked". Since that list was written, two further rulings re-tiled seven regions and ruled which
plan-named cut sites license an onset. You write v2; a distinct Fable check follows.

## What you write

1. `book_strategy_Ezek.v2.md` - strategy v1 revised, section structure kept, every collected order applied where it
   orders a change. The unit lists describe the book AS NOW TILED - read each span from the live rows; never from v1's
   lists or from memory. State CUT-RULE once. Name the transport class by its stated predicate and count. Present each
   named cut site as the ruling on cut-site licensing classes it (licensing; named on no device; premise byte-false).
   Put the device list in agreement with the therefore-turn ruling and the said-to-me/transport-in-vision ruling. Add a
   short "What changed from v1" section at the end: one line per change, each naming the order it executes.
2. `strategy_v2_dispositions.json` - for EVERY entry of the orders file (phrase-matched and structural, by index):
   `APPLIED` with the v2 section, `CITES_ONLY` where the ruling only cites the plan as a ground and orders no change, or
   `NOT_APPLIED` with the reason. No entry is left without a disposition. Also `what_i_could_not_verify`,
   `e19_selfreport`, `limit`, and the sha256 of both files after your final write.

## Rules

- v1 is never modified; v2 is a new file. Keep v1's register (a planning record for scholars and future agents): state
  substance and name the witness and its layers; a ruling may be named in the "What changed" section only.
- A claim about the witness is measured or quoted from a pinned input that already measured it; Hebrew is SLICED, never
  hand-typed; a mark is recorded on the verse it FOLLOWS and carries "single-witness".
- Where two orders conflict, the later ruling governs; record the conflict in the disposition.
- The register rule binds v2's body as it binds a scholar-facing record: no rule ids, file or tool names, digests or
  repair narration outside the "What changed" section.
- Where v2 states the conventions a row follows, it states them as the rulings now fix them: DEF-A4-ARGUED (every argued
  citation mirrored by a refs entry with a ROLE token; a warrant carries a face qualifier, a rival its seam pair first, a
  merge rival ':merge'); five or more WEB words in double curly quotes with a web: reference (A6-b exempts a counted
  device's fixed rendering); C2-amended (unsourced means absent from BOTH pinned inputs); the zone MT 21:1-5 = WEB
  20:45-49 written on BOTH faces; no 7-gram in more than a handful of rows, at least 4 distinct formulations for a
  repeated statement.

## Budget

The owner's token line for this book is close. Work from the orders file and v1; open a ruling only at the location an
entry names; measure only what an applied change rests on.

## Pinned inputs

%(table)s

Pin rows for the pre-launch check:

%(pins)s

## Outputs - write early, rewrite at every stage (E-29), digest after the final write

`%(deliv)s\book_strategy_Ezek.v2.md` and `%(deliv)s\strategy_v2_dispositions.json`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry; never list,
glob or search directories. A digest that differs from the table: record both and stop.
""" % {"table": "\n".join(table), "pins": "\n".join(pins), "deliv": str(DELIV)}
out = HERE / "STRATEGY_V2_AUTHOR_BRIEF.md"
out.write_text(B, encoding="utf-8", newline="\n")
DELIV.mkdir(parents=True, exist_ok=True)
print(json.dumps({"brief_sha256": sha(out), "orders_sha256": sha(ORD)}, indent=1))
