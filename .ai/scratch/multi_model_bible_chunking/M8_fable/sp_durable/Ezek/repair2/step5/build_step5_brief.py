#!/usr/bin/env python3
"""Generate REPAIR-2 step-5 SLICES, the RULE-SUBSTANCE file and the AUTHOR BRIEF (register prose pass; blind lanes).

The substance of every barred rule id is EXTRACTED verbatim from the pinned ruling or brief that defines it, with its
exact location, so a lane states the rule's substance from the record and never from the orchestrator's paraphrase.
Rows are split into two halves balanced by prose length; each half goes to two blind lanes (OW-19's floor per item).

usage: python build_step5_brief.py [--probe]
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
SP = EZ.parent
PROBE = "--probe" in sys.argv
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad")
BASE = (SCR / "ezek_step5_probe") if PROBE else HERE
WL = BASE / "step5_worklist.v1.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess")

wl = json.loads(WL.read_text(encoding="utf-8"))
rows = {r["decision_id"]: r for r in (json.loads(l) for l in (EZ / "repair" / "rows_v7_cwo24.jsonl")
                                      .read_text(encoding="utf-8").splitlines() if l.strip())}
if sha(EZ / "repair" / "rows_v7_cwo24.jsonl") != wl["rows_sha256"]:
    raise SystemExit("REFUSED: the rows changed since the worklist was built; rebuild the worklist first")

# ---- rule substance, verbatim, each with its exact location
e12 = json.loads((EZ / "ezek_controlling_agent_ruling_e12.v1.json").read_text(encoding="utf-8"))
e14 = json.loads((EZ / "ezek_controlling_agent_ruling_e14.v1.json").read_text(encoding="utf-8"))
e15 = json.loads((EZ / "ezek_controlling_agent_ruling_e15.v1.json").read_text(encoding="utf-8"))
awb = (EZ / "AUTHOR_WAVE_BRIEF.v1.md").read_text(encoding="utf-8")
subst = []
for i, r in enumerate(e12["rulings"]):
    cid = r["class_id"]
    key = cid.split("_")[0]
    if key in ("A2", "A3", "A5", "A6", "A7", "A9", "A10", "A16", "MARKS-3D"):
        subst.append({"id": key, "source": "Ezek/ezek_controlling_agent_ruling_e12.v1.json rulings[%d].ruling (%s)" % (i, cid),
                      "verbatim": r["ruling"]})


def between(start, end, label):
    a = awb.find(start)
    b = awb.find(end, a + len(start))
    if a < 0 or b < 0:
        raise SystemExit("REFUSED: could not extract %s from AUTHOR_WAVE_BRIEF.v1.md (markers moved)" % label)
    line = awb[:a].count("\n") + 1
    return {"id": label, "source": "Ezek/AUTHOR_WAVE_BRIEF.v1.md from line %d" % line, "verbatim": awb[a:b].strip()}


subst.append(between("**CONF-CAL", "**The scale has exactly", "CONF-CAL"))
subst.append(between("**#e14 Q2 refines", "---", "#e14 Q2"))
subst.append(between("## 1. CUT-RULE", "---", "CUT-RULE, limb (a), limb (b), and the precedence of a driver over a mark"))
subst.append(between("## 5. The A9/A16 weighing duty", "---", "A9/A16 weighing"))
subst.append({"id": "DEF-A4-ARGUED", "source": "Ezek/ezek_controlling_agent_ruling_e14.v1.json q1_a4_worklist_basis.definition_written_here_DEF_A4_ARGUED",
              "verbatim": e14["q1_a4_worklist_basis"]["definition_written_here_DEF_A4_ARGUED"]})
subst.append({"id": "clause 6 v2 (near and far for a rival)", "source": "Ezek/ezek_controlling_agent_ruling_e15.v1.json q5_role_vocabulary.DEF_A4_ARGUED_clause_6_v2",
              "verbatim": e15["q5_role_vocabulary"]["DEF_A4_ARGUED_clause_6_v2"]})
q9 = e15["q9_section8_register"]
subst_p = BASE / "step5_rule_substance.v1.json"
subst_p.write_text(json.dumps({"schema": "ezek_repair2_step5_rule_substance.v1", "what": "the substance of each barred "
                               "rule id, verbatim from the record that defines it; state the substance, never the id",
                               "entries": subst}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")

# ---- slices, two halves balanced by prose length
owed = {}
for it in wl["items"]:
    owed.setdefault(it["row"], []).append(it)
size = {r: sum(len(rows[r].get(f) or "") for f in PROSE) for r in owed}
halves, tot = {1: [], 2: []}, {1: 0, 2: 0}
for r in sorted(owed, key=lambda x: (-size[x], x)):
    h = 1 if tot[1] <= tot[2] else 2
    halves[h].append(r)
    tot[h] += size[r]
slice_paths = {}
for h, rs in halves.items():
    sl = {r: {"row": r, "span": rows[r].get("span"), "confidence": rows[r].get("confidence"),
              "live_prose": {f: rows[r].get(f) for f in PROSE}, "refs_read_only": rows[r].get("boundary_evidence_refs"),
              "owed_items": owed[r]} for r in sorted(rs)}
    p = BASE / ("step5_slices_half%d.v1.json" % h)
    p.write_text(json.dumps({"schema": "ezek_repair2_step5_slices.v1", "half": h, "rows_sha256": wl["rows_sha256"],
                             "rows": len(sl), "items": sum(len(v["owed_items"]) for v in sl.values()),
                             "prose_characters": tot[h], "slices": sl}, ensure_ascii=False, indent=1),
                 encoding="utf-8", newline="\n")
    slice_paths[h] = p


def rel(p):
    return str(Path(p).resolve().relative_to(SP)) if str(Path(p).resolve()).startswith(str(SP)) else str(p)


for h in (1, 2):
    PINS = [
        (EZ / "repair" / "rows_v7_cwo24.jsonl", "the live rows"),
        (slice_paths[h], "YOUR ROWS: span, confidence, live prose, refs (read only), and the owed items as data"),
        (WL, "the whole worklist and the gate's scope"),
        (subst_p, "the substance of every barred rule id, verbatim from the record that defines it"),
        (EZ / "ezek_controlling_agent_ruling_e15.v1.json", "the ruling: q9_section8_register governs this step"),
        (EZ / "ezek_controlling_agent_ruling_e12.v1.json", "the source of the A-class substance entries"),
        (EZ / "AUTHOR_WAVE_BRIEF.v1.md", "the source of CONF-CAL, CUT-RULE and A9/A16 substance; its 13.2 is SUPERSEDED in part (below)"),
        (HERE / "check_candidate_v5.py", "YOUR GATE (v5): claim accounting, English form, completion measure, the whole suite"),
        (EZ / "repair2" / "step4" / "check_candidate_v4.py", "imported by the gate"),
        (EZ / "repair2" / "step3" / "check_candidate_v3_1.py", "imported by the gate"),
        (EZ / "repair2" / "step3" / "check_candidate_v3.py", "imported by the gate"),
        (EZ / "repair2" / "step2_reconciliation" / "check_candidate_v2.py", "imported by the gate"),
        (EZ / "repair2" / "suite_delta.py", "imported by the gate"),
        (EZ / "tools" / "run_validator_suite.py", "run by the gate"),
        (EZ / "tools" / "check_register.py", "the register member, with the three arms #e15 Q9(b) ordered"),
        (EZ / "tools" / "check_role_tokens.py", "a hard member of the suite"),
        (EZ / "tools" / "role_tokens_phase.json", "that member's pinned phase"),
        (EZ / "tools" / "check_refs_mirror.py", "imported by the gate"),
        (EZ / "tools" / "ezek_lib.py", "imported by the gate"),
        (EZ / "tools" / "verse_map_web.json", "the English version by verse (for quotations)"),
        (EZ / "Ezek_oshb.txt", "the Hebrew witness (WLC/OSHB)"),
        (EZ / "pmarks_Ezek.json", "marks, K/Q, paseq, notes (single witness)"),
        (EZ / "ezek_device_inventory.v2.json", "the device census"),
        (EZ / "web_mt_offset_map.json", "the WEB/MT map"),
    ]
    table = ["| input | sha256 | what it is |", "|---|---|---|"]
    pins = []
    for p, what in PINS:
        if not Path(p).is_file():
            raise SystemExit("REFUSED: pinned input missing %s" % p)
        shown = ("SP\\" + rel(p)) if not str(p).startswith(str(SCR)) else str(p)
        table.append("| `%s` | `%s` | %s |" % (shown, sha(p), what))
        pins.append("| `%s` | `%s` |" % (shown, sha(p)))
    n_rows = len(halves[h])
    n_items = sum(len(owed[r]) for r in halves[h])
    B = r"""# REPAIR-2 STEP 5 - THE REGISTER PROSE PASS. Author brief, HALF %(h)d (two blind lanes on this half)

You are ONE OF TWO BLIND LANES on half %(h)d (%(rows)d rows, %(items)d owed items); a Fable adjudicator reconciles you
with the other lane, whose work you never see. The other half has its own two lanes.

## What this step is - the ruling's own words govern

#e15 Q9(c): "%(q9c)s"

#e15 Q9(a), the rule you apply: "%(q9a)s"

## A SUPERSESSION YOU MUST APPLY

`AUTHOR_WAVE_BRIEF.v1.md` section 13.2 once told authors to say "the section-mark record", "the verse census", "the
device census" and "the division plan" instead of file names. #e15 Q9(a) BARS those phrases: a row "never names a
record, census, plan, inventory, worklist, digest or key". Q9(a) governs; 13.2's substitution list does not. Name the
WITNESS and its layers ("this witness records a samekh after MT 8:14, single witness"; "the K/Q apparatus at MT 33:13
reads ..."; "the editors' note at MT 18:29"), state counts with the one sanctioned shorthand "(sweep: N verses)", and
state a method rule by its SUBSTANCE ("a row under three verses is held only for a complete word-event unit"), never
by its source. The rest of the author-wave brief is pinned only as the source of the rule substance it quotes.

## The owed items, by class (each item carries its data in your slices)

- **REG** - register flags on a field. Rewrite so the field states the substance and no flag remains. The substance of
  each barred id is in the rule-substance file, verbatim from the record that defines it: take only what the row's
  argument needs.
- **READBACK** - a field the orchestrator's own register, residue or grammar sweep edited and nobody read back. READ
  THE WHOLE FIELD AS ENGLISH. Repair what does not read (a doubled article, colliding substitutions, a dropped clause
  boundary, a paraphrase of a barred referent). If it reads correctly and bars nothing, it is NO_DEFECT with the
  sentence you read as evidence.
- **SPOT** - a spot lane's register finding; discharge it or show it is already gone.
- **ROUTED** - an earlier adjudication's routing to this step, verbatim; do what it names or STOP with evidence.
- **NEARFAR** - rejected-alternative prose that uses near and far in an older sense. Under clause 6 v2 a rival's near
  face is its candidate onset verse and its far face the verse behind it; reword so the prose and the tokens agree, or
  use wording that needs no face term. The refs are read-only here.
- **WEBQ** - a web_quotes flag. Five or more consecutive WEB words are a quotation whatever the delimiter and take
  double curly quotes and an in-field web: reference; a run that is nothing but the WEB's fixed rendering of a counted
  device is exempt (A6-b) - say so as NO_DEFECT. A case or apostrophe mismatch: quote the English exactly or quote
  fewer than five words.

## Rules for what you may write

- **Change no claim.** The gate extracts every face reference, verse number, Hebrew run, evidence-tier word, count and
  curly-quoted English from a row's prose; any that your rewrite removes must be ACCOUNTED FOR in discharge.json under
  `claim_accounting[row]` as `{"anchor": <exact string the gate prints>, "why": <barred referent removed | restated as
  ... | duplicate | moved to another field>}`. An unaccounted removal fails the gate.
- **Scope:** the prose fields of your rows only. No grade, span, identity, signals or refs change. If a rewrite would
  orphan a mirrored citation, keep the citation in the prose. HIGH rows are in scope for register rewrites and nothing
  else.
- **OW-18 survives:** the tier word and the witness are stated; the file is not. A mark, paseq or puncta mention keeps
  "single-witness". **Hebrew:** never hand-type it - SLICED from the witness or the live row. **Rotation:** do not
  template - no 7-gram in more than a handful of rows, at least 4 distinct formulations for a repeated statement.
- **The register rule:** a row is a scholar-facing record - no rule ids, ruling numbers, file or tool names,
  digests, review or wave talk, repair narration ("is withdrawn", "the earlier denial", "corrected here").
- **What a prose rewrite can break although the refs are read-only - the suite checks each:**
  DEF-A4-ARGUED - every argued citation in the prose stays mirrored by a refs entry carrying a ROLE token, so do not
  introduce an argued verse the refs do not carry; clause 6 v2 - the refs' face qualifier and seam pair on each
  WARRANT must still agree with what the prose says about near and far; the mark convention - a mark is recorded on
  the verse it FOLLOWS, and prose that restates a mark keeps that direction; C2-amended - a categorical claim you
  restate is unsourced only when absent from BOTH pinned inputs, so do not sharpen a claim into a universal the
  inputs do not carry; the zone - MT 21:1-5 = WEB 20:45-49 and MT 21:6-37 = WEB 21:1-32, and a verse in it that the
  prose names is written on BOTH faces, mapped by the offset map, never by arithmetic.
- **Read back as English:** every field you rewrite is read in full after your final edit; record `read_back: true`
  per item only after you have done it.

## Pinned inputs

%(table)s

Pin rows for the pre-launch check:

%(pins)s

## Your gate - run it until the verdict is clean, and drive the completion measure down honestly

`python -B <SP>\Ezek\repair2\step5\check_candidate_v5.py <your dir>\proposal.json --work <your ABSOLUTE dir>\gate_work --discharge <your dir>\discharge.json%(wl_arg)s`

It checks the per-row delta (no new register flag, unmirrored citation, orphan ref or mirror disagreement), the claim
accounting, new English-form problems, the WHOLE pinned suite with no hard member gaining a flag, and reports the
register flags left on the owed rows. Its English arm is a floor: it cannot see a doubled article across a noun or a
dropped clause boundary. Your reading can.

## Outputs - write early and rewrite at every stage (E-29); digest after the final write

1. `proposal.json` - `{"<row>": {"<field>": <full new value>}}`, only changed prose fields.
2. `discharge.json` - per item id (S5-nnn): `status` DISCHARGED | NO_DEFECT | STOP, `what_i_wrote` or `evidence`,
   `read_back`, `facts_reproduced` with tiers; top-level `claim_accounting`, `gate` (final verdict and completion
   measure), `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. Escalate
rather than write: any claim you believe false (that is not this step's repair), any grade you believe wrong, a
pinned input that contradicts itself, a digest that differs from the table.
""" % {"h": h, "rows": n_rows, "items": n_items, "q9c": q9["c_prose_pass"], "q9a": q9["a_paraphrase_of_a_barred_referent"],
       "table": "\n".join(table), "pins": "\n".join(pins),
       "wl_arg": (" --worklist %s" % WL) if PROBE else ""}
    out = BASE / ("STEP5_AUTHOR_BRIEF_HALF%d.md" % h)
    out.write_text(B, encoding="utf-8", newline="\n")
    print(json.dumps({"half": h, "brief": str(out), "brief_sha256": sha(out), "rows": n_rows, "items": n_items,
                      "prose_characters": tot[h], "slices_sha256": sha(slice_paths[h])}, indent=1))
print(json.dumps({"rule_substance_entries": len(subst), "rule_substance_sha256": sha(subst_p)}, indent=1))
