#!/usr/bin/env python3
"""REPAIR-2 step-5 CANDIDATE GATE, v5 - the register prose pass.

A prose pass is the step most able to change a claim while looking like a wording fix: E13-86 is the orchestrator's
own register substitution, green at the gate and broken as English. v5 keeps everything v4 checks and adds three
arms aimed at that failure, each a FLOOR under the reading the lanes and the adjudicator owe, never a substitute:

  1. CLAIM ACCOUNTING. Anchors are extracted from a row's prose fields together: face references (oshb:/web:), verse
     numbers (MT 22:31 and 22:31 read as one anchor), Hebrew runs, evidence-tier words, counts ("33 verses"), and
     curly-quoted English. An anchor present before and absent after must be ACCOUNTED FOR in the lane's
     discharge.json under claim_accounting[row] as {"anchor": <exact>, "why": <...>}; an unaccounted removal makes
     the row unclean. Added anchors are reported as data for the adjudicator. Row-level, so a claim may move between
     fields without accounting.
  2. ENGLISH FORM (delta: only occurrences the proposal introduces). A doubled word, an immediately repeated
     two-word phrase, a sentence beginning in lower case, and an unbalanced parenthesis or curly quote. Of E13-86's
     five breakages this catches three by fixture; a doubled article across a noun and a dropped clause boundary are
     not mechanically visible, and the selftest says so rather than pretending.
  3. COMPLETION MEASURE after the whole suite: register flags left on the rows the worklist owes, and web_quotes
     flags left book-wide, reported beside the verdict.

Kept from v4: the per-row delta against the live row (no NEW register flag, unmirrored citation, orphan ref or
mirror disagreement), the refs entry form with clause 6 v2 qualifiers, and the WHOLE pinned suite on the candidate
with no hard member allowed to gain a flag. Scope: the prose fields of a row the step-5 worklist owes; refs only
where an item names them; never grade, span, identity or signals.

usage: python check_candidate_v5.py <proposal.json> --work <dir> [--discharge <discharge.json>] [--worklist <path>]
       python check_candidate_v5.py --selftest [--worklist <path>]
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
sys.path.insert(0, str(EZ / "repair2" / "step3"))
sys.path.insert(0, str(EZ / "repair2" / "step4"))
import check_candidate_v3 as V3                                                # noqa: E402
import check_candidate_v3_1 as V31                                             # noqa: E402
import check_candidate_v4 as V4                                                # noqa: E402

V2 = V3.V2
REFS = V3.REFS
PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess")


def _arg(name):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None


WORKLIST = Path(_arg("--worklist") or (HERE / "step5_worklist.v1.json"))
HEB = "֐-׿יִ-ﭏ"
A_FACE = re.compile(r"(?:oshb|web):Ezek\.\d{1,2}\.\d{1,3}(?:-Ezek\.\d{1,2}\.\d{1,3})?")
A_CV = re.compile(r"(?<![\d.:])(\d{1,2}):(\d{1,3})(?![\d])")
A_HEB = re.compile(r"[%s]+(?:[\s־]+[%s]+)*" % (HEB, HEB))
A_TIER = re.compile(r"\b(MEASURED|EXTRACTED|TRANSCRIBED|REPORTED|INFERRED|ASSUMED|UNAVAILABLE)\b")
A_COUNT = re.compile(r"\b(\d+)[ -](verses?|occurrences?|members?|words?)\b", re.I)
A_QUOTE = re.compile(r"“([^”]{3,})”")


def anchors(row):
    out = set()
    for f in PROSE:
        t = row.get(f) or ""
        if not isinstance(t, str):
            continue
        out |= {"face " + m.group(0) for m in A_FACE.finditer(t)}
        stripped = A_FACE.sub(" ", t)
        out |= {"verse %s:%s" % (m.group(1), m.group(2)) for m in A_CV.finditer(stripped)}
        out |= {"hebrew " + m.group(0) for m in A_HEB.finditer(t)}
        out |= {"tier " + m.group(1) for m in A_TIER.finditer(t)}
        out |= {"count %s %s" % (m.group(1), m.group(2).lower().rstrip("s")) for m in A_COUNT.finditer(t)}
        out |= {"quote " + m.group(1) for m in A_QUOTE.finditer(t)}
    return out


E_DOUBLE = re.compile(r"\b([A-Za-z]{2,})\s+\1\b", re.I)
E_BIGRAM = re.compile(r"\b([A-Za-z]+ [A-Za-z]+) \1\b", re.I)
E_LOWER = re.compile(r"(?<!\be\.g)(?<!\bi\.e)(?<!\bcf)(?<!\bvs)(?<!\bff)(?<!\bv)(?<!\bvv)\. (?!oshb:|web:|ve'|we-)([a-z])")


def english(text):
    if not isinstance(text, str):
        return Counter()
    c = Counter()
    for m in E_DOUBLE.finditer(text):
        c["doubled word '%s'" % m.group(0)] += 1
    for m in E_BIGRAM.finditer(text):
        c["repeated phrase '%s'" % m.group(0)] += 1
    for m in E_LOWER.finditer(text):
        c["sentence begins lower case at '...%s'" % text[max(0, m.start() - 20):m.end() + 12]] += 1
    if text.count("(") != text.count(")"):
        c["unbalanced parentheses"] += 1
    if text.count("“") != text.count("”"):
        c["unbalanced curly quotes"] += 1
    return c


DISCHARGE = {}


def scope():
    wl = json.loads(WORKLIST.read_text(encoding="utf-8"))
    sc = {}
    for i in wl["items"]:
        if i["status"] == "DONE":
            continue
        s = sc.setdefault(i["row"], set(PROSE))
        if REFS in (i.get("fields_hint") or []):
            s.add(REFS)
    return sc


def check_row(live_row, fields, allowed):
    res = V31.check_row(live_row, fields, allowed)
    cand = dict(live_row)
    cand.update({f: v for f, v in fields.items() if f in allowed})
    before, after = anchors(live_row), anchors(cand)
    acc = {a.get("anchor") for a in (DISCHARGE.get("claim_accounting", {}).get(live_row["decision_id"]) or [])
           if isinstance(a, dict) and a.get("why")}
    removed = sorted(before - after)
    res["claim_removed_accounted"] = [a for a in removed if a in acc]
    res["claim_removed_UNACCOUNTED"] = [a for a in removed if a not in acc]
    res["claim_added_for_the_adjudicator"] = sorted(after - before)
    new_eng = {}
    for f in PROSE:
        if f in fields and f in allowed:
            d = english(cand.get(f)) - english(live_row.get(f))
            if d:
                new_eng[f] = sorted(d.elements())
    res["NEW_english_form_problems"] = new_eng
    res["clean"] = bool(res["clean"] and not res["claim_removed_UNACCOUNTED"] and not new_eng)
    return res


def selftest():
    global DISCHARGE
    live, sc = V2.live_rows(), scope()
    V2.check_new_entry = V4.check_new_entry
    cases = []
    cases.append(("E13-86 #3: 'the division the division plan' is a repeated phrase",
                  any("repeated phrase" in k for k in english("the division the division plan holds"))))
    cases.append(("E13-86 #2: a sentence beginning lower case is caught",
                  any("lower case" in k for k in english("It is not capped. the mark falls after 22:31."))))
    cases.append(("a doubled word is caught", any("doubled" in k for k in english("the the witness records a samekh"))))
    cases.append(("clean English passes", not english("It is not capped (MT 22:31). The witness records a samekh.")))
    cases.append(("an abbreviation or a face reference after a full stop is not a sentence start",
                  not english("Compare e.g. the close. oshb:Ezek.4.4 carries no formula.")))
    cases.append(("NOT CAUGHT, BY DESIGN AND DISCLOSED: E13-86 #1 'the pinned the section-mark record' - reading owns it",
                  not any("doubled" in k or "repeated" in k for k in english("Read off the pinned the section-mark record"))))
    rid = next(r for r in sorted(sc) if any(A_CV.search(live[r].get(f) or "") for f in PROSE))
    field = next(f for f in PROSE if A_CV.search(live[rid].get(f) or ""))
    # strip EVERY prose field of the row: accounting is row-level, so a verse the row cites in two fields is not removed
    # by stripping one (a first version of this fixture passed on one worklist and went vacuous on another)
    stripped = {f: A_CV.sub("that verse", A_FACE.sub("that verse", live[rid][f])) for f in PROSE if isinstance(live[rid].get(f), str)}
    stripped_text = stripped[field]
    DISCHARGE = {}
    r1 = check_row(live[rid], stripped, sc[rid])
    cases.append(("removing a verse number without accounting is UNCLEAN", bool(r1["claim_removed_UNACCOUNTED"]) and not r1["clean"]))
    DISCHARGE = {"claim_accounting": {rid: [{"anchor": a, "why": "selftest"} for a in r1["claim_removed_UNACCOUNTED"]]}}
    r2 = check_row(live[rid], stripped, sc[rid])
    cases.append(("the same removal ACCOUNTED FOR clears the claim arm", not r2["claim_removed_UNACCOUNTED"]))
    DISCHARGE = {}
    cases.append(("a rewrite that introduces a rule id is UNCLEAN",
                  not check_row(live[rid], {field: live[rid][field] + " Held under CUT-RULE limb (b)."}, sc[rid])["clean"]))
    out_row = next(x for x in live if x not in sc)
    cases.append(("a row the step-5 worklist owes nothing is refused",
                  not check_row(live[out_row], {"device_notes": "x"}, set())["clean"]))
    cases.append(("signals and confidence are never in scope", all("confidence" not in s and V3.SIG not in s for s in sc.values())))
    n_anchor = sum(len(anchors(live[r])) for r in sc)
    n_heb = sum(1 for r in sc for a in anchors(live[r]) if a.startswith("hebrew "))
    cases.append(("VACUITY GUARD (E-36): anchors extracted on the owed rows, Hebrew runs among them", n_anchor > 100 and n_heb > 0))
    failed = [n for n, ok in cases if not ok]
    print(json.dumps({"selftest_cases": len(cases), "failed": failed, "anchors_on_owed_rows": n_anchor,
                      "hebrew_anchors": n_heb, "worklist": str(WORKLIST)}, ensure_ascii=False, indent=1))
    return 1 if failed else 0


def main():
    global DISCHARGE
    if "--selftest" in sys.argv:
        return selftest()
    if selftest():
        raise SystemExit("REFUSED: selftest failed; no verdict computed (E-36)")
    DISCHARGE = json.loads(Path(_arg("--discharge")).read_text(encoding="utf-8")) if _arg("--discharge") else {}
    V2.check_new_entry = V4.check_new_entry
    V3.check_row = lambda live_row, fields, allowed: check_row(live_row, fields, allowed)
    V3.scope = scope
    V3.selftest = lambda: 0
    code = V3.main()
    work = Path(_arg("--work"))
    cand_rows = [json.loads(l) for l in (work / "candidate_rows.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    owed = set(scope())
    reg_left = [dict(f, row=r["decision_id"]) for r in cand_rows if r["decision_id"] in owed for f in V2.CR.scan_row(r, "c")]
    rep = json.loads((work / "candidate_rows.jsonl.validator_report.json").read_text(encoding="utf-8"))
    print(json.dumps({"COMPLETION_MEASURE": {
        "register_flags_left_on_owed_rows": len(reg_left),
        "register_left_by_row": dict(Counter(f["row"] for f in reg_left)),
        "web_quotes_flags_left_book_wide": (rep.get("web_quotes") or {}).get("flag_count"),
        "register_member_book_wide": (rep.get("register") or {}).get("flag_count")}}, ensure_ascii=False, indent=1))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
