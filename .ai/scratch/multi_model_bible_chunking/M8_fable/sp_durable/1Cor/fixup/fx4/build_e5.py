"""Build controlling round 5: the queue from S5's deliverable, then the brief and launch message with measured pins.
usage: build_e5.py                (writes the queue, the brief and the message; the ledger and carriers must be final first)"""
import hashlib, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
SP = HERE.parents[2]
R = SP / "1Cor/review"
P = Path("C:/Users/lowel/AppData/Local/Temp/claude/C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View/af84b702-d913-4495-8e57-252cf7894c63/scratchpad")
OUT = P / "cor_ctl5"
ATT = "cor_controlling_rulings_r5_a1"
DEL = "1cor_controlling_agent_rulings_r5_e1.v1.json"
BS = chr(92)
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def win(p):
    return str(p).replace("/", BS)
s5 = json.loads((R / "1cor_fixup3_review_S5.json").read_text(encoding="utf-8"))
PROPOSE = {
 "S5-01": ("controlling", "Rule in words that W2-013 observed_substrate_signals[3] stands under the CWO-1COR-07 remedy as a forced side effect of the ordered reword, with no byte change, so condition 12 is met."),
 "S5-02": ("fixup", "License W6-013 strongest_rejected_alternative: name 16:21 and 16:24 for the first-person tokens and give the tier, within what refs_mirror allows."),
 "S5-03": ("fixup", "License the replacement sentence in W4-001 and W4-004 device_notes. It makes no claim about the holders and takes no side."),
 "S5-04": ("fixup", "Relabel the two new MEASURED claims in W5-003 and W5-006 boundary_rationale as EXTRACTED: no pinned script produced them."),
 "S5-05": ("fixup", "License W5-010 boundary_evidence_refs[1] and W5-004 device_notes to match the refrain wording of R4-W5-009."),
 "S5-06": ("fixup", "License the doubled-locator fix in W6-003, W6-005, W6-006, W6-007 and W6-009, with the witness name as subject, the form ordered for W6-006, W6-007 and W6-014. Name the spans."),
 "S5-07": ("fixup", "License splitting the one clause in W6-006 boundary_rationale, no change of substance."),
 "S5-08": ("fixup", "Rule that R4-UNCERTAINTY reaches the two sentences that carry weight, W2-003 strongest_rejected_alternative and W6-009 boundary_evidence_refs[6], and license a reword of those two only. The other mood labels in list fields stay and go to the end review as the mood class."),
 "S5-09": ("controlling", "Accept the four refs_mirror flags for sign-site lists under the CWO-1COR-07 remedy, which says a listing supports no seam, unless the citation argues a seam; check W4-001's 11:5 on that test, and if it argues one, license one mirroring ref element."),
 "S5-10": ("controlling", "No change to the pinned suite in this book. The landing tool already reads per_check; pass the summary defect to the method-change proposer."),
 "S5-11": ("controlling", "Rule whether the rows' script name needs a licensed reword or only a recorded pin of measure_w3b.py. Prefer the record."),
 "S5-12": ("fable_end_review", "Route to the end review."),
 "S5-13": ("orchestrator", "Record it; no sweep in this book. Pass the field to the method-change proposer."),
 "S5-14": ("orchestrator", "Record it; the close carries the record inconsistencies, and none bears on a row."),
}
fnd = {f["id"]: f for f in s5["new_findings"]}
if set(fnd) != set(PROPOSE):
    raise SystemExit("REFUSED: S5 ids differ from the proposals")
items = [{"id": "R5-" + i, "route": r, "proposal": t, "review_finding": fnd[i]} for i, (r, t) in PROPOSE.items()]
q = {"schema": "m8_controlling_queue.v1", "book": "1Cor", "for_execution": ATT + "#e1", "status": "proposed_by_orchestrator",
     "review_deliverable": "1Cor/review/1cor_fixup3_review_S5.json", "prior_rulings": ["E1", "E2", "E3", "E4"],
     "rows_under_review": "1Cor/fixup/draft_rows_fixup3_applied.jsonl",
     "measured_context": {"s5_readiness": s5["readiness"], "findings": 14, "rows_sha256": sha(SP / "1Cor/fixup/draft_rows_fixup3_applied.jsonl")},
     "items": items}
qp = R / "1cor_controlling_agent_queue_e5.v1.json"
qp.write_bytes((json.dumps(q, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
PINS = ["1Cor/review/1cor_controlling_agent_queue_e5.v1.json", "1Cor/review/1cor_fixup3_review_S5.json",
        "1Cor/review/1cor_controlling_agent_rulings_E4.v1.json", "1Cor/review/1cor_controlling_agent_rulings_E3.v1.json",
        "1Cor/review/1cor_controlling_agent_rulings_E2.v1.json", "1Cor/review/1cor_controlling_agent_rulings_E1.v1.json",
        "1Cor/fixup/draft_rows_fixup3_applied.jsonl", "1Cor/fixup/draft_rows_fixup3_applied.manifest.json",
        "1Cor/fixup/fixup3_licence_table.v1.json", "1Cor/fixup/landed3/author_unresolved_for_S5.md",
        "1Cor/review/cwo_1cor_post_fixup3_report.v1.json", "1Cor/book_strategy_1Cor.md", "1Cor/strategy_plan_1Cor.json",
        "1Cor/tools/TOOLKIT.md", "1Cor/1Cor_rp.txt", "1Cor/1Cor_sbl.txt", "1Cor/1Cor_web_clean.txt",
        "1Cor/tools/check_refs_mirror.py", "1Cor/tools/run_validator_suite.py", "1Cor/fixup/landed3/W3_e1/measure_w3b.py",
        "campaign/grader_models.v1.json", "../ERROR_PATTERN_LEDGER.v1.md"]
SPW = win(SP)
OW = win(OUT)
table = "".join("| `SP%s%s` | `%s` |\n" % (BS, p.replace("/", BS), sha(SP / p)) for p in PINS)
ids = ", ".join(i["id"] for i in items)
contract = (SP / "campaign/REVIEWER_CONTINUATION_CONTRACT.v1.md")
brief = (HERE / "CONTROLLING_BRIEF_E5.template.md").read_text(encoding="utf-8")
for k, v in {"@@SP@@": SPW, "@@OUT@@": OW, "@@DEL@@": DEL, "@@ATT@@": ATT, "@@PINS@@": table, "@@IDS@@": ids,
             "@@CONTRACT@@": win(contract), "@@CONTRACT_SHA@@": sha(contract)}.items():
    brief = brief.replace(k, v)
if "@@" in brief:
    raise SystemExit("REFUSED: unfilled slot")
bp = R / "CONTROLLING_BRIEF_E5.md"
bp.write_bytes(brief.encode("utf-8"))
msg = (HERE / "launch_message_E5.template.txt").read_text(encoding="utf-8")
msg = msg.replace("@@BRIEF@@", win(bp)).replace("@@BRIEF_SHA@@", sha(bp)).replace("@@LEDGER@@", win(SP.parent / "ERROR_PATTERN_LEDGER.v1.md"))
if "@@" in msg:
    raise SystemExit("REFUSED: unfilled message slot")
mp = P / "cor_review_msgs/launch_message_CTL_E5.txt"
mp.write_bytes(msg.encode("utf-8"))
(OUT / "work").mkdir(parents=True, exist_ok=True)
print(json.dumps({"queue": sha(qp), "brief": sha(bp), "message": sha(mp), "pins": len(PINS), "items": len(items)}))
