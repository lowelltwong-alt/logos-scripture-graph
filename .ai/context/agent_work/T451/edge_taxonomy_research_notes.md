# T451 Edge Taxonomy Research Notes

These notes are non-authorizing and support `.ai/control/bible_edge_candidate_type_catalog.yaml`.

## Repo Baseline

Existing registered predicates are still limited to:

- `editorial_cross_reference`
- `quotesFrom`
- `alludesTo`
- `echoes`
- `fulfills`
- `typifies`
- `parallelTo`
- `thematicallyRelatedTo`
- `groundedIn`
- `renders`
- `occursIn`

Existing schemas already distinguish stricter future `GraphEdgeRecord` classes from looser current `RelationshipObject` candidates. T451 does not change either schema.

## Subagent Findings Folded In

Read-only repo sweep found:

- predicate registry exists but is small,
- `GraphEdgeRecord` is stricter but planning-only,
- `RelationshipObject` is loose,
- candidate semantic edges exist under `data/candidate/connections/`, but T451 does not touch them,
- editorial crossrefs exist as canonical source metadata only,
- dossier queues already deny graph-edge authority.

Read-only domain sweep recommended deeper candidate types for:

- textual/intertextual relations,
- covenant/law/sacrifice/calendar,
- prophecy/fulfillment/typology,
- Christology/Trinity/creedal guardrails,
- historical/geographic context,
- literary/discourse forms,
- linguistic/original-language evidence,
- textual criticism/manuscript witnesses,
- apologetic/polemic pressure,
- pastoral/doctrinal risk labels.

## External Anchors Checked

- Nicene Creed reference via Greek Orthodox Archdiocese
- Chicago Statements via Defending Inerrancy
- INTF CBGM overview
- Codex Sinaiticus Project
- Leon Levy Dead Sea Scrolls Digital Library
- Open Scriptures Hebrew Bible / OSHB

These are anchors for future review, not local authority. Local repo governance controls adoption.

## Main Design Decision

T451 keeps the first usable edge vocabulary separate from predicate registration. The catalog names candidate edge types so models can review and improve the map, but every type is `candidate_type_only`.

## Key Guardrail

The most dangerous transition is turning a helpful review tag into an asserted edge:

- WJ marker -> Jesus speaker truth
- editorial crossref -> intertext truth
- Strong's id -> lexical/theological truth
- oldest manuscript -> preferred reading
- model agreement -> reviewed graph truth
- apologetic usefulness -> proven conclusion

T451 records those as never-auto-create failures.
