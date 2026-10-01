"""Census author-wave landings against the order plan. Run from SP/Isa.
Usage: python tools/_author_census.py [a01 a02 ...]   (default: all agents with orders)
Checks per landed attempt file: parses per line; ops legal; rows == assigned exactly;
replace rows carry all 22 fields, correct ids, unchanged chunk_index; retires only the
two boss-adopted ones. Reports missing attempts (not an error pre-landing).
"""
import json, glob, sys, os

FIELDS = ['decision_id', 'book', 'model_id', 'chunk_index_in_book', 'span',
          'boundary_rationale', 'boundary_evidence_refs', 'strongest_rejected_alternative',
          'literature_type_guess', 'confidence', 'strong_or_hebrew_tags_used',
          'wj_or_red_letter_considered', 'frontier_flag_considered', 'non_authorizing',
          'review_status', 'parent_collection', 'unit_type', 'writer_part',
          'writer_decision_id', 'writer_attempt_id', 'observed_substrate_signals', 'device_notes']
RETIRES = {"P15-003", "P09-004"}
ROWS = {json.loads(l)["writer_decision_id"]: json.loads(l)
        for l in open("draft_rows_combined.jsonl", encoding="utf-8")}

agents = sys.argv[1:] or [os.path.basename(f)[7:10] for f in sorted(glob.glob("author/orders_a*.json"))]
defects, landed, missing, seen_rows = [], 0, [], {}
for aid in agents:
    plan = json.load(open(f"author/orders_{aid}.json", encoding="utf-8"))
    for att in plan["attempts"]:
        path = "author/" + os.path.basename(att["output"])
        if not os.path.exists(path):
            missing.append(att["attempt_id"]); continue
        landed += 1
        got = {}
        for i, line in enumerate(open(path, encoding="utf-8")):
            line = line.strip()
            if not line: continue
            try:
                o = json.loads(line)
            except Exception as e:
                defects.append(f"{path}:{i+1} unparseable: {e}"); continue
            op = o.get("_op")
            rid = o.get("writer_decision_id")
            if rid in got: defects.append(f"{path} duplicate row {rid}")
            got[rid] = op
            if rid in seen_rows and seen_rows[rid] != path:
                defects.append(f"{rid} appears in BOTH {seen_rows[rid]} and {path}")
            seen_rows[rid] = path
            if op == "retire":
                if rid not in RETIRES: defects.append(f"{path} illegal retire {rid}")
                continue
            if op != "replace":
                defects.append(f"{path} {rid} illegal _op {op!r}"); continue
            if rid in RETIRES: defects.append(f"{path} {rid} must be retire, got replace")
            row_fields = [k for k in o if k != "_op"]
            miss = [f for f in FIELDS if f not in row_fields]
            extra = [f for f in row_fields if f not in FIELDS]
            if miss: defects.append(f"{path} {rid} missing fields {miss}")
            if extra: defects.append(f"{path} {rid} unknown fields {extra}")
            orig = ROWS.get(rid)
            if orig is None: defects.append(f"{path} {rid} not in corpus")
            elif o.get("chunk_index_in_book") != orig["chunk_index_in_book"]:
                defects.append(f"{path} {rid} chunk_index changed {orig['chunk_index_in_book']} -> {o.get('chunk_index_in_book')}")
        want = set(att["rows"]); have = set(got)
        if want != have:
            if have - want: defects.append(f"{att['attempt_id']} extra rows {sorted(have-want)}")
            if want - have: defects.append(f"{att['attempt_id']} missing rows {sorted(want-have)}")
strays = [f for f in glob.glob("author/*") if os.path.basename(f) not in
          {os.path.basename(p) for p in glob.glob("author/orders_a*.json")}
          and not os.path.basename(f).startswith("author_a")
          and os.path.basename(f) not in ("varsweep_A_edits.jsonl", "varsweep_B_edits.jsonl")]
print(json.dumps({"landed_attempts": landed, "missing_attempts": missing,
                  "rows_landed": len(seen_rows), "defects": defects,
                  "stray_files_in_author_dir": strays,
                  "status": "GREEN" if not defects else "RED"}, indent=1))
