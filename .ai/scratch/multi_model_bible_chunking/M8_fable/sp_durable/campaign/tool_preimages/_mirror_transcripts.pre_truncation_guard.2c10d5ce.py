#!/usr/bin/env python3
"""Durable copy of the subagent REASONING TRANSCRIPTS (owner directive OW-6c evidence preservation).

The transcripts the runtime writes live in the SESSION scratch tree, which does not survive the session; the
end-of-campaign re-check the owner reserved needs them to still exist. This copies each non-empty transcript to
sp_durable/transcripts/<session-id>/ and verifies every destination by sha256 after the copy (fail closed, never
deletes, never overwrites a byte-identical file). The orchestrator does NOT read transcript content - only sizes and
digests - so its own context is never flooded.

Size discipline: the run prints the bytes added and the running total of the durable transcript store, so growth over
the remaining books stays visible and can be ruled on rather than discovered late.
Usage: _mirror_transcripts.py [--dry-run]"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

SC = Path(__file__).resolve().parent
SESSION = SC.parent
TASKS = SESSION / "tasks"
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
DST = M8 / "sp_durable" / "transcripts" / SESSION.name



def is_subagent_transcript(p):
    """A subagent transcript is JSONL whose first line is a JSON object with agentId/isSidechain.

    The runtime writes captured ORCHESTRATOR shell output into the same directory under the same
    "<id>.output" name, so a bare glob cannot tell the two apart. Content decides, not the filename:
    the id prefixes happen to differ today but that is an undocumented convention to not depend on.
    Reads ONE line, so this never pulls transcript content into the caller's context."""
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            first = f.readline(65536)
        o = json.loads(first)
        return isinstance(o, dict) and ("agentId" in o or "isSidechain" in o)
    except Exception:
        return False

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    dry = "--dry-run" in sys.argv
    man_p = SC / "SP" / "campaign" / "transcript_manifest.v1.json"
    man = json.load(open(man_p, encoding="utf-8")) if man_p.is_file() else {"mapped_transcripts": [], "unmapped_transcripts": []}
    known = {Path(e["transcript"]).name: e for e in man.get("mapped_transcripts", [])}
    copied, unchanged, failures, added = 0, 0, [], 0
    skipped_not_transcript = 0
    if not dry:
        DST.mkdir(parents=True, exist_ok=True)
    for src in sorted(TASKS.glob("*.output")):
        if src.stat().st_size == 0:
            continue
        # the same directory holds captured ORCHESTRATOR shell output; mirroring it would pad the durable
        # transcript store with files that are not subagent evidence at all
        if not is_subagent_transcript(src):
            skipped_not_transcript += 1
            continue
        s = sha(src)
        dst = DST / src.name
        if dst.is_file() and sha(dst) == s:
            unchanged += 1
            continue
        if dry:
            copied += 1; added += src.stat().st_size; continue
        shutil.copyfile(src, dst)
        if sha(dst) != s:
            failures.append(str(dst))
        else:
            copied += 1; added += src.stat().st_size
    total = sum(p.stat().st_size for p in DST.glob("*.output")) if DST.is_dir() else 0
    idx = {"schema": "m8_transcript_store_index.v1", "session": SESSION.name, "destination": str(DST),
           "files": (sorted(p.name for p in DST.glob("*.output")) if DST.is_dir() else []),
           "attempt_ids_mapped": {k: v["attempt_id"] for k, v in known.items()},
           "store_bytes": total, "note": "verbatim runtime transcripts (reasoning + tool calls) retained for the OW-6 final checker and the OW-6c end-of-campaign re-check"}
    if not dry and not failures:
        (DST / "_index.json").write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")
    out = {"status": "TRANSCRIPTS_MIRRORED" if not failures else "MIRROR_FAILED", "copied": copied, "unchanged": unchanged,
           "bytes_added": added, "skipped_not_transcript": skipped_not_transcript, "store_bytes_total": total, "store_mb": round(total / 1048576, 1), "failures": failures, "dry_run": dry,
           "growth_note": "one book's cycle produced this much; 41 books remain - if the store's growth becomes a decision, it is an OW-6 escalation for the controlling agent, not a silent deletion"}
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(out, indent=1))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
