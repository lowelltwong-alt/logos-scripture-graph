#!/usr/bin/env python3
"""Build one 1 Corinthians Phase 0 lane's brief and launch message from its template, with the pin table MEASURED from
disk.

Ported 2026-10-14 from Dan/phase0_lanes/build_launch.py. What changed, beyond the book constants:
  - the launch message carries OW-36's authority (the owner's "Your six-book queue (Recommended)") and the NT research
    preamble, never OW-11's Hebrew Bible shape, which `_launch_message_check.py --book 1Cor` refuses;
  - the message and the brief both carry the efficiency worker block (m8_execution_efficiency.worker_block, the
    OWNER_EXECUTION_EFFICIENCY_2026-10-06 contract) and an `EFFICIENCY-OUT: <absolute OUT>` line;
  - the witnesses are WEB plus the committed Greek substrate (RP primary, SBLGNT secondary; OW-31/OW-35), on identity
    numbering, so there is no crosswalk zone and no language zone.

The brief's pin rows are the two-column shape `_brief_pin_check.py` parses: | `SP\\<path>` | `<64 hex>` |. The use line
for each input sits in a separate list that carries no digest. The script refuses to overwrite a brief or message that
exists and differs (E-41, E-44). It then runs both checkers and prints their verdicts and the digests. It is not the
last command before a launch: the scratch prelaunch_gate.py is (E-69).

usage: build_launch.py --lane D|T2|T1|T3|S|C1|C2|K1|K2 [--execution N]
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
M8 = SP.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(SP / "campaign"))
from _inflight_pin_guard import lands  # noqa: E402  one landing rule, shared with the pin guard
from m8_execution_efficiency import worker_block  # noqa: E402  the efficiency launch contract
LEDGER = M8 / "ERROR_PATTERN_LEDGER.v1.md"
REC = SP / "1Cor" / "1cor_phase0_attempt_receipts.jsonl"
STOPS = {"FAILED_BY_RUNTIME_WATCHDOG": "stopped by the runtime watchdog",
         "FAILED_BY_API_SESSION_LIMIT": "stopped by the account's API session limit",
         "FAILED_BY_API_WEEKLY_LIMIT": "stopped by the account's API weekly limit"}
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_p0")
MIRROR = "READ; copy byte-exact to the same relative path under OUT\\mirror\\M8\\sp_durable"
COR_FACE = [
    ("1Cor/1Cor_rp.txt", MIRROR, "the primary Greek witness: Byzantine RP, one verse per line `1Cor.C.V<TAB>text`, "
     "byte-identical to greek_lib.load_rp(); pilcrows removed and recorded in pmarks_1Cor.json"),
    ("1Cor/1Cor_sbl.txt", MIRROR, "the secondary Greek witness: SBLGNT, one verse per line, byte-identical to "
     "greek_lib.load_sbl(); its inline critical signs U+2E00-U+2E05 are kept"),
    ("1Cor/1Cor_web_clean.txt", MIRROR, "the WEB text, cleaned: chapter banners, `[v] N` verse lines, `¶` paragraph "
     "lines and ` |q1`/` |q2` continuation lines"),
    ("1Cor/pmarks_1Cor.json", MIRROR, "the mark evidence: RP pilcrows, WEB paragraph starts, SBLGNT sign sites, RP/SBL "
     "skeleton differences, WEB footnote verses"),
    ("1Cor/web_greek_offset_map.json", MIRROR, "the WEB/Greek crosswalk: identity on all 437 verses"),
    ("1Cor/verse_inventory.json", MIRROR, "the verse counts per chapter, declared on the WEB face"),
    ("1Cor/web_greek_verse_check.json", MIRROR, "per-chapter WEB, RP and SBL counts"),
]
LIBS = [
    ("1Cor/tools/cor_lib.py", MIRROR + "; your code imports the mirror copy, running python -B; never run its "
     "--selftest (it reads the whole substrate, which is not pinned; the orchestrator ran it: 24/24 GREEN)",
     "the 1 Corinthians library: verse order, faces, refs, witness loaders, collation and the Greek skeleton"),
    ("../greek_substrate/tools/greek_lib.py", MIRROR + " (that is, OUT\\mirror\\M8\\greek_substrate\\tools); READ in "
     "ranges; never call its load_* functions", "the Greek substrate library cor_lib imports at load time: nfc, "
     "strip_accents, skeleton, bounded_find, collate_greek"),
]
SOURCE = "READ ONLY - NEVER RUN; " + MIRROR[len("READ; "):] + " (your adapter reads the copy)"
PORT_CANDIDATES = ["check_web_quotes.py", "check_refs_mirror.py", "check_universals.py", "cap_sweep.py",
                   "check_register.py", "check_role_tokens.py", "check_tiling.py", "check_placeholders.py",
                   "check_brief_vs_suite.py", "ngram7.py", "_punct_boundary_sweep.py", "check_atomic_isolation.py",
                   "sweep.py", "_audit_book_token_transform.py"]
COMMON = [
    ("campaign/grader_models.v1.json", "READ", "the grader carrier: the OW-25 fallback model and its statement"),
    ("campaign/REVIEWER_CONTINUATION_CONTRACT.v1.md", "READ whole", "the continuation contract the efficiency block "
     "names"),
    ("../ERROR_PATTERN_LEDGER.v1.md", "READ lines 3412-3434 only", "the M8 ledger: OW-36, the owner's grant for this book"),
]
K2_TOOLS = [  # every tool TOOLKIT.md's "Staged tools" section names, with the adapter and its specs
    ("run_validator_suite.py", "the suite runner"), ("citation_sweep.py", "the citation sweep"),
    ("normalize_greek_in_json.py", "the Greek normalizer"), ("check_marks.py", "the mark checker"),
    ("check_role_tokens.py", "the role-token member"), ("check_brief_vs_suite.py", "the brief-versus-suite checker"),
    ("check_placeholders.py", "the placeholder member"), ("ngram7.py", "the 7-gram member"),
    ("cap_sweep.py", "the whole-chapter cap sweep"), ("cor_lib.py", "the shared library"),
    ("_toolkit_selfcheck.py", "the toolkit selfcheck"), ("_test_tools_1cor.py", "the T1 fixture test"),
    ("_test_marks_tools_1cor.py", "the T3 fixture test"), ("check_web_quotes.py", "a suite member"),
    ("check_refs_mirror.py", "a suite member"), ("check_universals.py", "a suite member"),
    ("check_register.py", "a suite member"), ("check_tiling.py", "a tool named in the toolkit"),
    ("sweep.py", "a tool named in the toolkit"), ("check_atomic_isolation.py", "a tool named in the toolkit"),
    ("_punct_boundary_sweep.py", "a tool named in the toolkit"),
    ("_audit_book_token_transform.py", "a tool named in the toolkit"),
    ("_adapt_tools_1cor.py", "the adapter that ported the tools"), ("_adapt_tools_1cor_spec.py", "its base spec"),
    ("_adapt_tools_1cor_spec_t1.py", "lane T1's extra spec"), ("_adapt_tools_1cor_spec_t3.py", "lane T3's extra spec"),
]
LANES = {
    "D": {
        "attempt": "cor_p0_device_inventory_a1",
        "pins": [
            ("Dan/_build_device_inventory_dan.py", "READ ONLY - NEVER RUN; in ranges",
             "the Daniel builder: the model of form, not of content"),
            ("Dan/dan_device_inventory.json", "READ, through a script of yours", "the Daniel inventory it wrote"),
            ("Dan/tools/citation_sweep.py", "READ ONLY - NEVER RUN; lines 40-50, 300-310, 385-400 and 575-700 only",
             "the calendar arm that consumes Daniel's inventory constants"),
        ] + COR_FACE + LIBS + COMMON,
    },
    "T2": {
        "attempt": "cor_p0_toolport_t2_a1",
        "pins": [
            ("Dan/tools/_adapt_tools_dan.py", "READ ONLY - NEVER RUN", "Daniel's adapter: the model for yours"),
            ("Dan/tools/_adapt_tools_dan_spec.py", "READ ONLY - NEVER RUN", "Daniel's base spec: the model for yours"),
            ("Dan/tools/dan_lib.py", "READ ONLY - NEVER RUN; in ranges", "the Daniel library the tools import"),
            ("Dan/tools/TOOLKIT.md", "READ lines 226-262 only", "Daniel's toolkit's own account of its tools"),
            ("Dan/tools/run_validator_suite.py", "READ ONLY - NEVER RUN", "Daniel's suite: its member list, which a "
             "later lane ports; you only classify its members"),
        ] + [("Dan/tools/" + t, SOURCE, "a candidate to port") for t in PORT_CANDIDATES] + COR_FACE + LIBS + COMMON,
    },
    "T1": {
        "attempt": "cor_p0_toolport_t1_a1",
        "pins": [
            ("Dan/tools/citation_sweep.py", "READ ONLY - NEVER RUN; in ranges; the installed adapter reads it in place",
             "the Daniel source of citation_sweep.py"),
            ("Dan/tools/_test_zone_tools_dan.py", "READ ONLY - NEVER RUN; in ranges; the installed adapter reads it in "
             "place (RENAME)", "the Daniel source of _test_tools_1cor.py"),
            ("Dan/tools/dan_lib.py", "READ ONLY - NEVER RUN; in ranges", "the Daniel library both sources import"),
            ("Dan/tools/TOOLKIT.md", "READ lines 97-167 only", "Daniel's fabrication classes and device spine"),
            ("Dan/dan_device_inventory.json", "READ, through a script of yours", "the Daniel inventory the calendar "
             "arm reads"),
            ("1Cor/tools/_adapt_tools_1cor.py", "READ whole; RUN only as `python -B SP\\1Cor\\tools\\_adapt_tools_1cor.py "
             "--stage OUT\\stage --extra-spec OUT\\spec_t1.py` from cwd SP, never with --install", "the installed "
             "adapter (lane T2's, reproduced byte-identically by the orchestrator)"),
            ("1Cor/tools/_adapt_tools_1cor_spec.py", "READ whole; the adapter imports it", "the base spec: the model "
             "of shape for yours"),
            ("1Cor/tools/check_web_quotes.py", MIRROR + "; run only by the test", "an installed 1 Corinthians tool "
             "the ported test runs"),
            ("1Cor/tools/check_register.py", MIRROR + "; run only by the test", "an installed 1 Corinthians tool the "
             "ported test runs"),
            ("1Cor/1cor_device_inventory.json", MIRROR + "; the only source of the device constants",
             "the 1 Corinthians device inventory (WEB face = Greek face)"),
            ("../greek_substrate/tools/citation_sweep.py", "READ ONLY - NEVER RUN", "the substrate's Greek citation "
             "sweep: the model for the quote binding and its tier-overclaim rule"),
            ("../greek_substrate/tools/collate.py", "READ ONLY - NEVER RUN", "the substrate's collation front end"),
        ] + COR_FACE + LIBS + COMMON,
    },
    "T3": {
        "attempt": "cor_p0_toolport_t3_a1",
        "pins": [
            ("Dan/tools/check_marks.py", "READ ONLY - NEVER RUN; in ranges; the installed adapter reads it in place",
             "the Daniel source of check_marks.py"),
            ("Dan/tools/normalize_hebrew_in_json.py", "READ ONLY - NEVER RUN; the installed adapter reads it in place "
             "(RENAME)", "the Daniel source of normalize_greek_in_json.py"),
            ("Dan/tools/run_validator_suite.py", "READ ONLY - NEVER RUN; the installed adapter reads it in place",
             "the Daniel source of run_validator_suite.py"),
            ("Dan/tools/_test_zone_tools_dan.py", "READ ONLY - NEVER RUN; in ranges, searching inside it by its exact "
             "path", "the Daniel test whose check_marks and normalizer sections you port into _test_marks_tools_1cor.py"),
            ("Dan/tools/dan_lib.py", "READ ONLY - NEVER RUN; in ranges", "the Daniel library the sources import"),
            ("Dan/tools/TOOLKIT.md", "READ lines 81-138 and 226-276 only", "Daniel's parashah layer, fabrication "
             "classes, disclosure inventories, staged tools and encoding notes"),
            ("1Cor/tools/_adapt_tools_1cor.py", "READ whole; RUN only as `python -B SP\\1Cor\\tools\\_adapt_tools_1cor.py "
             "--stage OUT\\stage --extra-spec OUT\\spec_t3.py` from cwd SP, never with --install", "the installed "
             "adapter (lane T2's, reproduced byte-identically by the orchestrator)"),
            ("1Cor/tools/_adapt_tools_1cor_spec.py", "READ whole; the adapter imports it", "the base spec: the model "
             "of shape for yours"),
        ] + [("1Cor/tools/" + t, MIRROR + "; run only by the suite or the test", "an installed 1 Corinthians suite "
              "member") for t in ["check_web_quotes.py", "check_refs_mirror.py", "check_universals.py", "ngram7.py",
                                  "cap_sweep.py", "check_register.py", "check_role_tokens.py",
                                  "check_placeholders.py"]] + [
            ("1Cor/tools/check_brief_vs_suite.py", MIRROR + "; run only as --selftest against your staged suite",
             "the installed brief-versus-suite checker"),
            ("1Cor/1cor_device_inventory.json", MIRROR + "; ngram7 reads it", "the 1 Corinthians device inventory"),
            ("../greek_substrate/tools/normalize_greek_in_json.py", "READ ONLY - NEVER RUN", "the substrate's Greek "
             "normalizer: the model for yours"),
        ] + COR_FACE + LIBS + COMMON,
    },
    "S": {
        "attempt": "cor_strategy_a1",
        "work": "writing the book strategy, the planning record every later 1 Corinthians writer and checker reads",
        "pins": [
            ("Dan/book_strategy_Dan.md", "READ lines 1-68 and 140-529; lines 69-139 only as needed", "Daniel's final "
             "strategy: the model of form only, never of content (E-65)"),
            ("../BIBLE_CHUNKING_METHOD.v7.md", "READ lines 147-311, 512-633 and 690-878 only", "the cross-generation "
             "method record (that is, M8\\BIBLE_CHUNKING_METHOD.v7.md)"),
            ("1Cor/1cor_start_readiness.v1.json", "READ whole", "the 1 Corinthians readiness record: track, authority, "
             "lens kinds and the 7 prepared scrutiny targets"),
            ("campaign/hardness_batch_03.json", "READ lines 9-38 only", "the hardness scorer's 1 Corinthians entry"),
            ("1Cor/_validate_strategy_1cor.py", "READ; RUN only as `python -B SP\\1Cor\\_validate_strategy_1cor.py "
             "--md OUT\\book_strategy_1Cor.md --plan OUT\\strategy_plan_1Cor.json` (it writes nothing)",
             "the strategy validator"),
            ("1Cor/1cor_device_inventory.json", "READ, through scripts of yours", "the 1 Corinthians device inventory "
             "(WEB face = Greek face), with its 8 for_fable_end_review items"),
        ] + [(r, "READ, through scripts of yours that print counts and short slices", w) for r, _u, w in COR_FACE] + [
            ("1Cor/tools/cor_lib.py", "READ in ranges; your scripts may import it in place, running python -B; never "
             "run its --selftest", "the 1 Corinthians library: verse order, faces, refs, witness loaders and the Greek "
             "skeleton"),
            ("../greek_substrate/tools/greek_lib.py", "READ in ranges; cor_lib imports it at load time; never call "
             "its load_* functions", "the Greek substrate library: nfc, strip_accents, skeleton, bounded_find"),
        ] + COMMON,
    },
    # the two blind strategy checks (OW-19); built only after S lands and its candidate is copied, byte-exact, to
    # 1Cor/strategy_candidate/
    "C1": {
        "attempt": "cor_strategy_check_c1_a1",
        "work": "checking, against the book's own bytes, a plan for how it divides into units for later annotation",
        "pins": [
            ("1Cor/strategy_candidate/book_strategy_1Cor.a1.md", "READ, through scripts of yours",
             "the candidate strategy"),
            ("1Cor/strategy_candidate/strategy_plan_1Cor.a1.json", "READ", "the candidate's plan"),
            ("1Cor/_validate_strategy_1cor.py", "RUN `python -B ... --md <the candidate md> --plan <the candidate "
             "plan>` only (it writes nothing); READ", "the strategy validator"),
            ("1Cor/1cor_device_inventory.json", "READ, through scripts of yours", "the 1 Corinthians device inventory "
             "(WEB face = Greek face)"),
        ] + [(r, "READ, through scripts of yours", w) for r, _u, w in COR_FACE] + [
            ("1Cor/tools/cor_lib.py", "READ; you may import it in place, running python -B; never run its --selftest",
             "the 1 Corinthians library: verse order, faces, refs, witness loaders and the Greek skeleton"),
            ("../greek_substrate/tools/greek_lib.py", "READ in ranges; cor_lib imports it at load time; never call its "
             "load_* functions", "the Greek substrate library"),
            ("1Cor/1cor_start_readiness.v1.json", "READ whole", "the prepared scrutiny targets and lens kinds"),
            ("campaign/hardness_batch_03.json", "READ lines 9-38 only", "the 1 Corinthians hardness entry and its "
             "boundary risks"),
        ] + COMMON,
    },
    "C2": {
        "attempt": "cor_strategy_check_c2_a1",
        "work": "checking, against a first-hand reading of the book's text, a plan for how it divides into units for "
                "later annotation",
        "pins": [(r, "READ, through scripts of yours, in Stage A", w) for r, _u, w in COR_FACE[:4]] + [
            ("1Cor/web_greek_offset_map.json", "READ", "the WEB/Greek crosswalk: identity on all 437 verses"),
            ("1Cor/verse_inventory.json", "READ", "the verse counts per chapter, declared on the WEB face"),
            ("1Cor/tools/cor_lib.py", "READ; you may import it in place, running python -B; never run its --selftest",
             "the 1 Corinthians library: verse order, faces, refs and witness loaders"),
            ("../greek_substrate/tools/greek_lib.py", "READ in ranges; cor_lib imports it at load time; never call its "
             "load_* functions", "the Greek substrate library"),
            ("1Cor/strategy_candidate/book_strategy_1Cor.a1.md", "READ in Stage B only, through scripts of yours",
             "the candidate strategy"),
            ("1Cor/strategy_candidate/strategy_plan_1Cor.a1.json", "READ in Stage B only", "the candidate's plan"),
            ("campaign/hardness_batch_03.json", "READ lines 9-38 only, in Stage B only",
             "the 1 Corinthians hardness entry, with its divided readings"),
            ("1Cor/1cor_start_readiness.v1.json", "READ whole, in Stage B only", "the prepared scrutiny targets"),
        ] + COMMON,
    },
    # the two blind toolkit reviews (OW-19): K1 re-measures TOOLKIT.md's facts on the bytes, K2 audits its tool
    # contracts against the code and runs no pinned file (E-67)
    "K1": {
        "attempt": "cor_toolkit_review_k1_a1",
        "work": "checking, against the book's own bytes, the figures and rules of a verification toolkit",
        "pins": [
            ("1Cor/tools/TOOLKIT.md", "READ, through scripts of yours that print counts and short slices",
             "the toolkit under review"),
        ] + [(r, "READ, through scripts of yours that print counts and short slices", w) for r, _u, w in COR_FACE] + [
            ("1Cor/1Cor_web.usfm", "READ, through scripts of yours", "the WEB source the clean extract was cut from"),
            ("1Cor/1cor_stage_report.json", "READ", "the staging report the Data files table cites"),
            ("1Cor/1cor_device_inventory.json", "READ, through scripts of yours", "the 1 Corinthians device inventory "
             "(WEB face = Greek face)"),
            ("1Cor/book_strategy_1Cor.md", "READ, through scripts of yours", "the reconciled strategy"),
            ("1Cor/strategy_plan_1Cor.json", "READ", "the reconciled strategy's plan"),
            ("1Cor/_validate_strategy_1cor.py", "READ; RUN only as `python -B SP\\1Cor\\_validate_strategy_1cor.py "
             "--md SP\\1Cor\\book_strategy_1Cor.md --plan SP\\1Cor\\strategy_plan_1Cor.json` (it writes nothing)",
             "the strategy validator"),
            ("1Cor/tools/cor_lib.py", "READ; your scripts may import it in place, running python -B; never run its "
             "selftest", "the 1 Corinthians library: verse order, faces, refs, witness loaders and the Greek skeleton"),
            ("../greek_substrate/tools/greek_lib.py", "READ in ranges; cor_lib loads it by exact path; never call its "
             "load_* functions and never run it", "the Greek substrate library: nfc, strip_accents, skeleton"),
        ] + COMMON,
    },
    "K2": {
        "attempt": "cor_toolkit_review_k2_a1",
        "work": "checking, against the tools' source code, the contracts a verification toolkit states for its tools",
        "pins": [
            ("1Cor/tools/TOOLKIT.md", "READ in ranges", "the toolkit under review"),
        ] + [("1Cor/tools/" + t, "READ ONLY - NEVER RUN; in ranges", w) for t, w in K2_TOOLS] + [
            ("../greek_substrate/tools/greek_lib.py", "READ ONLY - NEVER RUN; in ranges", "the Greek substrate library "
             "cor_lib loads by exact path: nfc, strip_accents, skeleton, collate_greek"),
            ("1Cor/1cor_device_inventory.json", "READ, through scripts of yours", "the device inventory ngram7.py "
             "reads its keys from"),
            ("campaign/_cure_verification.py", "READ ONLY - NEVER RUN; in ranges", "the tool a standing rule names"),
            ("campaign/_launch_message_check.py", "READ ONLY - NEVER RUN; in ranges", "the tool a standing rule names"),
        ] + COMMON,
    },
}
MESSAGE = """RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Greek New Testament (the \
first letter to the Corinthians, in Greek with a public-domain English translation) for a study corpus: {work}. \
Quotations are short, sliced from public witnesses (Robinson-Pierpont Byzantine text, Unlicense; SBLGNT, CC BY 4.0; \
World English Bible, public domain), and carry their attribution.

AUTHORITY (OW-36; it travels in this message, per OW-11-h). The owner authorized this Opus orchestration and its \
subagents for six books: 1 Corinthians, John, Romans, Revelation, Hebrews and Matthew. The owner's answer, verbatim: \
"Your six-book queue (Recommended)". authorization_ref: lowell_chat_2026-10-14_m8_opus_orchestration_six_book_queue. \
You may verify this in the ledger {ledger} (OW-36, lines 3412-3434; read that range only). Every role runs on \
claude-opus-5-5, as a recorded grader_fallback (OW-25). Within that grant this subagent writes only in its own OUT \
directory. It never runs git, never writes a receipt and never touches the registry.

BRIEF: {brief} sha256 {sha}
First verify that the brief's sha256 equals the digest above. A mismatch is a hard stop: report it and stop. Then read \
the brief whole and execute it. The brief is binding on scope, inputs, budget and outputs.

{efficiency}EFFICIENCY-OUT: {out}

E-19: Never run any existence check, listing, glob or recursive search, whether on SP, on OUT or anywhere else. Every \
path you need is written in the brief; open each by that exact path. State in your final message that you ran no \
listing and no glob.
"""
WORK = "counting the book's structural signals and porting deterministic checking tools"


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
                    help="N > 1 writes BRIEF_<L>_e<N>.md and launch_message_<L>_e<N>.txt naming execution #e<N>")
    args = ap.parse_args()
    L, N = args.lane, args.execution
    if N < 1:
        raise SystemExit("REFUSED: --execution must be >= 1")
    spec = LANES[L]
    tag = "" if N == 1 else "_e%d" % N
    out = SCR / ("lane_" + L + tag)
    rows = ["| input | sha256 |", "|---|---|"]
    uses = ["", "How you may use each input:", ""]
    for rel, use, what in spec["pins"]:
        p = (SP / rel).resolve()
        win = "SP\\" + rel.replace("/", "\\")
        rows.append("| `%s` | `%s` |" % (win, sha(p.read_bytes())))
        uses.append("- `%s`: %s. %s." % (win, use, what[0].upper() + what[1:]))
    eff = worker_block(M8)
    tpl = (HERE / ("BRIEF_%s.template.md" % L)).read_text(encoding="utf-8")
    body = (tpl.replace("{{SP}}", str(SP)).replace("{{M8}}", str(M8)).replace("{{OUT}}", str(out))
            .replace("{{PINS}}", "\n".join(rows + uses))
            .replace("{{EFFICIENCY}}", eff + "EFFICIENCY-OUT: %s\n" % out))
    if "{{" in body:
        raise SystemExit("REFUSED: an unfilled placeholder remains")
    if N > 1:
        e1 = "execution `%s#e1`." % spec["attempt"]
        if body.count(e1) != 1 or body.count("#e1") != 1:
            raise SystemExit("REFUSED: the template must name %s#e1 exactly once" % spec["attempt"])
        prev = "%s#e%d" % (spec["attempt"], N - 1)
        recs = [json.loads(x) for x in REC.read_text(encoding="utf-8").splitlines() if x.strip()]
        land = [r for r in recs if lands(r) and prev in (r.get("execution_id"), r.get("amends_execution_id"))]
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
    msg = MESSAGE.format(ledger=str(LEDGER), brief=str(brief), sha=bsha, work=spec.get("work", WORK),
                         efficiency=eff, out=str(out))
    mfile = SCR / ("launch_message_%s%s.txt" % (L, tag))
    write_once(mfile, msg.encode("utf-8"))
    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONUTF8="1")
    run = lambda *a: subprocess.run([sys.executable, "-B", *a], cwd=str(SP), capture_output=True, text=True,  # noqa: E731
                                    encoding="utf-8", env=env)
    pc = run("campaign/_brief_pin_check.py", "--brief", str(brief))
    lm = run("campaign/_launch_message_check.py", "--book", "1Cor", "--message", str(mfile))
    print(json.dumps({"lane": L, "attempt": spec["attempt"], "execution": N, "brief": str(brief), "brief_sha256": bsha,
                      "pins": len(spec["pins"]), "message": str(mfile), "message_sha256": sha(mfile.read_bytes()),
                      "brief_pin_check": json.loads(pc.stdout)["verdict"],
                      "launch_message_check": json.loads(lm.stdout)["verdict"],
                      "launch_message_gaps": json.loads(lm.stdout)["gaps"]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
