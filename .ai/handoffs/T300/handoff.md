# Task Handoff

## Task

- task_id: T300
- title: Architecture and chunking review (extra-high effort)
- phase: phase_0
- status: complete

## Agent

- agent_name: claude
- mode: review
- stage: final
- updated_at: 2026-05-29T16:05:00+00:00
- handoff_id: b56111100787c374
- amended_after_t201: true

## Concurrency note

Codex's T201 ("Implement Patch 2A WEB Classic USFM embedded feature extraction") completed at 2026-05-28T21:38Z, before this review session began. During my review I initially read the pre-T201 state from earlier notes; mid-review I observed `ROADMAP_STATE.yaml` change under me from `current_phase: phase_0` to `current_phase: phase_2` (adding T201) and re-verified every finding against the live tree before finalizing this handoff. The findings below describe the **post-T201 state** as of 2026-05-29T16:00Z.

## Files read

- AI_FRONT_DOOR.md, README.md, ROADMAP.md, ROADMAP_STATE.yaml, HANDOFF_PROTOCOL.md, CLAUDE.md, AGENTS.md, LICENSE_POLICY.md, pyproject.toml, .gitignore
- docs/architecture/ARCHITECTURE.md, docs/architecture/ADR-0001..0004
- docs/chunking/CHUNKING_DESIGN.md, CHUNKING_RULES.md, LITERARY_POLICIES.md, EVALUATION_PLAN.md
- docs/workflows/AGENT_COORDINATION_WORKFLOW.md, INGESTION_WORKFLOW.md, ROADMAP_CHANGE_WORKFLOW.md
- config/chunking/chunking_policy.yaml, config/agents/agent_roles.yaml, config/governance/trust_zones.yaml, config/sources/sources.yaml
- data/raw/README.md, data/raw/bible/README.md, data/raw/bible/eng-web/README.md, data/raw/bible/eng-web/source_manifest.example.yaml
- data/raw/bible/eng-web/usfm/eng-web_usfm.zip (presence and full contents inspected)
- data/canonical/scripture/passages/passages.jsonl (T201 output, sampled)
- data/canonical/translations/eng-web/translation_witnesses.jsonl (T201 output, sampled)
- data/canonical/translations/eng-web/word_tokens.jsonl, footnotes.jsonl, editorial_cross_references.jsonl, section_headings.jsonl, boundary_claims.jsonl, glossary_entries.jsonl (T201 outputs, sampled)
- data/canonical/README.md, data/processed/README.md, data/derived/README.md
- schemas/{scripture_passage,source_manifest,chunk,relationship_object,handoff,roadmap_state,translation_witness,word_token,footnote,editorial_cross_reference,section_heading,boundary_claim,glossary_entry,usfm_event,unsupported_usfm_marker}.schema.json
- pipelines/ingest/usfm_importer.py, pipelines/ingest/usfm_inline_parser.py, pipelines/util/usfm_to_osis.py
- pipelines/validate/validate_manifest.py
- pipelines/chunking/boundary_scorer.py, chunker.py
- scripts/validate_repo.py, scripts/validate_jsonl.py, scripts/agent/{force_handoff,record_roadmap_event,validate_handoffs}.py, scripts/hooks/session_start_notice.py
- .github/workflows/validate.yml, .github/CODEOWNERS, .github/pull_request_template.md
- .claude/settings.example.json
- .ai/{README.md, handoffs/README.md, handoffs/_TEMPLATE.handoff.md, handoffs/T000/handoff.md, T001/handoff.md, T001-web-usfm-ingest/handoff.md, T002/handoff.md, T100/handoff.md, T201/handoff.md, tasks/_TEMPLATE.task.yaml, control/current_focus.yaml, control/handoff_ledger.jsonl, control/roadmap_events.jsonl, prompts/architecture_review_prompt.md, prompts/chunking_review_prompt.md}
- tests/fixtures/usfm/JHN.usfm

## Files changed

- .ai/handoffs/T300/handoff.md (this file)
- ROADMAP_STATE.yaml (T300 added to phase_0; `last_updated` bumped)
- .ai/control/roadmap_events.jsonl (T300 event appended via scripts/agent/record_roadmap_event.py)
- .ai/control/handoff_ledger.jsonl (T300 entry appended by scripts/agent/force_handoff.py)

No code, config, schema, raw-source, or canonical-data files were modified during this review.

## Decisions made

### Executive verdict (post-T201)
- Continued Phase 2 ingest work: T201 closed most of the gap. Remaining blockers are CHK-4 (newly introduced), VAL-1, LIC-2.
- Chunking implementation (Phase 3): NOT ready. The chunker now also actively crashes on the new passage shape.
- Hebrew/Greek expansion: architecture allows; no implementation gates passed.
- Public release: NOT ready (no commits, no LICENSE, placeholder CODEOWNERS).

### Findings (revised after re-verification against the post-T201 tree)

**Fixed by T201 (close these):**

- ~~DATA-1~~ ScripturePassage no longer embeds TranslationWitness. Passage and witness are separate JSONL with `passage_id` foreign-key. Schema updated to `additionalProperties: true` with provenance fields. Confirmed via sample of `data/canonical/scripture/passages/passages.jsonl` and `.../translations/eng-web/translation_witnesses.jsonl`.
- ~~DATA-2~~ OSIS book IDs are now canonical (`Gen.1.1`, `Matt.1.1`, `1Cor.3.16`, `Phlm.1.1`, `Ps151`). USFM book code preserved as parallel `usfm_book` attribute. `pipelines/util/usfm_to_osis.py` added.
- ~~CHK-2~~ TranslationWitness `text` is clean: `"In the beginning, God created the heavens and the earth."` no longer contains `\w`, `\f`, `\+wh`, or footnote markup. Inline parser at `pipelines/ingest/usfm_inline_parser.py` extracts them as sidecars.
- ~~MODEL-1 (partial)~~ Nine new schemas landed: TranslationWitness, WordToken, Footnote, EditorialCrossReference, SectionHeading, BoundaryClaim, USFMEvent, GlossaryEntry, UnsupportedUSFMMarker. Still missing: **TextSpan, ContextPacket, ProvenanceRecord, CanonProfile, TraditionScopedCanonClaim, SourceDataset, ScriptureCrossReference** (note: `editorial_cross_reference` is the inline `\x` marker, not the cross-reference relationship object the graph will eventually need).
- ~~CI-1~~ Pytest now runs and passes 5 tests; T201 added `tests/test_usfm_inline_parser.py` and `tests/test_web_usfm_feature_extraction.py`. The original `tests/fixtures/usfm/JHN.usfm` is no longer load-bearing as a fixture, so its bug is no longer blocking.

**Newly introduced by T201 (NEW blockers and issues):**

1. **[BLOCKER, NEW] CHK-4 — `pipelines/chunking/chunker.py` crashes on the new passage shape.** Line 37 reads `p["translation_witness"].get("text", "")`. The new `passages.jsonl` no longer has a `translation_witness` key (T201's DATA-1 fix). I verified by running `python pipelines/chunking/chunker.py --input data/canonical/scripture/passages/passages.jsonl --out build/check_chunks.jsonl`:
   ```
   KeyError: 'translation_witness'
     File "pipelines/chunking/chunker.py", line 37, in make_chunk
       text = " ".join(p["translation_witness"].get("text", "").strip() for p in buffer).strip()
   ```
   The DATA-1 fix shipped without updating the only downstream consumer. Patch 4 was always going to rewrite the chunker; this just makes it more urgent — the existing chunker is dead code as of T201.

2. **[HIGH, NEW] CANON-1 — 6,213 deuterocanonical verse records are now in `data/canonical/scripture/passages/passages.jsonl` with `status: "imported"` and no canon-scope marker.** Confirmed book set includes Tob, Jdt, AddEsth, Wis, Sir, Bar, AddDan, 1Macc, 2Macc, 3Macc, 4Macc, 1Esd, 2Esd, PrMan, Ps151 (15 books, 6,213 records). T201's own decision note acknowledged this: "Used explicit OSIS mapping for the 81 content files in the WEB archive, including deuterocanonical/additional books present in the archive without making a canon claim." The disclaimer is correct; the on-disk shape contradicts it — a consumer cannot distinguish deuterocanonical from protocanonical without re-deriving canon membership from the book ID. There is no `canon_profiles` value on any record. There is no `CanonProfile` or `TraditionScopedCanonClaim` schema. `LITERARY_POLICIES.md` has no entry for deutero genres. Resolution requires (a) a `CanonProfile` schema before `data/canonical/` is published anywhere; (b) attaching `canon_profiles` to each passage; (c) an ADR documenting the default canon profile choice.

3. **[MEDIUM, NEW] PROV-1 — Provenance is duplicated per-record but not canonicalized.** Every JSONL record carries `source_sha256: "a745365f53ab95570e9c39a60a7d245ba10bbf6c863832006876b01ea8654f8e"` (verified WEB ZIP SHA256). This is correct provenance, but it is duplicated 864,904 times into derived records without a `source_manifest.yaml` to canonicalize it. If a corrected manifest later changes the SHA, every record will diverge silently. Resolution: land `source_manifest.yaml` (LIC-2), add a `ProvenanceRecord` schema, and have records reference a `provenance_id` instead of carrying the full provenance inline.

4. **[LOW, NEW] RAW-1 — Extracted ZIP under `data/processed/bible/eng-web/usfm/extracted/` (81 files, ~9 MB) is not in `.gitignore`.** `data/raw/` is correctly untouched (ADR-0002 honored). But the extracted USFM files are bulky and regenerable; they will be picked up by `git add -A`. Add `data/processed/**/extracted/` to `.gitignore`.

5. **[LOW, NEW] MODEL-2 — Schema shape may not match what some consumers expect.** `schemas/scripture_passage.schema.json` now has `additionalProperties: true` and a long list of optional fields. That solves the strict-validation problem (which is good) but it means the schema no longer enforces *anything* about the extra provenance fields. A passage missing `source_sha256` would still validate. If those fields are load-bearing, add them to `required`.

**Still broken — NOT addressed by T201:**

- **[blocker] CHK-1** Even rewritten to read the new shape, the chunker still does not consume `chunking_policy.yaml`, does not import `boundary_scorer.py`, does not consume `usfm_events.jsonl` or `boundary_claims.jsonl`, and still hard-codes `boundary_basis`. Patch 4 still needed.
- **[high] CHK-3** Cannot be re-tested until CHK-4 is fixed.
- **[high] VAL-1** `validate_manifest.py` still uses substring containment. Verified `["id:" not in text]` check is unchanged. False positives remain.
- **[high] GIT-1** Branch `citation-audit-frontdoor` still has zero commits. Working tree still sits inside parent workspace.
- **[high] AGENT-1** `force_handoff.py` still does not validate task IDs. T201 happened to use a conforming ID. The orphan `.ai/handoffs/T001-web-usfm-ingest/` from Codex's earlier run is still present.
- **[medium] AGENT-2** Handoffs still markdown without machine-readable frontmatter. T201's handoff confirms the pattern (also exhibits the `force_handoff.py --mode` substitution bug — the script accepts `--mode` but does not interpolate it into the template; I observed this directly when scaffolding T300).
- **[medium] AGENT-3** `.ai/handoffs/T000/handoff.md` and `.ai/handoffs/T001/handoff.md` are still byte-identical copy-paste with `status: in_progress`.
- **[medium] LIC-1** No root `LICENSE` file. `.github/CODEOWNERS` still `@owner`. Trust zones documented but data dirs cover only 4 of 6.
- **[medium] LIC-2** `data/raw/bible/eng-web/source_manifest.yaml` still missing. T201 explicitly deferred it ("Who should create data/raw/bible/eng-web/source_manifest.yaml, given the current task forbids modifying data/raw?"). The known SHA256 is now embedded in every canonical record but not in a manifest. Validator still fails: `Missing manifest: data/raw/bible/eng-web/source_manifest.yaml`. **This is now the highest-leverage Phase 1 task.**
- **[medium] DET-1** Chunk IDs are still positional (moot until Patch 4 rewrites chunker.py). Ledger backslash paths persist; T201 added two more.
- **[medium] CI-2** `.github/workflows/validate.yml` still runs only `validate_repo.py` and `validate_handoffs.py`. T201 added `scripts/validate_jsonl.py` and 5 pytest tests, neither of which CI runs. Manifest validator is not in CI either.

### Strengths (do not regress)

1. Doctrine remains consistent across documents.
2. Five-layer model + four ADRs + trust zones + role allowlists remain right.
3. T201's split of passage vs. witness is exactly what the architecture demanded.
4. T201's per-record provenance (with the actual SHA256) is the right primitive even though it should be canonicalized (PROV-1).
5. T201's BoundaryClaim sample (`boundary_kind: usfm_structural_marker, is_canonical_ancient_boundary: false, claim_scope: future_chunking_evidence`) correctly distinguishes USFM editorial structure from ancient canonical structure — a subtle and important distinction. Keep this discipline.
6. T201 added 9 new schemas in one shot and they pass pytest. The schema-first discipline is working.
7. T201's OSIS book-ID handling is canonical and includes the full WEB book set (66 + 15 deuterocanonical = 81 content files).

### Patch plan (revised — dependency-ordered, post-T201)

1. **Patch 6** — Git baseline (still required). Effort low.
2. **Patch 1** — Drop the missing `source_manifest.yaml`. Use the SHA256 already known to T201 (`a745365f53ab95570e9c39a60a7d245ba10bbf6c863832006876b01ea8654f8e`). Rewrite `validate_manifest.py` to be sound. Verify the per-record `source_sha256` matches the manifest. Effort low.
3. **Patch 5** — Handoff/governance hardening. Effort low.
4. **Patch 4a (NEW URGENT)** — Update `pipelines/chunking/chunker.py` to read the new passage+witness shape so it stops crashing. This can be a minimum-viable fix (read `passage_id`-linked witness text) ahead of the full Patch 4 rewrite. Effort low. **Do this before any agent tries to demo Phase 3.**
5. **Patch 3 (revised)** — Land the still-missing schemas (TextSpan, ContextPacket, ProvenanceRecord, CanonProfile, TraditionScopedCanonClaim, SourceDataset, ScriptureCrossReference) + chunking gold set + start CanonProfile-tagging deuterocanonicals. Effort medium.
6. **Patch 4 (full)** — Real Bible-aware chunker (load policy YAML, consume `usfm_events.jsonl` AND `boundary_claims.jsonl`, score boundaries, refuse forbidden splits, emit ContextPacket records). Effort extra-high.

Original Patch 2 (importer) is now mostly superseded by T201. Remaining Patch 2 work: extend CI with `scripts/validate_jsonl.py`, `validate_manifest.py`, `pytest`, and a raw-tree mutation tripwire.

## Validation run

- command: `python scripts/validate_repo.py`
  result: passed (exit 0)
- command: `python scripts/agent/validate_handoffs.py`
  result: passed for 5 referenced handoff paths (exit 0)
  failures: zero — but AGENT-1/2 still apply; pass is not load-bearing.
- command: `python pipelines/validate/validate_manifest.py data/raw/bible/eng-web/source_manifest.yaml`
  result: **failed** — manifest still missing (LIC-2 unchanged).
- command: `python pipelines/validate/validate_manifest.py data/raw/bible/eng-web/source_manifest.example.yaml`
  result: passed (exit 0) — but VAL-1 means the pass is not load-bearing.
- command: `python -m pytest -q`
  result: **passed; 5 tests in 0.39s** (T201 added them).
- command: `python pipelines/chunking/chunker.py --input data/canonical/scripture/passages/passages.jsonl --out build/check_chunks.jsonl`
  result: **CRASH — `KeyError: 'translation_witness'`** at `chunker.py:37`. CHK-4 confirmed.
- Build artifacts removed; only `build/.gitkeep` remains.

## Known risks

1. **Chunker is now broken, not just incomplete.** Any agent that tries to run the existing chunker against T201's output will hit `KeyError`. Document this loudly until Patch 4a lands.
2. **Deuterocanonical records are in `data/canonical/` indistinguishable from protocanonical records.** If anyone publishes `passages.jsonl` before CanonProfile lands, that publication is a de facto canon claim, regardless of T201's stated disclaimer.
3. **The known WEB ZIP SHA256 is canonicalized only in 864,904 derived records, not in a `source_manifest.yaml`.** A future manifest correction will be impossible to apply consistently without a re-ingest.
4. **No commits exist.** Every artifact above (canonical data, schemas, scripts) is untracked. A `git clean` would erase Codex's entire T201 output.
5. **CI is shallow enough that T201's tests + JSONL validator + manifest validator don't run.** A red CI signal is currently impossible for the things that matter.
6. **`data/processed/.../extracted/` is not gitignored** and will sweep into a `git add -A` (RAW-1).
7. **`current_focus.yaml` still says `current_task: T001`** while `ROADMAP_STATE.yaml` says `current_phase: phase_2` with T201 active. Drift between control files.
8. **Multi-agent concurrency demonstrated live.** During this review session, `ROADMAP_STATE.yaml` was edited under me by a separate agent — the exact scenario the handoff protocol is meant to mediate. The handoff system worked enough that I could detect the change and re-verify findings, but the lack of a locking or merge protocol means two agents writing the same file at the same time would silently overwrite each other.

## Open questions

1. Should `source_manifest.yaml` be created by extending T201's task scope (since it already has the SHA256 in memory) or by a fresh `source_ingestor` task with explicit `data/raw/` write authority? Recommendation: fresh task — keeps the no-mutation discipline pure.
2. What default `CanonProfile` should the WEB ingest carry? Protestant 66 only? Catholic + protocanonical + DC? Eastern Orthodox? Anglican? Recommendation: write an ADR proposing `canon_profiles: {protestant_66: included|excluded, roman_catholic: included|excluded, eastern_orthodox: included|excluded}` per book, with the *book-level* membership set deterministically and the per-passage record inheriting.
3. Should `data/canonical/scripture/passages/passages.jsonl` be split by canonical scope (`passages_protocanonical.jsonl`, `passages_deuterocanonical.jsonl`) for safety, or kept unified with `canon_profiles` metadata? Recommendation: unified with metadata — splitting builds a tradition assumption into the filesystem.
4. Should the new BoundaryClaim records become the chunker's only boundary source, or should the chunker also consume `usfm_events.jsonl` directly? Recommendation: BoundaryClaim only — that's the canonical layer. `usfm_events.jsonl` is processed-tier evidence.
5. Should `force_handoff.py` reject non-conforming task IDs (breaking change) or warn (compatible)? Recommendation: reject — the validation is already in the schema; this just enforces it.

## Next agent instruction

Do these in order. Do not skip.

1. **GIT-1 first.** Verify the directory is its own git repo (`git rev-parse --show-toplevel` should point here, not at the parent workspace). If not, decide whether to `git init` here or to move this tree to its own root. Add `data/processed/**/extracted/` to `.gitignore`. Add `.pytest_cache/` to `.gitignore` if it isn't already covered. First commit: `chore: initial scaffold + T201 USFM feature extraction`.

2. **Patch 4a (NEW URGENT) — un-break the chunker.** Minimum-viable rewrite of `pipelines/chunking/chunker.py` so it reads `passages.jsonl` + `translation_witnesses.jsonl` joined by `passage_id`. Keep the same token-budget grouping behavior for now; the structural rewrite is Patch 4. Acceptance: `python pipelines/chunking/chunker.py --passages data/canonical/scripture/passages/passages.jsonl --witnesses data/canonical/translations/eng-web/translation_witnesses.jsonl --out build/chunks.jsonl` exits 0 and writes ≥ one chunk. Add a smoke test under `tests/`.

3. **Patch 1 — close LIC-2 and VAL-1.** Create `data/raw/bible/eng-web/source_manifest.yaml` (use the SHA256 `a745365f53ab95570e9c39a60a7d245ba10bbf6c863832006876b01ea8654f8e` already known to T201). Rewrite `validate_manifest.py` to parse YAML (or anchor each required key with `^key:` multiline regex) and to verify the SHA matches the archive. Update `config/sources/sources.yaml` → `eng-web.status: present`. Update `ROADMAP_STATE.yaml`: T100 status → `complete`. Append a roadmap event. Add a CI step.

4. **Patch 5 — governance hardening.** Enforce the `^T[0-9]{3,}$` pattern in `force_handoff.py`. Fix the `--mode` flag substitution bug (script accepts the flag but does not interpolate `mode:` into the template — I observed this when scaffolding T300). Normalize ledger paths to posix (`as_posix()`). Add orphan-handoff check to `validate_handoffs.py`. Decide and apply the orphan `.ai/handoffs/T001-web-usfm-ingest/` (most likely rename to `T200/` and record the event). Replace `@owner` in `.github/CODEOWNERS`. Add root `LICENSE`. Reconcile `.ai/control/current_focus.yaml` with `ROADMAP_STATE.yaml`.

5. **CANON-1 ADR.** Before any further consumer uses `data/canonical/scripture/passages/passages.jsonl`, write `docs/architecture/ADR-0005-canon-profiles.md` documenting the default canon-profile assumption and add a `schemas/canon_profile.schema.json` stub.

6. **CI-2 — extend CI.** Add steps for `pytest -q`, `pipelines/validate/validate_manifest.py` against every `data/raw/**/source_manifest.yaml`, `scripts/validate_jsonl.py` against every `data/canonical/**/*.jsonl`, and a `git diff --quiet data/raw/` raw-mutation tripwire.

Only after those are clean: start Patch 3 (remaining schemas + gold set), then full Patch 4 (real Bible-aware chunker).
