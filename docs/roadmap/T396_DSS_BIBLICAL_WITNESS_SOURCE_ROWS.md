---
object_type: roadmap_task_record
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-23 during T396 from the T391 official-source research packet and T395 SQLite source-catalog shell."
reason_for_inclusion: "Document the first metadata-only DSS biblical witness exemplar row population while preventing text import, authority drift, and overclaiming from a single witness."
---

# T396 DSS Biblical Witness Source Rows

## Summary

T396 adds a tiny, metadata-only DSS biblical witness exemplar set for the Great Isaiah Scroll.
It uses the T395 SQLite schema and keeps the original T395 source seed rows unchanged.

New data artifacts:

- `data/candidate/source_catalog/manuscript_reliability/sqlite/dss_biblical_witness_rows.jsonl`
- `data/candidate/source_catalog/manuscript_reliability/sqlite/dss_biblical_witness_rows_manifest.yaml`
- `.ai/control/dss_biblical_witness_source_rows.yaml`

No Bible text, manuscript transcription, translation, source excerpt, image, preferred reading,
graph edge, retrieval truth, vector output, or apologetic conclusion is stored.

## Row Scope

T396 populates only one witness candidate:

```text
dss_great_isaiah_scroll_1qisa
```

The population file contains nine rows:

| Table | Rows | Scope |
| --- | ---: | --- |
| `scripture_holding_institution` | 1 | Israel Museum holding-institution anchor. |
| `scripture_catalog_witness_record` | 1 | Great Isaiah Scroll witness record candidate. |
| `scripture_witness_identifier` | 2 | Candidate siglum/title identifiers. |
| `scripture_witness_date_claim` | 1 | Source-display date claim, not normalized proof. |
| `scripture_witness_material_claim` | 1 | Candidate language/material/format metadata. |
| `scripture_witness_coverage_claim` | 1 | Book-level Isaiah coverage metadata, no text. |
| `scripture_witness_discovery_event` | 1 | IAA/Leon Levy discovery-publication context. |
| `evidence_catalog_review_queue` | 1 | Blocked normalization and review questions. |

## Source Anchors

T396 uses only official anchors already routed through T391/T395:

- `https://dss.collections.imj.org.il/isaiah`
- `https://www.imj.org.il/en/collections/198208-0`
- `https://www.deadseascrolls.org.il/learn-about-the-scrolls/discovery-and-publication`

The rows cite the source URLs and record source method, confidence, provenance, review status,
rights/access status, source family, and non-authorizing labels.

## Candidate And Blocked Claims

Date, material, coverage, and identifier rows remain candidate/review-pending where the official
pages expose summary-level or rendered metadata. T396 does not normalize date intervals, adjudicate
all catalog identifiers, decide exact script classification, settle rights/reuse status, or expand
to additional DSS witnesses.

Those blockers are preserved in `evidence_catalog_review_queue` rather than silently promoted.

## Premortem And Red-Team Fixes

Assume this task fails badly. The P0/P1 risks were:

- Source rows become Scripture authority or preferred-reading authority.
- Rows are invented from memory instead of official row-level anchors.
- Bible text, source text, manuscript transcription, translation, images, commentary, or creed
  wording is imported.
- DSS dates/discovery are treated as apologetic proof.
- Candidate claims become confirmed facts.
- One famous witness is treated as a source-tradition preference.
- Non-biblical DSS/Qumran material leaks into Scripture Graph.
- T393 chunking focus is disturbed.
- Parallel-agent work is overwritten or mixed into this branch.

Fixes applied:

- Use one Great Isaiah Scroll exemplar only.
- Keep every row metadata-only with false text-storage flags.
- Require source URL, method, confidence, provenance, review status, rights/access status, source
  family, and non-authorizing scope label.
- Preserve date/material/coverage uncertainty as candidate status or review-queue blockers.
- Add a validator that rejects forbidden text-bearing keys, unauthorized source URLs, and unscoped
  extra witnesses.
- Leave current-focus/chunking output/graph/retrieval/vector surfaces unchanged.

## Non-Authorizations

T396 authorizes no additional witness population without a later task, committed SQLite database
file, source text import, transcription storage, Bible text storage, image ingestion,
image-derived text, canonical Bible text change, canonical passage record change, chunk output,
reviewed-gold promotion, textual-critical decision, preferred reading, source-tradition
preference, canon-scope change, non-biblical DSS import, Boundary Literature import, commentary or
patristic import, Doctrine Genealogy import, graph edge generation, retrieval truth, embedding or
vector work, or apologetic conclusion as truth.

## Validation

T396 is guarded by:

```bash
python scripts/validate_dss_biblical_witness_source_rows.py
python -m pytest -q tests/test_dss_biblical_witness_source_rows.py
python scripts/validate_task_scope.py --task-id T396
python scripts/agent/validate_handoffs.py
python scripts/validate_all.py
python -m pytest -q
```

The focused validator loads the T395 schema and source seed rows into in-memory SQLite, inserts the
T396 population rows, checks row counts, verifies official source URLs against the T391 source
packet, rejects forbidden text-bearing keys, requires false text-storage flags, and fails if any
`canonical_*`, `boundary_*`, or `doctrine_*` object appears.

## Next Goal Prompt

```text
Work in logos-scripture-graph from live origin/main after T396 is merged. T397, T398, and T399 already exist on main; use T400 for this manuscript-reliability task. Start with a premortem and red-team pass, then fix P0/P1 risks before editing. Populate a tiny metadata-only NT papyri/codices exemplar set from official INTF/NTVMR/Liste, CSNTM, and holding-institution anchors already routed through T391/T395. Prefer one or two exemplars only. Do not import source text, manuscript transcription, Bible text, images, preferred readings, source-tradition preferences, graph/retrieval/vector output, Boundary Literature material, Doctrine Genealogy material, or apologetic conclusions as authority. Every row must carry source_url, method, confidence, provenance_note, review_status, rights_access_status, source_family, non_authorizing_scope_label, and candidate/blocked status where appropriate. Add validation/tests and update TOCs/status/decision/lesson/data-map surfaces.
```
