#!/usr/bin/env python3
"""Build a CLASS SWEEP over every skeleton/sweep verse-count citation in the corpus, plus the P01-007 absolute.

WHY A SWEEP AND NOT THREE POINT FIXES: the third final check raised three E-05 count-object findings (P01-005,
P02-007 and, at medium, P01-007) and said the thing that matters about them - "the same class was cured on P02-003
in the first fix round; these three sibling citations were verified by the earlier checks with the same substring
method the writer used, which is why they passed." That is a class, not three incidents. A writer counted verses
containing a SUBSTRING and wrote the digit as though it counted the FORM; every reviewer who checked it re-ran the
same substring method and confirmed it; and the corpus carries 36 such citations across 19 rows. Curing the three
that were sampled would leave the rest, and a fourth check would find the fourth instance.

So every citation is re-derived, and the sweep is the unit of work. Most will be correct - the checker found several
true token counts sitting beside the false ones in the same sentence - and an author that reports a citation as
already sound is doing the job, not shirking it.

The P01-007 medium rides in the same wave because it is the same failure of naming: an absolute ("no first-person
form at all") that is false of the bytes as written and true of what the writer meant (the speaker's OWN first
person). It passed every stage because the order scanner's universal list does not contain the phrase "at all".
Usage: _build_e05_sweep_orders.py [--apply]"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "rows_v13.jsonl"
PAT = re.compile(r"(sweep|skeleton)[^.;]{0,80}?(\d+)\s*verses", re.I)
FIELDS = ("boundary_rationale", "device_notes", "strongest_rejected_alternative")

P01_007 = {
    "e_class": "E-05/E-16 byte-false absolute in a driver field",
    "severity": "medium", "origin": "OW-6 stage-2 final check 03", "field": "boundary_rationale",
    "defective_text": "give way to no first-person form at all across this stretch",
    "byte_evidence": "Lam.2.16 carries four first-person-PLURAL verbs inside the enemies' quoted taunt, which this "
                     "same field renders as “We have swallowed her up.” web:Lam.2.16. The speaker's own "
                     "first-person-SINGULAR forms are indeed absent from 2.14-2.17, so the seam ground stands and "
                     "only the wording overshoots. The sentence carries no sweep citation for its absolute, and the "
                     "order scanner's universal token list does not contain 'at all', which is how it passed every "
                     "stage including two earlier final checks.",
    "proposed_cure": "Name the object: 'give way to no first-person form of the speaker's own across this stretch "
                     "(the four first-person-plural verbs at web:Lam.2.16 stand inside the enemies' quoted taunt)'. "
                     "Read back against Lam.2.14-2.17. No span, label or confidence change."}

SWEEP_ITEM = {
    "e_class": "E-05 count-object naming (CLASS SWEEP)",
    "severity": "low", "origin": "OW-6 stage-2 final check 03, generalised from three sampled instances",
    "field": "every field of this row carrying a sweep/skeleton verse count",
    "defective_text": "(per citation - see citations_in_this_row)",
    "byte_evidence": "A skeleton sweep counts verses containing a SUBSTRING. Written as though it counted the form, "
                     "the digit is false: on P01-005 the eye-form's 'sweep: 7 verses' counts 5 as a whole token, the "
                     "two extras being a first-PLURAL form and, at 1.8, a different lexeme; on P02-007 'skeleton "
                     "lanu: 7 verses' counts 5 as a whole token. Both were confirmed by earlier reviewers who re-ran "
                     "the same substring method. True token counts sit beside the false ones in the same sentences.",
    "proposed_cure": "For EVERY citation in this row: re-derive both numbers from the pointed text - how many verses "
                     "carry the WHOLE TOKEN, and how many carry the substring. If they agree, the citation is sound; "
                     "say so and change nothing. If they differ, either state the whole-token count or name the "
                     "object explicitly ('skeleton substring sweep: N verses, M as the whole token'). Never leave a "
                     "digit whose object is unstated. Report EVERY citation you checked with both numbers, including "
                     "the ones you left alone."}


def main():
    apply = "--apply" in sys.argv
    rows = {r["decision_id"]: r for r in
            (json.loads(l) for l in (HERE / BASE).read_text(encoding="utf-8-sig").splitlines() if l.strip())}
    cites = {}
    for rid, r in rows.items():
        for f in FIELDS:
            t = r.get(f) or ""
            for m in PAT.finditer(t):
                cites.setdefault(rid, []).append({"field": f, "citation": t[max(0, m.start() - 70):m.end() + 15]})

    ids = sorted(set(cites) | {"P01-007"}, key=lambda r: rows[r]["chunk_index_in_book"])
    base_sha = hashlib.sha256((HERE / BASE).read_bytes()).hexdigest()
    per = 7
    slices = []
    for n in range(0, len(ids), per):
        k = n // per + 6  # fix_01..fix_05 exist
        ch = ids[n:n + per]
        orders = {}
        for rid in ch:
            res = []
            if rid == "P01-007":
                res.append(P01_007)
            if rid in cites:
                res.append(dict(SWEEP_ITEM, citations_in_this_row=cites[rid]))
            orders[rid] = {"row_id": rid, "op": "replace", "current_row": rows[rid], "residuals": res}
        sl = {"schema": "lam_fc_fix_orders_slice.v1", "agent": f"f{k:02d}", "attempt_id": f"lam_fcfix_f{k:02d}_a1",
              "base": BASE, "base_sha256": base_sha,
              "source": "OW-6 stage-2 final check 03; the E-05 count-object class generalised to every sweep citation",
              "output_file": f"spot/fix_{k:02d}.jsonl", "row_ids": ch,
              "law": "This is a CLASS SWEEP. Most citations will be correct; report every one you check with both "
                     "numbers, and change only those whose object is misstated. A row you leave unchanged still "
                     "needs an emitted row - emit it byte-identical apart from _op, and say in your final message "
                     "that nothing needed changing and why.",
              "orders": orders}
        (HERE / "spot" / f"orders_fix_{k:02d}.json").write_text(json.dumps(sl, ensure_ascii=False, indent=1),
                                                                encoding="utf-8", newline="\n")
        slices.append({"attempt_id": sl["attempt_id"], "orders": f"spot/orders_fix_{k:02d}.json",
                       "output": sl["output_file"], "rows": ch,
                       "citations": sum(len(cites.get(r, [])) for r in ch)})

    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"base": BASE, "rows_with_citations": len(cites),
                      "citations_total": sum(len(v) for v in cites.values()),
                      "rows_ordered": len(ids), "slices": slices, "dry_run": not apply}, indent=1))


if __name__ == "__main__":
    main()
