"""Land the staged TOOLFIX-2 of ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 (b) DURABLY as SP/Ezek/proposals/toolfix2_batch1,
with its install BLOCKED. The corpus-impact report found a new HARD class that condition (c) returns to the controlling agent
before install. Nothing is installed.

The lander takes the CURRENT stage_tf2b outputs, which must already exist: stage_run.json, corpus_impact.json,
marks_review.json and flags_analysis.json. It re-verifies that the staged files still carry the digests the stage run
recorded.

Gates (all must hold to land):
  - tests GREEN; the ezek_lib selftest, toolkit selfcheck and verifier selftest GREEN;
  - the verifier over the real claims files GREEN;
  - discrimination: no check fails on the installed tools except section-10b vectors;
  - staged digests reproduced.

Writes staged/ (including staged/campaign), diffs/ against the installed files, scripts/, runs/, corpus_impact.json,
marks_review.json, flags_analysis.json and manifest.json. The in-flight pin guard runs first; the batch directory is
never replaced.

Usage: land_tf2b_proposal.py --batch toolfix2_batch1"""
import argparse
import difflib
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
EZ = SP / "Ezek"
SCR = Path(__file__).resolve().parent
ROOT = SCR / "stage_tf2b"
ST = ROOT / "sp_durable"
TOOL_FILES = ("citation_sweep.py", "check_marks.py", "_adapt_zone_tools_ezek.py", "_test_zone_tools_ezek.py", "TOOLKIT.md",
              "ezek_lib.py", "normalize_hebrew_in_json.py", "check_register.py", "check_web_quotes.py")
SCRIPTS = ("stage_tf2b_patch.py", "review_tf2b_marks_changes.py", "analyze_tf2b_flags.py", "land_tf2b_proposal.py")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


ap = argparse.ArgumentParser()
ap.add_argument("--batch", required=True)
a = ap.parse_args()
OUT = EZ / "proposals" / a.batch
if OUT.exists():
    raise SystemExit("ABORT: %s exists; a landed proposal is never replaced" % OUT)
for f in ("stage_run.json", "corpus_impact.json", "marks_review.json", "flags_analysis.json"):
    if not (ROOT / f).is_file():
        raise SystemExit("ABORT: stage output %s is absent; run the patch, the review and the analysis first" % f)
run = json.loads((ROOT / "stage_run.json").read_text(encoding="utf-8"))
impact = json.loads((ROOT / "corpus_impact.json").read_text(encoding="utf-8"))
analysis = json.loads((ROOT / "flags_analysis.json").read_text(encoding="utf-8"))
mreview = json.loads((ROOT / "marks_review.json").read_text(encoding="utf-8"))
disc = run["discrimination_installed"]
gate = {"tests_green": run["tests"].get("verdict") == "GREEN",
        "ezek_lib_selftest_green": run["ezek_lib_selftest"].get("verdict") == "GREEN",
        "toolkit_selfcheck_green": run["toolkit_selfcheck"].get("verdict") == "GREEN",
        "verifier_selftest_green": run["verifier_selftest"].get("verdict") == "GREEN",
        "verifier_real_claims_green": all(v.get("verdict") == "GREEN" for v in run["verifier_real_claims"].values()),
        "discrimination_clean": not disc.get("error") and all("tf2b" in c for c in disc["failed_on_installed"]) and len(disc["failed_on_installed"]) > 0,
        "staged_digests_reproduced": all(sha((ST / name) if name.startswith("campaign/") else (ST / "Ezek" / "tools" / name)) == d
                                         for name, d in run["staged_digests"].items())}
if not all(gate.values()):
    print(json.dumps({"gate": gate}, indent=1))
    raise SystemExit("ABORT: gate failed; nothing landed")
g = subprocess.run([sys.executable, str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek", "--target", str(OUT / "manifest.json")],
                   capture_output=True, text=True, encoding="utf-8")
if g.returncode != 0:
    raise SystemExit("ABORT: the landing target is pinned:\n" + g.stdout)
for d in ("staged/campaign", "diffs", "scripts", "runs"):
    (OUT / d).mkdir(parents=True, exist_ok=False)
files = {}
for name in list(TOOL_FILES) + ["campaign/_cure_verification.py"]:
    inst = (SP / name) if name.startswith("campaign/") else (EZ / "tools" / name)
    stg = (ST / name) if name.startswith("campaign/") else (ST / "Ezek" / "tools" / name)
    dst = OUT / "staged" / name
    shutil.copyfile(stg, dst)
    diff = "".join(difflib.unified_diff(inst.read_text(encoding="utf-8").splitlines(True), stg.read_text(encoding="utf-8").splitlines(True),
                                        fromfile="SP/%s (installed %s)" % (name if name.startswith("campaign/") else "Ezek/tools/" + name, sha(inst)[:12]),
                                        tofile="proposals/%s/staged/%s (%s)" % (a.batch, name, sha(stg)[:12])))
    dp = OUT / "diffs" / (name.replace("/", "__") + ".diff")
    dp.write_text(diff, encoding="utf-8", newline="\n")
    files[name] = {"installed_sha256": sha(inst), "staged_sha256": sha(dst), "staged_path": "Ezek/proposals/%s/staged/%s" % (a.batch, name),
                   "diff_vs_installed": "Ezek/proposals/%s/diffs/%s" % (a.batch, dp.name), "diff_lines": diff.count("\n")}
for s in SCRIPTS:
    shutil.copyfile(SCR / s, OUT / "scripts" / s)
for f in ("corpus_impact.json", "marks_review.json", "flags_analysis.json", "whatif.json"):
    if not (ROOT / f).is_file():
        raise SystemExit("ABORT: stage output %s is absent" % f)
    shutil.copyfile(ROOT / f, OUT / f)
shutil.copyfile(ROOT / "stage_run.json", OUT / "runs" / "stage_run.json")
hc = impact["hard_classes"]
manifest = {
    "schema": "m8_tool_edit_proposal.v1", "book": "Ezek", "batch": a.batch, "built": datetime.now(timezone.utc).isoformat(),
    "built_by": "orchestrator (claude-opus-5) under OW-11; executes a ruling, never rules",
    "status": "STAGED - INSTALL BLOCKED. Condition (c) of ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 returns the new HARD class "
              "below to the controlling agent before install. Nothing is installed.",
    "ordered_by": "ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 (a)-(g)",
    "builds_on_installed": {"receipt": "SP/campaign/receipts/ezek_tools_install_t4fix_batch2.json"},
    "supersedes_proposal": {"batch": "toolfix2_batch2", "why": "landed by the orchestrator before #e4 ruled; its content differs from (b) "
                            "(grapheme-only boundary, refs rebound to named refs, broader register arms, no S1-22); never installed"},
    "content_per_condition_b": {
        "S1-07": "collate_hebrew word boundaries: byte, nfd and accent_stripped matches have no Hebrew letter or combining mark beside them; "
                 "skeleton matches have no Hebrew letter beside them. The normalizer inherits them, and its book-wide Qere scope is unchanged (R4-i).",
        "S1-06": "citation_sweep REF HEBREW arm: runs inside a ref entry bind to that entry's own (first) ref, with walk()'s collate, raw-note "
                 "Qere and in-sentence K/Q keyword functions [CWO-EZ-16]",
        "S1-05": "check_register class author_wave_register_s1_05 with the ruling's alternatives verbatim; GREEN controls 'part of the court' "
                 "and 'the order of the gates' [CWO-EZ-14]",
        "S1-10": "check_web_quotes e15d: a prose field whose curly double quote counts differ [CWO-EZ-17]",
        "S1-22": "check_marks rules 1, 3 and 4: a claim binds to its own clause's C:V, C.V, MT C:V or dotted numbers; absence phrases are scoped "
                 "to the verse, range or chapter they name; a negated K/Q token is an absence claim (false_kq_absence_claim)",
        "S1-19": "_cure_verification: refuses (a) a claim with no author, (b) duplicate cure_ids, (c) an ordering id not bounded against "
                 "'-', (d) any digest that is not 64 hex; classifies (e) as ruling_names_retired_cure, r5_with_trigger or unclassified; adds "
                 "--require-rulings",
        "e": "TOOLKIT.md rows and a sentence; check_marks docstring rules 1, 3 and 4"},
    "disclosed_test_change": "ezek_lib's existing selftest 'collate_hebrew returns byte for a verbatim verse' now collates MT 1:1 "
                             "against the verses joined by ' | ' (as the tools join them). The old fixture concatenated the verses with "
                             "no separator, so the new word boundary correctly refused a match running into 1:2's first letter.",
    "files": files,
    "tests": {"staged": {k: run["tests"].get(k) for k in ("checks", "passed", "verdict")}, "ezek_lib_selftest": run["ezek_lib_selftest"],
              "toolkit_selfcheck": run["toolkit_selfcheck"], "verifier_selftest": {k: run["verifier_selftest"].get(k) for k in ("vectors", "failed", "verdict")},
              "verifier_over_real_claims": run["verifier_real_claims"],
              "discrimination_on_installed_tools": {"checks": disc["checks"], "passed_on_installed": disc["passed_on_installed"],
                                                    "failed_on_installed": len(disc["failed_on_installed"]), "all_failures_are_section_10b": True}},
    "corpus_impact_condition_c": {
        "path": "Ezek/proposals/%s/corpus_impact.json" % a.batch, "summaries": impact["summaries"],
        "lists_moved": run["corpus_impact_summary"]["lists_moved"],
        "hard_known": {"citation_sweep_S1-07": hc["citation_sweep"]["S1-07_known"], "citation_sweep_S1-06": hc["citation_sweep"]["S1-06_known"],
                       "normalizer": hc["normalizer"]["known"]},
        "NEW_HARD_CLASS_RETURNED": {"items": hc["NEW_HARD_CLASS_ITEMS"], "facts": mreview.get("new_hard_class"),
                                    "class": "an unpointed citation form (the recognition family label 'ידעתם') standing inside the inflected verse "
                                             "word וִֽידַעְתֶּ֖ם at MT 12:20, which the skeleton-tier word boundary newly refuses"},
        "check_marks_removed_review": {"path": "Ezek/proposals/%s/marks_review.json" % a.batch, "counts": mreview["counts"],
                                       "analysis": "Ezek/proposals/%s/flags_analysis.json" % a.batch, "pairing": analysis["check_marks"]},
    },
    "gate": gate,
    "scripts": {s: sha(OUT / "scripts" / s) for s in SCRIPTS},
}
(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"landed": str(OUT), "manifest_sha256": sha(OUT / "manifest.json"), "gate": gate,
                  "files": {n: f["staged_sha256"][:16] for n, f in files.items()}}, ensure_ascii=False, indent=1))
