# Task Handoff

## Task

- task_id: T353
- title: Divine Capitalization Inventory Harness
- phase: phase_4
- status: in_progress

## Agent

- agent_name: codex
- mode: implementation
- stage: start
- updated_at: 2026-06-17T23:58:00+00:00
- handoff_id: t353-start

## Files read

- AI_FRONT_DOOR.md
- .ai/control/current_focus.yaml
- .ai/control/PROJECT_STATUS.md
- .ai/control/chunking_agent_preflight.yaml
- .ai/control/bible_chunking_research_triage_map.yaml
- .ai/control/chunking_theological_decision_register.yaml
- .ai/control/harness_upgrade_roadmap.yaml
- .ai/tasks/T352.task.yaml
- ROADMAP_STATE.yaml
- data/canonical/translations/eng-web/word_tokens.jsonl
- data/canonical/translations/eng-web/translation_witnesses.jsonl

## Files changed

- .ai/control/divine_capitalization_inventory.yaml
- scripts/build_divine_capitalization_inventory.py
- scripts/validate_divine_capitalization_inventory.py
- tests/test_divine_capitalization_inventory.py
- .ai/control/chunking_agent_preflight.yaml
- scripts/validate_chunking_agent_preflight.py
- scripts/validate_task_scope.py
- tests/test_chunking_agent_preflight.py
- .ai/control/chunking_theological_decision_register.yaml
- docs/roadmap/T353_DIVINE_CAPITALIZATION_INVENTORY_HARNESS.md
- .ai/tasks/T353.task.yaml
- .ai/handoffs/T353/handoff.md
- ROADMAP_STATE.yaml
- .ai/control/current_focus.yaml
- .ai/control/PROJECT_STATUS.md
- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md
- .ai/control/harness_upgrade_roadmap.yaml
- scripts/validate_all.py
- tests/test_task_scope_validator.py
- .ai/control/roadmap_events.jsonl
- .ai/control/handoff_ledger.jsonl

## Decisions made

- Record capitalization variants as observed evidence only, not authority.
- Treat pronoun capitalization as broad evidence only; T353 does not infer referent identity.
- Preserve Strong's-style numbers as source metadata evidence only; T353 does not infer lexical truth.
- Use translation witness text for phrase observations because some phrase surfaces, such as Alpha/Omega language, can be present in witness text without a corresponding standalone word-token surface.
- Stack T353 after T352 so the intended merge order is T352 first, then the capitalization inventory harness.

## Validation run

- pending

## Known risks

- The inventory is a watchlist, not an exhaustive theology of divine names.
- Future agents might overread counts or Strong's-style numbers unless the validator and preflight remain mandatory.
- PR69/T352 must merge before this stacked branch is retargeted to main.

## Open questions

- Which exact capitalization observation, if any, should later become a human-reviewed graph or retrieval policy?
- Should future Hebrew/Greek alignment add lemma-scoped review packets for a subset of these observations?

## Next agent instruction

Continue T353 only as a non-output-changing harness. Regenerate the inventory with
`python scripts/build_divine_capitalization_inventory.py --write` if canonical token or witness
data changes, then run the T353 validation commands. Do not implement graph edges, retrieval truth,
chunk boundaries, speaker attribution, reviewed gold, or output changes from capitalization.
