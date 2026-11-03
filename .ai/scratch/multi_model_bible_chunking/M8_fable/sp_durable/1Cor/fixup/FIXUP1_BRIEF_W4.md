# FIXUP-1 AUTHOR BRIEF, part W4 (execution #e1): 1 Corinthians, ruled row repairs (M8_fable, OW-36 queue)

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

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W4` already exists. Write your deliverables directly to
`C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W4\fixup1_W4_rows.jsonl` and `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W4\fixup1_W4_changes.json`. **Never run any existence check, listing, glob or recursive search against it or any
other directory.** A shell wildcard is a glob. Private scratch goes in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W4\work\`, created with
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

You are the FIXUP-1 AUTHOR for part W4. Attempt `cor_fixup1_W4_a1`, execution `cor_fixup1_W4_a1#e1`. You authored none of the rows, the
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
- `SP\1Cor\writer_lanes\_validate_writer_part_1cor.py`: RUN on a slice of your private copy holding only your part's rows, with `--part W4 --book-index` (it writes nothing).
- `SP\campaign\grader_models.v1.json`: READ where you check your model role (grader_fallback).
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: READ lines 3412-3434 only (OW-36, the owner's grant).

## The orders to part W4 (quoted from the rulings file, sha256 93e5918b10b17842e5700471087290036549f4ab2327220d518967c49b53dc90)

### S1-02b

Decision (verbatim): Minor-class instances of the same defect are fixed on W3, W4, W5 and W6, and the class is swept by CWO-1COR-01, whose classified support-use hits are appended to the owning part orders before fix-up launches.

Your order (verbatim): Delete the mark-agreement clauses and the web: mark refs.

Exact spans (verbatim): ["W4-001, W4-002, W4-003 boundary_rationale: the sentence pairing a mark word with 'agree'", "boundary_evidence_refs: web:1Cor.11.11, web:1Cor.11.3 (W4-001); web:1Cor.11.17, web:1Cor.11.23 (W4-003); web:1Cor.11.23, web:1Cor.11.27 (W4-004)"]

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

- `W4-001` boundary_evidence_refs[9]: "web:1Cor.11.11 [DISCLOSURE-mark] (WEB paragraph start; decides nothing)"
- `W4-001` boundary_evidence_refs[10]: "web:1Cor.11.3 [DISCLOSURE-mark] (three WEB footnote markers on the word head; decide nothing)"
- `W4-003` boundary_evidence_refs[9]: "web:1Cor.11.17 [DISCLOSURE-mark] (WEB paragraph start agrees; decides nothing)"
- `W4-003` boundary_evidence_refs[10]: "web:1Cor.11.23 [DISCLOSURE-mark] (WEB paragraph start; decides nothing)"
- `W4-004` boundary_evidence_refs[13]: "web:1Cor.11.23 [DISCLOSURE-mark] (WEB paragraph start; decides nothing)"
- `W4-004` boundary_evidence_refs[14]: "web:1Cor.11.27 [DISCLOSURE-mark] (WEB paragraph start; decides nothing)"

B hits:

- `W4-001.boundary_rationale` **support-use** (a pilcrow and a WEB paragraph agreeing (also S1-02b)); disposition: delete the sentence pairing the marks with 'agree'. Sentence: "The RP pilcrow at 11:2 and the WEB paragraph start at 11:2 agree with this onset and do not decide it."
- `W4-002.boundary_rationale` **support-use** (a pilcrow agreeing (also S1-02b)); disposition: delete the clause pairing the pilcrow with 'agrees'. Sentence: "the RP pilcrow at 11:17 agrees and decides nothing."
- `W4-003.boundary_rationale` **support-use** (a pilcrow and a WEB paragraph agreeing (also S1-02b)); disposition: delete the sentence pairing the marks with 'agree'. Sentence: "The RP pilcrow at 11:17 and the WEB paragraph start at 11:17 agree;"

A compliant hit stays as it is. A support-use hit is cured by deleting the support-use clause; the content argument
stays, reworded only as far as the deletion requires. No replacement formula is prescribed.

## What you may change (the lander refuses any other difference)

| row | field | licensed by |
|---|---|---|
| W4-001 | boundary_evidence_refs | CWO-1COR-01, S1-02b (deletion only) |
| W4-001 | boundary_rationale | CWO-1COR-01, S1-02b |
| W4-002 | boundary_rationale | CWO-1COR-01, S1-02b |
| W4-003 | boundary_evidence_refs | CWO-1COR-01, S1-02b (deletion only) |
| W4-003 | boundary_rationale | CWO-1COR-01, S1-02b |
| W4-004 | boundary_evidence_refs | CWO-1COR-01, S1-02b (deletion only) |

`boundary_evidence_refs` is deletion only: the new list must be the old list with some elements removed, order kept,
no element added or edited. The only elements you may remove:

- `W4-001`: "web:1Cor.11.11 [DISCLOSURE-mark] (WEB paragraph start; decides nothing)"; "web:1Cor.11.3 [DISCLOSURE-mark] (three WEB footnote markers on the word head; decide nothing)"
- `W4-003`: "web:1Cor.11.17 [DISCLOSURE-mark] (WEB paragraph start agrees; decides nothing)"; "web:1Cor.11.23 [DISCLOSURE-mark] (WEB paragraph start; decides nothing)"
- `W4-004`: "web:1Cor.11.23 [DISCLOSURE-mark] (WEB paragraph start; decides nothing)"; "web:1Cor.11.27 [DISCLOSURE-mark] (WEB paragraph start; decides nothing)"

MEASURED (the orchestrator's simulation on a scratch copy): deleting every element above for every part leaves each
row at least 4 refs, and the suite's refs members stay GREEN (W4-001 13->11, W4-003 14->12, W4-004 16->14). The
suite is the judge of "below what the suite accepts"; if your applied copy turns refs_mirror or role_tokens RED, stop
and report it (CWO-1COR-01 remedy). Adding a ref is outside your licence.

The current text of each of those fields, as pinned (JSON values):

- `W4-001.boundary_evidence_refs`: ["rp:1Cor.11.2 [WARRANT-onset:near] (praise opening Ἐπαινῶ δὲ ὑμᾶς, with tradition vocabulary; RP pilcrow at 11:2 agrees and decides nothing)", "rp:1Cor.11.1 [WARRANT-onset:far] (imitation command Μιμηταί μου γίνεσθε, closes the argument behind the seam)", "rp:1Cor.11.12 [WARRANT-close:near] (τὰ δὲ πάντα ἐκ τοῦ θεοῦ. ends the reciprocity qualification)", "rp:1Cor.11.13 [WARRANT-close:far] (asyndetic imperative, Ἐν ὑμῖν αὐτοῖς κρίνατε·; text alone, no device)", "rp:1Cor.11.13-1Cor.11.16 [WARRANT-rival:merge] 11.12/11.13 (one row for 11:2-11:16; recorded as the live rival)", "rp:1Cor.11.11 [WARRANT-rival:near] 11.10/11.11 (adversative Πλὴν; rejected, the qualification answers 11:7-11:10)", "rp:1Cor.11.3 [DISCLOSURE-device] (disclosure formula Θέλω δὲ ὑμᾶς εἰδέναι, continues 11:2; no row opens here)", "sbl:1Cor.11.2 [DISCLOSURE-note] (SBLGNT reads Ἐπαινῶ δὲ ⸀ὑμᾶς ὅτι, with a sign at the pronoun and no vocative)", "sbl:1Cor.11.11 [DISCLOSURE-note] (SBLGNT reads the two clauses in the other order inside a sign pair: ⸂γυνὴ χωρὶς ἀνδρὸς οὔτε ἀνὴρ χωρὶς γυναικὸς⸃ ἐν)", "web:1Cor.11.11 [DISCLOSURE-mark] (WEB paragraph start; decides nothing)", "web:1Cor.11.3 [DISCLOSURE-mark] (three WEB footnote markers on the word head; decide nothing)", "rp:1Cor.11.17 [ANCHOR] (negated praise οὐκ ἐπαινῶ, answers the praise of 11:2)", "rp:1Cor.11.7-1Cor.11.10 [ANCHOR] (argument from the creation account that 11:11-11:12 qualifies)"]
- `W4-001.boundary_rationale`: "Onset at 11:2, weighed from both sides. Behind the seam, rp:1Cor.11.1 Μιμηταί μου γίνεσθε, closes the argument over food and conscience with an imitation command (web:1Cor.11.1 “Be imitators of me, even as I also am of Christ.”) and opens no fresh subject. Across the seam, rp:1Cor.11.2 Ἐπαινῶ δὲ ὑμᾶς, opens a statement of praise whose object is the delivered traditions (rp:1Cor.11.2 καθὼς παρέδωκα ὑμῖν τὰς παραδόσεις); the praise verb returns negated at rp:1Cor.11.17 οὐκ ἐπαινῶ,, so the pair brackets the material before the meal discussion (EXTRACTED: device ids epaino and ouk_epaino at 11:2, 11:17 and 11:22). The RP pilcrow at 11:2 and the WEB paragraph start at 11:2 agree with this onset and do not decide it. No row opens at 11:3: rp:1Cor.11.3 Θέλω δὲ ὑμᾶς εἰδέναι, states the thesis that the praise of 11:2 leads into, and its connective ties it back to 11:2 (INFERRED). Close at 11:12, weighed from both sides. Inside, rp:1Cor.11.12 τὰ δὲ πάντα ἐκ τοῦ θεοῦ. ends the reciprocity qualification that rp:1Cor.11.11 Πλὴν introduced, which answers the argument from the creation account in 11:7-11:10 (INFERRED). Beyond, rp:1Cor.11.13 Ἐν ὑμῖν αὐτοῖς κρίνατε· begins asyndetically and turns from argument to an appeal to the hearers' own judgment, followed by the argument from nature and the appeal to custom (INFERRED). This close seam rests on the text alone: there is no RP pilcrow and no WEB paragraph start at 11:13, and no device from the device listing stands there (EXTRACTED), so the evidence for it is one-sided and confidence stays medium-low."
- `W4-002.boundary_rationale`: "Onset at 11:13, weighed from both sides. Behind the seam, rp:1Cor.11.12 τὰ δὲ πάντα ἐκ τοῦ θεοῦ. closes the qualification that began at 11:11 by grounding man and woman in God (INFERRED). Across it, rp:1Cor.11.13 Ἐν ὑμῖν αὐτοῖς κρίνατε· opens asyndetically and asks the hearers to judge (web:1Cor.11.13 “Judge for yourselves.”), and the verses after it argue from what nature teaches (web:1Cor.11.14 “Doesn’t even nature itself teach you”) rather than from the creation account. No device from the device listing and no RP pilcrow stands at 11:13 (EXTRACTED), so the onset rests on the turn in argument alone, which keeps confidence medium-low. Close at 11:16, weighed from both sides. Inside, rp:1Cor.11.16 ἡμεῖς τοιαύτην συνήθειαν οὐκ ἔχομεν, appeals to a shared custom, widened by rp:1Cor.11.16 οὐδὲ αἱ ἐκκλησίαι τοῦ θεοῦ., and sets aside further dispute; it ends the discussion of covering. Beyond, rp:1Cor.11.17 Τοῦτο δὲ παραγγέλλων οὐκ ἐπαινῶ, turns to the assemblies at their meals and negates the praise of 11:2 (EXTRACTED: device ids epaino and ouk_epaino at 11:2 and 11:17); the RP pilcrow at 11:17 agrees and decides nothing. This close seam is also the seam between the head-covering material and the meal material."
- `W4-003.boundary_evidence_refs`: ["rp:1Cor.11.17 [WARRANT-onset:near] (negated praise Τοῦτο δὲ παραγγέλλων οὐκ ἐπαινῶ, answering 11:2; RP pilcrow at 11:17 agrees and decides nothing)", "rp:1Cor.11.16 [WARRANT-onset:far] (appeal to custom οὐδὲ αἱ ἐκκλησίαι τοῦ θεοῦ. closes the covering discussion)", "rp:1Cor.11.22 [WARRANT-close:near] (inclusio with 11:17: Ἐπαινέσω ὑμᾶς ἐν τούτῳ; Οὐκ ἐπαινῶ.)", "rp:1Cor.11.23 [WARRANT-close:far] (tradition formula Ἐγὼ γὰρ παρέλαβον ἀπὸ τοῦ κυρίου; its gar link back to 11:22 is disclosed)", "rp:1Cor.11.23-1Cor.11.34 [WARRANT-rival:merge] 11.22/11.23 (one row for 11:17-11:34; recorded as the live rival)", "rp:1Cor.11.20 [WARRANT-rival:near] 11.19/11.20 (resumptive Συνερχομένων οὖν ὑμῶν ἐπὶ τὸ αὐτό,; rejected, the report of 11:18 is incomplete before 11:20-11:22)", "rp:1Cor.11.18 [DISCLOSURE-device] (report verb ἀκούω σχίσματα with the gathering participle)", "sbl:1Cor.11.22 [DISCLOSURE-note] (SBLGNT reads ἐπαινέσω ὑμᾶς; ἐν τούτῳ οὐκ ἐπαινῶ.)", "sbl:1Cor.11.17 [DISCLOSURE-note] (sign pair ⸂παραγγέλλων οὐκ ἐπαινῶ⸃; the variant content behind it is UNAVAILABLE)", "web:1Cor.11.17 [DISCLOSURE-mark] (WEB paragraph start agrees; decides nothing)", "web:1Cor.11.23 [DISCLOSURE-mark] (WEB paragraph start; decides nothing)", "rp:1Cor.11.33-1Cor.11.34 [DISCLOSURE-device] (the gathering verb returns in the closing commands)", "rp:1Cor.11.2 [ANCHOR] (the praise that 11:17 withholds)", "rp:1Cor.11.19 [ANCHOR] (remark on factions before the resumptive gathering clause)"]
- `W4-003.boundary_rationale`: "Onset at 11:17, weighed from both sides. Behind the seam, rp:1Cor.11.16 οὐδὲ αἱ ἐκκλησίαι τοῦ θεοῦ. ends the covering discussion with an appeal to the custom of the assemblies. Across it, rp:1Cor.11.17 Τοῦτο δὲ παραγγέλλων οὐκ ἐπαινῶ, withholds the praise given at 11:2 and names a fresh subject, the gatherings (web:1Cor.11.17 “together not for the better but for the worse.”). The RP pilcrow at 11:17 and the WEB paragraph start at 11:17 agree; neither decides. Through the span and past it, the gathering verb (the stem of rp:1Cor.11.17 συνέρχεσθε.) stands in 5 verses of chapter 11 in RP, at 11:17, 11:18, 11:20, 11:33 and 11:34 (MEASURED by the lane script gen_w4, skeleton match). Close at 11:22, weighed from both sides. Inside, the report introduced by rp:1Cor.11.18 ἀκούω σχίσματα ends in a run of questions and the negated praise rp:1Cor.11.22 Ἐπαινέσω ὑμᾶς ἐν τούτῳ; Οὐκ ἐπαινῶ., which returns to the wording of 11:17 and closes the report as an inclusio (EXTRACTED: device ids ouk_epaino at 11:17 and 11:22, epaineso at 11:22). Beyond, rp:1Cor.11.23 Ἐγὼ γὰρ παρέλαβον ἀπὸ τοῦ κυρίου opens a received tradition (EXTRACTED: device ids parelabon and paredoka at 11:23). Its causal connective (gar) ties the tradition to the questions of 11:22 as the ground of the withheld praise, so the far side of the close seam is weaker than a fresh start; the gar link is disclosed here, the WEB paragraph start at 11:23 decides nothing, and confidence stays medium."
- `W4-004.boundary_evidence_refs`: ["rp:1Cor.11.23 [WARRANT-onset:near] (tradition formula Ἐγὼ γὰρ παρέλαβον ἀπὸ τοῦ κυρίου with paredoka; gar link back to 11:22 disclosed)", "rp:1Cor.11.22 [WARRANT-onset:far] (negated praise Οὐκ ἐπαινῶ. closes the report)", "rp:1Cor.11.34 [WARRANT-close:near] (deferral Τὰ δὲ λοιπά, ὡς ἂν ἔλθω, διατάξομαι.)", "rp:1Cor.12.1 [WARRANT-close:far] (peri de topic marker Περὶ δὲ τῶν πνευματικῶν, with the disclosure formula)", "rp:1Cor.11.17-1Cor.11.22 [WARRANT-rival:merge] 11.22/11.23 (one row for 11:17-11:34; recorded as the live rival)", "rp:1Cor.11.27 [WARRANT-rival:near] 11.26/11.27 (inferential Ὥστε opens the application; rejected, tradition and application stay together)", "rp:1Cor.11.33 [WARRANT-rival:near] 11.32/11.33 (inferential with vocative Ὥστε, ἀδελφοί μου, closes the application; rejected as an onset)", "rp:1Cor.11.24 [QUOTE] (words of Jesus inside the tradition: καὶ εἶπεν, Λάβετε, φάγετε·)", "sbl:1Cor.11.24 [DISCLOSURE-note] (SBLGNT reads καὶ ⸀εἶπεν· Τοῦτό and τὸ ὑπὲρ ⸀ὑμῶν·, at signs)", "sbl:1Cor.11.23 [DISCLOSURE-note] (SBLGNT reads ᾗ ⸀παρεδίδετο)", "sbl:1Cor.11.26 [DISCLOSURE-note] (SBLGNT reads ὁσάκις γὰρ ⸀ἐὰν ἐσθίητε)", "sbl:1Cor.11.27 [DISCLOSURE-note] (SBLGNT reads ⸀ἀναξίως,)", "sbl:1Cor.11.29 [DISCLOSURE-note] (SBLGNT reads τὸ ⸀σῶμα.)", "web:1Cor.11.23 [DISCLOSURE-mark] (WEB paragraph start; decides nothing)", "web:1Cor.11.27 [DISCLOSURE-mark] (WEB paragraph start; decides nothing)", "rp:1Cor.11.32 [ANCHOR] (judgment as discipline, before the closing command)"]

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

## How you check your work (in `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W4\work\`)

1. Copy `SP\1Cor\writer\draft_rows_combined.jsonl` byte-identically to `work\rows_base.jsonl` and to
   `work\rows_applied.jsonl`; in the second, replace your part's changed rows with your revised rows (same order).
2. RUN `run_validator_suite.py` on each copy. MEASURED baseline on the pinned rows: hard_status RED, triage_flags 0,
   dead_members none; members: citation_sweep GREEN, greek_normalize_dryrun None, web_quotes GREEN, refs_mirror GREEN, mark_symmetry GREEN, universals GREEN, ngram7 RED, cap_sweep GREEN, register GREEN, role_tokens GREEN, placeholders GREEN. The only RED is ngram7: the gram 'rp pilcrow at and web paragraph at' in
   W5-002, W5-011, W5-012, W5-013, W5-014, W6-002, W6-003, W6-008, W6-011, W6-012 (the S1-01/S1-01b rows; the W5 and
   W6 deletions cure it). After the simulated ref deletions alone: citation_sweep GREEN, greek_normalize_dryrun None, web_quotes GREEN, refs_mirror GREEN, mark_symmetry GREEN, universals GREEN, ngram7 RED, cap_sweep GREEN, register GREEN, role_tokens GREEN, placeholders GREEN. On your rows no member may gain a hit or
   a flag; report per member before and after.
3. RUN `ngram7.py work\rows_applied.jsonl --gate 10 --full-ids`; report any gram that names one of your rows.
4. RUN `check_tiling.py work\rows_applied.jsonl --range 1Cor.1.1-1Cor.16.24`; it must read GREEN, 437 of 437.
5. Write your part's rows from the applied copy to `work\slice_W4.jsonl` and RUN
   `_validate_writer_part_1cor.py work\slice_W4.jsonl --part W4 --book-index`; it must read GREEN (MEASURED
   GREEN on the pinned rows).
6. Confirm by script that every field outside the table is byte-identical (as a JSON value) to the pinned rows, and
   that each boundary_evidence_refs change is a deletion of listed elements only.

## Deliverables

- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W4\fixup1_W4_rows.jsonl`: one JSON object per line, the FULL revised row for every row you changed (and only those), in the
  pinned rows' order, every untouched field byte-identical as a JSON value.
- `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W4\fixup1_W4_changes.json`:

```
{"attempt_id":"cor_fixup1_W4_a1","execution_id":"cor_fixup1_W4_a1#e1","rows_file_sha256":"<pinned rows digest>",
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
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_fx1\W4

## YOUR FINAL MESSAGE (OW-8 evidence-and-decision record)

Return JSON only:

```
{"attempt_id":"cor_fixup1_W4_a1","execution_id":"cor_fixup1_W4_a1#e1",
 "sources":["<exact paths you read, with sha256>"],
 "outcome":{"changed":[{"what":"<row.field>","why":"<ruling id>"}]},
 "verification":[{"claim":"...","how":"<tool + argument, or the exact bytes read>","result":"confirmed|refuted"}],
 "unresolved_uncertainty":[{"what":"...","why_it_matters":"..."}],
 "e19_selfreport":"ran no listing, no glob, no recursive search, read no transcript; read only the exact paths named",
 "rows_sha256":"<sha256 of fixup1_W4_rows.jsonl>","changes_sha256":"<sha256 of fixup1_W4_changes.json>",
 "limit":"accountable work summary; not chain of thought and not independent proof"}
```
