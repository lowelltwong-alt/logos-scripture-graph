---
object_type: roadmap_task_record
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-22 during T387 as a planning-only Scripture Graph scaffold for manuscript-witness reliability evidence."
reason_for_inclusion: "Record the safe repo placement, database shape, source anchors, and anti-guessing controls for oldest fragments, manuscript witnesses, variants, discovery timeline, and reliability evidence before any corpus import."
---

# T387 Manuscript Witness Reliability Scaffold

## Purpose

T387 starts the Scripture Graph side of the broader Bible reliability and provenance project.
It does not import manuscript text, Bible text, transcriptions, editions, or canonical records.
It defines what future data must prove before the project can responsibly make claims about old
fragments, Dead Sea Scrolls biblical witnesses, New Testament papyri/codices, textual variants,
copy abundance, discovery timeline, and reliability reports.

## Placement Decision

This belongs in `logos-scripture-graph` because the planned records are canonical Scripture
witness metadata: sigla, source catalogs, date ranges, languages, scripts, materials, coverage
scope, variant-unit metadata, attestation metadata, and discovery timeline events.

The boundary remains firm:

- biblical manuscript witness metadata belongs here;
- non-biblical Qumran/DSS corpus text belongs in `logos-boundary-literature`;
- patristic citations, church fathers, commentaries, and theologian writings belong in
  `logos-boundary-literature`;
- doctrine-development lineage belongs in future `logos-doctrine-genealogy`;
- cross-repo authority/routing policy belongs in `logos-governance-architecture`.

## Database Shape

The planning scaffold reserves only `scripture_*` and `evidence_*` namespaces:

- `scripture_witness_source`
- `scripture_manuscript_witness`
- `scripture_textual_variant_unit`
- `scripture_variant_attestation`
- `scripture_discovery_timeline_event`
- `evidence_reliability_claim`

It forbids `canonical_*` tables for this layer. That matters because manuscript/reliability
evidence can support review, but it must not silently become canonical Bible text or a preferred
reading.

## Evidence Fields

Future records must carry:

- source catalog or holding-institution reference;
- date range, precision, method, confidence, and dissent where applicable;
- language, script, material, repository, and coverage scope;
- confirmed facts separated from candidate claims;
- provenance, source URL, license or rights status, and review status;
- non-authorization flags for text import, preferred readings, canon changes, graph edges,
  retrieval truth, and apologetic conclusions.

## Source Anchors

Initial anchors are deliberately conservative:

- Israel Antiquities Authority Leon Levy Dead Sea Scrolls Digital Library for DSS/Judean Desert
  fragment catalog and image-access metadata.
- IAA discovery/publication history for what was discovered, published, or made accessible when.
- Israel Museum Great Isaiah Scroll page for a biblical DSS witness example with date and coverage
  scope.
- INTF institute and ECM pages for New Testament manuscript catalog and textual-critical method
  anchors.
- University of Manchester Greek P 457/P52 page and CSNTM P52 catalog page for early-fragment
  date-caution fields.
- Codex Sinaiticus Project for a major codex witness and completeness-scope wording.

These sources are anchors for metadata shape, not imported corpus data.

## Anti-Guessing Rules

No future agent may:

- store AI-inferred date, language, script, provenance, or coverage as fact without source, method,
  confidence, provenance, and review status;
- use "oldest", "earliest", "complete", or "unchanged" without defining scope;
- infer original text or preferred reading from witness age alone;
- treat copy abundance as proof without comparing attestation and variants;
- treat a discovery date as a solved apologetic conclusion;
- import noncanonical Qumran/community texts into canonical Scripture records;
- store Scripture text, creed wording, or manuscript transcription text in this scaffold.

## Next Safe Steps

1. Build source-catalog metadata rows for biblical DSS witnesses only, with no transcription text.
2. Build a New Testament papyri/codices source-catalog metadata plan from INTF/CSNTM/holding
   institution records.
3. Add a method profile for copy abundance, variant detection, and what witness distribution can
   and cannot prove.
4. Add a discovery timeline map showing what was knowable before and after major discoveries.
5. Join with Boundary Literature only through labeled `evidence_*` derived report views.

## Non-Authorizations

T387 authorizes no source-text import, canonical Bible text change, canonical passage record
change, chunk output change, reviewed-gold promotion, textual-critical decision, preferred reading,
source-tradition preference, canon-scope change, boundary import, graph edge, retrieval truth,
embedding/vector work, doctrinal system, or apologetic conclusion as truth.
