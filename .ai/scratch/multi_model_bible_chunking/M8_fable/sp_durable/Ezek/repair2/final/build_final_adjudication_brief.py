#!/usr/bin/env python3
"""Generate the FINAL REMEDIATION Fable ADJUDICATION brief for one slice, once both blind lanes have landed durably.

The divergence section is COMPUTED from the two discharge files and proposals - item statuses that differ, items only lane
A held (scope cut 3: lanes ONE), fields only one lane changed, fields both changed differently, stops and grade questions -
and states them without a preference. The adjudicator reads the lanes' own words; the summary only tells it where to look.

usage: python build_final_adjudication_brief.py --slice K
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
SP = EZ.parent
K = int(sys.argv[sys.argv.index("--slice") + 1])
DELIV = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
             r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_final") / ("s%d_adjudication" % K)
LANES = EZ / "author" / "final"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
la = {k: json.loads((LANES / ("s%d_lane_a" % K) / k).read_text(encoding="utf-8")) for k in ("proposal.json", "discharge.json")}
lb = {k: json.loads((LANES / ("s%d_lane_b" % K) / k).read_text(encoding="utf-8")) for k in ("proposal.json", "discharge.json")}
sa = json.loads((HERE / ("final_slices_s%d_laneA.v1.json" % K)).read_text(encoding="utf-8"))
sb = json.loads((HERE / ("final_slices_s%d_laneB.v1.json" % K)).read_text(encoding="utf-8"))
ids_a = sorted(i["id"] for s in sa["slices"].values() for i in s["owed_items"])
ids_b = sorted(i["id"] for s in sb["slices"].values() for i in s["owed_items"])
one_only = sorted(set(ids_a) - set(ids_b))


def items(d):
    for k in ("items", "per_item"):
        if isinstance(d.get(k), dict):
            return d[k]
        if isinstance(d.get(k), list):
            return {x.get("id"): x for x in d[k] if isinstance(x, dict)}
    return {k: v for k, v in d.items() if isinstance(k, str) and k.startswith("F-")}


ia, ib = items(la["discharge.json"]), items(lb["discharge.json"])
status = lambda it: str((it or {}).get("status", "MISSING")).upper()          # noqa: E731
st_diff = [(i, status(ia.get(i)), status(ib.get(i))) for i in ids_b if status(ia.get(i)) != status(ib.get(i))]
missing = {"A": [i for i in ids_a if i not in ia], "B": [i for i in ids_b if i not in ib]}
pa, pb = la["proposal.json"], lb["proposal.json"]
only_a = sorted("%s.%s" % (r, f) for r in pa for f in pa[r] if f not in (pb.get(r) or {}))
only_b = sorted("%s.%s" % (r, f) for r in pb for f in pb[r] if f not in (pa.get(r) or {}))
both_diff = sorted("%s.%s" % (r, f) for r in pa for f in pa[r] if f in (pb.get(r) or {}) and pa[r][f] != pb[r][f])
both_same = sorted("%s.%s" % (r, f) for r in pa for f in pa[r] if f in (pb.get(r) or {}) and pa[r][f] == pb[r][f])
stops = {"A": [i for i in ids_a if status(ia.get(i)) == "STOP"], "B": [i for i in ids_b if status(ib.get(i)) == "STOP"]}
gq = {"A": [i for i in ids_a if status(ia.get(i)) == "GRADE_QUESTION"], "B": [i for i in ids_b if status(ib.get(i)) == "GRADE_QUESTION"]}
div = {"slice": K, "items_lane_a": len(ids_a), "items_lane_b": len(ids_b), "items_lane_a_only_by_scope_cut_3": one_only,
       "status_differs": st_diff, "missing_from_discharge": missing, "fields_only_lane_a_changed": only_a,
       "fields_only_lane_b_changed": only_b, "fields_both_changed_differently": both_diff,
       "fields_both_changed_identically": both_same, "stops": stops, "grade_questions": gq}
k3 = json.loads((HERE / "k3_caps_plan.v1.json").read_text(encoding="utf-8"))
caps_here = sorted(c["row"] for c in k3["caps"] if c["row"] in sa["slices"])
div["k3_caps_on_this_slice"] = caps_here
div_p = HERE / ("final_divergence_s%d.v1.json" % K)
div_p.write_text(json.dumps(div, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")

PINS = [
    (EZ / "repair" / "rows_v7_cwo24.jsonl", "the live rows"),
    (HERE / ("final_slices_s%d_laneA.v1.json" % K), "this slice's rows, prose and ALL owed items (lane A's file)"),
    (HERE / ("final_slices_s%d_laneB.v1.json" % K), "lane B's file (omits the scope-cut-3 items)"),
    (HERE / "final_worklist.v2.json", "the worklist (the gate's scope)"),
    (HERE / "final_substance.v1.json", "the substance, verbatim from the records that define it"),
    (HERE / ("FINAL_AUTHOR_BRIEF_S%d_A.md" % K), "the brief lane A held; its rules bind you identically"),
    (LANES / ("s%d_lane_a" % K) / "proposal.json", "blind lane A - proposal"),
    (LANES / ("s%d_lane_a" % K) / "discharge.json", "blind lane A - per-item discharge and claim accounting"),
    (LANES / ("s%d_lane_b" % K) / "proposal.json", "blind lane B - proposal"),
    (LANES / ("s%d_lane_b" % K) / "discharge.json", "blind lane B - per-item discharge and claim accounting"),
    (div_p, "where the lanes diverge, computed from their files (a map, not a reading)"),
    (HERE / "k3_caps_plan.v1.json", "the grade caps the orchestrator applies after the merge (#e17 K3), with the section-7 text measured"),
    (EZ / "author" / "e17" / "ruling_e17.json", "the controlling agent's latest ruling"),
    (EZ / "author" / "e16" / "ruling_e16.json", "the ruling before it"),
    (HERE / "check_candidate_v6.py", "YOUR GATE (v6)"),
    (EZ / "repair2" / "step5" / "check_candidate_v5.py", "imported by the gate"),
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
    (EZ / "tools" / "check_web_quotes.py", "the quotation member"),
    (EZ / "tools" / "ezek_lib.py", "imported by the gate"),
    (EZ / "tools" / "verse_map_web.json", "the English version by verse"),
    (EZ / "Ezek_oshb.txt", "the Hebrew witness (WLC/OSHB)"),
    (EZ / "pmarks_Ezek.json", "marks, K/Q, paseq, notes (single witness)"),
    (EZ / "ezek_device_inventory.v3.json", "the device census v3"),
    (EZ / "book_strategy_Ezek.md", "the division plan"),
    (EZ / "web_mt_offset_map.json", "the WEB/MT map"),
]
table, pins = ["| input | sha256 | what it is |", "|---|---|---|"], []
for p, what in PINS:
    if not Path(p).is_file():
        raise SystemExit("REFUSED: pinned input missing - land both lanes durably first: %s" % p)
    rel = "SP\\" + str(Path(p).resolve().relative_to(SP))
    table.append("| `%s` | `%s` | %s |" % (rel, sha(p), what))
    pins.append("| `%s` | `%s` |" % (rel, sha(p)))

B = r"""# FINAL REMEDIATION - ADJUDICATION OF TWO BLIND AUTHOR LANES, SLICE %(k)d (Fable)

Attempt `ezek_final_s%(k)d_adjudication_a1`, execution `ezek_final_s%(k)d_adjudication_a1#e1`. You are the controlling
adjudicator for this slice (OW-13: Fable adjudicates). Two blind Opus lanes answered the owed items of this slice in the
book's last authoring pass; you produce ONE proposal. Every other slice has its own adjudicator.

## What you decide, recorded in adjudication.json

1. Per item (F-nnn): DISCHARGED (with the text you adopt), NO_DEFECT (with evidence), STOP (with evidence) or
   GRADE_QUESTION (with the faces). %(n_one)d items were given to lane A alone (a low-severity defect one earlier reader
   raised); on those, lane A's work is the only lane - read it against the witness yourself before adopting it.
2. Per changed field: which lane's text you adopt, or a reconciled text of your own where neither lane's text both states
   the substance and reads as English - and why. A reconciled text owes everything a lane's text owes.
3. READ EVERY ADOPTED FIELD IN FULL AS ENGLISH after your final edit (the second reading under OW-19); record
   `read_back: true` per field only then.
4. CLAIMS: any anchor the gate reports removed on a non-re-tiled row is accounted for in your own
   `claim_accounting[row]`, taken from the lane you followed or written by you; a claim neither lane can account for is
   restored, never dropped. On a re-tiled row the gate reports the anchors removed from the seed: confirm the row you adopt
   still states every face the ruling measured and every disclosure for the verses of its span.
5. GRADE QUESTIONS and anything beyond this pass (a seam move, a class question): listed under `routed` with the faces.
   Never change a grade, span, identity or signals.

## Where the lanes diverge - computed from their files, stated without a preference

- items whose statuses differ: %(n_st)d; missing from a discharge: A %(miss_a)d, B %(miss_b)d
- fields only lane A changed: %(only_a)d; only lane B: %(only_b)d; both changed differently: %(both_diff)d; identically: %(both_same)d
- stops: lane A %(stops_a)d, lane B %(stops_b)d; grade questions: lane A %(gq_a)d, lane B %(gq_b)d

The full lists are in the pinned divergence file. A field only one lane changed is a question in itself: was the other
lane right to leave it, or did it miss an owed item?

## Grade caps the orchestrator applies after the merge

%(k3)s

## Rules - lane A's brief is pinned and binds you identically

The register rule: a row is a scholar-facing record - no rule ids, ruling numbers, file or tool names, digests, record,
census, plan, inventory or worklist names, scale labels, review or wave talk, repair narration. "single-witness" on any
mark, paseq or puncta mention; a mark is recorded on the verse it FOLLOWS; never hand-type Hebrew - SLICE it from the
witness or the live row; five or more WEB words take double curly quotes and a web: reference (a counted device's fixed
rendering is exempt); unsourced means absent from BOTH pinned inputs; every argued citation stays mirrored by a refs entry
with a ROLE token whose face qualifier and seam pair agree with the prose (':merge' for a rival that contests the row's own
seam); the zone - MT 21:1-5 = WEB 20:45-49 - on BOTH faces; no 7-gram in more than a handful of rows.

## Budget

The owner's token line for this book is close. Adjudicate from the lanes' files and the divergence map; measure on the
witness only what a decision rests on.

## Pinned inputs

%(table)s

Pin rows for the pre-launch check:

%(pins)s

## The gate

`python -B <SP>\Ezek\repair2\final\check_candidate_v6.py %(deliv)s\proposal.json --work %(deliv)s\gate_work --discharge %(deliv)s\adjudication.json --worklist <SP>\Ezek\repair2\final\final_worklist.v2.json`

Run it until ALL_CLEAN is true; report the completion measure beside it, and account for every register flag you leave.

## Outputs - write early, rewrite at every stage (E-29), digest after the final write

1. `%(deliv)s\proposal.json` - only changed fields, FULL new values (refs as full lists).
2. `%(deliv)s\adjudication.json` - `items` per item id; `fields` per changed field (lane followed or reconciled, why);
   top-level `claim_accounting`, `grade_questions`, `gate` with the completion measure, `routed`,
   `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry; never list,
glob or search directories. Escalate rather than write: any seam move, any grade you believe wrong, a pinned input that
contradicts itself, a digest that differs from the table.
""" % {"k": K, "n_one": len(one_only), "n_st": len(st_diff), "miss_a": len(missing["A"]), "miss_b": len(missing["B"]),
       "only_a": len(only_a), "only_b": len(only_b), "both_diff": len(both_diff), "both_same": len(both_same),
       "stops_a": len(stops["A"]), "stops_b": len(stops["B"]), "gq_a": len(gq["A"]), "gq_b": len(gq["B"]),
       "table": "\n".join(table), "pins": "\n".join(pins), "deliv": str(DELIV),
       "k3": (("The controlling agent's class ruling K3 (#e17) caps a row whose span or region the plan names as an open question "
               "at medium_low; the pinned caps plan lists, with the plan text measured, the rows above that cap. On this slice: %s. "
               "The orchestrator moves each to medium_low through its own guarded confidence operation after the merge - you "
               "change no grade. The prose you adopt on these rows must not argue a medium grade; where an item asks for the "
               "grade's ground, state in one clause, in the faces' own terms, that the plan holds the region as an open "
               "question, which holds the grade at medium_low. If you measure that the plan does NOT name a listed span or "
               "region, say so with the text under routed, and the row is not capped." % ", ".join(caps_here))
              if caps_here else "None on this slice.")}
out = HERE / ("FINAL_ADJUDICATION_BRIEF_S%d.md" % K)
out.write_text(B, encoding="utf-8", newline="\n")
DELIV.mkdir(parents=True, exist_ok=True)
print(json.dumps({"brief": out.name, "sha256": sha(out), "divergence": {k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in div.items()}}, indent=1))
