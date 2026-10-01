#!/usr/bin/env python3
"""Fix-round item (6), part: correct the wave-to-corpus-version attribution in the late cycle-log entries.

WHAT THE STAGE-2 CHECKER FOUND: the four entries I appended to close the log gap carry correct DIGITS and wrong
WAVE-TO-VERSION ATTRIBUTION. It named the cause precisely: "the risk of counting off disk without re-reading the
apply reports". That is exactly what happened. I read the corpora and their digests, saw v5 through v9, and mapped
waves onto versions in the order the waves ran, which assumes one apply per wave in sequence. The corpus-wide-order
CORRECTION rounds also produced versions, interleaved with the cure round, so the assumption was false.

THE TRUE LINEAGE, taken from each apply report's own base and out fields:
    draft_rows_combined -> rows_v2   author wave            (_apply_author_report.json)
    rows_v2 -> rows_v3               order-execution wave   (_apply_cwo_report.json)
    rows_v3 -> rows_v4               order correction 1     (_apply_cwo_corr_report.json)
    rows_v4 -> rows_v5               order correction 2     (_apply_cwo_corr2_report.json)
    rows_v5 -> rows_v6               MICRO / CURE round     (_apply_micro_report.json)
    rows_v6 -> rows_v7               order correction 3     (_apply_cwo_corr3_report.json)
    rows_v7 -> rows_v8               finalize               (_finalize.py; no apply report - it is not a guarded apply)
    rows_v8 -> rows_v9               BOUNDED FIX round      (_apply_fix_report.json)
Corroborated independently by the postchecks: postcheck_01 audited rows_v8 against pre-cure rows_v5; postcheck_02
audited rows_v9 against pre-cure rows_v8.

WHAT I GOT WRONG: I attributed rows_v6 and rows_v7 to the spot wave, rows_v8 to the cure round, and rows_v9 to
finalize. The cure round produced rows_v6, finalize produced rows_v8, and the fix round produced rows_v9. The spot
wave produced no corpus version of its own - it produced findings that the cure and fix rounds then executed.

The wrong entries are NOT edited. This appends a correction that names each wrong statement and the true one beside
it, because a log that silently repairs itself cannot be audited.
Usage: _correct_log_lineage.py [--apply]"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = HERE / "freeze" / "CYCLE_STATE.md"
NL = "\n"

LINEAGE = [
    ("draft_rows_combined.jsonl", "rows_v2.jsonl", "author wave", "_apply_author_report.json"),
    ("rows_v2.jsonl", "rows_v3.jsonl", "order-execution wave", "_apply_cwo_report.json"),
    ("rows_v3.jsonl", "rows_v4.jsonl", "order correction 1", "_apply_cwo_corr_report.json"),
    ("rows_v4.jsonl", "rows_v5.jsonl", "order correction 2", "_apply_cwo_corr2_report.json"),
    ("rows_v5.jsonl", "rows_v6.jsonl", "MICRO / CURE round", "_apply_micro_report.json"),
    ("rows_v6.jsonl", "rows_v7.jsonl", "order correction 3", "_apply_cwo_corr3_report.json"),
    ("rows_v7.jsonl", "rows_v8.jsonl", "finalize", "_finalize.py (no apply report; not a guarded apply)"),
    ("rows_v8.jsonl", "rows_v9.jsonl", "BOUNDED FIX round", "_apply_fix_report.json"),
]

CORRECTIONS = [
    ("SPOT WAVE COMPLETE", "corpus after the wave's applies: rows_v6.jsonl, rows_v7.jsonl",
     "the spot wave produced NO corpus version of its own; it produced the findings that the cure and fix rounds "
     "executed. rows_v6 came from the cure round and rows_v7 from order correction 3."),
    ("MICRO / CURE ROUND COMPLETE", "guarded apply -> rows_v8.jsonl",
     "the cure round applied rows_v5 -> rows_v6 (_apply_micro_report.json base e2d0e790, out rows_v6)."),
    ("BOUNDED FIX ROUND COMPLETE", "(no corpus version stated)",
     "the fix round applied rows_v8 -> rows_v9 (_apply_fix_report.json base 31a52f2f, out rows_v9)."),
    ("FINALIZE + SIDECARS + POSTCHECKS COMPLETE", "-> rows_v9.jsonl (FINAL)",
     "finalize produced rows_v8; rows_v9 is the FIX round's output. rows_v9 IS the final corpus, so the entry's "
     "conclusion holds and only its attribution was wrong."),
]


def main():
    apply = "--apply" in sys.argv
    # verify the lineage against disk before writing it into an immutable log
    problems = []
    for base, out, wave, src in LINEAGE:
        if not (HERE / out).is_file():
            problems.append(f"{out} missing")
        if src.endswith(".json") and not (HERE / src).is_file():
            problems.append(f"{src} missing")
    for base, out, wave, src in LINEAGE:
        if src.endswith(".json"):
            d = json.load(open(HERE / src, encoding="utf-8-sig"))
            if Path(str(d.get("out"))).name != out:
                problems.append(f"{src} says out={d.get('out')}, lineage claims {out}")
            got = hashlib.sha256((HERE / out).read_bytes()).hexdigest()
            if d.get("out_sha256") and d["out_sha256"] != got:
                problems.append(f"{out} digest differs from {src}'s out_sha256")

    sys.stdout.reconfigure(encoding="utf-8")
    if problems:
        print(json.dumps({"status": "REFUSED", "problems": problems,
                          "note": "the lineage must verify against the apply reports before it is written into an "
                                  "append-only log; writing an unverified correction would repeat the original "
                                  "mistake with more confidence"}, indent=1))
        return 1
    if not apply:
        print(json.dumps({"dry_run": True, "lineage_verified_against_apply_reports": True,
                          "steps": [f"{b} -> {o}  ({w})" for b, o, w, _ in LINEAGE],
                          "corrections": len(CORRECTIONS)}, indent=1))
        return 0

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    L = ["",
         f"## LOG LINEAGE CORRECTION {stamp} (session dce0b6e2) - fix-round item 6",
         "- the four late entries appended earlier today carry correct DIGITS and WRONG wave-to-version attribution.",
         "  Found by the OW-6 stage-2 final checker, which named the cause exactly: counting off disk without",
         "  re-reading the apply reports. I mapped waves onto version numbers in the order the waves ran, which",
         "  assumes one apply per wave; the order-CORRECTION rounds also produced versions, interleaved with the",
         "  cure round, so the assumption was false.",
         "- TRUE LINEAGE, from each apply report's own base and out fields:"]
    for base, out, wave, src in LINEAGE:
        L.append(f"    {base:26} -> {out:14} {wave:22} ({src})")
    L.append("  corroborated independently by the postchecks: postcheck_01 audited rows_v8 against pre-cure rows_v5;")
    L.append("  postcheck_02 audited rows_v9 against pre-cure rows_v8.")
    L.append("- each wrong statement, and the true one beside it:")
    for section, wrong, right in CORRECTIONS:
        L.append(f"    in '{section}':")
        L.append(f"      WROTE: {wrong}")
        L.append(f"      TRUE : {right}")
    L.append("- the wrong entries are NOT edited. A log that silently repairs itself cannot be audited, and the")
    L.append("  mistake is more instructive standing beside its correction than erased.")
    L.append("")

    pre = LOG.read_bytes()
    body = pre if pre.endswith(b"\n") else pre + b"\n"
    LOG.write_bytes(body + NL.join(L).encode("utf-8"))
    assert LOG.read_bytes().startswith(body), "log preimage not intact"
    print(json.dumps({"status": "APPENDED", "corrections": len(CORRECTIONS), "lineage_steps": len(LINEAGE),
                      "pre_sha16": hashlib.sha256(pre).hexdigest()[:16],
                      "post_sha16": hashlib.sha256(LOG.read_bytes()).hexdigest()[:16],
                      "preimage_intact": True}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
