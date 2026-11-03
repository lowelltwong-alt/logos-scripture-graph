# FIXUP-3 AUTHOR BRIEF, part W6 (execution #e1): 1 Corinthians, ruled row repairs (M8_fable, OW-36 queue)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Greek New Testament (the first letter to the Corinthians, in Greek with a public-domain English translation) for a study corpus. You revise a few fields of candidate reading-unit rows under ruled orders. Quotations are short, sliced from public witnesses (Robinson-Pierpont Byzantine text, Unlicense; SBLGNT, CC BY 4.0; World English Bible, public domain), and carry their attribution.

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## AUTHORITY (OW-36; it also travels in your launch message)

The owner authorized this Opus orchestration and its subagents for six books: 1 Corinthians, John, Romans, Revelation, Hebrews and Matthew. The owner's answer, verbatim: "Your six-book queue (Recommended)". authorization_ref `lowell_chat_2026-10-14_m8_opus_orchestration_six_book_queue`; verify in `SP\..\ERROR_PATTERN_LEDGER.v1.md` lines 3412-3434 only. You run on claude-opus-5-5 as a recorded grader_fallback (OW-25). You read files under the worktree and write only under your OUT directory; the orchestrator lands and applies your deliverable. You never run git, never write a receipt and never touch the registry.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx3\W6` already exists. Write your deliverables directly to `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx3\W6\fixup3_W6_rows.jsonl` and `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx3\W6\fixup3_W6_changes.json`. Do not test for the directory, list it or glob it, and write nothing to any other directory. A shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx3\W6\work\`, created with os.makedirs(exist_ok=True) and never tested first.

**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. No listing, no glob, no recursive search. State in your final message that you ran no listing and no glob.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`, `M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or `comparison\`; every other book's directory under SP; every other part's fix-up OUT; the writers', the reviewers' and the controlling agent's OUT directories, receipts, final messages and evidence notes; every `*_attempt_receipts.jsonl`; transcripts; any file not named in this brief. Nothing from another book passes as 1 Corinthians' (E-65).

**Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run `python -B`. Never run any tool not marked RUN below. Never pass `--write`. Never edit any file under the worktree. Put any script that holds a regular expression or a backslash in a file written whole, never through a shell heredoc or `python -c`.

## Your role

You are the FIXUP-3 AUTHOR for part W6. Attempt `cor_fixup3_W6_a1`, execution `cor_fixup3_W6_a1#e1`. You authored none of the rows, the reviews or the rulings. The controlling agent (execution cor_controlling_rulings_r4_a1#e1) ruled on the primary reviews; its orders to your part are quoted verbatim below. You carry out exactly those orders and nothing else changes. You do not adjudicate a divided reading, select a textual reading or tradition, settle a contested interpretation, move any seam or raise any confidence.

Rules for every author (verbatim from GATE-E4): Every author: replacement words come from the witness bytes; no sentence is shared across rows (ngram7); RP first, SBL quoted only to disclose; cut, span, tiling, unit_type and confidence stay unless the order says so; the named spans are the whole licence, and the round-1 licence did not cover them; if a removal or reword leaves a seam without ground, the author stops and reports.

Unlike earlier fix-ups, many orders here ask you to reword, so no expected value is given. You author the words, under the order, from the witness bytes. Where an order gives an exact span or an exact phrase, use it exactly.

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a hard stop: report it and stop.

| input | sha256 |
|---|---|
| `SP\1Cor\fixup\draft_rows_fixup2_applied.jsonl` | `75933a142375d8736ae71cdcc7f0e0b9052c36ea4ac4b87ccacf676ae50c6fbe` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E4.v1.json` | `33ac57245ee930b1484a1227fc019e11c6f082b5c984a20ecc9e7c765d463187` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E3.v1.json` | `a7f32674dee0b0e27f25803729f93142cefdaf2847f9d7122010397e992efe70` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E1.v1.json` | `93e5918b10b17842e5700471087290036549f4ab2327220d518967c49b53dc90` |
| `SP\1Cor\review\cwo_1cor_post_fixup2_cwo0607_report.v1.json` | `9daa00d3197cf79f17389016e8bf75afad7b9ea51bc45da4c114116259b1162c` |
| `SP\1Cor\book_strategy_1Cor.md` | `70e344fed9f0f64654baa97dff80e03b706a1288b47de182628dc453212e39ca` |
| `SP\1Cor\tools\TOOLKIT.md` | `49de0883f5cbed7fd9e25fdc8a156a083f8794bdd6490de1b0eee82aa2c7361e` |
| `SP\1Cor\tools\run_validator_suite.py` | `ebe7197b35635d9f8cbf88914219003e32816ba37173f00205668eb5aab2dbb4` |
| `SP\1Cor\tools\ngram7.py` | `2dc3a80d5785d2048fc7b17dac093a47c26f10599922bd083bb7158de10d0230` |
| `SP\1Cor\tools\check_tiling.py` | `71b5ee67b98eeb6815515928448b52baa5cac45692afe09212acf2f85d17bbcf` |
| `SP\1Cor\review\cwo_sweep_1cor.py` | `6f6578ea5958ee580493dbf56edec56bd0ee2cd6daf99c26fc9353cfba2ee92f` |
| `SP\1Cor\writer_lanes\_validate_writer_part_1cor.py` | `59ef3318dbd98201e57107e9747f17b579f750116ba875061493fbd3012a46e9` |
| `SP\1Cor\1Cor_rp.txt` | `94f7cf39fbd87f7952aba3ca957b7a4790edfb5d120dceffc8deac0ad0ccc2eb` |
| `SP\1Cor\1Cor_sbl.txt` | `354b6dcf5b5f43a24dd85918e9759eeeb3153dc5284ab707a4167b64919456ff` |
| `SP\1Cor\1Cor_web_clean.txt` | `7c8224ccf9eb0a06df20c5b2289d33ea32267dda136e88e73ea5761807cf0778` |
| `SP\1Cor\pmarks_1Cor.json` | `5cd9055a8ecbfbc8dcf0f5dbc43e7bedbb0e69dc4fb7e8d9000e164e074c7fd7` |
| `SP\campaign\grader_models.v1.json` | `cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `4753992a2229a8a09f427fe52d654758af9074b1f18fd2f7cad306792858029f` |

How you may use each input:

- `SP\1Cor\fixup\draft_rows_fixup2_applied.jsonl`: READ your part's rows in full; other rows only where you check a fact. You change ONLY what the orders license.
- `SP\1Cor\review\1cor_controlling_agent_rulings_E4.v1.json`: READ where you check an order's context (your orders are quoted verbatim below).
- `SP\1Cor\review\1cor_controlling_agent_rulings_E3.v1.json` and `SP\1Cor\review\1cor_controlling_agent_rulings_E1.v1.json`: READ where you check S3-01 or CWO-1COR-01..03 (quoted below).
- `SP\1Cor\review\cwo_1cor_post_fixup2_cwo0607_report.v1.json`: READ where you check a CWO-1COR-05, -06 or -07 hit (your rows' hits are listed below).
- `SP\1Cor\book_strategy_1Cor.md`: READ sections 7 and 8 in full. BINDING. Section 7 is the record REPORTED sentences may name.
- `SP\1Cor\tools\TOOLKIT.md`: READ where you check a suite member's contract. Where it and a tool's code differ, the code is the contract.
- `SP\1Cor\1Cor_rp.txt`, `SP\1Cor\1Cor_sbl.txt`, `SP\1Cor\1Cor_web_clean.txt`: READ by line; each RP and SBL line is `1Cor.C.V<TAB>text`. Slice every new Greek run or WEB quotation from these bytes by script. RP first; SBL only to disclose.
- `SP\1Cor\pmarks_1Cor.json`: READ where an order turns on a pilcrow's verse. A mark is cited at the verse it follows.
- `SP\1Cor\tools\run_validator_suite.py`: RUN on a PRIVATE COPY of the rows in your OUT\work only (it writes its report beside its input). Run no member directly except ngram7.py below.
- `SP\1Cor\tools\ngram7.py`: RUN on your private copy with `--gate 10 --full-ids` (it writes nothing).
- `SP\1Cor\tools\check_tiling.py`: RUN on your private copy with `--range 1Cor.1.1-1Cor.16.24` (it writes nothing).
- `SP\1Cor\review\cwo_sweep_1cor.py`: RUN on your private copy with `--out <a file in your OUT\work>` (it writes only that file).
- `SP\1Cor\writer_lanes\_validate_writer_part_1cor.py`: RUN on a slice of your private copy holding only your part's rows, with `--part W6 --book-index` (it writes nothing).
- `SP\campaign\grader_models.v1.json`: READ where you check your model role (grader_fallback).
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 3412-3434 only (OW-36, the owner's grant).

## The orders to part W6 (quoted from the rulings file, sha256 33ac57245ee930b1484a1227fc019e11c6f082b5c984a20ecc9e7c765d463187)

### R4-W6-003

Decision (verbatim): Adopt as a reword. Cut and confidence stand. 15:29 is third person (ποιήσουσιν, βαπτίζονται); the first second-person form is ὑμετέραν at 15:31, so 'the readers' own practice' claims too much. The row names the actors as unstated and installs no opposite claim. The Latter-day Saint and other readings stay named and unadjudicated.

Your order (verbatim): W6-003: reword the boundary_rationale sentence so it does not call the practice the readers'. This licenses, in words, the named field(s) of the named row(s) for this edit only.

Exact spans (verbatim): ["turning from the eschatological order to the readers' own practice."]

### R4-W6-004

Decision (verbatim): Adopt as a reword. Cut and medium stand. The rival is restated on the person sequence, third at 15:29, first at 15:30-15:32, direct address at 15:33-15:34, and on the return of νεκροὶ οὐκ ἐγείρονται at 15:15, 15:16, 15:29 and 15:32. The DN sentence on 15:29's site is corrected: the sign falls on SBL's closing αὐτῶν, a word RP does not have there. 'The onset carries an RP pilcrow at 15:29.' is S2-02's prescribed sentence and stays. The hand class for the CWO-1COR-06 hit at 15:35 is false positive: Ἀλλ’ against Ἀλλὰ is elision, and W6-005 discloses that verse.

Your order (verbatim): W6-004: reword the SRA sentence and the named DN sentence; tier the DN division per R4-UNCERTAINTY (c). This licenses, in words, the named field(s) of the named row(s) for this edit only.

Exact spans (verbatim): ["Joining 15:29-15:34 to the sequence of 15:20-15:28 because Epei reasons from what precedes: the reasoning turns to the readers' practice and the apostle's peril, a new line of argument, so it stands as its own step.", "SBL variant site at 15:29 touches the closing pronoun of the verse, not the quoted onset."]

### R4-W6-005

Decision (verbatim): Keep the cut and medium; do not move the confidence; route the split. Adopt OL's reword: Τοῦτο δέ φημι announces the clause that follows, so 'summarising' is not measured. The mood labels at 15:49 are one letter in each witness and are labelled the writer's reading. The backward reading stays disclosed, and the row keeps its pointer to 15:50-15:58.

Your order (verbatim): W6-005: reword the named sentence and the annotations of boundary_evidence_refs[6], [7] and [8]: the formula announces the clause after it, and the mood labels are the writer's reading. The annotation edits leave the ref ids byte-identical. This licenses, in words, the named field(s) of the named row(s) for this edit only. This licenses, in words, an edit of the annotation text of the named boundary_evidence_refs element(s) only; the ref id, the ref locator and the bracketed tag stay byte-identical, and no element is added or removed unless this order says so.

Exact spans (verbatim): ["RP pilcrow at 15:50 (close seam), where a summarising formula follows.", "rp:1Cor.15.50 (summarising formula; RP pilcrow)", "rp:1Cor.15.49 (close of the reply; subjunctive verb)", "sbl:1Cor.15.49 (SBL variant site: future indicative)"]

### R4-W6-006

Decision (verbatim): Adopt OL's and LF's medium findings; reject LF's low finding. The cut, medium_low and the frontier flag stand. The row says the formula announces the following clause, that 15:50 carries only texture and a pilcrow (D4), and that φθορὰ / ἀφθαρσίαν looks back to 15:42 and on to 15:52-15:54 and spans the seam, deciding nothing. The SRA gives the reason the seam is contested. No 7:29 analogy returns (S1-03). 'listed for Fable's end review' stays.

Your order (verbatim): W6-006: reword the 'Front face' sentence; extend the SRA with the reason for the contest, in words distinct from W6-005's; change the annotation of boundary_evidence_refs[3] only if its wording says 'summarising'. This licenses, in words, the named field(s) of the named row(s) for this edit only. This licenses, in words, an edit of the annotation text of the named boundary_evidence_refs element(s) only; the ref id, the ref locator and the bracketed tag stay byte-identical, and no element is added or removed unless this order says so.

Exact spans (verbatim): ["is a summarising formula with vocative, and the flesh-and-blood statement it introduces sets the premise that the mystery resolves.", "Opening at 15:51 on idou, leaving 15:50 to end the reply of 15:35-15:50; it is a contested seam, held at a lowered confidence and listed for Fable's end review."]

### R4-W6-007

Decision (verbatim): Adopt, including the confidence move from high to medium, which both lanes reach and which is licensed here in words. Both seams stand. First-person travel crosses the 16:4/16:5 seam (ἔλθω 16:2, πέμψω 16:3, κἀμὲ πορεύεσθαι 16:4, Ἐλεύσομαι 16:5, πορεύωμαι 16:6), no inventoried device stands there, §7 G gives that seam no grade, and W6-008 holds medium on it. The close rests on the end of the collection vocabulary (λογίας 16:1, λογίαι 16:2, χάριν 16:3).

Your order (verbatim): W6-007: set confidence to medium; reword the SRA to disclose the travel crossing and rest on the collection vocabulary; This licenses, in words, the field confidence of this row, from high to medium, and any sentence of the row that states the old grade. Span, tiling, unit_type and frontier_flag_considered stay. This licenses, in words, the named field(s) of the named row(s) for this edit only.

Exact spans (verbatim): ["Carrying the collection on through 16:9 because 16:3-16:4 already speak of travel: those verses concern the bearers of the gift, while 16:5 changes subject to the apostle's own route and stay."]

### R4-W6-008

Decision (verbatim): Adopt as a reword. Cut and medium stand. The phrase 'with the brothers' falls in the waiting clause, and its attachment is open. The unit's stop is the heading at 16:12 (C4), and the wording shared across 16:11/16:12 is disclosed. 16:10 has no formula, which is the row's reason for not opening there.

Your order (verbatim): W6-008: reword the close sentence of boundary_rationale and the annotation of boundary_evidence_refs[6] so the phrase's attachment stays open and the close rests on the heading; add to the SRA the absence of a formula at 16:10. This licenses, in words, the named field(s) of the named row(s) for this edit only. This licenses, in words, an edit of the annotation text of the named boundary_evidence_refs element(s) only; the ref id, the ref locator and the bracketed tag stay byte-identical, and no element is added or removed unless this order says so.

Exact spans (verbatim): ["Close: 16:11 sends Timothy on with the brothers.", "rp:1Cor.16.11 (Timothy sent on, close)", "Opening a separate unit at 16:10 on the conditional: the apostle's plans and Timothy's coming answer one practical question, who is coming to Corinth and when, so the commendation stays with the itinerary."]

### R4-W6-009

Decision (verbatim): Adopt as a reword. Cut and medium stand. The readers are already named at 16:12 (πρὸς ὑμᾶς), so the change is from report to command, not of addressee, and mood is the writer's reading. θέλημα has no possessor in either witness: the row reports that as unstated and uses no WEB rendering. The back face weighs μετὰ τῶν ἀδελφῶν at 16:11 and 16:12 and the shared ἵνα ἔλθῃ.

Your order (verbatim): W6-009: reword the named sentences so the one-verse justification rests on report against command; add the back-face links to the SRA. This licenses, in words, the named field(s) of the named row(s) for this edit only.

Exact spans (verbatim): ["One-verse justification: the heading and its answer occupy one verse, and the imperatives that follow change addressee and mood, so the topic stands alone.", "Close: the report on Apollos's reluctance and later visit is complete within the verse.", "Folding the verse into the itinerary of 16:5-16:11 as further travel business: the heading must begin a unit, and joining it to the imperatives of 16:13-16:14 would bind a report about Apollos to commands addressed to the readers."]

### R4-W6-010

Decision (verbatim): Adopt as a reword. Cut, medium and the frontier flag stand. The measured signal is the connective-free opening. The row adds the shape Πάντα ... γινέσθω at 14:26, 14:40 and 16:14, 'sums' is tiered INFERRED, and the tiling sentence is qualified: parent assignment and the C6 typing would move under the rival. The locator of boundary_evidence_refs[6] is corrected to the extent the SRA states, 16:13-16:24; this is a locator change and it is licensed here in words.

Your order (verbatim): W6-010: reword the named sentences; change boundary_evidence_refs[6] from web:1Cor.16.15-1Cor.16.24 to web:1Cor.16.13-1Cor.16.24, this element's locator only, by this express licence; the annotation stays. This licenses, in words, the named field(s) of the named row(s) for this edit only.

Exact spans (verbatim): ["opens four asyndetic imperatives,", "sums the commands under love.", "and keeping 16:13 as a unit onset leaves the tiling intact under either reading.", "web:1Cor.16.15-1Cor.16.24 (extent of the rival frame reading)"]

### R4-W6-011

Decision (verbatim): Adopt as a reword. Cut, medium and the frontier flag stand. The sign at 16:17 falls on ὅτι τὸ ⸀ὑμέτερον ὑστέρημα, a causal clause, not the arrival clause. The SRA tests 16:15 while the rationale and strategy name 16:13, and its ground is contradicted by Ἀσπάσασθε ἀλλήλους at 16:20. It is restated against 16:13: the frame family has no hit at 16:13-16:18 and its first hit is at 16:19. 'recognise such workers' imports a noun class and is replaced by the text's τοὺς τοιούτους.

Your order (verbatim): W6-011: reword the DN sentence, the SRA sentence, the boundary_rationale clause and the annotation of boundary_evidence_refs[3]. This licenses, in words, the named field(s) of the named row(s) for this edit only. This licenses, in words, an edit of the annotation text of the named boundary_evidence_refs element(s) only; the ref id, the ref locator and the bracketed tag stay byte-identical, and no element is added or removed unless this order says so.

Exact spans (verbatim): ["SBL variant site at 16:17 falls in the visitors' arrival clause and touches neither edge.", "Placing the frame edge at 16:15 so that the appeal and commendation open the closing: the commendation still asks the readers to act, which is body business, while the greetings of 16:19 address no request to them.", "a call to recognise such workers", "rp:1Cor.16.18 (recognise such workers, close)"]

### R4-W6-012

Decision (verbatim): Adopt as a reword. Cut, medium and the frontier flag stand. The asp- stem runs through 16:19, 16:20 and 16:21, so the close does not rest on the greetings ending. It rests on the change to the first-person named hand at 16:21. Add the 16:19 sign disclosure: RP Πρίσκιλλα, SBL ⸀Πρίσκα.

Your order (verbatim): W6-012: reword the close sentence of boundary_rationale and the 'recognise such workers' clause in words distinct from W6-011's; add to device_notes one clause giving the name at 16:19 in each witness. This licenses, in words, the named field(s) of the named row(s) for this edit only.

Exact spans (verbatim): ["Close: the greetings end at 16:20; at 16:21 the autograph, rp:1Cor.16.21 \"Ὁ ἀσπασμὸς τῇ ἐμῇ χειρὶ Παύλου.\", begins.", "Back face: the commendation closes at 16:18 with a call to recognise such workers."]

### R4-W6-013

Decision (verbatim): Adopt, including the confidence move from high to medium, which both lanes reach and which is licensed here in words. The cuts stand. 16:21 is verbless and states no extent; first person continues to 16:24, and 16:19-16:24 has no connective. The ground of the autograph unit is labelled the writer's reading. The SRA weighs the join of 16:21 with 16:19-16:20 and the closing-formula rule at 16:23. The row states the maranatha class is provisional and referred. The RP form and the SBL division at 16:22 stay (C8). 'The autograph has an RP pilcrow at 16:21.' is S2-06's prescribed sentence and stays.

Your order (verbatim): W6-013: set confidence to medium; reword the named SRA sentence; label the ground in boundary_rationale; add to device_notes one clause naming SBL's sign at 16:22 on the title, and one naming the maranatha referral. This licenses, in words, the field confidence of this row, from high to medium, and any sentence of the row that states the old grade. Span, tiling, unit_type and frontier_flag_considered stay. This licenses, in words, the named field(s) of the named row(s) for this edit only.

Exact spans (verbatim): ["Opening a unit at 16:22 on the curse: the curse and acclamation belong to the autograph's own hand, and the benediction at 16:23 is the next formal element.", "The witnesses also differ in the object of the curse clause, where SBLGNT has a shorter title."]

### R4-W6-014

Decision (verbatim): Adopt, including the confidence move from high to medium, which both lanes reach and which is licensed here in words. The cut stands. TOOLKIT's rule says a closing formula, the grace benediction named, belongs to the unit before it. The row names that rule, states that 16:23 is held as the strategy's listed P13 candidate, and gives its Greek ground: the parallel nominal wishes Ἡ χάρις ... μεθ’ ὑμῶν at 16:23 and Ἡ ἀγάπη μου ... μετὰ πάντων ὑμῶν at 16:24.

Your order (verbatim): W6-014: set confidence to medium; reword the named SRA sentence to name the rule and the parallel wishes. This licenses, in words, the field confidence of this row, from high to medium, and any sentence of the row that states the old grade. Span, tiling, unit_type and frontier_flag_considered stay. This licenses, in words, the named field(s) of the named row(s) for this edit only.

Exact spans (verbatim): ["Joining the benediction to the autograph of 16:21-16:22: the benediction is a separate formal element of the closing, and the love closing completes it."]

### R4-UNCERTAINTY

Decision (verbatim): (a) Mood: adopted. A grammatical label (mood, case, tense) that carries a seam or the rejection of a rival is replaced by what the form measures (verse-initial word, connective-free opening, person) or labelled the writer's reading in the same sentence, in the author's own words. A label that carries nothing stays. Strategy text does not change. 'citation-imperative' stays as strategy I3's term, with RP's form stated at W2-003. (b) Variant disclosure: adopted as CWO-1COR-06, and CWO-1COR-07 is added for the sign-site duty that OL_c06 and LF_c05 raise; both have exact predicates and their own coverage. (c) Tier: adopted as a FIXUP-3 rule over the 16 rows that carry the word, with no sweep tool, because the class is enumerated in full (MEASURED). (d) Cessationist and continuationist readings: on the chapter-level row W5-007 only, the scope question recorded for the end review. (e) C5 goes to the method-change proposer at close; it is tool-enforced from TF-5, in widened form. (f) The 15:50 listing: nothing to add, but the proposal's reason is corrected. It sits at strategy section 7 D, plan for_fable_end_review[4] and E1 S1-03; a walk of the inventory's string values finds 15:50 only under formulae and paragraph_marks, in no end-review list (MEASURED).Added, from the bytes: 10 doubled locators in seven W6 rows, licensed below. Other items are recorded, with no row action, in unresolved_uncertainty.

Your order (verbatim): Mood class: W6-005's sentence on 15:49, and the named spans of W6-009, W6-011 and W6-012. Tier rule: W6-004. Each sentence with the whole word REPORTED names its record in the row's own words (a strategy section number, or hardness_batch_03 via strategy section 7 B). Content beyond what that record states is relabelled ASSUMED, or INFERRED where derived, and is not cut, because rule 9 keeps names and holders. Holders no pinned input gives are UNAVAILABLE. No reading is selected. Fields: boundary_rationale, strongest_rejected_alternative, device_notes of the named rows. Doubled locators: delete the first of an adjacent pair; for 'X reads X "..."' write 'SBLGNT reads X "..."' or 'RP reads X "..."' so the token stays beside the quote. No quoted Greek byte changes. This licenses, in words, the named field(s) of the named row(s) for this edit only.

Exact spans (verbatim): ["At 15:49 the witnesses differ in mood:", "sbl:1Cor.15.35 reads sbl:1Cor.15.35", "sbl:1Cor.15.49 sbl:1Cor.15.49", "rp:1Cor.15.51 reads rp:1Cor.15.51", "sbl:1Cor.16.1 reads sbl:1Cor.16.1", "sbl:1Cor.16.12 reads sbl:1Cor.16.12", "opens a run of asyndetic imperatives addressed to the readers", "the summary imperatives close at 16:14", "on the imperatives", "rp:1Cor.16.19 reads rp:1Cor.16.19", "sbl:1Cor.16.19 sbl:1Cor.16.19", "rp:1Cor.16.22 rp:1Cor.16.22", "sbl:1Cor.16.22 sbl:1Cor.16.22", "sbl:1Cor.16.23 reads sbl:1Cor.16.23"]

### CWO-1COR-06 (corpus-wide order)

Predicate (verbatim): `For each locator matching (?<![\w:])rp:1Cor\.(\d+)\.(\d+)(?!-) in a field, take the Greek run immediately after it (allowing one optional [TAG], then an opening parenthesis or double quote) or immediately before it where the locator is preceded by ' ('. The verse must be in pmarks rp_sbl_differences. Using a skeleton (NFD, casefold, final sigma to sigma, letters alpha to omega only), the quote hits if its token sequence is not contiguous in the SBL verse (kind wording_absent_from_sbl) or is contiguous with a token flagged by an SBL sign (kind on_sign: the whitespace token carrying ⸀ or ⸁, the tokens from ⸂ to ⸃ or from ⸄ to ⸅ inclusive, the token carrying ⸆, ⸇ or ⸈ and the next token). A hit is open unless the row holds the exact token sbl:1Cor.C.V for that verse anywhere; a range token holding the verse does not clear it. One hit per row, verse and token sequence.`

Fields (verbatim): boundary_rationale, strongest_rejected_alternative, each element of boundary_evidence_refs. device_notes is excluded because it is not a warrant field.

Remedy (verbatim): FIXUP-3 adds one boundary_evidence_refs element per true hit in the row's local form, giving the SBL reading, under each row's named order. Widening over C5: C5 requires the quoted words to fall on or across a sign; this also takes quotes whose words are not contiguous in the SBL verse though no sign falls on them, the rp_sbl_note class. False positives are classed by hand, only where the difference is orthography (elision, spelling) or the quote carries no seam or rival argument (§8 rule 2), with the reason recorded per hit. Nothing is narrowed.

### CWO-1COR-07 (corpus-wide order)

Predicate (verbatim): `For each verse in pmarks sbl_variant_sites inside a row's span: listed if a sentence unit (split on (?<=[.;])\s+) of the prose fields, or one element of the list fields, contains sbl:1Cor\.C\.V(?!\d), or contains both (?<![\d:])C:V(?!\d) and the substring SBL. Otherwise the verse is unlisted.`

Fields (verbatim): boundary_rationale, strongest_rejected_alternative, device_notes (sentence units); observed_substrate_signals, boundary_evidence_refs (elements).

Remedy (verbatim): FIXUP-3 adds full C:V strings for the unlisted verses to the row's existing SBL-sign element of observed_substrate_signals, or adds one such element where none exists. It is a bare location list with no quote and no reading. This licenses, in words, observed_substrate_signals of the rows named in the coverage report for that edit only. Source: pmarks sbl_variant_note, 'A row spanning one discloses it'. A sign marks a variant site and nothing else, so a listing supports no seam. W3-005 10:11 and W5-009 14:6 clear through their CWO-1COR-06 elements. New predicate, so nothing is narrowed; false positives: none expected, since a listing is true or missing by construction, and any exception is classed by hand.

CWO-1COR-06 hits on your rows (MEASURED by the installed sweep on the pinned rows; hand class by the controlling agent):

- `W6-004.boundary_rationale` at 1Cor.15.35, kind wording_absent_from_sbl, range_token False, class false_positive:elision, quote `Ἀλλ’ ἐρεῖ τις,`

CWO-1COR-05 hits on your rows (MEASURED); these are the classes the controlling round recorded, 0 of them open true. Do not create a new true hit. Where a reword touches one, keep it as a location or a plain statement.

- `W6-001.boundary_evidence_refs`
- `W6-009.boundary_evidence_refs`
- `W6-010.boundary_evidence_refs`

### CWO-1COR-01 (standing; your new text must not reopen it)

Remedy (verbatim): Every A hit is deleted (a web: ref is never boundary evidence, rule 4). Every B hit is classified support-use (a WEB paragraph or chapter division informing, agreeing, joining, corroborating, leaning, favouring, supporting or confirming; or a pilcrow agreeing, joining, corroborating or confirming) or compliant (a disclaimer that the mark does not drive the seam, or an RP pilcrow that informs without deciding). Support-use clauses are deleted by the owning part. If a deletion leaves boundary_evidence_refs below what the suite accepts, the author stops and reports.

### CWO-1COR-03 (standing; your new text must not reopen it)

Remedy (verbatim): Each offending gram goes back to its owning parts with the named rows; reword, never exclude.

## What you may change (the lander refuses any other difference)

Only the rows and fields an order above names, and for CWO-1COR-06 and -07 the elements the remedies describe. Whatever the order, a row may differ from its pinned value only in: `boundary_rationale`, `strongest_rejected_alternative`, `device_notes`, `observed_substrate_signals`, `boundary_evidence_refs`.
Named exceptions for your part, each only as its order says: `W6-007.confidence`; `W6-013.confidence`; `W6-014.confidence`.
`span`, the tiling, `unit_type`, `decision_id`, `writer_*` and every other field stay byte-identical as JSON values. `confidence` stays except where an order says otherwise; nothing is raised. Within a licensed field, text no order touches stays byte-identical.

If an order cannot be followed as written, or a removal or reword leaves a seam without ground, leave that field at its pinned value and report it under `blocked` with the measured evidence. Do not improvise and do not widen a licence.

## Suite duties your new text must keep (the suite is the mechanical judge)

- placeholder: no unfilled template placeholder (%s, %(x)s, {name}, {0}, {}) in any field of any row.
- Never hand-type Greek: every Greek run you add is sliced by script from the witness bytes, NFC as the witness has it.
- WEB quotations are sliced from `SP\1Cor\1Cor_web_clean.txt`, in double curly quotes, attributed (the A6-b convention).
- register rule: this is a scholar-facing record; no staged file names, internal rule labels, ruling ids, row pointers or process talk in row prose.
- single-witness: keep the literal single-witness disclosure wherever a row already carries it.
- A mark is cited at the verse it FOLLOWS.
- A categorical claim ("no", "only", "every") stands only if the thing is absent from BOTH witnesses.
- 7-gram: add no run of seven words that repeats across rows. Write each row's new sentences for that row: no sentence shared across rows, including between rows of your own part.
- Refs: the DEF-A4-ARGUED entries, each ROLE token, face qualifier and seam pair in boundary_evidence_refs stay; no element is removed unless an order says so; new elements follow the row's local form.
- language_zones and cap_sweep are out of scope (no seam moves).

## What the next check measures (GATE-E4's conditions, verbatim)

1. S5 is a fresh agent distinct from every author and earlier checker, working on the FIXUP-3 applied rows, and returns the readiness ACCEPT form: fit=true, or fit_with_changes with the rows named.
2. run_validator_suite hard members GREEN.
3. ngram7 GREEN at gate 10 with 0 offending rows.
4. Tiling 437/437 with no gap or overlap.
5. CWO-1COR-01 complete with every B hit hand-classed compliant; CWO-1COR-02 0 failures.
6. CWO-1COR-04: 0 open support_use, 0 count_excess, every hit hand-classed. W6-013's false-positive class is re-read against its new bytes (S3-05).
7. CWO-1COR-05 installed by TF-4 with plants passing, every hit classed, 0 open true. W1-011 is re-classed against its new bytes.
8. CWO-1COR-06 and CWO-1COR-07 installed by TF-5 with 10 of 10 plants passing; CWO-1COR-06: every hit classed, 0 open true; CWO-1COR-07: 0 unlisted verses.
9. Every sentence with the whole word REPORTED in boundary_rationale, strongest_rejected_alternative or device_notes of any row names a record.
10. Regex ((?:rp|sbl|web):1Cor\.\d+\.\d+)( reads)? \1\b has 0 hits over boundary_rationale, strongest_rejected_alternative and device_notes.
11. confidence shown at medium for W6-007, W6-013 and W6-014, and unchanged for every other row, with the count of high at 3.
12. Each licensed span shown fixed byte by byte, including S3-01's seven W4 spans; RP and SBL slices unchanged; no change outside the licences.
13. From receipts, at most three 1Cor launches lack completion rows.

## How you check your work (in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx3\W6\work\`)

1. Copy `SP\1Cor\fixup\draft_rows_fixup2_applied.jsonl` byte-identically to `work\rows_applied.jsonl` and replace your part's changed rows with your revised rows (same order).
2. RUN `run_validator_suite.py work\rows_applied.jsonl`: hard_status GREEN, every member GREEN, triage_flags 0.
3. RUN `ngram7.py work\rows_applied.jsonl --gate 10 --full-ids`: no offending gram.
4. RUN `check_tiling.py work\rows_applied.jsonl --range 1Cor.1.1-1Cor.16.24`: GREEN, 437 of 437.
5. RUN `cwo_sweep_1cor.py work\rows_applied.jsonl --out work\cwo.json`: on your rows A 0; CWO-1COR-04 support_use and count_excess 0 (W6 only: the W6-013 false-positive flag may remain, reported as such); CWO-1COR-05 no new hit you cannot class as location or false positive; CWO-1COR-06 only the two false positives may remain (W2-008 7:9, W6-004 15:35); CWO-1COR-07 0 unlisted on your rows.
6. Write your part's rows to `work\slice_W6.jsonl` and RUN `_validate_writer_part_1cor.py work\slice_W6.jsonl --part W6 --book-index`: GREEN.
7. By a script file, on your rows: every sentence with the whole word REPORTED names a record; condition 10's regular expression has 0 hits; each exact span named in an order is gone or changed as ordered; every field not licensed is equal as a JSON value to the pinned row.

## Deliverables

- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx3\W6\fixup3_W6_rows.jsonl`: one JSON object per line, the FULL revised row for every row you changed (and only those), in the pinned rows' order, every untouched field byte-identical as a JSON value.
- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx3\W6\fixup3_W6_changes.json`:

```
{"attempt_id":"cor_fixup3_W6_a1","execution_id":"cor_fixup3_W6_a1#e1","rows_file_sha256":"<pinned rows digest>",
 "changes":[{"row":"<id>","field":"<field>","order":"<ruling id or CWO id>","before":"<exact removed span, or empty>","after":"<exact new span, or empty>",
             "tier":"MEASURED|INFERRED","evidence":"<script + input + output>"}],
 "blocked":[{"order":"<ruling id>","why":"...","evidence":"..."}],
 "checks":{"suite":"<hard_status and members>","ngram7":"...","tiling":"...","cwo":"...","part_validator":"...","unlicensed_fields_equal":true}}
```

## Budget

Keep to roughly 30 tool calls. Report exactly what you ran and what it returned.

## Efficiency contract

M8-EFFICIENCY-V1
EFFICIENCY-CONTRACT: C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md sha256 4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66
Save each complete bounded review unit and exact next cursor in your authorized OUT; partial output is not acceptance. Preserve the unchanged legacy final deliverable contract.
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx3\W6

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"cor_fixup3_W6_a1","execution_id":"cor_fixup3_W6_a1#e1",
 "sources":["<exact paths you read, with sha256>"],
 "outcome":{"changed":[{"what":"<row.field>","why":"<ruling id>"}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search, read no transcript; read only the exact paths named",
 "rows_sha256":"<sha256 of fixup3_W6_rows.jsonl>","changes_sha256":"<sha256 of fixup3_W6_changes.json>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
