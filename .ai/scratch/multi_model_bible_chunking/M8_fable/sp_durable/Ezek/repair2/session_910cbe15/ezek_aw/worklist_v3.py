#!/usr/bin/env python3
"""Worklist v3: add the A6 items #e13 R3's union requires and that v2's basis did not carry.

WHY THERE IS A v3 AT ALL, stated plainly because a silent overwrite is how E-30 happened. v2's A6 class came
from the boss audit's a6_measured_attachment - 170 runs on 86 rows, the boss's own MEASURED sweep. But R3 does
not say "the boss's sweep". It says:

    the worklist is the arm's output UNIONED with every peer's hand-named run ... filtered by A6-b

So the boss's sweep is a THIRD measurement, and using it alone makes the arm and the peers alternatives when the
ruling makes them union MEMBERS. Measured (a6_union_check.v2.json, a6_peer_union.v1.json):

  * the ARM names 95 runs on 66 rows; ONE has no overlapping run in v2's A6 class (P04-005).
  * the PEERS, as a true superset filtered to strings that actually occur in the WEB, name 39 runs on 24 rows;
    SEVEN have no overlapping run in v2's A6 class.

Eight items. v2 is kept; v3 supersedes it, and a new negative fixture makes the union coverage a BUILD GATE so
the next version cannot quietly lose it again.

TWO MEASUREMENT MISTAKES ON THE WAY HERE, both mine, both recorded because the numbers are still in my transcript
and someone reading it deserves to know which were real:
  * comparing run TEXT exactly reported 66 of 96 arm runs "not in" the boss set. The three sweeps name run
    EXTENTS independently, so the same site at a different extent counted as a miss. 66 measured my comparison
    rule; the real figure by overlap is 1.
  * collecting peer runs only from A6-context strings gave 10 WEB runs; collecting from the whole item gives 39.
    A superset argument is worthless if the superset is not actually a superset, so the narrow collection was a
    real defect and not a conservative choice.
"""
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(EZ / "tools"))
V2 = EZ / "author_wave_worklist.v2.json"
OUT = EZ / "author_wave_worklist.v3.json"
NOW = datetime.now(timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()          # noqa: E731

v2 = json.loads(V2.read_text(encoding="utf-8"))
arm = json.loads((HERE / "a6_union_check.v2.json").read_text(encoding="utf-8"))
peer = json.loads((HERE / "a6_peer_union.v1.json").read_text(encoding="utf-8"))

arm_resid = arm["containment_three_ways"][
    "2_OVERLAP_one_run_contains_the_other_on_the_same_row"]["the_residue"]
peer_resid = peer["coverage_by_overlap"]["sample"]
assert len(peer_resid) == peer["coverage_by_overlap"]["not_covered_by_the_worklists_a6_class"], \
    "the peer residue sample is truncated; the builder would install fewer items than were measured"

items = list(v2["items"])
added = []
for r in arm_resid:
    it = {"row_id": r["row"], "cls": "A6_UNION",
          "action": ("check this run at the row: it is named by the CORRECTED A6 ARM and no run in the boss's "
                     "sweep overlaps it. Install the convention (double curly quotes plus an in-field web: "
                     "reference) unless A6-b exempts it - that is, unless the run is nothing but the WEB's "
                     "fixed rendering of a counted device or an addressee title AND this row names the device. "
                     "AUTHOR JUDGEMENT."),
          "source": "the corrected A6 arm (P3), as #e13 R3's first union member",
          "tier": "MEASURED for run existence by the arm; the duty is applied at the row under A6/A6-b",
          "run": r["run"], "kind": "AUTHOR_JUDGEMENT", "union_member": "arm", "moves_seam": False}
    items.append(it)
    added.append(it)
for r in peer_resid:
    it = {"row_id": r["row"], "cls": "A6_UNION",
          "action": ("check this run at the row: a PEER quoted it and it occurs in the WEB, and no run in the "
                     "boss's sweep overlaps it. Install the convention unless A6-b exempts it. AUTHOR "
                     "JUDGEMENT."),
          "source": "a peer's hand-named run, as #e13 R3's second union member",
          "tier": ("EXTRACTED from the peer packet and MEASURED to occur in the WEB; whether the peer named it "
                   "AS an A6 run is the orchestrator's inference from its presence in the packet, and is "
                   "disclosed as such"),
          "run": r["string"], "kind": "AUTHOR_JUDGEMENT", "union_member": "peer", "moves_seam": False}
    items.append(it)
    added.append(it)


# ---------------------------------------------------------------- the new fixture, as a BUILD GATE
def fixture_a6_union_covered():
    """Every run named by the arm or by a peer (WEB-filtered) is covered by an A6 or A6_UNION item on its row.
    This is the regression for v2's basis using the boss's sweep alone where R3 orders a union."""
    a6_rows = {i["row_id"] for i in items if i["cls"] in ("A6", "A6_UNION")}
    named = [(r["row"], r["run"]) for r in arm_resid] + [(r["row"], r["string"]) for r in peer_resid]
    if not named:
        return False
    installed = {(i["row_id"], i.get("run")) for i in items if i["cls"] == "A6_UNION"}
    return all((row, run) in installed for row, run in named) and all(row in a6_rows for row, _ in named)


def fixture_v2_items_preserved():
    """v3 is an ADDITION. Every v2 item must still be present, byte-identical, so a version bump cannot quietly
    drop work - which is exactly what E-30's change table did in prose."""
    v2s = [json.dumps(i, sort_keys=True, ensure_ascii=False) for i in v2["items"]]
    v3s = {json.dumps(i, sort_keys=True, ensure_ascii=False) for i in items}
    return all(s in v3s for s in v2s) and len(items) == len(v2["items"]) + len(added)


FIX = [("R3's A6 union is covered: every arm-named and peer-named run has an item on its row",
        fixture_a6_union_covered,
        "v2 built the A6 class from the boss's sweep ALONE, where R3 makes the arm and the peers union MEMBERS; "
        "one arm run and seven peer runs had no item"),
       ("every v2 item survives into v3 byte-identical", fixture_v2_items_preserved,
        "a version bump that drops work while claiming to add it is ledger row E-30")]
results = [{"fixture": n, "fired": bool(f()), "guards_against": w} for n, f, w in FIX]
carried = v2["negative_fixtures"]["results"]
failed = [r for r in results if not r["fired"]]

doc = dict(v2)
doc["schema"] = "m8_author_wave_worklist.v3"
doc["supersedes"] = "author_wave_worklist.v2.json (kept; never overwritten), which superseded v1 (also kept)"
doc["built_at"] = NOW
doc["what_changed_from_v2"] = {
    "added": len(added),
    "class": "A6_UNION",
    "why": ("#e13 R3 makes the corrected A6 ARM and the PEERS' hand-named runs union MEMBERS of the A6 "
            "worklist. v2's A6 class came from the boss audit's own sweep alone, which is a third measurement. "
            "Measured: one arm-named run and seven peer-named runs have no overlapping run in v2's A6 class."),
    "arm_side": arm_resid,
    "peer_side": peer_resid,
    "nothing_removed": "every v2 item is carried byte-identical; a fixture asserts it",
    "two_measurement_mistakes_disclosed": [
        "exact run-text comparison reported 66 of 96 arm runs missing; the three sweeps name run EXTENTS "
        "independently, so that number measured the comparison rule. By overlap the real figure is 1.",
        "collecting peer runs only from A6-context strings gave 10 WEB-occurring runs; collecting from the "
        "whole item gives 39. A superset argument requires an actual superset, so the narrow collection was a "
        "defect and not a conservative choice."],
}
doc["a6_basis"] = {
    "order": "#e13 R3",
    "boss_sweep_runs": 170, "boss_sweep_rows": 86,
    "arm_runs": arm["sets"]["arm_runs"], "arm_rows": arm["sets"]["arm_rows"],
    "peer_web_occurring_runs": peer["superset_collected"]["strings_that_ARE_web_runs"],
    "peer_rows": peer["superset_collected"]["rows"],
    "union_additions": len(added),
    "a6b_filter": "applied at the ROW by the author, not here - A6-b's exemption is conditional on the row "
                  "naming the device, which the tool cannot judge",
}
doc["negative_fixtures"] = {
    "why": v2["negative_fixtures"]["why"],
    "results": carried + results,
    "all_fired": all(r["fired"] for r in carried + results),
    "note": "the nine v2 fixtures are carried and re-reported; the two new ones are this version's gates",
}
doc["counts"] = {
    "items_total": len(items),
    "by_class": dict(Counter(i["cls"] for i in items)),
    "a4_by_class": v2["counts"]["a4_by_class"], "a4_by_kind": v2["counts"]["a4_by_kind"],
    "a6_by_kind": v2["counts"]["a6_by_kind"],
    "rows_touched": len({i["row_id"] for i in items if i["row_id"] != "*"}),
    "blocked_classes": [i["cls"] for i in items if i.get("blocked")],
    "items_moving_a_seam": sum(1 for i in items if i.get("moves_seam")),
}
doc["items"] = items

OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"written": OUT.name, "sha256": sha(OUT), "bytes": OUT.stat().st_size,
                  "added": len(added), "counts": doc["counts"],
                  "new_fixtures": [{"fired": r["fired"], "fixture": r["fixture"]} for r in results],
                  "all_fixtures_fired": doc["negative_fixtures"]["all_fired"],
                  "BUILD": "FAILED" if failed else "OK"}, indent=1, ensure_ascii=False))
if failed:
    raise SystemExit(1)
