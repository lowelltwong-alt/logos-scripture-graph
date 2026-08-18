# M7 Sol Agent System and Graph-Evidence Design

**Evidence revision:** `scratch/t423-m7-sol@eaf31a940d3166b49c38ca26eb279392e0a3b25b`

This document explains how the M7 Sol whole-Bible candidate campaign was designed and
recorded: the subagent roles, book/form specialists, case-by-case review mesh, evidence
graph, validation, and limitations. It is a transparency and engineering record, not a
claim that M7 is released, correct in every case, or converged with M8.

## Current status and the honest headline

- Runtime profile: `sol_xhigh_frontier_marathon` on the `sol` agent surface.
- Scope: candidate-only literary/structural mapping for the canonical 66 books.
- Strategy coverage: the committed head contains one `book_strategy/<Book>.md` for all
  66 books.
- Quality state: `model_manifest.yaml` records 22/66 books through corrective re-review,
  with Ecclesiastes current and Job the latest completed book.
- Conflicting aggregate: `marathon_progress.yaml` says 66/66 candidate coverage. That
  means a complete candidate surface exists; it does not erase the 22/66 corrective
  quality state.
- Open evidence: the manifest derives 1,426 unresolved appeals across the 66-book
  candidate surface.
- Isolation: M7 was forbidden to read M1-M6 maps, comparison output, or T417 model layers
  before completion.
- Convergence: M7 and M8 have not been compared or converged. The owner has directed that
  this begin only after Fable and its subagents complete M8.

The corrective contract also marks publication forbidden. A later publication task must
reconcile that historical contract/status and issue an explicit candidate-release
manifest; pushing a branch does not promote its contents.

## What “Sol subagents” means

M7 used a role-separated mesh around one Sol model substrate. The roles were given
different evidence scopes, blind artifacts, attempt identifiers, and write permissions.
That separation is valuable for challenge generation and auditability, but it is not
cross-model independence.

The contract says the entire shared-model mesh counts as **one correlated model voice**.
Reviewer count is not authority. Cross-model or human evidence is required for later
convergence, and promotion remains human-gated.

Key execution limits:

- delegation depth: one;
- one accountable writer per book;
- reviewers read-only;
- distinct writer and checker identities;
- no overlapping writes;
- one ordinary primary domain specialist plus at most two evidence specialists;
- no forced consensus; unresolved evidence becomes a hold or appeal.

## Agent hierarchy

```text
owner/governance gates
  -> campaign controller and freshness/authority checks
     -> one book writer
        -> literary-form primary (blind)
        -> Hebrew/Aramaic/Greek primary (blind, evidence only)
        -> canonical-relation/retrieval premortem (blind, evidence only)
     -> peer cross-check
     -> writer response to every challenge
     -> evidence-dispute boss ruling
     -> append-only specialist appeals
     -> read-only post-resolution checker
     -> deterministic validators
     -> hash-bound book completion receipt written last
```

## Control and campaign roles

The display names are mnemonic identities only. The role contract explicitly says they
confer no spiritual, textual, theological, or decision authority.

| Control role | Display name | Engineering responsibility |
|---|---|---|
| Router | Bezalel | Select the smallest marker-evidenced specialist set; never route from book reputation alone. |
| Authority guardian | Esther | Enforce canonical scope, trust zones, evidence precedence, non-authorizations, and owner gates. |
| Family architect | Gamaliel | Maintain packet, schema, validation, and release contracts without changing domain authority. |
| Foreman | Nehemiah | Create non-overlapping assignments with one writer and a distinct checker. |
| Boundary synthesizer | Ezra | Combine cited observations into serious alternatives without approving one. |
| Anti-imputation checker | Nathan | Detect proof-texting, hidden theology, unsupported themes, and authority leakage. |
| Freshness sentinel | Haggai | Fail closed on missing, stale, circular, or hash-drifted knowledge references. |

| Campaign role | Display name | Engineering responsibility |
|---|---|---|
| Parent-unit worker | Ezra | Propose larger literary parents before any child-boundary review. |
| Child-necessity reviewer | Jethro | Default to no children and require an existing parent before subdivision. |
| Textual-witness specialist | Jeremiah | Record variant/source-tradition dependency without selecting a preferred reading. |
| Speaker/discourse specialist | John | Preserve alternatives and hold unresolved speaker-dependent boundaries. |
| Reviewed-gold custodian | Joshua | Compare against reviewed evidence without editing or promoting it. |
| Historical-model calibrator | Caleb | Normalize old maps as non-voting evidence; M1/M5 are known mechanical outliers. |
| Evidence-dispute boss | Gamaliel | Make one bounded candidate ruling after debate, without creating human authority. |
| Human-docket steward | Esther | Project mandatory human-review questions; exercise no decision authority. |

Three observation roles supplied exact structure, discourse context, and canonical
cross-witness evidence: Bezalel (text structure), John (discourse), and Priscilla
(quotations, parallels, and clear callbacks).

## Case-by-case corrective review mesh

For each decision or small passage cluster, the M7 corrective contract defined seven
working roles:

1. **Book writer** — authors the proposed span and passage-specific rationale.
2. **Original-language primary** — tests Hebrew, Aramaic, or Koine Greek form and
   translation pressure as evidence only.
3. **Literary-form primary** — identifies genre, child function, actual seam, and the
   strongest real rejected alternative.
4. **Canonical-relation premortem** — tests parent loss, retrieval danger, and internal
   canonical relations without making doctrine or canon decisions.
5. **Peer cross-checker** — challenges claims but cannot assign a verdict merely because
   of its role.
6. **Boss/adjudicator** — answers divergences decision by decision, preserves
   counterevidence, and cannot force consensus.
7. **Post-resolution checker** — re-reads the current hash-bound artifacts without
   editing them.

At least two primaries had to be blind to each other's review artifacts. Ordinary
attempts could cover no more than eight decisions, identities had to remain separated,
and every formal challenge needed an author response and a decision-local ruling.
Appeals were append-only; a losing reviewer could preserve dissent after the boss ruled.

## Specialist packs and literary forms

Routing uses observed markers and the smallest sufficient specialist set. A book's genre
is only a prior; it can never be the sole routing reason.

| Primary pack | Display identity | Routed form IDs / triggers |
|---|---|---|
| Prose/discourse | Samuel | `prose_paragraph`, `prose_section_heading`; paragraph and discourse continuity |
| Narrative scene | Samuel | `narrative_scene`; scene, location, participant, speaker, or episode closure |
| Genealogy/list | Zerubbabel | `genealogy_or_list`; list formula, genealogy, marked subunit |
| Law/covenant | Moses | `law_statute`; legal, covenant, procedure, or statute unit |
| Psalms/poetry | Asaph | line/colon, stanza, acrostic, or whole-psalm forms |
| Wisdom/dialogue | Job | `wisdom_saying_cluster`, `speaker_dialogue`; saying clusters, turns, parallelism |
| Prophecy | Isaiah | `prophetic_oracle`, `vision_report`; speech formula, audience/oracle/vision shift |
| Gospel | Matthew | `gospel_pericope`, `parable_or_discourse`; framed scenes, parables, discourse continuity |
| Acts | Barnabas | `acts_speech_or_episode`; speech frame, episode, participant/location shift |
| Epistle | Paul | `epistle_argument`, `epistle_opening_closing`; argument, epistolary function, doxology/benediction |
| Apocalyptic | Daniel | `apocalyptic_cycle`; vision cycle, symbolic scene, oracle, or voice shift |

The three formal evidence-only specialist packs were Huldah for Hebrew structural
evidence, Apollos for Greek syntax/discourse, and Priscilla for
quotations/parallels/intertexts. Jeremiah and John were campaign roles used for
textual-witness pressure and speaker ambiguity; Luke was a campaign evidence identity
for verified historical context. Campaign identity aliases also used Solomon for wisdom
and Phoebe for epistle openings/closings. These categories are recorded separately and
must not be counted as additional specialist packs. None of these roles could choose
doctrine, translation, preferred reading, source tradition, or a boundary by itself.

## Expected routing across all 66 book strategies

Every one of the following books has a committed strategy file. The table shows expected
primary routes; it is not an observed all-book assignment inventory. Actual assignments
were selected at the passage/decision level from markers and risks, so mixed-form books
could activate several packs. The executed assignments remain in each book's per-decision
review artifacts.

| Book group | Books with strategy records | Normal primary routes and common specialist/campaign evidence roles |
|---|---|---|
| Torah | Gen, Exod, Lev, Num, Deut | Moses for law/covenant; Samuel for narrative; Zerubbabel for lists/genealogies; Huldah for Hebrew evidence. |
| Historical books | Josh, Judg, Ruth, 1Sam, 2Sam, 1Kgs, 2Kgs, 1Chr, 2Chr, Ezra, Neh, Esth | Samuel for scenes; Zerubbabel for registers/genealogies; Huldah, Jeremiah, or Priscilla only when triggered. |
| Poetry and wisdom | Job, Ps, Prov, Eccl, Song | Job for wisdom/dialogue; Asaph for poetry/stanza/acrostic/psalm; Samuel for prose frames; Huldah for Hebrew pressure. |
| Major prophets | Isa, Jer, Lam, Ezek, Dan | Isaiah for oracle/vision; Daniel for apocalyptic cycles; Samuel for narrative frames; Huldah and Jeremiah as evidence-only lanes. |
| Minor prophets | Hos, Joel, Amos, Obad, Jonah, Mic, Nah, Hab, Zeph, Hag, Zech, Mal | Isaiah for oracle/vision; Samuel for narrative episodes such as Jonah; Daniel for apocalyptic cycles when evidenced; Hebrew/textual/intertext lanes as triggered. |
| Gospels | Matt, Mark, Luke, John | Matthew for pericopes/parables/discourse; John for unresolved speaker/discourse; Apollos for Greek; Priscilla for explicit parallels/callbacks; Jeremiah for variants. |
| Acts | Acts | Barnabas for speeches/episodes, with Apollos, Priscilla, Jeremiah, or John only when evidence triggers them. |
| Pauline letters | Rom, 1Cor, 2Cor, Gal, Eph, Phil, Col, 1Thess, 2Thess, 1Tim, 2Tim, Titus, Phlm | Paul for argument; Phoebe identity for opening/closing function; Apollos for Greek structure; Priscilla/Jeremiah for explicit relations or variant pressure. |
| General letters | Heb, Jas, 1Pet, 2Pet, 1John, 2John, 3John, Jude | Paul pack as the generic epistle-argument engine and Phoebe opening/closing identity; Greek, speaker, intertext, and textual evidence lanes by trigger. The display name does not assert authorship. |
| Apocalypse | Rev | Daniel for apocalyptic cycles; Isaiah for prophetic/oracle forms; John for voice/speaker ambiguity; Apollos, Priscilla, and Jeremiah as evidence-only lanes. |

This route design is deliberately polymorphic. For example, Job activates prose frames,
speaker dialogue, wisdom poetry, Hebrew difficulty, disputed attribution, and canonical
retrieval premortem. Matthew activates genealogy/list, narrative scene, gospel
pericope, parable/discourse, Greek/textual pressure, speaker changes, and explicit
canonical/Synoptic relation review. The strategy files spell out those seams before the
writer creates or revises chunks.

## Evidence-graph engineering

M7 did not merely emit a flat chunk list. Its artifacts form a typed, hash-bound evidence
graph:

```text
book strategy
  -> candidate decision/chunk
     -> frozen chunk hash
     -> exact source/evidence refs
     -> blind primary reviews
        -> challenges
        -> author responses
        -> boss rulings
        -> append-only appeals
     -> parent-hydration relations
     -> candidate canonical relations
     -> post-resolution checks
     -> book completion receipt
```

`reviews/<Book>/decision_relations.jsonl` records typed connections. Job records
children, mandatory parent surfaces, a passage-specific rationale, and
`mandatory_hydration: true`; each row also says `boundary_authority: false` and
`non_authorizing: true`. Matthew relation rows connect decisions to related passages but
explicitly deny boundary symmetry, harmonization, preferred-witness selection,
dependency claims, or theological authority.

That is graph engineering for provenance and review, not a published Scripture knowledge
graph. Candidate relations cannot silently become asserted graph truth, retrieval truth,
or symmetric edges. The relationship layer exists to prevent isolated chunks from losing
their speech, scene, dialogue cycle, discourse, or book-level parent.

## Concrete Job receipt

The figures below come from the committed
`receipts/Job_literary_completion_owner_ruling_v1.json`, which supersedes the earlier
`receipts/Job_completion_v2.json` for this owner-ruling summary. It demonstrates the
intended depth for a corrected book:

- 93 candidate chunks covering 1,070/1,070 verses in exact order;
- 87 accepted decisions and 6 held decisions;
- 279 primary-review rows with 279 unique primary attempt IDs;
- 465 workflow attempt IDs total;
- 80 scoped challenge claims, all answered and ruled;
- 3 active post-ruling specialist appeals;
- 162 decision-relation records;
- source, literary, and boss postchecks recorded as pass or pass-with-holds;
- hashes for strategy, chunks, review packets, evidence, relations, rulings, appeals,
  postchecks, and preserved failure history.

These numbers are evidence about one book's recorded process, not proof that all 66 books
currently have the same corrective depth.

## Quality and stop gates

A book could be marked correctively complete only after:

- exact ordered verse coverage and positive contiguous indices;
- passage-specific forms, seams, rationales, and rejected alternatives;
- no pervasive templates, arithmetic-midpoint substitutes, generic form buckets, or
  batch-reused reviewer identities;
- all challenges answered, dissent preserved, and hold states synchronized;
- chunk and review hashes bound into the final artifacts;
- a role-separated adversarial postcheck;
- a completion receipt written after validation.

Security/privacy exposure, dependency hash drift, write conflicts, failed gold standards,
or inconclusive validation were stop conditions. Research autonomy never granted
reviewed-gold, output, canon, graph, retrieval, vector, preferred-reading, or theology
authority.

## Primary evidence paths on the M7 branch

- `model_manifest.yaml` — current corrective status, baseline pins, isolation, and open
  appeal count.
- `marathon_progress.yaml` — aggregate 66-book candidate coverage; must be read alongside
  the corrective manifest.
- `campaign_prompt.md` and `campaign.json` — objective, budgets, phases, stops, and replay
  contract.
- `corrective_rereview_contract.v1.yaml` — role separation, blind review, evidence,
  anti-batch, hash, hold, and completion rules.
- `review_contract.yaml` — provider-neutral review roles and independence disclosure.
- `book_strategy/<Book>.md` — all 66 case-specific literary/evidence plans.
- `book_chunks/<Book>/chunks.jsonl` — candidate decisions.
- `reviews/<Book>/` — blind proposals, review packets, relation graph, challenges,
  responses, rulings, appeals, red-team checks, and postchecks.
- `receipts/<Book>...json` — hash-bound completion evidence.
- `config/agents/families/scripture-first-biblical-chunking/` — portable family roles,
  routing policy, workflow, prompt pack, schemas, and runtime adapter.

Any future public M7 release should link these exact files at an immutable Git commit,
state which books meet the corrective standard, and keep the unresolved appeals and
failed-attempt archives visible.
