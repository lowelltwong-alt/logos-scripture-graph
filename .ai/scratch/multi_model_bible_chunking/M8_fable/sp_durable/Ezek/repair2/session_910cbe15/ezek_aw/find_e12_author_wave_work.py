#!/usr/bin/env python3
"""Which #e12 rulings route work to the AUTHOR WAVE, and on which rows?

#e13's worklist_basis_per_class says the C1/C4/A2/A3/A7/A9/A10/A16/D1/D7/D10 family is "as ruled in #e12
(MEASURED census) plus the per-row orders in this file". v4 added the per-row orders from #e13. This finds the
#e12 half, which I had not looked at at all.

THE SELECTOR IS MECHANICAL, not my reading. Every #e12 ruling carries `execution_shape` and
`execution_timing`; A7's read "per_row_fix" and "author wave" and its ruling text names eleven rows for wording
fixes plus two for a false-ground replacement. So: select rulings whose timing mentions the author wave, then
take the rows their own ruling TEXT names.

WHY THIS IS NOT JUST "EVERY ROW THE RULING MENTIONS". A ruling names rows for several reasons - to fix, to
exempt, to cite as evidence. A7 names P10-008 explicitly as INSIDE the allowance, i.e. not a defect. So the
rows are reported per ruling for a human read, with the exempting phrases flagged, and nothing is installed
from a bare mention. Counting a mention as an order would be the mirror-image of the error that produced E-32:
over-collecting instead of under-collecting, and just as wrong.
"""
import json
import re
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
ROW = re.compile(r"P\d{2}-\d{3}")
d12 = json.loads((EZ / "ezek_controlling_agent_ruling_e12.v1.json").read_text(encoding="utf-8"))
w = json.loads((EZ / "author_wave_worklist.v4.json").read_text(encoding="utf-8"))

v4_by_row = {}
for i in w["items"]:
    v4_by_row.setdefault(i["row_id"], set()).add(i["cls"])

# phrases that mark a row as NOT needing work, so a mention near one is not read as an order
EXEMPT_HINTS = ("is inside it", "not a defect", "no change", "stands", "already", "correct", "exempt",
                "withdrawn", "is inside")

out_rulings = []
for r in d12.get("rulings", []):
    timing = str(r.get("execution_timing", "")).lower()
    shape = str(r.get("execution_shape", "")).lower()
    if "author wave" not in timing:
        continue
    text = str(r.get("ruling", ""))
    rows = sorted(set(ROW.findall(text)))
    # for each row, the ~90 characters around its first mention, so a human can see why it is named
    ctx = {}
    for rid in rows:
        m = re.search(re.escape(rid), text)
        s = max(0, m.start() - 60)
        frag = text[s:m.end() + 60].replace("\n", " ")
        ctx[rid] = {"context": frag,
                    "looks_exempting": any(h in frag.lower() for h in EXEMPT_HINTS),
                    "v4_classes_on_this_row": sorted(v4_by_row.get(rid, set()))}
    out_rulings.append({
        "class_id": r.get("class_id"), "execution_shape": shape, "execution_timing": timing,
        "blast_radius_rows": (r.get("blast_radius") or {}).get("rows"),
        "moves_seam": (r.get("blast_radius") or {}).get("moves_seam"),
        "rows_named_in_the_ruling_text": rows,
        "rows_named_count": len(rows),
        "per_row_context": ctx,
        "ruling_text": text,
    })

# the rows that carry NO v4 item at all: those are the clearest candidates for a missing item
never_in_v4 = {}
for r in out_rulings:
    for rid, c in r["per_row_context"].items():
        if not c["v4_classes_on_this_row"]:
            never_in_v4.setdefault(rid, []).append(r["class_id"])

out = {
    "schema": "ezek_e12_author_wave_work.v1",
    "why": ("#e13's worklist_basis_per_class makes the C1/C4/A2/A3/A7/A9/A10/A16/D1/D7/D10 family 'as ruled in "
            "#e12 (MEASURED census) plus the per-row orders in this file'. v4 added #e13's per-row orders. "
            "This is the #e12 half, which the worklist had never been checked against."),
    "selector": ("rulings whose execution_timing mentions the author wave, then the rows their own ruling TEXT "
                 "names - mechanical, not my reading of which classes matter"),
    "caution_stated_up_front": ("a ruling names rows to FIX, to EXEMPT and to cite as EVIDENCE. A7 names "
                                "P10-008 as inside the allowance, i.e. not a defect. Nothing here is installed "
                                "from a bare mention; counting a mention as an order would be the mirror image "
                                "of the error that produced E-32."),
    "rulings_routing_work_to_the_author_wave": len(out_rulings),
    "summary": [{"class_id": r["class_id"], "shape": r["execution_shape"],
                 "rows_named": r["rows_named_count"],
                 "blast_radius_rows": r["blast_radius_rows"],
                 "rows_with_no_v4_item": [rid for rid, c in r["per_row_context"].items()
                                          if not c["v4_classes_on_this_row"]]}
                for r in out_rulings],
    "rows_named_by_an_author_wave_ruling_with_NO_v4_item_at_all": {
        "count": len(never_in_v4), "detail": never_in_v4},
    "detail": out_rulings,
    "tier": "MEASURED over the pinned #e12 ruling; which named rows are ORDERS rather than mentions needs a "
            "read, and the context strings are provided for it",
}
(HERE / "e12_author_wave_work.v1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                                   encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("rulings_routing_work_to_the_author_wave", "summary",
                                      "rows_named_by_an_author_wave_ruling_with_NO_v4_item_at_all")},
                 ensure_ascii=False, indent=1))
