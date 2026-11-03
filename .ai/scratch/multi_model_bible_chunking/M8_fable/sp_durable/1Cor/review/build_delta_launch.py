#!/usr/bin/env python3
"""Build a delta-check brief and launch message from BRIEF_DELTA.template.md and a lane spec (TE-1, TE-4: data, not a new generator).

Ported 2026-11-01 from build_s5_launch.py. The gate text is read from the spec's rulings file, the pins are MEASURED from
disk, and only the delta's inputs are pinned. It refuses a brief that names another book (E-65) or does not name the
execution exactly once, refuses when the pin guard is not CLEAR, then runs _brief_pin_check.py and
_launch_message_check.py --book 1Cor.

A spec with a `task` key builds a close-kit lane from BRIEF_CLOSE.template.md instead.

usage: build_delta_launch.py --spec lane_spec_S6.json [--dry-run]
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
from build_launch import MESSAGE, write_once, sha, LEDGER, M8, worker_block  # noqa: E402
from build_writer_launch import OTHER_BOOK  # noqa: E402

SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\af84b702-d913-4495-8e57-252cf7894c63\scratchpad")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--dry-run", action="store_true", help="write the rendered brief to SCR/dry_review/ only")
    args = ap.parse_args()
    s = json.loads((HERE / args.spec).read_text(encoding="utf-8"))
    lane, attempt = s["lane"], s["attempt"]
    out = SCR / s["out_dir"]
    cond = []
    if "rulings" in s:
        rul = json.loads((SP / s["rulings"]).read_text(encoding="utf-8"))
        cond = rul["gate"]["s2_conditions"]
        if rul["gate"].get("primaries_may_launch") is not False:
            raise SystemExit("REFUSED: gate.primaries_may_launch is not false")
    rows = ["| input | sha256 |", "|---|---|"]
    uses = ["", "How you may use each input:", ""]
    for rel, use, what in s["pins"]:
        win = "SP\\" + rel.replace("/", "\\")
        rows.append("| `%s` | `%s` |" % (win, sha((SP / rel).read_bytes())))
        uses.append("- `%s`: %s. %s." % (win, use, what[0].upper() + what[1:]))
    if len({p[0] for p in s["pins"]}) != len(s["pins"]):
        raise SystemExit("REFUSED: a pin is listed twice")
    if s.get("unpinned_note"):
        uses += ["", s["unpinned_note"]]
    eff = worker_block(M8)
    fill = {"{{LANE}}": lane, "{{SP}}": str(SP), "{{OUT}}": str(out),
            "{{PINS}}": "\n".join(rows + uses), "{{ATTEMPT}}": attempt, "{{EXECUTION}}": attempt + "#e1",
            "{{DELIVERABLE}}": s["deliverable"], "{{GATE}}": "\n".join(cond), "{{EFFICIENCY}}": eff + "EFFICIENCY-OUT: %s\n" % out}
    if "task" in s:  # a close-kit lane: BRIEF_CLOSE.template.md, its task and its key list from the lane table
        keys = json.loads((BK / "close" / "close_lanes.v1.json").read_text(encoding="utf-8"))["lanes"][lane]["keys"]
        task = (SP / s["task"]).read_text(encoding="utf-8").rstrip("\n")
        for k, v in s.get("task_fill", {}).items():  # a campaign/close_kit task is book-agnostic; the spec names the book
            task = task.replace("{{%s}}" % k, v)
        fill.update({"{{TITLE}}": s["title"], "{{TASK}}": task,
                     "{{BUDGET}}": s["budget"], "{{KEYS}}": ", ".join("`%s`" % k for k in keys)})
    else:
        fill.update({"{{ROUND}}": s["round"], "{{CONTROLLING}}": s["controlling"], "{{APPLIED_NAME}}": Path(s["applied"]).name})
    body = (HERE / s.get("template", "BRIEF_DELTA.template.md")).read_text(encoding="utf-8")
    for k, v in fill.items():
        body = body.replace(k, v)
    if "{{" in body:
        raise SystemExit("REFUSED: an unfilled placeholder remains")
    if OTHER_BOOK.search(body) and not s.get("other_book_ok"):  # a port lane names its templates; the spec states why
        raise SystemExit("REFUSED: the brief names another book, %r (E-65)" % OTHER_BOOK.search(body).group(0))
    if body.count("execution `%s#e1`." % attempt) != 1 or body.count("#e1") != 1:
        raise SystemExit("REFUSED: the brief must name %s#e1 exactly once" % attempt)
    brief = HERE / ("BRIEF_%s.md" % lane)
    if args.dry_run:
        dry = SCR / "dry_review" / brief.name
        dry.parent.mkdir(parents=True, exist_ok=True)
        dry.write_bytes(body.encode("utf-8"))
        print(json.dumps({"dry_run": str(dry), "bytes": len(body.encode("utf-8")), "pins": len(s["pins"]), "conditions": len(cond)}, indent=1))
        return 0
    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    run = lambda *a: subprocess.run([sys.executable, "-B", *a], cwd=str(SP), capture_output=True, text=True,  # noqa: E731
                                    encoding="utf-8", env=env)
    g = run("campaign/_inflight_pin_guard.py", "--book", "1Cor", "--target", "1Cor/review/" + brief.name)
    if json.loads(g.stdout).get("verdict") != "CLEAR":
        raise SystemExit("REFUSED: the pin guard is not CLEAR on %s" % brief.name)
    write_once(brief, body.encode("utf-8"))
    bsha = sha(brief.read_bytes())
    msg = MESSAGE.format(ledger=str(LEDGER), brief=str(brief), sha=bsha, work=s["work"], efficiency=eff, out=str(out))
    mfile = SCR / "cor_review_msgs" / ("launch_message_%s.txt" % lane)
    mfile.parent.mkdir(parents=True, exist_ok=True)
    write_once(mfile, msg.encode("utf-8"))
    (out / "work").mkdir(parents=True, exist_ok=True)
    pc = run("campaign/_brief_pin_check.py", "--brief", str(brief))
    lm = run("campaign/_launch_message_check.py", "--book", "1Cor", "--message", str(mfile))
    print(json.dumps({"lane": lane, "attempt": attempt, "brief": brief.name, "brief_bytes": brief.stat().st_size, "brief_sha256": bsha,
                      "pins": len(s["pins"]), "message": str(mfile), "message_sha256": sha(mfile.read_bytes()),
                      "brief_pin_check": json.loads(pc.stdout)["verdict"], "launch_message_check": json.loads(lm.stdout)["verdict"],
                      "launch_message_gaps": json.loads(lm.stdout)["gaps"]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
