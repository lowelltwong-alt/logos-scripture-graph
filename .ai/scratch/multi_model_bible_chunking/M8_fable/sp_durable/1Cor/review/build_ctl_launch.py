#!/usr/bin/env python3
"""Build a 1 Corinthians controlling execution (playbook v3 section 2: S1 -> controlling #eN) on the landed S1 review.

Ported 2026-10-20 from the Daniel controlling builder (scratch build_ctl_dan.py). Steps:
  1. install the S1 deliverable byte-identical into 1Cor/review/ (its digest must equal the single completion row's
     output for --s1-execution) and append an install row to 1cor_review_attempt_receipts.jsonl (--expect-before);
  2. write the orchestrator's queue 1Cor/review/1cor_controlling_agent_queue_e<Q>.v1.json from --items (a JSON list of
     {"id","proposal","route"}; proposals only, the controlling execution rules). Every S1 finding id must be an item;
  3. write the brief 1Cor/review/CONTROLLING_BRIEF_E<Q>[_e<N>].md and the launch message scratch
     cor_review_msgs/launch_message_CTL_E<Q>[_e<N>].txt (both carry the efficiency worker block), then run
     _brief_pin_check.py and _launch_message_check.py --book 1Cor.
Every SP target is pin-guarded; an existing target with different bytes is REFUSED (E-41, E-44). A relaunch
(--execution N > 1) needs exactly one landing row for #e(N-1) whose outcome opens with a stop reason. --dry-run renders
the queue and brief to scratch dry_ctl/ and writes nothing in SP.

usage: build_ctl_launch.py --items FILE --expect-before SHA [--round Q] [--execution N] [--s1-execution ID] [--dry-run]
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
BK = HERE.parent
SP = BK.parent
sys.path.insert(0, str(BK / "phase0_lanes"))
from build_launch import MESSAGE, LEDGER, STOPS, lands, M8, worker_block  # noqa: E402

REC = HERE / "1cor_review_attempt_receipts.jsonl"
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\af84b702-d913-4495-8e57-252cf7894c63\scratchpad")
S1_NAME = "1cor_writer_wave_spot_review_S1.json"
WORK = "ruling on review findings about candidate reading units (chunk rows) with byte-cited boundary evidence"
sha = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731
env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")

RUN = [
    ("1Cor/review/{queue}", "READ in full. The items you rule on."),
    ("1Cor/review/" + S1_NAME, "READ new_findings, ngram7, flags, confidence and unresolved_uncertainty in full; the "
                               "rest where you check a fact."),
    ("1Cor/review/BRIEF_S1.md", "READ where you check what S1 was asked."),
    ("1Cor/book_strategy_1Cor.md", "READ sections 6, 7, 8 and 11 in full; the rest where you check a fact. BINDING."),
    ("1Cor/strategy_plan_1Cor.json", "READ where you check a fact."),
    ("1Cor/tools/TOOLKIT.md", "READ where you check a tool contract. Where it and a tool's code differ, the code is "
                              "the contract."),
    ("1Cor/writer/draft_rows_combined.jsonl", "READ where you check a fact (the rows S1 reviewed)."),
    ("1Cor/writer/draft_rows_combined.report.json", "READ where you check a fact."),
    ("1Cor/1Cor_rp.txt", "READ where you check bytes (Robinson-Pierpont Byzantine text, the primary witness)."),
    ("1Cor/1Cor_sbl.txt", "READ where you check bytes (SBLGNT, the secondary witness, signs kept)."),
    ("1Cor/1Cor_web_clean.txt", "READ where you check bytes (WEB)."),
    ("1Cor/1cor_device_inventory.json", "READ where you check a device class or key."),
    ("1Cor/pmarks_1Cor.json", "READ where you check a mark."),
    ("1Cor/tools/ngram7.py", "READ; you may RUN it on a private copy in your OUT\\work (it writes nothing)."),
    ("1Cor/tools/run_validator_suite.py", "READ ONLY - NEVER RUN."),
    ("1Cor/tools/check_universals.py", "READ ONLY - NEVER RUN."),
    ("1Cor/tools/check_marks.py", "READ ONLY - NEVER RUN."),
    ("1Cor/tools/cap_sweep.py", "READ ONLY - NEVER RUN."),
    ("1Cor/tools/citation_sweep.py", "READ ONLY - NEVER RUN."),
    ("campaign/grader_models.v1.json", "READ. The OW-25 fallback model and its statement."),
    ("../ERROR_PATTERN_LEDGER.v1.md", "READ lines 3412-3434 only (OW-36, the owner's grant)."),
]


def guard(p):
    rel = str(p.resolve().relative_to(SP)).replace("\\", "/")
    g = subprocess.run([sys.executable, "-B", str(SP / "campaign" / "_inflight_pin_guard.py"), "--book", "1Cor",
                        "--target", rel], capture_output=True, text=True, encoding="utf-8", cwd=str(SP), env=env)
    if '"verdict": "CLEAR"' not in g.stdout:
        raise SystemExit("REFUSED by pin guard on %s: %s" % (rel, g.stdout[-300:]))


def put(p, b):
    guard(p)
    if p.exists():
        if p.read_bytes() != b:
            raise SystemExit("REFUSED: %s exists with different bytes" % p.name)
        return
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_bytes(b)
    os.replace(tmp, p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", required=True)
    ap.add_argument("--expect-before", required=True)
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--execution", type=int, default=1)
    ap.add_argument("--s1-execution", default="cor_writer_wave_spot_review_s1_a1#e1")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    Q, N = a.round, a.execution
    if Q < 1 or N < 1:
        raise SystemExit("REFUSED: --round and --execution must be >= 1")
    tag = "" if N == 1 else "_e%d" % N
    aid = "cor_controlling_rulings_r%d_a1" % Q
    xid = "%s#e%d" % (aid, N)
    out = SCR / ("cor_ctl%d%s" % (Q, tag))
    deliv = out / ("1cor_controlling_agent_rulings_r%d_e%d.v1.json" % (Q, N))
    queue_p = HERE / ("1cor_controlling_agent_queue_e%d.v1.json" % Q)
    brief_p = HERE / ("CONTROLLING_BRIEF_E%d%s.md" % (Q, tag))
    msg_p = SCR / "cor_review_msgs" / ("launch_message_CTL_E%d%s.txt" % (Q, tag))
    if a.dry_run:
        queue_p = SCR / "dry_ctl" / queue_p.name
        brief_p = SCR / "dry_ctl" / brief_p.name
        queue_p.parent.mkdir(parents=True, exist_ok=True)

    # 1. install S1 by receipt
    s1_dst = HERE / S1_NAME
    before = REC.read_bytes()
    if sha(before) != a.expect_before:
        raise SystemExit("REFUSED: review receipts are at %s, not --expect-before" % sha(before)[:12])
    if b"\r" in before:
        raise SystemExit("REFUSED: CR bytes in the review receipts")
    old = [json.loads(x) for x in before.decode("utf-8").splitlines() if x.strip()]
    done = [r for r in old if r.get("record_kind") == "completion" and r.get("amends_execution_id") == a.s1_execution]
    if len(done) != 1 or len(done[0].get("outputs") or []) != 1:
        raise SystemExit("REFUSED: need exactly one completion row with one output for %s" % a.s1_execution)
    src = Path(done[0]["outputs"][0]["path"])
    s1sha = done[0]["outputs"][0]["sha256"]
    if sha(src.read_bytes()) != s1sha:
        raise SystemExit("REFUSED: the scratch S1 deliverable is not at the completion row's digest")
    installed = any(r.get("record_kind") == "install" and r.get("output_sha256") == s1sha for r in old)
    if not installed and not a.dry_run:
        put(s1_dst, src.read_bytes())
        guard(REC)
        row = {"schema": "m8_attempt_receipt.v1", "record_kind": "install", "book": "1Cor",
               "attempt_id": a.s1_execution.split("#")[0], "installs_execution_id": a.s1_execution,
               "source": str(src), "installed_path": "sp_durable/1Cor/review/" + S1_NAME, "output_sha256": s1sha,
               "method": "byte-identical copy by 1Cor/review/build_ctl_launch.py; pin guard CLEAR",
               "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        lock = REC.with_name(REC.name + ".lock")
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        try:
            if REC.read_bytes() != before:
                raise SystemExit("REFUSED: receipts changed under the lock")
            tmp = REC.with_name(REC.name + ".tmp_append")
            tmp.write_bytes(before + (json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8"))
            os.replace(tmp, REC)
        finally:
            os.close(fd)
            os.remove(lock)
    s1_bytes = s1_dst.read_bytes() if (installed or not a.dry_run) else src.read_bytes()
    if sha(s1_bytes) != s1sha:
        raise SystemExit("REFUSED: the installed S1 deliverable is not at the completion row's digest")
    s1 = json.loads(s1_bytes.decode("utf-8"))
    F = {f["id"]: f for f in s1.get("new_findings") or []}

    # 2. the queue
    items = json.loads(Path(a.items).read_text(encoding="utf-8"))
    ids = [i["id"] for i in items]
    if len(set(ids)) != len(ids) or any(set(i) != {"id", "proposal", "route"} for i in items):
        raise SystemExit("REFUSED: items must be unique {id, proposal, route} objects")
    missing = sorted(set(F) - set(ids))
    if missing:
        raise SystemExit("REFUSED: S1 findings without a queue item: %s" % ", ".join(missing))
    sev = {}
    for f in F.values():
        sev[f.get("severity")] = sev.get(f.get("severity"), 0) + 1
    queue = {"schema": "m8_controlling_queue.v1", "book": "1Cor", "for_execution": xid,
             "status": "PROPOSALS by the orchestrator (claude-opus-5-5, OW-25); the controlling execution rules on "
                       "each id",
             "s1_deliverable": {"path": "sp_durable/1Cor/review/" + S1_NAME, "sha256": s1sha,
                                "execution": a.s1_execution, "verdict": s1.get("verdict")},
             "rows_under_review": s1.get("rows_file_reviewed"),
             "measured_context": {"s1_findings_by_severity": sev, "books_closed": "27/66 (Daniel closed; 1 "
                                  "Corinthians open, the first book of the OW-36 queue)"},
             "items": [dict(i, **({"s1_finding": F[i["id"]]} if i["id"] in F else {})) for i in items]}
    qbytes = (json.dumps(queue, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    if a.dry_run:
        queue_p.write_bytes(qbytes)
    else:
        put(queue_p, qbytes)

    # 3. brief + message
    run = [(r.format(queue=queue_p.name), u) for r, u in RUN]
    if a.dry_run:
        pins = {r: sha(qbytes if "{queue}" in r0 else s1_bytes if r.endswith(S1_NAME) else (SP / r).read_bytes())
                for (r, _), (r0, _) in zip(run, RUN)}
    else:
        pins = {r: sha((SP / r).read_bytes()) for r, _ in run}
    win = lambda r: "SP\\" + r.replace("/", "\\")  # noqa: E731
    table = "\n".join("| `%s` | `%s` |" % (win(r), d) for r, d in pins.items())
    uses = "\n".join("- `%s`: %s" % (win(r), u) for r, u in run)
    eff = worker_block(M8)
    sev_s = ", ".join("%d %s" % (sev[k], k) for k in sorted(sev, key=str))
    ordinal = ("first execution" if N == 1 else "execution %d. This is a relaunch: #e%d landed no deliverable, so "
               "OUT starts empty and nothing of #e%d's is yours to use" % (N, N - 1, N - 1))
    if N > 1:
        recs = [json.loads(x) for x in REC.read_text(encoding="utf-8").splitlines() if x.strip()]
        prev = "%s#e%d" % (aid, N - 1)
        land = [r for r in recs if lands(r) and prev in (r.get("execution_id"), r.get("amends_execution_id"))]
        if len(land) != 1 or not any(str(land[0].get("outcome") or "").startswith(k + " ") for k in STOPS):
            raise SystemExit("REFUSED: %s needs exactly one landing row whose outcome opens with a stop reason" % prev)
    pyenv = "always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run `python -B`"
    brief = f"""# CONTROLLING-AGENT RULINGS (round {Q}, execution #e{N}): 1 Corinthians, S1's findings, the tool fixes and the fix-up wave's scope (M8_fable, OW-36 queue)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Greek New Testament (the first letter to the Corinthians, in Greek with a public-domain English translation) for a study corpus. You read the Robinson-Pierpont Byzantine text (primary), SBLGNT (secondary) and the World English Bible, verify quotations byte-for-byte, and rule on proposed reading-unit boundaries and on review findings. The material is ancient scripture and its translation; the task is textual and literary review.

`SP` = `{SP}`

## AUTHORITY (OW-36; it also travels in your launch message)

The owner authorized this Opus orchestration and its subagents for six books: 1 Corinthians, John, Romans,
Revelation, Hebrews and Matthew. The owner's answer, verbatim: "Your six-book queue (Recommended)". authorization_ref
`lowell_chat_2026-10-14_m8_opus_orchestration_six_book_queue`; verify in `SP\\..\\ERROR_PATTERN_LEDGER.v1.md` lines
3412-3434 only. You run on claude-opus-5-5 in the controlling agent's (Fable's) role, as a recorded grader_fallback
(OW-25): a recorded downgrade, not an equivalence. Your rulings go to Fable's end-of-campaign review (OW-28). You read
files under the worktree and write only under your OUT directory; the orchestrator lands your deliverable. You never run
git, never write a receipt and never touch the registry.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `{out}` already exists. Write your deliverable directly to
`{deliv}`. **Never run any existence check, listing, glob or recursive search against it or any other directory.** A
shell wildcard is a glob. Private scratch goes in `{out}\\work\\`, created with os.makedirs(exist_ok=True) and never
tested first.

**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. No listing, no glob,
no recursive search. State in your final message that you ran no listing and no glob.

**FORBIDDEN:** any path under `.ai\\scratch\\multi_model_bible_chunking\\` belonging to `M1_cursor`,
`M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or
`comparison\\`; every other book's directory under SP; the writers' and S1's OUT directories, receipts, final messages
and evidence notes; every `*_attempt_receipts.jsonl`; transcripts. Nothing from another book passes as 1 Corinthians'
(E-65).

**Running Python:** {pyenv}. Never run any tool not marked RUN below. Never pass `--write`. Never edit any file under the
worktree.

## Your role

You are the CONTROLLING AGENT for 1 Corinthians. Attempt `{aid}`, execution `{xid}` ({ordinal}). You authored none of
the rows, the strategy, the tools or the S1 review. S1, a distinct checker, landed on the combined writer draft:
verdict {s1.get("verdict")}, {len(F)} findings ({sev_s}). The orchestrator's queue proposes a ruling for each finding,
for S1's open questions and for the gate. The orchestrator proposes; you rule. You may adopt, change or reject any
proposal, and you may add an id only for a defect you find in the bytes.

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a
hard stop: report it and stop.

| input | sha256 |
|---|---|
{table}

How you may use each input:

{uses}

## What to rule on

**Every** item in the queue: {", ".join(ids)}. One ruling per id; no id may be missing.

- Nothing here may weaken a HARD gate without saying so in words. A tool change that narrows what a HARD member
  counts must state why it cannot hide a real defect, and name the fixture that proves it.
- A class ruling that orders a sweep names its predicate and its fields exactly, in corpus_wide_orders, so the
  orchestrator runs it as its own sweep with its own coverage report (E-18).
- A fix-up order names the part, the rows and the exact spans or fields; the fix-up author changes nothing else.
- No ruling adjudicates a divided reading, selects a textual reading or source tradition, or settles a contested
  interpretation (for example the 14:34-35 placement or the slogan attributions) in a boundary. Where a finding touches
  one, say so and route it to Fable's end review.
- Readiness wording you prescribe for S2 takes an ACCEPT form, with no red, reject*, blocker*, refut*, unfit or 'not
  fit'.
- **GATE-E{Q}:** set `tool_fixes_before_fixup`, `fixup_may_launch`, `fixup_parts`, `s2_conditions` and
  `primaries_may_launch`.

## Deliverable: `{deliv}`

```
{{"attempt_id":"{aid}","execution_id":"{xid}",
 "inputs_ruled_on":[{{"path":"SP\\\\...","sha256":"<digest of the bytes you read>"}}],
 "rulings":[{{"id":"<queue id>","ruling":"ratify|ratify_with_changes|reverse|adopt|reject|close|keep_open|defer|amend|hold|cut","decision":"...",
             "reason":"...","evidence":["<exact path + ref or bytes>"],
             "orders":[{{"to":"orchestrator|tool_fix|author_fixup:W<n>|s2|primaries|fable_end_review","order":"...","exact_spans":["..."]}}]}}],
 "corpus_wide_orders":[{{"id":"CWO-1COR-NN","predicate":"<exact>","fields":"<exact>","remedy":"...","coverage_report":"..."}}],
 "gate":{{"tool_fixes_before_fixup":["..."],"fixup_may_launch":false,"fixup_parts":["W<n>"],"s2_conditions":["..."],"primaries_may_launch":false}},
 "unresolved_uncertainty":[{{"what":"...","why_it_matters":"..."}}]}}
```

## Budget

Rule from the queue, S1's deliverable and the strategy; open rows, bytes and tools only where you check a fact. Keep to
roughly 40 tool calls. Report exactly what you ran and what it returned.

## Efficiency contract

{eff}EFFICIENCY-OUT: {out}

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{{"attempt_id":"{aid}","execution_id":"{xid}",
 "sources":["<exact paths you read>"],
 "outcome":{{"changed":[{{"what":"<your deliverable>","why":"..."}}]}},
 "verification":[{{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}}],
 "unresolved_uncertainty":[{{"what":"...","why_it_matters":"..."}}],
 "e19_selfreport":"ran no listing, no glob, no recursive search, read no transcript; read only the exact paths named",
 "ruling_count":0,"deferred":[],"deliverable_sha256":"<sha256 of the deliverable bytes>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}}
```
"""
    if xid not in brief or brief.count("#e%d" % N) < 1:
        raise SystemExit("REFUSED: the brief does not name %s" % xid)
    bb = brief.encode("utf-8")
    if a.dry_run:
        brief_p.write_bytes(bb)
        print(json.dumps({"dry_run": str(brief_p.parent), "queue_sha256": sha(qbytes)[:12], "brief_sha256": sha(bb)[:12],
                          "items": len(items), "s1_findings": len(F), "pins": len(pins)}, ensure_ascii=False))
        return 0
    put(brief_p, bb)
    msg = MESSAGE.format(ledger=str(LEDGER), brief=str(brief_p), sha=sha(bb), work=WORK, efficiency=eff, out=str(out))
    msg_p.parent.mkdir(parents=True, exist_ok=True)
    if msg_p.exists() and msg_p.read_bytes() != msg.encode("utf-8"):
        raise SystemExit("REFUSED: %s exists and differs" % msg_p.name)
    msg_p.write_bytes(msg.encode("utf-8"))
    (out / "work").mkdir(parents=True, exist_ok=True)
    run_ = lambda *x: subprocess.run([sys.executable, "-B", *x], cwd=str(SP), capture_output=True, text=True,  # noqa: E731
                                     encoding="utf-8", env=env)
    pc = run_("campaign/_brief_pin_check.py", "--brief", str(brief_p))
    lm = run_("campaign/_launch_message_check.py", "--book", "1Cor", "--message", str(msg_p))
    print(json.dumps({"execution": xid, "s1_installed": sha(s1_dst.read_bytes())[:12], "receipts": sha(REC.read_bytes())[:12],
                      "queue": sha(queue_p.read_bytes())[:12], "items": len(items), "brief": brief_p.name,
                      "brief_sha256": sha(bb), "message": str(msg_p), "message_sha256": sha(msg_p.read_bytes()),
                      "pins": len(pins), "brief_pin_check": json.loads(pc.stdout)["verdict"],
                      "launch_message_check": json.loads(lm.stdout)["verdict"],
                      "launch_message_gaps": json.loads(lm.stdout)["gaps"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
