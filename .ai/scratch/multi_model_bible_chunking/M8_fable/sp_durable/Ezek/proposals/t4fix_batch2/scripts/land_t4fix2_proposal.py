"""Land TOOLFIX-1 as amended by ezek_controlling_rulings_a1#e4 (t4fix_batch2) DURABLY, without installing anything.

The run:
  - re-runs stage_t4fix2_patch.py, which rebuilds the stage from SP and t4fix_batch1's landed staged files and applies
    A1-A3 and the eight vectors;
  - gates on the result:
      - zone tests GREEN; the ezek_lib selftest and the toolkit selfcheck GREEN;
      - NO list difference from suite_v3_2acbc045 over the chain head (HARD GREEN, triage flags unchanged);
      - every new vector passes staged and fails on at least one baseline (the installed tools or the unamended batch1);
      - batch1's vectors still fail on the installed tools;
      - no unexpected failure on either baseline.
Then it runs the in-flight pin guard and writes SP/Ezek/proposals/t4fix_batch2/ (staged/, diffs/ against the installed
files, diffs_vs_batch1/, scripts/, runs/, manifest.json). The run refuses if the directory exists.

Usage: land_t4fix2_proposal.py --batch t4fix_batch2"""
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
STAGE_T = SCR / "stage_t4fix2" / "sp_durable" / "Ezek" / "tools"
B1 = EZ / "proposals" / "t4fix_batch1"
FILES = ("citation_sweep.py", "check_marks.py", "_adapt_zone_tools_ezek.py", "_test_zone_tools_ezek.py", "TOOLKIT.md")
SCRIPTS = ("stage_t4fix2_patch.py", "land_t4fix2_proposal.py")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def udiff(a_path, b_path, a_label, b_label):
    return "".join(difflib.unified_diff(Path(a_path).read_text(encoding="utf-8").splitlines(True),
                                        Path(b_path).read_text(encoding="utf-8").splitlines(True), fromfile=a_label, tofile=b_label))


ap = argparse.ArgumentParser()
ap.add_argument("--batch", required=True)
a = ap.parse_args()
OUT = EZ / "proposals" / a.batch
if OUT.exists():
    raise SystemExit("ABORT: %s exists; a landed proposal is never replaced" % OUT)
p = subprocess.run([sys.executable, str(SCR / "stage_t4fix2_patch.py")], capture_output=True, text=True, encoding="utf-8", env=ENV, cwd=str(SCR))
if p.returncode != 0:
    raise SystemExit("ABORT: staging failed:\n" + (p.stderr or p.stdout)[-2000:])
run_raw = p.stdout
r = json.loads(run_raw)
dsc = r["discrimination"]
gate = {"tests_green": (r.get("tests") or {}).get("verdict") == "GREEN",
        "ezek_lib_selftest_green": r.get("ezek_lib_selftest") == "GREEN",
        "toolkit_selfcheck_green": (r.get("toolkit_selfcheck") or {}).get("verdict") == "GREEN",
        "suite_parity_none": r.get("suite_list_differences") == "NONE"
                             and (r["suite_summary"]["staged"] or {}).get("hard_status") == "GREEN"
                             and (r["suite_summary"]["staged"] or {}).get("triage_flags") == (r["suite_summary"]["installed"] or {}).get("triage_flags"),
        "new_vectors_discriminate_against_a_baseline": dsc["new_vectors_failing_on_some_baseline"],
        "all_vectors_pass_staged": dsc["all_pass_staged"],
        "batch1_vectors_still_fail_on_installed": dsc["batch1_vectors_still_failing_on_installed"],
        "no_unexpected_failures": not any(dsc["unexpected_failures"].values()),
        "staged_digests_reproduced": all(sha(STAGE_T / n) == r["staged_digests"][n] for n in FILES)}
if not all(gate.values()):
    print(json.dumps({"gate": gate, "run": r}, ensure_ascii=False, indent=1))
    raise SystemExit("ABORT: the proposal does not pass its own gate; nothing landed")
g = subprocess.run([sys.executable, str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek", "--target", str(OUT / "manifest.json")],
                   capture_output=True, text=True, encoding="utf-8")
if g.returncode != 0:
    raise SystemExit("ABORT: the landing target is pinned:\n" + g.stdout)
for d in ("staged", "diffs", "diffs_vs_batch1", "scripts", "runs"):
    (OUT / d).mkdir(parents=True, exist_ok=False)
b1m = json.loads((B1 / "manifest.json").read_text(encoding="utf-8"))
files = {}
for n in FILES:
    inst, stg, b1s = EZ / "tools" / n, STAGE_T / n, B1 / "staged" / n
    shutil.copyfile(stg, OUT / "staged" / n)
    (OUT / "diffs" / (n + ".diff")).write_text(udiff(inst, stg, "SP/Ezek/tools/%s (installed %s)" % (n, sha(inst)[:12]),
                                                     "proposals/%s/staged/%s (%s)" % (a.batch, n, sha(stg)[:12])), encoding="utf-8", newline="\n")
    (OUT / "diffs_vs_batch1" / (n + ".diff")).write_text(udiff(b1s, stg, "proposals/t4fix_batch1/staged/%s (%s)" % (n, sha(b1s)[:12]),
                                                               "proposals/%s/staged/%s (%s)" % (a.batch, n, sha(stg)[:12])), encoding="utf-8", newline="\n")
    files[n] = {"installed_sha256": sha(inst), "batch1_staged_sha256": b1m["files"][n]["staged_sha256"], "staged_sha256": sha(OUT / "staged" / n),
                "staged_path": "Ezek/proposals/%s/staged/%s" % (a.batch, n), "diff_vs_installed": "Ezek/proposals/%s/diffs/%s.diff" % (a.batch, n),
                "diff_vs_batch1": "Ezek/proposals/%s/diffs_vs_batch1/%s.diff" % (a.batch, n)}
for s in SCRIPTS:
    shutil.copyfile(SCR / s, OUT / "scripts" / s)
(OUT / "runs" / "stage_run.json").write_text(run_raw, encoding="utf-8", newline="\n")
manifest = {
    "schema": "m8_tool_edit_proposal.v1", "book": "Ezek", "batch": a.batch, "built": datetime.now(timezone.utc).isoformat(),
    "built_by": "orchestrator (claude-opus-5) under OW-11; executes a ruling, never rules",
    "status": "ADOPTED BY RULING, NOT YET INSTALLED. Install is by digest with one receipt naming ezek_controlling_rulings_a1#e4 ruling "
              "TOOLFIX-1; T5 binds to the installed digests; no cure claim on any file here before T5.",
    "ordered_by": "ezek_controlling_rulings_a1#e4 rulings TOOLFIX-1, T4-03 (A1, A2), T4-04 (A3)",
    "supersedes_proposal": {"batch": "t4fix_batch1", "manifest_sha256": sha(B1 / "manifest.json"), "why": "#e4 adopted it with amendments A1-A3; "
                            "t4fix_batch1 was never installed"},
    "amendments": {"A1": "the copular denial's clause-end lookahead is (?=[.;,()\\n]|$)",
                   "A2": "coordinated-denial guard: a coordinated denial with a verse number and no expectation modal before it does not deny; the "
                         "mention is judged on the numbers before the denial (DENIAL_COORD, DENIAL_COPULAR, EXPECT_MODAL, denial_after, claim_upper; "
                         "puncta_claim_numbers and dateline_claim_numbers take upper=)",
                   "A3": "citation_sweep's mark, small-letter and paseq ref checks test SINGLE_WITNESS (hyphenated or spaced); TOOLKIT.md says so"},
    "files": files,
    "tests": {"staged": r["tests"], "ezek_lib_selftest": r["ezek_lib_selftest"], "toolkit_selfcheck": r["toolkit_selfcheck"]},
    "suite_parity_on_chain_head": {"rows": "Ezek/repair/rows_v3_cwo12.jsonl", "rows_sha256": sha(EZ / "repair" / "rows_v3_cwo12.jsonl"),
                                   "compared_with": "Ezek/repair/suite_v3_2acbc045/rows.jsonl.validator_report.json",
                                   "list_differences": r["suite_list_differences"], "summaries": r["suite_summary"]},
    "discrimination": {
        "baselines": ["the installed tools (SP)", "the unamended t4fix_batch1 staged files over SP"], "per_vector": dsc["per_vector"],
        "baseline_counts": dsc["baseline_counts"], "unexpected_failures": dsc["unexpected_failures"],
        "literal_requirement_note": ("#e4 ruling TOOLFIX-1 asks every new vector to FAIL on the installed tools and PASS staged. Six of the eight do. "
                                     "cs_e4_a2_positive_then_denial_nonsite_red and cm_e4_a2_positive_then_denial_nonsite_flags PASS on the installed "
                                     "tools and FAIL on t4fix_batch1: they pin the silent-pass hole the unamended T4-03 rule opened, which #e4's own "
                                     "trace states the installed tools do not have ('the installed tools flag both'). They are carried as "
                                     "discriminating against batch1 and reported here for T5 rather than counted as meeting the literal wording.")},
    "gate": gate,
    "residuals_disclosed": [
        "T4-03: a denial behind a comma stays outside the clause and reads RED (a rewording order, never a pass).",
        "R4ii-D1: a prose puncta number more than 60 characters from the word on a covering span passes; the primaries' hand-check is permanent.",
        "A2 is traced on the vectors and on the chain head (no list difference); its effect on prose not yet written is T5's to attack both ways."],
    "scripts": {s: sha(OUT / "scripts" / s) for s in SCRIPTS}, "runs": {"stage_run.json": sha(OUT / "runs" / "stage_run.json")},
}
(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"landed": str(OUT), "manifest_sha256": sha(OUT / "manifest.json"), "gate": gate,
                  "staged": {n: f["staged_sha256"][:16] for n, f in files.items()}}, ensure_ascii=False, indent=1))
