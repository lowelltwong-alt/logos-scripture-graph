"""TF-5 builder: adds CWO-1COR-06 and CWO-1COR-07 to the sweep as added sections. The section is copied line by line from
the reference bytes (cwo06_ref.py, sha f8dce30c), so no pattern is retyped; only the reference's own path constant and the
two load lines that use it are rewritten to the sweep's SP. Writes OUT only.
usage: mk_tf5.py SWEEP_IN.py REF.py OUT.py
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
src, ref_p, out = map(Path, sys.argv[1:4])
s = src.read_text(encoding="utf-8")
ref = ref_p.read_text(encoding="utf-8").split("\n")
sign = ref[5:39]         # SIGNS .. find
rest = ref[43:108]       # units .. sweep07
assert sign[0].startswith("SIGNS = ") and sign[-1].strip() == "return -1", (sign[0], sign[-1])
assert ref[39].startswith("SP = r") and ref[40].startswith("RP, SBL = load(") and ref[41].startswith("pm = json.load(")
assert ref[42].startswith("DIFF = ") and rest[0].startswith("def units(r):") and rest[-1].strip() == "return out"
load = ['RP, SBL = load(SP / "1Cor" / "1Cor_rp.txt"), load(SP / "1Cor" / "1Cor_sbl.txt")',
        'pm = json.load(open(SP / "1Cor" / "pmarks_1Cor.json", encoding="utf-8"))', ref[42]]
section = ["# CWO-1COR-06 and CWO-1COR-07 (TF-5): copied from the E4 reference cwo06_ref.py, sha f8dce30c; only its path constant"
           " changed.", *sign, *load, *rest, "", ""]


def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


s = once(s, "import sys\nfrom collections import Counter\n", "import sys\nimport unicodedata\nfrom collections import Counter\n")
s = once(s, "\nusage: cwo_sweep.py ROWS.jsonl --out FILE.json\n",
         " TF-5 (cor_controlling_rulings_r4_a1#e1) adds CWO-1COR-06 and CWO-1COR-07 as additions, from the"
         " E4 reference; these two also read 1Cor_rp.txt, 1Cor_sbl.txt and pmarks_1Cor.json, read-only."
         "\nusage: cwo_sweep.py ROWS.jsonl --out FILE.json\n")
s = once(s, "rows = [json.loads(x) for x in rows_p.read_text(", "\n".join(section) + "rows = [json.loads(x) for x in rows_p.read_text(")
s = once(s, "e_hits = [h for r in rows for h in cwo05_row(r)]\n",
         "e_hits = [h for r in rows for h in cwo05_row(r)]\nh6, h7 = sweep06(rows), sweep07(rows)\n")
s = once(s, '"list": e_hits}}\n',
         '"list": e_hits},\n'
         '       "CWO06": {"hits": len(h6), "rows": len({h["row"] for h in h6}), "range_token": sum(h["range_token"] for h in h6),\n'
         '                 "by_kind": dict(Counter(h["kind"] for h in h6)), "list": h6},\n'
         '       "CWO07": {"unlisted": len(h7), "rows": len({h["row"] for h in h7}), "list": h7}}\n')
out.write_text(s, encoding="utf-8", newline="\n")
print("wrote", out, "lines", s.count("\n"))
