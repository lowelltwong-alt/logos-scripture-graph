# T471 Leipzig Sinaiticus Split-Corpus Start Plan

Status: planning-only, non-authorizing  
Date: 2026-07-15  
Owner: Lowell Wong  
Agent: Codex

## Purpose

Start with the one Codex Sinaiticus source where written permission is now clear: the Leipzig University Library IIIF manifest for Cod. gr. 1. The plan separates what the manuscript is allowed to be from what each page is allowed to mean inside the project.

The Leipzig reply gives broad rights for Leipzig's digitized images. It does not make every work inside the manuscript part of the canonical 66-book Scripture Graph corpus. A single manuscript can contain:

- canonical 66-book biblical witness material;
- deuterocanonical/apocrypha material;
- other early Christian boundary material such as Barnabas or Hermas in the wider Codex Sinaiticus tradition; and
- uncertain, mixed, blank, or imaging-only pages.

## Source Start Point

Use only this source for the first acquisition plan:

```text
Source ID: codex_sinaiticus_leipzig_iiif
Holder: Leipzig University Library
Manifest: https://iiif.ub.uni-leipzig.de/0000061851/manifest.json
Viewer: https://digital.ub.uni-leipzig.de/object/viewid/0000061851
Shelfmark: Leipzig, Universitaetsbibliothek Leipzig, Cod. gr. 1
Observed manifest title: 'Codex Sinaiticus' (Biblia graeca, Vetus Testamentum)
Observed extent: 43 leaves
Observed material: parchment
Observed language: Greek
Observed date: 4th century
```

Rights basis: Leipzig University Library replied on 2026-07-15 that all digital images of the Leipzig-held Codex Sinaiticus parts digitized by Leipzig University Library are under Public Domain Mark 1.0 and free to use in any way. This applies only to Leipzig-held/digitized images unless another holder gives separate permission.

## Two-Lane Corpus Plan

### Lane A: Canonical 66 Biblical Witness

Destination: `logos-scripture-graph`.

Use this lane for any Leipzig canvas containing material from the repo's governed canonical 66-book scope.

Allowed future records, after a separate acquisition task:

- source catalog row;
- folio/canvas metadata;
- rights/provenance record;
- checksum/storage ledger;
- candidate passage coverage;
- candidate OCR/transcription output.

Forbidden:

- changing canonical Bible text;
- changing canonical passage records;
- choosing a preferred reading;
- selecting a source tradition;
- creating reviewed gold;
- creating graph/retrieval/vector truth;
- changing canon scope.

### Lane B: Boundary / Non-66 Material

Destination: `logos-boundary-literature` or a separately scoped boundary profile, not default Scripture Graph authority.

Use this lane for any deuterocanonical/apocrypha, Barnabas, Hermas, or other non-66 material. Lowell does want this material, so it should be preserved and studied, but it must stay separated from canonical Scripture authority.

Allowed future records, after a separate acquisition task:

- boundary source catalog row;
- folio/canvas metadata;
- rights/provenance record;
- tradition scope;
- candidate OCR/transcription output;
- support/background links to canonical Scripture.

Forbidden:

- canonical passage records;
- canonical chunks;
- leaderboard inputs;
- default Scripture retrieval;
- canonical truth claims;
- canon-scope changes.

## Required First Step

Create a metadata-only coverage map from the Leipzig IIIF manifest:

```text
canvas_id
canvas_label
image_service_id
folio_or_quire_label
probable_work
probable_book
probable_passage_range
lane_classification: canonical_66 | boundary_non_66 | mixed_or_uncertain | non_text_artifact
rights_basis
review_status
notes
```

Do not download image binaries during this step. The goal is to know what each canvas is before storing anything.

## Execution Waves

### L0: Metadata-only coverage map

Parse the IIIF manifest and build a canvas coverage table. Classify every canvas as canonical 66, boundary non-66, mixed/uncertain, or non-text artifact. No image downloads.

### L1: Quarantined image acquisition

Only after explicit owner authorization, download Leipzig images into a non-Git, non-cloud-synced quarantine path. Keep canonical and boundary images in separate folders and record checksums.

### L2: OCR / transcription candidates

Run OCR or diplomatic transcription experiments separately per lane. All outputs remain candidate until reviewed.

### L3: Analysis / embeddings

Only after explicit owner authorization, build separate experimental indexes. Do not put boundary material in the default Scripture retrieval profile.

## Practical Recommendation

Start with Leipzig because its rights are clear, but treat the manuscript as a split corpus:

```text
one legal source
  -> two research lanes
     -> canonical 66 biblical witness evidence
     -> boundary/non-66 historical and reception evidence
```

That preserves the value of the whole manuscript while protecting the project's Scripture authority boundary.

## Non-Authorizations

This plan does not authorize:

- raw image downloads;
- source text import;
- transcription storage;
- canonical Bible text changes;
- canonical passage record changes;
- textual-critical decisions;
- preferred readings;
- source-tradition preference;
- canon-scope changes;
- graph edges;
- retrieval truth;
- vector indexes;
- boundary material in default Scripture retrieval;
- apologetic conclusions as authority;
- theology authority.
