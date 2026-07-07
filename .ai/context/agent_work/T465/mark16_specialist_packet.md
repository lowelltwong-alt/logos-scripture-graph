# T465 Mark 16 Specialist Packet

Status: frontier/specialist review needed. Non-authorizing.

Source row: `DELTA-Mark-016`

Scopes:

- `Mark.16.1-Mark.16.20`
- `Mark.16.9-Mark.16.20`

Repo evidence used:

- `.ai/scratch/multi_model_bible_chunking/comparison/owner_decision_docket.yaml`
- `.ai/scratch/multi_model_bible_chunking/comparison/frontier_review_queue.jsonl`
- `.ai/control/textual_variant_source_tradition_dossier_queue.yaml`
- `eval/chunking_gold/review_packets/mark16_9_20_textual_variant_review.md`

## Why This Is A Specialist Case

T464 routes Mark 16 to frontier review with these risk flags:

- `high_risk_book`
- `low_confidence`
- `notes_or_variant_pressure`
- `sidecar_low_confidence_or_frontier`
- `strongs_original_language_metadata`
- `variant_hot_zone`
- `wj_or_red_letter`

The row also names specialist lanes for Codex Vaticanus layout review, Codex Sinaiticus ending review, major codex witness review, manuscript transmission history, Mark 16 longer-ending specialist review, original-language alignment review, scribal layout and blank-space review, scribal letters-per-column capacity review, textual-variant source-tradition review, and WJ/speaker discourse review.

## Current Repo Review Packet Baseline

The existing review packet at `eval/chunking_gold/review_packets/mark16_9_20_textual_variant_review.md` is pending human review. It proposes the longer-ending span as a review question but does not authorize output. It records source evidence from the available WEB surface only and explicitly says no external textual-critical data has been imported.

## Research-Needed Fields

These fields must be completed by a specialist/frontier task before any owner-gated chunking decision:

- Codex Vaticanus layout: whether the relevant blank-space/column layout exists, how large it is, and whether reconstructed text capacity arguments are methodologically sound.
- Codex Sinaiticus ending evidence: what the manuscript contains at the ending of Mark, what hands/corrections are relevant, and how the evidence should be represented without overclaiming.
- letters-per-line and letters-per-column capacity: measured or cited scribal-layout estimates, margin/column assumptions, and uncertainty.
- Other manuscript witnesses: major uncials, minuscules, versions, and lectionary or transmission evidence relevant to Mark 16:9-20.
- Patristic evidence: early citations or references, with date, geography, work, and confidence.
- Editorial history: how modern editions/translations flag the longer ending and where punctuation, paragraphing, headings, and red-letter/WJ formatting are editorial layers.
- Downstream chunking implications: whether a later owner packet should preserve `Mark.16.1-Mark.16.8` and `Mark.16.9-Mark.16.20` as distinct review spans, keep a larger `Mark.16.1-Mark.16.20` unit, or defer output until textual-critical evidence is represented.

## Chunking Implications

Mark 16 should not be chunked by simple model agreement, paragraph markers, WJ/red-letter markers, or Strong's metadata. A later task must separate:

- textual witness evidence,
- editorial formatting evidence,
- speaker/discourse evidence,
- reviewed-gold authority,
- and output authority.

If the longer ending is represented later, the representation must be transparent about variant status and witness support. It must not silently normalize a preferred reading or imply a source-tradition preference.

## Non-Authorizations

This packet authorizes no reviewed gold, chunk output, child spans, target selection, preferred reading, source-tradition choice, canon change, Mark 16 inspiration decision, route/evaluator behavior, graph/retrieval/vector truth, embedding/index work, or theology authority.
