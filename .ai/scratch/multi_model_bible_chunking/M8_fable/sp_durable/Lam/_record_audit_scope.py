#!/usr/bin/env python3
"""Record that the OW-6 stage-1 audit scope SPANS MORE THAN ONE BOOK, and what that means for findings.

The transcript manifest is labelled "book": "Lam" because it was built during the Lamentations cycle. That label is
accurate for the three mapped attempts and MISLEADING for the eight unmapped ones: the durable store holds every
subagent transcript this session produced, and this session also ran the tail of the Jeremiah cycle. Stage-1 auditors
have already identified Jeremiah lanes (jer_spot_S3_a1, jer_cwo_10_a1) among their assigned transcripts.

The manifest is NOT edited to say so. Its sha256 is pinned in the stage-1 attempt receipts as the input the auditors
were actually given, and rewriting a pinned input after the fact is how provenance dies. The correction is recorded
here instead, beside it, and is carried into the stage-2 launch message.

WHY IT MATTERS, and it matters more than a label: a finding against JEREMIAH cannot be cured by the LAMENTATIONS
close. Jeremiah is already closed. Such a finding has exactly three honest dispositions, and picking one is a
judgement the OW-6 boss makes, not the orchestrator:
  (a) it is real and material -> reopening a closed book is an owner decision, escalated with the OW-6 packet
  (b) it is real and immaterial -> recorded as a retained residual against the closed book, visible in its record
  (c) it is a false positive -> dismissed with the evidence that refutes it
What must NOT happen is the fourth path: a Jeremiah finding quietly counted as "dispositioned" by a Lamentations
close gate that has no power over Jeremiah's corpus. That would launder a defect in one book through the close of
another.
Usage: _record_audit_scope.py"""
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAN = HERE / "transcript_manifest.v2.json"
OUT = HERE / "final_check" / "_audit_scope_note.v1.json"


def main():
    man = json.load(open(MAN, encoding="utf-8"))
    mapped = [e for e in man["mapped_transcripts"] if e["bytes"] > 0]
    unmapped = man["unmapped_transcripts"]

    # what stage 1 has identified so far (packets that have landed); absent packets are simply not yet known
    identified = {}
    for p in sorted((HERE / "final_check").glob("transcript_audit_0*.json")):
        try:
            pk = json.load(open(p, encoding="utf-8-sig"))
        except Exception:
            continue
        for t in pk.get("per_transcript", []):
            aid = t.get("attempt_id") or ""
            identified[Path(t.get("transcript", "")).name] = {"attempt_id": aid, "lane": t.get("lane"),
                                                              "book": ("Jer" if aid.startswith("jer_")
                                                                       else "Lam" if aid.startswith("lam_")
                                                                       else "unknown"), "slice": pk.get("slice")}
    books = Counter(v["book"] for v in identified.values())
    for e in mapped:
        books[e["attempt_id"].split("_")[0].capitalize() if e["attempt_id"][:3] in ("lam", "jer") else "unknown"] += 0

    rec = {
        "schema": "m8_audit_scope_note.v1",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "manifest": MAN.name,
        "manifest_sha256": hashlib.sha256(MAN.read_bytes()).hexdigest(),
        "manifest_book_label": man["book"],
        "correction": "the manifest's book label is accurate for the mapped attempts and MISLEADING for the unmapped "
                      "ones; the durable store holds every subagent transcript this session produced, and this "
                      "session also ran the tail of the Jeremiah cycle",
        "manifest_not_edited_because": "its sha256 is pinned in the stage-1 attempt receipts as the input the "
                                       "auditors were actually given; rewriting a pinned input after the fact "
                                       "destroys the provenance the pin exists to protect",
        "mapped_attempts": [{"attempt_id": e["attempt_id"], "lane": e["lane"], "bytes": e["bytes"]} for e in mapped],
        "unmapped_transcripts": len(unmapped),
        "identified_by_stage1_so_far": identified,
        "book_spread_so_far": dict(books),
        "routing_law_for_cross_book_findings": {
            "problem": "a finding against JEREMIAH cannot be cured by the LAMENTATIONS close; Jeremiah is closed",
            "honest_dispositions": [
                "real and material -> reopening a closed book is an OWNER decision, escalated with the OW-6 packet "
                "(question, recommendation with reason, every alternative with pros and cons)",
                "real and immaterial -> recorded as a retained residual against the closed book, visible in its record",
                "false positive -> dismissed with the evidence that refutes it"],
            "forbidden": "counting a Jeremiah finding as 'dispositioned' by a Lamentations close gate that has no "
                         "power over Jeremiah's corpus; that launders a defect in one book through another's close",
            "who_decides": "the stage-2 claude-fable-5-1 final checker, as the OW-6 boss; not the orchestrator"},
        "authority": "orchestrator note; candidate-only, non-authorizing; no corpus row is affected"}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"written": str(OUT), "manifest_label": man["book"],
                      "identified_so_far": len(identified), "book_spread": dict(books)}, indent=1))


if __name__ == "__main__":
    main()
