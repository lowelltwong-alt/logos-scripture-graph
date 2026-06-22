---
object_type: roadmap_research_packet
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-22 during T391 from official/primary manuscript source anchors."
reason_for_inclusion: "Give future agents a curated source-catalog research packet for biblical manuscript reliability metadata before any SQLite database, source rows, witness rows, transcriptions, preferred readings, graph output, or apologetic report authority."
---

# T391 Manuscript Source Catalog Research Packet

## Summary

T391 turns the T390 source-catalog metadata plan into a research packet. It records source metadata
only:

- curated official/primary source anchors;
- source-family taxonomy;
- DSS biblical witness packet;
- NT papyri/codices packet;
- discovery timeline source anchors;
- open questions and blocked claims;
- validation and handoff requirements.

It does not create a SQLite database, populate rows, import manuscript text, store transcription
text, store Bible text, select preferred readings, prefer a source tradition, change canon scope,
generate graph/retrieval/vector truth, import Boundary Literature, or state apologetic conclusions
as authority.

Primary machine-readable packet:

```text
.ai/control/manuscript_source_catalog_research_packet.yaml
```

Validator:

```text
scripts/validate_manuscript_source_catalog_research_packet.py
```

## Curated Source List

| Source ID | Family | Institution | Use |
| --- | --- | --- | --- |
| `iaa_leon_levy_dss_digital_library` | DSS biblical witness catalogs | Israel Antiquities Authority | Official DSS digital-library anchor. |
| `iaa_dss_archive_browser` | DSS biblical witness catalogs | Israel Antiquities Authority | Archive browsing by site, language, content, and search. |
| `iaa_dss_discovery_publication` | DSS biblical witness catalogs | Israel Antiquities Authority | Discovery/publication timeline anchor. |
| `iaa_dss_content_categories` | DSS biblical witness catalogs | Israel Antiquities Authority | Biblical/non-biblical content boundary source. |
| `israel_museum_great_isaiah_scroll` | DSS biblical witness catalogs | Israel Museum | Great Isaiah Scroll digital collection anchor. |
| `israel_museum_great_isaiah_collection_record` | Holding institution catalogs | Israel Museum | Great Isaiah Scroll collection-record cross-check. |
| `intf_ntvmr` | NT manuscript catalogs | INTF | Greek NT manuscript catalog/workspace anchor. |
| `intf_liste` | NT manuscript catalogs | INTF | Greek NT manuscript recording-list lookup anchor. |
| `intf_institute_profile` | Method profiles | INTF | Institutional authority and cataloging role. |
| `intf_ecm` | Method profiles | INTF | ECM method profile for textual history and apparatus scope. |
| `intf_cbgm` | Method profiles | INTF | CBGM method profile for variants and witness relationships. |
| `csntm_manuscripts_catalog` | NT manuscript catalogs | CSNTM | NT manuscript catalog cross-check. |
| `csntm_p52` | NT manuscript catalogs | CSNTM | P52 source-record metadata exemplar. |
| `manchester_rylands_p52` | Holding institution catalogs | University of Manchester Library | P52/Greek P 457 holding-institution cross-check. |
| `codex_sinaiticus_project` | Major codex project catalogs | Codex Sinaiticus Project | Sinaiticus project and digital reunification anchor. |
| `codex_sinaiticus_project_about` | Major codex project catalogs | Codex Sinaiticus Project | Conservation/digitization/project activity anchor. |
| `vatican_library_codex_vaticanus` | Major codex project catalogs | Vatican Library | Vat.gr.1209 official digital manuscript and rights anchor. |
| `british_library_codex_alexandrinus` | Major codex project catalogs | British Library | Royal MS 1 D V / Alexandrinus official archive anchor. |

Every source row in the packet carries source URL, method, confidence, provenance, review status,
and a limit statement.

## Source-Family Taxonomy

T391 keeps five source families:

- `dss_biblical_witness_catalogs`
- `nt_manuscript_catalogs`
- `major_codex_project_catalogs`
- `holding_institution_catalogs`
- `critical_apparatus_method_profiles`

These families belong in Scripture Graph only for manuscript source metadata. Non-biblical
Qumran/DSS compositions, church fathers, patristic citations, commentaries, early creed wording,
theologian writings, reception history, and doctrine lineage route outside this repo.

## DSS Biblical Witness Packet

Confirmed facts are limited to official source-metadata claims. T391 confirms that:

- IAA/Leon Levy is the official DSS digital-library anchor;
- IAA archive browsing exposes source navigation by site, language, content, and search;
- IAA content categories distinguish biblical compositions from non-biblical and other content families;
- IAA content scope gives a biblical-compositions source boundary without changing canon authority;
- IAA discovery/publication page is the source anchor for discovery, first-scroll, publication, and access timing;
- Israel Museum Great Isaiah Scroll anchors are located for later row-level review.

Blocked DSS claims include:

- "the DSS prove the Bible was unchanged";
- "the DSS discovery by itself settles prophecy-date debates";
- "non-biblical DSS texts belong in Scripture Graph canonical records";
- exact all-witness lists before row-level catalog review;
- earliest-by-book claims before date/method/dissent rows exist.

## NT Papyri And Codices Packet

Confirmed facts are limited to source roles and source-record metadata:

- INTF documents/analyzes the Greek NT textual tradition and operates the international recording list;
- NTVMR/Liste are first-stop catalog anchors for Greek NT witnesses;
- ECM and CBGM are method-profile anchors, not preferred-reading authority;
- CSNTM P52 and Manchester Greek P 457 are cross-check anchors for P52 metadata and dating-method discussion;
- Codex Sinaiticus Project is the official Sinaiticus project/digital reunification anchor;
- Vatican Library and British Library records anchor Vaticanus/Alexandrinus source planning.

Blocked NT claims include:

- P52 exact date or definitive earliest-fragment status;
- Sinaiticus or Vaticanus as preferred text by default;
- catalog abundance as proof without variant units, witness distribution, and method profiles;
- P45/P46/P66/P75 metadata population before official source sets and rights/access review.

## Discovery Timeline Anchors

T391 identifies source anchors for future timeline work:

- DSS discovery and publication history from IAA;
- DSS content scope and archive filtering from IAA;
- Greek NT catalog source-of-record anchors from INTF/NTVMR/Liste;
- NT method-profile context from INTF ECM/CBGM;
- major codex digitization and holding-institution anchors from Codex Sinaiticus Project, Vatican Library, and British Library.

Timeline rows are not populated yet. Discovery timing must record what became knowable, what
remained uncertain, source, method, confidence, provenance, and review status.

## Open Questions

The packet leaves these claims blocked:

- complete biblical DSS witness list;
- earliest DSS witness by biblical book;
- exact P52 date or earliest-fragment status;
- P45/P46/P66/P75 official source bundle;
- copy-abundance/reliability method profile;
- patristic reconstruction and commentary routing.

## Next Goal Prompt

Use this as the next goal when ready:

```text
Work in logos-scripture-graph from live origin/main. Read AI_FRONT_DOOR.md, MASTER_CONTEXT.md read-only, PROJECT_STATUS.md, DATA_MAP.md, T387 manuscript witness scaffold, T390 source catalog metadata plan, and T391 source-catalog research packet. Build the SQLite source-catalog schema shell and seed only curated source_catalog/source_family/method_profile/trust-rule metadata rows from T391 official source anchors. Do not populate witness rows yet, do not import source text, do not store manuscript transcription or Bible text, do not select preferred readings/source traditions, do not create graph/retrieval/vector outputs, and do not state apologetic conclusions as authority. Every row must have source URL, method, confidence, provenance, review status, source family, rights/access status, and an explicit non-authorizing scope label. Add validation/tests proving no canonical_* table or view includes source-catalog, boundary, commentary, patristic, theologian, doctrine, or apologetic data.
```

## Validation

Required:

```bash
python scripts/validate_manuscript_source_catalog_research_packet.py
python scripts/validate_chunking_lesson_index.py
python scripts/validate_chunking_theological_decision_register.py
python scripts/validate_task_scope.py --task-id T391
python scripts/agent/validate_handoffs.py
python scripts/validate_all.py
python -m pytest -q
```
