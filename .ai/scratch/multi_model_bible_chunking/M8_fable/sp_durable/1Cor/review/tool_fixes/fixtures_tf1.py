"""TF-1 fixtures (1Cor controlling ruling S1-07, cor_controlling_rulings_r1_a1#e1): the --book-index mode of
1Cor/writer_lanes/_validate_writer_part_1cor.py.

Compares a CANDIDATE validator source (--candidate; default the installed one) with the BASELINE source (--baseline;
the pre-TF-1 bytes, pinned by --baseline-sha), both run as if installed (via _exec_as.py), on slices of the installed
combined draft written to --work (never to SP; E-67). Cases:
  T1 every slice W1..W6 goes GREEN in --book-index mode;
  T2 in the default mode the candidate's output is byte-identical to the baseline's on every slice (the default mode is
     unchanged), and W2..W6 go RED with only chunk_index_in_book problems, as S1 measured;
  T3 on part-local re-indexed slices (1..k) both go GREEN and their outputs are byte-identical;
  T4 one index gap, one repeat and a whole-slice offset of +1 each go RED in --book-index mode, naming chunk_index_in_book.
Prints one JSON result; ALL_PASS gates the install.
usage: fixtures_tf1.py --baseline FILE --baseline-sha SHA --work DIR [--candidate FILE] [--book-dir DIR]
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
env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
ap = argparse.ArgumentParser()
ap.add_argument("--baseline", required=True)
ap.add_argument("--baseline-sha", required=True)
ap.add_argument("--work", required=True)
ap.add_argument("--candidate")
ap.add_argument("--book-dir", default=str(HERE.parents[1]))  # staging runs point this at SP/1Cor
a = ap.parse_args()
BK = Path(a.book_dir)
INST = BK / "writer_lanes" / "_validate_writer_part_1cor.py"
COMB = BK / "writer" / "draft_rows_combined.jsonl"
a.candidate = a.candidate or str(INST)
if hashlib.sha256(Path(a.baseline).read_bytes()).hexdigest() != a.baseline_sha:
    raise SystemExit("REFUSED: the baseline source is not at --baseline-sha")
W = Path(a.work)
W.mkdir(parents=True, exist_ok=True)
EXEC = HERE / "_exec_as.py"


def run(src, rows, part, *extra):
    p = subprocess.run([sys.executable, "-B", str(EXEC), str(src), str(INST), str(rows), "--part", part, *extra],
                       capture_output=True, text=True, encoding="utf-8", env=env)
    return p.stdout, json.loads(p.stdout) if p.stdout.strip().startswith("{") else {"verdict": "ERROR", "err": p.stderr[-400:]}


def write(name, rows):
    p = W / name
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")
    return p


rows = [json.loads(x) for x in COMB.read_text(encoding="utf-8").splitlines() if x.strip()]
res, ok = {}, True
for n in range(1, 7):
    part = "W%d" % n
    sl = [r for r in rows if r.get("writer_part") == part]
    f = write("slice_%s.jsonl" % part, sl)
    _, j1 = run(a.candidate, f, part, "--book-index")
    t1 = j1.get("verdict") == "GREEN"
    o0, j0 = run(a.baseline, f, part)
    oc, jc = run(a.candidate, f, part)
    only_idx = all("chunk_index_in_book" in p for p in jc.get("problems", []))
    t2 = o0 == oc and (jc.get("verdict") == ("GREEN" if n == 1 else "RED")) and only_idx
    loc = [dict(r, chunk_index_in_book=i) for i, r in enumerate(sl, 1)]
    g = write("slice_%s_partidx.jsonl" % part, loc)
    p0, k0 = run(a.baseline, g, part)
    pc, kc = run(a.candidate, g, part)
    t3 = p0 == pc and k0.get("verdict") == "GREEN" and kc.get("verdict") == "GREEN"
    res[part] = {"rows": len(sl), "T1_book_index_green": t1, "T2_default_identical_and_as_measured": t2,
                 "T2_default_verdict": jc.get("verdict"), "T3_partidx_identical_green": t3,
                 "first_index": (j1.get("index_mode") or {}).get("first_index")}
    ok = ok and t1 and t2 and t3
sl = [r for r in rows if r.get("writer_part") == "W3"]
bad = {"gap": [dict(r, chunk_index_in_book=r["chunk_index_in_book"] + (1 if i >= 2 else 0)) for i, r in enumerate(sl)],
       "repeat": [dict(r, chunk_index_in_book=sl[0]["chunk_index_in_book"]) if i == 1 else r for i, r in enumerate(sl)],
       "offset": [dict(r, chunk_index_in_book=r["chunk_index_in_book"] + 1) for r in sl]}
for k, v in bad.items():
    _, j = run(a.candidate, write("bad_W3_%s.jsonl" % k, v), "W3", "--book-index")
    t4 = j.get("verdict") == "RED" and any("chunk_index_in_book" in p for p in j.get("problems", []))
    res["T4_" + k] = {"verdict": j.get("verdict"), "red_on_index": t4}
    ok = ok and t4
print(json.dumps({"fixture": "TF-1 (S1-07)", "candidate": a.candidate,
                  "candidate_sha256": hashlib.sha256(Path(a.candidate).read_bytes()).hexdigest(),
                  "baseline_sha256": a.baseline_sha, "combined_sha256": hashlib.sha256(COMB.read_bytes()).hexdigest(),
                  "cases": res, "verdict": "ALL_PASS" if ok else "FAIL"}, ensure_ascii=False))
