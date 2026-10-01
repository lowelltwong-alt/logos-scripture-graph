#!/usr/bin/env python3
"""R3's SECOND union member: every peer's hand-named A6 run, and whether the worklist covers it.

#e13 R3 names the peers' counts: peer_01 34, peer_04 11 (of six words or more), peer_07 5, peer_09 20 (defective
of 27), peer_10 38, peer_11 9, "and the others as their packets name them". As with A4, the ruling gives COUNTS
and not lists, and the packets are schema-heterogeneous. So the same method applies: build a SUPERSET of every
run-like string any peer names in an A6/web_quotes context, and test whether the worklist's A6 class covers it.
If a superset is covered, every subset is - including the one the ruling meant.

Coverage is by OVERLAP on the same row, because the arm, the boss and the peers all name run EXTENTS
independently and a different extent is the same site. (Exact-text comparison reported 66 phantom misses against
the boss's sweep before this was fixed; see a6_union_check.v2.json.)
"""
import json
import re
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
att = json.loads((EZ / "ezek_boss_audit.v1.json").read_text(encoding="utf-8"))["a6_measured_attachment"]
arm_resid = json.loads((HERE / "a6_union_check.v2.json").read_text(encoding="utf-8"))
R3_COUNTS = {"peer_01": 34, "peer_04": 11, "peer_07": 5, "peer_09": 20, "peer_10": 38, "peer_11": 9}


def norm(s):
    return " ".join(re.sub(r"[^\w\s']", " ", str(s).lower()).split())


boss_runs = {}
for rid, runs in att["by_row"].items():
    for r in runs:
        boss_runs.setdefault(rid, []).append(norm(r.get("run", "")))

# a run-like English string: 5+ words of latin letters. The A6 predicate is 5+ consecutive words, so anything
# shorter cannot be an A6 run and is not collected.
RUNLIKE = re.compile(r"(?:[A-Za-z][A-Za-z']*\s+){4,}[A-Za-z][A-Za-z']*")
per_peer, superset = {}, {}
for n in range(1, 12):
    d = json.loads((EZ / "reviews" / ("peer_%02d.json" % n)).read_text(encoding="utf-8"))
    raw = d.get("items") or {}
    pairs = list(raw.items()) if isinstance(raw, dict) else \
        [(str(x.get("row_id") or x.get("row") or "?"), x) for x in raw if isinstance(x, dict)]
    cnt = 0
    for rid, it in pairs:
        # A TRUE SUPERSET: collect from the ENTIRE item, not only from A6-context text. The earlier version
        # restricted collection to strings near "A6"/"web_quotes"/"quotation", which would have missed a run a
        # peer quoted while discussing something else - and a superset argument is worthless if the superset is
        # not actually a superset. The WEB-occurrence filter below is what makes precision, so collection can
        # afford to be total.
        blob = [json.dumps(it, ensure_ascii=False)]
        for b in blob:
            for m in RUNLIKE.finditer(b):
                s = norm(m.group(0))
                if len(s.split()) >= 5:
                    superset.setdefault(rid, set()).add(s)
                    cnt += 1
    per_peer["peer_%02d" % n] = cnt

# ---- THE FILTER THAT MAKES THE SUPERSET MEAN ANYTHING.
# The raw superset is 1231 strings and almost all of them are the PEERS' OWN PROSE ("and no parashah mark is
# recorded on any of"), not quotations of the translation. A6's predicate is 5+ consecutive words identical to
# the WEB, so a peer's hand-named run must actually OCCUR IN THE WEB TEXT. Intersecting with the WEB converts a
# noisy superset into a precise one by a mechanical test rather than by my judgement about which strings "look
# like" quotations.
# MEASURED PATH, not assumed: the A6 arm reads the translation through ezek_lib.load_verse_maps(), which loads
# tools/verse_map_web.json (WEB-keyed). My first attempt guessed Ezek_web.txt and got FileNotFoundError - the
# right move was to read what the arm itself uses rather than invent a filename.
WEB = EZ / "tools" / "verse_map_web.json"
_wm = json.loads(WEB.read_text(encoding="utf-8"))
_vals = _wm.values() if isinstance(_wm, dict) else _wm
web_norm = norm(" ".join(
    (v.get("text") or v.get("web") or v.get("t") or "") if isinstance(v, dict) else str(v) for v in _vals))
before = {rid: set(v) for rid, v in superset.items()}
superset = {rid: {s for s in v if s in web_norm} for rid, v in superset.items()}
superset = {rid: v for rid, v in superset.items() if v}
filtered_out = sum(len(v) for v in before.values()) - sum(len(v) for v in superset.values())

n_sup = sum(len(v) for v in superset.values())
miss = []
for rid, runs in superset.items():
    b = boss_runs.get(rid, [])
    for r in runs:
        if not any(r in x or x in r for x in b):
            miss.append((rid, r))

out = {
    "schema": "ezek_a6_peer_union.v1",
    "order": "#e13 R3's second union member: every peer's hand-named A6 run",
    "method": ("the ruling gives COUNTS not lists and the packets are schema-heterogeneous, so this builds a "
               "SUPERSET of every 5+-word English run-like string any peer names in an A6/web_quotes context "
               "and tests coverage by OVERLAP on the same row. A superset that is covered covers every subset, "
               "including the one the ruling meant. The superset deliberately OVER-collects: it will pull in "
               "ordinary prose sentences that are not runs at all, so a low miss count is strong evidence and a "
               "high one needs reading before it means anything."),
    "r3_stated_counts": R3_COUNTS,
    "superset_collected": {
        "raw_strings_before_the_web_filter": sum(len(v) for v in before.values()),
        "discarded_because_they_do_not_occur_in_the_WEB": filtered_out,
        "strings_that_ARE_web_runs": n_sup, "rows": len(superset),
        "per_peer_raw_hits_before_filter": per_peer,
        "why_the_filter": ("A6's predicate is 5+ consecutive words identical to the WEB, so a hand-named run "
                           "must OCCUR in the WEB. Without this filter the superset is 1231 strings and almost "
                           "all are the peers' own prose - a number that measures my collection rule and not "
                           "the worklist. The filter is mechanical, not a judgement about which strings look "
                           "like quotations."),
    },
    "coverage_by_overlap": {
        "not_covered_by_the_worklists_a6_class": len(miss),
        "rows_affected": len({r for r, _ in miss}),
        "sample": [{"row": r, "string": t[:90]} for r, t in sorted(miss)[:25]],
    },
    "arm_side_residue_from_v2": arm_resid["containment_three_ways"][
        "2_OVERLAP_one_run_contains_the_other_on_the_same_row"]["the_residue"],
    "tier": "MEASURED; the collection rule is the orchestrator's and over-collects by design, which is stated "
            "so the number is read correctly",
}
(HERE / "a6_peer_union.v1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                            encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("r3_stated_counts", "superset_collected", "coverage_by_overlap",
                                      "arm_side_residue_from_v2")}, ensure_ascii=False, indent=1)[:3000])
