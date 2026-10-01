#!/usr/bin/env python3
"""Collect every order for the book strategy's next version - v1's collection (#e12-#e15) plus #e16 and #e17 - verbatim,
with exact locations. v1 (collect_strategy_orders.py, strategy_v2_orders.v1.json) is kept unchanged.

What v2 adds, and why a phrase search alone is not enough:
  - #e16 and #e17 strings matching v1's phrase pattern, widened to 'the plan' / 'division plan' / 'section 7' / 'section 6'
    phrasing, because those rulings name the strategy as 'the plan';
  - #e17 K1 in full (which strategy-named cut sites license an onset and which name no device or rest on a byte-false
    premise) - the strategy must stop presenting those sites as licensed;
  - #e17's seven re-tiling orders with their resulting tilings - the strategy's unit lists for chapters 16-18, 20-21, 28
    and 35-36 must describe the book as it is now tiled;
  - #e16 C3 and C4 (the therefore-turn is not a licensed onset; said-to-me and transport inside a vision are) - the
    strategy's device list must agree.

usage: python collect_strategy_orders_v2.py
"""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
v1 = json.loads((HERE / "strategy_v2_orders.v1.json").read_text(encoding="utf-8"))
if v1["strategy_v1"]["sha256"] != sha(EZ / "book_strategy_Ezek.md"):
    raise SystemExit("REFUSED: the strategy changed since v1's collection")
PAT = re.compile(r"strategy(?:['’]s)? (?:v2|next version)|strategy v2|next version of the strategy|strategy's next|in strategy v2|"
                 r"the (?:division )?plan(?:['’]s)? (?:next|v2|text|section|names|should|must)|section [67] (?:of the plan|names|must|should)", re.I)
R16 = EZ / "author" / "e16" / "ruling_e16.json"
R17 = EZ / "author" / "e17" / "ruling_e17.json"
orders = list(v1["orders"])
for tag, p in (("#e16", R16), ("#e17", R17)):
    d = json.loads(p.read_text(encoding="utf-8-sig"))

    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, "%s.%s" % (path, k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, "%s[%d]" % (path, i))
        elif isinstance(o, str) and PAT.search(o):
            sents = [s.strip() for s in re.split(r"(?<=[.;])\s+", o) if PAT.search(s)]
            orders.append({"ruling": tag, "source": "Ezek/author/%s/%s %s" % (p.parent.name, p.name, path), "sentences": sents, "full_text": o})
    walk(d, "")
r16 = json.loads(R16.read_text(encoding="utf-8-sig"))
r17 = json.loads(R17.read_text(encoding="utf-8-sig"))
cr = r17["class_rulings"] if isinstance(r17["class_rulings"], list) else list(r17["class_rulings"].values())
structural = [
    {"ruling": "#e17", "source": "Ezek/author/e17/ruling_e17.json class_rulings[K1]", "kind": "cut-site licensing",
     "order_for_strategy": "present the named cut sites as K1 rules them: licensing, named on no device, or resting on a byte-false premise",
     "full_text": next(c for c in cr if c.get("id") == "K1")},
    {"ruling": "#e17", "source": "Ezek/author/e17/ruling_e17.json retiling_orders", "kind": "the book's tiling",
     "order_for_strategy": "describe the units of chapters 16-18, 20-21, 28 and 35-36 as re-tiled (138 rows)",
     "full_text": [{k: o[k] for k in o if k != "orders_voided_on_retired_rows"} for o in r17["retiling_orders"]]},
    {"ruling": "#e16", "source": "Ezek/author/e16/ruling_e16.json c3_lakhen_turn", "kind": "device list",
     "order_for_strategy": "the therefore-turn messenger onset is not a licensed onset", "full_text": r16["c3_lakhen_turn"]},
    {"ruling": "#e16", "source": "Ezek/author/e16/ruling_e16.json c4_confcal_member", "kind": "device list",
     "order_for_strategy": "'he said to me' and interior transport inside a vision stretch are licensed onsets", "full_text": r16["c4_confcal_member"]},
]
out = {"schema": "ezek_strategy_v2_orders.v2", "strategy_v1": v1["strategy_v1"],
       "rulings": dict(v1["rulings"], e16=sha(R16), e17=sha(R17)), "orders": orders, "structural_orders": structural,
       "count": len(orders) + len(structural)}
p = HERE / "strategy_v2_orders.v2.json"
data = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
if p.exists() and p.read_bytes() != data:
    raise SystemExit("REFUSED: %s exists with different bytes (E-41)" % p.name)
p.write_bytes(data)
print(json.dumps({"orders": len(orders), "structural": len(structural),
                  "by_ruling": {r: sum(1 for o in orders if o["ruling"] == r) for r in ("#e12", "#e13", "#e14", "#e15", "#e16", "#e17")},
                  "bytes": len(data), "sha256": sha(p)}, indent=1))
for o in orders[len(v1["orders"]):]:
    print("-", o["ruling"], o["source"][-60:], "|", " / ".join(o["sentences"])[:200])
