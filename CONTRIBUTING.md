# Contributing

This repo is a **governed** Scripture-graph substrate. Every contributor — human or
AI agent — follows the same path. Governance is enforced at the gate (CI + CODEOWNERS),
not by trusting any model or person.

## 0. Start at the front door

**Read [`AI_FRONT_DOOR.md`](AI_FRONT_DOOR.md) first**, then the control plane it points to:
`.ai/control/MASTER_CONTEXT.md` (read-only theory) → `PROJECT_STATUS.md` → `DATA_MAP.md`.
Lower-capability agents: read [`.ai/handoffs/AGENT_ROUTING_GUIDE.md`](.ai/handoffs/AGENT_ROUTING_GUIDE.md).

## 1. `main` is protected — work via Pull Requests

Direct pushes to `main` are blocked. Every change lands through a PR that must:

- pass the **`validate`** CI check (re-ingests data, runs all gates + tests), and
- get **CODEOWNER review** (see [`.github/CODEOWNERS`](.github/CODEOWNERS)).

```bash
git checkout -b <type>/<short-description>   # feat/ fix/ docs/ chore/ roster/
# ... make changes ...
python scripts/validate_all.py && python -m pytest -q   # must be green locally first
git push -u origin <branch>
gh pr create   # describe what changed and why; link the task handoff
```

Do not merge your own PR without the required review. The maintainer
(@lowelltwong-alt) reviews and merges.

## 2. Agent swarms & access (important)

If you run AI agents (local, hosted, or swarms) against this repo:

- **Give agents fork or non-admin write access — never an admin token.** Branch
  protection only gates non-admins; an admin token bypasses it and defeats the
  whole control plane (see `docs/architecture/ADR-0009`).
- **All AI/bulk output is `candidate` trust zone** until a human promotes it. Never
  auto-promote generated artifacts to canonical/asserted.
- Untrusted/local-agent output must go through CI in isolation before merge.

## 3. Pick the right model (capability routing)

Route by **capability profile**, not habit — see
[`config/agents/model_routing.yaml`](config/agents/model_routing.yaml) and the dated
[`.ai/control/MODEL_ROSTER.md`](.ai/control/MODEL_ROSTER.md):

| Task | Profile |
|------|---------|
| architecture, ADRs, schema/canon/literary design, gold sets | **reasoner** |
| implement-to-spec, tests, mechanical fixes, audits | **executor** |
| triage, summarization, doc chores | **orchestrator** |

**Security tier:** code touching sensitive surfaces (`pipelines/ scripts/ schemas/
config/ .github/workflows/ data/raw/ .ai/control/`) must come from an **approved
provider** (see roster allowlist) **and** get CODEOWNER review. Docs/handoffs are
general-tier. Executor-profile models that hit a design decision must **escalate to a
reasoner-profile model**, not guess.

## 4. Task discipline (handoffs)

Non-trivial work needs a deterministic handoff:

```bash
python scripts/agent/force_handoff.py --task-id T### --agent <name> --stage start --mode <mode>
```

Update the handoff at the end (files changed, decisions, validation, next step), and
update `ROADMAP_STATE.yaml` + `.ai/control/PROJECT_STATUS.md` + append to
`.ai/control/roadmap_events.jsonl` if status changed. Task IDs must match `^T\d{3,}$`.

## 5. Data is regenerated, not committed

Canonical/processed data is gitignored (regenerable; see `DATA_MAP.md` + ADR-0007).
After cloning, regenerate before working with data:

```bash
pip install -e ".[validate,test]"
python pipelines/ingest/usfm_importer.py        # ~60s; rebuilds canonical + processed
python scripts/generate_data_map.py             # refresh DATA_MAP if data/pipelines changed
```

## 6. Hard rules (from MASTER_CONTEXT)

- Never edit `.ai/control/MASTER_CONTEXT.md` or its `.lock.yaml`; propose via
  `scripts/agent/propose_master_context_change.py`. Never run `approve_master_context.py`
  (human-only).
- `data/raw/` is immutable. Chunks are derived, never canonical truth.
- Editorial `\x` crossrefs stay `editorial_cross_reference` — never auto-promoted to
  theological graph edges.
- Publishing canonical data requires canon metadata (ADR-0005).

## 7. License

Code is MIT (see `LICENSE`). Ingested source texts keep their own licenses, recorded
in each `data/raw/**/source_manifest.yaml` (see `LICENSE_POLICY.md`).
