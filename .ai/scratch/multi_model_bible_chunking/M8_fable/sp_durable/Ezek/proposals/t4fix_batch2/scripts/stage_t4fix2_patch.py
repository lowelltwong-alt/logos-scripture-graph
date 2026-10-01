"""Re-stage TOOLFIX-1 as t4fix_batch2 per ezek_controlling_rulings_a1#e4 (rulings TOOLFIX-1, T4-03, T4-04): t4fix_batch1 plus
amendments A1, A2 and A3 and the eight vectors the ruling names. Session scratch only; nothing is installed.

  A1  the copular denial's clause-end lookahead also accepts a newline: (?=[.;,()\\n]|$).
  A2  coordinated-denial guard. The coordinated forms ('but|though|although|yet [there is|are] none', never 'none of';
      'none stands|is present|is written|is there|is found|appears|exists') deny the mention only when the words between
      the mention and the denial name no verse number, or carry an expectation modal. Otherwise the mention is a POSITIVE
      claim judged on the numbers before the denial; the number window stops at the denial and reads no parenthetical past
      it. The copular form ('is|are absent|lacking|missing' at the clause end) always denies.
  A3  citation_sweep's mark, small-letter and paseq ref checks test SINGLE_WITNESS (hyphenated or spaced), not the literal
      'single-witness'. TOOLKIT.md says '(hyphenated or spaced)'.

The run:
  - regenerates the tools with the staged adapter;
  - runs the zone tests, the ezek_lib selftest and the toolkit selfcheck;
  - runs the suite over the chain head and requires NO list difference from suite_v3_2acbc045;
  - checks discrimination against TWO baselines: the installed tools, and the unamended t4fix_batch1. #e4's own trace shows
    the A2 hole exists only in batch1, so an A2 vector passes on the installed tools and fails on batch1. Each vector's
    behaviour on both baselines is reported, never assumed."""
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
B1 = SP / "Ezek" / "proposals" / "t4fix_batch1"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
applied = []
NEW_VECTORS = ["cm_e4_a1_copular_denial_at_field_end_flags", "cs_e4_a2_positive_then_denial_nonsite_red",
               "cs_e4_a2_positive_then_denial_site_ok", "cm_e4_a2_positive_then_denial_nonsite_flags",
               "cal_e4_a2_positive_then_denial_red", "cal_e4_a2_true_then_denial_ok",
               "cs_e4_a3_mark_spaced_single_witness_ok", "cs_e4_a3_paseq_spaced_single_witness_ok"]
BATCH1_VECTORS = ["cs_t4_01_decoy_letter_id_ok", "cs_t4_03_puncta_denial_after_nonsite_ok", "cs_t4_04_site_without_disclosure",
                  "cs_t4_03_puncta_denial_after_at_site", "cal_t4_03_apposition_denial_ok", "cal_t4_03_parenthesis_denial_ok",
                  "cal_t4_03_absent_at_clause_end_ok", "cm_t4_01_decoy_letter_id_ok", "cm_t4_03_denial_after_nonsite_ok",
                  "cm_t4_03_denial_after_at_site_flags"]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(args, cwd):
    return subprocess.run([sys.executable] + [str(a) for a in args], capture_output=True, text=True, encoding="utf-8", env=ENV, cwd=str(cwd))


def fresh_tree(root, overlay=None):
    assert root.parent == SCR and root.name.startswith("stage_t4fix2")
    if root.exists():
        shutil.rmtree(root)
    st = root / "sp_durable"
    ign = shutil.ignore_patterns("__pycache__", "*.pyc")
    shutil.copytree(SP / "Ezek" / "tools", st / "Ezek" / "tools", ignore=ign)
    shutil.copytree(SP / "Jer" / "tools", st / "Jer" / "tools", ignore=ign)
    for f in (SP / "Ezek").iterdir():
        if f.is_file():
            shutil.copy2(f, st / "Ezek" / f.name)
    if overlay:
        man = json.loads((overlay / "manifest.json").read_text(encoding="utf-8"))
        for n, f in man["files"].items():
            if sha(overlay / "staged" / n) != f["staged_sha256"]:
                raise SystemExit("ABORT: %s staged %s does not match its manifest" % (overlay.name, n))
            shutil.copyfile(overlay / "staged" / n, st / "Ezek" / "tools" / n)
    return st / "Ezek" / "tools"


def sub(path, old, new, label, count=1):
    t = path.read_text(encoding="utf-8")
    n = t.count(old)
    if n != count:
        raise SystemExit("ABORT: %s: expected %d occurrence(s) in %s, found %d" % (label, count, path.name, n))
    path.write_text(t.replace(old, new), encoding="utf-8", newline="\n")
    applied.append(label)


rec = json.loads((SP / "campaign" / "receipts" / "ezek_tools_install_r4ii_cal1.json").read_text(encoding="utf-8"))
for n, f in rec["files"].items():
    if sha(SP / "Ezek" / "tools" / n) != f["after"]:
        raise SystemExit("ABORT: SP tools/%s is not the installed digest" % n)
T = fresh_tree(SCR / "stage_t4fix2", overlay=B1)
applied.append("stage rebuilt from SP with t4fix_batch1 staged files laid over it (manifest-checked)")
SUITE = SCR / "stage_t4fix2" / "sp_durable" / "Ezek" / "repair" / "suite_t4fix2"
SUITE.mkdir(parents=True)
shutil.copy2(SP / "Ezek" / "repair" / "rows_v3_cwo12.jsonl", SUITE / "rows.jsonl")
ADAPT, TEST, TK = T / "_adapt_zone_tools_ezek.py", T / "_test_zone_tools_ezek.py", T / "TOOLKIT.md"

# ---- A1 + A2: the denial block ----
sub(ADAPT, r'''# T4-03: the closed set of denials that may FOLLOW a mention inside its clause. 'none of' is a partitive, and 'is absent',
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
''', r'''# T4-03: the closed set of denials that may FOLLOW a mention inside its clause. 'none of' is a partitive, and 'is absent',
# 'is lacking' or 'is missing' deny only at the clause end ('the dateline at 45:18 is missing its year word' still names
# a dateline). #e4 amendments: A1 - the clause end may be a newline (check_marks joins fields with newlines); A2 - a
# COORDINATED denial with a verse number and no expectation modal between the mention and the denial does not deny: the
# mention is a positive claim over the numbers before the denial ('stand at 41:5 but none is present in ch 46' claims 41:5).
DENIAL_COORD = re.compile(r"\b(?:but|though|although|yet)\s+(?:there\s+(?:is|are)\s+)?none\b(?!\s+of\b)"
                          r"|\bnone\s+(?:stands?|is\s+(?:present|written|there|found)|appears?|exists?)\b", re.I)
DENIAL_COPULAR = re.compile(r"\b(?:is|are)\s+(?:absent|lacking|missing)\s*(?=[.;,()\n]|$)", re.I)
EXPECT_MODAL = re.compile(r"\b(?:would|should|could|might|may|expected|anticipated)\b", re.I)


def _denial_window_end(text, end):
    """The end of the mention's clause, reading through a parenthetical that opens directly after it."""
    f_hi = field_bounds(text, end, end)[1]
    _, hi = clause_bounds(text, end, end, NEG_CLAUSE_END)
    p = PAREN_AFTER.match(text, hi)
    if p and p.end() <= f_hi:
        close = text.find(")", p.end(), f_hi)
        if close != -1:
            nxt = NEG_CLAUSE_END.search(text, close + 1, f_hi)
            hi = nxt.start() if nxt else f_hi
    return hi


def denial_after(text, end):
    """(kind, start) of the first closed-set denial after a mention inside its clause. 'copular' always denies;
    'coordinated' denies because the words between the mention and the denial name no verse number or carry an expectation
    modal; 'positive' is a coordinated form that does NOT deny (A2), and start bounds the mention's own numbers.
    (None, None) when the clause carries no closed-set denial."""
    hi = _denial_window_end(text, end)
    found = [m for m in (DENIAL_COPULAR.search(text, end, hi), DENIAL_COORD.search(text, end, hi)) if m]
    if not found:
        return None, None
    first = min(found, key=lambda m: m.start())
    if first.re is DENIAL_COPULAR:
        return "copular", first.start()
    between = text[end:first.start()]
    if not RANGE_NUM.search(between) or EXPECT_MODAL.search(between):
        return "coordinated", first.start()
    return "positive", first.start()


def denied_after(text, end):
    return denial_after(text, end)[0] in ("copular", "coordinated")


def claim_upper(text, end):
    """A2: where a mention's own number window stops - the start of a coordinated denial that does not deny - or None."""
    kind, start = denial_after(text, end)
    return start if kind == "positive" else None
''', "A1+A2 denial block (DENIAL_COORD, DENIAL_COPULAR with newline, EXPECT_MODAL, denial_after, claim_upper)")
sub(ADAPT, "def puncta_claim_numbers(text, start, end, reach=None, ends=NUM_CLAUSE_END, with_paren=True):",
    "def puncta_claim_numbers(text, start, end, reach=None, ends=NUM_CLAUSE_END, with_paren=True, upper=None):", "A2 puncta_claim_numbers upper")
sub(ADAPT, "    lo, hi = clause_bounds(text, start, end, ends)\n",
    "    lo, hi = clause_bounds(text, start, end, ends)\n"
    "    if upper is not None:   # A2: numbers after a coordinated denial belong to the denial; no parenthetical past it\n"
    "        hi, with_paren = min(hi, upper), False\n", "A2 puncta_claim_numbers window bound")
sub(ADAPT, "def dateline_claim_numbers(text, start, end, reach=60):", "def dateline_claim_numbers(text, start, end, reach=60, upper=None):",
    "A2 dateline_claim_numbers upper")
sub(ADAPT, "    lo, hi = clause_bounds(text, start, end, NEG_CLAUSE_END)\n    items = puncta_claim_numbers(text, start, end, reach, NEG_CLAUSE_END)\n",
    "    lo, hi = clause_bounds(text, start, end, NEG_CLAUSE_END)\n"
    "    if upper is not None:   # A2\n        hi = min(hi, upper)\n"
    "    items = puncta_claim_numbers(text, start, end, reach, NEG_CLAUSE_END, upper=upper)\n", "A2 dateline_claim_numbers window bound")
sub(ADAPT, "        m = RANGE_NUM.match(text, nx.end()) if nx else None\n        if not m:\n            break\n",
    "        m = RANGE_NUM.match(text, nx.end()) if nx else None\n        if not m or (upper is not None and m.end() > upper):\n            break\n",
    "A2 list continuation stops at the denial")
sub(ADAPT, "verdict = puncta_verdict(puncta_claim_numbers(tail, pm_.start(), pm_.end()))",
    "verdict = puncta_verdict(puncta_claim_numbers(tail, pm_.start(), pm_.end(), upper=claim_upper(tail, pm_.end())))", "A2 cs puncta call")
sub(ADAPT, "verdict = puncta_verdict(puncta_claim_numbers(text, m.start(), m.end(), PROSE_REACH))",
    "verdict = puncta_verdict(puncta_claim_numbers(text, m.start(), m.end(), PROSE_REACH, upper=claim_upper(text, m.end())))", "A2 cm puncta call")
sub(ADAPT, "named_ = {p for pairs in dateline_claim_numbers(tail, dm_.start(), dm_.end()) for p in pairs}",
    "named_ = {p for pairs in dateline_claim_numbers(tail, dm_.start(), dm_.end(), upper=claim_upper(tail, dm_.end())) for p in pairs}",
    "A2 cs calendar ref call")
sub(ADAPT, "cal = sorted({p for pairs in dateline_claim_numbers(o, m.start(), m.end()) for p in pairs}",
    "cal = sorted({p for pairs in dateline_claim_numbers(o, m.start(), m.end(), upper=claim_upper(o, m.end())) for p in pairs}",
    "A2 cs calendar prose call")

# ---- A3 ----
sub(ADAPT, '    t = sub_exact(t, "from jer_lib import (", "from ezek_lib import (kq_split_bytes, ", 1, "cs import")\n',
    '    t = sub_exact(t, "from jer_lib import (", "from ezek_lib import (kq_split_bytes, ", 1, "cs import")\n'
    "    # A3 (#e4 ruling T4-04): the mark, small-letter and paseq ref checks accept the SINGLE_WITNESS form the puncta check\n"
    "    # accepts (hyphenated or spaced); the elif is replaced first because the plain form is a substring of it\n"
    "    t = sub_exact(t, 'elif \"single-witness\" not in tail:', \"elif not SINGLE_WITNESS.search(tail):\", 1, \"cs A3 small-letter\")\n"
    "    t = sub_exact(t, 'if \"single-witness\" not in tail:', \"if not SINGLE_WITNESS.search(tail):\", 2, \"cs A3 mark and paseq\")\n",
    "A3 adapter replaces the literal single-witness tests")
sub(TK, "  a mark, small-letter or paseq ref; in prose that symmetry is model territory).\n",
    "  a mark, small-letter or paseq ref (hyphenated or spaced); in prose that symmetry is model territory).\n", "A3 TOOLKIT wording")
sub(TK, "`none is present`, and `is absent` / `is missing` at the clause end); dateline claims use\nthe same test. So",
    "`none is present`, and `is absent` / `is missing` at the clause end); dateline claims use\n"
    "the same test. A coordinated denial (`but none`, `none stands`, ...) denies only when the words\n"
    "between the mention and the denial name no verse number or carry an expectation modal (would,\n"
    "should, could, might, may, expected, anticipated); otherwise the mention is judged on the\n"
    "numbers before the denial (`stand at 41:5 but none is present in ch 46` claims 41:5). So", "A2 TOOLKIT paragraph")

# ---- the eight vectors ----
SECTION9B = r'''# 9b. #e4 AMENDMENTS to TOOLFIX-1 (ezek_controlling_rulings_a1#e4 rulings TOOLFIX-1, T4-03, T4-04). A1: the copular denial's
# clause end may be a newline. A2: a coordinated denial with a verse number and no expectation modal before it does not deny;
# the mention is judged on the numbers before the denial. A3: mark and paseq refs accept 'single witness' spaced.
E4_CS = [
    ("cs_e4_a2_positive_then_denial_nonsite_red",
     ["web:Ezek.41.1-Ezek.41.26 puncta extraordinaria stand at 41:5 but none is present in ch 46, single-witness"], "claims puncta extraordinaria"),
    ("cs_e4_a2_positive_then_denial_site_ok",
     ["web:Ezek.41.1-Ezek.41.26 puncta extraordinaria stand at 41:20 but none is present at 41:21, single-witness"], None),
    ("cs_e4_a3_mark_spaced_single_witness_ok", ["oshb:Ezek.1.28-Ezek.1.28 samekh (single witness)"], None),
    ("cs_e4_a3_paseq_spaced_single_witness_ok", ["oshb:Ezek.3.27-Ezek.3.27 paseq (count-only, single witness)"], None),
]
E4_CAL = [
    ("cal_e4_a2_positive_then_denial_red", {"boundary_rationale": "a dateline stands at 45:18 but none stands at 45:20"},
     "claims a dateline at MT 45:18 - a calendar"),
    ("cal_e4_a2_true_then_denial_ok", {"boundary_rationale": "the dateline at 40:1 opens the vision but none stands at 45:18"}, None),
]
E4_CM = [
    ("cm_e4_a1_copular_denial_at_field_end_flags",
     {"boundary_rationale": "puncta extraordinaria are absent", "device_notes": "the span is otherwise unremarkable",
      "span": "Ezek.41.12-Ezek.41.20"}, {"false_puncta_absence_claim": True}),
    ("cm_e4_a2_positive_then_denial_nonsite_flags",
     {"boundary_rationale": "puncta extraordinaria stand at 41:5 but none is present in ch 46", "span": "Ezek.41.12-Ezek.41.20"},
     {"puncta_claim_in_ezek": True}),
]
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "e4_cs.jsonl"
    p.write_text("\n".join([json.dumps({"decision_id": d, "boundary_evidence_refs": refs}, ensure_ascii=False) for d, refs, _ in E4_CS]
                           + [json.dumps(dict({"decision_id": d}, **f), ensure_ascii=False) for d, f, _ in E4_CAL]), encoding="utf-8")
    rep = run("citation_sweep.py", p)
    for did, _, expect in E4_CS + E4_CAL:
        mine = [x for x in rep["problems"] if x.startswith(did + ":")]
        check("citation_sweep %s: %s" % (did, "no problem" if expect is None else repr(expect)),
              (not mine) if expect is None else any(expect in x for x in mine), mine)
    p = Path(td) / "e4_cm.jsonl"
    p.write_text("\n".join(json.dumps(dict({"decision_id": d}, **f), ensure_ascii=False) for d, f, _ in E4_CM), encoding="utf-8")
    rep = run("check_marks.py", p)
    for d, _, expect in E4_CM:
        for rule, fires in expect.items():
            mine = [fl for fl in rep["flags"] if fl.get("decision_id") == d and fl.get("rule") == rule]
            check("check_marks %s: %s %s" % (d, rule, "fires" if fires else "silent"), bool(mine) == fires, mine)

'''
sub(TEST, 'failed = [r for r in results if not r["ok"]]\n', SECTION9B + 'failed = [r for r in results if not r["ok"]]\n', "section 9b vectors")

# ---- regenerate, test, parity ----
pins = ["citation_sweep.py=" + sha(T / "citation_sweep.py"), "check_marks.py=" + sha(T / "check_marks.py")]
g = run([ADAPT, "--replace"] + pins, T)
out = {"applied": applied, "regen_exit": g.returncode, "regen": g.stdout.strip().splitlines()[-4:], "regen_err": g.stderr[-800:]}
if g.returncode != 0:
    print(json.dumps(out, ensure_ascii=False, indent=1))
    raise SystemExit(1)


def test_run(tools_dir):
    p = run([tools_dir / "_test_zone_tools_ezek.py"], tools_dir)
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"error": True, "stdout_tail": p.stdout[-1500:], "stderr_tail": p.stderr[-1500:]}
    return {"checks": d["checks"], "passed": d["passed"], "verdict": d["verdict"], "failed": [f.get("check", "") for f in d["failed"]],
            "failed_detail": [{"check": f.get("check"), "detail": str(f.get("detail"))[:300]} for f in d["failed"]]}


staged = test_run(T)
out["tests"] = {k: staged.get(k) for k in ("checks", "passed", "verdict", "failed_detail", "error", "stdout_tail", "stderr_tail") if k in staged}
lib = run([T / "ezek_lib.py"], T)
out["ezek_lib_selftest"] = json.loads(lib.stdout).get("verdict") if lib.stdout.strip().startswith("{") else {"exit": lib.returncode, "tail": lib.stdout[-400:]}
sc = run([T / "_toolkit_selfcheck.py"], T)
try:
    scd = json.loads(sc.stdout)
    out["toolkit_selfcheck"] = {"checks": scd.get("checks"), "passed": scd.get("passed"), "verdict": scd.get("verdict")}
except json.JSONDecodeError:
    out["toolkit_selfcheck"] = {"exit": sc.returncode, "tail": sc.stdout[-400:]}
s = run([T / "run_validator_suite.py", SUITE / "rows.jsonl"], T)
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
out["suite_summary"] = {"installed": old.get("summary"), "staged": new.get("summary")}
out["suite_list_differences"] = diff or "NONE"

# ---- discrimination against two baselines ----
staged_test = TEST.read_text(encoding="utf-8")
baselines = {}
for label, overlay in (("installed", None), ("t4fix_batch1", B1)):
    bt = fresh_tree(SCR / ("stage_t4fix2_base_" + label), overlay=overlay)
    (bt / "_test_zone_tools_ezek.py").write_text(staged_test, encoding="utf-8", newline="\n")
    baselines[label] = test_run(bt)


def fails(label, vid):
    return any(vid in c for c in baselines[label].get("failed", []))


per_vector = {v: {"fails_on_installed": fails("installed", v), "fails_on_t4fix_batch1": fails("t4fix_batch1", v),
                  "passes_staged": not any(v in c for c in staged.get("failed", []))} for v in NEW_VECTORS + BATCH1_VECTORS}
declared = NEW_VECTORS + BATCH1_VECTORS
unexpected = {label: [c for c in baselines[label].get("failed", []) if not any(v in c for v in declared)] for label in baselines}
out["discrimination"] = {
    "per_vector": per_vector,
    "new_vectors_failing_on_some_baseline": all(per_vector[v]["fails_on_installed"] or per_vector[v]["fails_on_t4fix_batch1"] for v in NEW_VECTORS),
    "new_vectors_failing_on_installed": [v for v in NEW_VECTORS if per_vector[v]["fails_on_installed"]],
    "new_vectors_passing_on_installed": [v for v in NEW_VECTORS if not per_vector[v]["fails_on_installed"]],
    "batch1_vectors_still_failing_on_installed": all(per_vector[v]["fails_on_installed"] for v in BATCH1_VECTORS),
    "all_pass_staged": all(per_vector[v]["passes_staged"] for v in declared),
    "unexpected_failures": unexpected,
    "baseline_counts": {k: {"checks": v.get("checks"), "passed": v.get("passed")} for k, v in baselines.items()},
}
out["staged_digests"] = {n: sha(T / n) for n in ("citation_sweep.py", "check_marks.py", "_adapt_zone_tools_ezek.py", "_test_zone_tools_ezek.py", "TOOLKIT.md")}
(SCR / "stage_t4fix2" / "stage_run.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps(out, ensure_ascii=False, indent=1))
