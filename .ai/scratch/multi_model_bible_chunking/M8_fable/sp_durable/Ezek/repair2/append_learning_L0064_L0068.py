#!/usr/bin/env python3
"""OW-14: append this session's orchestration learnings (L-0064 .. L-0068) to the append-only learning log.

No new playbook version is written. OW-14 puts a new version at BOOK CLOSE, and Ezekiel did not close - it is held at
the gate. Writing ORCHESTRATION_PLAYBOOK.v4.md now would date the method to a close that did not happen.
"""
import hashlib
import json
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
LOG = M8 / "orchestration_learning_log.v1.jsonl"
D = "2026-09-21"

rows = [
    {"id": "L-0064", "stage": "launch", "element": "failure_diagnosis",
     "observation": ("Two blind audit lanes were refused at launch (HTTP 429, out of usage credits, claude-fable-5-1) "
                     "with the five-hour window measured at 95 percent. The window was the first true, measurable "
                     "thing found, so it was adopted as the cause; the lanes were relaunched after it reset to 6 "
                     "percent and were refused identically. Four dispatches produced no diagnosis. The fifth was "
                     "made deliberately minimal - one line, no brief, no file read, every tool forbidden, reply OK - "
                     "and its identical refusal eliminated brief size, pinned-input cost, context, tool budget and "
                     "both usage windows in a single dispatch."),
     "recommendation": ("Before retrying a launch whose failure cause is INFERRED, spend the smallest dispatch that "
                        "DISCRIMINATES between the candidate causes rather than the retry that can only confirm one. "
                        "A one-line no-tool probe costs less than any retry of the real work and refuses in seconds. "
                        "Standing rule for this campaign: probe Fable before ordering a Fable lane."),
     "verdict": "ADOPTED", "metric": "5 dispatches to reach the diagnosis; 1 would have sufficed",
     "evidence_refs": ["E-48", "E-49", "ezek_close_audit_attempt_receipts.jsonl"]},

    {"id": "L-0065", "stage": "close", "element": "scope_definition",
     "observation": ("An owner decision packet stated that a Fable-gated grade was the only thing between Ezekiel and "
                     "closure and that every non-Fable item was finished. Each item named was individually verified; "
                     "the SET was invented from the phase's task list. Reading the tool that actually closed "
                     "Lamentations showed four outstanding passes - the #e16 application, an OPUS-authored postcheck "
                     "that was never Fable-blocked at all, the Fable stage-1 transcript audits and the Fable OW-6 "
                     "final check - plus no assembled corpus and no close tool for the book."),
     "recommendation": ("Measure completeness against the mechanism that enforces it, never against the task list: "
                        "before any near-completion claim, enumerate the close tool's own assertions and the "
                        "directory each requires, from its bytes. An owner-facing near-completion claim must cite "
                        "where its definition of complete came from, so a false premise cannot be smuggled into a "
                        "decision the owner then makes on it."),
     "verdict": "ADOPTED", "metric": "1 of 5 outstanding passes identified before reading the gate",
     "evidence_refs": ["E-50", "EZEK_CLOSE_GATE_OWNER_DECISION.v2.md"]},

    {"id": "L-0066", "stage": "review_launch", "element": "brief_generation",
     "observation": ("Both blind lanes' briefs were emitted from ONE retained generator with the pin digests computed "
                     "from disk at generation time. The two 12,139-byte briefs differ on exactly four lines - the "
                     "lane letter twice and the lane's own two output paths - proved by a line-level diff recorded as "
                     "evidence rather than asserted, and the pin table cannot go stale because a stale table cannot "
                     "pass the pin check it is generated against."),
     "recommendation": ("Treat blindness as a BYTE property, not an intention: generate every lane of a blind set "
                        "from one text, then record the line-level diff as the evidence that the lanes hold the same "
                        "rules. A rule that differs by a word between lanes turns a disagreement into an artefact of "
                        "the briefs."),
     "verdict": "ADOPTED", "metric": "4 differing lines; pins MATCH 21 of 21, zero drift, both briefs",
     "evidence_refs": ["ezek_close_audit_prelaunch.v1.json", "gen_close_audit_brief.py"]},

    {"id": "L-0067", "stage": "prelaunch", "element": "control_applicability",
     "observation": ("The checkpoint's own next_job said to run check_brief_vs_suite.py to PASS. It FAILED, because it "
                     "is an AUTHOR-brief control that demands a duty for each of the 11 row-validator suite members, "
                     "and an audit lane writes no rows: 1 member out of scope, 10 duties missing. Reporting the FAIL "
                     "as a PASS would have been a half-truth; skipping it silently would have been another."),
     "recommendation": ("Record an inapplicable control as a THIRD outcome - not a pass, not a skip - with the "
                        "verdict it actually returned, the reason it does not apply, and what would make it apply. "
                        "An inapplicable control is evidence about the artifact's kind, and a checklist inherited "
                        "from a previous phase can name the wrong control for the current artifact."),
     "verdict": "ADOPTED", "metric": "1 control recorded as check_NOT_applicable with its FAIL verdict retained",
     "evidence_refs": ["ezek_close_audit_prelaunch.v1.json", "OW-18"]},

    {"id": "L-0068", "stage": "close", "element": "governance_floor_dependency",
     "observation": ("The Fable dependency is COMPILED INTO the close tool, which asserts the model name and the "
                     "fit_to_close verdict (sp_durable/Lam/_close_book.py lines 58, 60, 61, 88). When the model "
                     "became unreachable the pipeline therefore REFUSED TO CLOSE rather than closing at a lower "
                     "standard. No silent downgrade was possible, and the orchestrator - the party the floor exists "
                     "to check - could not grant itself an exception without visibly rewriting an assertion whose "
                     "stated purpose is to prevent exactly that."),
     "recommendation": ("Keep the failure mode: a floor should refuse rather than degrade, and the assertion belongs "
                        "in the tool, not in the prompt. What it additionally needs is a fallback grader DECLARED IN "
                        "ADVANCE by the owner, with its downgrade stated in the completion receipt's own bytes - so "
                        "the substitution is a recorded owner decision rather than an improvisation at the gate."),
     "verdict": "PROPOSED - the fallback grader is an owner decision, not adopted here",
     "metric": "4 code assertions held; 0 gates weakened",
     "evidence_refs": ["E-48", "E-49", "OW-6", "OW-13", "EZEK_CLOSE_GATE_OWNER_DECISION.v2.md"]},
]

pre = LOG.read_bytes()
have = {json.loads(l)["id"] for l in pre.decode("utf-8").splitlines() if l.strip()}
new = [r for r in rows if r["id"] not in have]
with LOG.open("a", encoding="utf-8", newline="\n") as fh:
    for r in new:
        fh.write(json.dumps({"schema": "m8_orchestration_learning.v1", "date": D, "book": "Ezek", **r,
                             "supersedes": None}, ensure_ascii=False) + "\n")
if not LOG.read_bytes().startswith(pre):
    raise SystemExit("INTEGRITY FAILURE: the learning log was not appended to")
print(json.dumps({"appended": [r["id"] for r in new],
                  "total_rows": len([l for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]),
                  "sha256": hashlib.sha256(LOG.read_bytes()).hexdigest(),
                  "playbook_version_written": "NONE - OW-14 puts a new version at book close, and Ezekiel is held"},
                 ensure_ascii=False, indent=1))
