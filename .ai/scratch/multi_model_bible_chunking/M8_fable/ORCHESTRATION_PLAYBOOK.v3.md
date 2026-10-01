# M8_fable Orchestration Playbook — v3 (2026-09-14)

This playbook records how the campaign runs its agents and subagents, and what the receipts say worked, so the method can be re-run and
improved. It was written at the owner's direction (ledger OW-14, 2026-09-11, verbatim there).

- **Scope.** The M8_fable whole-Bible chunking marathon, as practiced through Ezekiel's FIXUP-3 wave and S4's stopped execution.
- **Status.** Candidate-only and non-authorizing. Owner directives, the error-pattern ledger, the close gate and the controlling agent's
  rulings outrank anything here. This file describes them and points to them; it never replaces them.
- **History is append-only.** A version is never rewritten. A change is a new version with a "Changed since" section naming the learning-log
  entries that justify it. v1 and v2 are retained unchanged. The resume prompt names the current version.

## Changed since v2

Four entries, all from 2026-09-13/14, change recommendations in §3–§5:

- **L-0017 (control, mixed).** #e10 ordered a lookup along a route that did not exist: neither Jeremiah nor Lamentations has a transcript
  map, and the capture index carries the literal string `UNAVAILABLE` as the agent_id of all 135 of their rows. 115 transcripts and 115 meta
  files (90,640,229 bytes, none empty) stood in a session the census recorded as retaining 0 and 5. → §3 step 7, §4.
- **L-0018 (control, failed).** S4's brief was copied from S3's and launched with four keys `validate_s4` refuses. A brief's deliverable
  schema and the landing job's validator are two statements of one contract. → §3 step 3b, §4, §5.
- **L-0019 (tool, failed).** `budget_pre_primaries.py`, named by GATE-E10 for the owner check-in, hardcoded the superseded ceiling of
  21,500,000 and read a stale corpus, so it reported a headroom of −1,433,978 that was not real. → §3 step 5, §4, §5.
- **L-0020 (control, mixed).** A failed notification shows an agent's FIRST words, not its last. S4 was read as a dead start and reported to
  the owner as having produced nothing; it had made 95 tool calls and written a complete 108,580-byte review. → §2, §3 step 8, §4.

## 0. Where everything is

Campaign root: `C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\` (below, `M8\`). `SP\` means `M8\sp_durable\`.

| What | Where |
|---|---|
| This playbook, its learning log, its metrics | `M8\ORCHESTRATION_PLAYBOOK.v3.md` (v1, v2 retained), `M8\orchestration_learning_log.v1.jsonl`, `M8\orchestration_metrics.v1.json` |
| Owner directives and error classes | `M8\ERROR_PATTERN_LEDGER.v1.md` + `M8\error_pattern_ledger.v1.jsonl` |
| Book-close conditions | `M8\CAMPAIGN_CLOSE_GATE.v1.md` (items 1-18) |
| Capture law (per-attempt records, three layers) | `SP\campaign\CAPTURE_CONTRACT.v3.md` |
| Resume after a clear | `M8\RESUME_PROMPT_CURRENT.md` from `SP\orchestrator_scratch\_gen_resume_prompt.py` + `_state_*.json`, verified by `SP\Jer\_safe_to_clear_check.py`; index `M8\CURRENT_STATE.v1.json` |
| A book's working state | `SP\<Book>\` — `freeze\CYCLE_STATE.md` (append-only, with the cursor), rulings, orders, briefs, repair chain, suites, coverage |
| Execution records | `SP\<Book>\**\*_attempt_receipts.jsonl`, `SP\<Book>\_transcript_map.<book>.json`, `SP\<Book>\evidence_notes\`, `SP\transcripts\`, `SP\campaign\capture_index.v1.jsonl` |
| Superseded outputs (never deleted) | `SP\<Book>\repair\superseded_<stage>\` with a `NOTE.json` holding every digest before and after |
| **A finished deliverable whose execution did not land** | `SP\<Book>\pending_<job>\` with a `NOTE.json`: held is not accepted (§3 step 8) |
| Campaign controls | `SP\campaign\_inflight_pin_guard.py`, `_brief_pin_check.py`, `_guarded_json_patch.py`, `_brief_shape_headroom.py`, `_check_brief_schema_vs_validator.py`, `_cure_verification.py`, `_orchestration_metrics.py` |
| Scripts the orchestrator actually ran (Ezekiel, from S2 on) | `SP\orchestrator_scratch\ezek_post_s2\`, kept byte for byte |

## 1. The mesh (who does what)

### 1.1 Current roles (owner directive OW-13, 2026-09-11)

| Role | Model | Does | Never does |
|---|---|---|---|
| Orchestrator | the claude-opus-5 main session (Ezekiel and Daniel, under OW-11) | routes; builds orders, briefs and launch messages from sources; launches; lands; runs the deterministic tools; keeps records and checkpoints | rules, authors rows, or checks its own work |
| Controlling agent / architect | claude-fable-5-1 executions | rulings, gates, corpus-wide orders, strategy acceptance, the hardest judgment | author the rows it rules on |
| Substantive author and researcher | claude-opus-5 subagents | author and fix-up waves, research-heavy lanes, repair of another model's rows | check its own output |
| Checker and adjudicator | claude-fable-5-1 subagents | distinct checks, boss adjudication, final checks | check work it authored |
| Bounded low-level worker | claude-sonnet-5 subagents | narrow, low-judgment work | work that should be Fable's, or substantive authoring |
| Deterministic tools | scripts | sweeps, coverage, tiling, the suite, pin guard, pin check, shape headroom, schema check, gate checks, landing, apply, checkpoints | judgment |
| Owner | Lowell | authority, budgets, directives | — |

**When the checker's model runs out.** Fable quota can be exhausted mid-campaign, and was on 2026-09-14. The distinct check is NOT reassigned
to save quota — #e10 S3-ROUTING (7) and OW-13 both require a checker that is not an author, and the authors here were Opus. An execution the
runtime kills is RESUMED UNDER ITS OWN EXECUTION ID once quota returns, and if it had already finished its work, the resume asks only for the
missing record. Its receipt states what the runtime reported and what it did not. Everything that does not need the scarce model — scripts,
applies, gates, records, findings, preservation, this playbook — runs meanwhile.

### 1.2 Earlier meshes

- **Books 1-24.** A claude-fable-5 orchestrator with a capability-routed mesh; escalation deterministic → haiku → sonnet → opus → fable →
  human, "higher tier is not automatically correct", ≤3 hops and ≤8 decisions per attempt; two blind primaries on different models.
- **Genesis.** Sonnet book writer; blind primaries OL on opus-5 and LF on sonnet-5; sonnet peers; fable-5 boss adjudication.
- **Proverbs.** First scoped mesh: dual-blind LF+OL over scoped rows, remainder carried by Tier-0 checks and a sample.
- **Ezekiel (OW-11).** Opus: orchestrator, Phase 0, T5, and S1-S3. Fable: the strategy and #e1-#e10. Sonnet: eleven writers, T1-T4, T6, and
  the FIXUP-1/2/3 authors. From OW-13: p01 #e3 and p03 #e2 on Opus; S4 on Fable.

A mesh on one model family is one correlated voice. Agreement inside it is corroboration, not independent evidence.

## 2. The loop for a hard-track book

```
Phase 0 staging -> strategy (Fable) -> writer wave -> S1 spot review (distinct)
  -> controlling execution #eN (Fable rulings)
       -> deterministic sweeps (CWO) -> tool fixes staged and installed by receipt
       -> fix-up wave: orders -> brief (example wording MEASURED; schema CHECKED against the landing validator)
            -> pin check -> budget test -> gate check -> launch -> land -> transcript audit
            -> apply -> suite -> coverage
            -> a gate failure relaunches the part that caused it, with the measurement in the message,
               and the earlier apply's outputs are superseded, never overwritten
       -> fresh distinct check S(N+1) on the applied rows
            -> if the runtime kills it: HOLD any finished deliverable, record the execution as stopped,
               resume that execution id for what is missing; never re-run finished work
       -> repeat until the distinct check reads rows readiness fit=true
  -> rows cure claims (artifact-bound verification + the distinct checker's verdict)
  -> primaries -> finalize -> close gate -> OW-12 status update -> OW-14 playbook and log -> next book
```

Ezekiel's path: FIXUP-1 → S2 → #e9 → FIXUP-2 → S3 → #e10 → CWO-EZ-23/22 → TOOLFIX-5 → FIXUP-3 (applied twice; run 1 failed its ngram7 gate
and p03 ran again on Opus) → S4 (reviewed, stopped at its final message, held).

## 3. The launch protocol

1. **Generate, never hand-transform.** Orders come from the rulings text by a builder that refuses a disagreement; briefs carry ruled text
   verbatim.
2. **Preview, then write.**
3. **Pin check MATCH before every launch** (`_brief_pin_check.py`, OW-11-l).
3a. **Measure any example wording before the brief offers it** (`_brief_shape_headroom.py`, L-0012/L-0014): a shape is SAFE only when
   `gate - 1 - rows_already_carrying_the_gram >= parts`.
3b. **Check the brief's deliverable schema against the landing validator** (`_check_brief_schema_vs_validator.py`, L-0018): every
   `d.get("<key>")` in the validator's own body must appear in the brief's schema block. The validator is the contract; the brief restates
   it. Where the validator demands a value no artifact can supply, the brief says so and tells the agent to measure it. A brief pinned by a
   running execution is never edited — the correction goes to the agent by message and into the builder.
4. **The launch message** carries, in order: the E-13 preamble; the OW-11 authority paragraph with the owner's verbatim answers; the E-19
   no-check line and exact-path law; the pinned-input rule; the validator verdict; the #e8 T6-02 verdict wording; the job with digests.
5. **Budget test at the measured maximum**, from a script that reads the ceiling from the carrier the owner's answer updates — never from a
   hardcoded constant (L-0019). When an owner answer changes a number, control (u)'s sweep includes the SCRIPTS that consume it.
6. **Gate check before a gated launch**: a script decides each ruled clause from the artifacts and binds every report to the corpus digest.
7. **Record at launch:** transcript-map entry through `_guarded_json_patch.py`, then one CYCLE_STATE entry, then a durability checkpoint.
   **Write the map entry WHILE the agent runs** (L-0017): an agent id not recorded at launch cannot be recovered from any later artifact.
8. **On completion — and on failure, which looks nothing like it (L-0020):**
   - a failed notification carries the agent's FIRST words, its error, and sometimes no usage at all. **Check the deliverable path by exact
     path before describing the execution.**
   - if a finished deliverable exists, copy it out of the volatile scratchpad into `pending_<job>\` with a NOTE, and record it as HELD —
     holding bytes is not accepting them;
   - save the record from the runtime notification by script; run the pin guard; land with the ordinal from the agent's own record;
   - preserve transcripts, then **audit** them: count the tool calls, prove no listing or existence check stands on a line carrying a tool
     call, prove no write landed inside the worktree;
   - write a CYCLE_STATE landing entry whose observations are checked against the record, not copied from it.
9. **A decline** is recorded and relaunched once with a context paragraph; a second goes to the owner. **A gate failure** is relaunched with
   the measurement. **A runtime kill** is resumed under the same execution id for exactly what is missing.
10. **Tool changes are plumbing or they are rulings.** Plumbing is staged with a preimage, a diff the distinct checker reads, an install
    receipt and a regression reproducing existing outputs byte for byte. A tool verifying another tool's digest names the receipt per member.
11. **The distinct check** reads the applied rows. Cure claims are written only on its fit=true verdict in the ACCEPT form.

## 4. What the evidence says

- **Worked: generating artifacts from sources.** Builders that refuse disagreements caught a misstated ruling span before any author saw it.
- **Worked: the pin check, the authority paragraph, and auditing transcripts at landing.** p08's undisclosed lapses were found this way;
  p03 #e2's audit, by contrast, confirmed its self-report (24 tool calls, no listing, one write in its own scratch).
- **Failed: example wording in a brief (L-0012)** — cost one re-execution, a second apply and two plumbing patches.
- **Failed: figures read rather than measured (L-0014)**; **a brief schema never checked against its validator (L-0018)**; **a gate's own
  script carrying a superseded ceiling (L-0019)**. Each was caught by reading an artifact, not by a control; each now has one.
- **Worked: Opus repairing another model's rows (L-0015)** — 47% more tokens, suite RED → GREEN, three byte-corrections disclosed.
- **Worked: superseding rather than overwriting**, and **preserving on discovery (L-0017)**: 230 files, 90.6 MB, one runtime cleanup away
  from being unrecoverable, in a session the census called empty.
- **Mixed: reading a failed notification as a status report (L-0020).** A completed 108,580-byte review looked like a dead start; the owner
  was told the wrong thing and chose a full re-run on that basis. A guard caught it — the record script refused because it found a
  deliverable at the path it was asserting did not exist — and the owner was corrected before anything was spent.
- **Open: the residual the gate does not catch.** Two seven-word families stand at 9 rows against a gate of 10 over rows_v6.
- **Open: model versus wording in declines.** Every REFUSED_NO_DELIVERABLE receipt in Ezekiel is a claude-sonnet-5 execution; model and
  wording are confounded.

## 5. Re-running from this

1. **Read first:** this playbook, the ledger, the close gate, `model_manifest.yaml`, and the learning log's latest entries.
2. **Stand up a lane:** a registered worktree with the governance validator passing; the `SP\` layout with the capture contract; a resume
   generator and checker with the owner's rules as canonical clauses; **a transcript map written from the first launch onward**.
3. **Per book:** follow §2, with the Ezekiel scripts in `SP\orchestrator_scratch\ezek_post_s2\` as templates:
   - orders and brief builders: `_build_fixup3_orders_ezek.py`, `_fixup3_brief.py`, `_s4_brief.py`;
   - before a brief: `SP\campaign\_brief_shape_headroom.py`, `SP\campaign\_check_brief_schema_vs_validator.py`;
   - launches and relaunches: `post_launch_fixup3.py`, `_fixup3_relaunch_message.v3.py`, `post_relaunch_fixup3.v3.py`, `post_launch_s4.py`;
   - records: `_save_agent_record_fixup3.py`, `record_refusal_fixup3.v2.py`, `record_s4_stop.v2.py`;
   - holding a finished deliverable: `preserve_s4_deliverable.py`;
   - landing entries and audits: `post_land_p03_e2_and_run2.py`;
   - apply pipeline (latest landed execution per part): `post_fixup3_pipeline.py`; superseding: `supersede_v6_run1.py`;
   - gates and budget: `gate_e10_s4_check.py`, `budget_pre_primaries.v2.py` (v1 retained, superseded ceiling);
   - evidence preservation: `preserve_jer_lam_transcripts.py`;
   - checkpoints: `checkpoint_fixup3_ready.py`, `checkpoint_s4_ready.py`, `checkpoint_s4_inflight.py`, `checkpoint_s4_stopped.py`.
4. **Owner answers:** every owner answer that changes a standing rule is recorded as a directive in every carrier (ledger MD and JSONL, gate,
   CYCLE_STATE, canonical checker clause, state input, campaign memory) **and in every script that consumes it**, in the same step.
5. **Iterate** by §6.

## 6. Iteration protocol (OW-14)

- **When.** At every wave landing, distinct-check landing, controlling-execution landing, and book close.
- **Learning log.** Append to `M8\orchestration_learning_log.v1.jsonl`; never edit an entry; a correction is a new entry with `supersedes`.
  Schema `m8_orchestration_learning.v1`: `id`, `date`, `book`, `stage`; `element` (role | model | lane | topology | control | tool | wording |
  budget); `observation`, `evidence_refs[]`, `metric{}`; `verdict` (worked | failed | mixed | open); `recommendation`, `supersedes`.
- **Metrics.** `python SP\campaign\_orchestration_metrics.py --write`, grouped by book, lane and model ordered.
- **Versions.** When the evidence changes a recommendation in §1-§5, write the next version with "Changed since vN" naming the entries, and
  point the resume prompt at it. Earlier versions are retained unchanged.
- **Gate.** Close-gate item 18 checks this at every book close.
- **DAD.** Major lessons also go to DAD's lesson intake (campaign memory: dad-lesson-routing-rule).
