"""B-6 whole-chapter cap sweep. Run from SP/Isa: python tools/_cap_sweep.py [rows_file]

Sweeps EVERY row span against verse_inventory.json chapter counts. A row whose span
is exactly one whole WEB chapter must: confidence in {medium_low, low};
frontier_flag_considered True; a cap disclosure present in its own prose (heuristic:
mentions the chapter's verse count AND a cap/whole-chapter phrasing). The returned
set must exactly equal the expected treated set. Exit 1 on any failure.
"""
import json, re, sys

rows_file = sys.argv[1] if len(sys.argv) > 1 else "rows_v2.jsonl"
inv = json.load(open("verse_inventory.json", encoding="utf-8"))
counts = inv["chapters"]
if isinstance(counts, list):
    counts = {(c["chapter"] if isinstance(c, dict) else i + 1):
              (c["verses"] if isinstance(c, dict) else c) for i, c in enumerate(counts)}
counts = {int(k): int(v) for k, v in counts.items()}
assert len(counts) == 66 and sum(counts.values()) == 1292, (len(counts), sum(counts.values()))

EXPECTED = {"P02-009", "P03-014", "P04-008", "P05-005", "P05-009", "P09-001",
            "P09-005", "P09-006", "P09-007", "P15-002", "P15-004", "P16-005", "P17-001"}
SPAN = re.compile(r"^Isa\.(\d+)\.(\d+)-Isa\.(\d+)\.(\d+)$")
found, failures = set(), []
for line in open(rows_file, encoding="utf-8"):
    r = json.loads(line)
    m = SPAN.match(r["span"])
    if not m: failures.append(f"{r['writer_decision_id']} unparseable span {r['span']}"); continue
    c1, v1, c2, v2 = map(int, m.groups())
    if c1 == c2 and v1 == 1 and v2 == counts.get(c1, -1):
        rid = r["writer_decision_id"]
        found.add(rid)
        prose = " ".join(str(r.get(f, "")) for f in
                         ("boundary_rationale", "device_notes", "strongest_rejected_alternative"))
        if r["confidence"] not in ("medium_low", "low"):
            failures.append(f"{rid} whole-chapter (ch {c1}) at confidence {r['confidence']}")
        if str(r["frontier_flag_considered"]) not in ("True", "true"):
            failures.append(f"{rid} whole-chapter without frontier flag")
        has_count = str(counts[c1]) in prose
        has_cap = re.search(r"whole[- ]chapter|chapter[- ]fallback|capped|cap\b", prose, re.I)
        if not (has_count and has_cap):
            failures.append(f"{rid} cap disclosure missing/incomplete (count-cited={has_count}, cap-phrase={bool(has_cap)})")
if found != EXPECTED:
    if found - EXPECTED: failures.append(f"UNTREATED whole-chapter rows: {sorted(found - EXPECTED)}")
    if EXPECTED - found: failures.append(f"expected class members not whole-chapter anymore: {sorted(EXPECTED - found)}")
print(json.dumps({"whole_chapter_rows": sorted(found), "failures": failures,
                  "status": "GREEN" if not failures else "RED"}, indent=1))
sys.exit(1 if failures else 0)
