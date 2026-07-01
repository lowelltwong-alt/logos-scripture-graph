# Agent Routing Guide — Start Here Every Time

This guide makes any agent (especially lower-capability agents) **self-aware** of the project
and routes it correctly. It is not task-specific; it is the always-on navigation contract.

> **Rule 0:** Every agent ALWAYS starts at `AI_FRONT_DOOR.md`. No exceptions.

---

## Step 1 — Orient (read, in this order)

| Order | File | Tells you |
|-------|------|-----------|
| 1 | `AI_FRONT_DOOR.md` | Entry rules, modes, validation gates |
| 2 | `.ai/control/MASTER_CONTEXT.md` | **Why** the project exists (READ ONLY — never edit) |
| 3 | `.ai/control/PROJECT_STATUS.md` | **Where** we are now (phase, blockers, active task) |
| 4 | `.ai/control/DATA_MAP.md` | **What** data + pipeline endpoints exist (generated) |
| 4b | `.ai/control/RAW_SOURCE_INVENTORY.md` | **The actual raw documents** to be processed — markers, Strong's, `\wj`, `\fqa`, etc. **Mandatory before ingest/chunking/graph work.** |
| 5 | `ROADMAP_STATE.yaml` | Machine-readable task list + statuses |
| 6 | `.ai/handoffs/<active_task>/handoff.md` | **Your** exact next actions (active task in PROJECT_STATUS) |

After step 1 you should be able to answer: what is this repo, what phase, what is blocked, what files hold the data, what is my task.

---

## Step 2 — Claim a task

1. Find the active task in `PROJECT_STATUS.md` → "Active task".
2. Confirm scope in that task's handoff (`.ai/handoffs/T###/handoff.md`).
3. Declare a mode (`explore` / `plan` / `build` / `validate` / `review`).
4. Start a handoff:
   ```bash
   python scripts/agent/force_handoff.py --task-id <ID> --agent <name> --stage start
   ```
5. Check your role's allowed paths in `config/agents/agent_roles.yaml`. Stay in scope.

---

## Step 2.5 — Use the right model for the task

Route by **capability profile**, not by habit (`config/agents/model_routing.yaml`):

| Task kind | Profile | Examples |
|-----------|---------|----------|
| Design / judgment | **reasoner** | architecture, ADRs, schema design, canon/literary policy, gold sets |
| Bounded build | **executor** | implement-to-spec, tests, mechanical fixes, exhaustive audits |
| Chores | **orchestrator** | triage, summarization, doc path fixes |

- Which real model fills each profile **this month**: `.ai/control/MODEL_ROSTER.md`.
- **Security tier:** code touching `pipelines/ scripts/ schemas/ config/ .github/workflows/ data/raw/ .ai/control/` (sensitive) must come from an **approved-provider** model AND get human CODEOWNER review (see roster allowlist). Docs/handoffs are general-tier.
- If you are an **executor**-profile model and hit a design decision → write it in "Open questions" and stop. Do not guess.
- All AI output is `candidate` trust zone until a human promotes it — regardless of model.

---

## Step 2.6 — Multi-agent review cadence (chunking / autonomous prep)

If the task involves chunking prep, autonomous runs, or review-packet drafts, read:

| File | Purpose |
|------|---------|
| `.ai/control/multi_agent_review_cadence.yaml` | Canonical roles and frequencies |
| `.ai/control/agent_review_ledger.jsonl` | Last daily/weekly verdicts |
| `.ai/control/autonomous_corpus_processor.yaml` | Efficiency rules (stop when backlog empty) |

| If you are… | Cadence | Prompt / action |
|-------------|---------|-----------------|
| **Cursor** | Until backlog empty | `autonomous_run_queue.yaml` + task handoff; drafts in `agent_work/` only |
| **Codex** | ~daily on active prep branch | `.ai/prompts/codex_daily_prep_review_prompt.md` → `APPROVE_PREP` / `HOLD_WITH_FINDINGS` |
| **Claude Opus 4.8** | ~weekly on active program | `.ai/prompts/claude_weekly_architecture_chunking_audit_prompt.md` → architecture + chunking errors + Cursor/Codex rollup |
| **Owner** | Per batch before gold/output | Confirm docket; authorize gold/output only |

Operational role aliases: `config/agents/agent_roles.yaml` → `prep_agent`, `daily_integrator`, `weekly_architecture_auditor`.

---

## Step 2.7 — Scratch lane (fast prep worktree)

For experimental prep without running full `validate_all` on every commit:

| File | Purpose |
|------|---------|
| `.ai/control/scratch_lane_policy.yaml` | Allowed/forbidden paths, promotion packet contract |
| `.ai/scratch/submissions/_template/promotion_packet.yaml` | Copy to `SUB-###/` before promotion PR |
| `scripts/validate_scratch_scope.py` | Fast pre-commit check on `scratch/*` branches |
| `.ai/prompts/codex_promotion_packet_review_prompt.md` | Higher-tier review when promoting to `main` |

```bash
git worktree add ../logos-scratch -b scratch/<lane-name> origin/main
cd ../logos-scratch
python scripts/validate_scratch_scope.py
```

Promotion PRs **must** include a filled `promotion_packet.yaml` with `risk_summary` and `decisions[]` premortem fields.

---

## Step 3 — Work within guardrails

**Never:**
- Touch ingest/chunking/graph logic without first inspecting the real raw documents (`RAW_SOURCE_INVENTORY.md` + `python scripts/scan_raw_sources.py`). `validate_raw_coverage.py` fails CI on any unclassified marker.
- Edit `.ai/control/MASTER_CONTEXT.md` or `MASTER_CONTEXT.lock.yaml` (human-gated).
- Run `scripts/agent/approve_master_context.py` — that is the **human's** command, not an agent's.
  (The script's name blocklist does **not** make it agent-safe; using it is a governance violation
  even though it would not error. Real enforcement is CODEOWNERS + branch protection — see CP-1.)
- Touch `data/raw/` contents (immutable).
- Mutate canonical data outside an approved task.
- Promote editorial `\x` crossrefs to theological graph edges.
- Mark a task complete without a passing handoff + validation.

**If architecture feels wrong:** propose, don't refactor:
```bash
python scripts/agent/propose_master_context_change.py --agent <name> --summary "..." --body "..."
```

**Working notes** (non-authoritative) go in `.ai/context/agent_work/`.

> **CI green ≠ healthy.** As of T304, `validate_all.py` + pytest can pass while the chunker is
> broken (CHK-4) and canon metadata is missing (CANON-1). Do not read "gates green" as "everything
> works" — check `PROJECT_STATUS.md` blockers before trusting the build.

---

## Step 4 — Keep the map current (self-awareness contract)

If you change pipelines, schemas, or data outputs, you MUST regenerate the data/endpoint map:

```bash
python scripts/generate_data_map.py
```

This keeps `.ai/control/DATA_MAP.md` accurate so the next agent knows every endpoint and data file.

---

## Step 5 — Close out (before you stop)

1. Update your handoff: files read/changed, decisions, validation, risks, next instruction.
2. Update `.ai/control/PROJECT_STATUS.md` (phase/blockers/active task).
3. Update `ROADMAP_STATE.yaml` if status changed; append to `.ai/control/roadmap_events.jsonl`.
4. Update `.ai/control/current_focus.yaml` (active task pointer).
5. Regenerate `DATA_MAP.md` if data/pipelines changed.
6. Run the gates (must be green):
   ```bash
   python scripts/validate_all.py
   python -m pytest -q
   ```

If any gate is red, you are not done.

---

## Routing map (mental model)

```text
AI_FRONT_DOOR.md
   ├─ MASTER_CONTEXT.md ........ theory (human-gated, read-only)
   ├─ PROJECT_STATUS.md ........ current state (agents update)
   ├─ DATA_MAP.md .............. data + endpoints (generated)
   ├─ ROADMAP_STATE.yaml ....... task list
   └─ handoffs/T###/handoff.md . your task
          │
          ├─ scripts/validate_all.py ... gates (green/red)
          ├─ scripts/generate_data_map.py ... refresh map
          └─ scripts/agent/force_handoff.py ... handoff lifecycle
```

---

## Lower-level agent task menu (only if explicitly assigned)

These are safe, well-scoped tasks. Do NOT invent architecture or write ADRs.

| Task | Where | Acceptance |
|------|-------|------------|
| Fix doc path drift | `docs/workflows/INGESTION_WORKFLOW.md` | Paths match DATA_MAP.md |
| Add `.gitignore` entries | `.gitignore` | extracted/, caches ignored |
| Regenerate data map | `scripts/generate_data_map.py` | `DATA_MAP.md` updated; gates green |
| Add a fixture test | `tests/` | pytest passes; no flakiness |
| Wire a validation step | `.github/workflows/validate.yml` | CI green on PR |

For anything involving chunking design, schemas, canon, or master context: **escalate to Claude**, do not attempt.

---

## When stuck

1. Re-read `PROJECT_STATUS.md` and your handoff.
2. Check `DATA_MAP.md` for the real input/output paths.
3. If blocked by a decision, write it in your handoff "Open questions" and stop — do not guess on architecture.
