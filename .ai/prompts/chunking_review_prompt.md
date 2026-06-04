# Chunking Architecture Review Prompt

Use this prompt with Claude, GPT, or another review agent.

## Task

Review the Bible chunking architecture in this repo. Do not rewrite everything. Identify architectural errors, missing safeguards, weak assumptions, and implementation risks.

## Required files to read first

1. `AI_FRONT_DOOR.md`
2. `ROADMAP.md`
3. `ROADMAP_STATE.yaml`
4. `docs/architecture/ARCHITECTURE.md`
5. `docs/chunking/CHUNKING_DESIGN.md`
6. `docs/chunking/CHUNKING_RULES.md`
7. `config/chunking/chunking_policy.yaml`
8. `config/agents/agent_roles.yaml`
9. `schemas/chunk.schema.json`
10. `pipelines/chunking/chunker.py`

## Required output

Return a structured review with:

- `critical_findings`
- `recommended_changes`
- `missing_tests`
- `source_language_risks`
- `literary_form_risks`
- `implementation_risks`
- `files_to_modify`
- `proposed_adr_if_needed`

## Review standards

Evaluate whether the chunker:

- preserves source text immutability
- avoids sentence splits
- preserves USFM paragraph, poetry, headings, footnotes, and cross-reference signals
- treats verses as address units, not default meaning units
- supports Hebrew/Greek alignment later
- has provenance and boundary witness metadata
- separates canonical text from derived chunks
- can be validated by tests and reviewer gold sets

Do not expose private chain-of-thought. Provide concise reasoning and evidence-based recommendations.
