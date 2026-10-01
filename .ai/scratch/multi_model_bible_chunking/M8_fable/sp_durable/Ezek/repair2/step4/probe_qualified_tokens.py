#!/usr/bin/env python3
"""STEP-4 COMPATIBILITY PROBE (read-only on the corpus): does the pinned suite survive QUALIFIED role tokens?

No member has ever seen '[WARRANT-onset:near]'. A member whose token stripper expects '[WARRANT-onset]' could read the
colon form as prose, fire an arm on the device word inside it, or stop recognising the entry. So before step 4 writes
a single qualifier, the whole derived plan is applied IN MEMORY to a copy of the live rows and the whole suite is run on
that copy, diffed against the live rows. The staged role-token member runs on the same copy and must verify every one.

usage: python probe_qualified_tokens.py --work <dir>
"""
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
sys.path.insert(0, str(EZ / "repair2"))
import suite_delta as SD                                                       # noqa: E402

work = Path(sys.argv[sys.argv.index("--work") + 1])
work.mkdir(parents=True, exist_ok=True)
plan = json.loads((HERE / "face_qualification_plan.v1.json").read_text(encoding="utf-8"))
live_b = (EZ / "repair" / "rows_v7_cwo24.jsonl").read_bytes()
rows = [json.loads(l) for l in live_b.decode("utf-8").splitlines() if l.strip()]
by = {r["decision_id"]: r for r in rows}
applied = 0
for it in plan["derivable_now"]:
    refs = by[it["row"]]["boundary_evidence_refs"]
    if refs.count(it["entry_before"]) != 1:
        raise SystemExit("REFUSED: plan entry not found exactly once on %s: %r" % (it["row"], it["entry_before"][:60]))
    refs[refs.index(it["entry_before"])] = it["entry_after"]
    applied += 1
cand = work / "qualified_candidate.jsonl"
cand.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")
live = work / "live_rows.jsonl"
live.write_bytes(live_b)
env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
for p in (cand, live):
    subprocess.run([sys.executable, "-B", str(EZ / "tools" / "run_validator_suite.py"), str(p)], cwd=str(EZ / "tools"),
                   capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
rc = json.loads(Path(str(cand) + ".validator_report.json").read_text(encoding="utf-8"))
rl = json.loads(Path(str(live) + ".validator_report.json").read_text(encoding="utf-8"))
cm, lm = SD.members(rc), SD.members(rl)
moved = {}
for name in sorted(set(cm) | set(lm)):
    cs, cl = cm.get(name, ({}, {}))
    ls, ll = lm.get(name, ({}, {}))
    d = {}
    for k in set(cl) | set(ll):
        a, b = cl.get(k, Counter()), ll.get(k, Counter())
        if a != b:
            d[k] = {"added": len(list((a - b).elements())), "removed": len(list((b - a).elements())),
                    "added_examples": [json.loads(x) for x in list((a - b).elements())[:3]]}
    for k in set(cs) | set(ls):
        if cs.get(k) != ls.get(k) and k in ("status", "flag_count"):
            d[k] = {"live": ls.get(k), "qualified": cs.get(k)}
    if d:
        moved[name] = d
rt = subprocess.run([sys.executable, "-B", str(HERE / "check_role_tokens.py"), str(cand), "--phase", "pre"],
                    capture_output=True, text=True, encoding="utf-8", env=env)
role = json.loads(rt.stdout[rt.stdout.find("{"):])
print(json.dumps({"qualifiers_applied_in_memory": applied, "summary_live": rl.get("summary"),
                  "summary_qualified": rc.get("summary"), "members_that_moved": moved,
                  "role_token_member": {"status": role["status"], "flags": role["flag_count"], "counts": role["counts"],
                                        "first_flags": role["flags"][:5]}}, ensure_ascii=False, indent=1))
