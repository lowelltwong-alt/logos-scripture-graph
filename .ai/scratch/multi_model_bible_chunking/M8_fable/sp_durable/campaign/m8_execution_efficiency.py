"""Small M8 continuation helpers. No model calls, acceptance, or implicit writes.

The orchestrator supplies exact paths; reviewers use only their authorized OUT.
Delta evidence is additive. It never substitutes for the legacy final deliverable.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import uuid

CONTRACT = "OWNER_EXECUTION_EFFICIENCY_2026-10-06.md"
WORKER = "sp_durable/campaign/REVIEWER_CONTINUATION_CONTRACT.v1.md"
MARKER = "M8-EFFICIENCY-V1"
SCHEMA = "m8_review_delta.v1"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def parse(raw):
    def unique(pairs):
        out = {}
        for k, v in pairs:
            if k in out:
                raise ValueError("duplicate JSON key")
            out[k] = v
        return out
    return json.loads(raw, object_pairs_hook=unique)


def contract_binding(m8):
    m8 = Path(m8)
    progress = m8 / "marathon_progress.yaml"
    pins = {"marathon_progress.yaml": sha(progress)}
    current = re.search(r"^current_book:\s*(\S+)\s*$", progress.read_text(encoding="utf-8"), re.M)
    if current and current.group(1) == "Dan":
        receipt = "sp_durable/Dan/review/dan_review_attempt_receipts.jsonl"
        pins[receipt] = sha(m8 / receipt)
        records = [parse(line) for line in (m8 / receipt).read_bytes().splitlines() if line.strip()]
        latest = next((r["applied_rows"] for r in reversed(records) if isinstance(r.get("applied_rows"), dict)), None)
        if latest:
            p = (m8 / latest["path"]).resolve()
            if not p.is_relative_to(m8.resolve()) or sha(p) != latest["sha256"]:
                raise ValueError("installed rows identity mismatch")
            pins[latest["path"]] = latest["sha256"]
    return {"path": CONTRACT, "sha256": sha(m8 / CONTRACT),
            "worker_path": WORKER, "worker_sha256": sha(m8 / WORKER), "evidence": pins}


def resume_block(m8):
    b = contract_binding(m8)
    return ("\nM8-EFFICIENCY-V1 RESUME PREFLIGHT\n"
            f"Read {b['path']} sha256 {b['sha256']} before acting on historical navigation.\n"
            "EFFICIENCY-EVIDENCE: " + json.dumps(b["evidence"], sort_keys=True, separators=(",", ":")) + "\n"
            "Current owner directives govern; OW-28 remains tracked-not-enforced.\n"
            "Reconcile current receipts and actual outputs before replaying any old cursor.\n"
            "Resume the same reviewer's completed units; no transferred reading credit.\n"
            "Run the efficiency preflight and existing safe-to-clear check before claiming restart readiness.\n")


def check_resume(m8, text):
    b = contract_binding(m8)
    return [] if resume_block(m8).strip() in text else ["efficiency resume block absent or stale"]


def worker_block(m8):
    p = Path(m8) / WORKER
    return (f"{MARKER}\nEFFICIENCY-CONTRACT: {p} sha256 {sha(p)}\n"
            "Save each complete bounded review unit and exact next cursor in your authorized OUT; "
            "partial output is not acceptance. Preserve the unchanged legacy final deliverable contract.\n")


def check_launch(m8, text, briefs):
    errors = []
    p = Path(m8) / WORKER
    expected = f"EFFICIENCY-CONTRACT: {p} sha256 {sha(p)}"
    for label, body in [("launch", text)] + [(str(p), Path(p).read_text(encoding="utf-8")) for p in briefs]:
        if MARKER not in body or expected not in body:
            errors.append(label + ": missing or stale reviewer continuation contract")
        match = re.search(r"^EFFICIENCY-OUT: (.+)$", body, re.M)
        if not match or not Path(match.group(1).strip()).is_absolute():
            errors.append(label + ": EFFICIENCY-OUT must name the exact authorized absolute OUT")
    return errors


def load_chain(last, reviewer, inputs, expected_last_sha=None):
    """Read exact predecessor paths in one authorized directory; no glob/listing."""
    last = Path(last)
    if expected_last_sha is not None and sha(last) != expected_last_sha:
        raise ValueError("last delta hash mismatch")
    if not isinstance(inputs, dict) or not inputs or any(not isinstance(v, str) or not re.fullmatch(r"[0-9a-f]{64}", v) for v in inputs.values()):
        raise ValueError("complete dependency identities must be named SHA256 values")
    root = last.parent.resolve()
    chain, seen = [], set()
    current = last
    while current is not None:
        if current.resolve().parent != root or current.name in seen or len(chain) >= 1000:
            raise ValueError("invalid predecessor scope, cycle, or unbounded chain")
        seen.add(current.name)
        d = parse(current.read_bytes())
        if d.get("schema") != SCHEMA or d.get("reviewer_id") != reviewer or d.get("input_identities") != inputs:
            raise ValueError("schema, reviewer, or dependency identity mismatch")
        if d.get("accepted") is not False or d.get("status") not in {"partial", "interrupted", "quota_blocked", "ready_for_final_check"}:
            raise ValueError("delta cannot grant acceptance")
        if not isinstance(d.get("execution_id"), str) or not d["execution_id"]:
            raise ValueError("physical execution identity required")
        if not isinstance(d.get("completed_units"), list) or not isinstance(d.get("pending_checks"), list):
            raise ValueError("complete units and pending checks required")
        if "next_cursor" not in d:
            raise ValueError("next cursor required")
        chain.append(d)
        prev = d.get("previous")
        if prev is None:
            current = None
        else:
            name = prev["file"]
            if Path(name).name != name or name in {".", ".."}:
                raise ValueError("predecessor must be an exact same-directory filename")
            current = root / name
            if sha(current) != prev["sha256"]:
                raise ValueError("predecessor hash mismatch")
    units = {}
    for d in reversed(chain):
        for unit in d["completed_units"]:
            if not isinstance(unit, dict) or not isinstance(unit.get("id"), str) or not unit["id"] or "evidence" not in unit:
                raise ValueError("complete identified evidence unit required")
            if unit["id"] in units:
                raise ValueError("duplicate completed unit; no silent replacement")
            units[unit["id"]] = unit
    return {"accepted": False, "completed_units": list(units.values()),
            "next_cursor": chain[0]["next_cursor"], "pending_checks": chain[0]["pending_checks"],
            "status": chain[0]["status"], "delta_count": len(chain)}


def save_delta(path, data):
    """Create-only atomic publication; never modifies a predecessor or final file."""
    path = Path(path)
    temp = path.with_name(path.name + ".owned-" + uuid.uuid4().hex + ".tmp")
    raw = (json.dumps(data, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    try:
        with temp.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        # Validate the complete chain before exposing the new record.
        load_chain(temp, data["reviewer_id"], data["input_identities"])
        os.link(temp, path)  # atomic create-only; an existing name fails
        if path.read_bytes() != raw:
            raise ValueError("published delta readback mismatch")
    finally:
        # Only this call's nonce temporary is removed, never campaign evidence.
        try:
            temp.unlink()
        except FileNotFoundError:
            pass
    return {"file": path.name, "sha256": sha(path), "accepted": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--m8", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--resume-block", action="store_true")
    parser.add_argument("--worker-block", action="store_true")
    parser.add_argument("--check-resume", type=Path)
    parser.add_argument("--resume-delta", type=Path)
    parser.add_argument("--reviewer")
    parser.add_argument("--inputs", type=Path)
    parser.add_argument("--last-sha")
    args = parser.parse_args()
    if args.resume_block:
        print(resume_block(args.m8)); return 0
    if args.worker_block:
        print(worker_block(args.m8)); return 0
    if args.check_resume:
        errors = check_resume(args.m8, args.check_resume.read_text(encoding="utf-8"))
        state = parse((args.m8 / "CURRENT_STATE.v1.json").read_bytes())
        if state.get("execution_efficiency") != contract_binding(args.m8):
            errors.append("current-state efficiency binding absent or stale")
        print(json.dumps({"verdict": "FAIL" if errors else "PASS", "errors": errors,
                          "phase": state.get("phase"), "next": state.get("next_authorized_job"),
                          "limits": "Binding check only; live status must be reconciled against current receipts."}))
        return int(bool(errors))
    if args.resume_delta and args.reviewer and args.inputs and args.last_sha:
        print(json.dumps(load_chain(args.resume_delta, args.reviewer, parse(args.inputs.read_bytes()), args.last_sha), ensure_ascii=False))
        return 0
    parser.error("choose a read-only preflight or exact delta-resume operation")


if __name__ == "__main__":
    raise SystemExit(main())
