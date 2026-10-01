#!/usr/bin/env python3
"""Answer the exact-path existence checks the stage-1 auditors were forbidden to run themselves.

The E-19 exact-path law bars an agent from running any existence check or listing against a shared SP directory.
That ban is right - it is what stops an auditor browsing another lane's work - but it has a consequence: when an
auditor finds, in a transcript, that some agent WROTE a stray file into a shared directory, it can prove the write
happened and cannot say whether the file is still there. Slice 1's auditor said exactly that and handed the check
back: "the final checker or the orchestrator should check those two exact paths."

An unanswered handback is a finding that quietly expires. This tool answers each one at the named exact path and
records the answer as evidence the stage-2 checker can weigh, clearly attributed to the orchestrator rather than to
an agent, because the orchestrator is the only party permitted to look.

Paths are listed explicitly below, not discovered by scanning: a tool that went looking for stray files would be
doing the very thing the law forbids, and would also find files nobody alleged.
Usage: _answer_auditor_path_checks.py"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "final_check" / "_orchestrator_path_checks.v1.json"

# each entry: the exact path an auditor named, and which finding asked for it
REQUESTS = [
    {"path": "tools/out_bat_edom.txt", "asked_by": "lam_tscript_01_a1",
     "about_attempt": "lam_cwo_04_a1", "finding_class": "law_breach",
     "allegation": "sweep.py output redirected into the shared SP\\Lam\\tools directory (925-byte encoding traceback)"},
    {"path": "tools/out_bat_tsiyon.txt", "asked_by": "lam_tscript_01_a1",
     "about_attempt": "lam_cwo_04_a1", "finding_class": "law_breach",
     "allegation": "second sweep.py output redirected into the same shared directory"},
    {"path": "tools/collate_err.tmp", "asked_by": "lam_tscript_01_a1 (named in its transcript_shows)",
     "about_attempt": "another agent (observed in a directory listing, author not identified)",
     "finding_class": "law_breach", "allegation": "0-byte stray observed in the shared tools directory"},
    {"path": "tools/collate_out.tmp", "asked_by": "lam_tscript_01_a1 (named in its transcript_shows)",
     "about_attempt": "another agent (observed in a directory listing, author not identified)",
     "finding_class": "law_breach", "allegation": "2989-byte stray observed in the shared tools directory"},
    {"path": "../Jer/tools/quote1.txt", "asked_by": "lam_tscript_03_a1",
     "about_attempt": "jer_cwo_10_a1", "finding_class": "law_breach",
     "allegation": "unassigned scratch write into the shared SP\\Jer\\tools directory"},
]


def main():
    answers = []
    for r in REQUESTS:
        p = (HERE / r["path"]).resolve()
        exists = p.is_file()
        a = dict(r, resolved_path=str(p), present_now=exists)
        if exists:
            b = p.read_bytes()
            a.update(bytes=len(b), sha256=hashlib.sha256(b).hexdigest(),
                     disposition="STILL PRESENT - the stray survives and must be removed or ruled on")
        else:
            a.update(bytes=None, sha256=None,
                     disposition="ABSENT - the write happened as the transcript shows, and the file was removed "
                                 "before this check; the breach is real, the residue is gone")
        answers.append(a)

    present = [a for a in answers if a["present_now"]]
    rec = {"schema": "m8_orchestrator_path_checks.v1", "checked_at": datetime.now(timezone.utc).isoformat(),
           "why_the_orchestrator_and_not_an_agent": "the E-19 exact-path law bars an agent from running an existence "
                                                    "check against a shared SP directory; the auditors correctly "
                                                    "refused and handed the checks back",
           "method": "each path was named by an auditor and is checked here explicitly; no directory was scanned, "
                     "because scanning for strays would itself be the banned operation and would surface files "
                     "nobody alleged",
           "requests": len(REQUESTS), "still_present": len(present), "absent": len(answers) - len(present),
           "answers": answers,
           "note_for_stage2": "ABSENT does not make the finding false. The transcript evidence that the write "
                              "occurred stands on its own, and the breach is what the finding is about; the check "
                              "only settles whether residue remains. Weigh the breach, not just the residue.",
           "authority": "orchestrator evidence; candidate-only, non-authorizing"}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"written": str(OUT), "requests": len(REQUESTS), "still_present": len(present),
                      "absent": len(answers) - len(present),
                      "present_paths": [a["path"] for a in present]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
