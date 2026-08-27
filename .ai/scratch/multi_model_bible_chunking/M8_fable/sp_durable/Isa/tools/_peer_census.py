"""Deterministic census over Isaiah peer-wave outputs (m8-mesh-r3).

Checks each landed peer_NN.json / peer_NN_r2.json against
peer_assignments.json: attempt id, role, clusters, exact ruling coverage of
the assigned row list, the <=8 cap, deferred_row_ids exactness, ruling-value
validity, summary arithmetic, and supported-sample presence. Prints a wave
aggregate. Usage: python _peer_census.py [peer numbers...] (default: all
landed files).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SP_ISA = os.path.dirname(HERE)
REVIEWS = os.path.join(SP_ISA, "reviews")

VALID_RULINGS = {"uphold", "refine", "refute", "escalate"}
VALID_SEV = {"high", "medium", "low", "n/a"}

with open(os.path.join(SP_ISA, "peer_assignments.json"), encoding="utf-8") as f:
    ASSIGN = {p["peer"]: p for p in json.load(f)["peers"]}

def check_file(nn, round_no):
    a = ASSIGN[nn]
    fname = a["output_r1"] if round_no == 1 else a["output_r2"]
    expected_attempt = a["attempt_id_r1"] if round_no == 1 else a["attempt_id_r2"]
    expected_rows = a["r1_row_ids"] if round_no == 1 else a["expected_deferred_row_ids"]
    expected_deferred = a["expected_deferred_row_ids"] if round_no == 1 else []
    path = os.path.join(REVIEWS, fname)
    defects = []
    if not os.path.exists(path):
        return None, ["MISSING: " + fname]
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
    except Exception as e:  # noqa: BLE001
        return None, ["PARSE FAIL %s: %s" % (fname, e)]
    if d.get("attempt_id") != expected_attempt:
        defects.append("attempt_id %r != %r" % (d.get("attempt_id"), expected_attempt))
    if d.get("role") != "peer":
        defects.append("role %r" % d.get("role"))
    if sorted(d.get("clusters", [])) != sorted(a["clusters"]):
        defects.append("clusters %r != %r" % (d.get("clusters"), a["clusters"]))
    rulings = d.get("rulings", [])
    if len(rulings) > 8:
        defects.append("CAP VIOLATION: %d rulings" % len(rulings))
    ruled = [r.get("row_id") for r in rulings]
    if sorted(ruled) != sorted(set(ruled)):
        defects.append("duplicate ruling row_ids")
    if sorted(set(ruled)) != sorted(expected_rows):
        defects.append("coverage: ruled %s expected %s" % (sorted(set(ruled)), sorted(expected_rows)))
    for r in rulings:
        if r.get("ruling") not in VALID_RULINGS:
            defects.append("%s: bad ruling %r" % (r.get("row_id"), r.get("ruling")))
        if r.get("severity_final") not in VALID_SEV:
            defects.append("%s: bad severity %r" % (r.get("row_id"), r.get("severity_final")))
        if r.get("ruling") in ("uphold", "refine") and not r.get("remedy"):
            defects.append("%s: %s without remedy" % (r.get("row_id"), r.get("ruling")))
        if not r.get("grounds"):
            defects.append("%s: empty grounds" % r.get("row_id"))
    deferred = d.get("deferred_row_ids", [])
    if sorted(deferred) != sorted(expected_deferred):
        defects.append("deferred %s != expected %s" % (sorted(deferred), sorted(expected_deferred)))
    s = d.get("summary", {})
    counts = {k: sum(1 for r in rulings if r.get("ruling") == k) for k in VALID_RULINGS}
    if s.get("challenges_adjudicated") not in (len(rulings), sum(counts.values())):
        defects.append("summary adjudicated %r vs %d rulings" % (s.get("challenges_adjudicated"), len(rulings)))
    for k in VALID_RULINGS:
        if s.get(k) != counts[k]:
            defects.append("summary %s %r vs counted %d" % (k, s.get(k), counts[k]))
    if round_no == 1 and a["supported_sample_row_ids"]:
        got = [x.get("row_id") for x in d.get("supported_sample", [])]
        for rid in a["supported_sample_row_ids"]:
            if rid not in got:
                defects.append("missing supported_sample %s" % rid)
    return d, defects

def main():
    peers = sys.argv[1:] or sorted(ASSIGN)
    agg = {k: 0 for k in VALID_RULINGS}
    total_rulings = 0
    landed = 0
    all_defects = []
    sample_results = []
    for nn in peers:
        for rnd in (1, 2):
            if rnd == 2 and not ASSIGN[nn]["output_r2"]:
                continue
            d, defects = check_file(nn, rnd)
            tag = "peer_%s%s" % (nn, "" if rnd == 1 else "_r2")
            if d is None:
                if defects and defects[0].startswith("MISSING"):
                    print("%s: not landed" % tag)
                else:
                    all_defects.extend("%s: %s" % (tag, x) for x in defects)
                continue
            landed += 1
            rl = d.get("rulings", [])
            total_rulings += len(rl)
            for r in rl:
                if r.get("ruling") in agg:
                    agg[r["ruling"]] += 1
            for x in d.get("supported_sample", []):
                sample_results.append((x.get("row_id"), x.get("result")))
            status = "GREEN" if not defects else "DEFECTS: " + "; ".join(defects)
            print("%s: %d rulings, %s" % (tag, len(rl), status))
            all_defects.extend("%s: %s" % (tag, x) for x in defects)
    print("---")
    print("landed files: %d | rulings: %d | uphold %d / refine %d / refute %d / escalate %d"
          % (landed, total_rulings, agg["uphold"], agg["refine"], agg["refute"], agg["escalate"]))
    if sample_results:
        print("supported samples:", sample_results)
    print("CENSUS %s (%d defect lines)" % ("GREEN" if not all_defects else "RED", len(all_defects)))
    return 1 if all_defects else 0

if __name__ == "__main__":
    raise SystemExit(main())
