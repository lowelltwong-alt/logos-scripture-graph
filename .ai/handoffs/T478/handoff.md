# Task Handoff

## Task

- task_id: T478
- title: Cursor Rights-Gated Codex Image And Metadata Acquisition Prompt
- phase: phase_5
- status: complete

## Agent

- agent_name: codex
- mode: governed_prompt_authoring
- stage: start
- updated_at: 2026-07-18T03:40:43+00:00
- handoff_id: 719b3b562b43bd5a

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/primary_witness_acquisition_waves.yaml
- .ai/control/leipzig_sinaiticus_split_corpus_plan.yaml
- .ai/control/manuscript_source_catalog_research_packet.yaml
- data/raw/primary_witnesses/greek_codices/codex_sinaiticus/leipzig/0000061851/showcase/source_manifest.yaml
- docs/roadmap/T476_LOGOS_NAS_PHASE2A_EXECUTION_PLAN.md
- docs/roadmap/T477_UNAS_AI_WORKSPACE_ARCHITECTURE.md
- .ai/tasks/T477.task.yaml
- .ai/handoffs/T477/handoff.md
- C:/Users/lowel/.codex/skills/dad-work-router/SKILL.md
- C:/Users/lowel/.codex/skills/dad-agent-skill-forge/SKILL.md
- C:/Users/lowel/.codex/skills/portable-capability-governance/SKILL.md

## Files changed

- .ai/tasks/T478.task.yaml
- .ai/prompts/cursor_leipzig_codex_full_image_and_metadata_acquisition_prompt.md
- docs/roadmap/T478_CURSOR_RIGHTS_GATED_CODEX_IMAGE_ACQUISITION_PROMPT.md
- .ai/handoffs/T478/handoff.md
- .ai/control/handoff_ledger.jsonl
- .ai/control/PROJECT_STATUS.md

## Decisions made

- Confirmed through the local drive mapping that Z: has DisplayRoot `\\UNAS-Pro\AI.Workspace`; the Cursor prompt must independently reverify this before writing.
- Treated Lowell's latest instruction as execution authorization for a new Cursor acquisition task, not as authorization for T478 itself to download artifacts.
- Authorized the Leipzig-held/digitized Codex Sinaiticus set immediately from the library's exact written PDM 1.0 scope.
- Required a complete exact-source rights ledger before any additional image source can be acquired; public visibility, no-login access, or a planning label is not sufficient.
- Required factual metadata-only cataloging for other tracked codices when image rights do not pass the complete gate.
- Separated immutable NAS source originals, normalized catalogs, manifests, provenance, staging, and quarantine; large binaries never enter Git or OneDrive.
- Made the transfer resumable and bounded at 20 elapsed hours, with progress checkpoints, residual accounting, safe collision handling, and exact status/verify/resume commands.
- Kept OCR, transcription, embeddings, model training, canon decisions, Scripture authority, publication, and redistribution outside scope.
- Classified the result as a Cursor runtime adapter with a provider-neutral acquisition/rights/provenance core; no cross-provider promotion claim was made.

## Validation run

- command: `Get-PSDrive -Name Z`
- result: pass; Z: DisplayRoot is `\\UNAS-Pro\AI.Workspace`
- failures: direct root enumeration was denied by the current sandbox, so T478 performed no NAS content read or write; the prompt requires Cursor to repeat the identity and front-door checks in its authorized execution environment.

- command: targeted prompt guardrail scan
- result: pass; found the 20-hour limit, Z: DisplayRoot check, 500 GiB reserve, permission gate, no-OCR boundary, no-overwrite behavior, and resumable completion state.
- failures: none

- command: `git diff --check` over T478 files
- result: pass
- failures: none

- command: `python scripts/validate_task_scope.py` for the six declared T478 change surfaces
- result: pass
- failures: none

- command: `python scripts/agent/validate_handoffs.py`
- result: pass for 120 referenced handoff paths
- failures: none

- command: repository-wide `python scripts/validate_all.py` and `python -m pytest -q`
- result: coverage unavailable in this run
- failures: the initial concurrent attempt timed out after 64 seconds without output; a single isolated `validate_all.py` process then exceeded a 184-second bound without yielding output. Per the iteration-optimizer policy, the unchanged expensive gate was not repeated again. Targeted T478 validation remained green.

## Known risks

- Cursor remains responsible for actually implementing, running, monitoring, and verifying the acquisition; T478 creates no downloader and downloads no artifact.
- Network endpoints or IIIF structures may change. The execution prompt captures the manifest immutably, detects drift, and stops rather than silently broadening scope.
- A long-running Cursor session can still be interrupted by the host or application. The prompt therefore requires durable checkpoints and a clean resume command.
- Public-domain and open-license status for non-Leipzig candidates must be reverified at exact object/file scope before acquisition.

## Open questions

- After Lowell pastes the prompt into Cursor Agent mode, Cursor should allocate a new unused task ID and clean isolated worktree, then execute the Leipzig acquisition and metadata catalog under the prompt's gates.

## Next agent instruction

Paste `.ai/prompts/cursor_leipzig_codex_full_image_and_metadata_acquisition_prompt.md` into Cursor Agent mode at the repository root. Let Cursor run its preflight, create a clean task worktree, verify Z:, and continue through acquisition/verification for up to 20 hours.

---

## Handoff refresh: final

- agent_name: codex
- mode: 
- updated_at: 2026-07-18T03:45:26+00:00
- handoff_id: af3543cc157f4144

---

## Handoff refresh: final

- agent_name: codex
- mode: 
- updated_at: 2026-07-18T03:52:37+00:00
- handoff_id: af3543cc157f4144
