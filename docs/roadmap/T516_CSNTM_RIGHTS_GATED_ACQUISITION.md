# T516 — CSNTM rights-gated acquisition campaign

Status: specification complete; acquisition blocked by external permission.

## Requested outcome

Create a durable local research collection for all 1,908 manuscript records currently shown by the CSNTM Digital Manuscript Collection, including available metadata and images, organized on the Logos NAS.

## Current evidence and boundary

- Live catalog observation on 2026-07-18: `1908 Total` at `https://collections.csntm.org/interactive?advancedSearch=true&advancedTab=physical&sort=rank`.
- CSNTM terms: `https://www.csntm.org/terms-of-use-copyright/`.
- CSNTM collaboration statement: `https://new.csntm.org/collaboration/`.
- `/robots.txt` returned HTTP 404 on 2026-07-18; absence of a robots file is not permission to crawl.
- CSNTM says manuscript image use requires permission from CSNTM and the holding institution, viewing is non-commercial/research-only, and permission is individual.
- CSNTM also says its viewer inhibits image downloads. The campaign must not bypass that safeguard.
- CSNTM's general terms do not expressly authorize bulk copying of the 1,908-record catalog into an information-retrieval system. Metadata inventory therefore also needs written bulk/API permission or a documented licensed export.

## Storage contract

Use UNC paths in executable configuration; `Z:` is shown here only for human readability.

| Lane | Planned path | Rule |
|---|---|---|
| Intake and checkpoints | `Z:\01-Projects\Logos\staging\T516\` | Task-scoped, resumable, disposable only by later approval |
| Catalog and rights decisions | `Z:\01-Projects\Logos\manuscript-witnesses\catalog\T516\` | IDs, holder, license evidence, decision, receipts |
| Provenance | `Z:\01-Projects\Logos\provenance\logos-scripture-graph\csntm\T516\` | URL, observed terms, hashes, acquisition receipts |
| Source originals | `Z:\01-Projects\Logos\source-originals\manuscript-witnesses\csntm\<holder_slug>\<csntm_id>\` | Write once after rights gate and verification; never overwrite |
| Campaign state | `Z:\08-AI-Operations\campaigns\T516\` | Controller-owned leases, checkpoints, budgets, stop evidence |

No images, catalog dump, or large metadata payload belongs in Git, OneDrive, `data/raw`, a release lane, or a publication lane.

## Rights states

Each record must end in exactly one state:

1. `authorized_csntm_and_holder`: written scope permits the requested local storage and analysis.
2. `authorized_upstream_direct`: an official upstream repository supplies the object under an exact compatible license; acquisition uses the upstream source, not a CSNTM download path.
3. `metadata_only_authorized`: bulk catalog fields are permitted but images are not.
4. `permission_required`: holder and/or CSNTM permission is missing or ambiguous.
5. `blocked`: terms prohibit the requested effect, the image is study-only, or evidence is inconsistent.

The ledger must separately capture local storage, OCR/transcription, AI analysis, embeddings/vectorization, redistribution, attribution, modification, and commercial-use rights. Silence is `not_authorized`, never implied permission.

## Known initial decisions

- P45: only the Chester Beatty-held Dublin portion is in the favorable correspondence scope; the Vienna portion is separate.
- P46: only the Chester Beatty-held Dublin portion is in scope; the Ann Arbor portion is separate.
- P66: Chester Beatty fragment 2 and Cologne fragment 1 have favorable cited terms, but the main Bodmer corpus is separate and may carry non-commercial conditions at its upstream host.
- P75: study-only/paid-reproduction boundary; blocked for this acquisition until separate permission is documented.

These are candidates for exact evidence binding, not blanket authorization for other CSNTM objects.

## Required permission request

Before catalog acquisition, obtain written authorization from `manuscripts@csntm.org` for:

- a complete machine-readable export or API access for all 1,908 catalog records;
- long-term private NAS storage of that metadata;
- automated, rate-limited retrieval and future refreshes;
- the exact fields supplied and required attribution;
- whether metadata may be parsed, normalized, OCR-linked, embedded/vectorized, and used in AI-assisted research;
- whether results may support commercial and public products, while source images remain private;
- a manifest identifying which images CSNTM itself may authorize and which require holder permission;
- permission to download authorized images by a supported method, not by bypassing viewer safeguards.

For every holder not covered by CSNTM's grant, obtain an object-specific or collection-specific license covering private long-term storage, OCR/transcription, computational analysis, AI/embedding/vector use, attribution, redistribution, and commercial use.

## Launch gates

The campaign stays `specification_only` until all of the following exist:

1. CSNTM bulk metadata/API authorization or a licensed export.
2. Object/collection rights ledger with evidence hashes and no inferred rights.
3. Revision-bound controller and CSNTM/upstream adapters.
4. Rate-limit and concurrency agreement.
5. Ten-record metadata dry run and one small image-set dry run.
6. Storage estimate with at least 500 GiB NAS reserve.
7. Deterministic checksum, resume, idempotency, and no-overwrite tests.
8. Independent launch review and Lowell's approval of the exact campaign revision.

## What this revision did not do

It did not scrape catalog pages, call private APIs, bypass the viewer, download images, copy metadata records, create NAS folders, run OCR, create embeddings, publish, or send email.
