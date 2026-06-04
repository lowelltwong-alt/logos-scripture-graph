# Task Handoff

## Task

- task_id: T201
- title: Implement Patch 2A WEB Classic USFM embedded feature extraction
- phase: phase_2
- status: complete

## Agent

- agent_name: Codex
- mode: build
- stage: final
- updated_at: 2026-06-03T17:15:00+00:00
- handoff_id: T201-codex-final-amended

## Files read

- AI_FRONT_DOOR.md
- ROADMAP.md
- ROADMAP_STATE.yaml
- HANDOFF_PROTOCOL.md
- CLAUDE.md
- AGENTS.md
- docs/architecture/ARCHITECTURE.md
- docs/chunking/CHUNKING_DESIGN.md
- docs/chunking/CHUNKING_RULES.md
- docs/chunking/LITERARY_POLICIES.md
- config/chunking/chunking_policy.yaml
- schemas/*.json
- pipelines/ingest/usfm_importer.py
- tests/fixtures/usfm/JHN.usfm
- data/raw/bible/eng-web/source_manifest.yaml (created by T100/claude)

## Files changed (amended 2026-06-03)

- ROADMAP_STATE.yaml
- .ai/control/roadmap_events.jsonl
- .ai/control/handoff_ledger.jsonl
- .ai/handoffs/T201/handoff.md
- pipelines/ingest/usfm_inline_parser.py
- pipelines/ingest/usfm_importer.py
- pipelines/util/usfm_to_osis.py
- scripts/validate_jsonl.py
- schemas/scripture_passage.schema.json
- schemas/translation_witness.schema.json
- schemas/word_token.schema.json
- schemas/footnote.schema.json
- schemas/editorial_cross_reference.schema.json
- schemas/section_heading.schema.json
- schemas/boundary_claim.schema.json
- schemas/glossary_entry.schema.json
- schemas/usfm_event.schema.json
- schemas/unsupported_usfm_marker.schema.json
- tests/test_usfm_inline_parser.py
- tests/test_web_usfm_feature_extraction.py
- data/processed/bible/eng-web/usfm/extracted/
- data/processed/bible/eng-web/usfm/extraction_manifest.yaml
- data/processed/bible/eng-web/usfm/parser_report.yaml
- data/processed/bible/eng-web/usfm/usfm_events.jsonl
- data/processed/bible/eng-web/usfm/unsupported_usfm_markers.jsonl
- data/canonical/scripture/passages/passages.jsonl
- data/canonical/translations/eng-web/translation_witnesses.jsonl
- data/canonical/translations/eng-web/word_tokens.jsonl
- data/canonical/translations/eng-web/footnotes.jsonl
- data/canonical/translations/eng-web/editorial_cross_references.jsonl
- data/canonical/translations/eng-web/section_headings.jsonl
- data/canonical/translations/eng-web/boundary_claims.jsonl
- data/canonical/translations/eng-web/glossary_entries.jsonl

## Decisions made

- Implemented a deterministic inline parser that strips readable TranslationWitness text and emits sidecar records for word tokens, footnotes, editorial crossrefs, structural events, boundary evidence, section headings, unsupported markers, and glossary entries.
- Preserved raw marker strings in sidecar/audit records while ensuring TranslationWitness.text does not contain raw USFM markers.
- Treated USFM structural markers as future chunking evidence, not canonical ancient boundaries.
- Used explicit OSIS mapping for the 81 content files in the WEB archive, including deuterocanonical/additional books present in the archive without making a canon claim.
- Kept task status in_progress because the required source manifest path is missing and data/raw is immutable for this task.
- **Amended 2026-06-03:** T100 closed the manifest blocker; T201 is now complete. Full ingest re-run passes with manifest.

## Validation run

- command: python pipelines\ingest\usfm_importer.py
- result: passed; generated canonical and processed outputs
- command: python scripts\validate_jsonl.py data\canonical\scripture\passages\passages.jsonl data\canonical\translations\eng-web\translation_witnesses.jsonl data\canonical\translations\eng-web\word_tokens.jsonl data\canonical\translations\eng-web\footnotes.jsonl data\canonical\translations\eng-web\editorial_cross_references.jsonl data\canonical\translations\eng-web\section_headings.jsonl data\canonical\translations\eng-web\boundary_claims.jsonl data\canonical\translations\eng-web\glossary_entries.jsonl data\processed\bible\eng-web\usfm\usfm_events.jsonl data\processed\bible\eng-web\usfm\unsupported_usfm_markers.jsonl
- result: passed; JSONL validation passed for 864904 records
- command: python scripts\validate_repo.py
- result: passed
- command: python scripts\agent\validate_handoffs.py
- result: passed after final handoff update; 5 referenced handoff path(s)
- command: python pipelines\validate\validate_manifest.py data\raw\bible\eng-web\source_manifest.yaml
- result: passed (2026-06-03, post-T100)
- command: python -m pytest -q
- result: passed; 5 passed in 0.32s

## Known risks

- data/raw/bible/eng-web/source_manifest.yaml was absent; **resolved by T100**.

## Open questions

- Should non-verse FRT footnotes remain in the same Footnote stream with null passage_id, or move to a source-frontmatter sidecar in a later patch?
- Should generated sidecar files be partitioned by book before review, or is one JSONL file per record type acceptable for Patch 2A?
- Who should create data/raw/bible/eng-web/source_manifest.yaml — **resolved: T100/claude**.

## Next agent instruction

T201 complete. Ingest is closed for WEB Classic. Next: `.ai/handoffs/T301/handoff.md` (chunking + governance).
