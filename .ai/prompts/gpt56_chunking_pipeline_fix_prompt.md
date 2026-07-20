# GPT-5.6 Codex Task Prompt — Chunking Pipeline Fixes After Frontier Review (2026-07-09)

Status: owner-issued execution prompt. Non-authorizing prep/harness/metric work only.
Source review: independent frontier review of the eight standing chunking decisions
(Claude Opus 4.8, 2026-07-09), reconciled against T464/T465/T467/T468/T470/T471 evidence.

---

## Role and mode

You are GPT-5.6 acting as Codex integrator on `logos-scripture-graph`.
Declare mode `build`. Allocate the next free task ID from `ROADMAP_STATE.yaml`
(T472 is reserved for the first owner review-packet lane — do not take it).
Create `.ai/tasks/<ID>.task.yaml` and `.ai/handoffs/<ID>/handoff.md` via
`python scripts/agent/force_handoff.py --task-id <ID> --agent codex --stage start`.

## Mandatory reading before any change

1. `AI_FRONT_DOOR.md`
2. `.ai/control/MASTER_CONTEXT.md` (read only — never edit)
3. `.ai/control/PROJECT_STATUS.md`
4. `.ai/control/chunking_agent_preflight.yaml`
5. `.ai/control/t468_owner_faithful_chunking_policy.yaml` (merged on main)
6. `.ai/control/t470_transparent_chunking_research_evidence_rubric.yaml` and
   `.ai/control/t471_near_boundary_docket_refinement.yaml`
   (on branch `codex/t471-near-boundary-docket-refinement` / worktree
   `build/codex_worktrees/logos-t471-v2/` if not yet merged — verify merge state first)
7. `.ai/context/agent_work/T465/harness_triage.md`
8. `docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md`
   (CHUNK-SEM-001, CHUNK-GOLD-001/004, CHUNK-METADATA-001, CHUNK-WJ-001,
   CHUNK-VARIANT-001, CHUNK-ROUTE-002, RISK-GATE-001)
9. Comparison artifacts under `.ai/scratch/multi_model_bible_chunking/comparison/`:
   `model_agreement_matrix.yaml`, `disagreement_delta.jsonl` (1,048 rows),
   `agreement_chunks.jsonl` (144 rows), `frontier_review_queue.jsonl`.

## Evidence you must accept as ground truth (verified against repo files)

- Overall six-model agreement: 6.17% verse-coverage, 0.93% exact-span. Only
  Psalms (0.74) and Lamentations (0.57) show real agreement.
- `M1_cursor` and `M5_gemini_thinking` are mechanical over-splitters
  (Ps: M5=2399 chunks/2461 verses; Job: M5=1041/1070; Prov: M5=901/915).
  `harness_triage.md` already names this a prompt/harness signal.
- With majority_required=5 and two miscalibrated members, "majority of 6" is
  effectively unreachable for coarse literary units — the majority clause is vacuous.
- 18 of 19 T471 "codex_fable_owner_ready_candidate" rows are exact whole-chapter
  spans (X.1 → X.last). Chapter divisions are editorial reference layers
  (MASTER_CONTEXT §5; T470-WS-003), so this is correlated chapter-anchoring, not
  independent literary confirmation.
- In at least 5 of the 19, another model proposed the larger genuine literary unit
  and the M4/M6 lens discarded it:
  - DELTA-Josh-018: M2/M3 = Josh.18.1–19.51 (Shiloh allotment); lens = Josh 18 only.
  - DELTA-1Chr-025: M3 = 1Chr.23.1–26.32 (Levitical register); lens = 1Chr 25 only.
  - DELTA-Num-029: M2/M3 = Num.28.1–29.40 (festival calendar); lens = Num 29 only.
  - DELTA-2Kgs-019: M2 = 2Kgs.18.1–19.37 (Sennacherib narrative); lens = 2Kgs 19 only.
  - DELTA-1Chr-015: M3 = 1Chr.15.1–16.6 (ark procession); lens = 1Chr 15 only.
- DELTA-2John-001 is mislabeled in the T471 docket: presented span is the whole book
  (2John.1.1–1.13) but the actual codex_fable_span is 2John.1.12–1.13. No model
  proposed whole-book 2 John as one chunk. Region-as-span inflation.
- T471's `real_literary_disagreement` class contains 0 rows while genuine
  cross-chapter unit-size disagreements were routed to
  `codex_fable_owner_ready_candidate`. The 19 support/debate tables are
  templated (identical three claims per row).

## Fixes to implement (in order)

### Fix 1 — Delta reclassification (data triage, no re-run)

Write `scripts/build_delta_chapter_artifact_triage.py` that reads
`disagreement_delta.jsonl` (frozen — never mutate) and emits a NEW generated ledger
(e.g. `.ai/context/agent_work/<ID>/delta_chapter_artifact_triage.jsonl`) classifying
all 1,048 rows into:

- `chapter_coincident_agreement` — agreed/lens span exactly equals a whole chapter;
- `larger_unit_disagreement` — any model's span strictly contains the lens span and
  crosses a chapter boundary (record which model and both spans);
- `near_boundary_offset` — spans differ by <=3 verses at either edge;
- `genuine_literary_disagreement` — none of the above;
- `hard_zone` — matches any T468 hard exception (never downgrade).

Chapter extents come from repo canonical data (verse counts per chapter), not memory.
Every row keeps `non_authorizing: true`, `promotion_authority: none`.

### Fix 2 — Larger-unit rescue extraction

From Fix 1, emit `larger_unit_rescue_queue.jsonl`: every case where M2 or M3
proposed a larger coherent unit than the M4/M6 lens. These are candidate evidence
for owner review packets, ranked by genre risk (lists/registers first). Include the
five verified cases above as required members (fail validation if absent).

### Fix 3 — Docket integrity rebuild

Regenerate the owner candidate docket so each row shows:

- `agreed_span` (the actual span models agreed on — never the enclosing region),
- `per_model_spans` (all six),
- `chapter_coincident: true/false` with a required literary justification field
  when true,
- a genre-specific support/debate note (templated identical text across rows must
  fail validation).

Correct the 2John row: the whole-book parent is NOT model-supported; the supported
evidence is a body/closing child structure. Mark it accordingly.

### Fix 4 — Model-agreement policy patch (routing layer)

Add a control file (e.g. `.ai/control/<id>_model_agreement_recalibration.yaml`)
recording, as non-authorizing policy pending owner approval:

- M1_cursor and M5_gemini_thinking are excluded from agreement counts until
  recalibrated under a fixed harness; document why (harness_triage evidence).
- "Six-model/majority agreement raises confidence" is suspended until the panel is
  recalibrated.
- M4/M6 agreement is triage evidence only, never a "preferred lens"; when any model
  proposes a larger literary unit than an agreed span, that is an escalation signal,
  not a discard.
- Chapter-coincident agreement in narrative/list/prophecy/epistle material LOWERS
  confidence and triggers the question: "genuine literary unit, or chapter-slice of
  a larger scene/list/argument?"
- No level of agreement bypasses hard exceptions, reviewed gold, owner gates,
  route isolation, or non-target identity.

### Fix 5 — Harness prompt hardening (future reruns only; no rerun now)

Extend the T467 overlay/marathon prompt so future model slots must:

- state, before chunking each section, whether any proposed boundary coincides with
  a chapter division and justify the coincidence literarily;
- name the literary form (scene / register / oracle / argument / poem) before
  choosing boundaries (already partially in T467 — strengthen with the chapter rule);
- for lists/registers, answer "is this the whole functional list or a slice?";
- for dense epistle argument (Rom, 1–2Cor, Gal, Eph, Heb), prefer the smallest unit
  preserving the complete premise→conclusion movement, NOT the largest parent;
- emit per-boundary confidence and escalate unfamiliar literary forms
  (chiasm, cross-chapter inclusio, Aramaic document seam) to the frontier queue.

### Fix 6 — Metric upgrade

Implement the T470-R1 recommendation: a near-boundary/WindowDiff-style comparison
script over the frozen model maps so a 1–3 verse offset is scored differently from
a different discourse-unit decision. Triage-evidence only; it can prioritize review
but never decide adequacy (T470-WS-005 limits).

### Fix 7 — Standing-decision edit drafts (owner decides, you draft)

Draft (do not activate) the edited wording for the eight standing decisions per the
2026-07-09 frontier review, as an owner decision packet following
`.ai/control/owner_decision_option_presentation_policy.yaml`:

- D1 short-epistle: parent must carry candidate child spans in the same packet;
  exclude 1 John; recipient-identity/variant pressure escalates.
- D2 narrative: scenes cross chapters; chapter numbers never cap a scene; multi-scene
  cycles are parent+child, not one chunk.
- D3 lists: lists span chapters; ban chapter-slice registers; never encode Decalogue
  numbering, Ezra2∥Neh7 priority, or source-partition theories via boundaries.
- D4 epistles: invert "prefer larger parent" for dense argument; preserve
  hymns/creeds/catenae intact; "too large" = crosses a major rhetorical hinge or
  bundles independently-contested claims.
- D5 poetry: never split inside an acrostic; do not inherit editorial speaker
  headings (Song, Job); superscriptions and Psalter book-doxologies are review flags.
- D6 metadata: add tiering — chapter/verse numbers are the lowest-authority layer;
  source-text syntax/discourse features rank above editorial paragraphing;
  evidence-only never means ignore.
- D7 fence: add adjacency rule (abutting a fenced span is fenced), positive
  detection of unlisted variant features (\f/\fqa/apparatus/disagreement spikes),
  and the additional named passages from the review (1 Cor 14:34–35,
  Luke 22:19b–20/43–44, John 1:18, 1 Tim 3:16, Acts 8:37, Matt 6:13b, John 5:3b–4,
  Mark 1:1, Rom 5:1, Isa 7:14, Ps 22:16; Gen 1:1 syntax and the Daniel Aramaic seam
  as notes).
- D8 agreement: adopt principle; retire the M4/M6 mechanism per Fix 4.

## Validation gates (required before stopping)

- New validators + tests for every new generated ledger and control file
  (fail-closed; templated identical support tables must fail; the five rescue rows
  must be present; 2John whole-book must not appear as model-supported).
- `python scripts/validate_all.py` (timeout >= 900000 ms) and `python -m pytest -q`
  per `.ai/control/test_runtime_preflight.yaml`. Do not treat timeout as green.
- Update handoff, `PROJECT_STATUS.md`, `ROADMAP_STATE.yaml`,
  `.ai/control/roadmap_events.jsonl`, lesson index + decision register entries
  (midflight lesson capture per preflight), and the methodology supply-chain doc or
  a no-change rationale.

## Non-authorizations (absolute)

This task authorizes NO: model rerun, reviewed gold, chunk output, child spans,
target selection, route/evaluator behavior change, graph/retrieval/vector truth,
embeddings/indexes, boundary import, preferred reading, source-tradition preference,
canon-scope change, variant/inspiration decision, mutation of frozen T464/T465/T471
artifacts, or theology authority. All Fix 7 drafts are owner decision packets only.
Recommendation is not owner selection.

## Stop conditions

Stop and escalate to the owner if: a fix would require mutating a frozen comparison
artifact; a hard-exception row would be downgraded; the T471 branch merge state is
ambiguous; any validator conflict with T468/T470/T471 appears; or any change would
alter output, evaluator, or route behavior.
