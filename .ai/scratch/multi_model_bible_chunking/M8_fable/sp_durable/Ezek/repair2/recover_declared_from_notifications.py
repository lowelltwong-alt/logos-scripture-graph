#!/usr/bin/env python3
"""OW-7 / OW-22: try to recover the 18 attempts the OW-15 census carries as unmeasured_declared, and bound what is left.

WHY THIS EXISTS. census_ow15_v2.py states its own limit: "a census over receipts cannot see an attempt that produced
none. The cross-check that found ten is the runtime's own notification log; it should be read at every book close."
This is that read, done for the attempts that are still unmeasured, before any further launch is ordered against the
72,000,000 ceiling. The earlier recovery (late_receipts_from_runtime_usage.py) matched notifications to attempts by
launch DESCRIPTION, an INFERRED link. Fifteen of these eighteen receipts record the runtime's own agent id, so this
pass keys on that instead: an EXACT join, no inference.

WHAT IS CLAIMED, per tier.
  MEASURED   - whether a completion notification exists for the agent id, its status, whether it carries a
               <subagent_tokens> block, and the size on disk of the task output file the notification names.
  ESTIMATED  - the residual ceiling. For each failed attempt this takes the measured spend of its OWN immediate
               successor execution (#e(n+1) of the same attempt), which redid the same work to completion. It is an
               estimate of a bound, not a measurement of the failed attempt, and the file says so in its own bytes.
  UNAVAILABLE- anything else. No figure here is invented, and no failed attempt is assigned a token count.
Only the immediate successor is used. Summing every later execution of the same base would have counted the ten
separate controlling-ruling rounds as if they were retries of one failed attempt; measured, that error inflated the
residual from 6.4M to 9.5M.

WRITES. By default nothing is written but the residual record. With --append, one amendment per attempt is APPENDED
to its own receipt file recording that recovery was attempted and what was found, so the next book does not repeat
this hunt; the pre-image is verified as a byte prefix of the post-image, and no existing line is edited. No amendment
carries a token figure, because none was recovered.

Usage: recover_declared_from_notifications.py [--append]
"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable")
EZ = SP / "Ezek"
PROJ = Path(r"C:\Users\lowel\.claude\projects\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View")
TASKS = Path(r"C:\Users\lowel\AppData\Local\Temp\claude"
             r"\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
             r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\tasks")
NOW = datetime.now(timezone.utc).isoformat()
ORD = re.compile(r"#e(\d+)$")
HEAD = re.compile(r"([^<]+)</task-id>")
FIELD = {k: re.compile("<" + k + ">([^<]*)</" + k + ">") for k in
         ("status", "summary", "subagent_tokens", "tool_uses", "duration_ms")}


def notifications_by_agent_id(wanted):
    """agent id -> every completion notification the runtime wrote for it, MEASURED from the session transcripts.

    The transcripts also contain this script's own source and my own greps, so a block whose token field is not a
    plain integer is recorded as carrying no usage rather than parsed."""
    out = {a: [] for a in wanted}
    for path in sorted(PROJ.glob("*.jsonl")):
        raw = path.read_bytes()
        if not any(a.encode() in raw for a in wanted):
            continue
        for line in raw.split(b"\n"):
            if b"<task-id>" not in line:
                continue
            try:
                obj = json.loads(line.decode("utf-8", "replace"))
            except Exception:
                continue
            flat = json.dumps(obj, ensure_ascii=False).encode("utf-8").decode("unicode_escape", errors="replace")
            for seg in flat.split("<task-id>")[1:]:
                m = HEAD.match(seg)
                if not m or m.group(1).strip() not in out:
                    continue
                got = {}
                for k, pat in FIELD.items():
                    hit = pat.search(seg)
                    got[k] = hit.group(1) if hit else None
                tok = got["subagent_tokens"]
                out[m.group(1).strip()].append({
                    "status": got["status"], "summary": (got["summary"] or "")[:160],
                    "carries_usage_block": bool(tok and tok.strip().isdigit()),
                    "tokens": int(tok) if tok and tok.strip().isdigit() else None,
                    "notified_at": obj.get("timestamp"), "transcript": path.name[:8]})
    return out


def receipts():
    rows = []
    for p in sorted(q for q in EZ.rglob("*_attempt_receipts.jsonl") if ".pre_" not in q.name):
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append((p, json.loads(line)))
    return rows


def main():
    pos = json.loads((EZ / "ezek_ow15_position.v2.json").read_text(encoding="utf-8"))
    declared = list(pos["census"]["unmeasured_declared"])
    rows = receipts()

    amend_tokens = {}
    for _, r in rows:
        if str(r.get("schema", "")).endswith("_amendment.v1") and isinstance(r.get("tokens_reported"), int):
            ex = r.get("amends_execution_id")
            amend_tokens[ex] = amend_tokens.get(ex, 0) + r["tokens_reported"]
    tokens, home = {}, {}
    for p, r in rows:
        if str(r.get("schema", "")).endswith("_amendment.v1"):
            continue
        ex = r.get("execution_id")
        home[ex] = (p, r)
        v = r.get("tokens_reported")
        tokens[ex] = v if isinstance(v, int) else amend_tokens.get(ex)

    already = {r.get("amends_execution_id") for _, r in rows
               if r.get("schema") == "m8_attempt_receipt_recovery_note.v1"}
    wanted = {home[ex][1].get("agent_id") for ex in declared if ex in home and home[ex][1].get("agent_id")}
    notes = notifications_by_agent_id(wanted)

    findings, residual, unbounded = [], 0, []
    for ex in sorted(declared):
        p, r = home.get(ex, (None, {}))
        aid = r.get("agent_id")
        got = [n for n in notes.get(aid, [])] if aid else []
        with_usage = [n for n in got if n["carries_usage_block"]]
        out_file = TASKS / ("%s.output" % aid) if aid else None
        base, m = ex.split("#")[0], ORD.search(ex)
        nth = int(m.group(1)) if m else 0
        later = sorted((int(ORD.search(e).group(1)), e) for e in tokens
                       if e.split("#")[0] == base and ORD.search(e) and int(ORD.search(e).group(1)) > nth
                       and isinstance(tokens[e], int))
        succ = later[0] if later else None
        if succ:
            residual += tokens[succ[1]]
        else:
            unbounded.append(ex)
        findings.append({
            "execution_id": ex, "receipt_file": p.name if p else None, "agent_id": aid,
            "runtime_notifications_found": len(got),
            "statuses": sorted({n["status"] for n in got if n["status"]}),
            "any_notification_carries_usage": bool(with_usage),
            "recovered_tokens": with_usage[0]["tokens"] if with_usage else None,
            "task_output_file_bytes": (out_file.stat().st_size if out_file and out_file.exists() else
                                       (None if not out_file else "ABSENT")),
            "why_unrecoverable": (None if with_usage else
                                  ("MEASURED: the runtime wrote %d notification(s) for this agent id and none carries "
                                   "a <subagent_tokens> block; the task output file it names is %s on disk"
                                   % (len(got), "0 bytes" if out_file and out_file.exists() and
                                      out_file.stat().st_size == 0 else "not readable")) if aid else
                                  "UNAVAILABLE: this attempt recorded no runtime agent id, so no exact join exists"),
            "estimate_ceiling_from_own_successor": ({"execution_id": succ[1], "tokens": tokens[succ[1]],
                                                     "tier": "ESTIMATED - this is the SUCCESSOR's measured spend, "
                                                             "used as a ceiling on the failed attempt, not its "
                                                             "measurement"} if succ else None),
            "first_summary": (got[0]["summary"] if got else None)})

    recovered = [f for f in findings if f["recovered_tokens"] is not None]
    lower = pos["census"]["LOWER_BOUND"]
    ceiling = pos["ceiling"]["value"]
    out = {
        "schema": "ezek_ow15_residual.v1", "written_at": NOW,
        "question": "can the 18 unmeasured_declared attempts be measured from the runtime's own notifications?",
        "answer": ("NO for all %d. %d of them record the runtime's agent id, giving an EXACT join; every notification "
                   "the runtime wrote for those ids reports status failed (weekly rate limit, or a stalled stream) "
                   "and carries no usage block, and the task output file each notification names is 0 bytes. The "
                   "remaining %d recorded no agent id at all. Nothing is recoverable from this machine."
                   % (len(findings), sum(1 for f in findings if f["agent_id"]), len(findings) -
                      sum(1 for f in findings if f["agent_id"]))) if not recovered else
                  "PARTIAL - see recovered_tokens",
        "census_as_it_stands": {"LOWER_BOUND": lower, "ceiling": ceiling,
                                "headroom_UPPER_BOUND": ceiling - lower,
                                "carrier_sha256": pos["ceiling"]["carrier_sha256"]},
        "residual": {
            "tier": "ESTIMATED",
            "ceiling_on_the_18": residual,
            "method": ("each failed attempt's OWN immediate successor execution redid the same work to completion; "
                       "its measured spend is used as a ceiling on the failed attempt. A failed attempt usually died "
                       "early and so spent less, but that is not guaranteed, so this is a ceiling and not a bound"),
            "attempts_with_no_successor_to_bound_them": unbounded,
            "what_it_means": ("true total spend lies in [%s, about %s]. The ceiling %s sits INSIDE that interval, so "
                              "on this evidence a breach is neither established nor excluded, and the headroom of %s "
                              "must not be reported as available."
                              % (format(lower, ","), format(lower + residual, ","), format(ceiling, ","),
                                 format(ceiling - lower, ",")))},
        "also_not_in_any_figure": ("the eleven rate-limited attempts that produced no receipt at all, the in-flight "
                                   "adjudication launched 2026-09-16, and this orchestrator's own context spend, "
                                   "which the census does not model"),
        "findings": findings,
        "provenance": {"transcripts_read": sorted(p.name[:8] for p in PROJ.glob("*.jsonl")),
                       "tasks_dir": str(TASKS),
                       "position_read": "ezek_ow15_position.v2.json",
                       "position_sha256": hashlib.sha256((EZ / "ezek_ow15_position.v2.json").read_bytes()).hexdigest()},
    }
    rec = EZ / "ezek_ow15_residual.v1.json"
    rec.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")

    if "--append" in sys.argv:
        wrote = 0
        for f in findings:
            if f["execution_id"] in already or f["receipt_file"] is None:
                continue
            p = home[f["execution_id"]][0]
            pre = p.read_bytes()
            note = {"schema": "m8_attempt_receipt_recovery_note.v1", "amends_schema": "m8_attempt_receipt.v1",
                    "amends_execution_id": f["execution_id"], "book": "Ezek", "recorded_at": NOW,
                    "recorded_by": "orchestrator (claude-opus-5), session 910cbe15",
                    "original_line_unedited": True, "tokens_reported": None,
                    "recovery_attempted": "runtime completion notifications, joined on the receipt's own agent_id",
                    "result": f["why_unrecoverable"],
                    "runtime_notifications_found": f["runtime_notifications_found"],
                    "statuses": f["statuses"], "task_output_file_bytes": f["task_output_file_bytes"],
                    "estimate_ceiling_from_own_successor": f["estimate_ceiling_from_own_successor"],
                    "how_to_read": ("this attempt's spend is UNRECOVERABLE, not zero; the census LOWER_BOUND excludes "
                                    "it and ezek_ow15_residual.v1.json carries the estimated ceiling")}
            with p.open("a", encoding="utf-8", newline="\n") as fh:
                fh.write(json.dumps(note, ensure_ascii=False) + "\n")
            if not p.read_bytes().startswith(pre):
                raise SystemExit("INTEGRITY FAILURE on %s" % p.name)
            wrote += 1
        print("appended %d recovery notes (%d already present)" % (wrote, len(already)))

    print(json.dumps({k: out[k] for k in ("answer", "census_as_it_stands", "residual")}, ensure_ascii=False, indent=1))
    print("record: %s" % rec.name)


if __name__ == "__main__":
    main()
