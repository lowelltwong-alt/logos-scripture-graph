#!/usr/bin/env python3
"""RECONCILE the landed stage-1 transcript-audit packets against the slice plan and the manifest they were built from.

WHY THIS EXISTS: the OW-6 close gate asserted that each auditor's coverage_statement was PRESENT. It never asserted
that the statement was TRUE. That is exactly how 18 orchestrator shell outputs reached four auditors' slices on
2026-09-07 while every mechanical check passed - the digits looked complete because nothing compared them to
anything. A coverage claim that nothing can contradict is not evidence, it is decoration.

This compares, per slice and then across the whole stage:
  - the packet's transcripts_assigned / bytes_assigned against the slice plan the launch message was built from
  - the set of transcripts the packet actually reports on against the set the slice assigned (missing AND extra)
  - bytes_processed against bytes_assigned (a mechanical pass that claims 100% must account for 100%)
  - bytes_read_closely <= bytes_processed (you cannot read closely more than you processed)
  - the union of all slices against the manifest's transcript set, and disjointness between slices
  - that every file named is a real subagent transcript by the same content test the manifest uses

Exit 1 on any mismatch. Digits are the tool's COUNTS, never a packet's self-report.
Usage: _final_check_reconcile.py [--plan ../../_lam_final_check_stage1_launch_msgs.json]
                                 [--manifest transcript_manifest.v2.json] [--out final_check/_reconcile.json]"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SC = HERE.parent.parent
A = sys.argv[1:]
def arg(k, d): return A[A.index(k) + 1] if k in A else d
PLAN = Path(arg("--plan", str(SC / "_lam_final_check_stage1_launch_msgs.json")))
MAN = HERE / arg("--manifest", "transcript_manifest.v2.json")
OUT = HERE / arg("--out", "final_check/_reconcile.json")


def is_subagent_transcript(p):
    """Same content test the manifest uses: one line, must be a JSON object with agentId/isSidechain."""
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            o = json.loads(f.readline(65536))
        return isinstance(o, dict) and ("agentId" in o or "isSidechain" in o)
    except Exception:
        return False


def slice_paths(msg):
    """The exact transcript paths a launch message assigned. Parsed from the message the agent actually received,
    not from a parallel structure, so the check tests what was really ordered."""
    out = []
    for line in msg.split("\n"):
        line = line.strip()
        if line.startswith("- C:") and ".output" in line:
            out.append(line[2:line.index(".output") + 7])
    return out


def main():
    plan = json.load(open(PLAN, encoding="utf-8"))
    man = json.load(open(MAN, encoding="utf-8"))
    man_set = {Path(e["transcript"]).name
               for e in man["mapped_transcripts"] + man["unmapped_transcripts"] if e["bytes"] > 0}

    problems, per_slice, seen = [], [], {}
    for aid, spec in sorted(plan.items()):
        assigned = slice_paths(spec["message"])
        assigned_names = [Path(p).name for p in assigned]
        row = {"attempt_id": aid, "assigned": len(assigned_names), "packet": None}

        for n in assigned_names:
            if n in seen:
                problems.append(f"{aid}: {n} is also assigned to {seen[n]} - slices must be disjoint")
            seen[n] = aid
        for p in assigned:
            if not Path(p).is_file():
                problems.append(f"{aid}: assigned path does not exist: {p}")
            elif not is_subagent_transcript(Path(p)):
                problems.append(f"{aid}: assigned file is NOT a subagent transcript: {Path(p).name}")

        pkt_path = Path(spec["output"])
        if not pkt_path.is_file():
            problems.append(f"{aid}: stage-1 packet ABSENT at {pkt_path}")
            per_slice.append(row); continue
        try:
            pkt = json.load(open(pkt_path, encoding="utf-8-sig"))
        except Exception as e:
            problems.append(f"{aid}: packet unparsable: {e!r}")
            per_slice.append(row); continue

        row["packet"] = pkt_path.name
        ta, ba = pkt.get("transcripts_assigned"), pkt.get("bytes_assigned")
        bp, bc = pkt.get("bytes_processed"), pkt.get("bytes_read_closely")
        if ta != len(assigned_names):
            problems.append(f"{aid}: packet says transcripts_assigned={ta}, the slice assigned {len(assigned_names)}")
        if ba != spec["bytes"]:
            problems.append(f"{aid}: packet says bytes_assigned={ba}, the slice assigned {spec['bytes']}")

        reported = {Path(t.get("transcript", "")).name for t in pkt.get("per_transcript", [])}
        missing = sorted(set(assigned_names) - reported)
        extra = sorted(reported - set(assigned_names))
        if missing:
            problems.append(f"{aid}: packet reports on none of these assigned transcripts: {missing}")
        if extra:
            problems.append(f"{aid}: packet reports on transcripts it was NOT assigned: {extra}")

        if isinstance(bp, int) and isinstance(ba, int) and bp < ba:
            problems.append(f"{aid}: bytes_processed={bp:,} < bytes_assigned={ba:,}; the mechanical pass is "
                            f"contracted to cover 100% of the slice")
        if isinstance(bc, int) and isinstance(bp, int) and bc > bp:
            problems.append(f"{aid}: bytes_read_closely={bc:,} > bytes_processed={bp:,}, which is not possible")
        if not (pkt.get("coverage_statement") or "").strip():
            problems.append(f"{aid}: coverage_statement is empty")
        if pkt.get("model") != "claude-fable-5-1":
            problems.append(f"{aid}: packet model is {pkt.get('model')!r}, expected claude-fable-5-1")

        row.update({"reported": len(reported), "bytes_assigned": ba, "bytes_processed": bp,
                    "bytes_read_closely": bc,
                    "findings": sum(len(t.get("findings", [])) for t in pkt.get("per_transcript", []))})
        per_slice.append(row)

    union = set(seen)
    if union != man_set:
        for n in sorted(man_set - union):
            problems.append(f"manifest transcript assigned to NO slice: {n}")
        for n in sorted(union - man_set):
            problems.append(f"slice names a transcript absent from the manifest: {n}")

    res = {"schema": "m8_final_check_reconcile.v1", "plan": str(PLAN), "manifest": str(MAN),
           "manifest_transcripts": len(man_set), "slices": len(plan), "assigned_total": len(union),
           "per_slice": per_slice, "problems": problems,
           "verdict": "GREEN" if not problems else "RED",
           "law": "digits here are this tool's counts; a packet's self-reported coverage is compared against them, "
                  "never trusted in place of them"}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "per_slice"}, indent=1))
    for r in per_slice:
        print(f"  {r['attempt_id']}: assigned {r['assigned']}, reported {r.get('reported')}, "
              f"processed {r.get('bytes_processed')}, close {r.get('bytes_read_closely')}, "
              f"findings {r.get('findings')}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
