#!/usr/bin/env python3
"""Queue E13-109: REPAIR-2 step 7 (spot re-read) landed and reconciled; the X2 WARRANT re-face applied mechanically."""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
before = Q.read_bytes()
if any(json.loads(l).get("id") == "E13-109" for l in before.decode("utf-8").splitlines() if l.strip()):
    raise SystemExit("REFUSED: E13-109 already recorded")
if sha(EZ / "repair" / "rows_v7_cwo24.jsonl") != "78a092c3a2ebf27d44dea346029e3d1940578caaca609827083756ce505dfd35":
    raise SystemExit("REFUSED: rows are not at the X2 WARRANT re-face post-image")
rec = EZ / "repair2" / "step7" / "step7_reconciled.v1.json"
c = json.loads(rec.read_text(encoding="utf-8"))
d = c["defects"]
plan = json.loads((EZ / "repair2" / "step7" / "x2_warrant" / "plan.json").read_text(encoding="utf-8"))
e = {
    "id": "E13-109", "opened_at": datetime.now(timezone.utc).isoformat(), "severity": "HIGH", "tier": "MEASURED",
    "blocks_close": True, "raised_by": "orchestrator (claude-opus-5)",
    "status": "DONE for step 7; the defects are OWED in the final remediation batch, the questions in #e16",
    "headline": ("REPAIR-2 STEP 7 LANDED: six blind Opus readers (three strides x two) re-read all 127 rows REPAIR-2 changed; "
                 "188 defect items on 105 rows (101 raised by both readers of a stride, 87 by one), 23 MEDIUM on 23 rows, "
                 "0 HIGH; 92 questions; CONF-CAL answers per row. Every reader answered every row of its slice. Then the "
                 "X2 re-face of WARRANT entries was applied MECHANICALLY: 27 entries whose annotation names an MT device "
                 "class the census or mark record confirms at that verse; rows 097799dc -> 78a092c3; the full suite on the "
                 "byte-identical candidate: hard GREEN, no member moved."),
    "reconciliation": {"file": "Ezek/repair2/step7/step7_reconciled.v1.json", "sha256": sha(rec),
                       "by_agreement": dict(Counter(x["agreement"] for x in d)),
                       "by_severity": dict(Counter(str(x["max_severity"]) for x in d)),
                       "by_item": dict(Counter(x["item"] for x in d)),
                       "medium_rows": sorted({x["row"] for x in d if x["max_severity"] == "MEDIUM"}),
                       "a_defect_in_the_reconciler": ("the first reconciliation read one reader layout only and reported 38 "
                                                     "A-only defects and 0 from B, though B had reported 47 and both named the "
                                                     "same MEDIUM rows; the reconciler now reads both layouts and REFUSES when "
                                                     "a reader reports defects and none are extracted (E-36)")},
    "readers_repeated_classes": [
        "WARRANT entries resting on MT formulae, datelines, transport or marks left on web: (mechanical part applied here; entries whose annotation names no device class are author calls)",
        "merge rivals tokenised four ways in step 4c (stopped, paired at the absorbing unit's onset, ordered in that form, unpaired) - a class question for #e16 beside the forward-merge class",
        "routed step-5 and step-6 repairs that never landed (P02-019 ADJ-R01/R02, P10-011 RT-01/RT-02)",
        "#e12 per-row orders still undone (A2 K/Q at P11-007 and P11-014; A7 wording at P01-014, P11-007, P11-012)",
        "a step-5 paseq re-gloss made a false claim about the witness (P03-002, P10-001)",
        "P08-011: the recognition refrain stands on 36:11, not 36:12",
        "the CONF-CAL view misses 'he said to me' and interior transport onsets inside visions, and interior rivals the prose weighs with no rival token",
    ],
    "x2_warrant_reface": {"plan": "Ezek/repair2/step7/x2_warrant/plan.json", "tally": plan["tally"],
                          "sweep": "repair2_step7_x2_warrant_reface", "parity": "27/27",
                          "distinct_check": "annotation names a device class AND the census or mark record shows it at the verse; single-verse, outside chapters 20-21, identity numbering by web_to_mt"},
    "cost_measured": {"step7_readers": 4728868, "note": "six readers, 737K-818K each; the pre-launch estimate was 4.2M"},
}
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(e, ensure_ascii=False) + "\n")
after = Q.read_bytes()
assert after.startswith(before) and after.count(b"\n") == before.count(b"\n") + 1
print("E13-109 appended; queue rows:", sum(1 for l in after.decode("utf-8").splitlines() if l.strip()))
