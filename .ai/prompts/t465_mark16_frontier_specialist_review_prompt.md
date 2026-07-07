# T465 Mark 16 Frontier Specialist Review Prompt

You are Claude/frontier reviewing a non-authorizing Mark 16 specialist packet for Logos Scripture Graph.

Read first:

- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md` as read-only
- `.ai/control/t465_multi_model_reconciliation_gate.yaml`
- `.ai/context/agent_work/T465/mark16_specialist_packet.md`
- `.ai/scratch/multi_model_bible_chunking/comparison/frontier_review_queue.jsonl`
- `.ai/control/textual_variant_source_tradition_dossier_queue.yaml`
- `eval/chunking_gold/review_packets/mark16_9_20_textual_variant_review.md`

Scope:

- Review `Mark.16.1-Mark.16.20` and `Mark.16.9-Mark.16.20` as a textual-critical, codex-layout, and downstream-chunking risk case.
- Do not make a chunk-output task.
- Do not select a preferred reading, source tradition, canon status, or inspiration status.
- Do not promote reviewed gold, create child spans, alter route/evaluator behavior, create graph/retrieval/vector truth, run embeddings, or build indexes.

Questions:

1. Does the packet correctly separate repo evidence from research-needed fields?
2. What exact evidence must be gathered for Codex Vaticanus blank-space/layout claims, including letters-per-line, letters-per-column, and column-capacity arguments?
3. What exact evidence must be gathered for Codex Sinaiticus ending evidence, corrections, hands, or scribal context?
4. Which other manuscript, versional, lectionary, and patristic witnesses should a later source-catalog task include?
5. How should downstream chunking represent variant status transparently without deciding inspiration, canon, or preferred reading?
6. Does WJ/red-letter or speaker/discourse metadata introduce any additional boundary risk?
7. Are there P0/P1/P2 findings in the T465 packet or control policy?

Return:

- approve / approve-with-edits / reject
- P0/P1/P2 findings
- required edits before any owner-gated review-packet strengthening
- recommended specialist evidence fields and citations to collect later
- confirmation that no chunk output, reviewed gold, source-tradition choice, canon change, or theology authority is authorized
