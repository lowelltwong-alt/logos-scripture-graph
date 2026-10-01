#!/usr/bin/env python3
"""Generate the REPAIR-2 step-5 Fable ADJUDICATION brief for one half, once both of its blind lanes have landed durably.

The divergence section is COMPUTED from the two discharge files and proposals - item statuses that differ, fields
only one lane changed, fields both changed differently, and each lane's stops - and states them without a preference.
The adjudicator reads the lanes' own words; the summary only tells it where to look.

usage: python build_step5_adjudication_brief.py --half <1|2>
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
SP = EZ.parent
H = int(sys.argv[sys.argv.index("--half") + 1])
DELIV = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
             r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_step5_adjudication") / ("h%d" % H)
LANES = EZ / "author" / "repair2_step5"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

la = {k: json.loads((LANES / ("h%d_lane_a" % H) / k).read_text(encoding="utf-8")) for k in ("proposal.json", "discharge.json")}
lb = {k: json.loads((LANES / ("h%d_lane_b" % H) / k).read_text(encoding="utf-8")) for k in ("proposal.json", "discharge.json")}
sl = json.loads((HERE / ("step5_slices_half%d.v1.json" % H)).read_text(encoding="utf-8"))
item_ids = sorted(i["id"] for s in sl["slices"].values() for i in s["owed_items"])


def items(d):
    for k in ("items", "per_item"):
        if isinstance(d.get(k), dict):
            return d[k]
    return {k: v for k, v in d.items() if isinstance(k, str) and k.startswith("S5-")}


ia, ib = items(la["discharge.json"]), items(lb["discharge.json"])
status = lambda it: str((it or {}).get("status", "MISSING")).upper()          # noqa: E731
st_diff = [(i, status(ia.get(i)), status(ib.get(i))) for i in item_ids if status(ia.get(i)) != status(ib.get(i))]
missing = {"A": [i for i in item_ids if i not in ia], "B": [i for i in item_ids if i not in ib]}
pa, pb = la["proposal.json"], lb["proposal.json"]
only_a = sorted("%s.%s" % (r, f) for r in pa for f in pa[r] if f not in (pb.get(r) or {}))
only_b = sorted("%s.%s" % (r, f) for r in pb for f in pb[r] if f not in (pa.get(r) or {}))
both_diff = sorted("%s.%s" % (r, f) for r in pa for f in pa[r] if f in (pb.get(r) or {}) and pa[r][f] != pb[r][f])
both_same = sorted("%s.%s" % (r, f) for r in pa for f in pa[r] if f in (pb.get(r) or {}) and pa[r][f] == pb[r][f])
stops = {"A": [i for i in item_ids if status(ia.get(i)) == "STOP"], "B": [i for i in item_ids if status(ib.get(i)) == "STOP"]}
div = {"half": H, "items": len(item_ids), "status_differs": st_diff, "missing_from_discharge": missing,
       "fields_only_lane_a_changed": only_a, "fields_only_lane_b_changed": only_b,
       "fields_both_changed_differently": both_diff, "fields_both_changed_identically": both_same, "stops": stops}
div_p = HERE / ("step5_divergence_half%d.v1.json" % H)
div_p.write_text(json.dumps(div, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")

PINS = [
    (EZ / "repair" / "rows_v7_cwo24.jsonl", "the live rows"),
    (HERE / ("step5_slices_half%d.v1.json" % H), "this half's rows, prose and owed items"),
    (HERE / "step5_worklist.v1.json", "the worklist and the gate's scope"),
    (HERE / "step5_rule_substance.v1.json", "the substance of every barred rule id, verbatim"),
    (HERE / ("STEP5_AUTHOR_BRIEF_HALF%d.md" % H), "the brief both lanes held; its rules bind you identically"),
    (LANES / ("h%d_lane_a" % H) / "proposal.json", "blind lane A - proposal"),
    (LANES / ("h%d_lane_a" % H) / "discharge.json", "blind lane A - per-item discharge and claim accounting"),
    (LANES / ("h%d_lane_b" % H) / "proposal.json", "blind lane B - proposal"),
    (LANES / ("h%d_lane_b" % H) / "discharge.json", "blind lane B - per-item discharge and claim accounting"),
    (div_p, "where the lanes diverge, computed from their files (a map, not a reading)"),
    (EZ / "ezek_controlling_agent_ruling_e15.v1.json", "the ruling: q9_section8_register governs"),
    (HERE / "check_candidate_v5.py", "YOUR GATE (v5)"),
    (EZ / "repair2" / "step4" / "check_candidate_v4.py", "imported by the gate"),
    (EZ / "repair2" / "step3" / "check_candidate_v3_1.py", "imported by the gate"),
    (EZ / "repair2" / "step3" / "check_candidate_v3.py", "imported by the gate"),
    (EZ / "repair2" / "step2_reconciliation" / "check_candidate_v2.py", "imported by the gate"),
    (EZ / "repair2" / "suite_delta.py", "imported by the gate"),
    (EZ / "tools" / "run_validator_suite.py", "run by the gate"),
    (EZ / "tools" / "check_register.py", "the register member"),
    (EZ / "tools" / "check_role_tokens.py", "a hard member"),
    (EZ / "tools" / "role_tokens_phase.json", "its pinned phase"),
    (EZ / "tools" / "check_refs_mirror.py", "imported by the gate"),
    (EZ / "tools" / "ezek_lib.py", "imported by the gate"),
    (EZ / "tools" / "verse_map_web.json", "the English version by verse"),
    (EZ / "Ezek_oshb.txt", "the Hebrew witness (WLC/OSHB)"),
    (EZ / "pmarks_Ezek.json", "marks, K/Q, paseq, notes (single witness)"),
    (EZ / "ezek_device_inventory.v2.json", "the device census"),
    (EZ / "web_mt_offset_map.json", "the WEB/MT map"),
]
table, pins = ["| input | sha256 | what it is |", "|---|---|---|"], []
for p, what in PINS:
    if not Path(p).is_file():
        raise SystemExit("REFUSED: pinned input missing - land both lanes durably first: %s" % p)
    rel = "SP\\" + str(Path(p).resolve().relative_to(SP))
    table.append("| `%s` | `%s` | %s |" % (rel, sha(p), what))
    pins.append("| `%s` | `%s` |" % (rel, sha(p)))

B = r"""# REPAIR-2 STEP 5 - ADJUDICATION OF TWO BLIND PROSE LANES, HALF %(h)d (Fable)

Attempt `ezek_repair2_step5_h%(h)d_adjudication_a1`, execution `ezek_repair2_step5_h%(h)d_adjudication_a1#e1`. You are
the controlling adjudicator (OW-13: Fable adjudicates). Two blind Opus lanes answered the same %(items)d owed items of
the register prose pass on this half; you produce ONE proposal. The other half has its own adjudicator.

## What you decide, recorded in adjudication.json

1. Per item (S5-nnn): DISCHARGED (with the text you adopt), NO_DEFECT (with evidence) or STOP (with evidence).
2. Per changed field: which lane's text you adopt, or a reconciled text of your own where neither lane's text both
   states the substance and reads as English - and why. A reconciled text owes everything a lane's text owes.
3. READ EVERY ADOPTED FIELD IN FULL AS ENGLISH after your final edit. This is the second reading #e15 Q9(b) requires
   under OW-19; the gate's English arm is a floor that cannot see a doubled article across a noun or a dropped clause
   boundary. Record `read_back: true` per field only after you have read it.
4. CLAIMS: any anchor the gate reports removed must be accounted for in your own `claim_accounting[row]`, taken from
   the lane you followed or written by you; a claim neither lane can account for is restored, never dropped.
5. ROUTED: anything beyond this step - a claim you believe false, a grade question, a class question for #e16, the
   second Fable review - listed with its reason.

## Where the lanes diverge - computed from their files, stated without a preference

- items whose statuses differ: %(n_st)d; items missing from a discharge: A %(miss_a)d, B %(miss_b)d
- fields only lane A changed: %(only_a)d; only lane B: %(only_b)d; both changed differently: %(both_diff)d; identically: %(both_same)d
- stops: lane A %(stops_a)d, lane B %(stops_b)d

The full lists are in the pinned divergence file. A field only one lane changed is a question in itself: was the other
lane right to leave it (NO_DEFECT), or did it miss an owed item?

## Rules - the lanes' brief is pinned and binds you identically

State substance, never a barred referent: no rule ids, ruling numbers, file or tool names, digests, record, census,
plan, inventory, worklist or key names, review or wave talk, repair narration. The register rule: a row is a
scholar-facing record. Name the witness and its layers; "(sweep: N verses)" is the one sanctioned count shorthand.
Change no claim; no grade, span, identity, signals or refs change. "single-witness" on any mark, paseq or puncta
mention; a mark is recorded on the verse it FOLLOWS; never hand-type Hebrew - SLICED from the witness or the live row;
five or more WEB words take double curly quotes and a web: reference, a counted device's fixed rendering is exempt
(A6-b); C2-amended - unsourced means absent from BOTH pinned inputs; DEF-A4-ARGUED - every argued citation stays
mirrored by a refs entry with a ROLE token, whose face qualifier and seam pair must still agree with the prose; the
zone - MT 21:1-5 = WEB 20:45-49 - on BOTH faces; rotation - no 7-gram in more than a handful of rows, at least 4
distinct formulations.

## Pinned inputs

%(table)s

Pin rows for the pre-launch check:

%(pins)s

## The gate

`python -B <SP>\Ezek\repair2\step5\check_candidate_v5.py %(deliv)s\proposal.json --work %(deliv)s\gate_work --discharge %(deliv)s\adjudication.json`

Run it until ALL_CLEAN is true; report the completion measure (register flags left on the owed rows) beside it, and
account for every flag you leave with its reason.

## Outputs - write early, rewrite at every stage (E-29), digest after the final write

1. `%(deliv)s\proposal.json` - only changed prose fields, FULL new values.
2. `%(deliv)s\adjudication.json` - per item the decision; per field the lane followed or the reconciled text and why;
   top-level `claim_accounting`, `gate` with the completion measure, `routed`, `what_i_could_not_verify`,
   `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. Escalate
rather than write: any seam move, any grade you believe wrong, a pinned input that contradicts itself, a digest that
differs from the table.
""" % {"h": H, "items": len(item_ids), "n_st": len(st_diff), "miss_a": len(missing["A"]), "miss_b": len(missing["B"]),
       "only_a": len(only_a), "only_b": len(only_b), "both_diff": len(both_diff), "both_same": len(both_same),
       "stops_a": len(stops["A"]), "stops_b": len(stops["B"]), "table": "\n".join(table), "pins": "\n".join(pins),
       "deliv": str(DELIV)}
out = HERE / ("STEP5_ADJUDICATION_BRIEF_HALF%d.md" % H)
out.write_text(B, encoding="utf-8", newline="\n")
DELIV.mkdir(parents=True, exist_ok=True)
print(json.dumps({"brief": str(out), "sha256": sha(out), "divergence": {k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in div.items()}}, indent=1))
