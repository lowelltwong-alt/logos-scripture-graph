#!/usr/bin/env python3
"""Record the member extension, the brief-vs-suite control, the corrected brief, and the in-flight pin mutation.

Plus ledger E-34: a brief written from the orders and never checked against the gate.
"""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
M8 = EZ.parents[1]
HERE = Path(__file__).resolve().parent
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
MD = M8 / "ERROR_PATTERN_LEDGER.v1.md"
JL = M8 / "error_pattern_ledger.v1.jsonl"
NOW = datetime.now(timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()          # noqa: E731

# land the control beside the tools it checks, so it is runnable where it matters
shutil.copy2(HERE / "check_brief_vs_suite.py", EZ / "tools" / "check_brief_vs_suite.py")
E = []


def add(**kw):
    E.append(dict(kw, opened_at=NOW))


add(id="E13-80",
    severity="HIGH",
    headline="THE STRUCTURAL CURE IS BUILT AND IT VALIDATES AGAINST ITS OWN FAILURE CASE: a control that checks "
             "the author brief against the validator suite's OWN member list named exactly the three checks "
             "that regressed, without being told which they were",
    raised_by="orchestrator (claude-opus-5)", status="DONE", blocks_close=False, tier="MEASURED",
    the_control={"file": "Ezek/tools/check_brief_vs_suite.py",
                 "sha256": sha(EZ / "tools" / "check_brief_vs_suite.py"),
                 "what_it_does": ("discovers the suite's member list FROM THE SUITE'S OWN SOURCE, then for each "
                                  "member requires either that the brief carries an explicit duty (matched by "
                                  "phrases pinned to that member) or that the member is DECLARED out of scope "
                                  "with a reason. An unmapped member is a FAILURE, not a pass.")},
    the_validation=("run against the brief as it stood when the wave launched, it returned FAIL on exactly "
                    "citation_sweep, hebrew_normalize_dryrun and register - the three checks that went from "
                    "GREEN to red. It was not told which had regressed; it derived them from the suite."),
    after_the_fix="9 duties present, 1 declared out of scope, VERDICT PASS",
    what_it_cannot_establish=("that a duty as WRITTEN is sufficient - only that the brief speaks to the check "
                              "at all. Stated rather than papered over. It would have caught all three of this "
                              "book's regressions because in each case the brief said nothing whatsoever."),
    brief_now={"file": "Ezek/AUTHOR_WAVE_BRIEF.v1.md", "sha256": sha(EZ / "AUTHOR_WAVE_BRIEF.v1.md"),
               "lines": len((EZ / "AUTHOR_WAVE_BRIEF.v1.md").read_text(encoding="utf-8").splitlines()),
               "added": "section 13, carrying the three omitted duties in full"})

add(id="E13-81",
    severity="MEDIUM",
    headline="I MUTATED A PINNED INPUT WHILE AN AGENT WAS RUNNING AGAINST IT. The remediation agent holds a "
             "brief digest that my own edit made stale, mid-flight.",
    raised_by="orchestrator (claude-opus-5), self-reported", status="CONTAINED", blocks_close=False,
    tier="MEASURED",
    what_happened=("I launched the remediation agent with a brief pinning AUTHOR_WAVE_BRIEF.v1.md at "
                   "a9a4b28d..., then appended section 13 to that same file while the agent was running, "
                   "moving it to 31f58d77.... An agent instructed to STOP on a digest mismatch was handed one."),
    why_it_is_the_OW_11_l_class=("the campaign already carries a lesson about pinned digests going stale "
                                 "before a launch, with a pin-check tool to prevent it. This is the same class "
                                 "AFTER launch, which no tool covers: nothing stopped me editing an artifact "
                                 "an in-flight agent depends on."),
    containment=("I messaged the running agent with the new digest, told it not to stop on the mismatch, and "
                 "stated exactly what changed - an APPENDED section only, no earlier section edited, so "
                 "nothing it had already read was altered. I also asked it to record both digests in its "
                 "sources block rather than quietly accepting the new one."),
    what_i_should_have_done=("edited the brief BEFORE launching, or waited. The edit was not urgent: it "
                             "corrected a document for its next reader, and the agent already had those duties "
                             "in its own remediation brief."),
    for_daniel=("a pinned artifact an in-flight agent depends on is FROZEN for the duration. The in-flight pin "
                "guard should cover the running window, not only the launch."))

add(id="E13-82",
    headline="THE A4 MEMBER NOW READS DOTTED CONTINUATIONS; the full residue is 54 citations on 30 rows and a "
             "remediation batch of 59 items is running",
    raised_by="orchestrator (claude-opus-5)", status="RUNNING", blocks_close=False, tier="MEASURED",
    member={"file": "Ezek/tools/check_refs_mirror.py", "sha256": sha(EZ / "tools" / "check_refs_mirror.py"),
            "selftest": "31/31 (was 28/28)",
            "new_fixtures": ["a dotted continuation of an OSIS list is read as its own citation",
                             "its unmirrored members reach the worklist",
                             "a bare decimal with NO OSIS token earlier in the string is NOT a citation"],
            "predicate": ("a dotted pair counts only where an OSIS token stands EARLIER IN THE SAME STRING, "
                          "which distinguishes a list continuation from a decimal, a version number or a "
                          "figure. The witness prefix of the list's last explicit token governs the "
                          "continuation, so a continuation of an oshb: list is an MT reference - and MT and WEB "
                          "diverge in chs 20-21, which is exactly where this corpus's longest such lists sit."),
            "reading_disclosed": ("DEF-A4-ARGUED clause 1's governing phrase is 'any verse anchor a prose field "
                                  "carries' and clause 2 makes a list one citation per member, so this "
                                  "implements the clause rather than extending it. Routed to the controlling "
                                  "agent regardless (E13-77).")},
    residue_measured={"total": 54, "rows": 30, "in_span": 31, "at_seam": 23,
                      "by_arm": {"dotted_continuation": 39, "osis_token": 13, "colon": 1, "mt_colon": 1},
                      "reading": ("39 are the newly visible class; 15 are citations the author wave's OWN "
                                  "rewrites introduced, which is the class lane 04 anticipated and "
                                  "pre-mirrored three of")},
    remediation_batch={"items": 59, "rows": 33,
                       "classes": {"A4_RESIDUE": 54, "HEBREW_FORM": 4, "TOKEN_MISUSE": 1},
                       "worklist_has_stable_ids": True,
                       "includes_an_error_of_mine": ("P01-009, where my Hebrew repair gave both occurrences of "
                                                     "one word Ezek.5.7's bytes though the second occurrence's "
                                                     "clause attributes it to Ezek.5.10")},
    repairs_already_applied={"register": "96 flags -> 0, GREEN (30 edits, 22 rows), tested against the checker "
                                         "BEFORE applying",
                             "hebrew_normalize": "8 defects -> 0, GREEN (16 runs repaired across two passes)",
                             "single_witness_disclosure": "46 entries across two passes",
                             "citation_sweep": "65 problems -> 5"})

with Q.open("a", encoding="utf-8", newline="\n") as fh:
    for e in E:
        fh.write(json.dumps(e, ensure_ascii=False) + "\n")

# ---- ledger E-34
rows = [json.loads(l) for l in JL.read_text(encoding="utf-8").splitlines() if l.strip()]
assert not any(r.get("id") == "E-34" for r in rows), "E-34 present"
ADD = """
---

## Addendum 2026-09-16 (E-34, session 910cbe15, Ezekiel's author wave) — A BRIEF WRITTEN FROM THE ORDERS AND NEVER CHECKED AGAINST THE GATE: six compliant agents broke three green checks

WHAT HAPPENED. An author brief governing a 427-edit mutation wave was written from the controlling agent's
RULINGS. Six author agents followed it closely and delivered work that validated on every check the brief named.
The corpus's hard status went from GREEN to RED, because three validator members enforce duties the brief never
mentioned:

  * a contract disclosure phrase required verbatim on a whole class of citation - and the brief's six-word
    annotation cap made that phrase impossible to write, so the two rules were in direct contradiction;
  * a register rule barring internal file names and rule labels from row prose - which the brief actively
    instructed agents to violate, by telling them to cite rules by name;
  * a byte-identity rule for quoted source text, with an explicit "never hand-type it, slice it" instruction in
    the toolkit - which the brief never passed on.

THE ASYMMETRY THAT MAKES THIS ITS OWN CLASS. The rulings say WHAT TO REPAIR. The validator suite decides WHAT
CORRECT LOOKS LIKE. They are different documents, written by different parties, and an instruction built from one
of them can be perfectly faithful and still fail. Worse, the agents had no way to discover the gap: they were
given a brief and a worklist, and compliance was exactly the wrong strategy.

WHY "READ THE VALIDATORS TOO" IS NOT THE CURE. That is advice, and the same advice would have been given before
this happened. The cure has to be a control that FAILS.

THE CURE, and it validates against its own failure case. A generated check that:
  1. discovers the gate's member list FROM THE GATE'S OWN SOURCE, not from a list the brief's author maintains;
  2. for each member, requires either an explicit duty in the brief or an EXPLICIT out-of-scope declaration with
     a reason;
  3. treats an UNMAPPED member as a failure rather than a pass.
Run against the brief as it stood at launch, it returned FAIL on exactly the three checks that had regressed,
without being told which those were. That is the test of a control worth keeping: it reproduces the failure it
was built after.

ITS HONEST LIMIT, which belongs in the record: it establishes that the brief SPEAKS TO each check, not that the
duty as written is sufficient. It would have caught all three instances here only because in each case the brief
said nothing whatsoever - a partial or wrong duty would pass it.

GENERALISABLE: any instruction document that governs work which will be measured by an automated gate - a
contributor guide against CI, a code-review checklist against linters, a migration runbook against schema
validation, a style guide against a formatter. Derive the acceptance criteria from the GATE, and check the
instruction against them mechanically before the work starts, not after it fails.

RELATED, same session: E-32 (an artifact built from part of an order) and E-33 (a class measured from part of a
definition). This is the third instance of one shape - **an artifact built from PART of its governing set, where
the part used was the part the author was thinking about** - and the cure in each case was the same: generate the
check from the part that was not used.
"""
E34 = {
    "id": "E-34", "kind": "error_pattern", "date": "2026-09-16",
    "headline": ("a brief written from the orders and never checked against the gate: six compliant agents "
                 "broke three green checks"),
    "severity": "high",
    "severity_basis": ("a 427-edit wave took the corpus from GREEN to RED on hard status; 96 register flags "
                       "from a baseline of zero, 46 citation entries missing a required disclosure, 8 "
                       "byte-identity defects in quoted source text. All repaired before any close, none "
                       "shipped."),
    "the_asymmetry": ("the orders say WHAT TO REPAIR; the gate decides WHAT CORRECT LOOKS LIKE. Different "
                      "documents, different authors. An instruction built from one can be perfectly faithful "
                      "and still fail, and the agents following it have no way to discover the gap - "
                      "compliance is the wrong strategy."),
    "worst_sub_case": ("one omitted duty was not merely missing but CONTRADICTED: the brief capped an "
                       "annotation at six words while the gate required a phrase that did not fit, so a "
                       "compliant agent could not pass"),
    "why_advice_is_not_the_cure": "'read the validators too' is what would have been said beforehand; the cure "
                                  "must be a control that FAILS",
    "cure": ["discover the gate's member list FROM THE GATE'S OWN SOURCE, never from a list the instruction's "
             "author maintains",
             "for each member require an explicit duty in the instruction OR an explicit out-of-scope "
             "declaration with a reason",
             "treat an UNMAPPED member as a failure, not a pass",
             "run it before the work starts"],
    "validated_by": ("run against the brief as it stood at launch it returned FAIL on exactly the three checks "
                     "that had regressed, without being told which - it reproduces the failure it was built "
                     "after"),
    "honest_limit": ("it establishes that the instruction SPEAKS TO each check, not that the duty as written is "
                     "sufficient; a partial or wrong duty would pass it"),
    "generalisable": ("any instruction document governing work measured by an automated gate: a contributor "
                      "guide against CI, a review checklist against linters, a runbook against schema "
                      "validation, a style guide against a formatter"),
    "relation_to_E_32_and_E_33": ("third instance of one shape - an artifact built from PART of its governing "
                                  "set, where the part used was the part the author was thinking about - and "
                                  "the cure each time was to generate the check from the part that was not "
                                  "used"),
    "recorded_by": "orchestrator (claude-opus-5)", "recorded_at": NOW,
}
md_pre, jl_pre = MD.read_bytes(), JL.read_bytes()
t1 = MD.with_suffix(".md.tmpE34")
t1.write_bytes(md_pre + ADD.encode("utf-8"))
t1.replace(MD)
t2 = JL.with_suffix(".jsonl.tmpE34")
t2.write_bytes(jl_pre + (json.dumps(E34, ensure_ascii=False) + "\n").encode("utf-8"))
t2.replace(JL)

print(json.dumps({"appended": [e["id"] for e in E], "ledger_row": "E-34",
                  "queue_rows": len(Q.read_text(encoding="utf-8").strip().splitlines()),
                  "ledger_md_lines": len(MD.read_text(encoding="utf-8").splitlines()),
                  "ledger_rows": len([l for l in JL.read_text(encoding="utf-8").splitlines() if l.strip()]),
                  "control_landed": "Ezek/tools/check_brief_vs_suite.py"}, indent=1))
