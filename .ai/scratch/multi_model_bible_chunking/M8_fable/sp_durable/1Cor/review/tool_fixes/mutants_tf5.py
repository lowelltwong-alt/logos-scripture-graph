"""TF-5 mutants: each breaks one clause of the installed sections; test_cwo0607.py must go RED on every one.
usage: mutants_tf5.py SWEEP.py ROWS.jsonl --work DIR --out RESULT.json
"""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
TEST = HERE.parent / "tools" / "test_cwo0607.py"
sweep, rows, work, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[sys.argv.index("--work") + 1]), Path(sys.argv[sys.argv.index("--out") + 1])
MUTANTS = {"M1 a range token clears": ("if ex or key in seen: continue", "if ex or rg or key in seen: continue"),
           "M2 on_sign dropped": ('elif any(b for a, b in st[js:js + len(qt)]): kind = "on_sign"', 'elif False: kind = "on_sign"'),
           "M3 any C:V lists a verse": (' and "SBL" in u)', ')'),
           "M4 non-difference verses taken": ("if v not in DIFF: continue", "pass")}
work.mkdir(parents=True, exist_ok=True)
src, res = sweep.read_text(encoding="utf-8"), {}
for name, (old, new) in MUTANTS.items():
    if src.count(old) != 1:
        raise SystemExit("mutant anchor not unique: " + name)
    p = work / ("mutant_%s.py" % name[:2])
    p.write_text(src.replace(old, new), encoding="utf-8", newline="\n")
    r = subprocess.run([sys.executable, "-B", str(TEST), str(p), rows, "--work", str(work / name[:2])], capture_output=True,
                       text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    res[name] = {"exit": r.returncode, "red": r.returncode != 0}
verdict = "ALL_RED" if all(v["red"] for v in res.values()) else "A_MUTANT_SURVIVED"
out.write_text(json.dumps({"mutants": res, "verdict": verdict}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
print(verdict, {k: v["exit"] for k, v in res.items()})
sys.exit(0 if verdict == "ALL_RED" else 1)
