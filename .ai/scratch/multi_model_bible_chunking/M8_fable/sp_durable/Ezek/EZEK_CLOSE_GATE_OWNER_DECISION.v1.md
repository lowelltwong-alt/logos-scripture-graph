# Ezekiel close gate — OWNER DECISION REQUIRED: who may grade items 20–23

Written 2026-09-21 by the orchestrator (claude-opus-5), session 910cbe15. **This file states a choice and does not
make it.** The orchestrator authored the artifacts under audit, so it is the one party that may not decide who grades
them.

---

## 1. What is finished

Every close-gate item that does not need a grader is done, and the gate's own artifacts are built and verified:

| Thing | State | Evidence |
|---|---|---|
| Merged blind audit brief, items 20–23 | BUILT, reproducible, provably blind | `repair2/CLOSE_AUDIT_BRIEF_A.md` / `_B.md`, 12,139 bytes each, differing on exactly 4 lines (1, 3, 117, 125 — the lane letter and the lane's own output paths) |
| One retained generator for both lanes | `repair2/gen_close_audit_brief.py` | deterministic regeneration **MATCH**; a rule cannot differ by a word between the lanes because both come from one text |
| Pin integrity | **MATCH, 21 of 21 pins, zero drift, both briefs** | `_brief_pin_check.py`, selftest GREEN on 5 vectors, re-verified immediately before the last launch |
| Blindness | **MEASURED**, not asserted | `ezek_close_audit_prelaunch.v1.json` records the line-level diff |
| The author-brief control | Run, FAILED, recorded as **inapplicable** with its verdict, 11 members and the reason | same file, `check_NOT_applicable` — an audit lane writes no rows, so every suite member is out of scope. Not a pass, not a skip |
| Item 24 (OW-18 provenance tiers) | Evidenced; gate **GREEN on 18 vectors this run** | `ezek_close_items_24_25_evidence.v1.json` |
| Item 25 (OW-19 lens multiplicity) | Evidenced; **22 of 22 clusters dual-lens, zero single-lens** | same file |
| Budget census | **223 attempts, ZERO undeclared**, LOWER_BOUND 69,506,687 vs the 72,000,000 hard line | `repair2/census_ow15_v3.py` |
| Error ledger | E-44 … E-49 written | `ERROR_PATTERN_LEDGER.v1.md`, 19 entries |

**One finding is deliberately left open** rather than resolved in the direction that closes the book: 8 of the 138
shipped rows carry ids minted after the dual-blind round, so their *text* was inside a dual-blind cluster but their
*final seams* were seen only by waves that read the shipped rows. Item 25's own rule says a lane that reads the
shipped chunking is RETROFIT-AUDIT and does **not** count toward lens multiplicity. Whether that satisfies "no unit
group is reviewed by one lens" is a judgement, and it is one of the things a grader would settle.

## 2. What is blocked, and what was measured

The two blind lanes were dispatched five times. All five were refused before doing any work — HTTP 429,
`rate_limit`, "You're out of usage credits", model `claude-fable-5-1`.

| # | Dispatch | Five-hour window when it failed | Result |
|---|---|---|---|
| 1–2 | lanes A#e1, B#e1 | **95%** used | refused |
| 3–4 | lanes A#e2, B#e2, after the window reset | **6%** used, fresh to 2026-09-22T06:10Z | refused |
| 5 | a deliberately minimal probe: one line, no brief, no file read, every tool forbidden, reply `OK` | 6% used | refused |

The fifth dispatch is the one that matters. Because it read nothing and used no tool, it eliminates brief size,
pinned-input cost, context and tool budget; the 95%/6% pair eliminates the five-hour window; the weekly all-models
window measured 14%. **What remains is the model itself: `claude-fable-5-1` cannot be dispatched on this account as
configured.** The account's usage card shows extra usage **disabled**, 0.00 of 65.00 USD spent, and the error's own
remedy is to switch model or add usage credits.

- Tier: **MEASURED by elimination** across five dispatches and two window states.
- **NOT established:** that enabling paid extra usage would make Fable run. Nothing here tests that, and it is a
  paid setting only you may change. I did not change it and will not.
- All five are receipted under OW-7 with `tokens_reported: "UNAVAILABLE"` — status failed, no usage block, 0-byte
  output. That spend is unrecoverable, **not zero**.

## 3. The blocker is narrower than "no grader exists" — read this before choosing

It would be easy to say Ezekiel cannot be graded by anything. That is not what the rules say, and the distinction
decides how cheap your ruling is.

**OW-19's "same family = one voice" governs the *third* lens, not the two-lane floor.** The dual-blind primaries
rounds that carried this whole book (LF and OL) were *both* Anthropic-family and they counted as the floor. The two
planned Fable lanes were **also** Anthropic-family — they were never decorrelated either. Their admissibility rested
on two other things:

1. **they are not the author** — a separate context that never saw the authoring, reading only a pinned brief; and
2. **OW-13 names Fable for the checking and adjudicating role.**

Two blind **Opus subagent** lanes would satisfy (1) exactly as the Fable lanes would have. They fail only (2). So the
gap is not "nothing may grade this" — it is **"OW-13 assigns this role to a model this account cannot reach, and only
you may reassign it."**

**And the weakness in reassigning it is real, so here it is plainly.** The authoring model and the grading model
would be the same weights. Correlated blind spots are exactly what OW-13's Fable assignment exists to avoid: a
reviewer that shares the author's habits will accept the author's habits. An Opus lane is a genuine second *context*
and a genuine non-author; it is a weaker second *mind* than what the rule intends. That is a downgrade of the floor,
disclosed, not a technicality to be waved through — and I am not entitled to grant it to myself.

## 4. The three options

**A — Enable paid extra usage, then run the Fable lanes as designed.**
Everything is already built; nothing needs rewriting. The briefs and pins are on disk and verified, so the lanes can
launch the moment Fable is reachable. Cost: a paid setting change, which is **yours alone to make** — I will not
touch billing. Risk: unverified. Nothing measured here proves credits are what Fable needs; if it is a plan-level
model restriction, paying may not unblock it.
*Remaining work after this: two lanes plus the separate proposal adjudication (3 executions), then the close.*

**B — Authorize two blind Opus subagent lanes as the declared fallback grader, with the downgrade recorded.**
Unblocks the close today, at the cost named in §3. If you choose this, the close gate should record — in its own
bytes, not in chat — that items 20–23 were graded by a same-weights non-author fallback rather than by the OW-13
grader, so a future reader is never misled about the strength of the check. This amends OW-13 and is why it needs you.
*Remaining work after this: the same 3 executions, then the close.*

**C — Close Ezekiel with a RECORDED grading gap on items 20–23.**
The book ships with items 20–23 built, blind, pinned and **ungraded**, stated as an owed item rather than a met one.
Honest, and it keeps the campaign moving to the hardest-books queue. Cost: item 25's open 8-row seam question stays
unsettled, and the first book graded under a permanent gap sets the precedent for the 41 that follow.

**Not offered, and why:** me grading my own items (OW-19 forbids it outright); a Sonnet lane (OW-13: "never
Fable-level"); or reporting the floor as met by lanes that did not run.

## 5. A standing question your ruling should also answer

E-48 was written as a temporary rate-limit lesson and E-49 had to amend it, because the cause was permanent. The
design lesson survives being re-diagnosed: **a governance floor that depends on one named model can vanish for
reasons this campaign does not control.** Whatever you choose for Ezekiel, the floor needs a *declared-in-advance*
fallback grader — chosen by you, written into the campaign rules — rather than one improvised at the gate by the
agent the floor exists to check. That is the durable fix; A, B and C are only this book.
