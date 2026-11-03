# FIXUP-2 AUTHOR BRIEF, part W6 (execution #e1): 1 Corinthians, span-exact ruled row repairs (M8_fable, OW-36 queue)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Greek New Testament (the first letter to the Corinthians, in Greek with a public-domain English translation) for a study corpus. You revise a few fields of candidate reading-unit rows under exact orders that delete or replace quoted spans. The material is ancient scripture and its translation; the task is textual and literary editing.

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## AUTHORITY (OW-36; it also travels in your launch message)

The owner authorized this Opus orchestration and its subagents for six books: 1 Corinthians, John, Romans,
Revelation, Hebrews and Matthew. The owner's answer, verbatim: "Your six-book queue (Recommended)". authorization_ref
`lowell_chat_2026-10-14_m8_opus_orchestration_six_book_queue`; verify in `SP\..\ERROR_PATTERN_LEDGER.v1.md` lines
3412-3434 only. You run on claude-opus-5-5 as a recorded grader_fallback (OW-25). You read files under the worktree and
write only under your OUT directory; the orchestrator lands and applies your deliverable. You never run git, never write
a receipt and never touch the registry.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W6` already exists. Write your deliverables directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W6\fixup2_W6_rows.jsonl` and `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W6\fixup2_W6_changes.json`. **Never run any existence check, listing, glob or recursive search against it or any
other directory.** A shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W6\work\`, created with
os.makedirs(exist_ok=True) and never tested first.

**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. No listing, no glob,
no recursive search. State in your final message that you ran no listing and no glob.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`,
`M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or
`comparison\`; every other book's directory under SP; every other part's fix-up OUT; the writers', the reviewers' and
the controlling agent's OUT directories, receipts, final messages and evidence notes; every `*_attempt_receipts.jsonl`;
transcripts; any file not named in this brief. Nothing from another book passes as 1 Corinthians' (E-65).

**Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run `python -B`. Never run any tool not marked RUN below. Never pass `--write`. Never edit any file under the
worktree.

## Your role

You are the FIXUP-2 AUTHOR for part W6. Attempt `cor_fixup2_W6_a1`, execution `cor_fixup2_W6_a1#e1`. You authored none of the rows, the
reviews or the rulings. The controlling agent (execution cor_controlling_rulings_r2_a1#e1) ruled on the S2 review; its
orders to your part are quoted verbatim below. Each order names exact spans; you carry out exactly those orders and
nothing else changes. You do not adjudicate a divided reading, select a textual reading or tradition, settle a contested
interpretation, move any seam or raise any confidence.

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a
hard stop: report it and stop.

| input | sha256 |
|---|---|
| `SP\1Cor\fixup\draft_rows_fixup1_applied.jsonl` | `646f9eeaad82edaf0f4d1f6651ba1f7b06fbbefe0f3d8da1d0e07a4e7d8f8eec` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E2.v1.json` | `1299a598b60bbf3c8fb193381ead098e394242a713d8bac4e584b39fdf0e0541` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E1.v1.json` | `93e5918b10b17842e5700471087290036549f4ab2327220d518967c49b53dc90` |
| `SP\1Cor\review\cwo_1cor_post_fixup1_cwo04_report.v1.json` | `3ec5221234fd7ce7dd82779ffdc026d666a60e9b0511dfc58829a5f6adfbe150` |
| `SP\1Cor\book_strategy_1Cor.md` | `70e344fed9f0f64654baa97dff80e03b706a1288b47de182628dc453212e39ca` |
| `SP\1Cor\tools\TOOLKIT.md` | `49de0883f5cbed7fd9e25fdc8a156a083f8794bdd6490de1b0eee82aa2c7361e` |
| `SP\1Cor\tools\run_validator_suite.py` | `ebe7197b35635d9f8cbf88914219003e32816ba37173f00205668eb5aab2dbb4` |
| `SP\1Cor\tools\ngram7.py` | `2dc3a80d5785d2048fc7b17dac093a47c26f10599922bd083bb7158de10d0230` |
| `SP\1Cor\tools\check_tiling.py` | `71b5ee67b98eeb6815515928448b52baa5cac45692afe09212acf2f85d17bbcf` |
| `SP\1Cor\review\cwo_sweep_1cor.py` | `bb71fd0bc1347ac6ff17f5d0222249d78b19de8e6ce43b7a31eea276fbd58cd9` |
| `SP\1Cor\writer_lanes\_validate_writer_part_1cor.py` | `59ef3318dbd98201e57107e9747f17b579f750116ba875061493fbd3012a46e9` |
| `SP\campaign\grader_models.v1.json` | `cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `4dc47a3e406c7d5a2ca7bf6acd27960f9390424fe236d84b4083e586bb200b9b` |

How you may use each input:

- `SP\1Cor\fixup\draft_rows_fixup1_applied.jsonl`: READ your part's rows in full; other rows only where you check a fact. You change ONLY the row-fields listed below.
- `SP\1Cor\review\1cor_controlling_agent_rulings_E2.v1.json`: READ where you check an order's context (your orders are quoted verbatim below).
- `SP\1Cor\review\1cor_controlling_agent_rulings_E1.v1.json`: READ where you check CWO-1COR-01..03 (quoted below).
- `SP\1Cor\review\cwo_1cor_post_fixup1_cwo04_report.v1.json`: READ where you check a CWO-1COR-04 hit class (your rows' hits are listed below).
- `SP\1Cor\book_strategy_1Cor.md`: READ section 8 in full. BINDING.
- `SP\1Cor\tools\TOOLKIT.md`: READ where you check a suite member's contract. Where it and a tool's code differ, the code is the contract.
- `SP\1Cor\tools\run_validator_suite.py`: RUN on a PRIVATE COPY of the rows in your OUT\work only (it writes its report beside its input). Run no member directly except ngram7.py below.
- `SP\1Cor\tools\ngram7.py`: RUN on your private copy with `--gate 10 --full-ids` (it writes nothing).
- `SP\1Cor\tools\check_tiling.py`: RUN on your private copy with `--range 1Cor.1.1-1Cor.16.24` (it writes nothing).
- `SP\1Cor\review\cwo_sweep_1cor.py`: RUN on your private copy with `--out <a file in your OUT\work>` (it writes only that file).
- `SP\1Cor\writer_lanes\_validate_writer_part_1cor.py`: RUN on a slice of your private copy holding only your part's rows, with `--part W6 --book-index` (it writes nothing).
- `SP\campaign\grader_models.v1.json`: READ where you check your model role (grader_fallback).
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 3412-3434 only (OW-36, the owner's grant).

## The orders to part W6 (quoted from the rulings file, sha256 1299a598b60bbf3c8fb193381ead098e394242a713d8bac4e584b39fdf0e0541)

### S2-02

Decision (verbatim): Adopt. W6-004.boundary_rationale is licensed by name and loses its WEB-paragraph clause; the orchestrator adds this field to the W6 fix-up map.

Your order (verbatim): This licenses, in words, the named field(s) of the named row(s) for this edit only; the round-1 licence did not cover them. W6-004.boundary_rationale: delete the exact span; the sentence then reads 'The onset carries an RP pilcrow at 15:29.'

Exact spans (verbatim): [", and the WEB breaks its paragraph there as well"]

### S2-05

Decision (verbatim): Adopt. 'Splitting at 15:42 on the WEB paragraph and the application formula' becomes 'Splitting at 15:42 on the application formula'.

Your order (verbatim): W6-005.strongest_rejected_alternative: delete the exact span.

Exact spans (verbatim): ["the WEB paragraph and "]

### S2-06

Decision (verbatim): Ratify with changes. S1-02b is extended by name to W6-009 and W6-013.boundary_rationale, licensed for these deletions only. The W6-013 pilcrow hit is classed by hand as a sentence-split artefact: 'marks the autograph' has the Greek words as its subject, and after the WEB deletion the pilcrow stays a bare location.

Your order (verbatim): This licenses, in words, the named field(s) of the named row(s) for this edit only; the round-1 licence did not cover them. W6-009.boundary_rationale: delete both exact spans.

Exact spans (verbatim): [" and opens a WEB paragraph at 16:12", ", with a WEB paragraph at 16:13 as well"]

### S2-06

Decision (verbatim): Ratify with changes. S1-02b is extended by name to W6-009 and W6-013.boundary_rationale, licensed for these deletions only. The W6-013 pilcrow hit is classed by hand as a sentence-split artefact: 'marks the autograph' has the Greek words as its subject, and after the WEB deletion the pilcrow stays a bare location.

Your order (verbatim): This licenses, in words, the named field(s) of the named row(s) for this edit only; the round-1 licence did not cover them. W6-013.boundary_rationale: delete the exact span; the sentence then reads 'The autograph has an RP pilcrow at 16:21.'

Exact spans (verbatim): [" and WEB likewise opens a paragraph at 16:21"]

### S2-09

Decision (verbatim): Adopt S1-01b as written, extended from the bytes to W6-008 (an S1-01b row). In W6-002, W6-003, W6-008, W6-011 and W6-012 the pilcrow remains once, as one bare observed_substrate_signals item naming only its location; every other pilcrow mention in br, sra and dn is deleted. Ref annotations are handled under S2-11.

Your order (verbatim): observed_substrate_signals: merge the two pilcrow items into one bare item and remove the second item. W6-002: oss[1] becomes 'RP pilcrow at 15:12 and 15:20' and oss[2] is removed. W6-003: oss[1] becomes 'RP pilcrow at 15:20 and 15:29' and oss[2] is removed. W6-011: oss[4] becomes 'RP pilcrow at 16:15 and 16:19' and oss[5] is removed. W6-012: oss[3] becomes 'RP pilcrow at 16:19 and 16:21' and oss[4] is removed. W6-008: oss[2] becomes 'RP pilcrow at 16:10'. This licenses, in words, the named field(s) of the named row(s) for this edit only; the round-1 licence did not cover them.

Exact spans (verbatim): ["W6-002.observed_substrate_signals[1..2]", "W6-003.observed_substrate_signals[1..2]", "W6-011.observed_substrate_signals[4..5]", "W6-012.observed_substrate_signals[3..4]", "W6-008.observed_substrate_signals[2]"]

### S2-09

Decision (verbatim): Adopt S1-01b as written, extended from the bytes to W6-008 (an S1-01b row). In W6-002, W6-003, W6-008, W6-011 and W6-012 the pilcrow remains once, as one bare observed_substrate_signals item naming only its location; every other pilcrow mention in br, sra and dn is deleted. Ref annotations are handled under S2-11.

Your order (verbatim): Delete each exact span (the whole sentence where a sentence is quoted). W6-002.boundary_rationale: 'RP pilcrow at 15:20 (close seam).'; W6-002.device_notes: ' and the pilcrow informs it' (the clause then ends 'the onset rests on the conditional.'); W6-003.boundary_rationale: both sentences; W6-011.boundary_rationale: both sentences; W6-012.boundary_rationale: the sentence; W6-008.boundary_rationale: the sentence; W6-008.strongest_rejected_alternative: ' and the RP pilcrow' (the rival at 16:10 stays). This licenses, in words, the named field(s) of the named row(s) for this edit only; the round-1 licence did not cover them.

Exact spans (verbatim): ["RP pilcrow at 15:20 (close seam).", " and the pilcrow informs it", "RP pilcrow at 15:20 stands on the onset.", "RP pilcrow at 15:29 (close seam).", "RP pilcrow at 16:15 stands on the onset.", "RP pilcrow at 16:19 (close seam).", "RP pilcrow at 16:21 (close seam).", "RP pilcrow at 16:10 falls inside the unit.", " and the RP pilcrow"]

### S2-11

Decision (verbatim): Rule that S1-01's 'at most once per row' counts every pilcrow mention in the row, ref annotations included. License annotation edits that strip the pilcrow words from the ref elements of the S1-01 and S1-01b rows. S1-01 itself stands as written and is not relaxed; its strictness beyond rule 5 is recorded as a method-change candidate for the end review.

Your order (verbatim): This licenses, in words, an edit of the annotation text of the named boundary_evidence_refs element(s) only; the ref id, the ref locator and the bracketed tag stay byte-identical, and no element is added or removed unless this order says so. Delete the first exact span from W6-002.ber[2], W6-002.ber[4], W6-003.ber[2], W6-003.ber[5], W6-011.ber[2], W6-011.ber[4], W6-012.ber[2] and W6-012.ber[5]; delete the second exact span from W6-008.ber[4], which then reads 'rp:1Cor.16.10 (Timothy commended)'.

Exact spans (verbatim): ["; RP pilcrow", "; RP pilcrow, interior"]

### CWO-1COR-01 (corpus-wide order)

Predicate (verbatim): `A: an element of boundary_evidence_refs matching ^\s*web: and matching (?i)WEB paragraph|paragraph start|DISCLOSURE-mark. B: a sentence (split on (?<=[.;])\s+) of boundary_rationale, strongest_rejected_alternative or device_notes matching (?i)pilcrow|WEB paragraph|paragraph start|chapter division and also matching (?i)corroborat|agree|join|inform|favour|support|lean|confirm.`

Fields (verbatim): boundary_evidence_refs, boundary_rationale, strongest_rejected_alternative, device_notes; all 70 rows of SP\1Cor\writer\draft_rows_combined.jsonl

Remedy (verbatim): Every A hit is deleted (a web: ref is never boundary evidence, rule 4). Every B hit is classified support-use (a WEB paragraph or chapter division informing, agreeing, joining, corroborating, leaning, favouring, supporting or confirming; or a pilcrow agreeing, joining, corroborating or confirming) or compliant (a disclaimer that the mark does not drive the seam, or an RP pilcrow that informs without deciding). Support-use clauses are deleted by the owning part. If a deletion leaves boundary_evidence_refs below what the suite accepts, the author stops and reports.

### CWO-1COR-03 (corpus-wide order)

Predicate (verbatim): `ngram7 as installed with TF-2, default gate 10, --full-ids, on the applied combined rows: any 7-gram shared by 10 or more rows.`

Fields (verbatim): the fields ngram7.prose() walks

Remedy (verbatim): Each offending gram goes back to its owning parts with the named rows; reword, never exclude.

### CWO-1COR-04 (corpus-wide order)

Predicate (verbatim): `Over sentences of the S fields (split on (?<=[.;])\s+) and each element of the L fields (non-string elements json.dumps'd): W = (?i)\bWEB\b[^.;]{0,40}?\bparagraph(?: starts?)?|\bparagraph starts?\b|\bchapter (?:division|break)s?\b ; P = (?i)pilcrow|\bparagraph marks?\b ; DIS = (?i)not weighed|formatting|decides? nothing|does not decide|do not decide|never drives?|neither drives? nor corroborates?|excluded|not (?:drive|corroborate)|without deciding|informs? and does not decide ; PD2 = (?i)corroborat|agree|\bjoin|confirm|support|favou?r|\blean|points? to|(?<!paragraph )(?<!-)\bmark(?:s|ed|ing)?\b|\bsignal|establish|determin ; VERB = (?i)\b(?:falls?|stands?|sits?|opens?|starts?|breaks?|coincides?|points?|agrees?|marks?|as well|likewise|too|same|also)\b. A W hit is disclosure_only if DIS matches the unit; it is location_only if the unit is an observed_substrate_signals item and VERB does not match the unit with the W matches removed; otherwise it is support_use (presence and absence forms alike). A P hit is support_use if PD2 matches, and informs_compliant if only DIS matches; otherwise it is not listed. In rows W5-001, 002, 003, 010, 011, 012, 013, 014 and W6-002, 003, 008, 011, 012 (round-1 S1-01/S1-01b), every P mention other than the first observed_substrate_signals P item is count_excess.`

Fields (verbatim): S fields: boundary_rationale, strongest_rejected_alternative, device_notes. L fields: observed_substrate_signals, boundary_evidence_refs (annotation text; ids and tags are scanned but never edited).

Remedy (verbatim): Delete the supporting clause or crediting verb and keep the content. Every rival location stays. A crediting verb on a pilcrow becomes a locating verb. count_excess mentions are deleted, with oss items merged into one bare location item. The exact spans are in rulings S2-01..S2-12 and S2-15.

### CWO-1COR-04 support-use and count-excess hits on your rows (MEASURED by the installed sweep on the pinned rows; hand classes by the orchestrator)

- `W6-002.boundary_rationale` CNT count_excess (true_ordered; ordered by S2-09)
- `W6-002.device_notes` CNT count_excess (true_ordered; ordered by S2-09)
- `W6-002.observed_substrate_signals[2]` CNT count_excess (true_ordered; ordered by S2-09)
- `W6-002.boundary_evidence_refs[2]` CNT count_excess (true_ordered; ordered by S2-11)
- `W6-002.boundary_evidence_refs[4]` CNT count_excess (true_ordered; ordered by S2-11)
- `W6-003.boundary_rationale` CNT count_excess (true_ordered; ordered by S2-09)
- `W6-003.boundary_rationale` CNT count_excess (true_ordered; ordered by S2-09)
- `W6-003.observed_substrate_signals[2]` CNT count_excess (true_ordered; ordered by S2-09)
- `W6-003.boundary_evidence_refs[2]` CNT count_excess (true_ordered; ordered by S2-11)
- `W6-003.boundary_evidence_refs[5]` CNT count_excess (true_ordered; ordered by S2-11)
- `W6-004.boundary_rationale` W support_use (true_ordered; ordered by S2-02)
- `W6-005.strongest_rejected_alternative` W support_use (true_ordered; ordered by S2-05)
- `W6-008.boundary_rationale` CNT count_excess (true_ordered; ordered by S2-09)
- `W6-008.strongest_rejected_alternative` CNT count_excess (true_ordered; ordered by S2-09)
- `W6-008.boundary_evidence_refs[4]` CNT count_excess (true_ordered; ordered by S2-11)
- `W6-009.boundary_rationale` W support_use (true_ordered; ordered by S2-06)
- `W6-009.boundary_rationale` W support_use (true_ordered; ordered by S2-06)
- `W6-011.boundary_rationale` CNT count_excess (true_ordered; ordered by S2-09)
- `W6-011.boundary_rationale` CNT count_excess (true_ordered; ordered by S2-09)
- `W6-011.observed_substrate_signals[5]` CNT count_excess (true_ordered; ordered by S2-09)
- `W6-011.boundary_evidence_refs[2]` CNT count_excess (true_ordered; ordered by S2-11)
- `W6-011.boundary_evidence_refs[4]` CNT count_excess (true_ordered; ordered by S2-11)
- `W6-012.boundary_rationale` CNT count_excess (true_ordered; ordered by S2-09)
- `W6-012.observed_substrate_signals[4]` CNT count_excess (true_ordered; ordered by S2-09)
- `W6-012.boundary_evidence_refs[2]` CNT count_excess (true_ordered; ordered by S2-11)
- `W6-012.boundary_evidence_refs[5]` CNT count_excess (true_ordered; ordered by S2-11)
- `W6-013.boundary_rationale` W support_use (true_ordered; ordered by S2-06)
- `W6-013.boundary_rationale` P support_use (false_positive; ordered by -)

## The edits, one per line (the orders above, as operations on the pinned rows)

- `W6-004.boundary_rationale` (S2-02) del delete ", and the WEB breaks its paragraph there as well"
- `W6-005.strongest_rejected_alternative` (S2-05) del delete "the WEB paragraph and "
- `W6-009.boundary_rationale` (S2-06) del delete " and opens a WEB paragraph at 16:12"
- `W6-009.boundary_rationale` (S2-06) del delete ", with a WEB paragraph at 16:13 as well"
- `W6-013.boundary_rationale` (S2-06) del delete " and WEB likewise opens a paragraph at 16:21"
- `W6-002.observed_substrate_signals[1]` (S2-09) oss_set set the element to "RP pilcrow at 15:12 and 15:20"
- `W6-003.observed_substrate_signals[1]` (S2-09) oss_set set the element to "RP pilcrow at 15:20 and 15:29"
- `W6-011.observed_substrate_signals[4]` (S2-09) oss_set set the element to "RP pilcrow at 16:15 and 16:19"
- `W6-012.observed_substrate_signals[3]` (S2-09) oss_set set the element to "RP pilcrow at 16:19 and 16:21"
- `W6-008.observed_substrate_signals[2]` (S2-09) oss_set set the element to "RP pilcrow at 16:10"
- `W6-002.observed_substrate_signals[2]` (S2-09) oss_del remove the element (the pinned list's index 2)
- `W6-003.observed_substrate_signals[2]` (S2-09) oss_del remove the element (the pinned list's index 2)
- `W6-011.observed_substrate_signals[5]` (S2-09) oss_del remove the element (the pinned list's index 5)
- `W6-012.observed_substrate_signals[4]` (S2-09) oss_del remove the element (the pinned list's index 4)
- `W6-002.boundary_rationale` (S2-09) del delete "RP pilcrow at 15:20 (close seam)." (a whole sentence, with one adjoining space)
- `W6-002.device_notes` (S2-09) del delete " and the pilcrow informs it"
- `W6-003.boundary_rationale` (S2-09) del delete "RP pilcrow at 15:20 stands on the onset." (a whole sentence, with one adjoining space)
- `W6-003.boundary_rationale` (S2-09) del delete "RP pilcrow at 15:29 (close seam)." (a whole sentence, with one adjoining space)
- `W6-011.boundary_rationale` (S2-09) del delete "RP pilcrow at 16:15 stands on the onset." (a whole sentence, with one adjoining space)
- `W6-011.boundary_rationale` (S2-09) del delete "RP pilcrow at 16:19 (close seam)." (a whole sentence, with one adjoining space)
- `W6-012.boundary_rationale` (S2-09) del delete "RP pilcrow at 16:21 (close seam)." (a whole sentence, with one adjoining space)
- `W6-008.boundary_rationale` (S2-09) del delete "RP pilcrow at 16:10 falls inside the unit." (a whole sentence, with one adjoining space)
- `W6-008.strongest_rejected_alternative` (S2-09) del delete " and the RP pilcrow"
- `W6-002.boundary_evidence_refs[2]` (S2-11) del delete "; RP pilcrow"
- `W6-002.boundary_evidence_refs[4]` (S2-11) del delete "; RP pilcrow"
- `W6-003.boundary_evidence_refs[2]` (S2-11) del delete "; RP pilcrow"
- `W6-003.boundary_evidence_refs[5]` (S2-11) del delete "; RP pilcrow"
- `W6-011.boundary_evidence_refs[2]` (S2-11) del delete "; RP pilcrow"
- `W6-011.boundary_evidence_refs[4]` (S2-11) del delete "; RP pilcrow"
- `W6-012.boundary_evidence_refs[2]` (S2-11) del delete "; RP pilcrow"
- `W6-012.boundary_evidence_refs[5]` (S2-11) del delete "; RP pilcrow"
- `W6-008.boundary_evidence_refs[4]` (S2-11) del delete "; RP pilcrow, interior"

MEASURED (the orchestrator's script applied every part's edits to a scratch copy of the pinned rows): suite hard_status
GREEN with every member GREEN, triage_flags 0; ngram7 GREEN, 0 offending grams; tiling GREEN 437/437; CWO-1COR-01 A 0;
CWO-1COR-02 0 of 70; CWO-1COR-04 support-use and count-excess 0 except W6-013 boundary_rationale, which the sweep still
flags because the sentence on the Greek greeting ("... marks the autograph") shares a sentence span with the pilcrow
clause (a known split artifact, classed false_positive in the coverage report). That flag is the orchestrator's to
re-class; it is not yours to edit around.

## What you may change (the lander refuses any other difference)

Each licensed field, with its pinned value and the value the orders produce, as JSON values:

#### `W6-002.boundary_evidence_refs` (S2-11)

Pinned: ["web:1Cor.15.12-1Cor.15.19 (span: the if-chain against the deniers)", "rp:1Cor.15.11 (back face: preaching and believing)", "rp:1Cor.15.12 (conditional onset; RP pilcrow)", "rp:1Cor.15.19 (conclusion of the if-chain)", "rp:1Cor.15.20 (adversative affirmation opens the following unit; RP pilcrow)", "web:1Cor.15.20-1Cor.15.28 (counter-assertion that the rejected merge would absorb)", "sbl:1Cor.15.12 (SBL variant site in the clause naming the deniers)", "sbl:1Cor.15.14 (SBL variant site)", "sbl:1Cor.15.17 (SBL variant site)", "sbl:1Cor.15.19 (SBL variant site)"]

Expected after the orders: ["web:1Cor.15.12-1Cor.15.19 (span: the if-chain against the deniers)", "rp:1Cor.15.11 (back face: preaching and believing)", "rp:1Cor.15.12 (conditional onset)", "rp:1Cor.15.19 (conclusion of the if-chain)", "rp:1Cor.15.20 (adversative affirmation opens the following unit)", "web:1Cor.15.20-1Cor.15.28 (counter-assertion that the rejected merge would absorb)", "sbl:1Cor.15.12 (SBL variant site in the clause naming the deniers)", "sbl:1Cor.15.14 (SBL variant site)", "sbl:1Cor.15.17 (SBL variant site)", "sbl:1Cor.15.19 (SBL variant site)"]

#### `W6-002.boundary_rationale` (S2-09)

Pinned: "Back face: the tradition unit closes at 15:11 with the shared preaching and believing. Front face: rp:1Cor.15.12 \"Εἰ δὲ χριστὸς κηρύσσεται ὅτι ἐκ νεκρῶν ἐγήγερται,\" states the premise as a condition and asks how some deny resurrection, web:1Cor.15.12 “how do some among you say that there is no resurrection of the dead?” Interior: the if-clauses of 15:13-15:18 draw out what follows if resurrection is denied. Close: the chain ends at 15:19 on the pitiable state of those whose hope is confined to this life; at 15:20 rp:1Cor.15.20 \"Νυνὶ δὲ\" reverses the hypothesis with an emphatic affirmation. RP pilcrow at 15:20 (close seam)."

Expected after the orders: "Back face: the tradition unit closes at 15:11 with the shared preaching and believing. Front face: rp:1Cor.15.12 \"Εἰ δὲ χριστὸς κηρύσσεται ὅτι ἐκ νεκρῶν ἐγήγερται,\" states the premise as a condition and asks how some deny resurrection, web:1Cor.15.12 “how do some among you say that there is no resurrection of the dead?” Interior: the if-clauses of 15:13-15:18 draw out what follows if resurrection is denied. Close: the chain ends at 15:19 on the pitiable state of those whose hope is confined to this life; at 15:20 rp:1Cor.15.20 \"Νυνὶ δὲ\" reverses the hypothesis with an emphatic affirmation."

#### `W6-002.device_notes` (S2-09)

Pinned: "SBL variant site at 15:12: SBLGNT orders the clause naming the deniers differently, and the conditional words quoted on the front face stand in both witnesses apart from capitalisation of the title. SBL variant sites at 15:14, 15:17 and 15:19 fall inside the if-chain and bear on no edge. No device id fires on either face; the onset rests on the conditional and the pilcrow informs it. Witness lines for the conditional: Robinson-Pierpont Byzantine Textform (Unlicense) for conditional wording; SBLGNT (CC BY 4.0) conditional comparison."

Expected after the orders: "SBL variant site at 15:12: SBLGNT orders the clause naming the deniers differently, and the conditional words quoted on the front face stand in both witnesses apart from capitalisation of the title. SBL variant sites at 15:14, 15:17 and 15:19 fall inside the if-chain and bear on no edge. No device id fires on either face; the onset rests on the conditional. Witness lines for the conditional: Robinson-Pierpont Byzantine Textform (Unlicense) for conditional wording; SBLGNT (CC BY 4.0) conditional comparison."

#### `W6-002.observed_substrate_signals` (S2-09)

Pinned: ["conditional onset Ei de (15:12, glossed)", "RP pilcrow (15:12)", "RP pilcrow on the close seam (15:20)", "SBL variant sites (15:12, 15:14, 15:17, 15:19)"]

Expected after the orders: ["conditional onset Ei de (15:12, glossed)", "RP pilcrow at 15:12 and 15:20", "SBL variant sites (15:12, 15:14, 15:17, 15:19)"]

#### `W6-003.boundary_evidence_refs` (S2-11)

Pinned: ["web:1Cor.15.20-1Cor.15.28 (span: firstfruits and the ordered sequence)", "rp:1Cor.15.19 (back face: end of the reductio)", "rp:1Cor.15.20 (adversative affirmation; RP pilcrow)", "rp:1Cor.15.23 (order of the sequence, interior)", "rp:1Cor.15.28 (final subjection closes the sequence)", "rp:1Cor.15.29 (Epei opens the following unit; RP pilcrow)", "sbl:1Cor.15.20 (SBLGNT lacks the closing verb)", "sbl:1Cor.15.21 (SBL variant site)", "sbl:1Cor.15.24 (SBL variant site)", "sbl:1Cor.15.25 (SBL variant site)", "sbl:1Cor.15.28 (SBL variant site)"]

Expected after the orders: ["web:1Cor.15.20-1Cor.15.28 (span: firstfruits and the ordered sequence)", "rp:1Cor.15.19 (back face: end of the reductio)", "rp:1Cor.15.20 (adversative affirmation)", "rp:1Cor.15.23 (order of the sequence, interior)", "rp:1Cor.15.28 (final subjection closes the sequence)", "rp:1Cor.15.29 (Epei opens the following unit)", "sbl:1Cor.15.20 (SBLGNT lacks the closing verb)", "sbl:1Cor.15.21 (SBL variant site)", "sbl:1Cor.15.24 (SBL variant site)", "sbl:1Cor.15.25 (SBL variant site)", "sbl:1Cor.15.28 (SBL variant site)"]

#### `W6-003.boundary_rationale` (S2-09)

Pinned: "Back face: the reductio closes at 15:19. Front face: rp:1Cor.15.20 \"Νυνὶ δὲ χριστὸς ἐγήγερται ἐκ νεκρῶν,\" affirms the resurrection of Christ against the hypothesis, web:1Cor.15.20 “But now Christ has been raised from the dead.” RP pilcrow at 15:20 stands on the onset. Interior: 15:23, rp:1Cor.15.23 \"Ἕκαστος δὲ ἐν τῷ ἰδίῳ τάγματι·\", sets out the order of firstfruits, those of Christ at his coming, and the end; it is interior to the sequence and opens nothing. Close: the sequence ends at 15:28 with the final subjection of the Son. Across the seam, 15:29 opens with rp:1Cor.15.29 \"Ἐπεὶ τί ποιήσουσιν\", turning from the eschatological order to the readers' own practice. RP pilcrow at 15:29 (close seam)."

Expected after the orders: "Back face: the reductio closes at 15:19. Front face: rp:1Cor.15.20 \"Νυνὶ δὲ χριστὸς ἐγήγερται ἐκ νεκρῶν,\" affirms the resurrection of Christ against the hypothesis, web:1Cor.15.20 “But now Christ has been raised from the dead.” Interior: 15:23, rp:1Cor.15.23 \"Ἕκαστος δὲ ἐν τῷ ἰδίῳ τάγματι·\", sets out the order of firstfruits, those of Christ at his coming, and the end; it is interior to the sequence and opens nothing. Close: the sequence ends at 15:28 with the final subjection of the Son. Across the seam, 15:29 opens with rp:1Cor.15.29 \"Ἐπεὶ τί ποιήσουσιν\", turning from the eschatological order to the readers' own practice."

#### `W6-003.observed_substrate_signals` (S2-09)

Pinned: ["nyni de onset (15:20, glossed)", "RP pilcrow (15:20)", "RP pilcrow on the close seam (15:29)", "interior ordering clause (15:23)"]

Expected after the orders: ["nyni de onset (15:20, glossed)", "RP pilcrow at 15:20 and 15:29", "interior ordering clause (15:23)"]

#### `W6-004.boundary_rationale` (S2-02)

Pinned: "Back face: the sequence closes at 15:28. Front face: rp:1Cor.15.29 \"Ἐπεὶ τί ποιήσουσιν οἱ βαπτιζόμενοι ὑπὲρ τῶν νεκρῶν;\" opens an argument from practice and peril, web:1Cor.15.29 “baptized for the dead”. The onset carries an RP pilcrow at 15:29, and the WEB breaks its paragraph there as well. Interior: the apostle's daily danger at 15:30-15:32 and the quoted maxim of 15:33 extend the same ad hominem move. Close: 15:34 calls the readers to wake up and ends on their shame; 15:35 then voices an imagined questioner, rp:1Cor.15.35 \"Ἀλλ’ ἐρεῖ τις,\". RP pilcrow at 15:35 (close seam)."

Expected after the orders: "Back face: the sequence closes at 15:28. Front face: rp:1Cor.15.29 \"Ἐπεὶ τί ποιήσουσιν οἱ βαπτιζόμενοι ὑπὲρ τῶν νεκρῶν;\" opens an argument from practice and peril, web:1Cor.15.29 “baptized for the dead”. The onset carries an RP pilcrow at 15:29. Interior: the apostle's daily danger at 15:30-15:32 and the quoted maxim of 15:33 extend the same ad hominem move. Close: 15:34 calls the readers to wake up and ends on their shame; 15:35 then voices an imagined questioner, rp:1Cor.15.35 \"Ἀλλ’ ἐρεῖ τις,\". RP pilcrow at 15:35 (close seam)."

#### `W6-005.strongest_rejected_alternative` (S2-05)

Pinned: "Splitting at 15:42 on the WEB paragraph and the application formula rp:1Cor.15.42 \"Οὕτως καὶ\": the words apply the analogies already given rather than raise a new question, so the reply runs on through the Adam contrast."

Expected after the orders: "Splitting at 15:42 on the application formula rp:1Cor.15.42 \"Οὕτως καὶ\": the words apply the analogies already given rather than raise a new question, so the reply runs on through the Adam contrast."

#### `W6-008.boundary_evidence_refs` (S2-11)

Pinned: ["web:1Cor.16.5-1Cor.16.11 (span: itinerary and the envoy)", "rp:1Cor.16.4 (back face: bearers of the gift)", "rp:1Cor.16.5 (travel statement onset)", "web:1Cor.16.8 (Pentecost, metadata)", "rp:1Cor.16.10 (Timothy commended; RP pilcrow, interior)", "sbl:1Cor.16.10 (SBL variant site at the end of the verse)", "rp:1Cor.16.11 (Timothy sent on, close)", "rp:1Cor.16.12 (heading on the far side of the seam)", "sbl:1Cor.16.6 (SBL variant site)", "sbl:1Cor.16.7 (SBL variant site)", "sbl:1Cor.16.8 (SBL variant site)", "sbl:1Cor.16.11 (SBL variant site)"]

Expected after the orders: ["web:1Cor.16.5-1Cor.16.11 (span: itinerary and the envoy)", "rp:1Cor.16.4 (back face: bearers of the gift)", "rp:1Cor.16.5 (travel statement onset)", "web:1Cor.16.8 (Pentecost, metadata)", "rp:1Cor.16.10 (Timothy commended)", "sbl:1Cor.16.10 (SBL variant site at the end of the verse)", "rp:1Cor.16.11 (Timothy sent on, close)", "rp:1Cor.16.12 (heading on the far side of the seam)", "sbl:1Cor.16.6 (SBL variant site)", "sbl:1Cor.16.7 (SBL variant site)", "sbl:1Cor.16.8 (SBL variant site)", "sbl:1Cor.16.11 (SBL variant site)"]

#### `W6-008.boundary_rationale` (S2-09)

Pinned: "Back face: the collection arrangements close at 16:4. Front face: rp:1Cor.16.5 \"Ἐλεύσομαι δὲ πρὸς ὑμᾶς,\" announces the apostle's coming after Macedonia, a travel statement. Interior: the delay in Ephesus up to the feast (16:8) and the open door of 16:9 explain the delay; at 16:10, rp:1Cor.16.10 \"Ἐὰν δὲ ἔλθῃ Τιμόθεος,\", the envoy Timothy is commended. RP pilcrow at 16:10 falls inside the unit. Close: 16:11 sends Timothy on with the brothers. Across the seam, 16:12 begins with a second peri de heading."

Expected after the orders: "Back face: the collection arrangements close at 16:4. Front face: rp:1Cor.16.5 \"Ἐλεύσομαι δὲ πρὸς ὑμᾶς,\" announces the apostle's coming after Macedonia, a travel statement. Interior: the delay in Ephesus up to the feast (16:8) and the open door of 16:9 explain the delay; at 16:10, rp:1Cor.16.10 \"Ἐὰν δὲ ἔλθῃ Τιμόθεος,\", the envoy Timothy is commended. Close: 16:11 sends Timothy on with the brothers. Across the seam, 16:12 begins with a second peri de heading."

#### `W6-008.observed_substrate_signals` (S2-09)

Pinned: ["travel statement (16:5)", "pentecost (16:8, metadata)", "RP pilcrow inside the unit (16:10)"]

Expected after the orders: ["travel statement (16:5)", "pentecost (16:8, metadata)", "RP pilcrow at 16:10"]

#### `W6-008.strongest_rejected_alternative` (S2-09)

Pinned: "Opening a separate unit at 16:10 on the conditional and the RP pilcrow: the apostle's plans and Timothy's coming answer one practical question, who is coming to Corinth and when, so the commendation stays with the itinerary."

Expected after the orders: "Opening a separate unit at 16:10 on the conditional: the apostle's plans and Timothy's coming answer one practical question, who is coming to Corinth and when, so the commendation stays with the itinerary."

#### `W6-009.boundary_rationale` (S2-06)

Pinned: "Back face: the envoy's commendation closes at 16:11. Front face: rp:1Cor.16.12 opens with the heading rp:1Cor.16.12 \"Περὶ δὲ Ἀπολλὼ τοῦ ἀδελφοῦ,\", a peri de topic marker. WEB renders it web:1Cor.16.12 “Now concerning Apollos the brother,” and opens a WEB paragraph at 16:12. Close: the report on Apollos's reluctance and later visit is complete within the verse. Across the seam, 16:13 rp:1Cor.16.13 \"Γρηγορεῖτε, στήκετε ἐν τῇ πίστει,\" opens a run of asyndetic imperatives addressed to the readers. RP pilcrow at 16:13 (close seam), with a WEB paragraph at 16:13 as well. One-verse justification: the heading and its answer occupy one verse, and the imperatives that follow change addressee and mood, so the topic stands alone."

Expected after the orders: "Back face: the envoy's commendation closes at 16:11. Front face: rp:1Cor.16.12 opens with the heading rp:1Cor.16.12 \"Περὶ δὲ Ἀπολλὼ τοῦ ἀδελφοῦ,\", a peri de topic marker. WEB renders it web:1Cor.16.12 “Now concerning Apollos the brother,”. Close: the report on Apollos's reluctance and later visit is complete within the verse. Across the seam, 16:13 rp:1Cor.16.13 \"Γρηγορεῖτε, στήκετε ἐν τῇ πίστει,\" opens a run of asyndetic imperatives addressed to the readers. RP pilcrow at 16:13 (close seam). One-verse justification: the heading and its answer occupy one verse, and the imperatives that follow change addressee and mood, so the topic stands alone."

#### `W6-011.boundary_evidence_refs` (S2-11)

Pinned: ["web:1Cor.16.15-1Cor.16.18 (span: appeal and commendation)", "rp:1Cor.16.14 (back face: love summary)", "rp:1Cor.16.15 (parakalo de hymas with vocative; RP pilcrow)", "rp:1Cor.16.18 (recognise such workers, close)", "rp:1Cor.16.19 (greeting formula opens the closing frame; RP pilcrow)", "rp:1Cor.16.13 (rival frame onset)", "rp:1Cor.16.12 (rival body end)", "sbl:1Cor.16.17 (SBL variant site)"]

Expected after the orders: ["web:1Cor.16.15-1Cor.16.18 (span: appeal and commendation)", "rp:1Cor.16.14 (back face: love summary)", "rp:1Cor.16.15 (parakalo de hymas with vocative)", "rp:1Cor.16.18 (recognise such workers, close)", "rp:1Cor.16.19 (greeting formula opens the closing frame)", "rp:1Cor.16.13 (rival frame onset)", "rp:1Cor.16.12 (rival body end)", "sbl:1Cor.16.17 (SBL variant site)"]

#### `W6-011.boundary_rationale` (S2-09)

Pinned: "Back face: the summary imperatives close at 16:14. Front face: rp:1Cor.16.15 \"Παρακαλῶ δὲ ὑμᾶς,\" is an appeal formula with vocative that introduces the household of Stephanas. RP pilcrow at 16:15 stands on the onset. Close: 16:18 ends the commendation with rp:1Cor.16.18 \"ἐπιγινώσκετε οὖν τοὺς τοιούτους.\", a call to recognise such workers. Across the seam, 16:19 opens the third-person greetings, rp:1Cor.16.19 \"Ἀσπάζονται ὑμᾶς αἱ ἐκκλησίαι τῆς Ἀσίας·\". RP pilcrow at 16:19 (close seam). The parent seam at 16:18/16:19 is contested against the rival edge at 16:13, and is listed for Fable's end review."

Expected after the orders: "Back face: the summary imperatives close at 16:14. Front face: rp:1Cor.16.15 \"Παρακαλῶ δὲ ὑμᾶς,\" is an appeal formula with vocative that introduces the household of Stephanas. Close: 16:18 ends the commendation with rp:1Cor.16.18 \"ἐπιγινώσκετε οὖν τοὺς τοιούτους.\", a call to recognise such workers. Across the seam, 16:19 opens the third-person greetings, rp:1Cor.16.19 \"Ἀσπάζονται ὑμᾶς αἱ ἐκκλησίαι τῆς Ἀσίας·\". The parent seam at 16:18/16:19 is contested against the rival edge at 16:13, and is listed for Fable's end review."

#### `W6-011.observed_substrate_signals` (S2-09)

Pinned: ["parakalo (16:15)", "parakalo_hymas (16:15)", "parakalo_de_hymas (16:15)", "adelphoi vocative (16:15)", "RP pilcrow (16:15)", "RP pilcrow on the close seam (16:19)"]

Expected after the orders: ["parakalo (16:15)", "parakalo_hymas (16:15)", "parakalo_de_hymas (16:15)", "adelphoi vocative (16:15)", "RP pilcrow at 16:15 and 16:19"]

#### `W6-012.boundary_evidence_refs` (S2-11)

Pinned: ["web:1Cor.16.19-1Cor.16.20 (span: third-person and imperative greetings)", "rp:1Cor.16.18 (back face: commendation close)", "rp:1Cor.16.19 (greet_third_person; RP pilcrow)", "sbl:1Cor.16.19 (SBL variant site: singular verb at the second greeting)", "rp:1Cor.16.20 (greet_imperative)", "rp:1Cor.16.21 (autograph opens the following unit; RP pilcrow)", "rp:1Cor.16.13 (rival frame onset)"]

Expected after the orders: ["web:1Cor.16.19-1Cor.16.20 (span: third-person and imperative greetings)", "rp:1Cor.16.18 (back face: commendation close)", "rp:1Cor.16.19 (greet_third_person)", "sbl:1Cor.16.19 (SBL variant site: singular verb at the second greeting)", "rp:1Cor.16.20 (greet_imperative)", "rp:1Cor.16.21 (autograph opens the following unit)", "rp:1Cor.16.13 (rival frame onset)"]

#### `W6-012.boundary_rationale` (S2-09)

Pinned: "Back face: the commendation closes at 16:18 with a call to recognise such workers. Front face: rp:1Cor.16.19 \"Ἀσπάζονται ὑμᾶς αἱ ἐκκλησίαι τῆς Ἀσίας·\" opens the third-person greetings from the churches of Asia, web:1Cor.16.19 “The assemblies of Asia greet you.” The greeting formula carries the onset. Interior: 16:20 adds the greeting of the brothers and the command rp:1Cor.16.20 \"Ἀσπάσασθε ἀλλήλους ἐν φιλήματι ἁγίῳ.\". Close: the greetings end at 16:20; at 16:21 the autograph, rp:1Cor.16.21 \"Ὁ ἀσπασμὸς τῇ ἐμῇ χειρὶ Παύλου.\", begins. RP pilcrow at 16:21 (close seam)."

Expected after the orders: "Back face: the commendation closes at 16:18 with a call to recognise such workers. Front face: rp:1Cor.16.19 \"Ἀσπάζονται ὑμᾶς αἱ ἐκκλησίαι τῆς Ἀσίας·\" opens the third-person greetings from the churches of Asia, web:1Cor.16.19 “The assemblies of Asia greet you.” The greeting formula carries the onset. Interior: 16:20 adds the greeting of the brothers and the command rp:1Cor.16.20 \"Ἀσπάσασθε ἀλλήλους ἐν φιλήματι ἁγίῳ.\". Close: the greetings end at 16:20; at 16:21 the autograph, rp:1Cor.16.21 \"Ὁ ἀσπασμὸς τῇ ἐμῇ χειρὶ Παύλου.\", begins."

#### `W6-012.observed_substrate_signals` (S2-09)

Pinned: ["greet_third_person (16:19, 16:20)", "greet_imperative (16:20)", "adelphoi, articular nominative (16:20)", "RP pilcrow (16:19)", "close-seam RP pilcrow (16:21)"]

Expected after the orders: ["greet_third_person (16:19, 16:20)", "greet_imperative (16:20)", "adelphoi, articular nominative (16:20)", "RP pilcrow at 16:19 and 16:21"]

#### `W6-013.boundary_rationale` (S2-06)

Pinned: "Back face: the greetings close at 16:20 with the holy kiss. Front face: rp:1Cor.16.21 \"Ὁ ἀσπασμὸς τῇ ἐμῇ χειρὶ Παύλου.\" marks the autograph, web:1Cor.16.21 “This greeting is by me, Paul, with my own hand.” The autograph has an RP pilcrow at 16:21 and WEB likewise opens a paragraph at 16:21. Interior: 16:22 pronounces the curse and the acclamation, and opens no unit. Close: 16:23 turns to the grace benediction, rp:1Cor.16.23 \"Ἡ χάρις τοῦ κυρίου\"."

Expected after the orders: "Back face: the greetings close at 16:20 with the holy kiss. Front face: rp:1Cor.16.21 \"Ὁ ἀσπασμὸς τῇ ἐμῇ χειρὶ Παύλου.\" marks the autograph, web:1Cor.16.21 “This greeting is by me, Paul, with my own hand.” The autograph has an RP pilcrow at 16:21. Interior: 16:22 pronounces the curse and the acclamation, and opens no unit. Close: 16:23 turns to the grace benediction, rp:1Cor.16.23 \"Ἡ χάρις τοῦ κυρίου\"."

Verify each expected value yourself against the order and the pinned bytes (a script: apply the exact span edit, compare).
If you find an expected value that does not follow from the order as written, do not improvise and do not emit a
different text: leave that field at its pinned value and report it in the change log as `blocked` with the measured
evidence. Every field not listed stays byte-identical as a JSON value.

## Suite duties your new text must keep (the suite is the mechanical judge)

- placeholder: no unfilled template placeholder (%s, %(x)s, {name}, {0}, {}) in any field of any row.
- Never hand-type Greek: every Greek run in the rows stays byte-identical; you add none.
- WEB quotations stay as they are: sliced from `SP\1Cor\1Cor_web_clean.txt`, in double curly quotes, attributed (the
  A6-b convention); you add none.
- register rule: this is a scholar-facing record; no staged file names, internal rule labels, ruling ids, row pointers
  or process talk in row prose.
- single-witness: keep the literal single-witness disclosure wherever a row already carries it.
- A mark is cited at the verse it FOLLOWS; do not re-cite marks.
- A categorical claim ("no", "only", "every") stands only if the thing is absent from BOTH witnesses (C2-amended); add
  none.
- 7-gram: add no run of seven words that repeats across rows (CWO-1COR-03).
- Refs: the DEF-A4-ARGUED entries, each ROLE token, face qualifier and seam pair in boundary_evidence_refs stay; only
  the listed annotation spans change; no element is removed.
- language_zones and cap_sweep are out of scope (no seam moves).

## How you check your work (in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W6\work\`)

1. Copy `SP\1Cor\fixup\draft_rows_fixup1_applied.jsonl` byte-identically to `work\rows_applied.jsonl` and replace your
   part's changed rows with your revised rows (same order).
2. RUN `run_validator_suite.py work\rows_applied.jsonl`: hard_status GREEN, every member GREEN, triage_flags 0.
3. RUN `ngram7.py work\rows_applied.jsonl --gate 10 --full-ids`: no offending gram.
4. RUN `check_tiling.py work\rows_applied.jsonl --range 1Cor.1.1-1Cor.16.24`: GREEN, 437 of 437.
5. RUN `cwo_sweep_1cor.py work\rows_applied.jsonl --out work\cwo.json`: on your rows A 0 and CWO-1COR-04 support_use and
   count_excess 0 (W6 only: the W6-013 boundary_rationale flag noted above may remain).
6. Write your part's rows to `work\slice_W6.jsonl` and RUN `_validate_writer_part_1cor.py work\slice_W6.jsonl
   --part W6 --book-index`: GREEN.
7. Confirm by script that every revised field equals its expected value above and every other field is byte-identical (as a JSON value) to the pinned rows.

## Deliverables

- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W6\fixup2_W6_rows.jsonl`: one JSON object per line, the FULL revised row for every row you changed (and only those), in the
  pinned rows' order, every untouched field byte-identical as a JSON value.
- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W6\fixup2_W6_changes.json`:

```
{"attempt_id":"cor_fixup2_W6_a1","execution_id":"cor_fixup2_W6_a1#e1","rows_file_sha256":"<pinned rows digest>",
 "changes":[{"row":"<id>","field":"<field>","order":"<ruling id>","before":"<exact removed span>","after":"<exact new span or empty>",
             "tier":"MEASURED|INFERRED","evidence":"<script + input + output>"}],
 "blocked":[{"order":"<ruling id>","why":"...","evidence":"..."}],
 "checks":{"suite":"<hard_status and members>","ngram7":"...","tiling":"...","cwo":"...","part_validator":"...","expected_match":true}}
```

## Budget

Keep to roughly 20 tool calls. Report exactly what you ran and what it returned.

## Efficiency contract

M8-EFFICIENCY-V1
EFFICIENCY-CONTRACT: C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md sha256 4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66
Save each complete bounded review unit and exact next cursor in your authorized OUT; partial output is not acceptance. Preserve the unchanged legacy final deliverable contract.
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W6

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"cor_fixup2_W6_a1","execution_id":"cor_fixup2_W6_a1#e1",
 "sources":["<exact paths you read, with sha256>"],
 "outcome":{"changed":[{"what":"<row.field>","why":"<ruling id>"}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search, read no transcript; read only the exact paths named",
 "rows_sha256":"<sha256 of fixup2_W6_rows.jsonl>","changes_sha256":"<sha256 of fixup2_W6_changes.json>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
