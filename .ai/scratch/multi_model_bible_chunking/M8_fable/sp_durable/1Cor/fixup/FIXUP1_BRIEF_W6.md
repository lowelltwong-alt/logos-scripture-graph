# FIXUP-1 AUTHOR BRIEF, part W6 (execution #e1): 1 Corinthians, ruled row repairs (M8_fable, OW-36 queue)

RESEARCH CONTEXT (E-13 preamble): this is scholarly text-structure research on the Greek New Testament (the first letter to the Corinthians, in Greek with a public-domain English translation) for a study corpus. You revise a few fields of candidate reading-unit rows under exact orders, slicing any quotation byte-for-byte from the Robinson-Pierpont Byzantine text (primary), SBLGNT (secondary) and the World English Bible. The material is ancient scripture and its translation; the task is textual and literary editing.

`SP` = `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`

## AUTHORITY (OW-36; it also travels in your launch message)

The owner authorized this Opus orchestration and its subagents for six books: 1 Corinthians, John, Romans,
Revelation, Hebrews and Matthew. The owner's answer, verbatim: "Your six-book queue (Recommended)". authorization_ref
`lowell_chat_2026-10-14_m8_opus_orchestration_six_book_queue`; verify in `SP\..\ERROR_PATTERN_LEDGER.v1.md` lines
3412-3434 only. You run on claude-opus-5-5 as a recorded grader_fallback (OW-25). You read files under the worktree and
write only under your OUT directory; the orchestrator lands and applies your deliverable. You never run git, never write
a receipt and never touch the registry.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W6` already exists. Write your deliverables directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W6\fixup1_W6_rows.jsonl` and `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W6\fixup1_W6_changes.json`. **Never run any existence check, listing, glob or recursive search against it or any
other directory.** A shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W6\work\`, created with
os.makedirs(exist_ok=True) and never tested first.

**EXACT-PATH LAW:** every path you may read is named in this brief. Open each by that exact path. No listing, no glob,
no recursive search. State in your final message that you ran no listing and no glob.

**FORBIDDEN:** any path under `.ai\scratch\multi_model_bible_chunking\` belonging to `M1_cursor`,
`M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, `M6_fable5`, `M7_sol` or
`comparison\`; every other book's directory under SP; every other part's fix-up OUT; the writers', S1's and the
controlling agent's OUT directories, receipts, final messages and evidence notes; every `*_attempt_receipts.jsonl`;
transcripts; any file not named in this brief. Nothing from another book passes as 1 Corinthians' (E-65).

**Running Python:** always set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` and run `python -B`. Never run any tool not marked RUN below. Never pass `--write`. Never edit any file under the
worktree.

## Your role

You are the FIXUP-1 AUTHOR for part W6. Attempt `cor_fixup1_W6_a1`, execution `cor_fixup1_W6_a1#e1`. You authored none of the rows, the
review or the rulings. The controlling agent (execution cor_controlling_rulings_r1_a1#e1) ruled on the S1 review; its
orders to your part are quoted verbatim below, with the corpus-wide orders and the orchestrator's classified CWO-1COR-01
hits on your rows (S1-02b: they are appended to your orders). You carry out exactly those orders: nothing outside the
named rows and fields changes (S1-ROUTING). You do not adjudicate a divided reading, select a textual reading or
tradition, settle a contested interpretation, move any seam or raise any confidence.

## PINNED INPUTS

These are the sha256 digests as this brief was built. Record the digest of each input as you read it; a mismatch is a
hard stop: report it and stop.

| input | sha256 |
|---|---|
| `SP\1Cor\writer\draft_rows_combined.jsonl` | `3d328c8afa9f2616b963413a15041d916e0d54ad474835da4f92af90b2588af6` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E1.v1.json` | `93e5918b10b17842e5700471087290036549f4ab2327220d518967c49b53dc90` |
| `SP\1Cor\review\cwo_1cor_baseline_report.v1.json` | `451c051d1a5ee2827904a6da863b15214bdc101dcb942325d77da8427367cd2b` |
| `SP\1Cor\book_strategy_1Cor.md` | `70e344fed9f0f64654baa97dff80e03b706a1288b47de182628dc453212e39ca` |
| `SP\1Cor\tools\TOOLKIT.md` | `49de0883f5cbed7fd9e25fdc8a156a083f8794bdd6490de1b0eee82aa2c7361e` |
| `SP\1Cor\1Cor_rp.txt` | `94f7cf39fbd87f7952aba3ca957b7a4790edfb5d120dceffc8deac0ad0ccc2eb` |
| `SP\1Cor\1Cor_sbl.txt` | `354b6dcf5b5f43a24dd85918e9759eeeb3153dc5284ab707a4167b64919456ff` |
| `SP\1Cor\1Cor_web_clean.txt` | `7c8224ccf9eb0a06df20c5b2289d33ea32267dda136e88e73ea5761807cf0778` |
| `SP\1Cor\1cor_device_inventory.json` | `62c608d775710f56040d3889db9c2cc2a98f40589d15e9b11b8ba2af9b3795ad` |
| `SP\1Cor\pmarks_1Cor.json` | `5cd9055a8ecbfbc8dcf0f5dbc43e7bedbb0e69dc4fb7e8d9000e164e074c7fd7` |
| `SP\1Cor\tools\run_validator_suite.py` | `ebe7197b35635d9f8cbf88914219003e32816ba37173f00205668eb5aab2dbb4` |
| `SP\1Cor\tools\ngram7.py` | `2dc3a80d5785d2048fc7b17dac093a47c26f10599922bd083bb7158de10d0230` |
| `SP\1Cor\tools\check_tiling.py` | `71b5ee67b98eeb6815515928448b52baa5cac45692afe09212acf2f85d17bbcf` |
| `SP\1Cor\writer_lanes\_validate_writer_part_1cor.py` | `59ef3318dbd98201e57107e9747f17b579f750116ba875061493fbd3012a46e9` |
| `SP\campaign\grader_models.v1.json` | `cf88544383c707c6e2d87c75829740d696ede0e537403284da0ee84cc239526d` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `4dc47a3e406c7d5a2ca7bf6acd27960f9390424fe236d84b4083e586bb200b9b` |

How you may use each input:

- `SP\1Cor\writer\draft_rows_combined.jsonl`: READ your part's rows in full; other rows only where you check a fact. You change ONLY the row-fields in the table below.
- `SP\1Cor\review\1cor_controlling_agent_rulings_E1.v1.json`: READ where you check a ruling's context (your orders and the CWO texts are quoted verbatim below).
- `SP\1Cor\review\cwo_1cor_baseline_report.v1.json`: READ where you check a CWO-1COR-01 class (your rows' hits are quoted below).
- `SP\1Cor\book_strategy_1Cor.md`: READ section 8 in full. BINDING.
- `SP\1Cor\tools\TOOLKIT.md`: READ where you check a suite member's contract. Where it and a tool's code differ, the code is the contract.
- `SP\1Cor\1Cor_rp.txt`: READ where you slice Greek bytes (Robinson-Pierpont Byzantine text, the primary witness).
- `SP\1Cor\1Cor_sbl.txt`: READ where you slice Greek bytes (SBLGNT, the secondary witness, signs kept).
- `SP\1Cor\1Cor_web_clean.txt`: READ where you slice WEB bytes.
- `SP\1Cor\1cor_device_inventory.json`: READ where you check a device class or key.
- `SP\1Cor\pmarks_1Cor.json`: READ where you check a mark.
- `SP\1Cor\tools\run_validator_suite.py`: RUN on a PRIVATE COPY of the rows in your OUT\work only (it writes its report beside its input). It runs every suite member itself; run no member directly except ngram7.py below.
- `SP\1Cor\tools\ngram7.py`: RUN on your private copy with `--gate 10 --full-ids` (it writes nothing).
- `SP\1Cor\tools\check_tiling.py`: RUN on your private copy (it writes nothing).
- `SP\1Cor\writer_lanes\_validate_writer_part_1cor.py`: RUN on a slice of your private copy holding only your part's rows, with `--part W6 --book-index` (it writes nothing).
- `SP\campaign\grader_models.v1.json`: READ where you check your model role (grader_fallback).
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 3412-3434 only (OW-36, the owner's grant).

## The orders to part W6 (quoted from the rulings file, sha256 93e5918b10b17842e5700471087290036549f4ab2327220d518967c49b53dc90)

### S1-01b

Decision (verbatim): Same remedy as S1-01 for W6-002, W6-003, W6-008, W6-011, W6-012, and the W6 web: refs these rows carry are deleted.

Your order (verbatim): Apply the S1-01 deletions to the named rows; keep at most one bare RP pilcrow location item per row.

Exact spans (verbatim): ["W6-002, W6-003, W6-008, W6-011, W6-012 observed_substrate_signals: every item containing 'WEB paragraph'", "same rows boundary_rationale and strongest_rejected_alternative: every clause containing 'WEB paragraph'", "boundary_evidence_refs: web:1Cor.15.12 (W6-002), web:1Cor.15.20 (W6-003), web:1Cor.16.5 and web:1Cor.16.10 (W6-008), web:1Cor.16.15 and web:1Cor.16.19 (W6-011), web:1Cor.16.19 and web:1Cor.16.21 (W6-012)"]

### S1-02

Decision (verbatim): Major. The clauses that offer a WEB paragraph or a pilcrow as agreement, corroboration or joining evidence for a seam are deleted. W6-006 is added: its WEB-paragraph mentions in boundary_rationale, strongest_rejected_alternative, boundary_evidence_refs and observed_substrate_signals are deleted, and its 'RP pilcrow at 15:50.' sentence is kept only as a bare observed_substrate_signals location item. Pilcrow wording of the form 'informs without deciding' is compliant under rule 5 and stays. No replacement formula is prescribed.

Your order (verbatim): Delete the support clauses and the W6-006 WEB-paragraph material.

Exact spans (verbatim): ["W6-010 boundary_rationale: 'Both witnesses of layout agree here: RP pilcrow at 16:13, WEB paragraph at 16:13'", "W6-002 boundary_rationale: the sentence pairing a mark word with 'corroborat'", "W6-012 boundary_rationale: the sentence pairing a mark word with 'corroborat'", "W6-006 boundary_rationale: 'RP pilcrow at 15:50.' and 'WEB paragraph at 15:51.'", "W6-006 strongest_rejected_alternative: 'with the WEB paragraph'", "W6-006 boundary_evidence_refs: 'web:1Cor.15.51 (WEB paragraph)', 'web:1Cor.15.56 (WEB paragraph)'", "W6-006 observed_substrate_signals: 'WEB paragraph starts at 15:51 and 15:56'"]

### S1-02b

Decision (verbatim): Minor-class instances of the same defect are fixed on W3, W4, W5 and W6, and the class is swept by CWO-1COR-01, whose classified support-use hits are appended to the owning part orders before fix-up launches.

Your order (verbatim): Delete the WEB-paragraph mentions and refs.

Exact spans (verbatim): ["W6-004 and W6-007 boundary_rationale: every clause containing 'WEB paragraph'", "boundary_evidence_refs: web:1Cor.15.29 (W6-004); web:1Cor.16.1, web:1Cor.16.5 (W6-007)"]

### S1-03

Decision (verbatim): W6-006 deletes the 7:29 analogy clause and the ref rp:1Cor.7.29, with no replacement analogy. Its confidence is not raised. The 15:50/15:51 seam question stays with fable_end_review, unchanged.

Your order (verbatim): Delete the clause and the ref; add nothing in their place; confidence stays medium_low or lower.

Exact spans (verbatim): ["W6-006 boundary_rationale: 'the formula of 15:50 also opens a unit at 7:29, which favours the onset reading without settling it'", "W6-006 boundary_evidence_refs: 'rp:1Cor.7.29 (the same summarising formula opens a unit there)'"]

### S1-05

Decision (verbatim): Narrowed to five phrases. The proposal's blanket removal of end-review language is not adopted: 'listed for Fable's end review' disclosures that the strategy directs (W4-001..W4-004, W6-006, W6-010..W6-012) stay.

Your order (verbatim): Name the span.

Exact spans (verbatim): ["W6-005 device_notes: 'the unit that opens at 15:50' becomes the explicit span of that unit"]

### CWO-1COR-01 (corpus-wide order)

Predicate (verbatim): `A: an element of boundary_evidence_refs matching ^\s*web: and matching (?i)WEB paragraph|paragraph start|DISCLOSURE-mark. B: a sentence (split on (?<=[.;])\s+) of boundary_rationale, strongest_rejected_alternative or device_notes matching (?i)pilcrow|WEB paragraph|paragraph start|chapter division and also matching (?i)corroborat|agree|join|inform|favour|support|lean|confirm.`

Fields (verbatim): boundary_evidence_refs, boundary_rationale, strongest_rejected_alternative, device_notes; all 70 rows of SP\1Cor\writer\draft_rows_combined.jsonl

Remedy (verbatim): Every A hit is deleted (a web: ref is never boundary evidence, rule 4). Every B hit is classified support-use (a WEB paragraph or chapter division informing, agreeing, joining, corroborating, leaning, favouring, supporting or confirming; or a pilcrow agreeing, joining, corroborating or confirming) or compliant (a disclaimer that the mark does not drive the seam, or an RP pilcrow that informs without deciding). Support-use clauses are deleted by the owning part. If a deletion leaves boundary_evidence_refs below what the suite accepts, the author stops and reports.

### CWO-1COR-03 (corpus-wide order)

Predicate (verbatim): `ngram7 as installed with TF-2, default gate 10, --full-ids, on the applied combined rows: any 7-gram shared by 10 or more rows.`

Fields (verbatim): the fields ngram7.prose() walks

Remedy (verbatim): Each offending gram goes back to its owning parts with the named rows; reword, never exclude.

### CWO-1COR-01 hits on your rows (MEASURED by the installed sweep on the pinned rows; classes by the orchestrator, by the remedy text above)

A hits (each is deleted):

- `W6-001` boundary_evidence_refs[10]: "web:1Cor.15.1 (WEB paragraph)"
- `W6-001` boundary_evidence_refs[11]: "web:1Cor.15.3 (WEB paragraph)"
- `W6-002` boundary_evidence_refs[10]: "web:1Cor.15.12 (WEB paragraph)"
- `W6-003` boundary_evidence_refs[11]: "web:1Cor.15.20 (WEB paragraph)"
- `W6-004` boundary_evidence_refs[9]: "web:1Cor.15.29 (WEB paragraph)"
- `W6-005` boundary_evidence_refs[14]: "web:1Cor.15.35 (WEB paragraph)"
- `W6-005` boundary_evidence_refs[15]: "web:1Cor.15.42 (WEB paragraph)"
- `W6-005` boundary_evidence_refs[16]: "web:1Cor.15.45 (WEB paragraph)"
- `W6-006` boundary_evidence_refs[13]: "web:1Cor.15.51 (WEB paragraph)"
- `W6-006` boundary_evidence_refs[14]: "web:1Cor.15.56 (WEB paragraph)"
- `W6-007` boundary_evidence_refs[11]: "web:1Cor.16.1 (WEB paragraph)"
- `W6-007` boundary_evidence_refs[12]: "web:1Cor.16.5 (WEB paragraph)"
- `W6-008` boundary_evidence_refs[12]: "web:1Cor.16.5 (WEB paragraph)"
- `W6-008` boundary_evidence_refs[13]: "web:1Cor.16.10 (WEB paragraph)"
- `W6-009` boundary_evidence_refs[7]: "web:1Cor.16.12 (WEB paragraph)"
- `W6-009` boundary_evidence_refs[8]: "web:1Cor.16.13 (WEB paragraph)"
- `W6-010` boundary_evidence_refs[8]: "web:1Cor.16.13 (WEB paragraph)"
- `W6-010` boundary_evidence_refs[9]: "web:1Cor.16.15 (WEB paragraph)"
- `W6-011` boundary_evidence_refs[8]: "web:1Cor.16.15 (WEB paragraph)"
- `W6-011` boundary_evidence_refs[9]: "web:1Cor.16.19 (WEB paragraph)"
- `W6-012` boundary_evidence_refs[7]: "web:1Cor.16.19 (WEB paragraph)"
- `W6-012` boundary_evidence_refs[8]: "web:1Cor.16.21 (WEB paragraph)"
- `W6-013` boundary_evidence_refs[7]: "web:1Cor.16.21 (WEB paragraph)"

B hits:

- `W6-001.boundary_rationale` **compliant** (an RP pilcrow that informs without deciding ('informs that edge and does not decide it')); disposition: none. Sentence: "RP pilcrow at 15:12 (the close seam): it informs that edge and does not decide it."
- `W6-002.boundary_rationale` **support-use** (a pilcrow and a WEB paragraph corroborating (also S1-02)); disposition: delete the sentence 'RP pilcrow at 15:12 and WEB paragraph at 15:12 corroborate the conditional onset.'. Sentence: "Front face: rp:1Cor.15.12 \"Εἰ δὲ χριστὸς κηρύσσεται ὅτι ἐκ νεκρῶν ἐγήγερται,\" states the premise as a condition and asks how some deny resurrection, web:1Cor.15.12 “how do some among you say that there is no resurrection of the dead?” RP pilcrow at 15:12 and WEB paragraph at 15:12 corroborate the conditional onset."
- `W6-002.device_notes` **compliant** (an RP pilcrow that informs without deciding (the same sentence rests the onset on the conditional)); disposition: none. Sentence: "the onset rests on the conditional and the pilcrow informs it."
- `W6-005.boundary_rationale` **support-use** (a WEB paragraph informing: the next clause 'the WEB also starts a paragraph at 15:35' pairs the WEB start with the informing pilcrow (the predicate's split at ';' separates them; classified on the pair)); disposition: delete the WEB clause; the pilcrow clause stays only as informing without deciding. Sentence: "An RP pilcrow at 15:35 informs the onset;"
- `W6-010.boundary_rationale` **support-use** (a pilcrow and a WEB paragraph agreeing (also S1-02)); disposition: delete 'Both witnesses of layout agree here: RP pilcrow at 16:13, WEB paragraph at 16:13.'. Sentence: "Front face: rp:1Cor.16.13 \"Γρηγορεῖτε, στήκετε ἐν τῇ πίστει,\" opens four asyndetic imperatives, web:1Cor.16.13 “Watch! Stand firm in the faith!” Both witnesses of layout agree here: RP pilcrow at 16:13, WEB paragraph at 16:13."
- `W6-012.boundary_rationale` **support-use** (a pilcrow and a WEB paragraph corroborating (also S1-02)); disposition: delete the sentence 'RP pilcrow at 16:19 and WEB paragraph at 16:19 corroborate the greeting formula, which carries the onset.'; the greeting-formula content stays. Sentence: "Front face: rp:1Cor.16.19 \"Ἀσπάζονται ὑμᾶς αἱ ἐκκλησίαι τῆς Ἀσίας·\" opens the third-person greetings from the churches of Asia, web:1Cor.16.19 “The assemblies of Asia greet you.” RP pilcrow at 16:19 and WEB paragraph at 16:19 corroborate the greeting formula, which carries the onset."

A compliant hit stays as it is. A support-use hit is cured by deleting the support-use clause; the content argument
stays, reworded only as far as the deletion requires. No replacement formula is prescribed.

## What you may change (the lander refuses any other difference)

| row | field | licensed by |
|---|---|---|
| W6-001 | boundary_evidence_refs | CWO-1COR-01 (deletion only) |
| W6-002 | boundary_evidence_refs | CWO-1COR-01, S1-01b (deletion only) |
| W6-002 | boundary_rationale | CWO-1COR-01, S1-01b, S1-02 |
| W6-002 | observed_substrate_signals | S1-01b |
| W6-003 | boundary_evidence_refs | CWO-1COR-01, S1-01b (deletion only) |
| W6-003 | boundary_rationale | S1-01b |
| W6-003 | observed_substrate_signals | S1-01b |
| W6-004 | boundary_evidence_refs | CWO-1COR-01, S1-02b (deletion only) |
| W6-005 | boundary_evidence_refs | CWO-1COR-01 (deletion only) |
| W6-005 | boundary_rationale | CWO-1COR-01 |
| W6-005 | device_notes | S1-05 |
| W6-006 | boundary_evidence_refs | CWO-1COR-01, S1-02, S1-03 (deletion only) |
| W6-006 | boundary_rationale | S1-02, S1-03 |
| W6-006 | observed_substrate_signals | S1-02 |
| W6-006 | strongest_rejected_alternative | S1-02 |
| W6-007 | boundary_evidence_refs | CWO-1COR-01, S1-02b (deletion only) |
| W6-007 | boundary_rationale | S1-02b |
| W6-008 | boundary_evidence_refs | CWO-1COR-01, S1-01b (deletion only) |
| W6-008 | boundary_rationale | S1-01b |
| W6-008 | observed_substrate_signals | S1-01b |
| W6-009 | boundary_evidence_refs | CWO-1COR-01 (deletion only) |
| W6-010 | boundary_evidence_refs | CWO-1COR-01 (deletion only) |
| W6-010 | boundary_rationale | CWO-1COR-01, S1-02 |
| W6-011 | boundary_evidence_refs | CWO-1COR-01, S1-01b (deletion only) |
| W6-011 | boundary_rationale | S1-01b |
| W6-011 | observed_substrate_signals | S1-01b |
| W6-012 | boundary_evidence_refs | CWO-1COR-01, S1-01b (deletion only) |
| W6-012 | boundary_rationale | CWO-1COR-01, S1-01b, S1-02 |
| W6-012 | observed_substrate_signals | S1-01b |
| W6-013 | boundary_evidence_refs | CWO-1COR-01 (deletion only) |

Not licensed although an order's row list names them (MEASURED: the field holds no 'WEB paragraph'): W6-002.strongest_rejected_alternative (no 'WEB paragraph'); W6-003.strongest_rejected_alternative (no 'WEB paragraph'); W6-008.strongest_rejected_alternative (no 'WEB paragraph'); W6-011.strongest_rejected_alternative (no 'WEB paragraph'); W6-012.strongest_rejected_alternative (no 'WEB paragraph'); W6-004.boundary_rationale (no 'WEB paragraph'). Leave them unchanged.

`boundary_evidence_refs` is deletion only: the new list must be the old list with some elements removed, order kept,
no element added or edited. The only elements you may remove:

- `W6-001`: "web:1Cor.15.1 (WEB paragraph)"; "web:1Cor.15.3 (WEB paragraph)"
- `W6-002`: "web:1Cor.15.12 (WEB paragraph)"
- `W6-003`: "web:1Cor.15.20 (WEB paragraph)"
- `W6-004`: "web:1Cor.15.29 (WEB paragraph)"
- `W6-005`: "web:1Cor.15.35 (WEB paragraph)"; "web:1Cor.15.42 (WEB paragraph)"; "web:1Cor.15.45 (WEB paragraph)"
- `W6-006`: "web:1Cor.15.51 (WEB paragraph)"; "web:1Cor.15.56 (WEB paragraph)"; "rp:1Cor.7.29 (the same summarising formula opens a unit there)"
- `W6-007`: "web:1Cor.16.1 (WEB paragraph)"; "web:1Cor.16.5 (WEB paragraph)"
- `W6-008`: "web:1Cor.16.5 (WEB paragraph)"; "web:1Cor.16.10 (WEB paragraph)"
- `W6-009`: "web:1Cor.16.12 (WEB paragraph)"; "web:1Cor.16.13 (WEB paragraph)"
- `W6-010`: "web:1Cor.16.13 (WEB paragraph)"; "web:1Cor.16.15 (WEB paragraph)"
- `W6-011`: "web:1Cor.16.15 (WEB paragraph)"; "web:1Cor.16.19 (WEB paragraph)"
- `W6-012`: "web:1Cor.16.19 (WEB paragraph)"; "web:1Cor.16.21 (WEB paragraph)"
- `W6-013`: "web:1Cor.16.21 (WEB paragraph)"

MEASURED (the orchestrator's simulation on a scratch copy): deleting every element above for every part leaves each
row at least 4 refs, and the suite's refs members stay GREEN (W6-001 12->10, W6-002 11->10, W6-003 12->11, W6-004 10->9, W6-005 17->14, W6-006 15->12, W6-007 13->11, W6-008 14->12, W6-009 9->7, W6-010 10->8, W6-011 10->8, W6-012 9->7, W6-013 8->7). The
suite is the judge of "below what the suite accepts"; if your applied copy turns refs_mirror or role_tokens RED, stop
and report it (CWO-1COR-01 remedy). Adding a ref is outside your licence.

The current text of each of those fields, as pinned (JSON values):

- `W6-001.boundary_evidence_refs`: ["web:1Cor.15.1-1Cor.15.11 (span: tradition and its application)", "rp:1Cor.14.40 (order maxim closes the gifts unit)", "rp:1Cor.15.1 (disclosure formula with vocative; parelabete)", "rp:1Cor.15.3 (tradition handed on and received)", "rp:1Cor.15.8 (the apostle appends his own sighting)", "rp:1Cor.15.12 (conditional opens the following argument; RP pilcrow)", "sbl:1Cor.15.1 (SBLGNT agrees on the opening clause)", "sbl:1Cor.15.4 (SBL variant site inside the creed)", "sbl:1Cor.15.6 (SBL variant site inside the creed)", "sbl:1Cor.15.10 (SBL variant site inside the application)", "web:1Cor.15.1 (WEB paragraph)", "web:1Cor.15.3 (WEB paragraph)"]
- `W6-002.boundary_evidence_refs`: ["web:1Cor.15.12-1Cor.15.19 (span: the if-chain against the deniers)", "rp:1Cor.15.11 (back face: preaching and believing)", "rp:1Cor.15.12 (conditional onset; RP pilcrow)", "rp:1Cor.15.19 (conclusion of the if-chain)", "rp:1Cor.15.20 (adversative affirmation opens the following unit; RP pilcrow)", "web:1Cor.15.20-1Cor.15.28 (counter-assertion that the rejected merge would absorb)", "sbl:1Cor.15.12 (SBL variant site in the clause naming the deniers)", "sbl:1Cor.15.14 (SBL variant site)", "sbl:1Cor.15.17 (SBL variant site)", "sbl:1Cor.15.19 (SBL variant site)", "web:1Cor.15.12 (WEB paragraph)"]
- `W6-002.boundary_rationale`: "Back face: the tradition unit closes at 15:11 with the shared preaching and believing. Front face: rp:1Cor.15.12 \"Εἰ δὲ χριστὸς κηρύσσεται ὅτι ἐκ νεκρῶν ἐγήγερται,\" states the premise as a condition and asks how some deny resurrection, web:1Cor.15.12 “how do some among you say that there is no resurrection of the dead?” RP pilcrow at 15:12 and WEB paragraph at 15:12 corroborate the conditional onset. Interior: the if-clauses of 15:13-15:18 draw out what follows if resurrection is denied. Close: the chain ends at 15:19 on the pitiable state of those whose hope is confined to this life; at 15:20 rp:1Cor.15.20 \"Νυνὶ δὲ\" reverses the hypothesis with an emphatic affirmation. RP pilcrow at 15:20 (close seam), with a WEB paragraph there too."
- `W6-002.observed_substrate_signals`: ["conditional onset Ei de (15:12, glossed)", "RP pilcrow (15:12)", "RP pilcrow on the close seam (15:20)", "WEB paragraph (15:12)", "SBL variant sites (15:12, 15:14, 15:17, 15:19)"]
- `W6-003.boundary_evidence_refs`: ["web:1Cor.15.20-1Cor.15.28 (span: firstfruits and the ordered sequence)", "rp:1Cor.15.19 (back face: end of the reductio)", "rp:1Cor.15.20 (adversative affirmation; RP pilcrow)", "rp:1Cor.15.23 (order of the sequence, interior)", "rp:1Cor.15.28 (final subjection closes the sequence)", "rp:1Cor.15.29 (Epei opens the following unit; RP pilcrow)", "sbl:1Cor.15.20 (SBLGNT lacks the closing verb)", "sbl:1Cor.15.21 (SBL variant site)", "sbl:1Cor.15.24 (SBL variant site)", "sbl:1Cor.15.25 (SBL variant site)", "sbl:1Cor.15.28 (SBL variant site)", "web:1Cor.15.20 (WEB paragraph)"]
- `W6-003.boundary_rationale`: "Back face: the reductio closes at 15:19. Front face: rp:1Cor.15.20 \"Νυνὶ δὲ χριστὸς ἐγήγερται ἐκ νεκρῶν,\" affirms the resurrection of Christ against the hypothesis, web:1Cor.15.20 “But now Christ has been raised from the dead.” RP pilcrow at 15:20 and WEB paragraph at 15:20 stand on the onset. Interior: 15:23, rp:1Cor.15.23 \"Ἕκαστος δὲ ἐν τῷ ἰδίῳ τάγματι·\", sets out the order of firstfruits, those of Christ at his coming, and the end; it is interior to the sequence and opens nothing. Close: the sequence ends at 15:28 with the final subjection of the Son. Across the seam, 15:29 opens with rp:1Cor.15.29 \"Ἐπεὶ τί ποιήσουσιν\", turning from the eschatological order to the readers' own practice. RP pilcrow at 15:29 (close seam)."
- `W6-003.observed_substrate_signals`: ["nyni de onset (15:20, glossed)", "RP pilcrow (15:20)", "RP pilcrow on the close seam (15:29)", "WEB paragraph (15:20)", "interior ordering clause (15:23)"]
- `W6-004.boundary_evidence_refs`: ["web:1Cor.15.29-1Cor.15.34 (span: argument from practice and peril)", "rp:1Cor.15.28 (back face: final subjection)", "web:1Cor.15.20-1Cor.15.28 (sequence the rejected join would absorb)", "rp:1Cor.15.29 (Epei onset; RP pilcrow)", "rp:1Cor.15.34 (call to wake up closes the move)", "rp:1Cor.15.35 (objection opener; RP pilcrow)", "sbl:1Cor.15.29 (SBL variant site at the end of the verse)", "sbl:1Cor.15.31 (SBL variant site)", "sbl:1Cor.15.34 (SBL variant site)", "web:1Cor.15.29 (WEB paragraph)"]
- `W6-005.boundary_evidence_refs`: ["web:1Cor.15.35-1Cor.15.49 (span: objection and reply)", "rp:1Cor.15.34 (back face: call to wake up)", "rp:1Cor.15.35 (objection opener; RP pilcrow)", "sbl:1Cor.15.35 (SBLGNT reads the opener without elision)", "rp:1Cor.15.42 (application of the analogies, interior)", "rp:1Cor.15.45 (scripture citation formula, interior)", "rp:1Cor.15.49 (close of the reply; subjunctive verb)", "sbl:1Cor.15.49 (SBL variant site: future indicative)", "rp:1Cor.15.50 (summarising formula; RP pilcrow)", "sbl:1Cor.15.36 (SBL variant site)", "sbl:1Cor.15.38 (SBL variant site)", "sbl:1Cor.15.39 (SBL variant site)", "sbl:1Cor.15.44 (SBL variant site)", "sbl:1Cor.15.47 (SBL variant site)", "web:1Cor.15.35 (WEB paragraph)", "web:1Cor.15.42 (WEB paragraph)", "web:1Cor.15.45 (WEB paragraph)"]
- `W6-005.boundary_rationale`: "Back face: the call to wake up closes the practice argument at 15:34. Front face: rp:1Cor.15.35 \"Ἀλλ’ ἐρεῖ τις,\" introduces an imagined questioner asking how the dead are raised, web:1Cor.15.35 “But someone will say,” SBLGNT gives the opener without elision: sbl:1Cor.15.35 reads sbl:1Cor.15.35 \"Ἀλλὰ ἐρεῖ τις·\". An RP pilcrow at 15:35 informs the onset; the WEB also starts a paragraph at 15:35. Interior: 15:42, rp:1Cor.15.42 \"Οὕτως καὶ ἡ ἀνάστασις τῶν νεκρῶν.\", applies the seed and body analogies, and 15:45, rp:1Cor.15.45 \"Οὕτως καὶ γέγραπται,\", cites scripture for the Adam contrast; both continue the reply. Close: the reply ends at 15:49 on bearing the heavenly likeness. RP pilcrow at 15:50 (close seam), where a summarising formula follows. One-move statement for a fifteen-verse unit: the questioner's two questions at 15:35 are answered by analogy and by the Adam contrast through 15:49, and no seam inside the reply carries signals on both faces."
- `W6-005.device_notes`: "At 15:49 the witnesses differ in mood: rp:1Cor.15.49 has the subjunctive rp:1Cor.15.49 \"φορέσωμεν\". In SBLGNT the verb is future, sbl:1Cor.15.49 sbl:1Cor.15.49 \"⸀φορέσομεν\", at an SBL variant site at 15:49; WEB follows the subjunctive and carries a footnote marker at 15:49. SBL variant sites at 15:36, 15:38, 15:39, 15:44 and 15:47 lie inside the reply and touch no edge. Backward reading of the close: 15:50 can be read as the summary that ends this reply; that rival is disclosed on the unit that opens at 15:50. Witness lines for the objection: Robinson-Pierpont Byzantine Textform (Unlicense) for objection wording; SBLGNT (CC BY 4.0) objection comparison."
- `W6-006.boundary_evidence_refs`: ["web:1Cor.15.50-1Cor.15.58 (span: mystery, victory, closing charge)", "web:1Cor.15.35-1Cor.15.49 (backward reading: the bodies reply)", "rp:1Cor.15.49 (back face: image of the heavenly)", "rp:1Cor.15.50 (touto de phemi with vocative; RP pilcrow)", "rp:1Cor.15.51 (idou and the mystery; rival onset)", "sbl:1Cor.15.51 (SBL variant site: SBLGNT lacks the particle)", "rp:1Cor.7.29 (the same summarising formula opens a unit there)", "rp:1Cor.15.57 (thanksgiving to God)", "rp:1Cor.15.58 (hoste with vocative closes the argument)", "rp:1Cor.16.1 (heading on the far side of the seam)", "sbl:1Cor.15.50 (SBL variant site)", "sbl:1Cor.15.54 (SBL variant site)", "sbl:1Cor.15.55 (SBL variant site)", "web:1Cor.15.51 (WEB paragraph)", "web:1Cor.15.56 (WEB paragraph)"]
- `W6-006.boundary_rationale`: "Back face: the Adam contrast ends at 15:49. Front face, the working answer: rp:1Cor.15.50 \"Τοῦτο δέ φημι, ἀδελφοί,\" is a summarising formula with vocative, and the flesh-and-blood statement it introduces sets the premise that the mystery resolves. RP pilcrow at 15:50. The rival onset is 15:51, where rp:1Cor.15.51 \"Ἰδού, μυστήριον ὑμῖν λέγω·\" announces the mystery. WEB paragraph at 15:51. Backward reading disclosed: 15:50 can close 15:35-15:49 as the summary of the bodies reply, with this unit then opening at 15:51 on the idou formula; the formula of 15:50 also opens a unit at 7:29, which favours the onset reading without settling it. Close: the thanksgiving of 15:57, rp:1Cor.15.57 \"τῷ δὲ θεῷ χάρις\", and the hoste exhortation with vocative at 15:58, rp:1Cor.15.58 \"Ὥστε, ἀδελφοί μου ἀγαπητοί,\", conclude the resurrection argument, and the exhortation is the closing verse of its unit. Across the seam, 16:1 begins with a peri de heading."
- `W6-006.observed_substrate_signals`: ["touto_de_phemi (15:50)", "adelphoi vocative (15:50)", "idou (15:51)", "charis_to_theo (15:57)", "adelphoi_mou_agapetoi with hoste (15:58)", "RP pilcrow (15:50)", "WEB paragraph starts at 15:51 and 15:56"]
- `W6-006.strongest_rejected_alternative`: "Opening at 15:51 on idou with the WEB paragraph, leaving 15:50 to end the reply of 15:35-15:50; it is a contested seam, held at a lowered confidence and listed for Fable's end review."
- `W6-007.boundary_evidence_refs`: ["web:1Cor.16.1-1Cor.16.4 (span: the collection arrangements)", "rp:1Cor.15.58 (back face: closing hoste charge)", "rp:1Cor.16.1 (peri de heading)", "sbl:1Cor.16.1 (SBLGNT spells the collection noun differently)", "web:1Cor.16.2 (weekly day reference, metadata)", "rp:1Cor.16.4 (travel possibility closes the arrangements)", "rp:1Cor.16.5 (itinerary opens the following unit)", "web:1Cor.16.5-1Cor.16.9 (itinerary the rejected extension would absorb)", "sbl:1Cor.16.2 (SBL variant site)", "sbl:1Cor.16.3 (SBL variant site)", "sbl:1Cor.16.4 (SBL variant site)", "web:1Cor.16.1 (WEB paragraph)", "web:1Cor.16.5 (WEB paragraph)"]
- `W6-007.boundary_rationale`: "Back face: the resurrection argument closes at 15:58 with the exhortation rp:1Cor.15.58 \"Ὥστε, ἀδελφοί μου ἀγαπητοί,\", its closing verse. Front face: rp:1Cor.16.1 opens with the heading rp:1Cor.16.1 \"Περὶ δὲ τῆς λογίας\", a peri de topic marker. WEB renders it web:1Cor.16.1 “Now concerning the collection for the saints:” WEB paragraph at 16:1. Close: the arrangements end at 16:4 with the possibility that the apostle travels with the bearers. Across the seam, 16:5 turns to his own itinerary, rp:1Cor.16.5 \"Ἐλεύσομαι δὲ πρὸς ὑμᾶς,\", with a WEB paragraph at 16:5."
- `W6-008.boundary_evidence_refs`: ["web:1Cor.16.5-1Cor.16.11 (span: itinerary and the envoy)", "rp:1Cor.16.4 (back face: bearers of the gift)", "rp:1Cor.16.5 (travel statement onset)", "web:1Cor.16.8 (Pentecost, metadata)", "rp:1Cor.16.10 (Timothy commended; RP pilcrow, interior)", "sbl:1Cor.16.10 (SBL variant site at the end of the verse)", "rp:1Cor.16.11 (Timothy sent on, close)", "rp:1Cor.16.12 (heading on the far side of the seam)", "sbl:1Cor.16.6 (SBL variant site)", "sbl:1Cor.16.7 (SBL variant site)", "sbl:1Cor.16.8 (SBL variant site)", "sbl:1Cor.16.11 (SBL variant site)", "web:1Cor.16.5 (WEB paragraph)", "web:1Cor.16.10 (WEB paragraph)"]
- `W6-008.boundary_rationale`: "Back face: the collection arrangements close at 16:4. Front face: rp:1Cor.16.5 \"Ἐλεύσομαι δὲ πρὸς ὑμᾶς,\" announces the apostle's coming after Macedonia, a travel statement with a WEB paragraph at 16:5. Interior: the delay in Ephesus up to the feast (16:8) and the open door of 16:9 explain the delay; at 16:10, rp:1Cor.16.10 \"Ἐὰν δὲ ἔλθῃ Τιμόθεος,\", the envoy Timothy is commended. RP pilcrow at 16:10 and WEB paragraph at 16:10 fall inside the unit. Close: 16:11 sends Timothy on with the brothers. Across the seam, 16:12 begins with a second peri de heading."
- `W6-008.observed_substrate_signals`: ["travel statement (16:5)", "pentecost (16:8, metadata)", "RP pilcrow inside the unit (16:10)", "WEB paragraph starts at 16:5 and 16:10"]
- `W6-009.boundary_evidence_refs`: ["web:1Cor.16.12-1Cor.16.12 (span: the Apollos topic)", "rp:1Cor.16.11 (back face: Timothy sent on)", "web:1Cor.16.5-1Cor.16.11 (itinerary the rejected fold would join)", "web:1Cor.16.13-1Cor.16.14 (imperatives the rejected join would bind)", "rp:1Cor.16.12 (peri de heading)", "sbl:1Cor.16.12 (SBLGNT accents the name differently)", "rp:1Cor.16.13 (imperatives open the following unit; RP pilcrow)", "web:1Cor.16.12 (WEB paragraph)", "web:1Cor.16.13 (WEB paragraph)"]
- `W6-010.boundary_evidence_refs`: ["web:1Cor.16.13-1Cor.16.14 (span: summary imperatives)", "rp:1Cor.16.12 (back face: Apollos report)", "rp:1Cor.16.13 (asyndetic imperatives; RP pilcrow; rival frame onset)", "rp:1Cor.16.14 (love summary closes the commands)", "rp:1Cor.16.15 (appeal formula opens the following unit; RP pilcrow)", "rp:1Cor.16.19 (adopted frame edge on the greeting formula)", "web:1Cor.16.15-1Cor.16.24 (extent of the rival frame reading)", "sbl:1Cor.16.13 (SBLGNT agrees on the imperatives)", "web:1Cor.16.13 (WEB paragraph)", "web:1Cor.16.15 (WEB paragraph)"]
- `W6-010.boundary_rationale`: "Back face: the Apollos report closes at 16:12. Front face: rp:1Cor.16.13 \"Γρηγορεῖτε, στήκετε ἐν τῇ πίστει,\" opens four asyndetic imperatives, web:1Cor.16.13 “Watch! Stand firm in the faith!” Both witnesses of layout agree here: RP pilcrow at 16:13, WEB paragraph at 16:13. Close: 16:14, rp:1Cor.16.14 \"Πάντα ὑμῶν ἐν ἀγάπῃ γινέσθω.\", sums the commands under love. Across the seam, 16:15 opens an appeal formula, rp:1Cor.16.15 \"Παρακαλῶ δὲ ὑμᾶς,\". RP pilcrow at 16:15 (close seam). Frontier: 16:13 is the rival onset of the closing frame, since a run of imperatives could begin the letter's close; the frame edge adopted is 16:19 on the greeting formula, and keeping 16:13 as a unit onset leaves the tiling intact under either reading. Listed for Fable's end review."
- `W6-011.boundary_evidence_refs`: ["web:1Cor.16.15-1Cor.16.18 (span: appeal and commendation)", "rp:1Cor.16.14 (back face: love summary)", "rp:1Cor.16.15 (parakalo de hymas with vocative; RP pilcrow)", "rp:1Cor.16.18 (recognise such workers, close)", "rp:1Cor.16.19 (greeting formula opens the closing frame; RP pilcrow)", "rp:1Cor.16.13 (rival frame onset)", "rp:1Cor.16.12 (rival body end)", "sbl:1Cor.16.17 (SBL variant site)", "web:1Cor.16.15 (WEB paragraph)", "web:1Cor.16.19 (WEB paragraph)"]
- `W6-011.boundary_rationale`: "Back face: the summary imperatives close at 16:14. Front face: rp:1Cor.16.15 \"Παρακαλῶ δὲ ὑμᾶς,\" is an appeal formula with vocative that introduces the household of Stephanas. RP pilcrow at 16:15 and WEB paragraph at 16:15 stand on the onset. Close: 16:18 ends the commendation with rp:1Cor.16.18 \"ἐπιγινώσκετε οὖν τοὺς τοιούτους.\", a call to recognise such workers. Across the seam, 16:19 opens the third-person greetings, rp:1Cor.16.19 \"Ἀσπάζονται ὑμᾶς αἱ ἐκκλησίαι τῆς Ἀσίας·\". RP pilcrow at 16:19 (close seam). The parent seam at 16:18/16:19 is contested against the rival edge at 16:13, and is listed for Fable's end review."
- `W6-011.observed_substrate_signals`: ["parakalo (16:15)", "parakalo_hymas (16:15)", "parakalo_de_hymas (16:15)", "adelphoi vocative (16:15)", "RP pilcrow (16:15)", "RP pilcrow on the close seam (16:19)", "WEB paragraph starts at 16:15 and 16:19"]
- `W6-012.boundary_evidence_refs`: ["web:1Cor.16.19-1Cor.16.20 (span: third-person and imperative greetings)", "rp:1Cor.16.18 (back face: commendation close)", "rp:1Cor.16.19 (greet_third_person; RP pilcrow)", "sbl:1Cor.16.19 (SBL variant site: singular verb at the second greeting)", "rp:1Cor.16.20 (greet_imperative)", "rp:1Cor.16.21 (autograph opens the following unit; RP pilcrow)", "rp:1Cor.16.13 (rival frame onset)", "web:1Cor.16.19 (WEB paragraph)", "web:1Cor.16.21 (WEB paragraph)"]
- `W6-012.boundary_rationale`: "Back face: the commendation closes at 16:18 with a call to recognise such workers. Front face: rp:1Cor.16.19 \"Ἀσπάζονται ὑμᾶς αἱ ἐκκλησίαι τῆς Ἀσίας·\" opens the third-person greetings from the churches of Asia, web:1Cor.16.19 “The assemblies of Asia greet you.” RP pilcrow at 16:19 and WEB paragraph at 16:19 corroborate the greeting formula, which carries the onset. Interior: 16:20 adds the greeting of the brothers and the command rp:1Cor.16.20 \"Ἀσπάσασθε ἀλλήλους ἐν φιλήματι ἁγίῳ.\". Close: the greetings end at 16:20; at 16:21 the autograph, rp:1Cor.16.21 \"Ὁ ἀσπασμὸς τῇ ἐμῇ χειρὶ Παύλου.\", begins. RP pilcrow at 16:21 (close seam)."
- `W6-012.observed_substrate_signals`: ["greet_third_person (16:19, 16:20)", "greet_imperative (16:20)", "adelphoi, articular nominative (16:20)", "RP pilcrow (16:19)", "close-seam RP pilcrow (16:21)", "WEB paragraph starts at 16:19 and 16:21"]
- `W6-013.boundary_evidence_refs`: ["web:1Cor.16.21-1Cor.16.22 (span: autograph, curse and acclamation)", "rp:1Cor.16.20 (back face: holy kiss)", "rp:1Cor.16.21 (greeting_own_hand; RP pilcrow)", "rp:1Cor.16.22 (curse with maranatha in RP word division)", "sbl:1Cor.16.22 (SBL variant site and SBLGNT word division)", "rp:1Cor.16.23 (grace benediction opens the following unit)", "web:1Cor.16.22 (WEB footnote markers)", "web:1Cor.16.21 (WEB paragraph)"]

Change only the spans the orders name inside those fields; every other byte of the field stays as it is. Any field not
in the table stays byte-identical. If an order cannot be carried out as written (a span is absent, a count differs, an
order would need a field outside the table), do not improvise: leave that field unchanged and report it in the change
log as `blocked` with the measured evidence.

## Suite duties your new text must keep (the suite is the mechanical judge)

- placeholder: no unfilled template placeholder (%s, %(x)s, {name}, {0}, {}) in any field of any row.
- Never hand-type Greek: every Greek run is SLICED by script from `SP\1Cor\1Cor_rp.txt` or `SP\1Cor\1Cor_sbl.txt`,
  byte-identical, never typed and never written as unicode escapes; a row carrying Greek keeps both attribution lines
  (rule 14).
- WEB quotations are SLICED by script from `SP\1Cor\1Cor_web_clean.txt`, in double curly quotes, attributed (the
  A6-b convention).
- register rule: this is a scholar-facing record; no staged file names, internal rule labels, ruling ids, row pointers
  or process talk in row prose.
- single-witness: keep the literal single-witness disclosure wherever a row already carries it.
- A mark is cited at the verse it FOLLOWS; do not re-cite marks.
- A categorical claim ("no", "only", "every") stands only if the thing is absent from BOTH witnesses (C2-amended); add
  none.
- 7-gram: add no run of seven words that repeats across rows; where a disclosure recurs, keep at least 4 distinct
  formulations. Reword, never exclude (CWO-1COR-03).
- Refs: the DEF-A4-ARGUED entries, each ROLE token, face qualifier and seam pair in boundary_evidence_refs stay; your
  only ref change is the deletion-only list above.
- language_zones and cap_sweep are out of scope (no seam moves).

## How you check your work (in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W6\work\`)

1. Copy `SP\1Cor\writer\draft_rows_combined.jsonl` byte-identically to `work\rows_base.jsonl` and to
   `work\rows_applied.jsonl`; in the second, replace your part's changed rows with your revised rows (same order).
2. RUN `run_validator_suite.py` on each copy. MEASURED baseline on the pinned rows: hard_status RED, triage_flags 0,
   dead_members none; members: citation_sweep GREEN, greek_normalize_dryrun None, web_quotes GREEN, refs_mirror GREEN, mark_symmetry GREEN, universals GREEN, ngram7 RED, cap_sweep GREEN, register GREEN, role_tokens GREEN, placeholders GREEN. The only RED is ngram7: the gram 'rp pilcrow at and web paragraph at' in
   W5-002, W5-011, W5-012, W5-013, W5-014, W6-002, W6-003, W6-008, W6-011, W6-012 (the S1-01/S1-01b rows; the W5 and
   W6 deletions cure it). After the simulated ref deletions alone: citation_sweep GREEN, greek_normalize_dryrun None, web_quotes GREEN, refs_mirror GREEN, mark_symmetry GREEN, universals GREEN, ngram7 RED, cap_sweep GREEN, register GREEN, role_tokens GREEN, placeholders GREEN. On your rows no member may gain a hit or
   a flag; report per member before and after.
3. RUN `ngram7.py work\rows_applied.jsonl --gate 10 --full-ids`; report any gram that names one of your rows.
4. RUN `check_tiling.py work\rows_applied.jsonl --range 1Cor.1.1-1Cor.16.24`; it must read GREEN, 437 of 437.
5. Write your part's rows from the applied copy to `work\slice_W6.jsonl` and RUN
   `_validate_writer_part_1cor.py work\slice_W6.jsonl --part W6 --book-index`; it must read GREEN (MEASURED
   GREEN on the pinned rows).
6. Confirm by script that every field outside the table is byte-identical (as a JSON value) to the pinned rows, and
   that each boundary_evidence_refs change is a deletion of listed elements only.

## Deliverables

- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W6\fixup1_W6_rows.jsonl`: one JSON object per line, the FULL revised row for every row you changed (and only those), in the
  pinned rows' order, every untouched field byte-identical as a JSON value.
- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W6\fixup1_W6_changes.json`:

```
{"attempt_id":"cor_fixup1_W6_a1","execution_id":"cor_fixup1_W6_a1#e1","rows_file_sha256":"<pinned rows digest>",
 "changes":[{"row":"<id>","field":"<field>","order":"<ruling or CWO id>","before":"<exact removed span>","after":"<exact new span>",
             "tier":"MEASURED|EXTRACTED|TRANSCRIBED|REPORTED|INFERRED","evidence":"<script + input + slice/count output>"}],
 "blocked":[{"order":"<ruling id>","why":"...","evidence":"..."}],
 "suite":{"base":{"<member>":"<status>"},"applied":{"<member>":"<status>"},"hits_on_my_rows_before_after":{}},
 "untouched_fields_identical":true}
```

## Budget

Keep to roughly 35 tool calls. Report exactly what you ran and what it returned.

## Efficiency contract

M8-EFFICIENCY-V1
EFFICIENCY-CONTRACT: C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md sha256 4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66
Save each complete bounded review unit and exact next cursor in your authorized OUT; partial output is not acceptance. Preserve the unchanged legacy final deliverable contract.
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W6

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"cor_fixup1_W6_a1","execution_id":"cor_fixup1_W6_a1#e1",
 "sources":["<exact paths you read, with sha256>"],
 "outcome":{"changed":[{"what":"<row.field>","why":"<ruling id>"}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search, read no transcript; read only the exact paths named",
 "rows_sha256":"<sha256 of fixup1_W6_rows.jsonl>","changes_sha256":"<sha256 of fixup1_W6_changes.json>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
