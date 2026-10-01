#!/usr/bin/env python3
"""Fix-round item (4): write the 14 attempt receipts that were never recorded, from the packets themselves.

WHAT THE STAGE-2 CHECKER FOUND: seven receipt files cover the writer, primary, peer, boss, author, order-execution
and final-check lanes. Fourteen attempts have none - the whole spot wave, both cure attempts, the fix attempt, both
postchecks, all three sidecar attempts and the third boss attempt. The permanent safeguard requires a per-attempt
record of model, effort, producer/catcher, evidence paths and hashes. The checker could not confirm the receipts were
truly absent rather than at an unnamed path, because the exact-path law bars it from searching. I searched: they are
absent. All fourteen.

PROVENANCE IS THE POINT HERE. These receipts are written AFTER the fact, so every field must say where it came from:
  - model and effort: the ORDERED values from the launch messages, marked ORDERED NOT VERIFIED as always
  - digits: counted from the delivered packet at write time, never recalled
  - the packet digest: computed now, over the file as it stands
  - written_late: true, with the reason, on every one of them
A receipt written late and labelled as if it were contemporaneous would be worse than no receipt, because it would
claim a discipline that was not kept. Each of these says plainly that it was reconstructed.

What CANNOT be reconstructed is stated as unknown rather than guessed: token counts, tool-use counts and durations
lived in runtime notifications that are gone, and 13 of these 14 attempts left no transcript.
Usage: _write_missing_receipts.py [--apply]"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTE = ("RECONSTRUCTED AFTER THE FACT during the OW-6 fix round: this attempt ran without a receipt being written at "
        "the time, which the stage-2 final checker found. Digits here are counted from the delivered packet at "
        "write time; the model is READ from the launch record the transcript manifest was built from, never "
        "inferred - an earlier version of this tool inferred it and got five of fourteen wrong. Runtime facts that were only "
        "in task notifications (tokens, tool uses, duration) are gone and are recorded as unknown, not estimated.")

# (attempt_id, lane, agent, packet path, ordered model, output file for the lane receipts)
SPEC = [
    ("lam_spot_S1_a1", "lam_spot_wave", "S1", "spot/spot_S1.json", "claude-opus-5", "spot/lam_spot_attempt_receipts.jsonl"),
    ("lam_spot_S2_a1", "lam_spot_wave", "S2", "spot/spot_S2.json", "claude-opus-5", "spot/lam_spot_attempt_receipts.jsonl"),
    ("lam_spot_S3_a1", "lam_spot_wave", "S3", "spot/spot_S3.json", "claude-opus-5", "spot/lam_spot_attempt_receipts.jsonl"),
    ("lam_spot_S4_a1", "lam_spot_wave", "S4", "spot/spot_S4.json", "claude-opus-5", "spot/lam_spot_attempt_receipts.jsonl"),
    ("lam_spot_S5_a1", "lam_spot_wave", "S5", "spot/spot_S5.json", "claude-opus-5", "spot/lam_spot_attempt_receipts.jsonl"),
    ("lam_micro_m01_a1", "lam_micro_round", "m01", "spot/micro_01.jsonl", "claude-sonnet-5", "spot/lam_micro_attempt_receipts.jsonl"),
    ("lam_micro_m02_a1", "lam_micro_round", "m02", "spot/micro_02.jsonl", "claude-sonnet-5", "spot/lam_micro_attempt_receipts.jsonl"),
    ("lam_fix_f01_a1", "lam_fix_round", "f01", "spot/fix_01.jsonl", "claude-sonnet-5", "spot/lam_fix_attempt_receipts.jsonl"),
    ("lam_postcheck_01_a1", "lam_postcheck", "pc01", "postcheck/postcheck_01.json", "claude-opus-5", "postcheck/lam_postcheck_attempt_receipts.jsonl"),
    ("lam_postcheck_02_a1", "lam_postcheck", "pc02", "postcheck/postcheck_02.json", "claude-opus-5", "postcheck/lam_postcheck_attempt_receipts.jsonl"),
    ("lam_sidecar_1_a1", "lam_finalize_sidecars", "sc1", "sidecar_src_1.jsonl", "claude-sonnet-5", "postcheck/lam_sidecar_attempt_receipts.jsonl"),
    ("lam_sidecar_2_a1", "lam_finalize_sidecars", "sc2", "sidecar_src_2.jsonl", "claude-sonnet-5", "postcheck/lam_sidecar_attempt_receipts.jsonl"),
    ("lam_sidecar_corr_a1", "lam_finalize_sidecars", "sccorr", "sidecar_corr.jsonl", "claude-sonnet-5", "postcheck/lam_sidecar_attempt_receipts.jsonl"),
    ("lam_boss_b3_a1", "lam_boss_round", "b3", "reviews/boss_lam_b3.json", "claude-opus-5", "reviews/lam_boss_attempt_receipts.jsonl"),
]

CATCHERS = {
    "lam_spot_wave": "the cure round that executed its findings, the postchecks that re-verified the cured rows, and "
                     "the stage-1 transcript audit + stage-2 final checker (claude-fable-5-1)",
    "lam_micro_round": "_apply_micro.py guarded apply + postcheck_01 (a different model), which returned not_fit and "
                       "ordered the fix round",
    "lam_fix_round": "_apply_micro.py guarded apply (parametrised globs) + postcheck_02 (a different model), "
                     "verdict fit_to_assemble",
    "lam_postcheck": "the OW-6 stage-2 final checker (claude-fable-5-1), which re-verified its residuals against the "
                     "corpus bytes",
    "lam_finalize_sidecars": "the sidecar validator + the OW-6 stage-2 final checker",
    "lam_boss_round": "the author wave that executed its rulings + the OW-6 stage-2 final checker",
}


def digits_for(p):
    """Count what the packet actually contains. Shapes differ per lane, so count what is there and say what."""
    if p.suffix == ".jsonl":
        rows = [json.loads(l) for l in p.read_text(encoding="utf-8-sig").splitlines() if l.strip()]
        return {"object_counted": "delivered rows", "rows": len(rows)}
    d = json.load(open(p, encoding="utf-8-sig"))
    out = {}
    for k in ("verdict", "status"):
        if d.get(k) is not None:
            out[k] = d[k]
    for k, label in (("findings", "findings"), ("items", "items"), ("residual", "residual"),
                     ("rows_checked", "rows_checked"), ("verified", "verified"), ("blocking", "blocking")):
        v = d.get(k)
        if isinstance(v, list):
            out[label] = len(v)
        elif isinstance(v, int):
            out[label] = v
    if isinstance(d.get("findings"), list):
        for sev in ("high", "medium", "low"):
            out[f"severity_{sev}"] = sum(1 for f in d["findings"] if f.get("severity") == sev)
    out["object_counted"] = "packet fields present; absent fields are omitted rather than reported as zero"
    return out


def main():
    apply = "--apply" in sys.argv
    now = datetime.now(timezone.utc).isoformat()
    man = json.load(open(HERE / "transcript_manifest.v2.json", encoding="utf-8"))
    launch_models = {e["attempt_id"]: e.get("model") for e in man["mapped_transcripts"]}
    per_file, missing_pkt, made = {}, [], []

    for aid, lane, agent, rel, model, outrel in SPEC:
        p = HERE / rel
        if not p.is_file():
            missing_pkt.append({"attempt_id": aid, "packet": rel})
            continue
        b = p.read_bytes()
        # 2026-09-07: the model is READ FROM the launch record here. It used to come from the SPEC table above,
        # which was a hand-written guess, while the field claimed a launch record as its source - a fabricated
        # provenance citation, and five of fourteen were wrong. A receipt that cites a source is generated FROM it.
        real = launch_models.get(aid)
        assert real, f"no launch record entry for {aid}; a receipt may not assert a model that nothing records"
        rec = {"schema": "m8_attempt_receipt.v1", "lane": lane, "agent": agent, "attempt_id": aid,
               "corrects": None, "model": real,
               "model_source": f"transcript_manifest.v2.json (built from the launch map) - READ, not inferred",
               "effort": "ORDERED, NOT VERIFIED - no runtime effective-effort evidence was retained for this attempt",
               "producer": f"{lane} attempt {agent}",
               "catcher": CATCHERS[lane],
               "role_separation": "no agent checked its own work; the catcher named above is a different attempt "
                                  "and, where stated, a different model",
               "output_file": rel, "output_sha256": hashlib.sha256(b).hexdigest(), "output_bytes": len(b),
               "digits": digits_for(p),
               "transcript": "none retained for this attempt (see transcript_manifest.v2.json)"
                             if aid != "lam_boss_b3_a1" else
                             "no transcript retained; the manifest records the attempt with a zero-byte file",
               "tokens_reported": None, "tool_uses": None, "duration_ms": None,
               "runtime_facts_note": "unknown - these lived only in runtime task notifications, which are gone. "
                                     "Recorded as unknown rather than estimated.",
               "written_late": True, "written_late_note": NOTE,
               "raised_by": "the OW-6 stage-2 final checker (claude-fable-5-1), attempt lam_final_check_01_a1, "
                            "residual 'attempt receipts for 14 attempts'",
               "kill_events": [], "recorded_at": now}
        per_file.setdefault(outrel, []).append(rec)
        made.append(aid)

    sys.stdout.reconfigure(encoding="utf-8")
    if not apply:
        print(json.dumps({"dry_run": True, "would_write": {k: len(v) for k, v in per_file.items()},
                          "attempts": made, "packets_missing": missing_pkt}, indent=1))
        return 0

    written = {}
    for rel, recs in per_file.items():
        p = HERE / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        existing = set()
        if p.is_file():
            for l in p.read_text(encoding="utf-8").splitlines():
                if l.strip():
                    existing.add(json.loads(l).get("attempt_id"))
        add = [r for r in recs if r["attempt_id"] not in existing]
        with open(p, "a", encoding="utf-8", newline="\n") as f:
            for r in add:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        written[rel] = {"appended": len(add), "already_present": len(recs) - len(add),
                        "sha16": hashlib.sha256(p.read_bytes()).hexdigest()[:16]}

    print(json.dumps({"status": "WRITTEN", "files": written, "attempts_recorded": len(made),
                      "packets_missing": missing_pkt}, indent=1))
    return 1 if missing_pkt else 0


if __name__ == "__main__":
    sys.exit(main())
