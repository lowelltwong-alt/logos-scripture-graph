# Task Handoff — Claude 4.8 Full Architecture + Software Engineering Review

## Task

- task_id: T304
- title: Claude 4.8 full review (architecture, SWE, control plane) + CI roadmap
- phase: phase_3
- status: complete

## Agent

- agent_name: claude-4.8-opus
- mode: review
- stage: final
- updated_at: 2026-06-03T17:40:00+00:00
- handoff_id: T304-full-review-final
- builds_on: T300 (first review), T302 (senior review), T303 (control plane)

## Files read

- Front door + control plane: `AI_FRONT_DOOR.md`, `.ai/control/MASTER_CONTEXT.md`, `MASTER_CONTEXT.lock.yaml`, `PROJECT_STATUS.md`, `DATA_MAP.md`, `current_focus.yaml`, `handoff_ledger.jsonl`, `roadmap_events.jsonl`
- Roadmap/protocol: `ROADMAP.md`, `ROADMAP_STATE.yaml`, `HANDOFF_PROTOCOL.md`, `CLAUDE.md`, `AGENTS.md`, `LICENSE_POLICY.md`
- Architecture/chunking docs: `docs/architecture/ARCHITECTURE.md`, ADR-0001..0004, `docs/chunking/*.md`
- Config: `config/chunking/chunking_policy.yaml`, `config/agents/agent_roles.yaml`, `config/governance/trust_zones.yaml`, `config/sources/sources.yaml`
- Pipelines: `pipelines/ingest/usfm_importer.py`*, `usfm_inline_parser.py`*, `pipelines/util/usfm_to_osis.py`*, `pipelines/chunking/chunker.py`, `boundary_scorer.py`, `pipelines/validate/validate_manifest.py` (* = skim, unchanged since T302)
- Scripts: `scripts/validate_all.py`, `validate_repo.py`, `validate_control_plane.py`, `validate_jsonl.py`, `scripts/agent/{force_handoff,validate_handoffs,record_roadmap_event,approve_master_context,propose_master_context_change}.py`, `scripts/generate_data_map.py`
- CI/build: `.github/workflows/validate.yml`, `pyproject.toml`, `.gitignore`, `tests/test_control_plane.py`
- Handoffs: T300, T301, T302, T303, T304; `AGENT_ROUTING_GUIDE.md`
- Data spot-checks: `passages.jsonl`, `translation_witnesses.jsonl`, `word_tokens.jsonl`, `source_manifest.yaml`

## Files changed

- `.ai/handoffs/T304/handoff.md` (this file — full review)
- `.ai/control/PROJECT_STATUS.md` (verdict refresh + CP findings + revised blockers)
- `.ai/handoffs/AGENT_ROUTING_GUIDE.md` (control-plane bypass warning, CI-reality note, DATA_MAP staleness, escalation specifics)
- `ROADMAP_STATE.yaml` (T304 → complete; flagged stale T000/T001)
- `.ai/control/current_focus.yaml` (pointer → Codex Sprint 1)
- `.ai/control/roadmap_events.jsonl` (T304 complete event)
- `.ai/context/recommendations/20260603T173513Z-...-human-gate-...-bypassable...md` (CP-1/CP-2 governance proposal via `propose_master_context_change.py`)

No edits to: `MASTER_CONTEXT.md`, `MASTER_CONTEXT.lock.yaml`, `data/raw/`, canonical data, chunker logic, crossref promotion. (Per task constraints.)

## Decisions made

- **Did not implement Sprint 1 mechanical fixes** (chunker join, CI extension, gitignore). They are Codex's queued T301 work; doing them here would collide with the planned sprint. Delivered exact specs/diffs instead.
- **Did not regenerate DATA_MAP.md** — no data/schema/pipeline changed this session, so regeneration would only churn the timestamp.
- **Filed CP-1/CP-2 as a master-context proposal** rather than an ADR, because it is an *enforcement gap in an existing principle*, not a new principle. Human decides remediation.
- **CI roadmap delivers the YAML but does not apply it** — see "What you may fix directly" excludes nothing here, but applying it now would conflict with Sprint 1 item 2 (Codex). Specs below are copy-paste ready.

## Validation run

- `python scripts/validate_all.py` → **passed** (repo + control plane + handoffs; 10 referenced handoff paths)
- `python -m pytest -q` → **passed (9 tests, 1.33s)**
- `python pipelines/chunking/chunker.py --input data/canonical/scripture/passages/passages.jsonl --out build/...` → **FAILED, `KeyError: 'translation_witness'`** (CHK-4 reconfirmed against live tree)
- Lock integrity: `sha256(MASTER_CONTEXT.md)` == lock == `e58064da…` ✓ (file is LF; raw-bytes hash also matches)
- Bypass probe (sandbox, real lock untouched): `approve_master_context.py --approved-by claude` → REJECTED; `--approved-by Lowell|Human|L` → would write lock + pass CI (CP-1 confirmed)
- Active-task regex probe: planned `T002` (missing handoff) before in_progress `T304` → regex returned `('T002','T304/handoff.md')`, skipping the missing handoff (CP-2 confirmed)
- Canon probe: 0 / 38,058 passages carry `canon_profiles` (CANON-1 confirmed)
- Git: `git rev-list --count HEAD` → no HEAD (zero commits; GIT-1 confirmed)

---

# T304 REVIEW REPORT

## Executive verdict

The project has materially improved since T302. **T201 (ingest) and T303 (control plane) are real, well-built layers** — the passage/witness split is clean, sidecar extraction is correct, and the control plane adds genuine governance machinery (lock, proposal flow, data map, routing guide, 9 passing tests). The **MASTER_CONTEXT.md authored in T303 is excellent** and has absorbed essentially every architectural finding from T300/T302.

But three things are simultaneously true and must not be blurred:

1. **The architecture/governance theory is A-grade.**
2. **The ingest pipeline is production-quality (A-).**
3. **Everything downstream of ingest is still foundation/scaffold**, and the chunker is not just incomplete — it is **broken** (`KeyError: 'translation_witness'`).

New this session: the control plane's central guarantee — human-gated master context — **is locally bypassable** (CP-1). That is the most important finding in this review, because the entire governance model defers to master context as the authority layer.

| Layer | Grade | Δ vs T302 |
|-------|-------|-----------|
| Architecture docs / MASTER_CONTEXT | **A** | = (now codified, human-gated) |
| Control plane (T303) | **B+ design / C+ enforcement** | new |
| Ingest pipeline | **A-** | = |
| Data model | **B** | = (TextSpan/ContextPacket still missing) |
| Chunking impl | **F** | = (still crashes) |
| CI / testing | **C-** | ↑ from D (validate_all + 9 tests) but JSONL/manifest/chunker ungated |
| Release readiness | **F** | = (no commits, no LICENSE, no CanonProfile) |

**Bottom line:** safe to start Sprint 1 (Codex) and Sprint 2 (Claude). **Not** safe to (a) trust the human gate as access control, (b) publish `data/canonical/` (canon gap), or (c) build anything on chunks.

---

## Architecture review

### Strengths (preserve)
1. **MASTER_CONTEXT.md is the right artifact** — separates *why* (theory, human-gated) from *where* (PROJECT_STATUS) from *what changed* (handoffs). The five-layer write-permission table is enforced by `validate_control_plane.py`. This is better than 95% of repos.
2. **Identity chain is explicit and honest** — it names the *current gap* (TextSpan, ContextPacket, SourceLanguageWitness, AlignmentRecord absent) inside the doc itself. Self-aware architecture.
3. **Canon-is-explicit principle (§7)** is correctly stated as non-negotiable. The doc forbids publishing canonical data without CanonProfile — the data just hasn't caught up yet.
4. **Sidecar ingest + BoundaryClaim `is_canonical_ancient_boundary:false`** — preserved from T201; still the subtlest correct decision in the repo.
5. **DATA_MAP.md as a generated self-awareness contract** is a genuinely good idea — agents get inputs/outputs/sizes without spelunking.

### Flaws / missing contracts
- **CANON-1 (P0, open):** 0/38,058 passages carry canon metadata; 6,213 deuterocanonical verses are indistinguishable from protocanonical. Per MASTER_CONTEXT §"Explicit rejections", publishing this = forbidden implicit theology. Needs ADR-0005 + `canon_profiles` on passages (book-level membership inherited per verse).
- **MODEL-GAP (P0, open):** `TextSpan`, `ContextPacket`, `ProvenanceRecord`, `SourceLanguageWitness`, `AlignmentRecord` still unimplemented. The identity chain cannot be realized; the chunker cannot be built to design without TextSpan.
- **SCHEMA-LOCK (P1, open):** 8 schemas + `validate_jsonl.py` hardcode `translation_id == "eng-web"`. The validator literally fails any non-WEB record (`validate_jsonl.py:59-62`). Blocks WLC/SBLGNT without a schema fork. Needs generalization before Phase 5.
- **PRED-GAP (P1, open):** `RelationshipObject.predicate` is a free string; no registry. Graph-edge sprawl risk.
- **DATA_MAP omits the control/contract surface** — it maps `data/**` but not `schemas/*.json` (15 contracts) and not the control-plane scripts as endpoints. An agent reading DATA_MAP doesn't learn the schema contracts exist. See "Data + endpoint map review".

---

## Software engineering review

### Code quality
- **Ingest (A-/B+):** unchanged since T302; deterministic, zip-slip protected, duplicate-id detection. Still a 650-line monolith; still needs `pipelines/ingest/common.py` before a second importer. Hardcoded `SOURCE_SHA256` duplicates the manifest (PROV-1).
- **Control-plane scripts (B):** clean, dependency-light, readable. `validate_all.py` is a tidy subprocess aggregator. Two real bugs: CP-1 (approve guard) and CP-2 (active-task regex). `validate_control_plane.py` re-reads files with `read_text` (newline-normalizing) — good for cross-platform hashing, but undocumented; a human running `sha256sum` on a CRLF checkout would get a mismatch. Document the normalization.
- **Chunker (F):** still the T300/T302 skeleton. Reads `p["translation_witness"]` which no longer exists post-T201 → hard crash. Ignores `--policy`, never imports `boundary_scorer`, never reads `boundary_claims.jsonl`. `included_text_span_ids` stores OSIS refs, not TextSpan ids (architecture mismatch).

### Testing (C-)
9 tests now (4 control-plane + 4 inline-parser + 1 e2e ingest). Real gaps:
- **No chunker test** — so CHK-4 (a hard crash) is invisible to CI. A 1-line smoke test would have caught it.
- **No manifest/JSONL gate in the test suite or CI** — `validate_jsonl.py` and `validate_manifest.py` exist but nothing runs them automatically.
- **No full-corpus invariant test** (footnotes=1855, word_tokens=677688, witnesses=38058) — regressions in record counts are silent.
- **No test asserts canon metadata presence** — CANON-1 can't regress-fail.

### Data engineering
- `word_tokens.jsonl` = **432 MB** (DATA_MAP totals ~570 MB). Real Git/LFS decision (see Q1 answer).
- Single 677k-line token file, unpartitioned. Defer partitioning until a 2nd translation lands (agree with T302).
- `derived/` empty — no chunks despite phase_3 active (because chunker crashes).

### Security / ops
- Zip-slip protection present. No secrets. **CP-1 is the security headline** — the governance gate is advisory, not enforced.
- OneDrive working tree + 570 MB regenerable data + **zero git commits** = real data-loss exposure (a `git clean`/sync hiccup is unrecoverable). GIT-1 is now the highest *operational* risk.
- Loose `web_usfm_patch_2a_package/` (76 KB) sits at repo root — tooling clutter; move to `docs/patches/` or `.ai/`.

---

## Control plane review (T303) — soundness, bypass risks, improvements

**Soundness:** The *model* is correct — lock-by-hash + proposal flow + CI gate + routing guide is the right shape. The *enforcement* has two holes, both verified this session:

### CP-1 (BLOCKER) — human gate is locally bypassable
`approve_master_context.py`'s only guard is a name blocklist `{ai,agent,codex,claude,gpt,opus,auto}`. An agent edits `MASTER_CONTEXT.md`, runs `--approved-by Lowell`, regenerates a matching lock, CI goes green. Verified in sandbox: `claude` → REJECTED; `Lowell|Human|L|the-human` → lock written + control-plane green. **A script inside the agent's own sandbox cannot gate against that agent.** Enforcement must move to the forge:
1. **CODEOWNERS + branch protection** on `MASTER_CONTEXT.md` + `.lock.yaml` (only layer an in-repo agent can't bypass).
2. Lock records `approved_commit`; CI verifies the lock change landed via a CODEOWNER-approved PR (not a name string).
3. Optional: signed commits from an allowlisted human key.
4. Re-document the local check as **tamper-evidence**, not access control.
Filed as a proposal: `.ai/context/recommendations/20260603T173513Z-...-human-gate-...md`.

### CP-2 (HIGH) — fail-open active-task handoff gate
`validate_active_task_handoff`'s multi-line regex mis-pairs a planned task's id with a later in_progress task's handoff. Verified: planned `T002` (handoff missing) + in_progress `T304` → `('T002','T304/handoff.md')`, the missing handoff silently skipped. A real in_progress task with a missing handoff can pass CI. Fix: parse `ROADMAP_STATE.yaml` with PyYAML (optional dep) and iterate tasks structurally; fall back to the regex only if PyYAML is absent.

### Lesser control-plane notes
- `validate_handoffs.py` checks section *headers exist*, not that they're *filled*. Stale stubs (T000/T001, byte-identical, `in_progress` since scaffold) pass. Add a "non-empty body" check for `in_progress` tasks.
- `validate_control_plane` requires front-door/README/CLAUDE/AGENTS to *reference* master context (good) but cannot detect drift of their *content*.
- Lock has no `approved_commit`/`version_of_master` field — can't tell *which* master version a human saw.

---

## CI improvement roadmap (P0/P1/P2, copy-paste ready)

Current CI (`.github/workflows/validate.yml`) runs only `validate_all.py` + `pytest`. `validate_all.py` runs repo + control-plane + handoffs — but **not** `validate_jsonl.py`, **not** `validate_manifest.py`, **not** the chunker, **not** a raw-mutation tripwire. So CI is green while the chunker crashes and canon metadata is missing.

### P0 — make CI catch what's already broken (Codex, Sprint 1)
Add to `validate.yml` after the pytest step:
```yaml
      - name: Manifest checksum gate
        run: python pipelines/validate/validate_manifest.py data/raw/bible/eng-web/source_manifest.yaml
      - name: Raw-source immutability tripwire
        run: |
          git diff --quiet -- data/raw/ || (echo "data/raw mutated"; exit 1)
```
And add a **chunker smoke test** so CHK-4 can never pass CI again (`tests/test_chunker_smoke.py`): run chunker on a 5-line fixture, assert exit 0 + ≥1 chunk + no `KeyError`. (Pairs with Codex's Patch 4a.)

### P1 — referential integrity + schema validation
- Add `jsonschema`+`pyyaml` as `[project.optional-dependencies] validate = [...]`; install in CI (`pip install -e ".[validate]"`).
- JSONL gate on canonical outputs **excluding** the 432 MB token file for time (validate it in a nightly job or on a sampled head):
```yaml
      - name: JSONL referential integrity (fast subset)
        run: |
          python scripts/validate_jsonl.py \
            data/canonical/scripture/passages/passages.jsonl \
            data/canonical/translations/eng-web/translation_witnesses.jsonl
```
- Add a JSON-Schema validation step (records vs `schemas/*.json`) once `jsonschema` is available.
- Fix CP-2 (PyYAML task parser) so the handoff gate stops failing open.

### P2 — staleness + governance hardening
- **DATA_MAP staleness gate:** `python scripts/generate_data_map.py && git diff --exit-code .ai/control/DATA_MAP.md` (red if an agent changed data/pipelines without regenerating). *Caveat:* the generator stamps a timestamp every run, so first make the timestamp stable or diff-exclude that line; otherwise this gate is always red.
- **CODEOWNERS + branch protection** for CP-1 (the real fix; CI can't self-enforce it).
- **Canon presence gate:** once ADR-0005 lands, fail CI if any passage lacks `canon_profiles`.
- Decide canonical-data-in-CI: don't re-ingest 570 MB per PR (60 s + bloat). **Recommend:** commit manifest+schemas+scripts; regenerate canonical in a release/nightly job and diff record counts, not full content.

---

## Data + endpoint map review (DATA_MAP.md)

**Good:** size + record counts + trust zone per file; pipeline endpoints with inputs/outputs; the flow diagram. Accurate vs live tree (21 files, 864,904 records — matches).

**Gaps to add to `scripts/generate_data_map.py`:**
1. **Schema contracts** — list `schemas/*.json` (15) with their `title`. Agents currently can't discover the contract surface from the map.
2. **Validation endpoints** — `validate_jsonl.py`, `validate_manifest.py`, `validate_control_plane.py` are pipeline-relevant endpoints but absent.
3. **Stale-flagging** — mark the chunker output as `BROKEN (CHK-4)` rather than just "not yet produced" (it *crashes*, it isn't merely pending).
4. **LFS/commit-policy column** — flag files >100 MB (`word_tokens.jsonl`) as "LFS-candidate" inline.
5. **Timestamp determinism** — see P2 caveat; needed before a staleness gate is viable.

---

## Recommended ADRs (unchanged priority from T302; restated for the human)

| ADR | Title | Why now |
|-----|-------|---------|
| ADR-0005 | Canon profiles for multi-tradition corpus | **P0** — blocks canonical publish |
| ADR-0009 | **Control-plane enforcement model** (CODEOWNERS/branch protection vs local lock) | **P0/new** — CP-1 |
| ADR-0006 | Source-language boundary precedence | P2 — Phase 5 |
| ADR-0007 | Provenance canonicalization (`provenance_id`) | P1 — PROV-1 |
| ADR-0008 | Chunk identity stability (content-addressed vs positional) | P1 — before chunks ship |

## Specific questions answered

1. **Git/LFS for 570 MB regenerable JSONL?** **Commit** manifest + schemas + scripts + small canonical (passages, witnesses, headings, footnotes, crossrefs, glossary). **LFS** `word_tokens.jsonl` (432 MB) *or* exclude it and regenerate from the zip in a release job. Rationale: small canonical gives reviewable diffs + reproducibility anchor; the token file is pure derivative bulk.
2. **CI regenerate vs trust snapshot?** Trust the committed snapshot for PR CI (fast); add a **nightly** full re-ingest that diffs record counts (not content) against committed. Keeps PR CI well under budget.
3. **Control-plane self-approve?** **Yes, today (CP-1).** Cannot be fixed by a local script. CODEOWNERS + branch protection on master+lock; CI verifies CODEOWNER-approved PR. See proposal.
4. **Schema validation gap?** Yes — add `jsonschema` as optional `[validate]` extra, required in CI (P1).
5. **DATA_MAP staleness gate?** Worth it, but first make the generator's timestamp deterministic/diff-excluded, else the gate is permanently red (P2).

## Known risks
1. **CP-1**: governance gate is advisory; an agent can rewrite + self-approve master context. Until CODEOWNERS lands, treat master context as *trusted-by-convention*, not enforced.
2. **GIT-1**: zero commits + OneDrive + 570 MB = unrecoverable on a sync/clean accident. Highest operational risk.
3. **CANON-1**: any publish of `data/canonical/` before ADR-0005 is a silent canon-theology decision (violates MASTER_CONTEXT §"Explicit rejections").
4. **CHK-4**: chunker crashes; CI is green anyway (no chunker test). Phase 3 cannot demo.
5. **CP-2**: handoff gate can fail open for a genuinely missing handoff.
6. **Stale T000/T001** `in_progress` since scaffold — roadmap state misrepresents reality; close or archive them.

## Open questions
- Should `web_usfm_patch_2a_package/` move into `docs/patches/` before first commit? (Recommend yes.)
- Who owns ADR-0009 (control-plane enforcement) — Claude drafts, human decides forge config? (Recommend yes.)
- Confirm LFS availability on the chosen remote before committing the 432 MB token file.

## Next agent instruction

**Order matters. GIT-1 first (data-loss risk), then un-break, then govern.**

1. **Codex — Sprint 1 (T301), in this order:**
   a. **GIT baseline first**: add `.gitignore` entries (`data/processed/**/extracted/` already covered by skip but confirm; `.pytest_cache/` already present), decide LFS for `word_tokens.jsonl`, make the first commit. Verify `git rev-list --count HEAD` ≥ 1.
   b. **Patch 4a**: fix `chunker.py` to join `passages.jsonl` + `translation_witnesses.jsonl` by `passage_id` (keep token-grouping for now; full boundary chunker is Sprint 3). Add `tests/test_chunker_smoke.py`.
   c. **CI P0**: add manifest gate + raw tripwire + chunker smoke to `validate.yml` (YAML above).
   d. **GOV**: fix `force_handoff.py` to interpolate `--mode` (currently accepted but dropped — verified: template `- mode:` stays blank) and enforce `^T\d{3,}$` task ids. Fix **CP-2** (PyYAML task parser in `validate_control_plane.py`).
   e. Fix `INGESTION_WORKFLOW.md` path drift.

2. **Claude — Sprint 2 (after 4a):** ADR-0005 CanonProfile + tag deuterocanonical passages; `schemas/text_span.schema.json` + `context_packet.schema.json`; `config/chunking/book_genres.yaml`; draft ADR-0009 (control-plane enforcement) responding to the filed proposal.

3. **Human:** review `.ai/context/recommendations/2026...-human-gate-...md`; decide CP-1 remediation (CODEOWNERS + branch protection); close/archive stale T000/T001.

4. **Lower-tier agents:** only the menu in `AGENT_ROUTING_GUIDE.md`. No ADRs, no chunker design, no master context.
