"""Land the staged TOOLFIX-2 proposal DURABLY, without installing anything. It is built on TOOLFIX-1, so the staged files are
the combined result that one distinct review (T5) would read.

The run:
  - re-runs stage_toolfix2_patch.py, which rebuilds the stage from the installed SP bytes plus TOOLFIX-1's landed staged files;
  - re-runs stage_discrimination.py, which checks that the declared fix-dependent vectors of sections 9 and 10 fail on the
    installed tools and nothing else does;
  - gates on the exact expected corpus impact over the chain head:
      - only the citation_sweep, normalizer, register and web_quotes lists move, and nothing is removed from any list;
      - citation_sweep gains problems on exactly P01-012, P03-004, P03-005, P03-006, P03-010, P03-012, P03-017 and P03-019;
      - the normalizer gains exactly 8 defect runs;
      - register gains only flags;
      - web_quotes changes only by the added decision_id.
Then it runs the in-flight pin guard over its target and writes SP/Ezek/proposals/<batch>/ (staged/, diffs/, scripts/,
runs/, corpus_impact.json, manifest.json). The run refuses if the batch directory already exists.

Usage: land_toolfix2_proposal.py --batch toolfix2_batch2"""
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
STAGE = SCR / "stage_toolfix2" / "sp_durable"
B1 = EZ / "proposals" / "t4fix_batch1"
TOOL_FILES = ("citation_sweep.py", "check_marks.py", "_adapt_zone_tools_ezek.py", "_test_zone_tools_ezek.py", "TOOLKIT.md",
              "ezek_lib.py", "normalize_hebrew_in_json.py", "check_register.py", "check_web_quotes.py")
SCRIPTS = ("stage_toolfix2_patch.py", "stage_discrimination.py", "land_toolfix2_proposal.py")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
DECLARED = [
    # TOOLFIX-1 (section 9)
    "cs_t4_01_decoy_letter_id_ok", "cs_t4_03_puncta_denial_after_nonsite_ok", "cs_t4_04_site_without_disclosure",
    "cs_t4_03_puncta_denial_after_at_site", "cal_t4_03_apposition_denial_ok", "cal_t4_03_parenthesis_denial_ok",
    "cal_t4_03_absent_at_clause_end_ok", "cm_t4_01_decoy_letter_id_ok", "cm_t4_03_denial_after_nonsite_ok",
    "cm_t4_03_denial_after_at_site_flags",
    # TOOLFIX-2 (section 10)
    "cs_s1_06_accent_stripped_qere_in_ref", "cs_s1_06_undisclosed_qere_in_ref", "cs_s1_06_other_verse_words",
    "cs_s1_07_cut_splice_in_prose", "normalize S1-07: a splice cut", "reg_s1_05_originally_drafted", "reg_s1_05_former_span",
    "reg_s1_05_row_before_after", "reg_s1_05_last_of_three", "reg_s1_05_strategy_s", "reg_s1_05_posture",
    "reg_s1_05_officially_inventoried_in_ref", "wq_s1_10_unclosed"]
EXPECT_CS_ROWS = {"P01-012", "P03-004", "P03-005", "P03-006", "P03-010", "P03-012", "P03-017", "P03-019"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(args, cwd=SCR):
    return subprocess.run([sys.executable] + [str(x) for x in args], capture_output=True, text=True, encoding="utf-8", env=ENV, cwd=str(cwd))


ap = argparse.ArgumentParser()
ap.add_argument("--batch", required=True)
a = ap.parse_args()
OUT = EZ / "proposals" / a.batch
if OUT.exists():
    raise SystemExit("ABORT: %s exists; a landed proposal is never replaced (write a new batch)" % OUT)

p = run([SCR / "stage_toolfix2_patch.py"])
if p.returncode != 0:
    raise SystemExit("ABORT: the staging patch failed:\n" + (p.stderr or p.stdout)[-2000:])
patch_raw = p.stdout
patch = json.loads(patch_raw)
exp = SCR / "toolfix2_declared_vectors.json"
exp.write_text(json.dumps(DECLARED, indent=1), encoding="utf-8", newline="\n")
dsc = run([SCR / "stage_discrimination.py", "--stage", "stage_toolfix2", "--expect", exp])
disc_raw = dsc.stdout
disc = json.loads(disc_raw)

# ---- corpus impact, recomputed from the two reports ----
new = json.loads((STAGE / "Ezek" / "repair" / "suite_toolfix2" / "rows.jsonl.validator_report.json").read_text(encoding="utf-8"))
old = json.loads((EZ / "repair" / "suite_v3_2acbc045" / "rows.jsonl.validator_report.json").read_text(encoding="utf-8"))
impact, moved = {}, set()
for k in sorted(set(old) | set(new)):
    oa, nb = old.get(k), new.get(k)
    if not (isinstance(oa, dict) and isinstance(nb, dict)):
        continue
    for kk in sorted(set(oa) | set(nb)):
        la, lb = oa.get(kk), nb.get(kk)
        if not (isinstance(la, list) and isinstance(lb, list)):
            continue
        key = "%s.%s" % (k, kk)
        strip = bool(la) and not any(isinstance(x, dict) and "decision_id" in x for x in la)
        def norm(x, strip=strip):
            return json.dumps({q: w for q, w in x.items() if q != "decision_id"} if strip and isinstance(x, dict) else x, sort_keys=True, ensure_ascii=False)
        sa = {json.dumps(x, sort_keys=True, ensure_ascii=False) for x in la}
        added = [x for x in lb if norm(x) not in sa]
        sb = {norm(x) for x in lb}
        removed = [x for x in la if json.dumps(x, sort_keys=True, ensure_ascii=False) not in sb]
        id_added = strip and any(isinstance(x, dict) and "decision_id" in x for x in lb)
        if added or removed or id_added:
            moved.add(key)
            impact[key] = {"installed": len(la), "staged": len(lb), "added": added, "removed": removed, "decision_id_added": id_added}
cs_added = impact.get("citation_sweep.problems", {}).get("added", [])
cs_rows = {str(x).split(":", 1)[0] for x in cs_added}
norm_added = impact.get("hebrew_normalize_dryrun.defects", {}).get("added", [])
reg = impact.get("register.flags", {})
reg_by_class, reg_by_row = {}, {}
for fl in reg.get("added", []):
    reg_by_class[fl.get("class")] = reg_by_class.get(fl.get("class"), 0) + 1
    reg_by_row[fl.get("decision_id")] = reg_by_row.get(fl.get("decision_id"), 0) + 1
wq = impact.get("web_quotes.flags", {})
gate = {
    "tests_green": (patch.get("tests") or {}).get("verdict") == "GREEN",
    "ezek_lib_selftest_green": (patch.get("ezek_lib_selftest") or {}).get("verdict") == "GREEN",
    "toolkit_selfcheck_green": (patch.get("toolkit_selfcheck") or {}).get("verdict") == "GREEN",
    "verifier_selftest_green": (patch.get("verifier_selftest") or {}).get("verdict") == "GREEN",
    "verifier_real_claims_green": all(v.get("verdict") == "GREEN" for v in (patch.get("verifier_real_claims") or {}).values()),
    "vectors_discriminate": disc.get("verdict") == "DISCRIMINATING",
    "only_expected_lists_move": moved <= {"citation_sweep.problems", "hebrew_normalize_dryrun.defects", "register.flags", "web_quotes.flags"},
    "nothing_removed": all(not v["removed"] for v in impact.values()),
    "citation_sweep_rows_exact": cs_rows == EXPECT_CS_ROWS,
    "normalizer_defect_runs_8": len({json.dumps(x, ensure_ascii=False) for x in norm_added}) == 8,
    "web_quotes_only_decision_id": not wq or (not wq["added"] and not wq["removed"] and wq["decision_id_added"]),
}
if not all(gate.values()):
    print(json.dumps({"gate": gate, "cs_rows": sorted(cs_rows), "moved": sorted(moved), "discrimination": disc,
                      "patch_tests": patch.get("tests")}, ensure_ascii=False, indent=1))
    raise SystemExit("ABORT: the proposal does not pass its own gate; nothing landed")

g = run([SP / "campaign" / "_inflight_pin_guard.py", "--book", "Ezek", "--target", OUT / "manifest.json"])
if g.returncode != 0:
    raise SystemExit("ABORT: the landing target is pinned by an in-flight execution:\n" + g.stdout)

for d in ("staged", "staged/campaign", "diffs", "scripts", "runs"):
    (OUT / d).mkdir(parents=True, exist_ok=False)
files = {}
pairs = [(n, EZ / "tools" / n, STAGE / "Ezek" / "tools" / n, OUT / "staged" / n) for n in TOOL_FILES]
pairs.append(("campaign/_cure_verification.py", SP / "campaign" / "_cure_verification.py", STAGE / "campaign" / "_cure_verification.py",
              OUT / "staged" / "campaign" / "_cure_verification.py"))
for name, inst, stg, dst in pairs:
    shutil.copyfile(stg, dst)
    diff = "".join(difflib.unified_diff(inst.read_text(encoding="utf-8").splitlines(True), stg.read_text(encoding="utf-8").splitlines(True),
                                        fromfile="SP/%s (installed %s)" % (("Ezek/tools/" + name) if "/" not in name else name, sha(inst)[:12]),
                                        tofile="proposals/%s/staged/%s (staged %s)" % (a.batch, name, sha(stg)[:12])))
    dpath = OUT / "diffs" / (name.replace("/", "__") + ".diff")
    dpath.write_text(diff, encoding="utf-8", newline="\n")
    b1 = (json.loads((B1 / "manifest.json").read_text(encoding="utf-8"))["files"].get(name) or {}).get("staged_sha256")
    files[name] = {"installed_sha256": sha(inst), "batch1_staged_sha256": b1, "staged_sha256": sha(dst),
                   "changed_by_batch2": sha(dst) != (b1 or sha(inst)), "staged_path": "Ezek/proposals/%s/staged/%s" % (a.batch, name),
                   "diff_vs_installed": "Ezek/proposals/%s/diffs/%s" % (a.batch, dpath.name), "diff_lines": diff.count("\n")}
    if files[name]["staged_sha256"] != (patch["staged_digests"].get(name) or patch["staged_digests"].get(name.replace("campaign/", "campaign/"))):
        raise SystemExit("ABORT: landed %s does not equal the patch run's staged digest" % name)
for s in SCRIPTS:
    shutil.copyfile(SCR / s, OUT / "scripts" / s)
(OUT / "runs" / "stage_patch_run.json").write_text(patch_raw, encoding="utf-8", newline="\n")
(OUT / "runs" / "discrimination_run.json").write_text(disc_raw, encoding="utf-8", newline="\n")
corpus = {"schema": "m8_tool_edit_corpus_impact.v1", "rows": "Ezek/repair/rows_v3_cwo12.jsonl", "rows_sha256": sha(EZ / "repair" / "rows_v3_cwo12.jsonl"),
          "installed_report": "Ezek/repair/suite_v3_2acbc045/rows.jsonl.validator_report.json",
          "summaries": {"installed": old.get("summary"), "staged": new.get("summary")},
          "citation_sweep_added": cs_added, "normalizer_defects_added": norm_added,
          "register_added_by_class": reg_by_class, "register_added_by_row": reg_by_row, "register_added": reg.get("added", []),
          "web_quotes": {"installed": wq.get("installed"), "staged": wq.get("staged"), "decision_id_added": wq.get("decision_id_added")}}
(OUT / "corpus_impact.json").write_text(json.dumps(corpus, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
manifest = {
    "schema": "m8_tool_edit_proposal.v1", "book": "Ezek", "batch": a.batch, "built": datetime.now(timezone.utc).isoformat(),
    "built_by": "orchestrator (claude-opus-5) under OW-11; proposes, never rules",
    "status": "PROPOSAL - NOT INSTALLED. Built ON TOOLFIX-1 (t4fix_batch1). Staged while ezek_controlling_rulings_a1#e4 rules on the "
              "TOOLFIX-2 plan; nothing is installed before that ruling, and any install is followed by a fresh distinct review "
              "(T5) of both batches before any cure claim.",
    "builds_on": {"batch": "t4fix_batch1", "manifest_sha256": sha(B1 / "manifest.json")},
    "findings_addressed": ["S1-05", "S1-06", "S1-07", "S1-10", "S1-19"],
    "findings_not_in_this_batch": {"S1-22": "check_marks paragraph_mark_claim / false_mark_absence_claim / kq_claim false positives "
                                            "(TQ-01..03): FLAGS noise with no HARD consequence; needs its own design and vectors"},
    "s1_10_correction": ("S1 wrote that check_web_quotes has no arm for an unbalanced curly quote. Its e15a arm already flags all "
                         "10 p06 rows on the chain head (6 double-open, 4 unclosed); the flags carried only an array-index path, "
                         "not a decision_id. The edit adds decision_id to every flag. The TOOLFIX-2 item in the #e4 queue repeats "
                         "S1's wording; this manifest is the orchestrator's correction."),
    "files": files, "installed_baseline": "SP/campaign/receipts/ezek_tools_install_r4ii_cal1.json and SP/campaign/_cure_verification.py",
    "tests": {"staged": patch["tests"], "ezek_lib_selftest": patch["ezek_lib_selftest"], "toolkit_selfcheck": patch["toolkit_selfcheck"],
              "verifier_selftest": {k: patch["verifier_selftest"][k] for k in ("vectors", "failed", "verdict")},
              "verifier_over_real_claims": patch["verifier_real_claims"],
              "discrimination_on_installed_tools": {k: disc[k] for k in ("checks", "passed_on_installed", "failed_on_installed",
                                                                          "confirmed_failing_on_installed", "verdict")},
              "not_run_against_pre_edit_code": "the new ezek_lib selftest and verifier selftest vectors call functions and keys the "
                                               "pre-edit code does not have, so they fail there by construction; they were not executed "
                                               "against it"},
    "corpus_impact": {"path": "Ezek/proposals/%s/corpus_impact.json" % a.batch, "sha256": sha(OUT / "corpus_impact.json"),
                      "suite": corpus["summaries"], "citation_sweep_rows": sorted(cs_rows), "normalizer_defect_runs": len(norm_added),
                      "register_flags_added": len(reg.get("added", [])), "register_by_class": reg_by_class,
                      "register_rows": len(reg_by_row)},
    "gate": gate,
    "consequences_at_install": [
        "The suite over the chain head turns HARD RED (citation_sweep and E-01) on 8 rows until FIXUP-1 re-splices them: P01-012 "
        "(the Qere at 7:2) and P03-004, P03-005, P03-006, P03-010, P03-012, P03-017, P03-019 (grapheme-cut splices).",
        "EZEK-TK-CURE-normalizer and EZEK-TK-CURE-ezek_lib bind the pre-edit normalize_hebrew_in_json.py and ezek_lib.py digests. "
        "At install each is retired by a supersession record whose ordered_by names the execution and ruling that adopt TOOLFIX-2, "
        "and successor claims are written only on T5's review of the installed bytes.",
        "The verifier edit applies to every book's claims files. Closed books are not re-verified by it (completed checks are never "
        "re-run); it governs every claim written from install onward.",
        "check_register gains 79 triage flags on the chain head (26 governance posture, 21 strategy citation, 20 positional row "
        "reference, 10 repair history, 2 staged file stem). CWO-EZ-08 coverage is re-run after FIXUP-1."],
    "residuals_disclosed": [
        "S1-07: the grapheme boundary binds the byte and nfd tiers only; a quote that ends after a complete grapheme in mid-word (a "
        "prefix-stripped or suffix-stripped form) is still byte-true and is not flagged.",
        "S1-06: the ref arm reads Hebrew runs of 3+ letters; an MT qualifier or oshb: ref named anywhere in the annotation widens "
        "the verses a run may bind to.",
        "S1-05: the new register arms are lexical and may over-flag (for example 'the strategy' or 'posture' in a sense the "
        "section-8 law does not bar); they are triage flags, never RED.",
        "S1-19(e) is a warning, not a refusal, and it tests only whether the ordering ruling NAMES the retired cure id. #e2's "
        "R5 names both EZEK-P0-CURE-toolkit (the claim it retired) and EZEK-P0-CURE-toolkit-v2 (the successor it ordered), so "
        "the live supersession of v2 raises no warning even though R5 did not order v2's retirement. A name check cannot "
        "tell a successor from a retirement; that link stays a matter for the controlling agent (V3-W)."],
    "scripts": {s: sha(OUT / "scripts" / s) for s in SCRIPTS},
    "runs": {n: sha(OUT / "runs" / n) for n in ("stage_patch_run.json", "discrimination_run.json")},
}
(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"landed": str(OUT), "manifest_sha256": sha(OUT / "manifest.json"), "gate": gate,
                  "discrimination": {k: disc[k] for k in ("failed_on_installed", "confirmed_failing_on_installed", "verdict")},
                  "corpus_impact": manifest["corpus_impact"], "files_changed_by_batch2": [n for n, f in files.items() if f["changed_by_batch2"]]},
                 ensure_ascii=False, indent=1))
