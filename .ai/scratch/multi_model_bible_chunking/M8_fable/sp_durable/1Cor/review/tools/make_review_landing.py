"""Build one 1Cor review landing row (m8_attempt_receipt.v1 completion) from the deliverable's bytes plus notification facts.

The landing check is MEASURED here on the deliverable: it parses as one JSON object, carries every top-level key of the
brief's schema, names this attempt and execution, has a verdict from the brief's set, and has no CR bytes. A deliverable
that fails is still landed (the outcome must then say so), but the row records each failure. notification_time is
stamped by this script's clock (E-78 candidate); there is no --notified.

usage: make_review_landing.py --lane S1 [--execution N] --agent-id ID --tokens N --tool-uses N --duration-ms N
       --outcome TEXT --summary TEXT [--note TEXT ...] --out FILE
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path

P = Path("C:/Users/lowel/AppData/Local/Temp/claude/C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View/af84b702-d913-4495-8e57-252cf7894c63/scratchpad")
LANES = {"S1": ("cor_writer_wave_spot_review_s1_a1", "cor_s1", "1cor_writer_wave_spot_review_S1.json", "review_S1"),
         "S2": ("cor_fixup_wave_review_s2_a1", "cor_s2", "1cor_fixup_wave_review_S2.json", "review_S2"),
         "S3": ("cor_fixup2_review_s3_a1", "cor_s3_out", "1cor_fixup2_review_S3.json", "review_S3"),
         "S5": ("cor_fixup3_review_s5_a1", "cor_s5_out", "1cor_fixup3_review_S5.json", "review_S5"),
         "S6": ("cor_fixup4_review_s6_a1", "cor_s6_out", "1cor_fixup4_review_S6.json", "review_S6")}
# Per lane: the brief's top-level keys, the verdict key and its value set (S2: BRIEF_S2.md deliverable section).
SCHEMA = {"S1": (("attempt_id", "execution_id", "verdict", "rows_file_reviewed", "artifacts_reviewed", "form", "seams",
                  "row_sample", "bytes", "book_wide", "flags", "confidence", "new_findings", "unresolved_uncertainty"),
                 "verdict", ("fit_to_accept", "fit_with_changes", "not_fit")),
          "S2": (("attempt_id", "execution_id", "readiness", "changes_required", "rows_file_reviewed",
                  "artifacts_reviewed", "conditions", "tool_fix_receipts", "fixup1_spans", "suite", "cwo",
                  "ruled_findings", "unresolved_uncertainty_bearing", "carried_items", "changed_rows",
                  "untouched_sample", "digests", "new_findings", "unresolved_uncertainty"),
                 "readiness", ("fit", "fit_with_changes")),
          # S3: BRIEF_S3.md deliverable section (fixup2_spans in place of fixup1_spans)
          "S3": (("attempt_id", "execution_id", "readiness", "changes_required", "rows_file_reviewed",
                  "artifacts_reviewed", "conditions", "tool_fix_receipts", "fixup2_spans", "suite", "cwo",
                  "ruled_findings", "unresolved_uncertainty_bearing", "carried_items", "changed_rows",
                  "untouched_sample", "digests", "new_findings", "unresolved_uncertainty"),
                 "readiness", ("fit", "fit_with_changes")),
          # S5: BRIEF_S5.md deliverable section (fixup3_spans; no S4 ran, GATE-E4 names S5 next)
          "S5": (("attempt_id", "execution_id", "readiness", "changes_required", "rows_file_reviewed",
                  "artifacts_reviewed", "conditions", "tool_fix_receipts", "fixup3_spans", "suite", "cwo",
                  "ruled_findings", "unresolved_uncertainty_bearing", "carried_items", "changed_rows",
                  "untouched_sample", "digests", "new_findings", "unresolved_uncertainty"),
                 "readiness", ("fit", "fit_with_changes")),
          # S6: BRIEF_S6.md deliverable section (delta check of FIXUP-4; BRIEF_DELTA.template.md)
          "S6": (("attempt_id", "execution_id", "readiness", "changes_required", "rows_file_reviewed",
                  "artifacts_reviewed", "conditions", "spans", "orders", "changed_text", "manifest", "suite", "cwo",
                  "new_findings", "unresolved_uncertainty"),
                 "readiness", ("fit", "fit_with_changes"))}
ROUTES = ("orchestrator_cwo", "tool_fix", "controlling_agent", "fable_end_review")
# Close-kit lanes come from the data table (TE-1); a new lane is a row there, not an edit here.
CLOSE = json.loads((Path(__file__).resolve().parents[2] / "close" / "close_lanes.v1.json").read_text(encoding="utf-8"))["lanes"]
for _l, _e in CLOSE.items():
    LANES[_l] = (_e["attempt"], _e["out_dir"], _e["deliverable"], _e["review_lane"])
    SCHEMA[_l] = (tuple(_e["keys"]), _e["verdict_key"], tuple(_e["verdicts"]))
ap = argparse.ArgumentParser()
for k in ("--lane", "--agent-id", "--outcome", "--summary", "--out"):
    ap.add_argument(k, required=True)
for k in ("--tokens", "--tool-uses", "--duration-ms"):
    ap.add_argument(k, required=True, type=int)
ap.add_argument("--execution", type=int, default=1)
ap.add_argument("--note", action="append", default=[])
a = ap.parse_args()
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
att, out, deliv, lane = LANES[a.lane]
KEYS, VKEY, VERDICTS = SCHEMA[a.lane]
tag = "" if a.execution == 1 else "_e%d" % a.execution
eid = "%s#e%d" % (att, a.execution)
out_dir = P / (out + tag)
f = out_dir / deliv
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
if isinstance(d, dict):
    problems += ["missing key %s" % k for k in KEYS if k not in d]
    if d.get("attempt_id") != att:
        problems.append("attempt_id %r" % d.get("attempt_id"))
    if d.get("execution_id") != eid:
        problems.append("execution_id %r" % d.get("execution_id"))
    if d.get(VKEY) not in VERDICTS:
        problems.append("%s %r" % (VKEY, d.get(VKEY)))
    if a.lane in ("S2", "S3", "S5", "S6"):
        cr = d.get("changes_required")
        if d.get("readiness") == "fit_with_changes" and not (isinstance(cr, list) and cr):
            problems.append("fit_with_changes with no changes_required")
        for c in cr if isinstance(cr, list) else []:
            r = c.get("route", "") if isinstance(c, dict) else ""
            if not (isinstance(c, dict) and c.get("id") and isinstance(c.get("rows"), list) and c["rows"]):
                problems.append("change %r names no rows" % (c.get("id") if isinstance(c, dict) else c))
            if not (r in ROUTES or (r.startswith("fixup:W") and r[7:].isdigit())):
                problems.append("change %r route %r" % (c.get("id") if isinstance(c, dict) else c, r))
elif d is not None:
    problems.append("not one JSON object")
nf = d.get("new_findings") if isinstance(d, dict) else None
sev = {}
for x in nf if isinstance(nf, list) else []:
    s = x.get("severity") if isinstance(x, dict) else None
    sev[str(s)] = sev.get(str(s), 0) + 1
work = sorted(p.name for p in (out_dir / "work").iterdir()) if (out_dir / "work").is_dir() else []
row = {
    "schema": "m8_attempt_receipt.v1", "record_kind": "completion", "book": "1Cor",
    "attempt_id": att, "amends_execution_id": eid, "lane": lane,
    "agent_id": a.agent_id, "model_ordered": "claude-opus-5-5",
    "model_actual": "UNAVAILABLE (the notification does not report the served model)",
    "model_actual_tier": "UNAVAILABLE", "grader_role": "grader_fallback (OW-25)",
    "outcome": a.outcome, "notification_time": NOW + " (the orchestrator's read of the notification, measured by this "
    "script's clock when the landing row was built; an upper bound; the notification carried no time)",
    "tokens_notification_unit": a.tokens,
    "tokens_spend_unit": "UNAVAILABLE (the notification reports subagent_tokens only)",
    "token_note": "subagent_tokens from the completion notification; OW-28 tracked, not enforced",
    "tool_uses": a.tool_uses, "duration_ms": a.duration_ms, "out_dir": str(out_dir).replace("\\", "/"),
    "outputs": ([{"path": str(f).replace("\\", "/"), "sha256": hashlib.sha256(b).hexdigest()}] if b else []),
    "result_summary": a.summary,
    "orchestrator_verification": {
        "method": "make_review_landing.py: JSON parse, schema keys, ids, verdict set, CR count (MEASURED)",
        "problems": problems, "verdict_field": d.get(VKEY) if isinstance(d, dict) else None,
        "new_findings": len(nf) if isinstance(nf, list) else None, "severity_counts": sev},
    "for_fable_end_review": a.note,
    "working_files_count": len(work), "working_files_manifest": work,
    "lane_verdict": ("LANDED_FORM_OK (form only; the findings are claims for the controlling execution, not facts)"
                     if not problems else "LANDED_WITH_FORM_PROBLEMS"),
}
Path(a.out).write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"row_built": eid, "problems": problems, "verdict": row["orchestrator_verification"]["verdict_field"],
                  "severity": sev, "work_files": len(work)}))
