# Bible Edge Taxonomy Model Review Prompt

You are reviewing the non-authorizing Bible edge taxonomy in `logos-scripture-graph`.

Read first:

1. `AI_FRONT_DOOR.md`
2. `.ai/control/MASTER_CONTEXT.md` read-only
3. `.ai/control/PROJECT_STATUS.md`
4. `config/governance/predicate_registry.yaml`
5. `schemas/graph_edge_record.schema.json`
6. `.ai/control/bible_edge_taxonomy_research_program.yaml`
7. `.ai/control/bible_edge_candidate_type_catalog.yaml`
8. `.ai/control/orthodox_hermeneutic_firewall_docket.yaml`
9. `.ai/control/contextual_reading_policy.yaml`

Mode: review only.

Do not:

- expand the predicate registry,
- generate graph edges,
- create candidate edge rows,
- write retrieval/vector/index artifacts,
- import boundary material,
- decide theology,
- select a source tradition,
- resolve textual variants,
- promote reviewed gold,
- change chunk output.

Review questions:

1. What candidate edge types are missing for faithful Bible study, apologetics, polemics, literary analysis, original-language work, manuscript evidence, calendar/feasts, covenant/law/sacrifice, prophecy/apocalyptic, or pastoral/doctrinal review?
2. Which existing candidate types are too broad, too risky, or likely to smuggle theology?
3. Which edge types can be deterministic/structural later, and which must require reviewed semantic or frontier review?
4. Which edge types need a clearer evidence floor?
5. Which edge types need stronger “never auto-create” rules?
6. Which claims should be split into separate candidate types?
7. Which proposed future predicates should not become predicates at all?

Return:

- verdict: approve / approve-with-edits / reject,
- P0/P1/P2 findings,
- missing edge families,
- candidate additions with evidence floors,
- candidate deletions or splits,
- hard cases for Claude/frontier,
- explicit confirmation that no graph/theology/retrieval/chunk authority is created.
