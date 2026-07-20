# T473 Subagent Family And Scholarship Knowledge Base

Status: non-authorizing scaffold  
Date: 2026-07-15  
Owner: Lowell Wong  
Agent: Codex

## Purpose

Build the first subagent-family and library knowledge-base scaffold for Logos Scripture Graph. This project now needs more than one general assistant. It needs a small, governed research family that can repeatedly ask:

- What do we know?
- What do we know we do not know?
- What do we not yet know we need to know?
- Which expert family would notice a mistake that a Bible software engineer would miss?

This is a scaffold only. It does not create persistent automations, import sources, run OCR, build embeddings, or authorize graph/retrieval/canon/theology changes.

## Subagent Family

### Rights / Provenance Scout

Finds holding institution, rights statement, license, permission contacts, attribution language, storage rules, OCR permission, AI/embedding permission, redistribution, and commercial terms.

Use before any download, OCR, local storage, public display, or contributor artifact.

### Source Cataloger

Turns a source into structured rows: holder, shelfmark, date, material, language, folio/canvas, work/book/passage coverage, source family, canon lane, confidence, and review status.

Use before any manuscript image or text is treated as project evidence.

### OCR / Paleography Pipeline Scout

Designs OCR/HTR/transcription experiments for Greek majuscule, Hebrew, papyri, parchment, raking-light images, damage, lacunae, corrections, and marginalia.

Owner note: Mock Trial / Albert OCR assets are approved as local IP candidates. Reusable patterns include confidence review gates, material anchor gates, exception learning, A/B context assist, and subagent decision flow. Do not copy code until a separate adaptation task records provenance, dependencies, and Scripture-specific safety changes.

### Biblical Scholarship Librarian

Maintains the knowledge-base taxonomy: textual criticism, Septuagint, Hebrew Bible, DSS, NT papyri/codices, patristics, reception history, archaeology, epigraphy, material culture, digital humanities, and library science.

This agent tracks expert families, not celebrity authorities.

### Archaeology / Material Culture Scout

Tracks what material evidence can and cannot support: inscriptions, sites, dating, provenance, scribal culture, ancient Near Eastern background, and archaeological claims.

Use before public-facing claims that sound like "archaeology proves..."

### Unknown Unknowns Radar

The high-intelligence recurring scout. It looks for blind spots, field gaps, missing expert families, false assumptions, and cross-domain failure modes.

Examples:

- Are we assuming a digitization license covers every derivative?
- Are we confusing canonical authority with manuscript evidence?
- Are OCR engines trained on printed Greek failing on nomina sacra or ancient column geometry?
- Are we missing archaeology, epigraphy, codicology, or library-rights expertise before a public claim?

### Governance / Evidence Reviewer

Checks every other agent's output for scope discipline, source traceability, authority boundary leakage, and missing validation.

## Scholarship Knowledge Base Families

| Family | What It Contributes | Anchor Sources |
|---|---|---|
| NT textual criticism | Greek NT witnesses, variants, ECM/CBGM, manuscript cataloging | INTF databases, ECM, CSNTM |
| Hebrew Bible and DSS | Hebrew textual witnesses, Qumran fragments, scroll material context | Leon Levy DSS Digital Library |
| Septuagint / Greek OT | Greek Old Testament witnesses, codices, translation tradition | SBL resources, Leipzig Sinaiticus |
| Patristics / reception | Early Christian quotations, commentary, canon reception, transmission history | BiblIndex, Open Greek and Latin |
| Archaeology / epigraphy / material culture | inscriptions, sites, dating, ancient Near East context, physical artifacts | ASOR, EpiDoc |
| Digital humanities / library technology | IIIF, TEI, EpiDoc, OCR/HTR, metadata, linked data, preservation | IIIF, TEI |
| Rights / provenance / library science | reuse terms, attribution, public-domain status, holding-institution permissions | holding-institution pages and permission replies |

## Anchor Projects And Why They Matter

- Society of Biblical Literature: field-level biblical studies and text-critical resources: <https://www.sbl-site.org/resources/>
- TC: A Journal of Biblical Textual Criticism: open-access text-critical scholarship: <https://www.sbl-site.org/sbl-press/browse-journals/textual-criticism/>
- INTF databases: NTVMR and CBGM research infrastructure: <https://www.uni-muenster.de/INTF/en/datenbanken/index.html>
- ECM: modern critical edition work using CBGM: <https://www.die-bibel.de/en/the-editio-critica-maior-ecm>
- CSNTM: Greek NT manuscript digitization and preservation: <https://www.csntm.org/>
- Leon Levy DSS Digital Library: DSS images and public access: <https://www.deadseascrolls.org.il/?locale=en_US>
- ASOR: Near Eastern archaeology and material culture scholarship: <https://www.asor.org/about-asor>
- IIIF: image delivery/interoperability standards: <https://iiif.io/>
- IIIF Image API: standardized image-region/size/rotation requests: <https://iiif.io/api/image/3.0/>
- TEI: machine-actionable cultural heritage text standards: <https://tei-c.org/>
- TEI Guidelines: current technical text-encoding guidance: <https://guidelines.tei-c.de/en/html/>
- EpiDoc: TEI guidelines for ancient documents: <https://epidoc.stoa.org/gl/latest/>

## Unknown Unknowns Radar

The radar uses a Rumsfeld grid:

```text
known known
  -> source-backed fact or owner decision

known unknown
  -> named missing evidence, permission, expert review, or owner decision

suspected unknown unknown
  -> plausible blind spot inferred from field structure, anomaly, or missing expert family
```

Run triggers:

- new source family;
- permission reply;
- before download or storage;
- before OCR/transcription;
- before public claim;
- weekly during acquisition expansion;
- evidence anomaly such as conflicting metadata, mixed canon status, uncertain dating, marginalia, lacunae, corrections, or OCR failure.

## Model And Effort Policy

Use cheap bounded scouts for exact extraction. Use stronger synthesis for cross-domain integration. Use frontier/high-intelligence review only when there is unresolved architecture, methodology, or unknown-unknown disagreement.

Ultra effort remains human-gated and is not authorized by this plan.

## Non-Authorizations

This scaffold does not authorize:

- source downloads;
- OCR or transcription storage;
- source text import;
- canonical Bible text changes;
- canonical passage record changes;
- textual-critical decisions;
- preferred readings;
- source-tradition preference;
- canon-scope changes;
- boundary material in default Scripture retrieval;
- graph truth;
- retrieval truth;
- embeddings or vector indexes;
- theology authority.
