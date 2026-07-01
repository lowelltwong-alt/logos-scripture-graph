# Claude Weekly Architecture And Chunking Audit Prompt

Use this prompt about once per week while the multi-agent prep program is active.

## Goal

Perform a frontier architecture and chunking-error deep dive. Roll up Cursor prep throughput and all Codex daily verdicts since the last weekly audit. Do not authorize reviewed gold, chunk output, child spans, or owner decisions.

## Required reads

1. `.ai/control/multi_agent_review_cadence.yaml`
2. `.ai/control/agent_review_ledger.jsonl` (all entries since last `claude_weekly`)
3. `.ai/control/autonomous_corpus_processor.yaml`
4. `.ai/control/parallel_chunking_research_program.yaml`
5. Active prep handoffs and `.ai/context/agent_work/<TASK_ID>/`
6. `.ai/context/agent_work/T411/escalation_packets/` (open rollup)
7. `.ai/control/PROJECT_STATUS.md` and `ROADMAP_STATE.yaml` diffs since last weekly

## Architecture review (P0–P2)

1. Authority leakage from prep/review artifacts into chunk boundaries, reviewed gold, route behavior, graph/retrieval truth, or theology authority.
2. Control-plane drift between task files, handoffs, readiness maps, and roadmap state.
3. Parallel safety and task-scope boundary violations.
4. Rust observation substrate and ledger-first gate integrity.

## Chunking error pattern review

1. Route leakage / non-target identity risks in recent prep or output references.
2. Mid-sentence split, book-crossing, or orphan-marker patterns in discussed spans.
3. Reviewed-gold smuggling or implementation language in draft packets.
4. Evaluator or leaderboard misuse (improvement claims without formula change proof).
5. Child-span pressure where parent-only evidence is insufficient.

## Codex rollup

Review every `codex_daily` ledger entry since last weekly:

- Were HOLD findings resolved?
- Any APPROVE_PREP that should have been HOLD?
- Consistent non-authorization language across integrator work?

## Cursor rollup

- Candidates completed vs backlog remaining.
- Escalation packets properly referenced for theology-sensitive spans.
- Token efficiency: no evidence of whole-Bible raw reread or redundant control-plane rewrites.

## Verdict (required)

Return exactly one:

- `APPROVE_WEEKLY` — no blocking architecture or chunking-error findings.
- `HOLD_WITH_FINDINGS` — prep/integration should pause until addressed.
- `ESCALATE_OWNER` — owner decision needed before further prep or batch promotion.

## Outputs

1. Write `.ai/audits/reports/weekly/<DATE>-T420-weekly-architecture-chunking-audit.md` with P0/P1/P2 findings.
2. Append one JSONL line to `.ai/control/agent_review_ledger.jsonl`:

```json
{
  "review_tier": "claude_weekly",
  "date": "YYYY-MM-DD",
  "branch": "codex/t4xx-...",
  "task_id": "T420",
  "verdict": "APPROVE_WEEKLY",
  "reviewer": "claude-opus-4.8",
  "subjects_reviewed": ["cursor_prep", "codex_daily_verdicts", "architecture", "chunking_errors"],
  "finding_count_p0": 0,
  "finding_count_p1": 0,
  "finding_count_p2": 0,
  "audit_report_path": ".ai/audits/reports/weekly/<DATE>-T420-weekly-architecture-chunking-audit.md",
  "codex_daily_entries_reviewed_count": 0,
  "non_authorizing": true
}
```

3. Update active handoff `last_claude_weekly_review` and `claude_weekly_verdict`.

## Distinction from triggered escalation

This weekly audit is scheduled program health review. Triggered frontier escalation (prophecy, apocalyptic, WJ, variants, dense epistle argument) remains mandatory per `.ai/control/frontier_chunking_escalation_policy.yaml` before gold or output even if weekly audit passes.

## Non-authorizations

This weekly audit does not authorize reviewed gold promotion, chunk output, child spans, owner decisions, hold clearing, or theology authority.
