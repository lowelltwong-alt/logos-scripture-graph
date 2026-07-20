# Unknown Unknowns Radar Runbook

Use this runbook when the project is about to expand scope, acquire sources, run OCR, publish a claim, or wire manuscript evidence into future graph/retrieval systems.

## When To Run

- A new source family is proposed.
- A permission reply arrives.
- A download, mirror, OCR, transcription, embedding, or vector step is proposed.
- A public-facing page, email, or contributor artifact is drafted.
- A manuscript has mixed canon status, uncertain coverage, lacunae, corrections, marginalia, conflicting metadata, or OCR failure.
- Weekly while manuscript, patristic, or archaeology acquisition is expanding.

## Inputs

- Relevant task or source plan.
- Rights/provenance notes.
- Source catalog or IIIF/canvas metadata if available.
- Public claim draft if applicable.
- Prior known-known and known-unknown rows.

## Procedure

1. Name the triggering event.
2. List current known knowns with evidence anchors.
3. List known unknowns as answerable questions.
4. Generate suspected unknown unknowns by asking which expert family would notice a hidden problem.
5. For each suspected unknown unknown, name the failure mode, consequence if wrong, and required expert family.
6. Route each item:
   - `record_only`
   - `needs_rights_review`
   - `needs_source_cataloging`
   - `needs_scholarship_review`
   - `needs_archaeology_or_material_culture_review`
   - `needs_ocr_method_review`
   - `needs_owner_decision`
   - `block_until_resolved`
7. Send material outputs to Governance / Evidence Reviewer.

## Output Shape

```yaml
radar_item_id:
classification: known_known | known_unknown | suspected_unknown_unknown
domain_family:
claim_or_question:
why_it_matters:
evidence_anchor:
confidence: low | medium | high
consequence_if_wrong:
recommended_next_action:
required_expert_family:
authority_boundary:
owner_decision_required: true_or_false
```

## Promotion Rules

- Known known to project fact requires source URL, date observed, scope label, and no governance conflict.
- Known unknown to task requires a clear owner action or research target.
- Suspected unknown unknown to known unknown requires a named plausible failure mode and an evidence or expert-family rationale.
- Nothing becomes canon, graph, retrieval, OCR, embedding, or theology authority from this runbook.

## Stop Conditions

Stop and report if:

- the proposed next action needs source download, OCR, embeddings, public release, or email send without explicit authorization;
- a source-rights term is unclear;
- a boundary/non-66 source would enter default Scripture authority;
- the review requires ultra effort without Lowell's exact approval;
- a public claim depends on unresolved archaeology, textual criticism, or rights questions.

## Good First Radar Prompt

```text
Run the Unknown Unknowns Radar for [source/task/claim].

Inputs:
- [source URL or task file]
- [rights/provenance note]
- [intended use]

Produce:
- 5-10 known knowns
- 5-10 known unknowns
- 5-10 suspected unknown unknowns
- required expert families
- blocked actions
- next owner decision, if any

Do not download, OCR, store, embed, publish, send, or create graph/retrieval/canon/theology authority.
```
