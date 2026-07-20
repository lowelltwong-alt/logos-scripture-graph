# Cursor Prompt: Rights-Gated Codex Image and Metadata Acquisition to Z:

## How to use

Paste everything from **BEGIN CURSOR PROMPT** through **END CURSOR PROMPT** into Cursor Agent mode at the root of `logos-scripture-graph-repo`. Allow it to run and monitor terminal commands. This is an execution prompt, not a planning prompt.

---

## BEGIN CURSOR PROMPT

You are the implementation and acquisition agent for the Logos / Scripture Graph repository family. Work persistently for as long as needed, up to **20 elapsed hours**, to complete the authorized acquisition below. Do not stop after writing a plan or a downloader. Build the governed, resumable acquisition tooling; execute it; monitor it; recover safely from transient failures; verify every result; and leave an exact checkpoint and resume command if the 20-hour ceiling is reached before completion.

### 1. Owner authorization and exact boundary

Lowell Wong authorizes this execution to:

1. Download and preserve **all distinct full-resolution digital images and associated IIIF/catalog metadata for the Leipzig University Library-held and Leipzig-digitized portions of Codex Sinaiticus** covered by the library's written permission.
2. Create a factual, source-cited metadata catalog for all other codices/manuscript witnesses already named in the repository's acquisition and research control files.
3. Download images from an additional source only when an existing, source-specific rights record supplies all of the following: an exact object/file or collection scope, an authoritative rights or license URL, an affirmative local-storage/download right, an affirmative commercial-use status or public-domain/CC0 status, and enough provenance to tie the right to the exact files. Lowell's instruction here authorizes acquisition of rows that pass that complete gate.

The confirmed permission basis for the immediate image acquisition is the 2026-07-15 email from Annika Schröer at Leipzig University Library stating that all digital images of the Leipzig-held Codex Sinaiticus parts digitized by Leipzig University Library are PDM 1.0 and may be used in any way. The official object and IIIF endpoints are:

- Object viewer: `https://digital.ub.uni-leipzig.de/object/viewid/0000061851`
- IIIF manifest: `https://iiif.ub.uni-leipzig.de/0000061851/manifest.json`
- Rights mark: `https://creativecommons.org/publicdomain/mark/1.0/`

This authorization **does not extend** to British Library, Vatican Library, St. Catherine's Monastery, Russian National Library, or shared Codex Sinaiticus project images merely because they depict the same codex. It also does not convert an old planning row, a public viewer, an accessible URL, or the absence of a login into download permission.

Do not ask Lowell again for permission to acquire the Leipzig-held/digitized set. Do stop before acquiring any other image set whose exact affirmative rights evidence is missing or ambiguous. Catalog its metadata and mark it `permission_required` instead.

### 2. Non-authorizations

Do not perform OCR, handwriting recognition, transcription, translation, text extraction, image enhancement, embeddings, vectorization, indexing, model training, preferred-reading selection, textual-critical adjudication, canon changes, Scripture authority changes, graph/retrieval truth promotion, public release, publication, or redistribution. Do not download books or text corpora as a side effect. Do not access personal, client, student-account, or private-email content. Do not send email.

Metadata may report what a holding institution or catalog says, with source and observation date. It may not make apologetic, theological, authenticity, date, authorship, or textual conclusions beyond the cited catalog evidence.

### 3. Mandatory reading and clean execution setup

Before changing or downloading anything, read in this order:

1. `AI_FRONT_DOOR.md`
2. `.ai/control/MASTER_CONTEXT.md` (read only; never edit)
3. `.ai/control/PROJECT_STATUS.md`
4. `.ai/control/DATA_MAP.md` if present, otherwise the front-door route to the current data map
5. `.ai/control/primary_witness_acquisition_waves.yaml`
6. `.ai/control/leipzig_sinaiticus_split_corpus_plan.yaml`
7. `.ai/control/manuscript_source_catalog_research_packet.yaml`
8. `data/raw/primary_witnesses/greek_codices/codex_sinaiticus/leipzig/0000061851/showcase/source_manifest.yaml`
9. `docs/roadmap/T469_PRIMARY_WITNESS_ACQUISITION_WAVES.md` if present
10. `docs/roadmap/T471_LEIPZIG_SINAITICUS_SPLIT_CORPUS_START_PLAN.md` if present
11. `.ai/handoffs/T472/handoff.md`
12. `docs/roadmap/T477_UNAS_AI_WORKSPACE_ARCHITECTURE.md`
13. `Z:\AI_FRONT_DOOR.md`
14. `Z:\AI_TABLE_OF_CONTENTS.md`
15. `Z:\00-Governance\WORKSPACE_MANIFEST.yml`
16. `Z:\00-Governance\STORAGE_POLICY.md`
17. `Z:\01-Projects\Logos\AI_FRONT_DOOR.md`

The current repository/worktree may contain unrelated user changes. Never overwrite, reset, clean, stash, stage, or commit them. Create a new clean isolated Git worktree and a branch named with the required `codex/` prefix for all repository-side code, task, control, receipt, and handoff changes. Allocate a new unused task ID at execution time; do not reuse T478, which owns this prompt. Run the required forced-handoff start step before material implementation and the final step when complete.

Search the DAD asset/skill library for a narrower existing governed acquisition/downloader asset before creating reusable tooling. Reuse it only if its provenance, rights behavior, storage contract, and current revision are applicable. Never send raw source artifacts, private messages, secrets, or source rows to DAD.

### 4. Verify Z: before any write

`Z:` is expected to be a mapped drive whose `DisplayRoot` is exactly `\\UNAS-Pro\AI.Workspace`. Before any write:

1. Resolve the mapping using PowerShell (`Get-PSDrive -Name Z`) and resolve the UNC destination.
2. Require the normalized mapping to equal `\\UNAS-Pro\AI.Workspace`.
3. Read the NAS front-door and Logos front-door files.
4. Confirm the free-space figure and require at least **500 GiB to remain free after the conservative projected transfer**.
5. Write and delete only a uniquely named zero-byte probe inside the new task's `staging` directory to prove authorized write access. Do not probe `source-originals` directly.

If Z: is absent, maps elsewhere, the front doors cannot be read, the reserve would be breached, or the write probe fails, stop with evidence. Do not silently substitute a local disk, OneDrive, another NAS share, or a private/backup share.

### 5. Authoritative storage layout

Large images and remote metadata payloads belong only on the NAS. The local Git worktree holds code, schemas, compact manifests, reports, and checksums—never the acquired images.

Use these roots:

```text
Z:\01-Projects\Logos\source-originals\manuscript-witnesses\greek_codices\codex_sinaiticus\leipzig\0000061851\
  iiif\manifest.json
  iiif\info\
  images\

Z:\01-Projects\Logos\manuscript-witnesses\catalog\
Z:\01-Projects\Logos\manifests\logos-scripture-graph\codices\
Z:\01-Projects\Logos\provenance\logos-scripture-graph\codices\
Z:\01-Projects\Logos\staging\<new-task-id>\
Z:\01-Projects\Logos\quarantine\<new-task-id>\
Z:\08-AI-Operations\manifests\<new-task-id>\
Z:\08-AI-Operations\handoffs\<new-task-id>\
```

Treat `source-originals` as immutable. Never overwrite or delete a source original. Domain folders hold normalized catalog/reference records and must not duplicate image binaries. Staging contains `.part` files, temporary responses, and resumable state. Quarantine contains only collisions or files that fail validation. Do not write to `Z:\05-Releases-and-Exports`, `Z:\Personal-Drive`, `Z:\ComputerBackups`, or any local `data/raw`, generated-data, build, release, publication, or OneDrive binary path.

If the NAS front door specifies a stricter compatible path, follow it and document the resolved path. If it conflicts materially with this authorized layout, stop rather than inventing a new authority.

### 6. Build a resumable acquisition program

Implement a small provider-neutral acquisition core with a thin Cursor/PowerShell invocation adapter. Prefer Python standard-library networking and hashing unless the repository already has an approved dependency. The program must support inventory-only, acquire, verify, status, and resume modes. It must be deterministic from the captured manifest and rights ledger.

Required safety behavior:

- Capture the IIIF manifest exactly once per run, retain its exact bytes, compute SHA-256, and use that immutable captured copy as the run input.
- Parse the manifest rather than hard-coding the expected canvas count. Record any difference from the previously observed 43 leaves / 86 canvases as manifest drift requiring review.
- Inventory every canvas, annotation/resource, image service, direct image URL, and distinct capture variant.
- Fetch and preserve each image service's `info.json` when available.
- Acquire one highest-resolution source representation for every distinct physical capture exposed by the authorized manifest. Include normal and raking-light or other genuinely distinct captures when separately represented.
- Do **not** download every thumbnail, tile, or size/format derivative. A resized rendition of the same capture is not another source artifact.
- Use the capabilities stated by each IIIF service. Do not assume one Image API version or invent URL syntax.
- Use bounded concurrency respectful of the library server (default 2 simultaneous image transfers), an identifying user agent naming the Logos research acquisition and a contact address already approved in local project metadata, exponential backoff with jitter for 429/5xx/network errors, and a conservative request rate.
- Stream downloads to uniquely named `.part` files in task staging; never buffer a whole image in memory.
- Resume with HTTP range requests only when the server and immutable identity evidence support it. Otherwise restart that one staging file without touching validated originals.
- Validate final HTTP status, resolved URL, content type, declared length when supplied, actual byte count, decodability/file signature without altering pixels, and SHA-256.
- Promote from staging to `source-originals` only by an atomic same-volume move after validation and receipt preparation.
- Before promotion, if the destination exists, hash it. If identical, record `already_present_identical` and skip. If different, move the new candidate to quarantine and stop that item with `destination_collision`; never overwrite.
- Deduplicate exact binary duplicates by SHA-256 while preserving every canvas/resource/capture reference in the inventory. Prefer one physical source binary plus catalog references where the NAS filesystem and policy allow it; never use risky cross-volume links.
- Persist machine-readable progress after each completed item and at least every 15 minutes. A crash, Cursor restart, network interruption, or machine reboot must not lose completed-item evidence.
- Never place access tokens, cookies, credentials, email bodies, or private data in logs or manifests.

### 7. Rights-gated source queue

Create a machine-readable rights ledger before image transfer. Each source row must include:

```text
source_id
holding_institution
object_id_or_shelfmark
exact_scope
official_object_url
official_manifest_or_api_url
rights_statement
rights_url
rights_evidence_type
rights_evidence_date
local_storage_allowed
image_download_authorized
commercial_use_status
redistribution_status
attribution_or_courtesy_terms
owner_authorization_reference
decision: acquire | metadata_only | blocked
decision_reason
```

Set the Leipzig row to `acquire` using the confirmed permission and PDM 1.0 evidence. Treat the earlier T472 three-image showcase limit as the scope of that old task, not as a revocation of Lowell's later authorization for this new execution. Preserve T472 unchanged and create a new acquisition receipt.

For candidate sources in `primary_witness_acquisition_waves.yaml`—including Leningrad Codex, Codex Sassoon 1053, British Library Or. 4445, Swete Septuagint, the 1592 Vulgate, Aleppo Codex, Cairo Codex, Codex Amiatinus, Vaticanus, Alexandrinus, papyri, Dead Sea Scrolls, or any other tracked witness—perform a fresh exact rights check against the authoritative item/file record already cited by the repository. A planning label such as `PDM candidate`, Internet Archive accessibility, or public visibility is insufficient by itself. Acquire only rows with the complete affirmative gate in section 1; otherwise create metadata-only rows and a permission/review queue.

Do not broaden a collection-level license to unrelated files or institutions. Do not use a student login to bypass terms or acquire restricted files.

### 8. Codex and witness metadata catalog

For the Leipzig set and every other witness already named in the local acquisition/research controls, create normalized metadata using official catalogs/APIs first. Metadata-only work may continue even when images are blocked. Record unknown values as null/unknown; do not guess.

At minimum capture, when officially available:

```text
witness_id
preferred_name
alternate_names
shelfmark_or_inventory_number
holding_institution
holding_location
repository_object_id
official_catalog_url
manifest_or_api_url
material
physical_format
language_or_script
catalog_date_or_date_range
catalog_provenance_or_origin
dimensions
folios_leaves_pages
columns_and_lines
contents_summary_as_cataloged
known_lacunae_or_completeness_as_cataloged
capture_types
canvas_count
image_resource_count
rights_state
rights_url
access_state
local_storage_state
attribution_terms
metadata_source_url
metadata_observed_at
field_level_source_or_evidence
confidence
notes
```

For Leipzig canvas coverage, use only metadata and official labels/ranges to classify each canvas/resource as one of:

- `canonical_66`
- `boundary_non_66`
- `mixed_or_uncertain`
- `non_text_artifact`

Do not infer a book, passage, or category solely from looking at pixels. Route ambiguous or mixed canvases to human review. Keep all deuterocanonical/apocryphal and other non-66 material outside default Scripture authority and default retrieval. Catalog it as boundary/supporting material for a later separately governed route; do not import it into `logos-scripture-graph` canonical data.

### 9. Required evidence artifacts

Create compact, parseable records on the NAS and mirror only appropriately small non-sensitive control/report files into the clean Git worktree where task scope permits:

1. Exact captured IIIF manifest and its SHA-256.
2. One preserved `info.json` per distinct image service, with hashes.
3. `source_inventory.jsonl`—one row per remote image resource/capture.
4. `canvas_resource_map.jsonl`—all canvas-to-resource-to-local-object mappings.
5. `codex_catalog.jsonl`—normalized metadata rows with field-level source evidence.
6. `rights_ledger.yaml`—all acquire/metadata-only/blocked decisions.
7. `SHA256SUMS`—every acquired source binary and preserved remote metadata payload.
8. `acquisition_receipt.json`—run ID, task ID, tool revision, start/end time, manifest hash, counts, bytes, paths, and outcomes.
9. `transfer_events.jsonl`—append-only non-secret item events with timestamps, URLs, ETag/Last-Modified when supplied, byte counts, hashes, retries, and results.
10. `collision_and_failure_report.jsonl`—all mismatches, validation failures, blocked items, and retry exhaustion.
11. `residual_report.json`—proof that every resource in the captured manifest is acquired, identically pre-existing, intentionally deduplicated, metadata-only, blocked, or failed with an exact reason.
12. `storage_ledger.json`—source-original, catalog, manifest, provenance, staging, and quarantine paths plus total bytes and free-space before/after.
13. A human-readable handoff with exact resume and verify commands.

Each acquired file record must include the official manifest ID, canvas ID/label, annotation/resource ID, image service ID, requested URL, final URL, retrieval timestamp in UTC, HTTP status, content type, byte count, ETag/Last-Modified if supplied, local relative path, SHA-256, rights ledger row, and attribution/courtesy terms.

Use stable, collision-resistant filenames derived from canvas/capture identifiers, not untrusted labels alone. Preserve original extensions only when consistent with validated media type.

### 10. Monitoring and the 20-hour ceiling

Once inventory, rights gating, and a dry-run pass, start acquisition and keep it running. Monitor real progress; do not repeatedly rerun unchanged expensive commands. Emit a compact heartbeat to the task log every 15 minutes containing completed/total captures, verified bytes, active item, retry count, last error, current free space, and estimated remaining time.

Continue through transient errors using the bounded retry policy. Re-run only failed or missing items, never the entire completed set. After each interruption, run `status`, then `resume`, then a residual verification.

At 19 hours 30 minutes, stop beginning large new transfers unless they are expected to finish safely before 20 hours. At 20 hours, terminate gracefully, flush receipts, verify all completed artifacts, and report `incomplete_resumable` with the exact remaining count and one exact resume command. Do not claim success unless residuals are zero except explicitly rights-blocked/metadata-only rows.

### 11. Stop conditions

Stop the affected item or the full run, as appropriate, and report evidence for:

- rights scope ambiguity or a source outside the exact approved institution/object;
- Z: mapping mismatch or unavailable NAS front door;
- projected free space below the 500 GiB reserve;
- captured manifest mutation/drift during the run;
- persistent 429/rate-limit or a robots/terms prohibition;
- checksum, length, media-signature, or destination collision mismatch;
- a request for credentials, login bypass, or restricted/private data;
- any proposed overwrite/delete;
- any attempt to mix non-66 boundary material into default Scripture authority;
- any attempt to publish, redistribute, OCR, transcribe, embed, index, or promote source content.

Do not solve a stop condition by weakening the gate.

### 12. Validation and completion

Before reporting completion:

1. Parse every JSON, JSONL, and YAML artifact.
2. Re-hash every promoted source original and preserved metadata payload and compare with `SHA256SUMS`.
3. Prove every captured manifest resource is represented in the residual report.
4. Prove no acquired binary was added beneath the Git worktree, OneDrive, local `data/raw`, generated-data roots, release/publication paths, personal share, or computer-backup share.
5. Prove no destination was overwritten and list all identical skips/deduplications/collisions.
6. Prove canonical/boundary classification did not create Scripture authority or imports.
7. Run the task-scope validator for only the new task's repository-side changes, `python scripts/agent/validate_handoffs.py`, `git diff --check`, targeted acquisition tests, then the repository-required `python scripts/validate_all.py` and `python -m pytest -q`. If unrelated pre-existing failures exist, distinguish them with evidence.
8. Run the forced-handoff final step.

The final report must state:

- elapsed time;
- manifest hash and observed canvas/resource/capture counts;
- acquired, identical-existing, deduplicated, metadata-only, blocked, failed, and remaining counts;
- verified bytes and Z: free space before/after;
- all authoritative storage paths;
- every rights basis used and its exact scope;
- every collision/error and disposition;
- whether completion is `complete_verified` or `incomplete_resumable`;
- the exact `status`, `verify`, and `resume` commands;
- the next human decision, if any.

Begin now. Planning alone is not completion.

## END CURSOR PROMPT
