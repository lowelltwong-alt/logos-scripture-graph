#!/usr/bin/env python3
"""Generate the REPAIR-2 step-3 author SLICES and BRIEF (two blind Opus lanes). Pin table computed from disk.

usage: python build_step3_brief.py [--preview]
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
SP = EZ.parent
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step3")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

rows = {r["decision_id"]: r for r in (json.loads(l) for l in (EZ / "repair" / "rows_v7_cwo24.jsonl")
                                      .read_text(encoding="utf-8").splitlines() if l.strip())}
wl = json.loads((HERE / "step3_worklist.v1.json").read_text(encoding="utf-8"))
dc = {r["item"]: r for r in json.loads((HERE / "distinct_checks_q10.v1.json").read_text(encoding="utf-8"))["results"]}
l02 = json.loads((EZ / "author" / "author_wave_2026-09-16" / "ezek_l02_work_7b3f" / "ezek_author_l02_deliverable.json")
                 .read_text(encoding="utf-8"))
l02_esc = {e["row"]: e["what"] for e in l02.get("escalations", [])}

slices = {}
for it in wl["items"]:
    if it["status"] == "DISCHARGED":
        continue
    rid = it["row"]
    s = slices.setdefault(rid, {"row": rid, "span": rows[rid].get("span"), "confidence": rows[rid].get("confidence"),
                                "live": {f: rows[rid].get(f) for f in ("boundary_rationale", "strongest_rejected_alternative",
                                                                       "device_notes", "literature_type_guess",
                                                                       "boundary_evidence_refs", "observed_substrate_signals")},
                                "owed_items": []})
    item = dict(it)
    n = it["distinct_check"] or ""
    if n.startswith("Q10 dc "):
        k = int(n.split()[-1])
        item["measured_fact"] = {"claim": dc[k]["claim_under_test"], "measured": dc[k]["measured"],
                                 "verdict": dc[k]["verdict"], "tier": "MEASURED by a distinct check from pinned inputs"}
    if it["source"].startswith("L02") and rid in l02_esc:
        item["reviewer_escalation_verbatim"] = l02_esc[rid]
        item["tier_of_that_text"] = "REPORTED by an author lane - reproduce every fact from the witness before writing it"
    s["owed_items"].append(item)

SCR.mkdir(parents=True, exist_ok=True)
slices_p = HERE / "step3_slices.v1.json"
slices_p.write_text(json.dumps({"schema": "ezek_repair2_step3_slices.v1", "rows_sha256": wl["rows_sha256"],
                                "rows": len(slices), "items": sum(len(s["owed_items"]) for s in slices.values()),
                                "slices": slices}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")

PINS = [
    ("Ezek\\repair\\rows_v7_cwo24.jsonl", "the live rows after REPAIR-2 step 2"),
    ("Ezek\\repair2\\step3\\step3_slices.v1.json", "per row: live fields and every owed item, with its measured fact where one exists"),
    ("Ezek\\repair2\\step3\\step3_worklist.v1.json", "the worklist the slices come from, and the gate's scope"),
    ("Ezek\\repair2\\step3\\distinct_checks_q10.v1.json", "the 13 distinct checks (all reproduce)"),
    ("Ezek\\repair2\\step3\\check_candidate_v3.py", "YOUR GATE - per-row checks plus the WHOLE pinned suite on your candidate"),
    ("Ezek\\repair2\\step2_reconciliation\\check_candidate_v2.py", "imported by the gate"),
    ("Ezek\\repair2\\suite_delta.py", "imported by the gate"),
    ("Ezek\\tools\\run_validator_suite.py", "run by the gate"),
    ("Ezek\\tools\\check_register.py", "imported by the gate"),
    ("Ezek\\tools\\check_refs_mirror.py", "imported by the gate; ROLE_VOCABULARY is the vocabulary in force"),
    ("Ezek\\tools\\ezek_lib.py", "imported by the gate; web_to_mt and load_verse_maps"),
    ("Ezek\\tools\\verse_map_web.json", "the English version by verse (WEB): read the 'clean' field"),
    ("Ezek\\Ezek_oshb.txt", "the Hebrew witness (WLC/OSHB) - slice Hebrew from here"),
    ("Ezek\\pmarks_Ezek.json", "section marks, K/Q notes, paseq, other notes (single witness)"),
    ("Ezek\\ezek_device_inventory.v2.json", "the device census"),
    ("Ezek\\web_mt_offset_map.json", "the WEB/MT numbering map"),
    ("Ezek\\ezek_controlling_agent_ruling_e15.v1.json", "the ruling behind the Q10 items"),
    ("Ezek\\a4_extraction_gap.v1.json", "the source of the bare-decimal items"),
]
table = ["| input | sha256 | what it is |", "|---|---|---|"]
pins = []
for rel, what in PINS:
    p = SP / rel
    if not p.is_file():
        raise SystemExit("REFUSED: pinned input missing %s" % rel)
    table.append("| `SP\\%s` | `%s` | %s |" % (rel, sha(p), what))
    pins.append("| `SP\\%s` | `%s` |" % (rel, sha(p)))

B = r"""# REPAIR-2 STEP 3 - MEASURED-FALSE CLAIMS ANYWHERE. Author brief (two blind lanes)

You are ONE OF TWO BLIND LANES. The other lane has this brief and these slices; you will not see its work and it will
not see yours. A Fable adjudicator reconciles the two. Your independence is the value of your pass.

## What this step is

#e15 ruled that "the repair scope extends to every claim a reviewer MEASURED false, wherever it sits and whichever
wave last touched the field ... the close gate cannot pass a row carrying a measured-false byte claim." The slices
carry %(items)d owed items on %(rows)d rows from seven sources: #e15's measured-false list (each fact distinct-checked
and reproduced), undischarged orders, stale census figures, bare-decimal verse anchors, an author lane's escalations,
obligations the step-2 adjudication carried forward, and two Hebrew runs the citation sweep cannot collate.

Every item has a STATUS measured on the current rows: PRESENT means the claim or entry still stands; READER means
the order names nothing a string test can find, so you read the row and decide. A READER item where you find no
defect is recorded as NO_DEFECT with your evidence - never skipped.

## The rules that decide what you may write

- **An order is authority for exactly what it names and nothing adjacent.** A false only-ground is a STOP, never a
  substitution: if removing a false sentence leaves a grade or a boundary without its ground, record a STOP with the
  evidence instead of inventing a new ground.
- **Reproduce before you write.** A fact the slice carries as MEASURED (a distinct check) may be written. A fact a
  reviewer REPORTED (for example lane 02's wheel-vocabulary counts) must be reproduced by you from the witness by
  exact path first; if it does not reproduce, it is a STOP.
- **No grade, span or identity changes.** Grades are not yours in this step.
- **Refs may be reworded or removed only where an owed item names the entry.** A new or changed entry uses the
  vocabulary pinned today: `<face>:Ezek.C.V[-Ezek.C.V] [TOKEN] annotation`, one ROLE token from
  check_refs_mirror.ROLE_VOCABULARY (DEF-A4-ARGUED: every argued citation is mirrored by an entry with a ROLE token),
  NO face qualifier (step 4 installs those), an annotation of one to six words. An MT-borne device (mark, K/Q, paseq,
  note, device) sits on the oshb: face; a quotation on the web: face.
- **The zone:** MT 21:1-5 = WEB 20:45-49 and MT 21:6-37 = WEB 21:1-32. Any entry touching it is written on BOTH faces,
  `web:... = oshb:...`, mapped by the offset map and never by arithmetic.
- **observed_substrate_signals** may change only on a row whose owed item names it (P03-019, P09-010).
- **Marks:** a mark is recorded on the verse it FOLLOWS. Any entry or sentence that mentions a mark, paseq or puncta
  carries the literal disclosure "single-witness".
- **Hebrew:** never hand-type Hebrew. Every run is SLICED from `Ezek_oshb.txt` or from the live row by exact bytes; a
  labelled Qere form collates against its K/Q note.
- **English:** five or more WEB words are a quotation - double curly quotes and an in-field web: reference; the A6-b
  exemption covers a formula rendering only when the row names the device.
- **Categorical claims:** C2-amended - a claim that something is unsourced must be absent from BOTH pinned inputs; the
  census governs counts and membership.
- **Register rule:** row prose is a scholar-facing record - no rule identifiers, ruling numbers, file or tool names,
  digests, review or wave talk, or repair narration. State the fact about the text.
- **Rotation:** vary your wording; no 7-gram in more than a handful of rows, at least 4 distinct formulations for
  repeated kinds of statement.
- **Bare decimals (Q11 items):** if the dotted pair is an argued anchor, rewrite it as an explicit `oshb:Ezek.C.V` or
  `web:Ezek.C.V` and mirror it; if it is not argued (a range description, a count), leave it and say why.

## Pinned inputs

%(table)s

Pin rows for the pre-launch check:

%(pins)s

## Your gate - run it until ALL_CLEAN

`python -B <SP>\Ezek\repair2\step3\check_candidate_v3.py <your dir>\proposal.json --work <your dir>\gate_work`

It checks each proposed row (scope from the worklist, entry form, register, mirroring) AND runs the whole pinned
suite on your candidate rows against the live rows: no hard member may gain a flag. Running the suite THROUGH THIS
GATE is permitted; run no validator any other way. Its selftest runs first and refuses a verdict if an arm cannot fire.
It is a floor: it cannot tell you a sentence is true.

## Outputs - write early and rewrite at every stage (E-29); digest after your final write

1. `proposal.json` - `{"<row>": {"<field>": <full new value>}}`, only fields you change; refs and signals as FULL values.
2. `discharge.json` - per item id (S3-nnn): `status` DISCHARGED | NO_DEFECT | STOP, `what_i_wrote` (the sentence or
   entry) or `evidence` (for NO_DEFECT and STOP), `facts_reproduced` (each with tier), plus top-level `gate` (final
   ALL_CLEAN summary), `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory. Never modify the corpus or any pinned file. Never run git, write a receipt or touch
a registry. Escalate rather than write: any seam move, any grade you believe wrong, a pinned input that contradicts
itself, a digest that differs from the table.
""" % {"items": sum(len(s["owed_items"]) for s in slices.values()), "rows": len(slices), "table": "\n".join(table),
       "pins": "\n".join(pins)}

out = HERE / "STEP3_AUTHOR_BRIEF.md"
if "--preview" in sys.argv:
    print(B[:3000])
    raise SystemExit(0)
out.write_text(B, encoding="utf-8", newline="\n")
for lane in ("lane_a", "lane_b"):
    (SCR / lane).mkdir(parents=True, exist_ok=True)
print(json.dumps({"brief": str(out), "brief_sha256": sha(out), "slices_sha256": sha(slices_p), "rows": len(slices),
                  "items": sum(len(s["owed_items"]) for s in slices.values()), "lane_dirs": str(SCR)}, indent=1))
