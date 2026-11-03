#!/usr/bin/env python3
"""Build the 1 Corinthians S2 brief and launch message from BRIEF_S2.template.md, pins MEASURED from disk.

Ported 2026-10-20 from build_review_launch.py (the S1 builder) and the Daniel S2 brief (playbook v3: FIXUP-1 applied ->
S2 until fit). The gate text, the ruling ids and the counts are read from the installed E1 rulings, and the digest
classes from the installed S2 receipt extract, never typed. The pins are the S2 inputs (the applied rows and manifest,
the combined draft, the rulings, the extract, the CWO reports and sweep, the tool-fix fixtures with their baselines,
each part's fix-up brief, landed rows and change record, the E-73 corrections) plus the writer wave's pins, with
ngram7 RUN. The script refuses to overwrite a brief or message that exists and differs (E-41, E-44), refuses a brief
that names another book (E-65), carries a lane path or a lane final message, or does not name the execution exactly
once, refuses when the pin guard is not CLEAR, then runs _brief_pin_check.py and _launch_message_check.py --book 1Cor.

usage: build_s2_launch.py [--dry-run]
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
ATTEMPT = "cor_fixup_wave_review_s2_a1"
OUT = SCR / "cor_s2"
DELIVERABLE = "1cor_fixup_wave_review_S2.json"
WORK = "reviewing applied reading-unit rows against the rulings, the book strategy and the witnesses' bytes"
RULINGS = BK / "review" / "1cor_controlling_agent_rulings_E1.v1.json"
EXTRACT = BK / "review" / "tool_fixes" / "s2_receipt_extract.v1.json"
APPLIED = BK / "fixup" / "draft_rows_fixup1_applied.jsonl"
PARTS = ("W2", "W3", "W4", "W5", "W6")
COPY = "READ; copy to work\\ before running anything on it"
S2_PINS = [
    ("1Cor/fixup/draft_rows_fixup1_applied.jsonl", COPY, "THE ROWS UNDER REVIEW: the FIXUP-1 applied rows"),
    ("1Cor/fixup/draft_rows_fixup1_applied.manifest.json", "READ",
     "the apply manifest: source rows, each part's landed rows, the applied rows and the suite on the orchestrator's "
     "scratch copy; a claim to test"),
    ("1Cor/writer/draft_rows_combined.jsonl", COPY, "the rows before FIXUP-1 (the installed combined writer draft)"),
    ("1Cor/review/1cor_controlling_agent_rulings_E1.v1.json", "READ whole",
     "the E1 rulings: every ruling, the unresolved uncertainty, the corpus-wide orders and the gate"),
    ("1Cor/review/tool_fixes/s2_receipt_extract.v1.json", "READ",
     "whitelisted fields of review receipts rows 7-21 (tool-fix installs, gate flip, CWO reports, FIXUP-1 launches "
     "with each licence map inlined, FIXUP-1 completions) and the orchestrator's digest classes; a claim to test"),
    ("1Cor/review/cwo_1cor_baseline_report.v1.json", "READ", "the CWO coverage report on the rows before FIXUP-1"),
    ("1Cor/review/cwo_1cor_post_fixup1_report.v1.json", "READ",
     "the CWO coverage report on the applied rows; a claim to test"),
    ("1Cor/review/cwo_sweep_1cor.py", "RUN on a private copy; --out under OUT\\work only",
     "the CWO-1COR-01/-02 sweep"),
    ("1Cor/review/tool_fixes/fixtures_tf1.py", "RUN with --work under OUT\\work only", "the TF-1 fixtures"),
    ("1Cor/review/tool_fixes/fixtures_tf1.result.json", "READ", "the recorded TF-1 fixture result"),
    ("1Cor/review/tool_fixes/fixtures_tf2.py", "RUN with --work under OUT\\work only", "the TF-2 fixtures"),
    ("1Cor/review/tool_fixes/fixtures_tf2.result.json", "READ", "the recorded TF-2 fixture result"),
    ("1Cor/review/tool_fixes/_exec_as.py", "READ (the fixtures run it; it writes nothing)",
     "the fixture harness that runs a source as if installed"),
    ("1Cor/writer_lanes/_validate_writer_part_1cor.py.pre_b0be0d01fde7", "READ; the TF-1 fixtures' --baseline",
     "the writer-part validator before TF-1"),
    ("1Cor/tools/ngram7.py.pre_8646f540acc3", "READ; the TF-2 fixtures' --baseline", "ngram7 before TF-2"),
] + [x for p in PARTS for x in (
    ("1Cor/fixup/FIXUP1_BRIEF_%s.md" % p, "READ", "the orchestrator's FIXUP-1 brief for part %s" % p),
    ("1Cor/fixup/landed/%s_e1/fixup1_%s_rows.jsonl" % (p, p), "READ", "part %s's landed FIXUP-1 rows" % p),
    ("1Cor/fixup/landed/%s_e1/fixup1_%s_changes.json" % (p, p), "READ",
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
    pins = S2_PINS + [(r, *RUN_HERE[r]) if r in RUN_HERE else (r, u, w) for r, u, w in WRITER_PINS]
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
    tpl = (HERE / "BRIEF_S2.template.md").read_text(encoding="utf-8")
    fill = {"{{SP}}": str(SP), "{{OUT}}": str(OUT), "{{PINS}}": "\n".join(rows + uses), "{{ATTEMPT}}": ATTEMPT,
            "{{EXECUTION}}": ATTEMPT + "#e1", "{{DELIVERABLE}}": DELIVERABLE, "{{ROWS_N}}": str(rows_n),
            "{{GATE}}": "\n".join("%d. %s" % (i, c) for i, c in enumerate(cond, 1)),
            "{{N_RULINGS}}": str(len(ids)), "{{RULING_IDS}}": ", ".join(ids),
            "{{N_UNRES}}": str(len(rul.get("unresolved_uncertainty", []))),
            "{{N_CWO}}": str(len(rul.get("corpus_wide_orders", []))), "{{EXTRACT_COUNTS}}": counts,
            "{{EFFICIENCY}}": eff + "EFFICIENCY-OUT: %s\n" % OUT}
    body = tpl
    for k, v in fill.items():
        body = body.replace(k, v)
    if "{{" in body:
        raise SystemExit("REFUSED: an unfilled placeholder remains")
    if OTHER_BOOK.search(body):
        raise SystemExit("REFUSED: the brief names another book, %r (E-65)" % OTHER_BOOK.search(body).group(0))
    for bad in ("cor_w\\lane_", "cor_w/lane_", "final_FX1_", "cor_fx1\\", "cor_fx1/", "allowed_W"):
        if bad in body:
            raise SystemExit("REFUSED: the brief carries %r (blindness)" % bad)
    e1 = "execution `%s#e1`." % ATTEMPT
    if body.count(e1) != 1 or body.count("#e1") != 1:
        raise SystemExit("REFUSED: the brief must name %s#e1 exactly once" % ATTEMPT)
    brief = HERE / "BRIEF_S2.md"
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
    mfile = SCR / "cor_review_msgs" / "launch_message_S2.txt"
    mfile.parent.mkdir(parents=True, exist_ok=True)
    write_once(mfile, msg.encode("utf-8"))
    (OUT / "work").mkdir(parents=True, exist_ok=True)
    pc = run("campaign/_brief_pin_check.py", "--brief", str(brief))
    lm = run("campaign/_launch_message_check.py", "--book", "1Cor", "--message", str(mfile))
    print(json.dumps({"lane": "S2", "attempt": ATTEMPT, "brief": brief.name, "brief_sha256": bsha, "pins": len(pins),
                      "message": str(mfile), "message_sha256": sha(mfile.read_bytes()),
                      "brief_pin_check": json.loads(pc.stdout)["verdict"],
                      "launch_message_check": json.loads(lm.stdout)["verdict"],
                      "launch_message_gaps": json.loads(lm.stdout)["gaps"]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
