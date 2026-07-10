# T469 Primary Bible Witness Acquisition Waves For Cursor

Status: planning-only, non-authorizing
Date: 2026-07-08
Owner: Lowell Wong
Agent: Codex

## Purpose

Give Cursor a concrete, wave-based plan to bring the most important primary and early Bible witnesses into the Logos knowledge base where rights permit. This plan creates no raw downloads, no manuscript image storage, no transcription storage, no source text import, no graph/retrieval/vector truth, no preferred reading, no source-tradition preference, and no theology authority.

The first deliverable is a governed acquisition scaffold. The system should visibly progress from "we know where the source is and what rights apply" to "we can store this text/image locally" only after each source has provenance, license, checksum, and review status.

## Cursor Start Instructions

Cursor must start by reading:

1. `AI_FRONT_DOOR.md`
2. `.ai/control/MASTER_CONTEXT.md` read-only
3. `.ai/control/PROJECT_STATUS.md`
4. `.ai/control/DATA_MAP.md`
5. `.ai/control/RAW_SOURCE_INVENTORY.md`
6. `.ai/control/manuscript_source_catalog_metadata_plan.yaml`
7. `.ai/control/manuscript_source_catalog_research_packet.yaml`
8. `.ai/control/dss_biblical_witness_source_rows.yaml`
9. `.ai/control/primary_witness_acquisition_waves.yaml`
10. this file

Cursor must create a task and handoff for any execution task. The first execution task should be metadata-only unless the owner explicitly authorizes downloads.

## Target Future File Structure

```text
data/candidate/source_catalog/primary_bible_witnesses/
  source_catalog_rows.jsonl
  image_rights_review.yaml
  text_acquisition_review.yaml
  acquisition_manifest.yaml
  storage_ledger.yaml
  blocked_or_permission_needed.yaml

data/raw/primary_witnesses/                  # later only after explicit authorization
  hebrew_masoretic/
    leningrad_codex/
      source_manifest.yaml
      raw/
    codex_sassoon_1053/
    bl_or_4445/
  greek_codices/
    codex_sinaiticus/
    codex_vaticanus/                         # catalog-only until permission
    codex_alexandrinus/                      # catalog-only until rights clear
  greek_papyri/
    p52/
    p45/
    p46/
    p66/
    p75/
  latin/
    codex_amiatinus/
    clementine_vulgate/
  lxx_printed_editions/
    swete_lxx/
```

Do not put files in `data/raw/primary_witnesses/` until the specific execution task authorizes storage and records rights. Metadata-only rows belong in `data/candidate/source_catalog/primary_bible_witnesses/`.

## Wave 0: Catalog And Rights Scaffold

Goal: create the knowledge-base shell with no downloads.

Cursor outputs:

- `source_catalog_rows.jsonl`
- `image_rights_review.yaml`
- `text_acquisition_review.yaml`
- `blocked_or_permission_needed.yaml`
- `storage_ledger.yaml`

Each source row must include:

```yaml
source_id:
title:
witness_family:
scope:
primary_url:
mirror_urls:
image_access: public_domain | open_with_conditions | public_view_only | permission_required | unknown
text_access: already_present | downloadable | transcription_available | ocr_only | unavailable | unknown
license:
can_store_metadata: true
can_store_text: true_or_false
can_store_images: true_or_false
recommended_storage_mode:
estimated_size:
source_priority:
confidence:
review_status:
non_authorizing_scope_label:
next_action:
```

Expected disk use: under 50 MB.

## Wave 1: Text And Transcription First

Goal: bring in or manifest machine-readable text/transcription where rights are open enough or already handled.

Acquire-now or already-present candidates:

- SBLGNT: Greek NT, CC BY 4.0, already represented in this repo's original-language raw/source-view lane.
- OSHB/WLC: Hebrew Bible, WLC public domain, morphology CC BY 4.0, already represented in this repo.
- Tanach.us UXLC: already represented in this repo.
- UGNT and CNTR: already represented in this repo as original-language evidence sources.
- Clementine Vulgate public-domain text: candidate Latin baseline after source review.
- Swete LXX: public-domain printed Greek OT edition via Internet Archive OCR/full text, useful as a text experiment after cleanup.
- Codex Sinaiticus XML transcription: downloadable XML, but CC BY-NC-SA 3.0, so treat as noncommercial/conditioned and do not mix into unrestricted release artifacts.

Expected new disk use: 100 MB to 1 GB. Most text is small; the headroom is for XML, OCR, manifests, checksums, and cleanup artifacts.

Success gate: every text source is either present, manifest-ready, or blocked with an explicit license reason.

## Wave 2: Cleanest Public-Domain/Open Image Sets

Goal: download only image sets that pass rights review, preferably original files rather than every derivative.

Best candidates:

| Source | Why | Approx Storage |
|---|---|---:|
| Leningrad Codex color images | Complete Hebrew Bible witness; IA marks Public Domain Mark 1.0 | 2.94 GB originals, 5.57 GB with derivatives |
| Codex Sassoon 1053 | Early near-complete Hebrew Bible | 5.22 GB originals, 9.20 GB with derivatives |
| BL Or. 4445 Torah | Early Tiberian Pentateuch witness; IA notes public-domain/CC0 terms | 1.33 GB originals, 3.20 GB with derivatives |
| Swete LXX | Public-domain Greek OT printed edition | 0.14 GB originals, 2.39 GB with derivatives |
| Biblia Sacra Vulgatae 1592 | Public-domain Latin Vulgate printed edition | 0.84 GB originals, 1.73 GB with derivatives |
| Codex Amiatinus | Earliest complete Latin Vulgate manuscript witness | 0.38 GB originals, 0.77 GB with derivatives, rights review required |
| Aleppo Codex | Major Masoretic witness | 2.72 GB originals, 4.10 GB with derivatives, noncommercial/rights review required |
| Codex Cairensis | Early Prophets codex | 0.68 GB total on IA probe, rights unclear |

Storage estimate:

- Without Aleppo/Cairensis: about 10.9 GB originals, or 22.9 GB with IA derivatives.
- With Aleppo/Cairensis after review: about 14.3 GB originals, or 27.6 GB with derivatives.
- Recommended free space: 30 GB minimum, 50 GB comfortable.

Cursor should not run "download everything" blindly. Prefer source archive/original files plus checksums; skip generated derivatives unless they are needed for display or OCR review.

## Wave 3: Important Public-View Or Permission-Needed Sources

Goal: catalog, do not store locally yet.

Sources:

- Great Isaiah Scroll and broader biblical DSS witnesses via Israel Museum and Leon Levy/IAA.
- Codex Vaticanus via DigiVatLib.
- Codex Alexandrinus via British Library.
- P52 via Manchester and CSNTM.
- P45, P46, P66, P75 via CSNTM and holding institutions.
- Codex Sinaiticus images via official project, while XML remains separately conditioned.

Expected local image size now: 0 GB. Store metadata URLs only.

If permissions are later obtained, budget 100 GB to 250 GB for high-resolution codex and papyrus expansion. That number is intentionally conservative because image viewers, IIIF tiles, derivatives, and backup copies can multiply storage.

## Wave 4: Advanced Or Restricted Research Datasets

Goal: route and rights-review before storage.

Candidates:

- BHSA / ETCBC Text-Fabric: powerful Hebrew linguistic data, CC BY-NC 4.0.
- CATSS LXX: valuable LXX morphology/alignment history, but restrictive licensing.
- Peshitta/Syriac resources.
- Samaritan Pentateuch manuscripts.
- Coptic and Syriac early versions.

These should stay catalog-only until license and repo-route decisions are approved.

## Disk Budget Summary

| Build Level | What It Includes | Approx New Disk Use |
|---|---|---:|
| Metadata only | Rows, rights review, manifests, hard questions | < 50 MB |
| Text-first | Open/already-present text, XML, OCR, manifests | 100 MB to 1 GB |
| Public/open image originals | Leningrad, Sassoon, BL Or.4445, Swete, Vulgate, Amiatinus after review | ~11 GB |
| Public/open full IA derivatives | Same, with IA generated derivatives | ~23 GB |
| Broader image set after Aleppo/Cairensis review | Adds Aleppo and Cairensis candidates | ~14 GB originals, ~28 GB with derivatives |
| Future permissioned image expansion | Vaticanus, Alexandrinus, DSS, papyri, Sinaiticus images | 100 GB to 250 GB |

Practical recommendation: reserve 50 GB now. If the project later gets permission or decides to mirror major public-view image sets, reserve a separate 250 GB+ storage area outside the normal git working tree and reference it by manifest.

## Non-Authorizations

This plan does not authorize:

- raw downloads
- image storage
- manuscript transcription storage
- source text import
- canonical Bible text changes
- canonical passage record changes
- textual-critical decisions
- preferred readings
- source-tradition preference
- canon-scope changes
- graph edges
- retrieval truth
- vector indexes
- apologetic conclusions as authority
- theology authority

## Cursor First Execution Prompt

```text
Work in logos-scripture-graph from the current worktree. Read AI_FRONT_DOOR.md, MASTER_CONTEXT.md read-only, PROJECT_STATUS.md, DATA_MAP.md, RAW_SOURCE_INVENTORY.md, manuscript source-catalog controls, T469_PRIMARY_WITNESS_ACQUISITION_WAVES_FOR_CURSOR.md, and .ai/control/primary_witness_acquisition_waves.yaml.

Create a metadata-only primary Bible witness acquisition scaffold under data/candidate/source_catalog/primary_bible_witnesses/. Do not download raw sources, do not store manuscript images, do not store manuscript transcriptions, do not import source text, do not change canonical data, do not create graph/retrieval/vector truth, do not select preferred readings or source traditions, and do not state apologetic conclusions as authority.

Populate source_catalog_rows.jsonl, image_rights_review.yaml, text_acquisition_review.yaml, blocked_or_permission_needed.yaml, storage_ledger.yaml, a task handoff, and validators/tests if needed. Every row must preserve source URL, rights status, source family, biblical scope, confidence, review status, recommended storage mode, estimated size, and non-authorizing scope label.
```
