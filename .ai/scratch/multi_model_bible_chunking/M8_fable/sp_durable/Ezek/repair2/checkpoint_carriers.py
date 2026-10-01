#!/usr/bin/env python3
"""DURABILITY CHECKPOINT at a phase transition (ledger E-37's cure): cursor -> index -> prompt -> checker.

WHY THIS TOOL. The resume carriers went stale for many phases because they were written only at a clear, and the
work ran through compactions. The cure recorded in E-37 is a CURSOR at every phase transition with the carriers
re-bound and the safe-to-clear check run each time. Doing that by hand at every step is how it was skipped; this
tool does all four in order and REFUSES to leave a prompt that fails the checker.

ORDER, and why. (1) append the CYCLE_STATE entry ending in the new CURSOR - the index builder reads the latest
cursor, so it must exist first; (2) regenerate CURRENT_STATE.v1.json FROM DISK with the stated next job; (3) archive
the prompt byte-for-byte, then re-bind exactly four things in it - the STATE-BINDING line (taken from the checker's
own --binding, never typed), the index hash inside the VERIFIED CURRENT STATE pointer, the cursor line, and one
marked work-state bullet; (4) run the checker and its selftest. On FAIL the previous prompt bytes are restored and
the tool exits 1; the cursor and index stay written, because they are true, and the refusal says so.

The caller runs SP/campaign/_inflight_pin_guard.py on CYCLE_STATE, CURRENT_STATE.v1.json and the prompt first.

usage: python checkpoint_carriers.py --spec <spec.json>
  spec = {"cursor": "<phase_token>", "entry_md": "<markdown for CYCLE_STATE, WITHOUT the cursor line>",
          "next_job": "<text after 'NEXT AUTHORIZED JOB: '>", "work_state_bullet": "<text after '- WORK STATE NOW: '>"}
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
SP = M8 / "sp_durable"
IDX = M8 / "CURRENT_STATE.v1.json"
PROMPT = M8 / "RESUME_PROMPT_CURRENT.md"
BUILDER = SP / "Jer" / "_build_current_state.py"
CHK = SP / "Jer" / "_safe_to_clear_check.py"
ENV = dict(os.environ, PYTHONUTF8="1")
MARK = "- WORK STATE NOW: "
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731


def run(args, cwd):
    return subprocess.run([sys.executable, "-B"] + args, cwd=str(cwd), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=ENV)


def live_cs():
    """AMENDED 2026-09-23 (Ezekiel's close): the log is the LIVE book's, resolved from marathon_progress.yaml
    current_book exactly as the checker resolves it. The pinned Ezekiel path went stale the moment the close moved
    current_book to Dan, and the checker then fell back to the closed Jeremiah log. There is no fallback here: a
    live book without a log is a refusal, and the cure is to open that book's log."""
    m = re.search(r"^current_book:\s*(\S+)\s*$", (M8 / "marathon_progress.yaml").read_text(encoding="utf-8"), re.M)
    p = SP / m.group(1) / "freeze" / "CYCLE_STATE.md" if m else None
    if p is None or not p.is_file():
        raise SystemExit("REFUSED: the live book's CYCLE_STATE is missing (%s); open that book's log first" % p)
    return p


CS = live_cs()


def main():
    spec = json.loads(Path(sys.argv[sys.argv.index("--spec") + 1]).read_text(encoding="utf-8"))
    cursor = spec["cursor"]
    if not re.fullmatch(r"[A-Za-z0-9_]+", cursor):
        raise SystemExit("REFUSED: a cursor is one token of letters, digits and underscores")
    # (1) CYCLE_STATE - IDEMPOTENT: a rerun after a checker refusal must not append a second entry for the same cursor
    last = re.findall(r"CURSOR: phase = ([A-Za-z0-9_]+)", CS.read_text(encoding="utf-8", errors="replace"))
    if last and last[-1] == cursor:
        print("cursor %s is already the latest in CYCLE_STATE - entry not appended again" % cursor)
    else:
        with CS.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write("\n" + spec["entry_md"].rstrip() + "\n- CURSOR: phase = %s.\n" % cursor)
    # (2) index from disk
    b = run([str(BUILDER), "--next", spec["next_job"], "--cycle-state", str(CS)], BUILDER.parent)
    idx = json.loads(IDX.read_text(encoding="utf-8"))
    if b.returncode != 0 or idx.get("phase") != cursor:
        raise SystemExit("REFUSED at the index: builder exit %s, index phase %r, cursor %r. stderr: %s"
                         % (b.returncode, idx.get("phase"), cursor, b.stderr[-400:]))
    # (3) archive and re-bind the prompt
    before = PROMPT.read_bytes()
    arch = M8 / "receipts" / "prompt_archive" / ("RESUME_PROMPT_%s_%s.md" % (
        datetime.now(timezone.utc).strftime("%Y-%m-%d"), hashlib.sha256(before).hexdigest()[:8]))
    if not arch.exists():
        arch.write_bytes(before)
    binding = run([str(CHK), "--binding"], CHK.parent).stdout.strip().splitlines()[-1]
    if not binding.startswith("STATE-BINDING: phase=%s;" % cursor):
        raise SystemExit("REFUSED: the checker's binding does not carry the new cursor: %r" % binding)
    lines = before.decode("utf-8").split("\n")

    def one(pred, what):
        hits = [i for i, l in enumerate(lines) if pred(l)]
        if len(hits) != 1:
            raise SystemExit("REFUSED: expected exactly one %s in the prompt, found %d" % (what, len(hits)))
        return hits[0]

    lines[one(lambda l: l.startswith("STATE-BINDING:"), "binding line")] = binding
    i = one(lambda l: "VERIFIED CURRENT STATE: CURRENT_STATE.v1.json (sha256 " in l, "index pointer")
    lines[i] = re.sub(r"(VERIFIED CURRENT STATE: CURRENT_STATE\.v1\.json \(sha256 )[0-9a-f]{8}",
                      lambda m: m.group(1) + sha(IDX)[:8], lines[i], count=1)
    c = one(lambda l: l.startswith("cursor: phase = "), "cursor line")
    lines[c] = "cursor: phase = %s. NEXT AUTHORIZED JOB: %s" % (cursor, spec["next_job"])
    ws = [k for k, l in enumerate(lines) if l.startswith(MARK)]
    bullet = MARK + spec["work_state_bullet"]
    if len(ws) > 1:
        raise SystemExit("REFUSED: more than one work-state bullet in the prompt")
    if ws:
        lines[ws[0]] = bullet
    else:
        lines.insert(c + 1, bullet)
    text = "\n".join(lines)
    # ANCHORED SUBSTRING REPLACEMENTS for stale statements elsewhere in the prompt: each "old" must occur EXACTLY
    # once, or nothing is written. The checker still decides; a FAIL restores the previous prompt bytes.
    for r in spec.get("replace_substrings", []):
        n = text.count(r["old"])
        if n != 1:
            raise SystemExit("REFUSED: replacement anchor found %d times (must be 1): %r" % (n, r["old"][:80]))
        text = text.replace(r["old"], r["new"])
    PROMPT.write_text(text, encoding="utf-8", newline="\n")
    # (4) checker
    chk = run([str(CHK), str(PROMPT)], CHK.parent).stdout.strip().splitlines()
    st = run([str(CHK), "--selftest"], CHK.parent).stdout.strip().splitlines()
    ok = bool(chk) and chk[0].startswith("SAFE_TO_CLEAR_CHECK: PASS") and bool(st) and st[-1].startswith("SELFTEST: PASS")
    if not ok:
        PROMPT.write_bytes(before)
        print("\n".join(chk[-12:]))
        raise SystemExit("REFUSED: the re-bound prompt failed the checker; the previous prompt bytes are RESTORED. "
                         "The cursor and index stay written because they are true - the prompt is now stale and the "
                         "checker will say so until it is fixed.")
    print(json.dumps({"cursor": cursor, "index_sha256": sha(IDX), "prompt_sha256": sha(PROMPT),
                      "prompt_archived_as": arch.name, "check": chk[0][:60], "selftest": st[-1]}, indent=1))


if __name__ == "__main__":
    main()
