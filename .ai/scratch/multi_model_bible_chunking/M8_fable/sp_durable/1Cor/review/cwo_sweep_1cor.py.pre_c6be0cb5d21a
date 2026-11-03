"""CWO-1COR-01 and CWO-1COR-02 sweep (1Cor controlling rulings cor_controlling_rulings_r1_a1#e1), predicates verbatim
from the installed rulings. Reads ROWS.jsonl and the installed ngram7.prose (import, read-only); writes --out only.
usage: cwo_sweep.py ROWS.jsonl --out FILE.json
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
SP = Path("C:/wt/logos-t423-m8-fable/.ai/scratch/multi_model_bible_chunking/M8_fable/sp_durable")
sys.path.insert(0, str(SP / "1Cor" / "tools"))
from ngram7 import prose  # noqa: E402

rows_p = Path(sys.argv[1])
out_p = Path(sys.argv[sys.argv.index("--out") + 1])
A1, A2 = re.compile(r"^\s*web:"), re.compile(r"(?i)WEB paragraph|paragraph start|DISCLOSURE-mark")
B1 = re.compile(r"(?i)pilcrow|WEB paragraph|paragraph start|chapter division")
B2 = re.compile(r"(?i)corroborat|agree|join|inform|favour|support|lean|confirm")
SPLIT = re.compile(r"(?<=[.;])\s+")
GREEK = re.compile("[\u0370-\u03FF\u1F00-\u1FFF]")
L1, L2 = "Robinson-Pierpont Byzantine Textform (Unlicense)", "SBLGNT (CC BY 4.0)"
rows = [json.loads(x) for x in rows_p.read_text(encoding="utf-8").splitlines() if x.strip()]
a_hits, b_hits, c_fail = [], [], []
for r in rows:
    rid = r["decision_id"]
    for i, ref in enumerate(r.get("boundary_evidence_refs") or []):
        s = ref if isinstance(ref, str) else json.dumps(ref, ensure_ascii=False)
        if A1.search(s) and A2.search(s):
            a_hits.append({"row": rid, "field": "boundary_evidence_refs", "index": i, "ref": s})
    for f in ("boundary_rationale", "strongest_rejected_alternative", "device_notes"):
        v = r.get(f)
        if not isinstance(v, str):
            continue
        for sent in SPLIT.split(v):
            if B1.search(sent) and B2.search(sent):
                b_hits.append({"row": rid, "field": f, "sentence": sent})
    p = prose(r)
    if GREEK.search(p) and not (L1 in p and L2 in p):
        c_fail.append({"row": rid, "has_L1": L1 in p, "has_L2": L2 in p})
part = lambda h: h["row"].split("-")[0]  # noqa: E731
res = {"rows_file": str(rows_p), "rows_scanned": len(rows),
       "A": {"hits": len(a_hits), "rows": len({h["row"] for h in a_hits}), "by_part": dict(Counter(map(part, a_hits))),
             "list": a_hits},
       "B": {"hits": len(b_hits), "rows": len({h["row"] for h in b_hits}), "by_part": dict(Counter(map(part, b_hits))),
             "list": b_hits},
       "CWO02": {"fail": len(c_fail), "of": len(rows), "list": c_fail}}
out_p.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({k: (v if k in ("rows_scanned",) else {kk: vv for kk, vv in v.items() if kk != "list"})
                  for k, v in res.items() if k != "rows_file"}, ensure_ascii=False))
