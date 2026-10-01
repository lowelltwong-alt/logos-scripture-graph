#!/usr/bin/env python3
"""Build the micro docket + micro orders from the spot packets (orchestrator; deterministic aggregation, the
orchestrator's delegated judgment recorded per finding). spot/micro_docket.json: every finding keyed by row with
lane, E-class, severity, defective_text, byte_evidence, proposed_cure, and a DISPOSITION: order (prose/refs/oss
cure) | record_only (span proposal outside the ruled strategy, a calibration change not ordered, a duplicate of an
already-ordered cure, or a proposal the orchestrator rejects with a reason) | genuine_warn (a validator WARN the lane
judged genuine). Span/unit_type/confidence changes are NEVER ordered by this builder (the fields stay closed to the
micro authors; an accepted span proposal would need an explicit orchestrator order in a separate file).
spot/orders_micro_NN.json: <=8 rows per agent, canonical order, each row with current_row (rows_v3) and its ordered
findings. Prints the COUNTS. Usage: _build_micro_docket.py"""
import json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
rows = [json.loads(l) for l in (HERE / "rows_v3.jsonl").read_text(encoding="utf-8-sig").splitlines() if l.strip()]
by = {r["decision_id"]: r for r in rows}; order = [r["decision_id"] for r in rows]
SPAN_WORDS = re.compile(r"\b(re-?span|move the (front|rear|opening|closing) seam|merge (this|the) row|split (this|the) row|change the span|extend the span|shrink the span|new span)\b", re.I)
FIELD_WORDS = re.compile(r"\b(confidence|unit_type|parent_collection)\b", re.I)
docket = {}
seen = set()
for sn in ("S1", "S2", "S3", "S4", "S5", "S6", "S7"):
    p = HERE / "spot" / f"spot_{sn}.json"
    if not p.is_file(): continue
    d = json.loads(p.read_text(encoding="utf-8-sig"))
    for i, f in enumerate(d.get("findings", [])):
        rids = f.get("row_ids") or ([f["row_id"]] if f.get("row_id") else [])
        for rid in rids:
            if rid not in by: continue
            cure = f.get("proposed_cure", "")
            key = (rid, f.get("e_class"), (f.get("defective_text") or "")[:60])
            if SPAN_WORDS.search(cure) or SPAN_WORDS.search(f.get("defective_text", "") or ""):
                disp, why = "record_only", "span proposal - recorded with its both-sides evidence, not ordered (span changes need an explicit orchestrator order inside the owner-ruled strategy)"
            elif FIELD_WORDS.search(cure):
                disp, why = "record_only", "cure names a closed field (confidence/unit_type/parent_collection) - recorded for the postcheck, not ordered to the micro author"
            elif key in seen:
                disp, why = "record_only", "duplicate of an already-ordered finding on the same row/class/text"
            else:
                disp, why = "order", "prose/refs/oss cure inside the author law"; seen.add(key)
            docket.setdefault(rid, []).append({"lane": sn, "e_class": f.get("e_class"), "severity": f.get("severity"), "defective_text": f.get("defective_text"),
                                               "byte_evidence": f.get("byte_evidence"), "proposed_cure": cure, "disposition": disp, "orchestrator_reason": why, "source_index": i})
    for w in d.get("warn_flags_dispositioned", []):
        if w.get("disposition") == "genuine" and w.get("row_id") in by:
            docket.setdefault(w["row_id"], []).append({"lane": sn, "e_class": w.get("class") or "warn", "severity": "low", "defective_text": w.get("flag"), "byte_evidence": w.get("evidence", ""),
                                                      "proposed_cure": w.get("cure") or "cure the genuine flag per its class (validator WARN judged genuine by the lane)", "disposition": "order", "orchestrator_reason": "genuine validator WARN", "source_index": None})
ordered_rows = [rid for rid in order if any(x["disposition"] == "order" for x in docket.get(rid, []))]
record_only = {rid: [x for x in xs if x["disposition"] == "record_only"] for rid, xs in docket.items() if any(x["disposition"] == "record_only" for x in xs)}
(HERE / "spot" / "micro_docket.json").write_text(json.dumps({"schema": "jer_micro_docket.v1", "corpus": "rows_v3.jsonl", "rows_with_findings": len(docket),
    "findings_total": sum(len(v) for v in docket.values()), "ordered_rows": len(ordered_rows), "record_only_rows": len(record_only),
    "by_severity": {s: sum(1 for v in docket.values() for x in v if x["severity"] == s) for s in ("high", "medium", "low")},
    "docket": docket, "record_only": record_only}, ensure_ascii=False, indent=1), encoding="utf-8")
chunks = [ordered_rows[i:i + 8] for i in range(0, len(ordered_rows), 8)]
for n, ch in enumerate(chunks, 1):
    o = {"schema": "jer_micro_orders.v1", "agent": f"m{n:02d}", "attempt_id": f"jer_micro_m{n:02d}_a1", "output_file": f"spot/micro_{n:02d}.jsonl", "row_ids": ch,
         "orders": {rid: {"row_id": rid, "op": "replace", "current_row": by[rid], "findings": [x for x in docket[rid] if x["disposition"] == "order"],
                          "recorded_not_ordered": [x for x in docket[rid] if x["disposition"] != "order"],
                          "instruction": "Execute every ordered finding's proposed cure on this row within the author law; fields span / chunk_index_in_book / parent_collection / unit_type / confidence stay unchanged; a cure you cannot execute truthfully is REPORTED with its byte reason."} for rid in ch}}
    (HERE / "spot" / f"orders_micro_{n:02d}.json").write_text(json.dumps(o, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"rows_with_findings": len(docket), "findings_total": sum(len(v) for v in docket.values()), "ordered_rows": len(ordered_rows), "record_only_rows": len(record_only),
                  "by_severity": {s: sum(1 for v in docket.values() for x in v if x["severity"] == s) for s in ("high", "medium", "low")}, "micro_slices": len(chunks)}, indent=1))
