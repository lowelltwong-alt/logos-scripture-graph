#!/usr/bin/env python3
"""Append E-60 to ERROR_PATTERN_LEDGER.v1.md (append-only). Refuses unless the ledger's sha256 is the one measured
after E-59 was appended and E-60 is absent."""
import hashlib
from pathlib import Path

MD = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\ERROR_PATTERN_LEDGER.v1.md")
PIN16 = "c3ffd585557dc286"
ENTRY = """
## E-60 (2026-09-23) - A MAP PLAN KEYED ON A NON-UNIQUE ID COLLIDED, AND THE SHARED PATCH TOOL LEFT ITS RED WRITE ON DISK

**What happened.** `Ezek/repair2/amend_identity_E55s1.py` amends seven Ezekiel launch rows that recorded the lane's own
runtime id in `parent_agent_id` (E-55 sibling 1). It adds each of the seven to `_transcript_map.ezek.json`. It addressed
the receipts by `execution_id`, which is unique, but keyed the map entries on `attempt_id`. Two close-audit attempts ran
twice each (#e1 and #e2), so two pairs of edits addressed the same map key. Both checks in each pair passed, because
both were written against the same absent value. `campaign/_guarded_json_patch.py` applied the plan, so the second edit
of each pair overwrote the first. Its postvalidation went RED on 2 keys, but it has no rollback, so the wrong map stayed
on disk. The wrapper's own postvalidation then restored all three files, in the same process run. Their digests were
MEASURED equal to the preimages (18159d165092, 5e2e8e51cf74, 3c0872b35194), and no lock or temp file remained. The tool's
receipt for the rolled-back write is kept as `amend_identity_E55s1.map_patch_receipt.FAILED_ROLLED_BACK.json`.

**Severity, scored on counterfactual blast radius.** Observed impact: nil. The wrong map existed only between the tool's
write and the wrapper's rollback, and no agent was running (INFERRED from the session: none had been launched since the
last compaction). Counterfactual: medium. Eight other scripts drive the same tool. A colliding plan applied directly
would have left the map silently short two Fable executions' pointers with only a RED receipt. The map is the pointer
index that the OWED OW-26 transcript audit reads. What caught it was the wrapper's check, not the tool.

**Root cause.** Two stores, two identities. The receipts are unique by execution id. The map is keyed by attempt id, and
retries share an attempt id. The address check proved uniqueness in the store with the unique key and assumed it in the
other. The shared tool had no in-plan uniqueness check and no rollback, and the safe-structured-registry-mutation
protocol requires both.

**Cure (durable).**
1. `_guarded_json_patch.py` now refuses, before any write, a plan that addresses a key more than once.
2. When the tool's own postvalidation goes RED, it now restores the exact preimage, but only if the file is still exactly
   what it wrote. Otherwise it skips the rollback and says so. The tool's preimage is kept as
   `_guarded_json_patch.py.pre_254a43bd2199`.
3. A regression test, `campaign/test_guarded_json_patch.py`, passes 4/4 on the fixed tool and fails 4/4 on the preimage
   copy (MEASURED).
4. The amendment keys execution n>1 as `<attempt_id>_e<n>`, following the `ezek_controlling_rulings_a1_e11` precedent,
   and itself refuses duplicate keys.

Applied after the fix, with every digest MEASURED:
- merged-close receipts 18159d165092 -> 3593f8bb33f3 (+2 rows);
- close-audit receipts 5e2e8e51cf74 -> af1ad7d83342 (+5 rows);
- map 3c0872b35194 -> 138a029c1e19 (+7 keys).

All seven executions now resolve to exactly their runtime id, both through an amending row and through the map. The
amendment token sums are unchanged. The receipt is `amend_identity_E55s1.receipt.json`.

**Sibling audit.** None of the other callers can collide, and a colliding plan is now refused anyway:
- `record_ow21/22/27_ceiling.py` and `record_ow28_directive.py` use fixed, distinct keys.
- `post_launch_e5.py` and `post_launch_t5.py` address one key.
- `map_launch.py` expects each key ABSENT.
- `map_relaunch.py` replaces the bare key and keeps the prior execution under `previous_executions`. An earlier reading
  in this session, that such attempts had lost their #e1, was wrong and was corrected before this entry.

**Reader gap found (OWED, not fixed here).** Census v4 joins a map entry only on its top-level `agent_id`, and never
reads `previous_executions[].agent_id`. Map coverage, MEASURED over the 231 Ezekiel attempts:

| Map path | Attempts |
|---|---|
| Top-level entry | 164 |
| Only in `previous_executions` (census v4 cannot join these through the map) | 11 |
| Key join only | 17 |
| No map path at all | 39 |

The census also joins through receipt fields, so 39 is not a count of unjoined attempts. Trigger: teach the readers
before Daniel's first census or metrics run.
"""


def main():
    b = MD.read_bytes()
    if hashlib.sha256(b).hexdigest()[:16] != PIN16:
        raise SystemExit("REFUSED: the ledger moved since E-59 was appended")
    t = b.decode("utf-8")
    if "\n## E-60 (" in t:
        raise SystemExit("REFUSED: E-60 already present")
    with MD.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(("" if t.endswith("\n") else "\n") + ENTRY)
    print("appended E-60; ledger sha256", hashlib.sha256(MD.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
