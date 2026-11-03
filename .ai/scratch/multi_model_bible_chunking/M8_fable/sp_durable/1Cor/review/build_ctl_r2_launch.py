#!/usr/bin/env python3
"""Build a 1 Corinthians controlling execution of round 2 or later on a landed, installed distinct check S(N).

Round-aware since 2026-10-20 (ROUND_INPUTS; round 2 output byte-identical, cor_ctl3/regress_r2.py). Ported 2026-10-20 from build_ctl_launch.py (round 1, on S1), playbook v3 section 2: FIXUP-1 -> S2 -> controlling #eN ->
FIXUP-2 -> S3. Differences from round 1: the review being ruled on must ALREADY be installed by receipt (an install row
for --review-execution whose output digest equals both its single completion row's output and the installed file's
bytes); the queue must carry every new finding of that review plus GATE-E<Q>; the brief pins the prior rulings, the
applied rows under review and the licence maps (in the S2 receipt extract). Steps:
  1. write the orchestrator's queue 1Cor/review/1cor_controlling_agent_queue_e<Q>.v1.json from --items (a JSON list of
     {"id","proposal","route"}; proposals only, the controlling execution rules);
  2. write the brief 1Cor/review/CONTROLLING_BRIEF_E<Q>[_e<N>].md and the launch message scratch
     cor_review_msgs/launch_message_CTL_E<Q>[_e<N>].txt (both carry the efficiency worker block), then run
     _brief_pin_check.py and _launch_message_check.py --book 1Cor.
Every SP target is pin-guarded before it is written; an existing target with different bytes is REFUSED (E-41, E-44).
A relaunch (--execution N > 1) needs exactly one landing row for #e(N-1) whose outcome opens with a stop reason.
--dry-run renders the queue and brief to scratch dry_ctl/ and writes nothing in SP.

usage: build_ctl_r2_launch.py --items FILE --expect-before SHA [--round Q] [--execution N]
       [--review-execution ID] [--review-name FILE] [--review-brief FILE] [--prior-rulings FILE] [--dry-run]
"""
import argparse
import hashlib
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
sys.path.insert(0, str(BK / "phase0_lanes"))
from build_launch import MESSAGE, LEDGER, STOPS, lands, M8, worker_block  # noqa: E402

REC = HERE / "1cor_review_attempt_receipts.jsonl"
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\af84b702-d913-4495-8e57-252cf7894c63\scratchpad")
WORK = "ruling on review findings about candidate reading units (chunk rows) with byte-cited boundary evidence"
sha = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731
env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")

RUN = [
    ("1Cor/review/{queue}", "READ in full. The items you rule on."),
    ("1Cor/review/{review}", "READ changes_required, new_findings, ruled_findings, carried_items, "
                             "unresolved_uncertainty_bearing and unresolved_uncertainty in full; the rest where you "
                             "check a fact."),
    ("1Cor/review/{review_brief}", "READ where you check what the review was asked."),
    ("1Cor/review/{prior}", "READ in full. The standing rulings, corpus-wide orders and gate; they stand unless you "
                            "amend them by id in words."),
    ("1Cor/review/tool_fixes/{extract}", "READ where you check a licence (the {fxp} allowed-change "
                                         "maps are inlined in its launch rows)."),
    ("1Cor/fixup/draft_rows_{fx}_applied.jsonl", "READ where you check a fact (the rows under review)."),
    ("1Cor/fixup/draft_rows_{fx}_applied.manifest.json", "READ where you check a fact."),
    ("1Cor/review/{report}", "READ where you check a CWO classification."),
    ("1Cor/review/cwo_sweep_1cor.py", "READ; you may RUN it on a private copy with --out under your OUT\\work only "
                                      "(it writes --out and nothing else)."),
    ("1Cor/book_strategy_1Cor.md", "READ sections 6, 7, 8 and 11 in full; the rest where you check a fact. BINDING."),
    ("1Cor/strategy_plan_1Cor.json", "READ where you check a fact."),
    ("1Cor/tools/TOOLKIT.md", "READ where you check a tool contract. Where it and a tool's code differ, the code is "
                              "the contract."),
    ("1Cor/1Cor_rp.txt", "READ where you check bytes (Robinson-Pierpont Byzantine text, the primary witness)."),
    ("1Cor/1Cor_sbl.txt", "READ where you check bytes (SBLGNT, the secondary witness, signs kept)."),
    ("1Cor/1Cor_web_clean.txt", "READ where you check bytes (WEB)."),
    ("1Cor/1cor_device_inventory.json", "READ where you check a device class or key."),
    ("1Cor/pmarks_1Cor.json", "READ where you check a mark."),
    ("1Cor/tools/ngram7.py", "READ; you may RUN it on a private copy in your OUT\\work (it writes nothing)."),
    ("1Cor/tools/run_validator_suite.py", "READ ONLY - NEVER RUN."),
    ("campaign/grader_models.v1.json", "READ. The OW-25 fallback model and its statement."),
    ("../ERROR_PATTERN_LEDGER.v1.md", "READ lines 3412-3434 only (OW-36, the owner's grant)."),
]
# Per round: the receipt extract, the applied rows under review and the CWO report on them (round 2 = the FIXUP-1 rows,
# round 3 = the FIXUP-2 rows). Round 3 and later also pin every earlier round's rulings (they stand unless amended).
ROUND_INPUTS = {2: dict(extract="s2_receipt_extract.v1.json", fx="fixup1",
                        report="cwo_1cor_post_fixup1_report.v1.json"),
                3: dict(extract="s3_receipt_extract.v1.json", fx="fixup2",
                        report="cwo_1cor_post_fixup2_report.v1.json")}


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
    ap.add_argument("--round", type=int, default=2)
    ap.add_argument("--execution", type=int, default=1)
    ap.add_argument("--review-execution", default="cor_fixup_wave_review_s2_a1#e1")
    ap.add_argument("--review-name", default="1cor_fixup_wave_review_S2.json")
    ap.add_argument("--review-brief", default="BRIEF_S2.md")
    ap.add_argument("--prior-rulings", default="1cor_controlling_agent_rulings_E1.v1.json")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    Q, N = a.round, a.execution
    if Q < 2 or N < 1:
        raise SystemExit("REFUSED: --round must be >= 2 (round 1 is build_ctl_launch.py) and --execution >= 1")
    if Q not in ROUND_INPUTS:
        raise SystemExit("REFUSED: no input map for round %d (add it to ROUND_INPUTS)" % Q)
    for nm in (a.review_name, a.review_brief, a.prior_rulings):
        if Path(nm).name != nm:
            raise SystemExit("REFUSED: %s must be a plain file name in 1Cor/review/" % nm)
    tag = "" if N == 1 else "_e%d" % N
    aid = "cor_controlling_rulings_r%d_a1" % Q
    xid = "%s#e%d" % (aid, N)
    nxt = "S%d" % (Q + 1)
    out = SCR / ("cor_ctl%d%s" % (Q, tag))
    deliv = out / ("1cor_controlling_agent_rulings_r%d_e%d.v1.json" % (Q, N))
    queue_p = HERE / ("1cor_controlling_agent_queue_e%d.v1.json" % Q)
    brief_p = HERE / ("CONTROLLING_BRIEF_E%d%s.md" % (Q, tag))
    msg_p = SCR / "cor_review_msgs" / ("launch_message_CTL_E%d%s.txt" % (Q, tag))
    if a.dry_run:
        queue_p = SCR / "dry_ctl" / queue_p.name
        brief_p = SCR / "dry_ctl" / brief_p.name
        queue_p.parent.mkdir(parents=True, exist_ok=True)

    # 0. the review must be installed by receipt
    before = REC.read_bytes()
    if sha(before) != a.expect_before:
        raise SystemExit("REFUSED: review receipts are at %s, not --expect-before" % sha(before)[:12])
    if b"\r" in before:
        raise SystemExit("REFUSED: CR bytes in the review receipts")
    old = [json.loads(x) for x in before.decode("utf-8").splitlines() if x.strip()]
    done = [r for r in old if r.get("record_kind") == "completion" and r.get("amends_execution_id") == a.review_execution]
    if len(done) != 1 or len(done[0].get("outputs") or []) != 1:
        raise SystemExit("REFUSED: need exactly one completion row with one output for %s" % a.review_execution)
    rsha = done[0]["outputs"][0]["sha256"]
    inst = [r for r in old if r.get("record_kind") == "install" and r.get("installs_execution_id") == a.review_execution
            and r.get("output_sha256") == rsha and r.get("installed_path") == "sp_durable/1Cor/review/" + a.review_name]
    if len(inst) != 1:
        raise SystemExit("REFUSED: %s is not installed by receipt as %s" % (a.review_execution, a.review_name))
    rb = (HERE / a.review_name).read_bytes()
    if sha(rb) != rsha:
        raise SystemExit("REFUSED: the installed review is not at its completion row's digest")
    rv = json.loads(rb.decode("utf-8"))
    F = {f["id"]: f for f in rv.get("new_findings") or []}
    prior = json.loads((HERE / a.prior_rulings).read_text(encoding="utf-8"))
    if prior.get("gate", {}).get("primaries_may_launch") is not False:
        raise SystemExit("REFUSED: the prior gate's primaries_may_launch is not false")

    # 1. the queue
    items = json.loads(Path(a.items).read_text(encoding="utf-8"))
    ids = [i["id"] for i in items]
    if len(set(ids)) != len(ids) or any(set(i) != {"id", "proposal", "route"} for i in items):
        raise SystemExit("REFUSED: items must be unique {id, proposal, route} objects")
    missing = sorted(set(F) - set(ids)) + ([] if "GATE-E%d" % Q in ids else ["GATE-E%d" % Q])
    if missing:
        raise SystemExit("REFUSED: queue items missing: %s" % ", ".join(missing))
    sev = {}
    for f in F.values():
        sev[f.get("severity")] = sev.get(f.get("severity"), 0) + 1
    queue = {"schema": "m8_controlling_queue.v1", "book": "1Cor", "for_execution": xid,
             "status": "PROPOSALS by the orchestrator (claude-opus-5-5, OW-25); the controlling execution rules on "
                       "each id",
             "review_deliverable": {"path": "sp_durable/1Cor/review/" + a.review_name, "sha256": rsha,
                                    "execution": a.review_execution, "readiness": rv.get("readiness")},
             "prior_rulings": {"path": "sp_durable/1Cor/review/" + a.prior_rulings,
                               "sha256": sha((HERE / a.prior_rulings).read_bytes())},
             "rows_under_review": rv.get("rows_file_reviewed"),
             "measured_context": {"review_findings_by_severity": sev,
                                  "review_changes_required": len(rv.get("changes_required") or []),
                                  "books_closed": "27/66 (Daniel closed; 1 Corinthians open, the first book of the "
                                                  "OW-36 queue)"},
             "items": [dict(i, **({"review_finding": F[i["id"]]} if i["id"] in F else {})) for i in items]}
    qbytes = (json.dumps(queue, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    if a.dry_run:
        queue_p.write_bytes(qbytes)
    else:
        put(queue_p, qbytes)

    # 2. brief + message
    fmt = dict(queue=queue_p.name, review=a.review_name, review_brief=a.review_brief, prior=a.prior_rulings,
               fxp="FIXUP-%d" % (Q - 1), **ROUND_INPUTS[Q])
    run = [(r.format(**fmt), u.format(**fmt)) for r, u in RUN]
    for k in range(Q - 2, 0, -1):
        run.insert(4, ("1Cor/review/1cor_controlling_agent_rulings_E%d.v1.json" % k,
                       "READ in full. The round-%d rulings; they stand unless a later round or you amend one by id in "
                       "words." % k))
    fxp = fmt["fxp"]
    earlier = "the round-1 rulings" if Q == 2 else "the earlier rounds' rulings"
    stand = ("round-1 rulings in `%s`" % a.prior_rulings if Q == 2 else
             "rulings of rounds 1-%d (`%s` and the earlier rulings pinned below)" % (Q - 1, a.prior_rulings))
    after_ids = "round-1" if Q == 2 else "earlier rounds'"
    std = "round-1" if Q == 2 else "standing"
    rv_name = a.review_name.rsplit("_", 1)[-1].split(".")[0]
    checkers = ("S1's and %s's" % rv_name if Q == 2 else
                ", ".join("S%d's" % k for k in range(1, Q)) + " and %s's" % rv_name)
    if a.dry_run:
        pins = {r: sha(qbytes if r.endswith(queue_p.name) else (SP / r).read_bytes()) for r, _ in run}
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
        prev = "%s#e%d" % (aid, N - 1)
        land = [r for r in old if lands(r) and prev in (r.get("execution_id"), r.get("amends_execution_id"))]
        if len(land) != 1 or not any(str(land[0].get("outcome") or "").startswith(k + " ") for k in STOPS):
            raise SystemExit("REFUSED: %s needs exactly one landing row whose outcome opens with a stop reason" % prev)
    rv_n = a.review_name.rsplit("_", 1)[-1].split(".")[0]
    pyenv = "always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run `python -B`"
    brief = f"""# CONTROLLING-AGENT RULINGS (round {Q}, execution #e{N}): 1 Corinthians, {rv_n}'s required changes, the class rulings and the next fix-up wave's scope (M8_fable, OW-36 queue)

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
`comparison\\`; every other book's directory under SP; the writers', the fix-up authors', {checkers} OUT
directories, receipts, final messages and evidence notes; every `*_attempt_receipts.jsonl`; transcripts. Nothing from
another book passes as 1 Corinthians' (E-65).

**Running Python:** {pyenv}. Never run any tool not marked RUN below. Never pass `--write`. Never edit any file under the
worktree.

## Your role

You are the CONTROLLING AGENT for 1 Corinthians, round {Q}. Attempt `{aid}`, execution `{xid}` ({ordinal}). You authored
none of the rows, the strategy, the tools, {earlier} or the reviews. {rv_n}, a fresh distinct checker, read
the {fxp} applied rows and recorded readiness {rv.get("readiness")}: {len(rv.get("changes_required") or [])} changes
required and {len(F)} new findings ({sev_s}). The orchestrator's queue proposes a ruling for each finding and for the
gate. The orchestrator proposes; you rule. You may adopt, change or reject any proposal, and you may add an id only for a
defect you find in the bytes. The {stand} stand unless you amend one by id, in words.

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
- A class ruling that orders a sweep names its predicate and its fields exactly, in corpus_wide_orders (new ids continue
  after the {after_ids} ids), so the orchestrator runs it as its own sweep with its own coverage report (E-18). A widened
  predicate states what it adds over the {std} predicate and how its false positives are classified.
- A fix-up order names the part, the rows and the exact spans or fields; the fix-up author changes nothing else. Where an
  order needs a field or a ref element outside the {std} licence, the ruling licenses it in words.
- No ruling adjudicates a divided reading, selects a textual reading or source tradition, or settles a contested
  interpretation (for example the 14:34-35 placement or the slogan attributions) in a boundary. Where a finding touches
  one, say so and route it to Fable's end review.
- Readiness wording you prescribe for the next check takes an ACCEPT form, with no red, reject*, blocker*, refut*, unfit
  or 'not fit'.
- **GATE-E{Q}:** set `tool_fixes_before_fixup`, `fixup_may_launch`, `fixup_parts`, `s2_conditions` and
  `primaries_may_launch`. The key `s2_conditions` keeps its round-1 name so the tools that read it still work; in this
  round it holds the conditions the next fresh distinct check, {nxt}, tests on the next applied rows.

## Deliverable: `{deliv}`

```
{{"attempt_id":"{aid}","execution_id":"{xid}",
 "inputs_ruled_on":[{{"path":"SP\\\\...","sha256":"<digest of the bytes you read>"}}],
 "rulings":[{{"id":"<queue id>","ruling":"ratify|ratify_with_changes|reverse|adopt|reject|close|keep_open|defer|amend|hold|cut","decision":"...",
             "reason":"...","evidence":["<exact path + ref or bytes>"],
             "orders":[{{"to":"orchestrator|tool_fix|author_fixup:W<n>|{nxt.lower()}|primaries|fable_end_review","order":"...","exact_spans":["..."]}}]}}],
 "corpus_wide_orders":[{{"id":"CWO-1COR-NN","predicate":"<exact>","fields":"<exact>","remedy":"...","coverage_report":"..."}}],
 "gate":{{"tool_fixes_before_fixup":["..."],"fixup_may_launch":false,"fixup_parts":["W<n>"],"s2_conditions":["..."],"primaries_may_launch":false}},
 "unresolved_uncertainty":[{{"what":"...","why_it_matters":"..."}}]}}
```

## Budget

Rule from the queue, {rv_n}'s deliverable, {earlier} and the strategy; open rows, bytes and tools only where you
check a fact. Keep to roughly 40 tool calls. Report exactly what you ran and what it returned.

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
    if brief.count(xid) < 1:
        raise SystemExit("REFUSED: the brief does not name %s" % xid)
    for bad in ("cor_w\\lane_", "cor_s1\\", "cor_s2\\", "cor_fx1\\", "final_FX1_", "cor_s3_out\\", "cor_fx2\\",
                "cor_tf\\"):
        if bad in brief:
            raise SystemExit("REFUSED: the brief carries %r" % bad)
    bb = brief.encode("utf-8")
    if a.dry_run:
        brief_p.write_bytes(bb)
        print(json.dumps({"dry_run": str(brief_p.parent), "queue_sha256": sha(qbytes)[:12], "brief_sha256": sha(bb)[:12],
                          "items": len(items), "review_findings": len(F), "pins": len(pins)}, ensure_ascii=False))
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
    print(json.dumps({"execution": xid, "receipts": sha(REC.read_bytes())[:12],
                      "queue": sha(queue_p.read_bytes())[:12], "items": len(items), "brief": brief_p.name,
                      "brief_sha256": sha(bb), "message": str(msg_p), "message_sha256": sha(msg_p.read_bytes()),
                      "pins": len(pins), "brief_pin_check": json.loads(pc.stdout)["verdict"],
                      "launch_message_check": json.loads(lm.stdout)["verdict"],
                      "launch_message_gaps": json.loads(lm.stdout)["gaps"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
