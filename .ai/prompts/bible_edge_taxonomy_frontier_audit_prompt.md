# Bible Edge Taxonomy Frontier Audit Prompt

You are Claude/frontier reviewer for the Bible edge taxonomy in `logos-scripture-graph`.

Goal:

Audit T450/T451 before any future predicate registry expansion or graph work. The owner wants a rich edge system useful for conservative, credal Christian, biblical, apologetic, polemic, historical, linguistic, manuscript, covenant, sacrificial, calendar, prophetic, apocalyptic, literary, and hermeneutic study without smuggling liberal-critical defaults or hidden denominational systems.

Do not expand the predicate registry. Do not generate graph edges. Do not decide theology.

Read:

- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md` read-only
- `.ai/control/bible_edge_taxonomy_research_program.yaml`
- `.ai/control/bible_edge_candidate_type_catalog.yaml`
- `.ai/control/orthodox_hermeneutic_firewall_docket.yaml`
- `.ai/control/contextual_reading_policy.yaml`
- `.ai/control/original_language_phrase_context_policy.yaml`
- `.ai/control/textual_variant_source_tradition_dossier_queue.yaml`
- `.ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml`
- `.ai/control/prophetic_oracle_vision_dossier_queue.yaml`
- `.ai/control/narrative_legal_covenant_dossier_queue.yaml`
- `.ai/control/wisdom_dialogue_poetry_dossier_queue.yaml`
- `.ai/control/gospel_wj_discourse_dossier_queue.yaml`
- `.ai/control/epistle_argument_theological_issue_dossier_queue.yaml`
- `config/governance/predicate_registry.yaml`
- `schemas/graph_edge_record.schema.json`

Check for:

1. Any edge type that should be P0/P1 blocked because it would likely create theology, graph, retrieval, source-tradition, canon, or apologetic authority.
2. Hidden liberal-critical, anti-supernatural, anti-canonical, heterodox, or one-denominational defaults.
3. Places where conservative/credal commitments are too weak or too broad.
4. Places where apologetic or polemic usefulness might be mistaken for evidence strength.
5. Prophecy, apocalyptic, typology, WJ/speaker, Christology, Trinity, law/gospel, covenant, manuscript, textual-variant, and original-language pressure points.
6. Missing edge families needed for faithful Bible study.
7. Candidate edge types that should remain tags only and never become graph predicates.
8. Whether the future Rust validator lane is safely limited to deterministic edge hygiene.

Return:

- approve / approve-with-edits / reject,
- P0/P1/P2 findings,
- required edits before T452 predicate proposal,
- edge families that require owner gate plus frontier review,
- edge families that can be left to deterministic tooling later,
- confirmation that no edge output, predicate registry expansion, retrieval truth, or theology authority is authorized.
