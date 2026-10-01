#!/usr/bin/env python3
"""Apply the author wave: pool six lanes' edits by SWEEP, simulate the whole plan, then mutate in order.

WHY POOLED BY SWEEP AND NOT BY LANE. #e13 orders the sweeps - confidence first so every later validator run
sees final levels, grounds before disclosures so wording does not collide - and E-18 wants executed/ordered
parity per sweep. Authors worked by ROW because judgement needs the whole row. So the orchestrator pools.

WHY CROSS-LANE CONFLICTS ARE IMPOSSIBLE HERE, stated rather than assumed: the lane slicer asserted
no_row_in_two_lanes, so two lanes never touch one row. Within a lane, the lane ordered its own edits and three
lanes reported edits whose expected_before deliberately assumes an earlier sweep's output.

THE SEQUENCE. Simulate the entire plan in memory first; only if every sweep validates against the state its
predecessors produce does anything reach disk. An ordering error then costs a report instead of a half-applied
corpus. Each sweep that does reach disk gets its own receipt with its own parity digits and its own
preimage/postimage pair.

WHAT THIS DOES NOT DO: judge whether the new prose is true. Six lanes' escalations and the spot wave at full
coverage of every changed row are where that happens.
"""
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import guarded_apply as GA                                                     # noqa: E402

HERE = Path(__file__).resolve().parent
EZ = GA.EZ
PIN = "25cdba568d98ec60aa719606be7b273e6a7c7256c55b79a3c579ada3c21d0ecc"
SWEEP_ORDER = ["confidence", "grounds", "marks", "a4", "a6", "disclosures", "vocab"]
NOW = datetime.now(timezone.utc).isoformat()

LANES = [
    ("ezek_author_l01", HERE.parent / "ezek_l01_work_7b3e" / "ezek_author_l01_deliverable.json",
     "34ed205eac2ef8f06e063eddbc707e5486855179dff84ec687ff8b10156773d5"),
    ("ezek_author_l02", HERE.parent / "ezek_l02_work_7b3f" / "ezek_author_l02_deliverable.json",
     "2e2215e2ddd63c2a68e3c951ba8ea0c65a946ba9307741a1c6197f8b29daa630"),
    ("ezek_author_l03", HERE.parent / "ezek_l03_work_4c9a" / "ezek_author_l03_deliverable.json",
     "71554cefa2a65c348f2c99864f8f2577ebbd15d497e4fb3203cddd4d4331277a"),
    ("ezek_author_l04", HERE.parent / "ezek_l04_work_7b3c" / "ezek_author_l04_deliverable.json",
     "2378ecf952b6492b49c39713f360e5f49a5f39e95cfedd47275fe4a4c572af5a"),
    ("ezek_author_l05", HERE.parent / "ezek_l05_work_7b3e" / "ezek_author_l05_deliverable.json",
     "fd8ad6330bf8ec34f8891213b8437dec7ddf5c73f60c65124e9ebd1151513a3a"),
    ("ezek_author_l06", HERE.parent / "ezek_l06_work_7c3f" / "ezek_author_l06_deliverable.json",
     "e7bec54bb400ff61335ca753fd5015a7bdb396cfea967307d84e6cbd8d14be84"),
]

# ---- load, verifying each lane's digest AGAIN at apply time
by_sweep = defaultdict(list)
lane_report, rows_by_lane = {}, {}
for lane, path, reported in LANES:
    measured = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if measured != reported:
        raise SystemExit("REFUSED: %s is %s, not the validated %s" % (lane, measured, reported))
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    edits = d.get("edits") or []
    for e in edits:
        e = dict(e, _lane=lane)
        by_sweep[str(e.get("sweep", "?"))].append(e)
    lane_report[lane] = {"edits": len(edits), "sha256": measured,
                         "by_sweep": dict(Counter(str(e.get("sweep")) for e in edits)),
                         "items_discharged": len(d.get("items_discharged") or []),
                         "items_not_discharged": len(d.get("items_NOT_discharged") or []),
                         "escalations": len(d.get("escalations") or [])}
    rows_by_lane[lane] = {e.get("row_id") for e in edits}

# ---- no two lanes may touch one row; asserted, not assumed
overlap = []
ls = list(rows_by_lane)
for i in range(len(ls)):
    for j in range(i + 1, len(ls)):
        both = rows_by_lane[ls[i]] & rows_by_lane[ls[j]]
        if both:
            overlap.append({"lanes": [ls[i], ls[j]], "rows": sorted(both)})
if overlap:
    raise SystemExit("REFUSED: lanes overlap on rows, so pooling could reorder an expected_before:\n"
                     + json.dumps(overlap, indent=1))

unknown = [s for s in by_sweep if s not in SWEEP_ORDER]
if unknown:
    raise SystemExit("REFUSED: unknown sweep names %r" % unknown)
plan = [(s, by_sweep[s]) for s in SWEEP_ORDER if s in by_sweep]

# ---- SIMULATE the whole plan before touching disk
sim = GA.simulate_plan(plan, PIN)
print(json.dumps({"simulation": {"ok": sim["ok"],
                                 "sweeps": [{k: v for k, v in s.items() if k != "problems"}
                                            for s in sim["sweeps"]],
                                 "final_digest_if_applied": sim.get("final_digest_if_applied"),
                                 "stopped_at": sim.get("stopped_at")}}, indent=1)[:2600])
if not sim["ok"]:
    raise SystemExit("\nREFUSED: the plan does not validate in sweep order; NOTHING was applied.")

if "--apply" not in sys.argv:
    print("\nSIMULATION CLEAN. Re-run with --apply to mutate. Expected final digest: %s"
          % sim["final_digest_if_applied"])
    raise SystemExit(0)

# ---- apply, one sweep at a time, each with its own receipt
RECEIPTS = EZ / "author" / "ezek_author_wave_sweep_receipts.jsonl"
RECEIPTS.parent.mkdir(exist_ok=True)
pooled_note = ("some edits carry a component belonging to a LATER sweep, because a citation install and a "
               "quotation repair can land on one field and cannot then be two independent edits. Those edits "
               "are counted under their declared sweep; queue E13-76 records which and why, so these parity "
               "digits are not read as a clean per-class count.")
applied, pre = [], PIN
for name, edits in plan:
    r = GA.apply_edits(edits, pre, "author_wave_%s" % name, ordered_count=len(edits), apply=True)
    r["lanes_contributing"] = dict(Counter(e["_lane"] for e in edits))
    r["pooling_disclosure"] = pooled_note
    r["recorded_at"] = NOW
    with RECEIPTS.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    applied.append({k: r[k] for k in ("sweep", "ordered", "executed", "e18_parity_digits", "rows_touched",
                                      "fields_touched", "preimage_sha256",
                                      "postimage_sha256_measured_from_disk")})
    pre = r["postimage_sha256_measured_from_disk"]

final = GA.sha_file(GA.ROWS)
out = {
    "schema": "ezek_author_wave_apply.v1",
    "preimage": PIN, "postimage": final,
    "postimage_equals_simulation_prediction": final == sim["final_digest_if_applied"],
    "sweeps_applied": applied,
    "total_edits": sum(len(e) for _, e in plan),
    "rows_touched": len({e["row_id"] for _, es in plan for e in es}),
    "lanes": lane_report,
    "rows_count_unchanged": len(GA.load_rows()) == 145,
    "pooling_disclosure": pooled_note,
    "recorded_at": NOW,
}
(HERE / "author_wave_apply.v1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                                encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("preimage", "postimage", "postimage_equals_simulation_prediction",
                                      "total_edits", "rows_touched", "rows_count_unchanged")}, indent=1))
print()
for a in applied:
    print("  %-26s %-8s rows=%-3d  -> %s" % (a["sweep"], a["e18_parity_digits"], a["rows_touched"],
                                             a["postimage_sha256_measured_from_disk"][:16]))
