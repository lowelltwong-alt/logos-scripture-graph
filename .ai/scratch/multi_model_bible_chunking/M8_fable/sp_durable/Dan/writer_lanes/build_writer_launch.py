#!/usr/bin/env python3
"""Build one Daniel writer part's brief and launch message from BRIEF_W.template.md, with the pin table MEASURED from disk.

The part facts come from strategy_plan_Dan.json (parts, parents) and from strategy §9, whose table header, the part's
table row and the part's hard-items line are sliced verbatim; strategy §8 is sliced verbatim into {{SECTION8}}. The
message, the digest helpers, the ledger path, the common pins and the stop reasons are imported from
../phase0_lanes/build_launch.py so that both waves launch under one contract. The script refuses to overwrite a brief or
message that exists and differs (E-41, E-44), refuses when the pin guard is not CLEAR on the brief it would write, and
then runs _brief_pin_check.py and _launch_message_check.py --book Dan and prints their verdicts and the digests.

usage: build_writer_launch.py --part W1..W6 [--execution N]
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
sys.path.insert(0, str(HERE.parent / "phase0_lanes"))
sys.path.insert(0, str(BK / "tools"))
from build_launch import MESSAGE, write_once, sha, LEDGER, COMMON, STOPS, lands  # noqa: E402
import dan_lib  # noqa: E402

REC = BK / "dan_writer_attempt_receipts.jsonl"
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\dan_w")
WORK = "dividing the book into candidate reading units (chunk rows) with byte-cited boundary evidence"
RO = "READ ONLY - NEVER RUN (the suite runs it)"
SUITE = ["citation_sweep", "normalize_hebrew_in_json", "check_web_quotes", "check_refs_mirror", "check_marks",
         "check_universals", "check_language_zones", "ngram7", "cap_sweep", "check_register", "check_role_tokens"]
PINS = [
    ("Dan/tools/TOOLKIT.md", "READ whole, first", "the book facts, the hazards and the tools' contracts"),
    ("Dan/book_strategy_Dan.md", "READ whole", "the BINDING book strategy"),
    ("Dan/strategy_plan_Dan.json", "READ", "the strategy's machine plan: parents, parts, scrutiny targets"),
    ("Dan/Dan_oshb.txt", "READ; splice every Hebrew or Aramaic string from it",
     "the witness: OSHB (WLC), one verse per line `Dan.C.V<TAB>text`, MT numbering"),
    ("Dan/Dan_web_clean.txt", "READ", "the WEB text, cleaned, one verse per line, WEB numbering"),
    ("Dan/dan_language_zones.json", "READ", "Hebrew and Aramaic by verse (`verse_language`) and by word run"),
    ("Dan/web_mt_offset_map.json", "READ", "the WEB/MT crosswalk for the four zones"),
    ("Dan/verse_inventory.json", "READ", "the verse counts per chapter, WEB face"),
    ("Dan/pmarks_Dan.json", "READ", "PE and SAMEKH marks, paseq, and the K/Q layer (`kq`), MT face"),
    ("Dan/dan_device_inventory.json", "READ", "the EXTRACTED devices: datelines, calendar dates, formulae, switches"),
    ("Dan/tools/dan_lib.py", "READ; you may import it (python -B with PYTHONDONTWRITEBYTECODE=1)",
     "Daniel's library: zones, faces, verse order, web_to_mt and mt_to_web"),
    ("Dan/tools/check_tiling.py", "RUN on a private copy in OUT\\work only", "the tiling check"),
    ("Dan/tools/run_validator_suite.py", "RUN on a private copy in OUT\\work only (it writes its report beside it)",
     "the validator suite"),
] + [("Dan/tools/%s.py" % m, RO, "a validator suite member") for m in SUITE] + [
    ("Dan/writer_lanes/_validate_writer_part_dan.py", "RUN on a private copy in OUT\\work only (it writes nothing)",
     "the writer-part validator: schema, tiling, seams, language, zone pairs, spliced Hebrew"),
] + COMMON


def cv(ch, v):
    return "%d:%d" % (ch, v)


def paired(ch, v):
    """A WEB verse as the brief must write it: plain C:V off the zones, a web/oshb pair inside them."""
    m = dan_lib.web_to_mt(ch, v)
    if tuple(m) == (ch, v):
        return cv(ch, v)
    return "`web:Dan.%d.%d`=`oshb:Dan.%d.%d`" % (ch, v, m[0], m[1])


def neighbour(ch, v, step):
    if step < 0:
        if v > 1:
            return ch, v - 1
        return (ch - 1, dan_lib.LAST_VERSE[ch - 1]) if ch > 1 else None
    if v < dan_lib.LAST_VERSE[ch]:
        return ch, v + 1
    return (ch + 1, 1) if ch + 1 in dan_lib.LAST_VERSE else None


def one(lines, pred, what):
    hits = [x for x in lines if pred(x)]
    if len(hits) != 1:
        raise SystemExit("REFUSED: strategy %s matched %d lines, not 1" % (what, len(hits)))
    return hits[0]


def part_facts(part, plan, strat):
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
    hard = one(sec9, lambda x: x.startswith("  - %s:" % part), "§9 hard items " + part)
    out = ["- **Part %s**: WEB %s-%s, %d verses. Your deliverable file name is `%s_rows.jsonl`."
           % (part, paired(*s), paired(*e), p["verses"], part)]
    out.append("- **Parents** (id, span on the WEB face, title; `parent_collection` is the id then the title in parentheses):")
    for pid in p["parents"]:
        q = parents[pid]
        a, b = [tuple(int(n) for n in x.split(":")) for x in (q["start"], q["end"])]
        dual = "; MT face %s" % q["mt_dual"] if q.get("mt_dual") else ""
        out.append("  - %s: %s-%s, %d verses%s. Title: %s" % (pid, paired(*a), paired(*b), q["verses"], dual, q["title"]))
    seams = ["/".join(paired(*[int(n) for n in y.split(":")]) for y in x.split("/")) for x in p["internal_parent_seams"]]
    out.append("- **Internal parent seams** (a row never straddles one): %s." % ("; ".join(seams) if seams else "none"))
    before, after = neighbour(*s, -1), neighbour(*e, 1)
    ro = [paired(*before) if before else None, paired(*after) if after else None]
    # strategy §9: W3's writer reads 7:1-7:2, and W4's writer reads WEB 6:25-6:28, as read-only context
    if part == "W3":
        ro[1] = "7:1-7:2"
    if part == "W4":
        ro[0] = "`web:Dan.6.25`-`web:Dan.6.28`=`oshb:Dan.6.26`-`oshb:Dan.6.29`"
    ro = [x for x in ro if x]
    out.append("- **Read-only context** (read it to weigh your outer edges; never tile it): %s."
               % (" and ".join(ro) if ro else "none"))
    out.append("- From strategy §9, verbatim:")
    out.append("")
    out.extend(head)
    out.append("")
    out.append(hard)
    rng = "Dan.%d.%d-Dan.%d.%d" % (s + e)
    return "\n".join(out), rng


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", required=True, choices=["W%d" % n for n in range(1, 7)])
    ap.add_argument("--execution", type=int, default=1)
    args = ap.parse_args()
    part, N = args.part, args.execution
    if N < 1:
        raise SystemExit("REFUSED: --execution must be >= 1")
    attempt = "dan_writer_%s_a1" % part
    tag = "" if N == 1 else "_e%d" % N
    out = SCR / ("lane_" + part)
    plan = json.loads((BK / "strategy_plan_Dan.json").read_text(encoding="utf-8"))
    strat = (BK / "book_strategy_Dan.md").read_text(encoding="utf-8")
    facts, rng = part_facts(part, plan, strat)
    a8 = strat.index("\n## §8 Register and hygiene\n") + 1
    b8 = strat.index("\n## §9 ", a8) + 1
    sec8 = strat[a8:b8].rstrip("\n")
    rows = ["| input | sha256 |", "|---|---|"]
    uses = ["", "How you may use each input:", ""]
    for rel, use, what in PINS:
        p = (SP / rel).resolve()
        win = "SP\\" + rel.replace("/", "\\")
        rows.append("| `%s` | `%s` |" % (win, sha(p.read_bytes())))
        uses.append("- `%s`: %s. %s." % (win, use, what[0].upper() + what[1:]))
    tpl = (HERE / "BRIEF_W.template.md").read_text(encoding="utf-8")
    fill = {"{{SP}}": str(SP), "{{OUT}}": str(out), "{{PINS}}": "\n".join(rows + uses), "{{PART}}": part,
            "{{ATTEMPT}}": attempt, "{{EXECUTION}}": attempt + "#e1", "{{DELIVERABLE}}": part + "_rows.jsonl",
            "{{RANGE}}": rng, "{{PART_FACTS}}": facts, "{{SECTION8}}": sec8}
    body = tpl
    for k, v in fill.items():
        body = body.replace(k, v)
    if "{{" in body:
        raise SystemExit("REFUSED: an unfilled placeholder remains")
    if "Ezek" in body:
        raise SystemExit("REFUSED: the brief names another book (E-65)")
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
    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    run = lambda *a: subprocess.run([sys.executable, "-B", *a], cwd=str(SP), capture_output=True, text=True,  # noqa: E731
                                    encoding="utf-8", env=env)
    g = run("campaign/_inflight_pin_guard.py", "--book", "Dan", "--target", "Dan/writer_lanes/" + brief.name)
    if json.loads(g.stdout).get("verdict") != "CLEAR":
        raise SystemExit("REFUSED: the pin guard is not CLEAR on %s" % brief.name)
    write_once(brief, body.encode("utf-8"))
    bsha = sha(brief.read_bytes())
    msg = MESSAGE.format(ledger=str(LEDGER), brief=str(brief), sha=bsha, work=WORK)
    mfile = SCR / ("launch_message_%s%s.txt" % (part, tag))
    write_once(mfile, msg.encode("utf-8"))
    (out / "work").mkdir(parents=True, exist_ok=True)
    pc = run("campaign/_brief_pin_check.py", "--brief", str(brief))
    lm = run("campaign/_launch_message_check.py", "--book", "Dan", "--message", str(mfile))
    print(json.dumps({"part": part, "attempt": attempt, "execution": N, "range": rng, "brief": brief.name,
                      "brief_sha256": bsha, "pins": len(PINS), "message": mfile.name,
                      "message_sha256": sha(mfile.read_bytes()),
                      "brief_pin_check": json.loads(pc.stdout)["verdict"],
                      "launch_message_check": json.loads(lm.stdout)["verdict"],
                      "launch_message_gaps": json.loads(lm.stdout)["gaps"]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
