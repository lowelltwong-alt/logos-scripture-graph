#!/usr/bin/env python3
"""Queue E13-110: #e16 landed; the second Fable review launched; the budget forecast corrected for close-gate items 20-23."""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
before = Q.read_bytes()
if any(json.loads(l).get("id") == "E13-110" for l in before.decode("utf-8").splitlines() if l.strip()):
    raise SystemExit("REFUSED: E13-110 already recorded")
R = EZ / "author" / "e16" / "ruling_e16.json"
r16 = json.loads(R.read_text(encoding="utf-8-sig"))
orders = r16.get("orders_for_final_remediation") or []
e = {
    "id": "E13-110", "opened_at": datetime.now(timezone.utc).isoformat(), "severity": "HIGH", "tier": "MEASURED",
    "blocks_close": True, "raised_by": "orchestrator (claude-opus-5)",
    "status": "DONE for #e16's landing; its orders are OWED (mechanical by sweep, author in the final remediation batch), its tool orders and section-7 conditionals OWED",
    "headline": ("#e16 LANDED (Fable controlling agent): C1 forward-merge rivals take a new ':merge' qualifier on the row's own dissolved "
                 "seam; C2 one pairing convention for every merge rival (12 re-pairings); C3 the lakhen-turn messenger onset is NOT "
                 "licensed - the three seams stand at medium_low and their tilings go to the second review; C4 'he said to me' and "
                 "interior transport inside a vision ARE licensed onsets and prose-weighed rivals must be tokenised. 57 grade moves "
                 "(21 conditional on a section-7 check the orchestrator owes), %d orders (%s), %d tool orders, %d escalations. All 17 "
                 "pins unchanged at the agent's final write." % (len(orders), dict(Counter(str(o.get("kind")) for o in orders)),
                                                                len(r16.get("tool_orders") or []), len(r16.get("escalations") or []))),
    "ruling": {"file": "Ezek/author/e16/ruling_e16.json", "sha256": sha(R)},
    "self_corrections_of_earlier_rulings": ["#e15 Q1's 17.10/17.11 pair for P03-012 withdrawn", "#e15 Q3's P08-003 move reversed",
                                           "#e15 Q4's P02-008 'MEDIUM stands' superseded", "#e15 Q8 blast-radius text corrected",
                                           "#e15 Q10's scrambled quotation list acknowledged", "#e14 Q2 holds for P07-001 and P08-013 superseded",
                                           "#e13's 'licensed as a discourse frame' at 17:19 confirmed withdrawn"],
    "second_review_launched": {"attempts": ["ezek_second_review_lane_a_a1", "ezek_second_review_lane_b_a1"], "rows": 48,
                               "brief": "Ezek/repair2/second_review/SECOND_REVIEW_BRIEF.md", "brief_sha256": sha(EZ / "repair2" / "second_review" / "SECOND_REVIEW_BRIEF.md"),
                               "sequencing": "after #e16 (it reads the rulings) and before the final remediation batch (its findings repaired in that one batch)"},
    "forecast_correction": ("the orchestrator's forecast (69.0-72.4M) omitted close-gate items 20-23 (the scholar-record Fable audit of a "
                            "913 KB record, the method-record update and check, the Ezekiel atlas and check, the method-change proposer "
                            "and adjudication). Corrected: ~74M total (range 70-79M) against the 72,000,000 hard line. Three named "
                            "scope cuts (~70.7M together) were put to the owner, who dismissed the question; the cuts bind at the "
                            "final remediation batch and the final check, and are asked again there."),
    "e41_resolution": "the #e16 agent re-hashed all pins after its final write and found them unchanged: the E-41 window did not reach it",
    "cost_measured": {"e16": 492236},
}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(e, ensure_ascii=False) + "\n")
after = Q.read_bytes()
assert after.startswith(before) and after.count(b"\n") == before.count(b"\n") + 1
print("E13-110 appended; queue rows:", sum(1 for l in after.decode("utf-8").splitlines() if l.strip()))
