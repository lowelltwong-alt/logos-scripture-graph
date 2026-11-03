"""TF-3 fixtures F1..F5 (1Cor controlling rulings cor_controlling_rulings_r2_a1#e1, S2-07 / CWO-1COR-04): the CWO04
addition to 1Cor/review/cwo_sweep_1cor.py.

Runs a CANDIDATE sweep source (--candidate; default the installed one) and the BASELINE source (--baseline; the pre-TF-3
bytes, pinned by --baseline-sha), both as if installed (via _exec_as.py). Inputs are read from SP; every file this
script makes goes to --work, and its result to --result (never to SP unless --result names the installed result path).
  F1 A, B and CWO02 are unchanged: on the FIXUP-1 applied rows, the pinned combined writer draft and the plant rows, the
     candidate's output minus its CWO04 key equals the baseline's output;
  F2 the W, P, DIS, PD2 and VERB pattern strings in the candidate equal the E2 predicate text, and the S1-01/S1-01b row
     list equals the ruling's;
  F3 on the FIXUP-1 applied rows the candidate reproduces the ruling's MEASURED baseline (106 hits in 52 rows; classes;
     support_use plus count_excess by part);
  F4 the 13 plants named in CWO-1COR-04 class as named (texts sliced from the named rows, Greek dropped);
  F5 two orchestrator-added plants: one count_excess per P mention after the first observed_substrate_signals P item in
     an S1-01 row, and a WEB mention with no paragraph is no hit.
Writes one JSON result; ALL_PASS gates the install.
usage: fixtures_tf3.py --baseline FILE --baseline-sha SHA --work DIR --result FILE [--candidate FILE]
"""
import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SP = Path("C:/wt/logos-t423-m8-fable/.ai/scratch/multi_model_bible_chunking/M8_fable/sp_durable")
REV = SP / "1Cor" / "review"
INSTALLED = REV / "cwo_sweep_1cor.py"
APPLIED = SP / "1Cor" / "fixup" / "draft_rows_fixup1_applied.jsonl"
COMBINED = SP / "1Cor" / "writer" / "draft_rows_combined.jsonl"
RULINGS = REV / "1cor_controlling_agent_rulings_E2.v1.json"
ap = argparse.ArgumentParser()
ap.add_argument("--baseline", required=True)
ap.add_argument("--baseline-sha", required=True)
ap.add_argument("--work", required=True)
ap.add_argument("--result", required=True)
ap.add_argument("--candidate", default=str(INSTALLED))
a = ap.parse_args()
sha = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731
work = Path(a.work)
work.mkdir(parents=True, exist_ok=True)
base_b, cand_b = Path(a.baseline).read_bytes(), Path(a.candidate).read_bytes()
if sha(base_b) != a.baseline_sha:
    sys.exit("REFUSED: baseline is at %s" % sha(base_b)[:12])
env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")


def run(src, rows, tag):
    out = work / ("out_%s.json" % tag)
    p = subprocess.run([sys.executable, "-B", str(HERE / "_exec_as.py"), str(src), str(INSTALLED), str(rows), "--out",
                        str(out)], capture_output=True, text=True, encoding="utf-8", env=env)
    if p.returncode:
        raise SystemExit("run %s failed: %s" % (tag, p.stderr[-400:]))
    return json.loads(out.read_text(encoding="utf-8"))


PLANTS = [  # (plant id, source named in CWO-1COR-04, field, text, expected [(predicate, class)])
    ("PLANT-01", "W1-012 co-location", "boundary_rationale",
     "At 4:1 a new account of how apostles should be regarded begins, and the WEB paragraph at 4:1 falls there too.",
     [("W", "support_use")]),
    ("PLANT-02", "W4-001 absence", "boundary_rationale",
     "This close seam rests on the text alone: there is no RP pilcrow and no WEB paragraph start at 11:13, and no device "
     "from the device listing stands there (EXTRACTED), so the evidence for it is one-sided", [("W", "support_use")]),
    ("PLANT-03", "W5-010 rival", "strongest_rejected_alternative",
     "A cut at 14:15, where WEB opens a paragraph and the question is asked, would split the instruction from its "
     "resolution.", [("W", "support_use")]),
    ("PLANT-04", "W4-001 ref 'agrees'", "boundary_evidence_refs",
     "rp:1Cor.11.2 [WARRANT-onset:near] (praise opening, with tradition vocabulary; RP pilcrow at 11:2 agrees and "
     "decides nothing)", [("P", "support_use")]),
    ("PLANT-05", "W1-003 'marks the onset'", "boundary_rationale",
     "The RP pilcrow at 1:10 marks the onset, and the RP pilcrow at 1:18 stands after that turn.",
     [("P", "support_use")]),
    ("PLANT-06", "W3-008 chapter division", "strongest_rejected_alternative",
     "The chapter division and the WEB paragraph start at 11:1 point to a seam at 10:33/11:1 that would attach the "
     "imitation call (rp:1Cor.11.1) to the praise of 11:2.", [("W", "support_use")]),
    ("PLANT-07", "W2-001 'not weighed'", "boundary_rationale",
     "WEB paragraph starts at 5:1 and 5:6 coincide with both seams and are not weighed (EXTRACTED).",
     [("W", "disclosure_only")]),
    ("PLANT-08", "W4-003 'decides nothing'", "boundary_rationale",
     "the gar link is disclosed here, the WEB paragraph start at 11:23 decides nothing, and confidence stays medium.",
     [("W", "disclosure_only")]),
    ("PLANT-09", "W2-001 oss 'formatting'", "observed_substrate_signals",
     "WEB paragraph start at 5:1 and 5:6 (formatting, not weighed)", [("W", "disclosure_only")]),
    ("PLANT-10", "W2-003 informs", "boundary_rationale",
     "RP pilcrow at 5:9 coincides with this onset (EXTRACTED) and informs without deciding.",
     [("P", "informs_compliant")]),
    ("PLANT-11", "W5-004 oss item", "observed_substrate_signals", "WEB paragraph at 12:27", [("W", "location_only")]),
    ("PLANT-12", "W4-001 oss item", "observed_substrate_signals", "WEB paragraph starts at 11:2 and 11:11",
     [("W", "location_only")]),
    ("PLANT-13", "a [DISCLOSURE-mark] tag", "boundary_evidence_refs", "rp:1Cor.5.10 [DISCLOSURE-mark] list of vices", []),
]
LIST_FIELDS = ("observed_substrate_signals", "boundary_evidence_refs")
plant_rows = [{"decision_id": pid, f: ([t] if f in LIST_FIELDS else t)} for pid, _, f, t, _ in PLANTS]
plant_rows += [  # F5, orchestrator-added
    {"decision_id": "W5-002", "observed_substrate_signals": ["RP pilcrow at 12:4"],
     "boundary_rationale": "The RP pilcrow at 12:4 is located."},
    {"decision_id": "PLANT-15", "boundary_rationale": "The WEB text at 4:1 is cited for the gloss only."},
]
prow = work / "plant_rows.jsonl"
prow.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in plant_rows), encoding="utf-8", newline="\n")
cases = {}

# F1
f1 = {}
for tag, rows in (("applied", APPLIED), ("combined", COMBINED), ("plants", prow)):
    b, c = run(a.baseline, rows, "base_" + tag), run(a.candidate, rows, "cand_" + tag)
    f1[tag] = {"equal_without_CWO04": {k: v for k, v in c.items() if k != "CWO04"} == b,
               "baseline_keys": sorted(b), "candidate_keys": sorted(c)}
cases["F1"] = {"pass": all(v["equal_without_CWO04"] and v["candidate_keys"] == sorted(v["baseline_keys"] + ["CWO04"])
                           for v in f1.values()), "inputs": f1}

# F2
pred = next(o for o in json.loads(RULINGS.read_text(encoding="utf-8"))["corpus_wide_orders"]
            if o["id"] == "CWO-1COR-04")["predicate"]


def between(s, lo, hi):
    i = s.index(lo) + len(lo)
    return s[i:s.index(hi, i)]


ruled = {"W4": between(pred, "W = ", " ; P = "), "P4": between(pred, " ; P = ", " ; DIS = "),
         "DIS4": between(pred, " ; DIS = ", " ; PD2 = "), "PD2": between(pred, " ; PD2 = ", " ; VERB = "),
         "VERB4": between(pred, " ; VERB = ", ". A W hit")}
got = {}
for node in ast.parse(cand_b.decode("utf-8")).body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        n = node.targets[0].id
        if n in ruled and isinstance(node.value, ast.Call) and node.value.args:
            got[n] = node.value.args[0].value
        if n == "S1_01_ROWS":
            got[n] = sorted(ast.literal_eval(node.value))
ROW_TEXT = "In rows W5-001, 002, 003, 010, 011, 012, 013, 014 and W6-002, 003, 008, 011, 012"
want_rows = sorted(["W5-001", "W5-002", "W5-003", "W5-010", "W5-011", "W5-012", "W5-013", "W5-014",
                    "W6-002", "W6-003", "W6-008", "W6-011", "W6-012"])
cases["F2"] = {"pass": all(got.get(k) == v for k, v in ruled.items()) and ROW_TEXT in pred
               and got.get("S1_01_ROWS") == want_rows,
               "patterns_equal": {k: got.get(k) == v for k, v in ruled.items()},
               "row_list_in_ruling": ROW_TEXT in pred, "row_list_equal": got.get("S1_01_ROWS") == want_rows}

# F3
c4 = run(a.candidate, APPLIED, "cand_applied")["CWO04"]
cov = next(o for o in json.loads(RULINGS.read_text(encoding="utf-8"))["corpus_wide_orders"]
           if o["id"] == "CWO-1COR-04")["coverage_report"]
want = {"hits": 106, "rows": 52, "by_class": {"support_use": 29, "count_excess": 35, "location_only": 18,
                                              "disclosure_only": 18, "informs_compliant": 6},
        "support_or_excess_by_part": {"W1": 7, "W3": 5, "W4": 5, "W5": 19, "W6": 28}}
texts = ["106 hits in 52 rows; support_use 29, count_excess 35, location_only 18, disclosure_only 18, informs_compliant 6",
         "W1 7, W3 5, W4 5, W5 19, W6 28, W2 0"]
measured = {k: c4[k] for k in want}
cases["F3"] = {"pass": measured == want and all(t in cov for t in texts), "measured": measured,
               "ruling_texts_present": [t in cov for t in texts]}

# F4, F5
cl = run(a.candidate, prow, "cand_plants")["CWO04"]["list"]
by = {}
for h in cl:
    by.setdefault(h["row"], []).append([h["predicate"], h["auto_class"]])
f4 = {pid: {"source": src, "expected": [list(x) for x in exp], "got": by.get(pid, [])}
      for pid, src, _, _, exp in PLANTS}
cases["F4"] = {"pass": all(v["expected"] == v["got"] for v in f4.values()) and len(f4) == 13, "plants": f4}
f5 = {"W5-002": {"expected": [["CNT", "count_excess"]], "got": by.get("W5-002", []),
                 "fields": sorted({h["field"] for h in cl if h["row"] == "W5-002"})},
      "PLANT-15": {"expected": [], "got": by.get("PLANT-15", [])}}
cases["F5"] = {"pass": all(v["expected"] == v["got"] for v in f5.values())
               and f5["W5-002"]["fields"] == ["boundary_rationale"], "plants": f5}

res = {"fixtures": "fixtures_tf3", "candidate": str(a.candidate).replace("\\", "/"), "candidate_sha256": sha(cand_b),
       "baseline_sha256": sha(base_b), "rulings_sha256": sha(RULINGS.read_bytes()),
       "applied_rows_sha256": sha(APPLIED.read_bytes()), "combined_rows_sha256": sha(COMBINED.read_bytes()),
       "cases": cases, "verdict": "ALL_PASS" if all(v["pass"] for v in cases.values()) else "FAIL"}
Path(a.result).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"verdict": res["verdict"], "pass": {k: v["pass"] for k, v in cases.items()},
                  "candidate": res["candidate_sha256"][:12]}))
