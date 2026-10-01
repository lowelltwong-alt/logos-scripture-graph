import json, sys
from pathlib import Path
EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
sys.path.insert(0, str(EZ / "tools"))
import check_refs_mirror as CM
from ezek_lib import expand_ref_token
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
live = {r["decision_id"]: r for r in (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}
sl = json.load(open('step2_slices.v1.json', encoding='utf-8'))['slices']
def fmt(ps):
    from collections import defaultdict
    d = defaultdict(list)
    for c, v in sorted(ps):
        d[c].append(v)
    return "; ".join("ch%d: %s" % (c, ",".join(str(v) for v in vs)) for c, vs in sorted(d.items()))
for rid in sl:
    row = live[rid]
    cov = CM.covered(row)
    own = set(expand_ref_token(str(row.get("span","")).replace("web:","")))
    print("==", rid, "span", row.get("span"))
    print("   COVERED(web):", fmt(cov))
    print("   OWN_SPAN_NOT_COVERED:", fmt(own - cov))
    print("   fields:", [k for k in row.keys()])
