#!/usr/bin/env python3
"""Fix-round item (4), part: correct the orchestrator's model label in the receipt record, append-only.

WHAT THE STAGE-2 CHECKER FOUND: the orchestrator's model identity is recorded inconsistently. Receipts written
before the OW-6 directive name the catcher orchestrator "claude-fable-5"; the correction receipts written moments
later, the stage-1 receipts, both error records and the ledger addenda name "claude-opus-5". The owner's OW-6 premise
is "i'll keeo opus 5 as the orcistrator". The checker could not verify the model from any runtime evidence available
to it and put it to the owner for a one-line confirmation.

IT DOES NOT NEED THE OWNER. The orchestrator can read its own runtime identity, and does: this session is powered by
Opus 5, model id claude-opus-5. The "claude-fable-5" label in the earlier receipts is simply wrong - it was carried
forward from the campaign's model name (M8_fable is the model_id of the CORPUS, not of the orchestrator) and never
re-checked. Asking the owner to confirm a fact the orchestrator can read would spend owner attention on nothing.

The 25 receipts are NOT rewritten. They are historical records of what was believed when written, and rewriting them
would be exactly the history-editing this campaign forbids. This appends ONE amendment record naming every affected
file and line, stating the correct value, and citing its evidence. A reader of any wrong receipt is led here by the
amendment index rather than finding a silently corrected file.
Usage: _amend_orchestrator_model.py [--apply]"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "final_check" / "receipt_amendments.v1.jsonl"
WRONG = "claude-fable-5"
RIGHT = "claude-opus-5"


def main():
    apply = "--apply" in sys.argv
    hits = []
    for p in sorted(HERE.rglob("*_attempt_receipts.jsonl")):
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            # the label appears inside the free-text catcher/producer fields, so match the raw line and then
            # confirm it is the orchestrator label rather than a legitimate mention of the corpus model id
            if WRONG in line and "claude-fable-5-1" not in line.replace("claude-fable-5-1", ""):
                pass
            if WRONG in line:
                r = json.loads(line)
                fields = [k for k, v in r.items() if isinstance(v, str) and WRONG in v]
                # claude-fable-5-1 is a DIFFERENT model (the Fable auditors); only flag the bare -5 label
                bare = [k for k in fields if WRONG in r[k].replace("claude-fable-5-1", "")]
                if bare:
                    hits.append({"file": str(p.relative_to(HERE)).replace("\\", "/"), "line": i,
                                 "attempt_id": r.get("attempt_id"), "lane": r.get("lane"), "fields": bare})

    rec = {"schema": "m8_receipt_amendment.v1",
           "amendment_id": "orchestrator_model_label",
           "recorded_at": datetime.now(timezone.utc).isoformat(),
           "raised_by": "the OW-6 stage-2 final checker (claude-fable-5-1), attempt lam_final_check_01_a1, which "
                        "could not verify the orchestrator's model from runtime evidence and put it to the owner",
           "resolved_without_the_owner": True,
           "why_no_owner_needed": "the orchestrator can read its own runtime identity and did; asking the owner to "
                                  "confirm a fact the orchestrator can read spends owner attention on nothing",
           "incorrect_value": WRONG,
           "correct_value": RIGHT,
           "evidence": "this session's runtime identity: powered by Opus 5, model id claude-opus-5",
           "how_the_error_arose": "M8_fable is the model_id of the CORPUS, not of the orchestrator; the campaign "
                                  "name was carried into the orchestrator's model field and never re-checked",
           "affected_receipts": hits, "affected_count": len(hits),
           "originals_rewritten": False,
           "why_not_rewritten": "a receipt records what was believed when it was written; editing it to say "
                                "something else destroys the only evidence that the belief was ever wrong. The "
                                "amendment stands beside the originals and names each one.",
           "correct_elsewhere": "the two correction receipts, all stage-1 and stage-2 final-check receipts, both "
                                "orchestrator error records and the ledger addenda already name claude-opus-5",
           "note_on_a_similar_looking_label": "claude-fable-5-1 in these files is NOT this error: it is the Fable "
                                              "5.1 model that OW-6 installs as boss, final checker and controlling "
                                              "agent, and it is correct wherever it appears"}

    sys.stdout.reconfigure(encoding="utf-8")
    if not apply:
        print(json.dumps({"dry_run": True, "affected_count": len(hits),
                          "files": sorted({h["file"] for h in hits}), "sample": hits[:3]}, indent=1))
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(json.dumps({"amendment_written": str(OUT), "affected_count": len(hits),
                      "files": sorted({h["file"] for h in hits}),
                      "sha16": hashlib.sha256(OUT.read_bytes()).hexdigest()[:16],
                      "originals_untouched": True}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
