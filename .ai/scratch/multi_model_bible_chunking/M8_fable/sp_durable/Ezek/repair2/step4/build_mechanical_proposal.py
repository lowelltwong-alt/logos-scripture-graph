#!/usr/bin/env python3
"""STEP 4a - compose the two MECHANICAL plans into one proposal, and judge it before any write.

Plans (both derived on the current rows and distinct-checked):
  face_qualification_plan.v1.json - derived face qualifiers for WARRANT-onset/close (decorrelated reader: 0 contradicted)
  x2_reface_plan.v1.json          - web: -> oshb: for MT-borne device entries outside the zone (identity + device found)

Judgement before write: every replaced entry must occur EXACTLY once in its row; the WHOLE pinned suite runs on the
candidate rows and no hard member may gain a flag against the live rows; the role-token member must verify every
qualifier on the candidate. Only then is proposal.json written for apply_proposal.py.

usage: python build_mechanical_proposal.py --work <dir>
"""
import hashlib
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

sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
work = Path(sys.argv[sys.argv.index("--work") + 1])
work.mkdir(parents=True, exist_ok=True)
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
live_b = ROWS.read_bytes()
face = json.loads((HERE / "face_qualification_plan.v1.json").read_text(encoding="utf-8"))
x2 = json.loads((HERE / "x2_reface_plan.v1.json").read_text(encoding="utf-8"))
if face["inputs"]["rows_sha256"] != sha(ROWS) or x2["rows_sha256"] != sha(ROWS):
    raise SystemExit("REFUSED: a plan was derived on different rows - re-derive both on the current rows")
rows = [json.loads(l) for l in live_b.decode("utf-8").splitlines() if l.strip()]
by = {r["decision_id"]: r for r in rows}
changes = [(i["row"], i["entry_before"], i["entry_after"], "face") for i in face["derivable_now"]] + \
          [(i["row"], i["entry_before"], i["entry_after"], "x2") for i in x2["plan"]]
proposal, tally = {}, Counter()
for rid, before, after, kind in changes:
    refs = proposal.setdefault(rid, {"boundary_evidence_refs": list(by[rid]["boundary_evidence_refs"])})["boundary_evidence_refs"]
    if refs.count(before) != 1:
        raise SystemExit("REFUSED: %s entry not present exactly once on %s: %r" % (kind, rid, before[:70]))
    refs[refs.index(before)] = after
    tally[kind] += 1
for rid, f in proposal.items():
    by[rid]["boundary_evidence_refs"] = f["boundary_evidence_refs"]
cand = work / "mechanical_candidate.jsonl"
cand.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")
live = work / "live.jsonl"
live.write_bytes(live_b)
env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
for p in (cand, live):
    subprocess.run([sys.executable, "-B", str(EZ / "tools" / "run_validator_suite.py"), str(p)], cwd=str(EZ / "tools"),
                   capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
rc = json.loads(Path(str(cand) + ".validator_report.json").read_text(encoding="utf-8"))
rl = json.loads(Path(str(live) + ".validator_report.json").read_text(encoding="utf-8"))
cm, lm = SD.members(rc), SD.members(rl)
FLAG_LISTS = {"problems", "flags", "defects", "failures", "offending_7grams", "worklist_citations", "prose_pair_problems"}
gained, lists = {}, 0
for name in set(cm) | set(lm):
    for k in set(cm.get(name, ({}, {}))[1]) | set(lm.get(name, ({}, {}))[1]):
        if k not in FLAG_LISTS:
            continue
        lists += 1
        add = list((cm.get(name, ({}, {}))[1].get(k, Counter()) - lm.get(name, ({}, {}))[1].get(k, Counter())).elements())
        if add:
            gained[name] = gained.get(name, 0) + len(add)
if lists == 0:
    raise SystemExit("REFUSED: zero flag lists compared (E-36)")
hard_gained = {n: v for n, v in gained.items() if n in SD.HARD}
rt = subprocess.run([sys.executable, "-B", str(HERE / "check_role_tokens.py"), str(cand), "--phase", "pre"],
                    capture_output=True, text=True, encoding="utf-8", env=env)
role = json.loads(rt.stdout[rt.stdout.find("{"):])
verdict = {"changes": dict(tally), "rows": len(proposal), "summary_live": rl.get("summary"),
           "summary_candidate": rc.get("summary"), "hard_members_gained": hard_gained,
           "triage_members_gained": {n: v for n, v in gained.items() if n not in SD.HARD},
           "role_token_member": {"status": role["status"], "flags": role["flag_count"], "counts": role["counts"]}}
print(json.dumps(verdict, ensure_ascii=False, indent=1))
if hard_gained or role["flag_count"]:
    raise SystemExit("REFUSED: the candidate gained hard flags or the role-token member flagged a qualifier")
out = HERE / "mechanical_proposal.v1.json"
out.write_text(json.dumps(proposal, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
(HERE / "mechanical_proposal_verdict.v1.json").write_text(json.dumps(verdict, ensure_ascii=False, indent=1),
                                                         encoding="utf-8", newline="\n")
print("proposal:", out.name, "sha256:", sha(out))
