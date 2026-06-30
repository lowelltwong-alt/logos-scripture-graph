---
object_type: agent_handoff
trust_zone: handoff_record
contract_scope: planning_only
governance_authority: false
control_plane_authority: false
lifecycle_status: active
provenance_note: "Created 2026-06-29 by Cursor for T409 read-only eng-web USFM observation pass."
reason_for_inclusion: "Record full 83-file in-situ marker observation, validations, and Codex review questions."
---

# T409 Handoff — Raw USFM Observation Pass

## Task

T409 — read-only raw source observation over `eng-web_usfm.zip` in canonical book order.

## Agent

Cursor (Agent mode).

## Mode

`explore` / `read_only_raw_source_observation`. Non-authorizing. No control-plane writes.

## Branch and base commit

| Field | Value |
| --- | --- |
| Repository | `logos-scripture-graph-repo` |
| Branch | `main` |
| Base commit | `23721ecf99214c953b4734c145c88568bcc358cd` (after T406 commit) |

## Preflight

- T406 artifacts committed on `main` before T409 started.
- T406 files not modified during T409.
- `data/raw/` read-only via `zipfile`; no writes under `data/`.

## Files read (governance / context)

1. `AI_FRONT_DOOR.md`
2. `AGENTS.md`
3. `.ai/control/MASTER_CONTEXT.md` (read-only)
4. `.ai/control/PROJECT_STATUS.md`
5. `.ai/control/test_runtime_preflight.yaml`
6. `.ai/control/RAW_SOURCE_INVENTORY.md`
7. `config/ingest/usfm_marker_coverage.yaml`
8. `.ai/context/README.md`
9. `.ai/context/agent_work/WHOLE_BIBLE_CHUNKING_RISK_ATLAS_PILOT.md` (method limits)
10. `.ai/control/original_language_phrase_context_policy.yaml`
11. `.ai/control/contextual_reading_policy.yaml`
12. `.ai/control/source_metadata_research_atlas.yaml`
13. `config/canon/canonical_66_books.yaml`
14. `pipelines/util/usfm_to_osis.py` (USFM `\id` → OSIS book mapping)
15. `scripts/scan_raw_sources.py` (regex patterns)

## Raw source read

| Archive | Files | Method |
| --- | ---: | --- |
| `data/raw/bible/eng-web/usfm/eng-web_usfm.zip` | **83 / 83** | Full decode per file; `\id` mapped via `USFM_TO_OSIS` |

**Completion:** all 83 entries with `files_read: true`, per-file `bytes_read`, `sha256_short`, verse/chapter counts, marker counters.

**Observation order:** `canonical_66_books.yaml` (66) then `excluded_books` appendix (17). Not naive zip sort.

## Files created / changed

| Path | Role |
| --- | --- |
| `.ai/tasks/T409.task.yaml` | Task scope contract |
| `.ai/context/agent_work/T409_RAW_USFM_OBSERVATION_PASS.md` | Master ledger + completion table + risk rollup |
| `.ai/context/agent_work/T409_BATCH_01.md` | Gen–Ruth |
| `.ai/context/agent_work/T409_BATCH_02.md` | 1Sam–2Chr |
| `.ai/context/agent_work/T409_BATCH_03.md` | Ezra–Song |
| `.ai/context/agent_work/T409_BATCH_04.md` | Isa–Mic |
| `.ai/context/agent_work/T409_BATCH_05.md` | Nah–Mal |
| `.ai/context/agent_work/T409_BATCH_06.md` | Matt–John |
| `.ai/context/agent_work/T409_BATCH_07.md` | Acts–Col |
| `.ai/context/agent_work/T409_BATCH_08.md` | 1Thess–Phlm |
| `.ai/context/agent_work/T409_BATCH_09.md` | Heb–Rev |
| `.ai/context/agent_work/T409_BATCH_APPENDIX.md` | FRT, GLO, deuterocanonical |
| `.ai/handoffs/T409/handoff.md` | This handoff |

## Books completed / skipped

- **Completed:** 66 canonical + 17 excluded = 83 files.
- **Skipped:** none.
- **Next batch:** N/A — full pass complete in one session.

## Risk classification summary (canonical 66)

| risk_class | count (approx.) |
| --- | ---: |
| `low_risk` | historical/narrative prose, short epistles |
| `medium_risk` | Torah, poetry-heavy, footnote-dense, Gospels (wj) |
| `high_risk` | Job, Song, John, Pauline dense argument, Heb, Rev |
| `complex` | excluded/deuterocanonical appendix only |

Risk labels are `book_level` or `raw_marker_only` (appendix); non-authorizing triage only.

## Atlas pilot qualifications

T409 in-situ reading **qualifies** T406 atlas Torah labels:

- Gen–Deut confirmed `medium_risk` at book_level (not whole-book `low_risk`).
- No `\wj` in Torah (atlas NT note confirmed).
- Footnotes and xrefs present throughout Torah.

## Stop conditions checked

- No chunk output, reviewed gold, child spans, or target selection.
- No route/evaluator, graph/retrieval/vector, embeddings, boundary import.
- No backend/profile promotion, manuscript rows, canon-scope change, theology authority.
- No promotion from `agent_work/` to `.ai/control/`.
- No T406 file modifications.

## Validations

| Command | Result |
| --- | --- |
| `python scripts/validate_task_scope.py --task-id T409` | **PASS** |
| `python scripts/agent/validate_handoffs.py` | **PASS** (111 referenced handoff paths) |
| `python scripts/validate_all.py` | **PASS** (~182s, 900000 ms timeout) |
| `git diff --check` | **PASS** |

## Codex review questions

1. Does each book entry include proof fields (`bytes_read`, `sha256_short`, marker counters)?
2. Is observation order canonical (not naive zip sort)?
3. Are excluded/deuterocanonical files documented separately in `T409_BATCH_APPENDIX.md`?
4. Are risk labels scoped (`book_level` / `example_span_level` / `raw_marker_only`) and non-authorizing?
5. Does T409 stay out of `data/` and `.ai/control/` git changes?

## Recommended next step

Codex review T409 observation artifacts; optionally reconcile atlas pilot book labels against batch checkpoints before any chunking target discussion.
