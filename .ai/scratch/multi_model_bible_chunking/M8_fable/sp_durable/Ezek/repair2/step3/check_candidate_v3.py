#!/usr/bin/env python3
"""REPAIR-2 step-3 CANDIDATE GATE, v3. Read-only on the corpus.

WHAT v3 ADDS OVER v2, and why each addition exists.
  1. THE WHOLE PINNED SUITE runs on the candidate rows (live rows with the proposal applied, in a work directory
     outside the corpus), diffed item by item against the live rows' own report. v2 ran two members; the step-2
     adjudicator iterated to ALL_CLEAN on them and the full suite still found a citation-sweep disclosure duty it
     could not see (E-34 addendum). A gate that is a subset of the suite repeats E-34 one level down.
  2. SCOPE FROM THE WORKLIST: a row may change only if the step-3 worklist owes it an item, and only in the fields
     those items name. Step 3 legitimately rewords and removes refs entries, so v2's append-only rule is replaced by
     a scope rule plus form checks on every new or changed entry.
  3. SIGNALS: observed_substrate_signals may change only on a row whose owed item names that field.
Kept from v2: register and mirroring per row, and v2's entry-form checks (pinned vocabulary, no face qualifier yet,
1-6 word annotation, MT devices on oshb:, quotations on web:, dual form in the zone mapped by the offset map).

A SELFTEST WITH FIXTURES THAT MUST FAIL runs first and gates every verdict (E-36).

usage: python check_candidate_v3.py <proposal.json> --work <dir>
       python check_candidate_v3.py --selftest
"""
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
sys.path.insert(0, str(EZ / "repair2" / "step2_reconciliation"))
import check_candidate_v2 as V2                                                # noqa: E402

WORKLIST = HERE / "step3_worklist.v1.json"
SUITE_DELTA = EZ / "repair2" / "suite_delta.py"
PROSE, REFS, SIG = V2.PROSE, V2.REFS, "observed_substrate_signals"


def scope():
    wl = json.loads(WORKLIST.read_text(encoding="utf-8"))
    allowed = {}
    for i in wl["items"]:
        if i["status"] == "DISCHARGED":
            continue
        fs = allowed.setdefault(i["row"], set())
        for f in i["fields"]:
            if f in PROSE or f in (REFS, SIG):
                fs.add(f)
            else:                                       # 'per the order' and the combined ADJ phrasing open all three
                fs.update(PROSE)
                fs.add(REFS)
                if "signals" in f:
                    fs.add(SIG)
    return allowed


def check_row(live_row, fields, allowed_fields):
    probs = []
    for f in fields:
        if f not in allowed_fields:
            probs.append({"field": f, "problem": "no owed step-3 item on this row names this field"})
    cand = dict(live_row)
    cand.update({f: v for f, v in fields.items() if f in allowed_fields})
    if REFS in fields and REFS in allowed_fields:
        old = list(live_row.get(REFS) or [])
        for e in fields[REFS]:
            if e in old:
                continue
            for p in V2.check_new_entry(e):
                probs.append({"field": REFS, "entry": e, "problem": p})
    flags = V2.CR.scan_row(cand, "candidate")
    a = V2.CM.analyze_row(cand)
    unm = [{"citation": x.get("citation"), "field": x.get("field")} for x in (a.get("items") or [])]
    orph, dis = a.get("orphan_refs") or [], a.get("mirror_reading_disagreements") or []
    return {"clean": not (probs or flags or unm or orph or dis), "form_problems": probs,
            "register_flags": [{"field": f["field"], "class": f["class"], "match": f["match"]} for f in flags],
            "unmirrored_argued_citations": unm, "orphan_refs": orph, "mirror_reading_disagreements": dis}


def selftest():
    live, sc = V2.live_rows(), scope()
    cases = []
    out_row = next(r for r in live if r not in sc)
    cases.append(("a row the worklist owes nothing is refused",
                  not check_row(live[out_row], {"device_notes": "x"}, set())["clean"]))
    r = "P09-010"
    cases.append(("P09-010 is in scope with refs and signals", r in sc and REFS in sc[r] and SIG in sc[r]))
    q = list(live[r][REFS]) + ["oshb:Ezek.39.21 [WARRANT-onset:near] onset verse"]
    cases.append(("a face qualifier is still refused in step 3",
                  any("step-4" in p["problem"] for p in check_row(live[r], {REFS: q}, sc[r])["form_problems"])))
    removed = [e for e in live[r][REFS] if "39.23" not in e]
    res = check_row(live[r], {REFS: removed}, sc[r])
    cases.append(("REMOVING an ordered entry is allowed in step 3", not res["form_problems"]))
    cases.append(("a signals change on a row whose items do not name signals is refused",
                  not check_row(live["P02-003"], {SIG: {}}, sc.get("P02-003", set()))["clean"]))
    cases.append(("a bare rule id is a register flag",
                  bool(check_row(live[r], {"device_notes": "held under CUT-RULE limb (b)"}, sc[r])["register_flags"])))
    failed = [n for n, ok in cases if not ok]
    print(json.dumps({"selftest_cases": len(cases), "failed": failed}, indent=1))
    return 1 if failed else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    if selftest():
        raise SystemExit("REFUSED: selftest failed; no verdict computed (E-36)")
    prop = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    work = Path(sys.argv[sys.argv.index("--work") + 1])
    live, sc = V2.live_rows(), scope()
    per_row = {rid: (check_row(live[rid], f, sc.get(rid, set())) if rid in live else
                     {"clean": False, "form_problems": [{"problem": "no such row"}]}) for rid, f in prop.items()}
    # the candidate rows file, and the WHOLE suite on it
    work.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(l) for l in V2.ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
    for r in rows:
        for f, v in (prop.get(r["decision_id"]) or {}).items():
            if f in sc.get(r["decision_id"], set()):
                r[f] = v
    cand = work / "candidate_rows.jsonl"
    cand.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    base_work = work / "live"
    base_work.mkdir(exist_ok=True)
    suite = subprocess.run([sys.executable, "-B", str(EZ / "tools" / "run_validator_suite.py"), str(cand)],
                           cwd=str(EZ / "tools"), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    rep_c = Path(str(cand) + ".validator_report.json")
    live_copy = base_work / "live_rows.jsonl"
    live_copy.write_bytes(V2.ROWS.read_bytes())
    subprocess.run([sys.executable, "-B", str(EZ / "tools" / "run_validator_suite.py"), str(live_copy)],
                   cwd=str(EZ / "tools"), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    rep_l = Path(str(live_copy) + ".validator_report.json")
    if not (rep_c.exists() and rep_l.exists()):
        raise SystemExit("REFUSED: the suite did not report on both the candidate and the live rows")
    sys.path.insert(0, str(EZ / "repair2"))
    import suite_delta as SD
    bm, cm = SD.members(json.loads(rep_l.read_text(encoding="utf-8"))), SD.members(json.loads(rep_c.read_text(encoding="utf-8")))
    FLAG_LISTS = {"problems", "flags", "defects", "failures", "offending_7grams", "worklist_citations", "prose_pair_problems"}
    gained, cleared, lists = {}, {}, 0
    for name in sorted(set(bm) | set(cm)):
        for k in set(bm.get(name, ({}, {}))[1]) | set(cm.get(name, ({}, {}))[1]):
            if k not in FLAG_LISTS:
                continue
            lists += 1
            b, c = bm.get(name, ({}, {}))[1].get(k), cm.get(name, ({}, {}))[1].get(k)
            from collections import Counter
            b, c = b or Counter(), c or Counter()
            add, rem = list((c - b).elements()), list((b - c).elements())
            if add:
                gained.setdefault(name, []).extend(json.loads(x) for x in add)
            if rem:
                cleared.setdefault(name, []).extend(json.loads(x) for x in rem)
    if lists == 0:
        raise SystemExit("REFUSED: zero flag lists compared (E-36)")
    hard_gained = {n: v for n, v in gained.items() if n in SD.HARD}
    all_clean = all(v["clean"] for v in per_row.values()) and not hard_gained
    print(json.dumps({"ALL_CLEAN": all_clean,
                      "rows_unclean": sorted(k for k, v in per_row.items() if not v["clean"]),
                      "suite": {"hard_members_that_GAINED_flags": hard_gained,
                                "triage_members_that_gained_flags": {n: len(v) for n, v in gained.items() if n not in SD.HARD},
                                "flags_CLEARED": {n: len(v) for n, v in cleared.items()},
                                "candidate_summary": json.loads(rep_c.read_text(encoding="utf-8")).get("summary")},
                      "per_row": per_row}, ensure_ascii=False, indent=1))
    return 0 if all_clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
