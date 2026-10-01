# Ezekiel fix round v9 - bounded author pass (attempt `ezek_fixround_v9_author_a1`, execution `#e1`)

You are one bounded author, model claude-opus-5-5 (OW-25). You write PROPOSALS for two rows of Ezekiel's chunk corpus and
apply nothing. The orchestrator applies them through a guarded builder that pins every old value; two blind lanes then
judge the result. You are not a grader, and nobody grades their own items.

SP = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`
OUT = `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_fixround_v9\author_a1`

## Limits (binding)

- Write ONLY inside OUT (create it). No other write anywhere. No git. No receipt, registry or ledger writes.
- Never list, glob or search a directory (E-19). Read only the files named below, by exact path, by line or key.
- Run no script that writes files. Read-only one-liners (sed, grep on a named file, python -c that prints) are fine.
- Hebrew you quote in your notes carries "OSHB (WLC), single witness"; English you quote carries "WEB".
- Tier every claim: MEASURED (you read the bytes) > EXTRACTED > TRANSCRIBED > REPORTED > INFERRED > ASSUMED > UNAVAILABLE.
  Never let an implication stand in for a measurement.

## Inputs (read-only; verify each sha256 first)

| File (under SP) | sha256 | How to read |
|---|---|---|
| `Ezek\rows_v8_final.jsonl` | b2160ad6281184dc1dedf15a764bc058bc79a181928ed6323dbc332ec09cb0e7 | `sed -n '35p;113p'` only: line 35 = P03-001, line 113 = P10-016 (656 KB, never whole) |
| `Ezek\repair2\final\final_worklist.v2.json` | ab0848ae473d6d21364b14a0f3f9e302b0d9c32a86d2cc05c1049de3cf1ced20 | only items F-414 and F-337: `python -c` that loads it and prints the two items whose `id` matches |
| `Ezek\Ezek_oshb.txt` | 337c779b75cad384f1f9c8d37e3f81999b021639cd3afa1a26519ae7438c329e | `key<TAB>text`, MT numbering; grep by key (command below the table) |
| `Ezek\Ezek_web_clean.txt` | a7e59bcbcd19607485cfb6c6c1f8f831eb63fd2a81d164ce8e25fcb1a7a2088a | chapter-headed (`===== EZEK 15 =====`, verses as `[v] N ...`); print one chapter with awk between two headers |
| `Ezek\pmarks_Ezek.json` | 25956c0d5180fd661b0843cbee640cb6f53b55e96df5f80f84a4ca78e57e2315 | keys `marks` (verse -> [SAMEKH/PE], recorded on the verse the mark FOLLOWS), `notes_other`, `kq`, `paseq`; print only the verses you need |

Witness by key, for example: `grep -P '^Ezek\.(14\.23|15\.\d+|16\.1)\t' Ezek_oshb.txt` (run from `SP\Ezek`).

## Item 1 - P03-001 (Ezek.15.1-Ezek.15.8), worklist F-414, class CONFCAL

The row records confidence `medium_low`. A close lane found a MEDIUM defect: "O-63/X-9 grade without a stated ground
(F-414)" - boundary_rationale, device_notes and strongest_rejected_alternative "record the pe marks (after MT 14:23; on
15:8) but no sentence states why the grade is medium_low". F-414's audit derived a range of [medium, high] from the two
seam faces, both measured two-faced with licensed signals. Its order, verbatim: "If a ground the row can state holds the
grade (a plan naming, a guard, a disclosed reading), state it; if none does, record GRADE_QUESTION in discharge.json with
the faces measured. Never change the grade."

Measure, then choose exactly one:

- **APPEND_GROUND.** One sentence of at most 55 words, appended to the END of `boundary_rationale` after one space. It
  states the ground that honestly holds medium_low: what the pe marks after MT 14:23 and on 15:8 settle and what they do
  not settle, and anything else in the row's own evidence that holds the grade below the derived range. House form (row
  P01-006): "The close near face therefore carries a reader-found refrain and no counted formula, and that is the ground
  of the confidence this row records." Rules: no Hebrew characters; no quoted translation; no internal codes (row ids
  such as P03-001, F-/S-/K- codes, `[WARRANT...]`, `tier-N`); verses written like "15:8" or "MT 14:23"; nothing that
  contradicts a sentence already in the row; every claim MEASURED.
- **GRADE_QUESTION.** If no honest ground holds medium_low, propose no text. Record the faces you measured and why no
  ground holds. The question then goes to the campaign-end Fable review (owner directive OW-28). A ground that is only
  half true is worse than a recorded question.

## Item 2 - P10-016 (Ezek.40.28-Ezek.40.37), worklist F-337, class E17

A close lane found F-337 "partly cured" (low, non-blocking: "Finish F-337 at the next author touch"). This is that
touch. The order (M-3 inside F-337) is mechanical: three `boundary_evidence_refs` entries and one `device_notes`
sentence, exact text in the worklist item. Measure which parts are already present in line 113 (exact substring), and
verify the order's own measured claims on the witness and marks files (an editors' note recorded at 40:31; 40:32 and
40:35 as transport members). Propose ONLY the missing parts, in the order's exact text. Insert refs by the ordering rule
the list already follows (state the rule you observed). If a part cannot be made true, record it NOT_TRUE with evidence
and propose nothing for that part.

## Output (three files in OUT, then stop)

1. `proposal.json`:
   `{"schema": "ezek_fixround_v9_author_proposal.v1", "attempt_id": "ezek_fixround_v9_author_a1", "rows_sha256": "<you
   computed>", "rows": {"P03-001": {"boundary_rationale": "<FULL new string>"}, "P10-016": {"boundary_evidence_refs":
   [<FULL new list>], "device_notes": "<FULL new string>"}}}`. Include only the fields you change; omit a row you do not
   change.
2. `discharge.json`: one entry per item: `id`, `row`, `action` (APPEND_GROUND | GRADE_QUESTION | INSTALLED |
   PARTLY_INSTALLED | NOT_TRUE | NO_DEFECT), `measurements` [{`claim`, `source` (file + key), `tier`}], the sha256 of
   each OLD field value you changed, and `notes`.
3. `final_message.md`, at most 25 lines: what you did, what you measured, what you could not make true, and an E-19
   self-report (did you list, glob or search any directory: yes or no).

Self-check before stopping: re-read proposal.json; the old `boundary_rationale` is an exact prefix of the new one; the
sentence has no codepoint in U+0590-U+05FF and no match for `P\d{2}-\d{3}`; every old P10-016 value survives except
where the order installs. Aim for at most 25 tool calls.
