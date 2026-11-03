# M8 TOKEN ECONOMY RULES (v1, 2026-11-01) — binding for every remaining book

Owner order, verbatim (chat, 2026-11-01): "is ther any thing else to get this moving and preserve quality? i mean can we
go more than 300 percent faster with out "fastmode" more liek how wo we acojlpish more per token alotment?" and
"preserve that forever in this project moving forward so we dont regress to wehat ever we wer doing slower. liek
those rebuklds are not good if they can be resued."

The unit the owner pays in is tokens per accepted book. Every rule below reduces re-sent or re-read context; none
weakens a gate, skips a lane, changes a model or bypasses a receipt. Where a rule and a gate conflict, the gate wins
and the conflict is recorded as a candidate method-change proposal.

## Where 1 Corinthians' subagent tokens went (MEASURED)

Source: `1Cor/review/1cor_review_attempt_receipts.jsonl`, completion rows with `tokens_notification_unit`, summed by
the scratch script `lane_cost.py` on 2026-11-01 (28 rows; writer lanes and the orchestrator's own context are NOT in
this file and are not counted here).

| lane kind | lanes | tokens | share | mean per lane |
|---|---|---|---|---|
| primary reviews (OL/LF/RT by chapter block) | 20 | 2,783,582 | 73% | 139K |
| fresh distinct checks S2-S5 | 4 | 591,003 | 15% | 148K |
| controlling rounds E1-E4 | 4 | 458,922 | 12% | 115K |
| total in this file | 28 | 3,833,507 | 100% | |

Reading: a lane's cost is dominated by what it re-reads, not by what it writes. Each lane opened the same brief,
contract, witnesses and tooling; each check re-read all 63 rows; each controlling round got freshly built tooling.

## The rules

**TE-1 Build once, parameterise forever.** One generator per artifact kind: brief, launch message, launch-row lane,
landing row, fix-up lander, close tool, close briefs. A new round or a new book is an argument to the generator, never
a new script and never a code patch to a tool. Lane definitions live in data (a JSON table), not in Python
constants that need patching per round. (1Cor did it wrong five times: E1-E5 each got a brief file written by hand or
near-hand and a `patch_launch_tool.py` edit to add the lane.)

**TE-2 Delta over full.** After a book's first full check, every later check tests the changed elements only; the
rest is carried by the digest of the applied rows and is out of scope by order. S6 for 1Cor is the first such check.
A full re-read of the rows is ordered only when a corpus-wide defect is measured in the bytes.

**TE-3 Scoped payloads.** A lane receives a pre-sliced extract of exactly its rows, its chapters and its witness
verses, written by the orchestrator's generator; it is never pointed at a whole witness file or a whole rows file.
Pre-slicing is the orchestrator's one deterministic step; it saves the slice cost in every lane. CANDIDATE until
measured: compare John's primary-lane mean against 1Cor's 139K.

**TE-4 Brief weight.** A brief is the required binding lines (E-13 preamble, authority, the two E-19 lines, the
efficiency lines) plus the task, pins and deliverable. Explanatory prose moves to one pinned contract referenced by
sha. Record brief bytes in the launch row; John's briefs target at most half of E5's 11,6xx bytes per lane kind.

**TE-5 One landing command.** Landing a lane is one invocation that appends the receipt row, the learning-log line,
the CYCLE_STATE note, the cursor line and HOT_STATE under one pin set, with one digest report. Five separate
tool-call sequences per landing is the measured cost of 1Cor's pattern.

**TE-6 Resume from HOT_STATE.** Each book keeps `<Book>/freeze/HOT_STATE.v1.json`: exact paths, sha256s, receipt line
numbers, next ids and the next authorized job. Written at every landing by TE-5. A compaction or a new session costs
one read, not a re-derivation of paths and digests from several carriers.

**TE-7 Book-agnostic close.** `_close_book.py`, its gate tests, the CWO parity tool, the final-rows builder and the
D1-D5 briefs take `--book` (and read witnesses, chapter counts and item lists from a per-book parameter file).
The port from Daniel is done once, for 1 Corinthians; John, Romans, Revelation, Hebrews and Matthew port nothing.

**TE-8 Parallel to the cap.** Independent lanes launch together up to the three-lane cap. Nothing the cap allows is
serialized. Fix-up parts, close lanes D1-D3 and the two blind close lanes are the standing parallel sets.

**TE-9 Ask once.** Every owner decision a stage will need is gathered and asked in one batch before the stage, not
one at a time as each blocks. Recorded answers travel in the ledger and the brief; they are not re-asked.

**TE-10 Small output, Write tool for text.** Commands print counts and filtered lists; no rows file, receipts file,
transcript or whole JSON is printed into context. Multi-line text is written with the Write tool; a shell heredoc or
`python -c` is never used for text with quotes or backslashes.

**TE-11 Measure, never guess.** The speed and token claims for a book cite `lane_cost.py` on its receipts and
`_orchestration_metrics.py`. No claim like "N% faster" is made without those two numbers.

**TE-12 No gate for speed.** OW-19 two blind lanes, OW-25 model roles, OW-30 no Fable call, E-62/E-69 launch gates,
E-73 digest discipline and every receipt stay as they are. A rule here that would need a gate relaxed is dropped, not
the gate.

## Where this binds

- `M8_fable/RESUME_PROMPT_CURRENT.md` names this file at the next cursor write; every resume reads it.
- `M8_fable/ORCHESTRATION_PLAYBOOK` gets a TE section at the 1Cor close.
- The ledger records the owner's order at the next permitted ledger write (the ledger is pinned by the running E5
  brief at the time of writing).
- Memory `m8-speed-first-execution` points here.

Things not yet rebuilt under these rules, as of 2026-11-01: the launch-row lane table (TE-1), the landing command and
HOT_STATE (TE-5/TE-6), pre-sliced lane payloads (TE-3), the book-agnostic close (TE-7). Each is built once, at its
next use in 1 Corinthians, and then reused.
