#!/usr/bin/env python3
"""Correct the producer model on the receipts I reconstructed, and disclose HOW the error was made.

THE ERROR IS MINE AND IT IS AN HONESTY ERROR, not a clerical one. When I wrote the fourteen missing receipts I put
in each one:

    "effort": "ORDERED (per the lane's launch record), NOT VERIFIED"

I did not consult any launch record. I inferred each attempt's model from what a lane of that kind usually runs -
review lanes opus, author lanes sonnet - and wrote a field that cites a source I never opened. Five of the fourteen
are wrong: the boss attempt is claude-fable-5-1 (not opus), two spot lanes are claude-sonnet-5 (not opus), and two
sidecar attempts are claude-haiku-4-5 (not sonnet). The launch record existed the whole time, in the launch map the
transcript manifest was built from, three commands away.

The boss label is load-bearing, which is why the stage-2 checker scored this medium rather than low: ruling B3-1
narrowed a corpus-wide order, and under OW-6 that ruling is valid only from the Fable boss. A receipt saying the
boss attempt ran on opus would, taken at face value, put the validity of a live corpus-wide-order narrowing in
question. The ruling is in fact valid - the packet's own header, its reasoning record and the cycle log all say
claude-fable-5-1, and the manifest agrees - but that is three records correcting my one, not my record being right.

What makes this worse than an ordinary mistake is the shape: a fabricated provenance citation is exactly the
class ("fabricated_evidence: a digit or label asserted without the read that would establish it") that this book's
transcript audit raised against four subagents. I wrote the same defect into the receipts that record their work.

The receipts are NOT rewritten. This appends the correction beside them, names the record I should have read, and
states plainly that the original field cited a source that was not consulted.
Usage: _amend_reconstructed_models.py [--apply]"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAN = HERE / "transcript_manifest.v2.json"
AMEND = HERE / "final_check" / "receipt_amendments.v1.jsonl"
LOG = HERE / "freeze" / "CYCLE_STATE.md"
NL = "\n"

WROTE = {"lam_spot_S1_a1": "claude-opus-5", "lam_spot_S2_a1": "claude-opus-5", "lam_spot_S3_a1": "claude-opus-5",
         "lam_spot_S4_a1": "claude-opus-5", "lam_spot_S5_a1": "claude-opus-5",
         "lam_micro_m01_a1": "claude-sonnet-5", "lam_micro_m02_a1": "claude-sonnet-5",
         "lam_fix_f01_a1": "claude-sonnet-5", "lam_postcheck_01_a1": "claude-opus-5",
         "lam_postcheck_02_a1": "claude-opus-5", "lam_sidecar_1_a1": "claude-sonnet-5",
         "lam_sidecar_2_a1": "claude-sonnet-5", "lam_sidecar_corr_a1": "claude-sonnet-5",
         "lam_boss_b3_a1": "claude-opus-5"}


def main():
    apply = "--apply" in sys.argv
    man = json.load(open(MAN, encoding="utf-8"))
    truth = {e["attempt_id"]: e.get("model") for e in man["mapped_transcripts"]}

    rows = []
    for aid, mine in sorted(WROTE.items()):
        real = truth.get(aid)
        rows.append({"attempt_id": aid, "recorded_by_me": mine, "launch_record_says": real,
                     "correct": mine == real})
    wrong = [r for r in rows if not r["correct"]]

    rec = {"schema": "m8_receipt_amendment.v1", "amendment_id": "reconstructed_receipt_models",
           "recorded_at": datetime.now(timezone.utc).isoformat(),
           "raised_by": "the fresh OW-6 stage-2 final checker (claude-fable-5-1), attempt lam_final_check_02_a1",
           "author_of_the_error": "orchestrator (claude-opus-5)",
           "severity": "medium",
           "what_i_did": "when writing the fourteen reconstructed receipts I recorded each attempt's model as "
                         "'ORDERED (per the lane's launch record)' WITHOUT CONSULTING ANY LAUNCH RECORD. I inferred "
                         "the model from what a lane of that kind usually runs and wrote a field citing a source I "
                         "never opened.",
           "why_it_is_worse_than_clerical": "a fabricated provenance citation is the same class - a label asserted "
                                            "without the read that would establish it - that this book's transcript "
                                            "audit raised against four subagents. I wrote that defect into the "
                                            "receipts recording their work.",
           "the_record_i_should_have_read": str(MAN) + " (built from the launch map, which carries each attempt's "
                                                       "ordered model)",
           "load_bearing_case": "lam_boss_b3_a1. Ruling B3-1 narrowed a corpus-wide order, and under OW-6 a boss "
                                "ruling is valid only from the Fable boss. My receipt said claude-opus-5. The "
                                "ruling IS valid - the packet header, its reasoning record, the cycle log and the "
                                "manifest all say claude-fable-5-1 - but that is three records correcting mine, not "
                                "mine being right.",
           "corrections": rows, "wrong_count": len(wrong), "total_checked": len(rows),
           "originals_rewritten": False,
           "why_not_rewritten": "the receipts record what I believed when I wrote them; editing them to say "
                                "something else would erase the evidence that the belief was wrong, and this "
                                "amendment is the only thing that shows a provenance field was once fabricated",
           "control": "a receipt that cites a source must be generated FROM that source. The reconstruction tool "
                      "now reads the model out of the manifest rather than taking it from a hand-written table."}

    sys.stdout.reconfigure(encoding="utf-8")
    if not apply:
        print(json.dumps({"dry_run": True, "wrong": len(wrong), "checked": len(rows),
                          "wrong_rows": wrong}, indent=1))
        return 0

    with open(AMEND, "a", encoding="utf-8", newline=NL) as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    entry = ["",
             f"## RECONSTRUCTED-RECEIPT MODEL CORRECTION {datetime.now(timezone.utc).strftime('%Y-%m-%d')} (session dce0b6e2)",
             "- the fourteen receipts I reconstructed recorded each attempt's model as 'ORDERED (per the lane's launch",
             "  record)'. I DID NOT CONSULT ANY LAUNCH RECORD. I inferred the model from what a lane of that kind",
             f"  usually runs. {len(wrong)} of {len(rows)} are wrong:"]
    for r in wrong:
        entry.append(f"    {r['attempt_id']:22} I wrote {r['recorded_by_me']:18} launch record says {r['launch_record_says']}")
    entry += [
        "- the load-bearing one is lam_boss_b3_a1: its ruling B3-1 narrowed a corpus-wide order, and under OW-6 that",
        "  is valid only from the Fable boss. The ruling IS valid - the packet header, its reasoning record, the log",
        "  and the manifest all say claude-fable-5-1 - but that is three records correcting mine.",
        "- this is the SAME defect class the transcript audit raised against four subagents: a label asserted without",
        "  the read that would establish it. I wrote it into the receipts that record their work.",
        "- correction appended to final_check/receipt_amendments.v1.jsonl; the receipts are NOT rewritten, because",
        "  the amendment is the only record that a provenance field was ever fabricated.",
        "- FOUND BY the fresh stage-2 final checker, not by me.",
        ""]
    pre = LOG.read_bytes()
    body = pre if pre.endswith(b"\n") else pre + b"\n"
    LOG.write_bytes(body + NL.join(entry).encode("utf-8"))
    assert LOG.read_bytes().startswith(body), "log preimage not intact"

    print(json.dumps({"status": "AMENDED", "wrong": len(wrong), "checked": len(rows),
                      "amendments_sha16": hashlib.sha256(AMEND.read_bytes()).hexdigest()[:16],
                      "log_appended": True}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
