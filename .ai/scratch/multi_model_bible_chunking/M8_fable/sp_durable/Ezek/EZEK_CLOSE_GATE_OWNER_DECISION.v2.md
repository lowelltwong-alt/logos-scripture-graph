# Ezekiel close — OWNER DECISION REQUIRED: the grader, the scope, and the hard line

Written 2026-09-21 by the orchestrator (claude-opus-5), session 910cbe15. **This file states choices and makes none
of them.** The orchestrator authored the artifacts under audit and is the one party that may not decide who grades
them, and the budget question is bound by OW-22, which reserves scope cuts to the owner.

## 0. This supersedes v1, which understated the problem — and why that matters

`EZEK_CLOSE_GATE_OWNER_DECISION.v1.md` was written an hour earlier and is **retained, not edited** (E-44: a position
is destroyed by being overwritten). It said the blocker was close-gate items 20–23 and that "every close item that
does not need Fable is finished." **That was wrong, and wrong in the direction that flattered the work.** I had not
checked what the close pipeline still requires. When I read the close tool that actually closed Lamentations, I found
three further passes Ezekiel has never had, two of them gated on Fable **in code**, and no assembled corpus. v1's
framing — "one grade away" — would have invited a ruling on a false premise. The correction is below.

This is the same error as E-49, twice in one session: the first true, measurable thing found was adopted as the whole
answer. I checked the *grading* blocker carefully and assumed the *rest* of the pipeline was done because the items I
happened to be holding were done.

## 1. What is genuinely finished

- **The chunking itself.** 138 shipped rows (`repair/rows_v7_cwo24.jsonl`), carried through repair waves to CWO-24.
- **Full dual-blind primaries review over the whole book** — 145 of 145 planned rows, no sampling. MEASURED: **22 of
  22 clusters carry two lenses (LF + OL); zero single-lens clusters.**
- **Close-gate item 24** (OW-18 provenance tiers): gate ran **GREEN on 18 vectors this session**; capture index
  covers 44 executions with 0 digest mismatches.
- **Close-gate item 25** (OW-19 lens multiplicity): measured, with one finding left open (§4).
- **Close-gate items 20–23 audit brief**: BUILT, reproducible from one retained generator, **provably blind** (two
  12,139-byte briefs differing on exactly 4 lines: the lane letter and the lane's own output paths), **pins MATCH 21
  of 21, zero drift**, selftest GREEN.
- **Budget census**: 223 attempts, **ZERO undeclared**, all five failed dispatches receipted.
- **Error ledger** E-44 … E-49; scholar record v2; method record v6; blast-radius atlas.
- Durability checkpoint written, carriers re-bound, safe-to-clear **PASS**.

## 2. What Ezekiel still needs, and what each thing is gated on

| # | Outstanding pass | Author per the Lam precedent | State | Gate |
|---|---|---|---|---|
| 1 | `#e16` ruling application / final remediation | Opus | docket + ruling brief **built**, application not evidenced | none |
| 2 | **Postcheck** → verdict `fit_to_assemble` | **claude-opus-5** (measured: Lam's `postcheck_01/02.json`) | **ABSENT** — no `postcheck/` directory | budget only |
| 3 | Stage-1 **transcript audit** packets | **claude-fable-5-1** | **ABSENT** | hard-gated in code |
| 4 | **OW-6 final check** → verdict `fit_to_close` | **claude-fable-5-1** | **ABSENT** — no `final_check/` directory | hard-gated in code |
| 5 | Close-gate items 20–23 **grade** | Fable, per OW-13 | brief built, **UNGRADED** | OW-13 + OW-19 |
| 6 | Assembly → `book_chunks/Ezek/chunks.jsonl`, 3 sidecars, whole-Bible map, `receipts/Ezek_completion.json`, `marathon_progress.yaml` | mechanical | **ABSENT** — and no `sp_durable/Ezek/_close_book.py` exists yet | gated on 2–5 |

**"Hard-gated in code" is literal.** The Lamentations close tool, which an Ezekiel close would be re-keyed from,
refuses at these assertions (`sp_durable/Lam/_close_book.py`):

- line 58 — the OW-6 packet must exist: *"no book closes without a claude-fable-5-1 fit_to_close verdict"*
- line 60 — `assert fc.get("model") == "claude-fable-5-1"` — *"the gate names the model"*
- line 61 — `assert fc.get("verdict") == "fit_to_close"`
- line 88 — every stage-1 transcript auditor must also be `claude-fable-5-1`

So closing Ezekiel without Fable is not a matter of judgement I could exercise quietly; it requires **removing or
rewriting an assertion whose stated purpose is to stop exactly this.** The registry-mutation policy I work under says
that when the guarded mechanism cannot represent the change, I stop and bring you a separately reviewed mechanism
rather than weakening the guard. **I have not touched those lines and will not without your explicit instruction.**

## 3. Fable is not dispatchable on this account — MEASURED across five dispatches

| # | Dispatch | Five-hour window | Result |
|---|---|---|---|
| 1–2 | lanes A#e1, B#e1 | **95%** used | HTTP 429 "out of usage credits" |
| 3–4 | lanes A#e2, B#e2 after the window reset | **6%** used, fresh to 2026-09-22T06:10Z | identical refusal |
| 5 | minimal probe: one line, no brief, no file read, **every tool forbidden**, reply `OK` | 6% used | identical refusal |

The fifth is decisive: reading nothing and using no tool, it eliminates brief size, pinned-input cost, context and
tool budget; the 95%/6% pair eliminates the five-hour window; the weekly all-models window measured 14%. **What
remains is the model.** Extra usage is **disabled**, 0.00 of 65.00 USD spent, and the error's own remedy is to switch
model or add credits. **NOT established:** that paying would unblock it — nothing here tests that, and it is a
financial setting only you may change. I did not change it. All five are receipted with
`tokens_reported: "UNAVAILABLE"` (status failed, no usage block, 0-byte output — unrecoverable spend, not zero).

## 4. The budget, which constrains the options as much as the model does

- **MEASURED lower bound: 69,506,687 tokens.** Ceiling per OW-22: **72,000,000, a hard line.**
- Residual unmeasured attempts: **ESTIMATED 6,420,990**, so true total lies in **[69,506,687, ≈75,927,677]**.
- **The hard line sits inside that interval.** A breach is neither established nor excluded, and the nominal
  2,493,313 of headroom **must not be reported as available**.

Consequence I am not entitled to decide: **passes 2, 3 and 4 are each substantial multi-lane work, and I cannot
honestly claim they fit under the hard line.** OW-22 says to bring you a named scope cut rather than ask for a raise.
I am bringing one (options below), and I did **not** start the Opus-doable postcheck, because beginning an unfunded
pass and stopping mid-way is the worst of the available outcomes.

**The open finding a grader would settle**, recorded rather than resolved toward closing: 8 of the 138 shipped ids
were minted after the dual-blind round (`P03-021/022/023, P04-012/013, P06-014/015, P08-016`). Their *text* sat inside
a dual-blind cluster; their *final seams* were seen only by waves that read the shipped rows — and item 25's own rule
says such a lane is RETROFIT-AUDIT and does **not** count toward lens multiplicity. So those 8 are dual-blind on text
and audit-only on seam. Whether that satisfies "no unit group is reviewed by one lens" is a judgement I have left open.

## 5. On substituting a grader — the honest version

OW-19's "same family = one voice" governs the **third** lens, not the two-lane floor: the LF and OL lanes that carried
this whole book were both Anthropic-family, and so were the two planned Fable lanes. Their admissibility rested on
(a) **not being the author** and (b) **OW-13 naming Fable for the checking role**. Two blind **Opus** lanes satisfy
(a) exactly as Fable lanes would; they fail only (b).

**But the weakness is real.** The authoring and grading weights would be identical, and correlated blind spots are
precisely what OW-13's Fable assignment exists to prevent: a reviewer sharing the author's habits will accept the
author's habits. An Opus lane is a genuine second *context* and a genuine non-author; it is a weaker second *mind*
than the rule intends. That is a disclosed downgrade of the floor, and not mine to grant myself.

**Not offered, and why:** me grading my own items (OW-19 forbids it); a Sonnet lane (OW-13: "never Fable-level");
editing the code gates myself; or reporting a floor as met by lanes that did not run.

## 6. The options

**A — Restore Fable, then run the pipeline as designed.** Enable paid extra usage (or otherwise make
`claude-fable-5-1` reachable). Nothing needs rewriting; the briefs and pins are on disk and verified. Then passes 3,
4 and 5 run as intended. **Cost:** a financial change that is yours alone, plus the spend for three Fable passes on
top of a budget already at the hard line. **Risk:** unverified — if the restriction is plan-level rather than credit
level, paying may not unblock it. **Cheapest test:** re-run the one-line probe after changing the setting, before
committing to a pass.

**B — Declare an Opus fallback grader, with the downgrade recorded in the close's own bytes.** Unblocks passes 3, 4
and 5 today at the cost named in §5, and requires amending the code gates through a reviewed mechanism rather than
deleting an assertion. The completion receipt must then state that Ezekiel was graded by a same-weights non-author
fallback, so no future reader mistakes it for an OW-13 grade. **This amends OW-13 and needs you.**

**C — Close Ezekiel with a recorded grading gap.** The book ships with passes 3, 4 and 5 stated as **owed, not met**.
Honest and cheap, and it frees the campaign for the hardest-books queue. **Cost:** it still needs pass 2 (postcheck)
and pass 6 (assembly), it still requires a reviewed change to the code gate, and the first book closed under a
permanent gap sets the precedent for the 41 that follow.

**D — Stop Ezekiel here and bank it.** Everything is checkpointed, receipted and reproducible; nothing is lost by
waiting. Ezekiel stays open at the gate, and the campaign either pauses or moves to the next book with Ezekiel's
close deferred. **Cost:** an open book is a standing liability, and OW-9's book-boundary discipline assumes closure.

## 7. The durable question your ruling should also settle

E-48 was written as a temporary rate-limit lesson and E-49 had to amend it, because the cause was permanent. The
design lesson survives the re-diagnosis: **a governance floor that depends on one named model can vanish for reasons
this campaign does not control** — and here that dependency is compiled into the close tool's assertions, so the
floor's failure mode is a refusal to close, not a silent downgrade. That is the right failure mode and it should be
kept. What it needs is a **declared-in-advance fallback grader**, chosen by you and written into the campaign rules
with its downgrade stated, rather than one improvised at the gate by the agent the floor exists to check. Options A–D
decide Ezekiel; §7 decides the remaining 41 books.
