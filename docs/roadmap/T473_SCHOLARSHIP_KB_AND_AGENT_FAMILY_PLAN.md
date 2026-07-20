# T473 Scholarship KB And Agent Family Plan

## Purpose

Create the first governed design for a Logos Scripture Graph scholarship knowledge base and subagent family. This is the layer that helps the project know what kinds of expertise it needs before it confidently builds over manuscripts, versions, archaeology, patristics, commentary, and digital-library data.

The goal is not to replace scholars. The goal is to make the project structurally honest: every claim should know which field can test it, which source family supports it, what remains unknown, and when a stronger review lane is required.

## What This Builds

T473 records:

- a scholarship-domain taxonomy for the project knowledge base;
- an initial role family for repeatable subagent work;
- a known-known / known-unknown / unknown-unknown review loop;
- trigger rules for when the review loop should run;
- source and expert-family anchors to guide later research;
- strict non-authorizations so this does not become canon, graph, retrieval, or theology authority.

This is planning/control-plane work. It does not ingest new source material, create new manuscript rows, create embeddings, build vector indexes, alter canon scope, select preferred readings, or create graph truth.

## Knowledge Families

| Family | What It Contributes | Main Failure If Missing |
|---|---|---|
| Textual criticism | Variant units, witness distribution, apparatus method, limits of reconstruction | Treating one manuscript or edition as automatic authority |
| Manuscript studies | Shelfmarks, holding institutions, provenance, catalog identity, conservation history | Confusing a digital image, a manuscript object, and a catalog record |
| Paleography, codicology, papyrology | Dating, script, hands, material, quires, columns, lacunae, scribal habits | Overclaiming dates or reconstructing impossible page layouts |
| Hebrew Bible and DSS studies | Second Temple Hebrew witnesses, DSS content categories, biblical/non-biblical routing | Treating all Qumran material as Scripture evidence |
| Septuagint and ancient versions | Greek OT, Old Latin, Syriac, Coptic, Armenian, Georgian, Vulgate witness lanes | Missing evidence where textual history is versional rather than Greek/Hebrew manuscript only |
| New Testament papyri and codices | GA/INTF identifiers, papyri, majuscules, lectionaries, major codex comparison | Flattening P52/P45/P46/P66/P75/Sinaiticus/Vaticanus/Alexandrinus into slogans |
| Patristics and reception history | Quotations, allusions, paraphrases, harmonizations, author/work/section references | Saying "the Fathers reconstruct the Bible" without scope, genre, or citation confidence |
| Early Christian literature | Barnabas, Hermas, apocrypha, deuterocanon, pseudepigrapha, creeds, liturgy | Mixing boundary material into default canonical authority |
| Biblical archaeology and material culture | Inscriptions, sites, objects, chronology, external historical controls | Turning archaeology into proof-texting or ignoring material-context constraints |
| Digital humanities | TEI, IIIF, OCR/HTR, alignment, identifiers, reproducible manifests | Building an impressive but unreproducible data swamp |
| Rights, provenance, and library science | Licenses, custody, access models, attribution, preservation, catalog methods | Downloading material the project cannot legally store or analyze |
| Governance and theological boundary review | Canon profiles, authority lanes, review gates, owner decisions | Letting evidence silently become doctrine or canon scope |

## Agent Family

| Role | Cadence | Output | Must Not Do |
|---|---|---|---|
| `rights_provenance_scout` | before any acquisition or reuse | rights summary, attribution, storage/OCR/AI terms | download artifacts or infer permission |
| `scholarship_domain_mapper` | when a new corpus/domain appears | domain map, expert-family list, source anchors | treat secondary summaries as authority |
| `source_cataloger` | before row population | source-catalog candidate rows and blockers | import source text or collapse conflicts |
| `acquisition_pipeline_builder` | only after rights approval | manifests, checksums, reproducible acquisition steps | process unapproved sources |
| `evidence_boundary_reviewer` | before public claims or graph/retrieval use | boundary review, canon-lane routing, risk ledger | promote claims to canon/graph truth |
| `unknown_unknown_sentinel` | recurring and trigger-based | knowns matrix, blind-spot docket, next research questions | decide the answer itself |
| `archaeology_material_context_scout` | when historical/material claims enter | material-culture source map and limits | turn artifacts into theological proof |
| `public_contributor_explainer` | before public showcase updates | contributor-facing explanation and scope warnings | overstate certainty or rights |

The family should start small. The first operational source is Leipzig Codex Sinaiticus because written permission is clear for Leipzig-held/digitized images. Generalization comes after Leipzig proves the pattern.

## Known / Unknown Matrix

Use this matrix for every source family and every public claim:

| Bucket | Meaning | Example |
|---|---|---|
| Known known | Sourced, scoped, and reviewable fact | Leipzig granted PDM 1.0 / free-use permission for Leipzig-held Sinaiticus images |
| Known unknown | Named missing fact or unresolved scholarly question | Exact Leipzig canvas-to-book coverage before full page classification |
| Unknown unknown candidate | A plausible blind spot that could embarrass the project later | A folio label may not equal biblical content; an image may include marginalia, later hands, or mixed material |
| Assumption under test | A working assumption that must not become fact | "This canvas belongs in canonical_66" before classification |
| Escalation trigger | The event requiring a stronger reviewer | Source conflict, rights ambiguity, variant sensitivity, public claim, archaeology linkage, AI/vector use |

## Trigger Rules

Run the `unknown_unknown_sentinel` when:

- a new source family is added;
- a rights reply changes storage, OCR, AI, attribution, redistribution, or commercial-use scope;
- a manuscript contains both canonical and boundary material;
- a claim uses words such as oldest, earliest, complete, unchanged, original, reconstruct, proves, or reliable;
- a source moves from metadata-only to image/text acquisition;
- OCR, transcription, alignment, embedding, vector indexing, or graph generation is proposed;
- a public page, contributor pitch, or grant-style description is updated;
- a specialist domain not represented in the current KB becomes relevant;
- two source catalogs disagree on date, shelfmark, coverage, material, or rights;
- an archaeology or historical-background claim is tied to Scripture interpretation.

Recommended recurring cadence:

- weekly while active acquisition is happening;
- every new rights reply;
- every new public showcase change;
- before any PR that creates source/manuscript rows, AI-derived text, vector artifacts, or evidence reports.

## Initial Source And Expert Anchors

The KB should prefer official or field-institution anchors first:

- INTF / NTVMR / ECM / CBGM for Greek New Testament manuscript cataloging and method.
- CSNTM and holding institutions for manuscript image/catalog cross-checks.
- Israel Antiquities Authority and Israel Museum for DSS official anchors.
- Codex Sinaiticus partner institutions and holder-specific permission replies for Sinaiticus.
- BiblIndex and patristics societies/projects for patristic citation/reception metadata.
- TEI and IIIF for machine-readable manuscript/text standards.
- ASOR and related archaeology institutions for material-culture controls.
- Library rights pages, IIIF manifests, and holding-institution catalogs for provenance and access terms.

## Expert Types To Represent

Minimum expert-family coverage:

- Greek NT textual critic;
- Hebrew Bible / DSS specialist;
- Septuagint / ancient versions specialist;
- patristics and early Christian literature specialist;
- paleographer/codicologist/papyrologist;
- biblical archaeologist or material-culture specialist;
- digital-humanities engineer familiar with IIIF, TEI, OCR/HTR, and manifests;
- rights/provenance/library-science reviewer;
- canonical-boundary/governance reviewer.

## Non-Authorizations

T473 does not authorize:

- source-text import;
- transcription storage;
- additional raw image download;
- OCR or HTR output storage;
- metadata row population beyond future explicitly scoped tasks;
- canonical Bible text change;
- canonical passage record change;
- canon-scope change;
- preferred reading or source-tradition selection;
- textual-critical decision;
- graph edge generation;
- retrieval truth;
- embeddings or vector indexes;
- boundary import into default Scripture authority;
- archaeology-as-proof or apologetic conclusion as authority;
- automated email sending or mailbox mutation.

## Next Practical Step

Run the first `unknown_unknown_sentinel` pass against the Leipzig public-showcase and split-corpus plan. The pass should produce a small blind-spot docket before any more Leipzig images are downloaded or any OCR/transcription/vector work is proposed.
