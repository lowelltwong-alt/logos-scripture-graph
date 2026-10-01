#!/usr/bin/env python3
"""ORCHESTRATOR ERROR: the sweep launch messages pinned a DIFFERENT corpus than their orders named.

WHAT I DID: I built the f06/f07/f08 launch messages by string-editing the f05 launch text. That text pinned
rows_v12.jsonl with its sha256. The orders those launches point at were built against rows_v13.jsonl and carry
rows_v13 rows as their current_row. So each author was handed a launch message naming one corpus by exact path and
an orders file naming another, and told the exact-path law forbids reading anything not named by exact path.

HOW IT WAS CAUGHT: not by me. Fix author f07 noticed the discrepancy, refused to read the corpus its orders named
because that path was not given to it by exact path, verified that every current_row in its orders was byte-identical
to the rows_v12 it HAD been given, used that, and disclosed the whole thing in its cure_tests. That is precisely the
behaviour the exact-path law and the honest-reporting rule are for, and it worked.

WHY IT DID NO HARM, AND WHY THAT IS LUCK: exactly one row differs between rows_v12 and rows_v13 - P02-006, whose
mark clause fix author f05 had just cured - and P02-006 is in none of the three slices. Every ordered row is
byte-identical across the two corpora, so the mismatch could not change any result.

WHAT WOULD HAVE HAPPENED OTHERWISE, which is the severity: had P02-006 fallen in a slice, the author would have
emitted a replacement built on the pre-cure v12 text. The guarded apply pins the BASE it is told to use, so applying
that against rows_v13 would have parity-matched and silently REVERTED the f05 cure - undoing the execution of a boss
ruling, re-installing the mark-symmetry defect, and doing it inside a wave whose whole purpose was to fix defects.
Nothing in the apply guard compares an emitted row against a corpus the author was not given.

ROOT CAUSE: a launch message was produced by editing a previous launch message instead of being generated from the
orders file it points at. Every other field survived that edit correctly; the corpus pin did not, because nothing
required it to agree with anything.

CONTROL: _check_launch_orders_agree.py compares every launch message against the orders it names and refuses a
mismatch. Run it before any launch. It is a five-line check that would have caught this in the second it took.
Usage: _record_launch_base_mismatch.py [--apply]"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SC = HERE.parent.parent
OUT = SC / "SP" / "campaign" / "finding_launch_orders_base_mismatch.v1.json"
LOG = HERE / "freeze" / "CYCLE_STATE.md"
NL = "\n"


def main():
    apply = "--apply" in sys.argv
    a = {r["decision_id"]: r for r in
         (json.loads(l) for l in (HERE / "rows_v12.jsonl").read_text(encoding="utf-8-sig").splitlines() if l.strip())}
    b = {r["decision_id"]: r for r in
         (json.loads(l) for l in (HERE / "rows_v13.jsonl").read_text(encoding="utf-8-sig").splitlines() if l.strip())}
    differ = sorted(k for k in a if a[k] != b[k])

    slices = {}
    for n in (6, 7, 8):
        o = json.loads((HERE / "spot" / f"orders_fix_{n:02d}.json").read_text(encoding="utf-8-sig"))
        t = (SC / f"_launch_fcfix_f{n:02d}.txt").read_text(encoding="utf-8")
        m = re.search(r"rows_v(\d+)\.jsonl", t)
        slices[f"f{n:02d}"] = {"launch_pins": f"rows_v{m.group(1)}.jsonl" if m else None,
                               "orders_base": o["base"], "rows": o["row_ids"],
                               "overlaps_the_differing_row": sorted(set(o["row_ids"]) & set(differ))}

    rec = {"schema": "m8_finding.v1", "finding_id": "launch_message_pinned_a_different_corpus_than_its_orders",
           "book": "Lam", "recorded_at": datetime.now(timezone.utc).isoformat(),
           "author_of_the_error": "orchestrator (claude-opus-5)", "severity": "medium",
           "severity_basis": "scored on counterfactual blast radius. Observed impact NIL; the escape was luck.",
           "class": "launch_integrity",
           "what": "the f06/f07/f08 launch messages pinned rows_v12.jsonl by exact path while the orders they point "
                   "at were built on rows_v13.jsonl and carry rows_v13 rows as current_row",
           "how_it_arose": "each launch was produced by string-editing the previous launch instead of being "
                           "generated from the orders file it points at; every other field survived the edit, the "
                           "corpus pin did not, and nothing required the two to agree",
           "caught_by": "fix author lam_fcfix_f07_a1, NOT the orchestrator. It refused to read the corpus its "
                        "orders named because that path was not given to it by exact path, verified byte-identity "
                        "between its orders' current_row values and the corpus it HAD been given, used the latter, "
                        "and disclosed the discrepancy in its cure_tests.",
           "why_no_harm": f"exactly one row differs between the two corpora ({differ}) and it is in none of the "
                          f"three slices, so every ordered row is byte-identical across both",
           "counterfactual": "had the differing row fallen in a slice, the author would have emitted a replacement "
                             "built on the PRE-CURE text. The guarded apply pins the base it is told to use, so the "
                             "apply would have parity-matched and silently REVERTED that row's cure - undoing a "
                             "boss ruling's execution and re-installing a validator defect, inside a wave whose "
                             "purpose was to remove defects. No guard in the apply compares an emitted row against "
                             "a corpus the author was never given.",
           "slices": slices, "rows_differing_v12_to_v13": differ,
           "control": "_check_launch_orders_agree.py: compares every launch message against the orders it names and "
                      "refuses a mismatch. Run before any launch.",
           "lesson": "a launch message is a contract between an author and a corpus. Deriving one by editing "
                     "another copies every field including the ones that must not be copied.",
           "authority": "orchestrator self-report; candidate-only, non-authorizing"}

    sys.stdout.reconfigure(encoding="utf-8")
    if not apply:
        print(json.dumps({"dry_run": True, "differ": differ, "slices": slices}, indent=1))
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8", newline=NL)
    entry = ["",
             f"## LAUNCH/ORDERS CORPUS MISMATCH {datetime.now(timezone.utc).strftime('%Y-%m-%d')} (session dce0b6e2)",
             "- the three sweep launch messages pinned rows_v12.jsonl while their orders were built on rows_v13.",
             "  I produced each launch by editing the previous one; every field survived but the corpus pin, and",
             "  nothing required the launch and its orders to agree.",
             "- CAUGHT BY fix author lam_fcfix_f07_a1, not by me. It refused to read the corpus its orders named",
             "  because that path was not given by exact path, verified its orders' rows were byte-identical to the",
             "  corpus it HAD been given, used that, and disclosed the discrepancy.",
             f"- no harm: only {differ} differs between the two corpora and it is in none of the three slices.",
             "- HAD IT FALLEN IN A SLICE the author would have emitted a pre-cure row; the guarded apply pins the",
             "  base it is told to use, so it would have parity-matched and silently reverted that row's cure,",
             "  undoing a boss ruling's execution inside a wave meant to remove defects.",
             "- control: _check_launch_orders_agree.py refuses a launch whose pin disagrees with its orders.",
             ""]
    pre = LOG.read_bytes()
    body = pre if pre.endswith(b"\n") else pre + b"\n"
    LOG.write_bytes(body + NL.join(entry).encode("utf-8"))
    assert LOG.read_bytes().startswith(body)
    print(json.dumps({"status": "RECORDED", "finding": str(OUT), "differ": differ,
                      "sha16": hashlib.sha256(OUT.read_bytes()).hexdigest()[:16]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
