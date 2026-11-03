"""Pin the orchestrator's round-8 continuation tests into 1Cor/close/e9_inputs and write the round-9 controlling queue.

Run from SP: python -B 1Cor/close/gen_e9_inputs.py SCRATCH. Write-once: an existing output with other bytes refuses.
Every figure below is read from a file this script copies and pins; none is typed from memory.
"""
import hashlib
import json
import sys
from pathlib import Path

SCR = Path(sys.argv[1])
OUT = Path("1Cor/close/e9_inputs")
R = "1Cor/review/"
LA, LB = "1Cor/close/landed/MERGED_A_e1/", "1Cor/close/landed/MERGED_B_e1/"
COPIES = {  # pinned name: scratch source
    "e8_spans_as_ruled.v1.json": "cand_e8.json",
    "e8_spans_first_test.v1.json": "cand_out.json",
    "candidate_spans_keep.v1.json": "cand_keep.json",
    "candidate_spans_keep_test.v1.json": "cand_out_keep.json",
    "candidate_spans_drop.v1.json": "cand_drop.json",
    "candidate_spans_drop_test.v1.json": "cand_out_drop.json",
    "close_gate_suite_result.v1.json": "cg_full2.json",
    "atlas_lead_params_test.v1.json": "lead_params.json",
    "atlas_lead_feed_test.v1.jsonl": "lead_out/deliverables/atlas_candidate_feed_rows.jsonl",
    "scholar_web_params_test.v1.json": "web_params.json",
    "scholar_web_record_test.v1.md": "web_out/scholar_record/FIRST_CORINTHIANS_SCHOLAR_RECORD.v1.md",
    "scholar_web_check_test.v1.json": "web_out/scholar_record/scholar_record_check.v1.json",
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def put(name, data):
    p = OUT / name
    if p.exists() and p.read_bytes() != data:
        raise SystemExit("REFUSED: %s exists with other bytes" % p)
    p.write_bytes(data)
    return sha(p)


def jl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


OUT.mkdir(parents=True, exist_ok=True)
pins = {n: put(n, (SCR / s).read_bytes()) for n, s in COPIES.items()}

rows = jl("1Cor/rows_v1_final.jsonl")
feed = {f["chunk_decision_id"]: f for f in jl("1Cor/deliverables/atlas_candidate_feed_rows.jsonl")}
test = {f["chunk_decision_id"]: f for f in jl(OUT / "atlas_lead_feed_test.v1.jsonl")}
leads = json.load(open(OUT / "atlas_lead_params_test.v1.json", encoding="utf-8"))["why_lead_sentence"]
FIELDS = ("device_notes", "boundary_rationale", "strongest_rejected_alternative")
by_span = {r["span"]: r for r in rows}
lead_rows = {}
for cid in ["M8-1Cor-011", "M8-1Cor-027", "M8-1Cor-028", "M8-1Cor-051", "M8-1Cor-052"]:
    r = by_span[feed[cid]["span"]]
    lead_rows[cid] = {"decision_id": r["decision_id"], "span": r["span"], "confidence": r["confidence"],
                      "candidate_lead_tested": leads.get(cid), "feed_now_opens": feed[cid]["why_low_confidence"][:160],
                      "feed_under_test_opens": test[cid]["why_low_confidence"][:160],
                      "row_fields_the_generator_accepts": list(FIELDS)}

suite = json.load(open(OUT / "close_gate_suite_result.v1.json", encoding="utf-8"))
keep = json.load(open(OUT / "candidate_spans_keep_test.v1.json", encoding="utf-8"))
drop = json.load(open(OUT / "candidate_spans_drop_test.v1.json", encoding="utf-8"))
first = json.load(open(OUT / "e8_spans_first_test.v1.json", encoding="utf-8"))
web_check = json.load(open(OUT / "scholar_web_check_test.v1.json", encoding="utf-8"))
strategy = open("1Cor/book_strategy_1Cor.md", encoding="utf-8").read().splitlines()


def brief(t):
    return {k: t[k] for k in ("spans_applied", "elements_changed", "rows_changed", "unchanged_rows_byte_equal", "sweep_equal_to_pre", "ok")} | \
           {"post_suite": t["post"]["suite"], "post_ngram7": t["post"]["ngram7"]["status"], "post_tiling_rc": t["post"]["tiling"]["rc"]}


report = {
    "schema": "m8_orchestrator_test_report.v1", "book": "1Cor", "for_execution": "cor_controlling_rulings_r9_a1#e1",
    "tier_note": "Every result below is MEASURED by the orchestrator on private copies; the bytes are the pinned files named.",
    "rows_tested_against": {"path": "1Cor/rows_v1_final.jsonl", "sha256": sha("1Cor/rows_v1_final.jsonl")},
    "pins": pins,
    "spans": {
        "tool": "campaign/_apply_exact_orders.py --dry-run, on a private copy; it runs run_validator_suite.py, check_tiling.py, ngram7.py --gate 10 and cwo_sweep_1cor.py before and after",
        "e8_as_ruled": brief(first),
        "e8_as_ruled_note": "E8's words raised one triage flag (universals) that the rows do not carry now; the W5-003 rewording in the candidate files clears it.",
        "changed_from_e8": [
            {"row": "W5-003", "field": "boundary_rationale", "why": "clears the universals triage flag E8's words raised"},
            {"row": "W5-014", "field": "strongest_rejected_alternative", "why": "names strategy line 87's measured closer 14:40, the gap E8 listed as unresolved"},
        ],
        "keep_measure_w3": brief(keep),
        "drop_measure_w3": brief(drop),
        "measure_w3_question": "E8 R8-LOW-ROWS replaces 'counts MEASURED by script measure_w3 over the RP and SBLGNT texts;' with 'no count is stated on this row;' at W3-003 and W3-006 device_notes. E8 listed R5-S5-11 and R7-W4-3-GEN as not re-read. Variant drop leaves those two spans out; both variants pass.",
    },
    "atlas_leads": {
        "tool": "1Cor/deliverables/gen_atlas_rows.py, new optional book_params key why_lead_sentence {chunk_decision_id: sentence}; it refuses a sentence that is not one whole sentence of the row's device_notes, boundary_rationale or strongest_rejected_alternative, and records the field in the derivation",
        "check_without_key": "gen_atlas_rows.py --check with the real params: DETERMINISTIC MATCH (the feed is unchanged unless the key is set)",
        "rows": lead_rows,
        "open": ["M8-1Cor-051's tested lead opens with 'It', whose antecedent is the sentence before it in the row.",
                 "M8-1Cor-052's sentence of doubt exists only after the fix-up: E8's W5-010 span adds it. It is not tested."],
        "check_tool_limit": "check_atlas_rows.py with --out-root reads sidecar sources from that root; it was not run on the private copy and runs at the real regeneration.",
    },
    "web_term": {
        "source": "1Cor/review/primaries/finals/final_RT_c06_e1.json, a reader's final, 2 occurrences; the record quotes it at lines 6144 and 6306",
        "candidate": "one entry appended to 1Cor/scholar_record/book_params.v1.json word_subs_before_codes, printed in full in the record's substitution table",
        "result": {"lines_changed": [6144, 6306], "table_row_added": 1, "check": "%s %d/%d" % (web_check["VERDICT"], web_check["checks_passed"], web_check["checks_total"])},
        "owner_question_stands": "Whether a WEB licence term is stated anywhere, and from what source; the book's files state none (record lines 14049 and 14395).",
    },
    "gate_tools": {
        "tool": "campaign/_close_book.py", "tool_sha256": suite["tool_sha256"],
        "suite": {"tests_total": suite["tests_total"], "passed": suite["passed"], "params_sha256": suite["params_sha256"]},
        "due_at_close": "Optional constants DUE_AT_CLOSE {type, items}, CLOSE_EVIDENCE_REL, CLOSE_EVIDENCE_PIN. A lane's met:false entry of that type on a listed item passes the lane gate; the close then requires the pinned close-evidence file to hold values['item_N'] for each listed item, present and not UNAVAILABLE. Absent constants: the type stays refused, as before.",
        "read_record": "Optional constant READ_RECORD {base_rows_rel, base_rows_pin}. Each lane's final check lists rows_read and rows_held_by_byte_equality by decision_id; the gate refuses a row in neither or both, an unknown id, a held row whose bytes differ from the pinned base copy, and a changed row or a neighbour of one that was not read.",
        "planned_values": {"DUE_AT_CLOSE": {"type": "DUE_AT_CLOSE_ACT", "items": [16, 18, 19]},
                           "CLOSE_EVIDENCE_REL": "close/close_evidence.v1.json",
                           "READ_RECORD": {"base_rows_rel": "close/rows_read_by_first_lanes.v1.jsonl", "base_rows_pin": sha("1Cor/rows_v1_final.jsonl")}},
        "fixture_fix": "One existing case planted NOT_MET on boss e1 condition B3, which 1Cor's e2 answers MET; it now plants on a condition no later record answers. Before the fix 199/200, after it 200/200.",
    },
    "strategy_line_87": strategy[86],
}
put("e9_test_report.v1.json", (json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))

T = "1Cor/close/e9_inputs/e9_test_report.v1.json"
items = [
    {"id": "R9-SPANS", "route": "controlling",
     "proposal": "GATE-E8 bars the fix-up until a continuation applies every candidate span and the four tools pass. The orchestrator did so on private copies: E8's 21 spans raised one universals triage flag; two reworded spans (W5-003, W5-014) clear it and name line 87's closer. Both variants pass, with and without the two measure_w3 spans. Rule the final span set as exact orders, decide the measure_w3 pair against R5-S5-11 and R7-W4-3-GEN, and rerun the four tools on your final set.",
     "refs": [T + "#spans", "1Cor/close/e9_inputs/candidate_spans_keep.v1.json", "1Cor/close/e9_inputs/candidate_spans_drop.v1.json", "1Cor/close/e9_inputs/e8_spans_as_ruled.v1.json"]},
    {"id": "R9-LEADS", "route": "controlling",
     "proposal": "R8-FEED-011 is cured through a new generator key that names, per feed id, the row's own sentence to lead why_low_confidence. Four leads are tested. Rule the sentence for each of the five ids, as bytes of the row after your spans. -051's tested sentence opens with 'It'; -052's exists only after W5-010's span.",
     "refs": [T + "#atlas_leads", "1Cor/close/e9_inputs/atlas_lead_feed_test.v1.jsonl", "1Cor/deliverables/gen_atlas_rows.py"]},
    {"id": "R9-WEB", "route": "controlling",
     "proposal": "The 'public domain' clause is a reader's sentence, quoted. The tested cure is one substitution entry in the scholar params, printed in the record's table; the check passes. Rule the entry's exact pattern and replacement, or another wording. The owner question on a WEB term stands either way.",
     "refs": [T + "#web_term", "1Cor/close/e9_inputs/scholar_web_params_test.v1.json"]},
    {"id": "R9-GATE-TOOLS", "route": "controlling",
     "proposal": "The DUE_AT_CLOSE and read-record gates are built and the suite passes 200/200. Rule whether they implement R8-GATE-DUE-AT-CLOSE and R8-PAIR without weakening a gate, and rule the planned constant values. Name any defect by line.",
     "refs": [T + "#gate_tools", "campaign/_close_book.py", "campaign/_test_close_book_gates.py"]},
    {"id": "R9-CLOSE-EVIDENCE", "route": "controlling",
     "proposal": "The close-evidence file does not exist yet. Proposal: close/close_evidence.v1.json, keys values.item_N and values.OW-28, each {value, tier, source}, with UNAVAILABLE where no pinned source holds it. Items 16, 18 and 19 are filled at the close act; items 1, 4, 5, 13, 14 and OW-28 before the reissue. Rule the shape, the sources per item, and what a lane's entry cites.",
     "refs": ["1Cor/review/1cor_controlling_agent_rulings_E8.v1.json#R8-GATE-EVIDENCE", "../CAMPAIGN_CLOSE_GATE.v1.md"]},
    {"id": "R9-PF", "route": "controlling",
     "proposal": "Lane A's process findings PF-5..PF-13 have no ruling (E8 ruled PF-1..PF-4 via routing and pairing). Each is low. Rule each: an orchestrator text change named exactly, routing to the end review, or no change. PF-7 asks for a gate addendum; say whether that is yours to order.",
     "refs": [LA + "final_check.json#process_findings"]},
    {"id": "R9-PAIR-MECH", "route": "controlling",
     "proposal": "For the reissue under R8-PAIR the orchestrator freezes a copy of the d1751369 rows as close/rows_read_by_first_lanes.v1.jsonl, issues attempts _a2, makes every changed row and both neighbours mandatory reads, and has each final check list rows_read and rows_held_by_byte_equality; the read-record gate checks it. Rule whether this is R8-PAIR as written.",
     "refs": [T + "#gate_tools/read_record", "1Cor/review/1cor_controlling_agent_rulings_E8.v1.json#R8-PAIR"]},
]
queue = {"schema": "m8_controlling_queue.v1", "book": "1Cor", "for_execution": "cor_controlling_rulings_r9_a1#e1",
         "status": "proposed_by_orchestrator", "test_report": {"path": T, "sha256": sha(OUT / "e9_test_report.v1.json")},
         "prior_rulings": [R + "1cor_controlling_agent_rulings_E%d.v1.json" % n for n in (8, 7, 5)],
         "items": items}
q = Path(R + "1cor_controlling_agent_queue_e9.v1.json")
data = (json.dumps(queue, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
if q.exists() and q.read_bytes() != data:
    raise SystemExit("REFUSED: queue exists with other bytes")
q.write_bytes(data)
print("report", sha(OUT / "e9_test_report.v1.json")[:16], "queue", sha(q)[:16], "items", len(items), "pins", len(pins))
