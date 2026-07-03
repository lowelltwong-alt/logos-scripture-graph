# Red-Team Pre-Mortem — T423 Whole-Bible Multi-Model Chunking Fork

**Reviewer:** Codex (independent red-team)  
**Date:** 2026-07-03  
**Task:** T423  
**Policy reviewed:** `.ai/control/multi_model_whole_bible_chunking_fork.yaml`  
**Verdict basis:** Mandatory reads A–H; assume 30-day failure scenario.

---

## Executive verdict

**HOLD** — The fork’s agreement-vs-delta strategy is plausible for prioritization, but P1 blockers (missing compare script, undefined revert thresholds, N=3 majority collapse, premature interim compare, T417 path confusion, and no chunk-map schema validator) make a multi-day M1–M5 marathon likely to waste effort before comparison is trustworthy; fix blockers and run a 5-book pilot only.

---

## Pre-mortem narrative

Thirty days after owner approval, the fork was abandoned. Chunking was slower than under T410, not faster. Five models had each produced `whole_bible_chunk_map.jsonl` files totaling tens of thousands of JSONL lines across 66 books. Comparison never ran deterministically because `scripts/compare_multi_model_bible_chunk_maps.py` was never implemented; interim compares were done manually by agents reading each other’s maps, violating independence and producing inconsistent `agreement_chunks.jsonl` entries.

Week one looked productive. M1 (Cursor) finished Genesis through Ruth in a continuous session; M2 (Codex) lagged on Pauline epistles; M3 (Claude) and M4 (Gemini) restarted mid-marathon after context limits, leaving `marathon_progress.yaml` stale on two folders. An eager integrator ran delta compare when only three models had completed overlapping books (minimum `compare_when_at_least_models: 3`), wrote 400 “easy” spans to `agreement_chunks.jsonl`, and circulated a DAD summary implying consensus chunks were “low-friction gold candidates.” LSN-041 was violated in spirit: standing scratch disposition and fork “easy bucket” language were read as step authorization.

Week two exposed comparability failure. Span strings diverged (`Gen.1.1-Gen.1.31` vs `Gen.1.1-Gen.1.31` vs `GEN 1:1-31`). `chunk_index_in_book` reset per model differently in Psalms. Near-miss boundaries (1–3 verse shifts) were invisible to the exact-match agreement rule in fork policy even though the delta prompt warned about them. At N=5, four models agreed on verse-aligned paragraph splits in Gospels—training-bias false consensus—while the fifth’s WJ-aware splits were buried in delta noise. Jonah, Jude, and Phlm regions that T417 batch2 had already escalated were re-chunked in scratch without frontier review; typology language appeared in `layer_decision_log.jsonl` rationales and leaked into boundary justifications.

Week three doubled control-plane drift. T417 batch2 (SUB-012, Phlm/Jude/Jonah) and T423 marathons ran in parallel using the same agent surfaces (cursor, codex, claude, gemini). Agents copied batch2 strengthened packets into T423 rationales, conflating three-book governed prep with whole-Bible scratch maps. M5 was skipped as “optional”; M6 was added ad hoc from `_TEMPLATE` without updating `manifest.yaml` active_slots, breaking the agreement matrix’s `complete_model_count`. Owner attempted revert per `revert_to_baseline_if` but found `agreement_rate_below_threshold_after_pilot_books` had no numeric threshold; P0 theology leakage was documented but not machine-detectable.

Week four: owner declared fork abandoned. Scratch artifacts remained (correct per policy) but polluted agent context—future T410 batches cited T423 “consensus” spans in review packets. Net result: three weeks of marathon compute, zero governed gold promotions, T410 batch2 starved for integrator attention, and chunking velocity below the pre-fork baseline because the team spent time reconciling incompatible maps instead of owner-gated span work.

---

## Findings table

| ID | Severity | Area | Failure mode | Fix before marathon |
|----|----------|------|--------------|---------------------|
| F-001 | P1 | D / H | `scripts/compare_multi_model_bible_chunk_maps.py` referenced in comparison README and delta queue but **does not exist**; manual compare invites inconsistency and peeking | Implement script + pytest; wire into `validate_all.py` |
| F-002 | P1 | D | No validator for `whole_bible_chunk_map.jsonl` record schema, span normalization, or book-complete coverage | Add `validate_whole_bible_chunk_map.py` (required fields, span format, contiguous coverage per book) |
| F-003 | P1 | H | `agreement_rate_below_threshold_after_pilot_books` has **no threshold value** or pilot book list | Define threshold (e.g. &lt;60% exact-span agreement on pilot set) and pilot books in fork YAML |
| F-004 | P1 | D / Extra | At **N=3**, `ceil(0.7×3)=3` → easy bucket = full consensus; “majority” tier is meaningless | Document N≥4 for easy tier OR add separate `simple_majority` tier at N=3; block interim easy-chunk writes at N=3 |
| F-005 | P1 | F / Extra | `compare_when_at_least_models: 3` allows interim “easy chunk” calls before M4/M5 finish | Require `initial_target` (5) complete OR owner-signed interim scope; default compare at N≥5 |
| F-006 | P1 | G | T417 batch2 and T423 share agent surfaces and overlapping books (Jonah/Jude/Phlm) with no isolation rule | Add fork policy `parallel_path_isolation`: T423 must not read T417 layer outputs; separate worktrees; cross-link ban in marathon prompt |
| F-007 | P0 | B / LSN-041 | `do_not_stop_for: per_book_owner_gates_in_scratch` + “easy chunks” language risks treating agreement as promotion authority | Add explicit banner in agreement ledger schema: `promotion_authority: none`; require promotion packet for any T423→T410 handoff |
| F-008 | P0 | E | Whole-Bible marathon includes Revelation/Daniel despite T410 default deferral for apocalyptic/vision material | Add `deferred_books: [Rev, Dan]` or `marathon_exclusions` with evidence refs; or require frontier flag per apocalyptic book |
| F-009 | P1 | A | Fork authorizes whole raw Bible re-read per model; T410 substrate rule is compressed packs + span exceptions only | Require observation-substrate-first in marathon prompt; log raw USFM touch per book with exception id |
| F-010 | P1 | A | “Agreement = easy” assumes model diversity; shared LLM training → false consensus on verse/paragraph splits | Mandate `false_consensus_warnings` section in compare outputs; flag books where all models agree but stress atlas marks high risk |
| F-011 | P1 | C | `may_extend_research_in_scratch: true` without parity rules lets models diverge on baseline before chunking | Require `research_baseline_read: true` + hash of baseline manifest in each `model_manifest.yaml`; extensions logged separately, not in boundary_evidence_refs |
| F-012 | P1 | C | Baseline missing explicit DSS/variant policy and pastoral-epistle queue nuance | Extend `research_baseline_manifest.yaml` with variant/deferral surfaces from T410 queue |
| F-013 | P1 | D | M6–M10 `_TEMPLATE` copy is manual; no validator enforces manifest registration or folder naming | Extend fork validator for M6–M10 pattern; fail if folder exists but not in manifest |
| F-014 | P2 | D | `comparison/README.md` says compare at **2** models; fork policy says **3** | Align docs to `minimum_to_compare: 3` |
| F-015 | P2 | F | `FORK_README.md` lists `decision_log.jsonl`; policy requires `layer_decision_log.jsonl` | Fix README naming |
| F-016 | P1 | F | Session breaks leave partial maps; no rule forbids comparing incomplete books | Compare script must check `marathon_progress.yaml` per-book completeness before book-level agreement |
| F-017 | P1 | G | No T423 promotion packet template (SUB-012 is T417-only) | Add SUB-T423 template or fork-specific handoff schema for any scratch→governed promotion |
| F-018 | P2 | A | 3–10 model scaling invites scope creep (`owner_may_add_slots` without cap on concurrent marathons) | Cap initial experiment at M1–M4 required + M5 optional; M6–M10 only after pilot metrics |
| F-019 | P1 | E | Batch2 theology risks (Jonah typology, Jude noncanonical, Phlm ethics) amplified across 66 books without frontier layer | Import T417 batch2 escalation packets into baseline as **non-authorizing** warnings; require frontier flag in chunk map for flagged books |
| F-020 | P2 | F | Git scratch branch JSONL size / merge conflicts on parallel model commits | Recommend one worktree per model slot per scratch_lane_policy |

---

## Agreement-vs-delta logic audit

### Majority formula at N=3, 5, 7, 10

| N | ceil(0.7×N) | Agreeing required | Effective rate | Notes |
|---|-------------|-------------------|----------------|-------|
| 3 | 3 | 3 | 100% | **Easy tier collapses to full consensus** — no “supermajority without unanimity” |
| 4 | 3 | 3 | 75% | First, but only one dissenter allowed |
| 5 | 4 | 4 | 80% | Matches policy examples |
| 6 | 5 | 5 | 83% | |
| 7 | 5 | 5 | 71% | Two dissenters → still “easy” |
| 8 | 6 | 6 | 75% | |
| 9 | 7 | 7 | 78% | |
| 10 | 7 | 7 | 70% | Matches policy examples |

**Counterexamples:**

1. **N=3, two wrong + one right:** Two models agree on a bad boundary; one dissents correctly. No easy bucket (needs 3/3). Delta records it—but if integrator compares early at N=3 on a subset of books, a later fifth model never reopens “easy” labels.

2. **N=5, four wrong + one right:** Four models share paragraph-marker bias → **easy_majority** despite one WJ-aware dissent. Agreement logic prioritizes wrong work away from governed review.

3. **Near-miss (1–verse shift):** M1 `Jude.1.1-Jude.1.2`, M2 `Jude.1.1-Jude.1.3` — exact-match rules treat as full delta, but human review might consider “same opening unit.” Without overlap % in the **automated** compare script, queue priority is noisy.

4. **Chunk count mismatch:** M1 splits Psalms into 150 chunks (per psalm); M2 into 50 (grouped). Exact span comparison fails to produce meaningful per-region delta without normalizing to verse coverage first.

5. **False consensus on “easy” narrative:** Genesis 1–11 creation/flood units: all five models agree on chapter boundaries (training prior) while stress atlas marks discourse boundaries differently — agreement ledger marks “easy” incorrectly.

**Can agreement/delta prioritize work?** Only if: (a) compare script is deterministic, (b) span normalization is enforced, (c) near-miss and coverage metrics are automated, (d) false-consensus pass runs against stress atlas, and (e) interim compare waits for target N. **Current plan: partially specified; not trustworthy for prioritization without F-001–F-006 fixes.**

---

## Baseline comparison

| Dimension | T410 baseline | T423 fork | When baseline is strictly better |
|-----------|---------------|-----------|----------------------------------|
| Scope | One exact span / batch at a time | 66 books × N models | Always for authority-bearing promotion |
| Owner gates | Per-step owner gate before gold | Explicitly skipped in scratch | Any output touching gold or routes |
| Observation substrate | Required; whole-Bible raw re-read forbidden | Each model reads full raw USFM | Token cost, consistency, audit trail |
| Theology risk | Frontier escalation step | No frontier step in marathon | Jonah, Jude, Phlm, WJ, apocalyptic |
| Review cadence | LSN-039 daily Codex / weekly Claude | Not wired into fork | Long autonomous marathons |
| Comparability | Single governed artifact per target | N incompatible maps | Until compare script + schema validator exist |
| Speed claim | Slower per span, parallel batches | Faster bulk map | **Unproven** — 5× whole Bible likely &gt; 5× batch prep |
| Revert | N/A | Defined but unmeasurable threshold | When metrics undefined |
| Multi-model value | T417 ladder on 3 books with layer independence | Whole Bible agreement mining | T417 better for **promotion-ready** multi-model audit |

**Baseline is strictly better** for: reviewed gold path, chunk output pilots, theology-gated books, and any work requiring owner-approved exact spans. **Fork could beat baseline** only as a **non-authorizing prioritization radar** after a bounded pilot proves agreement correlates with later governed approval.

---

## Minimum fixes before M1 marathon

1. **Implement** `scripts/compare_multi_model_bible_chunk_maps.py` with span normalization, per-book completeness checks, overlap/near-miss detection, and pytest coverage (F-001).
2. **Implement** chunk map schema validator; reject maps with non-contiguous spans or invalid book codes (F-002).
3. **Define** numeric revert threshold and pilot book list in fork YAML (F-003).
4. **Amend** comparison policy: interim compare default at N=5 (initial_target), not N=3; document N=3 easy-tier collapse (F-004, F-005).
5. **Add** `parallel_path_isolation` rules and marathon-prompt ban on reading T417 batch2 artifacts (F-006).
6. **Add** `deferred_books` or apocalyptic marathon exclusions aligned with T410 phase_one_batch_order (F-008).
7. **Require** observation-substrate-first reads in marathon prompt; raw USFM exception logging (F-009).
8. **Extend** research baseline with variant/DSS/deferral surfaces (F-012).
9. **Add** agreement ledger field `promotion_authority: none` and README warning (F-007).
10. **Owner sign-off** on this red-team report and pilot scope (5 books below) before M1 start.

---

## Non-blockers to monitor

- P2 doc drift: comparison README “2 models” vs policy “3” (F-014); FORK_README decision log naming (F-015).
- M6–M10 governance until needed (F-013, F-018).
- Git scratch JSONL size / worktree hygiene (F-020).
- DAD outbox notifications before compare is validated—risk of premature external signaling.
- `may_extend_research_in_scratch` parity (F-011) — monitor via layer_decision_log audits.
- SUB-012 T417 promotion path proceeding independently—ensure no merge of T423 maps into SUB-012.

---

## Recommended experiment scope

**Do not run all 66 books initially.**

**Pilot: 5 books** (covers genre diversity + batch2 overlap + apocalyptic probe):

| Book | Rationale |
|------|-----------|
| **Gen** | Narrative + genealogy + creation discourse; tests long-book marathon pacing |
| **Ps** | Poetry/stanza/acrostic routing; chunk-count divergence likely |
| **Phlm** | T417 batch2 precedent; ethics pressure; short |
| **Jonah** | T417 batch2 defer case; typology smuggling test |
| **Rev** | Apocalyptic defer policy test — expect **exclude or frontier-only**; if included, measures false consensus on symbolic lit |

**Models for pilot:** M1–M4 required; **defer M5** until compare script validated on pilot. **Do not add M6–M10** until pilot delta_summary reviewed by owner.

**Success criteria for pilot GO to full marathon:** compare script runs clean; ≥1 known batch2 span (Phlm/Jonah/Jude) appears in delta or agreement with documented false-consensus check; no P0 leakage in layer_decision_log; integrator can produce delta_focus_queue without manual map reading.

---

## Non-authorizations confirmed

This reviewer **does not** and **cannot**:

- Authorize reviewed gold, chunk output, or canon writes
- Approve the fork as replacing T410 without owner phrase
- Start marathons (M1–M5 or M6–M10) in this session
- Treat agreement ledger entries as promotion-ready
- Write `whole_bible_chunk_map.jsonl` entries
- Merge T423 scratch maps into T417 SUB-012 or eval surfaces

---

*End of red-team pre-mortem report.*
