"""Stage the batched tool edit proposed for T4's findings (T4-01, T4-03, T4-04) in session scratch, never in SP, and test it.

The stage is rebuilt from SP on every run (SP/Ezek/tools, SP/Jer/tools, the SP/Ezek top-level files, the chain head), so
each run edits exactly the installed bytes, and every replacement is exact and count-checked. Then:
  1. _adapt_zone_tools_ezek.py regenerates citation_sweep.py and check_marks.py in the stage (pinned to the copies);
  2. the zone tests (with the new section 9), the ezek_lib selftest and the toolkit selfcheck run in the stage;
  3. the validator suite runs over a copy of the chain head with the staged tools, and its report is compared list by
     list with the installed tools' report, SP/Ezek/repair/suite_v3_2acbc045/rows.jsonl.validator_report.json.
Nothing is installed. The controlling agent rules on the proposal (#e4), and a fresh distinct review follows any install."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
SCR = Path(__file__).resolve().parent
ROOT = SCR / "stage_t4fix"
ST = ROOT / "sp_durable"
T = ST / "Ezek" / "tools"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
applied = []


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sub(path, old, new, label, count=1):
    t = path.read_text(encoding="utf-8")
    n = t.count(old)
    if n != count:
        raise SystemExit("ABORT: %s: expected %d occurrence(s) in %s, found %d" % (label, count, path.name, n))
    path.write_text(t.replace(old, new), encoding="utf-8", newline="\n")
    applied.append(label)


def run(args, cwd=T):
    return subprocess.run([sys.executable] + [str(a) for a in args], capture_output=True, text=True, encoding="utf-8",
                          env=ENV, cwd=str(cwd))


# ---- rebuild the stage from the installed bytes ----
rec = json.loads((SP / "campaign" / "receipts" / "ezek_tools_install_r4ii_cal1.json").read_text(encoding="utf-8"))
for n, f in rec["files"].items():
    if sha(SP / "Ezek" / "tools" / n) != f["after"]:
        raise SystemExit("ABORT: SP tools/%s is not the installed digest %s" % (n, f["after"][:16]))
assert ROOT.parent == SCR and ROOT.name == "stage_t4fix"
if ROOT.exists():
    shutil.rmtree(ROOT)
ign = shutil.ignore_patterns("__pycache__", "*.pyc")
shutil.copytree(SP / "Ezek" / "tools", T, ignore=ign)
shutil.copytree(SP / "Jer" / "tools", ST / "Jer" / "tools", ignore=ign)
for f in (SP / "Ezek").iterdir():
    if f.is_file():
        shutil.copy2(f, ST / "Ezek" / f.name)
SUITE = ST / "Ezek" / "repair" / "suite_t4fix"
SUITE.mkdir(parents=True)
shutil.copy2(SP / "Ezek" / "repair" / "rows_v3_cwo12.jsonl", SUITE / "rows.jsonl")

ADAPT, TEST, TK = T / "_adapt_zone_tools_ezek.py", T / "_test_zone_tools_ezek.py", T / "TOOLKIT.md"

# ---- T4-01: digits that follow a letter directly are an id, never a verse number ----
sub(ADAPT, r'PUNCTA_NUM = re.compile(r"(?<!\d)(\d{1,2})[:.](\d{1,2})(?!\d)")',
    r'PUNCTA_NUM = re.compile(r"(?<![A-Za-z\d])(\d{1,2})[:.](\d{1,2})(?!\d)")' + "\n"
    + r'SINGLE_WITNESS = re.compile(r"\bsingle[-\s]+witness", re.I)   # T4-04: the disclosure, hyphenated or spaced',
    "T4-01 PUNCTA_NUM letter guard + T4-04 SINGLE_WITNESS")
sub(ADAPT, r'RANGE_NUM = re.compile(r"(?<!\d)(\d{1,2})[:.](\d{1,2})(?:',
    "# T4-01: digits that follow a letter directly ('R4.5', a ruling or row id) are an id, never a verse number\n"
    + r'RANGE_NUM = re.compile(r"(?<![A-Za-z\d])(\d{1,2})[:.](\d{1,2})(?:', "T4-01 RANGE_NUM letter guard")
sub(ADAPT, r'APPOSITION_NUM = re.compile(r"(?<!\d)(\d{1,2})', r'APPOSITION_NUM = re.compile(r"(?<![A-Za-z\d])(\d{1,2})',
    "T4-01 APPOSITION_NUM letter guard")

# ---- T4-03: a closed set of denials may FOLLOW the mention inside its clause ----
sub(ADAPT, r'''def puncta_negated(text, start):
    """Negation anywhere EARLIER in the mention's own comma-delimited clause (T2-03: an adjacency-only test dropped a
    distant 'not'). Two negators standing next to each other cancel ('not without', 'never lacking': T1-03)."""
''', r'''def puncta_negated(text, start, end=None):
    """Negation anywhere EARLIER in the mention's own comma-delimited clause (T2-03: an adjacency-only test dropped a
    distant 'not'). Two negators standing next to each other cancel ('not without', 'never lacking': T1-03). Given the
    mention's end, a denial LATER in the clause also counts, but only one DENIAL_AFTER reads (T4-03: '45:18, where a
    dateline would be expected but none stands'); a bare later 'no' or 'not' does not."""
    if end is not None and denied_after(text, end):
        return True
''', "T4-03 puncta_negated end parameter")
sub(ADAPT, 'PAREN_AFTER = re.compile(r"\\s*\\(")\n', r'''PAREN_AFTER = re.compile(r"\s*\(")
# T4-03: the closed set of denials that may FOLLOW a mention inside its clause. 'none of' is a partitive, and 'is absent',
# 'is lacking' or 'is missing' deny only at the clause end ('the dateline at 45:18 is missing its year word' still names
# a dateline).
DENIAL_AFTER = re.compile(r"\b(?:but|though|although|yet)\s+(?:there\s+(?:is|are)\s+)?none\b(?!\s+of\b)"
                          r"|\bnone\s+(?:stands?|is\s+(?:present|written|there|found)|appears?|exists?)\b"
                          r"|\b(?:is|are)\s+(?:absent|lacking|missing)\s*(?=[.;,()]|$)", re.I)


def denied_after(text, end):
    """A DENIAL_AFTER construction between the mention's end and its clause's end, reading through a parenthetical that
    opens directly after the clause ('the dateline (45:18) would be expected but none stands')."""
    f_hi = field_bounds(text, end, end)[1]
    _, hi = clause_bounds(text, end, end, NEG_CLAUSE_END)
    p = PAREN_AFTER.match(text, hi)
    if p and p.end() <= f_hi:
        close = text.find(")", p.end(), f_hi)
        if close != -1:
            nxt = NEG_CLAUSE_END.search(text, close + 1, f_hi)
            hi = nxt.start() if nxt else f_hi
    return bool(DENIAL_AFTER.search(text, end, hi))
''', "T4-03 DENIAL_AFTER + denied_after")
sub(ADAPT, "puncta_negated(tail, pm_.start())", "puncta_negated(tail, pm_.start(), pm_.end())", "T4-03 cs puncta call")
sub(ADAPT, "puncta_negated(text, m.start())", "puncta_negated(text, m.start(), m.end())", "T4-03 cm puncta call")
sub(ADAPT, "puncta_negated(tail, dm_.start())", "puncta_negated(tail, dm_.start(), dm_.end())", "T4-03 cs calendar ref call")
sub(ADAPT, "puncta_negated(o, m.start())", "puncta_negated(o, m.start(), m.end())", "T4-03 cs calendar prose call")
sub(ADAPT, "# comma-delimited clause makes it an absence claim; adjacent negators cancel (T1-03, T2-03).\n            pm_ = PUNCTA.search(tail)",
    "# comma-delimited clause makes it an absence claim; adjacent negators cancel (T1-03, T2-03); so does a closed-set\n"
    "            # denial later in the clause (T4-03). A true claim needs single-witness disclosure in the annotation, as mark,\n"
    "            # small-letter and paseq refs do (T4-04).\n            pm_ = PUNCTA.search(tail)", "T4-03/04 cs comment")
sub(ADAPT, "# comma-delimited clause makes it an absence claim; adjacent negators cancel (T1-03, T2-03).\n            span_sites",
    "# comma-delimited clause makes it an absence claim; adjacent negators cancel (T1-03, T2-03); so does a closed-set\n"
    "            # denial later in the clause (T4-03).\n            span_sites", "T4-03 cm comment")

# ---- T4-04: a true puncta ref needs single-witness disclosure ----
sub(ADAPT, "'the claim names another verse'})\")\n\"\"\"\n\nCS_QERE_TIER",
    "'the claim names another verse'})\")\n"
    "                elif not SINGLE_WITNESS.search(tail):\n"
    "                    problems.append(f\"{did}: puncta ref lacks single-witness disclosure: {ref!r}\")\n"
    "\"\"\"\n\nCS_QERE_TIER", "T4-04 cs single-witness check")

# ---- TOOLKIT.md ----
sub(TK, "a claim at those two needs\n  single-witness disclosure.\n",
    "a claim at those two needs\n  single-witness disclosure (citation_sweep fails a true puncta ref without it, as it does\n"
    "  a mark, small-letter or paseq ref; in prose that symmetry is model territory).\n", "T4-04 TOOLKIT book facts")
sub(TK, 'claim a denial, and two adjacent negators cancel ("not without puncta" asserts them). A\nQERE tier',
    'claim a denial, and two adjacent negators cancel ("not without puncta" asserts them). A\n'
    "denial may also FOLLOW the mention inside its clause, read through a parenthetical opening\n"
    "directly after it, but only as one of a closed set (`but none`, `though none`, `none stands`,\n"
    "`none is present`, and `is absent` / `is missing` at the clause end); dateline claims use\n"
    "the same test. So `45:18, where a dateline would be expected but none stands` is a denial,\n"
    "while `opens no new year`, `none of` and `is missing its year word` are not, and a denial\n"
    "behind a comma stays outside the clause. Digits that follow a letter directly (`R4.5`) are\n"
    "an id, never a verse number. A\nQERE tier", "T4-01/03 TOOLKIT staged-tools paragraph")

# ---- tests: section 9 ----
SECTION9 = r'''# 9. T4 FINDINGS - the batched edit proposed to ezek_controlling_rulings_a1#e4 (installed only after its ruling, then a
# fresh distinct review). T4-01: digits that follow a letter ('R4.5') are an id, not a verse. T4-03: a closed set of
# denials LATER in the clause denies, read through a parenthetical; a bare later 'no', 'none of' and a non-final
# 'is missing' do not, and a denial behind a comma stays outside the clause (a disclosed residual, pinned RED).
# T4-04: a true puncta ref needs single-witness disclosure, hyphenated or spaced.
T4_CS = [
    ("cs_t4_01_decoy_letter_id_ok",
     ["web:Ezek.41.1-Ezek.41.26 puncta extraordinaria (cross-referenced at row R4.5 in the ledger), single-witness"], None),
    ("cs_t4_01_dotted_ezek_ref_still_binds", ["web:Ezek.41.1-Ezek.41.26 puncta extraordinaria (Ezek.41.5, single-witness)"],
     "claims puncta extraordinaria"),
    ("cs_t4_03_puncta_denial_after_nonsite_ok",
     ["web:Ezek.41.1-Ezek.41.10 puncta extraordinaria would be expected at 41:5 but none stands"], None),
    ("cs_t4_03_puncta_denial_after_at_site",
     ["oshb:Ezek.41.20-Ezek.41.20 puncta extraordinaria would be expected here but none stands"], "denies puncta extraordinaria"),
    ("cs_t4_04_site_without_disclosure", ["web:Ezek.41.1-Ezek.41.26 puncta extraordinaria (41:20)"], "lacks single-witness disclosure"),
    ("cs_t4_04_spaced_single_witness_ok", ["web:Ezek.41.1-Ezek.41.26 puncta extraordinaria at 41:20, single witness"], None),
]
T4_CAL_ROWS = [
    ("cal_t4_03_apposition_denial_ok", {"boundary_rationale": "the unit opens at 45:18, where a dateline would be expected but none stands"}, None),
    ("cal_t4_03_parenthesis_denial_ok", {"boundary_rationale": "the dateline (45:18) would be expected but none stands"}, None),
    ("cal_t4_03_absent_at_clause_end_ok", {"boundary_rationale": "a dateline at 45:18 is absent"}, None),
    ("cal_t4_03_bare_later_no_stays_red", {"boundary_rationale": "the dateline at 45:18 opens no new year"}, "claims a dateline at MT 45:18"),
    ("cal_t4_03_none_of_stays_red", {"boundary_rationale": "the dateline at 45:18 but none of the festival dates"}, "claims a dateline at MT 45:18"),
    ("cal_t4_03_missing_not_final_stays_red", {"boundary_rationale": "the dateline at 45:18 is missing its year word"},
     "claims a dateline at MT 45:18"),
    ("cal_t4_03_denial_behind_comma_residual_red", {"boundary_rationale": "a dateline at 45:18 would be expected, though none stands"},
     "claims a dateline at MT 45:18"),
]
T4_CM = [
    ("cm_t4_01_decoy_letter_id_ok", "the puncta extraordinaria (cross-referenced at row R4.5 in the ledger)", "Ezek.41.12-Ezek.41.20",
     {"puncta_claim_in_ezek": False, "false_puncta_absence_claim": False}),
    ("cm_t4_03_denial_after_nonsite_ok", "puncta extraordinaria would be expected at 41:5 but none stands", "Ezek.41.1-Ezek.41.10",
     {"puncta_claim_in_ezek": False, "false_puncta_absence_claim": False}),
    ("cm_t4_03_denial_after_at_site_flags", "puncta extraordinaria would be expected at 41:20 but none stands", "Ezek.41.12-Ezek.41.20",
     {"false_puncta_absence_claim": True, "puncta_claim_in_ezek": False}),
]
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "t4_cs.jsonl"
    p.write_text("\n".join(json.dumps({"decision_id": d, "boundary_evidence_refs": refs}) for d, refs, _ in T4_CS)
                 + "\n" + "\n".join(json.dumps(dict({"decision_id": d}, **f), ensure_ascii=False) for d, f, _ in T4_CAL_ROWS),
                 encoding="utf-8")
    rep = run("citation_sweep.py", p)
    for did, _, expect in T4_CS + T4_CAL_ROWS:
        mine = [x for x in rep["problems"] if x.startswith(did + ":")]
        check("citation_sweep %s: %s" % (did, "no problem" if expect is None else repr(expect)),
              (not mine) if expect is None else any(expect in x for x in mine), mine)
    p = Path(td) / "t4_cm.jsonl"
    p.write_text("\n".join(json.dumps({"decision_id": d, "boundary_rationale": prose, "span": span}) for d, prose, span, _ in T4_CM),
                 encoding="utf-8")
    rep = run("check_marks.py", p)
    for d, _, _, expect in T4_CM:
        for rule, fires in expect.items():
            mine = [f for f in rep["flags"] if f.get("decision_id") == d and f.get("rule") == rule]
            check("check_marks %s: %s %s" % (d, rule, "fires" if fires else "silent"), bool(mine) == fires, mine)

'''
sub(TEST, 'failed = [r for r in results if not r["ok"]]\n', SECTION9 + 'failed = [r for r in results if not r["ok"]]\n', "section 9 vectors")

# ---- regenerate, test, compare ----
pins = ["citation_sweep.py=" + sha(T / "citation_sweep.py"), "check_marks.py=" + sha(T / "check_marks.py")]
g = run([ADAPT, "--replace"] + pins)
out = {"applied": applied, "regen_exit": g.returncode, "regen": g.stdout.strip().splitlines()[-4:], "regen_err": g.stderr[-600:]}
if g.returncode != 0:
    print(json.dumps(out, ensure_ascii=False, indent=1))
    raise SystemExit(1)
t = run([TEST])
try:
    td_ = json.loads(t.stdout)
    out["tests"] = {"checks": td_["checks"], "passed": td_["passed"], "verdict": td_["verdict"],
                    "failed": [{"name": f.get("name"), "detail": str(f.get("detail"))[:300]} for f in td_["failed"]]}
except json.JSONDecodeError:
    out["tests"] = {"exit": t.returncode, "stdout_tail": t.stdout[-800:], "stderr_tail": t.stderr[-800:]}
out["ezek_lib_selftest_exit"] = run([T / "ezek_lib.py"]).returncode
sc = run([T / "_toolkit_selfcheck.py"])
try:
    scd = json.loads(sc.stdout)
    out["toolkit_selfcheck"] = {"exit": sc.returncode, "checks": scd.get("checks"), "passed": scd.get("passed"), "verdict": scd.get("verdict")}
except json.JSONDecodeError:
    out["toolkit_selfcheck"] = {"exit": sc.returncode, "stdout_tail": sc.stdout[-600:]}
s = run([T / "run_validator_suite.py", SUITE / "rows.jsonl"])
new = json.loads((SUITE / "rows.jsonl.validator_report.json").read_text(encoding="utf-8"))
old = json.loads((SP / "Ezek" / "repair" / "suite_v3_2acbc045" / "rows.jsonl.validator_report.json").read_text(encoding="utf-8"))
diff = {}
for k in sorted(set(old) | set(new)):
    a, b = old.get(k), new.get(k)
    if isinstance(a, dict) and isinstance(b, dict):
        for kk in sorted(set(a) | set(b)):
            la, lb = a.get(kk), b.get(kk)
            if isinstance(la, list) and isinstance(lb, list):
                sa = {json.dumps(x, sort_keys=True, ensure_ascii=False) for x in la}
                sb = {json.dumps(x, sort_keys=True, ensure_ascii=False) for x in lb}
                if sa != sb:
                    diff["%s.%s" % (k, kk)] = {"installed": len(la), "staged": len(lb), "added": sorted(sb - sa)[:8], "removed": sorted(sa - sb)[:8]}
out["suite_exit"] = s.returncode
out["suite_summary"] = {"installed": old.get("summary"), "staged": new.get("summary")}
out["suite_list_differences"] = diff or "NONE"
out["staged_digests"] = {n: sha(T / n) for n in ("citation_sweep.py", "check_marks.py", "_adapt_zone_tools_ezek.py", "_test_zone_tools_ezek.py", "TOOLKIT.md")}
print(json.dumps(out, ensure_ascii=False, indent=1))
