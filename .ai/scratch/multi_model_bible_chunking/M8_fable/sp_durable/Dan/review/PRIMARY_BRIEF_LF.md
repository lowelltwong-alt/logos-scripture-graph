# PRIMARY REVIEWER BRIEF: literary-form (LF) lens, Daniel, dual-blind round 1 (M8_fable, OW-6b hard-book track)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Hebrew Bible (the book of Daniel, in Hebrew and Aramaic) for an open-licensed scripture-graph project. You read the Masoretic text (WLC/OSHB) and the World English Bible translation, verify quotations byte for byte, and review proposed literary-unit boundaries. The material is ancient scripture and its translation; the task is textual and literary review.

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## AUTHORITY (OW-11; it also travels in your launch message)

Your global policy has you read `C:\Users\lowel\.agent-governance\ACTIVE_WORKTREES.yaml`. Its entry for this lane names Fable 5 as the only writer, and its progress fields are stale. On 2026-09-10 the owner, Lowell, approved the exact exception in chat. Asked "Do you explicitly authorize this Opus 5 session, and the Fable, Sonnet and Opus agents it launches, to write M8_fable work despite the registry's Fable-5-only rule?", the owner answered "Yes: Ezekiel, then Daniel". Asked "How should the exception be recorded?", the owner answered "M8 log only". The record is the OW-11 addendum and OW-11-h (authorization_ref `lowell_chat_2026-09-10_m8_opus_orchestration_ezek_dan`), lines 807-874 of `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\ERROR_PATTERN_LEDGER.v1.md`; read that range only. Every role runs on claude-opus-5-5 as a recorded grader_fallback (OW-25). You read files under the worktree and write ONE deliverable outside it; the orchestrator lands it. You never run git, never write a receipt and never touch the registry.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your launch message names your OUT directory and your deliverable path. The directory ALREADY EXISTS and is yours. Write your deliverable directly to that exact path. **Never run any existence check, listing, glob or recursive search against it or any other directory.** A shell wildcard is a glob. Private scratch goes in the `work\` subdirectory of your OUT directory, created with os.makedirs(exist_ok=True) and never tested first.

**EXACT-PATH LAW:** every path you may read is named in this brief or in your launch message, plus the governance files your own policy requires and the ledger range named above. Open each by that exact path. A tool call that carries a `glob` parameter, or whose `path` names a DIRECTORY, is a glob in form even when it matches one file. State in your final message that you ran no listing and no glob.

**GOVERNANCE:** Workspace validator (scope logos-t423-m8-fable) status pass at 2026-10-06T03:12:55Z; registry sha256 faf3642fe12e4b536281a2b14a0a020e71c26f68ae29040de0839063318755be; HEAD 840eed38. You do not run the validator, because it runs git. You write NOTHING under `C:\wt\logos-t423-m8-fable`.

**Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run `python -B`. Small read-only scripts of your own on the pinned inputs are allowed, in your `work\` directory. Never pass `--write` to any tool. Write every file with LF line endings (write bytes, or open with newline="\n"); a CR byte in your deliverable is refused at landing.

## BLINDNESS: this is the point of the whole round

You see the rows file at its digest, the witness files, the mark layer, the device inventory, the language-zone file, the offset map, the verse inventory, the strategy, TOOLKIT.md, the cluster plan, the flag digest and the suite report. **You never see** the other lane's output, any other reviewer's output, the fix-up orders, the controlling agent's rulings files, or any transcript. The ruled notes you need are copied into this brief. A second lane is reviewing the same rows, and the value of the pair is that neither saw the other.

**FORBIDDEN:** every other model lane (`M1_cursor`, `M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol`, `comparison\`); every other book's directory under SP (nothing from another book passes as Daniel's, E-65); `SP\Dan\review\` and `SP\Dan\fixup\` beyond the files named in your table; `SP\Dan\primaries\`; the writers', reviewers' and fix-up authors' OUT directories and final messages; every `*_attempt_receipts.jsonl`; CYCLE_STATE, the campaign logs and transcripts.

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a hard stop: report it and stop.

| input | sha256 |
|---|---|
| `SP\Dan\fixup\draft_rows_fixup5_applied.jsonl` | `2bee5919f06c22aa61b8bedf2e66ba4b22218f4ec70e6f9b65b3049aaa0f8aca` |
| `SP\Dan\review_clusters.json` | `2f8b57ff5e62f46c96e81c22b7a0cc9df069093129862fc2e6ea257da15d9ec3` |
| `SP\Dan\flags_by_row.json` | `f53c0fe88ae136548c98ce8a8c16f0a048abcd3968bc9e654b7eb57e347e4ce7` |
| `SP\Dan\review\h_evidence_fx5\suite_report_post_fx5.json` | `80cdd32cf374b35582a552b16eafa8999de557bfe0a61d53a8761d9d135b8f2f` |
| `SP\Dan\book_strategy_Dan.md` | `158e517af36db3411fe5cb8647fea20a50218b89bcf0338129d558d60b5a20da` |
| `SP\Dan\pmarks_Dan.json` | `7df2d3054a57ade7b3441883f5601a03e0baeea4ae22c076ed446f268bad7c9b` |
| `SP\Dan\dan_device_inventory.json` | `466d7e6e91a6af396fe9d5e38e1e54fc10272be79229d398283af92168552964` |
| `SP\Dan\dan_language_zones.json` | `903cf551acd9fc7a4e2a3721bb1431435eeb52141cb0429799f19ad566f70a6b` |
| `SP\Dan\web_mt_offset_map.json` | `833d2ce37d015eccaaaac856d52c1931b9fd26bccb343064013fefc1da603da5` |
| `SP\Dan\Dan_oshb.txt` | `8424e3630879c53a44530dee0b87e6c1a64f020619a3c3c0ac758a387a33b3a0` |
| `SP\Dan\Dan_web_clean.txt` | `532fc0e391ac63777e1f57303213b3aaef4ce32071bede797a488bfcee5b6cfa` |
| `SP\Dan\verse_inventory.json` | `de3dcac0f4649981a1c4c342add61c65fa7fb8b537261078695e30007924658b` |
| `SP\Dan\tools\TOOLKIT.md` | `b9e9b59a75721682d5df005e69909cb7e6d7056aab0b1d0a29c7f02cd79269e5` |

## The corpus and your cluster

The rows file is `SP\Dan\fixup\draft_rows_fixup5_applied.jsonl` at `2bee5919f06c22aa61b8bedf2e66ba4b22218f4ec70e6f9b65b3049aaa0f8aca`: 75 rows tiling Daniel's 357 verses on the WEB numbering face. Your launch message names your cluster id; its row ids are in `SP\Dan\review_clusters.json` under that id (11 clusters, none spanning a writer part). **Review every row in your cluster. There is no sampling.** Read the neighbouring row on each side of your cluster's first and last row as context for the seam, but give items only for your own rows.

## Triage you are given, and must answer

Give one `triage_answers` entry for each of TRIAGE-DAN-01, TRIAGE-DAN-02, TRIAGE-DAN-03, TRIAGE-DAN-04, TRIAGE-DAN-05; where none of its rows is in your cluster, say `in_my_cluster: false` and nothing more.

- **TRIAGE-DAN-01 (missing tier words)** - **E3-N1-FIELDS** (ruling E3-N1-FIELDS, copied whole).
- order: Attached finding: in the listed rows and fields no tier word is present. For each, say whether the field holds a count or claim that lacks its tier (strategy section 8 item 7).
- rows: W2-001, W2-002, W2-003, W2-004, W2-005, W2-006, W2-008, W2-009, W2-010, W2-011, W2-012, W2-013, W2-014, W3-005, W3-007, W3-008, W3-009, W3-011, W3-012, W3-013, W3-014, W4-001, W4-002, W4-003, W4-004, W4-005, W4-006, W4-007, W4-008, W4-009, W4-010, W4-012, W4-013, W6-009
- fields: per the evidence list
- the ruling's evidence list, copied whole: ["work\\r3.py output: rows with at least one untiered prose field = 49; by part W2 14, W1 13, W4 13, W3 8, W6 1", "SP\\Dan\\fixup\\draft_rows_fixup2_applied.jsonl W1-001.boundary_rationale and .device_notes (read)", "untiered fields outside FIXUP-3 scope: {\"W2-001\": [\"strongest_rejected_alternative\"], \"W2-002\": [\"boundary_rationale\", \"strongest_rejected_alternative\"], \"W2-003\": [\"boundary_rationale\"], \"W2-004\": [\"boundary_rationale\", \"strongest_rejected_alternative\"], \"W2-005\": [\"boundary_rationale\", \"strongest_rejected_alternative\"], \"W2-006\": [\"boundary_rationale\", \"strongest_rejected_alternative\"], \"W2-008\": [\"strongest_rejected_alternative\"], \"W2-009\": [\"boundary_rationale\", \"strongest_rejected_alternative\"], \"W2-010\": [\"strongest_rejected_alternative\"], \"W2-011\": [\"strongest_rejected_alternative\"], \"W2-012\": [\"strongest_rejected_alternative\"], \"W2-013\": [\"strongest_rejected_alternative\", \"device_notes\"], \"W2-014\": [\"boundary_rationale\", \"strongest_rejected_alternative\"], \"W3-005\": [\"strongest_rejected_alternative\"], \"W3-007\": [\"strongest_rejected_alternative\", \"device_notes\"], \"W3-008\": [\"boundary_rationale\"], \"W3-009\": [\"boundary_rationale\"], \"W3-011\": [\"strongest_rejected_alternative\"], \"W3-012\": [\"boundary_rationale\"], \"W3-013\": [\"strongest_rejected_alternative\"], \"W3-014\": [\"strongest_rejected_alternative\", \"device_notes\"], \"W4-001\": [\"strongest_rejected_alternative\", \"device_notes\"], \"W4-002\": [\"strongest_rejected_alternative\"], \"W4-003\": [\"boundary_rationale\"], \"W4-004\": [\"strongest_rejected_alternative\"], \"W4-005\": [\"strongest_rejected_alternative\"], \"W4-006\": [\"strongest_rejected_alternative\"], \"W4-007\": [\"strongest_rejected_alternative\"], \"W4-008\": [\"strongest_rejected_alternative\", \"device_notes\"], \"W4-009\": [\"strongest_rejected_alternative\"], \"W4-010\": [\"boundary_rationale\", \"strongest_rejected_alternative\"], \"W4-012\": [\"strongest_rejected_alternative\", \"device_notes\"], \"W4-013\": [\"strongest_rejected_alternative\"], \"W6-009\": [\"device_notes\"]}"]
  Answer for every listed row that is in your cluster: does the field hold a count or a claim that lacks its tier? Name the field and the claim.
- **TRIAGE-DAN-02 (tier words set by the third fix-up)** - gate F11 of ruling GATE-E4 orders you to test the truth of every tier word in the 15 rows that fix-up changed. MEASURED by a value-by-value comparison of the rows before and after it, the 15 rows are: W1-001, W1-002, W1-003, W1-004, W1-005, W1-006, W1-007, W1-008, W1-009, W1-010, W1-011, W1-012, W1-013, W2-007, W4-011. For each one in your cluster, test every tier word (MEASURED, EXTRACTED, REPORTED, INFERRED, ASSUMED, UNAVAILABLE) against the layer it names: a tier stronger than the evidence is a defect, and so is a layer that does not hold the fact. Say what you opened to test it.
- **TRIAGE-DAN-03 (six author notes, REPORTED)** - **AUTHOR-TIER-QUERIES** (ruling AUTHOR-TIER-QUERIES, copied whole).
- order: Carry the six author notes (a) to (f) in the briefs as REPORTED, each with this ruling's finding. In particular: in W1-006 to W1-013 device_notes the MEASURED word beside a language word covers the language only; say whether the genre word beside it needs its own tier. Test the ketiv/qere lists of W1-006 and W1-012 against the mark layer.
- rows: W4-011, W2-007, W1-006, W1-007, W1-008, W1-009, W1-010, W1-011, W1-012, W1-013
- fields: boundary_rationale, strongest_rejected_alternative, device_notes
- the ruling's decision, copied whole: One change, five notes left as they stand. Changed: (d, second half) W1-010.strongest_rejected_alternative, last sentence, takes ' (INFERRED)' in the same FIXUP-4, by the span 'for the end review. -> for the end review (INFERRED).'. Not changed: (a), (b), (c), (d, first half: W2-007), (e), (f). All six notes travel in the primaries' briefs as REPORTED author notes, with my findings below, and go to the end review. W2 and W4 are not opened.
- the ruling's findings on notes (a) to (f), copied whole. They are REPORTED to you, not verified by you: I checked each note I could against the pinned bytes. (a) W4-011 'the seer seeks understanding (EXTRACTED, WEB)': Dan_web_clean.txt 8:15 has 'I sought to understand it' (and Dan_oshb.txt Dan.8.15 va-avaqsha vina); the claim is in the named layer's bytes, in paraphrase with the tense changed. The tier is true; no change. (b) W4-011 'where Gabriel comes near (8:17) (INFERRED)': Dan_web_clean.txt 8:17 has 'So he came near where I stood' and the name stands only in 8:16, in the voice's address; that 'he' is Gabriel is a reading. INFERRED is right; no change. (c) A sentence that mixes a witness fact with a reading and is tiered INFERRED states less than it could and nothing false; strategy section 8 item 7 forbids a stronger word, not a weaker one. No change; I used the same tier for W1-002. (d) W2-007 strongest_rejected_alternative first sentence ('Fold 3:30 back into 3:28-30 with the blessing and decree.') states the rival; it is a proposal, not a fact about a witness and not a conclusion, the field holds an annotation, and opening W2 for it would add a lane for no claim. No change. W1-010 last sentence ('Region (o), a weak edge, for the end review.') is different: 'a weak edge' is a conclusion of the kind E3 rule (c) names ('a seam is weak'), not a bare pointer, though the strategy lists region (o) among its expected low-confidence regions (book_strategy_Dan.md line 346). W1 is open anyway, the span is unique (MEASURED, work\r2.py: count 1) and INFERRED is true of a weighing. Ordered. (e) W1's seven device_notes of the form 'Aramaic narrative (MEASURED, language-zone layer)' (W1-007..W1-013, and 'wholly in the Aramaic section' in W1-006; MEASURED list, work\r1.py): the layer named is a language layer, so the MEASURED word is true of the language word only; the genre word beside it (narrative, hymn, dialogue, report) is the row's reading and is NOT measured. I say this in words because a reader may take the annotation to cover both (OW-18). I do not order a change: the grammar G offers no way to tier one word of a two-word phrase without adding words, which the TIER-ONLY RULE forbids, and the language-zone file is not among my inputs, so I could not check the claim I would be re-tiering. It goes to the primaries and the end review as a named weakness. (f) A complete list of ketiv/qere sites 'in span' is a range claim (it asserts there are no others), so MEASURED with a scan is the tier E3 rule (d) asks for; C5 REPORTS the W1 scan re-ran with the same output. The mark layer file is not among my inputs, so the truth of the two lists is REPORTED here, not checked by me.
- **TRIAGE-DAN-04 (W1-002)** - **C10-W1-002** (ruling C10-W1-002, copied whole).
- order: Note for the briefs: W1-002.boundary_rationale was corrected by FIXUP-4 (speaker of the fear at 1:10). The clause 'keeps giving vegetables' rests on the participles of oshb Dan.1.16 against the simple past of WEB 1:16; test it and the (INFERRED) tier like any other.
- rows: W1-002
- fields: boundary_rationale

- **TRIAGE-DAN-05** - **F9-W1-002-A6** (ruling F9-W1-002-A6, copied whole).
- order: Note for the briefs: W1-002.boundary_rationale was corrected by FIXUP-4 (speaker of the fear at 1:10) and reworded by FIXUP-5 so that the officer's title is not five consecutive WEB words outside the quotation convention. Test the sentence and its (INFERRED) tier like any other, including whether 'the fear of the eunuchs' prince' reads clearly as the fear he voices.
- rows: W1-002
- fields: boundary_rationale


**Coverage note (ruling S2-N5-COVERAGE, copied whole):** Read W1, W2, W5 and W6 prose with the same care as W3 and W4; the suite raised no triage flag there and that is not a finding of cleanness. (rows: all rows of W1, W2, W5, W6)

**Flags over your rows are triage input, never defects.** The suite on this rows file reads hard status GREEN with 137 triage flags (register.flags 70, universals.flags 67); by writer part: W1 0, W2 0, W3 8, W4 129, W5 0, W6 0. `SP\Dan\flags_by_row.json` lists every flag by row. A flag is a question to answer, never a verdict to repeat, and a row with no flag has not been found clean.

## Checklists

1. **NUMBERING ZONES (copied from the offset map's rule).** any structured ref touching WEB 4:1-37, WEB 5:31, WEB ch 6, MT 3:31-33, MT ch 4 or MT ch 6 MUST carry an explicit dual or numeric qualifier; bare coordinates are ambiguous there and only there Zones: MT 3:31-33 = WEB 4:1-3; MT 4:1-34 = WEB 4:4-37; MT 6:1 = WEB 5:31; MT 6:2-29 = WEB 6:1-28; identity in every other chapter. The rows are on the WEB face; the mark layer and the device inventory are on the MT face. A bare coordinate inside a zone is a finding.
2. **LANGUAGE ZONES (read from the language-zone file, not from this sentence).** At the pinned digest the runs are: H from Dan.1.1 w1 to Dan.2.4 w4 (345 words); A from Dan.2.4 w5 to Dan.7.28 w16 (3599 words); H from Dan.8.1 w1 to Dan.12.13 w8 (1975 words). Mixed verse: Dan.2.4 (12 words, the language changes before word 5). A row that calls Aramaic text Hebrew, or the reverse, or that places the change of language at a verse boundary, asserts something the layer does not hold.
3. **TIER WORDS (strategy section 8 item 7; OW-18).** A count or a claim carries its true evidence tier and names the layer that holds it. MEASURED and EXTRACTED need the named layer to hold the fact; a reading is INFERRED. A stronger word than the evidence is a defect; a weaker one is not. Implication is assertion: a tier set beside two words covers only what the layer holds.
4. **MARKS (single witness).** The mark layer is WLC (OSHB) only; a marker claim discloses that. Test every claimed mark in BOTH directions: a claimed mark that is not there, and a mark inside or at the edge of the row that is there and undisclosed. Absence of a mark is never counter-evidence. Setumah and petuchah are not equal.
5. **QUOTATIONS.** Five or more consecutive WEB words from a verse in the row's span or references are a quotation whatever the delimiter, and owe curly double quotes plus a `web:` reference in the same field. A WEB quotation is verbatim; a Hebrew or Aramaic quotation is an exact substring of the witness at its cited MT reference.
6. **REGISTER, for any prose you write.** No strategy section numbers, no decision ids inside a suggested fact, no reviewer names, no tool filenames, no talk of file positions or stages. State grounds by content.
7. **BOTH SIDES (OW-3).** Every seam is assessed from both sides: an onset-only diagnosis is incomplete until the adjacent unit's close is weighed.

## Word runs already repeated across rows (read from the suite's seven-word report at build time)

The hard seven-word gate fails when 10 rows share a run. These stand nearest the gate:

- `wlc aramaic reads this verse carries a` stands on 7 rows
- `verse carries a ketiv qere reading in` stands on 7 rows
- `this verse carries a ketiv qere reading` stands on 7 rows
- `reads this verse carries a ketiv qere` stands on 7 rows
- `qere reading in the k q layer` stands on 7 rows

**A finding names the FACT and the VERSE to install, never a sentence to paste.** If every reviewer proposes wording, the wording converges and the gate fails.

## Your lens: LITERARY FORM (LF)

You are the **literary-form primary**. Your question is whether each row is a coherent literary unit under Daniel's own conventions, and whether its boundaries fall where the text's form says they fall.

**READ IN THIS ORDER** (deliberately different from the other lane's):
1. `book_strategy_Dan.md`: the parents, the ruled granularity, the unit-type vocabulary. Read this FIRST; it is the frame everything else sits in.
2. `dan_device_inventory.json`: the device census (datelines, seeing formulas, decrees, doxologies and the rest), on the MT face. **Read every count from that file.** This brief prints none, so that it cannot go stale; where a row's count differs from the inventory, the inventory is the artifact and the difference is a finding.
3. Your rows.
4. `Dan_web_clean.txt` for the run of the text, then `Dan_oshb.txt` only where a form question turns on the Hebrew or Aramaic.
5. `pmarks_Dan.json`, `dan_language_zones.json` and the offset map only to check a mark, a language claim or a reference a row asserts.

**Judge:** unit_type against the book's vocabulary; whether the opening device actually opens a unit and the closing device actually closes one; whether a doxology, a decree or a narrative summary closes the unit BEFORE the seam rather than opening the one after; whether the row's span holds one literary movement or two; whether the court tales and the visions are cut by their own conventions rather than by chapter number; whether confidence matches the strength of the form evidence; whether the strongest rejected alternative is the strongest one.

**If you quote Hebrew or Aramaic at all, copy it.** Take the exact substring from `Dan_oshb.txt`, confirm programmatically that it is a substring of the line you took it from, and never retype or re-point it. The landing tool tests every Hebrew-script run in your packet against the witness and records each one it does not find.

## Deliverable

Your launch message names the exact output path. Write JSON only, LF line endings:

```
{"attempt_id":"<from your launch message>","execution_id":"<from your launch message>",
 "book":"Dan","role":"primary_LF","cluster":"<cluster id from your launch message>",
 "model_ordered":"claude-opus-5-5 (grader_fallback, OW-25)",
 "rows_file":{"path":"Dan/fixup/draft_rows_fixup5_applied.jsonl","sha256":"<the digest you hashed>"},
 "artifacts_reviewed":[{"path":"SP\\...","artifact_sha256_at_review":"<digest>"}],
 "rows_reviewed":["<every row id in your cluster; no sampling>"],
 "items":[{"row_id":"W1-001",
    "verdict":"support | challenge",
    "severity":"high | medium | low   (present EXACTLY when verdict is challenge, and absent on a support)",
    "claim":"the fact, stated by content, with its verse",
    "tier":"MEASURED | EXTRACTED | TRANSCRIBED | REPORTED | INFERRED | ASSUMED   (the true tier of YOUR claim)",
    "decision":"keep | cut at <exact verse> | confidence stands | confidence moves to <level> | reword <field>",
    "both_sides":"what the evidence on EACH side of the seam says (required for every cut you propose)",
    "suggested_fix":{"fact":"the fact to install","verse":"the verse it rests on"},
    "evidence":["<exact ref or byte quote>"]}],
 "triage_answers":[{"id":"TRIAGE-DAN-01","in_my_cluster":true,"rows":["..."],"decision":"...","evidence":["..."]}],
 "summary":{"supports":0,"challenges":0,"by_severity":{"high":0,"medium":0,"low":0}},
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"<state that you ran no listing and no glob>",
 "limit":"one lens on one cluster; candidate-only, non-authorizing research review"}
```

**THE FIELD NAMES ABOVE ARE THE CONTRACT AND THE LANDING TOOL ENFORCES THEM EXACTLY.** `role` is the string `primary_LF`; items are keyed `row_id`; the fact field is `claim`; `summary` uses `supports`, `challenges` and `by_severity`. `severity` takes `high`, `medium` or `low` and is present exactly when `verdict` is `challenge`. `attempt_id`, `execution_id` and `cluster` must equal your launch message's exactly. One item per row in your cluster, no more and no fewer, each with a non-empty `claim`, a `tier` from the list and a non-empty `evidence`. A row with several findings carries its gravest as the item and the rest inside `evidence`, each named. `summary` must equal the counts recomputed over `items`. `triage_answers` carries exactly one entry for each of TRIAGE-DAN-01, TRIAGE-DAN-02, TRIAGE-DAN-03, TRIAGE-DAN-04, TRIAGE-DAN-05. `rows_file.sha256` must be `2bee5919f06c22aa61b8bedf2e66ba4b22218f4ec70e6f9b65b3049aaa0f8aca`.

## Budget

Keep to roughly 40 tool calls. Report exactly what you ran and what it returned.

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only: `attempt_id`, `execution_id`, `cluster`, `sources` (exact paths with the digest you took), `deliverable`, `deliverable_sha256`, `rows_reviewed`, `summary`, `changes_made_or_no_change`, `verification_evidence`, `unresolved_uncertainty`, `e19_selfreport`, `limit` ("accountable work summary; not chain of thought and not independent proof").

**Do not soften a challenge to make the round look clean, and do not manufacture one to look thorough.** A row that is right is supported with its reason.
