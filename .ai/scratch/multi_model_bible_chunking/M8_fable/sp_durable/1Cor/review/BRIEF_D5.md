# D5: THE METHOD ADJUDICATOR (ITEM 23) (M8_fable, 1 Corinthians close kit, hard-book track)

You are lane D5 of the 1 Corinthians close. The work is candidate-only, NON-AUTHORIZING research. This brief is
binding. Attempt `cor_close_adjudicator_a1`, execution `cor_close_adjudicator_a1#e1`. You run on claude-opus-5-5 (OW-25).

M8-EFFICIENCY-V1
EFFICIENCY-CONTRACT: C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md sha256 4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66
Save each complete bounded review unit and exact next cursor in your authorized OUT; partial output is not acceptance. Preserve the unchanged legacy final deliverable contract.
EFFICIENCY-OUT: C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_close_D5

Your OUT is the only place you write. After each unit of the work below, write what is finished and the cursor (the next
unit) to `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_close_D5\work\progress.json` (LF). If you are continued after an interruption, open that exact path and go on
from its cursor, and say so in your final message.

## E-19: the two binding lines

**AFFIRMATIVE NO-CHECK LINE:** your OUT directory `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_close_D5` already exists, and so does its `work\` subdirectory. Write
your deliverables directly into it at the names given below. **Never run any existence check, listing, glob or recursive
search against it or any other directory.** A shell wildcard is a glob, and so is a directory scan inside a script.

**EXACT-PATH LAW:** every path you may read is named in this brief, or in a pinned manifest this brief tells you to read
paths from. Open each by that exact path. State in your final message that you ran no listing and no glob. **Never open
any session or agent transcript, `.output` file or compaction summary path, including your own, even if your context
names one; if your context is compacted, rebuild from your OUT working files only.**

## GOVERNANCE

- SP is `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable`. It is read-only for you. Write nothing under SP, not even a debug file.
- Never run git, never write a receipt, never touch any registry.
- **FORBIDDEN:** every path not named in this brief, including other models' directories, the Greek apparatus and Swete
  directories, and all final-message files. Nothing from another book passes as 1 Corinthians' evidence (E-65): where
  this brief pins another book's file, it is a template of FORM only.
- **Running Python:** set `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8`, and run `python -B`.
  Write scripts to files in OUT. Do not pass code through a shell here-document or `python -c`. Every file you write is
  UTF-8 with LF line endings (write bytes, or open with newline="\n").
- **Tiers (OW-18):** every claim names its true tier and never a stronger one: MEASURED if a script of yours produced it,
  EXTRACTED if you read it in a pinned file at a place you name, TRANSCRIBED if you copied it, REPORTED if a lane said it,
  otherwise INFERRED. No hand tallies. Every lane of this book ran on one model family, so agreement between lanes is one
  voice (OW-19).
- Record the sha256 of each pinned input as you read it. A mismatch is a hard stop: report it and stop.

## The work

**Your role.** You are the adjudicator. You did not write these proposals and you do not owe them agreement; you also do not
owe them rejection. The orchestrator has given you no view of them and you should infer none from this brief. You do not
edit the method record: the orchestrator carries adopted text into a new version exactly as you return it.

**What to do.** For each proposal, in id order:

1. **Admissibility.** Is it inside the proposer brief's scope, and does it carry evidence from this book? A proposal without
   book evidence is inadmissible (REJECT, with that reason).
2. **Test the evidence.** Open at least two of the artefacts its `evidence_from_this_book` cites (every one, if it cites fewer
   than three), by the exact path, through the manifest of landed outputs, and check that each says what the proposal says
   it says: the field path exists, the count or quotation is right, the cause claimed is the cause recorded. The proposer
   did not read any packet whole; a citation may be wrong. Record each check with path, sha256, what you looked for and
   what you found, with a true tier.
3. **Test the change against the method record.** Read the target section. Is the proposed text already there in substance?
   Does it contradict another section? Would it have prevented, or caught earlier, what the evidence shows, or is it a rule
   fitted to one book's accident? Is the stated blast radius and cost honest?
4. **Rule.** `verdict`: ADOPT, REJECT or DEFER. `rating`: NECESSARY, USEFUL or LOW_REWARD, your own, with reasons; it need not
   match the proposer's estimate, and where it differs say why. ADOPT means the text enters the next method version: return
   `adopted_text` (the exact text, which may be the proposal's `change` verbatim or your narrowed or corrected wording, with
   the difference stated) and `target_section`. DEFER names what evidence or decision it waits on and who can supply it.
   REJECT keeps the proposal in the log with your reasons; a rejected proposal is evidence.

Then look once across all the proposals: do two overlap or conflict, and does any adopted pair need one wording? Say so.
State your limits plainly: you are one reader, on the fallback model, and your verdicts share that reader.

**Deliverables, in OUT:** `method_change_adjudications.1Cor.v1.json`: `{schema: "m8_method_change_adjudication.v1", book:
"1Cor", proposals_sha256, adjudications: [...]}` with one entry per proposal in id order: `proposal_id`, `verdict`, `rating`,
`reasons`, `proposer_estimate`, `rating_differs_because` (or null), `admissible`, `evidence_checks` (list of `{path, sha256,
looked_for, found, holds, tier}`), `method_record_check`, `adopted_text` (or null), `target_section`, `defer_waits_on` (or
null). Then `cross_proposal_notes` and `rates` (proposed, adopted, rejected, deferred, low_reward). `adjudicator_notes.json`:
every file you opened (path and sha256), the model you ran on and the fallback it is recorded as, and every limit.

## PINNED INPUTS

| input | sha256 |
|---|---|
| `SP\1Cor\close\landed\D3_e1\method_change_proposals.1Cor.candidate.jsonl` | `4cbfecdfdae53fa57e4dc8676d3e2ea2937bcde3b2302c51d383bef4e23a6cd0` |
| `SP\1Cor\close\landed\D3_e1\proposer_notes.json` | `81f3c6c7c60a5e22392480761f001d5cdc739e1cc9bdc21a02122e7c57af67a2` |
| `SP\1Cor\close\1cor_landed_outputs_manifest.v1.json` | `e46eefd38aa481b2618b49de6b193acac12be8a8d418cc40223dbf342d560c4c` |
| `SP\..\METHOD_PROPOSER_BRIEF.md` | `d9cad3171014c32d856ad3a94518deff5ea45cbe227119de9921f04d169047e3` |
| `SP\..\BIBLE_CHUNKING_METHOD.v7.md` | `09a3f73fa7c0802ddb2eea6def57a711dced7ff3f6296f6c388e56b46c07f5a9` |
| `SP\..\method_change_proposals.v1.jsonl` | `e729cd979db57a58266d7df15ba73a6306e9e26fd69b0665f2dd82890c112e1d` |
| `SP\1Cor\rows_v1_final.jsonl` | `d175136999a5409789e055592c8341b2bd92230ef132b00697a30c2ec03e76b0` |
| `SP\1Cor\rows_v1_final.manifest.json` | `c4918d2383e1d2ab82432cc323d052f6abe130bc317b17fb7df98602dfa2794b` |
| `SP\1Cor\book_strategy_1Cor.md` | `70e344fed9f0f64654baa97dff80e03b706a1288b47de182628dc453212e39ca` |
| `SP\1Cor\fable_end_review\routed_items.v1.jsonl` | `9a649112983050c74901c11a38f0755604bdd84d69f8412c4f65f47a69243a35` |
| `SP\campaign\grader_models.v3.json` | `45a45ae1582c098f22979d674f2b479cb23e909cab383eaebbc9cbda20472d41` |
| `SP\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md` | `4577a87363a9dc378bf07d0055b85eac70a3139f9cec97f7bfb22cbdb9ab9d66` |
| `SP\..\CAMPAIGN_CLOSE_GATE.v1.md` | `e67bac0408f4935bd5a2696f223b893623b6a85fdb703ea68d552eda2ce84d16` |
| `SP\..\ERROR_PATTERN_LEDGER.v1.md` | `2f90b79e5caaf5dc2e237829eadfbc2bf34560e9f8e248e0a0599218fff4de7f` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E1.v1.json` | `93e5918b10b17842e5700471087290036549f4ab2327220d518967c49b53dc90` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E2.v1.json` | `1299a598b60bbf3c8fb193381ead098e394242a713d8bac4e584b39fdf0e0541` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E3.v1.json` | `a7f32674dee0b0e27f25803729f93142cefdaf2847f9d7122010397e992efe70` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E4.v1.json` | `33ac57245ee930b1484a1227fc019e11c6f082b5c984a20ecc9e7c765d463187` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E5.v1.json` | `c83f49370ed176790530dabdcdfabb85083e94e70acfa87dd4723c16fefa4171` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E6.v1.json` | `b2b3c6dd0ebebe681cabdfd528de9b1f5016f0e200dc0907d9d6d7f83d23d61a` |
| `SP\1Cor\review\1cor_controlling_agent_rulings_E7.v1.json` | `47926b2b0e2a3b31f6ef6f79e840675006484ec3acd08a3a0550ec702b0bc864` |

How you may use each input:

- `SP\1Cor\close\landed\D3_e1\method_change_proposals.1Cor.candidate.jsonl`: read. The proposals under adjudication.
- `SP\1Cor\close\landed\D3_e1\proposer_notes.json`: read. The proposer's notes.
- `SP\1Cor\close\1cor_landed_outputs_manifest.v1.json`: read. The manifest of landed outputs; open artefacts by its paths.
- `SP\..\METHOD_PROPOSER_BRIEF.md`: read. The proposer brief, for scope.
- `SP\..\BIBLE_CHUNKING_METHOD.v7.md`: read the target sections. The current method record.
- `SP\..\method_change_proposals.v1.jsonl`: read. The existing proposals log.
- `SP\1Cor\rows_v1_final.jsonl`: read. The final rows.
- `SP\1Cor\rows_v1_final.manifest.json`: read. The final rows' manifest.
- `SP\1Cor\book_strategy_1Cor.md`: read. The book strategy.
- `SP\1Cor\fable_end_review\routed_items.v1.jsonl`: read. The questions routed to the campaign-end review.
- `SP\campaign\grader_models.v3.json`: read. The review model shapes for this book.
- `SP\campaign\REVIEWER_CONTINUATION_CONTRACT.v1.md`: read. The reviewer continuation contract.
- `SP\..\CAMPAIGN_CLOSE_GATE.v1.md`: read. The close gate.
- `SP\..\ERROR_PATTERN_LEDGER.v1.md`: read by search, not whole. The error ledger.
- `SP\1Cor\review\1cor_controlling_agent_rulings_E1.v1.json`: read. The controlling rulings of one round.
- `SP\1Cor\review\1cor_controlling_agent_rulings_E2.v1.json`: read. The controlling rulings of one round.
- `SP\1Cor\review\1cor_controlling_agent_rulings_E3.v1.json`: read. The controlling rulings of one round.
- `SP\1Cor\review\1cor_controlling_agent_rulings_E4.v1.json`: read. The controlling rulings of one round.
- `SP\1Cor\review\1cor_controlling_agent_rulings_E5.v1.json`: read. The controlling rulings of one round.
- `SP\1Cor\review\1cor_controlling_agent_rulings_E6.v1.json`: read. The controlling rulings of one round.
- `SP\1Cor\review\1cor_controlling_agent_rulings_E7.v1.json`: read. The controlling rulings of one round.

## Budget

About 60 tool calls; stop and report at 100. Keep printed output small: count and summarise, never print a file whole.

## YOUR FINAL MESSAGE

Write the result to `C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\af84b702-d913-4495-8e57-252cf7894c63\scratchpad\cor_close_D5\D5_result.json`, then return the same JSON as your final message: one object with exactly
these keys: `attempt_id`, `execution_id`, `verdict`, `deliverables`, `verification`, `unresolved_uncertainty`. `verdict` is one of `delivered` or `delivered_with_gaps`, unless your task names another set. `deliverables` lists every file with name, sha256 and bytes. `verification` lists each claim with
how it was checked and the result. Add `e19_selfreport` as a note inside `verification`. This is an accountable work
summary, not chain of thought and not independent proof.
