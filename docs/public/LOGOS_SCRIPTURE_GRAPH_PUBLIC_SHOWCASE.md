# Logos Scripture Graph Public Showcase

This is the first visual starter pack for the Logos Scripture Graph project. It uses a tiny sample from the Leipzig University Library portion of Codex Sinaiticus because Leipzig gave clear written permission for its digitized images.

This page is meant to help contributors see where the project is going. It is not a full manuscript acquisition, not OCR, not a textual-critical decision, and not a change to the project's canonical Bible scope.

## The First Rights-Clean Visual Source

Source: Codex Sinaiticus, Leipzig University Library, Cod. gr. 1  
Manifest: <https://iiif.ub.uni-leipzig.de/0000061851/manifest.json>  
Viewer: <https://digital.ub.uni-leipzig.de/object/viewid/0000061851>  
Rights: Public Domain Mark 1.0 for Leipzig-held/digitized images, confirmed by Leipzig University Library email on 2026-07-15.  
Suggested attribution: Codex Sinaiticus, Leipzig University Library, digital images via Leipzig IIIF manifest.

## Starter Images

Web-sized IIIF derivatives from Leipzig (Public Domain Mark 1.0). Full-resolution acquisition stays outside this public doc surface.

![Codex Sinaiticus Leipzig canvas 1](https://iiif.ub.uni-leipzig.de/iiif/j2k/0000/0618/0000061851/00000001.jpx/full/800,/0/default.jpg)

Canvas 1: `1r (Q35-f. 1r)`

![Codex Sinaiticus Leipzig canvas 43](https://iiif.ub.uni-leipzig.de/iiif/j2k/0000/0618/0000061851/00000043.jpx/full/800,/0/default.jpg)

Canvas 43: `22r (Q47-f. 3r)`

![Codex Sinaiticus Leipzig canvas 86](https://iiif.ub.uni-leipzig.de/iiif/j2k/0000/0618/0000061851/00000086.jpx/full/800,/0/default.jpg)

Canvas 86: `43v (Q49-f. 8v)`

## What This Project Is Building

Most Bible tools give readers text, notes, search, or commentary. Logos Scripture Graph is trying to build the governed substrate underneath richer tools:

- source images and texts with rights, provenance, and checksums;
- manuscript witness records tied to folios, passages, dates, materials, and holding institutions;
- canonical 66-book Scripture records kept separate from deuterocanonical, apocrypha, patristic, commentary, and reception-history material;
- source-language evidence that can support alignment, variants, and manuscript comparison without silently choosing a preferred reading;
- chunking and retrieval objects that preserve discourse context instead of cutting Bible text into arbitrary token windows;
- graph relationships that distinguish asserted, inferred, candidate, reviewed, and rejected claims;
- contributor workflows where humans can review evidence packets instead of trusting opaque AI output.

## Why The Separation Matters

One manuscript can be legally usable while still containing different kinds of material. Codex Sinaiticus is valuable because it reaches across biblical witness, textual transmission, and early Christian reception history. The project keeps those lanes connected but not confused:

```text
rights-cleared source image
  -> folio/canvas metadata
  -> passage or work coverage
  -> lane classification
     -> canonical 66-book witness evidence
     -> boundary / non-66 / reception evidence
  -> reviewed downstream artifacts
```

That lets contributors study the whole historical picture while protecting the difference between Scripture authority, manuscript evidence, commentary, and background literature.

## What Can Be Built On Top

Future applications could include:

- a manuscript witness explorer that shows where a passage appears across early witnesses;
- an evidence-bundle viewer for textual variants;
- a canon-aware search tool that can include or exclude non-66 material on purpose;
- OCR and transcription review queues;
- AI-assisted paleography experiments with human review;
- contributor dashboards for cataloging folios, passage coverage, and rights status;
- retrieval profiles that can explain why a result is canonical Scripture, source-language evidence, commentary, or boundary material.

## What Does Not Exist Yet

The missing thing is not another Bible search box. The missing thing is an integrated, governed evidence layer where manuscripts, source-language texts, translations, canon scope, boundary literature, chunking, graph relationships, and AI/retrieval all share provenance and review gates.

This starter pack is the first public-facing visual proof of direction: a rights-clean manuscript source connected to a system that can grow without mixing up evidence, authority, and interpretation.

## Non-Authorizations

This showcase does not authorize:

- bulk manuscript download;
- full-resolution archival acquisition;
- OCR or transcription storage;
- canonical Bible text changes;
- canonical passage record changes;
- textual-critical decisions;
- preferred readings;
- source-tradition preference;
- canon-scope changes;
- graph truth;
- retrieval truth;
- embeddings or vector indexes;
- boundary material in default Scripture retrieval;
- theology authority.
