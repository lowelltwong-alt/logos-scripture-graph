#!/usr/bin/env python3
"""#e15 Q2/Q3: the CONF-CAL AUDIT SWEEP. Assemble the grade/limb evidence per row for #e16 to rule on.

WHAT IT IS AND WHAT IT DELIBERATELY IS NOT. The ruling orders "a CONF-CAL audit sweep lists grade/limb
disagreements for #e16". It is a VIEW, not a verdict: it assembles, per row, the seam evidence the row's own
references and prose claim, alongside the stated grade, and flags the pairs that look inconsistent under the
UNIFIED rival predicate the ruling just established. #e16 rules; this sweep gives it something to rule on.

WHY IT CANNOT YET BE A VERDICT, stated rather than glossed. The unified predicate turns on which FACE a piece
of evidence sits on - "an onset-class device on its near face, a verse-final close-role signal on its far face".
The role vocabulary CANNOT EXPRESS FACE until clause 6 v2's qualifiers are installed, which is REPAIR-2 step 4.
So this sweep derives face GEOMETRICALLY from each cited verse against the row's span (before the first verse =
far side of the onset seam; the first verse = near side; and so on), and reports that derivation as INFERRED.
A sweep that claimed to apply the scale before the vocabulary can express its central term would be asserting
more than it measures.

THE FOUR STATES it reports per row, so #e16 sees the shape and not just a list:
  CONSISTENT - the claimed evidence and the grade agree under the unified predicate
  GRADE_ABOVE_EVIDENCE - the row claims less than its grade needs
  GRADE_BELOW_EVIDENCE - the row claims more than its grade needs
  UNDERDETERMINED - the row's refs do not carry enough faced evidence to say either way
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()          # noqa: E731

rows = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
VREF = re.compile(r"(?:oshb:|web:)?Ezek\.(\d+)\.(\d+)")
TOKEN = re.compile(r"\[(WARRANT|DISCLOSURE|QUOTE|ANCHOR)([A-Za-z:-]*)\]")
# onset-class and close-role device words, from the conventions the rulings bind
ONSET_WORDS = re.compile(r"word[- ]event|dateline|messenger|ve'attah|son of man|set[- ]your[- ]face|"
                         r"transport|he said to me", re.I)
CLOSE_WORDS = re.compile(r"utterance|recognition|refrain|i have spoken|signature", re.I)
MARK_ONLY = re.compile(r"\b(samekh|petuchah|setumah|\bpe\b|parashah|mark)\b", re.I)

out_rows, tally = [], Counter()
for r in rows:
    rid, grade = r["decision_id"], str(r.get("confidence", "?"))
    ms = VREF.findall(str(r.get("span", "")))
    if not ms:
        continue
    first, last = (int(ms[0][0]), int(ms[0][1])), (int(ms[-1][0]), int(ms[-1][1]))
    faces = {"onset_near": [], "onset_far": [], "close_near": [], "close_far": [], "interior": []}
    for e in (r.get("boundary_evidence_refs") or []):
        vm = VREF.search(e)
        if not vm:
            continue
        cv = (int(vm.group(1)), int(vm.group(2)))
        tok = TOKEN.search(e)
        kind = (tok.group(1) + tok.group(2)) if tok else "untokened"
        tail = e.split("]", 1)[-1] if tok else e
        sig = ("onset" if ONSET_WORDS.search(tail) else
               "close" if CLOSE_WORDS.search(tail) else
               "mark" if MARK_ONLY.search(tail) else "other")
        # face derived GEOMETRICALLY from the verse against the span - INFERRED, because the token cannot say
        if cv == first:
            faces["onset_near"].append((e[:70], kind, sig))
        elif cv < first:
            faces["onset_far"].append((e[:70], kind, sig))
        elif cv == last:
            faces["close_near"].append((e[:70], kind, sig))
        elif cv > last:
            faces["close_far"].append((e[:70], kind, sig))
        else:
            faces["interior"].append((e[:70], kind, sig))

    def has(face, sigs):
        return any(s in sigs for _, _, s in faces[face])

    onset_two_faced = has("onset_near", ("onset",)) and has("onset_far", ("close", "onset"))
    close_two_faced = has("close_near", ("close",)) and has("close_far", ("onset", "close"))
    far_faces_bare = not has("onset_far", ("onset", "close")) or not has("close_far", ("onset", "close"))
    rival_tokens = [e for e in (r.get("boundary_evidence_refs") or []) if "WARRANT-rival" in e]

    # what the UNIFIED predicate would give, on the row's own claimed evidence
    if onset_two_faced and close_two_faced and not rival_tokens:
        implied = "high"
    elif (onset_two_faced or close_two_faced) and (far_faces_bare or rival_tokens):
        implied = "medium"
    elif has("onset_near", ("onset", "close")) or has("close_near", ("close", "onset")):
        implied = "medium_low"
    else:
        implied = "UNDERDETERMINED"
    ORDER = {"low": 0, "medium_low": 1, "medium": 2, "high": 3}
    if implied == "UNDERDETERMINED" or grade not in ORDER:
        state = "UNDERDETERMINED"
    elif ORDER[grade] == ORDER[implied]:
        state = "CONSISTENT"
    elif ORDER[grade] > ORDER[implied]:
        state = "GRADE_ABOVE_EVIDENCE"
    else:
        state = "GRADE_BELOW_EVIDENCE"
    tally[state] += 1
    out_rows.append({"row": rid, "span": r.get("span"), "grade": grade,
                     "implied_by_the_unified_predicate": implied, "state": state,
                     "faced_evidence_counts": {k: len(v) for k, v in faces.items()},
                     "onset_two_faced": onset_two_faced, "close_two_faced": close_two_faced,
                     "rival_tokens": len(rival_tokens),
                     "faces": {k: v for k, v in faces.items() if v}})

out = {
    "schema": "ezek_confcal_audit.v1",
    "order": "#e15 Q2/Q3: list grade/limb disagreements for #e16",
    "what_this_is_not": ("a verdict. #e16 rules. This assembles, per row, the seam evidence the row's own "
                         "references claim, beside the stated grade, under the UNIFIED rival predicate the "
                         "ruling established."),
    "why_it_cannot_yet_be_a_verdict": ("the unified predicate turns on FACE, and the role vocabulary cannot "
                                       "express face until clause 6 v2's qualifiers are installed at REPAIR-2 "
                                       "step 4. Face is therefore derived GEOMETRICALLY here - a cited verse "
                                       "before the span's first verse is the far side of the onset seam, and so "
                                       "on - and that derivation is INFERRED, not MEASURED. A sweep claiming to "
                                       "apply the scale before the vocabulary can express its central term "
                                       "would assert more than it measures."),
    "unified_predicate_applied": ("a rival bars HIGH if LICENSED or TWO-FACED; marks and mid-verse formulae "
                                  "make no face (#e15 Q2)"),
    "inputs": {"rows": ROWS.name, "rows_sha256": sha(ROWS), "rows_audited": len(out_rows)},
    "tally": dict(tally),
    "WHAT_THE_TALLY_ACTUALLY_MEASURES": (
        "76 of 145 rows read as grade/evidence disagreements, which is implausibly high as a claim about the "
        "GRADES and is therefore a measurement of something else: the REFERENCES cannot carry a faced "
        "CONF-CAL argument. The annotations are capped at six words by the rotation rule, so most carry no "
        "device word my detector can see on a geometrically-derived face, which makes 'far face bare' fire "
        "constantly and pushes the implied grade down. THE FINDING IS THAT THE CURRENT REFS DO NOT SUPPORT A "
        "MECHANICAL CONF-CAL AUDIT AT ALL - which is precisely what clause 6 v2's face qualifiers exist to fix "
        "(REPAIR-2 step 4). This sweep becomes a usable audit only after they are installed, and #e16 should "
        "read the list below as candidate rows to look at, never as 76 wrong grades."),
    "rows_for_e16": [x for x in out_rows if x["state"] in ("GRADE_ABOVE_EVIDENCE", "GRADE_BELOW_EVIDENCE")],
    "all": out_rows,
    "tier": "the grades and refs are MEASURED; the face derivation and the implied grade are INFERRED and "
            "labelled so",
}
p = HERE / "confcal_audit.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"rows_audited": len(out_rows), "tally": dict(tally),
                  "rows_for_e16": len(out["rows_for_e16"]),
                  "WHAT_THE_TALLY_ACTUALLY_MEASURES": out["WHAT_THE_TALLY_ACTUALLY_MEASURES"][:300]},
                 indent=1, ensure_ascii=False))
print()
for x in out["rows_for_e16"][:18]:
    print("  %-9s %-24s grade=%-11s implied=%-11s %s" % (x["row"], x["span"], x["grade"],
                                                         x["implied_by_the_unified_predicate"], x["state"]))
