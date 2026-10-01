#!/usr/bin/env python3
"""Item 23 cure for the v9 fix round: correct the stale Fable wording close lane A found in the retained proposal generator.

Lane A (item_23 fit_to_accept false): MCP-Ezek-004's evidence says a scope cut "merged ... into a single Fable
execution", and the generator header names Fable as adjudicator. Under OW-25 no Fable execution ran for Ezekiel: the items
20-23 check ran inside the two blind claude-opus-5-5 merged-close lanes (OW-26). OW-28 then made Fable the campaign-end
reviewer, so the header's adjudicator is true again once it says WHEN. The fix edits two exact strings in the generator,
re-runs it, and proves: the rebuilt candidate file differs from the old one ONLY in MCP-Ezek-004's evidence_from_this_book,
every adjudication stays null, and --check MATCHes. The old generator and candidate are kept beside them as .pre_<sha12>.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parents[2]
SP = EZ.parent
D = EZ / "deliverables"
GEN, OUT = D / "gen_proposals.py", D / "method_change_proposals.Ezek.candidate.jsonl"
GEN_PIN = "e3c3e0516f9377f01d5389e013389f39c47956fc32e6bd52d687326eee333be7"
OUT_PIN = "bc6c0c597a40a95d4a7e10d88d53bb87878ed5f1c3a50923adee5883279d1d13"
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731
env = dict(os.environ, PYTHONUTF8="1")

EDITS = [
    ("Output: method_change_proposals.Ezek.candidate.jsonl - a CANDIDATE file.",
     "AMENDED 2026-09-23 (v9 fix round, after close lane A found the Fable wording stale under OW-25). No Fable execution\n"
     "ran for Ezekiel: OW-25 put every role on claude-opus-5-5, and OW-26 folded the items 20-23 check into the two blind\n"
     "merged-close lanes. OW-28 then set Fable to review every book at the campaign's end and make the hardest decisions,\n"
     "so these proposals are adjudicated there, and until then every row's adjudication stays null. MCP-Ezek-004's\n"
     "evidence now says what ran.\n"
     "Output: method_change_proposals.Ezek.candidate.jsonl - a CANDIDATE file."),
    ('"BIBLE_CHUNKING_METHOD.v6.md, as one of two scope cuts declared against the OW-22 ceiling (the other "\n'
     '            "merged the scholar-record audit and the items 21-23 check into a single Fable execution). "',
     '"BIBLE_CHUNKING_METHOD.v6.md, as one of two scope cuts declared against the OW-22 ceiling (the other "\n'
     '            "planned to merge the scholar-record audit and the items 21-23 check into a single Fable execution; "\n'
     '            "under OW-25 and OW-26 that check ran instead inside the two blind claude-opus-5-5 merged-close lanes, "\n'
     '            "which judged items 20-23). "'),
]

g = subprocess.run([sys.executable, "-B", str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek",
                    "--target", "Ezek/deliverables/gen_proposals.py",
                    "--target", "Ezek/deliverables/method_change_proposals.Ezek.candidate.jsonl"],
                   cwd=str(SP), capture_output=True, text=True, encoding="utf-8", env=env)
if json.loads(g.stdout)["verdict"] != "CLEAR":
    raise SystemExit("REFUSED by pin guard: " + g.stdout[-400:])
gb, ob = GEN.read_bytes(), OUT.read_bytes()
if sha(gb) != GEN_PIN or sha(ob) != OUT_PIN:
    raise SystemExit("REFUSED: generator or candidate is not at its pinned digest")
src = gb.decode("utf-8")
for old, new in EDITS:
    if src.count(old) != 1:
        raise SystemExit("REFUSED: an edit anchor occurs %d times, not once" % src.count(old))
    src = src.replace(old, new)
for p, b in ((GEN, gb), (OUT, ob)):
    keep = p.with_name(p.name + ".pre_" + sha(b)[:12])
    if keep.exists() and keep.read_bytes() != b:
        raise SystemExit("REFUSED: %s exists with different bytes" % keep.name)
    keep.write_bytes(b)
GEN.write_bytes(src.encode("utf-8"))


def rollback(why):
    GEN.write_bytes(gb)
    OUT.write_bytes(ob)
    raise SystemExit("ROLLED BACK: " + why)


r = subprocess.run([sys.executable, "-B", str(GEN)], cwd=str(D), capture_output=True, text=True, encoding="utf-8", env=env)
if r.returncode:
    rollback("generator failed: " + (r.stdout + r.stderr)[-400:])
old_rows = [json.loads(l) for l in ob.decode("utf-8").splitlines()]
new_rows = [json.loads(l) for l in OUT.read_text(encoding="utf-8").splitlines()]
diff = [(o["proposal_id"], k) for o, n in zip(old_rows, new_rows) for k in o if o[k] != n.get(k)]
if (len(old_rows) != len(new_rows) or [list(o) for o in old_rows] != [list(n) for n in new_rows]
        or diff != [("MCP-Ezek-004", "evidence_from_this_book")] or any(n["adjudication"] is not None for n in new_rows)):
    rollback("the rebuilt candidate differs beyond MCP-Ezek-004's evidence: %s" % diff)
c = subprocess.run([sys.executable, "-B", str(GEN), "--check"], cwd=str(D), capture_output=True, text=True,
                   encoding="utf-8", env=env)
if c.returncode or "MATCH" not in c.stdout:
    rollback("--check did not MATCH: " + c.stdout[-300:])
print(json.dumps({"gen_proposals.py": [GEN_PIN, sha(GEN.read_bytes())], "candidate": [OUT_PIN, sha(OUT.read_bytes())],
                  "changed": diff, "check": c.stdout.strip().splitlines()[0],
                  "new_evidence_tail": new_rows[3]["evidence_from_this_book"][150:420]}, ensure_ascii=False, indent=1))
