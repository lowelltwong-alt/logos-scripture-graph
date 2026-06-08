# Task Handoff

## Task

- task_id: T327D
- title: Regenerate Chunks for Canonical 66 Baseline
- phase: phase_4
- status: complete

## Agent

- agent_name: Codex
- mode: build
- stage: final
- updated_at: 2026-06-08T22:10:00+00:00
- handoff_id: t327d-codex-20260608

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/RAW_SOURCE_INVENTORY.md
- .ai/control/METHODOLOGY_UPDATE_RULES.md
- docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md
- ROADMAP_STATE.yaml
- tests/test_chunker_gold.py
- tests/test_chunking_orchestrator.py
- eval/chunking_gold/per_form/psalms_gold_manifest.json
- eval/chunking_gold/per_form/psalms_gold_plan.md
- eval/chunking_gold/README.md
- eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md
- eval/chunking_gold/review_packets/REVIEW_PACKET_INDEX.md
- eval/chunking_gold/review_packets/review_packet_index.json
- pipelines/chunking/chunker.py
- pipelines/chunking/orchestrator.py
- pipelines/chunking/evaluate_chunks.py
- pipelines/chunking/leaderboard.py
- eval/chunking_runs/README.md
- docs/roadmap/T327C_REGENERATE_CANONICAL_66_OUTPUTS.md
- .ai/handoffs/T327C/handoff.md

## Files changed

- tests/test_chunker_gold.py
- tests/test_chunking_orchestrator.py
- eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md
- eval/chunking_gold/README.md
- eval/chunking_gold/per_form/psalms_gold_manifest.json
- eval/chunking_gold/per_form/psalms_gold_plan.md
- eval/chunking_gold/review_packets/REVIEW_PACKET_INDEX.md
- eval/chunking_gold/review_packets/review_packet_index.json
- eval/chunking_runs/README.md
- eval/chunking_runs/claude-opus-4.8__pass1__A_genre_default__20260605T034131Z.json
- eval/chunking_runs/claude-opus-4.8__pass1__B_genre_tight__20260605T034131Z.json
- eval/chunking_runs/claude-opus-4.8__pass1__C_naive_window__20260605T034131Z.json
- eval/chunking_runs/claude-opus-4.8__pass2__D_claude_pass2__20260605T112450Z.json
- eval/chunking_runs/claude-opus-4.8__pass2__D_claude_pass2_post_t327__20260608T215149Z.json
- eval/LEADERBOARD.md
- pipelines/chunking/leaderboard.py
- docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md
- docs/roadmap/T327D_REGENERATE_CHUNKS_BASELINE_RESET.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/roadmap_events.jsonl
- .ai/tasks/T327D.task.yaml
- .ai/handoffs/T327D/handoff.md
- ROADMAP_STATE.yaml

## Generated outputs

- data/derived/chunks/variants/claude-opus-4.8__pass2__D_claude_pass2_post_t327__20260608T215149Z/chunks.jsonl (ignored)
- build/t327d/D_claude_pass2_post_t327.jsonl (ignored inspection output)
- build/t327d/orchestrator_chunks.jsonl (ignored inspection output)
- build/t327d/route_ledger.jsonl (ignored inspection output)
- build/t327d/scores.json (ignored inspection output)
- build/t327d/report.md (ignored inspection output)

## Decisions made

- Confirmed T327C is merged on `main`.
- Confirmed canonical outputs contain 66 books and 31,103 passage/witness records.
- Regenerated the post-T327 D / Claude pass2 chunk output from the corrected 66-book canonical outputs.
- Updated the baseline chunk SHA to `4c4e4d1f62de1951d13327830f55031bfed4f3464e8c86d75cc2410053e93025`.
- Updated the post-T327 chunk count baseline to 1,131 chunks.
- Removed the two temporary T327C xfails from `tests/test_chunker_gold.py`.
- Removed `PrMan` and `Ps151` from canonical non-target poetry controls; retained canonical controls `Song` and `Lam`.
- Added `corpus_baseline` metadata to committed scorecards and leaderboard output.
- Marked pre-T327 scorecards as `pre_t327_wider_corpus`.
- Marked the new post-T327 scorecard as `post_t327_canonical_66_corpus`.
- Preserved the T314 evaluator formula; score movement is corpus-scope correction / baseline reset, not chunking improvement.
- Updated methodology with the reusable corpus-scope baseline reset rule.
- Did not start T327E/F/G.

## Validation run

- command: `python scripts/validate_canonical_66_scope.py data/canonical/scripture/passages/passages.jsonl data/canonical/translations/eng-web/translation_witnesses.jsonl data/canonical/translations/eng-web/boundary_claims.jsonl data/canonical/translations/eng-web/footnotes.jsonl data/canonical/translations/eng-web/editorial_cross_references.jsonl data/canonical/translations/eng-web/section_headings.jsonl data/canonical/translations/eng-web/glossary_entries.jsonl data/canonical/translations/eng-web/word_tokens.jsonl`
- result: passed, canonical 66 scope validation passed for 8 JSONL files.
- command: `python pipelines/chunking/chunker.py --passages data/canonical/scripture/passages/passages.jsonl --witnesses data/canonical/translations/eng-web/translation_witnesses.jsonl --boundary-claims data/canonical/translations/eng-web/boundary_claims.jsonl --footnotes data/canonical/translations/eng-web/footnotes.jsonl --crossrefs data/canonical/translations/eng-web/editorial_cross_references.jsonl --out data/derived/chunks/variants/claude-opus-4.8__pass2__D_claude_pass2_post_t327__20260608T215149Z/chunks.jsonl`
- result: passed, wrote 1,131 chunks.
- command: `python pipelines/chunking/evaluate_chunks.py D_claude_pass2_post_t327=build/t327d/D_claude_pass2_post_t327.jsonl --scorecard-dir eval/chunking_runs --agent claude-opus-4.8 --pass-num 2`
- result: passed, wrote post-T327 scorecard.
- command: `python pipelines/chunking/leaderboard.py`
- result: passed, post-T327 canonical-66 D / Claude pass2 row reports composite 93.6.
- command: `python scripts/validate_all.py`
- result: passed, all validation gates passed; handoff validation passed for 31 referenced paths,
  chunking gold validation passed for 1 manifest, canonical 66 scope validation passed for 8 JSONL
  files, and JSONL validation passed for 63,959 records.
- command: `python -m pytest -q`
- result: passed, `134 passed`.
- command: `git diff --check`
- result: passed.

## Known risks

- Existing stress atlas, observed audit, and review packet index surfaces may still mention non-66
  cases for historical or future boundary-literature cleanup. T327E owns that broader cleanup.
- The post-T327 scorecard is comparable within the canonical-66 corpus baseline only.
- The leaderboard ranks all rows mechanically, but its language now warns against treating pre/post
  corpus movement as chunking improvement.

## Open questions

- Whether T327E should preserve historical non-66 stress cases as boundary-literature candidates or
  move them entirely out of Scripture-side gold/stress surfaces.

## Next agent instruction

Claude review next. Merge if approved and green. Then run T327E only. Do not start T327F.
