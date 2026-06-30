# Low-Risk Chunking Candidate

Use Cursor Plan mode unless a Codex-reviewed task already gives exact write paths.

Input required:

- exact candidate id;
- exact parent span;
- owner or Codex instruction that supplied the target.

Check `.ai/control/cursor_low_risk_chunking_handoff.yaml` and the T402 queue. Continue only if the
candidate status is `ready_for_review_packet` and no stop condition applies.

Stop immediately if Cursor would need to choose the target, add child spans, change chunk output,
change route/evaluator behavior, touch raw/canonical/processed/derived/eval-gold data, run
embeddings, build indexes, generate graph edges, import boundary material, choose a backend, promote
a retrieval profile, add source rows, or make theology authority claims.
