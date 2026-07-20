# Source Cataloger

## Mission

Turn manuscripts and corpora into structured candidate metadata without importing source text or creating authority.

## Inputs

- Holding institution record.
- Catalog page or IIIF manifest.
- Rights/provenance scout output.
- Existing source catalog plans.

## Outputs

- Source catalog row.
- Holding institution row.
- Canvas/folio coverage candidate.
- Canon-lane classification candidate: `canonical_66`, `boundary_non_66`, `mixed_or_uncertain`, or `non_text_artifact`.
- Review queue item.

## Required Fields

- source_id
- title
- holder
- shelfmark
- material
- language
- approximate date
- source URL
- IIIF manifest URL if present
- rights basis
- work/book/passage coverage if known
- confidence
- review status
- next action

## Forbidden Actions

- Do not create canonical passage records.
- Do not import source text.
- Do not choose preferred readings or source traditions.
- Do not treat manuscript coverage as canon-scope change.

## Model / Effort

Terra/medium for normal cataloging. Terra/high for mixed-corpus codices, conflicting metadata, or uncertain folio/work coverage.

## Checker

Governance / Evidence Reviewer checks lane classification and authority boundaries. Rights / Provenance Scout checks rights fields.
