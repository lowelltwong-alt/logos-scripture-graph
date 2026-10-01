# CAMPAIGN CLOSE GATE — mandatory retro-passes before the marathon is declared complete

- Schema: `m8_campaign_close_gate.v1`
- Authority: owner directive, Lowell Wong in chat 2026-08-27 ("the LF-support audit lane
  runs by default in every future book — can you assure that we do [run it] on past books
  once Revelation is completed").
- Binding on: the session that closes Revelation (66/66) and ANY session asked to declare
  the M8_fable marathon complete, produce final campaign receipts, or hand off to
  convergence/comparison. This gate BLOCKS `marathon_status: complete` until satisfied
  or the owner explicitly waives a named item in chat.

## Gate items

1. **RETRO LF-SUPPORT AUDIT (the B-8 lane, applied backward).** The lane exists because
   Isaiah's audit found 19/31 sampled LF-supported rows defective (~12/31 LF-attributable,
   1 high). Books closed BEFORE the lane existed never had it:
   - REQUIRED SCOPE: the 22 pre-Isaiah books — Gen, Exod, Lev, Num, Deut, Josh, Judg,
     Ruth, 1Sam, 2Sam, 1Kgs, 2Kgs, 1Chr, 2Chr, Ezra, Neh, Esth, Job, Ps, Prov, Eccl, Song.
   - Per book: rebuild the LF-support frame from that book's primary packets
     (sp_durable/<book>/reviews or the durable review record), draw a deterministic
     sample at a size sustaining a reliability statement (Isa precedent: every 5th of
     the id-sorted frame, ~20%), audit each sampled row AS SHIPPED in
     book_chunks/<book>/chunks.jsonl with the OL-grade adversarial lens, and report the
     defect rate as a digit with its object named. File per-book packets + one campaign
     roll-up.
   - Books Isa..Rev carry the lane by default at close; verify each book's receipt
     records its digits — any book that slipped joins the retro scope.
   - Findings feed a remediation docket for owner triage; no silent fixes.
2. **STANDING RE-SCAN QUEUE (ERROR_PATTERN_LEDGER.v1.md).** Run the deterministic sweeps
   over every completed book's chunks.jsonl: normalize dry-run reading the fixed COUNT
   (E-01), whole-chapter cap sweep (E-02), register pattern list incl. the hardened
   "that row"/"cross-part" arms (E-06/E-18 residuals), mark-position grep (E-07), oss-key
   grep (E-09), curly-quote parity + Hebrew-inside-curly (E-15); plus the sampled passes:
   byte-claim re-collation (E-05) and reviewer-ledger Hebrew-citation verification (E-03).
3. **DEFERRED ITEMS STILL OPEN AT CLOSE.** Verify disposition (done or owner-waived) of:
   the Prov opus OL spot-wave; the tool promotions (nfd_degraded→hard, Tier-0 cap gate,
   E-15 unclosed-quote detector, E-16 universals-dampener patch).
4. **OW-1 OWNER-WARNING RETRO/PROSPECTIVE OBLIGATIONS (added 2026-08-31).** The owner
   process-quality warning (verbatim in ERROR_PATTERN_LEDGER.v1.md §Addendum 2026-08-31
   and in the OW-1 JSONL row) named three watch lanes: lost corpus-wide review orders
   (E-18), punctuation-driven boundary errors (E-23), second-generation repair defects
   (E-17). Status at recording:
   - DETERMINISTIC RETRO PASS: DONE 2026-08-31 over all 23 completed books —
     `retro_scans/2026-08-31_owner_warning/report.v1.json` (3,945 rows; trigger queues
     REG 771 / PUNCT 109 / EXCL 189 + the carriage-language inventory over the five
     books with surviving review layers). Flags are review triggers, not verdicts.
   - STILL BLOCKING at close: model-lane triage of those trigger queues (the PUNCT
     queue especially — sampled characterization found genuine E-23-class
     corroboration-position instances, incl. one in shipped Isa), folded into or run
     beside gate item 1's retro audit; and the E-18 carriage SEMANTIC audit for the
     books whose review layers survive (Eccl, Prov, Ps, Song, Isa). Books without
     surviving review layers are corpus-pattern auditable only — record that limit in
     the campaign roll-up, never paper over it.
   - PROSPECTIVE (per book from Jer on): the E-23 pattern sweep runs at every rev
     round; each book-close receipt records its E-23 sweep digits alongside the B-8
     lane digits; any book that slips joins the retro scope.

5. **OW-2 HARD CLOSE GATES (owner directive, 2026-08-31 — each blocks book-close for
   every book from Jeremiah on AND campaign close for all books).** Every book-close
   receipt must record, with exact denominators, evidence paths, and hashes (OW-2
   item 6):
   - CWO EXECUTION PARITY: every corpus-wide order recorded for the book carried to
     execution as its own sweep, with the executed/ordered parity digits.
   - HEBREW/GREEK QUOTE BYTES + TIER LABELS: every original-language splice
     byte-collated at its cited ref; every tier label per collate truth
     (byte / accent_stripped / skeleton never conflated).
   - WEB QUOTE/GLOSS FIDELITY: curly-quoted WEB runs verbatim with in-field refs;
     gloss extent equals splice extent.
   - UNICODE NORMALIZATION: normalize dry-run fixed=0 defect=0 over the final corpus
     (count read, never the status line).
   - REVIEW-PACKET RETENTION: the book's primary/peer/boss/author/spot/postcheck
     packets durably retained (sp_durable or successor), enumerated with hashes.
   - APPEALS: append-only appeal state resolved or explicitly held, enumerated.
   - FINAL review_status: no finalized row labeled draft; deferred-review labels
     enumerated with their owner disposition. (Backlog at recording time: the FOUR
     final_deferred_review rows — Deut M8-Deut-101, M8-Deut-193, Gen M8-Gen-084,
     Judg M8-Judg-140 — await owner triage; the 347 draft-labeled Eccl/Song/Isa rows
     were owner-ordered resolved under OW-2 item 3.)
   - SECOND-GENERATION ROLE SEPARATION (OW-2 item 4): each repair wave followed by a
     fresh full sweep; the repair author never the final checker; producer/catcher
     roles recorded.
6. **OW-2 REVELATION REQUIREMENTS (owner directive, 2026-08-31).** The Revelation
   cycle requires Opus 5 HIGH review PLUS Fable 5 HIGH adversarial adjudication for
   vision-cycle, speaker/voice, quotation, recapitulation-versus-sequence,
   textual-variant, and cross-chapter seams. Editorial headings and translation
   punctuation are NEVER boundary drivers (E-23 + the NT paragraphing law).
   Anthropic-family agreement is ONE correlated M8 voice.
7. **OW-2 RETRO SEMANTIC AUDIT (owner directive, 2026-08-31 — scheduled NOW, not at
   Revelation).** Item 1: Isa LF-SUPPORT frame 155/155 rows, fresh Opus 5 high
   primary review; med/high defects, span proposals, and disagreements route to
   Fable 5 high; xhigh only for unresolved book-level structure. Item 2: Ps/Job/
   Prov/Eccl/Song — the 213-row verified semantic-adjudication scope + the deferred
   38-row Proverbs Opus review. Pre-warning hashes preserved; M7 never read. The
   audit runs as internal M8 QC under the pause ordered before Lamentations.
   *(OW-2D SEQUENCING RULING, owner 2026-08-31: AUDIT FIRST — Jer waves 2-3 and all
   later Jer work stay paused while the three NOT STARTED items complete;
   CONDITIONAL AUTO-RESUME when all three audit receipts pass AND every required
   repair has passed a fresh independent second-generation sweep AND no unresolved
   medium/high defect, proposed span change, systemic method issue, or owner gate
   remains — Jer then resumes automatically from phase = ow2_checkpoint_pause at
   author wave 2 under the permanent safeguards; ANY unresolved such issue instead
   STOPS the resume and is reported with the exact evidence and decision needed.
   The `_safe_to_clear_check.py` exact-path + negative-fixture hardening is a
   pre-audit-launch gate, recorded as a transport/copy-resilience control
   improvement.)*

## Carry law

Every session's printed resume prompt from Jeremiah onward carries one sentence pointing
at this file (pattern: "CAMPAIGN-CLOSE GATE standing: CAMPAIGN_CLOSE_GATE.v1.md blocks
marathon completion behind the retro LF-support audit of the 22 pre-Isa books + the
ledger re-scan queue — carry this sentence in every future resume prompt"). A session
that notices the sentence missing restores it from this file and records the lapse as
an E-18-class instance.

OW-1 CARRY LAW (owner order, 2026-08-31): every session's printed resume prompt also
carries the owner process-quality warning VERBATIM — "Process-quality warning: watch
specifically for lost corpus-wide review orders, punctuation-driven boundary errors, and
second-generation defects introduced during repairs. Do not inspect or imitate M7
boundaries. Independently audit M8's own evidence, record the warning and method-version
change, preserve the pre-warning artifacts, and rerun the applicable checks
retrospectively across completed books as well as prospectively" — plus the instruction
to keep carrying it. A session that notices the clause missing restores it from this
file (or the ledger's OW-1 row) and records the lapse as an E-18-class instance.
*(SUPERSEDE-WITH-NOTE, owner clarification OW-2-CARRY-IDEMPOTENCY 2026-08-31: this
verbatim-carry obligation is SATISFIED from now on by the permanent-safeguards list in
each generated prompt — the list subsumes OW-1's substance; the warning text above
remains the durable restore source. OW-1's "rerun the applicable checks retrospectively"
means complete each governed retrospective scope ONCE, receipt-gated; it does not mean
repeat completed audits after every clear.)*

OW-2-CARRY-IDEMPOTENCY LAW (owner clarification, 2026-08-31 — verbatim in
ERROR_PATTERN_LEDGER.v1.md §Addendum OW-2-CARRY-IDEMPOTENCY, binding):
- The OW-2 retrospective rechecks are ONE-TIME, receipt-gated work. Until a one-time
  item is complete, prompts carry only its current status, unresolved scope, exact
  cursor, and expected receipt path. Once it has a passing completion receipt under
  M8_fable/receipts/ and its pinned input/dependency hashes still match, it is DONE:
  prompts carry only the receipt path and completion digest, and the work is NEVER
  rerun — except on an absent/failed receipt, a pinned-hash invalidation of the
  applicable gate, or an explicit owner rerun order.
- One-time items: the 155/155 Isaiah LF-support audit; the 213-row Ps/Job/Prov/Eccl/
  Song semantic scope; the deferred 38-row Proverbs Opus review; the immediate
  audit-budget checkpoint; the pre-Lamentations pause. The 347 review_status
  correction is DONE (receipts/OW2_review_status_resolution.json) — resume sessions
  verify its pinned hashes, never re-perform it unless invalidated.
- PERMANENT prospective safeguards (the only permanently-carried clauses): no M7 or
  comparison-data reads; translation punctuation, headings, and other tier-4 metadata
  never drive a boundary; corpus-wide-order execution parity; the hard book-close
  gates; a fresh full second-generation sweep after each repair wave with a checker
  distinct from the repair author; actual model/effort, denominators, producer/catcher
  roles, evidence paths, findings, and hashes in attempt receipts; Anthropic-family
  agreement treated as one correlated M8 voice; the Revelation-specific Opus 5 high +
  Fable 5 high adversarial review requirements.
- SESSION-CLOSE PROTOCOL: generate the next prompt from the latest durable cursor and
  receipts; never carry consumed batch instructions or completed rechecks as active
  work; before printing SAFE-TO-CLEAR, verify MECHANICALLY (staged tool
  sp_durable/Jer/_safe_to_clear_check.py) that the prompt contains the
  OW-2-CARRY-IDEMPOTENCY marker, the latest unresolved-item cursor, the
  completed-receipt pointers, the permanent safeguards, and the instruction to
  generate the following prompt. The pre-OW-2 pasted resume prompt is superseded and
  retained only as historical evidence.


8. **OW-3 QUALITY-CONTROL FOLLOW-UP (owner directive, 2026-09-04 — binds every remaining
   phase, every future book, and the campaign close; the verbatim directive lives in
   ERROR_PATTERN_LEDGER.v1.md §Addendum 2026-09-04 and the OW-3 JSONL rows).**
   - AUDIT != REPAIR: a DONE audit receipt never implies repairs; each remediation docket
     carries a dispositions ledger (open/resolved + independent post-repair evidence);
     low findings are retained with explicit handling; Jer resumes only when the OW-2D
     gate is ACTUALLY satisfied; the 347 correction and every completed retrospective
     audit are never rerun merely after a clear.
   - REPAIR PROPOSALS are validated as adversarially as rows: replacement claims need
     independent source evidence or qualification; unexpanded placeholders are rejected
     by every lane verifier and resolved from source bytes before any application; one
     source occurrence with several row repairs is recorded as such.
   - BOTH-SIDES SEAM LAW: refrains close units (Isa §6 and each book's ruled seam law);
     an onset-only diagnosis is incomplete until the adjacent unit's close/onset is
     weighed; bounded re-adjudication when a completed audit's subset depended on the
     onset-only assumption — never the whole audit by default.
   - DEPENDENCY APPLICABILITY: when a pinned shared tool changes, record old/new hashes,
     scope, and whether earlier receipts are affected; preserve old evidence; never
     silently rewrite history or reflexively redo unchanged work.
   - HONEST EFFORT REPORTING: the actual model is evidenced; "high ordered" is not
     "high verified" without runtime effective-effort evidence.
   - PRE-PRINT CHECKER (v2): canonical prohibitions verified, contradictions rejected,
     prompt bound to the latest durable cursor / attempt dispositions / audit-vs-repair
     state, docket pointer + hash required, negative fixtures for every case.

OW-3 CARRY LAW (owner order, 2026-09-04, verbatim: "make sure the next prompt you give me
for clear promp has the improtant things fomr this latest addition to the  prompt always
persistnat for the rest of the cycle until the bible isocompleted"): every generated resume
prompt carries the OW-3 permanent safeguards as canonical clauses until the marathon
completes (66/66); the hardened checker fails any prompt that drops one.


OW-4 SEQUENCING RULING (owner directive, 2026-09-05, verbatim: "get this book compleyted"): recorded in
ERROR_PATTERN_LEDGER.v1.md §Addendum 2026-09-05 and the OW-4 JSONL row. Operational reading
(orchestrator, correctable by the owner): Jeremiah's completion proceeds now under every
permanent safeguard and every hard close gate of this file; the OW-2D conditional-resume text
in item 7 stands as history with its criteria 2 and 3 recorded NOT satisfied at the time of
the ruling; the three owner-triage dockets stay OPEN; nothing is applied to any shipped
corpus; the pre-Lamentations pause is not lifted by this ruling.

OWNER CONFIRMATION of OW-4 (verbatim, in chat 2026-09-06, after the orchestrator stated its operational reading and offered to stop): "yes complete jeremiah". The reading recorded under OW-4 stands as confirmed: Jeremiah's completion proceeds under every permanent safeguard; the three owner-triage dockets stay OPEN; nothing is applied to any shipped corpus; the pre-Lamentations pause is not lifted by this confirmation.


9. **OWNER_REPAIR_ADVANCE_2026-09-06 (owner standing ruling, 2026-09-06; canonical verbatim copy: OWNER_REPAIR_ADVANCE_2026-09-06.md (sha256 597aea4fd24d2f1de93644cf2689ae4317d415403fa14dfca42c8445ebc9258a)).**
   - SUPERSEDED AS ACTIVE CONTROLS (kept above as history, marked here): item 7's OW-2D owner-only
     docket-triage WAIT and 'STOP and report the decision needed' arm; per-proposal owner
     span-approval; the owner-only pre-Lamentations pause (lifts when Jeremiah passes its hard
     close gates; then Lamentations and subsequent books proceed in canonical order).
   - STILL BINDING: every hard book-close gate of this file (items 5-6, 8); the OW-2D criteria as
     the ledger EVALUATION (three receipts DONE; every required repair through a fresh
     distinct-checker second-generation sweep; zero unresolved medium/high defect, span
     proposal, systemic issue, or owner gate) — an evidence-backed rejection is
     resolved-no-change, not an applied repair; r3 routing, blind coverage, Revelation's
     special review, honest effort reporting; budget check-ins; no merges/publication/new
     worktrees/cross-lane inputs/unattended runtime.
   - PROV DENOMINATOR RULED: 38 is the historical denominator of the completed Prov-38 review;
     supplemental crux-site observations are recorded separately with their own scope; the
     completed review is never reopened for a counting question (the crux-zones owner gate is
     CLOSED).
   - CONTINUITY: M8_fable/CURRENT_STATE.v1.json (verified current state + canonical active
     rules) replaces the mandatory full-history CYCLE_STATE reread; CYCLE_STATE remains the
     immutable log; the checker v3 requires the ruling + index pointers with hashes and rejects
     stale owner-triage waits; the prior current prompt is archived hash-addressed at every
     close; the saved prompt is read back and verified before it is printed.


OW-5 SEQUENCING + BUDGET RULING (owner directive, 2026-09-06 session 3, verbatim: "complete this book. dongt worry about the token budget just get it complete. then start the next book with out the clear repropt step. jsut proced to teh next book and complete it too."; confirmed verbatim: "approved"): recorded in
ERROR_PATTERN_LEDGER.v1.md §Addendum 2026-09-06 OW-5 and the OW-5 JSONL row. Operational reading (orchestrator, correctable by the owner):
budget check-in #2 answered (go); the per-session soft cap and pre-8M check-in are waived for completing Jeremiah and Lamentations; after the
Jeremiah hard close (items 5-6, 8 of this file) the lane proceeds straight into Lamentations in the same session with a silent durability
checkpoint (no printed prompt, no stop); every hard close gate of this file binds Lamentations exactly as it binds Jeremiah.


10. **OW-6 FINAL-CHECKER GATE + FABLE BOSS ESCALATION AUTHORITY (owner directive, 2026-09-07 — binds Lamentations and every book after it).**
    Owner words (verbatim): "lets change how we comnplet the books slightly. i'll keeo opus 5 as the orcistrator and run the smae sub agent artecture and flows but adapted to all teh future books we do. we will clear and reprompt only when needed so monitor that. but lets alway continue to th enext book form the rpevious one. and use fable 5.1 subagent to be the final checker of the books before we complet and close them checking all the work and audit logs everythign written by a  subagent even chain of thought fo rit. and fable 5.1 is the boss and escaltions go ti it and it decides when the risk is hienough and debendancies/blast radious of a ecision needs for it ti sak a human . when it ask a human it present the coices with its recomendation and why and hte other choices with the pros and cons. this ieeds to be persistant so add it to the clear follow up promt given when we do do that cycle for the rest of this."
    - **FINAL CHECKER (hard gate; blocks book-close).** Before a book is completed and closed, a claude-fable-5-1
      subagent audits the WHOLE book: the final corpus, every audit log and receipt, every artifact written by any
      subagent in the book's cycle, and the captured reasoning transcripts of those subagents where they exist. Its
      verdict vocabulary is fit_to_close | not_fit_to_close. fit_to_close is required for the close, exactly as the
      postcheck's fit_to_assemble is required; a not_fit_to_close verdict blocks the close, orders a bounded fix
      round, and is followed by a FRESH final check. The final checker never edits the corpus; it reviews.
    - **BOSS = claude-fable-5-1.** The mesh's boss role is Fable 5.1 from this directive on. Every escalation from any
      lane routes to it. It decides - the orchestrator does not - when a decision's risk, dependency graph and blast
      radius require a HUMAN.
    - **HUMAN-ESCALATION PACKET.** When the Fable boss escalates, it presents the choices: its RECOMMENDATION with the
      reason, and every other choice with pros and cons. The orchestrator surfaces the packet to the owner verbatim
      and does not pre-decide the escalated question.
    - **CONTINUITY.** Book-to-book continuation is permanent: every close is followed immediately by the next book
      under the silent durability checkpoint. Clear-and-re-prompt happens only when needed and the orchestrator
      monitors for that need; the directive is carried in the prompt slot as canonical clauses so a clear cannot drop
      it.


11. **OW-6b HARD-BOOK TRACK + FABLE AS CONTROLLING AGENT (owner directive, 2026-09-07 — binds every remaining book).**
    Owner words (verbatim): "also fable shoudl be teh controloing agent and extra scruiney over the hardest books we anticpate doing this to like revelation, daniel, research which those are thit lots hor hard greek or hebrew translations lots of hard types of litature or profacies or connections, or passages the Church struggles withor theChurch disagrees about."
    - **CLASSIFICATION ARTIFACT (blocks the start of a book's cycle).** book_hardness_classification.v1.json classifies
      every remaining book STANDARD or HARD against the owner's rubric: hard Greek/Hebrew translation problems; many or
      difficult literature types; prophecy; dense cross-book connections; passages the Church struggles with or
      disagrees about. Revelation and Daniel are owner-named HARD. Each entry carries its evidence and its score per
      criterion; the artifact is append-only versioned and may be re-classified upward with a recorded reason.
    - **HARD TRACK (extra scrutiny; each arm blocks that book's close).** claude-fable-5-1 is the CONTROLLING agent:
      every boundary decision, adopted change, escalation and the close are its calls. The boss lane runs Fable at high
      effort; peer and spot coverage are raised with no sampling shortcut on flagged regions; the final checker audits
      the whole book rather than a scope; and a second independent Fable review of the flagged regions precedes the
      close.
    - **STANDARD TRACK.** Fable keeps its OW-6 roles (boss and final pre-close checker); the orchestrator decides within
      the owner-ruled strategy as before.


12. **OW-6c END-OF-CAMPAIGN RE-CHECK DECISION (owner directive, 2026-09-07 — campaign-level; blocks the campaign's completion, not a book's).**
    Owner words (verbatim): "after all books are dont fable will prompt me to see if it wants me to recheck all work all chain of thought for this project easpecailly the earlier books done before fable was upgraded to 5.1 and inlight of our process we are developing"
    - **THE PROMPT.** When the 66th book closes, the claude-fable-5-1 controlling agent presents the owner a decision
      packet on a whole-project re-check of all work and all captured reasoning. The campaign is not declared finished
      until the owner answers.
    - **PACKET SHAPE (the OW-6 escalation contract).** Fable's recommendation with its reason, plus every alternative
      with pros and cons - at minimum full re-check, early-books-only re-check, sampled re-check, **LANE TOP-UP**
      and no re-check - each with cost, what it would catch, and what it would leave uncaught.
    - **LANE TOP-UP IS A NAMED OPTION (added 2026-09-15 by OW-19).** Owner's own proposal: a book already reviewed
      once needs only the MISSING lanes, not a whole re-review. The packet costs it as such, and states for each
      book which of the two retrofit shapes it would be - RETROFIT-REDERIVE (the added lane never sees the shipped
      rows; COUNTS as a blind lane) or RETROFIT-AUDIT (the added lane reads them; does NOT count). See item 25.
    - **REMEDIATION STATUS TRAVELS WITH THE OPTIONS (added 2026-09-15 by OW-19).** The packet states, per book, how
      many findings the review it already had are still open, so the owner is not choosing between more review
      and no more review while earlier findings sit unworked.
    - **PER-BOOK CONTROL GAP.** The packet states, for each book, which controls were in force when it was produced and
      which were added later, so the owner sees the actual gap. The early books predate the Fable 5.1 upgrade and the
      current process.
    - **EVIDENCE PRESERVATION (immediate).** From this directive forward every book keeps a transcript manifest
      indexing each subagent's captured reasoning transcript and audit logs. Where an early book's transcripts were
      never captured, the packet says so plainly.


## Item 13 — OW-7 UNIVERSAL PER-ATTEMPT CAPTURE (owner directive 2026-09-07; answers boss ruling B3-2)

Binding from the first brief of the book after Lamentations. Not retroactive, and the gap is stated rather than
papered over.

- **THREE LAYERS, NEVER MERGED.** Layer A is runtime-captured actions, tool calls, results and file writes, and is
  NOT self-authored, which is why it is the only layer that can catch an agent concealing something. Layer B is the
  exposed thinking summaries the runtime happens to surface: sporadic, summary-level, never a full chain of thought.
  Layer C is the agent's own evidence note: self-authored, and labelled so wherever it appears. A close packet that
  presents these as one thing manufactures a chain of thought that does not exist and does not meet this item.
- **UNAVAILABLE IS A VALUE.** A layer that does not exist for an attempt is recorded as UNAVAILABLE with its reason.
  Never blank, never omitted, never filled from another layer.
- **IDENTITY AND LINEAGE.** Every attempt carries book, task, agent id, parent agent id, role, model ordered, model
  ACTUAL where a runtime record shows it (else UNAVAILABLE, never inferred), and a unique attempt id. A nested
  subagent's records belong to the CHILD and are never attributed to the parent. A retry is its own attempt record
  carrying `retry_of`; the original is never overwritten, including when it failed or was stopped.
- **ONE INDEX, NO CONTENT.** `SP/campaign/capture_index.v1.jsonl` links the records and never holds them.
- **REVIEWER BLINDNESS SURVIVES THE INDEX.** Collecting records does not authorize sharing them. A lane still under
  a blindness constraint is never given the index, another lane's records, or any conclusion drawn from them, before
  its own independent review has landed. The index is a permitted read for the orchestrator and for post-review
  lanes only: final checkers, transcript auditors, and the end-of-campaign re-check.

CLOSE EVIDENCE: the book's close receipt carries the capture-index check verdict and the three layer counts stated
separately. Contract: `SP/campaign/CAPTURE_CONTRACT.v3.md` (v2 and v1 retained beside it; **v3 supersedes v2 on
identity** - see item 14. The pointer here read `v1` after OW-8 amended the contract to v2 and was corrected
under OW-10 together with that identity change).


## Item 14 — OW-10 EXECUTION IDENTITY, CURE BINDING, CENSUS COVERAGE, PERMANENT PROMPT DUTIES (owner directive 2026-09-08)

Binding from the first brief of Ezekiel. Contract: `SP/campaign/CAPTURE_CONTRACT.v3.md`.

- **TWO IDENTIFIERS, BECAUSE THERE ARE TWO THINGS.** `attempt_id` is the **stable logical job** and is **never
  renamed**: the E-14 re-launch ladder keys off it (deliverable ABSENT → fresh agent under the SAME attempt_id,
  appending to the same deliverable), and that is what keeps the ladder idempotent. `execution_id` =
  `<attempt_id>#e<N>` identifies **one physical run**, with `execution_of`, `execution_ordinal` and
  `previous_execution_id`. Every fresh launch gets one. OW-7's "a retry is its own record; the original is never
  overwritten" attaches to the **execution**. **E-14 is amended, not overridden.**
- **`retry_of` IS A DIFFERENT RELATION AND IS UNCHANGED.** It names another **job** this one corrects. Re-running
  the same job is `previous_execution_id`. A close packet that conflates them fails this item.
- **HISTORY IS NOT REWRITTEN TO SATISFY THIS.** Execution ids are additive and derived deterministically from
  receipt order; historical `attempt_id`s stay verbatim; no in-flight record is renamed and no completed work is
  re-run or duplicated.
- **LAYERS ATTACH TO THE EXECUTION, NOT THE JOB.** Run 1 and run 2 had different agents doing different things.
  Where a manifest maps a transcript to a job and cannot say which run produced it, layer A is **UNAVAILABLE with
  the ambiguity named** — never handed to whichever run happened to be first.
- **A CURE IS NOT CURED BECAUSE ITS AUTHOR SAYS SO.** Verification results must be bound to the **exact resulting
  artifact**, plus the existing distinct-checker review. Three digests must agree: what was verified
  (`artifact_sha256_at_run`), what the claim pins (`artifact_sha256`), and what is on disk now. Refused: any
  verification with no machine result; any result whose `artifact_sha256_at_run` ≠ the shipped artifact; a
  `distinct_checker` naming the author's own attempt or execution; the bare words *passed / cured / verified*
  standing in for any of these. Enforced by `SP/campaign/_cure_verification.py`. This does **not** replace the
  distinct-checker second-generation sweep; it adds the artifact binding that review alone never provided.
- **COVERAGE IS COUNTED, NEVER REMEMBERED.** Transcript coverage is reported from
  `SP/campaign/_transcript_coverage_census.py` → `transcript_coverage_census.v1.json`, which counts `attempts`,
  `transcript_retained` and `observed` per book and **never adds them together**. A close packet stating coverage
  in prose without the census fails this item. **Producing the census is not authority to launch another audit.**
- **THE FIVE RESTART-PROMPT DUTIES ARE PERMANENT AND MECHANICALLY CHECKED.** Every restart prompt is (1) generated
  from current durable state and the latest authorized rules, never edited down from an older pasted prompt;
  (2) checked for stale instructions, contradictions, **retry-identity confusion**, and completed work wrongly
  listed as pending, and corrected without inventing authority; (3) saved to `RESUME_PROMPT_CURRENT.md`, read back,
  and mechanically verified from the saved bytes; (4) **printed in full in the chat** as the exact verified text;
  and (5) carries these same five duties to its own successor. **"Safe to clear" may not be said unless every
  required state and prompt save is verified**; on failure, preserve the work and report the specific blocker.

CLOSE EVIDENCE: the close receipt carries the capture-index `--check` verdict (execution-chain integrity included),
the `_cure_verification.py` verdict over every cure claim in the book, and the per-book census figures by number.

WHAT THIS ITEM DOES NOT AUTHORIZE: broader audits, runtime-capture changes (still the separate open owner decision
from OW-8(f)), or any weakening of a quality gate.


## Item 15 — OW-11 WRITE AUTHORITY, ONE-BOUNDARY CONTINUATION, COMBINED CEILING (owner directive 2026-09-10)

Binding on the Ezekiel and Daniel closes. Record: ERROR_PATTERN_LEDGER.v1.md addendum 2026-09-10 (OW-11), authorization_ref
`lowell_chat_2026-09-10_m8_opus_orchestration_ezek_dan`.

- **AUTHORITY IS SCOPED AND EXPIRES.** The owner explicitly authorized this Opus 5 orchestration, and the Fable, Sonnet
  and Opus agents it launches, to write M8_fable work for Ezekiel and then Daniel despite the registry's Fable-5-only rule.
  The exception covers Ezekiel and Daniel only and expires at Daniel's close. A close packet that relies on it for any
  other book FAILS this item.
- **SUBAGENTS NEVER WRITE INSIDE THE WORKTREE.** Subagents write deliverables outside the worktree and the authorized
  orchestrator lands them. Every Ezekiel and Daniel receipt names its landed output path; a subagent write found inside
  the worktree FAILS this item until it is disclosed and dispositioned.
- **ONE BOUNDARY.** At Ezekiel's close the run continues into Daniel; at Daniel's close the OW-9 hard stop applies. The
  Ezekiel close packet records the continuation and still carries the durability checkpoint and a verified slot. The
  Daniel close packet records the stop and the printed prompt.
- **CEILING.** One combined 15M subagent-token ceiling for Ezekiel plus Daniel, with an owner check-in before crossing it.
  Each close packet states the cumulative spend, counted from receipts and never estimated.
- **RESUME.** Before the first M8 write, read the active-worktree registry's owner and identity rule for the lane. A
  validator PASS is not authority.

## Item 15 amendment (2026-09-11) — CEILING, as the owner's budget answers set it

Record: ERROR_PATTERN_LEDGER.v1.md addendum OW-11-n. The CEILING bullet of item 15 is kept as history and is superseded:

- **CEILING (amended).** Ezekiel's subagent-token ceiling is 49,604,821 and Daniel has its own 25M ceiling, with an owner check-in before any launch that would cross either. Each close packet states the cumulative spend, counted from receipts and
  never estimated.

- **CEILING (amended again, owner answer 2026-09-14; ledger OW-15).** Ezekiel's subagent-token ceiling is 55,000,000 and Daniel has its own 25M ceiling, with an owner check-in before any launch that would cross either. The 49,604,821 bullet above is kept as history and is superseded. The number the scripts read is `SP\campaign\budget_ceilings.v1.json`; a script that hardcodes a ceiling is a defect (learning log L-0019). Each close packet states the cumulative spend, counted from receipts and never estimated.


## Item 16 — OW-12 BOOK-CLOSE PROJECT STATUS UPDATE (owner directive 2026-09-11)

Binding on every book close from Ezekiel on. Record: ERROR_PATTERN_LEDGER.v1.md addendum 2026-09-11 (OW-12).

- **THE UPDATE.** At every book close the owner gets a project status update: books closed of 66 and books left, the time and tokens the rest will likely take, and what that means in time on the owner's Max 20x plan, measured from receipts and labeled as estimates. At Ezekiel's close it is given before Daniel's Phase 0 opens.
- **NO INVENTED ALLOWANCE.** Plan limits are not a fixed published token count. Time on the plan is translated through the campaign's
  measured pace, and the update says so.
- **PACKET.** The close packet records the update's figures and the receipts they come from. A close without the update FAILS this item.


## Item 17 — OW-13 MODEL ROLES (owner directive 2026-09-11)

Binding on every book close from Ezekiel on. Record: ERROR_PATTERN_LEDGER.v1.md addendum 2026-09-11 (OW-13).

- **THE ROLES.** Opus 5 orchestrates; Opus 5 subagents do the substantive writing and research where the orchestrator judges they will do good work, and a Fable 5.1 execution checks that work; Sonnet 5 subagents take only bounded lower-level work and never work that should be Fable's; Fable 5.1 architects, rules, checks, takes the hardest work and adjudicates disagreements.
- **CHECK AT CLOSE.** The close packet lists every execution of the book by role and model ordered, from its receipts, and shows
  two things for executions ordered after 2026-09-11:
  - no claude-sonnet-5 execution took work that should be Fable's (rulings, gates, strategy, distinct checks, boss adjudication,
    final checks) or substantive authoring;
  - every claude-opus-5-authored output was read by a claude-fable-5-1 check.
  Work done under the earlier routing is listed, stands, and is not redone.
- **A close that cannot show it FAILS this item.**


## Item 18 — OW-14 ORCHESTRATION PLAYBOOK (owner directive 2026-09-11)

Binding on every book close from Ezekiel on. Record: ERROR_PATTERN_LEDGER.v1.md addendum 2026-09-11 (OW-14).

- **THE PLAYBOOK.** The orchestration method is captured for re-runs in the M8_fable orchestration playbook (ORCHESTRATION_PLAYBOOK.vN.md, the highest version current) with its append-only learning log and receipt-derived metrics; every wave landing, distinct check, controlling execution and book close adds its evidence of what worked, so the agent and subagent workflow can be found, recreated and improved.
- **CHECK AT CLOSE.** The close packet names three things:
  - the learning-log entries added for the book, at least one for every wave landing, distinct-check landing and
    controlling-execution landing;
  - the digest of the regenerated orchestration_metrics.v1.json;
  - the current playbook version, with a new version where the book's evidence changed a recommendation.
- **A close without them FAILS this item.**


## Item 19 — OW-16 QUALITY AND COMPLETION OVER BUDGET (owner directive 2026-09-15)

Binding on every book close from Ezekiel on. Record: ERROR_PATTERN_LEDGER.v1.md addendum OW-16.

- **THE OBJECTIVE.** Quality of the completed book, and completion of the 66, are what the campaign optimises for.
  Budget is a recorded limit, not a driver of scope.
- **CEILINGS STAND.** OW-15's figures and its pre-crossing owner check-in are unchanged. A close packet still states
  cumulative spend counted from receipts and never estimated.
- **CHECK AT CLOSE.** The close packet states, in one line, whether any decision in the book traded quality for tokens,
  and if so which and on whose authority. "None" is the expected answer and is a real answer.
- **A close that shows a quality gate narrowed for spend, without the owner's word, FAILS this item.**


## Item 20 - OW-17 SCHOLAR-FACING TRANSPARENCY RECORD (owner directive 2026-09-15)

Binding on every book close from Ezekiel on; the 25 already-closed books are retrofitted before the campaign closes.

- **THE RECORD EXISTS** for this book, written for a future scholar and free of campaign vocabulary, covering: what made
  the book difficult, every dispute, the evidence on each side, the resolution, and what remains open.
- **IT IS GENERATED** from the landed review packets, and its generator and checker are both in the tree, so any reader
  can regenerate it and get the same document.
- **THE CHECKER PASSES**: every landed packet represented, every high-severity finding present, every cross-lane
  disagreement surfaced, and nothing asserted that is not in a packet.
- **A FABLE EXECUTION AUDITED IT POST-FLIGHT** against the primary sources and returned fit_to_accept. A not-fit verdict
  BLOCKS the close.
- **IT IS STAGED FOR PUBLICATION** with the witnesses' licence and attribution terms stated. The push itself is recorded
  as the owner's act, with the authorisation referenced.
- **A close that cannot show all five FAILS this item.**


## Item 21 - OW-17 (a) CROSS-GENERATION CHUNKING-METHOD RECORD (owner directive 2026-09-15)

Binding on every BOOK close and on every CAMPAIGN close from Ezekiel on.

- **AT EVERY BOOK CLOSE**: `BIBLE_CHUNKING_METHOD.md` is updated with whatever this book taught, each new rule naming the
  generation and book that produced it and the evidence behind it, and each open method question this book could not
  settle is added or amended. A book close whose method record is byte-identical to the previous one must say in one
  line why this book taught nothing - "nothing new" is a real answer and an unexamined one is not.
- **AT CAMPAIGN CLOSE**: the next version is published, and it is named as the REQUIRED Phase-0 input for the following
  generation. A campaign that ends without handing it forward has not closed.
- **THE OPEN QUESTIONS TRAVEL.** The list of what the generation could not settle with the witnesses it had is part of
  the deliverable, not an appendix.
- **A FABLE EXECUTION CHECKED** that what the book learned reached the record, and that nothing in it is asserted
  without evidence. Not-fit blocks the close.
- **A close that shows an unchanged and unexplained method record FAILS this item.**


## Item 22 - OW-17 (b) DIFFICULTY / RISK / BLAST-RADIUS ATLAS (owner directive 2026-09-15)

Binding on every book close from Ezekiel on.

- **THE BOOK'S PASSAGES ARE IN THE ATLAS** with their measured components (was it contested between blind lanes, what
  severities landed on it, does the seam carry device evidence on both faces, is the question answerable from the
  witnesses at all) recorded SEPARATELY from any judged hardness or risk rating.
- **EVERY OPEN QUESTION CARRIES A BLAST-RADIUS ESTIMATE** with its dependency class named: one unit, several units, one
  book, or campaign-wide. A convention question is never filed as a single-unit question.
- **LINKAGES ARE HARVESTED FROM THE PACKETS**, including the cross-references reviewers write themselves, and no
  linkage asserts a similarity that no packet supports.
- **WHERE TWO LINKED PASSAGES WERE TREATED DIFFERENTLY**, the close states whether that is a real distinction or an
  inconsistency to fix. Silence is not an answer.
- **A FABLE EXECUTION CHECKED** the atlas for completeness against the packets and for unsupported linkage.
- **A close that files a convention question as a one-unit question, or that leaves a divergent treatment of two linked
  passages unremarked, FAILS this item.**


## Item 23 - OW-17 (c) METHOD-CHANGE PROPOSALS PROPOSED AND ADJUDICATED (owner directive 2026-09-15)

Binding on every book close from Ezekiel on.

- **A PROPOSER EXECUTION RAN** for this book, reading the book's own landed evidence rather than a summary of it, and
  its proposals are in `method_change_proposals.v1.jsonl`. "No proposals, and here is why" is an acceptable result; an
  absent proposer is not.
- **EVERY PROPOSAL FROM THIS BOOK IS ADJUDICATED**: ADOPT / REJECT / DEFER, with an independent
  NECESSARY / USEFUL / LOW-REWARD rating and reasons, by someone who is neither the proposer nor the orchestrator that
  ran the book.
- **ADOPTED PROPOSALS ARE CARRIED INTO A NEW METHOD VERSION**, and the version's change table says which proposal each
  change came from.
- **REJECTED AND DEFERRED PROPOSALS REMAIN IN THE LOG** with their reasons.
- **THE CLOSE REPORTS THE RATES**: how many proposed, adopted, rejected, deferred, and how many rated low-reward.
- **A close with unadjudicated proposals, or with no proposer execution at all, FAILS this item.**


## Item 24 - OW-18 NO IMPLIED PROVENANCE: EVERY CLAIM CARRIES ITS TRUE EVIDENCE TIER (owner directive 2026-09-15)

Binding on every book close from Ezekiel on, and on every generation of this campaign.

- **NO RECORD IMPLIES A PROVENANCE IT DOES NOT HAVE.** The test is not whether a false sentence was written, but
  whether a careful reader would draw a false conclusion from what was written and omitted. A record silent about a
  change in how it was produced asserts, by keeping the shape of its neighbours, that nothing changed.
- **EVERY SUBSTANTIVE CLAIM NAMES ITS TIER** and never a stronger one than is true: MEASURED, EXTRACTED,
  TRANSCRIBED, REPORTED, INFERRED, ASSUMED, UNAVAILABLE / UNKNOWN. UNAVAILABLE is a value, never a blank.
- **SEPARATE FACTS STAY SEPARATE.** Where two different things are being claimed - how a record was produced and
  whether it is still re-derivable, for instance - each carries its own tier and its own basis. Collapsing them
  produces a confident wrong label; M8 did exactly this once and the correction is recorded.
- **CORROBORATION DOES NOT UPGRADE A TIER.** A transcribed record whose digest is independently measured is still a
  transcribed record.
- **THE TIER IS ENFORCED BY A TOOL, NOT BY MEMORY.** The landing path requires an explicit capture carrier and
  MEASURES the claim: an EXTRACTED claim over an empty or absent source is REFUSED, not annotated. A tool that
  cannot represent the weaker tier is the defect and is fixed. Evidence for this book:
  `sp_durable/Ezek/_land_review_packet_ezek.py` (capture_tier gate, **18 selftest vectors GREEN**) and
  `sp_durable/Ezek/primaries_capture_provenance.v2.json`.
- **A DURABLE CARRIER THE AGENT WROTE ITSELF IS NOT A RUNTIME CAPTURE.** Three carriers are distinguished and
  never collapsed: `extracted_from_transcript` (carrier held by the RUNTIME - this is OW-7 Layer A); `extracted_from_authored_file`
  (the agent's own durable final-message file - re-readable, so the tier is EXTRACTED, but written BY the agent,
  so it is not tamper-evident against the agent and does NOT restore Layer A; it is a durable Layer C); and
  `transcribed_from_notification` (no durable carrier at all). The gate requires the words SELF-AUTHORED CARRIER
  in the record's own note for the second, and the durable copy is named for its true layer rather than filed as
  Layer A. A close in which a self-authored record is presented as a runtime capture FAILS this item.
- **THE BACK CATALOGUE IS STATED, NOT LEFT SILENT.** Where records were landed before the tier field existed, the
  book carries an index giving each one's tier by measurement, with its superseded version kept on disk so the
  correction is auditable.
- **CAPTURE DOES NOT DEPEND ON THE RUNTIME'S OWN TRANSCRIPTS.** Measured 2026-09-15: 29 of 30 agent transcripts for
  this book's landed reviews were already 0 bytes. Layer A is copied into the durable store at landing time and the
  copy is digested.
- **THE SCHOLAR-FACING RECORD CARRIES TIERS TOO**: a boundary warrant resting on a measured mark is not written in
  the same voice as one resting on a reviewer's reported reading.
- **A close in which any record implies a provenance it does not hold FAILS this item.**


## Item 25 - OW-19 LENS MULTIPLICITY: SINGLE-LANE REVIEW IS BANNED (owner directive 2026-09-15)

Binding immediately, on every book close and every generation.

Owner words (verbatim): "would a tri ban review be even better down the road? lets make sure if we havent
alertady alfuture chunkning ai consider either of these but do nto do singl review" / "did the earlier bookw in m8
only have single band review? is so maybe after we are done with allthe books we revisit them with doal or tripple
blind lanes vs single lane being no good likly" / "if we redo any that are single lane currently. we woudl only
need to do it one omre time to hig dual, or do a dual on them to hit tripple."

- **NO UNIT GROUP IS REVIEWED BY ONE LENS.** Two blind lanes are the floor for every book in every generation. Not
  waivable for a short, easy or late book, nor by a budget ceiling. The OW-6b STANDARD/HARD track governs coverage,
  scrutiny and who controls the cycle; it NEVER governs lens count.
- **THE PER-BOOK LENS COUNT AND ITS REASON ARE RECORDED** in the book strategy. A close with an unrecorded lens
  count FAILS this item, because a number nobody chose is a number inherited by habit.
- **A THIRD LANE COUNTS ONLY IF IT IS DECORRELATED.** The campaign's own canonical clause holds that
  Anthropic-family agreement is one correlated voice. A 2-1 split among same-family lanes is therefore NOT a
  majority verdict, and reporting it as one FAILS item 24 as well as this one. Decorrelation, in rising strength:
  different reading order and lens definition (weakest); a different EVIDENCE BASE, such as a versional/reception
  lane; a different MODEL FAMILY; a HUMAN lens (sample only).
- **A TARGETED THIRD LENS CARRIES DECOYS.** If a third lane is run only on conflict rows, it is given its rows
  without the selection reason and with decoy rows from the agreed class mixed in at a stated rate. Without the
  decoys the round is not blind and its agreement rate cannot be interpreted.
- **A RETROFIT NAMES ITS SHAPE.** RETROFIT-REDERIVE (added lane blind to the shipped rows) counts toward lens
  multiplicity; RETROFIT-AUDIT (added lane reads them) does not, and the book stays recorded as
  single-lane-plus-audit. Blindness is an information barrier, not a clock: a lane that runs later but never sees
  the shipped chunking is a genuine blind lane. A close that reports an audit as a second blind lane FAILS.
- **BOOKS REVIEWED ONCE ARE CALLED UNDER-LENSED, NOT DEFECTIVE.** Which they are is a measurement, and item 12's
  packet owes it per book.
- **A close in which any unit group was reviewed by a single lens, or in which a correlated agreement is reported
  as independent confirmation, FAILS this item.**

## Addendum 2026-09-16 - OW-20 (Ezekiel paused, Daniel Phase 0 opened)

- Ezekiel's close gate is NOT evaluated and NOT waived: Ezekiel is paused at REPAIR-2 step 2 and every item stays owed.
- Ordering: Ezekiel must pass its close gate BEFORE Daniel's close gate is evaluated, because OW-11's authority for
  both books expires at Daniel's close.
- Resume point: sp_durable/Ezek/EZEK_PAUSE_HANDOFF_REPAIR2.v1.md.

## Addendum 2026-09-16 - OW-21 (Ezekiel ceiling 65,000,000)

- The close packet states Ezekiel's spend against 65,000,000, read from SP/campaign/budget_ceilings.v1.json; the owner check-in before a crossing launch binds there.
- The census is reconciled against the runtime notification log before the close packet's budget statement (E-38).

## Addendum 2026-09-16 - OW-22 (Ezekiel ceiling 72,000,000, a hard line)

- The close packet states Ezekiel's spend against 72,000,000, read from SP/campaign/budget_ceilings.v1.json.
- The forecast is re-made from measured per-step actuals after step 7 and after #e16; a forecast above the ceiling is brought to the owner as a named scope cut, never as a further raise.

## Addendum 2026-09-23 - OW-27 (Ezekiel ceiling 86,400,000)

- The close packet states Ezekiel's spend against 86,400,000, read from SP/campaign/budget_ceilings.v1.json.
- Spend is measured from the executions' usage fields (E-54), not the completion notification's figure; the census is re-measured before any further launch, and a forecast above the ceiling is brought as a named scope cut.

## Addendum 2026-09-23 - OW-28 (old count; budgets tracked; Fable at the end)

- Each close packet states the book's spend in the notification unit against its ceiling, and the spend-unit measurement beside it. A spend above the ceiling is reported, not a blocking gate.
- A gate that requires a Fable model is recorded DEFERRED to the campaign-end Fable review, never MET.
- Each close carries a deferred-Fable review packet: every low and medium_low row, its sidecar and low_confidence_register entry, and the orchestrator's notes on lane splits, reservations and open questions.

## Addendum 2026-09-23 - OW-29 (orchestrator runs the close; no routine book-boundary stop; atlas feed on the validator's rule)

- `--close` is run by the orchestrator only after a dry run of the same arguments shows 0 unmet. A refusal is a stop to report.
- After each close: the book-close status report, checkpoint the carriers, compact, and continue with the next book. Stop only for owner decisions.
- The `--acf` option must meet the coverage validator's per-book feed rule, measured by the close tool itself: exactly the low/medium_low chunks, each mirroring span, confidence, review status, hold state and the review-packet state its hold implies.
- Known campaign-level gap (E-57): the full validator also needs `reviews/<book>/review_packets.jsonl`, which no close from Job on writes, so it fails for Job..Lam and will fail for Ezekiel. Report that run as it is; the fix is an owner decision.

## Addendum 2026-09-23 - OW-30 (held atlas rows resolved by Fable's standing precedent; Fable itself not called)

- At every book's close, each atlas row held by the final review wave (a STOP or GRADE_QUESTION item) is resolved by measurement against the final corpus, using the ledger's OW-30 precedent:
  - P1: a row defect measured absent or cured -> release.
  - P2: a class or campaign-wide question no row edit could discharge -> release, or drop_from_feed when the row is graded above medium_low. Its question goes to the book's Fable end packet.
  - P3: a row defect still measured present -> keep_held. The final corpus row carries final_deferred_review / deferred_human_or_external_ai, is re-versioned, and is re-checked by two blind delta lanes.
- Per hold, record the rule applied and the measurement. A hold that fits no rule, or fits one only by judgment, goes to the owner. It is not put to Fable without a new owner authorization (OW-30).
- The atlas feed then follows the corpus. A row is in the feed only if it is graded low or medium_low, and it is held exactly when its corpus row carries a hold.
