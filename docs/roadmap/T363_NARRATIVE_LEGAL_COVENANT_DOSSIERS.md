---
object_type: roadmap_note
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-18 during T363 as non-output-changing research work after T358 Bible-wide research registry and T362 Gospel/WJ discourse dossiers."
reason_for_inclusion: "Explain the narrative/legal covenant dossier queue and its non-authorizing role before future narrative, law, covenant, graph, retrieval, evaluator, or chunking work resumes."
---

# T363 Narrative Legal Covenant Dossiers

## Purpose

T363 creates a research-only queue for narrative, legal, covenant, genealogy/list, royal-annal,
restoration-document, and Gospel birth-narrative review cases:

```text
.ai/control/narrative_legal_covenant_dossier_queue.yaml
```

The goal is to preserve scene, formula, list, document, and covenant evidence without letting those
features decide covenant theology, law/gospel framing, typology, harmonization, source-critical
partition, reviewed gold, or chunk boundaries.

## Research Cases

The initial queue records:

- `Gen.1-Gen.11`: primeval narrative and genealogy units.
- `Gen.12-Gen.50`: patriarchal covenant narrative cycles.
- `Exod.19-Exod.24`: Sinai covenant narrative and law complex.
- `Lev.1-Lev.7`: sacrifice and ritual law units.
- `Num.22-Num.24`: Balaam narrative and oracle complex.
- `Deut.5-Deut.30`: covenant speech, law, blessing, and curse units.
- `Josh.13-Josh.21`: land allotment and list units.
- `1Sam.8-1Sam.12`, `2Sam.7`, `1Kgs.3-1Kgs.11`, `1Kgs.17-2Kgs.8`: royal covenant,
  annal, temple, and prophetic-cycle units.
- `1Chr.1-1Chr.9`, `1Chr.22-1Chr.29`, `Ezra.1-Ezra.10`, `Neh.1-Neh.13`: genealogy,
  restoration, list, and embedded document units.
- `Matt.1-Matt.2`, `Luke.1-Luke.3`: Gospel genealogy and birth narrative units.

## Non-Authorization

T363 does not authorize:

- covenant theology or dispensational system selection
- law/gospel framework selection
- typological fulfillment boundaries
- Matthew/Luke harmonization
- source-critical partition
- chronology harmonization
- genealogy identity hierarchy
- reviewed-gold promotion
- chunk boundaries
- route behavior
- evaluator changes
- graph edges
- retrieval truth
- output changes
- boundary import
- T345

Future output-changing use of any dossier still requires exact passage scope, owner review,
reviewed gold or equivalent governed evidence, non-target identity proof, validators/tests, and a
later implementation-authorizing decision.

## Validation

T363 adds:

- `scripts/validate_narrative_legal_covenant_dossier_queue.py`
- `tests/test_narrative_legal_covenant_dossier_queue.py`

The validator fails closed if the queue authorizes covenant theology, output changes, chunk
boundaries, route behavior, graph edges, retrieval truth, or reviewed gold; loses required
evidence channels; drops required dossiers; or omits non-authorization guards.
