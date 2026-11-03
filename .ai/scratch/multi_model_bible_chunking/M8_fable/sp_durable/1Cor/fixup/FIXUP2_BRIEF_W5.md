# FIXUP-2 AUTHOR BRIEF, part W5 (execution #e1): 1 Corinthians, span-exact ruled row repairs (M8_fable, OW-36 queue)

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

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W5` already exists. Write your deliverables directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W5\fixup2_W5_rows.jsonl` and `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W5\fixup2_W5_changes.json`. **Never run any existence check, listing, glob or recursive search against it or any
other directory.** A shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W5\work\`, created with
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

You are the FIXUP-2 AUTHOR for part W5. Attempt `cor_fixup2_W5_a1`, execution `cor_fixup2_W5_a1#e1`. You authored none of the rows, the
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
- `SP\1Cor\writer_lanes\_validate_writer_part_1cor.py`: RUN on a slice of your private copy holding only your part's rows, with `--part W5 --book-index` (it writes nothing).
- `SP\campaign\grader_models.v1.json`: READ where you check your model role (grader_fallback).
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 3412-3434 only (OW-36, the owner's grant).

## The orders to part W5 (quoted from the rulings file, sha256 1299a598b60bbf3c8fb193381ead098e394242a713d8bac4e584b39fdf0e0541)

### S2-01

Decision (verbatim): Adopt the queue proposal. W5-010.strongest_rejected_alternative loses the WEB-paragraph clause; the rival cut at 14:15 stays and is argued only from the question.

Your order (verbatim): W5-010.strongest_rejected_alternative: delete the exact span; the sentence then reads 'A cut at 14:15, where the question Ti oun estin (transliterated gloss) is asked, would split the instruction from its resolution.' The field is already licensed by round-1 S1-02b.

Exact spans (verbatim): ["WEB opens a paragraph and "]

### S2-03

Decision (verbatim): Adopt. Delete the remaining WEB-paragraph clause from W5-008.boundary_rationale.

Your order (verbatim): W5-008.boundary_rationale: delete the exact span, so the sentence ends after 'analogies'.

Exact spans (verbatim): [", and WEB opens a paragraph there"]

### S2-04

Decision (verbatim): Ratify with changes. S1-02b is extended by name to W5-004 and W5-005.boundary_rationale, which are licensed for these deletions only. The bare observed_substrate_signals items 'WEB paragraph at X' in W5-004..W5-009 are location items and stay, with no order.

Your order (verbatim): This licenses, in words, the named field(s) of the named row(s) for this edit only; the round-1 licence did not cover them. W5-004.boundary_rationale: delete the exact span; the sentence then begins 'Onset at 12:27 with Ὑμεῖς δέ ...'.

Exact spans (verbatim): [", a WEB paragraph,"]

### S2-04

Decision (verbatim): Ratify with changes. S1-02b is extended by name to W5-004 and W5-005.boundary_rationale, which are licensed for these deletions only. The bare observed_substrate_signals items 'WEB paragraph at X' in W5-004..W5-009 are location items and stay, with no order.

Your order (verbatim): This licenses, in words, the named field(s) of the named row(s) for this edit only; the round-1 licence did not cover them. W5-005.boundary_rationale: delete the first exact span (the sentence then begins 'Onset at 13:1 with Ἐὰν ...') and delete the whole second sentence.

Exact spans (verbatim): [", a WEB paragraph,", "WEB opens a paragraph at 13:4."]

### S2-10

Decision (verbatim): Adopt S1-01 as written. Pilcrow prose is deleted from W5-001.strongest_rejected_alternative, W5-012.boundary_rationale and W5-013.boundary_rationale; the pilcrow stays only as the single oss item. This is substrate-signal wording only; no reading, slogan attribution or interpretation is chosen. The 14:34 rows are touched for pilcrow wording only; the 14:34-35 question is not addressed.

Your order (verbatim): W5-001.strongest_rejected_alternative: delete the whole first exact span (a sentence). W5-012.boundary_rationale: delete the second exact span. W5-013.boundary_rationale: delete the third exact span; the sentence then begins 'Onset at 14:34 with Αἱ γυναῖκες ...'.

Exact spans (verbatim): ["The RP pilcrow at 12:4 marks the turn to varieties of gifts.", ", and an RP pilcrow stands at 14:34", ", which carries an RP pilcrow,"]

### S2-11

Decision (verbatim): Rule that S1-01's 'at most once per row' counts every pilcrow mention in the row, ref annotations included. License annotation edits that strip the pilcrow words from the ref elements of the S1-01 and S1-01b rows. S1-01 itself stands as written and is not relaxed; its strictness beyond rule 5 is recorded as a method-change candidate for the end review.

Your order (verbatim): This licenses, in words, an edit of the annotation text of the named boundary_evidence_refs element(s) only; the ref id, the ref locator and the bracketed tag stay byte-identical, and no element is added or removed unless this order says so. Delete the exact span from W5-001.ber[2], W5-003.ber[0], W5-010.ber[3], W5-011.ber[0], W5-011.ber[3], W5-012.ber[0], W5-012.ber[3], W5-013.ber[0], W5-013.ber[3] and W5-014.ber[0].

Exact spans (verbatim): [", RP pilcrow"]

### CWO-1COR-01 (corpus-wide order)

Predicate (verbatim): `A: an element of boundary_evidence_refs matching ^\s*web: and matching (?i)WEB paragraph|paragraph start|DISCLOSURE-mark. B: a sentence (split on (?<=[.;])\s+) of boundary_rationale, strongest_rejected_alternative or device_notes matching (?i)pilcrow|WEB paragraph|paragraph start|chapter division and also matching (?i)corroborat|agree|join|inform|favour|support|lean|confirm.`

Fields (verbatim): boundary_evidence_refs, boundary_rationale, strongest_rejected_alternative, device_notes; all 70 rows of SP\1Cor\writer\draft_rows_combined.jsonl

Remedy (verbatim): Every A hit is deleted (a web: ref is never boundary evidence, rule 4). Every B hit is classified support-use (a WEB paragraph or chapter division informing, agreeing, joining, corroborating, leaning, favouring, supporting or confirming; or a pilcrow agreeing, joining, corroborating or confirming) or compliant (a disclaimer that the mark does not drive the seam, or an RP pilcrow that informs without deciding). Support-use clauses are deleted by the owning part. If a deletion leaves boundary_evidence_refs below what the suite accepts, the author stops and reports.

### CWO-1COR-02 (corpus-wide order)

Predicate (verbatim): `A row whose string fields outside boundary_evidence_refs contain a character in [\u0370-\u03FF\u1F00-\u1FFF] must contain both literal substrings 'Robinson-Pierpont Byzantine Textform (Unlicense)' and 'SBLGNT (CC BY 4.0)'.`

Fields (verbatim): every string field that ngram7.prose() walks, plus boundary_evidence_refs excluded from the Greek test; all 70 rows

Remedy (verbatim): Each failing row is given the S1-04 remedy by its owning part, unsalted.

### CWO-1COR-03 (corpus-wide order)

Predicate (verbatim): `ngram7 as installed with TF-2, default gate 10, --full-ids, on the applied combined rows: any 7-gram shared by 10 or more rows.`

Fields (verbatim): the fields ngram7.prose() walks

Remedy (verbatim): Each offending gram goes back to its owning parts with the named rows; reword, never exclude.

### CWO-1COR-04 (corpus-wide order)

Predicate (verbatim): `Over sentences of the S fields (split on (?<=[.;])\s+) and each element of the L fields (non-string elements json.dumps'd): W = (?i)\bWEB\b[^.;]{0,40}?\bparagraph(?: starts?)?|\bparagraph starts?\b|\bchapter (?:division|break)s?\b ; P = (?i)pilcrow|\bparagraph marks?\b ; DIS = (?i)not weighed|formatting|decides? nothing|does not decide|do not decide|never drives?|neither drives? nor corroborates?|excluded|not (?:drive|corroborate)|without deciding|informs? and does not decide ; PD2 = (?i)corroborat|agree|\bjoin|confirm|support|favou?r|\blean|points? to|(?<!paragraph )(?<!-)\bmark(?:s|ed|ing)?\b|\bsignal|establish|determin ; VERB = (?i)\b(?:falls?|stands?|sits?|opens?|starts?|breaks?|coincides?|points?|agrees?|marks?|as well|likewise|too|same|also)\b. A W hit is disclosure_only if DIS matches the unit; it is location_only if the unit is an observed_substrate_signals item and VERB does not match the unit with the W matches removed; otherwise it is support_use (presence and absence forms alike). A P hit is support_use if PD2 matches, and informs_compliant if only DIS matches; otherwise it is not listed. In rows W5-001, 002, 003, 010, 011, 012, 013, 014 and W6-002, 003, 008, 011, 012 (round-1 S1-01/S1-01b), every P mention other than the first observed_substrate_signals P item is count_excess.`

Fields (verbatim): S fields: boundary_rationale, strongest_rejected_alternative, device_notes. L fields: observed_substrate_signals, boundary_evidence_refs (annotation text; ids and tags are scanned but never edited).

Remedy (verbatim): Delete the supporting clause or crediting verb and keep the content. Every rival location stays. A crediting verb on a pilcrow becomes a locating verb. count_excess mentions are deleted, with oss items merged into one bare location item. The exact spans are in rulings S2-01..S2-12 and S2-15.

### CWO-1COR-04 support-use and count-excess hits on your rows (MEASURED by the installed sweep on the pinned rows; hand classes by the orchestrator)

- `W5-001.strongest_rejected_alternative` P support_use (true_ordered; ordered by S2-10)
- `W5-001.strongest_rejected_alternative` CNT count_excess (true_ordered; ordered by S2-10)
- `W5-001.boundary_evidence_refs[2]` CNT count_excess (true_ordered; ordered by S2-11)
- `W5-003.boundary_evidence_refs[0]` CNT count_excess (true_ordered; ordered by S2-11)
- `W5-004.boundary_rationale` W support_use (true_ordered; ordered by S2-04)
- `W5-005.boundary_rationale` W support_use (true_ordered; ordered by S2-04)
- `W5-005.boundary_rationale` W support_use (true_ordered; ordered by S2-04)
- `W5-008.boundary_rationale` W support_use (true_ordered; ordered by S2-03)
- `W5-010.strongest_rejected_alternative` W support_use (true_ordered; ordered by S2-01)
- `W5-010.boundary_evidence_refs[3]` CNT count_excess (true_ordered; ordered by S2-11)
- `W5-011.boundary_evidence_refs[0]` CNT count_excess (true_ordered; ordered by S2-11)
- `W5-011.boundary_evidence_refs[3]` CNT count_excess (true_ordered; ordered by S2-11)
- `W5-012.boundary_rationale` CNT count_excess (true_ordered; ordered by S2-10)
- `W5-012.boundary_evidence_refs[0]` CNT count_excess (true_ordered; ordered by S2-11)
- `W5-012.boundary_evidence_refs[3]` CNT count_excess (true_ordered; ordered by S2-11)
- `W5-013.boundary_rationale` CNT count_excess (true_ordered; ordered by S2-10)
- `W5-013.boundary_evidence_refs[0]` CNT count_excess (true_ordered; ordered by S2-11)
- `W5-013.boundary_evidence_refs[3]` CNT count_excess (true_ordered; ordered by S2-11)
- `W5-014.boundary_evidence_refs[0]` CNT count_excess (true_ordered; ordered by S2-11)

## The edits, one per line (the orders above, as operations on the pinned rows)

- `W5-010.strongest_rejected_alternative` (S2-01) del delete "WEB opens a paragraph and "
- `W5-008.boundary_rationale` (S2-03) del delete ", and WEB opens a paragraph there"
- `W5-004.boundary_rationale` (S2-04) del delete ", a WEB paragraph,"
- `W5-005.boundary_rationale` (S2-04) del delete ", a WEB paragraph,"
- `W5-005.boundary_rationale` (S2-04) del delete "WEB opens a paragraph at 13:4." (a whole sentence, with one adjoining space)
- `W5-001.strongest_rejected_alternative` (S2-10) del delete "The RP pilcrow at 12:4 marks the turn to varieties of gifts." (a whole sentence, with one adjoining space)
- `W5-012.boundary_rationale` (S2-10) del delete ", and an RP pilcrow stands at 14:34"
- `W5-013.boundary_rationale` (S2-10) del delete ", which carries an RP pilcrow,"
- `W5-001.boundary_evidence_refs[2]` (S2-11) del delete ", RP pilcrow"
- `W5-003.boundary_evidence_refs[0]` (S2-11) del delete ", RP pilcrow"
- `W5-010.boundary_evidence_refs[3]` (S2-11) del delete ", RP pilcrow"
- `W5-011.boundary_evidence_refs[0]` (S2-11) del delete ", RP pilcrow"
- `W5-011.boundary_evidence_refs[3]` (S2-11) del delete ", RP pilcrow"
- `W5-012.boundary_evidence_refs[0]` (S2-11) del delete ", RP pilcrow"
- `W5-012.boundary_evidence_refs[3]` (S2-11) del delete ", RP pilcrow"
- `W5-013.boundary_evidence_refs[0]` (S2-11) del delete ", RP pilcrow"
- `W5-013.boundary_evidence_refs[3]` (S2-11) del delete ", RP pilcrow"
- `W5-014.boundary_evidence_refs[0]` (S2-11) del delete ", RP pilcrow"

MEASURED (the orchestrator's script applied every part's edits to a scratch copy of the pinned rows): suite hard_status
GREEN with every member GREEN, triage_flags 0; ngram7 GREEN, 0 offending grams; tiling GREEN 437/437; CWO-1COR-01 A 0;
CWO-1COR-02 0 of 70; CWO-1COR-04 support-use and count-excess 0 except W6-013 boundary_rationale, which the sweep still
flags because the sentence on the Greek greeting ("... marks the autograph") shares a sentence span with the pilcrow
clause (a known split artifact, classed false_positive in the coverage report). That flag is the orchestrator's to
re-class; it is not yours to edit around.

## What you may change (the lander refuses any other difference)

Each licensed field, with its pinned value and the value the orders produce, as JSON values:

#### `W5-001.boundary_evidence_refs` (S2-11)

Pinned: ["rp:1Cor.12.1 [WARRANT-onset:near] heading with disclosure formula", "rp:1Cor.11.34 [WARRANT-onset:far] deferral of remaining matters to the visit", "rp:1Cor.12.4 [WARRANT-close:far] varieties of gifts, RP pilcrow", "web:1Cor.12.1-1Cor.12.3 (unit span)", "sbl:1Cor.12.3 (SBL wording of the consequence clause compared)"]

Expected after the orders: ["rp:1Cor.12.1 [WARRANT-onset:near] heading with disclosure formula", "rp:1Cor.11.34 [WARRANT-onset:far] deferral of remaining matters to the visit", "rp:1Cor.12.4 [WARRANT-close:far] varieties of gifts", "web:1Cor.12.1-1Cor.12.3 (unit span)", "sbl:1Cor.12.3 (SBL wording of the consequence clause compared)"]

#### `W5-001.strongest_rejected_alternative` (S2-10)

Pinned: "Merging 12:1-12:11 into one unit would keep the heading with the opening exposition of gifts, since 12:4 elaborates the Spirit named at 12:3. It is set aside because the confession test of 12:3 closes a self-contained criterion. The RP pilcrow at 12:4 marks the turn to varieties of gifts."

Expected after the orders: "Merging 12:1-12:11 into one unit would keep the heading with the opening exposition of gifts, since 12:4 elaborates the Spirit named at 12:3. It is set aside because the confession test of 12:3 closes a self-contained criterion."

#### `W5-003.boundary_evidence_refs` (S2-11)

Pinned: ["rp:1Cor.12.12 [WARRANT-onset:near] body analogy, RP pilcrow", "rp:1Cor.12.11 [WARRANT-onset:far] inclusio close of the gifts exposition", "rp:1Cor.12.26 [WARRANT-close:near] mutual-care conclusion", "rp:1Cor.12.27 [WARRANT-close:far] application to the addressees", "web:1Cor.12.12-1Cor.12.26 (unit span)", "sbl:1Cor.12.26 (SBL wording of the conclusion compared)"]

Expected after the orders: ["rp:1Cor.12.12 [WARRANT-onset:near] body analogy", "rp:1Cor.12.11 [WARRANT-onset:far] inclusio close of the gifts exposition", "rp:1Cor.12.26 [WARRANT-close:near] mutual-care conclusion", "rp:1Cor.12.27 [WARRANT-close:far] application to the addressees", "web:1Cor.12.12-1Cor.12.26 (unit span)", "sbl:1Cor.12.26 (SBL wording of the conclusion compared)"]

#### `W5-004.boundary_rationale` (S2-04)

Pinned: "Onset at 12:27, a WEB paragraph, with Ὑμεῖς δέ ἐστε σῶμα χριστοῦ (rp:1Cor.12.27), which applies the body image to the addressees directly. The ranked list of appointed roles follows at 12:28, and the rhetorical questions of 12:29-12:30 open with Μὴ πάντες ἀπόστολοι (rp:1Cor.12.29). The unit closes at 12:31 with the exhortation Ζηλοῦτε δὲ τὰ χαρίσματα τὰ (rp:1Cor.12.31). At 12:31 SBL reads τὰ ⸀μείζονα (sbl:1Cor.12.31) in place of the RP comparative. The second half of 12:31, Καὶ ἔτι καθ’ ὑπερβολὴν ὁδὸν ὑμῖν δείκνυμι (rp:1Cor.12.31), announces the way described in 13:1-13:13 and is kept with chapter 12 here; that attachment stays open."

Expected after the orders: "Onset at 12:27 with Ὑμεῖς δέ ἐστε σῶμα χριστοῦ (rp:1Cor.12.27), which applies the body image to the addressees directly. The ranked list of appointed roles follows at 12:28, and the rhetorical questions of 12:29-12:30 open with Μὴ πάντες ἀπόστολοι (rp:1Cor.12.29). The unit closes at 12:31 with the exhortation Ζηλοῦτε δὲ τὰ χαρίσματα τὰ (rp:1Cor.12.31). At 12:31 SBL reads τὰ ⸀μείζονα (sbl:1Cor.12.31) in place of the RP comparative. The second half of 12:31, Καὶ ἔτι καθ’ ὑπερβολὴν ὁδὸν ὑμῖν δείκνυμι (rp:1Cor.12.31), announces the way described in 13:1-13:13 and is kept with chapter 12 here; that attachment stays open."

#### `W5-005.boundary_rationale` (S2-04)

Pinned: "Onset at 13:1, a WEB paragraph, with Ἐὰν ταῖς γλώσσαις τῶν ἀνθρώπων λαλῶ (rp:1Cor.13.1), the conditional that sets the pattern of the inset. The refrain ἀγάπην δὲ μὴ ἔχω (rp:1Cor.13.1) recurs in 13:2 and 13:3, so the three verses form one anaphoric set of hypotheticals. The verse before, 12:31, promises a way beyond the gifts; this onset makes good on that promise, which is why the attachment of 12:31b stays open. Close after 13:3: the conditionals in the speaker's voice give way to predicates of love with Ἡ ἀγάπη μακροθυμεῖ (rp:1Cor.13.4). WEB opens a paragraph at 13:4."

Expected after the orders: "Onset at 13:1 with Ἐὰν ταῖς γλώσσαις τῶν ἀνθρώπων λαλῶ (rp:1Cor.13.1), the conditional that sets the pattern of the inset. The refrain ἀγάπην δὲ μὴ ἔχω (rp:1Cor.13.1) recurs in 13:2 and 13:3, so the three verses form one anaphoric set of hypotheticals. The verse before, 12:31, promises a way beyond the gifts; this onset makes good on that promise, which is why the attachment of 12:31b stays open. Close after 13:3: the conditionals in the speaker's voice give way to predicates of love with Ἡ ἀγάπη μακροθυμεῖ (rp:1Cor.13.4)."

#### `W5-008.boundary_rationale` (S2-03)

Pinned: "Onset at 14:1 with Διώκετε τὴν ἀγάπην (rp:1Cor.14.1). The same verse continues with ζηλοῦτε δὲ τὰ πνευματικά (rp:1Cor.14.1), taking up the exhortation of 12:31 after the inset. The unit sets prophecy above uninterpreted tongues by the criterion of building up the gathering, and 14:5 closes it with ἵνα ἡ ἐκκλησία οἰκοδομὴν λάβῃ (rp:1Cor.14.5). At 14:6 Νυνὶ δέ, ἀδελφοί (rp:1Cor.14.6) begins a hypothetical visit and a run of analogies, and WEB opens a paragraph there."

Expected after the orders: "Onset at 14:1 with Διώκετε τὴν ἀγάπην (rp:1Cor.14.1). The same verse continues with ζηλοῦτε δὲ τὰ πνευματικά (rp:1Cor.14.1), taking up the exhortation of 12:31 after the inset. The unit sets prophecy above uninterpreted tongues by the criterion of building up the gathering, and 14:5 closes it with ἵνα ἡ ἐκκλησία οἰκοδομὴν λάβῃ (rp:1Cor.14.5). At 14:6 Νυνὶ δέ, ἀδελφοί (rp:1Cor.14.6) begins a hypothetical visit and a run of analogies."

#### `W5-010.boundary_evidence_refs` (S2-11)

Pinned: ["rp:1Cor.14.13 [WARRANT-onset:near] inferential prescription", "rp:1Cor.14.12 [WARRANT-onset:far] framing repetition", "rp:1Cor.14.19 [WARRANT-close:near] preference for intelligible words", "rp:1Cor.14.20 [WARRANT-close:far] vocative appeal, RP pilcrow", "web:1Cor.14.13-1Cor.14.19 (unit span)", "sbl:1Cor.14.18 (SBL wording of the thanksgiving compared)", "web:1Cor.14.26 (named in the prose)"]

Expected after the orders: ["rp:1Cor.14.13 [WARRANT-onset:near] inferential prescription", "rp:1Cor.14.12 [WARRANT-onset:far] framing repetition", "rp:1Cor.14.19 [WARRANT-close:near] preference for intelligible words", "rp:1Cor.14.20 [WARRANT-close:far] vocative appeal", "web:1Cor.14.13-1Cor.14.19 (unit span)", "sbl:1Cor.14.18 (SBL wording of the thanksgiving compared)", "web:1Cor.14.26 (named in the prose)"]

#### `W5-010.strongest_rejected_alternative` (S2-01)

Pinned: "A cut at 14:15, where WEB opens a paragraph and the question Ti oun estin (transliterated gloss) is asked, would split the instruction from its resolution. The question answers the problem just posed, so it stays inside the unit; the same question at 14:26 does open a unit, since there it carries the vocative adelphoi (transliterated gloss) and leads into instructions for the gathering."

Expected after the orders: "A cut at 14:15, where the question Ti oun estin (transliterated gloss) is asked, would split the instruction from its resolution. The question answers the problem just posed, so it stays inside the unit; the same question at 14:26 does open a unit, since there it carries the vocative adelphoi (transliterated gloss) and leads into instructions for the gathering."

#### `W5-011.boundary_evidence_refs` (S2-11)

Pinned: ["rp:1Cor.14.20 [WARRANT-onset:near] vocative appeal, RP pilcrow", "rp:1Cor.14.19 [WARRANT-onset:far] preference for intelligible words", "rp:1Cor.14.25 [WARRANT-close:near] outsider confession", "rp:1Cor.14.26 [WARRANT-close:far] question formula with vocative, RP pilcrow", "web:1Cor.14.20-1Cor.14.25 (unit span)", "sbl:1Cor.14.25 (SBL word order of the confession differs)"]

Expected after the orders: ["rp:1Cor.14.20 [WARRANT-onset:near] vocative appeal", "rp:1Cor.14.19 [WARRANT-onset:far] preference for intelligible words", "rp:1Cor.14.25 [WARRANT-close:near] outsider confession", "rp:1Cor.14.26 [WARRANT-close:far] question formula with vocative", "web:1Cor.14.20-1Cor.14.25 (unit span)", "sbl:1Cor.14.25 (SBL word order of the confession differs)"]

#### `W5-012.boundary_evidence_refs` (S2-11)

Pinned: ["rp:1Cor.14.26 [WARRANT-onset:near] question formula with vocative, RP pilcrow", "rp:1Cor.14.25 [WARRANT-onset:far] outsider confession", "rp:1Cor.14.33 [WARRANT-close:near] ground with the 14:33b clause", "rp:1Cor.14.34 [WARRANT-close:far] asyndetic new subject, RP pilcrow", "web:1Cor.14.26-1Cor.14.33 (unit span)", "sbl:1Cor.14.34 (SBL wording across the close differs)", "web:1Cor.14.35 (named in the prose)", "web:1Cor.14.40 (named in the prose)"]

Expected after the orders: ["rp:1Cor.14.26 [WARRANT-onset:near] question formula with vocative", "rp:1Cor.14.25 [WARRANT-onset:far] outsider confession", "rp:1Cor.14.33 [WARRANT-close:near] ground with the 14:33b clause", "rp:1Cor.14.34 [WARRANT-close:far] asyndetic new subject", "web:1Cor.14.26-1Cor.14.33 (unit span)", "sbl:1Cor.14.34 (SBL wording across the close differs)", "web:1Cor.14.35 (named in the prose)", "web:1Cor.14.40 (named in the prose)"]

#### `W5-012.boundary_rationale` (S2-10)

Pinned: "Onset at 14:26 with Τί οὖν ἐστίν, ἀδελφοί (rp:1Cor.14.26), a vocative question that turns from argument to orderly practice. The governing principle stands in the same verse: Πάντα πρὸς οἰκοδομὴν γινέσθω (rp:1Cor.14.26). Orders for tongues and prophecy follow at 14:27-14:32, closing on καὶ πνεύματα προφητῶν προφήταις ὑποτάσσεται (rp:1Cor.14.32). At 14:33 the ground is given: Οὐ γάρ ἐστιν ἀκαταστασίας ὁ θεός, ἀλλὰ εἰρήνης (rp:1Cor.14.33). The verse continues with ὡς ἐν πάσαις ταῖς ἐκκλησίαις τῶν ἁγίων (rp:1Cor.14.33), and that clause is attached backward here to the ground it illustrates. Close after 14:33: at 14:34 a new subject enters without a connective, and an RP pilcrow stands at 14:34."

Expected after the orders: "Onset at 14:26 with Τί οὖν ἐστίν, ἀδελφοί (rp:1Cor.14.26), a vocative question that turns from argument to orderly practice. The governing principle stands in the same verse: Πάντα πρὸς οἰκοδομὴν γινέσθω (rp:1Cor.14.26). Orders for tongues and prophecy follow at 14:27-14:32, closing on καὶ πνεύματα προφητῶν προφήταις ὑποτάσσεται (rp:1Cor.14.32). At 14:33 the ground is given: Οὐ γάρ ἐστιν ἀκαταστασίας ὁ θεός, ἀλλὰ εἰρήνης (rp:1Cor.14.33). The verse continues with ὡς ἐν πάσαις ταῖς ἐκκλησίαις τῶν ἁγίων (rp:1Cor.14.33), and that clause is attached backward here to the ground it illustrates. Close after 14:33: at 14:34 a new subject enters without a connective."

#### `W5-013.boundary_evidence_refs` (S2-11)

Pinned: ["rp:1Cor.14.34 [WARRANT-onset:near] asyndetic new subject, RP pilcrow", "rp:1Cor.14.33 [WARRANT-onset:far] ground with the 14:33b clause", "rp:1Cor.14.36 [WARRANT-close:near] double question attached backward", "rp:1Cor.14.37 [WARRANT-close:far] conditional, RP pilcrow", "web:1Cor.14.34-1Cor.14.36 (unit span)", "sbl:1Cor.14.34 (SBL readings at the instruction)", "sbl:1Cor.14.35 (SBL readings in the follow-up)", "web:1Cor.14.40 (named in the prose)"]

Expected after the orders: ["rp:1Cor.14.34 [WARRANT-onset:near] asyndetic new subject", "rp:1Cor.14.33 [WARRANT-onset:far] ground with the 14:33b clause", "rp:1Cor.14.36 [WARRANT-close:near] double question attached backward", "rp:1Cor.14.37 [WARRANT-close:far] conditional", "web:1Cor.14.34-1Cor.14.36 (unit span)", "sbl:1Cor.14.34 (SBL readings at the instruction)", "sbl:1Cor.14.35 (SBL readings in the follow-up)", "web:1Cor.14.40 (named in the prose)"]

#### `W5-013.boundary_rationale` (S2-10)

Pinned: "Onset at 14:34, which carries an RP pilcrow, with Αἱ γυναῖκες ὑμῶν ἐν ταῖς ἐκκλησίαις (rp:1Cor.14.34): a new subject enters without a connective after the ground stated in 14:33. At 14:34 SBL reads Αἱ ⸀γυναῖκες ἐν ταῖς ἐκκλησίαις (sbl:1Cor.14.34), omitting the possessive. The instruction continues in 14:35 with Εἰ δέ τι μαθεῖν θέλουσιν (rp:1Cor.14.35). At 14:36 the double question Ἢ ἀφ’ ὑμῶν ὁ λόγος τοῦ θεοῦ ἐξῆλθεν (rp:1Cor.14.36) challenges the addressees and is attached backward here, as a retort that closes the instruction; this attachment is INFERRED. Close after 14:36: 14:37 opens a conditional with Εἴ τις δοκεῖ προφήτης εἶναι (rp:1Cor.14.37)."

Expected after the orders: "Onset at 14:34 with Αἱ γυναῖκες ὑμῶν ἐν ταῖς ἐκκλησίαις (rp:1Cor.14.34): a new subject enters without a connective after the ground stated in 14:33. At 14:34 SBL reads Αἱ ⸀γυναῖκες ἐν ταῖς ἐκκλησίαις (sbl:1Cor.14.34), omitting the possessive. The instruction continues in 14:35 with Εἰ δέ τι μαθεῖν θέλουσιν (rp:1Cor.14.35). At 14:36 the double question Ἢ ἀφ’ ὑμῶν ὁ λόγος τοῦ θεοῦ ἐξῆλθεν (rp:1Cor.14.36) challenges the addressees and is attached backward here, as a retort that closes the instruction; this attachment is INFERRED. Close after 14:36: 14:37 opens a conditional with Εἴ τις δοκεῖ προφήτης εἶναι (rp:1Cor.14.37)."

#### `W5-014.boundary_evidence_refs` (S2-11)

Pinned: ["rp:1Cor.14.37 [WARRANT-onset:near] conditional, RP pilcrow", "rp:1Cor.14.36 [WARRANT-onset:far] double question", "rp:1Cor.14.40 [WARRANT-close:near] summary exhortation", "rp:1Cor.15.1 [WARRANT-close:far] disclosure formula opening the gospel tradition", "web:1Cor.14.37-1Cor.14.40 (unit span)", "sbl:1Cor.14.39 (SBL possessive and order differ)", "web:1Cor.14.34-1Cor.14.35 (named in the prose)"]

Expected after the orders: ["rp:1Cor.14.37 [WARRANT-onset:near] conditional", "rp:1Cor.14.36 [WARRANT-onset:far] double question", "rp:1Cor.14.40 [WARRANT-close:near] summary exhortation", "rp:1Cor.15.1 [WARRANT-close:far] disclosure formula opening the gospel tradition", "web:1Cor.14.37-1Cor.14.40 (unit span)", "sbl:1Cor.14.39 (SBL possessive and order differ)", "web:1Cor.14.34-1Cor.14.35 (named in the prose)"]

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

## How you check your work (in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W5\work\`)

1. Copy `SP\1Cor\fixup\draft_rows_fixup1_applied.jsonl` byte-identically to `work\rows_applied.jsonl` and replace your
   part's changed rows with your revised rows (same order).
2. RUN `run_validator_suite.py work\rows_applied.jsonl`: hard_status GREEN, every member GREEN, triage_flags 0.
3. RUN `ngram7.py work\rows_applied.jsonl --gate 10 --full-ids`: no offending gram.
4. RUN `check_tiling.py work\rows_applied.jsonl --range 1Cor.1.1-1Cor.16.24`: GREEN, 437 of 437.
5. RUN `cwo_sweep_1cor.py work\rows_applied.jsonl --out work\cwo.json`: on your rows A 0 and CWO-1COR-04 support_use and
   count_excess 0 (W6 only: the W6-013 boundary_rationale flag noted above may remain).
6. Write your part's rows to `work\slice_W5.jsonl` and RUN `_validate_writer_part_1cor.py work\slice_W5.jsonl
   --part W5 --book-index`: GREEN.
7. Confirm by script that every revised field equals its expected value above and every other field is byte-identical (as a JSON value) to the pinned rows.

## Deliverables

- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W5\fixup2_W5_rows.jsonl`: one JSON object per line, the FULL revised row for every row you changed (and only those), in the
  pinned rows' order, every untouched field byte-identical as a JSON value.
- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W5\fixup2_W5_changes.json`:

```
{"attempt_id":"cor_fixup2_W5_a1","execution_id":"cor_fixup2_W5_a1#e1","rows_file_sha256":"<pinned rows digest>",
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
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W5

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"cor_fixup2_W5_a1","execution_id":"cor_fixup2_W5_a1#e1",
 "sources":["<exact paths you read, with sha256>"],
 "outcome":{"changed":[{"what":"<row.field>","why":"<ruling id>"}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search, read no transcript; read only the exact paths named",
 "rows_sha256":"<sha256 of fixup2_W5_rows.jsonl>","changes_sha256":"<sha256 of fixup2_W5_changes.json>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
