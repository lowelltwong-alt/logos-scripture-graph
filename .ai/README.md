# `.ai/` Control Surface

This directory is the AI coordination layer for the repo.

## Authority hierarchy

```text
MASTER_CONTEXT.md          ← human-gated theory (AI read-only)
PROJECT_STATUS.md          ← operational state (agents update)
handoffs/T###/handoff.md   ← task packets (agents update)
context/agent_work/        ← session notes (agents, non-authoritative)
context/recommendations/   ← master context proposals (agents)
```

It contains:

- deterministic handoffs
- human-gated master context + lock file
- project status and current focus
- task packets
- roadmap event logs
- prompts for structured review
- control metadata

Agents may write handoffs, PROJECT_STATUS, and context/ — but must **not** edit `MASTER_CONTEXT.md` or use this directory as a substitute for source manifests, schema, or canonical data.

Validation: `python scripts/validate_control_plane.py`
