# Codex Prompt Pack Review

Use this command when Cursor has completed a T410/T411+ non-authorizing research or review-prep
batch and Codex needs to review it.

## Read First

- Cursor handoff
- `cursor_notes_to_codex.md`
- `source_size_manifest.jsonl`
- `confidence_register.jsonl`
- `audit_log.jsonl`
- `claim_traceability_matrix.md`
- escalation packets
- `.ai/control/parallel_chunking_research_program.yaml`
- `.ai/control/cursor_to_codex_transparency_contract.yaml`
- `.ai/control/frontier_chunking_escalation_policy.yaml`
- `.ai/control/chunking_phase_completion_plan.yaml`

## Review Questions

- Did Cursor Stop before any authority or output change?
- Did Cursor expose source sizes, hashes, limitations, confidence, and claim traceability?
- Did Cursor avoid target selection, output, reviewed gold, child spans, route/evaluator changes,
  graph/retrieval/vector work, and theology authority?
- Are hard cases escalated?
- Can the next prompt pack be enriched from this work?
- Is the work ready for owner options, frontier review, edits, or deferral?

## Output

Codex should return approve, approve-with-edits, or reject for each deliverable, then identify the
next exact task gate.
