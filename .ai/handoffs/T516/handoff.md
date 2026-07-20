# Task Handoff

## Task

- task_id: T516
- title: CSNTM 1,908-record rights-gated NAS acquisition campaign specification
- phase: phase_5
- status: authorized_subset_complete_verified_blanket_campaign_blocked

## Agent

- agent_name: Codex
- mode: plan
- stage: final
- updated_at: 2026-07-18

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/coding_runtime_language_preflight.yaml
- Z:\AI_FRONT_DOOR.md
- Z:\AI_TABLE_OF_CONTENTS.md
- Z:\00-Governance\WORKSPACE_MANIFEST.yml
- Z:\00-Governance\AI_WORKSPACE_ARCHITECTURE.md
- Z:\00-Governance\PRIVATE_AND_BACKUP_BOUNDARY.md
- Z:\01-Projects\Logos\AI_FRONT_DOOR.md
- Z:\01-Projects\Logos\AI_TABLE_OF_CONTENTS.md
- T479 task, roadmap, and NAS layout
- CSNTM Terms of Use & Copyright
- CSNTM Collaboration statement
- orchestrate-long-run-campaigns and portable-capability-governance skill contracts

## Files changed

- .ai/tasks/T516.task.yaml
- .ai/campaigns/T516/campaign.json
- .ai/campaigns/T516/campaign.md
- .ai/campaigns/T516/jobs/README.md
- .ai/campaigns/T516/checks/README.md
- .ai/campaigns/T516/state/README.md
- .ai/campaigns/T516/handoff.md
- docs/roadmap/T516_CSNTM_RIGHTS_GATED_ACQUISITION.md
- .ai/handoffs/T516/handoff.md
- .ai/control/handoff_ledger.jsonl

## Decisions made

- Verified that the current CSNTM collection reports 1,908 records on 2026-07-18.
- Did not crawl, copy metadata records, call private APIs, bypass viewer safeguards, download images, or write to the NAS.
- Classified blanket CSNTM acquisition as unauthorized because CSNTM requires individual permission from CSNTM and each holder and does not expressly permit bulk catalog copying.
- Designed a four-job sequence: bind permission; inventory metadata; acquire rights-cleared images; independently reconcile all IDs and residual permissions.
- Chose Python governance/controller orchestration with a future Rust streaming checksum worker because the execution would exceed the repository's heavy-data thresholds.
- Kept execution.mode specification_only and all launch evidence not-authorized.

## Validation run

- command: python C:\Users\lowel\.codex\skills\orchestrate-long-run-campaigns\scripts\validate_campaign.py .ai\campaigns\T516\campaign.json
- result: PASS — valid long_run_campaign.v2 static specification; no execution authorization
- command: python scripts\validate_task_scope.py --task-id T516
- result: PASS
- command: python scripts\agent\validate_handoffs.py
- result: PASS — 130 referenced handoffs
- command: python scripts\validate_parallel_execution_safety.py --task-id T516 --allow-current-task-dirty --require-task-branch
- result: PASS after explicitly staging only T516-scoped paths so Git reported individual untracked paths
- command: git diff --cached --check
- result: PASS with CRLF normalization warning for the handoff ledger
- command: python scripts\validate_all.py
- result: PARTIAL FAIL after 593.8 seconds — repository and T516 gates passed; unrelated T439 validator could not find ignored generated data/canonical/translations/eng-web/word_tokens.jsonl. The initial parallel-safety failure caused by collapsed untracked directory reporting was fixed and the focused gate then passed.
- command: python -m pytest -q --basetemp=C:\tmp\logos-t516-csntm-campaign\.pytest-tmp
- result: TIMEOUT after 1,204 seconds with no assertion output or pytest verdict; classified as runtime/tool timeout per test_runtime_preflight, not pass or code failure

## Authorized subset completion

- CSNTM reply bound: 2026-07-16.
- Completed on: 2026-07-18.
- Scope: P45 and P46 at Chester Beatty Dublin; P66 fragment 2 at Chester Beatty Dublin; P66 fragment 1 at Cologne.
- NAS result: 77 object records, 156 JPEGs, 310,855,141 image bytes, 156 unique SHA-256 hashes, one 12,524-byte Cologne TEI/EpiDoc export.
- Verification: 156 manifest rows; 156 NAS image files; 156 unique NAS hashes; zero promotion conflicts; no overwrites or deletions.
- Rights: preserve CC BY 4.0 attribution. Chester line: CC BY 4.0, Chester Beatty Library, Dublin. Cologne attribution and official object permalink are recorded in the rights ledger.
- Metadata: exact Chester METS, MARC XML, Dublin Core, IIIF, PDF, and OPAC endpoints are recorded. Raw Chester exports were not copied because a direct request returned the anti-bot interstitial; no bypass was attempted. Cologne TEI/EpiDoc was downloaded through the official export.
- Excluded: P75; all other CSNTM records; OCR, transcription, AI analysis, embeddings, vectors, redistribution, and publication.
- Authoritative catalog: \\UNAS-Pro\AI.Workspace\01-Projects\Logos\manuscript-witnesses\catalog\T516\.
- Follow-up: an unsent draft asking CSNTM for a machine-readable public-domain/Creative-Commons holdings list is stored in the catalog.
## Known risks

- CSNTM terms may change; bind an observed revision/hash at launch.
- The 1,908 count is a live snapshot and may change before permission is granted.
- Total image volume is unknown and could exceed the provisional 5 TiB campaign ceiling.
- Holding-institution terms vary by object; silence cannot be treated as permission.
- Same-NAS storage is not an independent backup.
- DAD deterministic portability preflight was unavailable; status remains unverified_without_deterministic_harness until implementation and qualification.

## Open questions

- Will CSNTM provide a licensed machine-readable export or supported bulk API?
- Will CSNTM identify which image sets it can authorize and provide holder contacts for the rest?
- What rate, concurrency, attribution, AI-analysis, vectorization, redistribution, and commercial-use conditions will each grant impose?

## Exact next action

Review and approve the unsent CSNTM follow-up draft requesting a machine-readable list of public-domain and Creative Commons image sets. The blanket 1,908-record campaign remains fail-closed until a supported rights manifest or new item-level grants are received.