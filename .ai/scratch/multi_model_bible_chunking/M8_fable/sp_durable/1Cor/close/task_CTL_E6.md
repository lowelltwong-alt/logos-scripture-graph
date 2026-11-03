RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Greek New Testament (the first letter
to the Corinthians, in Greek with a public-domain English translation) for a study corpus. You read review findings on
proposed reading-unit boundaries and rule on them. The material is ancient scripture and its translation; the task is
textual and literary review.

**Authority.** OW-36 and OW-37 grant this Opus orchestration and its subagents the six-book queue; verify in
`SP\..\ERROR_PATTERN_LEDGER.v1.md` lines 3412-3434 and 3525-3545 only. You run in the controlling agent's (Fable's) role
as a recorded grader_fallback (OW-25): a recorded downgrade, not an equivalence. Your rulings go to Fable's end-of-campaign
review (OW-28).

**Your role.** You are the CONTROLLING AGENT for 1 Corinthians, round 6. You authored none of the rows, the tools, the
earlier rulings or S6's review. S6, a fresh distinct delta check, read the FIXUP-4 applied rows against GATE-E5's
conditions and returned fit_with_changes: six of seven met, condition 3 unmet on one clause. A finding is a candidate
claim. The orchestrator proposes in the queue; you rule. You may adopt, change or reject any proposal, and you may add an
id only for a defect you find in the bytes. The rulings of rounds 1-5 stand unless you amend one by id, in words.

**This round is narrower than any before it.** Rule on the six queue items and on nothing else. Do not reopen a row, a
boundary or a confidence no item touches.

**The question at the centre.** GATE-E5 condition 3 reads, in full: "run_validator_suite.py on the FIXUP-4 applied rows:
hard_status GREEN, no dead member, ngram7 GREEN at gate 10 with no new 7-gram shared across rows from FIXUP-4 text,
register and universals GREEN." The pinned gate-10 run is GREEN. S6 measured, by private means below gate 10, six new
7-grams each shared by two rows, all from text the rulings ordered byte for byte. Whether the clause reaches below gate
10 is a question about what the condition meant. It is yours to answer, in words, with your reason. Neither answer
weakens a HARD gate as long as you state which it is; the gate-10 member itself is not in question.

**Reading rules.** Read the queue whole. Read `1cor_fixup4_review_S6.json` by key only: `new_findings`, `changes_required`,
`conditions`, `unresolved_uncertainty`. Read the rulings at gate, at R5-S5-06 and at R5-S5-11, then where an item points.
Slice rows by a script of your own.

**Testing words.** Where you order words, first apply them to a private copy of the rows and run, on that copy,
`run_validator_suite.py`, `check_tiling.py`, `ngram7.py` and `cwo_sweep_1cor.py`, each with any output under OUT\work
only. Read a tool's header for its arguments first, and never pass an argument to a script whose code shows no parser.
Never pass `--write`. Earlier ordered words failed the register and universals members, so report what each run returned.

**Order form.** Every order that changes bytes uses the form of R5-S5-11: `{"to":"author_fixup:W<n>","order":"...",
"exact_spans":[{"row":"...","field":"...","replace_exactly_once":"...","with":"..."}]}`, so a tool applies it with no
author and no transcription step. A span must occur exactly once in the named field. No quoted Greek byte changes. If an
order prescribes wording for the next check, it takes an ACCEPT form, with no red, reject*, blocker*, refut*, unfit or
'not fit'.

**Limits.** No ruling adjudicates a divided reading, selects a textual reading or source tradition, or settles a contested
interpretation in a boundary; route such a thing to Fable's end review. No new corpus-wide sweep unless a defect in the
bytes demands it; `corpus_wide_orders` may be an empty list.

**Forbidden in addition to the template's list:** the writers', the fix-up authors', S5's, S6's and the primary reviewers'
OUT directories, receipts, final messages and evidence notes; every `*_attempt_receipts.jsonl`.

**GATE-E6.** Set `tool_fixes_before_fixup`, `fixup_may_launch`, `fixup_parts`, `s2_conditions` and `primaries_may_launch`
(false). The key `s2_conditions` keeps its round-1 name so the tools that read it still work. Name, for any clause you
keep or write, the run that decides it.

**Deliverable form.** One JSON object:

```
{"attempt_id":"cor_controlling_rulings_r6_a1","execution_id":"<your execution id>",
 "inputs_ruled_on":[{"path":"SP\\...","sha256":"<digest of the bytes you read>"}],
 "rulings":[{"id":"<queue id>","ruling":"ratify|ratify_with_changes|reverse|adopt|reject|close|keep_open|defer|amend|hold|cut",
             "decision":"...","reason":"...","evidence":["<exact path + ref or bytes>"],
             "orders":[{"to":"orchestrator|tool_fix|author_fixup:W<n>|s7|primaries|fable_end_review","order":"...","exact_spans":[]}]}],
 "corpus_wide_orders":[],
 "gate":{"tool_fixes_before_fixup":[],"fixup_may_launch":false,"fixup_parts":[],"s2_conditions":["..."],"primaries_may_launch":false},
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "deliverables":[],"verification":[]}
```

One ruling per queue id; no id missing.
