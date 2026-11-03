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

**Deliverables, in OUT:** `method_change_adjudications.{{BOOK}}.v1.json`: `{schema: "m8_method_change_adjudication.v1", book:
"{{BOOK}}", proposals_sha256, adjudications: [...]}` with one entry per proposal in id order: `proposal_id`, `verdict`, `rating`,
`reasons`, `proposer_estimate`, `rating_differs_because` (or null), `admissible`, `evidence_checks` (list of `{path, sha256,
looked_for, found, holds, tier}`), `method_record_check`, `adopted_text` (or null), `target_section`, `defer_waits_on` (or
null). Then `cross_proposal_notes` and `rates` (proposed, adopted, rejected, deferred, low_reward). `adjudicator_notes.json`:
every file you opened (path and sha256), the model you ran on and the fallback it is recorded as, and every limit.
