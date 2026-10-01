#!/usr/bin/env python3
"""Fix two defects in the durable attempt receipts, under the guarded-mutation discipline.

DEFECT 1 - A WRONG attempt_id ON TWO ROWS, and it is mine. reviews/ezek_rulings_attempt_receipts.jsonl carries
three rows whose execution_ids are correctly ezek_e12/e13/e14_ruling_a1#e1 and whose attempt_ids ALL read
ezek_e12_ruling_a1. I built each landing script from the previous one and carried the hardcoded attempt_id
forward. The rows are self-inconsistent rather than wholly wrong - output_file and execution_id are right - but
an attempt_id is provenance, and any census or audit keyed on it would merge three distinct attempts into one.
The fix is DERIVED from the execution_id rather than retyped, because retyping is how the error happened.

DEFECT 2 - AN ABSENT tokens_reported READS AS ZERO. Nine receipts carry no tokens_reported at all, including all
four I landed this session (the boss audit and the e12/e13/e14 rulings - substantial Fable runs). A census that
sums the field and skips what is missing reports 38,678,610 as an EQUALITY when it is a LOWER BOUND. That is
OW-18's "implication is assertion": an absent field in a summed column asserts zero.

I cannot recover the true counts - the runtime handed me no per-attempt token figure for those runs and the
receipts were written without one - so the honest value is UNAVAILABLE, and OW-18 says UNAVAILABLE is a VALUE to
be written, never a blank. It is written as a STRING so that any naive summing script FAILS LOUD on it instead of
skipping it: the campaign's own rule is that a guard failing closed toward "no problem" is the failure direction
nobody notices.

WHAT THIS CHANGES DOWNSTREAM, stated because it bears on a decision I was about to make: Ezekiel's census is
>= 38,678,610, not = 38,678,610, and OW-15's headroom of 16,321,390 is an UPPER bound on what is actually left.
"""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
NOW = datetime.now(timezone.utc).isoformat()
REASON = ("UNAVAILABLE - the landing script did not record a per-attempt token figure and the runtime handed "
          "the orchestrator none for this attempt. Written as a VALUE under OW-18 rather than left absent, "
          "because an absent field in a summed column asserts zero. A census must count this attempt as "
          "UNKNOWN and report its total as a LOWER BOUND.")

TARGETS = [
    EZ / "reviews" / "ezek_rulings_attempt_receipts.jsonl",
    EZ / "reviews" / "ezek_boss_attempt_receipts.jsonl",
]
report = {"schema": "ezek_receipt_repair.v1", "at": NOW, "files": []}

for p in TARGETS:
    pre = p.read_bytes()
    pre_sha = hashlib.sha256(pre).hexdigest()
    rows = [json.loads(l) for l in pre.decode("utf-8").splitlines() if l.strip()]
    changes = []
    for r in rows:
        rid = r.get("attempt_id")
        ex = str(r.get("execution_id") or "")
        # DERIVED, not retyped: the attempt id is the execution id up to the '#'
        want = ex.split("#")[0] if "#" in ex else rid
        if want and rid != want:
            changes.append({"execution_id": ex, "field": "attempt_id", "from": rid, "to": want,
                            "basis": "derived from the execution_id, which is correct on every row"})
            r["attempt_id"] = want
        if "tokens_reported" not in r:
            changes.append({"execution_id": ex, "field": "tokens_reported", "from": "ABSENT",
                            "to": "UNAVAILABLE (string)", "basis": "OW-18: UNAVAILABLE is a value, not a blank"})
            r["tokens_reported"] = REASON
            r["tokens_reported_recorded_at"] = NOW
    if not changes:
        report["files"].append({"file": str(p.relative_to(EZ)), "sha256": pre_sha, "changes": 0,
                                "note": "nothing to fix"})
        continue
    out = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows).encode("utf-8")
    # read-back before replacing
    tmp = p.with_suffix(p.suffix + ".tmpFIX")
    tmp.write_bytes(out)
    back = [json.loads(l) for l in tmp.read_text(encoding="utf-8").splitlines() if l.strip()]
    if len(back) != len(rows) or json.dumps(back, sort_keys=True) != json.dumps(rows, sort_keys=True):
        tmp.unlink()
        raise SystemExit("REFUSED: the rewritten receipts do not re-parse to what was intended")
    backup = p.with_suffix(p.suffix + ".pre_" + pre_sha[:12])
    if not backup.exists():
        shutil.copy2(p, backup)
    tmp.replace(p)
    report["files"].append({
        "file": str(p.relative_to(EZ)), "rows": len(rows),
        "preimage_sha256": pre_sha, "postimage_sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        "preimage_backup": backup.name,
        "changes": len(changes), "detail": changes,
    })

print(json.dumps(report, ensure_ascii=False, indent=1))
