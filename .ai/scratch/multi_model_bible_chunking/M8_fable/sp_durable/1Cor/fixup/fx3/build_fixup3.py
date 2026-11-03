#!/usr/bin/env python3
"""Build the FIXUP-3 author briefs and launch messages from the E3 and E4 rulings, the installed sweep's coverage report and the
FIXUP-2 applied rows. Orders are quoted verbatim from the rulings; nothing is restated by hand. Pins are measured here, so the
ledger and every other pinned input must be final before this runs (E-69).
usage: build_fixup3.py W1 [W2 ...]
Writes review/FIXUP3_BRIEF_<part>.md, the message in the scratchpad folder the launch-row tool reads, and a durable copy of it.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BK = HERE.parents[1]
SP = BK.parent
R = BK / "review"
SCR = (r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
       r"\af84b702-d913-4495-8e57-252cf7894c63\scratchpad")
SPW = r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable"
ROWS = BK / "fixup/draft_rows_fixup2_applied.jsonl"
E4 = R / "1cor_controlling_agent_rulings_E4.v1.json"
E3 = R / "1cor_controlling_agent_rulings_E3.v1.json"
E1 = R / "1cor_controlling_agent_rulings_E1.v1.json"
REPORT = R / "cwo_1cor_post_fixup2_cwo0607_report.v1.json"
SWEEP = R / "cwo_sweep_1cor.py"
WPV = BK / "writer_lanes/_validate_writer_part_1cor.py"
CONTRACT_SHA = "4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66"
ALLOWED = ["boundary_rationale", "strongest_rejected_alternative", "device_notes", "observed_substrate_signals", "boundary_evidence_refs"]
EXTRA = {"W2-006": ["literature_type_guess"], "W5-002": ["literature_type_guess"], "W6-007": ["confidence"], "W6-013": ["confidence"], "W6-014": ["confidence"]}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def win(p):
    return "SP\\" + str(Path(p).relative_to(SP)).replace("/", "\\")


e4 = json.loads(E4.read_text(encoding="utf-8"))
e3 = json.loads(E3.read_text(encoding="utf-8"))
e1 = json.loads(E1.read_text(encoding="utf-8"))
rep = json.loads(REPORT.read_text(encoding="utf-8"))
rows = [json.loads(x) for x in ROWS.read_text(encoding="utf-8").splitlines() if x.strip()]
gate = next(r for r in e4["rulings"] if r["id"] == "GATE-E4")
orch = next(o for o in gate["orders"] if o["to"] == "orchestrator")["order"]
AUTHOR_RULES = orch[orch.index("Every author:"):]
COND = e4["gate"]["s2_conditions"]
S301 = next(r for r in e3["rulings"] if r["id"] == "S3-01")
cwos = {c["id"]: c for c in e4["corpus_wide_orders"]}
e1c = {c["id"]: c for c in e1["corpus_wide_orders"]}


def sweep_hits(sec, part):
    return [h for h in rep[sec]["list"] if h["row"].startswith(part + "-")]


def brief(part):
    out = SCR + "\\cor_fx3\\" + part
    n = part
    att = "cor_fixup3_%s_a1" % n
    rows_f = "fixup3_%s_rows.jsonl" % n
    chg_f = "fixup3_%s_changes.json" % n
    pins = [ROWS, E4, E3, E1, REPORT, BK / "book_strategy_1Cor.md", BK / "tools/TOOLKIT.md", BK / "tools/run_validator_suite.py", BK / "tools/ngram7.py",
            BK / "tools/check_tiling.py", SWEEP, WPV, BK / "1Cor_rp.txt", BK / "1Cor_sbl.txt", BK / "1Cor_web_clean.txt", BK / "pmarks_1Cor.json",
            SP / "campaign/grader_models.v1.json", SP.parent / "ERROR_PATTERN_LEDGER.v1.md"]
    tab = "\n".join("| `%s` | `%s` |" % (win(p) if p.is_relative_to(SP) else "SP\\..\\" + p.name, sha(p)) for p in pins)
    t = []
    a = t.append
    a("# FIXUP-3 AUTHOR BRIEF, part %s (execution #e1): 1 Corinthians, ruled row repairs (M8_fable, OW-36 queue)\n" % n)
    a("RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Greek New Testament (the first letter to the Corinthians, in Greek with a public-domain English translation) for a study corpus. You revise a few fields of candidate reading-unit rows under ruled orders. Quotations are short, sliced from public witnesses (Robinson-Pierpont Byzantine text, Unlicense; SBLGNT, CC BY 4.0; World English Bible, public domain), and carry their attribution.\n")
    a("`SP` = `%s`\n" % SPW)
    a("## AUTHORITY (OW-36; it also travels in your launch message)\n")
    a("The owner authorized this Opus orchestration and its subagents for six books: 1 Corinthians, John, Romans, Revelation, Hebrews and Matthew. The owner's answer, verbatim: \"Your six-book queue (Recommended)\". authorization_ref `lowell_chat_2026-10-14_m8_opus_orchestration_six_book_queue`; verify in `SP\\..\\ERROR_PATTERN_LEDGER.v1.md` lines 3412-3434 only. You run on claude-opus-5-5 as a recorded grader_fallback (OW-25). You read files under the worktree and write only under your OUT directory; the orchestrator lands and applies your deliverable. You never run git, never write a receipt and never touch the registry.\n")
    a("## E-19: the two binding lines\n")
    a("**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `%s` already exists. Write your deliverables directly to `%s\\%s` and `%s\\%s`. Do not test for the directory, list it or glob it, and write nothing to any other directory. A shell wildcard is a glob. Private scratch goes in `%s\\work\\`, created with os.makedirs(exist_ok=True) and never tested first.\n" % (out, out, rows_f, out, chg_f, out))
    a("**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. No listing, no glob, no recursive search. State in your final message that you ran no listing and no glob.\n")
    a("**FORBIDDEN:** any path under `.ai\\scratch\\multi_model_bible_chunking\\` belonging to `M1_cursor`, `M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or `comparison\\`; every other book's directory under SP; every other part's fix-up OUT; the writers', the reviewers' and the controlling agent's OUT directories, receipts, final messages and evidence notes; every `*_attempt_receipts.jsonl`; transcripts; any file not named in this brief. Nothing from another book passes as 1 Corinthians' (E-65).\n")
    a("**Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run `python -B`. Never run any tool not marked RUN below. Never pass `--write`. Never edit any file under the worktree. Put any script that holds a regular expression or a backslash in a file written whole, never through a shell heredoc or `python -c`.\n")
    a("## Your role\n")
    a("You are the FIXUP-3 AUTHOR for part %s. Attempt `%s`, execution `%s#e1`. You authored none of the rows, the reviews or the rulings. The controlling agent (execution cor_controlling_rulings_r4_a1#e1) ruled on the primary reviews; its orders to your part are quoted verbatim below. You carry out exactly those orders and nothing else changes. You do not adjudicate a divided reading, select a textual reading or tradition, settle a contested interpretation, move any seam or raise any confidence.\n" % (n, att, att))
    a("Rules for every author (verbatim from GATE-E4): %s\n" % AUTHOR_RULES)
    a("Unlike earlier fix-ups, many orders here ask you to reword, so no expected value is given. You author the words, under the order, from the witness bytes. Where an order gives an exact span or an exact phrase, use it exactly.\n")
    a("## PINNED INPUTS\n")
    a("These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a hard stop: report it and stop.\n")
    a("| input | sha256 |\n|---|---|\n%s\n" % tab)
    a("How you may use each input:\n")
    a("- `%s`: READ your part's rows in full; other rows only where you check a fact. You change ONLY what the orders license." % win(ROWS))
    a("- `%s`: READ where you check an order's context (your orders are quoted verbatim below)." % win(E4))
    a("- `%s` and `%s`: READ where you check S3-01 or CWO-1COR-01..03 (quoted below)." % (win(E3), win(E1)))
    a("- `%s`: READ where you check a CWO-1COR-05, -06 or -07 hit (your rows' hits are listed below)." % win(REPORT))
    a("- `%s`: READ sections 7 and 8 in full. BINDING. Section 7 is the record REPORTED sentences may name." % win(BK / "book_strategy_1Cor.md"))
    a("- `%s`: READ where you check a suite member's contract. Where it and a tool's code differ, the code is the contract." % win(BK / "tools/TOOLKIT.md"))
    a("- `%s`, `%s`, `%s`: READ by line; each RP and SBL line is `1Cor.C.V<TAB>text`. Slice every new Greek run or WEB quotation from these bytes by script. RP first; SBL only to disclose." % (win(BK / "1Cor_rp.txt"), win(BK / "1Cor_sbl.txt"), win(BK / "1Cor_web_clean.txt")))
    a("- `%s`: READ where an order turns on a pilcrow's verse. A mark is cited at the verse it follows." % win(BK / "pmarks_1Cor.json"))
    a("- `%s`: RUN on a PRIVATE COPY of the rows in your OUT\\work only (it writes its report beside its input). Run no member directly except ngram7.py below." % win(BK / "tools/run_validator_suite.py"))
    a("- `%s`: RUN on your private copy with `--gate 10 --full-ids` (it writes nothing)." % win(BK / "tools/ngram7.py"))
    a("- `%s`: RUN on your private copy with `--range 1Cor.1.1-1Cor.16.24` (it writes nothing)." % win(BK / "tools/check_tiling.py"))
    a("- `%s`: RUN on your private copy with `--out <a file in your OUT\\work>` (it writes only that file)." % win(SWEEP))
    a("- `%s`: RUN on a slice of your private copy holding only your part's rows, with `--part %s --book-index` (it writes nothing)." % (win(WPV), n))
    a("- `SP\\campaign\\grader_models.v1.json`: READ where you check your model role (grader_fallback).")
    a("- `SP\\..\\ERROR_PATTERN_LEDGER.v1.md`: READ lines 3412-3434 only (OW-36, the owner's grant).\n")
    a("## The orders to part %s (quoted from the rulings file, sha256 %s)\n" % (n, sha(E4)))
    for r in e4["rulings"]:
        for o in r.get("orders") or []:
            if o["to"] != "author_fixup:" + n:
                continue
            a("### %s\n" % r["id"])
            a("Decision (verbatim): %s\n" % r.get("decision", ""))
            a("Your order (verbatim): %s\n" % o["order"])
            a("Exact spans (verbatim): %s\n" % json.dumps(o.get("exact_spans") or [], ensure_ascii=False))
    if n == "W4":
        o3 = next(o for o in S301["orders"] if o["to"] == "author_fixup:W4")
        a("### S3-01 (carried from round 3, rulings file sha256 %s)\n" % sha(E3))
        a("Your order (verbatim): %s\n" % o3["order"])
        a("Exact spans (verbatim): %s\n" % json.dumps(o3.get("exact_spans") or [], ensure_ascii=False))
    for cid in ("CWO-1COR-06", "CWO-1COR-07"):
        c = cwos[cid]
        a("### %s (corpus-wide order)\n" % cid)
        a("Predicate (verbatim): `%s`\n" % c.get("predicate", ""))
        a("Fields (verbatim): %s\n" % c.get("fields", ""))
        a("Remedy (verbatim): %s\n" % c.get("remedy", ""))
    h6 = sweep_hits("CWO06", n)
    if h6:
        a("CWO-1COR-06 hits on your rows (MEASURED by the installed sweep on the pinned rows; hand class by the controlling agent):\n")
        for h in h6:
            a("- `%s.%s` at %s, kind %s, range_token %s, class %s, quote `%s`" % (h["row"], h["field"] if h.get("index") is None else "%s[%s]" % (h["field"], h["index"]), h["verse"], h["kind"], h["range_token"], h["hand_class"], h.get("quote", "")))
        a("")
    h7 = sweep_hits("CWO07", n)
    if h7:
        by = {}
        for h in h7:
            by.setdefault(h["row"], []).append(h["verse"])
        a("CWO-1COR-07 unlisted verses on your rows (MEASURED). Rows `W3-005` 10:11 and `W5-009` 14:6 clear through their CWO-1COR-06 elements, as the remedy says.\n")
        for k, v in by.items():
            a("- `%s`: %s" % (k, ", ".join(v)))
        a("")
    h5 = sweep_hits("CWO05", n)
    if h5:
        a("CWO-1COR-05 hits on your rows (MEASURED); these are the classes the controlling round recorded, 0 of them open true. Do not create a new true hit. Where a reword touches one, keep it as a location or a plain statement.\n")
        for h in h5:
            a("- `%s.%s`" % (h["row"], h.get("field")))
        a("")
    for cid in ("CWO-1COR-01", "CWO-1COR-03"):
        c = e1c.get(cid)
        if c:
            a("### %s (standing; your new text must not reopen it)\n" % cid)
            a("Remedy (verbatim): %s\n" % c.get("remedy", ""))
    a("## What you may change (the lander refuses any other difference)\n")
    a("Only the rows and fields an order above names, and for CWO-1COR-06 and -07 the elements the remedies describe. Whatever the order, a row may differ from its pinned value only in: %s." % ", ".join("`%s`" % f for f in ALLOWED))
    ex = {k: v for k, v in EXTRA.items() if k.startswith(n + "-")}
    if ex:
        a("Named exceptions for your part, each only as its order says: %s." % "; ".join("`%s.%s`" % (k, f) for k, v in ex.items() for f in v))
    a("`span`, the tiling, `unit_type`, `decision_id`, `writer_*` and every other field stay byte-identical as JSON values. `confidence` stays except where an order says otherwise; nothing is raised. Within a licensed field, text no order touches stays byte-identical.\n")
    a("If an order cannot be followed as written, or a removal or reword leaves a seam without ground, leave that field at its pinned value and report it under `blocked` with the measured evidence. Do not improvise and do not widen a licence.\n")
    a("## Suite duties your new text must keep (the suite is the mechanical judge)\n")
    a("- placeholder: no unfilled template placeholder (%s, %(x)s, {name}, {0}, {}) in any field of any row.".replace("%s, %(x)s", "%" + "s, %" + "(x)s"))
    a("- Never hand-type Greek: every Greek run you add is sliced by script from the witness bytes, NFC as the witness has it.")
    a("- WEB quotations are sliced from `%s`, in double curly quotes, attributed (the A6-b convention)." % win(BK / "1Cor_web_clean.txt"))
    a("- register rule: this is a scholar-facing record; no staged file names, internal rule labels, ruling ids, row pointers or process talk in row prose.")
    a("- single-witness: keep the literal single-witness disclosure wherever a row already carries it.")
    a("- A mark is cited at the verse it FOLLOWS.")
    a("- A categorical claim (\"no\", \"only\", \"every\") stands only if the thing is absent from BOTH witnesses.")
    a("- 7-gram: add no run of seven words that repeats across rows. Write each row's new sentences for that row: no sentence shared across rows, including between rows of your own part.")
    a("- Refs: the DEF-A4-ARGUED entries, each ROLE token, face qualifier and seam pair in boundary_evidence_refs stay; no element is removed unless an order says so; new elements follow the row's local form.")
    a("- language_zones and cap_sweep are out of scope (no seam moves).\n")
    a("## What the next check measures (GATE-E4's conditions, verbatim)\n")
    for i, c in enumerate(COND, 1):
        a("%d. %s" % (i, c))
    a("")
    a("## How you check your work (in `%s\\work\\`)\n" % out)
    a("1. Copy `%s` byte-identically to `work\\rows_applied.jsonl` and replace your part's changed rows with your revised rows (same order)." % win(ROWS))
    a("2. RUN `run_validator_suite.py work\\rows_applied.jsonl`: hard_status GREEN, every member GREEN, triage_flags 0.")
    a("3. RUN `ngram7.py work\\rows_applied.jsonl --gate 10 --full-ids`: no offending gram.")
    a("4. RUN `check_tiling.py work\\rows_applied.jsonl --range 1Cor.1.1-1Cor.16.24`: GREEN, 437 of 437.")
    a("5. RUN `cwo_sweep_1cor.py work\\rows_applied.jsonl --out work\\cwo.json`: on your rows A 0; CWO-1COR-04 support_use and count_excess 0 (W6 only: the W6-013 false-positive flag may remain, reported as such); CWO-1COR-05 no new hit you cannot class as location or false positive; CWO-1COR-06 only the two false positives may remain (W2-008 7:9, W6-004 15:35); CWO-1COR-07 0 unlisted on your rows.")
    a("6. Write your part's rows to `work\\slice_%s.jsonl` and RUN `_validate_writer_part_1cor.py work\\slice_%s.jsonl --part %s --book-index`: GREEN." % (n, n, n))
    a("7. By a script file, on your rows: every sentence with the whole word REPORTED names a record; condition 10's regular expression has 0 hits; each exact span named in an order is gone or changed as ordered; every field not licensed is equal as a JSON value to the pinned row.\n")
    a("## Deliverables\n")
    a("- `%s\\%s`: one JSON object per line, the FULL revised row for every row you changed (and only those), in the pinned rows' order, every untouched field byte-identical as a JSON value." % (out, rows_f))
    a("- `%s\\%s`:\n" % (out, chg_f))
    a("```\n{\"attempt_id\":\"%s\",\"execution_id\":\"%s#e1\",\"rows_file_sha256\":\"<pinned rows digest>\",\n \"changes\":[{\"row\":\"<id>\",\"field\":\"<field>\",\"order\":\"<ruling id or CWO id>\",\"before\":\"<exact removed span, or empty>\",\"after\":\"<exact new span, or empty>\",\n             \"tier\":\"MEASURED|INFERRED\",\"evidence\":\"<script + input + output>\"}],\n \"blocked\":[{\"order\":\"<ruling id>\",\"why\":\"...\",\"evidence\":\"...\"}],\n \"checks\":{\"suite\":\"<hard_status and members>\",\"ngram7\":\"...\",\"tiling\":\"...\",\"cwo\":\"...\",\"part_validator\":\"...\",\"unlicensed_fields_equal\":true}}\n```\n" % (att, att))
    a("## Budget\n")
    a("Keep to roughly 30 tool calls. Report exactly what you ran and what it returned.\n")
    a("## Efficiency contract\n")
    a("M8-EFFICIENCY-V1\nEFFICIENCY-CONTRACT: %s\\campaign\\REVIEWER_CONTINUATION_CONTRACT.v1.md sha256 %s\nSave each complete bounded review unit and exact next cursor in your authorized OUT; partial output is not acceptance. Preserve the unchanged legacy final deliverable contract.\nEFFICIENCY-OUT: %s\n" % (SPW, CONTRACT_SHA, out))
    a("## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)\n")
    a("Return JSON only:\n")
    a("```\n{\"attempt_id\":\"%s\",\"execution_id\":\"%s#e1\",\n \"sources\":[\"<exact paths you read, with sha256>\"],\n \"outcome\":{\"changed\":[{\"what\":\"<row.field>\",\"why\":\"<ruling id>\"}]},\n \"verification\":[{\"claim\":\"...\",\"how\":\"<tool + argument, or the exact bytes read>\",\"result\":\"confirmed|refuted\"}],\n \"unresolved_uncertainty\":[{\"what\":\"...\",\"why_it_matters\":\"...\"}],\n \"e19_selfreport\":\"ran no listing, no glob, no recursive search, read no transcript; read only the exact paths named\",\n \"rows_sha256\":\"<sha256 of %s>\",\"changes_sha256\":\"<sha256 of %s>\",\n \"limit\":\"accountable work summary; not chain of thought and not independent proof\"}\n```" % (att, att, rows_f, chg_f))
    return "\n".join(t) + "\n", out


TEMPLATE = (R / "primaries/messages/launch_message_CTL_E4.txt").read_text(encoding="utf-8")
for part in sys.argv[1:]:
    text, out = brief(part)
    os.makedirs(out, exist_ok=True)
    bp = R / ("FIXUP3_BRIEF_%s.md" % part)
    bp.write_text(text, encoding="utf-8", newline="\n")
    i, j = TEMPLATE.index(": ruling on"), TEMPLATE.index("Quotations are short")
    m = TEMPLATE[:i] + ": revising a few fields of candidate reading-unit rows under ruled orders. " + TEMPLATE[j:]
    lines = m.split("\n")
    for k, x in enumerate(lines):
        if x.startswith("BRIEF: "):
            lines[k] = "BRIEF: %s\\1Cor\\review\\%s sha256 %s" % (SPW, bp.name, sha(bp))
        elif x.startswith("EFFICIENCY-OUT: "):
            lines[k] = "EFFICIENCY-OUT: " + out
    m = "\n".join(lines)
    d = Path(SCR) / "cor_review_msgs"
    os.makedirs(d, exist_ok=True)
    mp = d / ("launch_message_FX3_%s.txt" % part)
    mp.write_text(m, encoding="utf-8", newline="\n")
    (R / "primaries/messages" / mp.name).write_text(m, encoding="utf-8", newline="\n")
    print(part, "brief", sha(bp)[:12], len(text), "msg", sha(mp)[:12])
