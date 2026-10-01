#!/usr/bin/env python3
"""Measure P06-015's observed_substrate_signals on the pinned witness (lane B's MEDIUM finding SIGNAL_OUT_OF_SPAN).

Same method as repair2/final/plan_signals_and_token_fix.py: a report is evidence, not an order; an element is REMOVED only
when its skeleton is MEASURED absent from EVERY verse of the row's own span (the most generous test: position is not
required), and an element with no measurement defined here is KEPT. Signals are outside the author's writable scope by
design, so this deterministic pass is the repair path. The neighbour P06-014 is measured the same way, for contrast.

Writes signals_v9.report.json and signals_v9.proposal.json beside this file (write-new; same bytes left, else refused).
usage: python measure_signals_v9.py
"""
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
EZ = HERE.parents[1]
ROWS, ROWS_PIN = EZ / "rows_v8_final.jsonl", "b2160ad6281184dc1dedf15a764bc058bc79a181928ed6323dbc332ec09cb0e7"
OSHB, OSHB_PIN = EZ / "Ezek_oshb.txt", "337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e"
sha = lambda b: hashlib.sha256(b).hexdigest()                                 # noqa: E731
if sha(ROWS.read_bytes()) != ROWS_PIN or sha(OSHB.read_bytes()) != OSHB_PIN:
    raise SystemExit("REFUSED: an input is not at its pinned digest")
rows = {r["decision_id"]: r for r in (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}
heb = dict(l.split("\t", 1) for l in OSHB.read_text(encoding="utf-8").splitlines() if "\t" in l)


def skel(s):
    s = "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))
    return re.sub(r"[\s־]+", " ", s).strip()


# element -> skeleton that must stand in some verse of the span (chapter 28 is outside the MT/WEB zone: keys identical)
NEEDLE = {"wordevent.strict": skel("ויהי דבר יהוה אלי לאמר"), "address.son_of_man": skel("בן אדם"),
          "face.set_toward": skel("שים פניך"), "against.behold_i_am": skel("הנני על"),
          "messenger.formula": skel("כה אמר אדני יהוה"), "recognition.3mp": skel("וידעו כי אני")}


def verses(span):
    m = re.match(r"^Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)$", span)
    c1, v1, c2, v2 = (int(x) for x in m.groups())
    assert c1 == c2 == 28
    return ["Ezek.28.%d" % v for v in range(v1, v2 + 1)]


report, proposal = {}, {}
for rid in ("P06-015", "P06-014"):
    r = rows[rid]
    vs = verses(r["span"])
    live = list(r["observed_substrate_signals"])
    res = []
    for e in live:
        if e in NEEDLE:
            hit = [k for k in vs if NEEDLE[e] in skel(heb.get(k, ""))]
            res.append({"element": e, "supported": bool(hit), "verses_with_it": hit, "needle_skeleton": NEEDLE[e],
                        "test": "the skeleton stands in some verse of the row's own span", "tier": "MEASURED"})
        else:
            res.append({"element": e, "supported": None, "test": "no measurement defined here; kept"})
    report[rid] = {"span": r["span"], "verses": vs, "live": live, "measured": res}
    if rid == "P06-015":
        keep = [x["element"] for x in res if x["supported"] is not False]
        if keep != live:
            proposal[rid] = {"observed_substrate_signals": keep}
out = {"schema": "ezek_signals_v9.v1", "rows": "rows_v8_final.jsonl", "rows_sha256": ROWS_PIN, "witness_sha256": OSHB_PIN,
       "witness": "OSHB (WLC), single witness", "report": report,
       "removed": {rid: [x for x in report[rid]["live"] if x not in p["observed_substrate_signals"]] for rid, p in proposal.items()}}
for name, obj in (("signals_v9.report.json", out), ("signals_v9.proposal.json", proposal)):
    b = json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8")
    p = HERE / name
    if p.exists():
        if p.read_bytes() != b:
            raise SystemExit("REFUSED: %s exists with different bytes" % name)
    else:
        p.write_bytes(b)
    print(name, sha(b))
print(json.dumps({rid: [(x["element"], x["supported"], x.get("verses_with_it")) for x in v["measured"]] for rid, v in report.items()},
                 ensure_ascii=False, indent=1))
print("removed:", out["removed"])
