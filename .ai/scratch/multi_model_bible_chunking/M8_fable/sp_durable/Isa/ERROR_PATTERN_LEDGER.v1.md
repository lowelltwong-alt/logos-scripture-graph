# ERROR PATTERN LEDGER — subagent-caught defect classes, root causes, and re-scan guidance

- Schema: `m8_error_pattern_ledger.v1` (machine rows: `error_pattern_ledger.v1.jsonl` beside this file)
- Authority: owner directive, Lowell Wong in chat 2026-08-27 — "log and track the types of
  errors you catch with these sub agents … their root cause … look for patterns and know
  where to maybe look again for more passes … done repo wide by any agent using this repo."
- Status: candidate-only operational evidence. Nothing here re-opens an adjudicated row on
  its own; a re-scan flag is a REVIEW TRIGGER, not a verdict.
- Scope note: this ledger lives in the M8_fable subtree because that is the writing lane's
  allowlist. It is DESIGNED for repo-wide adoption; the owner's commit can promote a pointer
  to `.ai/control/` / `AI_FRONT_DOOR.md` (outside this lane's write scope — flagged, not done).
- Update law (any agent, any lane): when a defect a machine or reviewer catches is NOT an
  instance of a class below, append a class (M-row + JSONL row) in your own lane's ledger
  copy or this one if allowlisted; when it IS an instance, increment nothing — cite the
  class id in your own report. Never delete a class; supersede with a note.

## FORWARD-APPLICATION LAW (owner directive, 2026-08-27 — "big issues get run on future books, always")

The owner clears chat between sessions, so THIS FILE is the carrier — not any prompt's
hardcoded list, not chat, not one agent's memory. Binding on every future book:

1. Every class's `cure`/`rescan` text that names a forward behavior (a brief clause, a
   gate, a review lane, a tool promotion, a sweep) BINDS every subsequent book
   automatically from the moment the class is recorded.
2. At every book's Phase 0 / brief-authoring step, the session RE-DERIVES the applicable
   forward behaviors BY READING THIS LEDGER — never by copying the previous resume
   prompt's list. The prompt's list is a convenience snapshot; the ledger is the truth.
   A behavior found in the ledger but missing from the briefs/gates is a defect
   (E-18-class) to fix before launching agents.
3. Book-close checklist: (a) new classes found this book appended here (md + jsonl);
   (b) the next resume prompt's carried-laws snapshot regenerated FROM the ledger;
   (c) CAMPAIGN_CLOSE_GATE.v1.md items still block marathon completion.
4. Any agent in this repo may append classes; none may delete or weaken one — supersede
   with a note, owner approval to retire.

## How to read a class

`id | name — root cause → detector → cure → RE-SCAN (where more passes may find more) | machine-checkable?`

## Content-defect classes

- **E-01 | nfd_degraded_hebrew_splice** — writer carried pointed Hebrew through its own draft
  instead of splicing from the staged verse map; NFD-degraded quotes. Seen: 23 runs / 13 rows,
  ALL one writer (Isa P05). Root cause: single agent's method + the writer-facing suite
  treating `fixed>0` as non-hard (GREEN with a non-zero fixed count). Detector:
  `normalize_hebrew_in_json.py` dry-run + citation_sweep NFD counter; both primaries caught it
  independently. Cure: deterministic `--write` re-splice + byte-tier collate re-proof (one
  pass; boss Isa B-7). RE-SCAN: run the normalize dry-run over every COMPLETED book's
  chunks.jsonl once (cheap, deterministic); read the `fixed` COUNT, not the status. Owner
  item: promote nfd_degraded to hard in the writer-facing suite for future books.
  Machine-checkable: YES (tool exists).
- **E-02 | whole_chapter_cap_miss** — whole-chapter spans shipped above the medium_low
  confidence cap. Seen: 12 rows across 6 Isa parts; 4 of 12 found by NO packet or peer —
  only the boss's deterministic sweep. Root cause: a campaign rule enforced by reviewer
  attention with NO validator gate (the suite had no cap check). Detector: span-vs-
  verse-inventory sweep (`_cap_sweep.py`, built Isa session 5; reproduces the boss set
  exactly). Cure: one-pass confidence/flag/disclosure repair (boss Isa B-6). RE-SCAN:
  run the cap sweep over every completed book's corpus (cheap); generally, list every
  campaign rule that is prose-only and machine-checkable and give each a gate (durability
  law: validator > gate > contract > chat). Machine-checkable: YES.
- **E-03 | reviewer_ledger_prose_error** — factual errors inside REVIEW/RULING text itself:
  a peer remedy naming the wrong Hebrew token (Isa peer_05 P05-011: כל mis-named as the
  shamar-root noun; true token משמרתי at MT 21:8), ruling-text mis-citations caught at
  author time (Isa P07-001 remnant-root token + 1 more), boss-docket enumeration shortfalls
  (cap class filed 6 actual 12; NFD rows filed 11 actual 13). Root cause: reviewer prose
  written by carry-forward/inspection rather than by sweep; citations not byte-verified at
  writing time. Detector: author-phase byte re-verification (collate + word-index read)
  under the trust-but-verify-installs law. Cure: authors install the VERIFIED fact and file
  a discrepancy report; never propagate, never silently correct without reporting.
  RE-SCAN: HIGH-YIELD — peer/boss remedies containing Hebrew citations that were executed
  in earlier books BEFORE this law hardened; sample per book. The Isa spot wave adds a
  ruling-text mis-citation lens. Machine-checkable: PARTIAL (collate can verify quoted
  runs in ledger prose; enumerations need sweeps).
- **E-04 | byte_valid_wrong_token_splice** — an agent splices a token that collates
  byte-perfect against the cited verse but is the WRONG WORD for the claim (word-index
  slips; semantically wrong, mechanically green). Seen: 3 self-caught at author time
  (Isa a03, a05, a06); zero known shipped. Root cause: index arithmetic on token dumps;
  invisible to collate-vs-cited-verse. Detector: content read-back of every splice in its
  sentence (a03's manual read-through), citation_sweep occasionally. Cure: mandatory
  read-back; surgical exact-substring edits instead of retyping. RE-SCAN: warrant-
  substitution lane of any spot wave; no completed-book sweep exists (tooling gap —
  candidate: gloss/claim vs spliced-token semantic check is NOT mechanizable; keep the
  human lane). Machine-checkable: NO (this is why the review lane exists).
- **E-05 | tier_overclaim_and_count_object_blur** — "byte-identical"/"verbatim" where the
  truth is accent-stripped/skeleton/none; digits controlled by substring objects presented
  as word counts (שאר 22-verse trap, נס 44-verse, eternity-phrase 41-verse); load-bearing
  sweeps blending distinct objects. Seen: pervasive pre-cure (primaries HIGH finds c25_OL
  P15-004/P16-001; boss B-1 teudah; dozens of author re-tierings). Root cause: recurrence
  claims written from memory of a match, not from collate output; substring vs word-bound
  conflation. Detector: collate re-derivation + universals checker (digit-adjacency).
  Cure: tier-label every recurrence with its count object named (campaign law, Eccl B-4).
  RE-SCAN: HIGH-YIELD — grep completed books' prose for byte-identical/verbatim claims
  and re-collate each (semi-mechanizable). Machine-checkable: PARTIAL.
- **E-06 | register_bleed_workflow_language** — workflow/administrative language in row
  prose: part-range references ("the last verse of this part's assigned range"),
  governance-rule names, tool filenames, cross-row field references, erratum narration.
  Seen: multiple rows across Isa parts, cured this wave. Root cause: writers narrating
  the process instead of the text. Detector: register sweep (grep classes) + peers.
  Cure: strike and re-argue from bytes. RE-SCAN: the register-sweep pattern list is
  grep-able over completed books (cheap). Machine-checkable: YES (pattern list).
- **E-07 | mark_position_and_kq_overclaim** — parashah/paseq/K-Q claims beyond the
  inventory: position claims where the witness gives count-only, "opens" vs
  after-the-verse, slicing K/Q verses without checking pmarks first, PE/SAMEKH
  conflation, rank talk ("more emphatic"). Detector: check_marks + citation_sweep +
  boss B-4. Cure: restate to the sourceable fact; pmarks-before-slicing law. RE-SCAN:
  grep mark-adjacent verbs in completed Prophets/Writings books. Machine-checkable: YES.
- **E-08 | quote_gloss_parity_drift** — English gloss extent ≠ spliced Hebrew extent
  (cut-off verbs, over-long glosses). Detector: check_web_quotes + peers. Cure: re-cut
  gloss to the splice. RE-SCAN: candidate future Tier-0 (extent comparison is partially
  mechanizable). Machine-checkable: PARTIAL.
- **E-09 | oss_taxonomy_collision** — signal keys colliding with checker windows
  (parashah.* in oss vs the 120-char mark-proximity window, Isa p09) or compound keys;
  peer remedies conflicting with the taxonomy bar (Isa P04-007 — resolved brief-over-peer).
  Cure: parashah disclosure in prose only; dotted single-class keys. RE-SCAN: grep oss
  keys in completed books for barred/compound classes. Machine-checkable: YES.
- **E-10 | sibling_confidence_incoherence** — adjacent rows carrying confidences their
  shared-seam evidence cannot jointly support. Detector: peers; cross-row contradiction
  lane. Cure: reconcile with a stated reason. RE-SCAN: spot-wave cross-row lane.
  Machine-checkable: NO.

## Process/tooling classes

- **E-11 | orchestrator_fixture_finals_normalization** — hand-written needles/fixtures
  typed with final letters (ך ם ן ף ץ) against the finals-normalized index; 3+ Isa
  occurrences, ALL caught by hard assertions. Cure: normalize needles; never hand-type.
  Machine-checkable: YES (assertions).
- **E-12 | heuristic_fp_classes** — checker heuristics flagging mandated language
  (universals "only/count-only"), English matched by letter-name arms ("small vessel"),
  window collisions. NOT defects. Cure: whitelist patches (i1-class) + declared-FP triage
  queues; never auto-suppress, always disposition. Machine-checkable: n/a (meta).
- **E-13 | api_filter_misfire_kill** — provider safety classifier false-positives on
  biblical-Hebrew research content (`[bio]` tag), forbidding session continuation.
  3 lifetime (Isa s1, s5×2). Cure: NEVER resume-in-place; FRESH relaunch with a
  research-context preamble (3/3 success). The preamble MITIGATES but does not immunize
  (2 recurrences with it carried). Track per-session rate. Machine-checkable: n/a
  (operational).
- **E-14 | connection_lost_stall_kill** — connection-lost / stream-stall / orchestrator-
  exit, incl. same-minute multi-agent clusters (up to 5 agents). 19 of Isa's 22 lifetime
  kills; ZERO work lost ever. Cure: verify deliverable path; ABSENT → resume-in-place
  SAME attempt id; PRESENT → census then continue. BONUS FINDING: resume-completed
  self-checks catch real defects (3 confirmed instances) — treat every resume as a free
  re-verification pass. Machine-checkable: n/a (operational).

## Standing re-scan queue (candidate passes, cheap-first; owner may schedule)

1. normalize dry-run + cap sweep + register grep + oss-key grep over the 22 completed
   books' chunks.jsonl (E-01/E-02/E-06/E-09; all deterministic, one session).
2. byte-claim re-collation sweep over completed books (E-05; semi-mechanized).
3. reviewer-ledger Hebrew-citation verification sample per completed book (E-03).
4. mark-position grep over Prophets/Writings books (E-07).

## Addendum 2026-08-27 (Isa rev round) — three classes added by the spot wave

- **E-15 | checker_coverage_gap_unclosed_web_quote** — check_web_quotes matches only
  CLOSED curly pairs, so unclosed/uncurly WEB quotes sit outside Tier-0 coverage, and
  Hebrew-inside-curly pairs corrupt pairing enough to mask even well-formed English
  quotes (4 masked defects surfaced the instant a deterministic pass fixed the
  interleaving). Cure: binding repairs now; unclosed-quote detector for future books
  (owner item). Machine-checkable: YES once the detector exists.
- **E-16 | universals_dampener_tier_vocab_hole** — the universals checker suppresses
  flags when a tier word and a ref share the sentence; a tier label proves the QUOTE,
  not the EXCLUSIVITY — one false "sole discriminator" shipped GREEN through exactly
  this hole. Candidate patch: never dampen only/sole/unique/never (owner item).
- **E-17 | second_generation_repair_defect** — repair waves install fresh defects while
  curing ordered ones; Isa's checklist lanes filed ~19 such findings and the B-8 sample
  dated ~22.6% of its defects to the repair wave. The r3 second-generation checklist is
  hereby VINDICATED as a mandatory post-author lane, every book.
- **B-8 RECORD (Isa)** — LF-SUPPORT audit, sample n=31 of frame 155 (20.0%): defect-any
  19/31 = 61.3%; LF-attributable ~12/31 = 38.7% (incl. 1 high: tier-4 punctuation
  driving a boundary, certified by the support's own evidence); second-generation
  ~7/31 = 22.6%. Consequence: the LF-support audit lane runs BY DEFAULT in future
  books; no ledger sentence may call LF supports verified for books lacking the lane.

## Root-cause pattern (the durability law, restated operationally)

Every content class above shipped past a model reviewer and was caught by either a
DETERMINISTIC SWEEP or a BYTE RE-VERIFICATION lane. Rules that live only in prose get
enumerated short every time (E-01 fixed-count, E-02 four sleeper rows, E-03 docket
shortfalls). The fix that endures is always: name the object, give it a tool, read the
tool's COUNT not its status, and keep one human/model lane for the classes tools cannot
see (E-04, E-10).
