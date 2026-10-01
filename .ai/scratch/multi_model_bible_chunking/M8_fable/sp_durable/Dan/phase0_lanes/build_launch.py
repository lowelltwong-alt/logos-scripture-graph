#!/usr/bin/env python3
"""Build one Daniel Phase 0 lane's brief and launch message from its template, with the pin table MEASURED from disk.

The brief's pin rows are the two-column shape `_brief_pin_check.py` parses: | `SP\\<path>` | `<64 hex>` |. The use line for
each input sits in a separate list that carries no digest. The launch message carries every string that
`_launch_message_check.py` requires (ledger E-62), plus a BRIEF line naming the built brief at its digest. The script
refuses to overwrite a brief or message that exists and differs (E-41, E-44). It then runs both checkers, and prints
their verdicts and the digests.

usage: build_launch.py --lane D|T1|T2|S|C1|C2 [--execution N]
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
SP = HERE.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(SP / "campaign"))
from _inflight_pin_guard import lands  # noqa: E402  one landing rule, shared with the pin guard (2026-09-24)
LEDGER = SP.parent / "ERROR_PATTERN_LEDGER.v1.md"
REC = SP / "Dan" / "dan_phase0_attempt_receipts.jsonl"
STOPS = {"FAILED_BY_RUNTIME_WATCHDOG": "stopped by the runtime watchdog",
         "FAILED_BY_API_SESSION_LIMIT": "stopped by the account's API session limit",
         # added 2026-09-28: T1 #e2 and S #e2 were stopped by the weekly limit, a different limit from the session one
         "FAILED_BY_API_WEEKLY_LIMIT": "stopped by the account's API weekly limit"}
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\dan_p0")
MIRROR = "READ; copy into OUT\\mirror"
DAN_FACE = [
    ("Dan/Dan_oshb.txt", MIRROR, "the witness: OSHB (WLC), one verse per line `Dan.C.V<TAB>text`, MT numbering"),
    ("Dan/Dan_web_clean.txt", MIRROR, "the WEB text, cleaned, one verse per line, WEB numbering"),
    ("Dan/dan_language_zones.json", MIRROR, "Hebrew and Aramaic by verse and by word run; the mixed verse 2:4"),
    ("Dan/web_mt_offset_map.json", MIRROR, "the WEB/MT crosswalk: four zones, 66 verses per face"),
    ("Dan/verse_inventory.json", MIRROR, "the verse counts per chapter, declared on the WEB face"),
]
COMMON = [
    ("campaign/grader_models.v1.json", "READ", "the grader carrier: the OW-25 fallback model and its statement"),
    ("../ERROR_PATTERN_LEDGER.v1.md", "READ lines 807-874 only", "the M8 ledger: OW-11, the owner's exception, and OW-11-h"),
]
LANES = {
    "D": {
        "attempt": "dan_p0_device_inventory_a1",
        "pins": [
            ("Ezek/_build_device_inventory_ezek.py", "READ ONLY - NEVER RUN", "the Ezekiel builder you port"),
            ("Ezek/ezek_device_inventory.json", "READ, through a script of yours", "the Ezekiel inventory it wrote"),
            ("Ezek/tools/citation_sweep.py", "READ ONLY - NEVER RUN; lines 300-320, 390-410 and 590-700",
             "the calendar arm that consumes the inventory"),
            ("Ezek/tools/_toolkit_selfcheck.py", "READ ONLY - NEVER RUN; lines 40-125", "the counts it asserts"),
        ] + DAN_FACE + [
            ("Dan/web_mt_verse_check.json", "READ", "the per-chapter verse counts on both faces"),
            ("Dan/tools/dan_lib.py", "READ; you may import it, running python -B", "Daniel's zones, faces and verse order"),
        ] + COMMON,
    },
    "T2": {
        "attempt": "dan_p0_toolport_t2_a1",
        "pins": [
            ("Ezek/tools/check_web_quotes.py", "READ ONLY - NEVER RUN (the adapter reads it)", "tool to port"),
            ("Ezek/tools/check_refs_mirror.py", "READ ONLY - NEVER RUN (the adapter reads it)", "tool to port"),
            ("Ezek/tools/check_marks.py", "READ ONLY - NEVER RUN (the adapter reads it)", "tool to port"),
            ("Ezek/tools/_punct_boundary_sweep.py", "READ ONLY - NEVER RUN (the adapter reads it)", "tool to port"),
            ("Ezek/tools/_audit_book_token_transform.py", "READ ONLY - NEVER RUN (the adapter reads it)",
             "tool to port; it globs, so no one but the orchestrator runs it"),
            ("Ezek/tools/ezek_lib.py", "READ", "the Ezekiel library the five tools import"),
            ("Ezek/tools/TOOLKIT.md", "READ, in ranges", "the Ezekiel toolkit's own account of these tools"),
            ("Dan/tools/_adapt_tools_dan.py", "RUN `python -B ... --stage OUT\\stage --extra-spec OUT\\spec_t2.py` only",
             "the adapter"),
            ("Dan/tools/_adapt_tools_dan_spec.py", "READ ONLY - NEVER RUN", "the base spec: the model for yours"),
            ("Dan/tools/dan_lib.py", MIRROR, "Daniel's library: zones, faces and verse order"),
        ] + DAN_FACE + [
            ("Dan/web_mt_verse_check.json", MIRROR, "the per-chapter verse counts on both faces"),
            ("Dan/pmarks_Dan.json", MIRROR, "Daniel's paratextual marks"),
            ("Dan/tools/verse_map_web.json", MIRROR + "\\Dan\\tools", "verse map, WEB"),
            ("Dan/tools/verse_map_oshb.json", MIRROR + "\\Dan\\tools", "verse map, OSHB"),
            ("Dan/tools/consonantal_index.json", MIRROR + "\\Dan\\tools, if a tool reads it", "the consonantal index"),
        ] + COMMON,
    },
    # added 2026-09-24: built only after T2's five tools and lane D's inventory are installed (the pins need them)
    "T1": {
        "attempt": "dan_p0_toolport_t1_a1",
        "pins": [
            ("Ezek/tools/citation_sweep.py", "READ ONLY - NEVER RUN (the adapter reads it)", "tool to port"),
            ("Ezek/tools/_test_zone_tools_ezek.py", "READ ONLY - NEVER RUN (the adapter reads it, through RENAME)",
             "the test to port, as _test_zone_tools_dan.py"),
            ("Ezek/tools/ezek_lib.py", "READ", "the Ezekiel library both files import"),
            ("Ezek/tools/TOOLKIT.md", "READ lines 277-330 only", "the Ezekiel toolkit's own account of these arms"),
            ("Ezek/ezek_device_inventory.json", "READ, through a script of yours",
             "the Ezekiel inventory that the zone test's section 7 reads"),
            ("Dan/tools/_adapt_tools_dan.py", "RUN `python -B ... --stage OUT\\stage --extra-spec OUT\\spec_t1.py` only",
             "the adapter"),
            ("Dan/tools/_adapt_tools_dan_spec.py", "READ ONLY - NEVER RUN", "the base spec: the model for yours"),
            ("Dan/tools/dan_lib.py", MIRROR + "\\Dan\\tools", "Daniel's library: zones, faces and verse order"),
            ("Dan/tools/check_marks.py", MIRROR + "\\Dan\\tools; run only by the ported test, in the mirror",
             "installed (lane T2's port); the zone test runs it"),
            ("Dan/tools/check_web_quotes.py", MIRROR + "\\Dan\\tools; run only by the ported test, in the mirror",
             "installed (lane T2's port); the zone test runs it"),
            ("Dan/tools/check_register.py", MIRROR + "\\Dan\\tools; run only by the ported test, in the mirror",
             "installed (base spec); the zone test runs it"),
            ("Dan/tools/normalize_hebrew_in_json.py", MIRROR + "\\Dan\\tools; run only by the ported test, in the mirror",
             "installed (base spec); the zone test runs it"),
            ("Dan/dan_device_inventory.json", MIRROR + "\\Dan",
             "lane D's installed inventory: the only source of the calendar constants"),
        ] + DAN_FACE + [
            ("Dan/web_mt_verse_check.json", MIRROR + "\\Dan", "the per-chapter verse counts on both faces"),
            ("Dan/pmarks_Dan.json", MIRROR + "\\Dan", "Daniel's paratextual marks"),
            ("Dan/tools/verse_map_web.json", MIRROR + "\\Dan\\tools", "verse map, WEB; citation_sweep reads it"),
            ("Dan/tools/verse_map_oshb.json", MIRROR + "\\Dan\\tools", "verse map, OSHB; citation_sweep reads it"),
            ("Dan/tools/consonantal_index.json", MIRROR + "\\Dan\\tools, if a tool reads it", "the consonantal index"),
        ] + COMMON,
    },
    # added 2026-09-24: the book strategy (OW-6b controlling role, run on Opus per OW-25); it reads SP read-only and runs
    # only the strategy validator, which writes nothing, so no mirror is needed
    "S": {
        "attempt": "dan_strategy_a1",
        "work": "planning, from the book's own structural signals, how it divides into units for later annotation (a "
                "book strategy)",
        "pins": [
            ("Ezek/book_strategy_Ezek.v2.md", "READ lines 1-51 and 267-749; lines 52-266 only as needed",
             "Ezekiel's strategy, the model of FORM; none of its figures is Daniel's"),
            ("../BIBLE_CHUNKING_METHOD.v6.md", "READ lines 134-284, 464-583 and 640-819 only",
             "the cross-generation method record"),
            ("campaign/daniel_start_readiness.v2.json", "READ whole",
             "what is settled for Daniel: track, scrutiny targets, lens requirement"),
            ("campaign/hardness_batch_01.json", "READ lines 66-94 only", "Daniel's hardness entry"),
            ("Dan/_validate_strategy_dan.py", "RUN `python -B ... --md OUT\\book_strategy_Dan.md --plan "
             "OUT\\strategy_plan_Dan.json` only (it writes nothing); READ", "the strategy validator"),
            ("Dan/dan_device_inventory.json", "READ, through scripts of yours", "Daniel's device inventory, MT face"),
            ("Dan/pmarks_Dan.json", "READ, through scripts of yours", "Daniel's paratextual marks"),
            ("Dan/Dan_oshb.txt", "READ, through scripts of yours",
             "the witness: OSHB (WLC), one verse per line `Dan.C.V<TAB>text`, MT numbering"),
            ("Dan/Dan_web_clean.txt", "READ, through scripts of yours", "the WEB text, cleaned, one verse per line, WEB "
             "numbering"),
            ("Dan/dan_language_zones.json", "READ, through scripts of yours",
             "Hebrew and Aramaic by verse and by word run; the mixed verse 2:4"),
            ("Dan/web_mt_offset_map.json", "READ", "the WEB/MT crosswalk"),
            ("Dan/web_mt_verse_check.json", "READ", "the per-chapter verse counts on both faces"),
            ("Dan/verse_inventory.json", "READ", "the verse counts per chapter, declared on the WEB face"),
            ("Dan/tools/dan_lib.py", "READ; you may import it, running python -B", "Daniel's zones, faces and verse "
             "order"),
        ] + COMMON,
    },
    # added 2026-09-24: the two blind strategy check lanes (OW-19). They pin the candidate the orchestrator copies,
    # write-once, from lane S's OUT, so neither can be built before S lands. C1 re-measures the bytes; C2 reads the
    # text first and never sees the device inventory or the validator, so the two methods stay decorrelated.
    "C1": {
        "attempt": "dan_strategy_check_c1_a1",
        "work": "checking, against the book's own bytes, a plan for how it divides into units for later annotation",
        "pins": [
            ("Dan/strategy_candidate/book_strategy_Dan.a1.md", "READ, through scripts of yours", "the candidate strategy"),
            ("Dan/strategy_candidate/strategy_plan_Dan.a1.json", "READ", "the candidate's plan"),
            ("Dan/_validate_strategy_dan.py", "RUN `python -B ... --md <the candidate md> --plan <the candidate plan>` "
             "only (it writes nothing); READ", "the strategy validator"),
            ("Dan/verse_inventory.json", "READ", "the verse counts per chapter, declared on the WEB face"),
            ("Dan/web_mt_offset_map.json", "READ", "the WEB/MT crosswalk"),
            ("Dan/web_mt_verse_check.json", "READ", "the per-chapter verse counts on both faces"),
            ("Dan/dan_language_zones.json", "READ, through scripts of yours",
             "Hebrew and Aramaic by verse and by word run; the mixed verse 2:4"),
            ("Dan/dan_device_inventory.json", "READ, through scripts of yours", "Daniel's device inventory, MT face"),
            ("Dan/pmarks_Dan.json", "READ, through scripts of yours", "Daniel's paratextual marks"),
            ("Dan/Dan_oshb.txt", "READ, through scripts of yours",
             "the witness: OSHB (WLC), one verse per line `Dan.C.V<TAB>text`, MT numbering"),
            ("Dan/Dan_web_clean.txt", "READ, through scripts of yours", "the WEB text, cleaned, one verse per line, WEB "
             "numbering"),
            ("Dan/tools/dan_lib.py", "READ; you may import it, running python -B", "Daniel's zones, faces and verse "
             "order"),
            ("campaign/daniel_start_readiness.v2.json", "READ whole", "the prepared scrutiny targets"),
            ("campaign/hardness_batch_01.json", "READ lines 66-94 only", "Daniel's hardness entry and boundary risks"),
        ] + COMMON,
    },
    "C2": {
        "attempt": "dan_strategy_check_c2_a1",
        "work": "checking, against a first-hand reading of the book's text, a plan for how it divides into units for "
                "later annotation",
        "pins": [
            ("Dan/Dan_web_clean.txt", "READ, through scripts of yours, in Stage A", "the WEB text, cleaned, one verse "
             "per line, WEB numbering"),
            ("Dan/Dan_oshb.txt", "READ, through scripts of yours, in Stage A",
             "the witness: OSHB (WLC), one verse per line `Dan.C.V<TAB>text`, MT numbering"),
            ("Dan/dan_language_zones.json", "READ, through scripts of yours, in Stage A",
             "Hebrew and Aramaic by verse and by word run; the mixed verse 2:4"),
            ("Dan/pmarks_Dan.json", "READ, through scripts of yours, in Stage A", "Daniel's paratextual marks"),
            ("Dan/web_mt_offset_map.json", "READ", "the WEB/MT crosswalk"),
            ("Dan/verse_inventory.json", "READ", "the verse counts per chapter, declared on the WEB face"),
            ("Dan/tools/dan_lib.py", "READ; you may import it, running python -B", "Daniel's zones, faces and verse "
             "order"),
            ("Dan/strategy_candidate/book_strategy_Dan.a1.md", "READ in Stage B only, through scripts of yours",
             "the candidate strategy"),
            ("Dan/strategy_candidate/strategy_plan_Dan.a1.json", "READ in Stage B only", "the candidate's plan"),
            ("campaign/hardness_batch_01.json", "READ lines 66-94 only, in Stage B only",
             "Daniel's hardness entry, with its divided readings"),
            ("campaign/daniel_start_readiness.v2.json", "READ whole, in Stage B only", "the prepared scrutiny targets"),
        ] + COMMON,
    },
    # added 2026-09-28: the two blind toolkit review lanes (OW-19) that close Phase 0. K1 re-measures every figure and
    # fact in TOOLKIT.md against the bytes; K2 reads the tools' code against the toolkit's account of them and runs no
    # pinned file (E-67). Both briefs name E-65's item: the guard's blindness below 100, to Daniel-true figures and to
    # non-integers.
    "K1": {
        "attempt": "dan_toolkit_review_k1_a1",
        "work": "checking, against the book's own bytes, the statements of fact in a verification toolkit for the book",
        "pins": [
            ("Dan/tools/TOOLKIT.md", "READ whole", "the toolkit under review"),
            ("Dan/Dan_oshb.txt", "READ, through scripts of yours",
             "the witness: OSHB (WLC), one verse per line `Dan.C.V<TAB>text`, MT numbering"),
            ("Dan/Dan_web_clean.txt", "READ, through scripts of yours", "the WEB text, cleaned, one verse per line, WEB "
             "numbering"),
            ("Dan/Dan_web.usfm", "READ, through scripts of yours", "the WEB member, verbatim"),
            ("Dan/pmarks_Dan.json", "READ, through scripts of yours", "Daniel's paratextual marks and notes"),
            ("Dan/dan_language_zones.json", "READ, through scripts of yours",
             "Hebrew and Aramaic by verse and by word run; the mixed verse 2:4"),
            ("Dan/dan_device_inventory.json", "READ, through scripts of yours", "Daniel's device inventory, MT face"),
            ("Dan/web_mt_offset_map.json", "READ", "the WEB/MT crosswalk"),
            ("Dan/web_mt_verse_check.json", "READ", "the per-chapter verse counts on both faces"),
            ("Dan/verse_inventory.json", "READ", "the verse counts per chapter, declared on the WEB face"),
            ("Dan/dan_stage_report.json", "READ", "the staging report: sources, digests and counts"),
            ("Dan/book_strategy_Dan.md", "READ, through scripts of yours", "the reconciled book strategy"),
            ("Dan/strategy_plan_Dan.json", "READ", "the reconciled strategy plan"),
            ("Dan/tools/verse_map_web.json", "READ, through scripts of yours", "verse map, WEB"),
            ("Dan/tools/verse_map_oshb.json", "READ, through scripts of yours", "verse map, OSHB"),
            ("Dan/tools/dan_lib.py", "READ; you may import it, running python -B", "Daniel's library: zones, faces, "
             "verse order and the skeleton"),
        ] + COMMON,
    },
    "K2": {
        "attempt": "dan_toolkit_review_k2_a1",
        "work": "checking a verification toolkit's account of its checking tools against the tools' own code",
        "pins": [
            ("Dan/tools/TOOLKIT.md", "READ whole", "the toolkit under review"),
            ("Dan/tools/run_validator_suite.py", "READ ONLY - NEVER RUN; in ranges", "a staged tool the toolkit describes"),
            ("Dan/tools/citation_sweep.py", "READ ONLY - NEVER RUN; in ranges", "a staged tool the toolkit describes"),
            ("Dan/tools/normalize_hebrew_in_json.py", "READ ONLY - NEVER RUN; in ranges", "a staged tool the toolkit describes"),
            ("Dan/tools/check_marks.py", "READ ONLY - NEVER RUN; in ranges", "a staged tool the toolkit describes"),
            ("Dan/tools/check_language_zones.py", "READ ONLY - NEVER RUN; in ranges", "a staged tool the toolkit describes"),
            ("Dan/tools/check_role_tokens.py", "READ ONLY - NEVER RUN; in ranges", "a staged tool the toolkit describes"),
            ("Dan/tools/check_brief_vs_suite.py", "READ ONLY - NEVER RUN; in ranges", "a staged tool the toolkit describes"),
            ("Dan/tools/cap_sweep.py", "READ ONLY - NEVER RUN; in ranges", "a staged tool the toolkit describes"),
            ("Dan/tools/build_verse_maps.py", "READ ONLY - NEVER RUN; in ranges", "a staged tool the toolkit describes"),
            ("Dan/tools/dan_lib.py", "READ ONLY - NEVER RUN; in ranges", "a staged tool the toolkit describes"),
            ("Dan/tools/_toolkit_selfcheck.py", "READ ONLY - NEVER RUN; in ranges", "a staged tool the toolkit describes"),
            ("Dan/tools/_test_zone_tools_dan.py", "READ ONLY - NEVER RUN; in ranges", "a staged tool the toolkit describes"),
            ("Dan/tools/_test_language_zones_dan.py", "READ ONLY - NEVER RUN; in ranges", "a staged tool the toolkit describes"),
        ] + COMMON,
    },
}
WORK = "counting the book's structural signals and porting deterministic checking tools"
MESSAGE ="""RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible (the book of \
Daniel, in Hebrew and Aramaic) for a study corpus: {work}. Quotations are short, sliced from public witnesses, and \
carry their attribution.

AUTHORITY (OW-11; it travels in this message, per OW-11-h). The owner authorized this Opus orchestration and its \
subagents for Ezekiel and Daniel. The owner's answers, verbatim: on authority, "Yes: Ezekiel, then Daniel"; on \
recording, "M8 log only". authorization_ref: lowell_chat_2026-09-10_m8_opus_orchestration_ezek_dan. You may verify \
this in the ledger {ledger} (the OW-11 addendum and OW-11-h, lines 807-874; read that range only). Every role runs on \
claude-opus-5-5, as a recorded grader_fallback (OW-25). Within that exception this subagent writes only in its own OUT \
directory. It never runs git, never writes a receipt and never touches the registry.

BRIEF: {brief} sha256 {sha}
First verify that the brief's sha256 equals the digest above. A mismatch is a hard stop: report it and stop. Then read \
the brief whole and execute it. The brief is binding on scope, inputs, budget and outputs.

E-19: Never run any existence check, listing, glob or recursive search, whether on SP, on OUT or anywhere else. Every \
path you need is written in the brief; open each by that exact path. State in your final message that you ran no \
listing and no glob.
"""


def sha(b):
    return hashlib.sha256(b).hexdigest()


def write_once(p, data):
    if p.exists() and p.read_bytes() != data:
        raise SystemExit("REFUSED: %s exists and differs" % p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True, choices=sorted(LANES))
    ap.add_argument("--execution", type=int, default=1,
                    help="N > 1 writes BRIEF_<L>_e<N>.md and launch_message_<L>_e<N>.txt naming execution #e<N> "
                         "(amended 2026-09-24: a relaunch must never carry the earlier execution's id)")
    args = ap.parse_args()
    L, N = args.lane, args.execution
    if N < 1:
        raise SystemExit("REFUSED: --execution must be >= 1")
    spec = LANES[L]
    tag = "" if N == 1 else "_e%d" % N
    out = SCR / ("lane_" + L)
    rows = ["| input | sha256 |", "|---|---|"]
    uses = ["", "How you may use each input:", ""]
    for rel, use, what in spec["pins"]:
        p = (SP / rel).resolve()
        win = "SP\\" + rel.replace("/", "\\")
        rows.append("| `%s` | `%s` |" % (win, sha(p.read_bytes())))
        uses.append("- `%s`: %s. %s." % (win, use, what[0].upper() + what[1:]))
    tpl = (HERE / ("BRIEF_%s.template.md" % L)).read_text(encoding="utf-8")
    body = tpl.replace("{{SP}}", str(SP)).replace("{{OUT}}", str(out)).replace("{{PINS}}", "\n".join(rows + uses))
    if "{{" in body:
        raise SystemExit("REFUSED: an unfilled placeholder remains")
    if N > 1:
        e1 = "execution `%s#e1`." % spec["attempt"]
        if body.count(e1) != 1 or body.count("#e1") != 1:
            raise SystemExit("REFUSED: the template must name %s#e1 exactly once" % spec["attempt"])
        # amended 2026-09-24: the stop reason is read from #e(N-1)'s landing row, never hard-coded (T2 #e1 was stopped
        # by the session limit, not the watchdog); an unlanded or unknown-outcome predecessor refuses the relaunch
        prev = "%s#e%d" % (spec["attempt"], N - 1)
        recs = [json.loads(x) for x in REC.read_text(encoding="utf-8").splitlines() if x.strip()]
        land = [r for r in recs if lands(r)
                and prev in (r.get("execution_id"), r.get("amends_execution_id"))]
        why = [v for k, v in STOPS.items() if len(land) == 1 and str(land[0].get("outcome") or "").startswith(k + " ")]
        if len(why) != 1:
            raise SystemExit("REFUSED: %s needs exactly one landing row whose outcome opens with one of: %s"
                             % (prev, ", ".join(STOPS)))
        body = body.replace(e1, "execution `%s#e%d`. This is a relaunch: execution #e%d was %s and landed no "
                                "deliverable, so OUT starts empty and nothing of #e%d's is yours to use."
                            % (spec["attempt"], N, N - 1, why[0], N - 1))
    brief = HERE / ("BRIEF_%s%s.md" % (L, tag))
    write_once(brief, body.encode("utf-8"))
    bsha = sha(brief.read_bytes())
    msg = MESSAGE.format(ledger=str(LEDGER), brief=str(brief), sha=bsha, work=spec.get("work", WORK))
    mfile = SCR / ("launch_message_%s%s.txt" % (L, tag))
    write_once(mfile, msg.encode("utf-8"))
    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONUTF8="1")
    run = lambda *a: subprocess.run([sys.executable, "-B", *a], cwd=str(SP), capture_output=True, text=True,  # noqa: E731
                                    encoding="utf-8", env=env)
    pc = run("campaign/_brief_pin_check.py", "--brief", str(brief))
    lm = run("campaign/_launch_message_check.py", "--book", "Dan", "--message", str(mfile))
    print(json.dumps({"lane": L, "attempt": spec["attempt"], "execution": N, "brief": str(brief), "brief_sha256": bsha,
                      "pins": len(spec["pins"]), "message": str(mfile), "message_sha256": sha(mfile.read_bytes()),
                      "brief_pin_check": json.loads(pc.stdout)["verdict"],
                      "launch_message_check": json.loads(lm.stdout)["verdict"],
                      "launch_message_gaps": json.loads(lm.stdout)["gaps"]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
