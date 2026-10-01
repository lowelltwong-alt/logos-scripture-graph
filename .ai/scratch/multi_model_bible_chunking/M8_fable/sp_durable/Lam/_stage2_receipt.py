#!/usr/bin/env python3
"""Append the stage-2 final-checker receipt to the OW-6 final-check lane, and record the stage-1 roll-up it inherits.

The stage-2 checker is the last review before the close and nothing downstream re-checks it, so its receipt has to
carry more than "it ran": what it was given, what the evidence base actually was, and what the stage-1 lane handed
it. Those inherited digits are computed here from the delivered packets, not copied from any agent's summary.

Appends to the existing lane receipts file. Rerunning replaces the stage-2 line only, so the record can be brought
up to date when the attempt lands without disturbing the eight stage-1 receipts already written.
Usage: _stage2_receipt.py"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SC = HERE.parent.parent
LANE = HERE / "final_check" / "lam_final_check_attempt_receipts.jsonl"
AID = "lam_final_check_01_a1"


def main():
    plan = json.load(open(SC / "_lam_final_check_stage2_launch_msgs.json", encoding="utf-8"))
    spec = plan[AID]
    now = datetime.now(timezone.utc).isoformat()

    # stage-1 roll-up, computed from the packets themselves
    packets = sorted((HERE / "final_check").glob("transcript_audit_0*.json"))
    fs, tr, bp, bc, pos = [], 0, 0, 0, 0
    for p in packets:
        d = json.load(open(p, encoding="utf-8-sig"))
        tr += len(d.get("per_transcript", []))
        bp += d.get("bytes_processed") or 0
        bc += d.get("bytes_read_closely") or 0
        for t in d.get("per_transcript", []):
            fs.extend(t.get("findings", []))
            pos += len(t.get("positive_self_corrections", []) or [])

    def by(sev): return sum(1 for f in fs if f.get("severity") == sev)

    def book_of(t_aid): return "Jer" if t_aid.startswith("jer_") else "Lam" if t_aid.startswith("lam_") else "unknown"

    per_book = {}
    for p in packets:
        d = json.load(open(p, encoding="utf-8-sig"))
        for t in d.get("per_transcript", []):
            b = book_of(t.get("attempt_id") or "")
            for f in t.get("findings", []):
                per_book.setdefault(b, {"high": 0, "medium": 0, "low": 0})
                per_book[b][f.get("severity", "low")] = per_book[b].get(f.get("severity", "low"), 0) + 1

    corpus = HERE / spec["corpus"] if (HERE / spec["corpus"]).is_file() else HERE / "rows_v9.jsonl"
    out_p = Path(spec["output"])

    rec = {
        "schema": "m8_attempt_receipt.v1", "lane": "lam_final_check_stage2", "agent": "final_check_01",
        "attempt_id": AID, "wave": 1, "corrects": None, "model": "claude-fable-5-1",
        "effort": "ORDERED high, NOT VERIFIED (no runtime effective-effort evidence)",
        "producer": "OW-6 stage-2 FINAL CHECKER (claude-fable-5-1); its verdict gates the close and nothing "
                    "downstream re-checks it",
        "catcher": "the hard close gate in _close_book.py, which asserts the model, the fit_to_close verdict, the "
                   "audited corpus digest, a disposition with a reason for every stage-1 high and medium, a stated "
                   "transcript_coverage block, and a GREEN stage-1 reconciliation",
        "role_separation": "distinct from every stage-1 auditor and from every author, reviewer and postchecker in "
                           "this book; it authored none of the work it reviews",
        "corpus_audited": corpus.name,
        "corpus_sha256": hashlib.sha256(corpus.read_bytes()).hexdigest(),
        "stage1_packets": [Path(p).name for p in spec["stage1_packets"]],
        "stage1_rollup_computed_here": {
            "packets": len(packets), "transcripts_reported": tr,
            "bytes_processed": bp, "bytes_read_closely": bc,
            "findings_total": len(fs), "high": by("high"), "medium": by("medium"), "low": by("low"),
            "undisclosed_law_breaches": sum(1 for f in fs if f.get("class") == "law_breach"
                                            and not f.get("self_disclosed")),
            "positive_self_corrections": pos, "by_book": per_book},
        "evidence_base_caveat": "the transcript evidence is partial by construction and the checker is required to "
                                "say so: most attempts have no transcript because the runtime never wrote one, one "
                                "written transcript was deleted before it could be mirrored, and an earlier launch "
                                "of stage 1 was stopped because 18 orchestrator shell outputs had been served as "
                                "subagent transcripts",
        "cross_book_scope": "the audited transcripts span Lamentations AND Jeremiah; Jeremiah is CLOSED and this "
                            "close cannot cure a finding against it. The routing law is "
                            "final_check/_audit_scope_note.v1.json and the disposition is the checker's, not the "
                            "orchestrator's",
        "questions_put_to_the_checker": ["evidence-retention window for the remaining books",
                                         "whether the OW-6c re-check scope needs re-stating now",
                                         "whether the orchestrator's own error records are complete and sufficient"],
        "output_file": "final_check/" + out_p.name,
        "kill_events": [], "recorded_at": now}

    if out_p.is_file():
        d = json.load(open(out_p, encoding="utf-8-sig"))
        res = d.get("residual", []) or []
        rec["outcome"] = "LANDED"
        rec["output_sha256"] = hashlib.sha256(out_p.read_bytes()).hexdigest()
        rec["landed"] = {"verdict": d.get("verdict"),
                         "residual_high": sum(1 for r in res if r.get("severity") == "high"),
                         "residual_medium": sum(1 for r in res if r.get("severity") == "medium"),
                         "residual_low": sum(1 for r in res if r.get("severity") == "low"),
                         "blocking": len(d.get("blocking", []) or []),
                         "stage1_dispositions": len(d.get("stage1_findings_disposition", []) or []),
                         "needs_human": (d.get("escalation") or {}).get("needs_human"),
                         "reconcile_verdict": (d.get("transcript_coverage") or {}).get("reconcile_verdict")}
    else:
        rec["outcome"] = "IN FLIGHT at the time of writing"

    lines = [l for l in LANE.read_text(encoding="utf-8").splitlines() if l.strip()]
    lines = [l for l in lines if json.loads(l).get("attempt_id") != AID]
    lines.append(json.dumps(rec, ensure_ascii=False))
    LANE.write_text("".join(l + "\n" for l in lines), encoding="utf-8", newline="\n")

    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"lane_file": str(LANE), "receipts": len(lines), "stage2_outcome": rec["outcome"],
                      "stage1_rollup": rec["stage1_rollup_computed_here"],
                      "lane_sha256": hashlib.sha256(LANE.read_bytes()).hexdigest()[:16]}, indent=1))


if __name__ == "__main__":
    main()
