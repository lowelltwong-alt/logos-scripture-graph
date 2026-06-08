# Task Handoff

## Task

- task_id: T327C
- title: Regenerate Canonical 66 Outputs
- phase: phase_4
- status: complete

## Agent

- agent_name: Codex
- mode: build
- stage: final
- updated_at: 2026-06-08T22:45:00+00:00
- handoff_id: t327c-codex-20260608

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/RAW_SOURCE_INVENTORY.md
- ROADMAP_STATE.yaml
- pipelines/ingest/usfm_importer.py
- pipelines/ingest/usfm_inline_parser.py
- pipelines/util/usfm_to_osis.py
- scripts/validate_all.py
- scripts/generate_data_map.py
- tests/test_t327b_canonical_66_ingest_filter.py
- docs/roadmap/T327B_CANONICAL_66_INGEST_FILTER.md
- docs/roadmap/T327B1_CANONICAL_SCOPE_VALIDATOR_FAIL_CLOSED.md

## Files changed

- data/canonical/scripture/passages/passages.jsonl (ignored generated output, regenerated locally)
- data/canonical/translations/eng-web/translation_witnesses.jsonl (ignored generated output, regenerated locally)
- data/canonical/translations/eng-web/boundary_claims.jsonl (ignored generated output, regenerated locally)
- data/canonical/translations/eng-web/footnotes.jsonl (ignored generated output, regenerated locally)
- data/canonical/translations/eng-web/editorial_cross_references.jsonl (ignored generated output, regenerated locally)
- data/canonical/translations/eng-web/section_headings.jsonl (ignored generated output, regenerated locally)
- data/canonical/translations/eng-web/glossary_entries.jsonl (ignored generated output, regenerated locally)
- data/canonical/translations/eng-web/word_tokens.jsonl (ignored generated output, regenerated locally)
- pipelines/ingest/usfm_importer.py
- scripts/validate_all.py
- .github/workflows/validate.yml
- tests/test_t327b_canonical_66_ingest_filter.py
- .ai/control/DATA_MAP.md
- docs/roadmap/T327C_REGENERATE_CANONICAL_66_OUTPUTS.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/roadmap_events.jsonl
- .ai/tasks/T327C.task.yaml
- .ai/handoffs/T327C/handoff.md
- ROADMAP_STATE.yaml

## Decisions made

- Confirmed T327B and T327B.1 are merged on `main`.
- Regenerated canonical outputs with `--canonical-66-filter`.
- Directed processed USFM reports to ignored `build/t327c_processed/usfm` to avoid updating
  processed outputs in this task.
- Added book identity to canonical sidecars emitted before a verse scope so fail-closed validation
  can validate boundary claims, section headings, and non-verse inline sidecars.
- Updated CI regeneration to use `--canonical-66-filter`.
- Updated `validate_all` to run canonical-scope validation over present canonical outputs and
  sidecars, including boundary claims and word tokens.
- Added temporary `pytest.mark.xfail(strict=False)` quarantine markers to exactly two chunk-gold
  tests with expected T327D fallout.
- Did not regenerate chunks, leaderboard, scorecards, or gold/stress/index surfaces.
- Did not start T327D/E/F/G.

## Validation run

- command: `python scripts/validate_canonical_66_scope.py data/canonical/scripture/passages/passages.jsonl data/canonical/translations/eng-web/translation_witnesses.jsonl data/canonical/translations/eng-web/boundary_claims.jsonl data/canonical/translations/eng-web/footnotes.jsonl data/canonical/translations/eng-web/editorial_cross_references.jsonl data/canonical/translations/eng-web/section_headings.jsonl data/canonical/translations/eng-web/glossary_entries.jsonl data/canonical/translations/eng-web/word_tokens.jsonl`
- result: passed, canonical 66 scope validation passed for 8 JSONL files.
- command: `python -m pytest -q tests/test_t327b_canonical_66_ingest_filter.py tests/test_web_usfm_feature_extraction.py`
- result: passed, `16 passed`.
- command: `python scripts/generate_data_map.py --check`
- result: passed, DATA_MAP.md is current.
- command: `python scripts/validate_all.py`
- result: passed, all validation gates passed; canonical-scope validation passed for 8 JSONL files and JSONL validation passed for 63,959 records.
- command: `python scripts/validate_schemas.py data/canonical/scripture/passages/passages.jsonl data/canonical/translations/eng-web/translation_witnesses.jsonl data/canonical/translations/eng-web/footnotes.jsonl data/canonical/translations/eng-web/section_headings.jsonl data/canonical/translations/eng-web/editorial_cross_references.jsonl data/canonical/translations/eng-web/glossary_entries.jsonl`
- result: passed.
- command: `python scripts/validate_schemas.py --limit 5000 data/canonical/translations/eng-web/word_tokens.jsonl`
- result: passed.
- command: `python pipelines/chunking/chunker.py --passages data/canonical/scripture/passages/passages.jsonl --witnesses data/canonical/translations/eng-web/translation_witnesses.jsonl --out build/t327c_ci_chunks.jsonl`
- result: passed, wrote 866 chunks.
- command: `python -m pytest -q`
- result: passed with expected temporary quarantine, `132 passed, 2 xfailed`.
- command: `git diff --check`
- result: passed.

## Known risks

- T327D must regenerate chunks and update score/baseline language after the canonical corpus shrink.
- T327D must remove the two temporary xfails or convert them back to normal assertions after
  regenerating chunks and updating gold/baseline expectations.
- Existing committed scorecards/leaderboard and gold/stress/review-packet surfaces may still refer
  to the pre-T327C wider corpus until T327D/T327E.
- Future score movement is corpus-scope correction / baseline reset, not chunking improvement.

## Open questions

- Whether T327D should update chunk/gold tests in one PR or split score/baseline language from
  chunk-output regeneration.

## Next agent instruction

Claude review next. Merge if approved and green. Then run T327D only. Do not combine T327D with
T327E/F.
