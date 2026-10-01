#!/usr/bin/env python3
"""E-38's cure, run as a tool: reconcile the receipt census against the runtime's own completion notifications.

A census over receipts cannot see an attempt that produced none. The denominator is the runtime's notification log:
every '<task-notification>' in the orchestrating session's transcript carries the agent's id and its runtime-reported
subagent tokens. This tool reads that log (read-only), matches each notified agent id to receipts by agent_id, and
reports (a) notified agents with NO receipt, (b) receipts whose token figure differs from the notification, and
(c) the restated position against the carrier's ceiling. It writes Ezek/ezek_ow15_position.v3.json and appends nothing
to any receipt file.

usage: python census_reconcile_notifications.py --transcript <session.jsonl>
"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent
SP = EZ.parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
T = Path(sys.argv[sys.argv.index("--transcript") + 1])
NOTE = re.compile(r"<task-id>([0-9a-z]+)</task-id>.*?<status>([a-z_]+)</status>.*?(?:<subagent_tokens>(\d+)</subagent_tokens>)?", re.S)

notified = {}
for line in T.read_text(encoding="utf-8", errors="replace").splitlines():
    if "<task-notification>" not in line:
        continue
    try:
        d = json.loads(line)
    except json.JSONDecodeError:
        continue
    blob = json.dumps(d, ensure_ascii=False)
    blob = blob.encode("utf-8").decode("unicode_escape", errors="ignore") if "\\u003c" in blob else blob
    for chunk in blob.split("<task-notification>")[1:]:
        m_id = re.search(r"<task-id>([0-9a-z]+)</task-id>", chunk)
        m_tok = re.search(r"<subagent_tokens>(\d+)</subagent_tokens>", chunk)
        m_st = re.search(r"<status>([a-z_]+)</status>", chunk)
        if m_id and m_tok:
            notified[m_id.group(1)] = {"tokens": int(m_tok.group(1)), "status": m_st.group(1) if m_st else None}

receipts = {}
for f in sorted(EZ.rglob("*attempt_receipts.jsonl")):
    for l in f.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        r = json.loads(l)
        aid = r.get("agent_id")
        if aid and isinstance(r.get("tokens_reported"), int):
            receipts.setdefault(aid, []).append({"file": str(f.relative_to(EZ)), "execution_id": r.get("execution_id"), "tokens": r["tokens_reported"]})

# Older receipts (primaries, peers, boss, rulings, author wave) predate the agent_id field, so an id match alone reads a
# MISSING KEY as a missing receipt (a first run reported 61 'unreceipted' agents and a negative headroom that was an
# artifact). Fallback: an unmatched notification is receipted if its exact runtime token figure appears as an integer
# in any receipt or amendment row (runtime figures are 5-7 digit integers; a collision is reported, not assumed away).
all_ints = {}
for f in sorted(EZ.rglob("*attempt_receipts.jsonl")):
    for l in f.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        r = json.loads(l)
        for n in re.findall(r"(?<![\d.])(\d{5,7})(?![\d.])", json.dumps(r)):
            all_ints.setdefault(int(n), []).append({"file": str(f.relative_to(EZ)), "execution_id": r.get("execution_id") or r.get("amends")})
matched_by_figure = {k: {"tokens": v["tokens"], "receipt_rows": all_ints[v["tokens"]]} for k, v in notified.items()
                     if k not in receipts and v["tokens"] in all_ints}
no_receipt = {k: v for k, v in notified.items() if k not in receipts and k not in matched_by_figure}
mismatch = {k: {"notified": v["tokens"], "receipts": receipts[k]} for k, v in notified.items()
            if k in receipts and sum(x["tokens"] for x in receipts[k]) != v["tokens"]}
pos2 = json.loads((EZ / "ezek_ow15_position.v2.json").read_text(encoding="utf-8"))
t0 = pos2["restated_at"]
since = 0
for f in sorted(EZ.rglob("*attempt_receipts.jsonl")):
    for l in f.read_text(encoding="utf-8").splitlines():
        if l.strip():
            r = json.loads(l)
            if str(r.get("recorded_at", "")) > t0 and isinstance(r.get("tokens_reported"), int):
                since += r["tokens_reported"]
car = SP / "campaign" / "budget_ceilings.v1.json"
ceiling = json.loads(car.read_text(encoding="utf-8"))["books"]["Ezek"]["ceiling"]
lower = pos2["census"]["LOWER_BOUND"] + since
unreceipted = sum(v["tokens"] for v in no_receipt.values())
out = {"schema": "ezek_ow15_position.v3", "restated_at": datetime.now(timezone.utc).isoformat(),
       "ceiling": {"value": ceiling, "carrier_sha256": sha(car)},
       "census": {"v2_lower_bound": pos2["census"]["LOWER_BOUND"], "receipts_since_v2": since, "LOWER_BOUND": lower},
       "notification_reconciliation": {"transcript": str(T), "transcript_sha256": sha(T), "notified_agents": len(notified),
                                       "matched_by_agent_id": sum(1 for k in notified if k in receipts),
                                       "matched_by_exact_token_figure": len(matched_by_figure),
                                       "figure_collisions": {k: v for k, v in matched_by_figure.items() if len(v["receipt_rows"]) > 1},
                                       "notified_without_receipt": no_receipt, "unreceipted_tokens": unreceipted,
                                       "token_mismatches": mismatch},
       "position_including_unreceipted": lower + unreceipted, "headroom": ceiling - lower - unreceipted,
       "limit": ("the transcript is this orchestrating session's only; agents launched by earlier sessions are covered by the "
                 "v2 reconciliation (E13-101). A notification the runtime never delivered cannot be seen here either."),
       "tier": "MEASURED for every figure present"}
(EZ / "ezek_ow15_position.v3.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("ceiling", "census", "position_including_unreceipted", "headroom")}, indent=1))
print(json.dumps({"notified_agents": len(notified), "notified_without_receipt": no_receipt, "token_mismatches": mismatch}, indent=1)[:3000])
