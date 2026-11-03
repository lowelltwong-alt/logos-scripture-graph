#!/usr/bin/env python3
"""Build the 1 Corinthians S5 brief and launch message from BRIEF_S5.template.md, pins MEASURED from disk.

Ported 2026-11-01 from build_s2_launch.py. The gate text, the ruling ids and the counts are read from the installed E4
rulings, the digest classes from the installed S5 receipt extract, the tool-fix pre copies from the receipts, never typed.
The pins are the S5 inputs (the FIXUP-3 applied rows and manifest, the FIXUP-2 applied rows, the four rulings files, the
extract, the coverage report, the licence table, the authors' open items, the sweep, the tool-fix tests with their
references and results, each part's FIXUP-3 brief, landed rows and change record, the E-73 corrections) plus the writer
wave's pins, with ngram7 RUN. It refuses to overwrite a brief or message that exists and differs (E-41, E-44), refuses a
brief that names another book (E-65), carries a lane path or a lane final message, or does not name the execution exactly
once, refuses when the pin guard is not CLEAR, then runs _brief_pin_check.py and _launch_message_check.py --book 1Cor.

usage: build_s5_launch.py [--dry-run]
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
from build_writer_launch import PINS as WRITER_PINS, OTHER_BOOK  # noqa: E402

SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\af84b702-d913-4495-8e57-252cf7894c63\scratchpad")
ATTEMPT = "cor_fixup3_review_s5_a1"
OUT = SCR / "cor_s5_out"
DELIVERABLE = "1cor_fixup3_review_S5.json"
WORK = "reviewing applied reading-unit rows against the rulings, the book strategy and the witnesses' bytes"
RULINGS = BK / "review" / "1cor_controlling_agent_rulings_E4.v1.json"
EXTRACT = BK / "review" / "tool_fixes" / "s5_receipt_extract.v1.json"
APPLIED = BK / "fixup" / "draft_rows_fixup3_applied.jsonl"
PARTS = ("W1", "W2", "W3", "W4", "W5", "W6")
COPY = "READ; copy to work\\ before running anything on it"
S5_PINS = [
    ("1Cor/fixup/draft_rows_fixup3_applied.jsonl", COPY, "THE ROWS UNDER REVIEW: the FIXUP-3 applied rows"),
    ("1Cor/fixup/draft_rows_fixup3_applied.manifest.json", "READ",
     "the apply manifest: source rows, each part's landed rows, the applied rows and the suite on the orchestrator's "
     "scratch copy; a claim to test"),
    ("1Cor/fixup/draft_rows_fixup2_applied.jsonl", COPY, "the rows before FIXUP-3 (the FIXUP-2 applied rows)"),
    ("1Cor/review/1cor_controlling_agent_rulings_E4.v1.json", "READ whole",
     "the E4 rulings: every round-4 ruling with its orders and exact spans, CWO-1COR-06 and -07, the unresolved "
     "uncertainty and GATE-E4"),
    ("1Cor/review/1cor_controlling_agent_rulings_E3.v1.json", "READ", "the E3 rulings: S3-01's W4 spans and CWO-1COR-05"),
    ("1Cor/review/1cor_controlling_agent_rulings_E2.v1.json", "READ", "the E2 rulings: CWO-1COR-04"),
    ("1Cor/review/1cor_controlling_agent_rulings_E1.v1.json", "READ", "the E1 rulings: CWO-1COR-01, -02 and -03"),
    ("1Cor/review/tool_fixes/s5_receipt_extract.v1.json", "READ",
     "whitelisted fields of the review receipts from the round-4 install to the last row (TF-4 and TF-5 installs, the "
     "coverage reports, the gate flip, the FIXUP-3 launches and completions) and the orchestrator's digest classes; a "
     "claim to test"),
    ("1Cor/review/cwo_1cor_post_fixup2_cwo0607_report.v1.json", "READ",
     "the CWO-1COR-05, -06 and -07 coverage report on the rows before FIXUP-3"),
    ("1Cor/review/cwo_1cor_post_fixup3_report.v1.json", "READ",
     "the CWO coverage report on the applied rows with the orchestrator's hand classes; a claim to test"),
    ("1Cor/fixup/fixup3_licence_table.v1.json", "READ",
     "the orchestrator's table of changed fields against orders, with hunks outside named spans; a triage aid and a "
     "claim to test"),
    ("1Cor/fixup/landed3/author_unresolved_for_S5.md", "READ whole",
     "the orchestrator's digest of the six authors' open items; claims to test"),
    ("1Cor/review/cwo_sweep_1cor.py", "RUN on a private copy; --out under OUT\\work only",
     "the CWO sweep (TF-4 and TF-5 installed)"),
    ("1Cor/review/cwo_sweep_1cor.py.pre_bb71fd0bc134", "READ", "the sweep before TF-4"),
    ("1Cor/review/cwo_sweep_1cor.py.pre_23b15aef64e8", "READ; test_cwo0607.py's --pre", "the sweep before TF-5"),
    ("1Cor/review/tools/test_cwo05.py", "RUN with --work under OUT\\work only", "the TF-4 test"),
    ("1Cor/review/tools/cwo05_ref.py", "READ (the test runs it)", "the CWO-1COR-05 reference with its eleven plants"),
    ("1Cor/review/tools/test_cwo0607.py", "RUN with --work under OUT\\work only", "the TF-5 test"),
    ("1Cor/review/tools/cwo06_ref.py", "READ (the test runs it)", "the CWO-1COR-06 and -07 reference"),
    ("1Cor/review/tools/plants06.py", "READ (the test runs it)", "the ten E4 plants"),
    ("1Cor/review/tool_fixes/fixtures_tf4.result.json", "READ", "the recorded TF-4 result"),
    ("1Cor/review/tool_fixes/fixtures_tf5.result.json", "READ", "the recorded TF-5 result"),
    ("1Cor/review/tool_fixes/mk_tf5.py", "READ", "the script that built the TF-5 sections from the reference bytes"),
    ("1Cor/review/tool_fixes/mutants_tf5.py", "RUN with --work and --out under OUT\\work only", "the TF-5 mutants"),
    ("1Cor/review/tool_fixes/mutants_tf5.result.json", "READ", "the recorded mutant result"),
    ("1Cor/fixup/landed3/W3_e1/measure_w3b.py", "READ; copy to work\\ to run it",
     "the count script rows W3-004 and W3-005 name"),
] + [x for p in PARTS for x in (
    ("1Cor/review/FIXUP3_BRIEF_%s.md" % p, "READ", "the orchestrator's FIXUP-3 brief for part %s" % p),
    ("1Cor/fixup/landed3/%s_e1/fixup3_%s_rows.jsonl" % (p, p), "READ", "part %s's landed FIXUP-3 rows" % p),
    ("1Cor/fixup/landed3/%s_e1/fixup3_%s_changes.json" % (p, p), "READ",
     "part %s's change record (author's report; a claim to test)" % p))] + [
    ("campaign/eol_digest_corrections.v1.jsonl", "READ", "the E-73 line-ending digest corrections"),
]
RUN_HERE = {"1Cor/tools/ngram7.py": ("RUN on a private copy in OUT\\work only (it writes nothing)", "the 7-gram check")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="write the rendered brief to SCR/dry_review/ only")
    args = ap.parse_args()
    rul = json.loads(RULINGS.read_text(encoding="utf-8"))
    ids = [r.get("id") for r in rul["rulings"]]
    if not all(isinstance(i, str) and i for i in ids) or len(set(ids)) != len(ids):
        raise SystemExit("REFUSED: every ruling needs a unique id")
    cond = rul["gate"]["s2_conditions"]
    if rul["gate"].get("primaries_may_launch") is not False:
        raise SystemExit("REFUSED: gate.primaries_may_launch is not false")
    ext = json.loads(EXTRACT.read_text(encoding="utf-8"))
    om = ext["orchestrator_measured"]
    counts = "%d pairs: %s" % (om["pairs"], ", ".join("%d %s" % (v, k) for k, v in sorted(om["counts"].items())))
    rows_n = sum(1 for x in APPLIED.read_text(encoding="utf-8").splitlines() if x.strip())
    pins = S5_PINS + [(r, *RUN_HERE[r]) if r in RUN_HERE else (r, u, w) for r, u, w in WRITER_PINS]
    if len({r for r, _, _ in pins}) != len(pins):
        raise SystemExit("REFUSED: a pin is listed twice")
    rows = ["| input | sha256 |", "|---|---|"]
    uses = ["", "How you may use each input:", ""]
    for rel, use, what in pins:
        p = (SP / rel).resolve()
        b = p.read_bytes()
        win = "SP\\" + rel.replace("/", "\\")
        rows.append("| `%s` | `%s` |" % (win, sha(b)))
        uses.append("- `%s`: %s. %s." % (win, use, what[0].upper() + what[1:]))
    eff = worker_block(M8)
    tpl = (HERE / "BRIEF_S5.template.md").read_text(encoding="utf-8")
    fill = {"{{SP}}": str(SP), "{{OUT}}": str(OUT), "{{PINS}}": "\n".join(rows + uses), "{{ATTEMPT}}": ATTEMPT,
            "{{EXECUTION}}": ATTEMPT + "#e1", "{{DELIVERABLE}}": DELIVERABLE, "{{ROWS_N}}": str(rows_n),
            "{{GATE}}": "\n".join("%d. %s" % (i, c) for i, c in enumerate(cond, 1)),
            "{{N_RULINGS}}": str(len(ids)), "{{RULING_IDS}}": ", ".join(ids),
            "{{N_UNRES}}": str(len(rul.get("unresolved_uncertainty", []))), "{{EXTRACT_COUNTS}}": counts,
            "{{EFFICIENCY}}": eff + "EFFICIENCY-OUT: %s\n" % OUT}
    body = tpl
    for k, v in fill.items():
        body = body.replace(k, v)
    if "{{" in body:
        raise SystemExit("REFUSED: an unfilled placeholder remains")
    if OTHER_BOOK.search(body):
        raise SystemExit("REFUSED: the brief names another book, %r (E-65)" % OTHER_BOOK.search(body).group(0))
    for bad in ("cor_w\\lane_", "cor_w/lane_", "final_FX", "cor_fx3\\", "cor_fx3/", "allowed_W"):
        if bad in body:
            raise SystemExit("REFUSED: the brief carries %r (blindness)" % bad)
    e1 = "execution `%s#e1`." % ATTEMPT
    if body.count(e1) != 1 or body.count("#e1") != 1:
        raise SystemExit("REFUSED: the brief must name %s#e1 exactly once" % ATTEMPT)
    brief = HERE / "BRIEF_S5.md"
    if args.dry_run:
        dry = SCR / "dry_review" / brief.name
        dry.parent.mkdir(parents=True, exist_ok=True)
        dry.write_bytes(body.encode("utf-8"))
        print(json.dumps({"dry_run": str(dry), "sha256": sha(body.encode("utf-8")), "pins": len(pins),
                          "rows": rows_n, "rulings": len(ids), "conditions": len(cond), "extract": counts},
                         ensure_ascii=False, indent=1))
        return 0
    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    run = lambda *a: subprocess.run([sys.executable, "-B", *a], cwd=str(SP), capture_output=True, text=True,  # noqa: E731
                                    encoding="utf-8", env=env)
    g = run("campaign/_inflight_pin_guard.py", "--book", "1Cor", "--target", "1Cor/review/" + brief.name)
    if json.loads(g.stdout).get("verdict") != "CLEAR":
        raise SystemExit("REFUSED: the pin guard is not CLEAR on %s" % brief.name)
    write_once(brief, body.encode("utf-8"))
    bsha = sha(brief.read_bytes())
    msg = MESSAGE.format(ledger=str(LEDGER), brief=str(brief), sha=bsha, work=WORK, efficiency=eff, out=str(OUT))
    mfile = SCR / "cor_review_msgs" / "launch_message_S5.txt"
    mfile.parent.mkdir(parents=True, exist_ok=True)
    write_once(mfile, msg.encode("utf-8"))
    (OUT / "work").mkdir(parents=True, exist_ok=True)
    pc = run("campaign/_brief_pin_check.py", "--brief", str(brief))
    lm = run("campaign/_launch_message_check.py", "--book", "1Cor", "--message", str(mfile))
    print(json.dumps({"lane": "S5", "attempt": ATTEMPT, "brief": brief.name, "brief_sha256": bsha, "pins": len(pins),
                      "message": str(mfile), "message_sha256": sha(mfile.read_bytes()),
                      "brief_pin_check": json.loads(pc.stdout)["verdict"],
                      "launch_message_check": json.loads(lm.stdout)["verdict"],
                      "launch_message_gaps": json.loads(lm.stdout)["gaps"]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
