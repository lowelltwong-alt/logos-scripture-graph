

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
