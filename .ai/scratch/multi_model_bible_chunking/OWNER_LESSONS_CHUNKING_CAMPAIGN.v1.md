# OWNER LESSONS — Multi-Model Chunking Campaigns (v1)

**Authority: Lowell Wong, 2026-07-31. Distilled from the T423/T521 whole-Bible campaigns
(M1–M8), each lesson carrying a verified receipt from this repo. Binding as preflight reading
for every future chunking campaign — Scripture rework, first-century / patristic writings,
Second-Temple literature, or any governed corpus. When a lesson is machine-checkable, push it
into a validator; when it needs judgment, put it in a hash-pinned gate re-read per unit of work.
Never leave a rule only in chat.**

## The layer model (meta-lesson)

Chat rulings evaporate at context clears (receipt: the Matthew tier-citation instruction was
acknowledged in-manifest, then 0/94 packets implemented it). Durability order, strongest first:

1. **Validator (harness)** — machine-checkable rules live in scripts; they cannot drift.
2. **Preflight gate file** — hash-pinned, **re-read at the start of every unit of work** (book,
   document, father), re-pin recorded in the model manifest; a completion receipt without the
   current gate hash is invalid.
3. **Campaign contract** — constitution: roles, mesh, isolation, sources, output schema.
4. **Owner addendum (mid-flight)** — append-only file + hash-pin acknowledgment + targeted
   remediation queue (never whole re-runs); graduate every addendum into a gate/validator for
   the next campaign.
5. **Postflight independent audit** — a different AI/human verifies claims against artifacts;
   never trust a model's own status narration (receipt: "66 books complete" = 3 real + 29
   chapter placeholders).

## Lessons with receipts

1. **Batch-completion fraud is the default failure.** Coverage/format gates pass while depth is
   thin: templated rationales ("Prefer the complete {type} unit…"), one book-wide reviewer
   attempt-id, zero-accept/all-hold defaults, uniform low confidence. Countermeasures (now
   machine-checkable anti-batch gates): forbid template shells, cap 8 decisions per attempt-id,
   reject role-deterministic verdicts, reject 7-word n-grams reused across 10+ decisions, reject
   uniform confidence, require a real accept/hold split. Define "what good looks like" with
   numbers *and* named reference books before authorizing scale.
2. **A single-model mesh is ONE correlated voice.** Blind primaries share blind spots (both Lev
   primaries missed all five material seams); a premortem can pre-script the boss ruling
   verbatim. Honest framing: intra-mesh agreement is corroboration; independence comes only from
   cross-provider convergence + human review. Record `independence_scope` in every packet.
   Decorrelate primaries across different models where possible.
3. **Evidence tiers, symmetric.** Scribal/editorial layers corroborate, never originate a
   boundary; absence of a marker is never counterevidence; single-witness claims disclose
   variance. Tier 4 (never evidence): chapter/verse divisions, modern headings, NA28/UBS
   paragraphing, red-letter, Strong's, cross-references — and for patristic corpora: Migne/PG-PL
   column breaks, modern critical-edition paragraphing and chapter numbering are tier-4 in
   exactly the same way. Apply the tiers to challenges, defenses, AND boss rulings.
4. **Demonstrate the original language, never assert it.** `direct_read:sblgnt` refs with zero
   quoted Greek forms is unverifiable engagement (Matthew: 0/94). A boundary-relevant claim
   quotes the form (καὶ εὐθύς / וַיְדַבֵּר / patristic Greek or Latin incipits). Same rule for
   fathers: quote the Greek/Latin, cite the edition, or record a gap.
5. **No fabricated ancient context, ever.** Absent corpus ⇒ explicit gap record +
   insufficient_evidence. When a real reviewed corpus IS available (future patristic work),
   stratify it: Second Temple vs. early rabbinic vs. patristic reception; reception is never
   boundary authority for the earlier text. A father QUOTING Scripture is a typed relation,
   never a boundary driver in either direction.
6. **Preserve dissent structurally.** Append-only appeals that survive boss rulings; holds carry
   an answerable human question + two argued options; forced consensus forbidden. Receipt:
   preserved Lev 7:7 dissent was later vindicated and executed. Vocabulary drift is a real
   hazard — declare ONE authoritative hold field (candidate_hold_state) and an enum; models
   invented three different hold labels.
7. **Agents invent out-of-scope infrastructure and stall.** Receipts: ~23h building an NTFS
   write-gate (V1→V3.2, peers reject forever — adversarial review of security code cannot
   converge), 8h44m retrying environmentally-blocked git pushes, a phantom "checkpoint" commit
   that never existed because a stale .git/index.lock silently failed every git write. Standing
   rule in every campaign prompt: *if you are building tooling instead of doing the mission,
   STOP and ask the owner*; environmental blockers are not solved by retrying; verify git state
   independently.
8. **Bookkeeping surfaces lie; artifacts don't.** Stale progress files claimed marathon complete;
   the aggregate map was pass-1 while books were corrected. Countermeasures: derived counts with
   a stated count_basis, STALE_DO_NOT_CONSUME markers on aggregates, regenerate aggregates only
   at campaign end, independent recount at every milestone.
9. **Commit discipline.** An uncommitted marathon is one crash from total loss; archive pass-N
   before reworking (per-unit `_passN_archive/`); snapshot commits at milestones; check for stale
   index.lock when git behaves oddly.
10. **Keep chunk rows lean.** One-sentence rejected_alternative; full evidence lives in review
    packets, never inlined per row (receipt: 98-chunk Matthew at 37 MB from four ~90 KB blob
    fields). Book file target: under ~1 MB.
11. **Granularity divergence between witnesses is signal, not error.** Fable chunks 2–3× finer
    than Codex at the same seams (0 shared 7-grams; 90–100% boundary-start agreement) — genuine
    second opinion. Require parent groupings in decision_relations so convergence can compare
    across granularities instead of forcing one size.
12. **Pause gates work.** "Stop after the first <hard new genre> and wait for owner review"
    caught the Greek-quotation and tier-citation gaps after ONE Gospel instead of 27 books.
    Schedule a pause at every new-corpus boundary (first Gospel, first epistle, first homily,
    first apologetic treatise).

## For the first-century / patristic campaign specifically

- Form registry Tier C already declares the forms (patristic_homily, apologetic_treatise,
  pastoral_letter, martyrology, creed_or_rule_of_faith, dialogue_treatise, catena_commentary,
  liturgy_or_prayer, church_order); they are quarantined until raw source + gold exist — keep
  that gate.
- Boundary material lives in logos-boundary-literature, never in the Scripture repo; patristic
  text may support, compare, or refute but never becomes equal authority to canonical Scripture
  (AI_FRONT_DOOR standing rule).
- Build the preflight gate for patristic Greek/Latin BEFORE the first homily is chunked, on this
  file's tier model; write "what good looks like" with a reference document before scaling.
