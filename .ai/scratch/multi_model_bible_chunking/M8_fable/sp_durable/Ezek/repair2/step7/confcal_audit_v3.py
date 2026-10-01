#!/usr/bin/env python3
"""CONF-CAL AUDIT MEMBER v3 - #e16 tool order 2, built as a layer over v2 (v2's logic is imported, not copied).

What v3 changes, each from #e16:
  (a) ':merge' rival tokens are classified MERGE_CONTESTS_OWN_SEAM(onset|close) and derive no rival face (C1/C2)
  (b) 'he said to me' at a verse head inside a vision stretch is a LICENSED onset (C4; inventory v3 list)
  (c) transport verses are licensed onsets (already in v2)
  (d) STRATEGY-NAMED CUT SITES and RE-ONSETS license the near face at that verse (R-6): a data fixture extracted here from
      the pinned strategy by exact phrase, with its digest; sites a later ruling found byte-false are excluded with reason
  (e) genre colophons (19:14, 43:12) and vision returns (3:15, 11:25) are close-role signals (inventory v3; a reading)
  (f) rivals are also read from device_notes seam pairs and 'cutting at C:V' anchors; a weighed rival with no WARRANT-rival
      token (merge tokens included) is a MISSING_TOKEN finding
  (g) LICENSED vs TWO-FACED stay separate predicates (v2)
  (h) scene change on a close far face stays READER tier (v2)

usage: python confcal_audit_v3.py [--rows <rows.jsonl>] [--out <json>] | --selftest
"""
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
sys.argv_saved = list(sys.argv)
sys.argv = [sys.argv[0]]                       # v2 parses --rows/--out at import; import it with defaults
import confcal_audit_v2 as V2                                                  # noqa: E402
sys.argv = sys.argv_saved
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731


def _arg(n, d=None):
    return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d


ROWS = Path(_arg("--rows", str(EZ / "repair" / "rows_v7_cwo24.jsonl")))
OUT = Path(_arg("--out", str(HERE / "confcal_audit.v3.json")))
INV3 = EZ / "ezek_device_inventory.v3.json"
STRAT = EZ / "book_strategy_Ezek.md"
inv3 = json.loads(INV3.read_text(encoding="utf-8"))["v3_additions"]
cv = lambda r: tuple(int(x) for x in r.split(".")[1:3])                        # noqa: E731

# (d) strategy-named cut sites / re-onsets, by exact phrase over the pinned strategy
strategy = STRAT.read_text(encoding="utf-8")
# a first pattern stopped at the ';' inside '16:35 (pe; ...)' and missed the section-6 transport cut list (found 4 sites;
# the selftest's size fixture caught it). Parenthetical glosses are stripped before verses are read.
CUT_PHRASES = [r"Internal cuts at ((?:\d+:\d+(?:\s*\([^)]*\))?,?\s*(?:and\s+)?)+)", r"(\d+:\d+) as a morning re-onset",
               r"with the (\d+:\d+) and (\d+:\d+) messenger re-onsets", r"transport verb \(([^)]*)\)"]
sites = {}
for pat in CUT_PHRASES:
    for m in re.finditer(pat, strategy, re.S):
        txt = re.sub(r"\([^)]*\)", " ", " ".join(g for g in m.groups() if g)) if not pat.startswith("transport") else m.group(1)
        for c, v in re.findall(r"(\d{1,2}):(\d{1,3})", txt):
            sites.setdefault((int(c), int(v)), m.group(0)[:120].replace("\n", " "))
EXCLUDED = {(20, 27): "#e13 R8 found the strategy's named ch-20 instance byte-false and corrected it",
            (20, 30): "#e13 R8 byte-false; #e16 C3 rules the lakhen turn at 20:30 not a licensed onset"}
STRATEGY_SITES = {k: v for k, v in sites.items() if k not in EXCLUDED}

V2.ONSET_LICENSED["he said to me (in a vision)"] = {cv(x) for x in inv3["said_to_me_in_vision"]["verses_mt"]}
V2.ONSET_LICENSED["strategy-named cut site"] = set(STRATEGY_SITES)
READING_CLOSE = {cv(x): "genre colophon" for x in inv3["genre_colophon"]["verses_mt"]}
READING_CLOSE.update({cv(x): "vision return" for x in inv3["vision_return"]["verses_mt"]})
_close_v2 = V2.close_signal


def close_signal(c_v):
    if c_v in READING_CLOSE:
        return {"signal": "close", "classes": [READING_CLOSE[c_v]], "verse_final": "VERSE_FINAL",
                "tier": "a reading licensed by #e16 C4 (inventory v3)"}
    return _close_v2(c_v)


V2.close_signal = close_signal
MERGE = re.compile(r"\[WARRANT-rival:merge\]\s*(\d{1,2})\.(\d{1,3})/(\d{1,2})\.(\d{1,3})")
PAIR_ANY = re.compile(r"(?<![\d.:])(\d{1,2})[.:](\d{1,3})/(\d{1,2})[.:](\d{1,3})(?![\d])")
CUTTING = re.compile(r"cutting at (\d{1,2}):(\d{1,3})", re.I)


def audit_row_v3(r):
    refs = list(r.get("boundary_evidence_refs") or [])
    merges = [(e, MERGE.search(e)) for e in refs if MERGE.search(e)]
    rest = [e for e in refs if not MERGE.search(e)]
    extra = " ".join("%s/%s" % ("%d.%d" % V2.prev_cv((int(c), int(v))), "%s.%s" % (c, v))
                     for c, v in CUTTING.findall((r.get("strongest_rejected_alternative") or "") + " " + (r.get("device_notes") or ""))
                     if (int(c), int(v)) in V2.POS and V2.prev_cv((int(c), int(v))))
    view = dict(r, boundary_evidence_refs=rest,
                strongest_rejected_alternative=" ".join(x for x in (r.get("strongest_rejected_alternative"), r.get("device_notes"), extra) if x))
    out = V2.audit_row(view)
    m = re.match(r"Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)$", r["span"])
    first, last = V2.to_mt(int(m.group(1)), int(m.group(2))), V2.to_mt(int(m.group(3)), int(m.group(4)))
    out["merge_rivals"] = []
    for e, mm in merges:
        a, b = V2.to_mt(int(mm.group(1)), int(mm.group(2))), V2.to_mt(int(mm.group(3)), int(mm.group(4)))
        side = "close" if (a, b) == (last, V2.next_cv(last)) else ("onset" if (a, b) == (V2.prev_cv(first), first) else "NOT_AN_OWN_SEAM")
        out["merge_rivals"].append({"entry": e, "classification": "MERGE_CONTESTS_OWN_SEAM(%s)" % side})
    tokened = set()
    for e in refs:
        pm = re.search(r"\[WARRANT-rival[^\]]*\]\s*(\d{1,2})\.(\d{1,3})/(\d{1,2})\.(\d{1,3})", e)
        if pm:
            tokened.add((V2.to_mt(int(pm.group(1)), int(pm.group(2))), V2.to_mt(int(pm.group(3)), int(pm.group(4)))))
    weighed = set()
    for pm in PAIR_ANY.finditer(view["strongest_rejected_alternative"]):
        a, b = V2.to_mt(int(pm.group(1)), int(pm.group(2))), V2.to_mt(int(pm.group(3)), int(pm.group(4)))
        if a in V2.POS and b in V2.POS and V2.POS[b] == V2.POS[a] + 1 and V2.POS[first] < V2.POS[b] <= V2.POS[last]:
            weighed.add((a, b))
    out["missing_token"] = ["%d:%d/%d:%d" % (a + b) for a, b in sorted(weighed - tokened)]
    return out


def selftest():
    rows = {x["decision_id"]: x for x in (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}
    cases = [
        ("(b) 8:5 'he said to me' inside 8:1-11:25 is a licensed onset", V2.onset_signal((8, 5), (8, 4))["signal"] == "licensed"),
        ("(d) 36:33 is licensed by strategy naming", V2.onset_signal((36, 33), (36, 32))["signal"] == "licensed"),
        ("(e) 19:14 genre colophon is a close signal", close_signal((19, 14))["signal"] == "close"),
        ("(a) a :merge token is classified, not read as a rival", audit_row_v3(dict(rows["P03-011"], boundary_evidence_refs=[
            "web:Ezek.17.19-Ezek.17.21 [WARRANT-rival:merge] 17.18/17.19 forward merge weighed here"]))["merge_rivals"][0]["classification"] == "MERGE_CONTESTS_OWN_SEAM(close)"),
        ("(f) a pair weighed in prose with no token is MISSING_TOKEN", bool(audit_row_v3(dict(rows["P10-012"], boundary_evidence_refs=[],
            strongest_rejected_alternative="a cut at 43:4/43:5 was weighed", device_notes=""))["missing_token"])),
        ("the strategy fixture is non-empty and excludes the byte-false ch-20 sites", len(STRATEGY_SITES) > 5 and (20, 30) not in STRATEGY_SITES),
    ]
    failed = [n for n, ok in cases if not ok]
    print(json.dumps({"selftest_cases": len(cases), "failed": failed, "strategy_sites": sorted("%d:%d" % k for k in STRATEGY_SITES)}, indent=1))
    return 1 if failed else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    if selftest():
        raise SystemExit("REFUSED: selftest failed (E-36)")
    rows = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
    res = [audit_row_v3(r) for r in rows]
    out = {"schema": "ezek_confcal_audit.v3", "order": "#e16 tool_orders[1]",
           "inputs": {"rows_sha256": sha(ROWS), "inventory_v3_sha256": sha(INV3), "strategy_sha256": sha(STRAT)},
           "strategy_cut_site_fixture": {"%d:%d" % k: v for k, v in sorted(STRATEGY_SITES.items())},
           "strategy_sites_excluded": {"%d:%d" % k: v for k, v in EXCLUDED.items()},
           "tally": dict(Counter(x["state"] for x in res)),
           "rows_for_e16": [x for x in res if x["state"] in ("GRADE_ABOVE_DERIVED", "GRADE_BELOW_DERIVED")],
           "missing_token_rows": {x["row"]: x["missing_token"] for x in res if x["missing_token"]},
           "all": res}
    data = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
    if OUT.exists() and OUT.read_bytes() != data and "--overwrite" not in sys.argv:
        raise SystemExit("REFUSED: %s exists with different bytes (E-41)" % OUT.name)
    OUT.write_bytes(data)
    print(json.dumps({"tally": out["tally"], "rows_for_e16": len(out["rows_for_e16"]), "missing_token_rows": len(out["missing_token_rows"]),
                      "sha256": sha(OUT)}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
