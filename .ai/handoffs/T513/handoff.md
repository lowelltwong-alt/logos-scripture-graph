# Task Handoff

## Task

- task_id: T513
- title: Portable OCR research adoption for Logos
- phase: phase_4
- status: complete_candidate_foundation_only

## Agent

- agent_name: Codex
- mode: architecture_and_tooling
- stage: final
- updated_at: 2026-07-16

## Scope and authority

This task may add a domain-neutral, candidate-only OCR tool and a thin Logos
admission adapter. It may not download or process InduOCR, manuscript images,
Scripture payloads, or any tracked truth-bearing data. It may not change
Scripture Graph, retrieval, vector, preferred-reading, or theological authority.

InduOCR is being evaluated only as an externally provisioned research stress
benchmark. Its dataset rights are unresolved, and it has not demonstrated
Greek, Hebrew, Aramaic, Latin, critical-apparatus, marginalia, or verse-alignment
fitness.

## Starting evidence

- DAD preflight trace: `dad:trace:cb9c5d2d-e688-53ec-a75c-8e846d85813a`
- Source candidate: Albert modular OCR package on branch
  `codex/modular-ocr-system`; adoption will be content-hash recorded and will not
  claim commit-pinned provenance for uncommitted source work.
- Current Logos source-rights controls expressly withhold `OCR_now`.
- No repository payload directory is authorized for OCR inputs or outputs.

## Files read

- Repository front door, master context (read-only), status, roadmap, data map,
  task ledger, runtime preflight, source-rights readiness, and agent policies.
- Albert's uncommitted modular OCR candidate, read-only as porting evidence.
- Official InduOCRBench repository, ACL paper, Hugging Face dataset record, and
  OmniDocBench evaluator repository through bounded research.

## Files changed

- Added T513 task, handoff, roadmap, policy, portable OCR core, disabled
  InduOCR profile, Logos preliminary admission adapter, synthetic fixtures,
  focused tests, and validator.
- Updated project status, roadmap state/events, task ledger, AI TOCs, Data Map
  endpoint declaration/generator, aggregate validation registration, and lesson
  index LSN-068.
- No file under `data/raw/`, `data/canonical/`, `data/processed/`,
  `data/derived/`, graph, retrieval, vector, chunking, governance, master
  context, or GitHub workflow paths changed.

## Decisions made

- Ported the OCR package as provider- and domain-neutral `portable-ocr`; Logos
  integration remains a thin host-owned boundary.
- Registered InduOCR only as a disabled, external, no-download, no-training
  generic stress benchmark because dataset rights are unresolved and biblical
  script/manuscript fitness is unproven.
- Kept the Logos adapter preliminary and metadata-only. It cannot grant payload
  access or execution even if future feature flags are enabled.
- Required a later execution-boundary verifier, structured rights evidence,
  exact revision and hash inventory, independently attested engines, and a
  separate owner gate.
- Revalidated source, candidate, and comparison evidence before review and
  handoff; preserved Unicode base/mark association and high-consequence Hebrew
  punctuation.

## Validation run

- Portable core plus Logos focused suite: 21 passed.
- `python scripts/validate_t513_portable_ocr_adoption.py`: passed (24 files,
  15 source-provenance hashes).
- `python scripts/validate_task_scope.py --task-id T513`: passed.
- `python scripts/validate_chunking_lesson_index.py`: passed.
- `git diff --check`: passed (line-ending warnings only).
- Independent read-only checker: technical PASS after adversarial repair; source
  and candidate tampering fail closed, Unicode relocation routes Engine C, and
  simulated future policy activation grants no payload/execution authority.
- `python scripts/validate_all.py`: T513 and all relevant gates passed. The
  aggregate remained red only for the then-incomplete T513 handoff/lesson index
  (both repaired afterward) and inherited T439 failure caused by absent clean-
  worktree generated `word_tokens.jsonl`. The 138-second run was not repeated
  unchanged under the redundant-work rule.
- DAD privacy-safe postflight completed: handoff
  `dad:handoff:defa0a4c-8265-5504-97e0-9c97f320447a`; reusable lesson
  `dad:lesson:15b793c8-cb5b-5be5-bc4f-15510a2b56f1`.

## Known risks

- No InduOCR or biblical-manuscript payload has been tested. The dataset license
  is unresolved, and InduOCR cannot establish domain fitness.
- The execution-boundary verifier and authorized biblical domain-gold set do
  not exist yet; this foundation must remain inactive.
- Windows Media OCR and Tesseract are available adapters, not approved engine
  installations for this repository. Engine/model/license hashes remain host
  responsibilities.
- Clean-worktree aggregate validation retains the inherited T439 generated-
  sidecar dependency described above.

## Open questions

- Who will approve or reject InduOCR's ambiguous dataset rights and the exact
  allowed academic-research use?
- Which rights-cleared Greek/Hebrew/Aramaic/Latin manuscript pages and human
  transcriptions will form the separate domain-gold set?
- Which two independent engine families, and optional third engine, will be
  pinned for the first authorized external smoke?

## Next agent instruction

Do not activate or run data. First obtain the InduOCR rights decision. Then
open a separate task to implement the execution-boundary verifier and a tiny,
externally provisioned category-stratified smoke. In parallel, design the
rights-cleared biblical-manuscript domain-gold set; passing InduOCR alone is
never sufficient.

---

## Handoff refresh: start

- agent_name: Codex
- mode: 
- updated_at: 2026-07-17T00:49:54+00:00
- handoff_id: 5d9cad54a249ad51

---

## Handoff refresh: final

- agent_name: Codex
- mode: 
- updated_at: 2026-07-17T01:09:16+00:00
- handoff_id: ed187566818ffb9a
