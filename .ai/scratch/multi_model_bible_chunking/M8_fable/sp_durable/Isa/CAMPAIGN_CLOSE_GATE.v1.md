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

## Carry law

Every session's printed resume prompt from Jeremiah onward carries one sentence pointing
at this file (pattern: "CAMPAIGN-CLOSE GATE standing: CAMPAIGN_CLOSE_GATE.v1.md blocks
marathon completion behind the retro LF-support audit of the 22 pre-Isa books + the
ledger re-scan queue — carry this sentence in every future resume prompt"). A session
that notices the sentence missing restores it from this file and records the lapse as
an E-18-class instance.
