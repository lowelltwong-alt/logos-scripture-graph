# FIXUP-1 AUTHOR BRIEF, part W5 (execution #e1): 1 Corinthians, ruled row repairs (M8_fable, OW-36 queue)

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

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W5` already exists. Write your deliverables directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W5\fixup1_W5_rows.jsonl` and `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W5\fixup1_W5_changes.json`. **Never run any existence check, listing, glob or recursive search against it or any
other directory.** A shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W5\work\`, created with
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

You are the FIXUP-1 AUTHOR for part W5. Attempt `cor_fixup1_W5_a1`, execution `cor_fixup1_W5_a1#e1`. You authored none of the rows, the
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
- `SP\1Cor\writer_lanes\_validate_writer_part_1cor.py`: RUN on a slice of your private copy holding only your part's rows, with `--part W5 --book-index` (it writes nothing).
- `SP\campaign\grader_models.v1.json`: READ where you check your model role (grader_fallback).
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 3412-3434 only (OW-36, the owner's grant).

## The orders to part W5 (quoted from the rulings file, sha256 93e5918b10b17842e5700471087290036549f4ab2327220d518967c49b53dc90)

### S1-01

Decision (verbatim): W5 rows W5-001, W5-002, W5-003, W5-010, W5-011, W5-012, W5-013, W5-014 remove every WEB-paragraph mention used as layout evidence: from boundary_rationale and strongest_rejected_alternative delete the WEB-paragraph clause; from observed_substrate_signals delete every item naming a WEB paragraph; from boundary_evidence_refs delete every web: ref naming a WEB paragraph or tagged DISCLOSURE-mark. An RP pilcrow may remain at most once per row, as one observed_substrate_signals item naming only its location. The ngram7 gram is cured by rewording, never by a tool exclusion.

Your order (verbatim): Apply the deletions to the named rows and fields only; keep at most one bare RP pilcrow location item; reword in row-specific prose.

Exact spans (verbatim): ["W5-002 observed_substrate_signals item 'WEB paragraph at 12:4 and 12:12'", "W5-001, W5-003, W5-010..W5-014 observed_substrate_signals: every item containing 'WEB paragraph'", "W5-001, W5-002, W5-003, W5-010..W5-014 boundary_rationale and strongest_rejected_alternative: every clause containing 'WEB paragraph'", "W5-003 boundary_evidence_refs: web:1Cor.12.14 (predicate A hit)"]

### S1-02

Decision (verbatim): Major. The clauses that offer a WEB paragraph or a pilcrow as agreement, corroboration or joining evidence for a seam are deleted. W6-006 is added: its WEB-paragraph mentions in boundary_rationale, strongest_rejected_alternative, boundary_evidence_refs and observed_substrate_signals are deleted, and its 'RP pilcrow at 15:50.' sentence is kept only as a bare observed_substrate_signals location item. Pilcrow wording of the form 'informs without deciding' is compliant under rule 5 and stays. No replacement formula is prescribed.

Your order (verbatim): Delete the support clause; keep the content argument for the rival.

Exact spans (verbatim): ["W5-010 strongest_rejected_alternative: 'because a vocative and an RP pilcrow join it there' (restate the 14:26 onset on the vocative and wording only)", "W5-005 strongest_rejected_alternative: ', and the WEB paragraph at 13:4 agrees with it'"]

### S1-02b

Decision (verbatim): Minor-class instances of the same defect are fixed on W3, W4, W5 and W6, and the class is swept by CWO-1COR-01, whose classified support-use hits are appended to the owning part orders before fix-up launches.

Your order (verbatim): Delete the WEB-paragraph onset framing.

Exact spans (verbatim): ["W5-001 boundary_rationale: the sentence pairing a mark word with 'confirm'", "W5-001, W5-006, W5-007, W5-008, W5-009 boundary_rationale: the framing 'Onset at X, a WEB paragraph'"]

### S1-04

Decision (verbatim): All 14 W5 rows (W5-001..W5-014) carry both rule-14 strings verbatim: "Robinson-Pierpont Byzantine Textform (Unlicense)" and "SBLGNT (CC BY 4.0)". Each attribution passage is rewritten as plain row prose followed by the two exact strings, unsalted (no row words inserted inside or glued to them). This order depends on TF-2 being installed first.

Your order (verbatim): Replace each attribution passage so that both exact strings appear verbatim and contiguous, each standing alone.

Exact spans (verbatim): ["W5-001..W5-014: every occurrence of 'Robinson-Pierpont (Unlicense) and SBLGNT (CC BY 4.0)'"]

### S1-05

Decision (verbatim): Narrowed to five phrases. The proposal's blanket removal of end-review language is not adopted: 'listed for Fable's end review' disclosures that the strategy directs (W4-001..W4-004, W6-006, W6-010..W6-012) stay.

Your order (verbatim): State the content.

Exact spans (verbatim): ["W5-014 boundary_rationale: 'summarizes the chapter' becomes a statement of what 14:39 summarises"]

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

### CWO-1COR-01 hits on your rows (MEASURED by the installed sweep on the pinned rows; classes by the orchestrator, by the remedy text above)

A hits (each is deleted):

- `W5-003` boundary_evidence_refs[5]: "web:1Cor.12.14 (interior WEB paragraph, rejected cut)"

B hits:

- `W5-001.boundary_rationale` **support-use** (a WEB paragraph offered beside a confirmed fresh start (also S1-02b)); disposition: delete the WEB-paragraph clause; the disclosure-formula content stays. Sentence: "The disclosure formula οὐ θέλω ὑμᾶς ἀγνοεῖν (rp:1Cor.12.1) stands in the same verse at 12:1 and confirms a fresh start, and web:1Cor.12.1 “Now concerning spiritual things” opens a WEB paragraph at 12:1."
- `W5-005.strongest_rejected_alternative` **support-use** (a WEB paragraph agreeing (also S1-02)); disposition: delete ', and the WEB paragraph at 13:4 agrees with it'. Sentence: "The change of grammar at 13:4 is sharp, and the WEB paragraph at 13:4 agrees with it."
- `W5-010.strongest_rejected_alternative` **support-use** (a pilcrow joining (also S1-02)); disposition: delete 'because a vocative and an RP pilcrow join it there'; restate the 14:26 onset on the vocative and wording only. Sentence: "the same question at 14:26 does open a unit because a vocative and an RP pilcrow join it there."

A compliant hit stays as it is. A support-use hit is cured by deleting the support-use clause; the content argument
stays, reworded only as far as the deletion requires. No replacement formula is prescribed.

MEASURED (orchestrator's scan of the pinned rows): every W5 row carries its attribution passage in device_notes, in one of five wordings; the exact quoted string 'Robinson-Pierpont (Unlicense) and SBLGNT (CC BY 4.0)' occurs in W5-004, W5-009 and W5-014 only. S1-04 covers all 14 rows (W5-001..W5-014) and CWO-1COR-02 lists all 14 as failing, so each row's attribution passage, whatever its wording, is the passage you rewrite. 'Standing alone' means: no row word inserted inside either string or glued to it; the two strings may share one sentence separated by punctuation. The ngram7 tool (TF-2) treats each exact string as a segment break, so the prose AROUND the strings must still vary row to row (no shared run of seven words across ten or more rows).

## What you may change (the lander refuses any other difference)

| row | field | licensed by |
|---|---|---|
| W5-001 | boundary_rationale | CWO-1COR-01, S1-01, S1-02b |
| W5-001 | device_notes | CWO-1COR-02, S1-04 |
| W5-001 | observed_substrate_signals | S1-01 |
| W5-002 | boundary_rationale | S1-01 |
| W5-002 | device_notes | CWO-1COR-02, S1-04 |
| W5-002 | observed_substrate_signals | S1-01 |
| W5-003 | boundary_evidence_refs | CWO-1COR-01, S1-01 (deletion only) |
| W5-003 | boundary_rationale | S1-01 |
| W5-003 | device_notes | CWO-1COR-02, S1-04 |
| W5-003 | observed_substrate_signals | S1-01 |
| W5-003 | strongest_rejected_alternative | S1-01 |
| W5-004 | device_notes | CWO-1COR-02, S1-04 |
| W5-005 | device_notes | CWO-1COR-02, S1-04 |
| W5-005 | strongest_rejected_alternative | CWO-1COR-01, S1-02 |
| W5-006 | boundary_rationale | S1-02b |
| W5-006 | device_notes | CWO-1COR-02, S1-04 |
| W5-007 | boundary_rationale | S1-02b |
| W5-007 | device_notes | CWO-1COR-02, S1-04 |
| W5-008 | boundary_rationale | S1-02b |
| W5-008 | device_notes | CWO-1COR-02, S1-04 |
| W5-009 | boundary_rationale | S1-02b |
| W5-009 | device_notes | CWO-1COR-02, S1-04 |
| W5-010 | boundary_rationale | S1-01 |
| W5-010 | device_notes | CWO-1COR-02, S1-04 |
| W5-010 | observed_substrate_signals | S1-01 |
| W5-010 | strongest_rejected_alternative | CWO-1COR-01, S1-02 |
| W5-011 | boundary_rationale | S1-01 |
| W5-011 | device_notes | CWO-1COR-02, S1-04 |
| W5-011 | observed_substrate_signals | S1-01 |
| W5-012 | boundary_rationale | S1-01 |
| W5-012 | device_notes | CWO-1COR-02, S1-04 |
| W5-012 | observed_substrate_signals | S1-01 |
| W5-013 | boundary_rationale | S1-01 |
| W5-013 | device_notes | CWO-1COR-02, S1-04 |
| W5-013 | observed_substrate_signals | S1-01 |
| W5-014 | boundary_rationale | S1-01, S1-05 |
| W5-014 | device_notes | CWO-1COR-02, S1-04 |
| W5-014 | observed_substrate_signals | S1-01 |
| W5-014 | strongest_rejected_alternative | S1-01 |

Not licensed although an order's row list names them (MEASURED: the field holds no 'WEB paragraph'): W5-001.strongest_rejected_alternative (no 'WEB paragraph'); W5-002.strongest_rejected_alternative (no 'WEB paragraph'); W5-010.strongest_rejected_alternative (no 'WEB paragraph'); W5-011.strongest_rejected_alternative (no 'WEB paragraph'); W5-012.strongest_rejected_alternative (no 'WEB paragraph'); W5-013.strongest_rejected_alternative (no 'WEB paragraph'). Leave them unchanged.

`boundary_evidence_refs` is deletion only: the new list must be the old list with some elements removed, order kept,
no element added or edited. The only elements you may remove:

- `W5-003`: "web:1Cor.12.14 (interior WEB paragraph, rejected cut)"

MEASURED (the orchestrator's simulation on a scratch copy): deleting every element above for every part leaves each
row at least 4 refs, and the suite's refs members stay GREEN (W5-003 7->6). The
suite is the judge of "below what the suite accepts"; if your applied copy turns refs_mirror or role_tokens RED, stop
and report it (CWO-1COR-01 remedy). Adding a ref is outside your licence.

The current text of each of those fields, as pinned (JSON values):

- `W5-001.boundary_rationale`: "Onset at 12:1 with Περὶ δὲ τῶν πνευματικῶν (rp:1Cor.12.1), a peri de (transliterated gloss) topic heading that answers a matter raised by the addressees. The disclosure formula οὐ θέλω ὑμᾶς ἀγνοεῖν (rp:1Cor.12.1) stands in the same verse at 12:1 and confirms a fresh start, and web:1Cor.12.1 “Now concerning spiritual things” opens a WEB paragraph at 12:1. On the far side, 11:34 ends with Τὰ δὲ λοιπά, ὡς ἂν ἔλθω, διατάξομαι (rp:1Cor.11.34), deferring the remaining supper matters to a visit. Inside, Διὸ γνωρίζω ὑμῖν (rp:1Cor.12.3) at 12:3 draws a consequence from the reminder of former idol worship. Close after 12:3: at 12:4 Διαιρέσεις δὲ χαρισμάτων (rp:1Cor.12.4) turns to the distribution of gifts, and an RP pilcrow and a WEB paragraph both stand at 12:4."
- `W5-001.device_notes`: "INFERRED from the bytes: the heading introduces a topic response, and the vocative adelphoi (transliterated gloss) inside it does not open a separate unit. The consequence formula at 12:3 (dio gnorizo hymin, transliterated gloss) is internal. Greek wording above is spliced from Robinson-Pierpont (Unlicense); the SBLGNT text (CC BY 4.0) is set beside it where the heading and the consequence clause are quoted."
- `W5-001.observed_substrate_signals`: ["RP pilcrow at 12:4", "WEB paragraph at 12:1 and 12:4", "WEB footnote at 12:2", "SBL critical signs at 12:3"]
- `W5-002.boundary_rationale`: "Onset at 12:4, where an RP pilcrow and a WEB paragraph coincide, with Διαιρέσεις δὲ χαρισμάτων (rp:1Cor.12.4). The verse ends on τὸ δὲ αὐτὸ πνεῦμα (rp:1Cor.12.4), and 12:11 returns to that phrase in fuller form with τὸ ἓν καὶ τὸ αὐτὸ πνεῦμα (rp:1Cor.12.11). That inclusio binds 12:4-12:11 as one exposition of distributed gifts under one Spirit. Close after 12:11: 12:12 opens the body analogy with Καθάπερ γὰρ (rp:1Cor.12.12), and an RP pilcrow and a WEB paragraph both stand at 12:12."
- `W5-002.device_notes`: "Triadic variation at 12:4-12:6 (gifts, services, workings) feeds the inclusio. SBL critical signs stand at 12:6, 12:9 and 12:10; they touch wording inside the list and leave the seams untouched. Sources for the Greek: Robinson-Pierpont under the Unlicense, and SBLGNT under CC BY 4.0, the latter cited for the list of gifts carries edition differences."
- `W5-002.observed_substrate_signals`: ["RP pilcrow at 12:4 and 12:12", "WEB paragraph at 12:4 and 12:12", "inclusio on the same-Spirit phrase at 12:4 and 12:11"]
- `W5-003.boundary_evidence_refs`: ["rp:1Cor.12.12 [WARRANT-onset:near] body analogy, RP pilcrow", "rp:1Cor.12.11 [WARRANT-onset:far] inclusio close of the gifts exposition", "rp:1Cor.12.26 [WARRANT-close:near] mutual-care conclusion", "rp:1Cor.12.27 [WARRANT-close:far] application to the addressees", "web:1Cor.12.12-1Cor.12.26 (unit span)", "web:1Cor.12.14 (interior WEB paragraph, rejected cut)", "sbl:1Cor.12.26 (SBL wording of the conclusion compared)"]
- `W5-003.boundary_rationale`: "Onset at 12:12, which carries an RP pilcrow and a WEB paragraph, with Καθάπερ γὰρ (rp:1Cor.12.12) introducing the body as governing image. The image is worked out through shared baptism at 12:13 and the speeches of foot, ear, eye and head at 12:15-12:21. At 12:21 the eye says Χρείαν σου οὐκ ἔχω (rp:1Cor.12.21). The close comes at 12:26 with Καὶ εἴτε πάσχει ἓν μέλος, συμπάσχει πάντα τὰ μέλη (rp:1Cor.12.26), a two-sided conclusion of shared suffering and shared honour. At 12:27 Ὑμεῖς δέ ἐστε σῶμα χριστοῦ (rp:1Cor.12.27) turns from the analogy to its application."
- `W5-003.device_notes`: "Body vocabulary saturates the unit (soma, mele; transliterated glosses). SBL critical signs at 12:12, 12:13, 12:18, 12:20 and 12:24-12:26 affect wording, not the outer seams. The conclusion at 12:26 differs in wording between editions rest on Robinson-Pierpont, an Unlicense text, compared with SBLGNT, a CC BY 4.0 edition."
- `W5-003.observed_substrate_signals`: ["RP pilcrow at 12:12", "WEB paragraph at 12:12 and 12:14", "two-sided conclusion at 12:26"]
- `W5-003.strongest_rejected_alternative`: "The WEB paragraph at 12:14 invites a cut there, yet Καὶ γὰρ τὸ σῶμα (rp:1Cor.12.14) restates 12:13 with a parallel kai gar (transliterated gloss) and keeps the same image in play. A cut at 12:21 is weaker too, since the head and feet extend speeches already running. At fifteen verses the unit stays within the size range."
- `W5-004.device_notes`: "zeloute (transliterated gloss) at 12:31 recurs at 14:1 and 14:39, framing the inset and its resumption. INFERRED: 12:31b is a hinge whose attachment remains contested, and the opposite attachment is defensible. Attribution: Robinson-Pierpont (Unlicense) and SBLGNT (CC BY 4.0); the comparative at 12:31."
- `W5-005.device_notes`: "At 13:3 SBL reads ⸀καυθήσομαι (sbl:1Cor.13.3) against RP καυθήσωμαι (rp:1Cor.13.3); the variant site is noted and does not drive the seam. SBLGNT (CC BY 4.0) is consulted next to Robinson-Pierpont (Unlicense) to check the verb form at 13:3."
- `W5-005.strongest_rejected_alternative`: "Taking 13:1-13:7 together would join hypotheticals and predicates under the love theme. The change of grammar at 13:4 is sharp, and the WEB paragraph at 13:4 agrees with it."
- `W5-006.boundary_rationale`: "Onset at 13:4, a WEB paragraph, where Ἡ ἀγάπη μακροθυμεῖ (rp:1Cor.13.4) begins a chain of predicates with love as repeated subject. Positive and negated verbs alternate through 13:4-13:6. The chain reaches a fourfold cadence at 13:7, where πάντα στέγει (rp:1Cor.13.7) heads four clauses built on panta (transliterated gloss). At 13:8 Ἡ ἀγάπη οὐδέποτε ἐκπίπτει (rp:1Cor.13.8) restates love as subject and turns to permanence set against gifts that cease."
- `W5-006.device_notes`: "SBL places a critical sign at 13:4 around a repeated subject phrase; the predicates are unchanged. At 13:8 SBL reads οὐδέποτε ⸀πίπτει (sbl:1Cor.13.8) for the RP compound verb. Greek wording above is spliced from Robinson-Pierpont (Unlicense); the SBLGNT text (CC BY 4.0) is set beside it where the verb at 13:8 is set against the RP compound."
- `W5-007.boundary_rationale`: "Onset at 13:8, a WEB paragraph, with Ἡ ἀγάπη οὐδέποτε ἐκπίπτει (rp:1Cor.13.8), setting the permanence of love against prophecies, tongues and knowledge, which pass. The partial-versus-complete contrast runs through 13:9-13:12 and turns on ὅταν δὲ ἔλθῃ τὸ τέλειον (rp:1Cor.13.10) at 13:10. The mirror image at 13:12 follows: Βλέπομεν γὰρ ἄρτι δι’ ἐσόπτρου ἐν αἰνίγματι (rp:1Cor.13.12). The close at 13:13 is the triad Νυνὶ δὲ μένει πίστις, ἐλπίς, ἀγάπη (rp:1Cor.13.13), crowned by love. At 14:1 Διώκετε τὴν ἀγάπην (rp:1Cor.14.1) resumes exhortation on the basis of the inset."
- `W5-007.device_notes`: "At 13:8 SBL reads οὐδέποτε ⸀πίπτει (sbl:1Cor.13.8), a variant site that leaves the onset unchanged. The phrase to teleion (transliterated gloss) is rendered at 13:10 by WEB as web:1Cor.13.10 “that which is complete”. It stands in divided readings: cessationist and continuationist interpretations of chapters 12-14 differ on its referent, and no preference is taken here. The seam does not depend on that question. Sources for the Greek: Robinson-Pierpont under the Unlicense, and SBLGNT under CC BY 4.0, the latter cited for the simplex verb at 13:8."
- `W5-008.boundary_rationale`: "Onset at 14:1, a WEB paragraph, with Διώκετε τὴν ἀγάπην (rp:1Cor.14.1). The same verse continues with ζηλοῦτε δὲ τὰ πνευματικά (rp:1Cor.14.1), taking up the exhortation of 12:31 after the inset. The unit sets prophecy above uninterpreted tongues by the criterion of building up the gathering, and 14:5 closes it with ἵνα ἡ ἐκκλησία οἰκοδομὴν λάβῃ (rp:1Cor.14.5). At 14:6 Νυνὶ δέ, ἀδελφοί (rp:1Cor.14.6) begins a hypothetical visit and a run of analogies, and WEB opens a paragraph there."
- `W5-008.device_notes`: "At 14:6 SBL reads ⸀Νῦν δέ (sbl:1Cor.14.6) for the RP adverb. SBL critical signs at 14:2 and 14:5 concern wording inside the thesis. The wish at 14:5 (thelo de, transliterated gloss) is a preference statement, not a disclosure heading. The adverb at 14:6 rest on Robinson-Pierpont, an Unlicense text, compared with SBLGNT, a CC BY 4.0 edition."
- `W5-009.boundary_rationale`: "Onset at 14:6, a WEB paragraph, with Νυνὶ δέ, ἀδελφοί (rp:1Cor.14.6), a hypothetical visit in tongues that would bring the hearers no profit. Analogies from musical instruments and foreign speech follow at 14:7-14:11. The application at 14:9 reads Οὕτως καὶ ὑμεῖς (rp:1Cor.14.9). The same words return at 14:12 as the unit closes: Οὕτως καὶ ὑμεῖς (rp:1Cor.14.12). The repetition frames the analogies, and 14:12 ends on edifying the gathering. At 14:13 the inferential connective Διόπερ (rp:1Cor.14.13) draws a practical consequence."
- `W5-009.device_notes`: "At 14:13 SBL reads ⸀Διὸ (sbl:1Cor.14.13) in place of the RP compound connective; the variant site is noted. SBL critical signs at 14:7, 14:8 and 14:10 lie inside the analogies. Attribution: Robinson-Pierpont (Unlicense) and SBLGNT (CC BY 4.0); the connective at 14:13 differs."
- `W5-010.boundary_rationale`: "Onset at 14:13, a WEB paragraph, with Διόπερ (rp:1Cor.14.13) and the instruction that a tongue-speaker pray for interpretation. The question Τί οὖν ἐστίν (rp:1Cor.14.15) at 14:15 resolves into praying and singing with mind as well as spirit. Then 14:16 asks how the outsider can say τὸ Ἀμὴν (rp:1Cor.14.16). The personal testimony Εὐχαριστῶ τῷ θεῷ (rp:1Cor.14.18) at 14:18 leads to the close at 14:19, where the speaker prefers θέλω πέντε λόγους (rp:1Cor.14.19) over countless words in a tongue. Close after 14:19: at 14:20 an RP pilcrow and a WEB paragraph coincide with the vocative Ἀδελφοί (rp:1Cor.14.20)."
- `W5-010.device_notes`: "At 14:19 RP has the elided adversative and SBL the full form, so the quotation begins after the adversative. SBL critical signs at 14:16, 14:18 and 14:19 touch wording inside the unit. The amen at 14:16 and the thanksgiving at 14:18 are texture, not seams. SBLGNT (CC BY 4.0) is consulted next to Robinson-Pierpont (Unlicense) to check the testimony at 14:18 and 14:19 is compared across editions."
- `W5-010.observed_substrate_signals`: ["WEB paragraph at 14:13 and 14:15", "RP pilcrow at 14:20", "SBL critical signs at 14:13, 14:16, 14:18 and 14:19"]
- `W5-010.strongest_rejected_alternative`: "A cut at 14:15, where WEB opens a paragraph and the question Ti oun estin (transliterated gloss) is asked, would split the instruction from its resolution. The question answers the problem just posed, so it stays inside the unit; the same question at 14:26 does open a unit because a vocative and an RP pilcrow join it there."
- `W5-011.boundary_rationale`: "Onset at 14:20, where an RP pilcrow and a WEB paragraph coincide, with Ἀδελφοί, μὴ παιδία γίνεσθε (rp:1Cor.14.20), a vocative appeal for mature thinking. A scripture citation follows at 14:21, introduced by Ἐν τῷ νόμῳ γέγραπται (rp:1Cor.14.21). The citation is closed by λέγει κύριος (rp:1Cor.14.21). At 14:22 the inference is drawn with hoste (transliterated gloss), and 14:23-14:25 test it on an outsider entering the assembly, ending in his confession at 14:25. Close after 14:25: 14:26 reopens with Τί οὖν ἐστίν, ἀδελφοί (rp:1Cor.14.26), and an RP pilcrow and a WEB paragraph stand at 14:26."
- `W5-011.device_notes`: "The citation formula at 14:21 (gegraptai, legei kyrios; transliterated glosses) marks quoted scripture inside the unit and is not a seam. At 14:25 SBL orders the confession words differently from RP, so that clause is not quoted here. SBL critical signs at 14:21, 14:23 and 14:25 concern wording. Greek wording above is spliced from Robinson-Pierpont (Unlicense); the SBLGNT text (CC BY 4.0) is set beside it where the citation at 14:21 and the confession at 14:25."
- `W5-011.observed_substrate_signals`: ["RP pilcrow at 14:20 and 14:26", "WEB paragraph at 14:20 and 14:26", "citation formula at 14:21"]
- `W5-012.boundary_rationale`: "Onset at 14:26, where an RP pilcrow and a WEB paragraph coincide, with Τί οὖν ἐστίν, ἀδελφοί (rp:1Cor.14.26), a vocative question that turns from argument to orderly practice. The governing principle stands in the same verse: Πάντα πρὸς οἰκοδομὴν γινέσθω (rp:1Cor.14.26). Orders for tongues and prophecy follow at 14:27-14:32, closing on καὶ πνεύματα προφητῶν προφήταις ὑποτάσσεται (rp:1Cor.14.32). At 14:33 the ground is given: Οὐ γάρ ἐστιν ἀκαταστασίας ὁ θεός, ἀλλὰ εἰρήνης (rp:1Cor.14.33). The verse continues with ὡς ἐν πάσαις ταῖς ἐκκλησίαις τῶν ἁγίων (rp:1Cor.14.33), and that clause is attached backward here to the ground it illustrates. Close after 14:33: at 14:34 a new subject enters without a connective, and an RP pilcrow stands at 14:34."
- `W5-012.device_notes`: "The 14:33b clause is a contested attachment: it may complete the ground in 14:33a or head the instruction at 14:34. The SBL variant sites at 14:34, 14:35 and 14:40 fall in the verses that follow and are disclosed with them. Some witnesses reportedly set 14:34-14:35 after 14:40; this Western transposition is REPORTED metadata, not a seam reason. SBL punctuation brackets 14:32-14:33 as a parenthesis, which is edition punctuation and does not drive the seam. Sources for the Greek: Robinson-Pierpont under the Unlicense, and SBLGNT under CC BY 4.0, the latter cited for the order for worship."
- `W5-012.observed_substrate_signals`: ["RP pilcrow at 14:26 and 14:34", "WEB paragraph at 14:26", "asyndetic new subject at 14:34", "SBL parenthesis around 14:32-14:33 as edition punctuation"]
- `W5-013.boundary_rationale`: "Onset at 14:34, which carries an RP pilcrow, with Αἱ γυναῖκες ὑμῶν ἐν ταῖς ἐκκλησίαις (rp:1Cor.14.34): a new subject enters without a connective after the ground stated in 14:33. At 14:34 SBL reads Αἱ ⸀γυναῖκες ἐν ταῖς ἐκκλησίαις (sbl:1Cor.14.34), omitting the possessive. The instruction continues in 14:35 with Εἰ δέ τι μαθεῖν θέλουσιν (rp:1Cor.14.35). At 14:36 the double question Ἢ ἀφ’ ὑμῶν ὁ λόγος τοῦ θεοῦ ἐξῆλθεν (rp:1Cor.14.36) challenges the addressees and is attached backward here, as a retort that closes the instruction; this attachment is INFERRED. Close after 14:36: 14:37 opens a conditional with Εἴ τις δοκεῖ προφήτης εἶναι (rp:1Cor.14.37), and an RP pilcrow and a WEB paragraph coincide at 14:37."
- `W5-013.device_notes`: "Variant sites at 14:34: SBL reads ⸀ἐπιτρέπεται (sbl:1Cor.14.34) where RP has ἐπιτέτραπται (rp:1Cor.14.34). SBL also reads ⸀ὑποτασσέσθωσαν (sbl:1Cor.14.34) at 14:34 where RP has ὑποτάσσεσθαι (rp:1Cor.14.34). At 14:35 SBL marks ⸀μαθεῖν (sbl:1Cor.14.35) and orders the closing clause as ⸂λαλεῖν ἐν ἐκκλησίᾳ⸃ (sbl:1Cor.14.35), where RP has ἐν ἐκκλησίᾳ λαλεῖν (rp:1Cor.14.35). 14:40 holds a further SBL variant site with πάντα ⸀δὲ (sbl:1Cor.14.40). Some witnesses reportedly set 14:34-14:35 after 14:40; that Western transposition is REPORTED metadata and gives no seam reason. The 14:33b clause may instead head this instruction, and that forward attachment is disclosed with the preceding unit as well. The instruction at 14:34-14:35 stands in divided readings in debates over ordination; no preference between those readings is taken here. The instruction at 14:34-14:35, where the editions differ rest on Robinson-Pierpont, an Unlicense text, compared with SBLGNT, a CC BY 4.0 edition."
- `W5-013.observed_substrate_signals`: ["RP pilcrow at 14:34 and 14:37", "WEB paragraph at 14:37", "asyndetic onset at 14:34", "SBL critical signs at 14:34 and 14:35"]
- `W5-014.boundary_rationale`: "Onset at 14:37, where an RP pilcrow and a WEB paragraph coincide, with Εἴ τις δοκεῖ προφήτης εἶναι (rp:1Cor.14.37). The conditional addresses anyone claiming prophetic or spiritual standing, who must acknowledge ἃ γράφω ὑμῖν (rp:1Cor.14.37) as a command of the Lord. The sanction follows at 14:38 with Εἰ δέ τις ἀγνοεῖ (rp:1Cor.14.38). At 14:39 Ὥστε, ἀδελφοί, ζηλοῦτε τὸ προφητεύειν (rp:1Cor.14.39) summarizes the chapter. Then 14:40 closes with πάντα εὐσχημόνως καὶ κατὰ τάξιν γινέσθω (rp:1Cor.14.40). At 15:1 Γνωρίζω δὲ ὑμῖν, ἀδελφοί (rp:1Cor.15.1) introduces the gospel tradition with a disclosure formula."
- `W5-014.device_notes`: "SBL variant sites stand at 14:37, 14:38, 14:39 and 14:40. At 14:37 SBL ends the clause with κυρίου ⸀ἐστίν (sbl:1Cor.14.37), where RP has κυρίου εἰσὶν ἐντολαί (rp:1Cor.14.37). At 14:38 SBL reads ⸀ἀγνοεῖται (sbl:1Cor.14.38). At 14:39 SBL adds ἀδελφοί ⸀μου (sbl:1Cor.14.39) and orders the closing clause as ⸂μὴ κωλύετε γλώσσαις⸃ (sbl:1Cor.14.39). At 14:40 SBL reads πάντα ⸀δὲ (sbl:1Cor.14.40). The genitive at 14:37, κυρίου (rp:1Cor.14.37), names the command of the Lord as Paul writes it; red-letter speech was considered, and no saying of Jesus is quoted. The reported Western transposition would set 14:34-14:35 after 14:40; it is REPORTED metadata, not a seam reason. Attribution: Robinson-Pierpont (Unlicense) and SBLGNT (CC BY 4.0); the variant readings at 14:37-14:40."
- `W5-014.observed_substrate_signals`: ["RP pilcrow at 14:37 and 14:39", "WEB paragraph at 14:37 and 14:39", "disclosure formula at 15:1 beyond the close"]
- `W5-014.strongest_rejected_alternative`: "A cut at 14:39, where an RP pilcrow and a WEB paragraph stand, is the rival. There hoste with the vocative opens a summary, but cutting would leave 14:37-14:38 as a two-verse unit. The summary is phrased as the closing exhortation of this conditional section, and the hoste-plus-vocative opening is a known over-split temptation that is not followed."

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

## How you check your work (in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W5\work\`)

1. Copy `SP\1Cor\writer\draft_rows_combined.jsonl` byte-identically to `work\rows_base.jsonl` and to
   `work\rows_applied.jsonl`; in the second, replace your part's changed rows with your revised rows (same order).
2. RUN `run_validator_suite.py` on each copy. MEASURED baseline on the pinned rows: hard_status RED, triage_flags 0,
   dead_members none; members: citation_sweep GREEN, greek_normalize_dryrun None, web_quotes GREEN, refs_mirror GREEN, mark_symmetry GREEN, universals GREEN, ngram7 RED, cap_sweep GREEN, register GREEN, role_tokens GREEN, placeholders GREEN. The only RED is ngram7: the gram 'rp pilcrow at and web paragraph at' in
   W5-002, W5-011, W5-012, W5-013, W5-014, W6-002, W6-003, W6-008, W6-011, W6-012 (the S1-01/S1-01b rows; the W5 and
   W6 deletions cure it). After the simulated ref deletions alone: citation_sweep GREEN, greek_normalize_dryrun None, web_quotes GREEN, refs_mirror GREEN, mark_symmetry GREEN, universals GREEN, ngram7 RED, cap_sweep GREEN, register GREEN, role_tokens GREEN, placeholders GREEN. On your rows no member may gain a hit or
   a flag; report per member before and after.
3. RUN `ngram7.py work\rows_applied.jsonl --gate 10 --full-ids`; report any gram that names one of your rows.
4. RUN `check_tiling.py work\rows_applied.jsonl --range 1Cor.1.1-1Cor.16.24`; it must read GREEN, 437 of 437.
5. Write your part's rows from the applied copy to `work\slice_W5.jsonl` and RUN
   `_validate_writer_part_1cor.py work\slice_W5.jsonl --part W5 --book-index`; it must read GREEN (MEASURED
   GREEN on the pinned rows).
6. Confirm by script that every field outside the table is byte-identical (as a JSON value) to the pinned rows, and
   that each boundary_evidence_refs change is a deletion of listed elements only.

## Deliverables

- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W5\fixup1_W5_rows.jsonl`: one JSON object per line, the FULL revised row for every row you changed (and only those), in the
  pinned rows' order, every untouched field byte-identical as a JSON value.
- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W5\fixup1_W5_changes.json`:

```
{"attempt_id":"cor_fixup1_W5_a1","execution_id":"cor_fixup1_W5_a1#e1","rows_file_sha256":"<pinned rows digest>",
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
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W5

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"cor_fixup1_W5_a1","execution_id":"cor_fixup1_W5_a1#e1",
 "sources":["<exact paths you read, with sha256>"],
 "outcome":{"changed":[{"what":"<row.field>","why":"<ruling id>"}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search, read no transcript; read only the exact paths named",
 "rows_sha256":"<sha256 of fixup1_W5_rows.jsonl>","changes_sha256":"<sha256 of fixup1_W5_changes.json>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
