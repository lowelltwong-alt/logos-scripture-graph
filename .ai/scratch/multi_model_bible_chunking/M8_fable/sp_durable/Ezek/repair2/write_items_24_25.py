#!/usr/bin/env python3
"""Close-gate items 24 (OW-18 provenance tiers) and 25 (OW-19 lens multiplicity): the evidence, measured.

WHAT THIS DOES NOT DO. It does not declare either item PASSED. Items 24 and 25 are judgements about whether a record
implies a provenance it does not hold and whether any unit group was reviewed by one lens; the orchestrator authored
the records under audit, so the verdict belongs to the blind lanes and, where they split, to the owner. This file
supplies the measurements a verdict needs, and names the one place where the measurement does not settle the question.

THE ITEM 25 FINDING THAT MATTERS. The dual-blind round covered the whole book - 145 of 145 rows, no sampling, and all
22 clusters carry both an LF and an OL execution. But the shipped set is 138 rows, and 8 of them carry decision ids
minted during the repair waves. Their TEXT sat inside a dual-blind cluster; their FINAL SEAMS were set afterwards and
seen only by waves that read the shipped rows. Item 25's own rule says a lane that reads the shipped chunking is
RETROFIT-AUDIT and does not count toward lens multiplicity. So those 8 rows are dual-blind on their text and
audit-only on their seam as shipped. Whether that satisfies "no unit group is reviewed by one lens" is a judgement,
stated here as an open question rather than resolved in the direction that closes the book.
"""
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
EZ = M8 / "sp_durable" / "Ezek"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ---- item 24: the tool that enforces the tier, run now rather than quoted from a past run -------------------------
gate = subprocess.run(["python", "_land_review_packet_ezek.py", "--selftest"], capture_output=True, text=True,
                      cwd=str(EZ))
g = json.loads(gate.stdout[gate.stdout.find("{"):])
prov = json.loads((EZ / "primaries_capture_provenance.v3.json").read_text(encoding="utf-8"))

# ---- item 25: lens count per cluster, measured from the capture index, and coverage against the SHIPPED rows ------
lanes = {}
for e in prov["executions"]:
    m = re.search(r"_pr_(LF|OL)_", str(e.get("execution_id", "")))
    if m:
        lanes.setdefault(e.get("cluster"), set()).add(m.group(1))
plan = json.loads((EZ / "review_clusters.json").read_text(encoding="utf-8"))
planned = set(r for c in plan["clusters"] for r in c["row_ids"])
ship = [json.loads(l) for l in (EZ / "repair" / "rows_v7_cwo24.jsonl").read_text(encoding="utf-8").splitlines()
        if l.strip()]
shipped_ids = set(s["decision_id"] for s in ship)
minted = sorted((s["decision_id"], s["span"], s.get("confidence")) for s in ship if s["decision_id"] not in planned)
retired = sorted(planned - shipped_ids)

out = {
    "schema": "ezek_close_items_24_25_evidence.v1",
    "book": "Ezek",
    "built_at": datetime.now(timezone.utc).isoformat(),
    "built_by": "orchestrator (claude-opus-5), session 910cbe15",
    "authority": ("EVIDENCE ONLY. The orchestrator authored the records these items judge, so it does not grade them. "
                  "The verdict is the blind lanes', and where they split, the owner's (OW-11, OW-19)."),

    "item_24_OW18_provenance_tiers": {
        "what_the_gate_is": ("the landing path measures the claim instead of trusting it: an EXTRACTED claim over an "
                             "empty or absent source is REFUSED, not annotated, and a self-authored durable carrier "
                             "must say SELF-AUTHORED CARRIER in its own note rather than be filed as a Layer A "
                             "runtime capture."),
        "gate": {"tool": "sp_durable/Ezek/_land_review_packet_ezek.py",
                 "sha256": sha(EZ / "_land_review_packet_ezek.py"),
                 "selftest_suites": g.get("selftest"), "vectors": g.get("vectors"),
                 "failed": g.get("failed"), "verdict": g.get("verdict"),
                 "tier": "MEASURED - this run, not a quoted past run"},
        "index": {"file": "sp_durable/Ezek/primaries_capture_provenance.v3.json",
                  "sha256": sha(EZ / "primaries_capture_provenance.v3.json"),
                  "executions_covered": prov.get("executions_covered"),
                  "packets_whose_digest_no_longer_matches_their_receipt":
                      prov["coverage_check"].get("packets_whose_digest_no_longer_matches_their_receipt"),
                  "records_not_disclosing_their_own_tier_COUNT":
                      len(prov["coverage_check"].get("records_not_disclosing_their_own_tier") or []),
                  "tier": "MEASURED (digests re-read at index build time)"},
        "the_back_catalogue_is_stated_not_silent": {
            "v3_supersedes": list((prov.get("supersedes") or {}).keys()),
            "known_imprecision_the_index_states_about_itself": prov.get("known_imprecision_stated_rather_than_hidden"),
            "how_to_read": ("the index carries its own defect rather than presenting a clean face: the first 30 "
                            "durable copies are all named layer_a_*, including two that were only TRANSCRIBED. The "
                            "filename overclaims; the record corrects it. That is the item working, not failing.")},
        "what_is_NOT_established_here": [
            "that every claim in every Ezekiel record carries its true tier - no tool measures the whole corpus of prose",
            "that the orchestrator's own summaries in this session carry tiers; those are chat, the weakest layer",
            "the two failed audit lanes of 2026-09-21 spent an UNRECOVERABLE amount, not zero (see the receipts)",
        ],
    },

    "item_25_OW19_lens_multiplicity": {
        "recorded_lens_count": {
            "carrier": "book_strategy/Ezek.md",
            "sha256": sha(M8 / "book_strategy" / "Ezek.md"),
            "clause": "FULL dual-blind primaries (LF + OL) over ALL rows in clusters of <=8",
            "count": 2, "coverage_declared": "ALL rows, no sampling",
            "reason_recorded": ("the plan's own coverage field states the reason: ruling Q8 compensation 1 - FULL "
                                "dual-blind coverage of every row, no sampling, adopted in place of a sampled round"),
            "tier": "EXTRACTED from the strategy and the ratified cluster plan",
            "item_25_requirement": "the per-book lens count AND its reason are recorded in the book strategy - both are"},
        "measured_lens_count_per_cluster": {
            "clusters": len(lanes),
            "distribution": {str(k): v for k, v in
                             sorted({n: sum(1 for s in lanes.values() if len(s) == n)
                                     for n in set(len(s) for s in lanes.values())}.items())},
            "clusters_with_fewer_than_two_lenses": [c for c, s in sorted(lanes.items()) if len(s) < 2],
            "tier": "MEASURED - counted from the capture index's own execution ids, not from the plan's intention",
            "means": "no cluster of the primaries round was seen by a single lens"},
        "coverage_against_the_SHIPPED_rows": {
            "planned_rows": plan.get("rows_total"), "shipped_rows": len(ship),
            "shipped_rows_whose_id_was_a_dual_blind_target": len(shipped_ids & planned),
            "shipped_rows_whose_id_was_minted_after_the_primaries_round": [m[0] for m in minted],
            "their_spans": {m[0]: m[1] for m in minted},
            "planned_ids_retired_before_shipping": retired,
            "tier": "MEASURED (id set intersection); the cause of the difference is INFERRED",
            "inference_and_its_basis": ("8 ids minted and 15 retired, net -7, which is exactly 145 minus 138, and each "
                                        "minted id sits in the same writer part as the retired ones around it. That "
                                        "pattern is what merges during repair look like. It is INFERRED, not measured: "
                                        "no file read here records the merge event itself."),
            "what_is_true_of_those_8_rows": ("their TEXT was inside a dual-blind cluster, because the round covered "
                                             "145 of 145 rows with no sampling and every verse of the book with it. "
                                             "Their FINAL SEAMS were set during repair and seen afterwards only by "
                                             "waves that read the shipped rows."),
            "why_that_is_not_a_technicality": ("item 25 says a lane that reads the shipped chunking is RETROFIT-AUDIT "
                                               "and does NOT count toward lens multiplicity, because blindness is an "
                                               "information barrier. On its own words, those 8 rows are dual-blind on "
                                               "text and audit-only on the seam as shipped.")},
        "the_third_lens_is_NOT_an_independent_third_voice": {
            "what_exists": "the OW-6b second independent Fable review of the section 7 regions",
            "why_it_does_not_count_as_decorrelated": ("the campaign's own canonical clause holds Anthropic-family "
                                                      "agreement to be ONE correlated voice. LF, OL and a Fable review "
                                                      "are the same family, so a 2-1 split among them is not a "
                                                      "majority verdict and must never be reported as one."),
            "what_would_count": "a different evidence base (versional/reception), a different model family, or a human lens",
            "status": "the decorrelated third lens remains an OWNER packet (OW-6), unspent and not claimed here",
            "tier": "EXTRACTED from the close gate's own text plus the strategy"},
        "OPEN_QUESTION_FOR_THE_LANES_AND_THE_OWNER": (
            "does a book in which 130 of 138 shipped rows are dual-blind at their own identity, all 138 dual-blind in "
            "text, and 8 audit-only at their final seam, satisfy 'NO UNIT GROUP IS REVIEWED BY ONE LENS'? The "
            "orchestrator does not answer it. The two readings lead to different closes: on the strict reading those 8 "
            "seams owe a blind re-derivation by a lane that never sees them; on the text reading the item is met and "
            "the 8 are recorded as a stated limit. Neither reading is adopted here."),
    },

    "limit": ("this file measures. It does not grade, and nothing in it should be read as item 24 or item 25 having "
              "PASSED. Two blind audit lanes were launched on 2026-09-21 to grade items 20-23 and both failed at "
              "launch on the account's five-hour usage window, so no independent grade of any close-gate item exists "
              "yet; the close gate stays owed."),
}

p = EZ / "ezek_close_items_24_25_evidence.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"wrote": p.name, "bytes": p.stat().st_size, "sha256": sha(p),
                  "item_24_gate": g.get("verdict"), "item_24_vectors": g.get("vectors"),
                  "clusters": len(lanes), "single_lens_clusters": [c for c, s in lanes.items() if len(s) < 2],
                  "shipped_dual_blind_by_id": len(shipped_ids & planned), "of": len(ship),
                  "minted_after_primaries": [m[0] for m in minted]}, ensure_ascii=False, indent=1))
