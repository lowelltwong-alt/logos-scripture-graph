# T451 Bible Edge Candidate Type Catalog

T451 deepens the T450 edge-family map into a planning-only candidate edge catalog. It does not expand `config/governance/predicate_registry.yaml`, emit graph rows, populate `data/candidate/connections/`, run retrieval/vector work, or authorize theology.

## Why This Exists

Future Bible graph work needs more than a few broad predicates. Quotations, allusions, covenant development, sacrifices, lunar calendar references, WJ discourse, Greek/Hebrew syntax, manuscript witnesses, prophecy, typology, apologetic arguments, and pastoral themes are different kinds of claims with different evidence floors.

T451 gives worker models a shared vocabulary so they can propose and critique edge types without smuggling graph truth. It also gives Codex and Claude/frontier reviewers a checklist for where theology, source traditions, textual variants, or apologetic pressure require escalation.

## Catalog Shape

The control file at `.ai/control/bible_edge_candidate_type_catalog.yaml` records:

- candidate edge families,
- specific candidate edge-type IDs,
- default assertion path,
- evidence channels,
- minimum evidence floor,
- escalation triggers,
- never-auto-create rules,
- multi-model review roles,
- future task queue for schema, Rust hygiene, and candidate-edge sandboxing.

Candidate edge types remain vocabulary only. A later task must separately authorize exact predicate registration, inverse rules, schemas, candidate row paths, and validators.

## Major Families

- Structural source and occurrence
- Editorial metadata
- Textual and intertextual relations
- Covenant, law, sacrifice, and calendar
- Prophecy, apocalyptic, and typology
- Orthodox creedal and doctrinal review
- Historical and geographic context
- Literary, discourse, and genre form
- Linguistic and original-language evidence
- Textual criticism and manuscript witnesses
- Apologetic and polemic pressure
- Pastoral and doctrine-risk labels

## Conservative And Credal Guardrails

The catalog is intentionally Scripture-centered and credal: it refuses hidden anti-supernatural, anti-canonical, heterodox, or liberal-critical defaults. It also refuses to let a model pick one denominational system where several orthodox readings remain possible.

That means theology-facing edges need explicit scope, evidence, limitations, and review. WJ/red-letter metadata, Strong's numbers, editorial crossrefs, manuscript age, headings, punctuation, and model agreement are evidence only.

## How Models Should Use It

Cursor or another fast model can use T451 to identify omitted candidate edge types and examples. Codex integrates and checks against repo governance. Claude/frontier audits hard cases: prophecy, apocalyptic, typology, WJ, textual variants, Christology, Trinity, original-language pressure, apologetic/polemic claims, and source-tradition issues.

No model can use T451 to choose predicates, generate graph edges, decide theology, select a source tradition, resolve variants, or rank apologetic force.

## Future Tasks

- `T452`: owner-gated edge schema and predicate proposal packet
- `T453`: Rust edge-candidate hygiene validator for large JSONL ledgers
- `T454`: multi-model edge-family research sprint
- `T455`: tiny candidate-only edge sandbox for one low-risk structural/editorial lane after owner gate

## External Anchors

The catalog records reference anchors for creedal Christianity, conservative hermeneutics, textual criticism, manuscript witnesses, DSS metadata, and original-language metadata. These are source anchors for future review, not local authority. Local repo governance and owner gates still control adoption.

## Explicit Non-Authorization

T451 creates no graph edge authority, no theology authority, no apologetic conclusion, no predicate registry entry, no candidate edge database, no retrieval/vector truth, no source-tradition preference, no chunk output, and no reviewed gold.
