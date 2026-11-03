#!/usr/bin/env python3
"""Build the 1 Corinthians S1 spot-review brief and launch message from BRIEF_S1.template.md, pins MEASURED from disk.

Ported 2026-10-20 from the Daniel S1 builder (scratch build_s1_dan.py, playbook v3 section 2: writer wave -> S1). The
pins are the writer wave's pins (imported from ../writer_lanes/build_writer_launch.py, so both waves pin one tool set)
plus the installed combined draft and its combine report; ngram7 becomes RUN for this lane. The book-wide suite result
and the confidence spread are copied from the installed combine report (MEASURED there), never typed. The message, the
digest helpers, the stop reasons and the efficiency worker block come from ../phase0_lanes/build_launch.py. A relaunch
(--execution N > 1) gets a fresh OUT, cor_s1_e<N>, and needs exactly one landing row for #e(N-1) whose outcome opens
with a stop reason. The script refuses to overwrite a brief or message that exists and differs (E-41, E-44), refuses a
brief that names another book (E-65) or carries a writer's lane path, refuses when the pin guard is not CLEAR, then runs
_brief_pin_check.py and _launch_message_check.py --book 1Cor and prints their verdicts and the digests.

usage: build_review_launch.py --lane S1 [--execution N] [--dry-run]
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
BK = HERE.parent
SP = BK.parent
sys.path.insert(0, str(BK / "writer_lanes"))
sys.path.insert(0, str(BK / "phase0_lanes"))
from build_launch import MESSAGE, write_once, sha, LEDGER, STOPS, lands, M8, worker_block  # noqa: E402
from build_writer_launch import PINS as WRITER_PINS, OTHER_BOOK  # noqa: E402

REC = HERE / "1cor_review_attempt_receipts.jsonl"
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\af84b702-d913-4495-8e57-252cf7894c63\scratchpad")
LANES = {"S1": {"attempt": "cor_writer_wave_spot_review_s1_a1", "out": "cor_s1",
                "deliverable": "1cor_writer_wave_spot_review_S1.json", "template": "BRIEF_S1.template.md",
                "work": "reviewing candidate reading-unit rows against the book strategy and the witnesses' bytes"}}
COMBINED = [
    ("1Cor/writer/draft_rows_combined.jsonl", "READ; copy to work\\ before running anything on it",
     "THE ROWS UNDER REVIEW: all six parts, renumbered book-wide"),
    ("1Cor/writer/draft_rows_combined.report.json", "READ",
     "the orchestrator's combine report: inputs, tiling, book-wide suite, joins, confidence spread; a claim to test, "
     "not a finding"),
]
RUN_HERE = {"1Cor/tools/ngram7.py": ("RUN on a private copy in OUT\\work only (it writes nothing)", "the 7-gram check")}


def red_members(per_check):
    """Names of suite members that are not GREEN. The suite stores each member as a plain status string ("GREEN",
    "RED", ...) or, for the Greek dry run, a counts string "ok=N fixed=N defects=N". A dict-only filter once dropped
    "ngram7: RED" silently in a dry run (2026-10-20), so an unrecognised form refuses instead of being skipped."""
    red = []
    for k, v in sorted(per_check.items()):
        st = str(v.get("status", "")) if isinstance(v, dict) else str(v)
        if st.upper() in ("GREEN", "PASS", "OK"):
            continue
        if st.startswith("ok=") and " defects=" in st:
            if not st.endswith(" defects=0"):
                red.append(k)
            continue
        if st.upper() in ("RED", "FLAGS", "ERROR", "DEAD"):
            red.append(k)
            continue
        raise SystemExit("REFUSED: suite member %s has an unrecognised status %r" % (k, st[:60]))
    return red


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True, choices=sorted(LANES))
    ap.add_argument("--execution", type=int, default=1)
    ap.add_argument("--dry-run", action="store_true", help="write the rendered brief to SCR/dry_review/ only")
    args = ap.parse_args()
    L, N = LANES[args.lane], args.execution
    if N < 1:
        raise SystemExit("REFUSED: --execution must be >= 1")
    tag = "" if N == 1 else "_e%d" % N
    out = SCR / (L["out"] + tag)
    attempt = L["attempt"]
    plan = json.loads((BK / "strategy_plan_1Cor.json").read_text(encoding="utf-8"))
    rep = json.loads((BK / "writer" / "draft_rows_combined.report.json").read_text(encoding="utf-8"))
    rows_n = sum(1 for x in (BK / "writer" / "draft_rows_combined.jsonl").read_text(encoding="utf-8").splitlines()
                 if x.strip())
    if rows_n != rep["rows"]:
        raise SystemExit("REFUSED: installed draft has %d rows, the combine report says %d" % (rows_n, rep["rows"]))
    s = rep["book_wide_suite"]
    bookwide = ("whole-book tiling %s (%s of %s verses); suite hard_status %s, triage_flags %s, dead_members %s"
                % (rep["whole_book_tiling"]["status"], rep["whole_book_tiling"]["verses_covered"],
                   rep["whole_book_tiling"]["verses_expected"], s.get("hard_status"), s.get("triage_flags"),
                   s.get("dead_members")))
    red = red_members(s.get("per_check") or {})
    if red:
        bookwide += "; members not GREEN: %s" % ", ".join(red)
    conf = ", ".join("%s %d" % kv for kv in sorted(rep["confidence_spread"].items()))
    pins = COMBINED + [(r, *RUN_HERE[r]) if r in RUN_HERE else (r, u, w) for r, u, w in WRITER_PINS]
    rows = ["| input | sha256 |", "|---|---|"]
    uses = ["", "How you may use each input:", ""]
    for rel, use, what in pins:
        p = (SP / rel).resolve()
        win = "SP\\" + rel.replace("/", "\\")
        rows.append("| `%s` | `%s` |" % (win, sha(p.read_bytes())))
        uses.append("- `%s`: %s. %s." % (win, use, what[0].upper() + what[1:]))
    eff = worker_block(M8)
    tpl = (HERE / L["template"]).read_text(encoding="utf-8")
    fill = {"{{SP}}": str(SP), "{{OUT}}": str(out), "{{PINS}}": "\n".join(rows + uses), "{{ATTEMPT}}": attempt,
            "{{EXECUTION}}": attempt + "#e1", "{{DELIVERABLE}}": L["deliverable"], "{{ROWS_N}}": str(rows_n),
            "{{N_PARENTS}}": str(len(plan["parents"])), "{{N_SCR}}": str(len(plan["scrutiny_targets"])),
            "{{N_DEV}}": str(len(plan["device_review_items"])), "{{BOOKWIDE}}": bookwide, "{{CONF}}": conf,
            "{{EFFICIENCY}}": eff + "EFFICIENCY-OUT: %s\n" % out}
    body = tpl
    for k, v in fill.items():
        body = body.replace(k, v)
    if "{{" in body:
        raise SystemExit("REFUSED: an unfilled placeholder remains")
    if OTHER_BOOK.search(body):
        raise SystemExit("REFUSED: the brief names another book, %r (E-65)" % OTHER_BOOK.search(body).group(0))
    if "cor_w\\lane_" in body or "cor_w/lane_" in body:
        raise SystemExit("REFUSED: the brief carries a writer's lane path (blindness)")
    e1 = "execution `%s#e1`." % attempt
    if body.count(e1) != 1 or body.count("#e1") != 1:
        raise SystemExit("REFUSED: the brief must name %s#e1 exactly once" % attempt)
    if N > 1:
        prev = "%s#e%d" % (attempt, N - 1)
        recs = [json.loads(x) for x in REC.read_text(encoding="utf-8").splitlines() if x.strip()]
        land = [r for r in recs if lands(r) and prev in (r.get("execution_id"), r.get("amends_execution_id"))]
        why = [v for k, v in STOPS.items() if len(land) == 1 and str(land[0].get("outcome") or "").startswith(k + " ")]
        if len(why) != 1:
            raise SystemExit("REFUSED: %s needs exactly one landing row whose outcome opens with one of: %s"
                             % (prev, ", ".join(STOPS)))
        body = body.replace(e1, "execution `%s#e%d`. This is a relaunch: execution #e%d was %s and landed no "
                                "deliverable, so OUT starts empty and nothing of #e%d's is yours to use."
                            % (attempt, N, N - 1, why[0], N - 1))
    brief = HERE / ("BRIEF_%s%s.md" % (args.lane, tag))
    if args.dry_run:
        dry = SCR / "dry_review" / brief.name
        dry.parent.mkdir(parents=True, exist_ok=True)
        dry.write_bytes(body.encode("utf-8"))
        print(json.dumps({"dry_run": str(dry), "sha256": sha(body.encode("utf-8")), "pins": len(pins),
                          "bookwide": bookwide, "conf": conf}, ensure_ascii=False, indent=1))
        return 0
    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    run = lambda *a: subprocess.run([sys.executable, "-B", *a], cwd=str(SP), capture_output=True, text=True,  # noqa: E731
                                    encoding="utf-8", env=env)
    g = run("campaign/_inflight_pin_guard.py", "--book", "1Cor", "--target", "1Cor/review/" + brief.name)
    if json.loads(g.stdout).get("verdict") != "CLEAR":
        raise SystemExit("REFUSED: the pin guard is not CLEAR on %s" % brief.name)
    write_once(brief, body.encode("utf-8"))
    bsha = sha(brief.read_bytes())
    msg = MESSAGE.format(ledger=str(LEDGER), brief=str(brief), sha=bsha, work=L["work"], efficiency=eff, out=str(out))
    mfile = out.parent / "cor_review_msgs" / ("launch_message_%s%s.txt" % (args.lane, tag))
    mfile.parent.mkdir(parents=True, exist_ok=True)
    write_once(mfile, msg.encode("utf-8"))
    (out / "work").mkdir(parents=True, exist_ok=True)
    pc = run("campaign/_brief_pin_check.py", "--brief", str(brief))
    lm = run("campaign/_launch_message_check.py", "--book", "1Cor", "--message", str(mfile))
    print(json.dumps({"lane": args.lane, "attempt": attempt, "execution": N, "brief": brief.name,
                      "brief_sha256": bsha, "pins": len(pins), "message": str(mfile),
                      "message_sha256": sha(mfile.read_bytes()),
                      "brief_pin_check": json.loads(pc.stdout)["verdict"],
                      "launch_message_check": json.loads(lm.stdout)["verdict"],
                      "launch_message_gaps": json.loads(lm.stdout)["gaps"]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
