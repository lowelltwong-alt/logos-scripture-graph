#!/usr/bin/env python3
"""Land one v9 blind delta lane (ezek_fixround_v9_delta_lane_<l>_a1#e1). Then, once both lanes have landed, write the
delta landing manifest that _close_book.py reads.

TRANSCRIPTION. delta_check.json and final_message.md are copied byte for byte from the lane's scratch OUT into
merged_close/delta_v9/delta_<l>/ (write-new: same bytes left, different bytes refused). The receipt records each sha256.

UNITS (OW-28 / E-55). Notification unit: the completion notification's subagent_tokens, passed on the command line
(REPORTED). Spend unit: input + cache_creation + output per unique message id, from the runtime transcript's usage
fields, by census v4's method. Cache reads are recorded beside it, never added (MEASURED). Only message.id,
message.usage and message.model are read from the transcript; no content is read or printed.

RECEIPT. One completion row amending the launch execution id, appended under an exclusive lock. The file's digest is
pinned before, checked after, and rolled back on mismatch (E-44: append, never edit).

MANIFEST (--manifest). Refused unless both lanes carry exactly one completion row and their durable files still match
it. Written new as merged_close/delta_v9/landing_manifest.v1.json, with paths relative to the manifest's own directory.
usage: land_delta_v9.py --lane a|b --notification N --tool-uses N --duration-ms N
       land_delta_v9.py --manifest
"""
import argparse
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
EZ = HERE.parents[1]
SP = EZ.parent
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_fixround_v9")
DV = EZ / "merged_close" / "delta_v9"
REC = HERE / "ezek_fixround_v9_attempt_receipts.jsonl"
PROJ = Path(os.path.expanduser("~")) / ".claude" / "projects" / "C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
FILES = ("delta_check.json", "final_message.md")
M = "claude-opus-5-5"
sha = lambda b: hashlib.sha256(b).hexdigest()      # noqa: E731


def guard(target):
    g = subprocess.run([sys.executable, "-B", str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "Ezek", "--target",
                        target], cwd=str(SP), capture_output=True, text=True, encoding="utf-8",
                       env=dict(os.environ, PYTHONUTF8="1"))
    if json.loads(g.stdout)["verdict"] != "CLEAR":
        raise SystemExit("REFUSED by pin guard on %s: %s" % (target, g.stdout[-300:]))


def receipts():
    b = REC.read_bytes()
    return b, [json.loads(l) for l in b.decode("utf-8").splitlines() if l.strip()]


def append(before, row):
    after = before + (b"" if before.endswith(b"\n") else b"\n") + (json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8")
    lock = REC.with_suffix(REC.suffix + ".lock")
    fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        if REC.read_bytes() != before:
            raise SystemExit("REFUSED: receipts changed under the lock")
        tmp = REC.with_suffix(REC.suffix + ".tmp")
        tmp.write_bytes(after)
        os.replace(tmp, REC)
        if sha(REC.read_bytes()) != sha(after):
            REC.write_bytes(before)
            raise SystemExit("ROLLED BACK: receipt post-write check failed")
    finally:
        os.close(fd)
        lock.unlink()
    return sha(before), sha(after)


def land(L, notification, tool_uses, duration_ms):
    att = "ezek_fixround_v9_delta_lane_%s_a1" % L
    exe = att + "#e1"
    guard("Ezek/repair2/fixround_v9/" + REC.name)
    guard("Ezek/merged_close/delta_v9/delta_%s/delta_check.json" % L)
    before, rows = receipts()
    if any(r.get("amends_execution_id") == exe for r in rows):
        raise SystemExit("REFUSED: a completion row for %s already exists" % exe)
    launch = [r for r in rows if r.get("execution_id") == exe and r.get("record_kind") == "launch"]
    if len(launch) != 1:
        raise SystemExit("REFUSED: expected one launch row for %s" % exe)
    agent = launch[0]["agent_id"]
    out, dur = SCR / ("delta_" + L), DV / ("delta_" + L)
    dur.mkdir(parents=True, exist_ok=True)
    outputs = {}
    for fn in FILES:
        b = (out / fn).read_bytes()
        p = dur / fn
        if p.exists() and p.read_bytes() != b:
            raise SystemExit("REFUSED: %s exists durable with different bytes" % fn)
        if not p.exists():
            shutil.copyfile(out / fn, p)
        if sha(p.read_bytes()) != sha(b):
            raise SystemExit("REFUSED: transcription of %s does not match" % fn)
        outputs[fn] = sha(b)
    dc = json.loads((dur / "delta_check.json").read_text(encoding="utf-8-sig"))

    found = glob.glob(str(PROJ / "*" / "subagents" / ("agent-%s.jsonl" % agent)))
    if len(found) != 1:
        raise SystemExit("REFUSED: expected one transcript for %s, found %d" % (agent, len(found)))
    usage, models = {}, set()
    with open(found[0], encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            m = d.get("message") if isinstance(d, dict) else None
            if isinstance(m, dict) and m.get("id") and isinstance(m.get("usage"), dict):
                usage[m["id"]] = m["usage"]
                if m.get("model"):
                    models.add(m["model"])
    g = lambda k: sum(int(u.get(k) or 0) for u in usage.values())               # noqa: E731
    spend = g("input_tokens") + g("cache_creation_input_tokens") + g("output_tokens")
    meas = {"spend_unit": spend, "cache_read": g("cache_read_input_tokens"), "requests": len(usage),
            "input": g("input_tokens"), "cache_creation": g("cache_creation_input_tokens"), "output": g("output_tokens")}
    if models != {M}:
        raise SystemExit("REFUSED: transcript models are %s, not %s only" % (sorted(models), M))
    row = {"schema": "m8_attempt_receipt.v1", "record_kind": "completion", "amends_execution_id": exe, "attempt_id": att,
           "book": "Ezek", "lane": "fixround_v9_delta_" + L, "outcome": "COMPLETED", "agent_id": agent,
           "model_ordered": M, "model_actual": M,
           "model_actual_tier": "MEASURED (message.model on every request of the runtime transcript)",
           "tokens_notification_unit": notification,
           "tokens_notification_tier": "REPORTED (completion notification, subagent_tokens; the OW-28 ceiling unit)",
           "tokens_spend_unit": spend, "tokens_spend_measure": meas,
           "tokens_spend_tier": "MEASURED (usage fields per unique message id, census v4 method; cache reads not added)",
           "tool_uses": tool_uses, "duration_ms": duration_ms, "interruptions": [],
           "durable_dir": "sp_durable/Ezek/merged_close/delta_v9/delta_" + L, "outputs": outputs,
           "lane_reported": {"model": dc.get("model"), "corpus_sha256": dc.get("corpus_sha256"),
                             "assembly_verdict": dc.get("assembly_verdict"), "verdict": dc.get("verdict"),
                             "output_sha256_matches_message": dc.get("output_sha256") == outputs["final_message.md"],
                             "tool_calls_used": dc.get("tool_calls_used")},
           "lane_reported_tier": "EXTRACTED from the lane's delta_check.json; judged by the close gates, not here",
           "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    shas = append(before, row)
    print(json.dumps({"lane": L, "outputs": outputs, "measure": meas, "notification": notification,
                      "ratio_spend_over_notification": round(spend / notification, 3) if notification else None,
                      "lane_reported": row["lane_reported"], "receipts_sha256": shas}, indent=1))


def manifest():
    guard("Ezek/merged_close/delta_v9/landing_manifest.v1.json")
    _, rows = receipts()
    man = {"schema": "ezek_delta_v9_landing.v1", "book": "Ezek",
           "note": "durable paths are relative to this manifest's directory; written by "
                   "repair2/fixround_v9/land_delta_v9.py --manifest", "lanes": {}}
    for L in ("a", "b"):
        att = "ezek_fixround_v9_delta_lane_%s_a1" % L
        done = [r for r in rows if r.get("amends_execution_id") == att + "#e1" and r.get("record_kind") == "completion"]
        if len(done) != 1:
            raise SystemExit("REFUSED: lane %s has %d completion rows, not one" % (L, len(done)))
        files = {}
        for fn in FILES:
            b = (DV / ("delta_" + L) / fn).read_bytes()
            if sha(b) != done[0]["outputs"][fn]:
                raise SystemExit("REFUSED: durable %s of lane %s no longer matches its receipt" % (fn, L))
            files[fn] = {"durable": "delta_%s/%s" % (L, fn), "sha256": sha(b)}
        man["lanes"][L.upper()] = {"attempt_id": att, "completion_recorded_at": done[0]["recorded_at"], "files": files}
    b = (json.dumps(man, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    p = DV / "landing_manifest.v1.json"
    if p.exists():
        if p.read_bytes() != b:
            raise SystemExit("REFUSED: the landing manifest exists with different bytes")
    else:
        tmp = p.with_suffix(".tmp")
        tmp.write_bytes(b)
        os.replace(tmp, p)
    print(json.dumps({"manifest": str(p.relative_to(EZ)).replace("\\", "/"), "sha256": sha(p.read_bytes())}))


ap = argparse.ArgumentParser()
ap.add_argument("--lane", choices=("a", "b"))
ap.add_argument("--notification", type=int)
ap.add_argument("--tool-uses", type=int)
ap.add_argument("--duration-ms", type=int)
ap.add_argument("--manifest", action="store_true")
a = ap.parse_args()
if a.manifest:
    manifest()
elif a.lane and None not in (a.notification, a.tool_uses, a.duration_ms):
    land(a.lane, a.notification, a.tool_uses, a.duration_ms)
else:
    raise SystemExit("usage: --lane a|b --notification N --tool-uses N --duration-ms N | --manifest")
