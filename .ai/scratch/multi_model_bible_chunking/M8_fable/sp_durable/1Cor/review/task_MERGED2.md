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

**This pass is a REISSUE ({{REISSUE_BASIS}}).** The first pair of merged lanes read the rows at `{{BASE_ROWS_REL}}` (sha256
`{{BASE_ROWS_SHA}}`). One repair round since then, {{REPAIR_ROUND}}, changed these rows: {{CHANGED_ROWS}}. Everything above
still binds. The duties below are added to it, and none of them shortens any duty above.

**Blindness, stated plainly.** You are blind to the other reissued lane: you never see its work, and it never sees yours,
until both reports are recorded. You are NOT blind on the changed spans: the rulings that ordered the repair were written
after the first pair's reports, and you may read them. You are not counted as a new blind lens. Say all of this in
`lane_meta.json` under `blindness_statement`.

**R1. The read record (in `final_check.json`).** Your mandatory row set above is replaced by this one: read whole, by line,
on the pinned corpus, every row in {{READ_ROWS}}. These are the changed rows, both seam neighbours of each, and the item 1
sample rows. Every other row, {{HELD_ROWS}}, is held by byte equality: show by script that its line in the corpus is
byte-identical to its line in `{{BASE_ROWS_REL}}`, and say so if any is not. Record `rows_read` (the row ids you read whole)
and `rows_held_by_byte_equality` (the row ids you held), with every corpus row in exactly one of the two lists. Record
`records_read`: each record part you read whole, `{path, locator, sha256}`, including every one named here:
{{MANDATORY_RECORDS}}.

**R2. Close-gate item 1, the LF-support sample (key `reissue_item_1` in `final_check.json`).** The sample file
`{{SAMPLE_REL}}` holds the frame (every row an LF primary final marked `support`) and the sample (every 5th of the id-sorted
frame). Run `{{SAMPLE_CHECK}}` and record what it prints. Then audit each sampled row on the corpus bytes with an adversarial
lens: does the boundary the row draws hold against the witnesses, and does the support the reading lens gave it survive?
Record `{sample_sha256, corpus_sha256, frame_size, sample_size, rows: [{row_id, defect: true|false, severity, defect_class,
lf_attributable: true|false, finding, byte_evidence}], defects, lf_attributable_defects, digits}`. `digits` is one sentence of
the form "d of n sampled LF-supported rows defective, k LF-attributable", with its object named. This is a separate check from
R4: a row in both is judged in each on its own question.

**R3. Close-gate item 14, the repair bytes (key `reissue_item_14` in `final_check.json`).** {{REPAIR_AUTHOR}} You did not
make this repair. By script, compare `{{REPAIR_BEFORE}}` with `{{REPAIR_AFTER}}` and list every row and every field whose
bytes differ. For each difference, find the order in `{{REPAIR_ORDERS}}` that requires it and say whether the after bytes are
exactly what the order states. Then say whether ANY byte differs that no order requires, and whether any order's change is
missing. Show that `{{REPAIR_AFTER}}` is byte-identical to the corpus. Record `{before_sha256, after_sha256, orders_sha256,
after_equals_corpus, rows_differing, fields_differing, orders_applied, per_change: [{row_id, field, order, matches: true|false,
evidence}], unordered_changes, missing_changes, verdict: "match"|"mismatch"}`.

**R4. Close-gate item 25, the changed rows (key `reissue_item_25` in `final_check.json`).** For each of the rows in
{{ITEM25_ROWS}}, give your verdict on the corpus bytes: `{row_id, changed: true|false, verdict: "sound"|"defect", severity,
finding, byte_evidence}`. For a changed row, test the change itself: is the new text the row's own, true to the witness, and
consistent with its neighbours' boundaries? For a neighbour, test the seam it shares with the changed row. Record also
`rows_reviewed` (the count) and `defects`. Any high or medium defect is also a residual above.

**R5. In the close-gate assessment**, items {{DUE_ITEMS}} are entered `met: false` with type `DUE_AT_CLOSE_ACT`: the
orchestrator fills items {{LANE_FILLED_ITEMS}} into the close-evidence file from your R2-R4 keys after both lanes land, and the
rest at the close act. Your `evidence` for each says where your finding is. If R2, R3 or R4 finds the item NOT met, say so in
`evidence` and in `final_message.md`; never write it as met.

{{REISSUE_BOOK_DUTIES}}
