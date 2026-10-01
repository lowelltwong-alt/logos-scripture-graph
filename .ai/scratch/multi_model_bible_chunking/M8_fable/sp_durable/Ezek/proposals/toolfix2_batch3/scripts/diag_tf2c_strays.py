"""Read-only hand-review aid for the four check_marks strays of the toolfix2_batch3 condition (c) re-run. For each row it prints:
  - every K/Q token and mark-letter absence phrase with its surrounding text;
  - the batch1 negation (puncta_negated) and the batch3 negation (kq_negation, denied_after), with the numbers each clause names;
  - the pmarks marks and kq entries at those numbers (both readings, and N-1 for mark claims);
  - each tool's flags for the row, run from the batch1 base and the batch3 stage.
Writes only under the scratchpad."""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SCR = Path(__file__).resolve().parent
EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
B3 = SCR / "stage_tf2c" / "sp_durable" / "Ezek" / "tools"
B1 = SCR / "stage_tf2c_base_batch1_staged" / "sp_durable" / "Ezek" / "tools"
IDS = ["P02-006", "P02-020", "P05-003", "P09-002"]
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
rows = {}
for l in (EZ / "repair" / "rows_v3_cwo12.jsonl").read_text(encoding="utf-8").splitlines():
    if l.strip():
        r = json.loads(l)
        for key in ("decision_id", "writer_decision_id"):
            if r.get(key) in IDS:
                rows[r[key]] = r


def load(tag, d):
    sys.path.insert(0, str(d))
    spec = importlib.util.spec_from_file_location("cm_" + tag, d / "check_marks.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.path.pop(0)
    return mod


m1, m3 = load("b1", B1), load("b3", B3)
pm = json.loads((EZ / "pmarks_Ezek.json").read_text(encoding="utf-8"))
marks, kq = pm["marks"], pm["kq"]
diag = SCR / "diag_tf2c"
diag.mkdir(exist_ok=True)
rp = diag / "rows4.jsonl"
rp.write_text("\n".join(json.dumps(rows[i], ensure_ascii=False) for i in IDS if i in rows) + "\n", encoding="utf-8")
flags = {}
for tag, d in (("batch1", B1), ("batch3", B3)):
    out = json.loads(subprocess.run([sys.executable, str(d / "check_marks.py"), str(rp)], capture_output=True, text=True, encoding="utf-8",
                                    env=ENV, cwd=str(d)).stdout)
    flags[tag] = out["flags"]
report = {}
for wid in IDS:
    r = rows.get(wid)
    if not r:
        report[wid] = "row not found"
        continue
    did = r["decision_id"]
    text = m3.prose_of(r) + " " + " ".join(r.get("boundary_evidence_refs", []))
    items = []
    for m in m3.KQ.finditer(text):
        named = [p for pairs in m3.puncta_claim_numbers(text, m.start(), m.end()) for p in pairs]
        keys = sorted({"Ezek.%d.%d" % rr for c, v in named for rr in m3.readings(c, v)})
        items.append({"token": m.group(0), "at": m.start(), "context": text[max(0, m.start() - 170):m.end() + 120].replace("\n", " | "),
                      "batch1_puncta_negated": m1.puncta_negated(text, m.start(), m.end()),
                      "batch3_kq_negation": m3.kq_negation(text, m.start()), "batch3_denied_after": m3.denied_after(text, m.end()),
                      "named": named[:12], "kq_at_named": {k: bool(kq.get(k)) for k in keys}})
    lets = []
    for m in m3.letter_absences(text):
        named = [p for pairs in m3.puncta_claim_numbers(text, m.start(), m.end()) for p in pairs]
        lets.append({"phrase": m.group(0), "context": text[max(0, m.start() - 170):m.end() + 120].replace("\n", " | "), "named": named[:12],
                     "marks_at_named": {"Ezek.%d.%d" % rr: marks.get("Ezek.%d.%d" % rr) for c, v in named for rr in m3.readings(c, v)},
                     "span": r.get("span"), "span_relevant_marks": m3.relevant(m3.span_pairs(r), marks)})
    report[wid] = {"decision_id": did, "span": r.get("span"), "kq_tokens": items, "letter_absences": lets,
                   "flags_batch1": [f for f in flags["batch1"] if f.get("decision_id") == did and f.get("rule") in
                                    ("kq_claim", "false_kq_absence_claim", "false_mark_absence_claim", "paragraph_mark_claim")],
                   "flags_batch3": [f for f in flags["batch3"] if f.get("decision_id") == did and f.get("rule") in
                                    ("kq_claim", "false_kq_absence_claim", "false_mark_absence_claim", "paragraph_mark_claim")]}
(diag / "strays.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps(report, ensure_ascii=False, indent=1)[:30000])
