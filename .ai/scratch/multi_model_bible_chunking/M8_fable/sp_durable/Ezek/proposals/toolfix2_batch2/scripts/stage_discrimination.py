"""Do a stage's new vectors discriminate? Run the STAGED zone-test file against the INSTALLED tools (a fresh scratch copy of
SP) and compare the failing checks with the declared fix-dependent vectors.
  - Each declared vector must FAIL on the installed tools: it proves the edit.
  - No other check may fail there: an unexpected failure means the staged test file changed an old expectation, or a
    vector was mis-declared.
Usage: stage_discrimination.py --stage <stage dir name under scratch> --expect <json file: list of substrings of check labels>
Prints JSON; exit 0 when DISCRIMINATING."""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
SCR = Path(__file__).resolve().parent

ap = argparse.ArgumentParser()
ap.add_argument("--stage", required=True)
ap.add_argument("--expect", required=True)
a = ap.parse_args()
declared = json.loads(Path(a.expect).read_text(encoding="utf-8"))
staged_test = SCR / a.stage / "sp_durable" / "Ezek" / "tools" / "_test_zone_tools_ezek.py"
if not staged_test.is_file():
    raise SystemExit("ABORT: no staged test file at %s" % staged_test)
root = SCR / (a.stage + "_baseline")
assert root.parent == SCR and root.name.endswith("_baseline")
if root.exists():
    shutil.rmtree(root)
T = root / "sp_durable" / "Ezek" / "tools"
ign = shutil.ignore_patterns("__pycache__", "*.pyc")
shutil.copytree(SP / "Ezek" / "tools", T, ignore=ign)
shutil.copytree(SP / "Jer" / "tools", root / "sp_durable" / "Jer" / "tools", ignore=ign)
for f in (SP / "Ezek").iterdir():
    if f.is_file():
        shutil.copy2(f, root / "sp_durable" / "Ezek" / f.name)
shutil.copyfile(staged_test, T / "_test_zone_tools_ezek.py")
p = subprocess.run([sys.executable, str(T / "_test_zone_tools_ezek.py")], capture_output=True, text=True, encoding="utf-8",
                   env=dict(os.environ, PYTHONIOENCODING="utf-8"), cwd=str(T))
try:
    d = json.loads(p.stdout)
except json.JSONDecodeError:
    print(json.dumps({"verdict": "ERROR", "exit": p.returncode, "stdout_tail": p.stdout[-1500:], "stderr_tail": p.stderr[-1500:]},
                     ensure_ascii=False, indent=1))
    raise SystemExit(2)
failed = [f.get("check", "") for f in d["failed"]]
confirmed = [x for x in declared if any(x in lbl for lbl in failed)]
not_failing = [x for x in declared if x not in confirmed]
unexpected = [lbl for lbl in failed if not any(x in lbl for x in declared)]
out = {"stage": a.stage, "checks": d["checks"], "passed_on_installed": d["passed"], "failed_on_installed": len(failed),
       "declared_fix_dependent": len(declared), "confirmed_failing_on_installed": len(confirmed),
       "declared_but_passing_on_installed": not_failing, "failing_but_not_declared": unexpected,
       "verdict": "DISCRIMINATING" if not not_failing and not unexpected else "CHECK"}
print(json.dumps(out, ensure_ascii=False, indent=1))
raise SystemExit(0 if out["verdict"] == "DISCRIMINATING" else 1)
