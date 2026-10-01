"""Do the section-9 vectors discriminate? Run the STAGED test file against the INSTALLED tools (a scratch copy of SP), and
list exactly which checks fail. A vector that passes on both the installed and the staged tools pins behaviour that was
already there (a control). A vector that fails on the installed tools and passes on the staged ones proves the edit.
Every section-1..8 check must still pass on the installed tools, or the staged test file changed an old expectation."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
SCR = Path(__file__).resolve().parent
ROOT = SCR / "stage_t4fix_baseline"
T = ROOT / "sp_durable" / "Ezek" / "tools"
STAGED_TEST = SCR / "stage_t4fix" / "sp_durable" / "Ezek" / "tools" / "_test_zone_tools_ezek.py"
EXPECT_FAIL_ON_INSTALLED = {"cs_t4_01_decoy_letter_id_ok", "cs_t4_03_puncta_denial_after_nonsite_ok", "cs_t4_04_site_without_disclosure",
                            "cs_t4_03_puncta_denial_after_at_site",
                            "cal_t4_03_apposition_denial_ok", "cal_t4_03_parenthesis_denial_ok", "cal_t4_03_absent_at_clause_end_ok",
                            "cm_t4_01_decoy_letter_id_ok", "cm_t4_03_denial_after_nonsite_ok", "cm_t4_03_denial_after_at_site_flags"}

assert ROOT.parent == SCR and ROOT.name == "stage_t4fix_baseline"
if ROOT.exists():
    shutil.rmtree(ROOT)
ign = shutil.ignore_patterns("__pycache__", "*.pyc")
shutil.copytree(SP / "Ezek" / "tools", T, ignore=ign)
shutil.copytree(SP / "Jer" / "tools", ROOT / "sp_durable" / "Jer" / "tools", ignore=ign)
for f in (SP / "Ezek").iterdir():
    if f.is_file():
        shutil.copy2(f, ROOT / "sp_durable" / "Ezek" / f.name)
shutil.copyfile(STAGED_TEST, T / "_test_zone_tools_ezek.py")
p = subprocess.run([sys.executable, str(T / "_test_zone_tools_ezek.py")], capture_output=True, text=True, encoding="utf-8",
                   env=dict(os.environ, PYTHONIOENCODING="utf-8"), cwd=str(T))
d = json.loads(p.stdout)
failed = [f.get("check", "") for f in d["failed"]]   # the test file's check() records its label under "check"
failed_ids = {n.split(" ")[1].rstrip(":") for n in failed if " " in n}
print(json.dumps({"checks": d["checks"], "passed": d["passed"], "failed_checks": failed,
                  "failed_vector_ids": sorted(failed_ids),
                  "fail_on_installed_as_expected": sorted(failed_ids & EXPECT_FAIL_ON_INSTALLED),
                  "expected_to_fail_but_passed_on_installed": sorted(EXPECT_FAIL_ON_INSTALLED - failed_ids),
                  "failed_but_not_expected": sorted(failed_ids - EXPECT_FAIL_ON_INSTALLED),
                  "verdict": "DISCRIMINATING" if failed_ids == EXPECT_FAIL_ON_INSTALLED else "CHECK"}, ensure_ascii=False, indent=1))
