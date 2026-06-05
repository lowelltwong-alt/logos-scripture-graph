# Connection-Discovery Agent — standing brief

For agents whose job is to **find connections we have not discovered or curated** —
intertextual, lexical, thematic, typological, and extra-biblical — and propose them
**safely** as candidates for human review. This is how the graph grows beyond what we
hand-author, without contaminating the canonical layer.

> Start at `AI_FRONT_DOOR.md`. Read `MASTER_CONTEXT.md` (§4, §6, §9). Then this file.

## Rule 0 — you propose, you never promote

Every connection you find is a **candidate**. It lands in `data/candidate/` (trust
zone `candidate`), carries evidence + provenance + confidence, and waits for human
review. You may NOT write to `data/canonical/` or `data/raw/`, and you may NOT mark a
candidate `asserted`/`canonical`. Editorial `\x` cross-references are NOT theological
edges — never relabel them as `quotesFrom`/`fulfills`/etc.

## What to mine (inputs — all already produced)

| Source | Found in | Discover |
|--------|----------|----------|
| Chunks + passages | `data/derived/chunks/`, `data/canonical/scripture/passages/` | thematic / discourse neighbors |
| Strong's WordTokens (677k) | `data/canonical/translations/eng-web/word_tokens.jsonl` | **lexical co-occurrence** (shared Strong's number across distant passages) |
| Footnotes + `\fqa` variants | `footnotes.jsonl`, `textual_variant` records | translation cruxes, variant-driven links |
| Editorial crossrefs (`\x`) | `editorial_cross_references.jsonl` | leads only — re-classify with evidence, never auto-promote |
| Classification axes | governance `bible-classification-taxonomy.md` | shared theme/speech-act/typology clusters |

## Predicates you may propose

Only from the registry (`config/governance/predicate_registry.yaml`):
`quotesFrom, alludesTo, echoes, fulfills, typifies, parallelTo, thematicallyRelatedTo, groundedIn`.
Each requires `assertion_mode: candidate` (per `schemas/relationship_object.schema.json`)
+ `evidence_refs`. Record the finer method (e.g. `inferred_ai_candidate`) in a
`discovery_method` field. (NOTE: the relationship_object enum {asserted,inferred,candidate}
and the classification_assignment 5-mode enum should be harmonized — tracked follow-up.)

## How to emit a candidate (the contract)

Write `RelationshipObject` records (schema: `schemas/relationship_object.schema.json`)
to `data/candidate/connections/<batch>.jsonl`:

```json
{"id":"cand:rel:Isa.53.5-alludedby-1Pet.2.24","type":"RelationshipObject",
 "subject_id":"scripture:1Pet.2.24","predicate":"alludesTo","object_id":"scripture:Isa.53.5",
 "assertion_mode":"candidate","discovery_method":"inferred_ai_candidate","confidence":0.6,
 "evidence_refs":["lexical:shared-wounds-healing","phrase:by-his-wounds-you-were-healed"],
 "provenance":{"created_by":"connection_discoverer","created_at":"...","method":"lexical+phrase"},
 "trust_zone":"candidate","status":"candidate"}
```

For extra-biblical links, the target is an `extra_biblical_source` (layer `context`) and
the edge MUST stay `candidate` + tradition-scoped — never a property of the passage.

## Method discipline (avoid garbage edges)

1. **Evidence or it didn't happen.** No edge without a concrete basis (shared Strong's
   id, shared rare phrase, explicit citation formula, shared semantic domain).
2. **Confidence honestly.** `inferred_ai_candidate` starts low; raise only with multiple
   independent evidence kinds.
3. **Precision over recall.** A few well-evidenced candidates beat thousands of
   `thematicallyRelatedTo` noise. Cap batches; rank by evidence strength.
4. **No tradition collapse.** A typological/fulfillment claim is tradition-scoped; tag it.
5. **De-dup against curated edges** before emitting (don't re-propose known cross-refs).

## Output (every run)

1. `data/candidate/connections/<date>-<method>.jsonl` — the candidate edges.
2. `discovery_report.md` — method, counts, top-20 by confidence, false-positive notes.
3. A handoff (`force_handoff.py`) + a `roadmap_event` (`connections_proposed`).
4. Run `python scripts/validate_all.py`. Do NOT mark anything `active`.

## Human promotion path

Human reviews candidates → promotes survivors to `asserted` (with review) via the
normal governed path (proposal → review → validation → promotion). Until then, retrieval
must treat candidate edges as weak and clearly labeled.
