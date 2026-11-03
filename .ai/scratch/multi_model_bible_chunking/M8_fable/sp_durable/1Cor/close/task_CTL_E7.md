RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Greek New Testament (the first letter
to the Corinthians, in Greek with a public-domain English translation) for a study corpus. You read review findings on
proposed reading-unit boundaries and rule on them. The material is ancient scripture and its translation; the task is
textual and literary review.

**Authority.** OW-36 and OW-37 grant this Opus orchestration and its subagents the six-book queue; verify in
`SP\..\ERROR_PATTERN_LEDGER.v1.md` lines 3412-3434 and 3525-3545 only. You run in the controlling agent's (Fable's) role
as a recorded grader_fallback (OW-25): a recorded downgrade, not an equivalence. Your rulings go to Fable's end-of-campaign
review (OW-28).

**Your role.** You are the CONTROLLING AGENT for 1 Corinthians, round 7. You authored none of the rows, the tools, the
earlier rulings or the boss audit. The boss read all 70 FIXUP-4 applied rows whole and returned RETURN: 13 conditions MET,
4 NOT_TESTABLE, 67 rows CONFIRM, 3 RETURN. A finding is a candidate claim. The orchestrator proposes in the queue; you rule.
You may adopt, change or reject any proposal, and you may add an id only for a defect you find in the bytes. The rulings of
rounds 1-6 stand unless you amend one by id, in words.

**This round is narrow.** Rule on the ten queue items and on nothing else. Do not reopen a row, a boundary or a confidence
no item touches, and do not re-raise a finding the boss marked `already_routed`.

**Reading rules.** Read the queue whole. Read `1cor_boss_audit.v1.json` by key: `rows`, for the rows and findings an item
names; `escalations`; `reported_where_measured`; the conditions B3, B4, B7, B8. Read the rulings at gate and where an item
points. Slice rows and witness lines by a script of your own. Check every Greek claim against `1Cor_rp.txt` and
`1Cor_sbl.txt`, by script, and name the tier: there is no morphology layer, so a form label is your reading, INFERRED.

**Testing words.** Before you order words, apply all of them to one private copy of the rows and run, on that copy,
`run_validator_suite.py`, `check_tiling.py`, `ngram7.py --gate 10` and `cwo_sweep_1cor.py`, each with any output under
OUT\work only. Read a tool's header for its arguments first, and never pass an argument to a script whose code shows no
parser. Never pass `--write`. Earlier ordered words failed the register and universals members, so report what each run
returned. The final-rows sweep is reviewed against the classes in `1cor_fixup3_review_S5.json`, so if your words create a
sweep hit that is not in FIXUP-4, name it, class it and say why it stands, or change the words.

**Order form.** Every order that changes bytes uses the form of R5-S5-11: `{"to":"author_fixup:W<n>","order":"...",
"exact_spans":[{"row":"...","field":"...","replace_exactly_once":"...","with":"..."}]}`, so a tool applies it with no
author and no transcription step. A span must occur exactly once in the named field. No quoted Greek byte changes, with one
exception: a quotation may be replaced by a contiguous run copied byte for byte from the same witness line. If an order
prescribes wording for the next check, it takes an ACCEPT form, with no red, reject*, blocker*, refut*, unfit or 'not fit'.
Use row ids as they stand in the rows file (W2-006, not the boss's W2-6). Keep the same order of magnitude of words: a span
replaces a sentence or less, and no row gains a new claim.

**Limits.** No ruling adjudicates a divided reading, selects a textual reading or source tradition, or settles a contested
interpretation in a boundary; route such a thing to Fable's end review. Moving a boundary is outside this round: if you
find a boundary cannot stand, rule `hold` on that item, state the bytes, and the orchestrator stops there. No new
corpus-wide sweep unless a defect in the bytes demands it; `corpus_wide_orders` may be an empty list.

**Forbidden in addition to the template's list:** the writers', the fix-up authors', S5's, S6's, the boss's and the primary
reviewers' OUT directories, receipts, final messages and evidence notes; every `*_attempt_receipts.jsonl`.

**GATE-E7.** Set `tool_fixes_before_fixup`, `fixup_may_launch`, `fixup_parts`, `s2_conditions` and `primaries_may_launch`
(false). The key `s2_conditions` keeps its round-1 name so the tools that read it still work. Name, in the same sentence as
each clause you keep or write, the run that decides it (E6).

**Deliverable form.** One JSON object:

```
{"attempt_id":"cor_controlling_rulings_r7_a1","execution_id":"<your execution id>",
 "inputs_ruled_on":[{"path":"SP\\...","sha256":"<digest of the bytes you read>"}],
 "rulings":[{"id":"<queue id>","ruling":"ratify|ratify_with_changes|reverse|adopt|reject|close|keep_open|defer|amend|hold|cut",
             "decision":"...","reason":"...","evidence":["<exact path + ref or bytes>"],
             "orders":[{"to":"orchestrator|tool_fix|author_fixup:W<n>|s8|primaries|fable_end_review","order":"...","exact_spans":[]}]}],
 "corpus_wide_orders":[],
 "gate":{"tool_fixes_before_fixup":[],"fixup_may_launch":false,"fixup_parts":[],"s2_conditions":["..."],"primaries_may_launch":false},
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "deliverables":[],"verification":[]}
```

One ruling per queue id; no id missing.
