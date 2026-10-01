"""Stage TOOLFIX-4 (ezek_controlling_rulings_a1#e8 ruling T6-01) and, on --land with every gate true, land it DURABLY as
SP/Ezek/proposals/toolfix4_batch1 in the toolfix3_batch1 shape. Nothing is installed here.

GATES (#e8 T6-01, as T5-SEQUENCE):
  - the staged selftest is GREEN with every vector, and every vector of the installed selftest keeps its name, expectation and pass;
  - each new REFUSED vector whose refusal is new is DISCRIMINATING: its verdict differs on the installed verifier (a61ec7ff);
  - both real claims files (private copies; --root SP/Ezek; --rulings #e2-#e8; --require-rulings) are GREEN on the installed and
    the staged verifier, with every verdict and every supersession class identical;
  - the diff against a61ec7ff is confined to the ruled regions: the candidate equals the installed text with exactly the six
    labelled replacements of build_tf4_candidate.py applied, and nothing else;
  - the staged digest is reproduced.

Usage: stage_land_tf4.py [--land]"""
import argparse
import difflib
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
EZ = SP / "Ezek"
ROOT = Path(__file__).resolve().parent
CAND = ROOT / "_cure_verification.tf4.py"
V_INST = SP / "campaign" / "_cure_verification.py"
V_INST_SHA = "a61ec7ff85aee3782b1e23fb6b6338398be773769f4936d235a71cd7c11b6042"
BATCH = "toolfix4_batch1"
OUT = EZ / "proposals" / BATCH
ORDERED_BY = "ezek_controlling_rulings_a1#e8 ruling T6-01"
RULINGS = [EZ / "ezek_controlling_agent_rulings.v1.json"] + [EZ / ("ezek_controlling_agent_rulings_e%d.v1.json" % n) for n in (3, 4, 5, 6, 7, 8)]
CLAIM_FILES = ("ezek_cure_claims.v1.jsonl", "ezek_cure_claims_toolkit_repair.v1.jsonl")
ALLOWED_LABELS = ["docstring: rule (7) and the T6-02 disclosure", "counts loop: negative refusal and rule (7)",
                  "no-machine-result reason names the counts shape", "evaluate: a pinned reason class", "tf4 vectors",
                  "selftest runs the tf4 vectors"]
REQUIRED_DISCRIMINATING = ("tf4_t6_a1_zero_counts_no_machine_result", "tf4_t6_a2_checks_zero_alone_no_machine_result",
                           "tf4_t6_a3_failed_zero_alone_no_machine_result", "tf4_checks_without_passed_no_machine_result",
                           "tf4_passed_alone_no_machine_result", "tf4_e8_01_negative_counts_refused")
SCRIPTS = ("build_tf4_candidate.py", "stage_land_tf4.py", "install_tf4.py", "replacements_tf4.json")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(args):
    return subprocess.run([sys.executable] + [str(a) for a in args], capture_output=True, text=True, encoding="utf-8", env=ENV, cwd=str(ROOT))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ap = argparse.ArgumentParser()
ap.add_argument("--land", action="store_true")
a = ap.parse_args()
if sha(V_INST) != V_INST_SHA:
    raise SystemExit("ABORT: the installed verifier is not a61ec7ff")
e8 = json.loads((EZ / "ezek_controlling_agent_rulings_e8.v1.json").read_text(encoding="utf-8"))
if not any(r["id"] == "T6-01" and r["ruling"] == "adopt" for r in e8["rulings"]):
    raise SystemExit("ABORT: #e8 does not adopt T6-01")
out = {"candidate_sha256": sha(CAND)}
vs, vi = json.loads(run([CAND, "--selftest"]).stdout), json.loads(run([V_INST, "--selftest"]).stdout)
out["selftest_staged"] = {"vectors": vs["vectors"], "failed": vs["failed"], "verdict": vs["verdict"],
                          "failed_vectors": [r for r in vs["results"] if not r.get("ok")]}
out["selftest_installed"] = {"vectors": vi["vectors"], "failed": vi["failed"], "verdict": vi["verdict"]}
staged_by = {r["vector"]: r for r in vs["results"]}
changed = {r["vector"]: {"installed": r.get("expected"), "staged": staged_by.get(r["vector"], {}).get("expected")}
           for r in vi["results"] if r.get("expected") != staged_by.get(r["vector"], {}).get("expected") or not staged_by.get(r["vector"], {}).get("ok")}
out["existing_vectors"] = {"count": len(vi["results"]), "changed_or_failing": changed}
inst, stg = load(V_INST, "ver_installed_a61"), load(CAND, "ver_staged_tf4")
td = Path(tempfile.mkdtemp(dir=ROOT, prefix="disc_"))
disc = {}
for v in stg.tf4_vectors(td):
    rs = stg.evaluate(stg, v, td)
    got_inst, reasons_inst = inst.check_claim(v[2], td)
    disc[v[1]] = {"expected": v[3], "expected_reason": v[4] if len(v) > 4 else None, "staged_ok": rs["ok"], "staged_first_reason": rs["first_reason"],
                  "installed_verdict": got_inst, "fails_on_installed": got_inst != v[3]}
out["tf4_vectors"] = disc
priv = Path(tempfile.mkdtemp(dir=ROOT, prefix="claims_"))
real = {}
for label, V in (("installed", V_INST), ("staged", CAND)):
    real[label] = {}
    for cf in CLAIM_FILES:
        shutil.copyfile(EZ / cf, priv / cf)
        r = json.loads(run([V, "--claims", priv / cf, "--root", EZ, "--rulings"] + RULINGS + ["--require-rulings"]).stdout)
        real[label][cf] = {"claims": r["claims"], "accepted": r["accepted"], "refused": r["refused"], "superseded": r["superseded"], "verdict": r["verdict"],
                           "verdicts": {o["cure_id"]: o["verdict"] for o in r["results"] if o.get("record") != "supersession"},
                           "classes": [(c["supersedes_cure_id"], c["ordered_by_class"]) for c in r["supersession_classes"]]}
out["real_claims_before_after"] = real
inst_text, cand_text = V_INST.read_text(encoding="utf-8"), CAND.read_text(encoding="utf-8")
repl = json.loads((ROOT / "replacements_tf4.json").read_text(encoding="utf-8"))
rebuilt = inst_text
for r in repl:
    rebuilt = rebuilt.replace(r["old"], r["new"]) if rebuilt.count(r["old"]) == 1 else None
    if rebuilt is None:
        break
diff = "".join(difflib.unified_diff(inst_text.splitlines(True), cand_text.splitlines(True),
                                    fromfile="SP/campaign/_cure_verification.py (installed %s)" % V_INST_SHA[:12],
                                    tofile="proposals/%s/staged/campaign/_cure_verification.py (%s)" % (BATCH, sha(CAND)[:12])))
(ROOT / "campaign__cure_verification.py.diff").write_text(diff, encoding="utf-8", newline="\n")
out["diff_scope"] = {"labels": [r["label"] for r in repl], "labels_are_the_ruled_regions": [r["label"] for r in repl] == ALLOWED_LABELS,
                     "candidate_equals_installed_plus_exactly_these_replacements": rebuilt == cand_text,
                     "diff_lines": diff.count("\n")}
gate = {
    "selftest_green": vs["verdict"] == "GREEN" and vs["failed"] == 0,
    "existing_vectors_keep_name_expectation_and_pass": not changed,
    "tf4_vectors_all_pass_on_staged": all(x["staged_ok"] for x in disc.values()),
    "new_refusals_discriminating": all(disc.get(n, {}).get("fails_on_installed") for n in REQUIRED_DISCRIMINATING),
    "real_claims_green_and_identical": all(real[l][cf]["verdict"] == "GREEN" for l in real for cf in CLAIM_FILES)
                                       and all({k: v for k, v in real["installed"][cf].items()} == {k: v for k, v in real["staged"][cf].items()} for cf in CLAIM_FILES),
    "diff_confined_to_ruled_regions": out["diff_scope"]["labels_are_the_ruled_regions"] and out["diff_scope"]["candidate_equals_installed_plus_exactly_these_replacements"],
}
out["gate"] = gate
(ROOT / "stage_run.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
summary = {"selftest_staged": {k: out["selftest_staged"][k] for k in ("vectors", "failed", "verdict")}, "existing_changed": changed,
           "discriminating": sorted(n for n, x in disc.items() if x["fails_on_installed"]), "tf4_not_ok": sorted(n for n, x in disc.items() if not x["staged_ok"]),
           "real": {l: {cf: (real[l][cf]["verdict"], real[l][cf]["accepted"], real[l][cf]["superseded"]) for cf in CLAIM_FILES} for l in real},
           "diff_scope": out["diff_scope"], "gate": gate}
if not a.land:
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    raise SystemExit(0 if all(gate.values()) else 1)
if not all(gate.values()):
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    raise SystemExit("ABORT: gate failed; nothing landed")
if OUT.exists():
    raise SystemExit("ABORT: %s exists; a landed proposal is never replaced" % OUT)
g = subprocess.run([sys.executable, str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek", "--target", str(OUT / "manifest.json")],
                   capture_output=True, text=True, encoding="utf-8", env=ENV)
if g.returncode != 0:
    raise SystemExit("ABORT: the landing target is pinned:\n" + g.stdout)
for d in ("staged/campaign", "diffs", "scripts", "runs"):
    (OUT / d).mkdir(parents=True, exist_ok=False)
shutil.copyfile(CAND, OUT / "staged" / "campaign" / "_cure_verification.py")
shutil.copyfile(ROOT / "campaign__cure_verification.py.diff", OUT / "diffs" / "campaign__cure_verification.py.diff")
shutil.copyfile(ROOT / "stage_run.json", OUT / "runs" / "stage_run.json")
for s in SCRIPTS:
    shutil.copyfile(ROOT / s, OUT / "scripts" / s)
staged = OUT / "staged" / "campaign" / "_cure_verification.py"
manifest = {
    "schema": "m8_tool_edit_proposal.v1", "book": "Ezek", "batch": BATCH, "built": datetime.now(timezone.utc).isoformat(),
    "built_by": "orchestrator (claude-opus-5) under OW-11; executes a ruling, never rules",
    "status": "STAGED - INSTALL PRE-AUTHORIZED by %s on the TOOLFIX-3 gates: every gate holds. Nothing is installed by this landing." % ORDERED_BY,
    "ordered_by": ORDERED_BY, "builds_on_installed": {"receipt": "SP/campaign/receipts/ezek_tools_install_toolfix3_batch1.json"},
    "touches_no_validator_suite_member": True,
    "content": {"rule_7": "a counts object carries a machine result only when checks is a positive integer and passed an integer",
                "E8-01": "a negative counts member is refused with its own reason",
                "vectors": "T6-A1..A3, checks without passed, passed alone, E8-01 (REFUSED with pinned reasons); the bound-and-FAILED reason class "
                           "pinned; GREEN controls {11,11,0} no exit and exit 0 with passed null; T6-A4..A10 as T6 ran them, A5-A7 named "
                           "*_disclosed_false_refusal (T6-02)",
                "documentation": "the module docstring gains the rule (7) paragraph and the T6-02 disclosure; listed as the first ruled region"},
    "files": {"campaign/_cure_verification.py": {"installed_sha256": V_INST_SHA, "staged_sha256": sha(staged),
                                                 "staged_path": "Ezek/proposals/%s/staged/campaign/_cure_verification.py" % BATCH,
                                                 "diff_vs_installed": "Ezek/proposals/%s/diffs/campaign__cure_verification.py.diff" % BATCH,
                                                 "diff_lines": out["diff_scope"]["diff_lines"]}},
    "tests": {"selftest_staged": out["selftest_staged"], "selftest_installed": out["selftest_installed"], "existing_vectors": out["existing_vectors"],
              "tf4_vectors_discrimination": disc},
    "real_claims_before_and_after": real, "diff_scope": out["diff_scope"],
    "runs": {"stage_run.json": sha(OUT / "runs" / "stage_run.json")}, "gate": gate,
    "scripts": {s: sha(OUT / "scripts" / s) for s in SCRIPTS},
    "distinct_check": "not a T7: S2 carries the section 'verifier at the TOOLFIX-4 digest', items (i)-(vi) of #e8 T6-01",
}
if sha(staged) != sha(CAND):
    raise SystemExit("ABORT: the landed staged copy does not reproduce the candidate")
(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"landed": str(OUT), "manifest_sha256": sha(OUT / "manifest.json"), "staged_sha256": sha(staged), "gate": gate}, indent=1))
