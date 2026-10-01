"""Install TOOLFIX-4 (SP/Ezek/proposals/toolfix4_batch1) by digest, as ezek_controlling_rulings_a1#e8 ruling T6-01 pre-authorizes. DRY RUN is
the default; --apply is the mutation boundary. It is install_tf3.py narrowed to one file: the in-flight pin guard; the expected-before
digest and the staged digest; the manifest gate all true; no ACCEPTED claim bound to the verifier; the atomic copy and re-verify; the
four post-install checks with passed = checks - failed and the verifier selftest's own {vectors, failed} line (T5-13); both claims
files re-verified under --rulings #e2-#e8 --require-rulings, with every verdict and class compared to the staging run; the receipt,
never overwritten.

Usage: install_tf4.py [--apply]"""
import argparse
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
BATCH = "toolfix4_batch1"
ORDERED_BY = "ezek_controlling_rulings_a1#e8 ruling T6-01"
NAME = "campaign/_cure_verification.py"
TGT = SP / NAME
CLAIMS = [EZ / "ezek_cure_claims.v1.jsonl", EZ / "ezek_cure_claims_toolkit_repair.v1.jsonl"]
RULINGS = [EZ / "ezek_controlling_agent_rulings.v1.json"] + [EZ / ("ezek_controlling_agent_rulings_e%d.v1.json" % n) for n in (3, 4, 5, 6, 7, 8)]
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(args, cwd):
    return subprocess.run([sys.executable] + [str(x) for x in args], capture_output=True, text=True, encoding="utf-8", env=ENV, cwd=str(cwd))


ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true")
a = ap.parse_args()
PROP = EZ / "proposals" / BATCH
man = json.loads((PROP / "manifest.json").read_text(encoding="utf-8"))
f = man["files"][NAME]
receipt_path = SP / "campaign" / "receipts" / ("ezek_tools_install_%s.json" % BATCH)
plan = {"batch": BATCH, "manifest_sha256": sha(PROP / "manifest.json"), "problems": []}
if receipt_path.exists():
    plan["problems"].append("%s exists; this install is never repeated" % receipt_path.name)
if man.get("ordered_by") != ORDERED_BY or not all(man.get("gate", {}).values()):
    plan["problems"].append("the manifest is not the gated TOOLFIX-4 proposal")
g = run([SP / "campaign" / "_inflight_pin_guard.py", "--book", "Ezek", "--target", TGT] + sum([["--target", str(c)] for c in CLAIMS], []), SP)
plan["pin_guard"] = json.loads(g.stdout)["verdict"]
if g.returncode != 0:
    plan["problems"].append("a target is pinned by an in-flight execution")
now = sha(TGT)
state = "already_installed" if now == f["staged_sha256"] else ("ready" if now == f["installed_sha256"] else "UNEXPECTED")
if state == "UNEXPECTED":
    plan["problems"].append("%s is %s, neither the expected-before nor the staged digest" % (NAME, now[:12]))
if sha(PROP / "staged" / NAME) != f["staged_sha256"]:
    plan["problems"].append("the staged file does not match its manifest digest")
plan["file"] = {"state": state, "before": now, "after": f["staged_sha256"]}
bound = []
for cf in CLAIMS:
    rep = json.loads(run([TGT, "--claims", cf, "--root", EZ], SP).stdout)
    accepted = {r["cure_id"] for r in rep["results"] if r.get("verdict") == "ACCEPTED"}
    for line in cf.read_text(encoding="utf-8").splitlines():
        if line.strip():
            c = json.loads(line)
            if c.get("record_type") != "supersession" and c.get("cure_id") in accepted and c.get("artifact_path") == NAME:
                bound.append(c["cure_id"])
plan["accepted_claims_bound_to_the_verifier"] = bound
if bound:
    plan["problems"].append("an ACCEPTED claim binds the verifier; its retirement is not this batch's to order")
if not a.apply or plan["problems"]:
    plan["mode"] = "DRY_RUN" if not plan["problems"] else "REFUSED"
    print(json.dumps(plan, ensure_ascii=False, indent=1))
    raise SystemExit(0 if not plan["problems"] else 1)
if state == "ready":
    tmp = TGT.with_name(".install_" + TGT.name)
    shutil.copyfile(PROP / "staged" / NAME, tmp)
    os.replace(tmp, TGT)
    if sha(TGT) != f["staged_sha256"]:
        raise SystemExit("ABORT: the installed verifier does not verify")
plan["file"]["state"] = "installed"
T = EZ / "tools"
checks = {}
for label, args, cwd in (("zone_tests", [T / "_test_zone_tools_ezek.py"], T), ("ezek_lib_selftest", [T / "ezek_lib.py"], T),
                         ("toolkit_selfcheck", [T / "_toolkit_selfcheck.py"], T), ("verifier_selftest", [TGT, "--selftest"], SP)):
    p = run(args, cwd)
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        checks[label] = {"exit": p.returncode, "stdout_tail": p.stdout[-400:]}
        continue
    n_checks = d.get("checks", d.get("vectors"))
    n_failed = d.get("failed") if isinstance(d.get("failed"), int) else len(d.get("failed") or [])
    passed = d.get("passed") if isinstance(d.get("passed"), int) else (n_checks - n_failed if isinstance(n_checks, int) else None)
    checks[label] = {"exit": p.returncode, "verdict": d.get("verdict"), "checks": n_checks, "passed": passed, "failed": n_failed}
    if label == "verifier_selftest":
        checks[label]["selftest_line"] = {"vectors": d.get("vectors"), "failed": d.get("failed")}
stage_real = man["real_claims_before_and_after"]["staged"]
verif, identical = {}, True
for cf in CLAIMS:
    d = json.loads(run([TGT, "--claims", cf, "--root", EZ, "--rulings"] + RULINGS + ["--require-rulings"], SP).stdout)
    verif[cf.name] = {k: d.get(k) for k in ("claims", "accepted", "refused", "superseded", "verdict")} | {"supersession_classes": d.get("supersession_classes")}
    now_verdicts = {o["cure_id"]: o["verdict"] for o in d["results"] if o.get("record") != "supersession"}
    now_classes = [[c["supersedes_cure_id"], c["ordered_by_class"]] for c in d["supersession_classes"]]
    identical &= now_verdicts == stage_real[cf.name]["verdicts"] and now_classes == [list(x) for x in stage_real[cf.name]["classes"]]
receipt = {"schema": "m8_tool_install_receipt.v1", "book": "Ezek", "recorded_at": datetime.now(timezone.utc).isoformat(),
           "batch": BATCH, "proposal_manifest_sha256": plan["manifest_sha256"], "ordered_by": ORDERED_BY,
           "files": {NAME: plan["file"]}, "checks_after": checks,
           "suite_after": {"note": "no suite member changed and no rows changed; the suite was not re-run for this verifier-only batch"},
           "claims_retired": [], "retained_bytes": {}, "claims_verification_after": verif,
           "claims_verdicts_and_classes_identical_to_staging": identical,
           "rulings_given_to_the_verifier": ["Ezek/" + p.name for p in RULINGS],
           "review": ("S2 carries the section 'verifier at the TOOLFIX-4 digest' (#e8 T6-01 (i)-(vi)); the S1-19 claim is written on S2's "
                      "verdict at this digest (#e8 S1-19-TIMING); no further cure claim is appended before this receipt")}
receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({k: receipt[k] for k in ("files", "checks_after", "claims_verification_after", "claims_verdicts_and_classes_identical_to_staging")},
                 ensure_ascii=False, indent=1))
raise SystemExit(0 if identical and all(c.get("exit") == 0 for c in checks.values()) else 1)
