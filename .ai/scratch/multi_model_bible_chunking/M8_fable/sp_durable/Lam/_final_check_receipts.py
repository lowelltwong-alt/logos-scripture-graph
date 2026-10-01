#!/usr/bin/env python3
"""Attempt receipts for the OW-6 final-check lane, INCLUDING the wave that was stopped.

A stopped attempt is part of the record. Recording only the wave that succeeded would leave a receipt file implying
the audit ran once and cleanly, which is not what happened: four claude-fable-5-1 auditors were launched against a
slice set that mixed 18 orchestrator shell outputs in with the real subagent transcripts, and were stopped about ten
minutes in when the orchestrator found its own defect. No deliverable from that wave was written or used.

Model and effort are ORDERED, NOT VERIFIED: the runtime exposes no effective-effort evidence, so the receipt says
what was ordered and says that it says only that.
Usage: _final_check_receipts.py [--out final_check/lam_final_check_attempt_receipts.jsonl]"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SC = HERE.parent.parent
A = sys.argv[1:]
OUT = HERE / (A[A.index("--out") + 1] if "--out" in A else "final_check/lam_final_check_attempt_receipts.jsonl")

EFFORT = "ORDERED high, NOT VERIFIED (no runtime effective-effort evidence)"
CATCHER = ("_final_check_reconcile.py (assigned vs reported transcripts, disjointness, union against the manifest, "
           "byte arithmetic) + the OW-6 close gate in _close_book.py + the stage-2 Fable final checker, which is a "
           "different agent from every stage-1 auditor")


def main():
    plan = json.load(open(SC / "_lam_final_check_stage1_launch_msgs.json", encoding="utf-8"))
    man_p = HERE / "transcript_manifest.v2.json"
    man = json.load(open(man_p, encoding="utf-8"))
    now = datetime.now(timezone.utc).isoformat()
    rows = []

    for aid in sorted(plan):
        rows.append({
            "schema": "m8_attempt_receipt.v1", "lane": "lam_final_check_stage1", "agent": aid.split("_")[2],
            "attempt_id": aid, "wave": 1, "corrects": None, "model": "claude-fable-5-1", "effort": EFFORT,
            "producer": "OW-6 stage-1 transcript auditor (claude-fable-5-1)",
            "catcher": CATCHER, "role_separation": "no stage-1 auditor is the stage-2 final checker",
            "outcome": "STOPPED BY THE ORCHESTRATOR before any deliverable was written",
            "kill_events": [{"when": now, "by": "orchestrator (claude-opus-5)",
                             "reason": "the slice this attempt was given described 29 files as subagent transcripts; "
                                       "only 11 were. The other 18 were captured orchestrator shell output that a "
                                       "bare glob('*.output') had swept into the manifest and the durable mirror. "
                                       "The attempt was stopped rather than allowed to produce coverage digits over "
                                       "an evidence set that was 62% the wrong kind of file by count.",
                             "deliverable_written": False, "any_output_used_downstream": False}],
            "finding": "SP/campaign/finding_orchestrator_shell_output_conflation.v1.json",
            "fault": "orchestrator, not the agent: the attempt was given a defective assignment",
            "recorded_at": now})

    for aid, spec in sorted(plan.items()):
        assigned = [l.strip()[2:l.strip().index(".output") + 7]
                    for l in spec["message"].split("\n")
                    if l.strip().startswith("- C:") and ".output" in l]
        rows.append({
            "schema": "m8_attempt_receipt.v1", "lane": "lam_final_check_stage1", "agent": aid.split("_")[2],
            "attempt_id": aid, "wave": 2, "corrects": f"{aid} (wave 1, stopped)", "model": "claude-fable-5-1",
            "effort": EFFORT,
            "producer": "OW-6 stage-1 transcript auditor (claude-fable-5-1); two-pass method - a mechanical pass "
                        "over 100% of the slice bytes, then close reading of the segments that pass flags",
            "catcher": CATCHER, "role_separation": "no stage-1 auditor is the stage-2 final checker",
            "slice": spec["slice"], "transcripts_assigned": len(assigned), "bytes_assigned": spec["bytes"],
            "transcripts": [Path(p).name for p in assigned],
            "read_source": "sp_durable/transcripts/<session>/ (the durable mirror), NOT the runtime tasks/ directory, "
                           "because the runtime deletes transcripts mid-session",
            "manifest": man_p.name, "manifest_sha256": hashlib.sha256(man_p.read_bytes()).hexdigest(),
            "output_file": "final_check/" + Path(spec["output"]).name,
            "attempts_with_no_transcript_at_all": len(spec.get("attempts_without_transcript", [])),
            "permanently_lost_transcripts": spec.get("lost_transcripts", []),
            "coverage_note": "the transcript evidence for this book is partial by construction: most attempts have no "
                             "transcript because the runtime never wrote one, and at least one written transcript was "
                             "deleted before it could be mirrored. The stage-2 checker states this in its verdict "
                             "rather than letting a clean-looking audit imply completeness.",
            "kill_events": [], "recorded_at": now})
        # the landing facts are read off the delivered packet, never from the agent's final message: a receipt that
        # records what an attempt SAID it did would repeat the very failure this lane exists to detect
        pkt = Path(spec["output"])
        r = rows[-1]
        if pkt.is_file():
            d = json.load(open(pkt, encoding="utf-8-sig"))
            fs = [f for t in d.get("per_transcript", []) for f in t.get("findings", [])]
            r["outcome"] = "LANDED"
            r["output_sha256"] = hashlib.sha256(pkt.read_bytes()).hexdigest()
            r["landed_digits"] = {
                "transcripts_reported": len(d.get("per_transcript", [])),
                "bytes_processed": d.get("bytes_processed"), "bytes_read_closely": d.get("bytes_read_closely"),
                "findings_total": len(fs),
                "high": sum(1 for f in fs if f.get("severity") == "high"),
                "medium": sum(1 for f in fs if f.get("severity") == "medium"),
                "low": sum(1 for f in fs if f.get("severity") == "low"),
                "undisclosed_law_breaches": sum(1 for f in fs if f.get("class") == "law_breach"
                                                and not f.get("self_disclosed")),
                "positive_self_corrections": sum(len(t.get("positive_self_corrections", []) or [])
                                                 for t in d.get("per_transcript", []))}
            r["reconciled_by"] = "_final_check_reconcile.py (assigned vs reported, disjointness, union, byte arithmetic)"
        else:
            r["outcome"] = "NOT LANDED at the time of writing"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"out": str(OUT), "receipts": len(rows), "wave1_stopped": sum(1 for r in rows if r["wave"] == 1),
                      "wave2_in_flight": sum(1 for r in rows if r["wave"] == 2),
                      "manifest_transcripts": len([e for e in man["mapped_transcripts"] + man["unmapped_transcripts"]
                                                   if e["bytes"] > 0]),
                      "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}, indent=1))


if __name__ == "__main__":
    main()
