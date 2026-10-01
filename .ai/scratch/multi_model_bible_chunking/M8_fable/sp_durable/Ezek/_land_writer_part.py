#!/usr/bin/env python3
"""Process ONE landed Ezekiel writer part, identically every time.

    validate -> persist (never over a landed part) -> receipt under the execution id -> evidence note -> index

WHY A SCRIPT. Eleven parts land one at a time over hours. Doing the sequence by hand eleven times is how a receipt
gets a stale digest, a draft gets persisted before it is validated, or a finished part gets silently overwritten by
a re-launch. This makes the sequence one command and makes its refusals explicit.

E-14 LADDER, ENFORCED HERE:
  - a part already DURABLE with DIFFERENT bytes is REFUSED - a landed part is validated, never replaced. A genuine
    re-run must come in under the next execution id and is persisted beside, not over, the earlier run.
  - a part already durable with IDENTICAL bytes is a no-op (idempotent re-landing).
  - a receipt already present for this execution id is not appended twice.

A RED DRAFT IS NEVER DISCARDED. It is persisted to writer/red/ under its execution id, with the validator report,
so the evidence survives and the part can be cured or re-run; it is simply not promoted to writer/draft_pNN.jsonl.

LAYER C IS SELF-AUTHORED. The evidence note is built from the writer's own OW-8 final message, saved by the
orchestrator to a JSON file and passed with --record. It is labelled self-authored and is never presented as chain
of thought.

Usage:
  _land_writer_part.py --part p02 --source <draft.jsonl> --record <ow8.json> --tokens N [--tool-uses N]
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SP = Path(__file__).resolve().parent
WRITER = SP / "writer"
RED = WRITER / "red"
NOTES = SP / "evidence_notes"
RECEIPTS = WRITER / "ezek_writer_attempt_receipts.jsonl"
CAMPAIGN = SP.parent / "campaign"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--record", required=True)
    ap.add_argument("--tokens", type=int, required=True)
    ap.add_argument("--tool-uses", type=int, default=None)
    ap.add_argument("--execution", default="e1", help="execution ordinal tag, e.g. e1 or e2")
    a = ap.parse_args()

    part = a.part
    aid = "ezek_writer_%s_a1" % part
    ordinal = int(a.execution.lstrip("e"))
    xid = "%s#e%d" % (aid, ordinal)
    src = Path(a.source)
    out = {"part": part, "execution_id": xid, "actions": [], "refusals": []}

    if not src.is_file() or src.stat().st_size == 0:
        out["verdict"] = "REFUSED"
        out["refusals"].append("source draft is absent or empty - nothing landed to process")
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 1
    rec = json.loads(Path(a.record).read_text(encoding="utf-8"))
    if rec.get("execution_id") and rec["execution_id"] != xid:
        out["verdict"] = "REFUSED"
        out["refusals"].append("the OW-8 record names execution %s, not %s - refusing to attach one run's record "
                               "to another" % (rec["execution_id"], xid))
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 1

    # ---- validate BEFORE anything is persisted ----
    v = subprocess.run([sys.executable, str(SP / "_validate_writer_part.py"), str(src), "--part", part],
                       capture_output=True, text=True, encoding="utf-8")
    val = json.loads(v.stdout)
    out["validator"] = {k: val[k] for k in ("verdict", "rows", "tiling", "confidence_spread")}
    out["validator"]["problems"] = val["problems"][:20]

    src_sha = sha(src)
    WRITER.mkdir(exist_ok=True)
    final = WRITER / ("draft_%s.jsonl" % part)

    if val["verdict"] != "GREEN":
        RED.mkdir(exist_ok=True)
        red = RED / ("draft_%s.e%d.jsonl" % (part, ordinal))
        shutil.copyfile(src, red)
        (RED / ("draft_%s.e%d.validator.json" % (part, ordinal))).write_text(
            json.dumps(val, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        assert sha(red) == src_sha
        out["actions"].append("RED draft preserved at writer/red/%s with its validator report; NOT promoted" % red.name)
        status, persisted = "LANDED_RED", "writer/red/" + red.name
    else:
        if final.is_file():
            if sha(final) == src_sha:
                out["actions"].append("already durable with identical bytes - no-op")
            else:
                out["verdict"] = "REFUSED"
                out["refusals"].append(
                    "writer/%s is already durable with DIFFERENT bytes. E-14: a landed part is validated, never "
                    "replaced. Land a genuine re-run under the next execution id instead." % final.name)
                print(json.dumps(out, ensure_ascii=False, indent=1))
                return 1
        else:
            shutil.copyfile(src, final)
            assert sha(final) == src_sha, "persist parity failure"
            out["actions"].append("persisted to writer/%s, parity verified" % final.name)
        status, persisted = "LANDED", "writer/" + final.name

    # ---- receipt, idempotent per execution id ----
    existing = set()
    if RECEIPTS.is_file():
        for line in RECEIPTS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                existing.add(json.loads(line).get("execution_id"))
    if xid in existing:
        out["actions"].append("receipt for %s already present - not appended twice" % xid)
    else:
        e19 = rec.get("e19_selfreport") or rec.get("e19_selfreported") or "NOT REPORTED by the agent"
        receipt = {
            "schema": "m8_attempt_receipt.v1", "lane": "ezek_writer_wave", "book": "Ezek", "wave": "main",
            "attempt_id": aid, "execution_id": xid, "execution_of": aid, "execution_ordinal": ordinal,
            "previous_execution_id": ("%s#e%d" % (aid, ordinal - 1)) if ordinal > 1 else None, "retry_of": None,
            "agent": part, "parent_agent_id": "orchestrator",
            "model": "claude-sonnet-5",
            "model_actual": "UNAVAILABLE - the runtime exposed no effective-model record; never inferred",
            "effort": "ORDERED default, NOT VERIFIED",
            "producer": "writer %s" % part,
            "catcher": "SP/Ezek/_validate_writer_part.py (deterministic; proves form, not judgment), then the peer "
                       "and boss rounds",
            "role_separation": "the validator is not the writer; semantic judgment is reserved for review rounds",
            "outcome": status, "recorded_at": datetime.now(timezone.utc).isoformat(),
            "validator_verdict": val["verdict"], "rows_landed": val["rows"], "tiling": val["tiling"],
            "confidence_spread": val["confidence_spread"],
            "tokens_reported": a.tokens, "tool_uses": a.tool_uses,
            "output_file": persisted, "output_sha256": src_sha,
            "findings_from_agent_record": [c.get("what") for c in rec.get("outcome", {}).get("changed", [])],
            "verification_from_agent_record": rec.get("verification", []),
            "unresolved_uncertainty": rec.get("unresolved_uncertainty", []),
            "e19_selfreported": e19,
            "e19_breach_disclosed": ("listing" in e19.lower() and "no listing" not in e19.lower())
                                    or "ls " in e19.lower() or "partial compliance" in e19.lower(),
        }
        with RECEIPTS.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(receipt, ensure_ascii=False) + "\n")
        out["actions"].append("receipt appended for %s" % xid)

    # ---- layer C evidence note ----
    NOTES.mkdir(exist_ok=True)
    note = {
        "attempt_id": aid, "execution_id": xid,
        "sources": rec.get("sources", []),
        "outcome": rec.get("outcome", {}),
        "verification": rec.get("verification", []),
        "unresolved_uncertainty": rec.get("unresolved_uncertainty", []),
        "self_authored": True,
        "limit": "accountable work summary; not chain of thought and not independent proof. Built verbatim from "
                 "the writer's own OW-8 final message.",
    }
    # An existing note is NEVER overwritten. A note belongs to one execution, and an idempotent re-landing - or a
    # re-landing handed a thinner OW-8 record - must not silently replace a richer layer-C record with a poorer
    # one. The first draft of this handler always rewrote it; the flaw was caught while designing its test, before
    # any real landing ran through it. A genuine new run lands under the next execution id and so gets its own note.
    note_p = NOTES / (xid.replace("#", "%23") + ".json")
    if note_p.is_file():
        out["actions"].append("evidence note for %s already present - kept, never overwritten" % xid)
    else:
        note_p.write_text(json.dumps(note, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        out["actions"].append("evidence note written")

    # ---- capture index ----
    ci = subprocess.run([sys.executable, str(CAMPAIGN / "_capture_index.py"), "--book", "Ezek", "--write"],
                        capture_output=True, text=True, encoding="utf-8")
    chk = subprocess.run([sys.executable, str(CAMPAIGN / "_capture_index.py"), "--check"],
                         capture_output=True, text=True, encoding="utf-8")
    out["capture_index"] = json.loads(chk.stdout)["verdict"]

    out["verdict"] = status
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if status == "LANDED" else 2


if __name__ == "__main__":
    sys.exit(main())
