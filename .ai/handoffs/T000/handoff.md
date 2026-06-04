# Task Handoff

## Task

- task_id: T000
- title: Establish AI front door and deterministic handoff protocol
- phase: phase_0
- status: in_progress

## Agent

- agent_name: scaffold_generator
- mode: build
- started_at: 2026-05-28
- completed_at: 2026-05-28

## Files read

- source architecture notes from uploaded project pack

## Files changed

- scaffold initialized

## Decisions made

- deterministic handoff path is `.ai/handoffs/<task_id>/handoff.md`
- raw Bible sources go under `data/raw/bible/`
- chunking policy is configured under `config/chunking/chunking_policy.yaml`

## Validation run

- command: python scripts/validate_repo.py
- result: pending user run
- failures: none known at scaffold creation

## Known risks

- importer and chunker are scaffolds, not production-grade parsers yet
- source-language alignment is planned but not implemented

## Open questions

- exact Hebrew/Greek source packages to adopt first
- whether to track public-domain raw zips in Git or external artifact storage

## Next agent instruction

Start with T002 or T100: drop `eng-web_usfm.zip`, create `source_manifest.yaml`, compute checksum, and run manifest validation.
