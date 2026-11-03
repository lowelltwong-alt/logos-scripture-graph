#!/usr/bin/env python3
"""Fixture for land_fixup3.py, on a temporary scratch folder named by argv[1]. Case 1: an edit that breaks nothing lands with only the
CWO-06 and -07 items it left undone reported, so the validators ran on the applied copy. Case 2: a span change is reported as a problem. Case 3: an unlogged change is reported.
Case 4: an unsorted row order is reported. Writes nothing under the worktree except landed3/W4_e1, which it removes.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BK = HERE.parents[1]
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\af84b702-d913-4495-8e57-252cf7894c63\scratchpad")
PART = "W4"
src = SCR / "cor_fx3" / PART
dest = BK / "fixup/landed3" / (PART + "_e1")
if dest.exists():
    sys.exit("REFUSED: a real landing is present")
out = Path(sys.argv[1])
os.makedirs(out, exist_ok=True)
rows = [json.loads(x) for x in (BK / "fixup/draft_rows_fixup2_applied.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
mine = [r for r in rows if r["decision_id"].startswith(PART + "-")]
env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def case(name, rr, chg):
    rf, cf = src / ("fixup3_%s_rows.jsonl" % PART), src / ("fixup3_%s_changes.json" % PART)
    rf.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rr), encoding="utf-8", newline="\n")
    cf.write_text(json.dumps(chg), encoding="utf-8", newline="\n")
    ro = out / (name + ".json")
    p = subprocess.run([sys.executable, "-B", str(HERE / "land_fixup3.py"), "land", "--part", PART, "--rows-sha", sha(rf), "--changes-sha", sha(cf), "--tokens", "1",
                        "--tool-uses", "1", "--duration-ms", "1", "--row-out", str(ro)], capture_output=True, text=True, encoding="utf-8", env=env)
    if p.returncode:
        sys.exit(p.stderr[-800:])
    return json.loads(ro.read_text(encoding="utf-8"))["orchestrator_verification"]["problems"]


results = {}
try:
    os.makedirs(src, exist_ok=True)
    a = json.loads(json.dumps(mine[0]))
    a["device_notes"] = str(a.get("device_notes", "")) + " Added fixture sentence for this row alone."
    p = case("clean", [a], {"changes": [{"row": a["decision_id"], "field": "device_notes"}], "blocked": []})
    results["clean_lands_only_cwo_left"] = all(x.startswith(("CWO-06 left", "CWO-07 left")) for x in p) and len(p) == 2
    b = json.loads(json.dumps(a))
    b["span"] = "1Cor.11.2-1Cor.11.3"
    p = case("span", [b], {"changes": [{"row": a["decision_id"], "field": "device_notes"}, {"row": a["decision_id"], "field": "span"}], "blocked": []})
    results["span_change_reported"] = any("span changed outside" in x for x in p)
    p = case("unlogged", [a], {"changes": [], "blocked": []})
    results["unlogged_reported"] = any("not in the change log" in x for x in p)
    c = json.loads(json.dumps(mine[1]))
    c["device_notes"] = str(c.get("device_notes", "")) + " Another fixture sentence, this one for the second row."
    p = case("order", [c, a], {"changes": [{"row": a["decision_id"], "field": "device_notes"}, {"row": c["decision_id"], "field": "device_notes"}], "blocked": []})
    results["order_reported"] = any("pinned order" in x for x in p)
finally:
    if dest.exists():
        shutil.rmtree(dest)
    for f in src.glob("fixup3_*"):
        f.unlink()
print(json.dumps(results), "PASS" if all(results.values()) else "FAIL")
sys.exit(0 if all(results.values()) else 1)
