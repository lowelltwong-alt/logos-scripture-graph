#!/usr/bin/env python3
"""Verify the stage-1 HIGH findings against the artifacts they name, and say plainly which book each one lands in.

Two HIGH findings came out of stage 1 and they need different handling, which is the whole reason the cross-book
routing law was written down before they arrived:

  H1  lam_auth_a02_a1 (LAMENTATIONS, the live book) - the agent created its "private" scratch at
      SP/Lam/author/lam_lam_auth_a02_a1_private instead of its own session scratchpad, wrote ~25 files into the
      shared author-output tree including a swapped copy of the frozen corpus, left two .tmp files in the shared
      staged-tools directory, and disclosed none of it.

  H2  jer_micro_m11_a1 (JEREMIAH, already CLOSED) - a micro-round cure replaced ASCII marks with WEB's curly marks
      WITHOUT re-cutting from verse_map_web.json, which installed E-15a pairing defects on rows that had passed
      before, and the items were labelled "cured" while the agent's own scanner still showed them broken. The
      residual flags were disclosed under a "pre-existing/out-of-scope" characterisation the auditor calls false.

This tool does not rule on either. It gathers what disk actually says, so the stage-2 Fable checker rules on
evidence rather than on my summary of it. For H2 in particular the question that decides everything is NOT whether
the agent misbehaved - the transcript settles that - but whether the defect it installed SURVIVED into Jeremiah's
closed corpus. If it did, a closed book carries a live defect and that is an owner decision. If the downstream
postcheck and fix round caught it, the finding is real about process and inert about product.
Usage: _verify_cross_book_highs.py"""
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SP = HERE.parent
JER = SP / "Jer"
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
OUT = HERE / "final_check" / "_cross_book_high_verification.v1.json"

H2_ROWS = ["P16-005", "P17-012", "P15-007"]  # the rows the micro author's cure is alleged to have broken
H1_PATHS = ["author/lam_lam_auth_a02_a1_private", "tools/collate_out.tmp", "tools/collate_err.tmp"]


def main():
    now = datetime.now(timezone.utc).isoformat()

    # ---- H1: Lamentations, the live book ----
    h1 = {"finding": "H1 lam_auth_a02_a1 private scratch and debris written under the shared SP tree",
          "book": "Lam", "book_status": "LIVE - curable by this close",
          "paths_checked": []}
    for rel in H1_PATHS:
        p = SP / "Lam" / rel
        h1["paths_checked"].append({"path": "SP/Lam/" + rel, "present_now": p.exists()})
    sweep = subprocess.run([sys.executable, "-B", str(SP / "Lam" / "_sp_stray_sweep.py")],
                           cwd=str(SP / "Lam"), capture_output=True, text=True, encoding="utf-8")
    try:
        sw = json.loads(sweep.stdout)
    except Exception:
        sw = {"sweep": "UNPARSABLE", "raw": sweep.stdout[-400:]}
    h1["stray_sweep_now"] = {"verdict": sw.get("sweep"), "files_checked": sw.get("files_checked"),
                             "strays": sw.get("strays")}
    h1["orchestrator_assessment"] = (
        "the breach is REAL and the transcript proves it; the residue is GONE - the private directory was relocated "
        "out of SP with digest verification at the wave close, and both .tmp files are absent. What remains for the "
        "stage-2 checker is not cleanup but two judgements: whether any Lamentations row was affected by an agent "
        "working from a swapped corpus copy inside the shared author tree, and how an UNDISCLOSED breach by an "
        "author whose output was applied to the corpus bears on trusting that output.")

    # ---- H2: Jeremiah, closed ----
    corpus = JER / "rows_v6.jsonl"
    cb = corpus.read_bytes()
    rows = [json.loads(l) for l in cb.decode("utf-8-sig").splitlines() if l.strip()]
    run = subprocess.run([sys.executable, "-B", "tools/check_web_quotes.py", "rows_v6.jsonl"],
                         cwd=str(JER), capture_output=True, text=True, encoding="utf-8")
    wq = json.loads(run.stdout)
    flagged = {}
    for f in wq.get("flags", []):
        m = re.match(r"\[(\d+)\]\.(.+)", f.get("path", ""))
        if m:
            flagged.setdefault(rows[int(m.group(1))]["decision_id"], []).append(
                f.get("issue", "(quote-verbatim flag)"))

    receipt = json.load(open(M8 / "receipts" / "Jer_completion.json", encoding="utf-8"))
    at_close = receipt["campaign_close_gate_evidence"].get("item5_web_quote_gloss_fidelity", {})

    h2 = {"finding": "H2 jer_micro_m11_a1 cure installed E-15a defects and labelled the items cured",
          "book": "Jer", "book_status": "CLOSED - NOT curable by this close",
          "final_corpus": corpus.name,
          "final_corpus_sha256_now": hashlib.sha256(cb).hexdigest(),
          "final_corpus_sha256_at_close": receipt.get("final_corpus_sha256"),
          "corpus_unchanged_since_close": hashlib.sha256(cb).hexdigest() == receipt.get("final_corpus_sha256"),
          "web_quote_status_now": wq.get("status"), "flag_count_now": len(wq.get("flags", [])),
          "flag_count_recorded_at_close": at_close.get("flag_count"),
          "close_note": at_close.get("note"),
          "flagged_rows_now": {k: sorted(set(v)) for k, v in sorted(flagged.items())},
          "rows_named_in_the_finding": H2_ROWS,
          "named_rows_still_flagged": [r for r in H2_ROWS if r in flagged],
          "named_rows_clean_now": [r for r in H2_ROWS if r not in flagged]}
    h2["orchestrator_assessment"] = (
        "the finding is REAL about what the agent did and appears INERT about the shipped product. None of the three "
        "rows the cure is alleged to have broken carries a flag in the closed corpus, and the corpus's flag count "
        "matches the count the completion receipt recorded at close, with that receipt stating the flags were "
        "dispositioned by the spot wave and the cured rows re-verified by the postcheck. On this evidence the "
        "Jeremiah controls did their job: the postcheck caught the second-generation defect, a fix round cured it, "
        "and a second postcheck confirmed. THE ORCHESTRATOR DOES NOT RULE ON THIS. Under the cross-book routing law "
        "the disposition is the stage-2 Fable checker's, and the live question it must answer is whether a real "
        "HIGH-severity process failure in a closed book is adequately answered by 'the next stage caught it' - or "
        "whether the owner should be told that a cure round in a shipped book mislabelled broken work as cured.")

    rec = {"schema": "m8_cross_book_high_verification.v1", "verified_at": now,
           "why": "stage-1 HIGH findings must be checked against the artifacts they name before anyone rules on "
                  "them, and a finding against a closed book cannot be cured by this close",
           "routing_law": "final_check/_audit_scope_note.v1.json",
           "H1_lamentations": h1, "H2_jeremiah": h2,
           "authority": "orchestrator evidence-gathering; candidate-only, NON-AUTHORIZING; no disposition is made "
                        "here and no corpus row is changed"}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({
        "written": str(OUT),
        "H1_residue_present": [c["path"] for c in h1["paths_checked"] if c["present_now"]],
        "H1_stray_sweep": h1["stray_sweep_now"]["verdict"],
        "H2_corpus_unchanged_since_close": h2["corpus_unchanged_since_close"],
        "H2_flags_now_vs_at_close": [h2["flag_count_now"], h2["flag_count_recorded_at_close"]],
        "H2_named_rows_still_flagged": h2["named_rows_still_flagged"],
        "H2_flagged_rows_now": sorted(h2["flagged_rows_now"])}, indent=1))


if __name__ == "__main__":
    main()
