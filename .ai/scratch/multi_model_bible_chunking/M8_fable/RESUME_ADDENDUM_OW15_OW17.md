# RESUME ADDENDUM — OW-15, OW-16, OW-17(a)(b)(c)

**Read this WITH `RESUME_PROMPT_CURRENT.md`, and read this one FIRST.**

## Why this file exists

`RESUME_PROMPT_CURRENT.md` (sha256 `565ac990f1c86c26…`) names the canonical active rules as the ledger addenda
"through 2026-09-11 … OW-13 and OW-14" and "close gate items 1-18". Four later owner directives and five later gate
items are therefore invisible to a session that trusts that pointer. The directives themselves are durable in
`ERROR_PATTERN_LEDGER.v1.md`; only the pointer was stale. The generator
(`sp_durable/orchestrator_scratch/_gen_resume_prompt.py`) has been corrected, so the next regeneration folds all of
this into the prompt itself and this addendum becomes redundant. Until then, this file is authoritative for the delta.

## The delta a resumed session MUST pick up

Read these in `ERROR_PATTERN_LEDGER.v1.md` (verbatim owner words are recorded there) and
`CAMPAIGN_CLOSE_GATE.v1.md`:

| Directive | Gate item | What it binds |
|---|---|---|
| **OW-15** (2026-09-14) | — | Ezekiel's ceiling 55,000,000; Daniel's 25,000,000, each its own. Read from `SP/campaign/budget_ceilings.v1.json`, never hardcoded. Owner check-in before any launch that would cross one. |
| **OW-16** (2026-09-15) | 19 | Quality and completion are the objective. Budget is a recorded limit, not a driver: spend never narrows a review, drops a lane, shortens a wave or picks a weaker model. Token efficiency = not wasting effort. Lowers no control. |
| **OW-17** (2026-09-15) | 20 | Per-book scholar-facing transparency record: what was contested, the evidence each side, how resolved, what is open. GENERATED from the landed packets. No campaign vocabulary. |
| **OW-17 (a)** | 21 | Cross-generation `BIBLE_CHUNKING_METHOD` record. **Re-version, never overwrite**, with a §0 change table. Updated at EVERY BOOK close. Carries the open method questions forward. Required Phase-0 input for the next generation. |
| **OW-17 (b)** | 22 | Difficulty / risk / **blast-radius** atlas. MEASURED, DEPENDENCY and JUDGED kept separate. Blast radius ≠ difficulty; settle widest-radius conventions first. Harvest cross-passage linkages from reviewers' uncertainty fields; compare treatments (same = precedent, different = distinction or inconsistency). |
| **OW-17 (c)** | 23 | One proposer subagent per book close, reading that book's own evidence and not the orchestrator's summary. It PROPOSES and never edits. Log to `method_change_proposals.v1.jsonl`, brief at `METHOD_PROPOSER_BRIEF.md`. A checking execution that is neither proposer nor orchestrator rules ADOPT/REJECT/DEFER and rates NECESSARY/USEFUL/LOW-REWARD. Rejected and deferred proposals are KEPT with reasons. Adopt rate and low-reward rate measure whether our own rule-making earns its cost. |

## Three gates, subagent-enforced

- **PRE-FLIGHT** — method record read; the per-book record's scaffolding exists and its checker passes; a checking
  execution reviews the record's design once; the atlas is consulted so the widest-radius questions are scheduled
  first. A wave that would produce evidence the record cannot represent does not launch.
- **MID-FLIGHT** — the checker runs at EVERY landing. If the record has fallen behind the packets, the wave STOPS
  until it catches up. Method changes and linkages are captured when found, never reconstructed at close.
- **POST-FLIGHT** — a checking execution audits the finished records against the PRIMARY SOURCES. **NOT-FIT blocks the
  book close.**

## Two facts that change how you plan

1. **Generations run CONCURRENTLY.** M9 was roughly 15 books into its own campaign while M8 was on book 26, neither
   aware of the other's conventions. Reconciliation is TWO-WAY and comes before mass review; keep a divergence
   register. A convention difference between generations affects every unit both have closed — the largest blast
   radius available. The M9 handoff prompt was delivered 2026-09-15; its section 2 lists the six conventions to
   reconcile (mark direction, translation-layout gating, apparatus read-forms, dual references in numbering zones, the
   finished-artefact re-check, both-face evidence).
2. **Publication is the owner's act.** OW-11 grants no commit, push or merge authority and the registry forbids lane
   mutation by other agents. Records are authored, checked and STAGED. The owner names the repository and path and
   authorises the push. OSHB and WEB attribution terms travel with any published quotation.

## Current method-record versions

| File | sha256 | Note |
|---|---|---|
| `BIBLE_CHUNKING_METHOD.v5.md` | `64c75f0c820da3dc738c990d1d517ff76d3be8fd5d6b393c1e35c361bcfa973a` | **current** — 718 lines; OW-19 §19 lens multiplicity, §10 write-early, §18 three carriers |
| `BIBLE_CHUNKING_METHOD.v4.md` | `2ed884c66cd64310c59abd521ec3e1888a0288df7730841666beaa85cebbda8b` | kept unchanged; OW-18 §18 provenance tiers |
| `BIBLE_CHUNKING_METHOD.v3.md` | `52657dc47bc6e975ff632a0dac6dc22564c79a85b86cab7a258cbaac02a4d382` | kept unchanged (was marked current until 2026-09-15; superseded twice that day) |
| `BIBLE_CHUNKING_METHOD.v2.md` | `82fcfbe245ac675ab0158d2767d50e9dc43b3ad81505167993d8d34f78a41ed3` | kept unchanged |
| `BIBLE_CHUNKING_METHOD.v1.md` | `6c9948faf67d7741558fb565e863376b41d60b05269e995173f116230fa8236a` | kept unchanged |

Re-read the newest version rather than trusting these digests if they differ from disk — the record is updated at
every book close by design, and a digest that has moved means it was updated, not corrupted.
