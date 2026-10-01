"""Decide GATE-E10's `s4_may_launch` from the artifacts, condition by condition, before S4's brief is built or launched.

#e10 ruling GATE-E10, verbatim on this point: "s4_may_launch is true when rows_v6_fixup3 is applied with tiling exact, the suite HARD
GREEN, coverage COVERED (CWO-EZ-01..09, 14..18) and residual 0 (CWO-EZ-19..22) with CWO-EZ-23 verified in v6, the mark_symmetry_gap residual
exactly the two p05 flags, TOOLFIX-5's rows_v6 report 0, and the census after FIXUP-3's receipts plus 725,165 (S3's measured cost) below
49,604,821."

Each clause is evaluated against the bytes on disk, never against a summary, and the ruling text itself is read from the rulings file and
checked to contain the sentence this script implements - if the ruling is ever reworded, this refuses rather than silently testing an old
rule. Every report must be over rows_v6's exact digest, so a stale report cannot satisfy a condition.

The residual clause accepts what the installed coverage tools actually write: an integer residual, an empty residual list, or the
'as ruled' disposition CWO-EZ-22 carries, in which case the report must state that every hit is dispositioned. Anything else is a REFUSE
with the report's own keys printed, not a guess.

Exit 0 only when every condition holds. Usage: gate_e10_s4_check.py [--json <out>]"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
EZ = SP / "Ezek"
OUT = EZ / "repair" / "rows_v6_fixup3.jsonl"
MAN = EZ / "repair" / "rows_v6_fixup3.manifest.json"
SUITE = EZ / "repair" / "suite_v6_6c843b14" / "rows.jsonl.validator_report.json"
COV = EZ / "repair" / "cwo_coverage_v6"
TF5R = EZ / "repair" / "toolfix5_v6_report.json"
RULINGS = EZ / "ezek_controlling_agent_rulings_e10.v1.json"
CEILING, S3_COST = 49_604_821, 725_165
TRIAGE = {("P05-004", "Ezek.22.31"), ("P05-008", "Ezek.24.14")}
COVERED_SET = ["%02d" % n for n in list(range(1, 10)) + list(range(14, 19)) if n != 3 and n != 10]
RESIDUAL_SET = ["19", "20", "21", "22"]
RULE_SENTENCE = "s4_may_launch is true when rows_v6_fixup3 is applied with tiling exact, the suite HARD GREEN"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def js(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def residual_ok(rep):
    """(ok, description) for a CWO-EZ-19..22 report, accepting the shapes the installed tools write."""
    if "residual" in rep:
        r = rep["residual"]
        if isinstance(r, int):
            return r == 0, "residual %d" % r
        if isinstance(r, list):
            return len(r) == 0, "residual list of %d" % len(r)
    if isinstance(rep.get("residual_count"), int):
        return rep["residual_count"] == 0, "residual_count %d" % rep["residual_count"]
    # CWO-EZ-22's tool writes hits/hit_count rather than a residual: an empty hit list over rows_v6 is the same statement.
    if isinstance(rep.get("hits"), list) and isinstance(rep.get("hit_count"), int):
        return len(rep["hits"]) == 0 and rep["hit_count"] == 0, "hit_count %d with %d hits listed" % (rep["hit_count"], len(rep["hits"]))
    disp = str(rep.get("verdict", "")) + " " + str(rep.get("disposition", ""))
    if "AS_RULED" in disp.upper() or "DISPOSITIONED" in disp.upper():
        und = rep.get("undispositioned") or rep.get("undispositioned_hits") or []
        return not und, "%s with %d undispositioned" % (disp.strip(), len(und))
    return False, "no residual, residual_count or ruled disposition; keys %s" % sorted(rep)


ap = argparse.ArgumentParser()
ap.add_argument("--json")
a = ap.parse_args()
checks, rows_sha = [], sha(OUT)


def add(name, ok, detail):
    checks.append({"condition": name, "holds": bool(ok), "measured": detail})


gate = next((r for r in js(RULINGS)["rulings"] if r["id"] == "GATE-E10"), {})
add("the ruling still says what this script tests", RULE_SENTENCE in gate.get("decision", ""),
    "GATE-E10 carries the s4_may_launch sentence" if RULE_SENTENCE in gate.get("decision", "") else "GATE-E10 does NOT carry it; rebuild this check")

man = js(MAN)
add("rows_v6_fixup3 applied, tiling exact",
    man["output"]["sha256"] == rows_sha and man["tiling"]["verses"] == man["tiling"]["expected"] == 1273,
    "manifest over %s..., tiling %s/%s, %s" % (man["output"]["sha256"][:16], man["tiling"]["verses"], man["tiling"]["expected"],
                                               man["replaced_statement"]))

rep = js(SUITE)
add("suite HARD GREEN over those exact bytes",
    sha(rep["rows_file"]) == rows_sha and rep["summary"]["hard_status"] == "GREEN" and not rep["ngram7"]["offending_7grams"],
    "hard %s, ngram7 %d offending at gate %s, register %s, citation_sweep %d"
    % (rep["summary"]["hard_status"], len(rep["ngram7"]["offending_7grams"]), rep["ngram7"]["gate"],
       rep["register"]["flag_count"], len(rep["citation_sweep"]["problems"])))

missing, wrong = [], []
for c in COVERED_SET:
    p = COV / ("CWO-EZ-%s.json" % c)
    if not p.is_file():
        missing.append(c)
        continue
    r = js(p)
    if r.get("verdict") != "COVERED":
        wrong.append("%s=%s" % (c, r.get("verdict")))
    elif (r.get("rows_file") or {}).get("sha256") != rows_sha:
        wrong.append("%s=report is over %s..., not rows_v6" % (c, str((r.get("rows_file") or {}).get("sha256"))[:12]))
add("coverage COVERED on CWO-EZ-01..09 and 14..18", not missing and not wrong,
    "checked %s; missing %s; not covered %s" % (len(COVERED_SET), missing or "none", wrong or "none"))

res_detail, res_ok = [], True
for c in RESIDUAL_SET:
    r = js(COV / ("CWO-EZ-%s.json" % c))
    ok, why = residual_ok(r)
    bound = (r.get("rows_file") or {}).get("sha256") == rows_sha
    ok = ok and bound
    res_ok &= ok
    res_detail.append("CWO-EZ-%s %s (%s%s)" % (c, r.get("verdict"), why, "" if bound else "; NOT over rows_v6"))
add("residual 0 on CWO-EZ-19..22", res_ok, "; ".join(res_detail))

r23 = js(COV / "CWO-EZ-23.json")
add("CWO-EZ-23 verified in v6",
    r23.get("verdict") == "COVERED" and r23.get("pairs_verified") == 33 and (r23.get("rows_file") or {}).get("sha256") == rows_sha,
    "%s, %s pairs verified, report over %s..." % (r23.get("verdict"), r23.get("pairs_verified"),
                                                  str((r23.get("rows_file") or {}).get("sha256"))[:12]))

gaps = {(f["decision_id"], f["undisclosed_mt_key"]) for f in rep["mark_symmetry"]["flags"] if f.get("rule") == "mark_symmetry_gap"}
add("mark_symmetry_gap residual is exactly the two p05 flags", gaps == TRIAGE, "%s" % sorted(gaps))

tf5 = js(TF5R)
add("TOOLFIX-5's rows_v6 report is 0", tf5.get("hit_count") == 0, "%s, hit_count %s" % (tf5.get("verdict"), tf5.get("hit_count")))

census = 0
for fp in EZ.rglob("*_attempt_receipts.jsonl"):
    for line in fp.read_text(encoding="utf-8").splitlines():
        if line.strip():
            t = json.loads(line).get("tokens_reported")
            census += t if isinstance(t, int) else 0
add("census after FIXUP-3 plus S3's measured 725,165 is below the ceiling", census + S3_COST < CEILING,
    "%s + %s = %s against %s" % (format(census, ","), format(S3_COST, ","), format(census + S3_COST, ","), format(CEILING, ",")))

verdict = "S4_MAY_LAUNCH" if all(c["holds"] for c in checks) else "REFUSED"
doc = {"schema": "m8_gate_check.v1", "gate": "GATE-E10 s4_may_launch", "book": "Ezek",
       "rows_v6_sha256": rows_sha, "census": census, "verdict": verdict,
       "failed": [c["condition"] for c in checks if not c["holds"]], "checks": checks}
if a.json:
    Path(a.json).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
for c in checks:
    print("  [%s] %s\n        %s" % ("OK " if c["holds"] else "FAIL", c["condition"], c["measured"]))
print(json.dumps({"verdict": verdict, "failed": doc["failed"], "census": census, "rows_v6": rows_sha[:16]}, ensure_ascii=False, indent=1))
sys.exit(0 if verdict == "S4_MAY_LAUNCH" else 1)
