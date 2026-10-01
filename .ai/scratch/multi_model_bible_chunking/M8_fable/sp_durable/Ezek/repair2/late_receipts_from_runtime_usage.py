#!/usr/bin/env python3
"""OW-7 CAPTURE RECOVERY: late attempt receipts, and amendments, from the runtime's own completion notifications.

WHAT WAS MISSING. Ten attempts launched in session 910cbe15 never received an attempt receipt - the six author-wave
lanes, the remediation batch and the three spot-review lanes - so the OW-15 census, which sums receipt rows, could
not see 3,476,769 tokens of real spend. Four more attempts carry receipts declaring their token figure UNAVAILABLE
(the #e12, #e13 and #e14 rulings and the boss audit) although the runtime DID report their usage in each completion
notification. The session transcript preserves those notifications, so the figures are recoverable as MEASURED
runtime values rather than estimated.

WHAT IS AND IS NOT CLAIMED, per field. tokens / tool uses / duration / completion time: MEASURED - copied from the
runtime's notification text in the session transcript. The link between a notification and an attempt: INFERRED from
the agent description the orchestrator gave at launch, the completion time, and (where the queue recorded one) the
landed deliverable digest - these launches recorded no agent id and no attempt id, so no exact key exists. Attempt ids
for the ten unreceipted attempts are ASSIGNED LATE here and say so. Every figure this script cannot support is
UNAVAILABLE with its reason. Nothing existing is edited: new files are created, and amendments are APPENDED with the
pre-image verified as a byte prefix of the post-image.
"""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
TRANSCRIPT = Path(r"C:\Users\lowel\.claude\projects\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
                  r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4.jsonl")
NOW = datetime.now(timezone.utc).isoformat()
SESSION = "910cbe15-396b-4a0e-82f6-8aa1e2edf1e4"

pat = re.compile(r"<task-id>([^<]+)</task-id>.*?<status>([^<]+)</status>.*?<summary>([^<]*)</summary>.*?"
                 r"<subagent_tokens>(\d+)</subagent_tokens>\s*<tool_uses>(\d+)</tool_uses>\s*"
                 r"<duration_ms>(\d+)</duration_ms>", re.S)
notes = {}
with TRANSCRIPT.open(encoding="utf-8", errors="replace") as fh:
    for line in fh:
        if "subagent_tokens" not in line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        s = json.dumps(obj, ensure_ascii=False).encode("utf-8").decode("unicode_escape", errors="replace")
        for m in pat.finditer(s):
            tid, st, summ, tok, tu, ms = m.groups()
            desc = re.sub(r'^Agent \\?"|\\?" finished$', "", summ.strip())
            notes.setdefault(desc, {"agent_id": tid, "status": st, "tokens": int(tok), "tool_uses": int(tu),
                                    "duration_ms": int(ms), "notified_at": obj.get("timestamp")})


def note(desc):
    hits = [v for k, v in notes.items() if k == desc]
    if len(hits) != 1:
        raise SystemExit("REFUSED: expected exactly one notification described %r, found %d" % (desc, len(hits)))
    return hits[0]


ATTR = ("INFERRED - no agent id or attempt id was recorded at launch; the link rests on the launch description, the "
        "completion time and, where recorded, the landed deliverable digest")
PROV = {"transcript": str(TRANSCRIPT), "transcript_sha256_at_read": hashlib.sha256(TRANSCRIPT.read_bytes()).hexdigest(),
        "read_at": NOW, "read_by": "orchestrator (claude-opus-5), session " + SESSION}

LATE = [
    ("author/ezek_author_wave_attempt_receipts.jsonl", "ezek_author_wave_lane_01_a1", "Author lane 01", "ezek_author_wave",
     "34ed205eac2e", "E13-71"),
    ("author/ezek_author_wave_attempt_receipts.jsonl", "ezek_author_wave_lane_02_a1", "Author lane 02", "ezek_author_wave",
     "2e2215e2ddd63c2a68e3c951ba8ea0c65a946ba9307741a1c6197f8b29daa630", "E13-75"),
    ("author/ezek_author_wave_attempt_receipts.jsonl", "ezek_author_wave_lane_03_a1", "Author lane 03", "ezek_author_wave",
     None, "E13-76/E13-78"),
    ("author/ezek_author_wave_attempt_receipts.jsonl", "ezek_author_wave_lane_04_a1", "Author lane 04", "ezek_author_wave",
     "2378ecf952b6", "E13-71"),
    ("author/ezek_author_wave_attempt_receipts.jsonl", "ezek_author_wave_lane_05_a1", "Author lane 05", "ezek_author_wave",
     "fd8ad6330bf8ec34f8891213b8437dec7ddf5c73f60c65124e9ebd1151513a3a", "E13-75"),
    ("author/ezek_author_wave_attempt_receipts.jsonl", "ezek_author_wave_lane_06_a1", "Author lane 06", "ezek_author_wave",
     None, "E13-76/E13-78"),
    ("author/ezek_remediation_attempt_receipts.jsonl", "ezek_remediation_batch_a1", "Ezekiel remediation batch",
     "ezek_author_wave_remediation", None, "E13-82/E13-83/E13-86"),
    ("reviews/spot/ezek_spot_attempt_receipts.jsonl", "ezek_spot_s01_a1", "Spot review lane 1", "ezek_spot_wave",
     "973b3bae714acf58", "E13-91"),
    ("reviews/spot/ezek_spot_attempt_receipts.jsonl", "ezek_spot_s02_a1", "Spot review lane 2", "ezek_spot_wave",
     "52d9c0abcb1479ff", "E13-91"),
    ("reviews/spot/ezek_spot_attempt_receipts.jsonl", "ezek_spot_s03_a1", "Spot review lane 3", "ezek_spot_wave",
     "76efe203be9b6193", "E13-88"),
]
AMEND = [
    ("reviews/ezek_rulings_attempt_receipts.jsonl", "ezek_e12_ruling_a1#e1", "Ezek e12 Fable ruling"),
    ("reviews/ezek_rulings_attempt_receipts.jsonl", "ezek_e13_ruling_a1#e1", "Ezek e13 Fable ruling"),
    ("reviews/ezek_rulings_attempt_receipts.jsonl", "ezek_e14_ruling_a1#e1", "Ezek e14 focused ruling"),
    ("reviews/ezek_boss_attempt_receipts.jsonl", "ezek_boss_audit_a1#e1", "Ezek boss audit"),
]

by_file, results = {}, []
for rel, attempt, desc, lane, dsha, qref in LATE:
    n = note(desc)
    by_file.setdefault(rel, []).append({
        "schema": "m8_attempt_receipt.v1", "lane": lane, "book": "Ezek",
        "attempt_id": attempt, "execution_id": attempt + "#e1", "execution_of": attempt, "execution_ordinal": 1,
        "previous_execution_id": None, "retry_of": None,
        "attempt_id_assigned_late": True,
        "agent": desc, "agent_id": n["agent_id"], "parent_agent_id": "orchestrator",
        "session": SESSION, "model": "claude-opus-5 (session default)",
        "model_actual": "UNAVAILABLE - the runtime exposed no effective-model record; never inferred",
        "outcome": "COMPLETED (runtime status %s); its output was landed and applied as the queue entries %s record" % (
            n["status"], qref),
        "deliverable_sha256": dsha or ("UNAVAILABLE - the queue records no deliverable digest for this attempt; its "
                                       "work reached the rows through the wave's sweep receipts"),
        "queue_refs": qref,
        "tokens_reported": n["tokens"], "tool_uses": n["tool_uses"], "duration_ms": n["duration_ms"],
        "completed_notified_at": n["notified_at"],
        "token_note": "runtime-reported subagent tokens from the completion notification preserved in the session transcript",
        "tiers": {"tokens_tool_uses_duration": "MEASURED (runtime-reported)", "attempt_attribution": ATTR},
        "why_late": ("no attempt receipt was written when this attempt landed - an OW-7 capture gap found on "
                     "2026-09-16 when a review of the step-3 docket looked for this lane's escalations"),
        "recovered_from": PROV, "recorded_at": NOW,
    })
    results.append((attempt, n["tokens"]))

pre_images = {}
for rel, rows in by_file.items():
    p = EZ / rel
    if p.exists():
        existing = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
        taken = {r.get("execution_id") for r in existing}
        if any(r["execution_id"] in taken for r in rows):
            raise SystemExit("REFUSED: a receipt already exists in %s" % rel)
        pre_images[rel] = p.read_bytes()
    else:
        pre_images[rel] = b""
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

for rel, exec_id, desc in AMEND:
    p = EZ / rel
    existing = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not any(r.get("execution_id") == exec_id for r in existing):
        raise SystemExit("REFUSED: no receipt %s in %s" % (exec_id, rel))
    if any(r.get("amends_execution_id") == exec_id and isinstance(r.get("tokens_reported"), int) for r in existing):
        raise SystemExit("REFUSED: %s already has a token amendment" % exec_id)
    n = note(desc)
    pre_images.setdefault(rel, p.read_bytes())
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({
            "schema": "m8_attempt_receipt_amendment.v1", "amends_schema": "m8_attempt_receipt.v1",
            "amends_execution_id": exec_id, "book": "Ezek", "recorded_at": NOW,
            "recorded_by": "orchestrator (claude-opus-5), session " + SESSION, "original_line_unedited": True,
            "what_this_amendment_adds": "the runtime-reported token figure the original receipt declared UNAVAILABLE",
            "tokens_reported": n["tokens"], "tool_uses": n["tool_uses"], "duration_ms": n["duration_ms"],
            "agent_id": n["agent_id"], "completed_notified_at": n["notified_at"],
            "token_note": ("FULL execution figure from the runtime's completion notification preserved in the session "
                           "transcript - not a segment"),
            "tiers": {"tokens": "MEASURED (runtime-reported)", "attempt_attribution": ATTR},
            "why": ("the original receipt said the runtime handed the orchestrator no token figure; the completion "
                    "notification in the session transcript carries one, so UNAVAILABLE was wrong as a value"),
            "recovered_from": PROV,
            "how_to_read": "a consumer resolves amendments: this execution's token figure is the one given here",
        }, ensure_ascii=False) + "\n")
    results.append((exec_id + " (amendment)", n["tokens"]))

for rel, pre in pre_images.items():
    post = (EZ / rel).read_bytes()
    if not post.startswith(pre):
        raise SystemExit("INTEGRITY FAILURE: %s pre-image is not a prefix of its post-image" % rel)
print(json.dumps({"written": results, "late_receipt_tokens": sum(t for a, t in results if "amendment" not in a),
                  "amended_tokens": sum(t for a, t in results if "amendment" in a),
                  "files": {rel: hashlib.sha256((EZ / rel).read_bytes()).hexdigest() for rel in pre_images},
                  "prefix_verified": True}, indent=1))
