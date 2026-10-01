#!/usr/bin/env python3
"""Receipts and cycle-log entry for the final-check fix wave and its follow-on.

The f02 receipt records something a receipt usually does not: the attempt CURED every ordered residual and INSTALLED
a new defect while doing it. Both go in the same record, because a receipt that showed only the seven cures would
read as an unqualified success and the eighth fact is the one a later reader needs. The catcher field names what
actually caught it - the post-apply re-scan and the validator suite, not the author's own self-check, whose list did
not include the arm that would have found it.

The author's honest E-19 self-report is carried verbatim: an attempted listing that errored before observing
anything. A self-reported near-miss is recorded exactly as reported and is not upgraded into a breach.
Usage: _fcfix_receipts.py"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE / "spot" / "lam_fix_attempt_receipts.jsonl"
LOG = HERE / "freeze" / "CYCLE_STATE.md"
NL = "\n"

E19 = ("One early command chained an ls -la against the shared SP/Lam/tools and SP/Lam directories using backslash "
       "Windows paths; Git Bash mangled the escaping and the command errored (exit 2, 'No such file or directory') "
       "before any directory was actually listed or its contents observed. No shared-directory listing succeeded, "
       "the pattern was not retried, and every subsequent file access used only exact paths named in the launch "
       "file, the briefs, or TOOLKIT.md's own data/tool inventory.")


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    now = datetime.now(timezone.utc).isoformat()
    orders = HERE / "spot" / "orders_fix_02.json"
    out = HERE / "spot" / "fix_02.jsonl"
    rep = json.load(open(HERE / "_apply_fcfix_report.json", encoding="utf-8-sig"))

    rec = {
        "schema": "m8_attempt_receipt.v1", "lane": "lam_fcfix_round", "agent": "f02",
        "attempt_id": "lam_fcfix_f02_a1", "corrects": None, "model": "claude-sonnet-5",
        "effort": "ORDERED high, NOT VERIFIED (no runtime effective-effort evidence)",
        "producer": "fix author f02; cures the corpus-row residuals raised by the OW-6 stage-2 final checker "
                    "against the assembled corpus, after the second postcheck had passed",
        "catcher": "_apply_micro.py guarded apply (parametrised globs) + the post-apply _cwo_scan.py re-scan over "
                   "rows_v10 + the full validator suite over rows_v10 + the follow-on round f03 + a FRESH OW-6 "
                   "stage-2 final check by a different fable attempt",
        "role_separation": "the fix author is not the checker that raised the residuals and is not the checker that "
                           "will verify the cures",
        "orders_file": "spot/orders_fix_02.json", "orders_sha256": sha(orders),
        "output_file": "spot/fix_02.jsonl", "output_sha256": sha(out),
        "base": "rows_v9.jsonl", "out_corpus": "rows_v10.jsonl",
        "out_corpus_sha256": rep.get("out_sha256"),
        "rows_ordered": 7, "rows_emitted": 7, "apply_status": rep.get("status"),
        "changed_fields_histogram": rep.get("changed_fields_histogram"),
        "immutable_drift": "none - verified field-by-field against rows_v9 before the apply",
        "cures_verified_by_the_author": ["ngram7 gate GREEN", "NFD dry-run ok=143 fixed=0 defects=0",
                                         "check_web_quotes 72 quotes flag_count=0", "tiling 154/154 GREEN"],
        "SECOND_GENERATION_DEFECT_INSTALLED": {
            "row": "P02-001",
            "what": "the cure that disclosed the held-open persona question wrote the bare universal 'never "
                    "decided'; CWO-2 bans undampened absolutes and check_universals flags them",
            "evidence": "rows_v9 universals GREEN and CWO-2 exact arm 0; rows_v10 universals FLAGS 1 and CWO-2 "
                        "exact arm 1, both naming the same sentence",
            "caught_by": "the post-apply re-scan and the validator suite - NOT the author's self-check",
            "why_the_self_check_missed_it": "the fix brief's self-check list did not include check_universals, and "
                                            "a prose cure writes new prose that can carry an absolute",
            "control_installed": "check_universals added to the fix brief's mandatory self-check list, with the "
                                 "reason stated in the brief",
            "fault": "partial author, partial brief: the cure was right in substance and wrong in form, and the "
                     "brief did not ask for the check that would have caught it",
            "record": "spot/second_generation_catch_02.v1.json",
            "ordered_for_cure": "spot/orders_fix_03.json (follow-on round f03)"},
        "items_reported_out_of_scope_by_the_author": [
            "P01-007's proposed cure also asked for a corpus-wide-order form-class disposition to be re-recorded "
            "and a discrepancy note appended to the boss ruling grounds; the author correctly reported both as "
            "outside a fix author's one-file scope rather than silently skipping or wrongly attempting them"],
        "e19_selfreported": E19,
        "e19_orchestrator_assessment": "recorded as reported: an attempted listing that errored before observing "
                                       "anything is a near-miss, not a breach, and is not upgraded into one. The "
                                       "self-report itself is the behaviour the affirmative line asks for.",
        "tokens_reported": 271049, "tool_uses": 34, "duration_ms": 805018,
        "tokens_note": "from the runtime task notification, not extracted from a transcript",
        "kill_events": [], "recorded_at": now}

    LANE.parent.mkdir(parents=True, exist_ok=True)
    lines = [l for l in LANE.read_text(encoding="utf-8").splitlines() if l.strip()] if LANE.is_file() else []
    lines = [l for l in lines if json.loads(l).get("attempt_id") != rec["attempt_id"]]
    lines.append(json.dumps(rec, ensure_ascii=False))
    LANE.write_text("".join(l + NL for l in lines), encoding="utf-8", newline=NL)

    entry = ["",
             f"## FINAL-CHECK FIX WAVE {datetime.now(timezone.utc).strftime('%Y-%m-%d')} (session dce0b6e2) -> rows_v10.jsonl",
             "- the OW-6 stage-2 final checker returned not_fit_to_close with 14 residuals (0 high, 5 medium, 9 low)",
             "  and escalated one question to the owner. 7 of the residuals were corpus rows; the rest were records",
             "  and are cured in the entries above.",
             f"- fix author lam_fcfix_f02_a1 (claude-sonnet-5): 7 rows ordered, 7 emitted, guarded apply GREEN ->",
             f"  rows_v10.jsonl (sha256 {str(rep.get('out_sha256'))[:16]}...), 26 rows, tiling GREEN, exactly one",
             "  field changed per row and no drift on any immutable field.",
             "- SECOND-GENERATION DEFECT INSTALLED AND CAUGHT: the P02-001 cure disclosed the held-open persona",
             "  question with the bare universal 'never decided'. rows_v9 had universals GREEN and CWO-2 at 0; rows_v10",
             "  has one flag on each arm, both naming that sentence. Caught by the post-apply re-scan and the",
             "  validator suite, NOT by the author's self-check - whose list did not include check_universals.",
             "  Recorded in spot/second_generation_catch_02.v1.json; check_universals is now mandatory in FIX_BRIEF.md.",
             "- also ordered into the follow-on: boss ruling B3-1's never-conflated sentence on P02-006, which f02",
             "  never received because the orders were amended after it launched (disclosed above).",
             "- follow-on round f03 ordered over rows_v10: 2 rows, 2 items, both medium.",
             ""]
    pre = LOG.read_bytes()
    body = pre if pre.endswith(b"\n") else pre + b"\n"
    LOG.write_bytes(body + NL.join(entry).encode("utf-8"))
    assert LOG.read_bytes().startswith(body), "log preimage not intact"

    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"receipt_written": str(LANE), "receipts_in_file": len(lines),
                      "lane_sha16": hashlib.sha256(LANE.read_bytes()).hexdigest()[:16],
                      "log_appended": True,
                      "log_sha16": hashlib.sha256(LOG.read_bytes()).hexdigest()[:16]}, indent=1))


if __name__ == "__main__":
    main()
