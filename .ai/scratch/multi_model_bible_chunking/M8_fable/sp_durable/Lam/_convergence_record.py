#!/usr/bin/env python3
"""Track what successive final checks actually find, so a close decision rests on the trajectory rather than on
whoever runs out of patience first.

WHY THIS EXISTS: this book has now had several independent Fable final checks, each returning not_fit_to_close, and
a fair question is whether that is convergence or a treadmill. Both look identical from inside a single round. The
difference is visible only across rounds, and only if someone writes the numbers down:

  - CONVERGENCE looks like: severity falling, corpus-text findings falling, and each round's findings being NEW
    things rather than the previous round's findings unfixed.
  - A TREADMILL looks like: the same class recurring, or the count staying flat while the subject drifts, or - the
    specific risk here - each round auditing the records the PREVIOUS round's fixes created, forever.

The third of those is real and this tool measures it directly: it separates residuals against the CORPUS from
residuals against RECORDS, and within records, those against records created during the fix rounds themselves.

It also records what an honest close needs: the campaign's gate says fit_to_close requires no high or medium
residual. Lows may be RETAINED with a reason, as Jeremiah closed with seven. So the question a close turns on is not
"are there findings" but "is any of them high or medium, and is the low tail understood".
Usage: _convergence_record.py [--write]"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
FC = HERE / "final_check"
OUT = FC / "_convergence.v1.json"
ROW = re.compile(r"^P\d{2}-\d{3}\b")
FIXROUND_RECORDS = ("ruling_execution_ledger", "receipt_amendments", "transcript_manifest.v3",
                    "finding_transcript_decay.v2", "cwo_parity.rows_v", "second_generation_catch",
                    "_convergence", "ruling_ground_notes", "cwo1_predicate_label")


def classify(subject):
    s = str(subject)
    if ROW.match(s.strip()):
        return "corpus_row"
    if any(k in s for k in FIXROUND_RECORDS):
        return "record_created_by_a_fix_round"
    return "record_pre_existing"


def main():
    rounds = []
    for p in sorted(FC.glob("final_check_0*.json")):
        try:
            d = json.load(open(p, encoding="utf-8-sig"))
        except Exception:
            continue
        res = d.get("residual") or []
        by_sev = {s: sum(1 for r in res if r.get("severity") == s) for s in ("high", "medium", "low")}
        by_kind = {}
        for r in res:
            by_kind[classify(r.get("row_or_artifact"))] = by_kind.get(classify(r.get("row_or_artifact")), 0) + 1
        rounds.append({"packet": p.name, "attempt": d.get("attempt_id"), "corpus": d.get("corpus"),
                       "verdict": d.get("verdict"), "residuals": len(res), **by_sev,
                       "by_subject": by_kind,
                       "byte_verifications": (d.get("digits") or {}).get("byte_verifications"),
                       "refuted": (d.get("digits") or {}).get("refuted")})

    def series(k): return [r.get(k, 0) for r in rounds]
    corpus_series = [r["by_subject"].get("corpus_row", 0) for r in rounds]
    fixrec_series = [r["by_subject"].get("record_created_by_a_fix_round", 0) for r in rounds]

    assess = []
    if rounds:
        if series("high") == [0] * len(rounds):
            assess.append("no round has found a HIGH residual against the corpus")
        if len(rounds) > 1 and series("medium")[-1] < series("medium")[0]:
            assess.append(f"medium residuals are falling: {series('medium')}")
        if len(rounds) > 1 and corpus_series[-1] <= corpus_series[0]:
            assess.append(f"corpus-row findings are not growing: {corpus_series}")
        if len(rounds) > 1 and fixrec_series[-1] > fixrec_series[0]:
            assess.append(f"CAUTION: findings against records the fix rounds themselves created are growing "
                          f"({fixrec_series}); this is the treadmill risk and it is why the low tail rises even as "
                          f"severity falls")

    res = {"schema": "m8_convergence_record.v1", "book": "Lam",
           "built": datetime.now(timezone.utc).isoformat(),
           "why": "successive not_fit verdicts look the same whether a book is converging or circling; the "
                  "difference is only visible across rounds and only if the numbers are written down",
           "rounds": rounds,
           "series": {"residuals": series("residuals"), "high": series("high"), "medium": series("medium"),
                      "low": series("low"), "corpus_row_findings": corpus_series,
                      "findings_against_fix_round_records": fixrec_series},
           "assessment": assess,
           "what_a_close_actually_requires": "the campaign gate requires NO high or medium residual. Lows may be "
                                             "RETAINED with a reason - Jeremiah closed with seven. So the close "
                                             "question is not 'are there findings' but 'is any high or medium, and "
                                             "is the low tail understood and recorded'.",
           "who_decides": "the OW-6 stage-2 final checker, on the corpus in front of it. This record is evidence "
                          "for that decision and is not itself a verdict.",
           "authority": "orchestrator record; candidate-only, non-authorizing"}
    sys.stdout.reconfigure(encoding="utf-8")
    if "--write" in sys.argv:
        OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in res.items() if k != "rounds"}, ensure_ascii=False, indent=1))
    for r in rounds:
        print(f"  {r['packet']}  {r['corpus']:15} {r['verdict']:18} "
              f"H{r['high']} M{r['medium']} L{r['low']}  subject={r['by_subject']}")


if __name__ == "__main__":
    main()
