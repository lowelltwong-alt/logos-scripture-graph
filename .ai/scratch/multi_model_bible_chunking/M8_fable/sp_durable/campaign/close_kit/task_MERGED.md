**Your role.** You are one of two blind graders of this close. You did not write, review or rule on any row of this book, and
you are not the orchestrator. The other grader works separately on the same question; you never see their work and they
never see yours. The orchestrator has given you no view of the answer. A question in this brief is a question: it does not
tell you what to find. You owe the book neither a pass nor a failure. If the evidence does not support a pass, say so; the
close tool will then refuse to close, and that is the correct result.

**What this pass is.** The owner approved a merged-verdict close for this book (read `book_close_shapes.{{BOOK}}` in the grader
carrier, including the owner's words). You return THREE verdicts in one pass: the postcheck, the final check, and the
grades for close-gate items 20-23, plus the named questions.

**What this pass is not.**

- The stage-1 transcript audit is OWED, NOT MET. No audit of the attempts' transcripts has been run and none will be before
  this close. Your final check must say so. It must never imply transcripts were audited.
- The model is the recorded fallback, not the model the close gate names for this role. The carrier holds the statement of
  that downgrade. It is a recorded downgrade, not an equivalence.
- One reader carries all three verdicts. That is the stated weakness of this shape. Do not let a pass on one verdict carry
  another: judge each on its own evidence, and say in `lane_meta.json` that the three verdicts share you as their reader.
- The campaign-end architect review of this book is DEFERRED by the owner (addendum OW-28). Deferred is never met.

Merging atlas rows into a shared feed, appending to a campaign log, publishing and running the close are not yours. If a
file must change, give the exact change in your findings.

**Verdict 1: the postcheck (`postcheck.json`).** Question: is `rows_v1_final.jsonl` fit to ASSEMBLE into the book's chunks?

Deterministic evidence over all {{ROW_COUNT}} rows: the parity tool `--check`; `gen_sidecars.py --check`; the validator report
(read, not run); and the close tool's dry report (see the pin table), from which you read `gates.json` by script and list
every gate that is not met. Gates about this pair of lanes and about the owner's two choices (`--acf`, `--next-book`) are
expected to be unmet now and are not findings; any other unmet gate is.

Rows you read whole, by line. Your mandatory set is every row graded low and every row a named question names:
{{MANDATORY_ROWS}}. Your EXTRA rows (computed; the other lane has different ones): {{EXTRA_ROWS}}.

For each row read, test against the witnesses by script extract of the row's span:

- Is the boundary warrant the row's own, in the row's own terms, and does the witness show what the row says it shows?
- Does the confidence follow from the stated grounds? Is the strongest rejected alternative a real one?
- Does every quotation appear in the witness it is attributed to?
- Does any field assert as measured something that is judged?

Record `verdict` (`fit_to_assemble` or `not_fit`); `blocking` (row ids, empty list if none); `residual` (entries with `row_id`,
`e_class`, `severity` `high`/`medium`/`low`, `origin`, `defective_text`, `byte_evidence`, `proposed_cure`; grade severity by what
a reader of the row would be misled about, not by how easy the cure is; any high or medium residual blocks assembly);
`rows_read` (each row id with one line of what you tested and found); `checks_run` (each command with its verdict as printed).

**Verdict 2: the final check (`final_check.json`).** Question: is the BOOK fit to CLOSE, over the whole record you could read?

Record:

- `book`: `{{BOOK}}`; `corpus`: `rows_v1_final.jsonl`; `corpus_sha256`: computed by you. If it is not the pinned value, stop and
  escalate.
- `model` and `grader_role`: `model` is the carrier's `declared_fallback_model`, ONLY if that is the model you are in fact
  running as. If you know you are a different model, or cannot tell, write what you know and say so in `limits`; do not copy
  the carrier's value to satisfy a gate. `grader_role` is `grader_fallback (OW-25)`.
- `audit_coverage`: exactly what you read, and `what_i_did_not_check`.
- `byte_verifications`: each with its claim, the tool run and the result.
- `residual`: same form as the postcheck's.
- `close_gate_assessment`: a list with one entry per item of `CAMPAIGN_CLOSE_GATE.v1.md` (items 1-25) and one for each addendum
  that binds this close, each `{item, met, type, evidence, tier}`. `met` is `true` or `false`, never anything else. Where an
  item is campaign-level or not yet due at a book close, say so in `evidence` and mark it by what is true of this book. An
  unmet entry carries in `type` why it is unmet. Two entries are unmet by the owner's own rulings and each carries a fixed
  type string: the campaign-end architect review deferred by OW-28, and the stage-1 transcript audit. Take the two strings
  from the close tool's `UNMET_TYPES`, exactly. Neither may ever be recorded as met. If you find any OTHER item unmet, record
  it with a `type` in your own words that says what is missing: the close tool will refuse, and that is correct.
- `process_findings`: what you saw in how this close was produced that the owner should know.
- `stage1_findings_disposition`: `[]`, because no stage-1 packet exists.
- `transcript_coverage`: integers `attempts_total` and `attempts_with_a_transcript` from the census tool's `per_book.{{BOOK}}`
  (`attempts`, `transcript_retained`), `attempts_with_no_transcript` (their difference), `bytes_audited_by_stage1: 0`,
  `reconcile_verdict: "NOT_RUN"`, and a `statement` in your own words that the stage-1 transcript audit is OWED, NOT MET.
- `verdict`: `fit_to_close` or `not_fit`. A `fit_to_close` means fit on the evidence you read, with the transcript audit owed and
  the campaign-end review deferred. Say that in `statement`, never more.

**Verdict 3: close-gate items 20-23 (`items_20_23.json`).** Keys `item_20` to `item_23`. For each: `fit_to_accept` (true or false),
`reservations`, `findings`, `checks_i_ran`. Read each item's demand in the close gate before grading it.

- **Item 20, the scholar record.** Run both tools with `--check`. Read these unit ranges and nothing else of the document:
  {{ITEM20_UNITS}}. For each unit ask: is every ground stated in the unit's own terms, and could a scholar who disagrees find
  the evidence against the row? Does the document bind the corpus it describes?
- **Item 21, the method record.** {{ITEM21}}
- **Item 22, the atlas rows.** Run `gen_atlas_rows.py --check`, and `check_atlas_rows.py` with `--out-root` set to `work\atlas` in
  your OUT, plain and with `--selftest`. Record `feed_sha256`: the sha256 you computed of `atlas_candidate_feed_rows.jsonl`. Read
  these ids in the feed and in the dimensions file: {{ITEM22_IDS}}, plus every row of the pairs in NQ-1. Audit the README's
  claims against the files. The question that matters: does any row carry, as measurement, something that is a judgement?
- **Item 23, the proposals and their adjudication.** Are the proposals inside the proposer brief's scope? Test at least two
  `evidence_from_this_book` claims, and at least two of the adjudicator's `evidence_checks`, against the files that would show
  them false. Is each REJECT reasoned? Does the adjudicated file say exactly what the adjudication says
  (`gen_proposals_adjudicated.py --check`)? {{ITEM23_TAIL}}

**Named questions (`named_questions.json`).** A JSON object with one key per id below, each `{answer, evidence, tier, class}`. `tier`
is one of MEASURED, EXTRACTED, TRANSCRIBED, REPORTED, INFERRED, ASSUMED, UNAVAILABLE: name the tier you actually hold. `class`
is `close_blocker`, `disclosed_residual`, `debt_after_close` or `resolved`.

- **NQ-1 the unruled pairs.** The atlas marks linked pairs `possible_inconsistency_unruled`. Find every such pair by script. For
  each, read both rows in the corpus. Is there an inconsistency a reader of the rows would be misled by?
- **NQ-2 licence wording.** What does the scholar record say about the licences or terms of the source texts? Is each such
  statement supported by a pinned file, and at what tier?
- **NQ-3 the adjudication.** One adjudicator ruled, on the same model family as the proposer. Does any adopted proposal depend on
  a rejected or deferred one? Does any adopted text rest on a citation that does not hold?
- **NQ-4 the shared files.** At `--close` the close tool appends to files shared across books (read its dry report for the list).
  Under the close gate's item 15 and its addenda, whose act is each append?
- **NQ-5 the completion receipt's wording.** Read the text the close tool will write into the completion receipt about what
  happens after this close and which directive it cites. Is it accurate against the close gate's addenda?
- **NQ-6 the dry report.** List every unmet gate of your dry report. Which, if any, is neither about this pair of lanes nor an
  owner's choice?
{{BOOK_QUESTIONS}}

**Your read order.** {{READ_ORDER}}

**`lane_meta.json`:** {{LANE_META}}

**`final_message.md`:** at most 40 lines: the three verdicts, every high or medium residual, every named question you class
`close_blocker`, and your limits.

**Deliverables.** Six files in OUT: `postcheck.json`, `final_check.json`, `items_20_23.json`, `named_questions.json`,
`lane_meta.json`, `final_message.md`. Write `postcheck.json` as soon as the rows are read, and rewrite each file whenever a
stage changes it. The result file named at the end of this brief lists all six. Its `verdict` says only whether you delivered
them; the three verdicts of the close are in the six files.

**Hard stops (escalate in your final message rather than write a verdict):** the corpus sha256 is not the pinned value; a pinned
file's sha256 is not the table's; a tool you were told writes nothing wrote something; you cannot tell which model you are and
the carrier's value would have to be assumed.
