---
object_type: roadmap_task_record
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-23 during T392 from the T390 metadata plan and T391 official-source research packet."
reason_for_inclusion: "Document the first SQLite source-catalog schema shell and source-only seed rows for biblical manuscript reliability metadata while keeping witness rows, source text, preferred readings, and apologetic authority out of scope."
---

# T392 SQLite Source Catalog Schema Shell

## Summary

T392 creates the first SQLite-ready source-catalog shell for biblical manuscript reliability
metadata. It commits text artifacts only:

- `data/candidate/source_catalog/manuscript_reliability/sqlite/schema.sql`
- `data/candidate/source_catalog/manuscript_reliability/sqlite/seed_rows.jsonl`
- `data/candidate/source_catalog/manuscript_reliability/sqlite/manifest.yaml`
- `.ai/control/manuscript_source_catalog_sqlite_shell.yaml`

No binary SQLite database is committed. Validation builds an in-memory SQLite database from the
schema and seed rows, then proves the guardrails.

## What Is Seeded

T392 seeds only four row families from the T391 official source anchors:

| Table | Rows | Scope |
| --- | ---: | --- |
| `scripture_source_family` | 5 | Source-family taxonomy from T391. |
| `scripture_source_catalog` | 18 | Curated official/primary/academic source anchors from T391. |
| `evidence_source_catalog_method_profile` | 5 | What each source family can and cannot prove. |
| `evidence_source_trust_rule` | 9 | Anti-guessing and conflict-handling rules from T390/T391. |

Every row carries:

- `source_url`
- `method`
- `confidence`
- `provenance_note`
- `review_status`
- `source_family`
- `rights_access_status`
- `non_authorizing_scope_label`

Every row also carries explicit false text-storage flags.

## Empty Shell Tables

These tables exist as schema shell only and must remain empty in T392:

- `scripture_holding_institution`
- `scripture_catalog_witness_record`
- `scripture_witness_identifier`
- `scripture_witness_date_claim`
- `scripture_witness_material_claim`
- `scripture_witness_coverage_claim`
- `scripture_witness_discovery_event`
- `evidence_catalog_review_queue`

They are present so future population tasks have a governed shape, but this PR does not populate
institution, witness, identifier, date, material, coverage, discovery, or review-queue rows.

## Data Boundary

Only `scripture_*` and `evidence_*` tables are allowed. T392 creates no `canonical_*`,
`boundary_*`, or `doctrine_*` table or view.

The candidate data path is deliberate:

```text
data/candidate/source_catalog/manuscript_reliability/sqlite/
```

The table names are Scripture Graph namespaces, but the committed file location stays visibly
candidate because this is not canonical Bible text and not a preferred-reading authority surface.

## Non-Authorizations

T392 authorizes no witness row population, holding-institution row population, date/material/
coverage/discovery row population, source text import, manuscript transcription storage, Bible
text storage, canonical Bible text change, canonical passage record change, preferred reading,
source-tradition preference, canon-scope change, Boundary Literature import, Doctrine Genealogy
import, graph edge generation, retrieval truth, embedding/vector work, chunk output, reviewed-gold
promotion, or apologetic conclusion as truth.

## Validation

T392 is guarded by:

```bash
python scripts/validate_manuscript_source_catalog_sqlite_shell.py
python scripts/validate_task_scope.py --task-id T392
python scripts/agent/validate_handoffs.py
python scripts/validate_all.py
python -m pytest -q
```

The focused validator loads the schema into in-memory SQLite, inserts the JSONL seed rows, confirms
row counts, confirms empty witness/review-queue tables, rejects forbidden namespaces, and proves no
`canonical_*` table or view carries source-catalog, boundary, commentary, patristic, theologian,
doctrine, or apologetic data.

## Next Goal Prompt

```text
Work in logos-scripture-graph after T391 and T392 are on live origin/main. Read AI_FRONT_DOOR.md, MASTER_CONTEXT.md read-only, PROJECT_STATUS.md, DATA_MAP.md, T387 scaffold, T390 metadata plan, T391 source-catalog research packet, and T392 SQLite source-catalog shell. Populate the first metadata-only biblical DSS witness source rows from official IAA/Leon Levy and Israel Museum anchors, beginning with a very small exemplar set such as the Great Isaiah Scroll only if official row-level source URLs, source method, date range, material/language/coverage scope, rights/access status, provenance, confidence, dissent/uncertainty, and review status are available. Do not import source text, manuscript transcription, Bible text, non-biblical Qumran content, commentary, patristic material, preferred readings, source-tradition preferences, graph/retrieval/vector outputs, or apologetic conclusions as authority. Preserve candidate and blocked claims separately and add validation proving witness rows cannot exist without source URL, method, confidence, provenance, review status, rights/access status, and non-authorizing scope labels.
```
