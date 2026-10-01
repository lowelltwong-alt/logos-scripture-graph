#!/usr/bin/env python3
"""Slice the author wave into lanes, one deliverable per lane, and write each lane's own worklist file.

THE DESIGN TENSION THIS RESOLVES, stated because it is a real one in the ruling and not a preference.
#e13's order_of_execution is by SWEEP - "every sweep is its own execution with executed/ordered parity digits
(E-18)", confidence first so later validator runs see final levels, grounds before disclosures so wording does
not collide. But an AUTHOR needs a whole row at once: the ROLE token on a reference depends on what the
rationale now says, and A9/A16 weighing and the A4 installs are the same judgement seen twice.

So the two are separated by WHO does what:
  * AUTHORS work by ROW LANE and produce a deliverable covering every class on their rows, because judgement
    needs the whole row.
  * THE ORCHESTRATOR applies BY SWEEP, in the ruling's order, pooling every lane's edits for that class into
    one guarded mutation with its own parity digits.
Neither half is compromised, and the parity digits stay meaningful because they count a sweep, not a lane.

LANE ASSIGNMENT is by contiguous decision_id, so one author sees a contiguous stretch of the book and its
seams. Lanes are balanced on ITEM COUNT rather than row count, because a row with 11 A4 citations is not the
same work as a row with one.
"""
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
OUTDIR = HERE / "lanes"
OUTDIR.mkdir(exist_ok=True)
N_LANES = 6

W = json.loads((EZ / "author_wave_worklist.v4.json").read_text(encoding="utf-8"))
rows = [json.loads(l) for l in (EZ / "repair" / "rows_v7_cwo24.jsonl")
        .read_text(encoding="utf-8").splitlines() if l.strip()]
order = [r["decision_id"] for r in rows]
rank = {rid: i for i, rid in enumerate(order)}

by_row = defaultdict(list)
for it in W["items"]:
    if it["row_id"] == "*":
        continue
    by_row[it["row_id"]].append(it)

# ---- balance contiguous stretches on item count
touched = sorted(by_row, key=lambda r: rank.get(r, 10 ** 6))
total = sum(len(v) for v in by_row.values())
target = total / N_LANES
lanes, cur, cur_n = [], [], 0
for rid in touched:
    n = len(by_row[rid])
    if cur and cur_n + n > target and len(lanes) < N_LANES - 1:
        lanes.append(cur)
        cur, cur_n = [], 0
    cur.append(rid)
    cur_n += n
if cur:
    lanes.append(cur)

manifest = []
for i, lane_rows in enumerate(lanes, 1):
    lane_items = [it for rid in lane_rows for it in by_row[rid]]
    # the row bytes the author needs, and nothing else
    lane_row_objs = [r for r in rows if r["decision_id"] in set(lane_rows)]
    doc = {
        "lane": "ezek_author_l%02d" % i,
        "rows": lane_rows,
        "row_count": len(lane_rows),
        "item_count": len(lane_items),
        "by_class": dict(Counter(it["cls"] for it in lane_items)),
        "span_range": "%s .. %s" % (lane_row_objs[0]["span"], lane_row_objs[-1]["span"]),
        "your_rows": lane_row_objs,
        "your_worklist_items": lane_items,
        "role_vocabulary": W["a4_basis"]["role_vocabulary"],
        "rows_file_sha256": W["bound_to"]["rows_sha256"],
        "worklist_sha256": hashlib.sha256((EZ / "author_wave_worklist.v4.json").read_bytes()).hexdigest(),
        "reminder": ("You produce a DELIVERABLE, not a mutation. Every proposed edit names its field, its "
                     "EXACT expected_before value copied from your_rows, and its new value. The orchestrator "
                     "applies it under the guarded mutation, pooled by sweep. An edit addressing span, "
                     "osis_start, osis_end, decision_id or any writer-identity field is REFUSED by the "
                     "harness - you have no authority to move a seam."),
    }
    p = OUTDIR / ("lane_%02d_worklist.json" % i)
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    manifest.append({"lane": doc["lane"], "file": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                     "rows": len(lane_rows), "items": len(lane_items), "by_class": doc["by_class"],
                     "first_row": lane_rows[0], "last_row": lane_rows[-1],
                     "bytes": p.stat().st_size})

# ---- checks: every item lands in exactly one lane, and no row is split across lanes
assigned = [it for m, lane_rows in zip(manifest, lanes) for rid in lane_rows for it in by_row[rid]]
seen_rows = [rid for lane_rows in lanes for rid in lane_rows]
checks = {
    "every_item_assigned_exactly_once": len(assigned) == total,
    "no_row_in_two_lanes": len(seen_rows) == len(set(seen_rows)),
    "every_touched_row_assigned": set(seen_rows) == set(by_row),
    "starred_items_excluded": len([i for i in W["items"] if i["row_id"] == "*"]),
    "total_items_in_worklist": len(W["items"]),
    "items_distributed": total,
}
(HERE / "lane_manifest.json").write_text(
    json.dumps({"lanes": manifest, "checks": checks, "n_lanes": len(manifest)},
               ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"lanes": [{k: m[k] for k in ("lane", "rows", "items", "first_row", "last_row", "by_class")}
                            for m in manifest], "checks": checks}, indent=1, ensure_ascii=False))
