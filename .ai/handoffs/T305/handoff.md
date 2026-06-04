# Task Handoff — T304 finding remediation (fix-all sprint)

## Task

- task_id: T305
- title: Remediate T304 findings (CHK-4, CANON-1, CP-1/CP-2, CI, GIT-1, schemas, docs)
- phase: phase_3
- status: complete

## Agent

- agent_name: claude-4.8-opus
- mode: build
- stage: final
- updated_at: 2026-06-04T12:20:00+00:00
- handoff_id: eeeed985cb999a7b
- builds_on: T304 (review)

## Files read

- All control-plane + review files per AI_FRONT_DOOR order (MASTER_CONTEXT, PROJECT_STATUS, DATA_MAP, T301–T304).
- `pipelines/ingest/usfm_importer.py`, `usfm_inline_parser.py`, `pipelines/util/usfm_to_osis.py`, `pipelines/chunking/chunker.py`.
- `scripts/validate_*.py`, `scripts/agent/*.py`, `.github/workflows/validate.yml`, `pyproject.toml`, `.gitignore`.

## Files changed

**New:**
- `pipelines/util/canon.py` — authoritative canon-profile + testament helper (dependency-free)
- `config/canon/canon_profiles.yaml` — human-readable canon mirror
- `config/governance/predicate_registry.yaml` — PRED-GAP relationship predicate registry
- `schemas/canon_profile.schema.json`, `schemas/text_span.schema.json`, `schemas/context_packet.schema.json`
- `scripts/validate_schemas.py` — best-effort JSON Schema validation (jsonschema optional)
- `tests/test_chunker_smoke.py` — CHK-4 regression guard (2 tests)
- `docs/architecture/ADR-0005-canon-profiles.md`, `ADR-0007-provenance-canonicalization.md`, `ADR-0009-control-plane-enforcement.md`
- `LICENSE` (MIT for code; data licensed per source manifest)
- `docs/patches/web_usfm_patch_2a/` (moved from repo root)

**Modified:**
- `pipelines/ingest/usfm_importer.py` — emits `canon_profiles` + `testament` on every passage (CANON-1)
- `pipelines/chunking/chunker.py` — **CHK-4 fixed**: joins passages + witnesses by `passage_id`; `--passages`/`--witnesses` CLI; policy version in chunk id; reads policy version
- `scripts/agent/force_handoff.py` — interpolates `--mode`; enforces `^T\d{3,}$` task id
- `scripts/validate_control_plane.py` — **CP-2 fixed**: structural task parser (PyYAML + fallback), fail-closed
- `scripts/agent/approve_master_context.py` — records `approved_commit`; documents tamper-evidence (CP-1)
- `scripts/validate_jsonl.py` — `--translation-id` (SCHEMA-LOCK), `--require-canon` (CANON-1 guard)
- `scripts/validate_all.py` — adds manifest gate + conditional JSONL/canon gate
- `scripts/generate_data_map.py` — schema contracts + validation endpoints + `--check` staleness mode + LFS flagging
- `.github/CODEOWNERS` — master-context + lock entries (CP-1 forge enforcement)
- `.github/workflows/validate.yml` — install deps, regen ingest, raw tripwire, manifest+JSONL+schema+chunker+DATA_MAP gates, pytest
- `pyproject.toml` — `[validate]` + `[test]` optional extras
- `docs/workflows/INGESTION_WORKFLOW.md` — corrected importer/chunker paths
- `.gitignore` — exclude regenerable generated data
- `.ai/control/{PROJECT_STATUS,DATA_MAP,current_focus,roadmap_events}`, `ROADMAP_STATE.yaml`

## Decisions made

- **Commit policy:** raw zip + code + schemas + configs + docs + control committed; generated
  canonical/processed data gitignored (regenerable; CI regenerates from raw). Resolves GIT-1 +
  the 432 MB token-file problem. (ADR-0007 direction; T304 Q1.)
- **Canon:** authoritative mapping in Python (`canon.py`), YAML mirror for humans. 3 traditions
  (protestant / roman_catholic / eastern_orthodox), 4 statuses. Asserts nothing globally (MASTER_CONTEXT §7).
- **CP-1:** real fix is forge-side (CODEOWNERS + branch protection). Locally added `approved_commit`
  + documented the lock as tamper-evidence (ADR-0009). Branch protection is a remaining human action.
- **Chunker:** v0 join only (un-break). Boundary-driven chunker remains Sprint 3. 8 end-of-book
  remainder chunks correctly flagged `status: candidate` (not a crash).
- **Deferred (with ADR/contract):** ProvenanceRecord migration (ADR-0007), full schema generalization
  beyond eng-web (validate_jsonl already parameterized), boundary-driven chunker (Sprint 3).

## Validation run

- `python scripts/validate_all.py` → **passed** (repo, control plane, handoffs, manifest, JSONL+canon 78,742 records)
- `python -m pytest -q` → **passed (11 tests)** (added 2 chunker smoke tests)
- `python scripts/validate_schemas.py` (small canonical + 3k token sample) → **passed**
- Re-ingest → 38,058/38,058 passages carry `canon_profiles` (Tobit = deuterocanonical RC/EO, excluded protestant; Genesis = included all)
- Chunker → 1,310 chunks, **0 raw-USFM leaks**, 8 candidate (end-of-book) chunks
- `generate_data_map.py --check` → current
- `force_handoff.py --task-id BADID` → rejected (exit 2); `--mode build` → interpolated

## Known risks

- **Branch protection not yet enabled** (forge-side human action) — CP-1 only fully closed once
  CODEOWNERS handle is set + "Require review from Code Owners" is on. Until then master context is
  trusted-by-convention.
- CI now runs a ~60s ingest per run; acceptable, but watch the time budget as corpora grow.
- DATA_MAP `--check` assumes deterministic importer output (it is); if a non-deterministic field is
  ever added, the staleness gate will flap.
- Generated data is not in git; a fresh clone must run the importer before chunking/validation of data.

## Open questions

- Confirm the real GitHub owner handle for `.github/CODEOWNERS` (currently `@owner` placeholder).
- Schedule ADR-0007 ProvenanceRecord migration as its own task (PROV-1).

## Next agent instruction

1. **Human:** set the real handle in `.github/CODEOWNERS` and enable branch protection
   ("Require review from Code Owners") on the default branch — closes CP-1.
2. **Sprint 3 (pair):** TextSpan generator (schema now exists) → boundary-driven chunker v0
   (consume `boundary_claims.jsonl` + `chunking_policy.yaml` + genres) → gold set (Ps 23, Rom 7-8, John 1).
3. **Follow-up task:** ProvenanceRecord migration per ADR-0007 (PROV-1).
4. Run `python scripts/validate_all.py && python -m pytest -q` before stopping.
