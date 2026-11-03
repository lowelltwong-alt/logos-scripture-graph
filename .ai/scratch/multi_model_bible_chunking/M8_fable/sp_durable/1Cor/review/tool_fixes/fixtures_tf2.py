"""TF-2 fixtures F1..F4 (1Cor controlling ruling S1-08, cor_controlling_rulings_r1_a1#e1): the licence-string segment
break in 1Cor/tools/ngram7.py.

Compares a CANDIDATE ngram7 source (--candidate; default the installed one) with the BASELINE source (--baseline; the
pre-TF-2 bytes, pinned by --baseline-sha), both run as if installed (via _exec_as.py). Inputs are built from the installed
combined draft and written to --work only (never to SP; E-67). Cases:
  F1 on the pinned 70-row draft: the candidate's gram set is the baseline's minus exactly the grams that touch a
     licence-string token (13601 -> 12939, 662 lost, 0 gained), and the offending set at gate 10 is unchanged;
  F2 on the draft with the S1-04 cure shape added to all 14 W5 rows (plain prose, then the two exact strings standing
     alone, appended to boundary_rationale; the W5 attribution wording varies, so it is appended, not substituted): the
     baseline gains offenders, every one touching a licence token; the candidate's offending set equals its F1 set;
  F3 ten rows carrying both exact strings plus one shared authored sentence stay RED on that sentence;
  F4 ten rows carrying the SALTED variant 'Robinson-Pierpont Byzantine Textform, Unlicense; SBLGNT, CC BY 4.0' are not
     stripped and stay RED on the variant's own grams.
Prints one JSON result; ALL_PASS gates the install.
usage: fixtures_tf2.py --baseline FILE --baseline-sha SHA --work DIR [--candidate FILE] [--book-dir DIR]
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
EXEC = HERE / "_exec_as.py"
env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
ap = argparse.ArgumentParser()
ap.add_argument("--baseline", required=True)
ap.add_argument("--baseline-sha", required=True)
ap.add_argument("--work", required=True)
ap.add_argument("--candidate")
ap.add_argument("--book-dir", default=str(HERE.parents[1]))  # staging runs point this at SP/1Cor
a = ap.parse_args()
BK = Path(a.book_dir)
INST = BK / "tools" / "ngram7.py"
COMB = BK / "writer" / "draft_rows_combined.jsonl"
a.candidate = a.candidate or str(INST)
if hashlib.sha256(Path(a.baseline).read_bytes()).hexdigest() != a.baseline_sha:
    raise SystemExit("REFUSED: the baseline source is not at --baseline-sha")
W = Path(a.work)
W.mkdir(parents=True, exist_ok=True)
S1, S2 = "Robinson-Pierpont Byzantine Textform (Unlicense)", "SBLGNT (CC BY 4.0)"
CURE = " Greek source: %s; %s." % ("Robinson-Pierpont Byzantine Textform (Unlicense)", "SBLGNT (CC BY 4.0)")  # prose under 7 tokens: the fixture plants no template of its own
SALTED = "Robinson-Pierpont Byzantine Textform, Unlicense; SBLGNT, CC BY 4.0"
LIC = {"robinson", "pierpont", "byzantine", "textform", "unlicense", "sblgnt", "cc"}


def touches(g):
    t = g.split()
    return bool(LIC & set(t)) or t[0] == "by"   # "by" is the last token of S2; a gram starting there touches it


def run(src, rows, *extra):
    p = subprocess.run([sys.executable, "-B", str(EXEC), str(src), str(INST), str(rows), "--gate", "10", *extra],
                       capture_output=True, text=True, encoding="utf-8", env=env)
    if not p.stdout.strip().startswith("{"):
        raise SystemExit("ERROR running %s: %s" % (src, p.stderr[-400:]))
    return json.loads(p.stdout)


def offenders(src, rows):
    d = run(src, rows, "--full-ids")
    return d["status"], {o["gram"]: o["row_ids"] for o in d["offending_7grams"]}


def write(name, rows):
    p = W / name
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")
    return p


rows = [json.loads(x) for x in COMB.read_text(encoding="utf-8").splitlines() if x.strip()]
res, ok = {}, True
# F1
g0, gc = run(a.baseline, COMB, "--dump-grams"), run(a.candidate, COMB, "--dump-grams")
lost, gained = set(g0) - set(gc), set(gc) - set(g0)
changed = [g for g in set(g0) & set(gc) if g0[g] != gc[g] and not touches(g)]
s0, o0 = offenders(a.baseline, COMB)
sc, oc = offenders(a.candidate, COMB)
f1 = (len(g0) == 13601 and len(gc) == 12939 and len(lost) == 662 and not gained and all(touches(g) for g in lost)
      and not changed and o0 == oc)
res["F1"] = {"baseline_grams": len(g0), "candidate_grams": len(gc), "lost": len(lost), "gained": len(gained),
             "lost_not_touching": sorted(g for g in lost if not touches(g))[:5], "row_sets_changed_untouched": len(changed),
             "offending_unchanged": o0 == oc, "offending": {g: len(v) for g, v in oc.items()}, "status": sc, "pass": f1}
ok = ok and f1
# F2
sim, n_rep = [], 0
for r in rows:
    if r.get("writer_part") == "W5":
        r = dict(r, boundary_rationale=r["boundary_rationale"] + CURE)
        n_rep += 1
    sim.append(r)
f = write("f2_sim_attr_w5.jsonl", sim)
sb, ob = offenders(a.baseline, f)
s2c, o2c = offenders(a.candidate, f)
extra = set(ob) - set(o0)
f2 = n_rep == 14 and bool(extra) and all(touches(g) for g in extra) and o2c == oc and s2c == "RED"
res["F2"] = {"w5_rows_cured": n_rep, "baseline_extra_offenders": len(extra), "candidate_offending_equals_F1": o2c == oc,
             "candidate_status": s2c, "pass": f2}
ok = ok and f2
# F3 / F4
words = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india", "juliet"]
shared = "the orchestrator plants this shared authored sentence across ten synthetic rows to test the gate."
f3 = [{"decision_id": "FX-F3-%02d" % i, "boundary_rationale": "Row %s opens a distinct test unit. Greek cited from %s and %s. %s"
       % (w, S1, S2, shared)} for i, w in enumerate(words, 1)]
s3, o3 = offenders(a.candidate, write("f3_both_strings_shared.jsonl", f3))
p3 = s3 == "RED" and any(not touches(g) and len(v) == 10 for g, v in o3.items())
res["F3"] = {"status": s3, "offenders": len(o3), "pass": p3}
f4 = [{"decision_id": "FX-F4-%02d" % i, "boundary_rationale": "Row %s opens a distinct test unit. Greek cited from %s per row."
       % (w, SALTED)} for i, w in enumerate(words, 1)]
s4, o4 = offenders(a.candidate, write("f4_salted.jsonl", f4))
p4 = s4 == "RED" and any(touches(g) and len(v) == 10 for g, v in o4.items())
res["F4"] = {"status": s4, "offenders": len(o4), "pass": p4}
ok = ok and p3 and p4
print(json.dumps({"fixture": "TF-2 (S1-08) F1..F4", "candidate": a.candidate,
                  "candidate_sha256": hashlib.sha256(Path(a.candidate).read_bytes()).hexdigest(),
                  "baseline_sha256": a.baseline_sha, "combined_sha256": hashlib.sha256(COMB.read_bytes()).hexdigest(),
                  "cases": res, "verdict": "ALL_PASS" if ok else "FAIL"}, ensure_ascii=False))
