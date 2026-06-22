---
object_type: roadmap_task_record
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-22 during T390 to turn the T387 manuscript witness reliability scaffold into a concrete source-catalog metadata plan."
reason_for_inclusion: "Give future agents a validated sequence for biblical DSS, NT papyri, major codices, variants, discovery timeline, SQLite metadata, Boundary Literature reception, and Doctrine Genealogy without mixing authority layers."
---

# T390 Manuscript Source Catalog Metadata Plan

## Purpose

T390 is the actual metadata plan before the database build. It defines the source-catalog tables,
field lists, source families, official source anchors, trust rules, review statuses, and future goal
prompts needed to populate biblical manuscript reliability evidence responsibly.

This is still plan-only. It creates no SQLite database, imports no manuscript text, and populates no
metadata rows.

## What Lives Here

`logos-scripture-graph` owns canonical Scripture witness metadata:

- biblical Dead Sea Scrolls/Judean Desert witness catalog metadata;
- New Testament papyri and codex catalog metadata;
- source catalogs, holding institutions, shelfmarks, sigla, identifiers, date ranges, language,
  script, material, and coverage claims;
- discovery, publication, digitization, and what-was-known-when timeline events;
- method profiles for what copy abundance and variant detection can and cannot prove.

Church fathers, patristic citations, commentaries, theologian writings, reception history, early
creed wording, and non-biblical Qumran/DSS content stay out of Scripture Graph records and route to
`logos-boundary-literature`. Denominational and theologian lineage belongs in future
`logos-doctrine-genealogy`.

## SQLite-Ready Tables

The plan reserves only `scripture_*` and `evidence_*` tables:

- `scripture_source_catalog`
- `scripture_holding_institution`
- `scripture_catalog_witness_record`
- `scripture_witness_identifier`
- `scripture_witness_date_claim`
- `scripture_witness_material_claim`
- `scripture_witness_coverage_claim`
- `scripture_witness_discovery_event`
- `evidence_source_catalog_method_profile`
- `evidence_source_trust_rule`
- `evidence_catalog_review_queue`

Every table is metadata-only. Every table denies Scripture text storage, manuscript transcription
storage, and boundary text storage. Every table requires source URL, provenance, confidence, and
review status.

No `canonical_*` table or view may include manuscript reliability, commentary, patristic,
theologian, doctrine, or boundary data.

## Source Families

Initial source families are:

- DSS biblical witness catalogs;
- New Testament manuscript catalogs;
- major codex project catalogs;
- holding institution catalogs;
- critical apparatus and method profiles.

The initial anchors are official or near-source catalog surfaces: IAA/Leon Levy DSS, IAA archive and
discovery pages, Israel Museum Great Isaiah Scroll, INTF/NTVMR, CSNTM, Manchester P52, Codex
Sinaiticus Project, Vatican Library Vat.gr.1209, and British Library Royal MS 1 D V.

## Trust Rules

T390 hardens the anti-vibes layer:

- prefer official holding institutions over secondary summaries, while preserving conflicts;
- require catalog identifiers before witness rows;
- store dates as ranges, never inferred point dates;
- require sourced coverage scope;
- preserve conflicting catalog claims as separate rows;
- store no transcription text;
- never select preferred readings from catalog metadata;
- record rights/access status before future population;
- route non-biblical DSS/Qumran material to Boundary Literature.

## Future Goal Prompts

1. DSS biblical source catalog population:
   create metadata-only rows for biblical DSS witnesses from official catalogs. No transcription
   text and no non-biblical Qumran content.
2. NT papyri and major codices population:
   populate source metadata from INTF/NTVMR, CSNTM, holding institutions, and official codex
   projects. Preserve conflicting dates and coverage as sourced claims.
3. Variant and copy abundance method profile:
   define what copy abundance, collation, witness distribution, and variant detection can and cannot
   prove.
4. Discovery timeline:
   map what became knowable when and what remained uncertain.
5. Boundary Literature reception/reconstruction:
   store patristic/commentary/reception metadata in `logos-boundary-literature`, with Scripture
   references only.
6. Doctrine Genealogy theologian lineage:
   later connect Scripture references and reception references to scoped doctrine development.

## Non-Authorizations

T390 authorizes no SQLite database creation, metadata row population, source text import,
transcription storage, canonical Bible text change, canonical passage record change, chunk output
change, reviewed-gold promotion, textual-critical decision, preferred reading, source-tradition
preference, canon-scope change, boundary import, commentary/patristic import, Doctrine Genealogy
import, graph edge, retrieval truth, embedding/vector work, doctrinal system, or apologetic
conclusion as truth.

## Validation

T390 is guarded by:

- `scripts/validate_manuscript_source_catalog_metadata_plan.py`
- `tests/test_manuscript_source_catalog_metadata_plan.py`
- `scripts/validate_all.py`

