# Prompt for a second agent: token-economy findings, fixes and self-check (M8 Bible chunking campaign)

Paste everything below the line into the other agent's session.

---

You are working in the M8 Bible-chunking campaign (repository worktree `C:\wt\logos-t423-m8-fable`). On 2026-11-01 the orchestrating Claude session measured where tokens were going, fixed part of it, and wrote binding rules. Your job: understand the findings, know exactly what was changed, apply the same rules to your own work, and check yourself against the list at the end before every substantive step. Do not rebuild anything listed as already built. Do not weaken any gate, hook or setting named here.

## 1. Read these first (exact paths)

- `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\campaign\TOKEN_ECONOMY_RULES.v1.md` (binding rules TE-1 to TE-12 with the owner's order verbatim and the measured table)
- `C:\Users\lowel\.claude\CLAUDE.md` section 20 "Token economy" (global policy; the 2026-09-21 measurement of 5,566 requests and 2.61 billion cache-read tokens in one session)
- `C:\Users\lowel\.claude\hooks\token_economy.py` (the read-guard, write-nudge, tick and reset hooks)
- `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\campaign\_land_lane.py` (the one-command lane landing)
- `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\1Cor\freeze\CYCLE_STATE.md`, the last two sections "E5 launched; owner decisions batch (2026-11-01)" and "E5 landed (2026-11-01)"

If you cannot reach these paths, sections 2 to 5 stand alone. Read each with ranges or a filtered command. Never print a whole rows file, receipts file or transcript into context.

## 2. What was measured (1 Corinthians review phase, all figures MEASURED from the receipts and brief files)

- The cost is structural, not per call: every byte resident in context is re-read by every later request. A 20 KB payload written at request 800 of a 5,566-request session is re-read about 4,700 times.
- Subagent tokens for 1 Corinthians: 3.83 million. Primary writer lanes 73%, check lanes 15%, controlling (adjudication) lanes 12%.
- Briefs: 48 files, 1,352,374 bytes. 42% of those bytes are paragraphs shared by three or more briefs (Daniel: 25%). Primary briefs averaged 24,996 bytes and pinned whole witness files (Byzantine 85,884 B, SBLGNT 85,708 B, WEB 52,897 B) and whole rows files (233,144 B). Fix-up briefs ran 34 to 37 KB, the controlling brief 14.8 KB, launch messages 2,482 bytes on average.
- Lane graph: 45 lanes, 295 hours wall, 837 lane-hours busy, mean concurrency 2.94 against a cap of 3, 10 idle hours. Parallelism was already at the cap. The critical path is the serial cycle check -> controlling ruling -> fix-up, where checks and rulings ran alone for 14 to 24 minutes each and single fix-up lanes ran alone for about 230 minutes in rounds 1 and 2.
- Orchestrator landing lag: median 0 to 1 minute. Landing is not the bottleneck.
- Harness settings (global `~/.claude/settings.json`): autoCompactWindow 200000, bashOutputMaxChars 8000, taskOutputMaxChars 8000, effortLevel xhigh, model opus[1m]. Hooks: PreToolUse read-guard, PostToolUse write-nudge (BIG_WRITE 20,000 characters) and tick (TICK_EVERY 150 tool calls), PostCompact reset.

## 3. What was fixed (done, verified)

1. Read guard tightened: `BIG_READ` in `token_economy.py` lowered from 400,000 to 150,000 bytes, because 217 to 233 KB rows files had passed as whole-file reads. The pre-change copy is `token_economy.py.pre_883f8c0bd843` beside the hook. The hook compiles.
2. `TOKEN_ECONOMY_RULES.v1.md` written and bound (TE-1 build once and parameterise, TE-2 delta over full, TE-3 scoped payloads, TE-4 brief weight at most half of the E5 brief's bytes, TE-5 one landing command, TE-6 resume from HOT_STATE, TE-7 book-agnostic close, TE-8 parallel to the cap, TE-9 ask the owner once per stage, TE-10 small command output and the Write tool for text, TE-11 measure never guess, TE-12 no gate traded for speed).
3. `_land_lane.py` built and used for the E5 landing: receipt row, install, learning-log line and CYCLE_STATE note in one pinned command instead of five hand-run carriers.
4. Controlling round E5 was run narrow: it ruled on the 14 findings only, tested all 18 ordered edits on a private copy before ordering them, and defined the next check (S6) as a delta over the changed elements. It took 12 minutes.
5. The owner's decisions for the whole six-book close were gathered in one batch (merged-verdict shape, close authority, standing checkpoint per book) so no stage stops to ask again.

## 4. Proposed, not changed (needs the owner)

- Session effort `high` as the default for orchestration, `xhigh` only for adjudication lanes. Only the owner sets effort. The global setting still reads `xhigh`. On 2026-11-01 the session itself read `claude-opus-5-5` at effort `high`, and the orchestrator did not make that change.
- Trim the fixed context. Measured at 105,436 tokens resident: 77,596 were fixed overhead (system tools 36,533, MCP tools 17,245, memory files 10,807, system prompt 6,680, skills 6,331) and only 26,140 were conversation. Disconnecting MCP servers an M8 session does not use and shortening `MEMORY.md` are the largest remaining savings, and both need the owner's say.
- 22 Python tools under `sp_durable` hardcode one old session's scratchpad path (`af84b702-d913-4495-8e57-252cf7894c63`). That folder is temporary, so those tools should read a durable path or a parameter.
- `<Book>/freeze/HOT_STATE.v1.json` (TE-6) is not yet built. The book-agnostic close kit (TE-7) is not yet built; Daniel's `_close_book.py` still holds 36 book-specific constants at lines 59 to 107.
- The FIXUP-4 brief generator (TE-1, derived from `1Cor/fixup/fx3/build_fixup3.py`) is in progress. Do not write a parallel one.

## 5. Self-check before every substantive step

- Am I reading a file over 150 KB whole? Use a range or a command that prints a count or filtered list.
- Will this command print more than about 2 KB? Filter, count or summarise inside the command.
- Is the plan's 5-hour limit at 100%? Check before launching lanes. Past that point work may draw on paid extra usage, and no campaign order grants spending authority, so stop and ask the owner.
- Am I rebuilding a brief, launch message, lane row, landing sequence, gate test or close script that already exists as a generator? Reuse it with parameters. If it is book- or round-specific, parameterise it once rather than copying it.
- Does my brief restate boilerplate that the lane can read by path and sha? Pin by reference; keep only the binding lines and the lane's own orders.
- Am I handing a lane a whole witness or whole rows file when it needs a slice? Slice first.
- Is this check a full re-read when the previous full check already passed? Test the changed elements only.
- Am I at a phase boundary or past about 120K resident tokens with work ahead? Record the handoff carriers, then compact.
- Am I about to claim a speed or token gain without a measured number from the receipts? Measure or say "not measured".
- Am I trading a gate (two blind lanes, model roles, launch-message check, pin checks, registry mutation protocol) for speed? Stop. No gate is traded.

Report in the campaign's form: Result, Evidence, Verification, Not verified, Files changed, Assumptions and risks. Label every figure MEASURED, INFERRED or ASSUMED.
