#!/usr/bin/env python3
"""Build the REPAIR-2 step-2 slices: per row, the LIVE prose plus THE ORDERS AS DATA.

WHY THE ORDERS TRAVEL. #e15 Q1: "The spot slices carried the pre- and post-wave bytes and the checklist, not the
per-row orders. Every 'unauthorised' verdict in the three lanes is a verdict on the bytes alone." Its order:
"every slice carries, per row, the list of orders that applied to it - ruling id, clause, and the ordered content
- as DATA in the slice, with the rule that an order is authority for exactly what it names and nothing adjacent."
So each slice below carries the ruling's own text, extracted at its digest, never my summary of it.
"""
import hashlib
import json
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
R15 = EZ / "ezek_controlling_agent_ruling_e15.v1.json"
R13 = EZ / "ezek_controlling_agent_ruling_e13.v1.json"
BOSS = EZ / "ezek_boss_audit.v1.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

r15 = json.loads(R15.read_text(encoding="utf-8"))
r13 = json.loads(R13.read_text(encoding="utf-8"))
boss = json.loads(BOSS.read_text(encoding="utf-8"))
live = {r["decision_id"]: r for r in
        (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}

CH18 = ["P03-014", "P03-015", "P03-016", "P03-017", "P03-018", "P03-019"]
Q3 = r15["q3_confidence_defects"]
Q4 = r15["q4_findings_of_fact"]
Q1 = r15["q1_redecision_threshold"]

ORDERS = {}
ORDERS["P08-002"] = {"#e15 Q1 per_row P08-002": Q1["per_row"]["P08-002"]}
for rid in ("P08-003", "P09-009", "P09-011", "P07-008", "P08-012", "P04-008"):
    ORDERS[rid] = {"#e15 Q3 " + rid: Q3[rid]}
for rid in CH18:
    ORDERS[rid] = {"#e15 Q3 P03-014_and_the_ch18_class (ONE class ruling over all six ch-18 rows)":
                   Q3["P03-014_and_the_ch18_class"],
                   "#e15 Q3 confidence_moves_by_this_ruling " + rid:
                   Q3["confidence_moves_by_this_ruling"][rid]}
ORDERS["P09-001"] = {"#e15 Q4 P09-001": Q4["P09-001"],
                     "#e15 Q3 confidence_moves_by_this_ruling P09-001":
                     Q3["confidence_moves_by_this_ruling"]["P09-001"]}
ORDERS["P09-010"] = {"#e15 Q4 P09-010": Q4["P09-010"]}
ORDERS["P02-008"] = {"#e15 Q4 P02-008": Q4["P02-008"]}

# the #e13 confidence ruling and author_wave order for each row that has one, carried verbatim
for e in r13.get("confidence_rulings", []):
    rid = e.get("row")
    if rid in ORDERS:
        ORDERS[rid]["#e13 confidence_rulings " + rid] = e
# THE BOSS AUDIT'S PER-ROW WORK ORDER, where the row has one. The per-row reconciliations live under `rows`;
# my first version read a guessed key name ("reconciliations"), found nothing, and attached nothing WITHOUT
# SAYING SO - the same silent-miss shape as the census harvester that read only `count` keys. The assert below
# is the control: a key name that stops matching now fails the build instead of quietly shipping thin slices.
_boss_attached = 0
for rec in boss["rows"]:
    rid = rec.get("row_id") or rec.get("row")
    if rid in ORDERS:
        ORDERS[rid]["boss audit reconciliation " + rid] = rec
        _boss_attached += 1
assert _boss_attached >= 10, ("the boss audit carries a per-row entry for all 145 rows, so at least the 16 in "
                              "this docket must attach; got %d - the key name or the row-id field moved"
                              % _boss_attached)
if isinstance(boss.get("p08_012_reweigh"), dict):
    ORDERS["P08-012"]["boss audit p08_012_reweigh"] = boss["p08_012_reweigh"]

PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess")
slices = {}
for rid, orders in ORDERS.items():
    r = live[rid]
    slices[rid] = {
        "row": rid,
        "span": r.get("span"),
        "confidence_NOW_after_step_1": r.get("confidence"),
        "live_prose": {f: r.get(f) for f in PROSE if isinstance(r.get(f), str)},
        "live_boundary_evidence_refs": r.get("boundary_evidence_refs"),
        "THE_ORDERS_THAT_APPLY_TO_THIS_ROW": orders,
        "the_rule_about_orders": ("an order is authority for exactly what it names and nothing adjacent "
                                 "(#e15 Q1). If an order's ground is false, that is a STOP to be reported, "
                                 "never a substitution of a different ground (#e15's line: 'a false "
                                 "only-ground is a STOP, never a substitution')."),
    }

out = {
    "schema": "ezek_repair2_step2_slices.v1",
    "step": "REPAIR-2 step 2 (grounds): #e15's sequence item 2 - 'Q1 P08-002; Q3 stale-ground prose (P08-003, "
            "P09-009, P09-011, P07-008, P08-012, the six ch-18 rows); Q4 three rows' - plus the grounds owed by "
            "step 1's nine grade moves, which the ruling binds into the same batch.",
    "inputs": {"rows": str(ROWS), "rows_sha256": sha(ROWS),
               "ruling_e15_sha256": sha(R15), "ruling_e13_sha256": sha(R13), "boss_audit_sha256": sha(BOSS)},
    "rows": len(slices),
    "slices": slices,
}
p = HERE / "step2_slices.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"rows": len(slices), "boss_entries_attached": _boss_attached,
                  "row_ids": sorted(slices),
                  "orders_per_row": {k: len(v["THE_ORDERS_THAT_APPLY_TO_THIS_ROW"]) for k, v in
                                     sorted(slices.items())},
                  "bytes": p.stat().st_size, "sha256": sha(p)}, indent=1))
