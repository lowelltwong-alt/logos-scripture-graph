#!/usr/bin/env python3
"""Fix-round item (2): stop the parity record from overwriting itself, preserve what exists, and disclose what was lost.

THE DEFECT, found by the stage-2 final checker and confirmed on disk: the cycle log pins cwo/cwo_parity.v1.json at
sha256 faa9248e...; the file now hashes to b40e0336... and reconciles rows_v7, not the corpus that was pinned. The
cause is in the tool: _cwo_parity.py writes a FIXED filename on every run, so a later run silently replaced a record
another artifact had already pinned. That is history rewriting by construction, not by anyone's decision.

The original bytes are UNRECOVERABLE. This does not pretend otherwise. It:
  1. moves the surviving record to the version it actually is, named for the corpus it reconciles
  2. leaves a TOMBSTONE at the pinned path recording the lost digest, so a reader following the log's pin finds an
     honest account instead of a different file wearing the same name
  3. patches _cwo_parity.py to refuse to overwrite: it writes the next free version and names the corpus
  4. appends a disclosure to the cycle log

A SECOND, LARGER PROBLEM the same finding exposes and this does NOT fix by itself: the surviving parity record
reconciles rows_v7, while the book's final corpus is rows_v9. Two versions landed after it. The close gate reads the
parity record and asserts GREEN without checking WHICH corpus it covers, so a stale parity record would pass. That
gate hole is closed in _patch_close_gate_parity.py, and parity must be re-run over the final corpus before the close.
Usage: _fix_parity_versioning.py [--apply]"""
import hashlib
import json
import os
import py_compile
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CWO = HERE / "cwo"
PINNED_NAME = "cwo_parity.v1.json"
PINNED_DIGEST = "faa9248ec128beaba55d1a30d73111b0179c44888eee397e83482a9f9e37aedf"
LOG = HERE / "freeze" / "CYCLE_STATE.md"
NL = "\n"


def main():
    apply = "--apply" in sys.argv
    src = CWO / PINNED_NAME
    cur = json.load(open(src, encoding="utf-8-sig"))
    cur_bytes = src.read_bytes()
    cur_digest = hashlib.sha256(cur_bytes).hexdigest()
    corpus = Path(cur.get("post_corpus") or "").name or "unknown"
    stem = corpus.replace(".jsonl", "") or "unknown"
    dest = CWO / f"cwo_parity.{stem}.json"

    plan = {"pinned_path": str(src), "pinned_digest_in_log": PINNED_DIGEST[:16],
            "actual_digest_now": cur_digest[:16],
            "overwrite_confirmed": cur_digest != PINNED_DIGEST,
            "surviving_record_reconciles": corpus,
            "will_move_to": dest.name, "will_leave_tombstone_at": PINNED_NAME,
            "original_bytes": "UNRECOVERABLE - no copy of the pinned version exists",
            "dry_run": not apply}
    sys.stdout.reconfigure(encoding="utf-8")
    if not apply:
        print(json.dumps(plan, indent=2))
        return 0

    assert cur_digest != PINNED_DIGEST, "digest matches the pin; nothing was overwritten - do not run this"
    shutil.copyfile(src, dest)
    assert hashlib.sha256(dest.read_bytes()).hexdigest() == cur_digest, "copy did not verify"

    tomb = {
        "schema": "m8_tombstone.v1",
        "replaces": "the CWO execution-parity record that the cycle log pinned at this exact path",
        "pinned_sha256_in_cycle_log": PINNED_DIGEST,
        "status": "THE PINNED BYTES NO LONGER EXIST",
        "what_happened": "_cwo_parity.py wrote a fixed filename on every run, so a later run over a later corpus "
                         "silently replaced the record this path had already been pinned to. No one decided to "
                         "overwrite it; the tool had no versioning and nothing checked the pin.",
        "found_by": "the OW-6 stage-2 final checker (claude-fable-5-1), attempt lam_final_check_01_a1",
        "the_surviving_record": {"file": dest.name, "sha256": cur_digest, "reconciles_corpus": corpus,
                                 "post_corpus_sha256": cur.get("post_corpus_sha256"), "status": cur.get("status")},
        "recovery": "none possible; the bytes were not mirrored before the overwrite",
        "control_installed": "_cwo_parity.py now refuses to overwrite an existing record and writes the next free "
                             "version named for the corpus it reconciles; the close gate now asserts the parity "
                             "record covers the corpus being closed",
        "law": "a file that still carries the name of a pinned artifact but not its bytes is worse than a missing "
               "file, because a reader following the pin gets a different record and no warning. This tombstone "
               "exists so the pin resolves to an honest account.",
        "written": datetime.now(timezone.utc).isoformat()}
    src.write_text(json.dumps(tomb, ensure_ascii=False, indent=1), encoding="utf-8", newline=NL)

    # ---- patch the tool so it cannot do this again ----
    tp = HERE / "_cwo_parity.py"
    s = tp.read_text(encoding="utf-8")
    old = '(HERE / "cwo" / "cwo_parity.v1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\\n")'
    if old in s:
        new = (
            '# 2026-09-07: this tool used to write a FIXED filename, so a re-run over a later corpus silently replaced\n'
            '# a record the cycle log had already pinned. It now names the record for the corpus it reconciles and\n'
            '# REFUSES to overwrite: an existing file of the same name means a parity record for that corpus already\n'
            '# exists, and replacing it would be exactly the history rewriting that defect produced.\n'
            '_stem = Path(post.get("corpus", "unknown")).name.replace(".jsonl", "") or "unknown"\n'
            '_dst = HERE / "cwo" / f"cwo_parity.{_stem}.json"\n'
            'if _dst.exists() and hashlib.sha256(_dst.read_bytes()).hexdigest() != hashlib.sha256(\n'
            '        json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")).hexdigest():\n'
            '    raise SystemExit(f"REFUSING to overwrite an existing parity record with different content: {_dst.name}. "\n'
            '                     "A parity record for this corpus already exists; re-run parity over the corpus you "\n'
            '                     "actually mean to reconcile, or version it explicitly.")\n'
            '_dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\\n")\n'
            'print(json.dumps({"parity_record": _dst.name, "corpus": post.get("corpus"), "status": out["status"]}, indent=1))')
        s = s.replace(old, new)
        s = s.replace("Writes cwo/cwo_parity.v1.json.", "Writes cwo/cwo_parity.<corpus>.json; never overwrites one.")
        tp.write_text(s, encoding="utf-8", newline=NL)
        py_compile.compile(str(tp), cfile=os.path.join(tempfile.gettempdir(), "cp.pyc"), doraise=True)

    # ---- disclose in the append-only log ----
    entry = [
        "",
        f"## PARITY RECORD OVERWRITE DISCLOSED {datetime.now(timezone.utc).strftime('%Y-%m-%d')} (session dce0b6e2) - fix-round item 2",
        f"- the entry above pins cwo/{PINNED_NAME} at sha256 {PINNED_DIGEST[:16]}...; the file at that path now hashes",
        f"  to {cur_digest[:16]}... and reconciles {corpus}. The pinned bytes are UNRECOVERABLE.",
        "- cause: _cwo_parity.py wrote a fixed filename on every run, so a later run replaced a pinned record. No one",
        "  decided to overwrite it and nothing checked the pin - the tool had no versioning.",
        f"- the surviving record is preserved as cwo/{dest.name} (sha256 {cur_digest[:16]}...); a tombstone now stands",
        f"  at cwo/{PINNED_NAME} recording the lost digest, so following the pin yields an honest account.",
        "- control: _cwo_parity.py now names the record for the corpus it reconciles and REFUSES to overwrite one.",
        "- FOUND BY the OW-6 stage-2 final checker, not by the orchestrator. Recorded as a defect of this cycle.",
        f"- OPEN at the time of writing: the surviving record reconciles {corpus} while the final corpus is rows_v9;",
        "  parity must be re-run over the final corpus and the close gate must assert the record covers it.",
        ""]
    pre_log = LOG.read_bytes()
    body = pre_log if pre_log.endswith(b"\n") else pre_log + b"\n"
    LOG.write_bytes(body + NL.join(entry).encode("utf-8"))
    assert LOG.read_bytes().startswith(body), "log preimage not intact"

    print(json.dumps({"status": "FIXED", "surviving_record": dest.name, "surviving_sha16": cur_digest[:16],
                      "tombstone_at": PINNED_NAME, "tool_patched": old not in tp.read_text(encoding="utf-8"),
                      "log_appended": True, "still_open": f"parity covers {corpus}, final corpus is rows_v9"},
                     indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
