# Next Book Or Stop

Use this checkpoint after each book in a Cursor T410/T411+ batch.

## Continue To Next Book If

- all required files are read or explicitly listed as not read
- per-book ledger is complete
- `cursor_notes_to_codex.md` is current
- `source_size_manifest.jsonl` has the book/source rows
- `confidence_register.jsonl` has confidence for all claims
- `audit_log.jsonl` records commands/actions and results
- `claim_traceability_matrix.md` links claims to evidence
- escalation packets exist for hard, low-confidence, or blocked issues
- no prohibited authority or output work occurred
- all records remain non-authorizing

## Stop And Report If

- Cursor would need to choose a target
- evidence is missing for a claim that controls the boundary
- source metadata would become boundary authority
- a textual variant, source tradition, WJ/speaker boundary, apocalyptic symbol, doxology, or
  doctrinal pressure controls the decision
- validation fails
- output, reviewed gold, child spans, route/evaluator changes, graph/retrieval/vector work,
  source rows, canon changes, or theology authority would be required

## Report Shape

State one of:

- `continue_next_book`
- `continue_next_book_with_escalation_packet`
- `stop_for_codex_review`
- `stop_for_owner_gate`
- `stop_for_frontier_review`
- `defer_to_phase_two_or_later`
