"""Land the TOOLFIX-2 re-stage of ezek_controlling_rulings_a1#e5 ruling INSTALL-TF2-1 DURABLY as SP/Ezek/proposals/toolfix2_batch3.
INSTALL-TF2-1 pre-authorizes the install when its gates hold. This lander recomputes those gates from the stage outputs on disk
and records the orchestrator's hand review of every delta outside the ruling's expected set. Nothing is installed here.

GATES (all must hold to land as install-ready):
  (2) - tests GREEN; the ezek_lib selftest, toolkit selfcheck and verifier selftest GREEN;
      - the verifier over both real claims files GREEN, with every supersession classed ruling_names_retired_cure;
      - no failure outside sections 10b and 10c on the installed tools or on batch1's staged tools;
      - each vector the ruling names DISCRIMINATING fails on a base where its arm is absent;
      - staged digests reproduced.
  (3) - the HARD lists equal the enumerated set: citation_sweep's 10 problems, and the normalizer's 8 distinct runs with 9 listed;
      - every expected check_marks removal is present and the three keeps hold;
      - every other check_marks delta is hand-reviewed below, and none is a new class;
      - web_quotes stays at its 10 e15d flags, unchanged;
      - no suite list other than mark_symmetry.flags and register.flags moved against batch1.

WRITES staged/ (and staged/campaign), diffs/ against the installed files, scripts/, runs/ (the stage run and both suite
reports), corpus_impact.json, hand_review.json and manifest.json. The in-flight pin guard runs first. The batch directory is
never replaced.

Usage: land_tf2c_proposal.py --batch toolfix2_batch3"""
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
ROOT = SCR / "stage_tf2c"
ST = ROOT / "sp_durable"
B1 = EZ / "proposals" / "toolfix2_batch1"
TOOL_FILES = ("citation_sweep.py", "check_marks.py", "_adapt_zone_tools_ezek.py", "_test_zone_tools_ezek.py", "TOOLKIT.md",
              "ezek_lib.py", "normalize_hebrew_in_json.py", "check_register.py", "check_web_quotes.py")
SCRIPTS = ("stage_tf2c_patch.py", "diag_tf2c_strays.py", "land_tf2c_proposal.py")
SUITE_TF2C = ST / "Ezek" / "repair" / "suite_tf2c" / "rows.jsonl.validator_report.json"
SUITE_B1 = SCR / "stage_tf2c_base_batch1_staged" / "sp_durable" / "Ezek" / "repair" / "suite_b1" / "rows.jsonl.validator_report.json"
NAMED_DISCRIMINATING = {"cs_e5_nc_proclitic_stripped_label_refused": "fails_on_installed", "cm_e5_w1_mark_before_onset_ok": "fails_on_batch1_staged",
                        "cm_e5_w2_distant_negator_silent": "fails_on_batch1_staged", "cm_e5_w5_negator_heads_list_ok": "fails_on_batch1_staged",
                        "cm_e5_w6_no_pe_or_samekh_true_silent": "fails_on_batch1_staged"}
HAND_REVIEW = {
    "schema": "m8_orchestrator_hand_review.v1", "book": "Ezek", "batch": "toolfix2_batch3",
    "ordered_by": "ezek_controlling_rulings_a1#e5 ruling INSTALL-TF2-1 (3): any other check_marks delta is listed and hand-reviewed; a new class "
                  "returns to the controlling lane before install, a same-class stray is listed and proceeds",
    "reviewer": "orchestrator (claude-opus-5) under OW-11; a hand review of deltas, not a ruling",
    "check_marks_strays": [
        {"row": "P02-006", "rule": "kq_claim", "delta": "removed (verse_cited Ezek.10.9)",
         "text": "No parashah, K/Q, paseq or editorial-note disclosure applies anywhere in 10:9-17; that absence is itself disclosed.",
         "bytes": "pmarks kq: no key in Ezek.10.9-10.17",
         "verdict": "correct removal of the W5 class: a true absence claim that batch1 read as a positive claim because the comma cut its negator. "
                    "FLAGS-TF2-1 listed three W5 rows (P10-003, P10-005, P10-006) and this fourth is the same shape.",
         "new_class": False},
        {"row": "P02-020", "rule": "false_kq_absence_claim", "delta": "removed twice where FLAGS-TF2-1 expected once",
         "text": "the Noah/Daniel/Job triad is the site of an undisclosed-by-L-and-BHS Qere adaptation, on top of the ordinary ketiv/qere note also "
                 "recorded at each verse (the sentence stands in two refs entries, oshb:Ezek.14.14 and oshb:Ezek.14.20)",
         "bytes": "pmarks kq present at Ezek.14.14 and Ezek.14.20; the sentence discloses them",
         "verdict": "correct removal of the W2 class. batch1's clause-wide negation read the 'do not indicate' of the quoted apparatus note, in the "
                    "same comma clause, as negating the Qere token. The sentence occurs in two refs entries, so batch1 carried two identical "
                    "flags and the ruling's count saw one.",
         "new_class": False},
        {"row": "P05-003", "rule": "kq_claim", "delta": "added (verse_cited Ezek.22.23)",
         "text": "No paseq or K/Q sites inside 22:23-31.",
         "bytes": "pmarks kq: no key in Ezek.22.23-22.31, so the claim is true",
         "verdict": "a false positive at the W2 adjacency limit the ruling names (unresolved_uncertainty[1]: a two-word negation such as 'no "
                    "intervening or later K/Q' stays on the positive-claim path). The ruling expected such a claim to fall silent; this one names "
                    "a verse range, so the positive path flags it. It is the same flag class as the W5 misreads (a true K/Q absence claim read "
                    "as a positive claim), in a FLAGS member with no HARD effect. Listed for T5 as the widening the ruling anticipates: a "
                    "negator heading an or-coordination ('no A or K/Q'), with vectors both ways.",
         "new_class": False},
        {"row": "P09-002", "rule": "false_mark_absence_claim", "delta": "added (scope named; Ezek.37.28 SAMEKH)",
         "text": "Rejected: no samekh or pe mark falls anywhere inside 37.15-28",
         "bytes": "pmarks marks: none at Ezek.37.15-37.27; SAMEKH at Ezek.37.28, which the same row discloses as 'the samekh closing it at 37.28'",
         "verdict": "W6 reads the letter-name absence phrase as ruled, and the one marked key is the named range's closing bound. That is the "
                    "persisting class FLAGS-TF2-1 records ('between X and Y' with the bounds themselves marked), reached through the W6 form. "
                    "The claim is true of the interior. Listed for T5 with that class's candidate fix (scope X+1..Y-1, here 'inside X-Y').",
         "new_class": False}],
    "register": {"verdict": "every addition is the S1-05 class the widened arms target",
                 "p10-10": "'one of the better-evidenced rows' is row talk of the same S1-05 class (a positional or dataset reference to rows), though "
                           "not among S1's quoted phrasings; like the others it is a CWO-EZ-14 input"},
    "discrimination": {
        "cm_e5_w1_mark_before_onset_ok": "fails on batch1's staged tools, as ruled, but passes on the INSTALLED tools. So the ruling's 'the "
                                         "installed and batch1 tools both flag it' does not hold for this vector. The installed rule 1 reads a "
                                         "120-character window that crosses into the row's span field ('Ezek.12.17-Ezek.12.20'), finds 12.20 "
                                         "and its PE, and stays silent for that reason (the cross-field leak batch1's field_bounds closed). W1's "
                                         "acceptance does not exist on the installed tools, so batch1 is the base where the arm is absent, and "
                                         "gate (2) holds."},
    "normalizer_equality": "batch1's corpus_impact lists hebrew_normalize_dryrun.defects.added as a set (8 distinct). The staged list carries 9 "
                           "(P03-005's run twice), as NEWCLASS-TF2-1 states, so equality is tested as the same distinct set with 9 listed.",
    "implementation_readings_for_T5": [
        "W2's negators are check_marks' NEG_WORD set, and two negators standing together cancel (T1-03, as puncta_negated does).",
        "T4-03's closed-set denial after the token still makes it an absence claim; the ruling replaced only the backward clause-wide negation.",
        "W2's exclusivity scope reads 'named anywhere in the row' over every string field check_marks joins (the span field included) and the "
        "refs; a written range names its two ends.",
        "W5 carries no exclusivity narrowing, because the ruling names none.",
        "W6 enters rule 3 as ABSENCE does: a named verse, range or chapter is checked there, and a phrase naming none is span-scoped.",
        "Rule 1's W6 skip is clause-level, as the existing ABSENCE skip is.",
        "The ruling's example vector names 'more' and 'second' among the exclusivity words, and KQ_EXCLUSIVE carries exactly other, further, "
        "additional, second and more."],
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def jkeys(xs):
    return sorted(json.dumps(x, sort_keys=True, ensure_ascii=False) for x in xs)


ap = argparse.ArgumentParser()
ap.add_argument("--batch", required=True)
a = ap.parse_args()
OUT = EZ / "proposals" / a.batch
if OUT.exists():
    raise SystemExit("ABORT: %s exists; a landed proposal is never replaced" % OUT)
run = json.loads((ROOT / "stage_run.json").read_text(encoding="utf-8"))
impact = json.loads((ROOT / "corpus_impact.json").read_text(encoding="utf-8"))
b1_impact = json.loads((B1 / "corpus_impact.json").read_text(encoding="utf-8"))
R3 = json.loads(SUITE_TF2C.read_text(encoding="utf-8"))
R1 = json.loads(SUITE_B1.read_text(encoding="utf-8"))
exp_cs = b1_impact["lists"]["citation_sweep.problems"]["added"]
exp_norm = b1_impact["lists"]["hebrew_normalize_dryrun.defects"]["added"]
n3, n1 = R3["hebrew_normalize_dryrun"].get("defects", []), R1["hebrew_normalize_dryrun"].get("defects", [])
disc, vec, cm = run["discrimination"], run["vectors_10c"], impact["check_marks"]
strays = sorted({(x[0], x[1]) for x in cm["removed_not_expected"] + cm["added"]})
reviewed = sorted((h["row"], h["rule"]) for h in HAND_REVIEW["check_marks_strays"])
gate = {
    "tests_green": run["tests"].get("verdict") == "GREEN",
    "ezek_lib_selftest_green": run["ezek_lib_selftest"].get("verdict") == "GREEN",
    "toolkit_selfcheck_green": run["toolkit_selfcheck"].get("verdict") == "GREEN",
    "verifier_selftest_green": run["verifier_selftest"].get("verdict") == "GREEN",
    "verifier_real_claims_green_and_classed": all(v.get("verdict") == "GREEN" and all(c.get("ordered_by_class") == "ruling_names_retired_cure"
                                                                                     for c in v.get("supersession_classes") or [])
                                                  for v in run["verifier_real_claims"].values()),
    "no_failure_outside_10b_10c": all(not disc[b].get("error") and not disc[b]["failed_outside_10b_10c"] for b in ("installed", "batch1_staged")),
    "named_vectors_discriminate": all(vec.get(v, {}).get(k) for v, k in NAMED_DISCRIMINATING.items()),
    "staged_digests_reproduced": all(sha((ST / n) if n.startswith("campaign/") else (ST / "Ezek" / "tools" / n)) == d for n, d in run["staged_digests"].items()),
    "hard_citation_sweep_equals_enumerated_10": jkeys(R3["citation_sweep"].get("problems", [])) == jkeys(exp_cs) and len(exp_cs) == 10,
    "hard_normalizer_equals_enumerated": set(jkeys(n3)) == set(jkeys(exp_norm)) == set(jkeys(n1)) and len(set(jkeys(exp_norm))) == 8 and len(n3) == 9,
    "check_marks_expected_removals_present": cm["expected_not_removed"] == [],
    "check_marks_keeps_hold": cm["keeps_hold"],
    "check_marks_strays_all_hand_reviewed_same_class": strays == reviewed and not any(h["new_class"] for h in HAND_REVIEW["check_marks_strays"]),
    "web_quotes_e15d_stays_at_10_unchanged": impact["web_quotes"]["stays_at_10"] and impact["web_quotes"]["all_web_quotes_flags_unchanged"],
    "only_marks_and_register_lists_moved": set(impact["lists_moved_vs_batch1"]) <= {"mark_symmetry.flags", "register.flags"},
}
if not all(gate.values()):
    print(json.dumps({"gate": gate, "strays": strays, "reviewed": reviewed}, ensure_ascii=False, indent=1))
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
    b1f = json.loads((B1 / "manifest.json").read_text(encoding="utf-8"))["files"].get(name, {})
    files[name] = {"installed_sha256": sha(inst), "batch1_staged_sha256": b1f.get("staged_sha256"), "staged_sha256": sha(dst),
                   "changed_from_batch1": sha(dst) != b1f.get("staged_sha256"),
                   "staged_path": "Ezek/proposals/%s/staged/%s" % (a.batch, name),
                   "diff_vs_installed": "Ezek/proposals/%s/diffs/%s" % (a.batch, dp.name), "diff_lines": diff.count("\n")}
for s in SCRIPTS:
    shutil.copyfile(SCR / s, OUT / "scripts" / s)
shutil.copyfile(ROOT / "stage_run.json", OUT / "runs" / "stage_run.json")
shutil.copyfile(SUITE_TF2C, OUT / "runs" / "suite_tf2c.validator_report.json")
shutil.copyfile(SUITE_B1, OUT / "runs" / "suite_batch1_base.validator_report.json")
shutil.copyfile(ROOT / "corpus_impact.json", OUT / "corpus_impact.json")
(OUT / "hand_review.json").write_text(json.dumps(HAND_REVIEW, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
manifest = {
    "schema": "m8_tool_edit_proposal.v1", "book": "Ezek", "batch": a.batch, "built": datetime.now(timezone.utc).isoformat(),
    "built_by": "orchestrator (claude-opus-5) under OW-11; executes a ruling, never rules",
    "status": "STAGED - INSTALL PRE-AUTHORIZED by ezek_controlling_rulings_a1#e5 ruling INSTALL-TF2-1: gates (2) and (3) hold, and the four "
              "check_marks strays were hand-reviewed as same-class. Nothing is installed by this landing.",
    "ordered_by": "ezek_controlling_rulings_a1#e5 ruling INSTALL-TF2-1 (re-stage of ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2)",
    "builds_on_installed": {"receipt": "SP/campaign/receipts/ezek_tools_install_t4fix_batch2.json"},
    "carries_batch1_unchanged": {"manifest": "Ezek/proposals/toolfix2_batch1/manifest.json", "manifest_sha256": sha(B1 / "manifest.json"),
                                 "how": "batch1's staged bytes were copied, each verified against its manifest digest, and then amended"},
    "supersedes_proposal": {"batch": "toolfix2_batch1", "why": "install-blocked on the returned class; carried here unchanged plus #e5's amendments; never installed. "
                                                              "toolfix2_batch2 is the superseded pre-#e4 landing and is not revived"},
    "content_per_install_tf2_1": {
        "carried_from_batch1": "S1-07, S1-06, S1-10, S1-19, S1-05, S1-22, the TOOLKIT.md rows and the selftest fixture, unchanged",
        "NEWCLASS-TF2-1": "no rule change; three citation_sweep vectors with the Hebrew derived from MT 12:20 and 17:12 at run time",
        "FLAGS-TF2-1": "check_marks through the adapter: W1 (rule 1 accepts a mark of the claimed type after N-1); W2 as amended (rule 4 negation "
                       "by kq_negation; 'no other K/Q' scoped to the span's kq keys the row names nowhere); W5 (distribution across a short comma "
                       "list); W6 (the letter-name absence form in rules 1 and 3); the docstring and TOOLKIT.md's check_marks row",
        "REG-TF2-1": "check_register's former/prior/rows arms widened, with the 'rows of' lookahead and the 'previously ... as' arm; RED vectors and "
                     "GREEN controls; TOOLKIT.md's register sentence",
        "section_10c": "all new vectors; section 10b untouched"},
    "files": files,
    "tests": {"staged": {k: run["tests"].get(k) for k in ("checks", "passed", "verdict")}, "ezek_lib_selftest": run["ezek_lib_selftest"],
              "toolkit_selfcheck": run["toolkit_selfcheck"], "verifier_selftest": {k: run["verifier_selftest"].get(k) for k in ("vectors", "failed", "verdict")},
              "verifier_over_real_claims": run["verifier_real_claims"],
              "discrimination": {b: {k: disc[b][k] for k in ("checks", "passed")} | {"failed": len(disc[b]["failed"])} for b in disc},
              "vectors_10c": vec},
    "corpus_impact_condition_c": {"path": "Ezek/proposals/%s/corpus_impact.json" % a.batch, "against": impact["against"],
                                  "hard": {k: v for k, v in impact["hard"].items() if not k.startswith("summary")},
                                  "summaries": {"batch1_staged": impact["hard"]["summary_batch1"], "toolfix2_batch3": impact["hard"]["summary_tf2c"]},
                                  "check_marks": {k: cm[k] for k in ("removed", "added", "expected_not_removed", "removed_not_expected", "keeps_hold")},
                                  "register": {k: impact["register"][k] for k in ("batch1_flags", "tf2c_flags", "added_per_row", "removed_per_row")},
                                  "web_quotes": impact["web_quotes"], "lists_moved_vs_batch1": impact["lists_moved_vs_batch1"]},
    "hand_review": {"path": "Ezek/proposals/%s/hand_review.json" % a.batch, "sha256": sha(OUT / "hand_review.json")},
    "runs": {n: sha(OUT / "runs" / n) for n in ("stage_run.json", "suite_tf2c.validator_report.json", "suite_batch1_base.validator_report.json")},
    "gate": gate,
    "scripts": {s: sha(OUT / "scripts" / s) for s in SCRIPTS},
}
(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"landed": str(OUT), "manifest_sha256": sha(OUT / "manifest.json"), "gate": gate,
                  "files": {n: {"staged": f["staged_sha256"][:16], "changed_from_batch1": f["changed_from_batch1"]} for n, f in files.items()}},
                 ensure_ascii=False, indent=1))
