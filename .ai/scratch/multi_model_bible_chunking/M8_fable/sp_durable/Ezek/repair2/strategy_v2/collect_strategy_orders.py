#!/usr/bin/env python3
"""Collect every order the rulings give for the book strategy's next version, verbatim, with its exact location.

#e15 close clearance item 3: "strategy v2 (CUT-RULE once; the transport predicate and 33; the Q2 unified rival
definitions; the 33:20 tiers; the section-6/section-2b transport reconciliation; the ch-18 and other Track-D
corrections already ordered) and the inventory note, distinct-checked (OW-10)". The orders are scattered through
#e12, #e13 and #e15; a v2 written from a summary would miss some (E-35 addendum: a count carried without its members).
This walks each ruling, keeps every string that orders a change to the strategy's next version, and records where.

usage: python collect_strategy_orders.py
"""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
PAT = re.compile(r"strategy(?:['’]s)? (?:v2|next version)|strategy v2|next version of the strategy|strategy's next|in strategy v2", re.I)
orders = []
for n in ("e12", "e13", "e14", "e15"):
    p = EZ / ("ezek_controlling_agent_ruling_%s.v1.json" % n)
    d = json.loads(p.read_text(encoding="utf-8"))

    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, "%s.%s" % (path, k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, "%s[%d]" % (path, i))
        elif isinstance(o, str) and PAT.search(o):
            sents = [s.strip() for s in re.split(r"(?<=[.;])\s+", o) if PAT.search(s)]
            orders.append({"ruling": "#" + n, "source": "Ezek/%s %s" % (p.name, path), "sentences": sents, "full_text": o})
    walk(d, "")
out = {"schema": "ezek_strategy_v2_orders.v1", "strategy_v1": {"file": "Ezek/book_strategy_Ezek.md", "sha256": sha(EZ / "book_strategy_Ezek.md"),
                                                               "bytes": (EZ / "book_strategy_Ezek.md").stat().st_size},
       "rulings": {n: sha(EZ / ("ezek_controlling_agent_ruling_%s.v1.json" % n)) for n in ("e12", "e13", "e14", "e15")},
       "orders": orders, "count": len(orders)}
p = HERE / "strategy_v2_orders.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"orders": len(orders), "by_ruling": {r: sum(1 for o in orders if o["ruling"] == r) for r in ("#e12", "#e13", "#e14", "#e15")},
                  "strategy_v1_bytes": out["strategy_v1"]["bytes"], "out": str(p), "sha256": sha(p)}, indent=1))
for o in orders:
    print("-", o["ruling"], o["source"][-70:], "|", " / ".join(o["sentences"])[:230])
