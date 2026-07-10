# Project Status — Single Source of Truth

**Last updated:** 2026-07-08
**Updated by:** T469 primary witness acquisition planning; active task remains T467
**Active task:** -> **T467 chunking harness hardening** on `codex/t467-harness-hardening`. This is future-rerun scratch harness policy only: no model rerun, chunk output, reviewed gold, child spans, route/evaluator behavior, graph/retrieval/vector truth, canon change, source-tradition choice, DAD reporting success gate, or theology authority.

> **T469 primary witness acquisition waves (2026-07-08):** Adds a planning-only
> Cursor execution plan for cataloging and later acquiring primary/early Bible
> witnesses in rights-reviewed waves. The plan starts with metadata-only source
> rows and separates acquire-now/open text, public-domain or open image sets,
> public-view-only/permission-needed manuscripts, and restricted linguistic
> datasets. Storage estimates: metadata-only <50 MB; text-first 100 MB-1 GB;
> public/open image originals about 11 GB, or about 23 GB with Internet Archive
> derivatives; broader reviewed image candidates about 14 GB originals, or about
> 28 GB with derivatives; later permissioned image expansion may need 100-250 GB.
> T469 authorizes no raw downloads, image storage, transcription storage, source
> text import, canonical Bible text change, canonical passage change, textual-
> critical decision, preferred reading, source-tradition preference, canon change,
> graph/retrieval/vector truth, apologetic conclusion as authority, or theology
> authority.

> **T467 harness hardening (2026-07-07):** T467 patches the T423 multi-model
> scratch chunking harness after T465 found 78 harness-fix rows. The new
> `T467_literary_coherence_v1` overlay requires future reruns/new model slots to
> preserve larger coherent list/register/legal/allotment/census/worship/admin/battle/
> covenant units unless a function change is logged, check epistle units such as
> greetings, thanksgiving/prayer, body argument, exhortation, travel notes, final
> greetings, doxology, and benediction, and keep Strong's/lemma/morphology/WJ/headings/
> footnotes/cross-references evidence-only. It updates the marathon prompt, T423
> quality protocol, model template, validator coverage, CD-106, and LSN-051. DAD
> reporting is explicitly deferred due to interface drift and is not a success gate.
> T467 authorizes no model rerun, reviewed gold, chunk output, child spans,
> route/evaluator behavior, graph/retrieval/vector truth, preferred reading,
> source-tradition preference, canon change, or theology authority.

> **T465 reconciliation gate (2026-07-07):** T465 turns T464's comparison outputs into
> governed next-action artifacts without promoting any chunk output. It adds
> `.ai/control/t465_multi_model_reconciliation_gate.yaml`, a harness triage for the
> 78 `harness_fix_or_rerun_required` rows, a Mark 16 frontier/specialist packet, a
> 19-row owner candidate docket from `M4_codex_gpt55` plus `M6_fable5` alignments,
> and a Claude/frontier Mark 16 review prompt. The Mark 16 packet names Vaticanus
> blank-space/layout, Sinaiticus ending, letters-per-line/column capacity, other
> witnesses, patristic evidence, and downstream chunking implications as research
> questions only. T465 authorizes no reviewed gold, chunk output, child spans,
> route/evaluator behavior, graph/retrieval/vector truth, preferred reading,
> source-tradition preference, canon change, Mark 16 inspiration decision, or
> theology authority.

> **T464 multi-model chunking comparison docket (2026-07-07):** Six whole-Bible scratch
> model lanes (`M1_cursor`, `M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`,
> `M5_gemini_thinking`, `M6_fable5`) are frozen as non-authorizing evidence and compared.
> Generated comparison artifacts live under
> `.ai/scratch/multi_model_bible_chunking/comparison/`: `agreement_chunks.jsonl`,
> `disagreement_delta.jsonl`, `owner_decision_docket.yaml`, `frontier_review_queue.jsonl`,
> `harness_improvement_queue.md`, `model_agreement_matrix.yaml`, and `delta_summary.md`.
> The fork signal is **FULL_FAIL** for direct promotion: verse-coverage agreement is 6.17%
> against a 50.00% full-run threshold, with 144 agreement candidates and 1048 deltas.
> Use the docket for reconciliation, frontier review, and harness improvement only. Agreement,
> including `M4_codex_gpt55` plus `M6_fable5` alignment, is evidence and not authority.
> Textual-variant/source-tradition hot zones route to frontier review even under model
> agreement. Mark 16 explicitly requires major codex witness review, Codex Vaticanus
> layout/blank-space review, Codex Sinaiticus ending review, scribal letters-per-column and
> column-space analysis, manuscript transmission history, and longer-ending specialist review.
> T464 authorizes no reviewed gold, chunk output, child spans, route/evaluator behavior,
> graph/retrieval/vector truth, source-tradition preference, canon change, or theology authority.

> **T463 integration hardening (2026-07-06):** Integrates the T431-T442
> original-language evidence stack on current `main`, adds
> `.ai/control/ai_pr_lifecycle_policy.yaml` so AI-created draft work must reach PR,
> merge, hold, superseded, abandoned-with-rationale, or owner/integrator escalation
> state, and adopts the Rust fast-path pattern for the legacy whole-Bible chunk-map
> validator while preserving `--python-only` parity/debugging. T463 also strengthens
> `.ai/control/coding_runtime_language_preflight.yaml` with the explicit Python-test
> migration strategy: keep Python command names stable, use Rust for deterministic hot
> paths when thresholds justify it, and require modular Rust `CheckReport` boundaries.
> DAD candidate lesson:
> `msg-20260706-t463-ai-draft-pr-and-rust-validator-strategy`. T463 authorizes no
> chunk output, reviewed gold, child spans, route/evaluator behavior,
> graph/retrieval/vector truth, source-tradition choice, canon change, DAD override,
> or theology authority.

> **T462 modular Rust validator bundle (2026-07-06):** `tools/logos_fast_validators`
> now uses the preferred Rust shape for combined deterministic checks: short
> `main.rs` dispatcher, named modules with `run_check(input) -> CheckReport`, and
> a `bundle` command that emits one aggregate JSON summary while preserving
> per-check names, timings, and failure messages. Python wrappers remain stable
> governance ergonomics. DAD candidate lesson:
> `msg-20260706-t462-modular-rust-validator-bundle`.

> **T466 likely next route:** do not rerun the whole comparison unless artifacts change. Use
> T465's owner docket for one exact owner-selected review-packet strengthening lane, or send
> `mark16_specialist_packet.md` to Claude/frontier before any Mark 16 owner decision.

> **T423 six-model whole-Bible marathon integration (2026-07-06):** M1_cursor,
> M2_claude_sonnet5, M3_claude_frontier, M4_codex_gpt55, M5_gemini_thinking, and
> M6_fable5 each completed all 66 canonical books in isolated scratch folders.
> The integration branch records the completed maps, per-book strategies, low-confidence
> registers, frontier escalation queues, atlas candidate feeds, quality summaries, and
> model summaries. The pilot gate is now `go` for completed scratch marathons, while
> comparison remains not run. Next route is batch comparison/delta analysis from main.
> These artifacts remain scratch/non-authorizing: no canon output, reviewed gold,
> child spans, route/evaluator behavior, graph/retrieval/vector truth, embeddings/indexes,
> or theology authority are created.

> **T461 Scripture front-door decomposition (2026-07-06):** Implements Fable PR-7 by
> keeping `AI_FRONT_DOOR.md` as a compact stable operating-rules surface, moving volatile
> T3xx/T4xx task-history narrative into `docs/roadmap/TASK_LEDGER.md`, adding tagged TOC
> routing, recording `CD-091` plus `LSN-047`, and validating the split with `scripts/validate_task_ledger.py`.
> This is a findability/auditability hardening PR only. It authorizes no Scripture data
> mutation, chunk output, reviewed gold, child spans, route/evaluator behavior,
> graph/retrieval/vector truth, embeddings/indexes, boundary import, source rows, preferred
> readings, source-tradition preference, canon-scope change, or theology authority.

> **T425 DAD lesson-slot integrity and runtime preflight enforcement (2026-07-05):** Hardens
> the T424 Rust/DAD asset lane by requiring DAD outbox rows with `lesson_learned_slot` or
> `context_map_entry` to point at tracked local slots that agree on task id, message id,
> trust zone, local adoption, extra context, and non-authorizations. It also makes
> `runtime_language_preflight` a forward task-scope requirement for post-T424 task contracts
> that touch validators, scanners, pipelines, workflows, generated-data, Rust, or CI hot-path
> surfaces. This closes the "policy but not gate" gap while keeping Python/pytest as the
> governance orchestrator and Rust as deterministic leaf tooling. T425 authorizes no chunk
> output, reviewed gold, child spans, route/evaluator behavior, graph/retrieval/vector truth,
> embeddings/indexes, source rows, canon changes, source-tradition preference, target selection,
> or theology authority.

> **T424 Rust-accelerated validation layer (2026-07-03):** Adds an isolated
> `tools/logos_fast_validators/` Rust CLI plus Python wrappers for deterministic
> JSONL and canonical-scope scans. `validate_all.py` uses these fast wrappers only
> for generated canonical data gates with Python fallback. Python/pytest remain
> authoritative for governance, task scopes, handoffs, theology-policy language,
> route/evaluator policy, and corpus QA. The new
> `.ai/control/coding_runtime_language_preflight.yaml` makes Rust-first consideration
> mandatory before adding high-resource deterministic code, with explicit thresholds
> and interop/maintenance tradeoff recording. T424 also sends DAD candidate-only lesson/assets
> via `.digital-asset/mail/outbox.jsonl` as `msg-20260703-t424-rust-validation-layer`,
> checked by `scripts/validate_dad_outbox.py`; local adoption remains required. No chunk output,
> reviewed gold, child spans,
> graph/retrieval/vector truth, embeddings/indexes, source rows, canon changes, target
> selection, or theology authority are authorized.

> **T442 production candidate-root decision packet (2026-07-05):** Presents owner options for
> whether a later task may open narrow original-language production candidate roots after
> T439/T440/T441 proof. Recommended option T442-A would authorize only a future implementation
> packet, not immediate root creation or row population. T442 adds no Rust; it records the next
> sensible Rust slice as a future production-root admission checker if T442-A is selected. T442
> authorizes no production roots, source-token rows, alignment rows, Strong's/lemma/morphology
> population, preferred readings, source-tradition choice, manuscript witness support,
> translation-faithfulness judgment, chunks, reviewed gold, KG/retrieval/vector truth, or
> theology authority.

> **T441 Rust no-text alignment coverage index (2026-07-05):** Adds a narrow Rust binary
> inside the original-language observation scanner crate to emit generated no-text coverage
> ledgers for T439 Philemon and T436/T440 Jonah fixtures. The generated ledgers live under
> `build/original_language_observation/T441/alignment_coverage/` and are not committed.
> Python remains the authority validator; `validate_all.py` runs only the fast contract check,
> not the generated Rust scan. T441 records source/ref coverage, alignment-coverage shape rows,
> semantic guardrails, and T440 negative-fixture carry-forward only. It opens no production
> evidence roots and authorizes no source-language truth, word-level alignment truth,
> Strong's/lemma/morphology population, preferred readings, source-tradition preference,
> manuscript witness support, translation-faithfulness judgment, chunks, reviewed gold,
> KG/retrieval/vector truth, or theology authority.

> **T438 alignment bridge goal gate (2026-07-05):** Records Option 1, the
> Greek/Hebrew-to-English alignment bridge, as the next original-language implementation
> lane while keeping Option 2 manuscript custody-chain work catalog-only in parallel.
> T438 defines the T439/T440/T441/T442 sequence: Greek Philemon bridge expansion
> contract, Hebrew Jonah source-specific parser contract, Rust no-text alignment
> coverage index, and an owner-gated production candidate-root opening packet. Rust is
> reserved for deterministic scanner/checker slices after parser semantics and negative
> parity fixtures are proved. T438 authorizes no production source-token rows, alignment
> rows, Strong's overlays, lemma/morphology rows, preferred readings, source-tradition
> choices, witness-support rows, translation judgments, KG/retrieval truth, chunks,
> reviewed gold, or theology authority.

> **T439 Philemon alignment bridge expansion (2026-07-05):** Expands T433's
> `Phlm.1.1-Phlm.1.3` SBLGNT-to-WEB bridge to all 25 verses of Philemon as
> no-text task-scoped candidate rows under
> `data/candidate/original_language_evidence/pilots/T439_phlm_alignment_bridge_expansion/`.
> T439 emits 334 source-token observation rows, 98 redacted editorial-layer rows,
> 25 low-confidence verse-level alignment rows, and a manifest for future Rust parity.
> It stores token hashes and IDs, not visible Greek source text or visible English text.
> It opens no production evidence roots and authorizes no source-language truth,
> alignment truth, Strong's/lemma/morphology population, translation judgment,
> preferred reading, source-tradition choice, witness support, KG/retrieval truth,
> chunks, reviewed gold, or theology authority.

> **T440 Jonah Hebrew parser contract (2026-07-05):** Defines source-specific
> UXLC and OSHB Jonah parser semantics before any Hebrew Rust expansion. It records
> full-Jonah lineage, expected counts, XML shape, OSHB `w@lemma` as Strong lookup-hint
> metadata, OSHB `w@morph` as source morphology metadata, and negative fixture
> requirements for T441. T440 adds no Rust code, no new Hebrew token rows, no
> production original-language evidence roots, no source-language truth, no
> Strong's/lemma/morphology population, no preferred readings, no source-tradition
> choice, no translation judgment, no KG/retrieval truth, no chunks, no reviewed
> gold, and no theology authority.

> **T437 OSHB lemma-attribute policy cover (2026-07-05):** Policy-covers OSHB
> `w@lemma` as Strong lookup-hint metadata without treating it as local lemma rows,
> Strong's rows, lexical truth, preferred readings, translation judgment, or theology
> authority. Updates the T431 allowlist, OSHB source manifest, canonical source-view
> manifest, all 39 included OSHB rows, T436 parity output, and validators. Hebrew Rust
> expansion remains unauthorized until a later source-specific UXLC/OSHB parser contract
> and no-text parity proof exists.

> **T436 Jonah Hebrew observation parity pilot (2026-07-04):** Adds a no-text
> Hebrew Jonah pilot under
> `data/candidate/original_language_evidence/pilots/T436_jonah_hebrew_observation_parity/`.
> T436 consumes only T431 canonical source views for Tanach.us UXLC and Open Scriptures OSHB,
> emits source-view file observations, 96 verse rows, 1,376 token-shape rows,
> editorial/metadata-shape rows, and a parity summary without Hebrew wording, morphology
> values, lemma values, Strong's values, raw archive reads, or production candidate-root writes.
> It records UXLC/OSHB verse and token-count parity for Jonah and explicitly records OSHB
> `w@lemma` metadata as policy-covered Strong lookup-hint metadata, not local lemma
> or Strong's authority. T436 blocks Hebrew Rust expansion until source-specific parser
> contracts exist. It authorizes no source-language truth, lexical truth,
> Strong's/lemma/morphology population, preferred reading, source-tradition choice, manuscript
> witness support, translation judgment, chunk boundary, reviewed gold, chunk output,
> KG/retrieval truth, embeddings/indexes, or theology authority.

> **T435 original-language Rust observation scanner (2026-07-04):** Added a narrow Rust
> SBLGNT canonical-source-view scanner at `tools/original_language_observation_scanner/`.
> It emits no-text generated ledgers under `build/original_language_observation/T435-A/sblgnt/`
> for source-view files, verses, token shapes, and editorial shapes, then checks T433
> Phlm.1.1-3 parity (41 source-token shapes and 7 editorial shapes). Python remains the
> authority validator through `scripts/validate_t435_original_language_observation_scanner.py`;
> `validate_all.py` runs only the fast contract check, not the full Rust scan. T435 records
> `CD-094` and authorizes no source-language truth, lexical truth, Strong's/lemma/morphology
> population, preferred reading, source-tradition choice, manuscript witness support, translation
> judgment, chunk boundary, reviewed gold, KG/retrieval truth, embeddings/indexes, or theology
> authority. Hebrew scanning remains deferred until a separate Jonah pilot proves Hebrew
> source-view and metadata assumptions.

> **T431 original-language raw intake (2026-07-04):** Added the T430/T431 original-language
> evidence lane and allowlisted raw intake guardrails. Downloaded manifest-backed raw archives for
> Tanach.us UXLC, Open Scriptures Hebrew Bible, SBLGNT, unfoldingWord UGNT, and CNTR Statistical
> Restoration under `data/raw/original_language/`. Manuscript libraries remain catalog-only:
> Leon Levy DSS, Codex Sinaiticus, Aleppo Codex, and NT papyri/major codices. Strong's, lemma,
> morphology, variant, witness-support, and translation-faithfulness layers remain future
> candidate evidence outside raw. T431 also builds canonical-only candidate source views with
> inclusion/exclusion ledgers so docs, app renderings, metadata, nested archives, duplicate text
> formats, images, and non-selected variants do not contaminate future Bible processing. Future
> T432+ work must consume the filtered source view, not the raw archive directly. T431 authorizes no source text mutation, Strong's overlay in raw,
> manuscript transcription/image import, preferred reading, source-tradition preference, canon
> change, reviewed gold, chunks, KG edges, retrieval truth, embeddings/indexes, or theology
> authority.
> T431 guardrail hardening records source-provided metadata truthfully in canonical source views:
> OSHB/UGNT/CNTR-style morphology, lemma, or Strong's columns remain evidence-only and are flagged
> in manifests/ledgers. The canonical source-view checker now validates included/excluded ledgers
> against actual archive members and rejects duplicate paths, duplicate included books, duplicate
> view paths, stale checksums, and scope/count drift. `docs/roadmap/T430_ORIGINAL_LANGUAGE_GOAL_OPTIONS.md`
> adds five possible next goals: alignment bridge, manuscript witness chain, variant/copying-error
> ledger, early creed/tradition-formula research lane, and integrated evidence workbench.

> **T423 whole-Bible multi-model fork (2026-07-03):** Experimental speed path — 3–10 models
> chunk entire Bible in separate scratch folders (continuous marathon, days OK), same research
> baseline, then compare agreement vs delta. Revert to T410 if fork fails. **Red-team required
> before marathons:** `.ai/prompts/multi_model_whole_bible_chunking_redteam_premortem_prompt.md`

> decision logs. Codex, Claude, Gemini, and hostile red-team each complete independent layers.
> Comparison matrix + audit bundle for Codex at end. No canon writes until bundle review.

> **T421 standing escalation policy (2026-07-03):** Owner recorded `APPROVE_STANDING_ESCALATION_POLICY`.
> Standing dispositions and batch2+3 ladder scope are active. Each strengthening, reviewed-gold, harness,
> and output step still requires an explicit owner gate plus Codex review. Audit:
> `.ai/audits/reports/20260703-T421-standing-escalation-policy-activation.md`.

> **T417 scratch marathon + phase ladder (2026-07-02):** Exhausted all 38 `ready_for_review_packet`
> candidates with non-authorizing prep only: drafts, strengthening prep, owner-gate prep, gold/harness/output
> prep under `.ai/context/agent_work/T417/`. Promotion packets SUB-001 through SUB-011 filed.
> Codex approved prep promotion for SUB-001..006 and SUB-009..011; SUB-007/008 remediated after integrator HOLD.
> Standing policy readiness `APPROVE_PREP` after per-step gate wording fix. No reviewed gold, chunk output,
> child spans, harness execution, or standing activation occurred in scratch lane.

> **T420 multi-agent review cadence (2026-07-02):** Recorded the canonical operating model:
> Cursor prep until backlog empty; Codex daily integrator (`APPROVE_PREP` / `HOLD_WITH_FINDINGS`);
> Claude Opus 4.8 weekly architecture and chunking-error audit (`APPROVE_WEEKLY` /
> `HOLD_WITH_FINDINGS` / `ESCALATE_OWNER`); owner retains docket/gold/output gates only.
> Recorded `CD-084` plus `LSN-039`. Review ledger: `.ai/control/agent_review_ledger.jsonl`.

> **T416 batch1 post-pilot review (2026-07-01):** Accepted T415 same-baseline safety:
> baseline 1138 chunks, candidate 1143 chunks, exactly five additive parent-only overlays,
> no non-target byte diff, no changed existing IDs, and no removed IDs. Recorded `CD-083`
> plus `LSN-038`. Child spans are not necessary now for the five pilot parents. The next
> route is owner selection for batch2 review-packet strengthening only, recommended docket
> `T402-LC-057`, `T402-LC-065`, and `T402-LC-032`; no batch2 output, reviewed-gold
> promotion, whole-Bible output, hold clearing, Cursor continuation, evaluator change,
> leaderboard claim, or broader epistle-opening generalization is authorized.

> **T415 batch1 output pilot (2026-07-01):** Added five exact additive parent-only epistle opening overlays
> (3John, 2Cor, 1Tim, Jas, 2John). Baseline 1138 → candidate 1143 chunks. Recorded `CD-082` plus `LSN-037`.
>
> **T414 batch1 parent-only reviewed-gold promotion (2026-07-01):** Promoted five opening spans as
> parent-only reviewed gold without output change. Recorded `CD-081` plus `LSN-036`.
>
> **T413 batch1 review-packet strengthening (2026-07-01):** Strengthened five owner-authorized opening
> review packets from the T413 docket. Recorded `CD-080` plus `LSN-035`.

T411 produced non-authorizing review-packet prep for all 66 T402 low-complexity queue candidates:
206 traceable non-authorizing claims, 66 escalation packets, 20 completed waves/chunks, and the
CHUNK 1 pilot Cursor observation pack. The T413->T416 batch1 ladder is complete for five short
epistle openings. The current next route is **T417 autonomous batch2 prep** on
`codex/t417-autonomous-batch2-prep` under the T420 cadence (daily Codex, weekly Claude);
owner selection for batch2 review-packet strengthening remains the next authority gate;
reviewed-gold promotion, output-changing chunk work, child spans, and
hold clearing remain unauthorized unless a later owner-gated task explicitly authorizes them.

T412 merged @ `e90bc3d`; Claude post-merge audit recorded **APPROVE_T411_CURSOR** with no P0/P1
(`.ai/audits/reports/20260630-T412-post-merge-claude-audit.md`). The Rust-first observation
substrate is proved: 83 source files, 66 canonical books, 38,058 verses, and 1,402 chapter spans;
generated-mode validation and the T411 compressed ledger pack check pass. Routine `validate_all.py`
contract checks do not rerun the full Rust scan unless scanner/raw/schema inputs change.
T411 `cursor_execution_allowed: false` remains correct after queue exhaustion; any further Cursor
work requires a new owner-gated task or wave.
T412 adds
`.ai/control/rust_first_observation_substrate.yaml`, `tools/usfm_observation_scanner/`,
`scripts/validate_rust_observation_substrate.py`, `scripts/build_cursor_observation_pack.py`, and
`docs/roadmap/T412_RUST_FIRST_OBSERVATION_SUBSTRATE.md`. T412 authorizes no Cursor whole-Bible raw
reread, target selection, reviewed gold, child spans, chunk output, route/evaluator behavior,
graph/retrieval/vector truth, embeddings/indexes, boundary import, backend choice, profile
promotion, source/manuscript rows, canon-scope change, preferred readings/source traditions, or
theology authority.

The completed **T410 Research-To-Chunking Phase One Roadmap** remains the governing
research-to-chunking conveyor. The
original T410 commit (`c006f36`) is already merged to `main`; the follow-up hardening records and
live-validates one-task/one-branch/one-worktree safety, clean-status and merge-state preflights,
cross-task artifact stop conditions, serialized shared control-file edits, and explicit validation
tiers before any T411 Cursor batch starts. T410 turns the T402/T404/T406 research runway into a
governed conveyor belt from Cursor research, review-packet prep, Codex review, frontier escalation,
owner gates, reviewed gold, route isolation, exact additive parent overlay output PRs, and
post-pilot review. T410 adds
`.ai/control/parallel_chunking_research_program.yaml`,
`.ai/control/bible_book_literature_prompt_hints.yaml`,
`.ai/control/cursor_to_codex_transparency_contract.yaml`,
`.ai/control/frontier_chunking_escalation_policy.yaml`,
`.ai/control/chunking_phase_completion_plan.yaml`, Cursor prompt-pack commands/rules, and
`scripts/validate_parallel_chunking_prompt_pack.py` plus
`scripts/validate_parallel_execution_safety.py`. T412 adds the Rust-first no-text observation
substrate required before T411 Cursor execution. T411 adds
`docs/roadmap/T411_CURSOR_READINESS_WITH_CLAUDE_GATE.md`,
`.ai/tasks/T411.task.yaml`, `.ai/handoffs/T411/handoff.md`, the T411 candidate docket and
per-candidate prompt notes, and the emitted-artifact validator. T410 defines Phase 1 as one governed
parent-only additive low-risk overlay per canonical book where safe, with explicit deferrals for
unsafe books. It authorizes no Cursor target selection, reviewed gold, child spans, chunk output,
route/evaluator behavior, graph/retrieval/vector truth, embeddings/indexes, boundary import,
backend choice, profile promotion, source/manuscript rows, canon-scope change, or theology
authority. T411 also authorizes none of those surfaces.
The prior T404/T406 low-risk handoff remains the review-only Cursor runway; T410 is the bridge
from that runway to later owner-gated implementation tasks, not an implementation task itself.
PR #123 conflict reconciliation also preserves the already-merged T405 governance dependency-map
mirror at `.ai/control/governance_dependency_map_mirror.yaml`, renumbered in the lesson index as
`LSN-033` after T402/T404. T405 remains a non-authorizing child-repo mirror of upstream
`logos-governance-architecture/governance/GOVERNANCE_DEPENDENCY_MAP.yaml`; it cannot override
upstream governance, weaken governance, change Scripture data, import boundary material, or create
graph/retrieval/vector truth.
**T308** connection discovery + **T309** chunking bake-off still open.

> **T404 Cursor low-risk chunking handoff (2026-06-29):** Added
> `.ai/control/cursor_low_risk_chunking_handoff.yaml`,
> `.ai/control/low_risk_chunking_multi_pass_plan.yaml`,
> `.cursor/commands/chunking-preflight.md`,
> `.cursor/commands/low-risk-chunking-candidate.md`,
> `.cursor/commands/codex-review-packet.md`,
> `.cursor/rules/logos-scripture-low-risk-chunking.mdc`,
> `docs/roadmap/T404_CURSOR_LOW_RISK_CHUNKING_HANDOFF.md`,
> `docs/roadmap/T406_LOW_RISK_CHUNKING_MULTI_PASS_PLAN.md`,
> `scripts/validate_cursor_low_risk_chunking_handoff.py`, and
> `tests/test_cursor_low_risk_chunking_handoff.py`; updated preflight, the decision register,
> lesson index, readiness map, TOCs, roadmap/status, methodology, validator, and handoff surfaces;
> and recorded `CD-078` plus `LSN-032`. T404 confirms T402 research is complete only at
> all-66-book triage depth and schedules T406 as a future review-only Cursor batch after exact
> owner-or-Codex targets are supplied. It authorizes no target selection, reviewed gold, child
> spans, output, route/evaluator behavior, graph/retrieval/vector truth, embeddings/indexes,
> boundary import, backend/profile choice, source/manuscript rows, canon-scope change, or theology
> authority.

> **T403 deterministic runtime timeout ceiling enforcement (2026-06-29):** Hardened
> `.ai/control/test_runtime_preflight.yaml`, `AI_FRONT_DOOR.md`,
> `scripts/validate_test_runtime_preflight.py`, `scripts/validate_chunking_agent_preflight.py`, and
> `tests/test_test_runtime_preflight.py` so `python scripts/validate_all.py` has a machine-checked
> minimum timeout of 900000 ms. This was prompted by a known 240000 ms timeout followed by a
> successful 900000 ms run. The rule is runtime discipline only and does not authorize skipping,
> bypassing, output, data, chunking, graph/retrieval/vector, boundary, source/manuscript, or
> theology-authority changes.

> **T402 low-complexity chunking runway (2026-06-25):** Added
> `.ai/control/t402_eph1_post_pilot_review.yaml`,
> `.ai/control/whole_bible_low_complexity_chunking_candidate_queue.yaml`,
> `docs/roadmap/T402_LOW_COMPLEXITY_CHUNKING_RUNWAY.md`, `.ai/tasks/T402.task.yaml`,
> `.ai/handoffs/T402/handoff.md`,
> `.ai/audits/reports/20260625-T402-low-complexity-runway.md`,
> `scripts/validate_t402_low_complexity_chunking_runway.py`, and
> `tests/test_t402_low_complexity_chunking_runway.py`; updated preflight, the decision register,
> lesson index, readiness map, TOCs, roadmap/status, audit, and handoff surfaces; and recorded
> `CD-077` plus `LSN-031`. T402 confirms child spans are not necessary now for the exact T401
> Eph.1.3-Eph.1.14 pilot and creates an all-66-book candidate queue. Low-complexity means review eligibility only. It is review/research only
> and authorizes no target selection, reviewed gold, child spans, output, route/evaluator behavior,
> graph/retrieval/vector truth, boundary import, source-tradition preference, canon-scope change,
> source/manuscript rows, whole-Bible output, or theology authority.

> **T401 Eph.1.3-Eph.1.14 output pilot (2026-06-25):** Added
> `.ai/control/t401_eph1_output_pilot_manifest.yaml`,
> `docs/roadmap/T401_EPH1_OUTPUT_PILOT.md`, `.ai/tasks/T401.task.yaml`,
> `.ai/handoffs/T401/handoff.md`,
> `.ai/audits/reports/20260625-T401-eph1-output-pilot.md`,
> `scripts/validate_t401_eph1_output_pilot.py`, and
> `tests/test_t401_eph1_output_pilot.py`; updated the orchestrator, preflight, decision register,
> lesson index, readiness map, TOCs, roadmap/status, audit, and handoff surfaces; and recorded
> `CD-076` plus `LSN-030`. T401 implements only the exact parent-only output pilot for
> `Eph.1.3-Eph.1.14`. It preserves all baseline/non-target output byte-identical and authorizes no
> child spans, broader behavior, evaluator changes, graph/retrieval/vector truth, boundary import,
> source/manuscript rows, preferred readings/source traditions, canon-scope change, whole-Bible
> output, or theology authority. Post-pilot review is next before any child-span or broader work.

> **T397 Eph.1.3-Eph.1.14 route-isolation harness (2026-06-24):** Added
> `.ai/control/t397_eph1_route_isolation_harness.yaml`,
> `docs/roadmap/T397_EPH1_ROUTE_ISOLATION_HARNESS.md`, `.ai/tasks/T397.task.yaml`,
> `.ai/handoffs/T397/handoff.md`,
> `.ai/audits/reports/20260624-T397-eph1-route-isolation-harness.md`,
> `scripts/chunking/route_isolation_harness.py`,
> `scripts/validate_t397_eph1_route_isolation_harness.py`, and
> `tests/test_route_isolation_harness.py` /
> `tests/test_t397_eph1_route_isolation_harness.py`; updated preflight, the decision register,
> lesson index, readiness map, TOCs, roadmap/status, audit, and handoff surfaces; and recorded
> `CD-074` plus `LSN-028`. T397 is a harness proof gate only. It does not authorize output,
> implementation, child spans, route/evaluator behavior, graph/retrieval/vector truth, boundary
> import, source/manuscript rows, preferred readings/source traditions, canon-scope change, or
> theology authority. A future output pilot requires a fresh owner gate.

> **T399 focused Bible-wide research queue (2026-06-24):** Added
> `.ai/control/t399_focused_bible_wide_research_queue.yaml`,
> `docs/roadmap/T399_FOCUSED_BIBLE_WIDE_RESEARCH_QUEUE.md`, `.ai/tasks/T399.task.yaml`,
> `.ai/handoffs/T399/handoff.md`,
> `.ai/audits/reports/20260624-T399-focused-bible-wide-research-queue.md`,
> `scripts/validate_t399_focused_bible_wide_research_queue.py`, and
> `tests/test_t399_focused_bible_wide_research_queue.py`; updated preflight, the decision register,
> lesson index, readiness map, TOCs, roadmap/status, audit, and handoff surfaces; and recorded
> `CD-073` plus `LSN-027`. T399 completes Goal 2 as a scored, non-output-changing focused queue
> with owner-decision prompts. Recommendations are not owner selections, high scores are not
> authority, and blocked variant/source-tradition cases remain blocked before promotion or
> implementation. T397 remains the separate harness route.

> **T398 Bible-wide phase-one research synthesis (2026-06-23):** Added
> `.ai/control/t398_bible_wide_phase_one_research_synthesis.yaml`,
> `docs/roadmap/T398_BIBLE_WIDE_PHASE_ONE_RESEARCH_SYNTHESIS.md`,
> `.ai/tasks/T398.task.yaml`, `.ai/handoffs/T398/handoff.md`,
> `.ai/audits/reports/20260623-T398-bible-wide-phase-one-research-synthesis.md`,
> `scripts/validate_t398_bible_wide_phase_one_research_synthesis.py`, and
> `tests/test_t398_bible_wide_phase_one_research_synthesis.py`; updated preflight, the decision
> register, lesson index, readiness map, TOCs, roadmap/status, audit, and handoff surfaces; and
> recorded `CD-072` plus `LSN-026`. T398 proves whole-corpus accounting at triage/registry depth,
> not deep verse-by-verse exegesis. It turns the T384/T386 findings into Goal 2 focused-research
> prompts and keeps T397 as the next harness route. Not authorized: target selection, reviewed
> gold, child spans, output, route/evaluator behavior, graph/retrieval/vector truth, boundary
> import, preferred reading/source-tradition choice, canon-scope change, source/manuscript row
> creation, whole-Bible output, or theology authority.

> **T396 DSS biblical witness source rows (2026-06-23):** Added
> `.ai/control/dss_biblical_witness_source_rows.yaml`,
> `data/candidate/source_catalog/manuscript_reliability/sqlite/dss_biblical_witness_rows.jsonl`,
> `data/candidate/source_catalog/manuscript_reliability/sqlite/dss_biblical_witness_rows_manifest.yaml`,
> `docs/roadmap/T396_DSS_BIBLICAL_WITNESS_SOURCE_ROWS.md`,
> `scripts/validate_dss_biblical_witness_source_rows.py`, and
> `tests/test_dss_biblical_witness_source_rows.py`. T396 loads the T395 schema and source seed
> rows in in-memory SQLite, then populates exactly nine metadata-only Great Isaiah Scroll exemplar
> rows across holding-institution, witness-record, identifier, date, material, coverage, discovery,
> and review-queue tables. It records `CD-075` and `LSN-029` after main used `CD-072`/`LSN-026`
> for T398, `CD-073`/`LSN-027` for T399, and `CD-074`/`LSN-028` for T397. It preserves candidate/blocked status for date/material/coverage/shelfmark/script/rights
> normalization, and validates official source URLs routed through T391/T395. It authorizes no
> additional witness population without a later
> task, committed SQLite database file, source text import, transcription storage, Bible text
> storage, image ingestion, preferred reading, source-tradition preference, non-biblical DSS import,
> boundary import, doctrine lineage import, graph/retrieval/vector truth, chunk output, or
> apologetic conclusion as Scripture authority.

> **T395 SQLite source catalog schema shell (2026-06-23):** Added
> `.ai/control/manuscript_source_catalog_sqlite_shell.yaml`,
> `data/candidate/source_catalog/manuscript_reliability/sqlite/schema.sql`,
> `data/candidate/source_catalog/manuscript_reliability/sqlite/seed_rows.jsonl`,
> `data/candidate/source_catalog/manuscript_reliability/sqlite/manifest.yaml`,
> `docs/roadmap/T395_SQLITE_SOURCE_CATALOG_SCHEMA_SHELL.md`,
> `scripts/validate_manuscript_source_catalog_sqlite_shell.py`, and
> `tests/test_manuscript_source_catalog_sqlite_shell.py`. T395 validates the schema in in-memory
> SQLite, seeds only source-family/source-catalog/method-profile/source-trust rows from T391
> official anchors, keeps witness/date/material/coverage/discovery/holding-institution/review
> queue tables empty, records `CD-070` and `LSN-024`, and forbids `canonical_*`, `boundary_*`,
> and `doctrine_*` source-catalog objects. It authorizes no committed SQLite database file,
> witness row population, source text import, transcription storage, Bible text storage, preferred
> reading, source-tradition preference, canon-scope change, graph/retrieval/vector truth,
> boundary import, doctrine lineage import, chunk output, or apologetic conclusion as Scripture
> authority.

> **T394 Eph.1.3-Eph.1.14 parent-only reviewed-gold promotion (2026-06-23):** Added
> `.ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml`,
> `docs/roadmap/T394_EPH1_PARENT_ONLY_REVIEWED_GOLD_PROMOTION.md`,
> `scripts/validate_t394_eph1_parent_only_reviewed_gold_promotion.py`, and
> `tests/test_t394_eph1_parent_only_reviewed_gold_promotion.py`; updated
> `eval/chunking_gold/per_form/epistle_argument_gold_manifest.json`, the decision register, lesson
> index, readiness map, TOCs, audit, status, and handoff surfaces; and recorded `CD-071` plus
> `LSN-025`. T394 promotes only `Eph.1.3-Eph.1.14` as parent-only reviewed gold, confirms no
> current-repo internal variant refs, confirms current-repo variant/source-tradition non-dependency,
> denies child spans now, and leaves T397 as later non-output-changing harness prep. Not authorized:
> chunk output, implementation, route/evaluator behavior, graph/retrieval/vector truth, boundary
> import, preferred reading/source-tradition choice, source/manuscript row creation, canon-scope
> change, or theology authority.

> **T393 Eph.1.3-Eph.1.14 reviewed-gold promotion decision packet (2026-06-23):** Added
> `.ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml`,
> `docs/roadmap/T393_EPH1_REVIEWED_GOLD_PROMOTION_DECISION_PACKET.md`,
> `scripts/validate_t393_eph1_reviewed_gold_promotion_decision_packet.py`, and
> `tests/test_t393_eph1_reviewed_gold_promotion_decision_packet.py`, and recorded `CD-068` plus
> `LSN-022`. This prepared Goal 5 only. It recommended `T393-A` for owner review and is now
> resolved by the separate T394 owner response; reviewed_gold_promoted remains false in the T393
> packet itself. No chunk output, child spans, route/evaluator behavior, graph/retrieval/vector
> truth, boundary import, preferred reading/source-tradition choice, canon-scope change, or theology
> authority is authorized by the T393 packet.

> **T392 Eph.1.3-Eph.1.14 review packet strengthening (2026-06-23):** Added strengthened
> evidence and controls to `eval/chunking_gold/review_packets/eph1_3_14_argument_review.md`,
> added `docs/roadmap/T392_EPH1_REVIEW_PACKET_STRENGTHENING.md`,
> `scripts/validate_t392_eph1_review_packet_strengthening.py`, and
> `tests/test_t392_eph1_review_packet_strengthening.py`, and recorded `CD-067` plus `LSN-021`.
> This completes Goal 4 only. Goal 5 must present exact promotion options, repercussions,
> theological risks, variant dependency/non-dependency, child-span necessity/denial, and a
> recommendation. No reviewed gold, chunk output, child spans, route/evaluator behavior,
> graph/retrieval/vector truth, boundary import, preferred reading/source-tradition choice,
> canon-scope change, or theology authority is authorized.

> **T385 owner decision packet (2026-06-23):** Added
> `.ai/control/t385_owner_decision_packet.yaml`,
> `docs/roadmap/T385_OWNER_DECISION_PACKET.md`,
> `scripts/validate_t385_owner_decision_packet.py`, and
> `tests/test_t385_owner_decision_packet.py`. T385 records all serious faithful next options:
> Eph.1.3-Eph.1.14, Gal.2.15-Gal.3.29, Jas.2.14-Jas.2.26, Rom.9.1-Rom.11.36,
> Heb.7.1-Heb.10.39, 1Cor.11.17-1Cor.14.40, John.3.1-John.3.36, Revelation research-only, and
> manuscript source-catalog research. It records `CD-066` and `LSN-020`, makes the packet mandatory
> preflight, and keeps owner selection pending. Recommended next owner choice is T385-A, but that
> recommendation does not authorize Goal 4 work until Lowell explicitly selects it.

> **T391 manuscript source catalog research packet (2026-06-22):** Added
> `.ai/control/manuscript_source_catalog_research_packet.yaml`,
> `docs/roadmap/T391_MANUSCRIPT_SOURCE_CATALOG_RESEARCH_PACKET.md`,
> `scripts/validate_manuscript_source_catalog_research_packet.py`, and
> `tests/test_manuscript_source_catalog_research_packet.py`. T391 curates official source anchors
> including IAA/Leon Levy DSS, Israel Museum Great Isaiah Scroll anchors, INTF/NTVMR/Liste/ECM/CBGM,
> CSNTM, Manchester Greek P 457/P52, Codex Sinaiticus Project, Vatican Library Vat.gr.1209, and
> British Library Royal MS 1 D V. It records a five-family taxonomy, DSS biblical witness packet,
> NT papyri/codices packet, discovery timeline anchors, open questions, blocked claims, and a next
> goal prompt for a fresh source-catalog schema/source-row shell task. It separates confirmed source
> facts from candidate claims and blocked claims and requires source, method, confidence, provenance,
> and review status. T391 records `CD-069` and `LSN-023` and authorizes no SQLite database creation,
> row population, source text import, transcription storage, Bible text storage, preferred reading,
> source-tradition preference, canon-scope change, graph/retrieval/vector truth, boundary import,
> Doctrine Genealogy import, chunk output, or apologetic conclusion as Scripture authority.

> **T390 manuscript source catalog metadata plan (2026-06-22):** Added
> `.ai/control/manuscript_source_catalog_metadata_plan.yaml`,
> `docs/roadmap/T390_MANUSCRIPT_SOURCE_CATALOG_METADATA_PLAN.md`,
> `scripts/validate_manuscript_source_catalog_metadata_plan.py`, and
> `tests/test_manuscript_source_catalog_metadata_plan.py`. T390 turns the T387 scaffold into a
> concrete SQLite-ready metadata plan with `scripture_*` and `evidence_*` table candidates for
> source catalogs, holding institutions, catalog witness records, identifiers, date claims,
> material claims, coverage claims, discovery events, method profiles, source trust rules, and
> review queues. Every planned table denies Scripture text, transcription text, and boundary text
> storage and requires source URL, provenance, confidence, and review status. It hard-routes church
> fathers, patristic citations, commentaries, theologian writings, reception history, early creed
> wording, non-biblical Qumran/DSS content, and doctrine lineage outside Scripture Graph. It records
> future goal prompts for DSS population, NT papyri/codices population, copy-abundance/variant
> method profiling, discovery timeline, Boundary Literature reception reconstruction, and Doctrine
> Genealogy lineage. T390 records `CD-065` and `LSN-019` and authorizes no SQLite database creation,
> row population, source text import, preferred reading, source-tradition preference,
> canon-scope change, graph/retrieval/vector truth, boundary import, Doctrine Genealogy import,
> chunk output, or apologetic conclusion as Scripture authority.

> **T389 Chunking Launch Readiness report (2026-06-22):** Added
> `docs/roadmap/T389_CHUNKING_LAUNCH_READINESS_REPORT.md`, task, handoff, roadmap state entry,
> status wiring, `CD-064`, `LSN-018`, and TOC/front-door routing. The project is ready for T385
> owner packet work, not output-changing chunking. The report uses T384 Bible-wide research/readiness, T386 passage
> coverage, T387 manuscript witness scaffold, T388 stale-branch audit, and the Governance branch
> reconciliation register as evidence. It keeps all output, target selection, reviewed-gold,
> child-span, route/evaluator, graph/retrieval/vector, boundary import, preferred-reading,
> source-tradition, canon-scope, and theology-authority changes blocked until explicit owner gates.

> **T388 legacy branch discovery audit (2026-06-22):** Added
> `.ai/audits/reports/20260622-T388-legacy-branch-discovery-audit.md`, task, handoff, roadmap
> state entry, LSN-017, and status wiring to preserve rediscovery instructions before retiring stale
> branches. `feat/scale-connection-discovery-codex-5-5` is an old T308 candidate run that must be
> treated as historical candidate signal only; it should be revisited only by rerunning/comparing
> current candidate discovery against current canonical 66-book data. Local-only
> `t320-t325-boundary-entity-commentary-planning-pack` contains useful but stale planning for
> boundary texts, commentary/reception, and raw-marker risks; it is superseded by current T327F,
> T382, T383, T386, T387, and Boundary Literature direction and should be revisited only as
> historical planning signal. Do not merge either branch directly.

> **T387 manuscript witness reliability scaffold (2026-06-22):** Added
> `.ai/control/manuscript_witness_reliability_scaffold.yaml`,
> `docs/roadmap/T387_MANUSCRIPT_WITNESS_RELIABILITY_SCAFFOLD.md`,
> `scripts/validate_manuscript_witness_reliability_scaffold.py`, and
> `tests/test_manuscript_witness_reliability_scaffold.py`. T387 records the placement decision:
> canonical Scripture manuscript-witness metadata belongs in Scripture Graph, while non-biblical
> Qumran/DSS corpus text, patristic reception, church fathers, commentaries, and theologian writings
> remain in Boundary Literature. The scaffold plans `scripture_*` and `evidence_*` tables for
> witness sources, manuscript witnesses, variant units, attestations, discovery timeline events,
> and derived reliability claims. It requires source, method, confidence, provenance, and review
> status before date, language, script, material, coverage, variant, copy-abundance, discovery, or
> reliability claims are trusted. It does not import source text, change canonical Bible text or
> passage records, select preferred readings or source traditions, change canon scope, import
> boundary corpora, create graph/retrieval/vector truth, or authorize apologetic conclusions as
> Scripture authority. T385 remains the next chunking owner-decision route.

> **T386 Bible-wide verse/passage coverage inventory (2026-06-22):** Added
> `.ai/control/bible_verse_passage_coverage_inventory.jsonl`,
> `.ai/control/bible_verse_passage_coverage_taxonomy.yaml`,
> `.ai/control/bible_verse_passage_coverage_summary.yaml`,
> `.ai/control/bible_verse_passage_readiness_matrix.yaml`,
> `.ai/control/bible_verse_passage_gap_register.yaml`, and
> `.ai/control/bible_verse_passage_human_review_docket.yaml`, checked by
> `scripts/validate_bible_verse_passage_coverage_inventory.py`. T386 accounts for every canonical
> passage at triage depth and records routine passages, review-packet needs, source metadata,
> Strong's-style tags, original-language phrase/context needs, textual-variant/source-tradition
> sensitivity, cross-reference/intertext risk, WJ/red-letter and speaker/discourse risk,
> divine-name/title capitalization sensitivity, known non-orthodox pressure passages, theological
> downstream risk, owner-decision requirements, and blocked authority actions. T386 records `CD-062`
> and `LSN-014`, updates preflight/TOC/readiness surfaces, and keeps T385 as the next non-output
> owner decision packet using both T384 and T386. It does not select an exact target, promote
> reviewed gold, authorize child spans, change output, alter route/evaluator behavior, generate
> graph/retrieval/vector truth, import boundaries, prefer readings/source traditions, change canon
> scope, or authorize theology claims. After the full pytest suite exceeded the default 5-minute
> tool timeout, T386 also added `.ai/control/test_runtime_preflight.yaml`, `LSN-015`, and
> `WORKFLOW-LESSON-010` so future agents know `python -m pytest -q` needs a longer timeout or split
> strategy and must not treat timeout as green.

> **T384 Bible-wide research/readiness synthesis (2026-06-21):** Added
> `.ai/control/t384_bible_wide_research_readiness_synthesis.yaml`,
> `docs/roadmap/T384_BIBLE_WIDE_RESEARCH_READINESS_SYNTHESIS.md`, and
> `.ai/audits/reports/20260621-T384-bible-wide-research-readiness.md`, checked by
> `scripts/validate_t384_bible_wide_research_readiness.py`. T384 completes the broad research-first
> goal as governed readiness, not chunk output. It records what is ready for review-packet
> strengthening, what still needs more research, required human decisions `HDM-001` through
> `HDM-007`, what must remain blocked, and `T385` as the next owner-decision packet. It records
> `CD-061` and `LSN-013` and does not select an exact target, promote reviewed gold, authorize
> child spans, change output, alter route/evaluator behavior, generate graph/retrieval/vector
> truth, import boundaries, prefer readings/source traditions, change canon scope, or allow
> denominational systematic theology as chunk authority.

> **T376 epistle argument research runway (2026-06-21):** Added
> `.ai/control/t376_epistle_research_runway.yaml`,
> `docs/roadmap/T376_EPISTLE_RESEARCH_RUNWAY.md`, and
> `.ai/audits/reports/20260621-T376-epistle-research-runway.md`, checked by
> `scripts/validate_t376_epistle_research_runway.py`. T376 records owner selection of `T376-A`:
> continue epistle argument review/prep only, and allow non-output-changing research/options work
> to proceed before later owner decisions. It records `CD-060` and `LSN-012`, and points the next
> route to T384: an epistle argument target-options/repercussions matrix. T376 does not select an
> exact target, promote reviewed gold, authorize child spans, change output, alter route/evaluator
> behavior, generate graph/retrieval/vector truth, import boundaries, prefer readings/source
> traditions, change canon scope, or allow denominational systematic theology as chunk authority.

> **T383 contextual reading policy (2026-06-21):** Added
> `.ai/control/contextual_reading_policy.yaml`, `docs/roadmap/T383_CONTEXTUAL_READING_POLICY.md`,
> and `.ai/audits/reports/20260621-T383-contextual-reading-policy.md`, checked by
> `scripts/validate_contextual_reading_policy.py`. T383 records that context always matters:
> immediate previous/following context, paragraph/section context, chapter/book flow, canonical
> links, original-language context, historical/cultural background, and source metadata context
> must be considered as applicable before chunking or review use. Historical/cultural background
> remains evidence only and cannot override Scripture, authorize liberal-critical or
> anti-supernatural defaults, govern chunks, or create a history repo. T383 records `CD-059` and
> `LSN-011` and does not authorize output, reviewed gold, route/evaluator behavior,
> graph/retrieval/vector truth, boundary import, doctrine, or history-sidecar authority. At T383
> creation, T376 owner lane selection was the next gate; T376 is now complete and T384 is active.

> **T382 chunking lesson index (2026-06-20):** Added
> `.ai/control/chunking_lesson_index.yaml`, `docs/roadmap/T382_CHUNKING_LESSON_INDEX.md`, and
> `.ai/audits/reports/20260620-T382-chunking-lesson-index.md`, checked by
> `scripts/validate_chunking_lesson_index.py`. T382 makes reusable lessons discoverable by category,
> tags, use-when triggers, related tasks/decisions, downstream risks, source surfaces,
> non-authorizations, validators, and graph edges. The index is mandatory chunking-agent preflight
> memory and a required midflight lesson-capture surface. It records `CD-058` and does not authorize
> chunk output, reviewed-gold promotion, route/evaluator behavior, graph/retrieval/vector truth,
> boundary import, or theology claims. At T382 creation, T376 owner lane selection was the next gate;
> T376 is now complete and T384 is active.

> **T375 post-pilot review (2026-06-20):** Added
> `.ai/control/t375_post_pilot_review.yaml`, `docs/roadmap/T375_POST_PILOT_REVIEW.md`, and
> `.ai/audits/reports/20260620-T375-post-pilot-review.md`, checked by
> `scripts/validate_t375_post_pilot_review.py`. T375 reviewed the T374 same-baseline evidence and
> no-context audit trail, recorded `CD-057`, and concluded that child spans are not necessary now
> because the additive parent-only overlay preserves the whole `1Cor.8.1-1Cor.10.33` argument while
> existing baseline chunks remain byte-identical for smaller local coverage. This is not a permanent
> child-span denial and does not authorize child spans, reviewed-gold promotion, route/evaluator
> behavior, graph/retrieval/vector truth, output changes, preferred readings, source-tradition
> preference, boundary import, broader epistle generalization, or whole-Bible output. The next gate
> is T376 owner lane selection.

> **T374 additive parent overlay implementation (2026-06-20):** Updated
> `pipelines/chunking/orchestrator.py` to append one exact non-truth-bearing parent overlay for
> `1Cor.8.1-1Cor.10.33` by default, with `--disable-t374-overlay` available for baseline proof.
> Added `.ai/control/t374_additive_parent_overlay_manifest.yaml`, checked by
> `scripts/validate_t374_additive_parent_overlay.py`, and recorded `CD-056`. The manifest records
> baseline chunk count `1136`, candidate count `1137`, candidate hash
> `681a0840edd8513daeb204579ed0a1b0b0f818c910abfc83a7890317c3b481e7`, and preserved baseline
> prefix hash `eda6232b2cb7f0ab4c8dacac10ed672c247a1e41ccb1f807ace05d0ca9eec619`. No raw/canonical
> data, generated committed derived chunks, evaluator formula, leaderboard, graph/retrieval/vector
> truth, child spans, replacement, adjacent spill splits, preferred readings, source-tradition
> preference, boundary import, broader epistle generalization, or whole-Bible output is authorized.
> The next safe task is T375 review: same-baseline review, no-context audit review, and
> child-necessity review.

> **T374-OVERLAP-B owner selection record (2026-06-20):** Updated
> `.ai/control/t374_baseline_overlap_owner_decision_packet.yaml`, checked by
> `scripts/validate_t374_baseline_overlap_owner_decision_packet.py`, after a temp baseline run
> showed current 1 Corinthians chunks crossing `1Cor.8.1-1Cor.10.33`: `1Cor.7.25-1Cor.9.2`,
> `1Cor.9.3-1Cor.10.5`, and `1Cor.10.6-1Cor.11.10`. Lowell selected additive parent overlay
> semantics, so a later implementation may add only an exact `1Cor.8.1-1Cor.10.33` parent overlay
> while preserving existing baseline chunks byte-identical. Replacement with adjacent spill splits,
> deletion/replacement, target widening, and dry-run-only semantics were not selected. No raw/canonical data,
> generated chunk output, chunker/route/evaluator behavior, graph/retrieval/vector truth, child
> spans, preferred readings, source-tradition preference, boundary import, broader epistle
> generalization, or whole-Bible output is changed by this selection record.

> **T373 owner implementation authorization (2026-06-19):** Added
> `.ai/control/t373_owner_implementation_authorization.yaml`, checked by
> `scripts/validate_t373_owner_implementation_authorization.py`, so future T374 work may implement
> only the exact parent-only `1Cor.8.1-1Cor.10.33` route-isolated output-changing pilot. T373
> authorizes parent-span-as-output-boundary and route behavior only for that exact target, and
> requires non-target identity proof, same-baseline evaluation, changed-output manifest,
> decision-register update, validators/tests, no-context audit surface, and handoff validation
> before any T374 merge. It does not authorize child spans, preferred readings, source-tradition
> preference, graph/retrieval/vector truth, evaluator changes, boundary imports, broader epistle
> generalization, whole-Bible output, or hidden theological systems. Added
> `.ai/control/owner_decision_option_presentation_policy.yaml`, checked by
> `scripts/validate_owner_decision_option_presentation_policy.py`, so future owner gates must show
> all serious faithful options, repercussions, risks, recommendations, and non-authorizations.

> **T381 original-language phrase/context policy (2026-06-19):** Added
> `.ai/control/original_language_phrase_context_policy.yaml`, checked by
> `scripts/validate_original_language_phrase_context_policy.py`, so future packets that include
> Greek/Hebrew words, lemmas, Strong's-style tags, lexical rarity, morphology, or grammar labels
> must preserve phrase/clause/syntax/discourse/canonical context and cannot use isolated words,
> one-gloss definitions, Strong's-style numbers, rare lemmas, or grammar labels as theological,
> graph, retrieval, route, chunk-boundary, reviewed-gold, or output authority. The policy records
> `CD-049` and is mandatory preflight context. T373 remains the next owner implementation gate; no
> route/evaluator behavior, graph/retrieval truth, vector, implementation, chunk output, boundary
> import, canon change, doctrine system, or output change is authorized.

> **T372 route-isolation harness plan (2026-06-19):** Added
> `.ai/control/t372_route_isolation_harness_plan.yaml`, checked by
> `scripts/validate_t372_route_isolation_harness_plan.py`, so future implementation work must prove
> T373 owner authorization, exact scope, non-target identity, same-baseline evaluation planning,
> source-metadata denial, and decision-register updates before any T374 output-changing work. The
> plan records `CD-048` and advances the next route to `T373`. No child spans, parent span as chunk
> boundary, preferred reading, source-tradition preference, route/evaluator behavior, graph/retrieval
> truth, vector, implementation, chunk output, boundary import, canon change, or output change is
> authorized.

> **T371-A parent-only reviewed-gold promotion (2026-06-19):** Added
> `.ai/control/t371_parent_only_reviewed_gold_promotion.yaml` and
> `eval/chunking_gold/per_form/epistle_argument_gold_manifest.json`, checked by
> `scripts/validate_t371_parent_only_reviewed_gold_promotion.py`. The promotion records owner
> confirmation of `T371-A`, promotes only `1Cor.8.1-1Cor.10.33` as parent-only reviewed gold, and
> records `1Cor.9.20` and `1Cor.10.9` as variant-non-dependent only for the parent boundary and
> parent-only reviewed-gold claim. It records `CD-047` and advances the next safe route to `T372`
> harness/non-target identity planning. No child spans, parent span as chunk boundary, preferred
> reading, source-tradition preference, route/evaluator behavior, graph/retrieval truth, vector,
> implementation, chunk output, boundary import, canon change, or output change is authorized.

> **T380 T371 variant-dependency owner decision packet (2026-06-19):** Added
> `.ai/control/t371_variant_dependency_owner_decision_packet.yaml`, checked by
> `scripts/validate_t371_variant_dependency_owner_decision_packet.py`, so the next owner decision
> is no-context-auditable. The packet names exact refs `1Cor.9.20` and `1Cor.10.9`, records
> options `T371-A` through `T371-D`, conditionally recommends `T371-A` only if the owner confirms
> variant non-dependency, and preserves `T371-B` as the conservative hold if there is doubt. It
> records `CD-046` and keeps T371 blocked until an exact owner response. No preferred reading,
> source-tradition preference, variant dependency/non-dependency finding, reviewed gold,
> route/evaluator behavior, graph/retrieval truth, chunk, implementation, vector, boundary import,
> canon change, or output change is authorized.

> **T379 textual-critical case-by-case policy selection (2026-06-19):** Owner selected
> `TCP-T378-B` as the standing case-by-case process policy before each variant-sensitive
> promotion. Added `.ai/control/textual_critical_case_policy.yaml`, checked by
> `scripts/validate_textual_critical_case_policy.py`, and updated the owner projection policy
> with `ODP-005` so future agents remember the process pattern without treating it as preferred
> reading, source-tradition preference, dependency finding, reviewed-gold promotion, graph/retrieval
> truth, route/evaluator behavior, implementation, chunk output, or output authority. T371 may now
> proceed to the narrower owner question: whether `1Cor.8.1-1Cor.10.33` is variant-non-dependent
> with respect to `1Cor.9.20` and `1Cor.10.9`, and whether the parent-only evidence packet should
> be promoted.

> **T378 textual-critical policy owner options (2026-06-19):** Added
> `.ai/control/textual_critical_policy_owner_options.yaml`, checked by
> `scripts/validate_textual_critical_policy_owner_options.py`, so the owner can select a
> textual-critical policy before variant-sensitive promotion. T378 identifies `1Cor.9.20` and
> `1Cor.10.9` inside the T370 parent-only evidence packet as T371 blockers. It recommends
> `TCP-T378-B`, case-by-case owner policy before each variant-sensitive promotion, because that
> preserves canonical Scripture authority without smuggling critical-text, majority-text, Textus
> Receptus, current-source, liberal-critical, or denominational defaults. No policy is selected
> and no preferred reading, source-tradition preference, reviewed gold, graph/retrieval truth,
> chunk boundary, route/evaluator behavior, canon change, boundary import, vector work, or output
> change is authorized.

> **T377 orthodox original-language pressure passage dossier queue (2026-06-19):** Added
> `.ai/control/orthodox_original_language_pressure_dossier_queue.yaml`, checked by
> `scripts/validate_orthodox_original_language_pressure_dossier_queue.py`, so future chunking,
> graph, retrieval, review-packet, route, and evaluator agents start with explicit pressure
> passages rather than chat memory. The queue records John 1:1, Colossians 1:15-20, Titus 2:13,
> 2 Peter 1:1, John 8:58, Hebrews 1, Matthew 28:19, Genesis 1:26-27, Deuteronomy 6:4,
> Psalm 110:1, Isaiah 43-44, 1 Corinthians 15:29, and 1 Peter 3:18-4:6 as future
> Greek/Hebrew grammar-overlay pressure dossiers. LDS, Watch Tower/New World Translation,
> anti-Trinitarian, translation-divergence, and divine plurality/unity labels are pressure labels
> only. No source-language truth, translation preference, non-orthodox source authority,
> extra-canonical authority, doctrine selection, graph/retrieval truth, reviewed gold, chunk
> boundary, canon-scope change, boundary import, route/evaluator change, vector work, or output
> change is authorized.

> **T370 1 Corinthians 8-10 parent-only evidence packet (2026-06-18):** Built a governed
> parent-only evidence packet for `1Cor.8.1-1Cor.10.33` from canonical eng-web sidecars and
> existing T352/T368/T369 controls. The packet records verse count, current chunk behavior,
> paragraph-marker evidence, variant-sensitive footnotes, editorial cross-references,
> Strong-style clusters, divine-name/title capitalization, conflict-scan carry-forward, and T371
> promotion blockers. It is ready for owner promotion review only. No reviewed gold, child span,
> route/evaluator behavior, graph/retrieval truth, textual-critical policy, chunk boundary, or
> output change is authorized.

> **T369 owner-pattern projection and register durability (2026-06-18):** Added
> `.ai/control/governance_memory_durability_policy.yaml`, checked by
> `scripts/validate_governance_memory_durability.py`, so the chunking theological decision
> register is treated as critical, non-deletable governance memory and remains discoverable from
> the front door, AI TOCs, audit map, preflight, readiness map, task scope, and `validate_all`.
> Added `.ai/control/owner_decision_projection_policy.yaml`, checked by
> `scripts/validate_owner_decision_projection_policy.py`, so future agents may project only
> high-confidence, materially same-shape, conservative owner patterns and must stop if prior owner
> decisions conflict for the target text. T369 applies that policy to select `1COR8-10-T369-B`:
> parent-only `1Cor.8.1-1Cor.10.33` review target, no child spans, no reviewed gold, no route or
> evaluator behavior, no graph/retrieval truth, no textual-critical policy, no doctrinal system,
> and no output change. T370 evidence prep has since completed; the current next route is T371
> owner reviewed-gold promotion review only.

> **T368 1 Corinthians 8-10 packet strengthening (2026-06-18):** Strengthened the
> `1Cor.8.1-1Cor.10.33` epistle argument packet with source-evidence snapshots, candidate owner
> options, orthodox-hermeneutic/firewall dependencies, textual-critical policy dependency, and
> explicit non-authorizations. Added `.ai/control/1cor8_10_epistle_owner_review_docket.yaml`,
> checked by `scripts/validate_1cor8_10_owner_review_docket.py`, added
> `.ai/control/chunking_human_decision_forecast.yaml`, checked by
> `scripts/validate_chunking_human_decision_forecast.py`, and recorded `CD-037` and `CD-038` in
> the chunking theological decision register. The forecast explains why the broad thread goal was
> blocked, names predictable owner decisions early, defines chunking-ready conditions, and extends
> the roadmap through T376 without authorizing output. The readiness map now points to T369 owner
> review. No
> parent span, child span, doctrinal system, sacramental/ecclesial/Christian-liberty framework,
> textual-critical policy, reviewed gold, route behavior, evaluator change, graph edge, retrieval
> truth, chunk output, boundary import, vector work, raw/canonical data, generated chunks, or
> output change is authorized.

> **T367 owner decision firewall and next target (2026-06-18):** Recorded
> `JOHN3-T356-B` as parent-only `John.3.1-John.3.36` review target selection in
> `.ai/control/john3_wj_owner_review_docket.yaml`; added the Orthodox Hermeneutic Firewall /
> Anti-Smuggling Docket, checked by `scripts/validate_orthodox_hermeneutic_firewall_docket.py`;
> added the textual-critical policy requirement docket, checked by
> `scripts/validate_textual_critical_policy_docket.py`; and advanced the readiness map to T368 /
> `1Cor.8-1Cor.10` review-only packet strengthening. The firewall affirms Nicene/Chalcedonian
> orthodox Christianity and canonical Scripture authority while refusing hidden anti-supernatural,
> anti-canonical, heterodox, liberal-critical, or one-denomination systematic-theology defaults.
> The textual-critical docket requires a later explicit owner policy before variant-sensitive
> promotion/use. No output, chunk, graph, retrieval, route, evaluator, reviewed-gold, textual-critical,
> canon-scope, source-tradition, boundary-import, or vector authority is created. Next work remains
> review-only; do not start Revelation implementation, T327G, or boundary import; do not import
> boundary texts.
> Boundary-text guardrail: do not import boundary texts.

> **T366 textual variant source tradition dossier queue (2026-06-18):** Added
> `.ai/control/textual_variant_source_tradition_dossier_queue.yaml`, checked by
> `scripts/validate_textual_variant_source_tradition_dossier_queue.py`, so future
> textual-variant, source-tradition, canon-sensitive, graph, retrieval, review-packet, evaluator,
> and chunking agents can start from explicit dossiers instead of chat memory. The queue records
> Mark 16 longer-ending, John 7:53-8:11 pericope adulterae, Acts empty witnesses, Romans doxology,
> Deuteronomy 32 source-tradition, Jeremiah MT/LXX order/length, Jude noncanonical reference,
> Daniel/Esther additions boundary-routing, and 1 John 5:7 Comma Johanneum risks. It is
> non-authorizing: no textual-critical decision, canon-scope change, source-tradition preference,
> noncanonical source authority, boundary import, reviewed gold, chunk boundary, route behavior,
> evaluator change, graph edge, retrieval truth, output change, vector work, intertext truth, or
> algorithm behavior is approved.

> **T365 prophetic oracle vision dossier queue (2026-06-18):** Added
> `.ai/control/prophetic_oracle_vision_dossier_queue.yaml`, checked by
> `scripts/validate_prophetic_oracle_vision_dossier_queue.py`, so future Isaiah, Jeremiah,
> Ezekiel, Daniel, Hosea, Joel, Zechariah, graph, retrieval, review-packet, evaluator, and
> chunking agents can start from explicit dossiers instead of chat memory. The queue records
> Isaiah servant and comfort oracles, Jeremiah restoration and new covenant material, Ezekiel
> restoration and temple visions, Daniel prophetic-apocalyptic visions, Hosea sign-act/covenant
> metaphor, Joel day-of-Yahweh/Spirit material, and Zechariah night visions. It is
> non-authorizing: no fulfillment theology, eschatological system, covenant system, Israel/church
> relation, messianic identification, temple theology, prophetic chronology, reviewed gold, chunk
> boundary, route behavior, evaluator change, graph edge, retrieval truth, output change, boundary
> import, vector work, intertext truth, or algorithm behavior is approved.

> **T364 wisdom dialogue poetry dossier queue (2026-06-18):** Added
> `.ai/control/wisdom_dialogue_poetry_dossier_queue.yaml`, checked by
> `scripts/validate_wisdom_dialogue_poetry_dossier_queue.py`, so future Job, Proverbs,
> Ecclesiastes, Song, Lamentations, Psalm 119, graph, retrieval, review-packet, evaluator, and
> chunking agents can start from explicit dossiers instead of chat memory. The queue records Job
> dialogue cycles and divine speeches, Proverbs wisdom speeches, Proverbs 31, Ecclesiastes refrain
> and argument cycles, Song speaker-boundary and genre-sensitive lyric units, Lamentations acrostic
> lament units, and Psalm 119. It is non-authorizing: no wisdom theology, Job theodicy system,
> Ecclesiastes frame, Song allegorical/literal system, speaker assignment, liturgical use,
> reviewed gold, chunk boundary, route behavior, evaluator change, graph edge, retrieval truth,
> output change, boundary import, vector work, or algorithm behavior is approved.

> **T363 narrative legal covenant dossier queue (2026-06-18):** Added
> `.ai/control/narrative_legal_covenant_dossier_queue.yaml`, checked by
> `scripts/validate_narrative_legal_covenant_dossier_queue.py`, so future narrative, legal,
> covenant, genealogy/list, royal-annal, restoration-document, graph, retrieval, review-packet,
> evaluator, and chunking agents can start from explicit dossiers instead of chat memory. The
> queue records Genesis primeval and patriarchal cycles, Sinai, Levitical ritual law, Balaam,
> Deuteronomy covenant speeches, Joshua allotments, Samuel-Kings royal covenant/annal material,
> Chronicles/Ezra/Nehemiah restoration lists/documents, and Matthew/Luke genealogy/birth
> narratives. It is non-authorizing: no covenant system, law/gospel framework, typology,
> harmonization, source-critical partition, reviewed gold, chunk boundary, route behavior,
> evaluator change, graph edge, retrieval truth, output change, boundary import, vector work, or
> algorithm behavior is approved.

> **T362 Gospel WJ discourse dossier queue (2026-06-18):** Added
> `.ai/control/gospel_wj_discourse_dossier_queue.yaml`, checked by
> `scripts/validate_gospel_wj_discourse_dossier_queue.py`, so future Gospel discourse,
> WJ/red-letter, speaker-boundary, graph, retrieval, review-packet, evaluator, and chunking agents
> can start from explicit discourse dossiers instead of chat memory. The queue records John 3,
> Sermon on the Mount, Farewell Discourse, Olivet discourse, John 7:53-8:11, Revelation voice
> shifts, and non-Gospel WJ/dominical quotation cases. It is non-authorizing: no Jesus speaker
> attribution, speaker boundary, discourse boundary, reviewed gold, chunk boundary, route behavior,
> evaluator change, graph edge, retrieval truth, output change, boundary import, vector work, or
> algorithm behavior is approved.

> **T361 epistle argument theological issue dossier queue (2026-06-18):** Added
> `.ai/control/epistle_argument_theological_issue_dossier_queue.yaml`, checked by
> `scripts/validate_epistle_argument_theological_issue_dossier_queue.py`, so future epistle
> argument, graph, retrieval, review-packet, evaluator, and chunking agents can start from explicit
> issue dossiers instead of chat memory. The queue records existing T352 pending packet risks for
> `Eph.1.3-Eph.1.14`, `Rom.9-Rom.11`, `Heb.7-Heb.10`, and `1Cor.8-1Cor.10`, plus future
> candidates in `Gal.3-Gal.4`, `Rom.7-Rom.8`, `Jas.2`, `1Pet.3.18-1Pet.3.22`,
> `1John.1-1John.2`, and `Jude.5-Jude.15`. It preserves multiple orthodox options for election,
> covenant, law/gospel, assurance, sacramental language, faith/works, justification, union with
> Christ, and source/tradition-sensitive questions. It is non-authorizing: no doctrine system,
> reviewed gold, argument boundary, chunk boundary, route behavior, evaluator change, graph edge,
> retrieval truth, output change, boundary import, vector work, or algorithm behavior is approved.

> **T360 apocalyptic prophetic intertext dossier queue (2026-06-18):** Added
> `.ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml`, checked by
> `scripts/validate_apocalyptic_prophetic_intertext_dossier_queue.py`, so future Revelation,
> Daniel, prophetic, Gospel discourse, graph, retrieval, review-packet, evaluator, and chunking
> agents can start from explicit intertext dossiers instead of chat memory. The queue preserves
> futurist, preterist, historicist, idealist, premillennial, amillennial, postmillennial,
> typological, and already/not-yet readings where orthodox, and refuses to select Revelation
> chronology, millennium view, tribulation timing, temple fulfillment, Babylon/beast identity, or
> Israel/church relation. It is non-authorizing: no Scripture truth, lexical truth, intertext truth,
> speaker attribution, graph edge, retrieval truth, reviewed gold, chunk boundary, output change,
> boundary import, vector work, or algorithm behavior is approved.

> **T359 source metadata research atlas (2026-06-18):** Added
> `.ai/control/source_metadata_research_atlas.yaml`, checked by
> `scripts/validate_source_metadata_research_atlas.py`, so future chunking, graph, retrieval,
> review-packet, evaluator, and audit agents can see source metadata families before relying on
> chat memory. The atlas records observed canonical surfaces and evidence-only handling for
> internal cross-references, Strong's-style word numbers, lexical rarity, footnotes, alternate
> readings, headings, paragraph/poetry markers, WJ/red-letter markers, speaker labels, edition
> formatting, and divine-name/title capitalization. It is stacked after T358 and remains
> non-authorizing: no Scripture truth, lexical truth, intertext truth, speaker attribution, graph
> edge, retrieval truth, reviewed gold, chunk boundary, output change, boundary import, vector work,
> or algorithm behavior is approved.

> **T358 Bible-wide chunking research registry (2026-06-18):** Added
> `.ai/control/bible_wide_chunking_research_registry.yaml`, checked by
> `scripts/validate_bible_wide_chunking_research_registry.py`, so future chunking agents can begin
> whole-Bible research from a canonical 66-book queue instead of chat memory. The registry records
> book-level lanes, boundary questions, theological downstream risks, source-metadata watchpoints,
> and future review-packet candidates. It is parallel research-only work: it does not select a John
> 3 option, does not supersede the pending T357 owner-selection/gold gate, and does not authorize
> chunks, reviewed gold, route behavior, graph edges, retrieval truth, embeddings, source metadata
> authority, speaker attribution, boundary import, or implementation.

> **T356 John 3 WJ owner-review docket (2026-06-18):** Added
> `.ai/control/john3_wj_owner_review_docket.yaml`, checked by
> `scripts/validate_john3_owner_review_docket.py`, so the next John 3 human decision is explicit
> and no-context-auditable. The docket presents options `JOHN3-T356-A` through `JOHN3-T356-E`:
> preserve current chunks, approve parent-only John 3 review scope, approve parent plus exact
> child-boundary review target, approve a narrower Jesus-speech unit only, or require more
> research. Owner selection remains pending. No John 3 parent span, child span, Jesus/narrator
> boundary, reviewed gold, chunk output, graph edge, retrieval truth, or route behavior is
> approved.

> **T355 WJ speaker/discourse policy and target selection (2026-06-18):** Added
> `.ai/control/wj_speaker_discourse_policy.yaml`, checked by
> `scripts/validate_wj_speaker_discourse_policy.py`, so future Gospel discourse,
> speaker-boundary, graph, retrieval, route, evaluator, review-packet, and chunk agents must read
> the WJ speaker policy before using red-letter evidence. The policy selects John 3 as the first
> exact owner-review target because the packet already exists, the scope is smaller than John
> 13-17, and observed WJ evidence is split. The selection remains non-authorizing: no John 3
> speaker boundary, discourse boundary, reviewed gold, chunk output, graph edge, retrieval truth,
> Revelation voice identity, or WJ-driven route behavior is approved.

> **T354 WJ marker inventory harness (2026-06-18):** Added
> `.ai/control/wj_marker_inventory.yaml`, generated by
> `scripts/build_wj_marker_inventory.py` and checked by
> `scripts/validate_wj_marker_inventory.py`, so future chunking, graph, retrieval, route,
> evaluator, speaker-boundary, and review-packet agents can see observed WJ/red-letter marker
> token runs before relying on chat memory. The inventory is mandatory preflight reading and
> records CD-021 in the chunking theological decision register. WJ evidence outside the four
> Gospels is visible, including Acts, epistle quotations, and Revelation. John 3 and John 13-17 are
> preserved as split WJ evidence rather than collapsed into a single speaker/discourse decision. No
> Jesus speaker attribution, speaker-boundary, discourse-boundary, graph-edge, chunk-boundary,
> retrieval-truth, reviewed-gold, or output-change authority is created.

> **T353 divine capitalization inventory harness (2026-06-17):** Added
> `.ai/control/divine_capitalization_inventory.yaml`, generated by
> `scripts/build_divine_capitalization_inventory.py` and checked by
> `scripts/validate_divine_capitalization_inventory.py`, so future chunking, graph, retrieval,
> route, evaluator, and review-packet agents can see observed capitalization variants before
> relying on chat memory. The inventory is mandatory preflight reading and records CD-020 in the
> chunking theological decision register. Pronoun casing and Strong's-style numbers remain broad
> source evidence only; no divine identity, Trinitarian relation, Christology, pneumatology,
> speaker attribution, lexical truth, graph-edge, chunk-boundary, retrieval-truth, reviewed-gold,
> or output-change authority is created.

> **T352 epistle argument review packets (2026-06-17):** Added pending review packets for
> `Eph.1.3-Eph.1.14`, `Rom.9-Rom.11`, `Heb.7-Heb.10`, and `1Cor.8-1Cor.10` as the first
> review-packet-ready lane after T351 triage. The packet and observed-behavior indexes now mark
> these cases as `review_packet_pending`, not reviewed gold. Added CD-019 and
> `scripts/validate_epistle_argument_review_packets.py` so epistle argument packets stay
> non-authorizing. No chunk implementation, reviewed-gold promotion, output change, evaluator
> change, generated chunk regeneration, graph/vector work, T345, or Revelation implementation is
> authorized.

> **T351 Bible-wide chunking research triage (2026-06-17):** Added
> `docs/roadmap/T351_BIBLE_WIDE_CHUNKING_RESEARCH_TRIAGE_ATLAS.md` and
> `.ai/control/bible_chunking_research_triage_map.yaml` so the project researches the whole Bible
> before selecting more chunking work. T351 also replaces invalid nonnumeric `T344R` continuation
> surfaces with numeric task `T351`. The triage says epistle argument and narrative/legal lanes are
> review-packet-ready, Revelation/prophetic/wisdom/Gospel-WJ/textual-variant lanes need research
> first, Psalms are a governed hold, and Bible-wide orchestration remains implementation-blocked.
> No output, reviewed-gold, graph/vector, boundary import, evaluator, generated chunk, or T345 work
> is authorized.
> Follow-up T351 divine-name/title capitalization lane: after the owner flagged `God/god`,
> `Spirit/spirit`, `Father/father`, `Word/word`, and related capitalization risks, T351 now treats
> English divine-name/title/pronoun capitalization as translation/editorial evidence only. It must
> be inventoried and reviewed before graph, retrieval, or chunking use, and it cannot by itself
> authorize divine identity, Trinitarian relation, speaker attribution, graph edges, chunk
> boundaries, lexical truth, or output changes.

> **T344 REV-T344-E owner decision (2026-06-17):** Added
> `docs/roadmap/T344_REVELATION_OWNER_SELECTION_DOCKET.md` as the exact decision surface for the
> pending `Rev.12.1-Rev.14.20` Revelation packet. The docket offers five owner options:
> `REV-T344-A` preserve current behavior, `REV-T344-B` promote parent-only reviewed gold,
> `REV-T344-C` promote parent plus exact child spans, `REV-T344-D` mark characterization-only, or
> `REV-T344-E` require more research. Lowell Wong selected `REV-T344-E`: Revelation work may
> continue as research/prep only until stronger governed evidence exists, and epistle argument
> boundaries are the next review lane after Revelation research prep. All implementation,
> output-change, reviewed-gold, graph-edge, embedding/index, boundary-import, source-metadata
> authority, and skill-promotion flags remain false. T344 also adds a no-context
> audit harness (`.ai/audits/`, `.ai/control/audit_surface_map.yaml`,
> `.ai/control/harness_upgrade_roadmap.yaml`, `scripts/agent/no_context_audit_harness.py`, and
> `scripts/validate_audit_surface_map.py`) so a separate reviewer can reconstruct intent, changed
> files, changelogs, decision surfaces, validation, future harness watch conditions, and likely
> harness-upgrade candidates from repo state after commit/push. Control-plane/selection/audit-
> harness only; no raw/canonical/generated chunk/evaluator/runtime work occurred.
> Follow-up audit report:
> `.ai/audits/reports/20260617-T344-codex-post-merge.md` records a post-merge no-context review
> of PR #60, no P0-P2 findings, one fixed stale-focus wording issue, and the then-pending T344
> owner selection before REV-T344-E was recorded.
> Follow-up HARN-012 gate: `scripts/validate_owner_selection_implementation_gate.py` is wired into
> `validate_all` to keep T345 planned and non-authorized while T344 is selected as REV-T344-E
> research/prep only, and to fail closed if T345/output-changing work starts before selected
> reviewed evidence agrees across the docket, task, review packet, readiness map, roadmap state,
> and harness roadmap.
> Post-merge audit report:
> `.ai/audits/reports/20260617-T344-HARN-012-codex-post-merge.md` records the merged PR #62
> HARN-012 state, no findings, and the then-remaining T344 owner-selection requirement.
> Follow-up HARN-006 scanner: `scripts/validate_source_metadata_authority.py` is wired into
> `validate_all` to keep source metadata, internal cross-references, Strong's-style numbers,
> lexical rarity, headings, footnotes, WJ markers, and formatting as evidence only, not boundary,
> lexical, intertext, graph-edge, truth, or output authority.
> Post-merge audit report:
> `.ai/audits/reports/20260617-T344-HARN-006-codex-post-merge.md` records the merged PR #64
> HARN-006 state, no findings, and the then-remaining T344 owner-selection requirement.
> Follow-up HARN-001 scope gate: `scripts/validate_task_scope.py` is wired into `validate_all` to
> require changed files to stay inside the active task's declared `allowed_paths`, fail on
> `forbidden_paths`, and hard-stop AI changes to the human-gated master context surfaces. CI now
> checks out full history so changed-path validators can inspect PR diffs.

> **T343 Revelation review packets and metadata preflight (2026-06-17):** Created
> `eval/chunking_gold/review_packets/rev12_14_symbolic_scenes_review.md` for the T342-selected
> `Rev.12.1-Rev.14.20` target. The packet is `pending_human_review` and records candidate
> parent/child options, current observed chunk behavior, Revelation hermeneutic-neutrality
> constraints, canonical allusion research-prep issues, source metadata risks, Greek lexical-rarity
> constraints, and RISK-GATE-001 risks. Added `docs/roadmap/T343_REVELATION_REVIEW_PACKETS_AND_GOLD_CANDIDATES.md`,
> updated the review-packet indexes, coverage docs, AI roadmap TOC, readiness map, roadmap state,
> task, tests, and handoff surfaces. Added `.ai/control/chunking_agent_preflight.yaml`,
> `scripts/validate_chunking_agent_preflight.py`, methodology rule `CHUNK-METADATA-001`, workflow
> lesson `BIBLE-CHUNKING-WORKFLOW-LESSON-003`, and decision register entry `CD-015` so future
> chunking agents must inherit the metadata lesson before work. Control-plane/review-only; no
> reviewed gold, output change, route behavior, evaluator change, generated output, raw/canonical
> mutation, boundary import, T327G, Revelation implementation, embedding/index/edge work, graph-edge
> generation, whole-Bible output-changing pass, or Psalm candidate promotion.

> **T342 Revelation review-packet candidate selection (2026-06-17):** Selected
> `Rev.12-Rev.14` / `Rev.12.1-Rev.14.20` as the single Revelation target for T343 packet creation
> because it concentrates symbolic scenes, speaker shifts, and cycle/interlude risk while remaining
> narrow enough for one packet. Added `docs/roadmap/T342_REVELATION_REVIEW_PACKET_CANDIDATE_SELECTION.md`,
> advanced `.ai/control/bible_chunking_readiness_map.yaml` to T343, recorded decision `CD-014` in
> the chunking theological decision register, and added deterministic tests for T342. Also added
> `docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md` after the maintainer observed that the T337A trail
> should have been easier to find; the local TOC links back to the main AI TOC and names the actual
> T337A task, handoff, and Psalm 89 review-packet files. Control-plane only; no review packet,
> reviewed gold, output change, route behavior, evaluator change, generated output, raw/canonical
> mutation, boundary import, T327G, Revelation implementation, embedding/index/edge work, graph-edge
> generation, whole-Bible output-changing pass, or Psalm candidate promotion.

> **T350 Bible-wide chunking readiness plan (2026-06-17):** Added
> `.ai/control/bible_chunking_readiness_map.yaml` as a machine-readable, non-authorizing readiness
> map for whole-Bible chunking. The map records the faithful route as one reviewed lane at a time
> under the Bible-wide goal, names current algorithm surfaces, records lane readiness and theological
> risks, points lesson storage to the workflow lessons, rules registry, supply chain, unintended
> consequence review, review-packet index, and chunking theological decision register, and keeps
> T342 as Revelation review-packet candidate selection only. Added
> `scripts/validate_bible_chunking_readiness_map.py`, focused tests, validate_all integration,
> T350 roadmap/task/handoff state, and a T350 decision-register entry. Control-plane only; no
> output-changing chunking, reviewed-gold promotion, evaluator formula change, generated output,
> raw/canonical mutation, boundary import, T327G, Revelation implementation, embedding/index/edge
> work, graph-edge generation, whole-Bible output-changing pass, or Psalm candidate promotion.

> **T349 first-class chunking theological decision register (2026-06-17):** Added
> `.ai/control/chunking_theological_decision_register.yaml` as a machine-readable,
> non-authorizing governance ledger for chunking/evaluator/gold/route/default-behavior decisions
> with possible theological downstream effects. The register uses the Nicene/Chalcedonian core as
> default orthodoxy boundary, classifies decisions as `text_neutral`, `theological_risk`,
> `interpretive_boundary`, `canon_scope`, or `non_authorizing_review`, and records owner decision
> refs, task/PR refs, affected passages/books/routes, downstream risks, theological assumptions
> avoided, reviewed-gold dependencies, non-authorizations, validators, and supersession/deprecation
> fields. Seeded decisions include canonical 66 scope, Psalm 78 parent/child, Psalm 89 Option C,
> WJ marker limits, Revelation non-implementation, Psalm candidate non-promotion, and vector/edge
> "never truth." `scripts/validate_chunking_theological_decision_register.py` is wired into
> `validate_all` and fails closed if required seed decisions, backfill coverage, non-authority
> flags, or changed-path register updates are missing. Control-plane only; no chunk algorithm,
> route behavior, reviewed-gold promotion, evaluator formula, generated output, raw/canonical data,
> boundary import, T327G, Revelation implementation, embedding/index/edge work, or Psalm candidate
> promotion occurred.

> **T340D remove post-merge verification requirement (2026-06-11):** Owner decision (Lowell Wong)
> deleted the post-merge verification script/workflow/templates/tests; the principle that a merged
> PR does not by itself authorize the next task is retained as front-door/roadmap guidance.

> **T340C harden post-merge verification script (2026-06-10):** Hardened
> `scripts/agent/post_merge_verify.py` (fail-closed missing-binary handling, explicit `--skip-pytest`
> surfacing, token-bounded next-task matching) and added `tests/test_post_merge_verify_behavior.py`.
> Gated on a passing post-merge verification of PR #52/T340B (verdict PASS). No verification gate or
> CLI flag removed; tooling/test/control-plane only; no raw/canonical/generated/chunk/evaluator/
> leaderboard/scorecard/boundary-import/T327G/Revelation-implementation/skill-lifecycle/Psalm-promotion
> work.

> **T340B standard post-merge verification (2026-06-10):** Added
> `scripts/agent/post_merge_verify.py`,
> `.ai/templates/POST_MERGE_AND_NEXT_TASK_PROMPT.md`,
> `.ai/templates/NEXT_TASK_HANDOFF_CHECKLIST.md`, and
> `docs/workflows/POST_MERGE_VERIFICATION_WORKFLOW.md`. The workflow standardizes recurring
> post-merge checks: sync `main`, confirm PR state, verify expected and merge commits are reachable,
> confirm clean tree and no merge/rebase state, run required validation, report optional next-task
> state, and stop on failure. The script does not edit files, create commits, create branches, push,
> open PRs, or start the next task. Entry surfaces now point agents to the reusable workflow before
> follow-up work. This is workflow/tooling/control-plane only and does not authorize output-changing
> work, raw/canonical mutation, generated output regeneration, evaluator/chunker/orchestrator
> changes, leaderboard/scorecard changes, boundary import, T327G, Revelation implementation, or
> Psalm candidate promotion.

> **T341 Revelation hard-book atlas (2026-06-10):** Post-merge verification for PR #50 / T340
> passed before T341 started: `main` fast-forwarded cleanly, PR #50 was `MERGED`, GitHub validate
> succeeded, merge commit `abaa35485a844db3b0ffcd00a84f6c308038908a` and commit `b1ca468` were
> reachable, the working tree had no merge/rebase state, and local validation passed. T341 adds
> `docs/roadmap/T341_REVELATION_HARD_BOOK_ATLAS.md` and
> `docs/roadmap/T341_REVELATION_OBSERVED_BEHAVIOR_AUDIT.md`. The atlas maps Revelation hard-case
> areas, current committed post-T327 Revelation chunks, RISK-GATE-001 unintended-consequence risks,
> candidate future review packets, and guardrails before implementation. The audit is limited to
> committed artifacts; no protected output was regenerated. T341 is non-output-changing
> planning/control-plane work only and does not authorize Revelation implementation, reviewed gold,
> route behavior, global apocalypse/prophecy/poetry/WJ/discourse rules, boundary import, T327G,
> skill promotion, evaluator/leaderboard/scorecard changes, or whole-Bible improvement claims. Next
> should be T342 Revelation review-packet candidate selection, not implementation.

> **T340 Psalm candidate promotion decision (2026-06-10):** Stage A post-merge verification for PR
> #49 / T339 passed: `main` fast-forwarded cleanly, PR #49 was `MERGED`, GitHub validate succeeded,
> merge commit `bd221478c01314bcd452a7d8fe6ca0dab869a956` and commit `fabb268` were reachable,
> protected paths were clean, and local validation passed. Stage B records decision `hold` in
> `.ai/control/t340_psalm_candidate_promotion_decision.yaml` and
> `docs/roadmap/T340_PSALM_CANDIDATE_PROMOTION_DECISION.md`. The Psalm candidate skill remains
> `lifecycle_state: candidate`; `approved-skills.json`, skill registries, runtime code, and chunking
> behavior were not changed. The decision preserves the exact Psalm 89 Option C route-isolated
> behavior and reviewed Psalm guardrails while explicitly not authorizing broad Psalm optimization,
> global Psalm/poetry/Selah/blank-line/doxology/long-Psalm rules, marker-only boundary authority,
> whole-Bible improvement claims, boundary import, T327G, or Revelation implementation. T341 may
> proceed only as a Revelation hard-book atlas/review lane, not implementation; alternatively collect
> additional reviewed Psalm evidence before reconsidering promotion.

> **T339 Psalm 89 same-baseline risk evaluation (2026-06-10):** Verified PR #48 / T338 was merged
> into `main`, confirmed merge commit `a495e0c78961195db8a0d6b3df95bcc58f203dd2` and commit
> `00cc891` are reachable, and evaluated pre-T338 commit `1db3f12` against current T338 main using
> temporary outputs under `%TEMP%/t339_eval`. Direct chunker output remained byte-identical at SHA
> `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025`; routed output moved from the
> same SHA to `eda6232b2cb7f0ab4c8dacac10ed672c247a1e41ccb1f807ace05d0ca9eec619`. The routed count
> changed from 1,131 to 1,136 because one Psalm 89 parent was replaced by six reviewed children.
> Non-Psalm-89 routed records were identical, including Ps78, Ps105, Ps106, Ps119, short Psalms,
> Ps3 superscription, Song, and Lamentations controls. Evaluator diagnostics changed as expected:
> raw literal Psalm fragmentation 1 -> 2, reviewed structural splits Ps78 -> Ps78/Ps89, final
> `literal_psalms_fragmented` stayed 0. T339 records RISK-GATE-001 risks for hidden global Psalm
> rules, global doxology handling, marker-heuristic confusion, premature candidate-skill promotion,
> and overclaiming broad Bible improvement. T340 is next as a promote-or-reject decision only; no
> chunking behavior, evaluator formula, leaderboard, scorecard, raw/canonical/derived data,
> committed output/chunk regeneration, boundary import, T327G, Revelation implementation, or global
> Psalm/poetry/Selah/blank-line/doxology rule changed.

> **T338 Psalm 89 route-isolated parent/child implementation (2026-06-10):** Verified PR #47 /
> T337B was merged into `main` before branching. Implemented the exact Psalm 89 Option C target only
> in `psalm-whole-then-stanza-v1`, behind the existing literal `Ps` orchestrator route. The skill
> delegates to the monolith Psalm behavior, applies the approved Psalm 89 child spans only when full
> `Ps.89.1-Ps.89.52` input is present, preserves downstream/non-target chunk records and IDs, and
> fails closed against reviewed Psalm gold. Same-baseline temp evaluation: direct chunker stayed
> byte-identical at SHA `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025`; routed
> output changed from 1,131 to 1,136 chunks with after SHA
> `eda6232b2cb7f0ab4c8dacac10ed672c247a1e41ccb1f807ace05d0ca9eec619`; non-Psalm-89 routed records
> were identical; evaluator diagnostics now show reviewed structural splits for Ps78 and Ps89 with
> `literal_psalms_fragmented` still 0. No committed chunk outputs, scorecards, leaderboard rows,
> evaluator formula, raw/canonical data, boundary import, T327G, Revelation implementation, global
> Selah/blank-line/doxology/poetry/long-Psalm rule, or whole-Bible improvement claim occurred.

> **T337B Psalm 89 owner decision Option C (2026-06-10):** PR #46 / T337A was already merged, so
> T337B was created as a follow-up branch from current `main`. Applied the owner's Option C human
> review decision to the Psalm 89 packet, Psalm manifest, Psalm plan, and review-packet index.
> Psalm 89 is now reviewed gold with `implementation_allowed: true`, `output_change_authorized:
> true`, and `reviewed_gold_promoted: true` for this exact target only. The approved model preserves
> parent `Ps.89.1-52`, keeps `Ps.89.49-52` as one final retrieval child, labels `Ps.89.52` as the
> Book III doxology, and forbids treating `Ps.89.52` as ordinary lament continuation or splitting it
> into a one-verse orphan. T337B authorizes future route-isolated T338 planning/implementation for
> Psalm 89 only; it does not authorize global Selah, blank-line, doxology, poetry, or long-Psalm
> rules. No T338 implementation, chunk output change, regeneration, evaluator/chunker/orchestrator
> behavior change, leaderboard/scorecard change, raw/canonical mutation, source import, boundary
> import, T327G, or Revelation implementation occurred.

> **T337A Psalm target human-review packet (2026-06-10):** Verified PR #45 / T337 was merged into
> `main`, confirmed commit `b78b267` is present, and confirmed a clean worktree with no merge/rebase
> state before starting. Selected Psalm 89, not Psalm 136, as the single human-review candidate.
> Psalm 89 is longer, structurally richer, and more likely to support a narrow parent/child review
> decision; Psalm 136 remains pending and non-authorizing. Expanded the Psalm 89 review packet with
> exact proposed child spans (`Ps.89.1-4`, `Ps.89.5-18`, `Ps.89.19-37`, `Ps.89.38-45`,
> `Ps.89.46-48`, `Ps.89.49-52`), required future executable checks, non-target identity
> requirements, and RISK-GATE-001 mapping. The packet is still pending and non-authorizing; no new
> reviewed gold, output authorization, chunking behavior, generated output, evaluator, leaderboard,
> scorecard, raw/canonical data, source import, boundary import, T327G, T338, or Revelation
> implementation changed.

> **T337 Psalm behavior-change target selection (2026-06-09):** After PR #44 / T336B post-merge
> verification passed, reviewed the Psalm gold manifest, Psalm gold plan, Ps78/Ps105/Ps106 reviewed
> packets, Ps89/Ps136 pending packets, T332/T335/T336 roadmap surfaces, and the existing Psalm
> candidate skill seam. T337 found no authorized behavior-changing Psalm target. Ps78, Ps105,
> Ps106, Ps119, short Psalm, and superscription cases are reviewed preservation or exact-current-
> behavior guardrails; Ps89 and Ps136 are pending only. T337 therefore blocks T338 until a T335-style
> follow-up human review promotes one exact Psalm target with executable checks and explicit output
> authorization. Documentation/control-plane/test only; no chunking behavior, generated output,
> evaluator, leaderboard, scorecard, raw/canonical data, source import, boundary import, T327G, or
> Revelation implementation changed.

> **T336B unintended consequence review gate (2026-06-09):** Verified PR #43 / T336 was merged into
> `main`, confirmed a clean worktree with no merge/rebase state, and created
> `t336b-unintended-consequence-review-gate`. Added `RISK-GATE-001` requiring high-leverage changes
> to map what they could accidentally authorize, weaken, contaminate, overfit, globalize, or make
> harder to reverse. Added `TEXT-HYGIENE-001` so machine-checked control strings prefer ASCII-safe
> punctuation and terminal mojibake is verified against real file bytes/content before editing.
> Added `WORKFLOW-LESSON-002`, the reusable methodology doc, front-door/TOC and
> workflow discoverability pointers, and deterministic doc-policy tests for the new rule plus T336
> Bible-first priority, Revelation atlas-before-implementation, route isolation, master-chunker
> safety, boundary import prohibition, T327G not-started state, and text-hygiene handling.
> Documentation/control-plane/test only; no runtime behavior or data/output mutation.

> **T336 optimized whole-Bible chunking roadmap (2026-06-09):** Reconstructed current state from
> `main`, confirmed T336 was unused, confirmed T335 was merged via PR #41, noted PR #42 as a T335
> follow-up during original drafting, and later refreshed the PR branch after PR #42 merged. Added
> `docs/roadmap/T336_OPTIMIZED_WHOLE_BIBLE_CHUNKING_ROADMAP.md` and
> concise updates to front-door, TOC, roadmap, roadmap state, prior roadmap docs, methodology, task,
> status, and handoff surfaces. T336 records the implementation order
> Psalms -> epistles -> narrative -> wisdom/dialogue -> prophetic oracle -> Gospel discourse/WJ ->
> Revelation/apocalypse -> Bible-wide orchestration, and the hard-book atlas order Revelation ->
> prophets -> Gospel discourse/WJ -> Job/Song/Wisdom -> Daniel bridge. T336 is planning/control-
> plane only and authorizes no chunking behavior change, Revelation implementation, boundary import,
> source import, raw/canonical/generated mutation, evaluator formula change, leaderboard/scorecard
> change, or T327G work.

> **T335 reviewed Psalm stress/gold coverage expansion (2026-06-09):** Verified PR #40 / T334 was
> merged into `main`, merge commit `4f9ce2` is present, T334 commit `a748cf3` is present, and no
> merge/rebase state existed before starting. Added pending human-review packets for `Ps.89.1-52`
> and `Ps.136.1-26` as characterization-only, non-authorizing Psalm stress/gold coverage. The
> Psalm manifest, gold plan, coverage inventory, observed stress behavior, review-packet index, and
> tests now agree that these cases are pending review, `implementation_allowed: false`, and
> `output_change_authorized: false`. Marker/refrain evidence remains evidence only; no new reviewed
> gold, output-changing authorization, chunk output/default behavior change, evaluator formula
> change, leaderboard/scorecard change, raw/canonical/generated mutation, source import, boundary
> import, Revelation implementation, or T327G work occurred. T335 records Revelation only as a
> future hard-book atlas/review-packet lane: likely higher interpretive risk than Psalms, requiring
> apocalypse/Revelation-specific review rules and reviewed gold before implementation. Next safe
> lane: human review may promote a specific Psalm packet with exact spans before any
> behavior-changing T336 work.

> **T334 T333 Psalm guardrail evaluation (2026-06-09):** Verified PR #39 / T333 was merged into
> `main`, commit `3bb9396` is present, GitHub validate succeeded, `main` fast-forwarded cleanly,
> and no merge/rebase state existed before starting. Added
> `docs/roadmap/T334_EVALUATE_T333_PSALM_GUARDRAIL.md` and small read-only assertions in
> `tests/test_psalm_candidate_skill.py`. Finding: T333 is same-baseline guardrail work only. The
> candidate Psalm skill still delegates to `chunker.chunk_book(...)`; reviewed Psalm spans fail
> closed on drift; reviewed evidence is cited; no chunk output/default behavior change or score
> movement is claimed. Next safe lane: T335 reviewed Psalm stress/gold coverage expansion before any
> behavior-changing Psalm work. No raw/canonical/generated/chunk/evaluator/runtime/scorecard/source-
> import/boundary-import/T327G work occurred.

> **T310 (new, 2026-06-05):** Four blind design proposals (Claude/Codex/Cursor/Composer) for a
> form-routed chunking orchestrator + skill registry were reconciled with the owner into **ADR-0011**
> (`docs/architecture/ADR-0011-…`). Decisions D1–D8 + B+ locked (marker-evidenced form routing +
> LLM-adjudicator shadow records; full ~40-form map flagged active/declared-gap; parametric skills;
> 8-state lifecycle; committed `registry/chunking/`; incremental per-form gold; deferred contract-lock
> gate). Build is a **byte-identical extraction** of the current chunker. Pre-T311 steps were gated at
> old-evaluator composite **≥ 88.5**; after T311, the unchanged D / Claude pass2 output is the
> corrected-evaluator baseline **93.0**. The chunking subtrees (`pipelines/chunking/`,
> `config/chunking/`, `registry/chunking/`)
> are now **proprietary / All Rights Reserved** (`pipelines/chunking/LICENSE`, carved out of root MIT).
> Source designs + reconciliation: `.ai/context/recommendations/`. Next: finish pre-3b readiness,
> then plan T310 3b against corrected baseline and per-form gold evidence.

> **T310 3b target selection (2026-06-06):** Planning-only investigation recommends **3b-gold**.
> Current D/pass2 chunks were located/regenerated in ignored space and byte-match SHA-256
> `8c134378e6391be2034c9e534267df218f5dd20b04970b55660aae128c86c5e7`; corrected score remains 93.0.
> `Ps.78` is the single literal Psalm fragmentation target, currently split into `Ps.78.1-69`,
> `Ps.78.70-71`, and `Ps.78.72` (1165 tokens if merged). Direct composite upside is only +0.5, and
> the split reflects soft-token/stanza evidence rather than a clear hard-gate bug. Before any output
> change, convert `eval/chunking_gold/per_form/psalms_gold_plan.md` into executable/reviewed Psalm
> gold covering Ps 23, Ps 119, Ps 78, short-Psalm holdouts, and non-target poetry controls.

> **T310 3b-gold implemented (2026-06-06):** Added executable Psalm gold manifest/tests for settled
> cases without changing output: Ps.23 one chunk, Ps.119 22 sections and not penalized, short Psalm
> holdouts (`Ps.1`, `Ps.8`, `Ps.100`, `Ps.117`), real Ps.3 superscription source evidence with no
> orphan title chunk, and non-target route controls (`Song`, `Lam`, `PrMan`, `Ps151`) staying on
> monolith fallback. Ps.78 is recorded as characterization-only with current boundaries/token counts
> and `pending_human_review`; no merge/preserve decision was promoted.

> **Methodology update (2026-06-06):** Living methodology, workflow checklist, skill playbook, and
> methodology control rule now distinguish scaffold/plan, executable reviewed gold,
> characterization-only evidence, and pending human review. Output-changing skill work now explicitly
> requires executable/reviewed gold first; weak evaluator levers like Ps.78's +0.5 upside cannot drive
> implementation without target-form evidence.

> **Post-3b roadmap planning pack (2026-06-06):** T310 3b-gold is complete and remains a gold-gate
> increment, not a chunking improvement claim. The next T310 action is human review of the Ps.78
> boundary packet, followed by an explicit merge-vs-preserve decision before any output-changing 3b
> work. T313 token-size evaluator/policy alignment, T320 biblical entity/spiritual realm layer, T330
> theological concept graph, and T340 retrieval/rendering contracts are separate future lanes. No
> output-changing 3b work has started.

> **Ps.78 parent/child gold decision (2026-06-06):** Human review approved preserving the current
> Psalm 78 child chunks under a parent whole-psalm literary unit. Parent: `Ps.78.1-72`; children:
> `Ps.78.1-69`, `Ps.78.70-71`, and `Ps.78.72`. This records reviewed gold and the parent/child
> structural-split lesson; it does not change chunk output, evaluator formula, raw/canonical data,
> runtime chunking code, or skill promotion. Current evaluator policy may still report
> `literal_psalms_fragmented=1`; any change to that treatment is a separate evaluator-policy task.

> **T314 reviewed structural split evaluator policy (2026-06-06):** Evaluator policy now preserves
> raw literal Psalm fragmentation diagnostics while excluding exact manifest-reviewed parent/child
> structural splits from final bad-fragmentation scoring. For unchanged D / Claude pass2 output,
> `literal_psalms_fragmented_raw=1`, `reviewed_structural_splits=1`, final
> `literal_psalms_fragmented=0`, and composite is 93.5. Score provenance chain is now 88.5 old
> evaluator -> 93.0 T311 book/chapter evaluator -> 93.5 T314 reviewed-structural-split policy. This
> is evaluator-policy correction, not chunk-output improvement.

> **T315 gold/evaluator/roadmap hardening (2026-06-07):** Added semantic validation for
> `eval/chunking_gold/per_form/*_manifest.json`, wired it into `validate_all`, added focused tests,
> created `GOLD_COVERAGE_INVENTORY.md`, audited score-language references, updated stale T313/ADR
> baseline prose to the T314 93.5 policy baseline, and created future-target / roadmap-registration
> plans. Broad future task registration is deferred until those tasks have real handoffs. No chunk
> output, evaluator formula, raw/canonical data, chunker/orchestrator behavior, runtime skill code, or
> skill promotion changed. Next possible work: T316 Biblical Chunking Stress Atlas, T313 token-size
> policy alignment, or T320/T321 planning. No output-changing chunk work is currently authorized.

> **T316 Biblical Chunking Stress Atlas (2026-06-07):** Created a proposed-only stress atlas under
> `eval/chunking_gold/stress_atlas/` with structured JSON cases and tests covering long structured
> units, long verses/lists, short context-dependent units, Greek long sentences, punctuation risk,
> major textual variants, DSS/LXX/MT divergence, speaker ambiguity, prophetic oracles, apocalyptic
> visions, legal/covenant blocks, genealogies/lists, parallel accounts, rhetorical arguments, hard
> exegesis, and parent/child candidates. All cases are `status: proposed` with
> `implementation_allowed: false`. This does not change chunk output, evaluator formula,
> raw/canonical data, chunker/orchestrator behavior, runtime skill code, or skill promotion. Stress
> cases must become reviewed gold or review packets before implementation.

> **T316b stress-case review packets (2026-06-07):** Created pending review packets for Ps.105,
> Ps.106, Isa.52.13-53.12, Mark.16.9-20, and John.7.53-8.11. Packets record current chunk behavior
> and local marker/footnote evidence only. All decisions remain `pending_human_review`; no packet is
> reviewed gold, no selected case is approved expected output, and no output-changing work is
> authorized. Ps.105 and Ps.106 are prioritized as long-Psalm parent/child candidates; textual
> variant packets require textual-criticism review before gold.

> **T316c words-of-Jesus marker stress cases (2026-06-07):** Added proposed stress-atlas coverage
> for words-of-Jesus `\wj` spans, Selah / `\qs` mid-psalm markers, John 3 speaker-boundary
> ambiguity, Matthew 5-7, John 13-17, Matthew 24-25 / Mark 13, and John 7:53-8:11 as a textual
> variant plus `\wj` speech issue. All cases remain `status: proposed` with
> `implementation_allowed: false`. `\wj` and `\qs` are recorded as marker evidence, not authority
> for speaker attribution, theological/text-critical decisions, or chunk boundaries. No reviewed
> gold, output change, evaluator change, raw/canonical mutation, runtime skill change, or skill
> promotion occurred.

> **T317 Psalm gold, WJ packets, token policy (2026-06-07):** Human review approved current Ps.105
> and Ps.106 whole-psalm behavior as reviewed gold: `Ps.105.1-45` remains one 601-token chunk and
> `Ps.106.1-48` remains one 721-token chunk. Ps.106 `b` markers are recorded as internal
> formatting/stanza evidence, not automatic child-boundary authority. Added pending WJ review
> packets for John 3 and Matthew 5-7; `\wj` and punctuation are evidence, not speaker attribution
> authority, and both packets remain `pending_human_review`. Updated T313 analysis to state that
> the p50 metric headroom is an evaluator/policy alignment risk, not authorization to retune
> chunking. No chunk output, evaluator formula, raw/canonical data, chunker/orchestrator behavior,
> runtime skill code, or skill promotion changed.

> **T318 observed stress atlas behavior audit (2026-06-08):** Added a diagnostic-only observed
> behavior surface for every T316/T316c stress-atlas case. The audit records current chunks touching
> each case, containment, splitting, extra-context mixing, marker evidence, review-packet status, and
> recommended next review steps. It preserves Ps.105/Ps.106 as already reviewed current behavior and
> keeps pending packets pending. All observed entries have `implementation_allowed: false`. This is
> triage evidence only: no reviewed gold was added, no evaluator policy changed, no chunk output
> changed, and no output-changing work is authorized.

> **T319 review packet index and promotion queue (2026-06-08):** Added
> `eval/chunking_gold/review_packets/review_packet_index.json` and
> `REVIEW_PACKET_INDEX.md` as a single diagnostic/control surface over 8 existing review packet
> files, 8 Psalm manifest reviewed cases, and all 44 observed stress-audit cases. The index has 60
> entries and a review queue for pending/policy-required/manual-investigation work. Every entry keeps
> `implementation_allowed: false` and `output_change_authorized: false`. T319 does not add reviewed
> gold, approve pending packets, change evaluator policy, change chunk output, mutate raw/canonical
> data, change runtime skill code, or authorize output-changing work.

> **T327A forensic canonical corpus scope audit (2026-06-08):** Owner decision recorded:
> `logos-scripture-graph` canonical Scripture/chunking scope is the 66-book canon. The current raw
> WEB archive has 83 USFM files: 66 canonical files, 15 deuterocanonical/apocrypha/non-66 files,
> front matter, and glossary. Current generated passages/witnesses contain 81 books and 6,955
> excluded non-66 records; local generated chunk variants and committed scorecards/leaderboard
> lineage were produced against the wider corpus. T327A is audit/planning only: no raw/canonical
> data, generated output, parser/chunker/orchestrator/evaluator behavior, scorecards, or boundary
> repo content changed. Next: T327B explicit 66-book allow-list / ingest filter before any
> T320/T325/T326 implementation work continues.

> **T327A1 three-repo routing guardrails (2026-06-08):** Added Scripture-side AI front-door routing
> and `.ai/control/boundary_material_routing.yaml`. `logos-scripture-graph` owns canonical 66-book
> Scripture truth and canonical chunking/evaluator/gold surfaces; `logos-boundary-literature` owns
> boundary, deuterocanonical/apocrypha, heterodox, disputed, forged, commentary/reception, and
> supporting literature as scoped background/comparison/refutation material; `logos-governance-
> architecture` owns the cross-repo registry / relationship-contract source of truth. Boundary
> material must not override, contaminate, or become equal authority to canonical Scripture.
> Scripture-side routing mirrors the governance registry locally for agent routing. No data, output,
> evaluator, scorecard, runtime, text-import, or T327B work occurred.

> **T327A2 boundary governance stop rules (2026-06-08):** Added Scripture-side mirrors of
> `BOUNDARY-GOV-001 - Governance Is Constraint, Not Obstacle` and `BOUNDARY-GOV-002 -
> Owner-Reserved Authorization for Boundary-Originated Higher-Layer Changes`. Boundary-originated
> requests that conflict with governance-layer policy, canonical Scripture authority,
> repository-link contracts, routing policy, trust hierarchy, or canonical scope must stop and be
> reviewed in the higher-authority repo. Only Lowell Wong, as project owner, may authorize
> boundary-originated changes to higher-authority governance, canonical Scripture authority,
> repository-link contracts, canonical scope, trust hierarchy, or cross-repo policy. Contributor
> consensus, contributor volume, automated recommendation, agent routing, and boundary-layer
> operational need are not sufficient authority. No data, output, evaluator, scorecard, runtime,
> text-import, or T327B work occurred.

> **T327B canonical 66-book ingest filter (2026-06-08):** Confirmed T327A.1 routing guardrails and
> T327A.2 stop-rule mirror are live on main, then added `config/canon/canonical_66_books.yaml`,
> `pipelines/util/canonical_scope.py`, and `scripts/validate_canonical_66_scope.py`. Future WEB
> USFM importer now has an explicit `--canonical-66-filter` flag that gates canonical passages,
> witnesses, and canonical sidecars to the owner-approved 66-book allow-list while preserving raw
> USFM event observation. Existing generated outputs may still contain non-66 records until T327C
> regeneration. T327D handles chunks,
> scorecards, leaderboard, and score language; T327E cleans gold/stress/review packet surfaces. No
> raw/canonical data, generated output, chunks, evaluator formula, leaderboard, scorecards, source
> texts, or T327C/D/E/F/G work changed.

> **T327B.1 canonical scope validator fail-closed hardening (2026-06-08):** Hardened
> `scripts/validate_canonical_66_scope.py` / `pipelines/util/canonical_scope.py` so optional
> canonical JSONL validation fails closed when a record has no resolvable `book`, `osis_book`,
> `usfm_book`, `osis_ref`, or `passage_id`. Valid 66-book records pass; excluded books, `GLO`,
> `FRT`, and glossary-like unclassified records fail. Glossary/front-matter/concordance/source
> metadata may be preserved only as separately scoped non-scripture supporting/reference artifacts,
> not canonical passages/chunks/witness text/leaderboard inputs/default retrieval text. The validator
> does not prove content authenticity if fake or altered text is falsely labeled with an allowed
> book such as `Mark`; that remains a raw source manifest, checksum, provenance, parser determinism,
> and raw immutability concern. No raw/canonical data, generated output, chunks, evaluator formula,
> leaderboard, scorecards, source texts, or T327C/D/E/F/G work changed.

> **T327C regenerate canonical 66 outputs (2026-06-08):** Regenerated local ignored canonical
> Scripture outputs with `python pipelines/ingest/usfm_importer.py --canonical-66-filter
> --processed-root build/t327c_processed/usfm`. Passage/witness outputs now contain exactly 66
> books and 31,103 records, down from 81 books and 38,058 records; 6,955 non-66
> deuterocanonical/apocrypha records were removed from generated canonical passage/witness outputs.
> `GLO` glossary entries are now zero in canonical outputs, and `FRT`/`GLO` are not canonical
> Scripture content. Canonical sidecars now carry book identity where needed for fail-closed
> validation. CI regeneration now uses `--canonical-66-filter`, and `validate_all` runs
> canonical-scope validation over regenerated canonical outputs and sidecars. This is corpus-scope
> correction, not chunking improvement. No data/raw mutation, chunk regeneration, evaluator formula
> change, leaderboard/scorecard update, gold/stress/review packet index update, source-text import,
> boundary repo change, or T327D/E/F/G work occurred. T327D owns chunk regeneration, scorecards,
> leaderboard, baseline language, and gold test hash/token updates.

> **T327D regenerate chunks for canonical 66 baseline (2026-06-08):** Regenerated D / Claude
> pass2 chunks from the corrected 66-book canonical outputs in ignored derived space. The
> post-T327 canonical-66 chunk baseline is 1,131 chunks with SHA-256
> `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025`, token p50 728,
> token p90 898, token max 1,152, and composite 93.6 under unchanged T314 evaluator policy. The
> previous 1,374-chunk / 93.5 row is now explicitly labeled as `pre_t327_wider_corpus`; the new
> row is `post_t327_canonical_66_corpus`. Removed temporary T327C xfails and removed `PrMan` /
> `Ps151` from canonical Psalm gold controls. This is corpus-scope correction / baseline reset,
> not chunking improvement. No raw data, canonical passage/witness outputs, evaluator formula,
> chunking algorithm, boundary repo, T327E/F/G, or text import work occurred. T327E owns broader
> gold/stress/observed/index cleanup.

> **T327E old-corpus eval surface cleanup (2026-06-09):** Searched old-corpus terms across
> gold/stress/observed/review-packet/governance surfaces and classified occurrences as active
> controls, stale baseline language, historical audit/provenance, exclusion tests, boundary-routing
> policy, or unclear review. Updated stress-atlas baseline wording to the post-T327 canonical-66
> 93.6 baseline, labeled the T318 observed audit as historical pre-T327 wider-corpus diagnostic
> evidence rather than current post-T327 behavior, and updated the Psalm candidate skill docs/metadata
> so active canonical non-target controls are only `Song` and `Lam`. Historical T327A/T327B/T327C
> audit evidence, exclusion tests/config, raw source inventories, and boundary-routing policy were
> preserved. This is corpus-scope cleanup, not chunking improvement. No raw data, canonical
> passage/witness outputs, chunk regeneration, evaluator formula, chunking algorithm, leaderboard
> scoring, boundary repo, T327F/G, or text import work occurred.

> **T327F boundary source intake planning (2026-06-09):** Verified T327E PR #31 was merged, commit
> `a20aefb` was present on `main`, CI validate succeeded, and the working tree had no merge/rebase
> state before starting T327F. Added `docs/roadmap/T327F_BOUNDARY_SOURCE_INTAKE_PLANNING.md` and
> `.ai/control/boundary_source_intake_plan.yaml` as planning-only surfaces for future
> `logos-boundary-literature` source intake. Candidate source families include
> deuterocanonical/apocrypha, noncanonical boundary literature, gnostic/heterodox texts,
> disputed/forged/fake texts, commentary/reception corpora, Josephus/Philo/DSS/Qumran/patristic
> corpora, and front matter/glossary artifacts as non-Scripture supporting material. T327F authorizes
> no imports, downloads, boundary corpus records, raw/canonical mutation, chunk regeneration,
> evaluator/chunker/orchestrator changes, leaderboard/scorecard changes, boundary repo edits, or
> T327G work. Future intake requires owner authorization, source/license/provenance controls,
> trust hierarchy, tradition-scoped canon status, contamination tests, and a separate boundary-repo
> PR.

> **T328 workflow lesson collector update (2026-06-09):** Verified T327F PR #32 was merged, commit
> `44da678` was present on `main`, CI validate succeeded, and the working tree had no merge/rebase
> state before starting T328. Created `docs/methodology/WORKFLOW_LESSONS.md` as a reusable
> control-plane lesson collector. Added `WORKFLOW-LESSON-001` for generated-artifact durability,
> `T327-LESSON-001` for untracked generated outputs shifting review burden to generator/config/CI
> validation and downstream handoff, `BOUNDARY-WORKFLOW-LESSON-001` for planning/authority-gated
> boundary-source intake, and `LAW-FIRM-WORKFLOW-LESSON-001` as an exception-to-action analogue.
> Governance and boundary repos were inspected but not edited because governance had existing dirty
> work and boundary had local untracked cache output; LawFirm/FMG repos were locally present but not
> safe for this Scripture-side PR because candidate worktrees were on unrelated branches or dirty.
> T328 is docs/control-plane only and authorizes no raw/canonical mutation, generated output
> regeneration, chunk regeneration, evaluator/chunker/orchestrator changes, leaderboard/scorecard
> changes, text import, boundary corpus records, or T327G work.

> **T330 canonical corpus QA (2026-06-09):** Verified T328 PR #33 was merged, commit `8498976` was
> present on `main`, CI validate succeeded, and the working tree had no merge/rebase state before
> starting T330. Added `scripts/qa_canonical_corpus.py` as a read-only corpus-health check over
> existing generated canonical outputs. The QA verifies configured 66-book presence/order,
> excluded-book absence, no `FRT`/`GLO` Scripture content, passage and witness ID integrity,
> passage/witness alignment, non-empty witness text except explicitly listed textual-variant empty
> witnesses, canonical sidecar book identity, glossary non-Scripture handling, and word-token
> canonical identity. Added synthetic tests and conditional
> `validate_all` integration when generated passage/witness files are present. T330 is QA/reporting
> only: no raw/canonical mutation, generated output regeneration, chunk regeneration, evaluator
> formula change, chunker/orchestrator behavior change, leaderboard/scorecard change, boundary
> import, boundary corpus records, source acquisition, or T327G work occurred.

> **T331 post-T327 chunking backlog reset (2026-06-09):** Verified current `main` includes merged
> T327F PR #32, T328 PR #33, and T330 PR #34, with commits `44da678`, `8498976`, and `5dd3718`
> present, green CI, clean working tree, and no merge/rebase state. Added
> `docs/roadmap/T331_POST_T327_CHUNKING_BACKLOG_RESET.md` as planning/reporting only. The backlog
> reset records the post-T327 canonical corpus baseline (66 books, 31,103 passages, 31,103
> witnesses), the T327D chunk baseline (1,131 chunks, SHA-256
> `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025`, score 93.6 under unchanged
> T314 policy), what T327 fixed, what it did not improve, candidate future chunking areas, and the
> recommended T332-T335 sequence. T331 authorizes no output-changing chunking work, raw/canonical
> mutation, regeneration, evaluator/leaderboard/scorecard change, boundary import, or T327G work.

> **T332 narrow chunking target selection (2026-06-09):** After T331 PR creation and clean `main`
> restoration, added `docs/roadmap/T332_SELECT_NARROW_CHUNKING_TARGET.md` as planning/reporting
> only. Selected **Psalms / poetry stanza behavior** as the single next chunking target because the
> repo already has the strongest local evidence base there: Psalm gold manifest coverage, reviewed
> Ps.78 parent/child structural split, reviewed Ps.105/Ps.106 whole-psalm preservation, Psalm 119
> sectioning precedent, stress/observed Psalm cases, and an existing behavior-preserving candidate
> Psalm skill seam. T332 rejects broader wisdom, prophetic, narrative, epistle, context-packet,
> stress-atlas, skill-promotion, and gold-only alternatives for now. Future T333 must cite reviewed
> target gold or an explicit human-reviewed review packet before output-changing work. T332 made no
> raw/canonical/generated/chunk/evaluator/leaderboard/runtime/boundary import/T327G changes.

> **T328 cross-repo lesson mirror prep (2026-06-09):** After T332 PR creation and clean `main`
> restoration, added `docs/roadmap/T328_CROSS_REPO_LESSON_MIRROR_PREP.md` as planning/reporting
> only. The report prepares future mirror updates for `logos-governance-architecture`,
> `logos-boundary-literature`, and the selected LawFirm/FMG repo. It names the lessons to mirror:
> `WORKFLOW-LESSON-001`, `T327-LESSON-001`, `BOUNDARY-WORKFLOW-LESSON-001`, and
> `LAW-FIRM-WORKFLOW-LESSON-001`; records repo-by-repo mirror needs, prerequisites, and future task
> prompts; and states that governance should eventually be the source of truth with child repos
> mirroring. No other repos were edited, and no raw/canonical/generated/chunk/evaluator/leaderboard/
> runtime/source-import/boundary-import/T327G work occurred.

> **T328B workflow rules registry lessons (2026-06-09):** Added
> `docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md` from the uploaded v0.3 T327 lessons
> artifact and linked it from the workflow lesson collector, chunking methodology, and AI table of
> contents. The registry records `RULE-META-001`, `CHUNK-CANON-001`, T327 corpus-scope rules,
> boundary intake/governance stop rules, `WORKFLOW-EXCEPTION-001`, and LawFirm transfer patterns.
> T327 root-cause lesson: semantic rules are insufficient without deterministic ingest/filter/
> validation architecture; raw source scope must not silently become canonical output scope. T328B
> is docs/control-plane only and authorizes no raw/canonical/generated/chunk/evaluator/runtime/
> scorecard/source-import/boundary-import/T327G work.

> **T333 Psalm stanza narrow improvement (2026-06-09):** Verified PR #37 and PR #38 were merged
> with green CI and started from clean current `main`. Implemented one narrow Psalm/poetry stanza
> guardrail inside the candidate `psalm-whole-then-stanza-v1` skill: the skill still delegates to
> `chunker.chunk_book(...)`, then validates exact reviewed Psalm postconditions when reviewed
> chapters are present. The guardrail cites reviewed Psalm manifest/review-packet evidence for
> Ps.23, Ps.3, short Psalm holdouts, Ps.119, Ps.78, Ps.105, and Ps.106. It fails closed on reviewed
> Psalm drift such as merging Ps.78, splitting Ps.105/Ps.106, or shifting Psalm 119 sections. T333
> does not create new Psalm boundaries, regenerate chunks, change output, change evaluator policy,
> update leaderboard/scorecards, mutate raw/canonical/generated outputs, import source or boundary
> texts, edit chunker/orchestrator, or start T327G.

> Every agent reads this file **after** `ROADMAP_STATE.yaml` and **before** starting work.  
> Read **`.ai/control/MASTER_CONTEXT.md`** first for architecture authority (AI read-only).
> New/lower-level agents: start with `.ai/handoffs/AGENT_ROUTING_GUIDE.md`.

---

## Navigation (always start at the front door)

```text
AI_FRONT_DOOR.md
  -> MASTER_CONTEXT.md  (theory, human-gated, read-only)
  -> PROJECT_STATUS.md  (this file, current state)
  -> DATA_MAP.md        (data + pipeline endpoints, generated)
  -> ROADMAP_STATE.yaml -> handoffs/T###/handoff.md (your task)
```

`AGENT_ROUTING_GUIDE.md` = full step-by-step for any agent.

---

## Control plane (CI enforced)

| Gate | Command | Enforces |
|------|---------|----------|
| All gates | `python scripts/validate_all.py` | repo + control plane + handoffs |
| Master context lock | `validate_control_plane.py` | human-approved SHA256; AI cannot drift master |
| Front-door routing | same | AI_FRONT_DOOR, README, CLAUDE, AGENTS reference master context |
| Handoffs | `validate_handoffs.py` | active tasks have valid handoff sections |
| Tests | `python -m pytest -q` | 9 tests including control plane |

**CI:** `.github/workflows/validate.yml` runs validate_all + pytest on every push/PR.

> Every agent reads this file **after** `ROADMAP_STATE.yaml` and **before** starting work.  
> Read **`.ai/control/MASTER_CONTEXT.md`** first for architecture authority (AI read-only).

---

## Authority files

| File | Role |
|------|------|
| [`.ai/control/MASTER_CONTEXT.md`](MASTER_CONTEXT.md) | Human-gated design theory — AI must not edit |
| This file | Operational status — agents update after tasks |
| [`.ai/handoffs/T301/handoff.md`](../handoffs/T301/handoff.md) | Active sprint queue |

---

## Executive verdict (T302)

| Layer | Grade |
|-------|-------|
| Architecture docs | **A** |
| Ingest pipeline | **A-** |
| Chunking design | **A** |
| Chunking implementation | **F** |
| CI / testing | **D / D+** |
| Release readiness | **F** |

**Ingest complete. Phase 3 not ready until P0 blockers cleared.**

Full review: `.ai/handoffs/T302/handoff.md`

---

## Current phase

| Field | Value |
|-------|-------|
| Phase | **phase_7** — Cross-reference and intertextual graph (T308 run 1 active alongside phase_3 chunking work) |
| Ingest | **COMPLETE** ✓ |
| T302 review | **COMPLETE** ✓ |
| Connection discovery | **RUN 1 EMITTED** — 500 candidate-only edges under `data/candidate/connections/`; no promotion |
| Next | Human runs additional A/B agents, then compares agreement/disagreement for adjudication |

## T308 connection discovery status (2026-06-05)

- Codex 5.5 run 1 emitted `data/candidate/connections/codex-5.5-2026-06-05.jsonl` plus manifest/report.
- Comparison harness ran against `data/candidate/connections/2026-06-04-ab-review.jsonl`; current overlap is 0 agreement triples and 508 disagreement triples.
- All emitted edges are candidate-only (`assertion_mode=status=trust_zone=candidate`) and remain outside canonical promotion.

---

## Blocker status (resolved in T305 unless noted)

| ID | Issue | Status |
|----|-------|--------|
| GIT-1 | Zero git commits | **RESOLVED** — repo is its own git root; first commit made; generated data gitignored |
| CHK-4 | Chunker crashed on passage shape | **RESOLVED** — chunker joins passages+witnesses; smoke tests added; 0 USFM leaks |
| CANON-1 | Passages lacked CanonProfile | **RESOLVED** — importer emits `canon_profiles`+`testament`; 38,058/38,058 covered; ADR-0005; `--require-canon` gate |
| MODEL-GAP | Missing TextSpan/ContextPacket schemas | **RESOLVED (contracts)** — `schemas/text_span.schema.json`, `schemas/context_packet.schema.json` added (generators are Sprint 3) |
| CP-1 | Master-context gate locally bypassable | **PARTIAL** — `approved_commit` + tamper-evidence docs + CODEOWNERS entries (ADR-0009); **human must enable branch protection** |
| CP-2 | Active-task handoff regex fails open | **RESOLVED** — structural PyYAML parser, fail-closed |
| CI-GAP | JSONL/manifest/chunker ungated | **RESOLVED** — `validate_all` + workflow now gate manifest, JSONL+canon, schemas, chunker, DATA_MAP freshness, raw tripwire, pytest |
| GOV-STALE | T000/T001 stale in_progress | **RESOLVED** (T304) — closed; phase_0 complete |
| PRED-GAP | No predicate registry | **RESOLVED (stub)** — `config/governance/predicate_registry.yaml` |
| PROV-1 | Inline SHA256 dup | **DEFERRED** — ADR-0007 accepted-direction; migration is its own task |
| LIC-GAP | No LICENSE / CODEOWNERS placeholder | **RESOLVED** — root `LICENSE` (MIT); CODEOWNERS has real entries (handle still `@owner` to set) |

**Post-T305 state:** all gates green (`validate_all` 5 gates + 11 pytest). Phase 3 chunker is
un-broken (v0 join); boundary-driven chunker + TextSpan generator + gold set remain (Sprint 3).
Reviews: `.ai/handoffs/T304/handoff.md` (findings) → `.ai/handoffs/T305/handoff.md` (remediation).

---

## Sprint plan (from T302 review)

### Sprint 1 — Codex (start now)

1. Fix chunker (passages + witnesses join)
2. Extend CI (pytest, validate_jsonl, validate_manifest)
3. `.gitignore` + first commit
4. Fix INGESTION_WORKFLOW.md drift
5. force_handoff.py fixes

### Sprint 2 — Claude (after 4a)

1. ADR-0005 CanonProfile
2. TextSpan + ContextPacket schemas
3. `config/chunking/book_genres.yaml`

### Sprint 3 — Pair

1. TextSpan generator
2. Boundary-driven chunker v0
3. Gold set (Ps 23, Rom 7-8, John 1)

---

## Validation baseline

manifest ✓ | JSONL 864,904 ✓ | pytest 5/5 ✓ | chunker ✗

---

## Active handoffs

1. **`.ai/handoffs/T301/handoff.md`** — Codex/Claude task queue (Sprint 1-3)
2. **`.ai/handoffs/T302/handoff.md`** — Full senior review (complete)
3. `.ai/handoffs/T201/handoff.md` — Ingest deliverables

---

## Agent routing

| Agent | Scope |
|-------|-------|
| **Codex** | Sprint 1 mechanical work only |
| **Claude** | Sprint 2 ADRs + schemas (after chunker fix) |
| **Lower-tier** | Subtasks in T301 only; no architecture |

---

## Update rules

When finishing work, update: this file → task handoff → ROADMAP_STATE.yaml → current_focus.yaml → roadmap_events.jsonl
