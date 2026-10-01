import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
sys.path.insert(0, str(EZ / "tools"))
import check_refs_mirror as CM
from ezek_lib import expand_ref_token
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
live = {r["decision_id"]: r for r in (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}
prop = json.loads((HERE / "proposal.json").read_text(encoding="utf-8"))
MENTION = re.compile(r"(?<![\w.:])(\d{1,3})[:.](\d{1,3})(?![\d.])")
for rid, fields in prop.items():
    row = dict(live[rid]); row.update(fields)
    own = set(expand_ref_token(str(row.get("span","")).replace("web:","")))
    win, _ = CM.a4_window(own)
    cov = CM.covered(row)
    chs = {c for c, _ in own}
    cits = CM.prose_citations(row, chs)
    read = set().union(*[c["verses"] for c in cits]) if cits else set()
    far = sorted(v for c in cits for v in c["verses"] if not (c["verses"] & win))
    # textual mentions in MY new text only
    hidden = set()
    for f, v in fields.items():
        for m in MENTION.finditer(v):
            p = (int(m.group(1)), int(m.group(2)))
            if p[0] in {c for c, _ in own} and p not in read:
                hidden.add(p)
    print("==", rid)
    print("   far_side verses cited:", ["Ezek.%d.%d" % p for p in sorted(set(far))] or "none")
    print("   mentioned-but-not-read-as-citation:", ["%d.%d" % p for p in sorted(hidden)] or "none",
          "| of those, uncovered:", ["%d.%d" % p for p in sorted(hidden - cov)] or "none")
