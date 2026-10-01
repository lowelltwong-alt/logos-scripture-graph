#!/usr/bin/env python3
"""Build the two records the v9 delta re-check lanes judge and the v9 close tool gates on (write-new, never overwrite).

delta_docket_v9.v1.json - every residual of both v1 merged-close final checks, keyed <lane><index> (A0..A9, B0..B20),
  with the orchestration's CLAIM of its state after the v9 fix round: cured_v9, partly_cured_v9 or carried_low. A claim
  is not a judgement; the two blind delta lanes judge each one (OW-19: the orchestrator never grades its own items).
v1_unmet_gate_dispositions.v1.json - every close_gate_assessment entry either v1 lane marked met:false, keyed
  <lane>:<gate text verbatim>, with one typed disposition:
    CURED_BY_DELTA_VERDICT          a verdict gate; cured only by both delta lanes' own verdict over v9 (field named)
    OWED_OW26                       the stage-1 transcript audit, OWED, NOT MET under OW-26 (the text must say so)
    DEFERRED_OW28_FABLE_END_REVIEW  a gate that needs a claude-fable-5-1 model; OW-28 defers Fable to the campaign-end
                                    review, so it is DEFERRED, never MET (the gate text must name fable)
    OWNER_ACT_OW11                  a placement only the owner may make (the lane's evidence must say owner)
The close tool re-derives both key sets from the v1 lane files and re-checks every type's text constraint itself.
Gate text and evidence are copied verbatim from the pinned v1 lane files.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
EZ = HERE.parents[1]
MC = EZ / "merged_close"
LANDING_PIN = None  # the v1 landing manifest is re-hashed per file below
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731
land = json.loads((MC / "landing_manifest.v1.json").read_text(encoding="utf-8"))
fc = {}
for L in ("A", "B"):
    f = land["lanes"][L]["files"]["final_check.json"]
    p = MC / f["durable"]
    if sha(p.read_bytes()) != f["sha256"]:
        raise SystemExit("REFUSED: lane %s final_check.json does not match the v1 landing manifest" % L)
    fc[L] = (json.loads(p.read_text(encoding="utf-8")), f["sha256"])

CURED, PART, CARRIED = "cured_v9", "partly_cured_v9", "carried_low"
CLAIMS = {
    "A0": (CURED, "rows_v9_final P03-001 boundary_rationale: one sentence appended stating the ground of the grade "
                  "(bounded author ezek_fixround_v9_author_a1#e1; manifest rows_v9_final.manifest.json). The link "
                  "between that ground and the grade is INFERRED; the writer's original motive is UNAVAILABLE."),
    "A1": (CARRIED, "not touched in v9; a grade question, left for the campaign-end Fable review (OW-28)"),
    "A2": (CARRIED, "not touched in v9"),
    "A3": (CURED, "rows_v9_final P10-016 boundary_evidence_refs positions 12-14 replaced in place by the bounded author; "
                  "device_notes already carried the F-337 sentence, so it is unchanged. The 40:35 inner-court claim is "
                  "INFERRED; 'the plan never cuts inside' is REPORTED."),
    "A4": (CARRIED, "not cured: the sidecar source regenerated over v9 byte-identical (9cea1004), so the M8-Ezek-090 "
                    "fragment, the five 'no ground' reasons and the P01-010 composed fallback stand"),
    "A5": (CARRIED, "parity re-run over v9 (cwo/cwo_parity.rows_v9_final.json GREEN), but the ruled-rewrite attribution by "
                    "row id is not added"),
    "A6": (PART, "gen_atlas_rows.py, check_atlas_rows.py and gen_sidecars.py now read rows_v9_final (atlas check 15/15 PASS, "
                 "input a80b6e67); gen_scholar_record.py still reads repair/rows_v7_cwo24 and is not re-pointed in v9"),
    "A7": (CURED, "gen_proposals.py header amended and MCP-Ezek-004 evidence corrected (patch_gen_proposals_v9.py); only "
                  "that field changed; every adjudication null; --check MATCH"),
    "A8": (CARRIED, "not touched in v9"),
    "A9": (CARRIED, "not touched in v9: the 8 atlas holds stay final_deferred_review while the rows are final; an owner "
                    "disposition, carried into the close packet"),
    "B0": (CURED, "rows_v9_final P06-015 observed_substrate_signals: the out-of-span signals removed by measurement "
                  "(signals_v9.report.json, MEASURED on Ezek_oshb.txt); atlas M8-Ezek-079 regenerated from v9 and it is "
                  "the only atlas row that changed (observed_substrate_signals)"),
    **{"B%d" % i: (CARRIED, "not touched in v9") for i in (1, 2, 4, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19)},
    "B3": (CARRIED, "not touched in v9: the v9 author changed only P10-016 refs 12-14; the boundary_rationale count "
                    "('four' where the list gives five) stands"),
    "B7": (CARRIED, "grade unchanged (medium_low); the appended A0 ground states why the row holds that grade, but the "
                    "grade question itself is left for the campaign-end Fable review (OW-28)"),
    "B10": (CURED, "the atlas generator and checker now read rows_v9_final (all 138 candidate_review_complete), not "
                   "rows_v7_cwo24"),
    "B20": (CARRIED, "not touched in v9: the MCP-Ezek-002 wording (0.643 is not four fifths) stands; adjudication of every "
                     "proposal is deferred to the campaign-end Fable review (OW-28)"),
}
docket = {}
for L in ("A", "B"):
    for i, r in enumerate(fc[L][0]["residual"]):
        k = "%s%d" % (L, i)
        if k not in CLAIMS:
            raise SystemExit("REFUSED: no claim written for %s" % k)
        st, why = CLAIMS[k]
        if r["severity"] in ("high", "medium") and st != CURED:
            raise SystemExit("REFUSED: %s is %s and not claimed cured" % (k, r["severity"]))
        docket[k] = {"v1_severity": r["severity"], "row_or_artifact": r.get("row_or_artifact"), "class": r.get("class"),
                     "claim": st, "claim_basis": why}
if set(docket) != set(CLAIMS):
    raise SystemExit("REFUSED: claims name residuals that do not exist: %s" % sorted(set(CLAIMS) - set(docket)))


def dtype(gate_text, evidence):
    g, e = gate_text.lower(), evidence.lower()
    if "fable" in g and "stage-1" not in g:
        return "DEFERRED_OW28_FABLE_END_REVIEW", None
    if any(w in g for w in ("transcript", "stage-1", "stage1", "reconcile")):
        return "OWED_OW26", None
    if "final-check packet" in g and "owner" in e:
        return "OWNER_ACT_OW11", None
    if "postcheck" in g:
        return "CURED_BY_DELTA_VERDICT", "assembly_verdict"
    if "verdict fit_to_close" in g or "no medium/high residual" in g:
        return "CURED_BY_DELTA_VERDICT", "verdict"
    raise SystemExit("REFUSED: no disposition type fits %r" % gate_text)


STATE = {"OWED_OW26": "OWED, NOT MET (OW-26): the stage-1 transcript audit did not run; nothing here cures it",
         "DEFERRED_OW28_FABLE_END_REVIEW": "DEFERRED, NOT MET (OW-28): the gate needs a claude-fable-5-1 model; Fable "
                                           "reviews every book at the campaign's end",
         "OWNER_ACT_OW11": "OWNER'S ACT (OW-11): the orchestrator does not place it",
         "CURED_BY_DELTA_VERDICT": "cured only if BOTH v9 delta lanes return this verdict over rows_v9_final with no "
                                   "high or medium residual"}
disp = {}
for L in ("A", "B"):
    for g in fc[L][0]["close_gate_assessment"]:
        if g.get("met") is False:
            t, field = dtype(g["gate"], g.get("evidence", ""))
            disp["%s:%s" % (L, g["gate"])] = {"v1_evidence": g.get("evidence"), "type": t, "cured_by": field,
                                               "state": STATE[t]}
common = {"book": "Ezek", "built_by": "repair2/fixround_v9/" + Path(__file__).name,
          "builder_sha256": sha(Path(__file__).read_bytes()),
          "v1_final_checks": {L: {"file": "merged_close/" + land["lanes"][L]["files"]["final_check.json"]["durable"],
                                  "sha256": fc[L][1]} for L in ("A", "B")},
          "status": "CLAIMS for the delta lanes to judge; not judgements"}
out = {HERE / "delta_docket_v9.v1.json": {"schema": "ezek_delta_docket.v1", **common, "entries": docket},
       HERE / "v1_unmet_gate_dispositions.v1.json": {"schema": "ezek_v1_unmet_gate_dispositions.v1", **common,
                                                      "types": STATE, "entries": disp}}
res = {}
for p, obj in out.items():
    b = (json.dumps(obj, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    if p.exists() and p.read_bytes() != b:
        raise SystemExit("REFUSED: %s exists with different bytes" % p.name)
    if not p.exists():
        p.write_bytes(b)
    res[p.name] = sha(b)
print(json.dumps({"written": res, "docket": {k: v["claim"] for k, v in docket.items() if v["claim"] != CARRIED},
                  "carried": sum(v["claim"] == CARRIED for v in docket.values()),
                  "dispositions": {k[:60]: (v["type"], v["cured_by"]) for k, v in disp.items()}},
                 ensure_ascii=False, indent=1))
