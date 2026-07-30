# M7_sol 22-book corrective-review checkpoint

## Transfer status

**Not yet backed up or merged.** The intended corpus is frozen locally as Git tree `1dfc563b62e1efea89cfe39d9378fa19ddf74b94`: 1,007 changed files, 163,969,083 bytes, largest file 3,897,024 bytes. The remote branch currently contains only this scope declaration and the T564 handoff because the execution runtime blocks terminal Git transport through `127.0.0.1:9`; the GitHub connector cannot ingest a local Git pack or local file references. Do not merge this scope-only branch.

## Purpose and authority boundary

This is the declared scope for a backup-only, candidate-only checkpoint of the 22 books whose corrective rereview is recorded as complete in `model_manifest.yaml` on 2026-07-30:

`Gen, Exod, Lev, Ps, Prov, Isa, Jer, Ezek, Dan, Hos, Joel, Amos, Obad, Jonah, Mic, Nah, Hab, Zeph, Hag, Zech, Mal, Job`.

It is not a complete whole-Bible result, reviewed gold, an external-review receipt, a canonical or theological ruling, a route/graph promotion, or a claim that T521/B01 is ready. Ecclesiastes is actively in progress and is deliberately absent. Agreement remains evidence, never authority.

The checkpoint is coherent for the listed book-local decisions and review records. It is not a self-contained whole-Bible replay bundle: generated global aggregates and sidecars are intentionally omitted.

## Exact allowlist

Only these paths may be included:

1. For each listed book: `book_chunks/<Book>/**`, `reviews/<Book>/**` subject to the Hosea exclusion below, `_pass1_archive/book_chunks/<Book>/**`, `_pass1_archive/reviews/<Book>/**`, `_pass1_archive/book_strategy/<Book>.md` when present, `book_strategy/<Book>.md`, and book-specific completion receipts in `receipts/`.
2. Shared candidate provenance: `campaign.json`, `campaign.md`, `campaign.rev7.json`, `campaign_prompt.md`, `review_contract.yaml`, `corrective_rereview_contract.v1.yaml`, `model_manifest.yaml`, `runtime/codex_adapter.yaml`, `receipts/preflight.json`, and this file.
3. Campaign handoffs `.ai/handoffs/T544/**` through `T549/**`, `T551/**` through `T562/**`, plus the T564 publication handoff.
4. `.ai/tasks/T521.task.yaml`, `.ai/control/PROJECT_STATUS.md`, `.ai/control/handoff_ledger.jsonl`, `.ai/control/roadmap_events.jsonl`, `ROADMAP_STATE.yaml`, and `docs/roadmap/TASK_LEDGER.md`.
5. Source manifests: `data/raw/bible/eng-web/source_manifest.yaml`, `data/raw/original_language/hebrew/openscriptures_oshb/source_manifest.yaml`, and `data/raw/original_language/hebrew/tanach_us_uxlc/source_manifest.yaml`.

Items 1 and 2 are rooted at `.ai/scratch/multi_model_bible_chunking/M7_sol/`.

## Mandatory exclusions

Exclude Ecclesiastes and all books outside the list; `whole_bible_chunk_map.jsonl`, `low_confidence_register.jsonl`, `atlas_candidate_feed.jsonl`, `frontier_escalation_queue.jsonl`, and `marathon_progress.yaml`; M7 checks/state/jobs/runtime scratch/caches/temp fixtures/test sandboxes; T550 and every rematerialization, live-gate, Windows measurement, static-allowlist, V8/V9, semantic-prose transaction, replacement-gate, or sidecar-install artifact including those under `reviews/Hos/`; M1-M6, comparison, T417, external-review receipts, `.digital-asset/`, unrelated config/scripts/tests/source catalogs, and every other dirty path.

## Source notices

- World English Bible Classic (WEB): public domain, sourced from eBible.org. “World English Bible” is an eBible.org trademark; these derived candidate annotations and excerpts are not represented as an unmodified WEB edition. Source: https://ebible.org/find/details.php?id=eng-web
- Open Scriptures Hebrew Bible (OSHB): Open Scriptures Hebrew Bible Project, based on the Westminster Leningrad Codex, licensed CC BY 4.0. License: https://github.com/openscriptures/morphhb/blob/master/LICENSE.md
- Unicode/XML Leningrad Codex (UXLC): UXLC 2.5 (27.6), Tanach.us Inc., West Redding, CT, USA, Apr 2026. Copying terms: https://tanach.us/License.html

The checkpoint contains derived observations and limited source quotations, not raw source archives.

## Validation and known exceptions

- Exact isolated path gate: PASS; zero mandatory-exclusion paths.
- Ordinary Git size gate: PASS; zero files at or above 50 MiB.
- `git diff-tree --check`: PASS after mechanical trailing-whitespace normalization in 17 handoffs.
- High-confidence secret scan: PASS; zero path hits.
- Applicable book-local checks: 82 PASS/reused PASS out of 85 probes.
- Hosea and Job literary-quality failures are only the intentionally omitted stale global sidecars, which Lowell ruled non-gating.
- Hosea's corrective-depth command reports three known repeated lane/provenance constructor fingerprints. Independent review found decision-local evidence remains distinct and passed Hosea for candidate-backup inclusion under the owner literary-completion receipt, but the command itself is not green. Do not claim otherwise.

Before any future push, the uploaded GitHub tree must exactly equal `1dfc563b62e1efea89cfe39d9378fa19ddf74b94`. The PR must repeat the candidate-only, 22-book, incomplete-campaign, license, omitted-aggregate, and Hosea-exception disclosures. Merge is permitted only for the exact checked head after the corpus is present.
