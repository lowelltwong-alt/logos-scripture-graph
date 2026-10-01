#!/usr/bin/env python3
"""CONF-CAL AUDIT MEMBER v4 - #e17 tool orders T-1 and T-5, built as a layer over v3 (v3 and v2 imported, not copied).

T-1: the R-6 site list is REPLACED by #e17 class_rulings[K1].fixture_for_the_conf_cal_member, read from the pinned ruling:
     'licensed_by_naming' verses license the onset near face; 'named_but_not_licensing' verses are recorded as PLAN SEAMS
     (a section-7 ground, medium_low) and never as licensed onsets. v3's phrase extraction of the strategy is retired.
T-5: c4 membership is the inventory v3 said_to_me_in_vision list (speaker immaterial, K4). Every member that is INTERIOR to a
     row's span (in span, not its first verse) needs a WARRANT-rival token on that seam; a member with none is listed.
     (All five vision stretches lie outside the chapter 20-21 zone, so the WEB and MT verse numbers agree there; the tool
     refuses if that ever stops being true.)

usage: python confcal_audit_v4.py [--rows <rows.jsonl>] [--out <json>] | --selftest
"""
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
_saved = list(sys.argv)
sys.argv = [sys.argv[0]]
import confcal_audit_v3 as V3                                                  # noqa: E402
sys.argv = _saved
V2 = V3.V2
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731


def _arg(n, d=None):
    return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d


ROWS = Path(_arg("--rows", str(EZ / "repair" / "rows_v7_cwo24.jsonl")))
OUT = Path(_arg("--out", str(HERE / "confcal_audit.v4.json")))
R17 = EZ / "author" / "e17" / "ruling_e17.json"
r17 = json.loads(R17.read_text(encoding="utf-8-sig"))
K1 = next(c for c in (r17["class_rulings"] if isinstance(r17["class_rulings"], list) else r17["class_rulings"].values()) if c.get("id") == "K1")
FIX = K1["fixture_for_the_conf_cal_member"]
cv = lambda r: tuple(int(x) for x in r.split(".")[1:3])                        # noqa: E731
LICENSED_BY_NAMING = {cv(x) for x in FIX["licensed_by_naming"]}
PLAN_SEAMS_NOT_LICENSING = {cv(k): v for k, v in FIX["named_but_not_licensing"].items()}
V2.ONSET_LICENSED["strategy-named cut site"] = set(LICENSED_BY_NAMING)          # T-1: replaces v3's extracted list
C4 = [cv(x) for x in V3.inv3["said_to_me_in_vision"]["verses_mt"]]
ZONE_MT = {(21, v) for v in range(1, 38)} | {(20, v) for v in range(45, 50)}
if any(x in ZONE_MT for x in C4):
    raise SystemExit("REFUSED: a said-to-me member lies in the chapter 20-21 zone; T-5's WEB=MT premise does not hold")
SPAN = re.compile(r"^Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)$")
RIVAL_PAIR = re.compile(r"\[WARRANT-rival(?::[a-z]+)?\]\s*(\d{1,2})\.(\d{1,3})/(\d{1,2})\.(\d{1,3})")


def c4_missing(r):
    m = SPAN.match(r["span"])
    first, last = V2.to_mt(int(m.group(1)), int(m.group(2))), V2.to_mt(int(m.group(3)), int(m.group(4)))
    have ={((int(a), int(b)), (int(c), int(d))) for e in r.get("boundary_evidence_refs") or [] for a, b, c, d in RIVAL_PAIR.findall(e)}
    out = []
    for v in C4:
        if first < v <= last and v in V2.POS:
            p = V2.prev_cv(v)
            if (p, v) not in have:
                out.append("%d:%d/%d:%d" % (p + v))
    return out


def plan_seam_notes(r):
    m = SPAN.match(r["span"])
    # spans are WEB-numbered; the position table is MT-keyed (chapters 20-21 diverge)
    first, last = V2.to_mt(int(m.group(1)), int(m.group(2))), V2.to_mt(int(m.group(3)), int(m.group(4)))
    nxt = V2.next_cv(last)
    return {"%d:%d" % k: why for k, why in PLAN_SEAMS_NOT_LICENSING.items() if k in (first, nxt)}


def selftest():
    rows = {x["decision_id"]: x for x in (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}
    anyrow = next(iter(rows.values()))
    cases = [
        ("T-1 46:1 is licensed by naming", V2.onset_signal((46, 1), (45, 25))["signal"] == "licensed"),
        ("T-1 16:44 is NOT licensed (named on no device)", V2.onset_signal((16, 44), (16, 43))["signal"] != "licensed"
         or (16, 44) not in V2.ONSET_LICENSED["strategy-named cut site"]),
        ("T-1 20:27 is not in the licensing list", (20, 27) not in V2.ONSET_LICENSED["strategy-named cut site"]),
        ("T-1 the fixture carries 15 licensing and 4 non-licensing verses", len(LICENSED_BY_NAMING) == 15 and len(PLAN_SEAMS_NOT_LICENSING) == 4),
        ("T-5 an interior said-to-me verse with no token is listed", c4_missing(dict(anyrow, span="Ezek.40.1-Ezek.40.16", boundary_evidence_refs=[])) == ["40:3/40:4"]),
        ("T-5 the token on the seam discharges it", c4_missing(dict(anyrow, span="Ezek.40.1-Ezek.40.16", boundary_evidence_refs=[
            "oshb:Ezek.40.4 [WARRANT-rival:near] 40.3/40.4 the guide's speech inside the vision: paragraph-grade, held"])) == []),
        ("T-5 a member on the row's first verse is not interior", c4_missing(dict(anyrow, span="Ezek.40.4-Ezek.40.16", boundary_evidence_refs=[])) == []),
        ("v3 (a) still classifies a close-seam :merge", V3.audit_row_v3(dict(anyrow, span="Ezek.17.11-Ezek.17.21", boundary_evidence_refs=[
            "web:Ezek.17.22-Ezek.17.24 [WARRANT-rival:merge] 17.21/17.22 the cedar coda weighed as part of this row"]))["merge_rivals"][0]["classification"] == "MERGE_CONTESTS_OWN_SEAM(close)"),
    ]
    failed = [n for n, ok in cases if not ok]
    print(json.dumps({"selftest_cases": len(cases), "failed": failed}, indent=1))
    return 1 if failed else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    if selftest():
        raise SystemExit("REFUSED: selftest failed (E-36)")
    rows = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
    res = []
    for r in rows:
        x = V3.audit_row_v3(r)
        x["c4_missing_token"] = c4_missing(r)
        x["plan_seam_not_licensing"] = plan_seam_notes(r)
        res.append(x)
    out = {"schema": "ezek_confcal_audit.v4", "orders": ["#e17 T-1", "#e17 T-5"],
           "inputs": {"rows_sha256": sha(ROWS), "ruling_e17_sha256": sha(R17), "inventory_v3_sha256": sha(V3.INV3)},
           "fixture": {"licensed_by_naming": sorted("%d:%d" % k for k in LICENSED_BY_NAMING),
                       "named_but_not_licensing": {"%d:%d" % k: v for k, v in PLAN_SEAMS_NOT_LICENSING.items()}},
           "tally": dict(Counter(x["state"] for x in res)),
           "rows_for_final": [x for x in res if x["state"] in ("GRADE_ABOVE_DERIVED", "GRADE_BELOW_DERIVED")],
           "missing_token_rows": {x["row"]: x["missing_token"] for x in res if x["missing_token"]},
           "c4_missing_token_rows": {x["row"]: x["c4_missing_token"] for x in res if x["c4_missing_token"]},
           "all": res}
    data = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
    if OUT.exists() and OUT.read_bytes() != data and "--overwrite" not in sys.argv:
        raise SystemExit("REFUSED: %s exists with different bytes (E-41)" % OUT.name)
    OUT.write_bytes(data)
    print(json.dumps({"tally": out["tally"], "rows_for_final": len(out["rows_for_final"]), "missing_token_rows": len(out["missing_token_rows"]),
                      "c4_missing_token_rows": out["c4_missing_token_rows"], "sha256": sha(OUT)}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
