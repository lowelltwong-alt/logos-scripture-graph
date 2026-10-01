"""Stage TOOLFIX-3 as toolfix3_batch1 per ezek_controlling_rulings_a1#e6 rulings T5-VERIFIER, T5-TOOLKIT-DOCS and T5-SEQUENCE,
over the INSTALLED tools (receipt ezek_tools_install_toolfix2_batch3.json). Session scratch only; nothing is installed and
nothing under SP is written.

CONTENT (no validator-suite member is touched):
  - campaign/_cure_verification.py: the verifier edit T5-VERIFIER (1)-(5), from _cure_verification.candidate.py beside this
    script;
  - Ezek/tools/TOOLKIT.md: T5-TOOLKIT-DOCS (1)-(3) and (a)-(d), each a count-checked replacement.

THE RUN (T5-SEQUENCE gates):
  - the staged verifier's selftest, and the installed verifier's, to show every existing vector keeps its expectation;
  - every TOOLFIX-3 vector evaluated against the INSTALLED verifier too (the DISCRIMINATING column);
  - both real claims files (private copies; --root SP/Ezek) under the installed and the staged verifier, with --rulings (#e2
    through #e6) and --require-rulings; supersession classes before and after;
  - the six draft suite-file claims appended to a private copy of the toolkit-repair claims file, and verified under the
    staged verifier;
  - the toolkit selfcheck at the corrected TOOLKIT.md (a stage copy of the tools and of SP/Ezek's top-level data files);
  - machine checks of the corrected statements:
    - the quoted note texts are byte-exact;
    - the closed set is tested against the code's regexes;
    - check_marks' copies of those regexes are identical to citation_sweep's;
    - W6's 60-character gate stands;
    - skeleton() deletes U+05BE;
    - the install receipts and the files each last installed;
  - the sibling-sweep statement list over the whole corrected file, for the orchestrator's review;
  - staged digests and diffs.

Usage: stage_tf3.py"""
import ast
import difflib
import hashlib
import importlib.util
import json
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
EZ = SP / "Ezek"
ROOT = Path(__file__).resolve().parent
ST = ROOT / "sp_durable"
CAND = ROOT / "_cure_verification.candidate.py"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
V_INST = SP / "campaign" / "_cure_verification.py"
TK_INST = EZ / "tools" / "TOOLKIT.md"
V_INST_SHA = "7f5ea4a9eb64dced70b2d3358e067de36e6a26f8ae6fc5ea43312ef72f7518da"
TK_INST_SHA = "9771c440a49404051e5845a0896afb8f18dbf8c7ff7d66e9a9cce43638dbb31c"
RECEIPTS = SP / "campaign" / "receipts"
REC_TF2 = RECEIPTS / "ezek_tools_install_toolfix2_batch3.json"
T5 = EZ / "ezek_toolkit_install_review_T5.json"
RULINGS = [EZ / "ezek_controlling_agent_rulings.v1.json", EZ / "ezek_controlling_agent_rulings_e3.v1.json",
           EZ / "ezek_controlling_agent_rulings_e4.v1.json", EZ / "ezek_controlling_agent_rulings_e5.v1.json",
           EZ / "ezek_controlling_agent_rulings_e6.v1.json"]
CLAIM_FILES = ("ezek_cure_claims.v1.jsonl", "ezek_cure_claims_toolkit_repair.v1.jsonl")
DRAFT_IDS = {"citation_sweep.py": "EZEK-TK-CURE-citation_sweep", "check_marks.py": "EZEK-TK-CURE-check_marks",
             "ezek_lib.py": "EZEK-TK-CURE-ezek_lib-v2", "check_register.py": "EZEK-TK-CURE-check_register",
             "check_web_quotes.py": "EZEK-TK-CURE-check_web_quotes", "normalize_hebrew_in_json.py": "EZEK-TK-CURE-normalizer-v2"}
SUCCESSOR_OF = {"ezek_lib.py": "EZEK-TK-CURE-ezek_lib", "normalize_hebrew_in_json.py": "EZEK-TK-CURE-normalizer"}
REQUIRED_DISCRIMINATING = ("s1_19a_whitespace_author", "author_exec_only_checker_bare_attempt_same_job",
                           "author_attempt_and_exec_differ_checker_is_exec_job", "case_variant_of_author_as_checker",
                           "failing_run_exit_1_accepted", "exit_is_the_word_passed", "checker_verdict_not_fit",
                           "s1_19b_dup_cure_id_trailing_space", "compound_ordered_by_second_bogus", "s1_19c_period_prefix",
                           "s1_19c_slash_prefix", "e_names_only_as_successor_overbroad", "ratify_with_changes_verb_ordering_retirement")
X = "\u00d7"
applied = []


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(args, cwd):
    return subprocess.run([sys.executable] + [str(a) for a in args], capture_output=True, text=True, encoding="utf-8", env=ENV, cwd=str(cwd))


def json_or_tail(p):
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"error": True, "exit": p.returncode, "stdout_tail": p.stdout[-1500:], "stderr_tail": p.stderr[-1500:]}


def sub(path, old, new, label):
    t = path.read_text(encoding="utf-8")
    n = t.count(old)
    if n != 1:
        raise SystemExit("ABORT: %s: expected 1 occurrence in %s, found %d" % (label, path.name, n))
    path.write_text(t.replace(old, new), encoding="utf-8", newline="\n")
    applied.append(label)


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def regex_from(path, name):
    for node in ast.parse(Path(path).read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return eval(compile(ast.Expression(node.value), str(path), "eval"), {"re": re})
    raise SystemExit("ABORT: %s defines no %s" % (Path(path).name, name))


# ------------------------------------------------------------------ preconditions
if sha(V_INST) != V_INST_SHA or sha(TK_INST) != TK_INST_SHA:
    raise SystemExit("ABORT: the installed verifier or TOOLKIT.md is not at the digest T5 reviewed")
rec = json.loads(REC_TF2.read_text(encoding="utf-8"))
for name, f in rec["files"].items():
    live = (SP / name) if name.startswith("campaign/") else (EZ / "tools" / name)
    if sha(live) != f["after"]:
        raise SystemExit("ABORT: %s is not the toolfix2_batch3 installed digest" % name)
t5 = json.loads(T5.read_text(encoding="utf-8"))
ready = {x["artifact"]: x for x in t5["cure_claim_readiness"]}
for name in DRAFT_IDS:
    r = ready.get("tools/" + name)
    if not r or r.get("fit") is not True or r.get("sha256") != rec["files"][name]["after"]:
        raise SystemExit("ABORT: T5 did not find tools/%s fit at its installed digest" % name)
if ready["campaign/_cure_verification.py"]["fit"] is not False:
    raise SystemExit("ABORT: T5's readiness for the verifier is not 'not fit'")
py_compile.compile(str(CAND), doraise=True)

# ------------------------------------------------------------------ stage tree
if ST.exists():
    shutil.rmtree(ST)
ign = shutil.ignore_patterns("__pycache__", "*.pyc")
shutil.copytree(EZ / "tools", ST / "Ezek" / "tools", ignore=ign)
for f in EZ.iterdir():
    if f.is_file():
        shutil.copy2(f, ST / "Ezek" / f.name)
(ST / "campaign").mkdir(parents=True)
V_STG = ST / "campaign" / "_cure_verification.py"
shutil.copyfile(CAND, V_STG)
TK = ST / "Ezek" / "tools" / "TOOLKIT.md"

# ------------------------------------------------------------------ T5-TOOLKIT-DOCS (1)-(3)
sub(TK, "every Hebrew run byte-true to the verse text or to a Qere, standing on word boundaries: no Hebrew letter or combining mark "
        "beside a pointed run, no Hebrew letter beside an unpointed one (S1-07; `collate_hebrew` applies the same rule); NFD-only "
        "matches stay defects",
    "every Hebrew run byte-true to the verse text or to a Qere, standing on word boundaries (S1-07; collate_hebrew applies the same "
    "rule); an NFD-only match at the verse tier is REPLACED by the verse's bytes and counted fixed, and the suite treats fixed>0 as "
    "HARD (E-01); an NFD-only Qere match is a defect and is never replaced", "(1) normalizer row")
sub(TK, "ranges expanded: every\nnamed verse a site = a true claim, none = a false claim, a mix = `ambiguous`",
    "a named single verse must be a site; a written range must hold at least one site; among several named items\n"
    "every one a site = a true claim, none = a false claim, a mix = ambiguous", "(2) puncta paragraph")
sub(TK, "but only as one of a closed set (`but none`, `though none`, `none stands`,\n`none is present`, and `is absent` / `is missing` "
        "at the clause end); dateline claims use\nthe same test.",
    "but only as one of a closed set: but|though|although|yet none, but|though|although|yet there is|are none,\n"
    "none stands, none is present|written|there|found, none appears|exists, and is|are absent|lacking|missing at the\n"
    "clause end - the set is DENIAL_COORD and DENIAL_COPULAR in citation_sweep.py; where this paragraph and the code differ,\n"
    "the code is the contract and this paragraph is the defect. Dateline claims use the same test.", "(3) closed set")
# ------------------------------------------------------------------ (a)-(d)
sub(TK, "## Staged tools (Tier-0, m8-mesh-r3) \u2014 staged 2026-09-10, after the writer wave\n",
    "## Staged tools (Tier-0, m8-mesh-r3) \u2014 staged 2026-09-10, after the writer wave; installed 2026-09-11 by receipts "
    "ezek_tools_install_t4fix_batch2.json and ezek_tools_install_toolfix2_batch3.json\n", "(a) heading")
sub(TK, "; `no pe or samekh` is an absence phrase (W6); mark-disclosure symmetry (FLAGS) |",
    "; `no pe or samekh` is an absence phrase (W6), read only in mark talk: a MARKISH_CTX word within 60 characters; besides "
    "that negator before it, a K/Q token is denied by a closed-set denial later in its clause, the same set as citation_sweep's "
    "DENIAL_COORD and DENIAL_COPULAR (T4-03); mark-disclosure symmetry (FLAGS) |", "(b) check_marks row")
PM = json.loads((EZ / "pmarks_Ezek.json").read_text(encoding="utf-8"))
NOTES = {n["text"] for v in PM["notes_other"].values() for n in v}
FAITHFUL = next(t for t in NOTES if t.startswith("BHS has been faithful"))
KETIB = next(t for t in NOTES if t.startswith("We have abandoned or added a ketib/qere"))
ADAPT = next(t for t in NOTES if t.startswith("Adaptations to a Qere"))
ANOM = next(t for t in NOTES if t.startswith("Marks an anomalous form"))
PUNCT = next(t for t in NOTES if t.startswith("We read punctuation in L"))
sub(TK, '13 %s "BHS has been faithful to L where there might be a question of validity"' % X, '13 %s "%s"' % (X, FAITHFUL), "(c) note 13")
sub(TK, '8 %s "we have abandoned or added a ketiv/qere relative to BHS"' % X, '8 %s "%s"' % (X, KETIB), "(c) note 8")
sub(TK, '3 %s "adaptations to a Qere which L and BHS do not indicate"' % X, '3 %s "%s"' % (X, ADAPT), "(c) note 3")
sub(TK, '2 %s "marks an anomalous form"' % X, '2 %s "%s"' % (X, ANOM), "(c) note 2")
sub(TK, 'OSHB note — *"We read punctuation in L differently from\n  BHS"* — followed directly by the pe mark.',
    'OSHB note — *"%s"* —\n  followed directly by the pe mark.' % PUNCT, "(c) note 33:20")
sub(TK, '  that a maqaf is "absent from the text" is reading the extract, not the source.\n',
    '  that a maqaf is "absent from the text" is reading the extract, not the source.\n'
    '- ezek_lib.skeleton() deletes U+05BE with the other points (POINTS spans U+0591-U+05C7), so a maqaf-joined quote never\n'
    '  collates at any tier; its docstring sentence "maps maqaf to SPACE" is wrong and unasserted (T5-07, recorded as debt);\n'
    '  write words space-separated, as the extract does.\n', "(d) encoding note")
out = {"applied": applied}

# ------------------------------------------------------------------ verifier selftests and the existing vectors
vs = json_or_tail(run([V_STG, "--selftest"], ROOT))
vi = json_or_tail(run([V_INST, "--selftest"], ROOT))
out["verifier_selftest_staged"] = {k: vs.get(k) for k in ("vectors", "failed", "verdict", "error")} | {
    "failed_vectors": [r for r in vs.get("results", []) if not r.get("ok")]}
out["verifier_selftest_installed"] = {k: vi.get(k) for k in ("vectors", "failed", "verdict", "error")}
staged_by = {r["vector"]: r for r in vs.get("results", [])}
keep = {}
for r in vi.get("results", []):
    s = staged_by.get(r["vector"], {})
    keep[r["vector"]] = {"installed_expected": r.get("expected"), "staged_expected": s.get("expected"), "staged_ok": s.get("ok")}
out["existing_vectors"] = {"count": len(keep), "all_present_and_ok": all(v["staged_ok"] is True for v in keep.values()),
                           "expectation_changed": {k: v for k, v in keep.items() if v["installed_expected"] != v["staged_expected"]}}

# ------------------------------------------------------------------ discrimination against the installed verifier
inst, stg = load_module(V_INST, "verifier_installed"), load_module(V_STG, "verifier_staged")
td = Path(tempfile.mkdtemp(dir=ROOT, prefix="disc_"))
disc = {}
for v in stg.tf3_vectors(td):
    rs, ri = stg.evaluate(stg, v, td), stg.evaluate(inst, v, td)
    disc[v[1]] = {"expected": rs["expected"], "staged_got": rs["got"], "staged_ok": rs["ok"], "installed_got": ri["got"],
                  "fails_on_installed": not ri["ok"], "discrimination_required": v[1] in REQUIRED_DISCRIMINATING}
out["tf3_vectors"] = disc
out["tf3_vectors_summary"] = {"count": len(disc), "staged_all_ok": all(x["staged_ok"] for x in disc.values()),
                              "required_discriminating_all_fail_on_installed": all(disc.get(n, {}).get("fails_on_installed") for n in REQUIRED_DISCRIMINATING),
                              "required_missing": [n for n in REQUIRED_DISCRIMINATING if n not in disc],
                              "discriminating": sorted(n for n, x in disc.items() if x["fails_on_installed"]),
                              "not_discriminating": sorted(n for n, x in disc.items() if not x["fails_on_installed"])}

# ------------------------------------------------------------------ the real claims files, before and after
priv = ROOT / "claims_private"
if priv.exists():
    shutil.rmtree(priv)
priv.mkdir()
for cf in CLAIM_FILES:
    shutil.copyfile(EZ / cf, priv / cf)
out["real_claims"] = {}
for label, V in (("installed", V_INST), ("staged", V_STG)):
    out["real_claims"][label] = {}
    for cf in CLAIM_FILES:
        r = json_or_tail(run([V, "--claims", priv / cf, "--root", EZ, "--rulings"] + RULINGS + ["--require-rulings"], ROOT))
        out["real_claims"][label][cf] = {k: r.get(k) for k in ("claims", "accepted", "refused", "superseded", "supersession_classes", "verdict", "error")} | {
            "verdicts": {o["cure_id"]: o["verdict"] for o in r.get("results", []) if o.get("record") != "supersession"},
            "refusal_reasons": [o for o in r.get("results", []) if o["verdict"] == "REFUSED"]}

# ------------------------------------------------------------------ the six draft claims (T5-SEQUENCE claims (1))
suite_rep = json.loads((EZ / "repair" / "suite_after_toolfix2_batch3" / "rows.jsonl.validator_report.json").read_text(encoding="utf-8"))
members = sorted(k for k in suite_rep if k != "rows_file")
par = t5["suite_parity"]
par_text = " ".join(par["differences"])
named = [m for m in members if m in par_text]
zone, lib = rec["checks_after"]["zone_tests"], rec["checks_after"]["ezek_lib_selftest"]
t5_tools = {x["path"].replace("\\", "/")[len("SP/Ezek/tools/"):]: x["artifact_sha256_at_review"] for x in t5["artifacts_reviewed"]
            if x["path"].replace("\\", "/").startswith("SP/Ezek/tools/")}   # the installed tools only, keyed by file name
drafts = []
for name, cid in DRAFT_IDS.items():
    d = rec["files"][name]["after"]
    claim = {"cure_id": cid, "author_attempt_id": "ezek_orchestrator_toolfix2_a1", "author_execution_id": "ezek_orchestrator_toolfix2_a1#e1",
             "author_note": ("orchestrator-staged TOOLFIX-2 (SP/Ezek/proposals/toolfix2_batch3), installed by receipt "
                             "ezek_tools_install_toolfix2_batch3.json under OW-11; no subagent authored it")}
    if name in SUCCESSOR_OF:
        claim["successor_of"] = SUCCESSOR_OF[name]
    claim.update({
        "ordered_by": "ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2; ezek_controlling_rulings_a1#e5 ruling INSTALL-TF2-1",
        "written_per": ("ezek_controlling_rulings_a1#e6 ruling T5-SEQUENCE claims (1): drafted on T5's verdict; appended only after the "
                        "TOOLFIX-3 verifier is installed, in one append followed by one verifier run under --rulings --require-rulings"),
        "items": {"per_t5_cure_claim_readiness": ready["tools/" + name]["why"]},
        "artifact_path": "tools/" + name, "artifact_sha256": d,
        "verification": [
            {"tool": "tools/_test_zone_tools_ezek.py", "tool_sha256": rec["files"]["_test_zone_tools_ezek.py"]["after"],
             "artifact_sha256_at_run": d, "exit": zone["exit"],
             "counts": {"checks": zone["checks"], "passed": zone["passed"], "failed": zone["failed"]}, "verdict": zone["verdict"],
             "run": "the post-install check recorded in the receipt", "evidence": "campaign/receipts/%s checks_after.zone_tests" % REC_TF2.name,
             "evidence_sha256": sha(REC_TF2)},
            {"tool": "tools/ezek_lib.py (selftest)", "tool_sha256": rec["files"]["ezek_lib.py"]["after"], "artifact_sha256_at_run": d,
             "exit": lib["exit"], "counts": {"checks": lib["checks"], "passed": lib["passed"], "failed": lib["failed"]}, "verdict": lib["verdict"],
             "run": "the post-install check recorded in the receipt", "evidence": "campaign/receipts/%s checks_after.ezek_lib_selftest" % REC_TF2.name,
             "evidence_sha256": sha(REC_TF2)},
            {"tool": "tools/run_validator_suite.py (T5's suite-parity comparison against the installed report)",
             "tool_sha256": t5_tools.get("run_validator_suite.py"), "artifact_sha256_at_run": d,
             "counts": {"checks": len(members), "passed": len(named), "failed": len(members) - len(named)},
             "verdict": par["verdict"], "run_by": "ezek_toolkit_install_review_t5_a1#e1",
             "rows_sha256": par["counts"]["private_rows_sha256"], "report_sha256_attested_by_t5": par["counts"]["private_report_sha256"],
             "suite_exit": par["counts"]["suite_exit"],
             "note": ("counts are the suite members T5 compared JSON-identical to the installed report; the suite's own exit is 1 on "
                      "the enumerated HARD set (FIXUP-1 items) and is recorded as suite_exit, not as this comparison's exit"),
             "evidence": "Ezek/ezek_toolkit_install_review_T5.json suite_parity", "evidence_sha256": sha(T5)}],
        "distinct_checker": {"attempt_id": "ezek_toolkit_install_review_t5_a1", "execution_id": "ezek_toolkit_install_review_t5_a1#e1",
                             "verdict": "fit_with_changes; artifact fit=true per cure_claim_readiness", "artifact_sha256_at_review": d,
                             "evidence_path": "Ezek/ezek_toolkit_install_review_T5.json"}})
    if t5_tools.get(name) != d:
        raise SystemExit("ABORT: T5 did not review tools/%s at %s" % (name, d[:16]))
    drafts.append(claim)
(ROOT / "draft_claims_tf3.jsonl").write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in drafts), encoding="utf-8", newline="\n")
with_drafts = priv / "ezek_cure_claims_toolkit_repair.with_drafts.jsonl"
with_drafts.write_bytes((EZ / "ezek_cure_claims_toolkit_repair.v1.jsonl").read_bytes() + (ROOT / "draft_claims_tf3.jsonl").read_bytes())
out["draft_claims"] = {"file": str(ROOT / "draft_claims_tf3.jsonl"), "sha256": sha(ROOT / "draft_claims_tf3.jsonl"), "ids": list(DRAFT_IDS.values()),
                       "suite_members_compared": members, "members_named_identical_by_t5": named}
for label, V in (("staged", V_STG), ("installed", V_INST)):
    r = json_or_tail(run([V, "--claims", with_drafts, "--root", EZ, "--rulings"] + RULINGS + ["--require-rulings"], ROOT))
    out["draft_claims"][label] = {k: r.get(k) for k in ("claims", "accepted", "refused", "superseded", "verdict", "error")} | {
        "verdicts": {o["cure_id"]: o["verdict"] for o in r.get("results", []) if o.get("record") != "supersession"},
        "refusal_reasons": [o for o in r.get("results", []) if o["verdict"] == "REFUSED"]}

# ------------------------------------------------------------------ toolkit selfcheck at the corrected TOOLKIT.md
tk = json_or_tail(run([ST / "Ezek" / "tools" / "_toolkit_selfcheck.py"], ST / "Ezek" / "tools"))
out["toolkit_selfcheck"] = {k: tk.get(k) for k in ("checks", "passed", "verdict", "error", "stdout_tail")} | {
    "failed": [c for c in tk.get("results", tk.get("failed", [])) if isinstance(c, dict) and not c.get("ok", True)][:10]}

# ------------------------------------------------------------------ machine checks of the corrected statements
text = TK.read_text(encoding="utf-8")
block = text[text.index("OSHB editorial notes"): text.index("### PROPHETIC FRAME SPINE")]
quoted = re.findall(r'"([^"]+)"', block)
cs_coord, cs_cop = regex_from(EZ / "tools" / "citation_sweep.py", "DENIAL_COORD"), regex_from(EZ / "tools" / "citation_sweep.py", "DENIAL_COPULAR")
cm_coord, cm_cop = regex_from(EZ / "tools" / "check_marks.py", "DENIAL_COORD"), regex_from(EZ / "tools" / "check_marks.py", "DENIAL_COPULAR")
coord_forms = ["%s %snone" % (c, t) for c in ("but", "though", "although", "yet") for t in ("", "there is ", "there are ")] + \
              ["none stands", "none is present", "none is written", "none is there", "none is found", "none appears", "none exists"]
cop_forms = ["%s %s." % (v, w) for v in ("is", "are") for w in ("absent", "lacking", "missing")]
sys.path.insert(0, str(ST / "Ezek" / "tools"))
lib_mod = load_module(ST / "Ezek" / "tools" / "ezek_lib.py", "ezek_lib_stage")
cm_src = (EZ / "tools" / "check_marks.py").read_text(encoding="utf-8")
receipts = {}
for p in sorted(RECEIPTS.glob("ezek_tools_install_*.json")):
    r = json.loads(p.read_text(encoding="utf-8"))
    receipts[p.name] = {"recorded_at": r.get("recorded_at"), "files": {n: f.get("after") for n, f in r.get("files", {}).items() if f.get("state") == "installed"}}
last_installer = {}
for rn, r in sorted(receipts.items(), key=lambda kv: kv[1]["recorded_at"]):
    for n, after in r["files"].items():
        last_installer[n] = (rn, after)
live_last = {n: {"receipt": rn, "live_equals_after": sha((SP / n) if n.startswith("campaign/") else (EZ / "tools" / n)) == after}
             for n, (rn, after) in last_installer.items()}
heading_names = {"ezek_tools_install_t4fix_batch2.json", "ezek_tools_install_toolfix2_batch3.json"}
out["machine_checks"] = {
    "note_quotes_byte_exact": {"quoted": quoted, "all_in_pmarks_notes_other": all(q in NOTES for q in quoted), "count": len(quoted)},
    "closed_set": {"coord_forms_all_match": all(cs_coord.search(f) for f in coord_forms),
                   "copular_forms_all_match": all(cs_cop.search(f) for f in cop_forms),
                   "check_marks_regexes_identical_to_citation_sweep": (cs_coord.pattern, cs_coord.flags, cs_cop.pattern, cs_cop.flags)
                   == (cm_coord.pattern, cm_coord.flags, cm_cop.pattern, cm_cop.flags),
                   "paragraph_carries_the_ruled_list": "but|though|although|yet none, but|though|although|yet there is|are none," in text},
    "w6_gate_60_characters": "MARKISH_CTX.search(text[max(0, m.start() - 60):m.start() + 60])" in cm_src,
    "t4_03_later_denial_in_check_marks_rule_4": 'kq_negation(text, m.start()) or ("plain" if denied_after(text, m.end()) else None)' in cm_src,
    "skeleton_deletes_maqaf": {"skeleton_of_alef_maqaf_bet": lib_mod.skeleton("\u05d0\u05be\u05d1"),
                               "deleted_without_space": lib_mod.skeleton("\u05d0\u05be\u05d1") == "\u05d0\u05d1",
                               "points_covers_u05be": bool(lib_mod.POINTS.fullmatch("\u05be"))},
    "install_receipts": {n: r["recorded_at"] for n, r in receipts.items()},
    "files_last_installed_by": live_last,
    "heading_receipts_are_the_last_installers_of_every_live_file": all(v["receipt"] in heading_names and v["live_equals_after"]
                                                                       for n, v in live_last.items()),
    "files_last_installed_by_another_receipt": {n: v for n, v in live_last.items() if v["receipt"] not in heading_names},
}

# ------------------------------------------------------------------ sibling-sweep statement list (for the orchestrator's review)
PHRASES = ["single-witness", "single witness", "NFD-only", "NFD", "word boundar", "combining mark", "maqaf", "160 characters", "QERE tier",
           "closed set", "denial", "ranges expanded", "range", "no other K/Q", "negator", "no pe or samekh", "MARKISH", "check_register",
           "REG-TF2-1", "check_web_quotes", "curly double", "HARD members", "E-01", "E-02", "measurements", "K/Q cluster", "puncta",
           "dateline", "45:18", "11:19", "26:10", "24:1", "OSHB", "33:20", "BHS", "faithful to", "do not indicate", "formula",
           "staged 2026-09-10", "installed 2026-09-11", "skeleton", "fixed"]
lines = text.splitlines()
hits = {}
for ph in PHRASES:
    hits[ph] = [{"line": i + 1, "text": l} for i, l in enumerate(lines) if ph.lower() in l.lower()]
(ROOT / "sibling_sweep_candidates.json").write_text(json.dumps({"toolkit_sha256": sha(TK), "phrases": hits}, ensure_ascii=False, indent=1),
                                                    encoding="utf-8", newline="\n")
out["sibling_sweep_candidates"] = {"path": str(ROOT / "sibling_sweep_candidates.json"), "phrases": len(PHRASES),
                                   "distinct_lines": len({h["line"] for v in hits.values() for h in v})}

# ------------------------------------------------------------------ digests and diffs
(ROOT / "diffs").mkdir(exist_ok=True)
for inst_p, stg_p, label in ((V_INST, V_STG, "campaign__cure_verification.py"), (TK_INST, TK, "Ezek__tools__TOOLKIT.md")):
    diff = "".join(difflib.unified_diff(inst_p.read_text(encoding="utf-8").splitlines(True), stg_p.read_text(encoding="utf-8").splitlines(True),
                                        fromfile="installed %s" % sha(inst_p)[:12], tofile="staged %s" % sha(stg_p)[:12]))
    (ROOT / "diffs" / (label + ".diff")).write_text(diff, encoding="utf-8", newline="\n")
out["staged_digests"] = {"campaign/_cure_verification.py": sha(V_STG), "tools/TOOLKIT.md": sha(TK)}
out["installed_digests"] = {"campaign/_cure_verification.py": sha(V_INST), "tools/TOOLKIT.md": sha(TK_INST)}
(ROOT / "stage_run.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
summary = {k: out[k] for k in ("applied", "verifier_selftest_staged", "verifier_selftest_installed", "existing_vectors", "tf3_vectors_summary",
                               "toolkit_selfcheck", "machine_checks", "sibling_sweep_candidates", "staged_digests")}
summary["real_claims"] = {lab: {cf: {k: v[k] for k in ("claims", "accepted", "refused", "superseded", "verdict")} | {"classes": [c["ordered_by_class"] for c in v["supersession_classes"] or []]}
                                for cf, v in d_.items()} for lab, d_ in out["real_claims"].items()}
summary["draft_claims"] = {k: out["draft_claims"][k] for k in ("sha256", "ids", "suite_members_compared", "members_named_identical_by_t5")} | {
    lab: {k: out["draft_claims"][lab][k] for k in ("claims", "accepted", "refused", "superseded", "verdict")} for lab in ("staged", "installed")}
print(json.dumps(summary, ensure_ascii=False, indent=1))
