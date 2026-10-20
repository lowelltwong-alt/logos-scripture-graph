#!/usr/bin/env python3
"""Build one 1 Corinthians writer part's brief and launch message from BRIEF_W.template.md, pins MEASURED from disk.

Ported 2026-10-19 in shape from Dan/writer_lanes/build_writer_launch.py. The part facts come from
strategy_plan_1Cor.json (parts, parents) and from strategy §9, whose table header, rule and the part's table row are
sliced verbatim with the part's "W<n> holds ..." line; strategy §8 is sliced verbatim into {{SECTION8}}. The message,
the digest helpers, the ledger path, the common pins, the stop reasons and the efficiency worker block are imported
from ../phase0_lanes/build_launch.py so that both waves launch under one contract. A relaunch (--execution N > 1)
gets a fresh OUT, lane_<part>_e<N>, per L-0089. The script refuses to overwrite a brief or message that exists and
differs (E-41, E-44), refuses a brief that names another book (E-65), refuses when the pin guard is not CLEAR on the
brief it would write, and then runs _brief_pin_check.py and _launch_message_check.py --book 1Cor and prints their
verdicts and the digests.

usage: build_writer_launch.py --part W1..W6 [--execution N] [--dry-run]
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
BK = HERE.parent
SP = BK.parent
sys.path.insert(0, str(HERE.parent / "phase0_lanes"))
from build_launch import MESSAGE, write_once, sha, LEDGER, COMMON, STOPS, lands, M8, worker_block  # noqa: E402

REC = BK / "1cor_writer_attempt_receipts.jsonl"
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_w")
WORK = "dividing the book into candidate reading units (chunk rows) with byte-cited boundary evidence"
RO = "READ ONLY - NEVER RUN (the suite runs it)"
SUITE = ["citation_sweep", "normalize_greek_in_json", "check_web_quotes", "check_refs_mirror", "check_marks",
         "check_universals", "ngram7", "cap_sweep", "check_register", "check_role_tokens", "check_placeholders"]
OTHER_BOOK = re.compile(r"\b(Dan|Daniel|Ezek|Ezekiel)\b")
PINS = [
    ("1Cor/tools/TOOLKIT.md", "READ whole, first", "the book facts, the hazards and the tools' contracts"),
    ("1Cor/book_strategy_1Cor.md", "READ whole", "the BINDING book strategy"),
    ("1Cor/strategy_plan_1Cor.json", "READ", "the strategy's machine plan: parents, parts, scrutiny targets"),
    ("1Cor/1Cor_rp.txt", "READ; splice every Greek string from it",
     "the primary witness: Robinson-Pierpont Byzantine Textform (Unlicense), one verse per line"),
    ("1Cor/1Cor_sbl.txt", "READ; splice a disclosed SBLGNT reading from it, signs kept",
     "the secondary witness: SBLGNT (CC BY 4.0) with its critical signs, one verse per line"),
    ("1Cor/1Cor_web_clean.txt", "READ", "the WEB text, cleaned, one verse per line"),
    ("1Cor/verse_inventory.json", "READ", "the verse counts per chapter, WEB face"),
    ("1Cor/web_greek_verse_check.json", "READ", "the WEB/RP/SBLGNT verse-count check per chapter"),
    ("1Cor/web_greek_offset_map.json", "READ", "the WEB/Greek crosswalk (identity in this book)"),
    ("1Cor/pmarks_1Cor.json", "READ", "the RP pilcrows, the WEB paragraph starts and footnote verses, the SBLGNT "
     "variant sites and the RP/SBLGNT difference list"),
    ("1Cor/1cor_device_inventory.json", "READ", "the EXTRACTED devices: formulae, onsets, slogans, signs, totals"),
    ("1Cor/tools/cor_lib.py", "READ; you may import it (python -B with PYTHONDONTWRITEBYTECODE=1); never run its "
     "--selftest", "the 1 Corinthians library: verse order, witnesses, marks, the Greek-run pattern"),
    ("../greek_substrate/tools/greek_lib.py", "READ ONLY - NEVER RUN; cor_lib imports it at load time",
     "the Greek substrate library: nfc, skeleton, strip_accents, the Greek-run pattern"),
    ("1Cor/tools/check_tiling.py", "RUN on a private copy in OUT\\work only", "the tiling check"),
    ("1Cor/tools/run_validator_suite.py", "RUN on a private copy in OUT\\work only (it writes its report beside it)",
     "the validator suite"),
] + [("1Cor/tools/%s.py" % m, RO, "a validator suite member") for m in SUITE] + [
    ("1Cor/writer_lanes/_validate_writer_part_1cor.py", "RUN on a private copy in OUT\\work only (it writes nothing)",
     "the writer-part validator: schema, tiling, seams, the §10 conventions, spliced Greek and attribution"),
] + COMMON


def cv(ch, v):
    return "%d:%d" % (ch, v)


def one(lines, pred, what):
    hits = [x for x in lines if pred(x)]
    if len(hits) != 1:
        raise SystemExit("REFUSED: strategy %s matched %d lines, not 1" % (what, len(hits)))
    return hits[0]


def neighbour(ch, v, step, last):
    if step < 0:
        if v > 1:
            return ch, v - 1
        return (ch - 1, last[ch - 1]) if ch > 1 else None
    if v < last[ch]:
        return ch, v + 1
    return (ch + 1, 1) if ch + 1 in last else None


def part_facts(part, plan, strat, last):
    p = {x["id"]: x for x in plan["parts"]}[part]
    parents = {x["id"]: x for x in plan["parents"]}
    s, e = [tuple(int(n) for n in x.split(":")) for x in (p["start"], p["end"])]
    lines = strat.splitlines()
    i9 = one(range(len(lines)), lambda i: lines[i].startswith("## §9 "), "§9 heading")
    i10 = one(range(len(lines)), lambda i: lines[i].startswith("## §10 "), "§10 heading")
    sec9 = lines[i9:i10]
    head = [one(sec9, lambda x: x.startswith("| id |"), "§9 table header"),
            one(sec9, lambda x: x.startswith("|---"), "§9 table rule"),
            one(sec9, lambda x: x.startswith("| %s |" % part), "§9 row " + part)]
    holds = one(sec9, lambda x: x.startswith("  - %s holds " % part), "§9 holds line " + part)
    out = ["- **Part %s**: WEB %s-%s, %d verses. Your deliverable file name is `%s_rows.jsonl`."
           % (part, cv(*s), cv(*e), p["verses"], part)]
    out.append("- **Parents** (id, span on the WEB face, title; `parent_collection` is the id then the title in "
               "parentheses):")
    for pid in p["parents"]:
        q = parents[pid]
        out.append("  - %s: %s-%s, %d verses. Title: %s" % (pid, q["start"], q["end"], q["verses"], q["title"]))
    seams = p["internal_parent_seams"]
    out.append("- **Internal parent seams** (a row never straddles one): %s." % ("; ".join(seams) if seams else "none"))
    ro = [neighbour(*s, -1, last), neighbour(*e, 1, last)]
    ro = [cv(*x) for x in ro if x]
    out.append("- **Read-only context** (read it to weigh your outer edges; never tile it): %s."
               % (" and ".join(ro) if ro else "none"))
    out.append("- From strategy §9, verbatim:")
    out.append("")
    out.extend(head)
    out.append("")
    out.append(holds)
    rng = "1Cor.%d.%d-1Cor.%d.%d" % (s + e)
    return "\n".join(out), rng


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", required=True, choices=["W%d" % n for n in range(1, 7)])
    ap.add_argument("--execution", type=int, default=1)
    ap.add_argument("--dry-run", action="store_true", help="write the rendered brief to SCR/dry/ only; nothing in SP")
    args = ap.parse_args()
    part, N = args.part, args.execution
    if N < 1:
        raise SystemExit("REFUSED: --execution must be >= 1")
    attempt = "cor_writer_%s_a1" % part
    tag = "" if N == 1 else "_e%d" % N
    out = SCR / ("lane_" + part + tag)
    plan = json.loads((BK / "strategy_plan_1Cor.json").read_text(encoding="utf-8"))
    strat = (BK / "book_strategy_1Cor.md").read_text(encoding="utf-8")
    inv = json.loads((BK / "verse_inventory.json").read_text(encoding="utf-8"))
    last = {int(c): n for c, n in inv["chapters"].items()}
    facts, rng = part_facts(part, plan, strat, last)
    a8 = strat.index("\n## §8 Register and hygiene (copy verbatim into every writer brief)\n") + 1
    b8 = strat.index("\n## §9 ", a8) + 1
    sec8 = strat[a8:b8].rstrip("\n")
    rows = ["| input | sha256 |", "|---|---|"]
    uses = ["", "How you may use each input:", ""]
    for rel, use, what in PINS:
        p = (SP / rel).resolve()
        win = "SP\\" + rel.replace("/", "\\")
        rows.append("| `%s` | `%s` |" % (win, sha(p.read_bytes())))
        uses.append("- `%s`: %s. %s." % (win, use, what[0].upper() + what[1:]))
    eff = worker_block(M8)
    tpl = (HERE / "BRIEF_W.template.md").read_text(encoding="utf-8")
    fill = {"{{SP}}": str(SP), "{{OUT}}": str(out), "{{PINS}}": "\n".join(rows + uses), "{{PART}}": part,
            "{{ATTEMPT}}": attempt, "{{EXECUTION}}": attempt + "#e1", "{{DELIVERABLE}}": part + "_rows.jsonl",
            "{{RANGE}}": rng, "{{PART_FACTS}}": facts, "{{SECTION8}}": sec8,
            "{{EFFICIENCY}}": eff + "EFFICIENCY-OUT: %s\n" % out}
    body = tpl
    for k, v in fill.items():
        body = body.replace(k, v)
    if "{{" in body:
        raise SystemExit("REFUSED: an unfilled placeholder remains")
    if OTHER_BOOK.search(body):
        raise SystemExit("REFUSED: the brief names another book, %r (E-65)" % OTHER_BOOK.search(body).group(0))
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
    brief = HERE / ("BRIEF_%s%s.md" % (part, tag))
    if args.dry_run:
        dry = SCR / "dry" / brief.name
        dry.parent.mkdir(parents=True, exist_ok=True)
        dry.write_bytes(body.encode("utf-8"))
        print(json.dumps({"dry_run": str(dry), "sha256": sha(body.encode("utf-8")), "range": rng}, indent=1))
        return 0
    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    run = lambda *a: subprocess.run([sys.executable, "-B", *a], cwd=str(SP), capture_output=True, text=True,  # noqa: E731
                                    encoding="utf-8", env=env)
    g = run("campaign/_inflight_pin_guard.py", "--book", "1Cor", "--target", "1Cor/writer_lanes/" + brief.name)
    if json.loads(g.stdout).get("verdict") != "CLEAR":
        raise SystemExit("REFUSED: the pin guard is not CLEAR on %s" % brief.name)
    write_once(brief, body.encode("utf-8"))
    bsha = sha(brief.read_bytes())
    msg = MESSAGE.format(ledger=str(LEDGER), brief=str(brief), sha=bsha, work=WORK, efficiency=eff, out=str(out))
    mfile = SCR / ("launch_message_%s%s.txt" % (part, tag))
    write_once(mfile, msg.encode("utf-8"))
    (out / "work").mkdir(parents=True, exist_ok=True)
    pc = run("campaign/_brief_pin_check.py", "--brief", str(brief))
    lm = run("campaign/_launch_message_check.py", "--book", "1Cor", "--message", str(mfile))
    print(json.dumps({"part": part, "attempt": attempt, "execution": N, "range": rng, "brief": brief.name,
                      "brief_sha256": bsha, "pins": len(PINS), "message": mfile.name,
                      "message_sha256": sha(mfile.read_bytes()),
                      "brief_pin_check": json.loads(pc.stdout)["verdict"],
                      "launch_message_check": json.loads(lm.stdout)["verdict"],
                      "launch_message_gaps": json.loads(lm.stdout)["gaps"]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
