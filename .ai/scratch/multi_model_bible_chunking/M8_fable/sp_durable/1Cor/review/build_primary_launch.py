#!/usr/bin/env python3
"""Build one 1 Corinthians primary-review brief and launch message (one lens on one cluster) from
PRIMARY_BRIEF.template.md, pins MEASURED from disk.

Ported 2026-10-20 from build_s2_launch.py. The round is ordered by GATE-E3 of the installed E3 rulings: two blind lanes
(OL original language, LF literary form) on every cluster of review_clusters.json, plus the RECEPTION_TRADITION lens (RT)
on the clusters the plan's reception_lens names, all on the FIXUP-2 applied rows. The two questions GATE-E3 sends to the
primaries are copied whole from the installed rulings (never typed); the rulings file itself is NOT pinned in the brief
(blindness), but its digest is checked here. The script refuses: a cluster or lens the plan does not hold; an input whose
digest differs from the round's pin; a brief or message that exists and differs (E-41, E-44); a brief that names another
book (E-65), carries another lane's OUT or any review, ruling, fix-up or CWO path (blindness), or does not name the
execution exactly once; a pin guard that is not CLEAR. It then runs _brief_pin_check.py and _launch_message_check.py.

usage: build_primary_launch.py --lane OL|LF|RT --cluster cNN [--dry-run]
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
ROWS_REL = "1Cor/fixup/draft_rows_fixup2_applied.jsonl"
ROWS_SHA = "75933a142375d8736ae71cdcc7f0e0b9052c36ea4ac4b87ccacf676ae50c6fbe"
PLAN_REL = "1Cor/review_clusters.json"
PLAN_SHA = "a393f453f58d956b6d0951b513416f6678b0a78f445a796254f43ee718a17101"
RULINGS = BK / "review" / "1cor_controlling_agent_rulings_E3.v1.json"
RULINGS_SHA = "a7f32674dee0b0e27f25803729f93142cefdaf2847f9d7122010397e992efe70"
WORK = "reviewing reading-unit rows of one cluster under one lens against the book strategy and the witnesses' bytes"
COPY = "READ; copy to work\\ before running anything on it"
TITLE = {"OL": "ORIGINAL LANGUAGE (OL)", "LF": "LITERARY FORM AND DISCOURSE (LF)", "RT": "RECEPTION TRADITION (RT)"}
LENS = {
    "OL": (
        "Read in this order: TOOLKIT.md, strategy sections 3 and 4 and conventions C2, C5 and C8 in section 10, then for "
        "each row the RP and SBLGNT lines of its verses and of the neighbouring verses on each side of its seams, then "
        "the row. For every row:\n\n"
        "1. **Splices.** Byte-collate every Greek string in every field against `1Cor_rp.txt`, or `1Cor_sbl.txt` for a "
        "disclosed reading, by script. A string that is not an exact substring of the line it cites is a high finding.\n"
        "2. **Witness differences (C5).** Where the row's argument quotes RP wording at a verse listed in "
        "`rp_sbl_differences`, test whether the quoted words fall on a difference; if they do, the row must disclose the "
        "SBLGNT reading, and a quote that crosses an SBL sign reaches only the skeleton tier.\n"
        "3. **The seam in Greek, from both sides.** Name the connective, particle, vocative, formula or other Greek "
        "signal at the row's onset AND the close of the unit before it; say whether the Greek bears the seam, is "
        "neutral, or tells against it.\n"
        "4. **Marks in both directions.** Test every mark the row claims against `pmarks_1Cor.json`, and every RP pilcrow "
        "or SBL sign inside the row against what the row says. Never let one mark type stand for another.\n"
        "5. **Offsets.** Where a claim depends on where an English verse begins in the Greek, check "
        "`web_greek_offset_map.json` and `web_greek_verse_check.json`.\n\n"
        "Your challenges concern the Greek evidence, the witnesses and the marks. A literary-form claim you note only "
        "where the Greek contradicts it."),
    "LF": (
        "Read in this order: TOOLKIT.md, the strategy whole (sections 1, 2, 5, 6, 7 and 8, and conventions C1, C3, C4, "
        "C6 and C7 in section 10), `1cor_device_inventory.json`, then for each row the WEB text of its verses and of "
        "the neighbouring rows, then the row. For every row:\n\n"
        "1. **The seam from both sides.** What closes the unit before and what opens this one: topic shift, heading "
        "formula (C4), address, inclusio, summary, return to an earlier topic. An onset-only argument is incomplete.\n"
        "2. **Devices.** Every device the row names, against the device inventory: a named device that is not there, or "
        "is there and misdescribed, is a finding; so is an inventoried device inside the row that bears on the seam and "
        "goes unweighed.\n"
        "3. **Conventions.** Slogan extent (C3), heading onsets (C4), frame typing (C6), and tradition and slogan "
        "integrity (C7), exactly as the strategy states them.\n"
        "4. **Typing and confidence.** The unit_type against the section 6 vocabulary, granularity against the over- and "
        "under-split risks, and the confidence against the evidence the row itself gives (section 7 names the "
        "low-confidence regions). A confidence stronger than its stated evidence is a finding.\n"
        "5. **Quotations and register.** Every WEB quotation verbatim, sliced by script; register under section 8.\n\n"
        "Your challenges concern form, typing, confidence, quotation and register. A Greek byte claim you note only "
        "where a form claim depends on it."),
    "RT": (
        "Read in this order: TOOLKIT.md, strategy section 4 (its marker policy and cross-tradition scope, including the "
        "14:33b-36 block), section 7 (scrutiny target B), section 8 (items 9, 10 and 13) and conventions C7 and C9 in "
        "section 10, then for each row the WEB, RP and SBLGNT text of its verses, then the row. For every row:\n\n"
        "1. **Divided readings.** Where interpretive traditions divide on a reading the row touches, is the division "
        "reported neutrally and attributed, never preferred, and never used to move or support a seam?\n"
        "2. **Silent adoption.** Does the row's seam, typing, title or rationale adopt one tradition's reading as if it "
        "were neutral description?\n"
        "3. **Scope.** Is cross-tradition material confined to metadata in prose, as section 8 requires?\n"
        "4. **C9.** On the row or rows holding 14:33-14:36: the attachment, SBL-site and transposition disclosures, "
        "measured against the witnesses and the strategy's own statement of them.\n\n"
        "Your knowledge of the traditions is not a pinned source. A claim about what a tradition holds is tier ASSUMED "
        "unless a pinned file states it, and it may ground a challenge only where the row itself prefers, adopts or "
        "omits what the strategy requires. Your challenges concern neutrality, attribution, scope and the C9 "
        "disclosures."),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True, choices=sorted(LENS))
    ap.add_argument("--cluster", required=True)
    ap.add_argument("--dry-run", action="store_true", help="write the rendered brief to SCR/dry_review/ only")
    a = ap.parse_args()
    for rel, want in ((ROWS_REL, ROWS_SHA), (PLAN_REL, PLAN_SHA)):
        if sha((SP / rel).read_bytes()) != want:
            raise SystemExit("REFUSED: %s digest differs from the round's pin" % rel)
    if sha(RULINGS.read_bytes()) != RULINGS_SHA:
        raise SystemExit("REFUSED: the E3 rulings digest differs from the round's pin")
    plan = json.loads((SP / PLAN_REL).read_text(encoding="utf-8"))
    cl = {c["id"]: c for c in plan["clusters"]}
    if a.cluster not in cl:
        raise SystemExit("REFUSED: no cluster %r in the plan" % a.cluster)
    if a.lane == "RT" and a.cluster not in plan["reception_lens"]["clusters"]:
        raise SystemExit("REFUSED: the RT lens runs only on %s" % plan["reception_lens"]["clusters"])
    c = cl[a.cluster]
    rows = [json.loads(x) for x in (SP / ROWS_REL).read_text(encoding="utf-8").splitlines() if x.strip()]
    ids = [r["decision_id"] for r in rows]
    i0, i1 = ids.index(c["row_ids"][0]), ids.index(c["row_ids"][-1])
    if ids[i0:i1 + 1] != c["row_ids"]:
        raise SystemExit("REFUSED: the cluster is not contiguous in the rows file")
    nb = ["%s (%s) before" % (ids[i0 - 1], rows[i0 - 1]["span"]) if i0 else "none before 1Cor.1.1",
          "%s (%s) after" % (ids[i1 + 1], rows[i1 + 1]["span"]) if i1 + 1 < len(ids) else "none after 1Cor.16.24"]
    gate = [r for r in json.loads(RULINGS.read_text(encoding="utf-8"))["rulings"] if r.get("id") == "GATE-E3"]
    orders = [o for o in gate[0]["orders"] if isinstance(o, dict) and o.get("to") == "primaries"] if len(gate) == 1 else []
    if len(orders) != 2 or not orders[0]["order"].startswith("Asked, not ruled (E1 S1-06") \
            or not orders[1]["order"].startswith("Asked, not ruled (E1 S1-02)"):
        raise SystemExit("REFUSED: GATE-E3 does not carry the two expected primaries questions")
    tids = ["TRIAGE-1COR-01", "TRIAGE-1COR-02"]
    w3 = sorted({x for x in ("W3-001", "W3-002", "W3-003", "W3-004") if x in c["row_ids"]})
    triage = "\n\n".join([
        "**%s** (GATE-E3, copied whole; it concerns W3-001..W3-004, %s): %s" % (
            tids[0], "of which your cluster holds " + ", ".join(w3) if w3 else "none of which is in your cluster",
            orders[0]["order"]),
        "**%s** (GATE-E3, copied whole; it concerns every row, so it is in your cluster): %s" % (tids[1],
                                                                                                orders[1]["order"])])
    tally = json.loads((BK / "pmarks_1Cor.json").read_text(encoding="utf-8"))["tally"]
    rt = ""
    if a.lane == "RT":
        rt = ("## The reception lens's scope\n\nThe RT lens reads only the rows overlapping 1Cor.11.2-1Cor.14.40, which "
              "the plan's `reception_lens` lists (%d rows in clusters %s). It is a third lens beside the two blind "
              "lanes, not a replacement for either.\n\n" % (len(plan["reception_lens"]["rows"]),
                                                             ", ".join(plan["reception_lens"]["clusters"])))
    pins = [(ROWS_REL, COPY, "THE ROWS UNDER REVIEW: the applied rows, %d rows" % len(ids)),
            (PLAN_REL, "READ", "the primary-round cluster plan; your cluster is %s" % a.cluster)] + list(WRITER_PINS)
    if len({r for r, _, _ in pins}) != len(pins):
        raise SystemExit("REFUSED: a pin is listed twice")
    tab = ["| input | sha256 |", "|---|---|"]
    uses = ["", "How you may use each input:", ""]
    for rel, use, what in pins:
        b = (SP / rel).resolve().read_bytes()
        win = "SP\\" + rel.replace("/", "\\")
        tab.append("| `%s` | `%s` |" % (win, sha(b)))
        uses.append("- `%s`: %s. %s." % (win, use, what[0].upper() + what[1:]))
    tag = "%s_%s" % (a.lane, a.cluster)
    attempt = "cor_primary_%s_a1" % tag.lower()
    out = SCR / "cor_prim" / (tag + "_e1")
    deliverable = "final_%s_e1.json" % tag
    eff = worker_block(M8)
    tpl = (HERE / "PRIMARY_BRIEF.template.md").read_text(encoding="utf-8")
    fill = {"{{SP}}": str(SP), "{{OUT}}": str(out), "{{PINS}}": "\n".join(tab + uses), "{{ATTEMPT}}": attempt,
            "{{EXECUTION}}": attempt + "#e1", "{{DELIVERABLE}}": deliverable, "{{LANE}}": a.lane,
            "{{LANE_TITLE}}": TITLE[a.lane], "{{CLUSTER}}": a.cluster, "{{PART}}": c["part"], "{{SPAN}}": c["span"],
            "{{CLUSTER_N}}": str(c["rows"]), "{{ROW_IDS}}": "`, `".join(c["row_ids"]), "{{ROWS_SHA}}": ROWS_SHA,
            "{{ROWS_N}}": str(len(ids)), "{{N_CLUSTERS}}": str(len(cl)), "{{CLUSTER_RULE}}": plan["rule"],
            "{{NEIGHBOURS}}": "; ".join(nb), "{{RT_SCOPE}}": rt, "{{TRIAGE_IDS}}": " and ".join(tids),
            "{{TRIAGE}}": triage, "{{TALLY}}": json.dumps(tally), "{{LENS}}": LENS[a.lane], "{{BUDGET}}": "45",
            "{{EFFICIENCY}}": eff + "EFFICIENCY-OUT: %s\n" % out}
    body = tpl
    for k, v in fill.items():
        body = body.replace(k, v)
    if "{{" in body:
        raise SystemExit("REFUSED: an unfilled placeholder remains")
    if OTHER_BOOK.search(body):
        raise SystemExit("REFUSED: the brief names another book, %r (E-65)" % OTHER_BOOK.search(body).group(0))
    bad = ["1cor_controlling_agent_rulings", "1cor_fixup2_review_S", "1cor_fixup_wave_review_S", "FIXUP2_BRIEF",
           "FIXUP1_BRIEF", "cwo_1cor", "draft_rows_fixup2_applied.manifest", "cor_ctl", "cor_s2", "cor_s3", "cor_w\\",
           "cor_fx", "sent_message_", "launch_message_"]
    bad += ["%s_%s_e" % (ln, ci) for ln in LENS for ci in cl if (ln, ci) != (a.lane, a.cluster)]
    hit = [x for x in bad if x in body]
    if hit:
        raise SystemExit("REFUSED: the brief carries %r (blindness)" % hit)
    e1 = "execution `%s#e1`." % attempt
    if body.count(e1) != 1 or body.count("#e1") != 1:
        raise SystemExit("REFUSED: the brief must name %s#e1 exactly once" % attempt)
    brief = HERE / "primaries" / ("PRIMARY_BRIEF_%s.md" % tag)
    if a.dry_run:
        dry = SCR / "dry_review" / brief.name
        dry.parent.mkdir(parents=True, exist_ok=True)
        dry.write_bytes(body.encode("utf-8"))
        print(json.dumps({"dry_run": str(dry), "sha256": sha(body.encode("utf-8")), "pins": len(pins),
                          "cluster": c["id"], "rows": c["rows"], "neighbours": nb, "triage_w3": w3}, ensure_ascii=False))
        return 0
    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    run = lambda *x: subprocess.run([sys.executable, "-B", *x], cwd=str(SP), capture_output=True, text=True,  # noqa: E731
                                    encoding="utf-8", env=env)
    g = run("campaign/_inflight_pin_guard.py", "--book", "1Cor", "--target", "1Cor/review/primaries/" + brief.name)
    if json.loads(g.stdout).get("verdict") != "CLEAR":
        raise SystemExit("REFUSED: the pin guard is not CLEAR on %s" % brief.name)
    brief.parent.mkdir(exist_ok=True)
    write_once(brief, body.encode("utf-8"))
    bsha = sha(brief.read_bytes())
    msg = MESSAGE.format(ledger=str(LEDGER), brief=str(brief), sha=bsha, work=WORK, efficiency=eff, out=str(out))
    mfile = SCR / "cor_review_msgs" / ("launch_message_PRIM_%s.txt" % tag)
    mfile.parent.mkdir(parents=True, exist_ok=True)
    write_once(mfile, msg.encode("utf-8"))
    (out / "work").mkdir(parents=True, exist_ok=True)
    pc = run("campaign/_brief_pin_check.py", "--brief", str(brief))
    lm = run("campaign/_launch_message_check.py", "--book", "1Cor", "--message", str(mfile))
    print(json.dumps({"lane": tag, "attempt": attempt, "brief": brief.name, "brief_sha256": bsha, "pins": len(pins),
                      "message": str(mfile), "message_sha256": sha(mfile.read_bytes()),
                      "brief_pin_check": json.loads(pc.stdout)["verdict"],
                      "launch_message_check": json.loads(lm.stdout)["verdict"],
                      "launch_message_gaps": json.loads(lm.stdout)["gaps"]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
