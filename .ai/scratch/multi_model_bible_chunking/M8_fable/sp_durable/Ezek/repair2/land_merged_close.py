#!/usr/bin/env python3
"""Land one OW-26 merged-close lane, or write the landing manifest once both have landed.

--lane A|B  reads the lane's launch receipt (record_kind "launch") for its output_dir, requires the six outputs, parses the
            five JSON ones, refuses a lane_meta that names another attempt, runs the in-flight pin guard on every path
            it will write, copies the six outputs write-new into Ezek/merged_close/lane_{a,b}/, and appends ONE
            completion row that AMENDS the launch row (amends_execution_id, attempt_id, record_kind "completion", no
            execution_id key: finding_pin_guard_blind_to_launch_receipts). The receipts file is replaced atomically under
            an exclusive lock with its expected-before digest pinned.
            --total-tokens, --tool-uses and --duration-ms come from the harness completion notification (REPORTED).
--manifest  writes Ezek/merged_close/landing_manifest.v1.json (write-new) from the two landed lanes' durable files.
--dry       prints what would be written and writes nothing.
--interruption TEXT (repeatable) records a stop-and-resume of the same execution in the completion row. A resumed
            execution keeps its launch row and gets no row of its own until it lands: any row amending it would read to
            the pin guard as a landing and release its pins while it still runs.
--token-note TEXT   states what the reported figure covers when that is not the whole run (e.g. after a resume).

The lanes' verdicts are NOT judged here. _close_book.py gates them; landing records what each lane returned.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent.parent
SP = EZ.parent
RECEIPTS = EZ / "ezek_merged_close_attempt_receipts.jsonl"
DEST = EZ / "merged_close"
MANIFEST = DEST / "landing_manifest.v1.json"
LANES = {"A": "ezek_merged_close_lane_a_a1", "B": "ezek_merged_close_lane_b_a1"}
FILES = ("postcheck.json", "final_check.json", "items_20_23.json", "named_questions.json", "lane_meta.json",
         "final_message.md")
GUARD = SP / "campaign" / "_inflight_pin_guard.py"
MODEL = "claude-opus-5-5"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rows():
    return [json.loads(l) for l in RECEIPTS.read_text(encoding="utf-8").splitlines() if l.strip()]


def guard(targets):
    args = [sys.executable, "-B", str(GUARD), "--book", "Ezek"]
    for t in targets:
        args += ["--target", str(t)]
    p = subprocess.run(args, cwd=str(SP), capture_output=True, text=True, encoding="utf-8",
                       env={**os.environ, "PYTHONUTF8": "1"})
    out = json.loads(p.stdout)
    if p.returncode != 0 or out["verdict"] != "CLEAR":
        raise SystemExit("REFUSED by pin guard: %s" % json.dumps({k: v["pinned_by"] for k, v in out["targets"].items()
                                                                  if v["verdict"] != "CLEAR"}))
    return out["in_flight"]


def write_new(p, b, dry):
    if p.exists():
        if p.read_bytes() == b:
            return "SAME"
        raise SystemExit("REFUSED: %s exists with different bytes" % p)
    if not dry:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b)
    return "NEW"


def append_row(row, dry):
    before = RECEIPTS.read_bytes()
    line = (json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8")
    after = before + (b"" if before.endswith(b"\n") or not before else b"\n") + line
    if dry:
        return sha(before), sha(after)
    lock = RECEIPTS.with_suffix(".jsonl.lock")
    fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        if sha(RECEIPTS.read_bytes()) != sha(before):
            raise SystemExit("REFUSED: receipts changed under the lock")
        tmp = RECEIPTS.with_suffix(".jsonl.tmp")
        tmp.write_bytes(after)
        os.replace(tmp, RECEIPTS)
        if sha(RECEIPTS.read_bytes()) != sha(after):
            RECEIPTS.write_bytes(before)
            raise SystemExit("ROLLED BACK: post-write digest mismatch")
    finally:
        os.close(fd)
        lock.unlink()
    return sha(before), sha(after)


def land(L, tokens, tool_uses, duration_ms, dry, interruptions=(), token_note=None):
    att = LANES[L]
    recs = rows()
    launch = [r for r in recs if r.get("attempt_id") == att and r.get("record_kind") == "launch"]
    if len(launch) != 1:
        raise SystemExit("REFUSED: %d launch rows for %s" % (len(launch), att))
    launch = launch[0]
    if any(r.get("attempt_id") == att and r.get("record_kind") == "completion" for r in recs):
        raise SystemExit("REFUSED: %s already has a completion row" % att)
    src = Path(launch["output_dir"])
    missing = [f for f in FILES if not (src / f).is_file()]
    if missing:
        raise SystemExit("REFUSED: lane %s output missing %s" % (L, missing))
    raw = {f: (src / f).read_bytes() for f in FILES}
    parsed = {f: json.loads(raw[f].decode("utf-8")) for f in FILES if f.endswith(".json")}
    meta = parsed["lane_meta.json"]
    if meta.get("attempt_id") not in (att, launch["execution_id"]):   # a lane may write the attempt or the execution id
        raise SystemExit("REFUSED: lane_meta names %r, launch row is %s" % (meta.get("attempt_id"), att))
    dest = DEST / ("lane_" + L.lower())
    in_flight = guard([dest / f for f in FILES] + [RECEIPTS])
    status = {f: write_new(dest / f, raw[f], dry) for f in FILES}
    pc, fc, it = parsed["postcheck.json"], parsed["final_check.json"], parsed["items_20_23.json"]
    row = {
        "schema": launch["schema"], "record_kind": "completion", "amends_execution_id": launch["execution_id"],
        "attempt_id": att, "book": "Ezek", "lane": launch.get("lane"), "outcome": "COMPLETED",
        "model_ordered": launch.get("model"), "model_actual": meta.get("model"),
        "model_actual_tier": "REPORTED (the lane's own lane_meta.json; the completion notification names no model)",
        "tokens_reported": tokens, "tool_uses": tool_uses, "duration_ms": duration_ms,
        "tokens_tier": "REPORTED (harness completion notification usage block, field subagent_tokens)",
        "token_note": token_note, "interruptions": list(interruptions),
        "durable_dir": "sp_durable/Ezek/merged_close/lane_%s" % L.lower(),
        "outputs": {f: sha(raw[f]) for f in FILES},
        "verdicts_as_returned": {"postcheck": pc.get("verdict"), "final_check": fc.get("verdict"),
                                 "final_check_corpus_sha256": fc.get("corpus_sha256"),
                                 "items_20_23_fit": {i: (it.get("item_%d" % i) or {}).get("fit_to_accept")
                                                     for i in range(20, 24)}},
        "e19_selfreport": meta.get("e19_selfreport"),
        "grader_fallback": {"model": MODEL, "replaces": "claude-fable-5-1", "carrier": "campaign/grader_models.v1.json"},
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "recorded_by": "orchestrator (claude-opus-5-5), session 910cbe15; transcript NOT read",
    }
    before, after = append_row(row, dry)
    print(json.dumps({"lane": L, "dry": dry, "in_flight_at_landing": in_flight, "files": status,
                      "receipts_sha256": {"before": before, "after": after}, "row": row}, ensure_ascii=False, indent=1))


def manifest(dry):
    recs = rows()
    man = {"schema": "ezek_merged_close_landing.v1", "written_at": datetime.now(timezone.utc).isoformat(), "lanes": {}}
    for L, att in LANES.items():
        done = [r for r in recs if r.get("attempt_id") == att and r.get("record_kind") == "completion"]
        if len(done) != 1:
            raise SystemExit("REFUSED: lane %s has %d completion rows" % (L, len(done)))
        files = {}
        for f in FILES:
            p = DEST / ("lane_" + L.lower()) / f
            d = sha(p.read_bytes())
            if d != done[0]["outputs"][f]:
                raise SystemExit("REFUSED: %s differs from its completion row" % p)
            files[f] = {"durable": "lane_%s/%s" % (L.lower(), f), "sha256": d}
        man["lanes"][L] = {"attempt_id": att, "files": files}
    guard([MANIFEST])
    b = (json.dumps(man, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    print(json.dumps({"manifest": str(MANIFEST.relative_to(SP)), "status": write_new(MANIFEST, b, dry),
                      "sha256": sha(b), "dry": dry}, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", choices=sorted(LANES))
    ap.add_argument("--total-tokens", type=int)
    ap.add_argument("--tool-uses", type=int)
    ap.add_argument("--duration-ms", type=int)
    ap.add_argument("--manifest", action="store_true")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--interruption", action="append", default=[])
    ap.add_argument("--token-note")
    a = ap.parse_args()
    if a.manifest == bool(a.lane):
        raise SystemExit("usage: --lane A|B --total-tokens N --tool-uses N --duration-ms N [--dry] | --manifest [--dry]")
    if a.lane:
        if None in (a.total_tokens, a.tool_uses, a.duration_ms):
            raise SystemExit("--lane needs --total-tokens, --tool-uses and --duration-ms from the notification")
        land(a.lane, a.total_tokens, a.tool_uses, a.duration_ms, a.dry, a.interruption, a.token_note)
    else:
        manifest(a.dry)


if __name__ == "__main__":
    main()
