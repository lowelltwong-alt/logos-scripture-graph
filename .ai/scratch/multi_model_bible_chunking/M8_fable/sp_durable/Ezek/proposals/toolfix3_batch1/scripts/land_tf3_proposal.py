"""Land TOOLFIX-3 (ezek_controlling_rulings_a1#e6 rulings T5-VERIFIER, T5-TOOLKIT-DOCS and T5-SEQUENCE) DURABLY as
SP/Ezek/proposals/toolfix3_batch1. T5-SEQUENCE pre-authorizes the install when its gates hold. This lander recomputes those
gates from the stage outputs on disk, and records the orchestrator's R6 sibling-sweep review of the corrected TOOLKIT.md.
Nothing is installed here.

GATES (all must hold to land as install-ready):
  - the verifier selftest is GREEN, and every existing vector keeps its expectation, except the S1-19(e) class that
    T5-VERIFIER (4) renames;
  - every T5-VERIFIER vector passes on the staged verifier, and each vector whose refusal is new is DISCRIMINATING (it fails on
    the installed verifier);
  - both real claims files are GREEN under --rulings --require-rulings on the installed and the staged verifier, with the
    supersession classes recorded before and after;
  - the six draft claims are GREEN, all ACCEPTED, on private copies under the staged verifier;
  - the toolkit selfcheck is GREEN at the corrected TOOLKIT.md;
  - the machine checks of the corrected statements hold;
  - the staged digests are reproduced;
  - no sibling-sweep statement is found contradictory.

WRITES staged/ (campaign/_cure_verification.py, TOOLKIT.md), diffs/, scripts/, runs/, draft_claims_tf3.jsonl, sibling_sweep.json
and manifest.json. The in-flight pin guard runs first; the batch directory is never replaced.

Usage: land_tf3_proposal.py"""
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
ROOT = Path(__file__).resolve().parent
ST = ROOT / "sp_durable"
OUT = EZ / "proposals" / "toolfix3_batch1"
BATCH = "toolfix3_batch1"
SCRIPTS = ("stage_tf3.py", "land_tf3_proposal.py", "_cure_verification.candidate.py")
RENAMED = {"S1-19(e) a ruling that names the retired cure id": ("ruling_names_retired_cure", "ruling_orders_retirement")}
# The orchestrator's R6 sibling-sweep review of the corrected file. Each key phrase lists the verdict for every line of the staged
# TOOLKIT.md that carries it (lines are recomputed from the staged bytes at landing). A 'contradiction' verdict blocks the landing.
REVIEW = {
    "closed set": ("consistent", "the check_marks row and the denial paragraph state the set as citation_sweep's DENIAL_COORD and "
                                 "DENIAL_COPULAR; machine check: every listed form matches, and check_marks' copies are identical"),
    "denial": ("consistent", "the denial paragraph (adjacent negators cancel; the closed-set later denial; the coordinated-denial "
                             "number/modal rule; its examples) agrees with DENIAL_COORD, EXPECT_MODAL and _denial_window_end; 'a denial "
                             "behind a comma stays outside the clause' describes the parse, not a verdict (T5-06 (b) is a puncta-at-a-"
                             "site outcome; #e6 restated the gate sentence for datelines only)"),
    "NFD": ("consistent", "the normalizer row states the verse-tier replacement and the Qere defect as ruled; the U+05C4 note, the "
                          "QERE-tier raw-bytes sentence and the skeleton-after-NFD note agree with it"),
    "ranges expanded": ("consistent", "the phrase no longer stands; the puncta sentence states the single-verse, range and several-"
                                      "items rule as ruled"),
    "range": ("consistent", "the citation_sweep row and 'the row's span or the ref's range decides' agree with puncta_verdict's rule "
                            "that a written range holds at least one site"),
    "staged 2026-09-10": ("consistent", "machine check: the two receipts the heading names are the last installers of every live "
                                        "tool file"),
    "faithful to": ("consistent", "machine check: every quoted OSHB note text in the notes block is byte-exact to pmarks notes_other"),
    "do not indicate": ("consistent", "byte-exact to pmarks notes_other (machine check)"),
    "BHS": ("consistent", "the note-class lines quote pmarks byte-exact or name classes without quotation marks; 'ketib/qere' in the "
                          "K/Q-note sentence agrees with the note text"),
    "33:20": ("consistent", "the MT 33:20 statement is unchanged except its quoted note, now byte-exact"),
    "maqaf": ("consistent", "the extract-is-maqaf-free lines agree with the ezek_lib selftest; the new skeleton line is confirmed by "
                            "machine check (skeleton deletes U+05BE without a space; POINTS covers U+05BE); ezek_lib's own docstring "
                            "stays wrong as the recorded T5-07 debt"),
    "skeleton": ("consistent", "the frame-spine heading uses 'skeleton' for the seam skeleton; the encoding notes agree with the new "
                               "maqaf line"),
    "MARKISH": ("consistent", "the W6 gate is check_marks.letter_absences: a MARKISH_CTX word within 60 characters either side"),
    "no pe or samekh": ("consistent", "the same row; rule 3's letter-name absence form"),
    "negator": ("consistent", "the check_marks row separates the negator before a K/Q token (W2, W5) from the closed-set denial "
                              "after it (T4-03), which rule 4 applies as kq_negation(...) or denied_after(...)"),
}
T5_PHRASES_NOTE = ("T5 reviewed 84 statements over its 17 key phrases at 9771c440 (ezek_toolkit_install_review_T5.json toolkit_md). "
                   "Every line this edit does not touch is byte-identical to the file T5 reviewed (diffs/Ezek__tools__TOOLKIT.md.diff); "
                   "the lines it touches and their siblings are reviewed below.")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


if OUT.exists():
    raise SystemExit("ABORT: %s exists; a landed proposal is never replaced" % OUT)
run = json.loads((ROOT / "stage_run.json").read_text(encoding="utf-8"))
V_STG, TK_STG = ST / "campaign" / "_cure_verification.py", ST / "Ezek" / "tools" / "TOOLKIT.md"
tk_lines = TK_STG.read_text(encoding="utf-8").splitlines()
statements, seen = [], set()
for phrase, (verdict, why) in REVIEW.items():
    for i, line in enumerate(tk_lines):
        if phrase.lower() in line.lower() and (i + 1, phrase) not in seen:
            seen.add((i + 1, phrase))
            statements.append({"line": i + 1, "phrase": phrase, "text": line, "verdict": verdict, "why": why})
distinct_lines = sorted({s["line"] for s in statements})
sibling = {"schema": "m8_sibling_sweep.v1", "book": "Ezek", "artifact": "tools/TOOLKIT.md", "artifact_sha256_staged": sha(TK_STG),
           "ordered_by": "ezek_controlling_rulings_a1#e6 ruling T5-TOOLKIT-DOCS (R6 sibling sweep over the whole file)",
           "swept_by": "orchestrator (claude-opus-5) under OW-11; T6 re-runs it at the installed digest",
           "key_phrases": ["T5's 17 key phrases (ezek_toolkit_install_review_T5.json toolkit_md.sibling_sweep.key_phrases)",
                           "closed set", "NFD-only", "ranges expanded", "staged 2026-09-10", "faithful to", "do not indicate", "maqaf"]
                          + [p for p in REVIEW if p not in ("closed set", "ranges expanded", "staged 2026-09-10", "faithful to", "do not indicate", "maqaf")],
           "t5_prior_review": T5_PHRASES_NOTE, "statements_reviewed": len(distinct_lines), "statements": statements,
           "contradictions": [s for s in statements if s["verdict"] != "consistent"],
           "machine_checks": run["machine_checks"]}
ev = run["existing_vectors"]
disc = run["tf3_vectors_summary"]
rc = run["real_claims"]
dc = run["draft_claims"]
gate = {
    "verifier_selftest_green": run["verifier_selftest_staged"]["verdict"] == "GREEN" and run["verifier_selftest_staged"]["failed"] == 0,
    "existing_vectors_keep_expectation_except_the_ruled_rename": ev["all_present_and_ok"] and
        {k: (v["installed_expected"], v["staged_expected"]) for k, v in ev["expectation_changed"].items()} == RENAMED,
    "tf3_vectors_all_pass_on_staged": disc["staged_all_ok"],
    "new_refusals_discriminating": disc["required_discriminating_all_fail_on_installed"] and not disc["required_missing"],
    "real_claims_green_before_and_after": all(v["verdict"] == "GREEN" for lab in ("installed", "staged") for v in rc[lab].values()),
    "draft_claims_green_all_accepted_on_staged": dc["staged"]["verdict"] == "GREEN" and dc["staged"]["accepted"] == 6 and dc["staged"]["refused"] == 0,
    "toolkit_selfcheck_green": run["toolkit_selfcheck"]["verdict"] == "GREEN" and run["toolkit_selfcheck"]["checks"] == run["toolkit_selfcheck"]["passed"],
    "machine_checks_hold": (run["machine_checks"]["note_quotes_byte_exact"]["all_in_pmarks_notes_other"]
                            and all(run["machine_checks"]["closed_set"].values()) and run["machine_checks"]["w6_gate_60_characters"]
                            and run["machine_checks"]["t4_03_later_denial_in_check_marks_rule_4"]
                            and run["machine_checks"]["skeleton_deletes_maqaf"]["deleted_without_space"]
                            and run["machine_checks"]["heading_receipts_are_the_last_installers_of_every_live_file"]),
    "staged_digests_reproduced": sha(V_STG) == run["staged_digests"]["campaign/_cure_verification.py"] and sha(TK_STG) == run["staged_digests"]["tools/TOOLKIT.md"],
    "no_sibling_sweep_contradiction": not sibling["contradictions"],
}
if not all(gate.values()):
    print(json.dumps({"gate": gate}, ensure_ascii=False, indent=1))
    raise SystemExit("ABORT: gate failed; nothing landed")
g = subprocess.run([sys.executable, str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek", "--target", str(OUT / "manifest.json")],
                   capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
if g.returncode != 0:
    raise SystemExit("ABORT: the landing target is pinned:\n" + g.stdout)
for d in ("staged/campaign", "diffs", "scripts", "runs"):
    (OUT / d).mkdir(parents=True, exist_ok=False)
files = {}
for name, stg, inst in (("campaign/_cure_verification.py", V_STG, SP / "campaign" / "_cure_verification.py"),
                        ("TOOLKIT.md", TK_STG, EZ / "tools" / "TOOLKIT.md")):
    dst = OUT / "staged" / name
    shutil.copyfile(stg, dst)
    diff_src = ROOT / "diffs" / ("campaign__cure_verification.py.diff" if name.startswith("campaign/") else "Ezek__tools__TOOLKIT.md.diff")
    dp = OUT / "diffs" / diff_src.name
    shutil.copyfile(diff_src, dp)
    files[name] = {"installed_sha256": sha(inst), "staged_sha256": sha(dst), "staged_path": "Ezek/proposals/%s/staged/%s" % (BATCH, name),
                   "diff_vs_installed": "Ezek/proposals/%s/diffs/%s" % (BATCH, dp.name), "diff_lines": dp.read_text(encoding="utf-8").count("\n")}
for s in SCRIPTS:
    shutil.copyfile(ROOT / s, OUT / "scripts" / s)
shutil.copyfile(ROOT / "stage_run.json", OUT / "runs" / "stage_run.json")
shutil.copyfile(ROOT / "sibling_sweep_candidates.json", OUT / "runs" / "sibling_sweep_candidates.json")
shutil.copyfile(ROOT / "draft_claims_tf3.jsonl", OUT / "draft_claims_tf3.jsonl")
(OUT / "sibling_sweep.json").write_text(json.dumps(sibling, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
manifest = {
    "schema": "m8_tool_edit_proposal.v1", "book": "Ezek", "batch": BATCH, "built": datetime.now(timezone.utc).isoformat(),
    "built_by": "orchestrator (claude-opus-5) under OW-11; executes a ruling, never rules",
    "status": ("STAGED - INSTALL PRE-AUTHORIZED by ezek_controlling_rulings_a1#e6 ruling T5-SEQUENCE: every gate holds. Nothing is "
               "installed by this landing."),
    "ordered_by": "ezek_controlling_rulings_a1#e6 rulings T5-VERIFIER, T5-TOOLKIT-DOCS, T5-SEQUENCE",
    "builds_on_installed": {"receipt": "SP/campaign/receipts/ezek_tools_install_toolfix2_batch3.json"},
    "touches_no_validator_suite_member": True,
    "content": {
        "T5-VERIFIER": "campaign/_cure_verification.py: (1) integer machine results and the passing test; (2) the ACCEPT/REFUSE checker "
                       "verdict; (3) normalized, both-field distinctness; (4) stripped cure ids, anchored every-pair ORDERED_BY, ratify "
                       "verbs only when the ruling orders the retirement, and the renamed classification; (5) the vectors",
        "T5-TOOLKIT-DOCS": "tools/TOOLKIT.md: (1) the normalizer row; (2) the puncta rule; (3) the closed set with its pointer to the "
                           "code; (a) the heading; (b) the check_marks row; (c) the quoted OSHB note texts byte-exact; (d) the "
                           "skeleton/maqaf line"},
    "files": files,
    "tests": {"verifier_selftest": run["verifier_selftest_staged"], "verifier_selftest_installed": run["verifier_selftest_installed"],
              "existing_vectors": ev, "tf3_vectors": run["tf3_vectors"], "tf3_vectors_summary": disc,
              "toolkit_selfcheck": run["toolkit_selfcheck"]},
    "real_claims_before_and_after": rc,
    "supersession_classes_moved": ("every live supersession record moved from 'ruling_names_retired_cure' to "
                                   "'ruling_orders_retirement', the class T5-VERIFIER (4) renames: each ordering ruling's decision or orders "
                                   "place the retired id within 200 characters of supersession/supersede/retire. EZEK-P0-CURE-toolkit-v2's "
                                   "record is among them (#e6 T5-VERIFIER (6)); its SUPERSEDED verdict does not move"),
    "draft_claims": {"path": "Ezek/proposals/%s/draft_claims_tf3.jsonl" % BATCH, "sha256": sha(OUT / "draft_claims_tf3.jsonl"),
                     "ids": dc["ids"], "on_staged_verifier": dc["staged"], "on_installed_verifier": dc["installed"],
                     "append_rule": "#e6 T5-SEQUENCE claims (1): appended to ezek_cure_claims_toolkit_repair.v1.jsonl only after this batch "
                                    "installs, in one append followed by one verifier run under --rulings --require-rulings",
                     "drafting_note": ("each claim binds three verification entries to the file's own digest: the receipt's zone tests, "
                                       "its ezek_lib selftest, and T5's suite-parity comparison. The comparison carries integer counts "
                                       "(members compared JSON-identical) and no exit, because the suite's own exit is 1 on the enumerated "
                                       "HARD set; that is recorded as suite_exit (#e6 unresolved_uncertainty[3] leaves this drafting to "
                                       "the orchestrator)")},
    "sibling_sweep": {"path": "Ezek/proposals/%s/sibling_sweep.json" % BATCH, "sha256": sha(OUT / "sibling_sweep.json"),
                      "statements_reviewed": sibling["statements_reviewed"], "contradictions": len(sibling["contradictions"])},
    "runs": {n: sha(OUT / "runs" / n) for n in ("stage_run.json", "sibling_sweep_candidates.json")},
    "gate": gate,
    "scripts": {s: sha(OUT / "scripts" / s) for s in SCRIPTS},
}
(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"landed": str(OUT), "manifest_sha256": sha(OUT / "manifest.json"), "gate": gate,
                  "files": {n: {"installed": f["installed_sha256"][:16], "staged": f["staged_sha256"][:16]} for n, f in files.items()},
                  "sibling_sweep": manifest["sibling_sweep"]}, ensure_ascii=False, indent=1))
