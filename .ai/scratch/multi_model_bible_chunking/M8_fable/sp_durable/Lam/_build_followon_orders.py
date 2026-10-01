#!/usr/bin/env python3
"""Build the bounded FOLLOW-ON round after the final-check fix wave, and record the second-generation catch.

TWO ITEMS, from two different sources, both on rows the fix wave just touched:

(1) P02-001 - SECOND-GENERATION DEFECT (E-17). The cure that disclosed the held-open persona question wrote
    "...held here as a disputed literary question, never decided." That bare universal is exactly what CWO-2 bans
    and what check_universals flags. rows_v9 had universals GREEN and CWO-2 at 0 candidates; rows_v10 has one flag
    on each. TWO INDEPENDENT ARMS caught the same sentence, which is the point of running both: a cure that fixes
    the ordered defect and installs a new one is the failure mode the second-generation lane exists for. The
    author's cure was right in substance - the strategy's own wording is "never decided" - and wrong in form,
    because quoting the strategy's phrasing does not exempt a row from the corpus's own universal-dampening law.

(2) P02-006 - BOSS RULING B3-1's CONDITION, still unexecuted. The condition was found after fix author f02 had
    already launched, the orders file was amended, and the author read the orders before the amendment. This was
    foreseen and recorded at the time rather than assumed away: "if the delivered P02-006 row lacks the
    never-conflated sentence, a bounded follow-on cures that one item." It does, so this is that follow-on.

Base is rows_v10 (the fix wave's output), so the follow-on cures what actually shipped.
Usage: _build_followon_orders.py [--apply]"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "rows_v10.jsonl"
ORDERS = HERE / "spot" / "orders_fix_03.json"
CATCH = HERE / "spot" / "second_generation_catch_02.v1.json"
NL = "\n"

ITEMS = {
    "P02-001": [{
        "e_class": "E-17 second-generation defect (CWO-2 undampened universal + check_universals)",
        "severity": "medium",
        "origin": "installed by the fix wave's own cure for the held-open-region residual; caught by the "
                  "post-apply re-scan and the validator suite, not by the author",
        "field": "boundary_rationale",
        "defective_text": "Whether this first-person speaker is an individual or a collective persona is held here "
                          "as a disputed literary question, never decided.",
        "byte_evidence": "rows_v9: universals GREEN, CWO-2 exact arm 0 candidates. rows_v10: universals FLAGS "
                         "(1 flag, [9].boundary_rationale, claim 'never') and CWO-2 exact arm 1 candidate, "
                         "P02-001 boundary_rationale, word 'never'. Both arms name the same sentence.",
        "proposed_cure": "Keep the disclosure - it executes a real residual and the held question must stay "
                         "disclosed - and remove the bare universal. Restate so the sentence says the corpus does "
                         "not decide the question, without the word 'never' standing as an undampened absolute: "
                         "e.g. '...is held here as a disputed literary question that this corpus does not decide.' "
                         "The owner-ruled strategy's own phrasing is 'never decided'; quoting it does not exempt "
                         "the row from the corpus's universal-dampening law, so paraphrase rather than quote. "
                         "Change nothing else on the row."}],
    "P02-006": [{
        "e_class": "boss ruling B3-1 condition not executed",
        "severity": "medium",
        "origin": "orchestrator, found while recording the CWO-1 ruling; ordered after fix author f02 had launched "
                  "and therefore not executed by it - foreseen and recorded at the time",
        "field": "device_notes",
        "defective_text": "(absence) - device_notes names the SAMEKH marks at Lam.3.42 and Lam.3.45 while the row's "
                          "key observed_substrate_signals carries acrostic.triplet_nun_samekh_pe_partial, the "
                          "samekh LETTER; no sentence distinguishes the two layers",
        "byte_evidence": "boss ruling B3-1 (reviews/boss_lam_b3.json) narrowed corpus-wide order CWO-1 and set its "
                         "price: 'The price at the one site where the collision is live is an explicit "
                         "never-conflated sentence in P02-006's device_notes.' The narrowing was implemented in "
                         "_cwo_scan.py; the sentence was never written. pmarks_Lam.json confirms SAMEKH marks at "
                         "Lam.3.42 and Lam.3.45; the acrostic letter samekh names triplet position 15.",
        "proposed_cure": "Add ONE sentence to device_notes stating that the samekh in this row's acrostic key is "
                         "the Hebrew LETTER naming the triplet's position in the alphabetic spine (tier-1, from "
                         "the verse bytes) and is never the SAMEKH parashah mark cited in this same field (tier-3, "
                         "single-witness, from the seg inventory), and that the two layers are not conflated. "
                         "MIND THE UNIVERSAL-DAMPENING LAW while you write it - phrase the distinction without an "
                         "undampened absolute, or you will install the very defect the other row in this slice is "
                         "here to cure. Change nothing else: no span, no label, no key, and do not alter the "
                         "existing mark citations."}],
}


def main():
    apply = "--apply" in sys.argv
    rows = {r["decision_id"]: r for r in
            (json.loads(l) for l in (HERE / BASE).read_text(encoding="utf-8-sig").splitlines() if l.strip())}
    ids = sorted(ITEMS, key=lambda r: rows[r]["chunk_index_in_book"])
    base_sha = hashlib.sha256((HERE / BASE).read_bytes()).hexdigest()

    sl = {"schema": "lam_fc_fix_orders_slice.v1", "agent": "f03", "attempt_id": "lam_fcfix_f03_a1",
          "base": BASE, "base_sha256": base_sha,
          "source": "post-apply re-scan of rows_v10 (second-generation arm) + boss ruling B3-1's unexecuted condition",
          "output_file": "spot/fix_03.jsonl", "row_ids": ids,
          "law": "TWO items, both on rows the previous wave touched. One is a defect that wave INSTALLED; the other "
                 "is a boss ruling's condition it never received. Cure exactly what each names and nothing else. "
                 "Both cures are prose that must obey the universal-dampening law - read your own new sentences "
                 "back against it before delivering, because the first item exists precisely because that was not "
                 "done last time.",
          "orders": {rid: {"row_id": rid, "op": "replace", "current_row": rows[rid], "residuals": ITEMS[rid]}
                     for rid in ids}}

    catch = {"schema": "m8_second_generation_catch.v1", "id": "lam_secondgen_02",
             "when": datetime.now(timezone.utc).isoformat(),
             "what": "the final-check fix wave cured 7 ordered residuals and INSTALLED one new defect",
             "row": "P02-001", "installed_by": "lam_fcfix_f02_a1", "wave": "final-check fix wave (fix_02)",
             "defect": "bare universal 'never' in the new held-open-region disclosure sentence",
             "caught_by": ["_cwo_scan.py CWO-2 exact arm over rows_v10 (0 -> 1 candidate)",
                           "tools/check_universals.py via the validator suite (GREEN -> FLAGS, 1)"],
             "why_two_arms_matter": "the same sentence was named independently by an order-specific scanner and a "
                                    "general validator; either alone would have caught it, and running both is what "
                                    "makes the catch robust rather than lucky",
             "not_caught_by": "the author's own self-checks, which ran the 7-gram gate, the NFD dry-run, "
                              "check_web_quotes and tiling - none of which tests universals",
             "control_gap_named": "the fix brief's self-check list did not include check_universals; a cure that "
                                  "writes NEW PROSE can install a universal, so the universals arm belongs in the "
                                  "self-check list of every prose-cure brief",
             "author_fault": "partial - the cure was right in substance and wrong in form; the brief did not ask "
                             "for the check that would have caught it",
             "status": "ORDERED for cure in the follow-on round (fix_03)"}

    sys.stdout.reconfigure(encoding="utf-8")
    if not apply:
        print(json.dumps({"dry_run": True, "base": BASE, "base_sha16": base_sha[:16], "rows": ids,
                          "items": sum(len(v) for v in ITEMS.values()),
                          "orders_file": ORDERS.name, "catch_file": CATCH.name}, indent=1))
        return 0

    ORDERS.parent.mkdir(parents=True, exist_ok=True)
    ORDERS.write_text(json.dumps(sl, ensure_ascii=False, indent=1), encoding="utf-8", newline=NL)
    CATCH.write_text(json.dumps(catch, ensure_ascii=False, indent=1), encoding="utf-8", newline=NL)
    print(json.dumps({"status": "BUILT", "orders": str(ORDERS), "rows": ids,
                      "orders_sha16": hashlib.sha256(ORDERS.read_bytes()).hexdigest()[:16],
                      "catch_record": str(CATCH),
                      "base_sha16": base_sha[:16]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
