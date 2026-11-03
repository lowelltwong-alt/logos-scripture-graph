"""Build the landing row (m8_attempt_receipt.v1 completion) of one 1Cor controlling round from the deliverable's bytes plus
notification facts. Derived from make_review_landing.py (the S1 maker, unchanged); same row shape.

The landing check is MEASURED here on the deliverable: one JSON object; every top-level key of the brief's schema; this
attempt and execution; exactly one ruling per queue id (no id missing, none extra, none twice); each ruling from the
brief's set; the five gate fields with their types; each order's "to" from the brief's set; no CR bytes. A deliverable
that fails is still landed (the outcome must then say so), but the row records each failure. notification_time is
stamped by this script's clock (E-78 candidate).

usage: make_ctl_landing.py --round 1 [--execution N] --agent-id ID --tokens N --tool-uses N --duration-ms N
       --outcome TEXT --summary TEXT [--note TEXT ...] --out FILE
"""
import argparse
import datetime
import hashlib
import json
import re
from pathlib import Path

P = Path("C:/Users/lowel/AppData/Local/Temp/claude/C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View/af84b702-d913-4495-8e57-252cf7894c63/scratchpad")
SPR = Path("C:/wt/logos-t423-m8-fable/.ai/scratch/multi_model_bible_chunking/M8_fable/sp_durable/1Cor/review")
KEYS = ("attempt_id", "execution_id", "inputs_ruled_on", "rulings", "corpus_wide_orders", "gate", "unresolved_uncertainty")
RULINGS = {"ratify", "ratify_with_changes", "reverse", "adopt", "reject", "close", "keep_open", "defer", "amend", "hold", "cut"}
GATE = {"tool_fixes_before_fixup": list, "fixup_may_launch": bool, "fixup_parts": list, "s2_conditions": list,
        "primaries_may_launch": bool}
TO_FIXED = {"orchestrator", "tool_fix", "s2", "primaries", "fable_end_review"}
ap = argparse.ArgumentParser()
for k in ("--agent-id", "--outcome", "--summary", "--out"):
    ap.add_argument(k, required=True)
for k in ("--round", "--tokens", "--tool-uses", "--duration-ms"):
    ap.add_argument(k, required=True, type=int)
ap.add_argument("--execution", type=int, default=1)
ap.add_argument("--note", action="append", default=[])
a = ap.parse_args()
# Round Q's brief names the next distinct check s<Q+1> as an order target (round 3: s4); the fixed set above predates it.
TO_FIXED = TO_FIXED | {"s%d" % (a.round + 1)}
NOW =datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
att = "cor_controlling_rulings_r%d_a1" % a.round
tag = "" if a.execution == 1 else "_e%d" % a.execution
eid = "%s#e%d" % (att, a.execution)
out_dir = P / ("cor_ctl%d%s" % (a.round, tag))
f = out_dir / ("1cor_controlling_agent_rulings_r%d_e%d.v1.json" % (a.round, a.execution))
qf = SPR / ("1cor_controlling_agent_queue_e%d.v1.json" % a.round)
qids = [x["id"] for x in json.loads(qf.read_text(encoding="utf-8"))["items"]]
problems, d, b = [], None, b""
if not f.is_file():
    problems.append("deliverable absent")
else:
    b = f.read_bytes()
    if b"\r" in b:
        problems.append("CR bytes %d" % b.count(b"\r"))
    try:
        d = json.loads(b.decode("utf-8"))
    except ValueError as e:
        problems.append("not JSON: %s" % e)
counts, gate, cwo = {}, None, None
if isinstance(d, dict):
    problems += ["missing key %s" % k for k in KEYS if k not in d]
    if d.get("attempt_id") != att:
        problems.append("attempt_id %r" % d.get("attempt_id"))
    if d.get("execution_id") != eid:
        problems.append("execution_id %r" % d.get("execution_id"))
    rl = d.get("rulings") if isinstance(d.get("rulings"), list) else []
    ids = [r.get("id") if isinstance(r, dict) else None for r in rl]
    problems += ["ruling missing for %s" % q for q in qids if q not in ids]
    problems += ["ruling for unknown id %r" % i for i in ids if i not in qids]
    problems += ["id ruled %d times: %s" % (ids.count(i), i) for i in sorted(set(ids), key=str) if ids.count(i) > 1]
    for r in rl:
        if not isinstance(r, dict):
            continue
        v = r.get("ruling")
        counts[str(v)] = counts.get(str(v), 0) + 1
        if v not in RULINGS:
            problems.append("ruling %r on %s" % (v, r.get("id")))
        for o in r.get("orders") or []:
            to = o.get("to") if isinstance(o, dict) else None
            if not (to in TO_FIXED or (isinstance(to, str) and re.fullmatch(r"author_fixup:W[1-6]", to))):
                problems.append("order to %r on %s" % (to, r.get("id")))
    gate = d.get("gate")
    if isinstance(gate, dict):
        problems += ["gate.%s not %s" % (k, t.__name__) for k, t in GATE.items() if not isinstance(gate.get(k), t)]
    else:
        problems.append("gate not an object")
    cwo = d.get("corpus_wide_orders")
elif d is not None:
    problems.append("not one JSON object")
work = sorted(p.name for p in (out_dir / "work").iterdir()) if (out_dir / "work").is_dir() else []
row = {
    "schema": "m8_attempt_receipt.v1", "record_kind": "completion", "book": "1Cor",
    "attempt_id": att, "amends_execution_id": eid, "lane": "controlling_r%d" % a.round,
    "agent_id": a.agent_id, "model_ordered": "claude-opus-5-5",
    "model_actual": "UNAVAILABLE (the notification does not report the served model)",
    "model_actual_tier": "UNAVAILABLE", "grader_role": "grader_fallback (OW-25; Fable's controlling role, OW-30)",
    "outcome": a.outcome, "notification_time": NOW + " (the orchestrator's read of the notification, measured by this "
    "script's clock when the landing row was built; an upper bound; the notification carried no time)",
    "tokens_notification_unit": a.tokens,
    "tokens_spend_unit": "UNAVAILABLE (the notification reports subagent_tokens only)",
    "token_note": "subagent_tokens from the completion notification; OW-28 tracked, not enforced",
    "tool_uses": a.tool_uses, "duration_ms": a.duration_ms, "out_dir": str(out_dir).replace("\\", "/"),
    "outputs": ([{"path": str(f).replace("\\", "/"), "sha256": hashlib.sha256(b).hexdigest()}] if b else []),
    "result_summary": a.summary,
    "orchestrator_verification": {
        "method": "make_ctl_landing.py: JSON parse, schema keys, ids, one ruling per queue id (%d ids from %s), ruling "
                  "set, order targets, gate field types, CR count (MEASURED)" % (len(qids), qf.name),
        "problems": problems, "ruling_counts": counts,
        "corpus_wide_orders": len(cwo) if isinstance(cwo, list) else None,
        "gate": gate if isinstance(gate, dict) else None},
    "for_fable_end_review": a.note,
    "working_files_count": len(work), "working_files_manifest": work,
    "lane_verdict": ("LANDED_FORM_OK (form only; the rulings bind the orchestrator's next acts, within the owner's grants)"
                     if not problems else "LANDED_WITH_FORM_PROBLEMS"),
}
Path(a.out).write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"row_built": eid, "problems": problems, "rulings": counts, "gate": row["orchestrator_verification"]["gate"],
                  "work_files": len(work)}))
