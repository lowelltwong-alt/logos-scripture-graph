# {{LANE}}: {{TITLE}} (M8_fable, 1 Corinthians close kit, hard-book track)

You are lane {{LANE}} of the 1 Corinthians close. The work is candidate-only, NON-AUTHORIZING research. This brief is
binding. Attempt `{{ATTEMPT}}`, execution `{{EXECUTION}}`. You run on claude-opus-5-5 (OW-25).

{{EFFICIENCY}}
Your OUT is the only place you write. After each unit of the work below, write what is finished and the cursor (the next
unit) to `{{OUT}}\work\progress.json` (LF). If you are continued after an interruption, open that exact path and go on
from its cursor, and say so in your final message.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `{{OUT}}` already exists, and so does its `work\` subdirectory. Write
your deliverables directly into it at the names given below. **Never run any existence check, listing, glob or recursive
search against it or any other directory.** A shell wildcard is a glob, and so is a directory scan inside a script.

**EXACT-PATH LAW:** every path you may read is named in this brief, or in a pinned manifest this brief tells you to read
paths from. Open each by that exact path. State in your final message that you ran no listing and no glob. **Never open
any session or agent transcript, `.output` file or compaction summary path, including your own, even if your context
names one; if your context is compacted, rebuild from your OUT working files only.**

## GOVERNANCE

- SP is `{{SP}}`. It is read-only for you. Write nothing under SP, not even a debug file.
- Never run git, never write a receipt, never touch any registry.
- **FORBIDDEN:** every path not named in this brief, including other models' directories, the Greek apparatus and Swete
  directories, and all final-message files. Nothing from another book passes as 1 Corinthians' evidence (E-65): where
  this brief pins another book's file, it is a template of FORM only.
- **Running Python:** set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8`, and run `python -B`.
  Write scripts to files in OUT. Do not pass code through a shell here-document or `python -c`. Every file you write is
  UTF-8 with LF line endings (write bytes, or open with newline="\n").
- **Tiers (OW-18):** every claim names its true tier and never a stronger one: MEASURED if a script of yours produced it,
  EXTRACTED if you read it in a pinned file at a place you name, TRANSCRIBED if you copied it, REPORTED if a lane said it,
  otherwise INFERRED. No hand tallies. Every lane of this book ran on one model family, so agreement between lanes is one
  voice (OW-19).
- Record the sha256 of each pinned input as you read it. A mismatch is a hard stop: report it and stop.

## The work

{{TASK}}

## PINNED INPUTS

{{PINS}}

## Budget

{{BUDGET}} Keep printed output small: count and summarise, never print a file whole.

## YOUR FINAL MESSAGE

Write the result to `{{OUT}}\{{DELIVERABLE}}`, then return the same JSON as your final message: one object with exactly
these keys: {{KEYS}}. `verdict` is one of `delivered` or `delivered_with_gaps`, unless your task names another set. `deliverables` lists every file with name, sha256 and bytes. `verification` lists each claim with
how it was checked and the result. Add `e19_selfreport` as a note inside `verification`. This is an accountable work
summary, not chain of thought and not independent proof.
