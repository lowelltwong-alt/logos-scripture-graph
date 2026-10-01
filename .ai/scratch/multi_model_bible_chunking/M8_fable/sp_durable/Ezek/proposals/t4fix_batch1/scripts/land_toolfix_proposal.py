"""Land the staged tool-edit proposal DURABLY for the controlling agent (#e4), without installing anything.

Re-runs stage_t4fix_patch.py, which rebuilds the stage from the installed SP bytes, so the proposal is reproducible, and
stage_t4fix_discrimination.py, which runs the staged vectors against the installed tools. Then it writes, under
SP/Ezek/proposals/<batch>/:
  staged/<file>      the five staged files, byte for byte;
  diffs/<file>.diff  a unified diff from the installed file to the staged one;
  scripts/           the patch and discrimination scripts that produced them;
  runs/              both scripts' JSON output;
  manifest.json      installed and staged digests, test counts on both sides, suite parity, and disclosed residuals.
The run refuses if the batch directory already exists; a landed proposal is never replaced, and a revision is a new batch.

Usage: land_toolfix_proposal.py --batch t4fix_batch1 --findings T4-01,T4-03,T4-04"""
import argparse
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
EZ = SP / "Ezek"
SCR = Path(__file__).resolve().parent
STAGE_T = SCR / "stage_t4fix" / "sp_durable" / "Ezek" / "tools"
FILES = ("citation_sweep.py", "check_marks.py", "_adapt_zone_tools_ezek.py", "_test_zone_tools_ezek.py", "TOOLKIT.md")
SCRIPTS = ("stage_t4fix_patch.py", "stage_t4fix_discrimination.py", "land_toolfix_proposal.py")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run_json(script):
    p = subprocess.run([sys.executable, str(SCR / script)], capture_output=True, text=True, encoding="utf-8", env=ENV, cwd=str(SCR))
    if p.returncode != 0:
        raise SystemExit("ABORT: %s exited %d: %s" % (script, p.returncode, (p.stderr or p.stdout)[-800:]))
    return p.stdout, json.loads(p.stdout)


ap = argparse.ArgumentParser()
ap.add_argument("--batch", required=True)
ap.add_argument("--findings", required=True)
a = ap.parse_args()
OUT = EZ / "proposals" / a.batch
if OUT.exists():
    raise SystemExit("ABORT: %s exists; a landed proposal is never replaced (write a new batch)" % OUT)

patch_raw, patch = run_json("stage_t4fix_patch.py")
disc_raw, disc = run_json("stage_t4fix_discrimination.py")
gate = {"tests_green": (patch.get("tests") or {}).get("verdict") == "GREEN",
        "toolkit_selfcheck_green": (patch.get("toolkit_selfcheck") or {}).get("verdict") == "GREEN",
        "ezek_lib_selftest_ok": patch.get("ezek_lib_selftest_exit") == 0,
        "suite_parity_none": patch.get("suite_list_differences") == "NONE",
        "vectors_discriminate": disc.get("verdict") == "DISCRIMINATING",
        "staged_digests_reproduced": all(sha(STAGE_T / n) == patch["staged_digests"][n] for n in FILES)}
if not all(gate.values()):
    print(json.dumps({"gate": gate, "patch": patch, "discrimination": disc}, ensure_ascii=False, indent=1))
    raise SystemExit("ABORT: the proposal does not pass its own gate; nothing landed")

for sub in ("staged", "diffs", "scripts", "runs"):
    (OUT / sub).mkdir(parents=True, exist_ok=False)
files = {}
for n in FILES:
    inst, stg = EZ / "tools" / n, STAGE_T / n
    shutil.copyfile(stg, OUT / "staged" / n)
    diff = "".join(difflib.unified_diff(inst.read_text(encoding="utf-8").splitlines(True), stg.read_text(encoding="utf-8").splitlines(True),
                                        fromfile="SP/Ezek/tools/%s (installed %s)" % (n, sha(inst)[:12]),
                                        tofile="proposals/%s/staged/%s (staged %s)" % (a.batch, n, sha(stg)[:12])))
    (OUT / "diffs" / (n + ".diff")).write_text(diff, encoding="utf-8", newline="\n")
    files[n] = {"installed_sha256": sha(inst), "staged_sha256": sha(OUT / "staged" / n),
                "staged_path": "Ezek/proposals/%s/staged/%s" % (a.batch, n), "diff_path": "Ezek/proposals/%s/diffs/%s.diff" % (a.batch, n),
                "diff_lines": diff.count("\n")}
for s in SCRIPTS:
    shutil.copyfile(SCR / s, OUT / "scripts" / s)
(OUT / "runs" / "stage_patch_run.json").write_text(patch_raw, encoding="utf-8", newline="\n")
(OUT / "runs" / "discrimination_run.json").write_text(disc_raw, encoding="utf-8", newline="\n")
manifest = {
    "schema": "m8_tool_edit_proposal.v1", "book": "Ezek", "batch": a.batch, "built": datetime.now(timezone.utc).isoformat(),
    "built_by": "orchestrator (claude-opus-5) under OW-11; proposes, never rules",
    "status": "PROPOSAL - NOT INSTALLED. For ezek_controlling_rulings_a1#e4 to rule; any install is followed by a fresh distinct review before any cure claim.",
    "findings_addressed": a.findings.split(","),
    "installed_baseline": "SP/campaign/receipts/ezek_tools_install_r4ii_cal1.json (after-digests)",
    "files": files,
    "tests": {"staged_tools": patch["tests"], "installed_tools_with_staged_test_file": {k: disc[k] for k in ("checks", "passed", "failed_vector_ids")},
              "discrimination": disc["verdict"]},
    "toolkit_selfcheck": patch["toolkit_selfcheck"], "ezek_lib_selftest_exit": patch["ezek_lib_selftest_exit"],
    "suite_parity_on_chain_head": {"rows": "Ezek/repair/rows_v3_cwo12.jsonl", "rows_sha256": sha(EZ / "repair" / "rows_v3_cwo12.jsonl"),
                                   "compared_with": "Ezek/repair/suite_v3_2acbc045/rows.jsonl.validator_report.json",
                                   "list_differences": patch["suite_list_differences"], "summaries": patch["suite_summary"]},
    "gate": gate,
    "residuals_disclosed": [
        "T4-03: a denial behind a comma stays outside the mention's clause, so 'a dateline at 45:18 would be expected, though none stands' stays RED (pinned as cal_t4_03_denial_behind_comma_residual_red). A RED on a HARD tool forces a rewording; it never passes a false claim silently.",
        "T4-03: DENIAL_AFTER is a closed set (but/though/although/yet none; none stands / is present / written / there / found; appears; exists; is or are absent / lacking / missing at the clause end). Any other later denial phrasing is not read as a denial.",
        "T4-04: the single-witness check is in citation_sweep's PUNCTA ref arm only, where its sibling mark, small-letter and paseq checks live; check_marks' prose arms carry that check for no mark. It accepts 'single-witness' and 'single witness'; the sibling arms accept only the hyphenated form.",
        "T4-01: the letter guard applies to every C:V or C.V number these arms read (clause, parenthetical, list, apposition), not only the parenthetical T4 attacked.",
        "R4ii-D1 (PROSE_REACH=60) is untouched by this batch; it is the controlling agent's ruling."],
    "scripts": {s: sha(OUT / "scripts" / s) for s in SCRIPTS},
    "runs": {"stage_patch_run.json": sha(OUT / "runs" / "stage_patch_run.json"), "discrimination_run.json": sha(OUT / "runs" / "discrimination_run.json")},
}
(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"landed": str(OUT), "manifest_sha256": sha(OUT / "manifest.json"), "gate": gate,
                  "staged": {n: f["staged_sha256"][:16] for n, f in files.items()}}, ensure_ascii=False, indent=1))
