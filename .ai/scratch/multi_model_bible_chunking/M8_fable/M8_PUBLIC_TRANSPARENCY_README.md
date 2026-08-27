# M8_fable — Public Transparency Checkpoint

> **STATUS: INCOMPLETE — CANDIDATE-ONLY RESEARCH OUTPUT.**
> This is a mid-campaign transparency snapshot of one model lane's in-progress
> work. It is published so the method can be inspected while it is still
> unfinished.

## What this is NOT

Read this section before reading anything else in this directory.

- **NOT complete.** 22 of 66 books. The campaign is `in_progress`; the current
  book (`Isa`) is **mid-cycle** — its writer wave has landed but it has not been
  assembled, reviewed, or closed, and it has no chunk file or completion receipt.
- **NOT M7/M8 convergence.** No cross-model convergence has been run. Nothing
  here has been compared against the M7_sol lane or any other lane. Convergence
  (T521) is a separate, later, gated step that has not begun.
- **NOT reviewed gold.** Chunks carry `review_status: candidate_review_complete`.
  That means *this lane's internal review mesh finished its pass* — not that a
  human, an editor, or any external body ratified the result.
- **NOT canonical Scripture.** Nothing here defines, replaces, re-versifies, or
  re-canonizes Scripture. The chunk boundaries are research hypotheses about
  literary units.
- **NOT theological authority.** No doctrinal, confessional, or interpretive
  claim here carries any authority. Boundary rationales cite literary and
  scribal evidence, not theological conclusions.
- **NOT a promotion path.** Records are machine-labeled `non_authorizing: true`
  and `candidate_only: true`. Presence in this checkpoint grants no downstream
  promotion into any canonical graph, atlas, or index. The atlas feed carries
  `atlas_promotion_authority: none`.

## What this is

One provider lane (`M8_fable`) of a multi-model whole-Bible literary-chunking
study. The lane proposes chunk boundaries over the Hebrew Bible, records *why*
each boundary was drawn, records the strongest alternative it rejected, and
preserves its own low-confidence and disagreement material rather than
discarding it.

The point of publishing an unfinished lane is that the **reasoning trail and the
preserved disagreements** are the research object — not the chunk list.

## Progress at this checkpoint

| | |
|---|---|
| Books completed | **22 / 66** |
| Current book (mid-cycle, not closed) | `Isa` |
| Campaign status | `in_progress` |
| Candidate chunks | 3,722 |
| Verses covered | 17,655 (exact ordered coverage, all 22 books) |
| Review packets retained | 2,353 |
| Superseded decisions retained | 35 |
| Appeals recorded | 0 |
| Low-confidence register rows | 253 |
| Frontier escalation queue rows | 253 |
| Atlas candidate feed rows | 253 |

Completed books: Gen, Exod, Lev, Num, Deut, Josh, Judg, Ruth, 1Sam, 2Sam, 1Kgs,
2Kgs, 1Chr, 2Chr, Ezra, Neh, Esth, Job, Ps, Prov, Eccl, Song.

In progress, not complete: Isa (writer wave landed, 225 draft rows across 18
parts; assembly, review, and close all still pending).

Remaining: 44 books, including the entire New Testament, which is additionally
gated behind `OWNER_GATE_NT_GREEK_PREFLIGHT.v1.md`.

## Layout

| Path | Contents |
|---|---|
| `marathon_progress.yaml` | Governed progress record (source of the 22/66 count) |
| `model_manifest.yaml` | Lane manifest: mesh revision, routing, isolation, non-authorizations |
| `book_chunks/<Book>/chunks.jsonl` | Candidate chunk rows with boundary rationale + rejected alternative |
| `whole_bible_chunk_map.jsonl` | Flat map of all 3,722 candidate chunks |
| `book_strategy/<Book>.md` | Per-book strategy written before chunking |
| `reviews/<Book>/` | Review packets, decision relations, appeal ledger, superseded decisions |
| `receipts/<Book>_completion.json` | Per-book close receipt with hash pins and audit counters |
| `checks/` | Replay and validation scripts (see below) |
| `sp_durable/<Book>/` | Full working substrate for Ps, Prov, Eccl, Song, and in-progress Isa |
| `low_confidence_register.jsonl` | Preserved low-confidence decisions |
| `frontier_escalation_queue.jsonl` | Preserved escalations |
| `layer_decision_log.jsonl` | Layer-weighting decisions |
| `corrective_rereview_contract.v1.yaml` | The review contract the mesh binds to |
| `continuation_receipt.yaml`, `OWNER_CHECKPOINT_*.md` | Governance receipts |
| `SOURCE_TEXT_ATTRIBUTION.md`, `LICENSE-CC-BY-4.0.txt` | Source-text licensing |
| `m8_public_release_manifest.yaml` | Machine-readable manifest for this checkpoint |

## Agent-mesh engineering

The lane is an orchestrated subagent mesh (`model_profile:
fable_5_orchestrated_subagent_mesh`), currently at mesh revision `m8-mesh-r3`.
Its governing rules, recorded in `model_manifest.yaml`, include:

- a fixed escalation ladder (`deterministic → haiku → sonnet → opus → fable →
  human`) with at most 3 escalation hops per decision;
- `higher_tier_is_not_automatically_correct: true`;
- `decorrelation_rule: two_blind_primaries_on_different_models_where_possible`;
- per-attempt routing recorded on every decision;
- ultra-effort attempts requiring named human approval each time.

**Intra-mesh agreement is not independent evidence.** All subagents are
Anthropic-family models. As `model_manifest.yaml` states: agreement inside
M8_fable is corroboration, never cross-provider evidence.

## Preserved disagreement

This lane is designed not to hide its weak points. Retained deliberately:

- **253 low-confidence register rows** — decisions the lane made but does not
  stand behind strongly, each with `why_low_confidence` and
  `possible_downstream_risk`.
- **35 superseded decisions** — earlier boundary calls that were overturned,
  kept alongside their replacements rather than deleted.
- **`strongest_rejected_alternative`** on chunk rows — the best case *against*
  the boundary that was chosen.
- **Hold states and conflict rows**, including `hold_for_convergence` rows that
  are explicitly unresolved pending a convergence step that has not happened.
- **A recorded method failure.** The Job receipt records
  `haiku r1 monolithic REJECTED (batch degradation)` — a batching approach that
  degraded and had to be re-sliced. It is kept in the receipt rather than
  scrubbed.

## Reproducing the validation

From the repository root:

```
python .ai/scratch/multi_model_bible_chunking/M8_fable/checks/validate_exact_book_coverage.py --book Eccl
python .ai/scratch/multi_model_bible_chunking/M8_fable/checks/validate_book_review_coverage.py --book Ezra
```

At this checkpoint:

- `validate_exact_book_coverage.py` — **22 / 22 pass**.
- `validate_book_review_coverage.py` — **17 pass, 5 error** (Job, Ps, Prov,
  Eccl, Song). See "Known gaps".

## Known gaps in this checkpoint

Stated plainly rather than omitted:

1. **Job, Ps, Prov, Eccl, and Song have no `reviews/<Book>/review_packets.jsonl`.**
   Those books were closed under mesh revision `m8-mesh-r3`, whose review
   substrate lives under `sp_durable/` (Ps, Prov, Eccl, Song) or survives only as
   a SHA-256 pin in the completion receipt (Job). `validate_book_review_coverage.py`
   therefore errors for those five books. This is a **retention and layout gap**,
   not a coverage failure: exact ordered verse coverage still passes for all
   five.
2. **`sp_durable/` covers only Ps, Prov, Eccl, Song, and Isa.** Earlier books'
   working substrate was not retained at this depth.
3. **Mixed mesh revisions.** Books through 2Chr closed under `m8-mesh-r2`; Ezra
   onward under `m8-mesh-r3`. Method is not uniform across the 22 books.
4. **Some working files record absolute local workstation paths** (e.g. in
   `model_manifest.yaml` and `sp_durable/**` briefs). These are
   development-environment paths only. No credentials, tokens, keys, or personal
   contact data are present anywhere in this lane.
5. **Only the Hebrew Bible so far.** No New Testament work exists; the Greek
   preflight gate has not been satisfied.
6. **Isa is an unfinished book checkpointed for durability.** Its 225 draft
   writer rows under `sp_durable/Isa/` are pre-assembly, pre-review working
   output. They are not candidate chunks, are not in the chunk map, and must not
   be read as an Isaiah result.

## Source texts and licensing

Two open-licensed source texts are used, and for some books partially
redistributed. Full detail, including the CC BY 4.0 indication-of-modification
notice, is in **[`SOURCE_TEXT_ATTRIBUTION.md`](SOURCE_TEXT_ATTRIBUTION.md)**.

- **OSHB — Open Scriptures Hebrew Bible**, licensed **CC BY 4.0**. Attribution:
  Open Scriptures Hebrew Bible Project; text based on the Westminster Leningrad
  Codex. Full license text: [`LICENSE-CC-BY-4.0.txt`](LICENSE-CC-BY-4.0.txt).
- **WEB — World English Bible Classic**, public domain. "World English Bible" is
  a trademark of eBible.org; modified extracts here are not presented as the
  World English Bible.

No restricted-license translation (NIV, ESV, NASB, NRSV, NKJV, CSB, HCSB, NLT,
LEB, NET) is quoted or redistributed anywhere in this lane.

These licenses cover the **source text**. They do not make this lane's research
output authoritative. The upstream OSHB source manifest itself records
`authorizes_chunk_boundaries: false` and `authorizes_reviewed_gold: false`.

## Governance

This lane operates under an owner-protected workspace lifecycle and has **no**
canon-output authority. `model_manifest.yaml` records the standing
non-authorizations: `canon_chunk_output`,
`read_other_model_maps_before_complete`, and `realtime_cross_model_compare`.

Publishing this checkpoint is a transparency act. It changes none of those
non-authorizations, and it is not a convergence, merge, or promotion event.
