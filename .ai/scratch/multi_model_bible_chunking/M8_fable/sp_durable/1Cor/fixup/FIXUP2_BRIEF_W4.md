# FIXUP-2 AUTHOR BRIEF, part W4 (execution #e1): 1 Corinthians, span-exact ruled row repairs (M8_fable, OW-36 queue)

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

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W4` already exists. Write your deliverables directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W4\fixup2_W4_rows.jsonl` and `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W4\fixup2_W4_changes.json`. **Never run any existence check, listing, glob or recursive search against it or any
other directory.** A shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W4\work\`, created with
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

You are the FIXUP-2 AUTHOR for part W4. Attempt `cor_fixup2_W4_a1`, execution `cor_fixup2_W4_a1#e1`. You authored none of the rows, the
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
- `SP\1Cor\writer_lanes\_validate_writer_part_1cor.py`: RUN on a slice of your private copy holding only your part's rows, with `--part W4 --book-index` (it writes nothing).
- `SP\campaign\grader_models.v1.json`: READ where you check your model role (grader_fallback).
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 3412-3434 only (OW-36, the owner's grant).

## The orders to part W4 (quoted from the rulings file, sha256 1299a598b60bbf3c8fb193381ead098e394242a713d8bac4e584b39fdf0e0541)

### S2-07

Decision (verbatim): Adopt the class ruling and open CWO-1COR-04. Rule 4 covers the adopted cut and every rival cut. Any mention of a WEB paragraph or a chapter division, present or absent, in boundary_rationale, strongest_rejected_alternative, device_notes or a boundary_evidence_refs annotation is support use unless the same sentence or element disclaims it in words (not weighed, formatting, decides nothing, does not decide, never drives, neither drives nor corroborates, excluded, informs and does not decide). Bare observed_substrate_signals location items are compliant. Remedy: delete the clause, keep the content and keep every rival location. W1 joins the fix-up.

Your order (verbatim): This licenses, in words, the named field(s) of the named row(s) for this edit only; the round-1 licence did not cover them. W4-001.strongest_rejected_alternative: delete the exact span; the rival 11:10/11:11 stays.

Exact spans (verbatim): [" and the WEB starts a paragraph"]

### S2-08

Decision (verbatim): Ratify with changes. The word 'agrees' is deleted from the pilcrow annotations in W4-001 ber[0] and W4-003 ber[0], and also, as found in the bytes, in W4-002 ber[3], W3-006 ber[7] and W3-007 ber[7]. The ref ids, the tags and the words 'decides nothing' / 'informs and does not decide' stay.

Your order (verbatim): This licenses, in words, an edit of the annotation text of the named boundary_evidence_refs element(s) only; the ref id, the ref locator and the bracketed tag stay byte-identical, and no element is added or removed unless this order says so. W4-001.boundary_evidence_refs[0], W4-002.boundary_evidence_refs[3] and W4-003.boundary_evidence_refs[0]: delete the exact span in each.

Exact spans (verbatim): ["agrees and "]

### S2-15

Decision (verbatim): Adopt: fold into S2-07 and CWO-1COR-04. An absent WEB paragraph used as a grade input is rule-4 use, and the absence form is part of the CWO-1COR-04 predicate. An absent RP pilcrow informing confidence is compliant under rule 5, so W4-002.boundary_rationale stays.

Your order (verbatim): This licenses, in words, the named field(s) of the named row(s) for this edit only; the round-1 licence did not cover them. W4-001.boundary_rationale: delete the exact span; the clause then reads 'there is no RP pilcrow at 11:13, and no device ...'.

Exact spans (verbatim): [" and no WEB paragraph start"]

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

- `W4-001.boundary_rationale` W support_use (true_ordered; ordered by S2-15)
- `W4-001.strongest_rejected_alternative` W support_use (true_ordered; ordered by S2-07)
- `W4-001.boundary_evidence_refs[0]` P support_use (true_ordered; ordered by S2-08)
- `W4-002.boundary_evidence_refs[3]` P support_use (true_ordered; ordered by S2-08)
- `W4-003.boundary_evidence_refs[0]` P support_use (true_ordered; ordered by S2-08)

## The edits, one per line (the orders above, as operations on the pinned rows)

- `W4-001.strongest_rejected_alternative` (S2-07) del delete " and the WEB starts a paragraph"
- `W4-001.boundary_evidence_refs[0]` (S2-08) del delete "agrees and "
- `W4-002.boundary_evidence_refs[3]` (S2-08) del delete "agrees and "
- `W4-003.boundary_evidence_refs[0]` (S2-08) del delete "agrees and "
- `W4-001.boundary_rationale` (S2-15) del delete " and no WEB paragraph start"

MEASURED (the orchestrator's script applied every part's edits to a scratch copy of the pinned rows): suite hard_status
GREEN with every member GREEN, triage_flags 0; ngram7 GREEN, 0 offending grams; tiling GREEN 437/437; CWO-1COR-01 A 0;
CWO-1COR-02 0 of 70; CWO-1COR-04 support-use and count-excess 0 except W6-013 boundary_rationale, which the sweep still
flags because the sentence on the Greek greeting ("... marks the autograph") shares a sentence span with the pilcrow
clause (a known split artifact, classed false_positive in the coverage report). That flag is the orchestrator's to
re-class; it is not yours to edit around.

## What you may change (the lander refuses any other difference)

Each licensed field, with its pinned value and the value the orders produce, as JSON values:

#### `W4-001.boundary_evidence_refs` (S2-08)

Pinned: ["rp:1Cor.11.2 [WARRANT-onset:near] (praise opening Ἐπαινῶ δὲ ὑμᾶς, with tradition vocabulary; RP pilcrow at 11:2 agrees and decides nothing)", "rp:1Cor.11.1 [WARRANT-onset:far] (imitation command Μιμηταί μου γίνεσθε, closes the argument behind the seam)", "rp:1Cor.11.12 [WARRANT-close:near] (τὰ δὲ πάντα ἐκ τοῦ θεοῦ. ends the reciprocity qualification)", "rp:1Cor.11.13 [WARRANT-close:far] (asyndetic imperative, Ἐν ὑμῖν αὐτοῖς κρίνατε·; text alone, no device)", "rp:1Cor.11.13-1Cor.11.16 [WARRANT-rival:merge] 11.12/11.13 (one row for 11:2-11:16; recorded as the live rival)", "rp:1Cor.11.11 [WARRANT-rival:near] 11.10/11.11 (adversative Πλὴν; rejected, the qualification answers 11:7-11:10)", "rp:1Cor.11.3 [DISCLOSURE-device] (disclosure formula Θέλω δὲ ὑμᾶς εἰδέναι, continues 11:2; no row opens here)", "sbl:1Cor.11.2 [DISCLOSURE-note] (SBLGNT reads Ἐπαινῶ δὲ ⸀ὑμᾶς ὅτι, with a sign at the pronoun and no vocative)", "sbl:1Cor.11.11 [DISCLOSURE-note] (SBLGNT reads the two clauses in the other order inside a sign pair: ⸂γυνὴ χωρὶς ἀνδρὸς οὔτε ἀνὴρ χωρὶς γυναικὸς⸃ ἐν)", "rp:1Cor.11.17 [ANCHOR] (negated praise οὐκ ἐπαινῶ, answers the praise of 11:2)", "rp:1Cor.11.7-1Cor.11.10 [ANCHOR] (argument from the creation account that 11:11-11:12 qualifies)"]

Expected after the orders: ["rp:1Cor.11.2 [WARRANT-onset:near] (praise opening Ἐπαινῶ δὲ ὑμᾶς, with tradition vocabulary; RP pilcrow at 11:2 decides nothing)", "rp:1Cor.11.1 [WARRANT-onset:far] (imitation command Μιμηταί μου γίνεσθε, closes the argument behind the seam)", "rp:1Cor.11.12 [WARRANT-close:near] (τὰ δὲ πάντα ἐκ τοῦ θεοῦ. ends the reciprocity qualification)", "rp:1Cor.11.13 [WARRANT-close:far] (asyndetic imperative, Ἐν ὑμῖν αὐτοῖς κρίνατε·; text alone, no device)", "rp:1Cor.11.13-1Cor.11.16 [WARRANT-rival:merge] 11.12/11.13 (one row for 11:2-11:16; recorded as the live rival)", "rp:1Cor.11.11 [WARRANT-rival:near] 11.10/11.11 (adversative Πλὴν; rejected, the qualification answers 11:7-11:10)", "rp:1Cor.11.3 [DISCLOSURE-device] (disclosure formula Θέλω δὲ ὑμᾶς εἰδέναι, continues 11:2; no row opens here)", "sbl:1Cor.11.2 [DISCLOSURE-note] (SBLGNT reads Ἐπαινῶ δὲ ⸀ὑμᾶς ὅτι, with a sign at the pronoun and no vocative)", "sbl:1Cor.11.11 [DISCLOSURE-note] (SBLGNT reads the two clauses in the other order inside a sign pair: ⸂γυνὴ χωρὶς ἀνδρὸς οὔτε ἀνὴρ χωρὶς γυναικὸς⸃ ἐν)", "rp:1Cor.11.17 [ANCHOR] (negated praise οὐκ ἐπαινῶ, answers the praise of 11:2)", "rp:1Cor.11.7-1Cor.11.10 [ANCHOR] (argument from the creation account that 11:11-11:12 qualifies)"]

#### `W4-001.boundary_rationale` (S2-15)

Pinned: "Onset at 11:2, weighed from both sides. Behind the seam, rp:1Cor.11.1 Μιμηταί μου γίνεσθε, closes the argument over food and conscience with an imitation command (web:1Cor.11.1 “Be imitators of me, even as I also am of Christ.”) and opens no fresh subject. Across the seam, rp:1Cor.11.2 Ἐπαινῶ δὲ ὑμᾶς, opens a statement of praise whose object is the delivered traditions (rp:1Cor.11.2 καθὼς παρέδωκα ὑμῖν τὰς παραδόσεις); the praise verb returns negated at rp:1Cor.11.17 οὐκ ἐπαινῶ,, so the pair brackets the material before the meal discussion (EXTRACTED: device ids epaino and ouk_epaino at 11:2, 11:17 and 11:22). No row opens at 11:3: rp:1Cor.11.3 Θέλω δὲ ὑμᾶς εἰδέναι, states the thesis that the praise of 11:2 leads into, and its connective ties it back to 11:2 (INFERRED). Close at 11:12, weighed from both sides. Inside, rp:1Cor.11.12 τὰ δὲ πάντα ἐκ τοῦ θεοῦ. ends the reciprocity qualification that rp:1Cor.11.11 Πλὴν introduced, which answers the argument from the creation account in 11:7-11:10 (INFERRED). Beyond, rp:1Cor.11.13 Ἐν ὑμῖν αὐτοῖς κρίνατε· begins asyndetically and turns from argument to an appeal to the hearers' own judgment, followed by the argument from nature and the appeal to custom (INFERRED). This close seam rests on the text alone: there is no RP pilcrow and no WEB paragraph start at 11:13, and no device from the device listing stands there (EXTRACTED), so the evidence for it is one-sided and confidence stays medium-low."

Expected after the orders: "Onset at 11:2, weighed from both sides. Behind the seam, rp:1Cor.11.1 Μιμηταί μου γίνεσθε, closes the argument over food and conscience with an imitation command (web:1Cor.11.1 “Be imitators of me, even as I also am of Christ.”) and opens no fresh subject. Across the seam, rp:1Cor.11.2 Ἐπαινῶ δὲ ὑμᾶς, opens a statement of praise whose object is the delivered traditions (rp:1Cor.11.2 καθὼς παρέδωκα ὑμῖν τὰς παραδόσεις); the praise verb returns negated at rp:1Cor.11.17 οὐκ ἐπαινῶ,, so the pair brackets the material before the meal discussion (EXTRACTED: device ids epaino and ouk_epaino at 11:2, 11:17 and 11:22). No row opens at 11:3: rp:1Cor.11.3 Θέλω δὲ ὑμᾶς εἰδέναι, states the thesis that the praise of 11:2 leads into, and its connective ties it back to 11:2 (INFERRED). Close at 11:12, weighed from both sides. Inside, rp:1Cor.11.12 τὰ δὲ πάντα ἐκ τοῦ θεοῦ. ends the reciprocity qualification that rp:1Cor.11.11 Πλὴν introduced, which answers the argument from the creation account in 11:7-11:10 (INFERRED). Beyond, rp:1Cor.11.13 Ἐν ὑμῖν αὐτοῖς κρίνατε· begins asyndetically and turns from argument to an appeal to the hearers' own judgment, followed by the argument from nature and the appeal to custom (INFERRED). This close seam rests on the text alone: there is no RP pilcrow at 11:13, and no device from the device listing stands there (EXTRACTED), so the evidence for it is one-sided and confidence stays medium-low."

#### `W4-001.strongest_rejected_alternative` (S2-07)

Pinned: "One row for 11:2-11:16. The appeal in 11:13-11:16 argues for the same practice as 11:4-11:10, and a reader who weighs the shared subject over the change in kind of warrant would merge the two; that merge is the live rival and is left as a question for end review. The split is kept because the imperative at 11:13 changes the mode of argument from the creation account to the hearers' judgment, nature and custom (INFERRED). A second candidate, a seam at 11:10/11:11, where rp:1Cor.11.11 Πλὴν turns the argument and the WEB starts a paragraph, is rejected: 11:11-11:12 qualifies 11:7-11:10 and is bound to it by rp:1Cor.11.12 Ὥσπερ γὰρ, so it completes that argument rather than opening a move (INFERRED)."

Expected after the orders: "One row for 11:2-11:16. The appeal in 11:13-11:16 argues for the same practice as 11:4-11:10, and a reader who weighs the shared subject over the change in kind of warrant would merge the two; that merge is the live rival and is left as a question for end review. The split is kept because the imperative at 11:13 changes the mode of argument from the creation account to the hearers' judgment, nature and custom (INFERRED). A second candidate, a seam at 11:10/11:11, where rp:1Cor.11.11 Πλὴν turns the argument, is rejected: 11:11-11:12 qualifies 11:7-11:10 and is bound to it by rp:1Cor.11.12 Ὥσπερ γὰρ, so it completes that argument rather than opening a move (INFERRED)."

#### `W4-002.boundary_evidence_refs` (S2-08)

Pinned: ["rp:1Cor.11.13 [WARRANT-onset:near] (asyndetic imperative, Ἐν ὑμῖν αὐτοῖς κρίνατε·; text alone, no device)", "rp:1Cor.11.12 [WARRANT-onset:far] (τὰ δὲ πάντα ἐκ τοῦ θεοῦ. closes the qualification)", "rp:1Cor.11.16 [WARRANT-close:near] (appeal to custom ἡμεῖς τοιαύτην συνήθειαν οὐκ ἔχομεν,)", "rp:1Cor.11.17 [WARRANT-close:far] (negated praise οὐκ ἐπαινῶ,; RP pilcrow at 11:17 agrees and decides nothing)", "rp:1Cor.11.2-1Cor.11.12 [WARRANT-rival:merge] 11.12/11.13 (one row for 11:2-11:16; recorded as the live rival)", "rp:1Cor.11.16 [WARRANT-rival:near] 11.15/11.16 (the appeal to custom as a unit of its own; rejected as too slight to stand as a move)", "sbl:1Cor.11.14 [DISCLOSURE-note] (SBLGNT reads ⸀οὐδὲ ⸂ἡ φύσις αὐτὴ⸃)", "sbl:1Cor.11.17 [DISCLOSURE-note] (sign pair ⸂παραγγέλλων οὐκ ἐπαινῶ⸃; the variant content behind it is UNAVAILABLE)", "web:1Cor.11.14 [QUOTE] (appeal to nature)", "rp:1Cor.11.11 [ANCHOR] (start of the qualification closed at 11:12)", "rp:1Cor.11.2 [ANCHOR] (the praise that 11:17 negates)"]

Expected after the orders: ["rp:1Cor.11.13 [WARRANT-onset:near] (asyndetic imperative, Ἐν ὑμῖν αὐτοῖς κρίνατε·; text alone, no device)", "rp:1Cor.11.12 [WARRANT-onset:far] (τὰ δὲ πάντα ἐκ τοῦ θεοῦ. closes the qualification)", "rp:1Cor.11.16 [WARRANT-close:near] (appeal to custom ἡμεῖς τοιαύτην συνήθειαν οὐκ ἔχομεν,)", "rp:1Cor.11.17 [WARRANT-close:far] (negated praise οὐκ ἐπαινῶ,; RP pilcrow at 11:17 decides nothing)", "rp:1Cor.11.2-1Cor.11.12 [WARRANT-rival:merge] 11.12/11.13 (one row for 11:2-11:16; recorded as the live rival)", "rp:1Cor.11.16 [WARRANT-rival:near] 11.15/11.16 (the appeal to custom as a unit of its own; rejected as too slight to stand as a move)", "sbl:1Cor.11.14 [DISCLOSURE-note] (SBLGNT reads ⸀οὐδὲ ⸂ἡ φύσις αὐτὴ⸃)", "sbl:1Cor.11.17 [DISCLOSURE-note] (sign pair ⸂παραγγέλλων οὐκ ἐπαινῶ⸃; the variant content behind it is UNAVAILABLE)", "web:1Cor.11.14 [QUOTE] (appeal to nature)", "rp:1Cor.11.11 [ANCHOR] (start of the qualification closed at 11:12)", "rp:1Cor.11.2 [ANCHOR] (the praise that 11:17 negates)"]

#### `W4-003.boundary_evidence_refs` (S2-08)

Pinned: ["rp:1Cor.11.17 [WARRANT-onset:near] (negated praise Τοῦτο δὲ παραγγέλλων οὐκ ἐπαινῶ, answering 11:2; RP pilcrow at 11:17 agrees and decides nothing)", "rp:1Cor.11.16 [WARRANT-onset:far] (appeal to custom οὐδὲ αἱ ἐκκλησίαι τοῦ θεοῦ. closes the covering discussion)", "rp:1Cor.11.22 [WARRANT-close:near] (inclusio with 11:17: Ἐπαινέσω ὑμᾶς ἐν τούτῳ; Οὐκ ἐπαινῶ.)", "rp:1Cor.11.23 [WARRANT-close:far] (tradition formula Ἐγὼ γὰρ παρέλαβον ἀπὸ τοῦ κυρίου; its gar link back to 11:22 is disclosed)", "rp:1Cor.11.23-1Cor.11.34 [WARRANT-rival:merge] 11.22/11.23 (one row for 11:17-11:34; recorded as the live rival)", "rp:1Cor.11.20 [WARRANT-rival:near] 11.19/11.20 (resumptive Συνερχομένων οὖν ὑμῶν ἐπὶ τὸ αὐτό,; rejected, the report of 11:18 is incomplete before 11:20-11:22)", "rp:1Cor.11.18 [DISCLOSURE-device] (report verb ἀκούω σχίσματα with the gathering participle)", "sbl:1Cor.11.22 [DISCLOSURE-note] (SBLGNT reads ἐπαινέσω ὑμᾶς; ἐν τούτῳ οὐκ ἐπαινῶ.)", "sbl:1Cor.11.17 [DISCLOSURE-note] (sign pair ⸂παραγγέλλων οὐκ ἐπαινῶ⸃; the variant content behind it is UNAVAILABLE)", "rp:1Cor.11.33-1Cor.11.34 [DISCLOSURE-device] (the gathering verb returns in the closing commands)", "rp:1Cor.11.2 [ANCHOR] (the praise that 11:17 withholds)", "rp:1Cor.11.19 [ANCHOR] (remark on factions before the resumptive gathering clause)"]

Expected after the orders: ["rp:1Cor.11.17 [WARRANT-onset:near] (negated praise Τοῦτο δὲ παραγγέλλων οὐκ ἐπαινῶ, answering 11:2; RP pilcrow at 11:17 decides nothing)", "rp:1Cor.11.16 [WARRANT-onset:far] (appeal to custom οὐδὲ αἱ ἐκκλησίαι τοῦ θεοῦ. closes the covering discussion)", "rp:1Cor.11.22 [WARRANT-close:near] (inclusio with 11:17: Ἐπαινέσω ὑμᾶς ἐν τούτῳ; Οὐκ ἐπαινῶ.)", "rp:1Cor.11.23 [WARRANT-close:far] (tradition formula Ἐγὼ γὰρ παρέλαβον ἀπὸ τοῦ κυρίου; its gar link back to 11:22 is disclosed)", "rp:1Cor.11.23-1Cor.11.34 [WARRANT-rival:merge] 11.22/11.23 (one row for 11:17-11:34; recorded as the live rival)", "rp:1Cor.11.20 [WARRANT-rival:near] 11.19/11.20 (resumptive Συνερχομένων οὖν ὑμῶν ἐπὶ τὸ αὐτό,; rejected, the report of 11:18 is incomplete before 11:20-11:22)", "rp:1Cor.11.18 [DISCLOSURE-device] (report verb ἀκούω σχίσματα with the gathering participle)", "sbl:1Cor.11.22 [DISCLOSURE-note] (SBLGNT reads ἐπαινέσω ὑμᾶς; ἐν τούτῳ οὐκ ἐπαινῶ.)", "sbl:1Cor.11.17 [DISCLOSURE-note] (sign pair ⸂παραγγέλλων οὐκ ἐπαινῶ⸃; the variant content behind it is UNAVAILABLE)", "rp:1Cor.11.33-1Cor.11.34 [DISCLOSURE-device] (the gathering verb returns in the closing commands)", "rp:1Cor.11.2 [ANCHOR] (the praise that 11:17 withholds)", "rp:1Cor.11.19 [ANCHOR] (remark on factions before the resumptive gathering clause)"]

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

## How you check your work (in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W4\work\`)

1. Copy `SP\1Cor\fixup\draft_rows_fixup1_applied.jsonl` byte-identically to `work\rows_applied.jsonl` and replace your
   part's changed rows with your revised rows (same order).
2. RUN `run_validator_suite.py work\rows_applied.jsonl`: hard_status GREEN, every member GREEN, triage_flags 0.
3. RUN `ngram7.py work\rows_applied.jsonl --gate 10 --full-ids`: no offending gram.
4. RUN `check_tiling.py work\rows_applied.jsonl --range 1Cor.1.1-1Cor.16.24`: GREEN, 437 of 437.
5. RUN `cwo_sweep_1cor.py work\rows_applied.jsonl --out work\cwo.json`: on your rows A 0 and CWO-1COR-04 support_use and
   count_excess 0 (W6 only: the W6-013 boundary_rationale flag noted above may remain).
6. Write your part's rows to `work\slice_W4.jsonl` and RUN `_validate_writer_part_1cor.py work\slice_W4.jsonl
   --part W4 --book-index`: GREEN.
7. Confirm by script that every revised field equals its expected value above and every other field is byte-identical (as a JSON value) to the pinned rows.

## Deliverables

- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W4\fixup2_W4_rows.jsonl`: one JSON object per line, the FULL revised row for every row you changed (and only those), in the
  pinned rows' order, every untouched field byte-identical as a JSON value.
- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W4\fixup2_W4_changes.json`:

```
{"attempt_id":"cor_fixup2_W4_a1","execution_id":"cor_fixup2_W4_a1#e1","rows_file_sha256":"<pinned rows digest>",
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
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx2\W4

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"cor_fixup2_W4_a1","execution_id":"cor_fixup2_W4_a1#e1",
 "sources":["<exact paths you read, with sha256>"],
 "outcome":{"changed":[{"what":"<row.field>","why":"<ruling id>"}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search, read no transcript; read only the exact paths named",
 "rows_sha256":"<sha256 of fixup2_W4_rows.jsonl>","changes_sha256":"<sha256 of fixup2_W4_changes.json>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
