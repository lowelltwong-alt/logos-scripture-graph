#!/usr/bin/env python3
"""Generate REPAIR-2 step-4c author SLICES and BRIEF (two blind Opus lanes; vocabulary). Pin table computed from disk."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
SP = EZ.parent
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step4c")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

rows = {r["decision_id"]: r for r in (json.loads(l) for l in (EZ / "repair" / "rows_v7_cwo24.jsonl")
                                      .read_text(encoding="utf-8").splitlines() if l.strip())}
wl = json.loads((HERE / "step4c_worklist.v1.json").read_text(encoding="utf-8"))
r15 = json.loads((EZ / "ezek_controlling_agent_ruling_e15.v1.json").read_text(encoding="utf-8"))
slices = {}
for it in wl["items"]:
    if it["status"] == "DONE":
        continue
    rid = it["row"]
    s = slices.setdefault(rid, {"row": rid, "span": rows[rid].get("span"), "confidence": rows[rid].get("confidence"),
                                "live": {f: rows[rid].get(f) for f in ("boundary_rationale", "strongest_rejected_alternative",
                                                                       "device_notes", "boundary_evidence_refs")},
                                "owed_items": []})
    s["owed_items"].append(it)
slices_p = HERE / "step4c_slices.v1.json"
slices_p.write_text(json.dumps({"schema": "ezek_repair2_step4c_slices.v1", "rows_sha256": wl["rows_sha256"],
                                "rows": len(slices), "items": sum(len(s["owed_items"]) for s in slices.values()),
                                "clause_6_v2_verbatim": r15["q5_role_vocabulary"]["DEF_A4_ARGUED_clause_6_v2"],
                                "slices": slices}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")

PINS = [
    ("Ezek\\repair\\rows_v7_cwo24.jsonl", "the live rows after step 4a"),
    ("Ezek\\repair2\\step4\\step4c_slices.v1.json", "per row: span, prose, refs, owed items; clause 6 v2 verbatim"),
    ("Ezek\\repair2\\step4\\step4c_worklist.v1.json", "the worklist and the gate's scope"),
    ("Ezek\\repair2\\step4\\check_candidate_v4.py", "YOUR GATE - form, delta checks, the whole suite, and the completion measure"),
    ("Ezek\\repair2\\step3\\check_candidate_v3_1.py", "imported by the gate"),
    ("Ezek\\repair2\\step3\\check_candidate_v3.py", "imported by the gate"),
    ("Ezek\\repair2\\step2_reconciliation\\check_candidate_v2.py", "imported by the gate"),
    ("Ezek\\repair2\\suite_delta.py", "imported by the gate"),
    ("Ezek\\tools\\run_validator_suite.py", "run by the gate - now with the hard role_tokens member"),
    ("Ezek\\tools\\check_role_tokens.py", "the member that verifies every face qualifier and seam pair"),
    ("Ezek\\tools\\role_tokens_phase.json", "the member's pinned phase"),
    ("Ezek\\tools\\check_register.py", "imported by the gate"),
    ("Ezek\\tools\\check_refs_mirror.py", "imported by the gate"),
    ("Ezek\\tools\\ezek_lib.py", "imported by the gate"),
    ("Ezek\\verse_inventory.json", "per-chapter verse counts on the WEB face (for the verse across a chapter seam)"),
    ("Ezek\\tools\\verse_map_web.json", "the English version by verse"),
    ("Ezek\\Ezek_oshb.txt", "the Hebrew witness (WLC/OSHB)"),
    ("Ezek\\pmarks_Ezek.json", "marks, K/Q, paseq, notes (single witness)"),
    ("Ezek\\ezek_device_inventory.v2.json", "the device census"),
    ("Ezek\\web_mt_offset_map.json", "the WEB/MT map"),
    ("Ezek\\ezek_controlling_agent_ruling_e15.v1.json", "the ruling whose clause 6 v2 you install"),
]
table = ["| input | sha256 | what it is |", "|---|---|---|"]
pins = []
for rel, what in PINS:
    p = SP / rel
    if not p.is_file():
        raise SystemExit("REFUSED: pinned input missing %s" % rel)
    table.append("| `SP\\%s` | `%s` | %s |" % (rel, sha(p), what))
    pins.append("| `SP\\%s` | `%s` |" % (rel, sha(p)))

B = r"""# REPAIR-2 STEP 4c - THE AUTHOR VOCABULARY BATCH. Author brief (two blind lanes)

You are ONE OF TWO BLIND LANES; a Fable adjudicator reconciles you with the other lane, whose work you never see.

## What this step installs

#e15 Q5 amended the argued-citation definition ("clause 6 v2", carried verbatim in the slices): the layer that
records warrants must be able to say WHICH FACE of a seam a warrant sits on, because the confidence scale is about
faces. A mechanical sweep has already given 124 onset and close warrants their derived face qualifier. What is left
needs a reader: %(items)d owed items on %(rows)d rows - 75 WARRANT-rival tokens that need a SEAM PAIR and a face
qualifier, 5 onset/close warrants the geometry could not qualify (three in the renumbering zone, two interior
without a device word), two ANCHOR absences to re-tokenise, two device entries the census does not support, and the
re-face and re-gloss items the rulings and the earlier adjudications carried to this step.

## Clause 6 v2, and one worked example per token

A **face qualifier** is ':near' (the seam verse INSIDE the unit the seam bounds - the row's first verse for its onset,
its last verse for its close, the candidate onset verse for a rival), ':far' (the adjacent verse ACROSS the seam), or
':interior' (an in-span verse a warrant rests on that is neither - for onset and close only when the annotation names
the device). The hard role_tokens member DERIVES the face for onset and close from verse and span and FAILS LOUD on a
mismatch; for a rival it checks the SEAM PAIR.

- `oshb:Ezek.33.10 [WARRANT-onset:near] ve'attah re-address opens the unit` - the row's first verse
- `oshb:Ezek.33.20 [WARRANT-onset:far] pe-marked close behind the dateline` - the verse before the first verse
- `oshb:Ezek.24.24 [WARRANT-close:interior] sign formula partner of the close` - in span, device named
- `oshb:Ezek.33.12 [WARRANT-rival:near] 33.11/33.12 ve'attah same audience unlicensed` - the annotation's FIRST token is
  the seam pair (two adjacent verses, dotted); the rival's candidate onset verse is :near, the verse behind it :far
- `oshb:Ezek.40.38 [WARRANT-absence] no formula mark K/Q or paseq here` - the boundary RESTS on the absence
- `oshb:Ezek.41.9 [DISCLOSURE-absence] census records no stroke here` - recorded, the boundary does not rest on it
- `oshb:Ezek.8.14 [DISCLOSURE-mark] samekh on this verse single-witness` - a mark (recorded on the verse it FOLLOWS)
- `oshb:Ezek.33.13 [DISCLOSURE-kq] ketiv and qere recorded here`, `[DISCLOSURE-paseq]`, `[DISCLOSURE-note]` likewise
- `oshb:Ezek.21.14 [DISCLOSURE-device] in-span messenger short form` - an inventoried device the boundary does not rest on
- `web:Ezek.11.13 [QUOTE] Pelatiah's death and the cry` - an English quotation, on the web: face
- `oshb:Ezek.37.9 [ANCHOR] the four winds content only` - a content statement the boundary does not rest on

**The three cases an earlier lane found divergent, decided:** (1) a verse with neither device nor mark that the
rationale RESTS on is a WARRANT with :near or :far and its ground named - content is a warrant when the rationale
rests on it; (2) an inventoried device the boundary does NOT rest on is DISCLOSURE-device, never ANCHOR; (3) a device
the census does NOT record is never DISCLOSURE-device - it is ANCHOR, or WARRANT-absence / DISCLOSURE-absence for a
true absence.

## Rules for what you may write

- **Change only what an owed item names.** Qualify, re-token, re-face or re-gloss the named entries. A prose sentence
  may change only where an item's order names it (a re-gloss that the rationale must match). No grade, span, identity
  or signals changes. A false only-ground is a STOP, never a substitution.
- **Read the seam pair off the row.** A rival's seam is where the rejected alternative would cut - read it from the
  strongest_rejected_alternative field and the rationale, and check it against the bytes. If the row does not let you
  determine it, STOP with the evidence.
- **Faces:** MT-borne devices and formula memberships on the oshb: face; English quotations on the web: face. **The
  zone:** MT 21:1-5 = WEB 20:45-49 and MT 21:6-37 = WEB 21:1-32 - an entry touching it is written on BOTH faces,
  `web:... = oshb:...`, mapped by the offset map, never by arithmetic.
- **Annotations** are one to six words (seven when a rival's first word is its seam pair). DEF-A4-ARGUED: every argued
  citation stays mirrored by an entry carrying a ROLE token. A mark, paseq or puncta mention carries "single-witness".
- **Hebrew:** never hand-type Hebrew - SLICED from `Ezek_oshb.txt` or the live row. **English:** five or more WEB words
  take double curly quotes and a web: reference (A6-b exempts a named formula rendering). **Categorical claims:**
  C2-amended - unsourced means absent from BOTH pinned inputs. **The register rule:** a row is a scholar-facing record -
  no rule ids, ruling numbers, file or tool names, digests, review or wave talk, repair narration. **Rotation:** no
  7-gram in more than a handful of rows, at least 4 distinct formulations for repeated statements.

## Pinned inputs

%(table)s

Pin rows for the pre-launch check:

%(pins)s

## Your gate - run it until the verdict is clean, and drive the completion measure to zero

`python -B <SP>\Ezek\repair2\step4\check_candidate_v4.py <your dir>\proposal.json --work <your ABSOLUTE dir>\gate_work`

It checks entry form and the flags your proposal introduces, runs the WHOLE pinned suite - including the hard
role_tokens member, which verifies every qualifier and seam pair - and then reports the warrants still unqualified on
your candidate. Use an ABSOLUTE --work path. Run no validator any other way.

## Outputs - write early and rewrite at every stage (E-29); digest after the final write

1. `proposal.json` - `{"<row>": {"<field>": <full new value>}}`, only changed fields; refs as FULL lists.
2. `discharge.json` - per item id (S4-nnn): `status` DISCHARGED | NO_DEFECT | STOP, `what_i_wrote` or `evidence`,
   `facts_reproduced` with tiers; top-level `gate` (the final verdict and the completion measure),
   `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. Escalate
rather than write: any seam move, any grade you believe wrong, a pinned input that contradicts itself, a digest that
differs from the table.
""" % {"items": sum(len(s["owed_items"]) for s in slices.values()), "rows": len(slices), "table": "\n".join(table),
       "pins": "\n".join(pins)}
out = HERE / "STEP4C_AUTHOR_BRIEF.md"
out.write_text(B, encoding="utf-8", newline="\n")
for lane in ("lane_a", "lane_b"):
    (SCR / lane).mkdir(parents=True, exist_ok=True)
print(json.dumps({"brief_sha256": sha(out), "slices_sha256": sha(slices_p), "rows": len(slices),
                  "items": sum(len(s["owed_items"]) for s in slices.values())}, indent=1))
