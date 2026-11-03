"""Read the 23 landed 1Cor primary finals and group them for controlling round 4.

extract(finals) takes (lane, cluster, path) triples and returns an ordered dict of queue findings:
  R4-<row_id>       every challenge on that row, whichever lane raised it, with the other lanes' verdicts on the same row
  TRIAGE-1COR-01/02 every lane's answer where the question touched its cluster
  R4-UNCERTAINTY    every lane's unresolved_uncertainty
The finals differ in shape (LF_c04 upper-cases verdicts; OL_c08 keeps evidence as a string and triage under triage_id), so
verdicts are lower-cased, a string evidence becomes one element and the triage id is read from either key. Anything that
is neither support nor challenge raises, so no finding is dropped silently.
usage: primaries_extract.py   (prints the counts over the finals on disk; writes nothing)
"""
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CLUSTERS = ["c%02d" % i for i in range(1, 11)]
PLAN = [("OL", c) for c in CLUSTERS] + [("LF", c) for c in CLUSTERS] + [("RT", c) for c in ("c06", "c07", "c08")]
RANK = {"high": 3, "medium": 2, "low": 1}
FIELDS = ("claim", "tier", "decision", "suggested_fix", "both_sides")


def extract(finals):
    rows, triage, uncertain = {}, {}, []
    for lane, cluster, path in finals:
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        tag = "%s_%s" % (lane, cluster)
        for it in d["items"]:
            verdict = str(it.get("verdict")).strip().lower()
            if verdict not in ("support", "challenge"):
                raise SystemExit("%s %s: verdict %r" % (tag, it.get("row_id"), it.get("verdict")))
            r = rows.setdefault(it["row_id"], {"findings": [], "other_lanes": []})
            if verdict == "support":
                r["other_lanes"].append({"lane": tag, "verdict": "support"})
                continue
            ev = it.get("evidence")
            f = {"lane": tag, "severity": str(it.get("severity")).lower(),
                 "evidence": ev if isinstance(ev, list) else [ev]}
            f.update({k: it.get(k) for k in FIELDS if k in it})
            r["findings"].append(f)
        for t in d.get("triage_answers") or []:
            tid = t.get("id") or t.get("triage_id")
            if tid is None:
                raise SystemExit("%s: a triage answer has no id" % tag)
            if t.get("in_my_cluster") is False:
                continue
            triage.setdefault(tid, []).append(dict(t, lane=tag))
        for u in d.get("unresolved_uncertainty") or []:
            uncertain.append({"lane": tag, "item": u})
    out = {}
    for rid in sorted(rows, key=lambda x: (x.split("-")[0], int(x.split("-")[1]))):
        r = rows[rid]
        if r["findings"]:
            out["R4-" + rid] = {"id": "R4-" + rid, "row_id": rid,
                                "severity": max((f["severity"] for f in r["findings"]), key=lambda s: RANK.get(s, 0)),
                                "findings": r["findings"], "other_lanes": r["other_lanes"]}
    for tid in sorted(triage):
        out[tid] = {"id": tid, "severity": "question", "answers": triage[tid]}
    out["R4-UNCERTAINTY"] = {"id": "R4-UNCERTAINTY", "severity": "question", "items": uncertain}
    return out


if __name__ == "__main__":
    fin = HERE.parent / "primaries" / "finals"
    have = [(l, c, fin / ("final_%s_%s_e1.json" % (l, c))) for l, c in PLAN]
    have = [x for x in have if x[2].is_file()]
    F = extract(have)
    print(json.dumps({"finals": len(have), "ids": len(F), "rows_challenged": sum(1 for k in F if k.startswith("R4-W")),
                      "challenges": sum(len(v["findings"]) for k, v in F.items() if k.startswith("R4-W")),
                      "triage": {k: len(v["answers"]) for k, v in F.items() if k.startswith("TRIAGE")},
                      "uncertainty": len(F["R4-UNCERTAINTY"]["items"])}))
