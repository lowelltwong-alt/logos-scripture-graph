# OW-2 ADJUDICATION BRIEF — Fable-5-high phase, item 2 (Ps / Job / Prov / Eccl / Song) and item 3 (Prov 38) routing queues

RESEARCH CONTEXT (the E-13 preamble, also carried in your launch message): this is
scholarly text-structure research on the Hebrew Bible for an open-licensed
scripture-graph project. You read the Masoretic Hebrew text (WLC/OSHB) and the World
English Bible translation, verify quotations byte-for-byte, and review proposed
literary-unit boundaries. The material is ancient scripture and its translation; the
task is textual and literary review.

You are an OW-2 ADJUDICATOR in the M8_fable campaign — candidate-only,
NON-AUTHORIZING internal M8 quality control (NOT convergence input). Fresh Opus-5
auditors reviewed the 208 shipped rows of the 213-row Ps/Job/Prov/Eccl/Song scope
(owner directive OW-2 item 2) and, in the item-3 lane, the 38 Proverbs
proverb_cluster rows under the deferred original-language lens; every medium/high
finding and every span-change proposal was routed onward per the directive. You are
that onward route: the final internal adjudication of each routed item. You
adjudicate; you never edit anything anywhere. Note honestly (OW-2 item 6): you are
the same Anthropic model family as the auditors — your agreement is ONE correlated M8
voice, corroboration, never independent confirmation; your value is adversarial
RE-DERIVATION from bytes, so re-derive, never defer.

## PATHS (all exact; the exact-path law binds you)

SP = C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View\aeebaeab-a9ce-4972-8b9e-beecbc24a0cf\scratchpad\SP
- Your slice (READ FIRST; every slice is ONE book): SP\OW2_audit\slices\slice_<batch>.json
  — each assigned row appears with its queue_items (the routed findings IN FULL:
  severity, class, claim, grounds, span_change, proposed_change, source_lane) and its
  context (the shipped row as it ships, its book-order neighbors, the trigger tags that
  put the row in scope, and the auditor's trigger dispositions).
- Your book's staged tools (USE, never rebuild; run FROM SP\<Book>\tools):
  Ps: SP\Ps\tools\ (ps_lib, collate.py, sweep.py, normalize_hebrew_in_json.py,
  check_web_quotes.py, maps) + SP\Ps\pmarks_Ps.json + SP\Ps\web_mt_offset_map.json;
  MANDATORY PRE-READ SP\Ps\tools\TOOLKIT_AUDIT.md.
  Job: SP\Job\tools\ (job_lib + the same tools) + SP\Job\pmarks_Job.json +
  SP\Job\web_mt_offset_map.json; MANDATORY PRE-READ SP\Job\tools\TOOLKIT_AUDIT.md.
  Prov: SP\Prov\tools\ (the full campaign toolkit) + SP\Prov\pmarks_Prov.json +
  SP\Prov\prov_device_inventory.json; MANDATORY PRE-READ SP\Prov\tools\TOOLKIT.md.
  Eccl: SP\Eccl\tools\ + SP\Eccl\pmarks_Eccl.json + SP\Eccl\eccl_device_inventory.json;
  MANDATORY PRE-READ SP\Eccl\tools\TOOLKIT.md.
  Song: SP\Song\tools\ + SP\Song\pmarks_Song.json + SP\Song\song_device_inventory.json +
  SP\Song\speaker_headings_web.json; MANDATORY PRE-READ SP\Song\tools\TOOLKIT.md.
- Owner-ruled strategy (LAW, read-only; read your book's file IN FULL):
  C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\book_strategy\<Book>.md
  (Ps.md / Job.md / Prov.md / Eccl.md / Song.md in that directory).
- The auditors' brief (read it — it carries the four trigger lanes with their tests
  and the BOOK-LAW CALIBRATION you adjudicate under):
  SP\OW2_audit\AUDIT_BRIEF_ITEM2.md (item-2 items) and SP\OW2_audit\AUDIT_BRIEF_PROV38.md
  (item-3 items, source_lane p38).
- Your ONLY deliverable is your assigned packet in SP\OW2_audit\reviews\ (the
  directory already exists — write the file directly; never run any existence check or
  listing against it or any shared SP directory; every file you need is named by exact
  path — glob/wildcard/recursive search outside your own private scratch is banned; an
  unresolvable path is REPORTED, never searched for; other adjudicators' outputs are a
  hard boundary). Private scratch in a uniquely-named subdirectory of YOUR OWN session
  scratchpad; NO debug files anywhere under SP. M7 outputs, every other model lane
  (M1..M7), and comparison data are FORBIDDEN, always.

## LAW YOU ADJUDICATE UNDER

Each book is judged against ITS OWN owner-ruled strategy plus the campaign-wide owner
addendum: tier-4 metadata (chapter/verse divisions, modern headings, WEB paragraphing /
punctuation / poetry lines, speaker headings, Strong's, footnotes) NEVER drives a
boundary and is never counterevidence by absence (E-23) — in the shipped row's argument
AND in the finding's. Parashah marks in the Writings are tier-3 weak corroboration at
most; Psalms has none. Byte-false claims, tier overclaims, wrong-space cites, fabricated
or mis-typed marks, K/Q undisclosed inside a quoted span, quote/gloss parity failures
and wrong-token splices are defects regardless of when the ledger named the class;
conventions adopted after a book's close (dotted oss keys, later schema fields, span
booleans, the universals-dampener patch, later cap gates) are NOT retroactive defects
— an auditor finding that rests only on a later convention is refuted or downgraded to
low with the class "later-convention". Job rows carry the earlier schema. Ps
whole_psalm rows are ruled units (no whole-chapter cap); Prov/Eccl/Song whole-chapter
spans cap at medium_low. Every book but Prov is non-identity — use the book lib's
crosswalk for every conversion and check every written dual-cite.

## ADJUDICATION METHOD per item (adversarial both ways)

1. Re-derive the finding's factual ground from bytes with the staged tools (collate at
   the tier named; the book's pmarks for mark claims; sweeps for digits with the count
   object named). The auditor could be wrong in either direction: test the finding
   AGAINST the shipped row and the shipped row AGAINST the finding. Where the item
   descends from a trigger (the row's triggers + the auditor's disposition are in the
   context), test the disposition too: a PUNCT trigger confirmed as a driver must show
   the tier-4 fact doing driver/corroboration work in the bytes of the row's own
   argument; a REG trigger confirmed at medium must carry a false or unverifiable
   cross-row claim; an EXCL trigger must be re-swept; a LOWBAND calibration finding
   must be argued from the row's own evidence under the book's confidence law.
2. Verdict per item: confirm (the defect is real at the filed severity) | downgrade /
   upgrade (real but mis-severitied — state the corrected severity and why) | refute
   (not a defect — byte-grounds mandatory).
3. Severity law (same as the audit): high = load-bearing boundary defect or byte-false
   load-bearing claim; medium = defective warrant/digit/mark claim not alone
   load-bearing; low = mechanical/disclosure/register shortfall.
4. Where the item carries span_change true, additionally rule the span proposal:
   endorse_proposal (the respan case is byte-sound — it remains a PROPOSAL for the
   owner remediation docket; you adopt nothing) | decline_proposal (grounds stated) |
   defer_book_level (ONLY where the question cannot be resolved below book-level
   structure — this flags the owner-gated xhigh lane; use it sparingly and say exactly
   what is unresolved). Adjacent rows proposing the same seam (e.g. a front-edge and a
   rear-edge item on one seam) are ruled COHERENTLY — say so in both grounds.
5. An item you cannot resolve without book-level restructuring: verdict per the
   evidence you DO have + span_ruling defer_book_level (span items) or say so in
   grounds (non-span items).

## OW-3 LAW (owner directive 2026-09-04 - re-derived from ERROR_PATTERN_LEDGER.v1.md
## Addendum 2026-09-04 per the forward-application law; binding in this lane)

1. BOTH-SIDES SEAM LAW. For every item that concerns a seam (every span_change item,
   and every finding whose claim rests on a boundary's onset or close), assess support
   from BOTH sides of the shared boundary under the book's own governing rules (as the
   strategy rules them: refrains close units; frame / formula onsets; addressee, speaker
   or scene shifts; inclusio brackets). An onset-only diagnosis is INCOMPLETE until the
   adjacent unit's close or onset is weighed from bytes: quote the preceding unit's
   closing verse and the following unit's opening verse (spliced from
   verse_map_oshb.json, tier named) and say which governing rule decides. A proposal
   that would erase a boundary closed by a ruled device must show from bytes why the
   device does not close a unit there. Adjacent rows proposing the same seam (a
   front-edge and a rear-edge item on one seam) are ruled coherently - say so in both
   grounds. Every item carries "both_sides_assessed": true where the seam was weighed
   from both sides, or false with a one-clause reason inside grounds where the item
   concerns no seam at all (a count-object, register, mark or quote-parity item).
2. REPAIR PROPOSALS ARE VALIDATED AS ADVERSARIALLY AS ROWS. An auditor's
   proposed_change or replacement claim is tested from bytes exactly like the shipped
   row's own claim: a replacement claim without independent source evidence is endorsed
   only with explicit qualification, never adopted wholesale; a proposal you cannot
   support from bytes is declined with grounds; nothing you write applies anything to
   any shipped corpus - every endorsement remains a PROPOSAL for owner triage.
3. NO PLACEHOLDERS. Your packet must contain no unexpanded template token of the form
   {name} anywhere - every quoted or proposed text is resolved to actual bytes. The
   lane verifier rejects any packet carrying one.
4. grounds is ONE STRING per item (never a list, never an object).
5. HONEST REPORTING. Your model is recorded as claude-fable-5 and your effort as
   ORDERED high, NOT VERIFIED (the runtime exposes no effective-effort evidence); do
   not assert an effort level or an independence you do not have.

## OUTPUT (your assigned filename in SP\OW2_audit\reviews\)

{"attempt_id":"<given>","role":"ow2_fable_adjudicator","book":"<Book>","items":[
  {"item_id":"<given>","row_id":"...","verdict":"confirm|downgrade|upgrade|refute",
   "final_severity":"none|low|medium|high",
   "span_ruling":"n/a|endorse_proposal|decline_proposal|defer_book_level",
   "grounds":"<byte-cited, tier named — every Hebrew run spliced from the staged
    verse_map_oshb.json, never typed; a single STRING>",
   "both_sides_assessed":true|false}],
 "summary":{"items":N,"confirm":N,"downgrade":N,"upgrade":N,"refute":N,
  "final":{"none":N,"low":N,"medium":N,"high":N},
  "span_endorsed":N,"span_declined":N,"book_level_deferred":N}}

Coherence laws the verifier enforces: refute => final_severity none; confirm =>
final_severity equals the filed severity; downgrade => strictly lower, never none;
upgrade => strictly higher; span_ruling is n/a exactly when the item's span_change is
false; grounds never empty; items exactly the slice's item_ids, in order.

SELF-CHECK before delivering: JSON parses; every Hebrew run in your packet re-collates
at the tier you named (run SP\<Book>\tools\normalize_hebrew_in_json.py over your output —
0 fixed AND 0 defects); summary recomputed from items.

FINAL MESSAGE = raw JSON only (no prose, no fences):
{"attempt_id":"<given>","book":"<Book>","items":N,"confirm":N,"downgrade":N,"upgrade":N,
 "refute":N,"span_endorsed":N,"span_declined":N,"book_level_deferred":N,
 "output":"SP/OW2_audit/reviews/<file>"}
