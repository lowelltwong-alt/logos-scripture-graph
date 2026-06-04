# Agent Context Layer (not master authority)

This directory holds **agent-writable** context. It is NOT a substitute for `MASTER_CONTEXT.md`.

## Structure

```text
.ai/context/
  README.md              ← this file
  agent_work/            ← agents write session notes freely
  recommendations/       ← proposals to amend MASTER_CONTEXT (human promotes)
```

## Rules

| Path | AI may write? | Becomes canonical? |
|------|---------------|-------------------|
| `../control/MASTER_CONTEXT.md` | **NO** | Yes (human-gated) |
| `../control/PROJECT_STATUS.md` | Yes (after tasks) | Yes (operational) |
| `../handoffs/T###/handoff.md` | Yes (task scope) | Yes (task state) |
| `agent_work/` | Yes | No — working notes only |
| `recommendations/` | Yes (via propose script) | No — until human promotes |

## Propose a master context change

```bash
python scripts/agent/propose_master_context_change.py \
  --agent claude \
  --summary "One-line reason" \
  --body-file path/to/rationale.md
```

Human reviews file in `recommendations/`, edits `MASTER_CONTEXT.md` if approved, recomputes lock:

```bash
python scripts/agent/approve_master_context.py --approved-by "Your Name"
```
