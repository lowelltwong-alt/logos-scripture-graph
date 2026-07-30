# Whole-Bible B01 Evidence-Mesh Replay Runbook

Status: candidate, non-authorizing, revision 7. This runbook captures the reusable process for book-level pre-chunk evidence work. It does not authorize B02 chunk boundaries, reviewed gold, promotion, source-tradition preference, or whole-Bible qualification.

## Purpose

B01 identifies translation, original-language, literary-form, canonical-relation, ancient-context, and premortem pressures before a candidate chunk map is written. It must be replayable without relying on chat memory, must preserve reasoned dissent, and must treat same-model subagents as one correlated model voice.

## Authority and privacy boundaries

- Local canonical Scripture and pinned source archives remain authoritative inputs. DAD stores only privacy-safe process lessons, paths, hashes, failure classes, and validation outcomes.
- Never export Scripture text, source rows, raw prompts, conversations, hidden reasoning, credentials, or private payloads to DAD.
- B01 outputs may contain references, hashes, bounded lexical or grammatical observations, paraphrases, uncertainty, and corpus gaps. They may not contain a complete partition of the book, raw Hebrew/Aramaic/Greek or English verse payloads, or any boundary decision.
- A same-provider or same-model mesh supplies role separation and adversarial checking, not cross-model independence. Record it as one correlated voice.
- An absent or unqualified Second Temple, ancient Jewish, or rabbinic corpus produces a gap receipt and no substantive historical-context claim.

## Required runtime identities

Every execution receives a fresh controller assignment and a distinct runtime instance identity. The controller records start and result events; agents do not self-author their own runtime attestation.

1. `original_language_translation_scout`
   - OT lane: Biblical Hebrew and, where applicable, Aramaic; pinned OSHB and UXLC lineage; morphology/orthography metadata; qere/ketiv and scribal markers; versification and English rendering pressures.
   - NT lane: Koine Greek; pinned SBLGNT, CNTR, and UGNT lineage; morphology, syntax, discourse, textual-lineage, versification, and English rendering pressures.
   - Must distinguish reference-label alignment from token/phrase alignment and must not inflate correlated witnesses into independent witnesses.

2. `literary_form_scout`
   - Identifies overlapping and sparse form observations: narrative, genealogy/list, law, covenant, ritual, poetry/song, wisdom, lament, oracle/prophecy, apocalypse, parable, discourse, epistle argument, quotation/allusion, and mixed forms.
   - Explains why candidate zones are difficult without tiling the book or selecting boundaries.

3. `canonical_relations_and_premortem_scout`
   - One assignment with two disclosed functions: canonical relation forecast and process premortem.
   - Records likely internal cross-references, quotation/allusion candidates, repeated motifs, and downstream interpretive dependencies.
   - Predicts failure modes and tests without prescribing the boss ruling.

4. `second_temple_rabbinic_context_scout`
   - Uses only a pinned, reviewed, qualified corpus and a qualification receipt.
   - Otherwise returns an explicit empty corpus-gap report with requested corpus classes and no contextual observation.

5. `root_synthesizer`
   - Separate from all four scouts. Reads their frozen reports only after all four finish.
   - Reconciles agreements and disagreements, records correlated-model limitations, and produces strategy, sparse form inventory, hard-passage forecast, source-gap register, challenge ledger, synthesis lineage, and appeal ledger.
   - Aggregate artifact blindness must be false because synthesis reads contributor outputs.

6. `exploit_red_team`
   - Separate read-only reviewer. Attempts provenance, timing, manifest, payload, boundary-leakage, source-closure, authority-smuggling, and replay bypasses.
   - Its findings are frozen before boss adjudication.

7. `evidence_dispute_boss`
   - Separate from scouts, synthesizer, and red team. Reviews the exact governed-input manifest, frozen evidence packet, red-team report, unresolved challenges, and appeals.
   - May authorize only preparation of the B01 receipt. It cannot authorize B02, promotion, reviewed gold, replay qualification, or launch.
   - Must record findings, counterevidence considered, rationale, rejected alternatives, conditions, dissent summary, and appeal route.

8. `prepared_commit_checker`
   - Separate read-only checker of the exact prepared receipt candidate and predecessor state.
   - A deterministic actuator may commit only the reviewed exact candidate. It never repairs content or auto-advances.

## B01 role-specific governed inputs

All roles must bind the exact campaign registry, workflow, prompt pack, runtime adapter, canonical passage index, and WEB witness index. No scout may receive another scout report.

- Original-language scout also receives every applicable source manifest, raw archive, derived-view manifest, included-files ledger, exact book view, source policy, and witness-lineage policy.
- Literary-form scout also receives the form registry, literary-marker quality protocol, and owner-faithful chunking policy.
- Canonical/premortem scout also receives the canonical-relation research registry, narrative/legal/covenant dossier queue, and cross-reference policy.
- Ancient-context scout receives the corpus registry and qualification receipt if qualified; otherwise it receives only the corpus-gap policy and inventory proving absence.

The source-gap register must reproduce the exact artifact ID, repository path, and digest closure. A non-empty subset is insufficient.

## Replay sequence

1. Validate the revision-7 static contract and exact blocked qualification labels.
2. Prepare B00 in a fresh run and attempt. Preparation writes no selected receipt, index entry, or receipt log.
3. Obtain a read-only boss verdict for the exact B00 prepared candidate. Commit only after a bounded GO; validate canonical receipt path and both logs.
4. Under the controller lock, create the immutable B01 governed-input manifest before any role assignment.
5. Dispatch the four scouts with fresh assignments. At most three may run concurrently; the fourth may run after a slot frees. All scout writes are isolated to controller-designated proposal files; the controller owns shared manifests and state.
6. Record controller assignment/result receipts and freeze four distinct, non-empty, schema-valid role reports. Reject duplicate report digests.
7. Run the separate root synthesis. Preserve every material disagreement in the challenge ledger; create an appeal row whenever a contributor rejects the proposed resolution.
8. Freeze an evidence packet index binding the governed-input manifest, controller receipts, role executions, reports, synthesis artifacts, challenge ledger, and appeal ledger.
9. Run the exploit red team against the frozen packet. Any P0/P1 finding is NO-GO and requires a fresh attempt when immutable evidence changes.
10. Run the separate boss. Its authorization binds the exact input manifest, evidence packet, red-team report, runtime identity, chronology, and bounded verdict.
11. Finalize the attempt-scoped output manifest, integrity scan, stage draft, and prepared commit. This still writes no selected receipt.
12. Run the prepared-commit checker. Under one state lock, revalidate every byte, campaign/registry digest, selected predecessor, canonical output path, and log state.
13. Commit idempotently. Write or verify the canonical receipt, run index, per-run log, and global log; a retry may repair missing exact log entries but must reject conflicts.
14. Validate the selected B00 to B01 chain. Stop. `B02_authorized` remains false until a separately reviewed B02 migration and authorization exist.

## Hard-passage forecasting rules

A forecast explains difficulty and required evidence; it does not select a boundary. Pay special attention to:

- versification differences and shifted reference labels;
- qere/ketiv, reversed nun, paragraph markers, unusual morphology, ambiguous syntax, discourse shifts, and translation divergence;
- poems or songs embedded in narrative; mixed law/narrative/ritual units; speeches within journeys; lists/genealogies with framing prose;
- quotation, allusion, fulfillment formula, repeated refrain, inclusio, chiasm, acrostic, parallelism, parable framing, oracle formulas, epistle argument turns, and apocalyptic vision cycles;
- Hebrew/Aramaic or Greek source-lineage correlation and places where a second independent witness or lexicon/grammar evidence is missing;
- internal canonical references whose interpretation could be distorted by decontextualized retrieval.

## Disagreement, boss rulings, and appeals

A boss decision does not erase disagreement. Every material challenge records:

- challenge ID, book and reference scope;
- claimant execution and evidence paths/hashes;
- disputed claim and proposed alternatives;
- boss ruling, rationale, conditions, and confidence;
- contributor response: accepted, unresolved, or appealed;
- appeal rationale, requested human or external-AI reviewer, disposition, and superseding evidence if later resolved.

Unresolved, well-reasoned appeals remain visible and produce holds. Human review is required when the dispute concerns canon, theology, source-tradition preference, high-impact translation ambiguity, unqualified ancient context, or repeated boss disagreement.

## Failure, resume, and supersession

- Evidence is immutable per run/stage/attempt. Never overwrite an attempt.
- A failed or abandoned attempt remains as negative evidence with its reason and hashes.
- Any changed governed input, contract file, role report, boss review, or prepared candidate requires a fresh attempt; a changed successful B00 or B01 requires a fresh run.
- Resume is allowed only when it adds missing downstream artifacts to an unselected attempt without changing existing bytes and the contract explicitly permits it.
- A partially completed commit is recoverable only when the existing canonical receipt bytes equal the prepared candidate. Recovery may repair an exact missing index/log row; it must reject any conflicting row.
- Rollback never deletes evidence. A later attempt or run supersedes earlier evidence through explicit lineage.

## Required validation evidence before promotion

- Static v2 contract validator passes, including version authority, exact qualification labels, all-book route honesty, and registry hash closure.
- Exploit tests cover direction-specific manifests, path aliasing, exact role inputs, report schemas, boundary variants, payload normalization, source closure, boss masquerade, chronology, commit races, canonical receipt paths, and log parity.
- One full Numbers B00 to B01 replay passes with four genuine controller-observed subagent executions, synthesis, red team, boss review, preserved appeals, prepare/commit, and chain validation.
- Separate calibration fixtures cover Hebrew prose/law, poetry/song, Aramaic, Koine Greek, synoptic/canonical relations, epistle argument, and both qualified and gap-only ancient-context routes.
- Provider, model, tools, schemas, dependencies, privacy boundary, or authority changes invalidate the affected evidence and require rerun.

Until those gates pass, this runbook and its v2 artifacts are candidate process assets only.
